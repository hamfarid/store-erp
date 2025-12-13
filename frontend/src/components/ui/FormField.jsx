// -*- javascript -*-
// FILE: frontend/src/components/ui/FormField.jsx | PURPOSE: Accessible Form Field Component | OWNER: Frontend | RELATED: theme/index.js | LAST-AUDITED: 2025-10-21

/**
 * مكون حقل النموذج المحسن لإمكانية الوصول
 * Enhanced Accessible Form Field Component
 * 
 * يدعم:
 * - إمكانية الوصول الكاملة (WCAG AA)
 * - RTL/LTR
 * - أنواع مختلفة من الحقول
 * - التحقق من صحة البيانات
 * - رسائل الخطأ والمساعدة
 */

import React, { forwardRef, useState, useId } from 'react';
import PropTypes from 'prop-types';
import './FormField.css';

const FormField = forwardRef(({
  label,
  labelAr,
  type = 'text',
  value,
  defaultValue,
  onChange,
  onBlur,
  onFocus,
  placeholder,
  placeholderAr,
  required = false,
  disabled = false,
  readOnly = false,
  error,
  errorAr,
  helpText,
  helpTextAr,
  size = 'md',
  className = '',
  inputClassName = '',
  icon,
  iconPosition = 'left',
  showPasswordToggle = false,
  autoComplete,
  maxLength,
  minLength,
  min,
  max,
  step,
  pattern,
  options = [], // للـ select
  multiple = false, // للـ select
  rows = 4, // للـ textarea
  id,
  name,
  'aria-describedby': ariaDescribedBy,
  ...props
}, ref) => {
  const fieldId = useId();
  const actualId = id || fieldId;
  const helpId = `${actualId}-help`;
  const errorId = `${actualId}-error`;
  
  const [showPassword, setShowPassword] = useState(false);
  const [focused, setFocused] = useState(false);

  // تحديد نوع الحقل الفعلي
  const actualType = type === 'password' && showPassword ? 'text' : type;

  // معالجة التركيز
  const handleFocus = (event) => {
    setFocused(true);
    onFocus?.(event);
  };

  const handleBlur = (event) => {
    setFocused(false);
    onBlur?.(event);
  };

  // تبديل إظهار كلمة المرور
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // تحديد الكلاسات
  const fieldClasses = [
    'form-field',
    `form-field--${size}`,
    error && 'form-field--error',
    disabled && 'form-field--disabled',
    focused && 'form-field--focused',
    className
  ].filter(Boolean).join(' ');

  const inputClasses = [
    'form-field__input',
    icon && `form-field__input--with-icon-${iconPosition}`,
    type === 'password' && showPasswordToggle && 'form-field__input--with-password-toggle',
    inputClassName
  ].filter(Boolean).join(' ');

  // تحديد aria-describedby
  const describedBy = [
    helpText && helpId,
    error && errorId,
    ariaDescribedBy
  ].filter(Boolean).join(' ');

  // تحديد التسمية والنص المساعد حسب اللغة
  const currentLanguage = document.documentElement.dir === 'rtl' ? 'ar' : 'en';
  const displayLabel = currentLanguage === 'ar' && labelAr ? labelAr : label;
  const displayPlaceholder = currentLanguage === 'ar' && placeholderAr ? placeholderAr : placeholder;
  const displayError = currentLanguage === 'ar' && errorAr ? errorAr : error;
  const displayHelpText = currentLanguage === 'ar' && helpTextAr ? helpTextAr : helpText;

  // رندر الحقل حسب النوع
  const renderInput = () => {
    const commonProps = {
      ref,
      id: actualId,
      name,
      value,
      defaultValue,
      onChange,
      onFocus: handleFocus,
      onBlur: handleBlur,
      placeholder: displayPlaceholder,
      required,
      disabled,
      readOnly,
      className: inputClasses,
      'aria-invalid': !!error,
      'aria-describedby': describedBy || undefined,
      autoComplete,
      maxLength,
      minLength,
      min,
      max,
      step,
      pattern,
      ...props
    };

    switch (type) {
      case 'textarea':
        return (
          <textarea
            {...commonProps}
            rows={rows}
          />
        );

      case 'select':
        return (
          <select
            {...commonProps}
            multiple={multiple}
          >
            {options.map((option, index) => (
              <option
                key={option.value || index}
                value={option.value}
                disabled={option.disabled}
              >
                {currentLanguage === 'ar' && option.labelAr ? option.labelAr : option.label}
              </option>
            ))}
          </select>
        );

      default:
        return (
          <input
            {...commonProps}
            type={actualType}
          />
        );
    }
  };

  return (
    <div className={fieldClasses}>
      {/* التسمية */}
      {displayLabel && (
        <label htmlFor={actualId} className="form-field__label">
          {displayLabel}
          {required && (
            <span className="form-field__required" aria-label="مطلوب">
              *
            </span>
          )}
        </label>
      )}

      {/* حاوية الحقل */}
      <div className="form-field__input-wrapper">
        {/* الأيقونة اليسرى */}
        {icon && iconPosition === 'left' && (
          <span className="form-field__icon form-field__icon--left" aria-hidden="true">
            {icon}
          </span>
        )}

        {/* الحقل */}
        {renderInput()}

        {/* الأيقونة اليمنى */}
        {icon && iconPosition === 'right' && (
          <span className="form-field__icon form-field__icon--right" aria-hidden="true">
            {icon}
          </span>
        )}

        {/* زر إظهار/إخفاء كلمة المرور */}
        {type === 'password' && showPasswordToggle && (
          <button
            type="button"
            className="form-field__password-toggle"
            onClick={togglePasswordVisibility}
            aria-label={showPassword ? 'إخفاء كلمة المرور' : 'إظهار كلمة المرور'}
            tabIndex={-1}
          >
            {showPassword ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            )}
          </button>
        )}
      </div>

      {/* النص المساعد */}
      {displayHelpText && !error && (
        <div id={helpId} className="form-field__help">
          {displayHelpText}
        </div>
      )}

      {/* رسالة الخطأ */}
      {displayError && (
        <div id={errorId} className="form-field__error" role="alert">
          <svg className="form-field__error-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
          {displayError}
        </div>
      )}
    </div>
  );
});

