/**
 * API 에러 메시지 추출 유틸리티
 * 백엔드의 통일된 에러 응답 형식을 처리합니다.
 */
export function getErrorMessage(error: any): string {
  // 백엔드 에러 응답의 message 필드
  if (error.response?.data?.message) {
    return error.response.data.message;
  }

  // ValidationError의 경우 details 배열 처리
  if (error.response?.data?.details && Array.isArray(error.response.data.details)) {
    const firstError = error.response.data.details[0];
    if (firstError?.message) {
      return firstError.message;
    }
    if (firstError?.msg) {
      // FastAPI ValidationError의 경우 msg 필드 사용
      return firstError.msg;
    }
    return '입력값을 확인해주세요';
  }

  // error 필드가 있는 경우
  if (error.response?.data?.error) {
    return error.response.data.error;
  }

  // JavaScript Error 객체
  if (error.message) {
    return error.message;
  }

  // 기본 메시지
  return '오류가 발생했습니다';
}

/**
 * HTTP 상태 코드에 따른 기본 메시지 반환
 */
export function getStatusMessage(statusCode: number): string {
  const statusMessages: Record<number, string> = {
    400: '잘못된 요청입니다',
    401: '인증이 필요합니다',
    403: '접근 권한이 없습니다',
    404: '요청한 리소스를 찾을 수 없습니다',
    422: '입력값 검증에 실패했습니다',
    500: '서버 오류가 발생했습니다',
    503: '서비스를 일시적으로 사용할 수 없습니다',
  };

  return statusMessages[statusCode] || '오류가 발생했습니다';
}
