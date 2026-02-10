from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.utils.auth import decode_access_token
from app.utils.exceptions import UnauthorizedException, ForbiddenException


oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/api/admin/auth/login")


async def get_current_admin(
    token: str = Depends(oauth2_scheme_admin),
    db: Session = Depends(get_db)
) -> Admin:
    """현재 로그인한 관리자 조회 (JWT + 세션 검증)"""
    # JWT 검증
    token_data = decode_access_token(token)

    # 세션 검증
    session = db.query(AdminSession).filter(
        AdminSession.token == token,
        AdminSession.expires_at > datetime.utcnow()
    ).first()

    if not session:
        raise UnauthorizedException("세션이 만료되었거나 유효하지 않습니다")

    # 관리자 조회
    admin = db.query(Admin).filter(Admin.email == token_data.email).first()

    if admin is None:
        raise UnauthorizedException("관리자를 찾을 수 없습니다")

    return admin


async def get_current_active_admin(
    current_admin: Admin = Depends(get_current_admin)
) -> Admin:
    """활성화된 관리자만 허용"""
    if not current_admin.is_active:
        raise ForbiddenException("비활성화된 관리자입니다")

    return current_admin


async def get_super_admin(
    current_admin: Admin = Depends(get_current_active_admin)
) -> Admin:
    """슈퍼 관리자만 허용"""
    if current_admin.role != "super_admin":
        raise ForbiddenException("슈퍼 관리자 권한이 필요합니다")

    return current_admin