FormField.displayName = 'FormField';

FormField.propTypes = {
  label: PropTypes.string,
  labelAr: PropTypes.string,
  type: PropTypes.oneOf([
    'text',
    'email',
    'password',
    'number',
    'tel',
    'url',
    'search',
    'date',
    'datetime-local',
    'time',
    'month',
    'week',
    'textarea',
    'select'
  ]),
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.array]),
  defaultValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.array]),
  onChange: PropTypes.func,
  onBlur: PropTypes.func,
  onFocus: PropTypes.func,
  placeholder: PropTypes.string,
  placeholderAr: PropTypes.string,
  required: PropTypes.bool,
  disabled: PropTypes.bool,
  readOnly: PropTypes.bool,
  error: PropTypes.string,
  errorAr: PropTypes.string,
  helpText: PropTypes.string,
  helpTextAr: PropTypes.string,
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  className: PropTypes.string,
  inputClassName: PropTypes.string,
  icon: PropTypes.node,
  iconPosition: PropTypes.oneOf(['left', 'right']),
  showPasswordToggle: PropTypes.bool,
  autoComplete: PropTypes.string,
  maxLength: PropTypes.number,
  minLength: PropTypes.number,
  min: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  max: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  step: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  pattern: PropTypes.string,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      label: PropTypes.string.isRequired,
      labelAr: PropTypes.string,
      disabled: PropTypes.bool
    })
  ),
  multiple: PropTypes.bool,
  rows: PropTypes.number,
  id: PropTypes.string,
  name: PropTypes.string,
  'aria-describedby': PropTypes.string
};

export default FormField;
