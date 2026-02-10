from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Admin(Base):
    """관리자 모델"""
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")  # "admin", "super_admin"
    is_active = Column(Boolean, default=True)

    # 2차 인증 필드
    enable_2fa = Column(Boolean, default=False)
    auth_profile_id = Column(Integer, ForeignKey("auth_profiles.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
