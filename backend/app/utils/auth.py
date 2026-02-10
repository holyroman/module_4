# WARNING: SHA-256은 비밀번호 해싱에 권장되지 않습니다.
# 프로덕션 환경에서는 bcrypt, Argon2 등을 사용하세요.

import hashlib
import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.schemas import TokenData
from app.utils.exceptions import UnauthorizedException


# JWT 설정 상수
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECRET_KEY는 서버 시작 시 main.py에서 생성됨
_SECRET_KEY: str | None = None


def set_secret_key(secret_key: str):
    """서버 시작 시 SECRET_KEY 설정 (main.py에서 호출)"""
    global _SECRET_KEY
    _SECRET_KEY = secret_key


def get_secret_key() -> str:
    """SECRET_KEY 조회"""
    if _SECRET_KEY is None:
        raise ValueError("SECRET_KEY가 초기화되지 않았습니다. 서버를 재시작하세요.")
    return _SECRET_KEY


def hash_password(password: str) -> str:
    """SHA-256으로 비밀번호 해싱 (salt 포함)"""
    # 랜덤 salt 생성 (16 bytes)
    salt = secrets.token_hex(16)
    # SHA-256으로 해싱
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    try:
        # salt와 hash 분리
        salt, stored_hash = hashed_password.split('$')
        # 입력 비밀번호를 같은 salt로 해싱
        hashed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return hashed == stored_hash
    except:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWT 토큰 생성 (메모리의 SECRET_KEY 사용)"""
    to_encode = data.copy()

    # 만료 시간 설정
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # 메모리에서 SECRET_KEY 로드
    secret_key = get_secret_key()

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """JWT 토큰 디코딩 (메모리의 SECRET_KEY 사용)"""
    # 메모리에서 SECRET_KEY 로드
    secret_key = get_secret_key()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException("유효하지 않은 토큰입니다")
        return TokenData(email=email)
    except JWTError:
        raise UnauthorizedException("유효하지 않은 토큰입니다")
