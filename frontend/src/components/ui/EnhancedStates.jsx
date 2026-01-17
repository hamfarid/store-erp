/**
 * Enhanced UI States Component
 * 
 * Provides improved Loading, Error, Empty, and Success states
 * with better UX and Arabic support
 * 
 * Date: 2025-01-25
 * Phase: 2 - Component Improvements
 */

import React from 'react';
import { 
  Loader2, AlertCircle, CheckCircle, Info, 
  RefreshCw, Package, Users, FileText, Inbox,
  TrendingUp, ShoppingCart, Database, Settings
} from 'lucide-react';

/**
 * Enhanced Loading State
 * Shows a spinner with optional message
 */
export const LoadingState = ({ 
  message = 'جاري التحميل...', 
  size = 'medium',
  fullScreen = false 
}) => {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  };

  const containerClasses = fullScreen
    ? 'fixed inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50'
    : 'flex flex-col items-center justify-center py-12';

  return (
    <div className={containerClasses}>
      <Loader2 className={`${sizeClasses[size]} text-primary-600 dark:text-primary-400 animate-spin`} />
      {message && (
        <p className="mt-4 text-gray-600 dark:text-gray-400 text-center font-medium">
          {message}
        </p>
      )}
    </div>
  );
};

/**
 * Enhanced Error State
 * Shows error message with retry button
 */
export const ErrorState = ({ 
  title = 'حدث خطأ',
  message = 'عذراً، حدث خطأ أثناء تحميل البيانات',
  onRetry,
  showRetry = true,
  icon: IconComponent = AlertCircle
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="bg-red-50 dark:bg-red-900/20 rounded-full p-4 mb-4">
        <IconComponent className="w-12 h-12 text-red-600 dark:text-red-400" />
      </div>
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400 text-center max-w-md mb-6">
        {message}
      </p>
      {showRetry && onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
        >
          <RefreshCw className="w-5 h-5" />
          إعادة المحاولة
        </button>
      )}
    </div>
  );
};

/**
 * Enhanced Empty State
 * Shows when no data is available
 */
export const EmptyState = ({ 
  title = 'لا توجد بيانات',
  message = 'لم يتم العثور على أي بيانات',
  icon: IconComponent = Inbox,
  actionLabel,
  onAction,
  showAction = false
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="bg-gray-100 dark:bg-gray-800 rounded-full p-6 mb-4">
        <IconComponent className="w-16 h-16 text-gray-400 dark:text-gray-600" />
      </div>
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400 text-center max-w-md mb-6">
        {message}
      </p>
      {showAction && onAction && actionLabel && (
        <button
          onClick={onAction}
          className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};

/**
 * Enhanced Success State
 * Shows success message
 */
export const SuccessState = ({ 
  title = 'تمت العملية بنجاح',
  message,
  onClose,
  autoClose = false,
  autoCloseDelay = 3000
}) => {
  React.useEffect(() => {
    if (autoClose && onClose) {
      const timer = setTimeout(onClose, autoCloseDelay);
      return () => clearTimeout(timer);
    }
  }, [autoClose, onClose, autoCloseDelay]);

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="bg-green-50 dark:bg-green-900/20 rounded-full p-4 mb-4">
        <CheckCircle className="w-12 h-12 text-green-600 dark:text-green-400" />
      </div>
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      {message && (
        <p className="text-gray-600 dark:text-gray-400 text-center max-w-md">
          {message}
        </p>
      )}
    </div>
  );
};

/**
 * Skeleton Loader
 * Shows placeholder while content is loading
 */
export const SkeletonLoader = ({ rows = 5, columns = 4 }) => {
  return (
    <div className="animate-pulse space-y-4">
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="flex gap-4">
          {Array.from({ length: columns }).map((_, colIndex) => (
            <div
              key={colIndex}
              className="h-12 bg-gray-200 dark:bg-gray-700 rounded flex-1"
            />
          ))}
        </div>
      ))}
    </div>
  );
};

// Export all components
export default {
  LoadingState,
  ErrorState,
  EmptyState,
  SuccessState,
  SkeletonLoader
};

