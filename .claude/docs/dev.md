# 개발 문서 (Development Guide)

> 최종 업데이트: 2026-02-10
> 버전: 1.0.0

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [기술 스택](#기술-스택)
3. [주요 기능](#주요-기능)
4. [프로젝트 구조](#프로젝트-구조)
5. [설치 및 실행](#설치-및-실행)
6. [API 문서](#api-문서)
7. [인증 시스템](#인증-시스템)
8. [에러 처리](#에러-처리)
9. [테스트](#테스트)
10. [배포 가이드](#배포-가이드)

---

## 프로젝트 개요

JWT 기반 인증 시스템을 갖춘 풀스택 웹 애플리케이션입니다.

**주요 특징**:
- 🔐 JWT 기반 인증/인가
- 🎨 Toast 알림 시스템
- ⚠️ 전역 예외 처리
- 🧪 자동화된 테스트 (87% 커버리지)
- 📦 프로덕션 준비 완료

---

## 기술 스택

### 백엔드
- **프레임워크**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0+
- **데이터베이스**: SQLite (개발), PostgreSQL (프로덕션 권장)
- **인증**: JWT (python-jose)
- **비밀번호 해싱**: SHA-256 + salt
- **테스트**: pytest (42개 테스트, 87% 커버리지)

### 프론트엔드
- **프레임워크**: Next.js 14 (App Router)
- **언어**: TypeScript
- **스타일링**: Tailwind CSS
- **상태 관리**: React Context API
- **알림**: 커스텀 Toast 시스템

---

## 주요 기능

### 1. 인증 시스템
- ✅ 회원가입 (이메일, 사용자명, 비밀번호)
- ✅ 로그인 (JWT 토큰 발급)
- ✅ 로그아웃 (클라이언트 토큰 삭제)
- ✅ 프로필 조회 및 수정
- ✅ Protected Route (인증 필요 페이지)

### 2. 보안
- 🔒 SHA-256 + salt 비밀번호 해싱
- 🔑 환경 변수 기반 SECRET_KEY 관리
- 🛡️ JWT 토큰 만료 (기본 30분)
- 🚫 CORS 설정 (localhost:3000 허용)

### 3. 사용자 경험
- 🎨 Toast 알림 (성공/에러/정보/경고)
- 🎭 자동 사라지는 알림 (3초)
- 🌊 슬라이드 인 애니메이션
- ⚡ 일관된 에러 메시지

### 4. 개발자 경험
- 🧪 자동화된 테스트 (pytest)
- 📊 코드 커버리지 87%
- 🔍 전역 예외 핸들러
- 📖 Swagger UI 문서

---

## 프로젝트 구조

```
module_4/
├── backend/
│   ├── app/
│   │   ├── dependencies/
│   │   │   └── auth.py              # 인증 의존성 (get_current_user)
│   │   ├── models/
│   │   │   ├── user.py              # User 모델
│   │   │   └── example.py           # Example 모델
│   │   ├── routers/
│   │   │   ├── auth.py              # 인증 API (회원가입, 로그인)
│   │   │   ├── users.py             # 사용자 API (프로필)
│   │   │   └── examples.py          # 예제 API
│   │   ├── schemas/
│   │   │   ├── user.py              # User 스키마
│   │   │   ├── error.py             # 에러 스키마
│   │   │   └── example.py           # Example 스키마
│   │   ├── utils/
│   │   │   ├── auth.py              # JWT 유틸리티
│   │   │   └── exceptions.py        # 커스텀 예외
│   │   ├── database.py              # DB 설정
│   │   └── main.py                  # FastAPI 앱
│   ├── tests/
│   │   ├── conftest.py              # pytest 픽스처
│   │   ├── test_auth.py             # 인증 테스트 (11개)
│   │   ├── test_users.py            # 사용자 테스트 (13개)
│   │   ├── test_error_handlers.py   # 예외 핸들러 테스트 (14개)
│   │   └── test_health.py           # Health Check 테스트 (6개)
│   ├── .env                         # 환경 변수 (SECRET_KEY)
│   ├── .env.example                 # 환경 변수 템플릿
│   ├── pytest.ini                   # pytest 설정
│   └── requirements.txt             # Python 의존성
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── auth.ts              # API 함수
│   │   ├── app/
│   │   │   ├── login/page.tsx       # 로그인 페이지
│   │   │   ├── register/page.tsx    # 회원가입 페이지
│   │   │   ├── profile/page.tsx     # 프로필 페이지
│   │   │   ├── layout.tsx           # Root Layout
│   │   │   └── page.tsx             # 홈 페이지
│   │   ├── components/
│   │   │   ├── Navigation.tsx       # 네비게이션 바
│   │   │   ├── ProtectedRoute.tsx   # 인증 가드
│   │   │   ├── Toast.tsx            # Toast 컴포넌트
│   │   │   └── ToastContainer.tsx   # Toast 컨테이너
│   │   ├── contexts/
│   │   │   ├── AuthContext.tsx      # 인증 상태 관리
│   │   │   └── ToastContext.tsx     # Toast 상태 관리
│   │   ├── types/
│   │   │   ├── user.ts              # User 타입
│   │   │   └── toast.ts             # Toast 타입
│   │   └── utils/
│   │       ├── token.ts             # 토큰 관리
│   │       └── api-error.ts         # API 에러 처리
│   ├── next.config.js               # Next.js 설정
│   ├── tailwind.config.ts           # Tailwind 설정
│   └── package.json                 # npm 의존성
│
└── .claude/
    └── docs/
        ├── dev.md                   # 개발 문서 (본 문서)
        ├── test.md                  # 테스트 문서
        └── progress.md              # 작업 이력
```

---

## 설치 및 실행

### 사전 요구사항
- Python 3.12+
- Node.js 18+
- npm 또는 yarn

### 백엔드 실행

```bash
# 1. 가상환경 생성 및 활성화
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정 (선택사항)
cp .env.example .env
# .env 파일에서 SECRET_KEY 수정 (프로덕션 필수)

# 4. 서버 실행
uvicorn app.main:app --reload

# 서버 주소: http://localhost:8000
# API 문서: http://localhost:8000/docs
```

### 프론트엔드 실행

```bash
# 1. 의존성 설치
cd frontend
npm install

# 2. 개발 서버 실행
npm run dev

# 서버 주소: http://localhost:3000
```

---

## API 문서

### 인증 API (Public)

| 메서드 | 엔드포인트 | 설명 | 요청 Body | 응답 |
|--------|-----------|------|----------|------|
| POST | `/api/auth/register` | 회원가입 | `UserCreate` | 201 `UserResponse` |
| POST | `/api/auth/login` | 로그인 | `UserLogin` | 200 `Token` |
| POST | `/api/auth/logout` | 로그아웃 | - | 200 `message` |

### 사용자 API (Protected)

| 메서드 | 엔드포인트 | 설명 | 요청 Body | 응답 |
|--------|-----------|------|----------|------|
| GET | `/api/users/me` | 프로필 조회 | - | 200 `UserResponse` |
| PUT | `/api/users/me` | 프로필 수정 | `UserUpdate` | 200 `UserResponse` |

**인증 방식**: Bearer Token
```http
Authorization: Bearer {access_token}
```

### 스키마

**UserCreate**:
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**UserLogin**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Token**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**UserResponse**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "created_at": "2026-02-10T12:00:00"
}
```

**UserUpdate**:
```json
{
  "username": "newusername",  // 선택
  "email": "newemail@example.com"  // 선택
}
```

**ErrorResponse**:
```json
{
  "error": "ValidationError",
  "message": "입력값 검증에 실패했습니다",
  "details": [
    {
      "field": "body.email",
      "message": "value is not a valid email address",
      "type": "value_error.email"
    }
  ],
  "status_code": 422
}
```

---

## 인증 시스템

### JWT 토큰 관리

**SECRET_KEY 설정**:
- 환경 변수(`.env`) 우선 로드
- 없으면 자동 생성 (개발 환경)
- 프로덕션에서는 `.env`에 고정값 설정 필수

```env
# backend/.env
SECRET_KEY=your-production-secret-key-min-64-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**토큰 생성**:
```python
# backend/app/utils/auth.py
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    secret_key = get_secret_key()
    algorithm = ALGORITHM

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
```

**토큰 검증**:
```python
# backend/app/dependencies/auth.py
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token_data = decode_access_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()

    if user is None:
        raise UnauthorizedException("사용자를 찾을 수 없습니다")

    return user
```

### 비밀번호 해싱

**SHA-256 + Salt**:
```python
# backend/app/utils/auth.py
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)  # 16 bytes = 32 hex chars
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt, stored_hash = hashed_password.split('$')
    hashed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return hashed == stored_hash
```

⚠️ **주의**: SHA-256은 비밀번호 해싱에 권장되지 않습니다. 프로덕션에서는 bcrypt, Argon2 사용을 권장합니다.

### 프론트엔드 인증 플로우

**AuthContext**:
```typescript
// frontend/src/contexts/AuthContext.tsx
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // 컴포넌트 마운트 시 토큰 확인
  useEffect(() => {
    const token = getToken();
    if (token) {
      getCurrentUser(token)
        .then(setUser)
        .catch(() => removeToken());
    }
    setLoading(false);
  }, []);

  // 로그인, 로그아웃, 회원가입 함수들...
};
```

**Protected Route**:
```typescript
// frontend/src/components/ProtectedRoute.tsx
export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) return <div>로딩 중...</div>;
  if (!user) return null;

  return <>{children}</>;
}
```

---

## 에러 처리

### 백엔드: 전역 예외 핸들러

**HTTP 예외 핸들러** (401, 404, 403 등):
```python
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )
```

**Pydantic 검증 에러 핸들러** (422):
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    details = [
        {
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "입력값 검증에 실패했습니다",
            "details": details,
            "status_code": 422
        }
    )
```

**커스텀 예외**:
```python
# backend/app/utils/exceptions.py
class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "리소스를 찾을 수 없습니다"):
        super().__init__(status_code=404, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "인증이 필요합니다"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "접근 권한이 없습니다"):
        super().__init__(status_code=403, detail=detail)
```

### 프론트엔드: Toast 알림 시스템

**Toast Context**:
```typescript
// frontend/src/contexts/ToastContext.tsx
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = (type: ToastType, message: string, duration = 3000) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, type, message, duration }]);

    setTimeout(() => removeToast(id), duration);
  };

  const success = (message: string) => showToast('success', message);
  const error = (message: string) => showToast('error', message);
  const info = (message: string) => showToast('info', message);
  const warning = (message: string) => showToast('warning', message);

  // ...
}
```

**Toast 컴포넌트**:
- 타입별 색상: 성공(초록), 에러(빨강), 정보(파랑), 경고(노랑)
- 자동 제거: 3초 후 사라짐
- 애니메이션: 우측에서 슬라이드 인

**사용 예시**:
```typescript
const { success, error } = useToast();

try {
  await login(email, password);
  success('로그인 성공!');
  router.push('/');
} catch (err) {
  error(getErrorMessage(err));
}
```

---

## 테스트

### 백엔드 테스트 (pytest)

**실행 명령어**:
```bash
cd backend

# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=app --cov-report=html

# 특정 파일만 실행
pytest tests/test_auth.py

# 상세 출력
pytest -v
```

**테스트 결과**:
```
====================== 42 passed in 2.71s ======================

---------- coverage: platform win32, python 3.14.3-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
app\routers\auth.py               37      1    97%
app\routers\users.py              26      0   100%
app\utils\auth.py                 44      5    89%
app\dependencies\auth.py          23      3    87%
--------------------------------------------------
TOTAL                            285     38    87%
```

**테스트 구조**:
- `tests/test_auth.py`: 인증 API 테스트 (11개)
- `tests/test_users.py`: 사용자 API 테스트 (13개)
- `tests/test_error_handlers.py`: 예외 핸들러 테스트 (14개)
- `tests/test_health.py`: Health Check 테스트 (6개)

**주요 픽스처**:
```python
# tests/conftest.py
@pytest.fixture
def client(db_session):
    """테스트 클라이언트"""
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client, test_user_data):
    """인증된 클라이언트"""
    client.post("/api/auth/register", json=test_user_data)
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = response.json()["access_token"]

    class AuthClient:
        def __init__(self, client, token):
            self._client = client
            self._token = token

        def get(self, *args, **kwargs):
            kwargs.setdefault('headers', {})['Authorization'] = f'Bearer {self._token}'
            return self._client.get(*args, **kwargs)

        # put, post, delete 메서드도 동일...

    return AuthClient(client, token)
```

### 프론트엔드 테스트 (향후 구현)

**권장 도구**:
- Jest + React Testing Library (단위 테스트)
- Playwright 또는 Cypress (E2E 테스트)

---

## 배포 가이드

### 백엔드 배포

**환경 변수 설정** (필수):
```env
# 프로덕션 .env
SECRET_KEY=<강력한-랜덤-문자열-최소-64자>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://user:password@host:port/dbname
```

**데이터베이스 마이그레이션**:
```bash
# Alembic 사용 권장 (현재는 SQLAlchemy auto-create 사용)
alembic upgrade head
```

**서버 실행**:
```bash
# Gunicorn + Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Docker** (권장):
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 프론트엔드 배포

**빌드**:
```bash
npm run build
```

**Vercel** (권장):
```bash
vercel deploy
```

**환경 변수** (Vercel):
```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

### 보안 체크리스트

- [ ] SECRET_KEY를 강력한 랜덤 문자열로 변경
- [ ] HTTPS 사용 (프로덕션 필수)
- [ ] CORS 설정을 특정 도메인으로 제한
- [ ] 비밀번호 해싱 알고리즘 변경 (bcrypt, Argon2)
- [ ] Rate Limiting 추가
- [ ] SQL Injection 방어 (SQLAlchemy ORM 사용 중)
- [ ] XSS 방어 (React 기본 이스케이프 처리)
- [ ] CSRF 토큰 (필요시)

---

## 다음 단계

- [ ] 비밀번호 재설정 기능
- [ ] Refresh Token 구현
- [ ] 이메일 인증
- [ ] 소셜 로그인 (OAuth2)
- [ ] 프론트엔드 테스트 (Jest, Playwright)
- [ ] CI/CD 파이프라인 (GitHub Actions)
- [ ] Docker Compose 설정
- [ ] 프로덕션 데이터베이스 (PostgreSQL)
- [ ] 로깅 시스템 (Loguru, Sentry)
- [ ] API 버전 관리

---

## 참고 자료

- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **Next.js 공식 문서**: https://nextjs.org/docs
- **JWT 소개**: https://jwt.io/introduction
- **pytest 문서**: https://docs.pytest.org/
- **Tailwind CSS 문서**: https://tailwindcss.com/docs

---

## 문의 및 기여

프로젝트 관련 문의 사항이나 버그 리포트는 GitHub Issues를 이용해주세요.

**작성일**: 2026-02-10
**작성자**: be-agent, fe-agent, main-agent
