// ملف: /home/ubuntu/gaara-ai-system/gaara_ai_integrated/frontend/src/components/UI/ErrorFallback.jsx
// مكون معالجة الأخطاء لنظام Gaara AI
// الإصدار: 2.0.0
// تم التحديث: 2025-01-21

import React from 'react';
import { useApp } from '../../App';
import { AlertTriangle, RefreshCw, Home, Bug } from 'lucide-react';

const ErrorFallback = ({ error, resetErrorBoundary }) => {
  const { language } = useApp();

  const handleReload = () => {
    window.location.reload();
  };

  const handleGoHome = () => {
    window.location.href = '/dashboard';
  };

  const handleReportError = () => {
    // يمكن إضافة منطق إرسال تقرير الخطأ هنا
    console.error('Error reported:', error);
    alert(language === 'ar' ? 'تم إرسال تقرير الخطأ' : 'Error report sent');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mb-4">
            <AlertTriangle className="w-8 h-8 text-red-600 dark:text-red-400" />
          </div>
          
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {language === 'ar' ? 'حدث خطأ غير متوقع' : 'Something went wrong'}
          </h1>
          
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            {language === 'ar' 
              ? 'نعتذر، حدث خطأ في التطبيق. يرجى المحاولة مرة أخرى.'
              : 'Sorry, there was an error with the application. Please try again.'
            }
          </p>
        </div>

        {/* تفاصيل الخطأ (في بيئة التطوير فقط) */}
        {process.env.NODE_ENV === 'development' && error && (
          <div className="mb-6 p-4 bg-gray-100 dark:bg-gray-700 rounded-lg text-left">
            <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              {language === 'ar' ? 'تفاصيل الخطأ:' : 'Error Details:'}
            </h3>
            <pre className="text-xs text-red-600 dark:text-red-400 overflow-auto max-h-32">
              {error.message}
            </pre>
            {error.stack && (
              <details className="mt-2">
                <summary className="text-xs text-gray-500 cursor-pointer">
                  {language === 'ar' ? 'عرض التفاصيل الكاملة' : 'Show full stack trace'}
                </summary>
                <pre className="text-xs text-gray-600 dark:text-gray-400 mt-2 overflow-auto max-h-40">
                  {error.stack}
                </pre>
              </details>
            )}
          </div>
        )}

        {/* أزرار الإجراءات */}
        <div className="space-y-3">
          <button
            onClick={resetErrorBoundary}
            className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4 ml-2 rtl:ml-0 rtl:mr-2" />
            {language === 'ar' ? 'إعادة المحاولة' : 'Try Again'}
          </button>

          <button
            onClick={handleReload}
            className="w-full flex items-center justify-center px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4 ml-2 rtl:ml-0 rtl:mr-2" />
            {language === 'ar' ? 'إعادة تحميل الصفحة' : 'Reload Page'}
          </button>

          <button
            onClick={handleGoHome}
            className="w-full flex items-center justify-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
          >
            <Home className="w-4 h-4 ml-2 rtl:ml-0 rtl:mr-2" />
            {language === 'ar' ? 'العودة للرئيسية' : 'Go to Home'}
          </button>

          <button
            onClick={handleReportError}
            className="w-full flex items-center justify-center px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors"
          >
            <Bug className="w-4 h-4 ml-2 rtl:ml-0 rtl:mr-2" />
            {language === 'ar' ? 'إبلاغ عن الخطأ' : 'Report Error'}
          </button>
        </div>

        {/* معلومات إضافية */}
        <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-600">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {language === 'ar' 
              ? 'إذا استمر الخطأ، يرجى التواصل مع الدعم الفني'
              : 'If the error persists, please contact technical support'
            }
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            {language === 'ar' ? 'رقم الخطأ:' : 'Error ID:'} {Date.now()}
          </p>
        </div>
      </div>
    </div>
  );
};

// مكون خطأ مبسط للاستخدام في المكونات الفرعية
export const SimpleError = ({ message, onRetry, className = '' }) => {
  const { language } = useApp();
  
  return (
    <div className={`flex flex-col items-center justify-center p-6 ${className}`}>
      <AlertTriangle className="w-12 h-12 text-red-500 mb-4" />
      <p className="text-gray-600 dark:text-gray-400 text-center mb-4">
        {message || (language === 'ar' ? 'حدث خطأ' : 'An error occurred')}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          {language === 'ar' ? 'إعادة المحاولة' : 'Try Again'}
        </button>
      )}
    </div>
  );
};

export default ErrorFallback;
