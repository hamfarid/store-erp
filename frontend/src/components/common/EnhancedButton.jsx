import React from 'react'
import { ButtonSpinner } from './LoadingSpinner'
import { logClick } from '../../utils/logger'
import './EnhancedButton.css'

const EnhancedButton = ({
  children,
  loading = false,
  disabled = false,
  variant = 'primary',
  size = 'medium',
  icon = null,
  loadingText = null,
  onClick,
  type = 'button',
  className = '',
  ...props
}) => {
  const isDisabled = disabled || loading

  const buttonClass = `
    enhanced-button 
    enhanced-button--${variant} 
    enhanced-button--${size}
    ${loading ? 'enhanced-button--loading' : ''}
    ${isDisabled ? 'enhanced-button--disabled' : ''}
    ${className}
  `.trim()

  const handleClick = (e) => {
    if (!isDisabled && onClick) {
      // تسجيل النقرة
      const buttonText = typeof children === 'string' ? children : 'button';
      const buttonId = props.id || `${variant}-${buttonText}`;

      logClick(buttonId, buttonText, {
        variant,
        size,
        disabled: isDisabled,
        loading,
        type
      });

      onClick(e)
    }
  }

  return (
    <button
      type={type}
      className={buttonClass}
      disabled={isDisabled}
      onClick={handleClick}
      {...props}
    >
      <div className="enhanced-button__content">
        {loading && <ButtonSpinner />}
        {!loading && icon && <span className="enhanced-button__icon">{icon}</span>}
        <span className="enhanced-button__text">
          {loading && loadingText ? loadingText : children}
        </span>
      </div>
    </button>
  )
}

// مكونات متخصصة للأزرار الشائعة
export const SaveButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="success"
    loading={loading}
    loadingText="جاري الحفظ..."
    icon={!loading && <i className="fas fa-save"></i>}
    {...props}
  >
    حفظ
  </EnhancedButton>
)

export const DeleteButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="danger"
    loading={loading}
    loadingText="جاري الحذف..."
    icon={!loading && <i className="fas fa-trash"></i>}
    {...props}
  >
    حذف
  </EnhancedButton>
)

export const EditButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="warning"
    loading={loading}
    loadingText="جاري التحديث..."
    icon={!loading && <i className="fas fa-edit"></i>}
    {...props}
  >
    تعديل
  </EnhancedButton>
)

export const AddButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="primary"
    loading={loading}
    loadingText="جاري الإضافة..."
    icon={!loading && <i className="fas fa-plus"></i>}
    {...props}
  >
    إضافة
  </EnhancedButton>
)

export const SearchButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="secondary"
    loading={loading}
    loadingText="جاري البحث..."
    icon={!loading && <i className="fas fa-search"></i>}
    {...props}
  >
    بحث
  </EnhancedButton>
)

export const ExportButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="info"
    loading={loading}
    loadingText="جاري التصدير..."
    icon={!loading && <i className="fas fa-download"></i>}
    {...props}
  >
    تصدير
  </EnhancedButton>
)

export const PrintButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="secondary"
    loading={loading}
    loadingText="جاري التحضير..."
    icon={!loading && <i className="fas fa-print"></i>}
    {...props}
  >
    طباعة
  </EnhancedButton>
)

export const RefreshButton = ({ loading, ...props }) => (
  <EnhancedButton
    variant="secondary"
    size="small"
    loading={loading}
    loadingText="جاري التحديث..."
    icon={!loading && <i className="fas fa-sync-alt"></i>}
    {...props}
  >
    تحديث
  </EnhancedButton>
)

export default EnhancedButton
