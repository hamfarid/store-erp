import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const DynamicForm = ({
  fields = [],
  initialData = {},
  onSubmit,
  onCancel,
  loading = false,
  title = "نموذج",
  submitText = "حفظ",
  cancelText = "إلغاء",
  className = ""
}) => {
  const [formData, setFormData] = useState(initialData)
  const [errors, setErrors] = useState({})
  const [showPasswords, setShowPasswords] = useState({})

  useEffect(() => {
    setFormData(initialData)
  }, [initialData])

  const handleChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }))
    
    // إزالة الخطأ عند التعديل
    if (errors[fieldName]) {
      setErrors(prev => ({
        ...prev,
        [fieldName]: null
      }))
    }
  }

  const validateField = (field, value) => {
    if (field.required && (!value || value.toString().trim() === '')) {
      return `${field.label} مطلوب`
    }

    if (field.type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(value)) {
        return 'البريد الإلكتروني غير صحيح'
      }
    }

    if (field.type === 'number' && value) {
      if (isNaN(value)) {
        return 'يجب أن يكون رقم'
      }
      if (field.min !== undefined && value < field.min) {
        return `يجب أن يكون أكبر من ${field.min}`
      }
      if (field.max !== undefined && value > field.max) {
        return `يجب أن يكون أصغر من ${field.max}`
      }
    }

    if (field.minLength && value && value.length < field.minLength) {
      return `يجب أن يكون على الأقل ${field.minLength} أحرف`
    }

    if (field.maxLength && value && value.length > field.maxLength) {
      return `يجب أن يكون أقل من ${field.maxLength} حرف`
    }

    if (field.pattern && value) {
      const regex = new RegExp(field.pattern)
      if (!regex.test(value)) {
        return field.patternMessage || 'تنسيق غير صحيح'
      }
    }

    return null
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const newErrors = {}
    fields.forEach(field => {
      const error = validateField(field, formData[field.name])
      if (error) {
        newErrors[field.name] = error
      }
    })

    setErrors(newErrors)

    if (Object.keys(newErrors).length === 0) {
      onSubmit(formData)
    }
  }

  const togglePasswordVisibility = (fieldName) => {
    setShowPasswords(prev => ({
      ...prev,
      [fieldName]: !prev[fieldName]
    }))
  }

  const renderField = (field) => {
    const value = formData[field.name] || ''
    const error = errors[field.name]
    const isPassword = field.type === 'password'
    const showPassword = showPasswords[field.name]

    const baseInputClasses = `w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors ${
      error ? 'border-red-500' : 'border-border'
    }`

    switch (field.type) {
      case 'text':
      case 'email':
      case 'number':
      case 'password':
        return (
          <div key={field.name} className="space-y-1">
            <label className="block text-sm font-medium text-foreground">
              {field.label}
              {field.required && <span className="text-red-500 mr-1">*</span>}
            </label>
            <div className="relative">
              <input
                type={isPassword && !showPassword ? 'password' : field.type}
                value={value}
                onChange={(e) => handleChange(field.name, e.target.value)}
                placeholder={field.placeholder}
                disabled={field.disabled || loading}
                className={baseInputClasses}
                min={field.min}
                max={field.max}
                step={field.step}
              />
              {isPassword && (
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility(field.name)}
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-muted-foreground"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              )}
            </div>
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
            {field.help && (
              <p className="text-sm text-gray-500">{field.help}</p>
            )}
          </div>
        )

      case 'textarea':
        return (
          <div key={field.name} className="space-y-1">
            <label className="block text-sm font-medium text-foreground">
              {field.label}
              {field.required && <span className="text-red-500 mr-1">*</span>}
            </label>
            <textarea
              value={value}
              onChange={(e) => handleChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              disabled={field.disabled || loading}
              rows={field.rows || 3}
              className={baseInputClasses}
            />
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
          </div>
        )

      case 'select':
        return (
          <div key={field.name} className="space-y-1">
            <label className="block text-sm font-medium text-foreground">
              {field.label}
              {field.required && <span className="text-red-500 mr-1">*</span>}
            </label>
            <select
              value={value}
              onChange={(e) => handleChange(field.name, e.target.value)}
              disabled={field.disabled || loading}
              className={baseInputClasses}
            >
              <option value="">اختر {field.label}</option>
              {field.options?.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
          </div>
        )

      case 'checkbox':
        return (
          <div key={field.name} className="space-y-1">
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={!!value}
                onChange={(e) => handleChange(field.name, e.target.checked)}
                disabled={field.disabled || loading}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-border rounded"
              />
              <label className="mr-2 text-sm font-medium text-foreground">
                {field.label}
                {field.required && <span className="text-red-500 mr-1">*</span>}
              </label>
            </div>
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
          </div>
        )

      case 'date':
        return (
          <div key={field.name} className="space-y-1">
            <label className="block text-sm font-medium text-foreground">
              {field.label}
              {field.required && <span className="text-red-500 mr-1">*</span>}
            </label>
            <div className="relative">
              <input
                type="date"
                value={value}
                onChange={(e) => handleChange(field.name, e.target.value)}
                disabled={field.disabled || loading}
                className={baseInputClasses}
              />
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            </div>
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
          </div>
        )

      case 'file':
        return (
          <div key={field.name} className="space-y-1">
            <label className="block text-sm font-medium text-foreground">
              {field.label}
              {field.required && <span className="text-red-500 mr-1">*</span>}
            </label>
            <div className="relative">
              <input
                type="file"
                onChange={(e) => handleChange(field.name, e.target.files[0])}
                disabled={field.disabled || loading}
                accept={field.accept}
                className={baseInputClasses}
              />
              <Upload className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            </div>
            {error && (
              <p className="text-sm text-destructive flex items-center">
                <AlertCircle className="w-4 h-4 ml-1" />
                {error}
              </p>
            )}
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-border ${className}`} dir="rtl">
      <div className="p-6 border-b border-border">
        <h2 className="text-lg font-semibold text-foreground">{title}</h2>
      </div>

      <form onSubmit={handleSubmit} className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {fields.map(renderField)}
        </div>

        <div className="flex items-center justify-end space-x-4 space-x-reverse mt-8 pt-6 border-t border-border">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="px-4 py-2 border border-border rounded-lg text-foreground hover:bg-muted/50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <X className="w-4 h-4 ml-1 inline" />
              {cancelText}
            </button>
          )}
          
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin ml-1"></div>
            ) : (
              <Save className="w-4 h-4 ml-1" />
            )}
            {submitText}
          </button>
        </div>
      </form>
    </div>
  )
}

export default DynamicForm

