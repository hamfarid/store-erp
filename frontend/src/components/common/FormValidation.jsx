import React, { useState, useCallback } from 'react'
import PropTypes from 'prop-types'
import './FormValidation.css'

// Validation Rules
export const validationRules = {
  required: (value, message = 'هذا الحقل مطلوب') => {
    if (value === null || value === undefined || value === '') {
      return message
    }
    return null
  },

  minLength: (min, message) => (value) => {
    if (value && value.length < min) {
      return message || `يجب أن يكون الطول ${min} أحرف على الأقل`
    }
    return null
  },

  maxLength: (max, message) => (value) => {
    if (value && value.length > max) {
      return message || `يجب أن لا يزيد الطول عن ${max} أحرف`
    }
    return null
  },

  email: (value, message = 'البريد الإلكتروني غير صحيح') => {
    if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return message
    }
    return null
  },

  phone: (value, message = 'رقم الهاتف غير صحيح') => {
    if (value && !/^[+]?[0-9\s\-()]{10,}$/.test(value)) {
      return message
    }
    return null
  },

  number: (value, message = 'يجب أن يكون رقماً') => {
    if (value && isNaN(Number(value))) {
      return message
    }
    return null
  },

  positiveNumber: (value, message = 'يجب أن يكون رقماً موجباً') => {
    if (value && (isNaN(Number(value)) || Number(value) <= 0)) {
      return message
    }
    return null
  },

  min: (min, message) => (value) => {
    if (value && Number(value) < min) {
      return message || `يجب أن يكون ${min} على الأقل`
    }
    return null
  },

  max: (max, message) => (value) => {
    if (value && Number(value) > max) {
      return message || `يجب أن لا يزيد عن ${max}`
    }
    return null
  },

  pattern: (regex, message) => (value) => {
    if (value && !regex.test(value)) {
      return message || 'التنسيق غير صحيح'
    }
    return null
  },

  custom: (validator, message) => (value) => {
    if (!validator(value)) {
      return message || 'القيمة غير صحيحة'
    }
    return null
  },

  // Arabic text validation
  arabicOnly: (value, message = 'يجب أن يحتوي على أحرف عربية فقط') => {
    if (value && !/^[\u0600-\u06FF\s]+$/.test(value)) {
      return message
    }
    return null
  },

  // SKU validation
  sku: (value, message = 'كود المنتج غير صحيح') => {
    if (value && !/^[A-Z0-9-]{3,20}$/.test(value)) {
      return message
    }
    return null
  },

  // Price validation
  price: (value, message = 'السعر غير صحيح') => {
    if (value && (isNaN(Number(value)) || Number(value) < 0)) {
      return message
    }
    return null
  }
}

// Form Validation Hook
export const useFormValidation = (initialValues = {}, validationSchema = {}) => {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateField = useCallback((name, value) => {
    const rules = validationSchema[name]
    if (!rules) return null

    for (const rule of rules) {
      const error = rule(value)
      if (error) return error
    }
    return null
  }, [validationSchema])

  const validateForm = useCallback(() => {
    const newErrors = {}
    let isValid = true

    Object.keys(validationSchema).forEach(name => {
      const error = validateField(name, values[name])
      if (error) {
        newErrors[name] = error
        isValid = false
      }
    })

    setErrors(newErrors)
    return isValid
  }, [values, validateField, validationSchema])

  const setValue = useCallback((name, value) => {
    setValues(prev => ({ ...prev, [name]: value }))
    
    // Validate field if it was touched
    if (touched[name]) {
      const error = validateField(name, value)
      setErrors(prev => ({ ...prev, [name]: error }))
    }
  }, [touched, validateField])

  const setFieldTouched = useCallback((name, isTouched = true) => {
    setTouched(prev => ({ ...prev, [name]: isTouched }))
    
    if (isTouched) {
      const error = validateField(name, values[name])
      setErrors(prev => ({ ...prev, [name]: error }))
    }
  }, [values, validateField])

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target
    const fieldValue = type === 'checkbox' ? checked : value
    setValue(name, fieldValue)
  }, [setValue])

  const handleBlur = useCallback((e) => {
    const { name } = e.target
    setFieldTouched(name, true)
  }, [setFieldTouched])

  const handleSubmit = useCallback(async (onSubmit) => {
    setIsSubmitting(true)
    
    // Mark all fields as touched
    const allTouched = Object.keys(validationSchema).reduce((acc, key) => {
      acc[key] = true
      return acc
    }, {})
    setTouched(allTouched)

    const isValid = validateForm()
    
    if (isValid && onSubmit) {
      try {
        await onSubmit(values)
      } catch (error) {
        }
    }
    
    setIsSubmitting(false)
    return isValid
  }, [values, validateForm, validationSchema])

  const reset = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
    setIsSubmitting(false)
  }, [initialValues])

  const isValid = Object.keys(errors).length === 0
  const hasErrors = Object.values(errors).some(error => error !== null)

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    hasErrors,
    setValue,
    setFieldTouched,
    handleChange,
    handleBlur,
    handleSubmit,
    validateForm,
    reset
  }
}

