"""인증 API 테스트"""
import pytest


def test_register_success(client, test_user_data):
    """회원가입 성공"""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data  # 비밀번호는 응답에 포함되지 않아야 함


def test_register_duplicate_email(client, test_user_data):
    """중복 이메일로 회원가입 실패"""
    # 첫 번째 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 중복 이메일로 재시도
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    data = response.json()
    assert "이메일" in data["message"]


def test_register_duplicate_username(client, test_user_data):
    """중복 사용자명으로 회원가입 실패"""
    # 첫 번째 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 다른 이메일, 같은 사용자명으로 재시도
    duplicate_username_data = test_user_data.copy()
    duplicate_username_data["email"] = "different@example.com"
    response = client.post("/api/auth/register", json=duplicate_username_data)
    assert response.status_code == 400
    data = response.json()
    assert "사용자명" in data["message"]


def test_register_invalid_email(client):
    """잘못된 이메일 형식으로 회원가입 실패"""
    response = client.post("/api/auth/register", json={
        "email": "invalid-email",
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "details" in data


def test_register_missing_fields(client):
    """필수 필드 누락으로 회원가입 실패"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com"
        # username, password 누락
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_login_success(client, test_user_data):
    """로그인 성공"""
    # 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 로그인
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_invalid_email(client):
    """존재하지 않는 이메일로 로그인 실패"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_login_invalid_password(client, test_user_data):
    """잘못된 비밀번호로 로그인 실패"""
    # 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 잘못된 비밀번호로 로그인
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_login_missing_fields(client):
    """필수 필드 누락으로 로그인 실패"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com"
        # password 누락
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_logout(client):
    """로그아웃 성공"""
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_register_login_flow(client, test_user_data):
    """회원가입 -> 로그인 전체 플로우"""
    # 1. 회원가입
    register_response = client.post("/api/auth/register", json=test_user_data)
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    # 2. 로그인
    login_response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token is not None

    # 3. 로그아웃
    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200
