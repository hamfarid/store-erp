/**
 * P2.74: Form Builder Utilities
 * 
 * Custom hooks for form handling with validation.
 */

import { useState, useCallback, useMemo, ChangeEvent, FormEvent } from 'react';

// =============================================================================
// Types
// =============================================================================

export type ValidationRule<T> = {
  required?: boolean | string;
  min?: number | { value: number; message: string };
  max?: number | { value: number; message: string };
  minLength?: number | { value: number; message: string };
  maxLength?: number | { value: number; message: string };
  pattern?: RegExp | { value: RegExp; message: string };
  email?: boolean | string;
  custom?: (value: T, formValues: Record<string, any>) => string | undefined;
};

export type FieldConfig<T> = {
  initialValue: T;
  validation?: ValidationRule<T>;
  transform?: (value: any) => T;
};

export type FormConfig<T extends Record<string, any>> = {
  [K in keyof T]: FieldConfig<T[K]>;
};

export type FormErrors<T> = Partial<Record<keyof T, string>>;

export type FormTouched<T> = Partial<Record<keyof T, boolean>>;

export interface UseFormReturn<T extends Record<string, any>> {
  values: T;
  errors: FormErrors<T>;
  touched: FormTouched<T>;
  isValid: boolean;
  isDirty: boolean;
  isSubmitting: boolean;
  
  // Handlers
  handleChange: (field: keyof T) => (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => void;
  handleBlur: (field: keyof T) => () => void;
  handleSubmit: (onSubmit: (values: T) => void | Promise<void>) => (e: FormEvent) => void;
  
  // Actions
  setValue: (field: keyof T, value: any) => void;
  setValues: (values: Partial<T>) => void;
  setError: (field: keyof T, error: string) => void;
  setErrors: (errors: FormErrors<T>) => void;
  clearErrors: () => void;
  reset: () => void;
  validate: () => boolean;
  validateField: (field: keyof T) => string | undefined;
  
  // Field helpers
  getFieldProps: (field: keyof T) => {
    value: any;
    onChange: (e: ChangeEvent<any>) => void;
    onBlur: () => void;
    name: string;
    id: string;
  };
  
  getFieldMeta: (field: keyof T) => {
    error: string | undefined;
    touched: boolean;
    dirty: boolean;
  };
}

// =============================================================================
// Validation Helpers
// =============================================================================

const getValidationMessage = (rule: any, defaultMessage: string): string => {
  if (typeof rule === 'object' && rule.message) return rule.message;
  if (typeof rule === 'string') return rule;
  return defaultMessage;
};

const getRuleValue = (rule: any): any => {
  if (typeof rule === 'object' && rule.value !== undefined) return rule.value;
  return rule;
};

function validateField<T>(
  value: T,
  rules: ValidationRule<T> | undefined,
  formValues: Record<string, any>
): string | undefined {
  if (!rules) return undefined;

  // Required
  if (rules.required) {
    if (value === undefined || value === null || value === '' || (Array.isArray(value) && value.length === 0)) {
      return getValidationMessage(rules.required, 'هذا الحقل مطلوب');
    }
  }

  // Skip other validations if empty and not required
  if (value === undefined || value === null || value === '') {
    return undefined;
  }

  // Min (for numbers)
  if (rules.min !== undefined && typeof value === 'number') {
    const minValue = getRuleValue(rules.min);
    if (value < minValue) {
      return getValidationMessage(rules.min, `القيمة الأدنى هي ${minValue}`);
    }
  }

  // Max (for numbers)
  if (rules.max !== undefined && typeof value === 'number') {
    const maxValue = getRuleValue(rules.max);
    if (value > maxValue) {
      return getValidationMessage(rules.max, `القيمة الأقصى هي ${maxValue}`);
    }
  }

  // MinLength (for strings)
  if (rules.minLength !== undefined && typeof value === 'string') {
    const minLen = getRuleValue(rules.minLength);
    if (value.length < minLen) {
      return getValidationMessage(rules.minLength, `الحد الأدنى ${minLen} أحرف`);
    }
  }

  // MaxLength (for strings)
  if (rules.maxLength !== undefined && typeof value === 'string') {
    const maxLen = getRuleValue(rules.maxLength);
    if (value.length > maxLen) {
      return getValidationMessage(rules.maxLength, `الحد الأقصى ${maxLen} أحرف`);
    }
  }

  // Pattern
  if (rules.pattern !== undefined && typeof value === 'string') {
    const pattern = getRuleValue(rules.pattern);
    if (!pattern.test(value)) {
      return getValidationMessage(rules.pattern, 'تنسيق غير صحيح');
    }
  }

  // Email
  if (rules.email && typeof value === 'string') {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(value)) {
      return getValidationMessage(rules.email, 'البريد الإلكتروني غير صحيح');
    }
  }

  // Custom validation
  if (rules.custom) {
    return rules.custom(value, formValues);
  }

