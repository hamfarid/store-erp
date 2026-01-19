import React, { Component } from 'react';
import { Link } from 'react-router-dom';

/**
 * ErrorBoundary Component
 * 
 * Catches JavaScript errors anywhere in the child component tree,
 * logs those errors, and displays a fallback UI.
 * 
 * Features:
 * - Catches render errors
 * - Logs errors to console (and optionally to error tracking service)
 * - Displays user-friendly error message
 * - Provides retry and navigation options
 * - Supports custom fallback components
 * - Error code detection for specific error pages
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      errorCode: null
    };
  }

  static getDerivedStateFromError(error) {
    // Update state to show fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error details
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    // Detect error code from error message or response
    let errorCode = 500; // Default to 500
    
    if (error.message) {
      const codeMatch = error.message.match(/(\d{3})/);
      if (codeMatch) {
        const code = parseInt(codeMatch[1]);
        if (code >= 400 && code < 600) {
          errorCode = code;
        }
      }
    }

    // Check for specific error types
    if (error.name === 'ChunkLoadError') {
      errorCode = 503;
    } else if (error.message?.includes('Network')) {
      errorCode = 502;
    } else if (error.message?.includes('unauthorized') || error.message?.includes('401')) {
      errorCode = 401;
    } else if (error.message?.includes('forbidden') || error.message?.includes('403')) {
      errorCode = 403;
    } else if (error.message?.includes('not found') || error.message?.includes('404')) {
      errorCode = 404;
    }

    this.setState({
      error,
      errorInfo,
      errorCode
    });

    // Optional: Send error to logging service
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Optional: Send to error tracking service (Sentry, etc.)
    // logErrorToService(error, errorInfo);
  }

  handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      errorCode: null
    });
  };

  render() {
    const { hasError, error, errorCode } = this.state;
    const { children, fallback, FallbackComponent, showDetails } = this.props;

    if (hasError) {
      // Use custom fallback if provided
      if (FallbackComponent) {
        return (
          <FallbackComponent
            error={error}
            errorCode={errorCode}
            resetError={this.handleRetry}
          />
        );
      }

      if (fallback) {
        return fallback;
      }

      // Default error UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-slate-800 to-zinc-900 p-4">
          <div className="max-w-lg w-full text-center">
            {/* Icon */}
            <div className="inline-flex items-center justify-center w-24 h-24 bg-red-600 rounded-full mb-6 shadow-2xl">
              <span className="text-5xl">⚠️</span>
            </div>

            {/* Error Code */}
            <h1 className="text-6xl font-bold text-white mb-4 drop-shadow-lg">
              {errorCode || 'خطأ'}
            </h1>

            {/* Title */}
            <h2 className="text-2xl font-bold text-white mb-4">
              حدث خطأ غير متوقع
            </h2>

            {/* Description */}
            <p className="text-gray-300 text-lg mb-8">
              نعتذر عن هذا الخطأ. يرجى المحاولة مرة أخرى أو العودة للصفحة الرئيسية.
            </p>

            {/* Error Details (Development only) */}
            {showDetails && error && (
              <div className="bg-black/30 rounded-xl p-4 mb-8 text-right overflow-auto max-h-40">
                <p className="text-red-400 text-sm font-mono break-all">
                  {error.toString()}
                </p>
              </div>
            )}

            {/* Actions */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={this.handleRetry}
                className="inline-flex items-center gap-2 bg-white hover:bg-gray-100 text-gray-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
              >
                <span>إعادة المحاولة</span>
                <span>🔄</span>
              </button>
              <Link
                to="/"
                className="inline-flex items-center gap-2 bg-transparent hover:bg-white/10 text-white font-bold py-3 px-8 rounded-xl transition border-2 border-white"
              >
                <span>الصفحة الرئيسية</span>
                <span>🏠</span>
              </Link>
            </div>

            {/* Error Reference */}
            <div className="mt-12 p-4 bg-black/20 rounded-xl">
              <p className="text-gray-400 text-sm font-mono">
                Error Code: {errorCode || 'UNKNOWN'}
              </p>
              <p className="text-gray-500 text-xs mt-2">
                Reference: {Math.random().toString(36).substring(7).toUpperCase()}
              </p>
            </div>
          </div>
        </div>
      );
    }

    return children;
  }
}

export default ErrorBoundary;

