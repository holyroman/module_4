from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.schemas.admin import (
    AdminCreate,
    AdminLogin,
    AdminResponse,
    AdminUpdate,
    AdminToken
)
from app.dependencies.admin_auth import (
    get_current_active_admin,
    get_super_admin,
    oauth2_scheme_admin
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils.exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    BadRequestException
)


router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ============================================
# 인증 엔드포인트
# ============================================

@router.post("/auth/login", response_model=AdminToken)
def admin_login(admin_login: AdminLogin, db: Session = Depends(get_db)):
    """관리자 로그인 (JWT + 세션 생성)"""
    # 1. 관리자 조회
    admin = db.query(Admin).filter(Admin.email == admin_login.email).first()
    if not admin:
        raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다")

    # 2. 비밀번호 검증
    if not verify_password(admin_login.password, admin.hashed_password):
        raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다")

    # 3. 활성 상태 확인
    if not admin.is_active:
        raise ForbiddenException("비활성화된 관리자입니다")

    # 4. JWT 토큰 생성 (subject에 email + role 포함)
    token = create_access_token(data={"sub": admin.email, "role": admin.role})

    # 5. 세션 DB에 저장
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    session = AdminSession(
        admin_id=admin.id,
        token=token,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()

    return AdminToken(access_token=token, role=admin.role)


@router.post("/auth/logout")
def admin_logout(
    current_admin: Admin = Depends(get_current_active_admin),
    token: str = Depends(oauth2_scheme_admin),
    db: Session = Depends(get_db)
):
    """관리자 로그아웃 (세션 삭제)"""
    # 세션 삭제
    db.query(AdminSession).filter(AdminSession.token == token).delete()
    db.commit()

    return {"message": "로그아웃되었습니다"}


@router.get("/users/me", response_model=AdminResponse)
def get_current_admin_profile(
    current_admin: Admin = Depends(get_current_active_admin)
):
    """현재 로그인한 관리자 프로필 조회"""
    return current_admin


# ============================================
# 관리자 CRUD 엔드포인트 (슈퍼 관리자 전용)
# ============================================

@router.post("/users", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(
    admin_create: AdminCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_super_admin)
):
    """관리자 생성 (슈퍼 관리자 전용)"""
    # 이메일 중복 확인
    existing_email = db.query(Admin).filter(Admin.email == admin_create.email).first()
    if existing_email:
        raise BadRequestException("이미 등록된 이메일입니다")

    # 사용자명 중복 확인
    existing_username = db.query(Admin).filter(Admin.username == admin_create.username).first()
    if existing_username:
        raise BadRequestException("이미 사용 중인 사용자명입니다")

    # 관리자 생성
    new_admin = Admin(
        email=admin_create.email,
        username=admin_create.username,
        hashed_password=hash_password(admin_create.password),
        role=admin_create.role,
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.get("/users", response_model=List[AdminResponse])
def list_admins(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_super_admin),
    skip: int = 0,
    limit: int = 100
):
    """관리자 목록 조회 (슈퍼 관리자 전용)"""
    admins = db.query(Admin).offset(skip).limit(limit).all()
    return admins


@router.get("/users/{admin_id}", response_model=AdminResponse)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_super_admin)
):
    """관리자 상세 조회 (슈퍼 관리자 전용)"""
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise NotFoundException("관리자를 찾을 수 없습니다")

    return admin


@router.put("/users/{admin_id}", response_model=AdminResponse)
def update_admin(
    admin_id: int,
    admin_update: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_super_admin)
):
    """관리자 수정 (슈퍼 관리자 전용)"""
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise NotFoundException("관리자를 찾을 수 없습니다")

    # 업데이트할 필드만 적용
    update_data = admin_update.model_dump(exclude_unset=True)

    # 이메일 중복 확인
    if "email" in update_data and update_data["email"] != admin.email:
        existing_email = db.query(Admin).filter(Admin.email == update_data["email"]).first()
        if existing_email:
            raise BadRequestException("이미 등록된 이메일입니다")

    # 사용자명 중복 확인
    if "username" in update_data and update_data["username"] != admin.username:
        existing_username = db.query(Admin).filter(Admin.username == update_data["username"]).first()
        if existing_username:
            raise BadRequestException("이미 사용 중인 사용자명입니다")

    # 필드 업데이트
    for key, value in update_data.items():
        setattr(admin, key, value)

    db.commit()
    db.refresh(admin)

    return admin


@router.delete("/users/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_super_admin)
):
    """관리자 삭제 (슈퍼 관리자 전용)"""
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise NotFoundException("관리자를 찾을 수 없습니다")

    # 자기 자신은 삭제 불가
    if admin.id == current_admin.id:
        raise BadRequestException("자기 자신은 삭제할 수 없습니다")

    # 관리자 삭제
    db.delete(admin)
    db.commit()

    return None
