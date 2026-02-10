"""사용자 API 테스트"""
import pytest


def test_get_profile_authenticated(authenticated_client, test_user_data):
    """인증된 사용자의 프로필 조회 성공"""
    response = authenticated_client.get("/api/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert "is_active" in data
    assert data["is_active"] is True


def test_get_profile_unauthenticated(client):
    """인증되지 않은 사용자의 프로필 조회 실패"""
    response = client.get("/api/users/me")
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_get_profile_invalid_token(client):
    """잘못된 토큰으로 프로필 조회 실패"""
    response = client.get("/api/users/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401


def test_update_profile_username(authenticated_client, test_user_data):
    """사용자명 수정 성공"""
    new_username = "newusername"
    response = authenticated_client.put("/api/users/me", json={
        "username": new_username
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == new_username
    assert data["email"] == test_user_data["email"]


def test_update_profile_email(authenticated_client, test_user_data):
    """이메일 수정 성공"""
    new_email = "newemail@example.com"
    response = authenticated_client.put("/api/users/me", json={
        "email": new_email
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_email
    assert data["username"] == test_user_data["username"]


def test_update_profile_both_fields(authenticated_client):
    """사용자명과 이메일 동시 수정 성공"""
    new_data = {
        "username": "newusername",
        "email": "newemail@example.com"
    }
    response = authenticated_client.put("/api/users/me", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == new_data["username"]
    assert data["email"] == new_data["email"]


def test_update_profile_duplicate_username(client, test_user_data):
    """다른 사용자가 사용 중인 사용자명으로 수정 실패"""
    # 첫 번째 사용자 생성 및 로그인
    client.post("/api/auth/register", json=test_user_data)

    # 두 번째 사용자 생성 및 로그인
    second_user_data = {
        "email": "second@example.com",
        "username": "seconduser",
        "password": "password123"
    }
    client.post("/api/auth/register", json=second_user_data)
    login_response = client.post("/api/auth/login", json={
        "email": second_user_data["email"],
        "password": second_user_data["password"]
    })
    token = login_response.json()["access_token"]

    # 첫 번째 사용자의 사용자명으로 변경 시도
    response = client.put("/api/users/me",
        json={"username": test_user_data["username"]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "사용자명" in data["message"]


def test_update_profile_duplicate_email(client, test_user_data):
    """다른 사용자가 사용 중인 이메일로 수정 실패"""
    # 첫 번째 사용자 생성
    client.post("/api/auth/register", json=test_user_data)

    # 두 번째 사용자 생성 및 로그인
    second_user_data = {
        "email": "second@example.com",
        "username": "seconduser",
        "password": "password123"
    }
    client.post("/api/auth/register", json=second_user_data)
    login_response = client.post("/api/auth/login", json={
        "email": second_user_data["email"],
        "password": second_user_data["password"]
    })
    token = login_response.json()["access_token"]

    # 첫 번째 사용자의 이메일로 변경 시도
    response = client.put("/api/users/me",
        json={"email": test_user_data["email"]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "이메일" in data["message"]


def test_update_profile_unauthenticated(client):
    """인증되지 않은 사용자의 프로필 수정 실패"""
    response = client.put("/api/users/me", json={
        "username": "newusername"
    })
    assert response.status_code == 401


def test_update_profile_invalid_email(authenticated_client):
    """잘못된 이메일 형식으로 프로필 수정 실패"""
    response = authenticated_client.put("/api/users/me", json={
        "email": "invalid-email"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_update_profile_empty_body(authenticated_client):
    """빈 요청으로 프로필 수정 (변경 없음)"""
    # 현재 프로필 조회
    current_profile = authenticated_client.get("/api/users/me").json()

    # 빈 요청으로 수정
    response = authenticated_client.put("/api/users/me", json={})
    assert response.status_code == 200
    data = response.json()

    # 프로필이 변경되지 않았는지 확인
    assert data["username"] == current_profile["username"]
    assert data["email"] == current_profile["email"]


def test_get_and_update_profile_flow(authenticated_client, test_user_data):
    """프로필 조회 -> 수정 -> 재조회 전체 플로우"""
    # 1. 초기 프로필 조회
    initial_response = authenticated_client.get("/api/users/me")
    assert initial_response.status_code == 200
    initial_data = initial_response.json()
    assert initial_data["username"] == test_user_data["username"]

    # 2. 프로필 수정
    new_username = "updated_username"
    update_response = authenticated_client.put("/api/users/me", json={
        "username": new_username
    })
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["username"] == new_username

    # 3. 수정된 프로필 재조회
    final_response = authenticated_client.get("/api/users/me")
    assert final_response.status_code == 200
    final_data = final_response.json()
    assert final_data["username"] == new_username
    assert final_data["id"] == initial_data["id"]
