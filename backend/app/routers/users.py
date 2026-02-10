from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.dependencies.auth import get_current_active_user
from app.utils.exceptions import BadRequestException

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """현재 사용자 프로필 조회"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """현재 사용자 프로필 수정"""
    # username 변경 시 중복 체크
    if user_update.username is not None:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise BadRequestException("이미 사용 중인 사용자명입니다")
        current_user.username = user_update.username

    # email 변경 시 중복 체크
    if user_update.email is not None:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise BadRequestException("이미 등록된 이메일입니다")
        current_user.email = user_update.email

    db.commit()
    db.refresh(current_user)

    return current_user
