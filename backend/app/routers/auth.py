from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    LoginResponse,
    TwoFactorAuthRequest,
    TwoFactorAuthResponse
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_temp_token,
    verify_temp_token
)
from app.utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException
from app.services.external_auth import verify_external_auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """회원가입"""
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise BadRequestException("이미 등록된 이메일입니다")

    # 사용자명 중복 체크
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise BadRequestException("이미 사용 중인 사용자명입니다")

    # 비밀번호 해싱 및 사용자 생성
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=LoginResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """로그인 (1차 인증)"""
    # 이메일로 사용자 조회
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다")

    # 비밀번호 검증
    if not verify_password(user_credentials.password, user.hashed_password):
        raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다")

    # 활성 사용자 확인
    if not user.is_active:
        raise ForbiddenException("비활성 사용자입니다")

    # 2차 인증 필요 여부 확인
    if user.enable_2fa and user.auth_profile_id:
        # 2차 인증 필요: 임시 토큰 발급
        temp_token = create_temp_token(user.email)
        return LoginResponse(
            requires_2fa=True,
            temp_token=temp_token,
            access_token=None,
            message="2차 인증이 필요합니다. /auth/verify-2fa 엔드포인트로 인증을 완료하세요."
        )

    # 2차 인증 불필요: 바로 JWT 토큰 발급
    access_token = create_access_token(data={"sub": user.email})
    return LoginResponse(
        requires_2fa=False,
        temp_token=None,
        access_token=access_token,
        message="로그인 성공"
    )


@router.post("/verify-2fa", response_model=TwoFactorAuthResponse)
def verify_2fa(auth_request: TwoFactorAuthRequest, db: Session = Depends(get_db)):
    """2차 인증 검증"""
    # 임시 토큰 검증 및 이메일 추출
    email = verify_temp_token(auth_request.temp_token)

    # 사용자 조회
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UnauthorizedException("사용자를 찾을 수 없습니다")

    # 2차 인증이 활성화되어 있는지 확인
    if not user.enable_2fa or not user.auth_profile_id:
        raise BadRequestException("2차 인증이 설정되지 않았습니다")

    # 외부 인증 수행
    success, error_msg = verify_external_auth(
        db=db,
        profile_id=user.auth_profile_id,
        username=user.username,
        password=auth_request.password
    )

    if not success:
        raise UnauthorizedException(f"2차 인증 실패: {error_msg}")

    # 인증 성공: 최종 JWT 토큰 발급
    access_token = create_access_token(data={"sub": user.email})

    return TwoFactorAuthResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/logout")
def logout():
    """로그아웃 (stateless JWT이므로 클라이언트에서 토큰 삭제)"""
    return {"message": "로그아웃되었습니다"}
