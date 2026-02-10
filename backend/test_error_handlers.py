"""
전역 예외 핸들러 테스트 스크립트
수동으로 API 엔드포인트 테스트 (pytest 없이)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title: str, response):
    """응답 출력"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_validation_error():
    """422 Validation Error 테스트"""
    # 잘못된 요청 데이터 (필수 필드 누락)
    response = requests.post(f"{BASE_URL}/api/auth/register", json={})
    print_response("Validation Error (422)", response)


def test_bad_request():
    """400 Bad Request 테스트 (이메일 중복)"""
    # 먼저 사용자 등록
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    requests.post(f"{BASE_URL}/api/auth/register", json=user_data)

    # 같은 이메일로 다시 등록 시도
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print_response("Bad Request (400) - 이메일 중복", response)


def test_unauthorized():
    """401 Unauthorized 테스트"""
    # 잘못된 토큰으로 보호된 엔드포인트 접근
    response = requests.get(
        f"{BASE_URL}/api/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    print_response("Unauthorized (401) - 잘못된 토큰", response)


def test_not_found():
    """404 Not Found 테스트"""
    response = requests.get(f"{BASE_URL}/api/nonexistent")
    print_response("Not Found (404)", response)


def test_successful_login():
    """정상 로그인 테스트"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    print_response("Successful Login (200)", response)
    return response.json().get("access_token")


if __name__ == "__main__":
    print("""
    전역 예외 핸들러 테스트

    주의: 백엔드 서버가 실행 중이어야 합니다.
    실행 방법: cd backend && .venv\\Scripts\\activate && uvicorn app.main:app --reload
    """)

    try:
        # Health check
        response = requests.get(f"{BASE_URL}/api/health")
        print_response("Health Check", response)

        # 테스트 실행
        test_validation_error()
        test_bad_request()
        test_unauthorized()
        test_not_found()

        print("\n" + "="*60)
        print("모든 테스트 완료!")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("\n❌ 오류: 백엔드 서버에 연결할 수 없습니다.")
        print("서버가 실행 중인지 확인하세요: http://localhost:8000")
