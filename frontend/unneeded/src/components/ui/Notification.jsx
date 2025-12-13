import React, { useState, useEffect } from 'react'
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react'

const Notification = ({
  type = 'info', 
  title, 
  message, 
  dismissible = true, 
  onDismiss,
  autoClose = false,
  autoCloseDelay = 5000,
  className = "",
  actions = []
}) => {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(() => {
        handleDismiss()
      }, autoCloseDelay)

      return () => clearTimeout(timer)
    }
  }, [autoClose, autoCloseDelay])

  const handleDismiss = () => {
    setIsVisible(false)
    if (onDismiss) {
      onDismiss()
    }
  }

  if (!isVisible) return null

  const alertConfig = {
    success: {
      icon: CheckCircle,
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/30',
      iconColor: 'text-primary',
      titleColor: 'text-green-800',
      messageColor: 'text-primary'
    },
    error: {
      icon: XCircle,
      bgColor: 'bg-destructive/10',
      borderColor: 'border-destructive/30',
      iconColor: 'text-destructive',
      titleColor: 'text-red-800',
      messageColor: 'text-destructive'
    },
    warning: {
      icon: AlertTriangle,
      bgColor: 'bg-accent/10',
      borderColor: 'border-yellow-200',
      iconColor: 'text-accent',
      titleColor: 'text-yellow-800',
      messageColor: 'text-yellow-700'
    },
    info: {
      icon: Info,
      bgColor: 'bg-primary-50',
      borderColor: 'border-primary-200',
      iconColor: 'text-primary-600',
      titleColor: 'text-primary-800',
      messageColor: 'text-primary-700'
    }
  }

  const config = alertConfig[type]
  const Icon = config.icon

  return (
    <div 
      className={`${config.bgColor} ${config.borderColor} border rounded-lg p-4 ${className}`}
      dir="rtl"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <Icon className={`w-5 h-5 ${config.iconColor}`} />
        </div>
        
        <div className="mr-3 flex-1">
          {title && (
            <h3 className={`text-sm font-medium ${config.titleColor} mb-1`}>
              {title}
            </h3>
          )}
          
          {message && (
            <div className={`text-sm ${config.messageColor}`}>
              {typeof message === 'string' ? (
                <p>{message}</p>
              ) : (
                message
              )}
            </div>
          )}

          {actions.length > 0 && (
            <div className="mt-3 flex space-x-2 space-x-reverse">
              {actions.map((action, index) => (
                <button
                  key={index}
                  onClick={action.onClick}
                  className={`text-sm font-medium px-3 py-1 rounded-md transition-colors ${
                    action.primary 
                      ? `${config.titleColor} bg-white hover:bg-muted/50 border border-current`
                      : `${config.messageColor} hover:${config.titleColor}`
                  }`}
                >
                  {action.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {dismissible && (
          <div className="flex-shrink-0 mr-auto">
            <button
              onClick={handleDismiss}
              className={`${config.iconColor} hover:${config.titleColor} transition-colors`}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

// مكون Loading Spinner
const LoadingSpinner = ({ 
  size = 'md', 
  color = 'blue', 
  text = 'جاري التحميل...',
  overlay = false,
  className = ""
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  }

  const colorClasses = {
    blue: 'border-primary-600',
    green: 'border-green-600',
    red: 'border-red-600',
    yellow: 'border-yellow-600',
    gray: 'border-gray-600'
  }

  const spinner = (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <div 
        className={`${sizeClasses[size]} border-2 ${colorClasses[color]} border-t-transparent rounded-full animate-spin`}
      />
      {text && (
        <p className="mt-2 text-sm text-muted-foreground">{text}</p>
      )}
    </div>
  )

  if (overlay) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6">
          {spinner}
        </div>
      </div>
    )
  }

  return spinner
}

// مكون Modal
const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  size = 'md',
  className = ""
}) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full mx-4'
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" dir="rtl">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Overlay */}
        <div 
          className="fixed inset-0 transition-opacity bg-muted/500 bg-opacity-75"
          onClick={onClose}
        />

        {/* Modal */}
        <div className={`inline-block w-full ${sizeClasses[size]} p-6 my-8 overflow-hidden text-right align-middle transition-all transform bg-white shadow-xl rounded-lg ${className}`}>
          {/* Header */}
          {title && (
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-foreground">
                {title}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-muted-foreground transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          )}

          {/* Content */}
          <div>
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}

export { Notification, LoadingSpinner, Modal }
export default Notification

