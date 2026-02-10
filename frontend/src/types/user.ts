// User type definitions

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  two_factor_enabled?: boolean;
  auth_profile_id?: number | null;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginResponse {
  access_token?: string;
  token_type?: string;
  requires_2fa: boolean;
  temp_token?: string;
}

export interface VerifyTwoFactorRequest {
  temp_token: string;
  external_password: string;
}

export interface TwoFactorSettings {
  two_factor_enabled: boolean;
  auth_profile_id: number | null;
}

export interface UserUpdate {
  username?: string;
  email?: string;
}
