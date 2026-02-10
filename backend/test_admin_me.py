"""Admin /users/me 엔드포인트 테스트"""

import requests
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

BASE_URL = "http://localhost:8000"

def test_admin_me():
    print("=" * 50)
    print("Admin /users/me Endpoint Test")
    print("=" * 50)

    # 1. 로그인
    print("\n=== Step 1: Admin Login ===")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    response = requests.post(f"{BASE_URL}/api/admin/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"[ERROR] Login failed: {response.text}")
        return

    data = response.json()
    token = data.get("access_token")
    print(f"Token: {token[:50]}...")
    print(f"Role: {data.get('role')}")

    # 2. /users/me 호출
    print("\n=== Step 2: Get Current Admin Profile (/users/me) ===")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/api/admin/users/me", headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        admin_data = response.json()
        print(f"Response: {admin_data}")
        print("\n[SUCCESS] /users/me endpoint works!")
        print("=" * 50)
        print(f"   Email: {admin_data['email']}")
        print(f"   Username: {admin_data['username']}")
        print(f"   Role: {admin_data['role']}")
        print("=" * 50)
    else:
        print(f"[ERROR] /users/me failed: {response.text}")

if __name__ == "__main__":
    test_admin_me()
