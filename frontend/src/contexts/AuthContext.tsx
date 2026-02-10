'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserCreate, UserUpdate } from '@/types/user';
import * as authApi from '@/api/auth';
import { getToken, setToken as saveToken, removeToken } from '@/utils/token';
import { getErrorMessage } from '@/utils/api-error';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: UserCreate) => Promise<void>;
  updateUser: (data: UserUpdate) => Promise<void>;
  showToast?: (type: 'success' | 'error' | 'info' | 'warning', message: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // 컴포넌트 마운트 시 토큰 확인 및 사용자 정보 조회
  useEffect(() => {
    const initAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          const userData = await authApi.getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          console.error('Failed to get user info:', error);
          removeToken();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const tokenData = await authApi.login({ email, password });
    saveToken(tokenData.access_token);

    const userData = await authApi.getCurrentUser(tokenData.access_token);
    setUser(userData);
  };

  const logout = () => {
    authApi.logout();
    setUser(null);
  };

  const register = async (data: UserCreate) => {
    await authApi.register(data);
    // 회원가입 후 자동 로그인
    await login(data.email, data.password);
  };

  const updateUser = async (data: UserUpdate) => {
    const token = getToken();
    if (!token) {
      throw new Error('인증 토큰이 없습니다.');
    }

    const updatedUser = await authApi.updateProfile(token, data);
    setUser(updatedUser);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    logout,
    register,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
