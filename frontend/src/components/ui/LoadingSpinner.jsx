import React from 'react'

const LoadingSpinner = ({ size = 'md', text = 'جاري التحميل...', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  }

  return (
    <div className={`flex flex-col items-center justify-center min-h-[200px] ${className}`}>
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-border border-t-blue-600 rounded-full animate-spin`}></div>
      </div>
      {text && (
        <p className="mt-4 text-muted-foreground text-sm font-medium">{text}</p>
      )}
    </div>
  )
}

// مكون تحميل للصفحة الكاملة
export const FullPageLoader = ({ text = 'جاري تحميل النظام...' }) => {
  return (
    <div className="fixed inset-0 bg-white z-50 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-border border-t-blue-600 rounded-full animate-spin mx-auto"></div>
        <p className="mt-4 text-muted-foreground text-lg font-medium">{text}</p>
        <div className="mt-2 text-sm text-gray-400">
          نظام إدارة المخزون المتكامل v1.5
        </div>
      </div>
    </div>
  )
}

// مكون تحميل مضمن
export const InlineLoader = ({ text = 'جاري التحميل...' }) => {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="w-6 h-6 border-2 border-border border-t-blue-600 rounded-full animate-spin mr-3"></div>
      <span className="text-muted-foreground text-sm">{text}</span>
    </div>
  )
}

// مكون تحميل للأزرار
export const ButtonLoader = ({ size = 'sm' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-5 h-5 border-2',
    lg: 'w-6 h-6 border-2'
  }

  return (
    <div className={`${sizeClasses[size]} border-white border-t-transparent rounded-full animate-spin`}></div>
  )
}

export default LoadingSpinner
