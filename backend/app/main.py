import os
import secrets
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import engine, Base
from app.routers import examples, auth, users
from app.utils.auth import set_secret_key

# 환경 변수 로드
load_dotenv()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# JWT SECRET_KEY 설정: 환경 변수 우선, 없으면 자동 생성
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(48)
    print("[WARNING] SECRET_KEY not set in .env. Using auto-generated key (will change on restart).")
    print(f"[INFO] Generated SECRET_KEY: {SECRET_KEY[:10]}...")
else:
    print("[INFO] SECRET_KEY loaded from .env")

set_secret_key(SECRET_KEY)

app = FastAPI(title="Module 5 API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(examples.router)
app.include_router(auth.router)
app.include_router(users.router)


# ============================================
# 전역 예외 핸들러
# ============================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """HTTP 예외 핸들러 (401, 404, 403 등)"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Pydantic 검증 에러 핸들러 (422)"""
    details = []
    for error in exc.errors():
        details.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "입력값 검증에 실패했습니다",
            "details": details,
            "status_code": 422
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """일반 예외 핸들러 (500)"""
    # 개발 환경에서는 상세 에러 출력
    import traceback
    print(f"[ERROR] Unhandled exception: {exc}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "서버 내부 오류가 발생했습니다",
            "status_code": 500
        }
    )


# ============================================
# 엔드포인트
# ============================================

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "FastAPI 서버가 정상 작동 중입니다."}
