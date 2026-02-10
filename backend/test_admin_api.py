"""Admin API 테스트 스크립트"""

import os
import sys
import secrets

# backend 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import set_secret_key

# SECRET_KEY 설정
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(48)
set_secret_key(SECRET_KEY)

client = TestClient(app)


def test_admin_login():
    """관리자 로그인 테스트"""
    print("\n=== Test: Admin Login ===")

    response = client.post(
        "/api/admin/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "super_admin"

    return data["access_token"]


def test_admin_list(token: str):
    """관리자 목록 조회 테스트"""
    print("\n=== Test: Admin List ===")

    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_create_admin(token: str):
    """관리자 생성 테스트"""
    print("\n=== Test: Create Admin ===")

    response = client.post(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "newadmin@example.com",
            "username": "newadmin",
            "password": "password123",
            "role": "admin"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newadmin@example.com"
    assert data["username"] == "newadmin"
    assert data["role"] == "admin"

    return data["id"]


def test_get_admin(token: str, admin_id: int):
    """관리자 상세 조회 테스트"""
    print("\n=== Test: Get Admin ===")

    response = client.get(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_id


def test_update_admin(token: str, admin_id: int):
    """관리자 수정 테스트"""
    print("\n=== Test: Update Admin ===")

    response = client.put(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "updated_admin",
            "is_active": False
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated_admin"
    assert data["is_active"] == False


def test_admin_logout(token: str):
    """관리자 로그아웃 테스트"""
    print("\n=== Test: Admin Logout ===")

    response = client.post(
        "/api/admin/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    assert response.json()["message"] == "로그아웃되었습니다"


def run_tests():
    """전체 테스트 실행"""
    print("=" * 50)
    print("Admin API Tests")
    print("=" * 50)

    try:
        # 1. 로그인
        token = test_admin_login()

        # 2. 관리자 목록 조회
        test_admin_list(token)

        # 3. 관리자 생성
        admin_id = test_create_admin(token)

        # 4. 관리자 상세 조회
        test_get_admin(token, admin_id)

        # 5. 관리자 수정
        test_update_admin(token, admin_id)

        # 6. 로그아웃
        test_admin_logout(token)

        print("\n" + "=" * 50)
        print("[SUCCESS] All tests passed!")
        print("=" * 50)

    except AssertionError as e:
        print("\n" + "=" * 50)
        print(f"[FAIL] Test failed: {e}")
        print("=" * 50)
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[ERROR] {e}")
        print("=" * 50)


if __name__ == "__main__":
    run_tests()
