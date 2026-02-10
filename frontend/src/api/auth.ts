// Auth API functions
import { User, UserCreate, UserLogin, Token, UserUpdate, LoginResponse, VerifyTwoFactorRequest, TwoFactorSettings } from '@/types/user';
import { AuthProfile, AuthProfileCreate, AuthProfileUpdate, AuthProfileTestResult } from '@/types/auth-profile';
import { removeToken } from '@/utils/token';

export async function register(data: UserCreate): Promise<User> {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    // 백엔드 에러 형식에 맞춰 에러 객체 구성
    const error: any = new Error(errorData.message || errorData.detail || '회원가입에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function login(data: UserLogin): Promise<LoginResponse> {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '로그인에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function verify2FA(data: VerifyTwoFactorRequest): Promise<Token> {
  const response = await fetch('/api/auth/verify-2fa', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '2차 인증에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch('/api/users/me', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '사용자 정보를 가져올 수 없습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function updateProfile(token: string, data: UserUpdate): Promise<User> {
  const response = await fetch('/api/users/me', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '프로필 수정에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export function logout(): void {
  removeToken();
}

// Auth Profile APIs
export async function getAuthProfiles(token: string): Promise<AuthProfile[]> {
  const response = await fetch('/api/auth-profiles', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '인증 프로필 목록을 가져올 수 없습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function createAuthProfile(token: string, data: AuthProfileCreate): Promise<AuthProfile> {
  const response = await fetch('/api/auth-profiles', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '인증 프로필 생성에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function updateAuthProfile(token: string, id: number, data: AuthProfileUpdate): Promise<AuthProfile> {
  const response = await fetch(`/api/auth-profiles/${id}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '인증 프로필 수정에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

export async function deleteAuthProfile(token: string, id: number): Promise<void> {
  const response = await fetch(`/api/auth-profiles/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '인증 프로필 삭제에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }
}

export async function testAuthProfile(token: string, id: number): Promise<AuthProfileTestResult> {
  const response = await fetch(`/api/auth-profiles/${id}/test`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '연결 테스트에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}

// User 2FA Settings
export async function update2FASettings(token: string, data: TwoFactorSettings): Promise<User> {
  const response = await fetch('/api/users/me/2fa', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '2FA 설정에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }

  return response.json();
}
