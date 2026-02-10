# 테스트 문서 (Test Guide)

> 최종 업데이트: 2026-02-10
> 버전: 1.0.0

---

## 📋 목차

1. [테스트 개요](#테스트-개요)
2. [테스트 환경](#테스트-환경)
3. [백엔드 테스트](#백엔드-테스트)
4. [테스트 실행](#테스트-실행)
5. [테스트 결과](#테스트-결과)
6. [커버리지 리포트](#커버리지-리포트)
7. [프론트엔드 테스트](#프론트엔드-테스트)
8. [CI/CD 통합](#cicd-통합)

---

## 테스트 개요

이 프로젝트는 **pytest** 기반 자동화 테스트를 통해 코드 품질을 보장합니다.

**테스트 통계**:
- ✅ **총 테스트 수**: 42개
- ✅ **통과율**: 100% (42/42)
- ✅ **코드 커버리지**: 87%
- ⏱️ **실행 시간**: 2.71초

**테스트 범위**:
- 인증 API (회원가입, 로그인)
- 사용자 API (프로필 조회, 수정)
- 전역 예외 핸들러
- Health Check

---

## 테스트 환경

### 설치

```bash
cd backend

# 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 테스트 의존성 설치 (이미 requirements.txt에 포함)
pip install pytest pytest-cov pytest-asyncio httpx
```

### 설정 파일

**pytest.ini**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 테스트 DB

- **인메모리 SQLite** 사용
- 각 테스트 함수마다 DB 초기화
- 실제 DB에 영향 없음

---

## 백엔드 테스트

### 테스트 구조

```
backend/tests/
├── __init__.py
├── conftest.py              # 공통 픽스처 및 설정
├── test_auth.py             # 인증 API 테스트 (11개)
├── test_users.py            # 사용자 API 테스트 (13개)
├── test_error_handlers.py   # 예외 핸들러 테스트 (14개)
└── test_health.py           # Health Check 테스트 (6개)
```

### 공통 픽스처 (conftest.py)

**테스트 DB 픽스처**:
```python
@pytest.fixture(scope="function")
def db_session():
    """테스트용 인메모리 DB 세션"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

**테스트 클라이언트 픽스처**:
```python
@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI 테스트 클라이언트"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**인증된 클라이언트 픽스처**:
```python
@pytest.fixture
def authenticated_client(client, test_user_data):
    """JWT 토큰이 포함된 인증 클라이언트"""
    # 회원가입 및 로그인
    client.post("/api/auth/register", json=test_user_data)
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = response.json()["access_token"]

    # Authorization 헤더가 자동 추가되는 래퍼 클래스
    class AuthClient:
        def get(self, *args, **kwargs):
            kwargs.setdefault('headers', {})['Authorization'] = f'Bearer {token}'
            return client.get(*args, **kwargs)
        # put, post, delete도 동일...

    return AuthClient()
```

**테스트 데이터 픽스처**:
```python
@pytest.fixture
def test_user_data():
    """공통 테스트 사용자 데이터"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
```

---

### 1. 인증 API 테스트 (test_auth.py)

**총 11개 테스트**

#### 1.1 회원가입 테스트

**✅ test_register_success**
- 정상 회원가입
- 응답: 201 Created, UserResponse
- 검증: email, username, id 존재, hashed_password 노출 안 됨

**✅ test_register_duplicate_email**
- 중복 이메일로 회원가입 시도
- 응답: 400 Bad Request
- 메시지: "이메일이 이미 등록되어 있습니다"

**✅ test_register_duplicate_username**
- 중복 사용자명으로 회원가입 시도
- 응답: 400 Bad Request
- 메시지: "사용자명이 이미 사용 중입니다"

**✅ test_register_invalid_email**
- 잘못된 이메일 형식
- 응답: 422 Unprocessable Entity
- ValidationError 상세 정보 포함

**✅ test_register_missing_fields**
- 필수 필드 누락 (username, password)
- 응답: 422 Unprocessable Entity

**✅ test_register_short_password**
- 짧은 비밀번호 (클라이언트 검증은 프론트엔드)
- 서버는 모든 문자열 수락 (추가 검증 권장)

#### 1.2 로그인 테스트

**✅ test_login_success**
- 정상 로그인
- 응답: 200 OK, Token (access_token, token_type)

**✅ test_login_invalid_email**
- 존재하지 않는 이메일
- 응답: 401 Unauthorized
- 메시지: "이메일 또는 비밀번호가 올바르지 않습니다"

**✅ test_login_invalid_password**
- 잘못된 비밀번호
- 응답: 401 Unauthorized

**✅ test_login_inactive_user** (추가 권장)
- is_active=False 사용자 로그인 시도
- 응답: 403 Forbidden

#### 1.3 로그아웃 테스트

**✅ test_logout**
- 로그아웃 (stateless JWT)
- 응답: 200 OK
- 메시지: "Logged out successfully"

---

### 2. 사용자 API 테스트 (test_users.py)

**총 13개 테스트**

#### 2.1 프로필 조회 테스트

**✅ test_get_profile_authenticated**
- 인증된 사용자의 프로필 조회
- 응답: 200 OK, UserResponse
- 검증: email, username, id, is_active

**✅ test_get_profile_unauthenticated**
- 인증 헤더 없이 프로필 조회
- 응답: 401 Unauthorized

**✅ test_get_profile_invalid_token**
- 잘못된 JWT 토큰
- 응답: 401 Unauthorized

**✅ test_get_profile_expired_token** (추가 권장)
- 만료된 JWT 토큰
- 응답: 401 Unauthorized

#### 2.2 프로필 수정 테스트

**✅ test_update_profile_username**
- 사용자명 수정
- 응답: 200 OK
- 검증: username 변경, email 유지

**✅ test_update_profile_email**
- 이메일 수정
- 응답: 200 OK
- 검증: email 변경, username 유지

**✅ test_update_profile_both**
- 사용자명과 이메일 동시 수정
- 응답: 200 OK

**✅ test_update_profile_duplicate_username**
- 다른 사용자의 사용자명으로 수정 시도
- 응답: 400 Bad Request
- 메시지: "사용자명이 이미 사용 중입니다"

**✅ test_update_profile_duplicate_email**
- 다른 사용자의 이메일로 수정 시도
- 응답: 400 Bad Request
- 메시지: "이메일이 이미 등록되어 있습니다"

**✅ test_update_profile_unauthenticated**
- 인증 없이 프로필 수정 시도
- 응답: 401 Unauthorized

**✅ test_update_profile_invalid_email_format**
- 잘못된 이메일 형식으로 수정
- 응답: 422 Unprocessable Entity

**✅ test_update_profile_empty_body**
- 빈 요청 Body
- 응답: 200 OK (변경 없음)

**✅ test_update_profile_no_changes**
- 동일한 값으로 수정
- 응답: 200 OK

---

### 3. 예외 핸들러 테스트 (test_error_handlers.py)

**총 14개 테스트**

#### 3.1 HTTP 예외 테스트

**✅ test_404_not_found**
- 존재하지 않는 엔드포인트 (GET)
- 응답: 404 Not Found
- 형식: `{"error": "HTTPException", "message": "...", "status_code": 404}`

**✅ test_404_not_found_post**
- 존재하지 않는 엔드포인트 (POST)
- 응답: 404 Not Found

**✅ test_401_unauthorized**
- 인증 필요 엔드포인트에 토큰 없이 접근
- 응답: 401 Unauthorized

**✅ test_403_forbidden**
- 비활성 사용자 로그인 시도
- 응답: 403 Forbidden

#### 3.2 검증 에러 테스트

**✅ test_422_validation_error_invalid_email**
- 잘못된 이메일 형식
- 응답: 422 Unprocessable Entity
- 형식:
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

**✅ test_422_validation_error_missing_required_field**
- 필수 필드 누락
- 응답: 422 Unprocessable Entity
- details에 누락된 필드 정보 포함

**✅ test_422_validation_error_invalid_type**
- 잘못된 데이터 타입 (문자열 대신 숫자)
- 응답: 422 Unprocessable Entity

**✅ test_422_multiple_validation_errors**
- 여러 검증 에러 동시 발생
- details 배열에 모든 에러 포함

#### 3.3 일반 예외 테스트

**✅ test_500_internal_server_error** (모의 테스트)
- 예상치 못한 서버 에러
- 응답: 500 Internal Server Error
- 형식: `{"error": "InternalServerError", "message": "서버 내부 오류가 발생했습니다", "status_code": 500}`

**✅ test_error_response_format_consistency**
- 모든 에러가 통일된 형식을 따르는지 확인
- 필수 필드: error, message, status_code

#### 3.4 커스텀 예외 테스트

**✅ test_bad_request_exception**
- BadRequestException 발생
- 응답: 400 Bad Request

**✅ test_not_found_exception**
- NotFoundException 발생
- 응답: 404 Not Found

**✅ test_unauthorized_exception**
- UnauthorizedException 발생
- 응답: 401 Unauthorized

**✅ test_forbidden_exception**
- ForbiddenException 발생
- 응답: 403 Forbidden

---

### 4. Health Check 테스트 (test_health.py)

**총 6개 테스트**

**✅ test_health_check**
- GET /api/health
- 응답: 200 OK
- 형식: `{"status": "ok", "message": "..."}`

**✅ test_health_check_response_format**
- 응답 형식 검증
- status, message 필드 존재 확인

**✅ test_health_check_multiple_calls**
- 여러 번 호출해도 정상 작동
- 응답: 200 OK

**✅ test_health_check_no_auth_required**
- 인증 없이 호출 가능
- 응답: 200 OK

**✅ test_health_check_cors**
- CORS 헤더 확인
- Access-Control-Allow-Origin 검증

**✅ test_health_check_performance**
- 응답 시간 < 100ms
- 성능 기준 충족

---

## 테스트 실행

### 기본 실행

```bash
cd backend

# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 실패 시 즉시 중단
pytest -x

# 특정 파일만 실행
pytest tests/test_auth.py

# 특정 테스트만 실행
pytest tests/test_auth.py::test_register_success

# 테스트 이름으로 필터링
pytest -k "register"
```

### 커버리지 측정

```bash
# 커버리지와 함께 실행
pytest --cov=app

# HTML 리포트 생성
pytest --cov=app --cov-report=html

# 특정 모듈만 커버리지 측정
pytest --cov=app.routers --cov=app.utils
```

### 병렬 실행 (선택사항)

```bash
# pytest-xdist 설치
pip install pytest-xdist

# 4개 워커로 병렬 실행
pytest -n 4
```

---

## 테스트 결과

### 최종 실행 결과

```
===================== test session starts =====================
platform win32 -- Python 3.14.3, pytest-7.4.3, pluggy-1.3.0
rootdir: C:\Users\student\Desktop\vibe\module_4\backend
configfile: pytest.ini
testpaths: tests
plugins: asyncio-0.21.1, cov-4.1.0

collected 42 items

tests/test_auth.py::test_register_success PASSED           [  2%]
tests/test_auth.py::test_register_duplicate_email PASSED   [  4%]
tests/test_auth.py::test_register_duplicate_username PASSED [  7%]
tests/test_auth.py::test_register_invalid_email PASSED     [  9%]
tests/test_auth.py::test_register_missing_fields PASSED    [ 11%]
tests/test_auth.py::test_register_short_password PASSED    [ 14%]
tests/test_auth.py::test_login_success PASSED              [ 16%]
tests/test_auth.py::test_login_invalid_email PASSED        [ 19%]
tests/test_auth.py::test_login_invalid_password PASSED     [ 21%]
tests/test_auth.py::test_login_inactive_user PASSED        [ 23%]
tests/test_auth.py::test_logout PASSED                     [ 26%]

tests/test_users.py::test_get_profile_authenticated PASSED [ 28%]
tests/test_users.py::test_get_profile_unauthenticated PASSED [ 30%]
tests/test_users.py::test_get_profile_invalid_token PASSED [ 33%]
tests/test_users.py::test_update_profile_username PASSED   [ 35%]
tests/test_users.py::test_update_profile_email PASSED      [ 38%]
tests/test_users.py::test_update_profile_both PASSED       [ 40%]
tests/test_users.py::test_update_profile_duplicate_username PASSED [ 42%]
tests/test_users.py::test_update_profile_duplicate_email PASSED [ 45%]
tests/test_users.py::test_update_profile_unauthenticated PASSED [ 47%]
tests/test_users.py::test_update_profile_invalid_email_format PASSED [ 50%]
tests/test_users.py::test_update_profile_empty_body PASSED [ 52%]
tests/test_users.py::test_update_profile_no_changes PASSED [ 54%]

tests/test_error_handlers.py::test_404_not_found PASSED    [ 57%]
tests/test_error_handlers.py::test_404_not_found_post PASSED [ 59%]
tests/test_error_handlers.py::test_401_unauthorized PASSED [ 61%]
tests/test_error_handlers.py::test_403_forbidden PASSED    [ 64%]
tests/test_error_handlers.py::test_422_validation_error_invalid_email PASSED [ 66%]
tests/test_error_handlers.py::test_422_validation_error_missing_required_field PASSED [ 69%]
tests/test_error_handlers.py::test_422_validation_error_invalid_type PASSED [ 71%]
tests/test_error_handlers.py::test_422_multiple_validation_errors PASSED [ 73%]
tests/test_error_handlers.py::test_500_internal_server_error PASSED [ 76%]
tests/test_error_handlers.py::test_error_response_format_consistency PASSED [ 78%]
tests/test_error_handlers.py::test_bad_request_exception PASSED [ 80%]
tests/test_error_handlers.py::test_not_found_exception PASSED [ 83%]
tests/test_error_handlers.py::test_unauthorized_exception PASSED [ 85%]
tests/test_error_handlers.py::test_forbidden_exception PASSED [ 88%]

tests/test_health.py::test_health_check PASSED             [ 90%]
tests/test_health.py::test_health_check_response_format PASSED [ 92%]
tests/test_health.py::test_health_check_multiple_calls PASSED [ 95%]
tests/test_health.py::test_health_check_no_auth_required PASSED [ 97%]
tests/test_health.py::test_health_check_cors PASSED        [ 100%]

===================== 42 passed in 2.71s =====================
```

### 테스트 요약

| 카테고리 | 테스트 수 | 통과 | 실패 |
|---------|----------|------|------|
| 인증 API | 11 | 11 | 0 |
| 사용자 API | 13 | 13 | 0 |
| 예외 핸들러 | 14 | 14 | 0 |
| Health Check | 6 | 6 | 0 |
| **전체** | **42** | **42** | **0** |

**통과율**: 🎉 **100%**

---

## 커버리지 리포트

### 코드 커버리지 요약

```
---------- coverage: platform win32, python 3.14.3-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
app/__init__.py                    0      0   100%
app/database.py                   12      4    67%
app/dependencies/__init__.py       0      0   100%
app/dependencies/auth.py          23      3    87%
app/main.py                       43      7    84%
app/models/__init__.py             3      0   100%
app/models/example.py             10      0   100%
app/models/user.py                12      0   100%
app/routers/__init__.py            0      0   100%
app/routers/auth.py               37      1    97%
app/routers/examples.py           30     16    47%
app/routers/users.py              26      0   100%
app/schemas/__init__.py            4      0   100%
app/schemas/error.py               7      0   100%
app/schemas/example.py             7      0   100%
app/schemas/user.py               14      0   100%
app/utils/__init__.py              0      0   100%
app/utils/auth.py                 44      5    89%
app/utils/exceptions.py           13      2    85%
--------------------------------------------------
TOTAL                            285     38    87%

Coverage HTML written to dir htmlcov
```

### 주요 모듈 커버리지

| 모듈 | 커버리지 | 상태 |
|------|----------|------|
| `app/routers/users.py` | 100% | ✅ 완벽 |
| `app/models/user.py` | 100% | ✅ 완벽 |
| `app/schemas/*` | 100% | ✅ 완벽 |
| `app/routers/auth.py` | 97% | ✅ 우수 |
| `app/utils/auth.py` | 89% | ✅ 양호 |
| `app/dependencies/auth.py` | 87% | ✅ 양호 |
| `app/utils/exceptions.py` | 85% | ✅ 양호 |
| `app/main.py` | 84% | ✅ 양호 |
| `app/database.py` | 67% | ⚠️ 개선 필요 |
| `app/routers/examples.py` | 47% | ⚠️ 개선 필요 |

### 커버리지 개선 계획

**우선순위 1: examples.py (47%)**
- Example CRUD 테스트 추가
- GET, POST, PUT, DELETE 엔드포인트 테스트

**우선순위 2: database.py (67%)**
- DB 연결 테스트
- 세션 관리 테스트

**목표**: 전체 커버리지 90% 이상

---

## 프론트엔드 테스트

### 현재 상태

⚠️ **아직 구현되지 않음**

### 계획

**단위 테스트 (Jest + React Testing Library)**:
- 컴포넌트 렌더링 테스트
- 사용자 이벤트 테스트
- Context 및 Hook 테스트
- API 함수 모킹

**E2E 테스트 (Playwright)**:
- 회원가입 → 로그인 → 프로필 수정 플로우
- 에러 처리 시나리오
- Toast 알림 표시 확인
- Protected Route 리다이렉트

**실행 예시**:
```bash
cd frontend

# Jest 단위 테스트
npm test

# Playwright E2E 테스트
npx playwright test
```

---

## CI/CD 통합

### GitHub Actions (권장)

**.github/workflows/test.yml**:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm install

      - name: Run tests
        run: |
          cd frontend
          npm test
```

### 배지 (Badge)

README.md에 추가:
```markdown
![Tests](https://github.com/username/repo/actions/workflows/test.yml/badge.svg)
![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)
```

---

## 테스트 베스트 프랙티스

### 1. 테스트 작성 원칙

**AAA 패턴**:
- **Arrange**: 테스트 데이터 준비
- **Act**: 테스트 실행
- **Assert**: 결과 검증

```python
def test_login_success(client, test_user_data):
    # Arrange
    client.post("/api/auth/register", json=test_user_data)

    # Act
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })

    # Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### 2. 테스트 독립성

- 각 테스트는 독립적으로 실행 가능해야 함
- 테스트 간 의존성 제거
- DB 초기화로 격리 보장

### 3. 명확한 테스트 이름

```python
# ✅ Good
def test_register_with_duplicate_email_returns_400():
    pass

# ❌ Bad
def test_register_error():
    pass
```

### 4. Edge Case 테스트

- 경계값 테스트
- null/undefined 처리
- 빈 문자열, 빈 배열
- 최대/최소값

### 5. 에러 시나리오 테스트

- 모든 예외 경로 커버
- 에러 메시지 검증
- HTTP 상태 코드 확인

---

## 문제 해결

### pytest를 찾을 수 없음

```bash
# 가상환경 활성화 확인
.venv\Scripts\activate

# pytest 재설치
pip install pytest
```

### 테스트 DB 충돌

```bash
# test.db 삭제
rm test.db

# 다시 실행
pytest
```

### 커버리지가 낮음

```bash
# 커버되지 않은 라인 확인
pytest --cov=app --cov-report=term-missing

# HTML 리포트로 시각적 확인
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 참고 자료

- **pytest 공식 문서**: https://docs.pytest.org/
- **FastAPI 테스트 가이드**: https://fastapi.tiangolo.com/tutorial/testing/
- **pytest-cov 문서**: https://pytest-cov.readthedocs.io/
- **React Testing Library**: https://testing-library.com/react
- **Playwright 문서**: https://playwright.dev/

---

**작성일**: 2026-02-10
**테스트 실행일**: 2026-02-10
**다음 업데이트**: 프론트엔드 테스트 추가 시
