"""관리자 관련 유틸리티 함수"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.admin_session import AdminSession


def cleanup_expired_sessions(db: Session) -> int:
    """만료된 세션 삭제

    Args:
        db: 데이터베이스 세션

    Returns:
        삭제된 세션 개수
    """
    deleted_count = db.query(AdminSession).filter(
        AdminSession.expires_at < datetime.utcnow()
    ).delete()
    db.commit()

    return deleted_count
