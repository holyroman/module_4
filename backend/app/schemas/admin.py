from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AdminCreate(BaseModel):
    """관리자 생성 스키마"""
    email: EmailStr
    username: str
    password: str
    role: str = "admin"


class AdminLogin(BaseModel):
    """관리자 로그인 스키마"""
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    """관리자 응답 스키마"""
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUpdate(BaseModel):
    """관리자 수정 스키마"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class AdminToken(BaseModel):
    """관리자 토큰 스키마"""
    access_token: str
    token_type: str = "bearer"
    role: str