  return undefined;
}

// =============================================================================
// Main Hook
// =============================================================================

export function useForm<T extends Record<string, any>>(
  config: FormConfig<T>
): UseFormReturn<T> {
  // Extract initial values
  const initialValues = useMemo(() => {
    const values: any = {};
    for (const key in config) {
      values[key] = config[key].initialValue;
    }
    return values as T;
  }, []);

  // State
  const [values, setValuesState] = useState<T>(initialValues);
  const [errors, setErrorsState] = useState<FormErrors<T>>({});
  const [touched, setTouched] = useState<FormTouched<T>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Computed
  const isDirty = useMemo(() => {
    return Object.keys(config).some(key => values[key as keyof T] !== initialValues[key as keyof T]);
  }, [values, initialValues, config]);

  const isValid = useMemo(() => {
    return Object.keys(errors).length === 0;
  }, [errors]);

  // Validation
  const validateFieldByName = useCallback((field: keyof T): string | undefined => {
    const fieldConfig = config[field];
    if (!fieldConfig) return undefined;
    return validateField(values[field], fieldConfig.validation, values);
  }, [config, values]);

  const validate = useCallback((): boolean => {
    const newErrors: FormErrors<T> = {};
    let valid = true;

    for (const key in config) {
      const error = validateField(values[key as keyof T], config[key].validation, values);
      if (error) {
        newErrors[key as keyof T] = error;
        valid = false;
      }
    }

    setErrorsState(newErrors);
    return valid;
  }, [config, values]);

  // Handlers
  const handleChange = useCallback((field: keyof T) => (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const fieldConfig = config[field];
    let value: any = e.target.type === 'checkbox' 
      ? (e.target as HTMLInputElement).checked 
      : e.target.value;

    // Apply transform if provided
    if (fieldConfig?.transform) {
      value = fieldConfig.transform(value);
    }

    setValuesState(prev => ({ ...prev, [field]: value }));

    // Clear error on change
    if (errors[field]) {
      setErrorsState(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  }, [config, errors]);

  const handleBlur = useCallback((field: keyof T) => () => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    // Validate on blur
    const error = validateFieldByName(field);
    if (error) {
      setErrorsState(prev => ({ ...prev, [field]: error }));
    }
  }, [validateFieldByName]);

  const handleSubmit = useCallback((onSubmit: (values: T) => void | Promise<void>) => async (e: FormEvent) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched: FormTouched<T> = {};
    for (const key in config) {
      allTouched[key as keyof T] = true;
    }
    setTouched(allTouched);

    // Validate
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await onSubmit(values);
    } finally {
      setIsSubmitting(false);
    }
  }, [config, validate, values]);

  // Actions
  const setValue = useCallback((field: keyof T, value: any) => {
    setValuesState(prev => ({ ...prev, [field]: value }));
  }, []);

  const setValues = useCallback((newValues: Partial<T>) => {
    setValuesState(prev => ({ ...prev, ...newValues }));
  }, []);

  const setError = useCallback((field: keyof T, error: string) => {
    setErrorsState(prev => ({ ...prev, [field]: error }));
  }, []);

  const setErrors = useCallback((newErrors: FormErrors<T>) => {
    setErrorsState(newErrors);
  }, []);

  const clearErrors = useCallback(() => {
    setErrorsState({});
  }, []);

  const reset = useCallback(() => {
    setValuesState(initialValues);
    setErrorsState({});
    setTouched({});
  }, [initialValues]);

  // Field helpers
  const getFieldProps = useCallback((field: keyof T) => ({
    value: values[field] ?? '',
    onChange: handleChange(field),
    onBlur: handleBlur(field),
    name: String(field),
    id: String(field),
  }), [values, handleChange, handleBlur]);

  const getFieldMeta = useCallback((field: keyof T) => ({
    error: errors[field],
    touched: touched[field] ?? false,
    dirty: values[field] !== initialValues[field],
  }), [errors, touched, values, initialValues]);

  return {
    values,
    errors,
    touched,
    isValid,
    isDirty,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    setValue,
    setValues,
    setError,
    setErrors,
    clearErrors,
    reset,
    validate,
    validateField: validateFieldByName,
    getFieldProps,
    getFieldMeta,
  };
}

// =============================================================================
// Utility Components
// =============================================================================

export interface FormFieldProps {
  label: string;
  error?: string;
  touched?: boolean;
  required?: boolean;
  helpText?: string;
  children: React.ReactNode;
}

export const FormField: React.FC<FormFieldProps> = ({
  label,
  error,
  touched,
  required,
  helpText,
  children,
}) => {
  const showError = touched && error;
  
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 mr-1">*</span>}
      </label>
      {children}
      {helpText && !showError && (
        <p className="mt-1 text-sm text-gray-500">{helpText}</p>
      )}
      {showError && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default useForm;

