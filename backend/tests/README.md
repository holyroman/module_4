# Backend API 테스트 가이드

## 개요

이 디렉토리는 FastAPI 백엔드 API의 자동화 테스트를 포함합니다.
pytest를 사용하여 모든 주요 엔드포인트와 예외 처리를 검증합니다.

## 설치

테스트 실행에 필요한 패키지를 설치합니다:

```bash
cd backend
pip install -r requirements.txt
```

필요한 테스트 패키지:
- `pytest==7.4.3` - 테스트 프레임워크
- `pytest-asyncio==0.21.1` - 비동기 테스트 지원
- `httpx==0.25.2` - FastAPI TestClient 의존성
- `pytest-cov==4.1.0` - 코드 커버리지 측정

## 테스트 실행

### 기본 실행
```bash
# 모든 테스트 실행
pytest

# 상세 출력 (-v)
pytest -v

# 짧은 트레이스백 출력 (이미 pytest.ini에 설정됨)
pytest --tb=short
```

### 특정 테스트 실행
```bash
# 특정 파일만 실행
pytest tests/test_auth.py

# 특정 테스트 함수만 실행
pytest tests/test_auth.py::test_login_success

# 패턴 매칭으로 실행
pytest -k "test_auth"
```

### 커버리지 측정
```bash
# 커버리지와 함께 실행
pytest --cov=app --cov-report=html

# 커버리지 리포트는 htmlcov/index.html에서 확인
```

### 실패한 테스트만 재실행
```bash
# 마지막 실패한 테스트만 실행
pytest --lf

# 실패한 테스트 먼저 실행
pytest --ff
```

## 테스트 구조

```
tests/
├── __init__.py              # 테스트 패키지
├── conftest.py              # 공통 픽스처 및 설정
├── test_auth.py             # 인증 API 테스트
├── test_users.py            # 사용자 API 테스트
├── test_error_handlers.py   # 전역 예외 핸들러 테스트
├── test_health.py           # Health Check 테스트
└── README.md                # 이 파일
```

## 주요 픽스처 (conftest.py)

### `client`
FastAPI TestClient 인스턴스를 제공합니다.

```python
def test_example(client):
    response = client.get("/api/health")
    assert response.status_code == 200
```

### `db_session`
테스트용 데이터베이스 세션을 제공합니다.
각 테스트 함수마다 DB가 초기화됩니다.

```python
def test_example(db_session):
    user = User(email="test@example.com", username="test")
    db_session.add(user)
    db_session.commit()
```

### `test_user_data`
테스트용 사용자 데이터를 제공합니다.

```python
def test_example(test_user_data):
    # test_user_data = {
    #     "email": "test@example.com",
    #     "username": "testuser",
    #     "password": "password123"
    # }
```

### `authenticated_client`
회원가입 및 로그인이 완료된 인증된 클라이언트를 제공합니다.
Authorization 헤더가 자동으로 포함됩니다.

```python
def test_example(authenticated_client):
    response = authenticated_client.get("/api/users/me")
    assert response.status_code == 200
```

## 테스트 케이스 목록

### 인증 API (test_auth.py)
- ✅ 회원가입 성공
- ✅ 회원가입 실패 (중복 이메일)
- ✅ 회원가입 실패 (중복 사용자명)
- ✅ 회원가입 실패 (잘못된 이메일 형식)
- ✅ 회원가입 실패 (필수 필드 누락)
- ✅ 로그인 성공
- ✅ 로그인 실패 (잘못된 이메일)
- ✅ 로그인 실패 (잘못된 비밀번호)
- ✅ 로그인 실패 (필수 필드 누락)
- ✅ 로그아웃
- ✅ 회원가입 → 로그인 전체 플로우

