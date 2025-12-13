import React from 'react'
import { AlertTriangle, CheckCircle, Info, X } from 'lucide-react'

// قواعد التحقق الأساسية
export const validationRules = {
  required: (value) => {
    if (value === null || value === undefined || value === '') {
      return 'هذا الحقل مطلوب'
    }
    return null
  },

  email: (value) => {
    if (!value) return null
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      return 'يرجى إدخال بريد إلكتروني صحيح'
    }
    return null
  },

  phone: (value) => {
    if (!value) return null
    const phoneRegex = /^01[0-9]{9}$/
    if (!phoneRegex.test(value)) {
      return 'يرجى إدخال رقم هاتف صحيح (01xxxxxxxxx)'
    }
    return null
  },

  minLength: (min) => (value) => {
    if (!value) return null
    if (value.length < min) {
      return `يجب أن يكون الطول ${min} أحرف على الأقل`
    }
    return null
  },

  maxLength: (max) => (value) => {
    if (!value) return null
    if (value.length > max) {
      return `يجب أن يكون الطول ${max} أحرف كحد أقصى`
    }
    return null
  },

  min: (min) => (value) => {
    if (value === null || value === undefined || value === '') return null
    const numValue = Number(value)
    if (isNaN(numValue) || numValue < min) {
      return `يجب أن تكون القيمة ${min} أو أكثر`
    }
    return null
  },

  max: (max) => (value) => {
    if (value === null || value === undefined || value === '') return null
    const numValue = Number(value)
    if (isNaN(numValue) || numValue > max) {
      return `يجب أن تكون القيمة ${max} أو أقل`
    }
    return null
  },

  number: (value) => {
    if (!value) return null
    if (isNaN(Number(value))) {
      return 'يجب أن تكون القيمة رقماً'
    }
    return null
  },

  integer: (value) => {
    if (!value) return null
    const numValue = Number(value)
    if (isNaN(numValue) || !Number.isInteger(numValue)) {
      return 'يجب أن تكون القيمة رقماً صحيحاً'
    }
    return null
  },

  positive: (value) => {
    if (!value) return null
    const numValue = Number(value)
    if (isNaN(numValue) || numValue <= 0) {
      return 'يجب أن تكون القيمة موجبة'
    }
    return null
  },

  url: (value) => {
    if (!value) return null
    try {
      new URL(value)
      return null
    } catch {
      return 'يرجى إدخال رابط صحيح'
    }
  },

  date: (value) => {
    if (!value) return null
    const date = new Date(value)
    if (isNaN(date.getTime())) {
      return 'يرجى إدخال تاريخ صحيح'
    }
    return null
  },

  futureDate: (value) => {
    if (!value) return null
    const date = new Date(value)
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    if (date <= today) {
      return 'يجب أن يكون التاريخ في المستقبل'
    }
    return null
  },

  pastDate: (value) => {
    if (!value) return null
    const date = new Date(value)
    const today = new Date()
    today.setHours(23, 59, 59, 999)
    if (date >= today) {
      return 'يجب أن يكون التاريخ في الماضي'
    }
    return null
  },

  match: (fieldName, otherValue) => (value) => {
    if (value !== otherValue) {
      return `يجب أن يطابق ${fieldName}`
    }
    return null
  },

  unique: (existingValues) => (value) => {
    if (!value) return null
    if (existingValues.includes(value)) {
      return 'هذه القيمة موجودة بالفعل'
    }
    return null
  },

  pattern: (regex, message) => (value) => {
    if (!value) return null
    if (!regex.test(value)) {
      return message || 'تنسيق غير صحيح'
    }
    return null
  }
}

// دالة التحقق من الحقل
export const validateField = (value, rules) => {
  if (!rules || rules.length === 0) return null

  for (const rule of rules) {
    const error = rule(value)
    if (error) return error
  }
  
  return null
}

// دالة التحقق من النموذج
export const validateForm = (data, fieldRules) => {
  const errors = {}
  let hasErrors = false

  Object.keys(fieldRules).forEach(fieldName => {
    const value = data[fieldName]
    const rules = fieldRules[fieldName]
    const error = validateField(value, rules)
    
    if (error) {
      errors[fieldName] = error
      hasErrors = true
    }
  })

  return { errors, isValid: !hasErrors }
}

// مكون عرض رسالة التحقق
export const ValidationMessage = ({ 
  error, 
  success, 
  info, 
  className = "" 
}) => {
  if (!error && !success && !info) return null

  const getConfig = () => {
    if (error) {
      return {
        icon: AlertTriangle,
        className: 'text-destructive bg-destructive/10 border-destructive/30',
        message: error
      }
    }
    if (success) {
      return {
        icon: CheckCircle,
        className: 'text-primary bg-primary/10 border-primary/30',
        message: success
      }
    }
    if (info) {
      return {
        icon: Info,
        className: 'text-primary-600 bg-primary-50 border-primary-200',
        message: info
      }
    }
  }

  const config = getConfig()
  const Icon = config.icon

  return (
    <div className={`flex items-center p-2 border rounded-md text-sm ${config.className} ${className}`}>
      <Icon className="w-4 h-4 ml-1 flex-shrink-0" />
      <span>{config.message}</span>
    </div>
  )
}

