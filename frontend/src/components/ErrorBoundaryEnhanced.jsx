/**
 * FILE: frontend/src/components/ErrorBoundaryEnhanced.jsx
 * PURPOSE: Robust error boundary with fallback UI, error reporting, and recovery options
 * OWNER: Frontend Team
 * RELATED: logger.js, traceId.js
 * LAST-AUDITED: 2025-10-23
 */

import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { logError, logEvent } from '../utils/logger';
import { getCurrentTraceId, formatTraceId } from '../utils/traceId';

class ErrorBoundaryEnhanced extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: null,
      isReporting: false,
      showDetails: false
    };
  }

  static getDerivedStateFromError(_error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    const errorId = `ERR_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const traceId = getCurrentTraceId();

    this.setState({
      error,
      errorInfo,
      errorId,
      traceId
    });

    // Log error with structured format
    logError(error, {
      errorId,
      traceId,
      componentStack: errorInfo.componentStack,
      severity: 'CRITICAL'
    });

    // Report to server
    this.reportErrorToServer(error, errorInfo, errorId, traceId);
  }

  reportErrorToServer = async (error, errorInfo, errorId, traceId) => {
    this.setState({ isReporting: true });

    try {
      const errorReport = {
        errorId,
        traceId,
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        url: window.location.href,
        userId: this.getUserId(),
        severity: 'CRITICAL'
      };

      const response = await fetch('/api/errors/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Trace-Id': traceId
        },
        body: JSON.stringify(errorReport)
      });

      if (response.ok) {
        logEvent('error_reported_successfully', { errorId, traceId });
      }
    } catch (reportError) {
      console.error('[ErrorBoundary] Failed to report error:', reportError);
      logEvent('error_report_failed', { errorId, traceId, reason: reportError.message });
    } finally {
      this.setState({ isReporting: false });
    }
  };

  getUserId = () => {
    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      return user.id || user.username || 'anonymous';
    } catch {
      return 'anonymous';
    }
  };

  handleReset = () => {
    logEvent('error_boundary_reset', { errorId: this.state.errorId });
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: null,
      showDetails: false
    });
  };

  handleReload = () => {
    logEvent('error_boundary_reload', { errorId: this.state.errorId });
    window.location.reload();
  };

  handleHome = () => {
    logEvent('error_boundary_navigate_home', { errorId: this.state.errorId });
    window.location.href = '/';
  };

  toggleDetails = () => {
    this.setState(prev => ({ showDetails: !prev.showDetails }));
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full p-8">
            {/* Header */}
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-red-100 rounded-full">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">حدث خطأ غير متوقع</h1>
                <p className="text-sm text-gray-600 mt-1">An unexpected error occurred</p>
              </div>
            </div>

            {/* Error Message */}
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800 font-mono text-sm break-words">
                {this.state.error?.message || 'Unknown error'}
              </p>
            </div>

            {/* Error ID and Trace ID */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Error ID</p>
                <p className="text-sm font-mono text-gray-900 break-all">
                  {this.state.errorId}
                </p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Trace ID</p>
                <p className="text-sm font-mono text-gray-900">
                  {formatTraceId(this.state.traceId)}
                </p>
              </div>
            </div>

            {/* Details Toggle */}
            <button
              onClick={this.toggleDetails}
              className="text-sm text-blue-600 hover:text-blue-800 mb-4 font-medium"
            >
              {this.state.showDetails ? '▼ إخفاء التفاصيل' : '▶ عرض التفاصيل'}
            </button>

            {/* Stack Trace */}
            {this.state.showDetails && (
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg mb-6 overflow-auto max-h-64 text-xs font-mono">
                <p className="text-red-400 mb-2">Stack Trace:</p>
                <pre className="whitespace-pre-wrap break-words">
                  {this.state.error?.stack}
                </pre>
                {this.state.errorInfo?.componentStack && (
                  <>
                    <p className="text-yellow-400 mt-4 mb-2">Component Stack:</p>
                    <pre className="whitespace-pre-wrap break-words">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </>
                )}
              </div>
            )}

            {/* Status Message */}
            {this.state.isReporting && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
                <p className="text-blue-800 text-sm">
                  جاري إرسال تقرير الخطأ... Sending error report...
                </p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3 flex-wrap">
              <button
                onClick={this.handleReset}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                إعادة محاولة
              </button>
              <button
                onClick={this.handleReload}
                className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                تحديث الصفحة
              </button>
              <button
                onClick={this.handleHome}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Home className="w-4 h-4" />
                الصفحة الرئيسية
              </button>
            </div>

            {/* Help Text */}
            <p className="text-xs text-gray-600 mt-6 text-center">
              إذا استمرت المشكلة، يرجى التواصل مع الدعم الفني مع ذكر معرف الخطأ أعلاه
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundaryEnhanced;

