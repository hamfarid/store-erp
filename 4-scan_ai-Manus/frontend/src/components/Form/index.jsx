/**
 * Form Components
 * ================
 * 
 * Reusable form input components with validation and RTL support.
 * 
 * Components:
 * - Input
 * - TextArea
 * - Select
 * - Checkbox
 * - Radio
 * - Switch
 * - FileUpload
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useRef } from 'react';
import { Eye, EyeOff, Upload, X, Check, AlertCircle } from 'lucide-react';

/**
 * Input Component
 */
export const Input = ({
  type = 'text',
  label,
  labelAr,
  placeholder,
  placeholderAr,
  value,
  onChange,
  error,
  errorAr,
  hint,
  hintAr,
  icon: Icon,
  required = false,
  disabled = false,
  className = '',
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayLabel = isRTL ? (labelAr || label) : label;
  const displayPlaceholder = isRTL ? (placeholderAr || placeholder) : placeholder;
  const displayError = isRTL ? (errorAr || error) : error;
  const displayHint = isRTL ? (hintAr || hint) : hint;

  const isPassword = type === 'password';
  const inputType = isPassword ? (showPassword ? 'text' : 'password') : type;

  return (
    <div className={`space-y-1.5 ${className}`}>
      {displayLabel && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {displayLabel}
          {required && <span className="text-red-500 ml-1 rtl:ml-0 rtl:mr-1">*</span>}
        </label>
      )}
      
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 rtl:left-auto rtl:right-0 pl-3 rtl:pl-0 rtl:pr-3 flex items-center pointer-events-none">
            <Icon className="w-5 h-5 text-gray-400" />
          </div>
        )}
        
        <input
          type={inputType}
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
          placeholder={displayPlaceholder}
          disabled={disabled}
          className={`
            w-full px-4 py-2.5 rounded-lg
            ${Icon ? 'pl-10 rtl:pl-4 rtl:pr-10' : ''}
            ${isPassword ? 'pr-10 rtl:pr-4 rtl:pl-10' : ''}
            bg-gray-50 dark:bg-gray-900
            border ${error ? 'border-red-500' : 'border-gray-200 dark:border-gray-700'}
            text-gray-800 dark:text-gray-200
            placeholder:text-gray-400
            focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500/30' : 'focus:ring-emerald-500/30'}
            focus:border-emerald-500
            disabled:opacity-50 disabled:cursor-not-allowed
            transition-all duration-200
          `}
          {...props}
        />
        
        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-0 rtl:right-auto rtl:left-0 pr-3 rtl:pr-0 rtl:pl-3 flex items-center"
          >
            {showPassword ? (
              <EyeOff className="w-5 h-5 text-gray-400 hover:text-gray-600" />
            ) : (
              <Eye className="w-5 h-5 text-gray-400 hover:text-gray-600" />
            )}
          </button>
        )}
      </div>
      
      {displayError && (
        <p className="text-sm text-red-500 flex items-center gap-1">
          <AlertCircle className="w-4 h-4" />
          {displayError}
        </p>
      )}
      
      {displayHint && !displayError && (
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {displayHint}
        </p>
      )}
    </div>
  );
};

/**
 * TextArea Component
 */
export const TextArea = ({
  label,
  labelAr,
  placeholder,
  placeholderAr,
  value,
  onChange,
  error,
  errorAr,
  hint,
  hintAr,
  rows = 4,
  required = false,
  disabled = false,
  maxLength,
  className = '',
  ...props
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayLabel = isRTL ? (labelAr || label) : label;
  const displayPlaceholder = isRTL ? (placeholderAr || placeholder) : placeholder;
  const displayError = isRTL ? (errorAr || error) : error;
  const displayHint = isRTL ? (hintAr || hint) : hint;

  return (
    <div className={`space-y-1.5 ${className}`}>
      {displayLabel && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {displayLabel}
          {required && <span className="text-red-500 ml-1 rtl:ml-0 rtl:mr-1">*</span>}
        </label>
      )}
      
      <textarea
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        placeholder={displayPlaceholder}
        rows={rows}
        maxLength={maxLength}
        disabled={disabled}
        className={`
          w-full px-4 py-2.5 rounded-lg
          bg-gray-50 dark:bg-gray-900
          border ${error ? 'border-red-500' : 'border-gray-200 dark:border-gray-700'}
          text-gray-800 dark:text-gray-200
          placeholder:text-gray-400
          focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500/30' : 'focus:ring-emerald-500/30'}
          focus:border-emerald-500
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-all duration-200
          resize-none
        `}
        {...props}
      />
      
      <div className="flex justify-between">
        <div>
          {displayError && (
            <p className="text-sm text-red-500 flex items-center gap-1">
              <AlertCircle className="w-4 h-4" />
              {displayError}
            </p>
          )}
          {displayHint && !displayError && (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {displayHint}
            </p>
          )}
        </div>
        
        {maxLength && (
          <p className="text-sm text-gray-400">
            {value?.length || 0} / {maxLength}
          </p>
        )}
      </div>
    </div>
  );
};

/**
 * Select Component
 */