// مكون حقل إدخال مع التحقق
export const ValidatedInput = ({
  label,
  value,
  onChange,
  rules = [],
  type = 'text',
  placeholder,
  required = false,
  disabled = false,
  className = "",
  ...props
}) => {
  const [touched, setTouched] = React.useState(false)
  const error = touched ? validateField(value, rules) : null

  const handleBlur = () => {
    setTouched(true)
  }

  const handleChange = (e) => {
    onChange(e.target.value)
    if (touched) {
      // إعادة التحقق فوراً إذا كان الحقل قد تم لمسه
    }
  }

  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-foreground">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      
      <input
        type={type}
        value={value || ''}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors ${
          error 
            ? 'border-red-500 bg-destructive/10' 
            : 'border-border hover:border-gray-400'
        } ${disabled ? 'bg-muted cursor-not-allowed' : ''}`}
        {...props}
      />
      
      <ValidationMessage error={error} />
    </div>
  )
}

// مكون منطقة نص مع التحقق
export const ValidatedTextarea = ({
  label,
  value,
  onChange,
  rules = [],
  placeholder,
  required = false,
  disabled = false,
  rows = 3,
  className = "",
  ...props
}) => {
  const [touched, setTouched] = React.useState(false)
  const error = touched ? validateField(value, rules) : null

  const handleBlur = () => {
    setTouched(true)
  }

  const handleChange = (e) => {
    onChange(e.target.value)
  }

  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-foreground">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      
      <textarea
        value={value || ''}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        rows={rows}
        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors resize-vertical ${
          error 
            ? 'border-red-500 bg-destructive/10' 
            : 'border-border hover:border-gray-400'
        } ${disabled ? 'bg-muted cursor-not-allowed' : ''}`}
        {...props}
      />
      
      <ValidationMessage error={error} />
    </div>
  )
}

// مكون قائمة منسدلة مع التحقق
export const ValidatedSelect = ({
  label,
  value,
  onChange,
  options = [],
  rules = [],
  placeholder = "اختر...",
  required = false,
  disabled = false,
  className = "",
  ...props
}) => {
  const [touched, setTouched] = React.useState(false)
  const error = touched ? validateField(value, rules) : null

  const handleBlur = () => {
    setTouched(true)
  }

  const handleChange = (e) => {
    onChange(e.target.value)
  }

  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-foreground">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      
      <select
        value={value || ''}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={disabled}
        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors ${
          error 
            ? 'border-red-500 bg-destructive/10' 
            : 'border-border hover:border-gray-400'
        } ${disabled ? 'bg-muted cursor-not-allowed' : ''}`}
        {...props}
      >
        <option value="">{placeholder}</option>
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      
      <ValidationMessage error={error} />
    </div>
  )
}

// Hook للتحقق من النموذج
export const useFormValidation = (initialData = {}, fieldRules = {}) => {
  const [data, setData] = React.useState(initialData)
  const [errors, setErrors] = React.useState({})
  const [touched, setTouched] = React.useState({})

  const validateField = React.useCallback((fieldName, value) => {
    const rules = fieldRules[fieldName]
    if (!rules) return null

    for (const rule of rules) {
      const error = rule(value)
      if (error) return error
    }
    return null
  }, [fieldRules])

  const setFieldValue = React.useCallback((fieldName, value) => {
    setData(prev => ({ ...prev, [fieldName]: value }))
    
    if (touched[fieldName]) {
      const error = validateField(fieldName, value)
      setErrors(prev => ({ ...prev, [fieldName]: error }))
    }
  }, [touched, validateField])

  const setFieldTouched = React.useCallback((fieldName) => {
    setTouched(prev => ({ ...prev, [fieldName]: true }))
    
    const error = validateField(fieldName, data[fieldName])
    setErrors(prev => ({ ...prev, [fieldName]: error }))
  }, [data, validateField])

  const validateForm = React.useCallback(() => {
    const newErrors = {}
    let isValid = true

    Object.keys(fieldRules).forEach(fieldName => {
      const error = validateField(fieldName, data[fieldName])
      if (error) {
        newErrors[fieldName] = error
        isValid = false
      }
    })

    setErrors(newErrors)
    setTouched(Object.keys(fieldRules).reduce((acc, key) => {
      acc[key] = true
      return acc
    }, {}))

    return { isValid, errors: newErrors }
  }, [data, fieldRules, validateField])

  const resetForm = React.useCallback(() => {
    setData(initialData)
    setErrors({})
    setTouched({})
  }, [initialData])

  return {
    data,
    errors,
    touched,
    setFieldValue,
    setFieldTouched,
    validateForm,
    resetForm,
    isValid: Object.keys(errors).length === 0
  }
}

