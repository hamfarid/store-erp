import React, { createContext, useContext, useState, useCallback } from 'react'
import './EnhancedToast.css'

// Toast Context
const ToastContext = createContext()

// Toast Provider
export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((toast) => {
    const id = Date.now() + Math.random()
    const newToast = {
      id,
      type: 'info',
      duration: 5000,
      dismissible: true,
      ...toast,
      timestamp: new Date()
    }

    setToasts(prev => [...prev, newToast])

    // Auto remove toast
    if (newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }

    return id
  }, [])

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }, [])

  const clearAllToasts = useCallback(() => {
    setToasts([])
  }, [])

  // Convenience methods
  const success = useCallback((message, options = {}) => {
    return addToast({
      type: 'success',
      message,
      icon: 'fas fa-check-circle',
      ...options
    })
  }, [addToast])

  const error = useCallback((message, options = {}) => {
    return addToast({
      type: 'error',
      message,
      icon: 'fas fa-exclamation-circle',
      duration: 8000, // Longer duration for errors
      ...options
    })
  }, [addToast])

  const warning = useCallback((message, options = {}) => {
    return addToast({
      type: 'warning',
      message,
      icon: 'fas fa-exclamation-triangle',
      ...options
    })
  }, [addToast])

  const info = useCallback((message, options = {}) => {
    return addToast({
      type: 'info',
      message,
      icon: 'fas fa-info-circle',
      ...options
    })
  }, [addToast])

  const loading = useCallback((message, options = {}) => {
    return addToast({
      type: 'loading',
      message,
      icon: 'fas fa-spinner fa-spin',
      duration: 0, // Don't auto-dismiss loading toasts
      dismissible: false,
      ...options
    })
  }, [addToast])

  const value = {
    toasts,
    addToast,
    removeToast,
    clearAllToasts,
    success,
    error,
    warning,
    info,
    loading
  }

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer />
    </ToastContext.Provider>
  )
}

// Toast Container Component
const ToastContainer = () => {
  const { toasts } = useContext(ToastContext)

  return (
    <div className="toast-container">
      {toasts.map(toast => (
        <Toast key={toast.id} toast={toast} />
      ))}
    </div>
  )
}

// Individual Toast Component
const Toast = ({ toast }) => {
  const { removeToast } = useContext(ToastContext)
  const [isVisible, setIsVisible] = useState(false)
  const [isExiting, setIsExiting] = useState(false)

  React.useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 10)
    return () => clearTimeout(timer)
  }, [])

  const handleDismiss = () => {
    if (!toast.dismissible) return
    
    setIsExiting(true)
    setTimeout(() => {
      removeToast(toast.id)
    }, 300) // Match CSS animation duration
  }

  const handleAction = () => {
    if (toast.action && toast.action.onClick) {
      toast.action.onClick()
    }
    if (toast.action && toast.action.dismissOnClick !== false) {
      handleDismiss()
    }
  }

  const toastClass = `
    toast 
    toast--${toast.type}
    ${isVisible ? 'toast--visible' : ''}
    ${isExiting ? 'toast--exiting' : ''}
    ${toast.dismissible ? 'toast--dismissible' : ''}
  `.trim()

  return (
    <div className={toastClass} onClick={toast.dismissible ? handleDismiss : undefined}>
      <div className="toast__content">
        {toast.icon && (
          <div className="toast__icon">
            <i className={toast.icon}></i>
          </div>
        )}
        
        <div className="toast__body">
          {toast.title && (
            <div className="toast__title">{toast.title}</div>
          )}
          <div className="toast__message">{toast.message}</div>
          {toast.description && (
            <div className="toast__description">{toast.description}</div>
          )}
        </div>

        {toast.action && (
          <button 
            className="toast__action"
            onClick={handleAction}
          >
            {toast.action.label}
          </button>
        )}

        {toast.dismissible && (
          <button 
            className="toast__close"
            onClick={handleDismiss}
            aria-label="إغلاق"
          >
            <i className="fas fa-times"></i>
          </button>
        )}
      </div>

      {toast.duration > 0 && (
        <div 
          className="toast__progress"
          style={{ animationDuration: `${toast.duration}ms` }}
        ></div>
      )}
    </div>
  )
}

// Hook to use toast
export const useToast = () => {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}

// Enhanced toast as hook to respect Rules of Hooks
export const useEnhancedToast = () => {
  const { error: showError, warning } = useToast()

  const apiError = (err, customMessage) => {
    let message = customMessage || 'حدث خطأ غير متوقع'
    let description = ''
    if (err?.response?.data?.message) {
      message = err.response.data.message
    } else if (err?.message) {
      description = err.message
    }
    return showError(message, {
      description,
      action: {
        label: 'إعادة المحاولة',
        onClick: () => window.location.reload()
      }
    })
  }

  const networkError = () => {
    return showError('مشكلة في الاتصال بالشبكة', {
      description: 'تحقق من اتصالك بالإنترنت وحاول مرة أخرى',
      action: {
        label: 'إعادة المحاولة',
        onClick: () => window.location.reload()
      }
    })
  }

  const validationError = (errors) => {
    const errorList = Array.isArray(errors) ? errors : [errors]
    const message = errorList.join('، ')
    return warning('يرجى تصحيح الأخطاء التالية:', {
      description: message
    })
  }

  return { apiError, networkError, validationError }
}

export default ToastProvider
