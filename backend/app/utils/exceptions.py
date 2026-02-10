from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """400 Bad Request 예외"""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFoundException(HTTPException):
    """404 Not Found 예외"""
    def __init__(self, detail: str = "리소스를 찾을 수 없습니다"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(HTTPException):
    """401 Unauthorized 예외"""
    def __init__(self, detail: str = "인증이 필요합니다"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    """403 Forbidden 예외"""
    def __init__(self, detail: str = "접근 권한이 없습니다"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
