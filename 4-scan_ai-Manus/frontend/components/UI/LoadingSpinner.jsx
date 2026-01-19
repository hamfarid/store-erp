// ملف: /home/ubuntu/gaara-ai-system/gaara_ai_integrated/frontend/src/components/UI/LoadingSpinner.jsx
// مكون مؤشر التحميل لنظام Gaara AI
// الإصدار: 2.0.0
// تم التحديث: 2025-01-21

import React from 'react';
import { useApp } from '../../App';

const LoadingSpinner = ({ size = 'medium', text = null, fullScreen = false }) => {
  const { language } = useApp();

  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12',
    xlarge: 'w-16 h-16'
  };

  const defaultText = language === 'ar' ? 'جاري التحميل...' : 'Loading...';
  const displayText = text || defaultText;

  const spinnerContent = (
    <div className="flex flex-col items-center justify-center space-y-3">
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-gray-200 dark:border-gray-700 rounded-full animate-spin`}>
          <div className="absolute top-0 left-0 w-full h-full border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
        </div>
      </div>
      
      {displayText && (
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
            {displayText}
          </p>
        </div>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white dark:bg-gray-900 bg-opacity-80 dark:bg-opacity-80 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 max-w-sm w-full mx-4">
          {spinnerContent}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center p-4">
      {spinnerContent}
    </div>
  );
};

// مكون تحميل مبسط للاستخدام داخل الأزرار
export const ButtonSpinner = ({ className = '' }) => (
  <div className={`inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin ${className}`}></div>
);

// مكون تحميل للصفحات
export const PageLoader = ({ message }) => {
  const { language } = useApp();
  const defaultMessage = language === 'ar' ? 'جاري تحميل الصفحة...' : 'Loading page...';
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <LoadingSpinner size="large" text={message || defaultMessage} />
    </div>
  );
};

// مكون تحميل للبيانات
export const DataLoader = ({ message, className = '' }) => {
  const { language } = useApp();
  const defaultMessage = language === 'ar' ? 'جاري تحميل البيانات...' : 'Loading data...';
  
  return (
    <div className={`flex items-center justify-center py-8 ${className}`}>
      <LoadingSpinner size="medium" text={message || defaultMessage} />
    </div>
  );
};

// مكون تحميل مصغر
export const MiniLoader = ({ className = '' }) => (
  <div className={`inline-flex items-center space-x-2 rtl:space-x-reverse ${className}`}>
    <div className="w-3 h-3 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
  </div>
);

export default LoadingSpinner;
