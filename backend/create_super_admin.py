"""초기 슈퍼 관리자 생성 스크립트"""

import os
import sys
import secrets

# backend 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, Base, engine
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.utils.auth import hash_password, set_secret_key


def create_super_admin():
    """슈퍼 관리자 생성"""
    # SECRET_KEY 설정 (서버와 동일하게)
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = secrets.token_urlsafe(48)
    set_secret_key(SECRET_KEY)

    # 테이블 생성
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 이미 존재하는지 확인
        existing = db.query(Admin).filter(Admin.email == "admin@example.com").first()
        if existing:
            print("[WARN] Super admin already exists.")
            print(f"   Email: {existing.email}")
            print(f"   Username: {existing.username}")
            print(f"   Role: {existing.role}")
            return

        # 슈퍼 관리자 생성
        admin = Admin(
            email="admin@example.com",
            username="superadmin",
            hashed_password=hash_password("admin123"),
            role="super_admin",
            is_active=True
        )
        db.add(admin)
        db.commit()

        print("[SUCCESS] Super admin created!")
        print("=" * 50)
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print("=" * 50)
        print("[WARNING] Change password in production!")

    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin()
