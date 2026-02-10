export interface Admin {
  id: number;
  email: string;
  username: string;
  role: 'admin' | 'super_admin';
  is_active: boolean;
  created_at: string;
}

export interface AdminCreate {
  email: string;
  username: string;
  password: string;
  role?: 'admin' | 'super_admin';
}

export interface AdminLogin {
  email: string;
  password: string;
}

export interface AdminToken {
  access_token: string;
  token_type: string;
  role: string;
}

export interface AdminUpdate {
  username?: string;
  email?: string;
  role?: 'admin' | 'super_admin';
  is_active?: boolean;
}
