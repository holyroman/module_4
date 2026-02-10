"""Admin /users/me 엔드포인트 테스트"""

import pytest
from app.models.admin import Admin
from app.utils.auth import hash_password


def test_get_current_admin_profile(client, db_session):
    """현재 로그인한 관리자 프로필 조회 테스트"""
    # 관리자 생성
    admin = Admin(
        email="testadmin@example.com",
        username="testadmin",
        hashed_password=hash_password("testpass123"),
        role="super_admin",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()

    # 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "testadmin@example.com",
        "password": "testpass123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # /users/me 호출
    response = client.get(
        "/api/admin/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testadmin@example.com"
    assert data["username"] == "testadmin"
    assert data["role"] == "super_admin"
    assert data["is_active"] == True
    assert "id" in data
    assert "hashed_password" not in data


def test_get_current_admin_profile_without_token(client):
    """/users/me 토큰 없이 호출 시 401 에러"""
    response = client.get("/api/admin/users/me")
    assert response.status_code == 401
