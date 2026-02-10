'use client';

import AdminProtectedRoute from '@/components/AdminProtectedRoute';
import AdminNavigation from '@/components/AdminNavigation';
import { useAdminAuth } from '@/contexts/AdminAuthContext';

export default function AdminDashboard() {
  const { admin } = useAdminAuth();

  return (
    <AdminProtectedRoute>
      <AdminNavigation />
      <div className="max-w-7xl mx-auto p-8">
        <h1 className="text-3xl font-bold mb-6">관리자 대시보드</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">환영합니다!</h2>
            <p className="text-gray-600">
              {admin?.username} ({admin?.role})
            </p>
          </div>

          <div className="bg-blue-100 p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">계정 상태</h2>
            <p className={admin?.is_active ? 'text-green-600' : 'text-red-600'}>
              {admin?.is_active ? '활성' : '비활성'}
            </p>
          </div>

          <div className="bg-green-100 p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">권한</h2>
            <p className="text-gray-700">
              {admin?.role === 'super_admin' ? '슈퍼 관리자' : '일반 관리자'}
            </p>
          </div>
        </div>

        <div className="mt-8 bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">관리자 정보</h2>
          <dl className="space-y-2">
            <div className="flex">
              <dt className="font-semibold w-32">ID:</dt>
              <dd>{admin?.id}</dd>
            </div>
            <div className="flex">
              <dt className="font-semibold w-32">이메일:</dt>
              <dd>{admin?.email}</dd>
            </div>
            <div className="flex">
              <dt className="font-semibold w-32">가입일:</dt>
              <dd>{admin?.created_at ? new Date(admin.created_at).toLocaleDateString('ko-KR') : ''}</dd>
            </div>
          </dl>
        </div>
      </div>
    </AdminProtectedRoute>
  );
}
