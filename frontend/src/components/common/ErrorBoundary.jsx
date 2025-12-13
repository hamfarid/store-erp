import React from 'react'
import PropTypes from 'prop-types'
import './ErrorBoundary.css'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null,
      errorId: null
    }
  }

  static getDerivedStateFromError(_error) {
    return { 
      hasError: true,
      errorId: Date.now().toString(36) + Math.random().toString(36).substring(2)
    }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    })

    // تسجيل الخطأ للمراقبة
    // يمكن إرسال الخطأ لخدمة المراقبة
    this.logErrorToService(error, errorInfo)
  }

  logErrorToService = (error, errorInfo) => {
    try {
      // إرسال تقرير الخطأ للخادم
      fetch('/api/errors/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: error.toString(),
          errorInfo: errorInfo.componentStack,
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href,
          errorId: this.state.errorId
        })
      }).catch(_ => { /* Error reporting failed */ })
    } catch (_) {
      /* Fallback failed silently */
    }
  }

  handleReload = () => {
    window.location.reload()
  }

  handleGoBack = () => {
    window.history.back()
  }

  handleReportError = () => {
    const errorReport = {
      error: this.state.error?.toString(),
      errorId: this.state.errorId,
      timestamp: new Date().toISOString()
    }
    
    const mailtoLink = `mailto:support@company.com?subject=خطأ في النظام - ${this.state.errorId}&body=${encodeURIComponent(JSON.stringify(errorReport, null, 2))}`
    window.open(mailtoLink)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-boundary__container">
            <div className="error-boundary__icon">
              <i className="fas fa-exclamation-triangle"></i>
            </div>
            
            <h1 className="error-boundary__title">
              عذراً، حدث خطأ غير متوقع
            </h1>
            
            <p className="error-boundary__message">
              لقد واجه التطبيق مشكلة تقنية. نعتذر عن الإزعاج.
            </p>
            
            <div className="error-boundary__details">
              <p><strong>رقم الخطأ:</strong> {this.state.errorId}</p>
              <p><strong>الوقت:</strong> {new Date().toLocaleString('ar-EG')}</p>
            </div>

            <div className="error-boundary__actions">
              <button 
                className="error-boundary__button error-boundary__button--primary"
                onClick={this.handleReload}
              >
                <i className="fas fa-sync-alt"></i>
                إعادة تحميل الصفحة
              </button>
              
              <button 
                className="error-boundary__button error-boundary__button--secondary"
                onClick={this.handleGoBack}
              >
                <i className="fas fa-arrow-left"></i>
                العودة للخلف
              </button>
              
              <button 
                className="error-boundary__button error-boundary__button--outline"
                onClick={this.handleReportError}
              >
                <i className="fas fa-bug"></i>
                إبلاغ عن المشكلة
              </button>
            </div>

            {import.meta.env.DEV && (
              <details className="error-boundary__debug">
                <summary>تفاصيل تقنية (للمطورين)</summary>
                <div className="error-boundary__debug-content">
                  <h4>الخطأ:</h4>
                  <pre>{this.state.error && this.state.error.toString()}</pre>
                  
                  <h4>معلومات المكون:</h4>
                  <pre>{this.state.errorInfo.componentStack}</pre>
                </div>
              </details>
            )}
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// مكون Error Fallback للاستخدام مع React Error Boundary
export const ErrorFallback = ({ error, resetErrorBoundary, errorInfo: _errorInfo }) => (
  <div className="error-fallback">
    <div className="error-fallback__content">
      <h2>حدث خطأ في هذا القسم</h2>
      <p>نعتذر عن الإزعاج. يرجى المحاولة مرة أخرى.</p>
      
      <div className="error-fallback__actions">
        <button onClick={resetErrorBoundary} className="error-fallback__retry">
          المحاولة مرة أخرى
        </button>
      </div>
      
      {import.meta.env.DEV && (
        <details className="error-fallback__details">
          <summary>تفاصيل الخطأ</summary>
          <pre>{error.message}</pre>
        </details>
      )}
    </div>
  </div>
)

// Hook للتعامل مع الأخطاء
export const useErrorHandler = () => {
  const [error, setError] = React.useState(null)

  const handleError = React.useCallback((error, errorInfo = {}) => {
    setError({ error, errorInfo, timestamp: new Date() })
  }, [])

  const clearError = React.useCallback(() => {
    setError(null)
  }, [])

  return { error, handleError, clearError }
}

export default ErrorBoundary

ErrorFallback.propTypes = {
  error: PropTypes.object.isRequired,
  resetErrorBoundary: PropTypes.func.isRequired,
  errorInfo: PropTypes.object
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired
}
