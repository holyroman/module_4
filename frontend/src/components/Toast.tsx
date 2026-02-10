import { Toast as ToastType } from '@/types/toast';

interface ToastProps {
  toast: ToastType;
  onClose: () => void;
}

export default function Toast({ toast, onClose }: ToastProps) {
  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
  }[toast.type];

  const icon = {
    success: '✓',
    error: '✕',
    info: 'ⓘ',
    warning: '⚠',
  }[toast.type];

  return (
    <div
      className={`${bgColor} text-white px-6 py-4 rounded-lg shadow-lg flex items-center justify-between mb-2 animate-slide-in min-w-[300px] max-w-[500px]`}
    >
      <div className="flex items-center gap-3">
        <span className="text-xl font-bold">{icon}</span>
        <span className="text-sm font-medium">{toast.message}</span>
      </div>
      <button
        onClick={onClose}
        className="ml-4 text-white hover:text-gray-200 text-2xl font-bold leading-none"
        aria-label="닫기"
      >
        ×
      </button>
    </div>
  );
}
