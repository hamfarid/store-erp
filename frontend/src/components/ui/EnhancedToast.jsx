/**
 * Enhanced Toast Notifications
 * 
 * Wrapper around react-hot-toast with better Arabic support
 * and consistent styling
 * 
 * Date: 2025-01-25
 * Phase: 2 - Component Improvements
 */

import { toast as hotToast } from 'react-hot-toast';
import { CheckCircle, AlertCircle, Info, AlertTriangle, X } from 'lucide-react';

/**
 * Toast Configuration
 */
const defaultConfig = {
  duration: 4000,
  position: 'top-center',
  style: {
    background: '#fff',
    color: '#1f2937',
    padding: '16px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    maxWidth: '500px',
    direction: 'rtl',
    fontFamily: 'Cairo, sans-serif'
  }
};

/**
 * Custom Toast Component
 */
const ToastContent = ({ icon: Icon, iconColor, title, message, onClose }) => (
  <div className="flex items-start gap-3">
    <div className={`flex-shrink-0 ${iconColor}`}>
      <Icon className="w-6 h-6" />
    </div>
    <div className="flex-1 min-w-0">
      {title && (
        <p className="font-bold text-gray-900 dark:text-white mb-1">
          {title}
        </p>
      )}
      <p className="text-sm text-gray-600 dark:text-gray-400">
        {message}
      </p>
    </div>
    {onClose && (
      <button
        onClick={onClose}
        className="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        <X className="w-5 h-5" />
      </button>
    )}
  </div>
);

/**
 * Enhanced Toast Functions
 */
export const toast = {
  /**
   * Success Toast
   */
  success: (message, options = {}) => {
    return hotToast.custom(
      (t) => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border-r-4 border-green-500">
          <ToastContent
            icon={CheckCircle}
            iconColor="text-green-500"
            title={options.title || 'نجح'}
            message={message}
            onClose={() => hotToast.dismiss(t.id)}
          />
        </div>
      ),
      { ...defaultConfig, ...options }
    );
  },

  /**
   * Error Toast
   */
  error: (message, options = {}) => {
    return hotToast.custom(
      (t) => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border-r-4 border-red-500">
          <ToastContent
            icon={AlertCircle}
            iconColor="text-red-500"
            title={options.title || 'خطأ'}
            message={message}
            onClose={() => hotToast.dismiss(t.id)}
          />
        </div>
      ),
      { ...defaultConfig, duration: 5000, ...options }
    );
  },

  /**
   * Warning Toast
   */
  warning: (message, options = {}) => {
    return hotToast.custom(
      (t) => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border-r-4 border-yellow-500">
          <ToastContent
            icon={AlertTriangle}
            iconColor="text-yellow-500"
            title={options.title || 'تحذير'}
            message={message}
            onClose={() => hotToast.dismiss(t.id)}
          />
        </div>
      ),
      { ...defaultConfig, ...options }
    );
  },

  /**
   * Info Toast
   */
  info: (message, options = {}) => {
    return hotToast.custom(
      (t) => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border-r-4 border-blue-500">
          <ToastContent
            icon={Info}
            iconColor="text-blue-500"
            title={options.title || 'معلومة'}
            message={message}
            onClose={() => hotToast.dismiss(t.id)}
          />
        </div>
      ),
      { ...defaultConfig, ...options }
    );
  },

  /**
   * Loading Toast
   */
  loading: (message, options = {}) => {
    return hotToast.loading(message, {
      ...defaultConfig,
      ...options,
      style: {
        ...defaultConfig.style,
        ...options.style
      }
    });
  },

  /**
   * Promise Toast
   * Automatically shows loading, success, or error based on promise
   */
  promise: (promise, messages, options = {}) => {
    return hotToast.promise(
      promise,
      {
        loading: messages.loading || 'جاري المعالجة...',
        success: messages.success || 'تمت العملية بنجاح',
        error: messages.error || 'حدث خطأ'
      },
      { ...defaultConfig, ...options }
    );
  },

  /**
   * Dismiss a specific toast
   */
  dismiss: (toastId) => {
    hotToast.dismiss(toastId);
  },

  /**
   * Dismiss all toasts
   */
  dismissAll: () => {
    hotToast.dismiss();
  }
};

export default toast;

