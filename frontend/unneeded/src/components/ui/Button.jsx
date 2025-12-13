// -*- javascript -*-
// FILE: frontend/src/components/ui/Button.jsx | PURPOSE: Accessible Button Component | OWNER: Frontend | RELATED: theme/index.js | LAST-AUDITED: 2025-10-21

/**
 * مكون الزر المحسن لإمكانية الوصول
 * Enhanced Accessible Button Component
 * 
 * يدعم:
 * - إمكانية الوصول الكاملة (WCAG AA)
 * - RTL/LTR
 * - أحجام وأنواع متعددة
 * - حالات التحميل والتعطيل
 * - أيقونات ونصوص
 */

import React, { forwardRef } from 'react';
import PropTypes from 'prop-types';
import { theme } from '../../theme';
import './Button.css';

const Button = forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  onKeyDown,
  type = 'button',
  className = '',
  icon,
  iconPosition = 'left',
  fullWidth = false,
  ariaLabel,
  ariaDescribedBy,
  id,
  ...props
}, ref) => {
  // معالجة النقر
  const handleClick = (event) => {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }
    onClick?.(event);
  };

  // معالجة لوحة المفاتيح
  const handleKeyDown = (event) => {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }
    
    // تفعيل الزر بمفتاح Enter أو Space
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onClick?.(event);
    }
    
    onKeyDown?.(event);
  };

  // تحديد الكلاسات
  const buttonClasses = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    disabled && 'btn--disabled',
    icon && !children && 'btn--icon-only',
    className
  ].filter(Boolean).join(' ');

  // محتوى الزر
  const buttonContent = (
    <>
      {loading && (
        <span className="btn__spinner" aria-hidden="true">
          <svg className="btn__spinner-icon" viewBox="0 0 24 24">
            <circle 
              className="btn__spinner-circle" 
              cx="12" 
              cy="12" 
              r="10" 
              fill="none" 
              strokeWidth="2"
            />
          </svg>
        </span>
      )}
      
      {icon && iconPosition === 'left' && !loading && (
        <span className="btn__icon btn__icon--left" aria-hidden="true">
          {icon}
        </span>
      )}
      
      {children && (
        <span className="btn__text">
          {children}
        </span>
      )}
      
      {icon && iconPosition === 'right' && !loading && (
        <span className="btn__icon btn__icon--right" aria-hidden="true">
          {icon}
        </span>
      )}
    </>
  );

  return (
    <button
      ref={ref}
      id={id}
      type={type}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-label={ariaLabel || (typeof children === 'string' ? children : undefined)}
      aria-describedby={ariaDescribedBy}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {buttonContent}
    </button>
  );
});

Button.displayName = 'Button';

Button.propTypes = {
  children: PropTypes.node,
  variant: PropTypes.oneOf([
    'primary',
    'secondary', 
    'success',
    'error',
    'warning',
    'outline',
    'ghost',
    'link'
  ]),
  size: PropTypes.oneOf(['xs', 'sm', 'md', 'lg', 'xl']),
  disabled: PropTypes.bool,
  loading: PropTypes.bool,
  onClick: PropTypes.func,
  onKeyDown: PropTypes.func,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  className: PropTypes.string,
  icon: PropTypes.node,
  iconPosition: PropTypes.oneOf(['left', 'right']),
  fullWidth: PropTypes.bool,
  ariaLabel: PropTypes.string,
  ariaDescribedBy: PropTypes.string,
  id: PropTypes.string
};

export default Button;
