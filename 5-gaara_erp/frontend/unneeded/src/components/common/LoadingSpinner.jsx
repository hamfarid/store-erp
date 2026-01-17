import React from 'react'
import './LoadingSpinner.css'

const LoadingSpinner = ({ 
  size = 'medium', 
  color = 'primary', 
  text = 'جاري التحميل...', 
  overlay = false,
  fullScreen = false 
}) => {
  const sizeClasses = {
    small: 'spinner-small',
    medium: 'spinner-medium',
    large: 'spinner-large'
  }

  const colorClasses = {
    primary: 'spinner-primary',
    secondary: 'spinner-secondary',
    success: 'spinner-success',
    warning: 'spinner-warning',
    danger: 'spinner-danger'
  }

  const spinnerClass = `loading-spinner ${sizeClasses[size]} ${colorClasses[color]}`

  const content = (
    <div className="spinner-container">
      <div className={spinnerClass}>
        <div className="spinner-circle"></div>
        <div className="spinner-circle"></div>
        <div className="spinner-circle"></div>
        <div className="spinner-circle"></div>
      </div>
      {text && <div className="spinner-text">{text}</div>}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="loading-fullscreen">
        {content}
      </div>
    )
  }

  if (overlay) {
    return (
      <div className="loading-overlay">
        {content}
      </div>
    )
  }

  return content
}

// مكون Loading للأزرار
export const ButtonSpinner = ({ size = 'small' }) => (
  <div className={`button-spinner spinner-${size}`}>
    <div className="spinner-dot"></div>
    <div className="spinner-dot"></div>
    <div className="spinner-dot"></div>
  </div>
)

// مكون Loading للجداول
export const TableLoader = ({ rows = 5, columns = 4 }) => (
  <div className="table-loader">
    {Array.from({ length: rows }).map((_, rowIndex) => (
      <div key={rowIndex} className="table-loader-row">
        {Array.from({ length: columns }).map((_, colIndex) => (
          <div key={colIndex} className="table-loader-cell">
            <div className="skeleton-line"></div>
          </div>
        ))}
      </div>
    ))}
  </div>
)

// مكون Loading للبطاقات
export const CardLoader = ({ count = 3 }) => (
  <div className="card-loader-container">
    {Array.from({ length: count }).map((_, index) => (
      <div key={index} className="card-loader">
        <div className="skeleton-header"></div>
        <div className="skeleton-line"></div>
        <div className="skeleton-line short"></div>
        <div className="skeleton-footer"></div>
      </div>
    ))}
  </div>
)

// Hook للتحكم في حالة التحميل
export const useLoading = (initialState = false) => {
  const [isLoading, setIsLoading] = React.useState(initialState)

  const startLoading = () => setIsLoading(true)
  const stopLoading = () => setIsLoading(false)
  
  const withLoading = async (asyncFunction) => {
    try {
      startLoading()
      const result = await asyncFunction()
      return result
    } finally {
      stopLoading()
    }
  }

  return {
    isLoading,
    startLoading,
    stopLoading,
    withLoading
  }
}

export default LoadingSpinner
