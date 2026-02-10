// Auth API functions
import { User, UserCreate, UserLogin, Token, UserUpdate } from '@/types/user';
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

export async function login(data: UserLogin): Promise<Token> {
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
