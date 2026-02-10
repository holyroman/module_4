'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { Admin, AdminLogin } from '@/types/admin';
import { adminLogin, adminLogout, getCurrentAdmin } from '@/api/admin';
import { getAdminToken, setAdminToken, removeAdminToken } from '@/utils/admin-token';
import { getErrorMessage } from '@/utils/api-error';

interface AdminAuthContextType {
  admin: Admin | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AdminAuthContext = createContext<AdminAuthContextType | undefined>(undefined);

export function AdminAuthProvider({ children }: { children: React.ReactNode }) {
  const [admin, setAdmin] = useState<Admin | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAdminToken();
    if (token) {
      getCurrentAdmin(token)
        .then(setAdmin)
        .catch(() => removeAdminToken())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const tokenData = await adminLogin({ email, password });
    setAdminToken(tokenData.access_token);
    const adminData = await getCurrentAdmin(tokenData.access_token);
    setAdmin(adminData);
  };

  const logout = async () => {
    await adminLogout();
    removeAdminToken();
    setAdmin(null);
  };

  return (
    <AdminAuthContext.Provider value={{ admin, isAuthenticated: !!admin, loading, login, logout }}>
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const context = useContext(AdminAuthContext);
  if (!context) throw new Error('useAdminAuth must be used within AdminAuthProvider');
  return context;
}
