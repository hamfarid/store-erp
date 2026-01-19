import React, { Suspense, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ErrorBoundary from '../ErrorBoundary/ErrorBoundary';

/**
 * Loading Spinner Component
 */
const LoadingSpinner = ({ message = 'جاري التحميل...' }) => (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-900 via-green-800 to-emerald-900">
    <div className="text-center">
      <div className="relative">
        <div className="w-20 h-20 border-4 border-green-200 border-opacity-20 rounded-full"></div>
        <div className="w-20 h-20 border-4 border-green-500 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
      </div>
      <p className="text-white text-lg mt-6">{message}</p>
    </div>
  </div>
);

/**
 * Error Fallback Component with navigation to specific error pages
 */
const ErrorFallback = ({ error, errorCode, resetError }) => {
  const navigate = useNavigate();

  useEffect(() => {
    // Navigate to specific error page based on error code
    if (errorCode && errorCode >= 400 && errorCode < 600) {
      const validCodes = [401, 402, 403, 404, 405, 406, 500, 501, 502, 503, 504, 505, 506];
      if (validCodes.includes(errorCode)) {
        navigate(`/${errorCode}`, { replace: true });
        return;
      }
    }
  }, [errorCode, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-900 via-red-800 to-orange-900 p-4">
      <div className="max-w-lg w-full text-center">
        <div className="inline-flex items-center justify-center w-24 h-24 bg-red-500 rounded-full mb-6 shadow-2xl animate-pulse">
          <span className="text-5xl">💥</span>
        </div>

        <h1 className="text-5xl font-bold text-white mb-4">خطأ!</h1>
        
        <p className="text-red-100 text-lg mb-8">
          حدث خطأ غير متوقع أثناء تحميل الصفحة.
          <br />
          يرجى المحاولة مرة أخرى.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={resetError}
            className="inline-flex items-center gap-2 bg-white hover:bg-red-50 text-red-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>إعادة المحاولة</span>
            <span>🔄</span>
          </button>
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center gap-2 bg-transparent hover:bg-white/10 text-white font-bold py-3 px-8 rounded-xl transition border-2 border-white"
          >
            <span>الصفحة الرئيسية</span>
            <span>🏠</span>
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * PageWrapper Component
 * 
 * Wraps each route with its own ErrorBoundary and Suspense.
 * Provides:
 * - Error boundary for catching render errors
 * - Suspense for lazy-loaded components
 * - Loading state handling
 * - Page title setting
 * - Error logging
 * 
 * @param {Object} props
 * @param {React.ReactNode} props.children - The page component to render
 * @param {string} props.title - Page title (optional)
 * @param {string} props.loadingMessage - Custom loading message (optional)
 * @param {boolean} props.showErrorDetails - Show error details in development (optional)
 * @param {Function} props.onError - Custom error handler (optional)
 */
const PageWrapper = ({
  children,
  title,
  loadingMessage,
  showErrorDetails = process.env.NODE_ENV === 'development',
  onError
}) => {
  const location = useLocation();

  // Update page title
  useEffect(() => {
    if (title) {
      document.title = `${title} | Gaara Scan AI`;
    }
  }, [title]);

  // Log page views
  useEffect(() => {
    console.log(`[PageWrapper] Navigated to: ${location.pathname}`);
  }, [location.pathname]);

  // Error handler
  const handleError = (error, errorInfo) => {
    console.error('[PageWrapper] Error caught:', {
      path: location.pathname,
      error: error.toString(),
      componentStack: errorInfo?.componentStack
    });

    // Call custom error handler if provided
    if (onError) {
      onError(error, errorInfo);
    }

    // Optional: Send to error tracking service
    // logErrorToService(error, errorInfo, { path: location.pathname });
  };

  return (
    <ErrorBoundary
      key={location.pathname} // Reset error boundary on route change
      onError={handleError}
      showDetails={showErrorDetails}
      FallbackComponent={ErrorFallback}
    >
      <Suspense fallback={<LoadingSpinner message={loadingMessage} />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
};

export default PageWrapper;

// Named exports for flexibility
export { LoadingSpinner, ErrorFallback, ErrorBoundary };

