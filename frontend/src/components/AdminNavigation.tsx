'use client';

import Link from 'next/link';
import { useAdminAuth } from '@/contexts/AdminAuthContext';
import { useToast } from '@/contexts/ToastContext';

export default function AdminNavigation() {
  const { admin, isAuthenticated, logout } = useAdminAuth();
  const { success, error } = useToast();

  const handleLogout = async () => {
    try {
      await logout();
      success('로그아웃되었습니다');
    } catch (err) {
      error('로그아웃 중 오류가 발생했습니다');
    }
  };

  return (
    <nav className="bg-gray-800 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/admin/dashboard" className="text-xl font-bold">
          🔐 Admin Panel
        </Link>

        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <Link href="/admin/dashboard" className="hover:text-gray-300">
                대시보드
              </Link>
              {admin?.role === 'super_admin' && (
                <Link href="/admin/users" className="hover:text-gray-300">
                  관리자 관리
                </Link>
              )}
              <span className="text-gray-400">
                {admin?.username} ({admin?.role})
              </span>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
              >
                로그아웃
              </button>
            </>
          ) : (
            <Link href="/admin/login" className="hover:text-gray-300">
              로그인
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
