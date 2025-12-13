import React from 'react'
import { AlertCircle, AlertTriangle, CheckCircle, Info, X } from 'lucide-react'

// مكون عرض الأخطاء
export const ErrorMessage = ({ message, className = '' }) => {
  if (!message) return null
  
  return (
    <div className={`flex items-center text-destructive text-sm mt-1 ${className}`}>
      <AlertCircle className="w-4 h-4 ml-1" />
      {message}
    </div>
  )
}

// مكون عرض رسائل النجاح
export const SuccessMessage = ({ message, className = '' }) => {
  if (!message) return null
  
  return (
    <div className={`flex items-center text-primary text-sm mt-1 ${className}`}>
      <CheckCircle className="w-4 h-4 ml-1" />
      {message}
    </div>
  )
}

// مكون عرض رسائل المعلومات
export const InfoMessage = ({ message, className = '' }) => {
  if (!message) return null
  
  return (
    <div className={`flex items-center text-primary-600 text-sm mt-1 ${className}`}>
      <Info className="w-4 h-4 ml-1" />
      {message}
    </div>
  )
}

// مكون عرض رسائل التحذير
export const WarningMessage = ({ message, className = '' }) => {
  if (!message) return null
  
  return (
    <div className={`flex items-center text-accent text-sm mt-1 ${className}`}>
      <AlertTriangle className="w-4 h-4 ml-1" />
      {message}
    </div>
  )
}

// مكون تنبيه شامل
export const Alert = ({ type = 'info', title, message, onClose, className = '' }) => {
  const typeStyles = {
    error: 'bg-destructive/10 border-destructive/30 text-red-800',
    success: 'bg-primary/10 border-primary/30 text-green-800',
    warning: 'bg-accent/10 border-yellow-200 text-yellow-800',
    info: 'bg-primary-50 border-primary-200 text-primary-800'
  }

  const icons = {
    error: AlertCircle,
    success: CheckCircle,
    warning: AlertTriangle,
    info: Info
  }

  const Icon = icons[type]

  return (
    <div className={`border rounded-lg p-4 ${typeStyles[type]} ${className}`}>
      <div className="flex items-start">
        <Icon className="w-5 h-5 ml-2 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          {title && <h3 className="font-medium mb-1">{title}</h3>}
          {message && <p className="text-sm">{message}</p>}
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="mr-2 text-gray-400 hover:text-muted-foreground"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  )
}

// مكون حقل الإدخال مع التحقق
export const ValidatedInput = ({ 
  label, 
  error, 
  required = false, 
  className = '', 
  ...props 
}) => {
  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-foreground mb-1">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      <input
        {...props}
        className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 ${
          error 
            ? 'border-red-300 focus:ring-red-500' 
            : 'border-border focus:ring-primary-500'
        }`}
      />
      <ErrorMessage message={error} />
    </div>
  )
}

// مكون قائمة منسدلة مع التحقق
export const ValidatedSelect = ({ 
  label, 
  error, 
  required = false, 
  options = [], 
  placeholder = 'اختر...', 
  className = '', 
  ...props 
}) => {
  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-foreground mb-1">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      <select
        {...props}
        className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 ${
          error 
            ? 'border-red-300 focus:ring-red-500' 
            : 'border-border focus:ring-primary-500'
        }`}
      >
        <option value="">{placeholder}</option>
        {options.map((option, index) => (
          <option key={index} value={option.value || option}>
            {option.label || option}
          </option>
        ))}
      </select>
      <ErrorMessage message={error} />
    </div>
  )
}

// مكون منطقة النص مع التحقق
export const ValidatedTextarea = ({ 
  label, 
  error, 
  required = false, 
  className = '', 
  ...props 
}) => {
  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-foreground mb-1">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      <textarea
        {...props}
        className={`w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 ${
          error 
            ? 'border-red-300 focus:ring-red-500' 
            : 'border-border focus:ring-primary-500'
        }`}
      />
      <ErrorMessage message={error} />
    </div>
  )
}

// مكون حالة التحميل
export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  }

  return (
    <div className={`animate-spin rounded-full border-2 border-border border-t-blue-600 ${sizeClasses[size]} ${className}`}></div>
  )
}

// مكون حالة فارغة
export const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  action, 
  className = '' 
}) => {
  return (
    <div className={`text-center py-12 ${className}`}>
      {Icon && <Icon className="w-12 h-12 text-gray-400 mx-auto mb-4" />}
      <h3 className="text-lg font-medium text-foreground mb-2">{title}</h3>
      {description && <p className="text-muted-foreground mb-4">{description}</p>}
      {action}
    </div>
  )
}

// مكون نافذة تأكيد
export const ConfirmDialog = ({ 
  isOpen, 
  title, 
  message, 
  confirmText = 'تأكيد', 
  cancelText = 'إلغاء', 
  onConfirm, 
  onCancel,
  type = 'warning'
}) => {
  if (!isOpen) return null

  const typeStyles = {
    warning: 'text-accent',
    danger: 'text-destructive',
    info: 'text-primary-600'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex items-center mb-4">
          <AlertTriangle className={`w-6 h-6 ml-2 ${typeStyles[type]}`} />
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
        
        <p className="text-muted-foreground mb-6">{message}</p>
        
        <div className="flex justify-end space-x-2 space-x-reverse">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-muted-foreground border border-border rounded-md hover:bg-muted/50"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`px-4 py-2 text-white rounded-md ${
              type === 'danger' 
                ? 'bg-destructive hover:bg-red-700' 
                : 'bg-primary-600 hover:bg-primary-700'
            }`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}


