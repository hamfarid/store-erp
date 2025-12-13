// FILE: frontend/src/components/ui/AccessibleForm.jsx | PURPOSE: WCAG AA Compliant Form Components | OWNER: Frontend | RELATED: accessibility.css | LAST-AUDITED: 2025-10-21

import React, { forwardRef, useState } from 'react';
import { cn } from '../../lib/utils';

/**
 * Accessible Form Components - WCAG AA Compliant
 * 
 * P2 Fixes Applied:
 * - P2.1: Proper label associations
 * - P2.2: Error message handling
 * - P2.3: ARIA attributes for screen readers
 * - P2.4: RTL language support
 */

// Form Group Container
export const FormGroup = ({ children, className, ...props }) => {
  return (
    <div className={cn("form-group", className)} {...props}>
      {children}
    </div>
  );
};

// Accessible Label
export const FormLabel = ({ 
  htmlFor, 
  required = false, 
  children, 
  className, 
  ...props 
}) => {
  return (
    <label 
      htmlFor={htmlFor}
      className={cn("form-label", className)}
      {...props}
    >
      {children}
      {required && (
        <span className="text-destructive mr-1" aria-label="مطلوب">
          *
        </span>
      )}
    </label>
  );
};

// Accessible Input
export const FormInput = forwardRef(({
  type = 'text',
  id,
  name,
  placeholder,
  required = false,
  disabled = false,
  error,
  helpText,
  ariaLabel,
  ariaDescribedBy,
  className,
  onChange,
  ...props
}, ref) => {
  const [value, setValue] = useState(props.value || '');
  
  const inputId = id || `input-${name}`;
  const errorId = error ? `${inputId}-error` : undefined;
  const helpId = helpText ? `${inputId}-help` : undefined;
  
  const describedBy = [
    ariaDescribedBy,
    errorId,
    helpId
  ].filter(Boolean).join(' ');

  const handleChange = (e) => {
    setValue(e.target.value);
    onChange?.(e);
  };

  return (
    <>
      <input
        ref={ref}
        type={type}
        id={inputId}
        name={name}
        value={value}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        aria-label={ariaLabel}
        aria-describedby={describedBy || undefined}
        aria-invalid={error ? 'true' : 'false'}
        aria-required={required}
        className={cn(
          "form-input",
          error && "border-destructive focus:border-destructive",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        onChange={handleChange}
        {...props}
      />
      
      {helpText && (
        <div id={helpId} className="form-help">
          {helpText}
        </div>
      )}
      
      {error && (
        <div id={errorId} className="form-error" role="alert">
          <svg 
            className="h-4 w-4 flex-shrink-0" 
            fill="currentColor" 
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path 
              fillRule="evenodd" 
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" 
              clipRule="evenodd" 
            />
          </svg>
          {error}
        </div>
      )}
    </>
  );
});

FormInput.displayName = "FormInput";

// Accessible Select
export const FormSelect = forwardRef(({
  id,
  name,
  options = [],
  placeholder = "اختر خيار...",
  required = false,
  disabled = false,
  error,
  helpText,
  ariaLabel,
  ariaDescribedBy,
  className,
  onChange,
  ...props
}, ref) => {
  const [value, setValue] = useState(props.value || '');
  
  const selectId = id || `select-${name}`;
  const errorId = error ? `${selectId}-error` : undefined;
  const helpId = helpText ? `${selectId}-help` : undefined;
  
  const describedBy = [
    ariaDescribedBy,
    errorId,
    helpId
  ].filter(Boolean).join(' ');

  const handleChange = (e) => {
    setValue(e.target.value);
    onChange?.(e);
  };

  return (
    <>
      <select
        ref={ref}
        id={selectId}
        name={name}
        value={value}
        required={required}
        disabled={disabled}
        aria-label={ariaLabel}
        aria-describedby={describedBy || undefined}
        aria-invalid={error ? 'true' : 'false'}
        aria-required={required}
        className={cn(
          "form-input",
          error && "border-destructive focus:border-destructive",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        onChange={handleChange}
        {...props}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
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
      
      {helpText && (
        <div id={helpId} className="form-help">
          {helpText}
        </div>
      )}
      
      {error && (
        <div id={errorId} className="form-error" role="alert">
          <svg 
            className="h-4 w-4 flex-shrink-0" 
            fill="currentColor" 
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path 
              fillRule="evenodd" 
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" 
              clipRule="evenodd" 
            />
          </svg>
          {error}
        </div>
      )}
    </>
  );
});

FormSelect.displayName = "FormSelect";

// Accessible Textarea
export const FormTextarea = forwardRef(({
  id,
  name,
  placeholder,
  rows = 4,
  required = false,
  disabled = false,
  error,
  helpText,
  ariaLabel,
  ariaDescribedBy,
  className,
  onChange,
  ...props
}, ref) => {
  const [value, setValue] = useState(props.value || '');
  
  const textareaId = id || `textarea-${name}`;
  const errorId = error ? `${textareaId}-error` : undefined;
  const helpId = helpText ? `${textareaId}-help` : undefined;
  
  const describedBy = [
    ariaDescribedBy,
    errorId,
    helpId
  ].filter(Boolean).join(' ');

  const handleChange = (e) => {
    setValue(e.target.value);
    onChange?.(e);
  };

  return (
    <>
      <textarea
        ref={ref}
        id={textareaId}
        name={name}
        value={value}
        placeholder={placeholder}
        rows={rows}
        required={required}
        disabled={disabled}
        aria-label={ariaLabel}
        aria-describedby={describedBy || undefined}
        aria-invalid={error ? 'true' : 'false'}
        aria-required={required}
        className={cn(
          "form-input resize-vertical",
          error && "border-destructive focus:border-destructive",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        onChange={handleChange}
        {...props}
      />
      
      {helpText && (
        <div id={helpId} className="form-help">
          {helpText}
        </div>
      )}
      
      {error && (
        <div id={errorId} className="form-error" role="alert">
          <svg 
            className="h-4 w-4 flex-shrink-0" 
            fill="currentColor" 
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path 
              fillRule="evenodd" 
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" 
              clipRule="evenodd" 
            />
          </svg>
          {error}
        </div>
      )}
    </>
  );
});

FormTextarea.displayName = "FormTextarea";

// Accessible Checkbox
export const FormCheckbox = forwardRef(({
  id,
  name,
  label,
  checked = false,
  required = false,
  disabled = false,
  error,
  helpText,
  ariaLabel,
  ariaDescribedBy,
  className,
  onChange,
  ...props
}, ref) => {
  const [isChecked, setIsChecked] = useState(checked);
  
  const checkboxId = id || `checkbox-${name}`;
  const errorId = error ? `${checkboxId}-error` : undefined;
  const helpId = helpText ? `${checkboxId}-help` : undefined;
  
  const describedBy = [
    ariaDescribedBy,
    errorId,
    helpId
  ].filter(Boolean).join(' ');

  const handleChange = (e) => {
    setIsChecked(e.target.checked);
    onChange?.(e);
  };

  return (
    <div className="flex items-start space-x-3 space-x-reverse">
      <input
        ref={ref}
        type="checkbox"
        id={checkboxId}
        name={name}
        checked={isChecked}
        required={required}
        disabled={disabled}
        aria-label={ariaLabel}
        aria-describedby={describedBy || undefined}
        aria-invalid={error ? 'true' : 'false'}
        aria-required={required}
        className={cn(
          "h-4 w-4 rounded border-2 border-input text-primary focus:ring-2 focus:ring-primary focus:ring-offset-2",
          error && "border-destructive",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        onChange={handleChange}
        {...props}
      />
      
      <div className="flex-1">
        {label && (
          <label 
            htmlFor={checkboxId}
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            {label}
            {required && (
              <span className="text-destructive mr-1" aria-label="مطلوب">
                *
              </span>
            )}
          </label>
        )}
        
        {helpText && (
          <div id={helpId} className="form-help mt-1">
            {helpText}
          </div>
        )}
        
        {error && (
          <div id={errorId} className="form-error mt-1" role="alert">
            <svg 
              className="h-4 w-4 flex-shrink-0" 
              fill="currentColor" 
              viewBox="0 0 20 20"
              aria-hidden="true"
            >
              <path 
                fillRule="evenodd" 
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" 
                clipRule="evenodd" 
              />
            </svg>
            {error}
          </div>
        )}
      </div>
    </div>
  );
});

FormCheckbox.displayName = "FormCheckbox";