// Validated Input Component
export const ValidatedInput = ({
  name,
  label,
  type = 'text',
  placeholder,
  required = false,
  validation,
  className = '',
  ...props
}) => {
  const [value, setValue] = useState('')
  const [error, setError] = useState(null)
  const [touched, setTouched] = useState(false)

  const validateValue = useCallback((val) => {
    if (!validation) return null
    
    for (const rule of validation) {
      const err = rule(val)
      if (err) return err
    }
    return null
  }, [validation])

  const handleChange = (e) => {
    const newValue = e.target.value
    setValue(newValue)
    
    if (touched) {
      setError(validateValue(newValue))
    }
    
    if (props.onChange) {
      props.onChange(e)
    }
  }

  const handleBlur = (e) => {
    setTouched(true)
    setError(validateValue(value))
    
    if (props.onBlur) {
      props.onBlur(e)
    }
  }

  const inputClass = `
    validated-input__field
    ${error ? 'validated-input__field--error' : ''}
    ${className}
  `.trim()

  return (
    <div className="validated-input">
      {label && (
        <label className="validated-input__label" htmlFor={name}>
          {label}
          {required && <span className="validated-input__required">*</span>}
        </label>
      )}
      
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        placeholder={placeholder}
        className={inputClass}
        onChange={handleChange}
        onBlur={handleBlur}
        {...props}
      />
      
      {error && touched && (
        <div className="validated-input__error">
          <i className="fas fa-exclamation-circle"></i>
          {error}
        </div>
      )}
    </div>
  )
}

// Validated Select Component
export const ValidatedSelect = ({
  name,
  label,
  options = [],
  placeholder = 'اختر...',
  required = false,
  validation,
  className = '',
  ...props
}) => {
  const [value, setValue] = useState('')
  const [error, setError] = useState(null)
  const [touched, setTouched] = useState(false)

  const validateValue = useCallback((val) => {
    if (!validation) return null
    
    for (const rule of validation) {
      const err = rule(val)
      if (err) return err
    }
    return null
  }, [validation])

  const handleChange = (e) => {
    const newValue = e.target.value
    setValue(newValue)
    
    if (touched) {
      setError(validateValue(newValue))
    }
    
    if (props.onChange) {
      props.onChange(e)
    }
  }

  const handleBlur = (e) => {
    setTouched(true)
    setError(validateValue(value))
    
    if (props.onBlur) {
      props.onBlur(e)
    }
  }

  const selectClass = `
    validated-select__field
    ${error ? 'validated-select__field--error' : ''}
    ${className}
  `.trim()

  return (
    <div className="validated-select">
      {label && (
        <label className="validated-select__label" htmlFor={name}>
          {label}
          {required && <span className="validated-select__required">*</span>}
        </label>
      )}
      
      <select
        id={name}
        name={name}
        value={value}
        className={selectClass}
        onChange={handleChange}
        onBlur={handleBlur}
        {...props}
      >
        <option value="">{placeholder}</option>
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      
      {error && touched && (
        <div className="validated-select__error">
          <i className="fas fa-exclamation-circle"></i>
          {error}
        </div>
      )}
    </div>
  )
}

// Form Summary Component
export const FormSummary = ({ errors, touched }) => {
  const visibleErrors = Object.keys(errors)
    .filter(key => touched[key] && errors[key])
    .map(key => errors[key])

  if (visibleErrors.length === 0) return null

  return (
    <div className="form-summary">
      <div className="form-summary__header">
        <i className="fas fa-exclamation-triangle"></i>
        <span>يرجى تصحيح الأخطاء التالية:</span>
      </div>
      <ul className="form-summary__list">
        {visibleErrors.map((error, index) => (
          <li key={index} className="form-summary__item">{error}</li>
        ))}
      </ul>
    </div>
  )
}

export default useFormValidation
