# 전역 예외 핸들러 가이드

## 개요
백엔드 전역 예외 핸들러를 통해 모든 API 엔드포인트에서 일관된 에러 응답을 제공합니다.

## 에러 응답 형식

모든 에러는 다음 형식으로 반환됩니다:

```json
{
  "error": "ValidationError",
  "message": "입력값 검증에 실패했습니다",
  "details": [
    {
      "field": "body.email",
      "message": "field required",
      "type": "value_error.missing"
    }
  ],
  "status_code": 422
}
```

## 에러 타입

### 1. ValidationError (422)
Pydantic 스키마 검증 실패 시 발생합니다.

**예시:**
- 필수 필드 누락
- 타입 불일치 (문자열 대신 숫자)
- 이메일 형식 오류

**응답 예시:**
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

### 2. BadRequestException (400)
잘못된 요청 데이터 (비즈니스 로직 위반)

**예시:**
- 이메일 중복
- 사용자명 중복

**사용법:**
```python
from app.utils.exceptions import BadRequestException

if existing_user:
    raise BadRequestException("이미 등록된 이메일입니다")
```

**응답 예시:**
```json
{
  "error": "HTTPException",
  "message": "이미 등록된 이메일입니다",
  "status_code": 400
}
```

### 3. UnauthorizedException (401)
인증 실패

**예시:**
- 잘못된 토큰
- 토큰 만료
- 잘못된 이메일/비밀번호

**사용법:**
```python
from app.utils.exceptions import UnauthorizedException

if not user:
    raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다")
```

**응답 예시:**
```json
{
  "error": "HTTPException",
  "message": "인증 정보를 확인할 수 없습니다",
  "status_code": 401
}
```

### 4. ForbiddenException (403)
권한 없음

**예시:**
- 비활성 사용자
- 접근 권한 없음

**사용법:**
```python
from app.utils.exceptions import ForbiddenException

if not user.is_active:
    raise ForbiddenException("비활성 사용자입니다")
```

**응답 예시:**
```json
{
  "error": "HTTPException",
  "message": "비활성 사용자입니다",
  "status_code": 403
}
```

### 5. NotFoundException (404)
리소스를 찾을 수 없음

**사용법:**
```python
from app.utils.exceptions import NotFoundException

if not item:
    raise NotFoundException("해당 게시글을 찾을 수 없습니다")
```

**응답 예시:**
```json
{
  "error": "HTTPException",
  "message": "리소스를 찾을 수 없습니다",
  "status_code": 404
}
```

### 6. InternalServerError (500)
서버 내부 오류

**예시:**
- 처리되지 않은 예외
- 데이터베이스 연결 오류

**응답 예시:**
```json
{
  "error": "InternalServerError",
  "message": "서버 내부 오류가 발생했습니다",
  "status_code": 500
}
```

## 커스텀 예외 사용법

### 기본 예외 (HTTPException) 대신 커스텀 예외 사용

**❌ Before:**
```python
from fastapi import HTTPException, status

if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="이미 등록된 이메일입니다"
    )
```

**✅ After:**
```python
from app.utils.exceptions import BadRequestException

if existing_user:
    raise BadRequestException("이미 등록된 이메일입니다")
```

### 전체 예시

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.utils.exceptions import BadRequestException, NotFoundException

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 중복 체크
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise BadRequestException("이미 등록된 이메일입니다")

    # 사용자 생성
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(f"ID {user_id}에 해당하는 사용자를 찾을 수 없습니다")

    return user
```

## 프론트엔드에서 에러 처리

```typescript
// Next.js 예시
try {
  const response = await fetch('/api/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    // 통일된 에러 형식으로 처리
    console.error(`[${error.error}] ${error.message}`);

    // 상세 에러가 있는 경우 (ValidationError)
    if (error.details) {
      error.details.forEach(detail => {
        console.error(`  - ${detail.field}: ${detail.message}`);
      });
    }

    // 상태 코드별 처리
    switch (error.status_code) {
      case 401:
        // 로그인 페이지로 리다이렉트
        router.push('/login');
        break;
      case 403:
        // 권한 없음 알림
        alert(error.message);
        break;
      case 422:
        // 폼 검증 에러 표시
        displayValidationErrors(error.details);
        break;
      default:
        // 일반 에러 알림
        alert(error.message);
    }
  }
} catch (err) {
  console.error('네트워크 오류:', err);
}
```

## 테스트

테스트 스크립트를 실행하여 전역 예외 핸들러를 확인할 수 있습니다:

```bash
# 백엔드 서버 실행 (터미널 1)
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# 테스트 실행 (터미널 2)
cd backend
.venv\Scripts\activate
python test_error_handlers.py
```

## 참고사항

- 모든 커스텀 예외는 `app.utils.exceptions`에 정의되어 있습니다.
- `main.py`에 전역 예외 핸들러가 등록되어 있습니다.
- 에러 스키마는 `app.schemas.error`에 정의되어 있습니다.
- 개발 환경에서는 500 에러 발생 시 콘솔에 traceback이 출력됩니다.