export const Select = ({
  label,
  labelAr,
  options = [],
  value,
  onChange,
  placeholder,
  placeholderAr,
  error,
  errorAr,
  required = false,
  disabled = false,
  className = '',
  ...props
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayLabel = isRTL ? (labelAr || label) : label;
  const displayPlaceholder = isRTL ? (placeholderAr || placeholder) : placeholder;
  const displayError = isRTL ? (errorAr || error) : error;

  return (
    <div className={`space-y-1.5 ${className}`}>
      {displayLabel && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {displayLabel}
          {required && <span className="text-red-500 ml-1 rtl:ml-0 rtl:mr-1">*</span>}
        </label>
      )}
      
      <select
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        disabled={disabled}
        className={`
          w-full px-4 py-2.5 rounded-lg
          bg-gray-50 dark:bg-gray-900
          border ${error ? 'border-red-500' : 'border-gray-200 dark:border-gray-700'}
          text-gray-800 dark:text-gray-200
          focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500/30' : 'focus:ring-emerald-500/30'}
          focus:border-emerald-500
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-all duration-200
          cursor-pointer
        `}
        {...props}
      >
        {displayPlaceholder && (
          <option value="" disabled>
            {displayPlaceholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {isRTL ? (option.labelAr || option.label) : option.label}
          </option>
        ))}
      </select>
      
      {displayError && (
        <p className="text-sm text-red-500 flex items-center gap-1">
          <AlertCircle className="w-4 h-4" />
          {displayError}
        </p>
      )}
    </div>
  );
};

/**
 * Checkbox Component
 */
export const Checkbox = ({
  label,
  labelAr,
  checked,
  onChange,
  disabled = false,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayLabel = isRTL ? (labelAr || label) : label;

  return (
    <label className={`inline-flex items-center gap-2 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}>
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange?.(e.target.checked)}
          disabled={disabled}
          className="sr-only"
        />
        <div className={`
          w-5 h-5 rounded border-2 flex items-center justify-center
          transition-colors duration-200
          ${checked 
            ? 'bg-emerald-500 border-emerald-500' 
            : 'border-gray-300 dark:border-gray-600'
          }
        `}>
          {checked && <Check className="w-3.5 h-3.5 text-white" />}
        </div>
      </div>
      {displayLabel && (
        <span className="text-sm text-gray-700 dark:text-gray-200">
          {displayLabel}
        </span>
      )}
    </label>
  );
};

/**
 * Switch Component
 */
export const Switch = ({
  label,
  labelAr,
  checked,
  onChange,
  disabled = false,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayLabel = isRTL ? (labelAr || label) : label;

  return (
    <label className={`inline-flex items-center gap-3 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}>
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange?.(e.target.checked)}
          disabled={disabled}
          className="sr-only"
        />
        <div className={`
          w-11 h-6 rounded-full
          transition-colors duration-200
          ${checked ? 'bg-emerald-500' : 'bg-gray-300 dark:bg-gray-600'}
        `}>
          <div className={`
            w-5 h-5 rounded-full bg-white shadow
            transform transition-transform duration-200
            absolute top-0.5 left-0.5
            ${checked ? 'translate-x-5 rtl:-translate-x-5' : ''}
          `} />
        </div>
      </div>
      {displayLabel && (
        <span className="text-sm text-gray-700 dark:text-gray-200">
          {displayLabel}
        </span>
      )}
    </label>
  );
};

/**
 * File Upload Component
 */
export const FileUpload = ({
  label,
  labelAr,
  accept,
  multiple = false,
  value,
  onChange,
  error,
  errorAr,
  maxSize = 10,
  hint,
  hintAr,
  disabled = false,
  className = ''
}) => {
  const inputRef = useRef(null);
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayLabel = isRTL ? (labelAr || label) : label;
  const displayError = isRTL ? (errorAr || error) : error;
  const displayHint = isRTL ? (hintAr || hint) : hint;

  const handleDrop = (e) => {
    e.preventDefault();
    if (disabled) return;
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleFiles = (files) => {
    const validFiles = files.filter(file => {
      const sizeMB = file.size / (1024 * 1024);
      return sizeMB <= maxSize;
    });
    
    if (multiple) {
      onChange?.(validFiles);
    } else {
      onChange?.(validFiles[0] || null);
    }
  };

  const removeFile = (index) => {
    if (Array.isArray(value)) {
      const newFiles = value.filter((_, i) => i !== index);
      onChange?.(newFiles);
    } else {
      onChange?.(null);
    }
  };

  const files = Array.isArray(value) ? value : value ? [value] : [];

  return (
    <div className={`space-y-1.5 ${className}`}>
      {displayLabel && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {displayLabel}
        </label>
      )}
      
      <div
        onClick={() => !disabled && inputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className={`
          relative border-2 border-dashed rounded-xl p-6 text-center
          transition-colors duration-200 cursor-pointer
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-emerald-500'}
          ${error 
            ? 'border-red-500 bg-red-50 dark:bg-red-900/10' 
            : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900'
          }
        `}
      >
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={(e) => handleFiles(Array.from(e.target.files))}
          disabled={disabled}
          className="hidden"
        />
        
        <Upload className="w-10 h-10 mx-auto mb-3 text-gray-400" />
        
        <p className="text-sm text-gray-600 dark:text-gray-300">
          {isRTL 
            ? 'اسحب وأفلت الملفات هنا أو انقر للتحميل'
            : 'Drag and drop files here or click to upload'
          }
        </p>
        
        <p className="text-xs text-gray-400 mt-1">
          {isRTL ? `الحد الأقصى: ${maxSize}MB` : `Max size: ${maxSize}MB`}
        </p>
      </div>
      
      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2 mt-3">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-800 rounded-lg"
            >
              <span className="text-sm text-gray-700 dark:text-gray-200 truncate">
                {file.name}
              </span>
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>
          ))}
        </div>
      )}
      
      {displayError && (
        <p className="text-sm text-red-500 flex items-center gap-1">
          <AlertCircle className="w-4 h-4" />
          {displayError}
        </p>
      )}
      
      {displayHint && !displayError && (
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {displayHint}
        </p>
      )}
    </div>
  );
};

export default Input;
