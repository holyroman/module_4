import { Admin, AdminCreate, AdminLogin, AdminToken, AdminUpdate } from '@/types/admin';
import { TwoFactorSettings } from '@/types/user';
import { getAdminToken } from '@/utils/admin-token';

const API_URL = '/api/admin';

// 인증
export async function adminLogin(data: AdminLogin): Promise<AdminToken> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function adminLogout(): Promise<void> {
  const token = getAdminToken();
  if (!token) return;

  await fetch(`${API_URL}/auth/logout`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
  });
}

export async function getCurrentAdmin(token: string): Promise<Admin> {
  const response = await fetch(`${API_URL}/users/me`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// CRUD (슈퍼 관리자 전용)
export async function createAdmin(token: string, data: AdminCreate): Promise<Admin> {
  const response = await fetch(`${API_URL}/users`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function getAdmins(token: string): Promise<Admin[]> {
  const response = await fetch(`${API_URL}/users`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function getAdmin(token: string, adminId: number): Promise<Admin> {
  const response = await fetch(`${API_URL}/users/${adminId}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function updateAdmin(token: string, adminId: number, data: AdminUpdate): Promise<Admin> {
  const response = await fetch(`${API_URL}/users/${adminId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function deleteAdmin(token: string, adminId: number): Promise<void> {
  const response = await fetch(`${API_URL}/users/${adminId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!response.ok) throw new Error(await response.text());
}

// 관리자용 사용자 2FA 설정
export async function updateUser2FA(token: string, userId: number, data: TwoFactorSettings): Promise<void> {
  const response = await fetch(`${API_URL}/users/${userId}/2fa`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error: any = new Error(errorData.message || errorData.detail || '사용자 2FA 설정에 실패했습니다.');
    error.response = { data: errorData };
    throw error;
  }
}