### 사용자 API (test_users.py)
- ✅ 프로필 조회 (인증됨)
- ✅ 프로필 조회 실패 (인증 안됨)
- ✅ 프로필 조회 실패 (잘못된 토큰)
- ✅ 프로필 수정 (사용자명)
- ✅ 프로필 수정 (이메일)
- ✅ 프로필 수정 (사용자명 + 이메일)
- ✅ 프로필 수정 실패 (중복 사용자명)
- ✅ 프로필 수정 실패 (중복 이메일)
- ✅ 프로필 수정 실패 (인증 안됨)
- ✅ 프로필 수정 실패 (잘못된 이메일 형식)
- ✅ 프로필 수정 (빈 요청)
- ✅ 프로필 조회 → 수정 → 재조회 전체 플로우

### 예외 핸들러 (test_error_handlers.py)
- ✅ 404 Not Found
- ✅ 422 Validation Error (잘못된 이메일)
- ✅ 422 Validation Error (필수 필드 누락)
- ✅ 422 Validation Error (잘못된 타입)
- ✅ 400 Bad Request (중복 이메일)
- ✅ 401 Unauthorized (토큰 없음)
- ✅ 401 Unauthorized (잘못된 토큰)
- ✅ 401 Unauthorized (잘못된 형식)
- ✅ 401 Unauthorized (잘못된 인증 정보)
- ✅ 에러 응답 구조 일관성

### Health Check (test_health.py)
- ✅ Health Check 엔드포인트
- ✅ Health Check 여러 번 호출
- ✅ 루트 경로 404
- ✅ OpenAPI 스키마 존재

## 새로운 테스트 추가 가이드

### 1. 테스트 파일 생성
`tests/` 디렉토리에 `test_*.py` 형식으로 파일을 생성합니다.

```python
# tests/test_example.py
def test_example(client):
    response = client.get("/api/example")
    assert response.status_code == 200
```

### 2. 테스트 함수 작성 규칙
- 함수명은 `test_`로 시작
- 명확하고 설명적인 이름 사용
- 각 테스트는 하나의 기능만 검증
- AAA 패턴 사용 (Arrange, Act, Assert)

```python
def test_user_registration_success(client, test_user_data):
    # Arrange: 테스트 데이터 준비
    user_data = test_user_data.copy()

    # Act: 동작 실행
    response = client.post("/api/auth/register", json=user_data)

    # Assert: 결과 검증
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

### 3. 픽스처 사용
필요한 픽스처를 파라미터로 받아 사용합니다.

```python
def test_with_auth(authenticated_client):
    response = authenticated_client.get("/api/users/me")
    assert response.status_code == 200
```

### 4. 새로운 픽스처 추가
`conftest.py`에 픽스처를 추가합니다.

```python
# conftest.py
@pytest.fixture
def sample_data():
    return {"key": "value"}
```

## 테스트 데이터베이스

- 테스트는 **인메모리 SQLite** (`test.db`)를 사용합니다
- 각 테스트 함수마다 DB가 생성되고 삭제됩니다
- 운영 DB (`app.db`)에는 영향을 주지 않습니다
- 테스트 종료 후 `test.db` 파일은 자동으로 삭제됩니다

## CI/CD 통합

GitHub Actions 등의 CI/CD 파이프라인에 통합할 수 있습니다:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```

## 문제 해결

### 테스트가 실패하는 경우

1. **ModuleNotFoundError**: 패키지가 설치되지 않음
   ```bash
   pip install -r requirements.txt
   ```

2. **테스트 DB 오류**: 이전 테스트 DB가 남아있음
   ```bash
   rm test.db
   ```

3. **SECRET_KEY 오류**: conftest.py에서 자동으로 설정됨 (문제 없음)

### 디버깅

테스트 실패 시 상세 정보를 보려면:
```bash
# 상세 출력
pytest -vv

# print 문 출력
pytest -s

# 전체 트레이스백
pytest --tb=long
```

## 추가 참고 자료

- [pytest 공식 문서](https://docs.pytest.org/)
- [FastAPI 테스팅 가이드](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov 문서](https://pytest-cov.readthedocs.io/)
