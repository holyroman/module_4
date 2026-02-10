"""관리자 비밀번호 재설정 스크립트"""

import os
import sys
import secrets

# backend 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.admin import Admin
from app.utils.auth import hash_password, verify_password, set_secret_key


def reset_admin_password():
    """관리자 비밀번호를 admin123으로 재설정"""
    # SECRET_KEY 설정
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = secrets.token_urlsafe(48)
    set_secret_key(SECRET_KEY)

    db = SessionLocal()

    try:
        # 관리자 조회
        admin = db.query(Admin).filter(Admin.email == "admin@example.com").first()

        if not admin:
            print("[ERROR] Admin not found!")
            return

        print(f"[INFO] Found admin: {admin.email}")

        # 현재 비밀번호로 검증 테스트
        print(f"[INFO] Testing current password verification...")
        is_valid = verify_password("admin123", admin.hashed_password)
        print(f"[INFO] Current password 'admin123' valid: {is_valid}")

        # 비밀번호 재설정
        new_hashed = hash_password("admin123")
        print(f"[INFO] New hashed password: {new_hashed[:50]}...")

        admin.hashed_password = new_hashed
        db.commit()

        # 재설정 후 검증
        db.refresh(admin)
        is_valid_after = verify_password("admin123", admin.hashed_password)
        print(f"[INFO] After reset, password 'admin123' valid: {is_valid_after}")

        print("\n" + "=" * 50)
        print("[SUCCESS] Password reset completed!")
        print("=" * 50)
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print("=" * 50)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    reset_admin_password()
