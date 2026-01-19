/**
 * Toast Notification Component
 * =============================
 * 
 * Beautiful, accessible toast notifications with bilingual support.
 * Features smooth animations, auto-dismiss, and stacking.
 * 
 * Features:
 * - Multiple toast types (success, error, warning, info)
 * - Auto-dismiss with progress bar
 * - Manual dismiss
 * - Stacking support
 * - RTL/LTR aware
 * - Dark mode support
 * - Keyboard accessible
 * 
 * @author Global System v35.0
 * @date 2026-01-17
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { X, CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react';

// ============================================
// Toast Context
// ============================================

const ToastContext = createContext(null);

/**
 * Hook to use toast notifications
 * 
 * @returns {Object} Toast utilities
 * 
 * @example
 * const { toast, success, error } = useToast();
 * success('Operation completed!');
 * error('Something went wrong');
 */
export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// ============================================
// Toast Item Component
// ============================================

const ToastItem = ({ 
  id, 
  type, 
  title, 
  message,
  duration,
  onDismiss,
  showProgress
}) => {
  const [progress, setProgress] = useState(100);
  const [isExiting, setIsExiting] = useState(false);

  // Icon configuration
  const icons = {
    success: <CheckCircle className="w-5 h-5" />,
    error: <XCircle className="w-5 h-5" />,
    warning: <AlertTriangle className="w-5 h-5" />,
    info: <Info className="w-5 h-5" />
  };

  // Color configuration
  const colors = {
    success: {
      bg: 'bg-emerald-50 dark:bg-emerald-900/30',
      border: 'border-emerald-200 dark:border-emerald-700',
      icon: 'text-emerald-500 dark:text-emerald-400',
      progress: 'bg-emerald-500'
    },
    error: {
      bg: 'bg-red-50 dark:bg-red-900/30',
      border: 'border-red-200 dark:border-red-700',
      icon: 'text-red-500 dark:text-red-400',
      progress: 'bg-red-500'
    },
    warning: {
      bg: 'bg-amber-50 dark:bg-amber-900/30',
      border: 'border-amber-200 dark:border-amber-700',
      icon: 'text-amber-500 dark:text-amber-400',
      progress: 'bg-amber-500'
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/30',
      border: 'border-blue-200 dark:border-blue-700',
      icon: 'text-blue-500 dark:text-blue-400',
      progress: 'bg-blue-500'
    }
  };

  const colorConfig = colors[type] || colors.info;

  // Auto-dismiss timer
  useEffect(() => {
    if (duration <= 0) return;

    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev - (100 / (duration / 100));
        if (newProgress <= 0) {
          clearInterval(interval);
          handleDismiss();
          return 0;
        }
        return newProgress;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [duration]);

  const handleDismiss = useCallback(() => {
    setIsExiting(true);
    setTimeout(() => onDismiss(id), 300);
  }, [id, onDismiss]);

  return (
    <div
      role="alert"
      aria-live="polite"
      className={`
        relative overflow-hidden
        w-full max-w-sm p-4 rounded-xl shadow-lg
        border ${colorConfig.border} ${colorConfig.bg}
        transform transition-all duration-300 ease-out
        ${isExiting 
          ? 'opacity-0 translate-x-full rtl:-translate-x-full scale-95' 
          : 'opacity-100 translate-x-0 scale-100'
        }
      `}
    >
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className={`flex-shrink-0 ${colorConfig.icon}`}>
          {icons[type]}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {title && (
            <h4 className="font-semibold text-gray-900 dark:text-white text-sm">
              {title}
            </h4>
          )}
          {message && (
            <p className="text-sm text-gray-600 dark:text-gray-300 mt-0.5">
              {message}
            </p>
          )}
        </div>

        {/* Dismiss button */}
        <button
          onClick={handleDismiss}
          className={`
            flex-shrink-0 p-1 rounded-lg
            text-gray-400 hover:text-gray-600
            dark:text-gray-500 dark:hover:text-gray-300
            hover:bg-gray-200/50 dark:hover:bg-gray-700/50
            transition-colors duration-150
            focus:outline-none focus:ring-2 focus:ring-offset-2
            focus:ring-${type === 'error' ? 'red' : type === 'success' ? 'emerald' : 'blue'}-500
          `}
          aria-label="Dismiss notification"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Progress bar */}
      {showProgress && duration > 0 && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-200/50 dark:bg-gray-700/50">
          <div
            className={`h-full ${colorConfig.progress} transition-all duration-100 ease-linear`}
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
};

// ============================================
// Toast Container Component
// ============================================

const ToastContainer = ({ toasts, onDismiss, position }) => {
  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'top-center': 'top-4 left-1/2 -translate-x-1/2',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-center': 'bottom-4 left-1/2 -translate-x-1/2'
  };

  // RTL adjustment
  const isRTL = document.documentElement.dir === 'rtl';
  let adjustedPosition = position;
  if (isRTL) {
    adjustedPosition = position.replace('right', 'temp').replace('left', 'right').replace('temp', 'left');
  }

  return (
    <div
      className={`
        fixed z-50 ${positionClasses[adjustedPosition]}
        flex flex-col gap-3
        pointer-events-none
      `}
      aria-label="Notifications"
    >
      {toasts.map(toast => (
        <div key={toast.id} className="pointer-events-auto">
          <ToastItem
            {...toast}
            onDismiss={onDismiss}
          />
        </div>
      ))}
    </div>
  );
};

// ============================================
// Toast Provider Component
// ============================================

/**
 * Toast Provider Component
 * 
 * Wrap your app with this provider to enable toast notifications.
 * 
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * @param {string} props.position - Toast position
 * @param {number} props.defaultDuration - Default auto-dismiss time (ms)
 * @param {number} props.maxToasts - Maximum visible toasts
 * 
 * @example
 * <ToastProvider position="top-right">
 *   <App />
 * </ToastProvider>
 */
export const ToastProvider = ({ 
  children,
  position = 'top-right',
  defaultDuration = 5000,
  maxToasts = 5,
  showProgress = true
}) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((toast) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    setToasts(prev => {
      const newToasts = [
        { 
          id, 
          duration: defaultDuration,
          showProgress,
          ...toast 
        }, 
        ...prev
      ];
      
      // Limit max toasts
      if (newToasts.length > maxToasts) {
        return newToasts.slice(0, maxToasts);
      }
      
      return newToasts;
    });

    return id;
  }, [defaultDuration, maxToasts, showProgress]);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setToasts([]);
  }, []);

  // Convenience methods
  const success = useCallback((message, options = {}) => {
    return addToast({ 
      type: 'success', 
      message,
      title: options.title || 'نجاح / Success',
      ...options 
    });
  }, [addToast]);

  const error = useCallback((message, options = {}) => {
    return addToast({ 
      type: 'error', 
      message,
      title: options.title || 'خطأ / Error',
      duration: options.duration || 7000, // Errors stay longer
      ...options 
    });
  }, [addToast]);

  const warning = useCallback((message, options = {}) => {
    return addToast({ 
      type: 'warning', 
      message,
      title: options.title || 'تحذير / Warning',
      ...options 
    });
  }, [addToast]);

  const info = useCallback((message, options = {}) => {
    return addToast({ 
      type: 'info', 
      message,
      title: options.title || 'معلومة / Info',
      ...options 
    });
  }, [addToast]);

  // Promise-based toast (useful for async operations)
  const promise = useCallback((
    promiseFn,
    { 
      loading = 'جاري التحميل... / Loading...',
      success: successMsg = 'تمت العملية بنجاح / Success!',
      error: errorMsg = 'حدث خطأ / Error occurred'
    } = {}
  ) => {
    const id = addToast({
      type: 'info',
      message: loading,
      duration: 0 // Don't auto-dismiss
    });

    promiseFn
      .then(() => {
        removeToast(id);
        addToast({
          type: 'success',
          message: successMsg
        });
      })
      .catch((err) => {
        removeToast(id);
        addToast({
          type: 'error',
          message: err?.message || errorMsg,
          duration: 7000
        });
      });

    return id;
  }, [addToast, removeToast]);

  const contextValue = {
    toasts,
    toast: addToast,
    dismiss: removeToast,
    clearAll,
    success,
    error,
    warning,
    info,
    promise
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      <ToastContainer 
        toasts={toasts} 
        onDismiss={removeToast}
        position={position}
      />
    </ToastContext.Provider>
  );
};

// ============================================
// Standalone Toast Component (without context)
// ============================================

/**
 * Standalone toast component for simple use cases
 * 
 * @param {Object} props
 * @param {boolean} props.show - Whether to show the toast
 * @param {string} props.type - Toast type
 * @param {string} props.title - Toast title
 * @param {string} props.message - Toast message
 * @param {Function} props.onClose - Close handler
 */
export const Toast = ({
  show = false,
  type = 'info',
  title,
  message,
  onClose,
  duration = 5000,
  position = 'top-right'
}) => {
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    setVisible(show);
  }, [show]);

  useEffect(() => {
    if (visible && duration > 0) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [visible, duration, onClose]);

  if (!visible) return null;

  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4'
  };

  return (
    <div className={`fixed z-50 ${positionClasses[position]}`}>
      <ToastItem
        id="standalone"
        type={type}
        title={title}
        message={message}
        duration={duration}
        showProgress={true}
        onDismiss={() => {
          setVisible(false);
          onClose?.();
        }}
      />
    </div>
  );
};

export default Toast;
