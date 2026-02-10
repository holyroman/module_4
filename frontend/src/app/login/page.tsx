'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useToast } from '@/contexts/ToastContext';
import { getErrorMessage } from '@/utils/api-error';
import * as authApi from '@/api/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { success, error: showError } = useToast();
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await authApi.login({ email, password });

      // 2FA가 필요한 경우
      if (response.requires_2fa) {
        if (!response.temp_token) {
          throw new Error('임시 토큰을 받지 못했습니다.');
        }
        // 임시 토큰을 세션 스토리지에 저장하고 2FA 화면으로 이동
        sessionStorage.setItem('temp_token', response.temp_token);
        router.push('/auth/verify-2fa');
        return;
      }

      // 2FA가 필요없는 경우 바로 로그인 처리
      if (response.access_token) {
        const { setToken } = await import('@/utils/token');
        setToken(response.access_token);
        success('로그인 성공!');
        router.push('/');
      } else {
        throw new Error('토큰을 받지 못했습니다.');
      }
    } catch (err) {
      showError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full mx-4">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">
          로그인
        </h1>
        <p className="text-gray-600 text-center mb-8">
          계정에 로그인하세요
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              이메일
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              비밀번호
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
              placeholder="비밀번호"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            계정이 없으신가요?{' '}
            <Link href="/register" className="text-indigo-600 hover:text-indigo-700 font-medium">
              회원가입
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
