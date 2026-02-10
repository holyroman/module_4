from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    """에러 상세 정보"""
    field: Optional[str] = None  # 필드 에러의 경우
    message: str
    type: Optional[str] = None


class ErrorResponse(BaseModel):
    """통일된 에러 응답 스키마"""
    error: str  # "ValidationError", "NotFoundError" 등
    message: str  # 사용자 친화적 메시지
    details: Optional[List[ErrorDetail]] = None  # 상세 에러 목록
    status_code: int
