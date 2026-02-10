import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.utils.auth import set_secret_key

# 테스트용 SECRET_KEY 설정
TEST_SECRET_KEY = "test-secret-key-for-pytest-testing-only"
set_secret_key(TEST_SECRET_KEY)

# 테스트용 인메모리 DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """테스트용 DB 세션 픽스처"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """테스트용 클라이언트 픽스처"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """테스트용 사용자 데이터"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }


@pytest.fixture
def authenticated_client(client, test_user_data):
    """인증된 클라이언트 픽스처"""
    # 회원가입
    client.post("/api/auth/register", json=test_user_data)

    # 로그인
    login_response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]

    # 인증 헤더 추가
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


def pytest_configure(config):
    """pytest 설정"""
    # 환경 변수 설정
    os.environ["SECRET_KEY"] = TEST_SECRET_KEY


def pytest_unconfigure(config):
    """pytest 종료 시 정리"""
    # 테스트 DB 파일 삭제 (Windows에서 파일 잠금 문제 가능성)
    import time
    if os.path.exists("test.db"):
        try:
            time.sleep(0.1)  # 짧은 대기
            os.remove("test.db")
        except (PermissionError, OSError):
            # Windows에서 파일이 잠겨있을 수 있음 (무시)
            pass
