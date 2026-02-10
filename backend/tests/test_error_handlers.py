"""전역 예외 핸들러 테스트"""
import pytest


def test_404_not_found(client):
    """404 Not Found 에러 핸들러 테스트"""
    response = client.get("/api/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "HTTPException"
    assert "message" in data
    assert data["status_code"] == 404


def test_404_not_found_post(client):
    """존재하지 않는 엔드포인트에 POST 요청"""
    response = client.post("/api/does-not-exist", json={})
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "HTTPException"


def test_422_validation_error_invalid_email(client):
    """422 Validation Error 에러 핸들러 테스트 - 잘못된 이메일"""
    response = client.post("/api/auth/register", json={
        "email": "not-an-email",
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "message" in data
    assert "details" in data
    assert isinstance(data["details"], list)
    assert len(data["details"]) > 0

    # 상세 에러 정보 확인
    detail = data["details"][0]
    assert "field" in detail
    assert "message" in detail
    assert "type" in detail


def test_422_validation_error_missing_required_field(client):
    """422 Validation Error 에러 핸들러 테스트 - 필수 필드 누락"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com"
        # username, password 누락
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "details" in data
    assert len(data["details"]) >= 2  # username, password 2개 필드 누락


def test_422_validation_error_wrong_type(client):
    """422 Validation Error 에러 핸들러 테스트 - 잘못된 타입"""
    response = client.post("/api/auth/register", json={
        "email": 12345,  # 문자열이어야 하는데 숫자
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_400_bad_request_duplicate_email(client, test_user_data):
    """400 Bad Request 에러 테스트 - 중복 이메일"""
    # 첫 번째 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 중복 이메일로 재시도
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "HTTPException"
    assert "이메일" in data["message"]
    assert data["status_code"] == 400


def test_401_unauthorized_no_token(client):
    """401 Unauthorized 에러 테스트 - 토큰 없음"""
    response = client.get("/api/users/me")
    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "HTTPException"
    assert data["status_code"] == 401


def test_401_unauthorized_invalid_token(client):
    """401 Unauthorized 에러 테스트 - 잘못된 토큰"""
    response = client.get("/api/users/me", headers={
        "Authorization": "Bearer invalid-token-12345"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "HTTPException"


def test_401_unauthorized_malformed_token(client):
    """401 Unauthorized 에러 테스트 - 잘못된 형식의 토큰"""
    response = client.get("/api/users/me", headers={
        "Authorization": "NotBearer token"
    })
    assert response.status_code == 401


def test_401_unauthorized_wrong_credentials(client):
    """401 Unauthorized 에러 테스트 - 잘못된 인증 정보"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "HTTPException"


def test_health_check_success(client):
    """Health Check 엔드포인트 정상 작동"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data


def test_method_not_allowed(client):
    """405 Method Not Allowed 테스트"""
    # GET만 지원하는 엔드포인트에 POST 요청
    response = client.post("/api/health")
    assert response.status_code in [405, 404]  # FastAPI는 404 반환할 수 있음


def test_error_response_structure(client):
    """에러 응답 구조 일관성 테스트"""
    # 404 에러
    response_404 = client.get("/api/nonexistent")
    data_404 = response_404.json()
    assert "error" in data_404
    assert "message" in data_404
    assert "status_code" in data_404

    # 422 에러
    response_422 = client.post("/api/auth/register", json={"email": "invalid"})
    data_422 = response_422.json()
    assert "error" in data_422
    assert "message" in data_422
    assert "details" in data_422
    assert "status_code" in data_422

    # 401 에러
    response_401 = client.get("/api/users/me")
    data_401 = response_401.json()
    assert "error" in data_401
    assert "message" in data_401
    assert "status_code" in data_401
