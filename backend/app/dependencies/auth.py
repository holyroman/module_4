from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.utils.auth import decode_access_token
from app.utils.exceptions import UnauthorizedException, ForbiddenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """토큰에서 현재 사용자 조회"""
    try:
        token_data = decode_access_token(token)
        if token_data is None or token_data.email is None:
            raise UnauthorizedException("인증 정보를 확인할 수 없습니다")
    except Exception:
        raise UnauthorizedException("인증 정보를 확인할 수 없습니다")

    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise UnauthorizedException("인증 정보를 확인할 수 없습니다")

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """활성 사용자 확인"""
    if not current_user.is_active:
        raise ForbiddenException("비활성 사용자입니다")
    return current_user
