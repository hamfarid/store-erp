import React, { useState, useCallback } from 'react';
// eslint-disable-next-line no-unused-vars
import { validateValue } from '../utils/validationRules';
import '../styles/FormValidation.css';

/**
 * FormField Component
 * Displays a single form field with validation and error handling
 */
export const FormField = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  touched,
  disabled = false,
  placeholder,
  required = false,
  validators = [],
  hint,
  className = '',
  ...props
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [validationMessage, setValidationMessage] = useState('');

  const handleChange = useCallback((e) => {
    const newValue = e.target.value;
    onChange({ target: { name, value: newValue } });

    // Real-time validation
    if (validators.length > 0 && isFocused) {
      for (const validator of validators) {
        const result = validator(newValue);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  }, [name, onChange, validators, isFocused]);

  const handleBlur = (e) => {
    setIsFocused(false);
    onBlur?.(e);

    // Validation on blur
    if (validators.length > 0) {
      for (const validator of validators) {
        const result = validator(value);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const showError = touched && (error || validationMessage);
  const showSuccess = touched && !error && !validationMessage && value;

  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={name} className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}

      <div className="form-field-wrapper">
        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          onFocus={handleFocus}
          disabled={disabled}
          placeholder={placeholder}
          className={`form-input ${
            showError ? 'input-invalid' : ''
          } ${showSuccess ? 'input-valid' : ''}`}
          aria-invalid={showError}
          aria-describedby={showError ? `${name}-error` : hint ? `${name}-hint` : undefined}
          {...props}
        />

        {showSuccess && (
          <span className="form-success-icon" aria-hidden="true">
            ✓
          </span>
        )}
        {showError && (
          <span className="form-error-icon" aria-hidden="true">
            ✕
          </span>
        )}
      </div>

      {showError && (
        <span id={`${name}-error`} className="form-error" role="alert">
          {error || validationMessage}
        </span>
      )}

      {hint && !showError && (
        <span id={`${name}-hint`} className="form-hint">
          {hint}
        </span>
      )}
    </div>
  );
};

/**
 * FormSelect Component
 * Displays a select field with validation
 */
export const FormSelect = ({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  touched,
  disabled = false,
  placeholder,
  options = [],
  required = false,
  validators = [],
  hint,
  className = '',
  ...props
}) => {
  const [validationMessage, setValidationMessage] = useState('');

  const handleChange = (e) => {
    const newValue = e.target.value;
    onChange({ target: { name, value: newValue } });

    // Real-time validation
    if (validators.length > 0) {
      for (const validator of validators) {
        const result = validator(newValue);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  };

  const handleBlur = (e) => {
    onBlur?.(e);

    // Validation on blur
    if (validators.length > 0) {
      for (const validator of validators) {
        const result = validator(value);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  };

  const showError = touched && (error || validationMessage);
  const showSuccess = touched && !error && !validationMessage && value;

  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={name} className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}

      <div className="form-field-wrapper">
        <select
          id={name}
          name={name}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          disabled={disabled}
          className={`form-input form-select ${
            showError ? 'input-invalid' : ''
          } ${showSuccess ? 'input-valid' : ''}`}
          aria-invalid={showError}
          aria-describedby={showError ? `${name}-error` : hint ? `${name}-hint` : undefined}
          {...props}
        >
          {placeholder && (
            <option value="">{placeholder}</option>
          )}
          {options.map((option) => (
            <option
              key={option.value}
              value={option.value}
              disabled={option.disabled}
            >
              {option.label}
            </option>
          ))}
        </select>

        {showSuccess && (
          <span className="form-success-icon" aria-hidden="true">
            ✓
          </span>
        )}
        {showError && (
          <span className="form-error-icon" aria-hidden="true">
            ✕
          </span>
        )}
      </div>

      {showError && (
        <span id={`${name}-error`} className="form-error" role="alert">
          {error || validationMessage}
        </span>
      )}

      {hint && !showError && (
        <span id={`${name}-hint`} className="form-hint">
          {hint}
        </span>
      )}
    </div>
  );
};

/**
 * FormTextarea Component
 * Displays a textarea field with validation
 */
export const FormTextarea = ({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  touched,
  disabled = false,
  placeholder,
  required = false,
  validators = [],
  hint,
  maxLength,
  rows = 4,
  className = '',
  ...props
}) => {
  const [validationMessage, setValidationMessage] = useState('');

  const handleChange = (e) => {
    const newValue = e.target.value;
    onChange({ target: { name, value: newValue } });

    // Real-time validation
    if (validators.length > 0) {
      for (const validator of validators) {
        const result = validator(newValue);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  };

  const handleBlur = (e) => {
    onBlur?.(e);

    // Validation on blur
    if (validators.length > 0) {
      for (const validator of validators) {
        const result = validator(value);
        if (result !== true) {
          setValidationMessage(result);
          return;
        }
      }
      setValidationMessage('');
    }
  };

  const showError = touched && (error || validationMessage);
  const showSuccess = touched && !error && !validationMessage && value;

  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={name} className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}

      <div className="form-field-wrapper">
        <textarea
          id={name}
          name={name}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          disabled={disabled}
          placeholder={placeholder}
          maxLength={maxLength}
          rows={rows}
          className={`form-input form-textarea ${
            showError ? 'input-invalid' : ''
          } ${showSuccess ? 'input-valid' : ''}`}
          aria-invalid={showError}
          aria-describedby={showError ? `${name}-error` : hint ? `${name}-hint` : undefined}
          {...props}
        />

        {showSuccess && (
          <span className="form-success-icon" aria-hidden="true">
            ✓
          </span>
        )}
        {showError && (
          <span className="form-error-icon" aria-hidden="true">
            ✕
          </span>
        )}
      </div>

      {maxLength && (
        <div className="form-char-count">
          {value.length} / {maxLength}
        </div>
      )}

      {showError && (
        <span id={`${name}-error`} className="form-error" role="alert">
          {error || validationMessage}
        </span>
      )}

      {hint && !showError && (
        <span id={`${name}-hint`} className="form-hint">
          {hint}
        </span>
      )}
    </div>
  );
};

/**
 * FormCheckbox Component
 * Displays a checkbox field with validation
 */
export const FormCheckbox = ({
  label,
  name,
  checked,
  onChange,
  disabled = false,
  error,
  touched,
  required = false,
  className = '',
  ...props
}) => {
  const handleChange = (e) => {
    onChange({ target: { name, value: e.target.checked } });
  };

  const showError = touched && error;

  return (
    <div className={`form-group form-checkbox-group ${className}`}>
      <div className="form-checkbox-wrapper">
        <input
          id={name}
          type="checkbox"
          name={name}
          checked={checked}
          onChange={handleChange}
          disabled={disabled}
          className="form-checkbox"
          aria-invalid={showError}
          aria-describedby={showError ? `${name}-error` : undefined}
          {...props}
        />
        <label htmlFor={name} className="form-checkbox-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      </div>

      {showError && (
        <span id={`${name}-error`} className="form-error" role="alert">
          {error}
        </span>
      )}
    </div>
  );
};

/**
 * FormRadio Component
 * Displays radio button fields with validation
 */
export const FormRadio = ({
  label,
  name,
  value,
  onChange,
  options = [],
  error,
  touched,
  required = false,
  disabled = false,
  className = '',
}) => {
  const handleChange = (e) => {
    onChange({ target: { name, value: e.target.value } });
  };

  const showError = touched && error;

  return (
    <div className={`form-group form-radio-group ${className}`}>
      {label && (
        <label className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}

      <div className="form-radio-options">
        {options.map((option) => (
          <div key={option.value} className="form-radio-wrapper">
            <input
              type="radio"
              id={`${name}-${option.value}`}
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={handleChange}
              disabled={disabled || option.disabled}
              className="form-radio"
              aria-invalid={showError}
            />
            <label htmlFor={`${name}-${option.value}`} className="form-radio-label">
              {option.label}
            </label>
          </div>
        ))}
      </div>

      {showError && (
        <span className="form-error" role="alert">
          {error}
        </span>
      )}
    </div>
  );
};

/**
 * FormContainer Component
 * Wrapper for entire form with validation state management
 */
export const FormContainer = ({
  children,
  onSubmit,
  className = '',
  noValidate = false,
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!noValidate) {
      e.target.checkValidity();
    }
    onSubmit?.(e);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={`form-container ${className}`}
      noValidate={noValidate}
    >
      {children}
    </form>
  );
};

export default FormField;
