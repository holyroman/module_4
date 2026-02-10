"""
백엔드 API 테스트 스크립트

실행 방법:
1. 백엔드 서버 실행: cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload
2. 새 터미널에서: python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_result(test_name, response):
    print(f"\n[{test_name}]")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    print_section("1. 헬스 체크")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print_result("Health Check", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_register(email, username, password):
    print_section("2. 회원가입 테스트")
    try:
        data = {
            "email": email,
            "username": username,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print_result("Register", response)
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login(email, password):
    print_section("3. 로그인 테스트")
    try:
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print_result("Login", response)

        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"\n✅ Access Token: {token[:50]}...")
            return token
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_profile(token):
    print_section("4. 프로필 조회 테스트")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
        print_result("Get Profile", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_update_profile(token, new_username):
    print_section("5. 프로필 수정 테스트")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"username": new_username}
        response = requests.put(f"{BASE_URL}/api/users/me", json=data, headers=headers)
        print_result("Update Profile", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_duplicate_email(email):
    print_section("6. 이메일 중복 테스트")
    try:
        data = {
            "email": email,
            "username": "anotheruser",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print_result("Duplicate Email", response)
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_login():
    print_section("7. 잘못된 로그인 테스트")
    try:
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print_result("Invalid Login", response)
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🚀" * 30)
    print("   백엔드 API 테스트 시작")
    print("🚀" * 30)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_email = f"test_{timestamp}@example.com"
    test_username = f"testuser_{timestamp}"
    test_password = "password123"

    results = []

    # 1. 헬스 체크
    results.append(("Health Check", test_health_check()))

    # 2. 회원가입
    results.append(("Register", test_register(test_email, test_username, test_password)))

    # 3. 로그인
    token = test_login(test_email, test_password)
    results.append(("Login", token is not None))

    if token:
        # 4. 프로필 조회
        results.append(("Get Profile", test_get_profile(token)))

        # 5. 프로필 수정
        new_username = f"updated_{timestamp}"
        results.append(("Update Profile", test_update_profile(token, new_username)))
    else:
        results.append(("Get Profile", False))
        results.append(("Update Profile", False))

    # 6. 이메일 중복 테스트
    results.append(("Duplicate Email", test_duplicate_email(test_email)))

    # 7. 잘못된 로그인
    results.append(("Invalid Login", test_invalid_login()))

    # 결과 출력
    print("\n" + "=" * 60)
    print("   테스트 결과 요약")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "-" * 60)
    print(f"총 {len(results)}개 테스트 중 {passed}개 통과, {failed}개 실패")
    print("-" * 60)

    if failed == 0:
        print("\n🎉 모든 테스트 통과!")
    else:
        print(f"\n⚠️ {failed}개 테스트 실패")

if __name__ == "__main__":
    main()
