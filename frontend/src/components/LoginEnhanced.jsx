import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Eye, EyeOff, Lock, LogIn, User, AlertCircle, CheckCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { isSuccess, getErrorMessage } from '../utils/responseHelper'

/**
 * صفحة تسجيل الدخول المحسّنة
 * Enhanced Login Page with improved validation and UX
 */
const LoginEnhanced = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  
  // State management
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [validationErrors, setValidationErrors] = useState({})
  const [touched, setTouched] = useState({})
  const [rememberMe, setRememberMe] = useState(false)

  // Load saved credentials if "Remember Me" was checked
  useEffect(() => {
    const savedUsername = localStorage.getItem('rememberedUsername')
    if (savedUsername) {
      setCredentials(prev => ({ ...prev, username: savedUsername }))
      setRememberMe(true)
    }
  }, [])

  /**
   * Validate individual field
   */
  const validateField = (name, value) => {
    const errors = {}

    if (name === 'username') {
      if (!value || value.trim() === '') {
        errors.username = 'اسم المستخدم مطلوب'
      } else if (value.length < 3) {
        errors.username = 'اسم المستخدم يجب أن يكون 3 أحرف على الأقل'
      } else if (value.length > 50) {
        errors.username = 'اسم المستخدم يجب أن لا يتجاوز 50 حرف'
      } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        errors.username = 'اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط'
      }
    }

    if (name === 'password') {
      if (!value || value.trim() === '') {
        errors.password = 'كلمة المرور مطلوبة'
      } else if (value.length < 6) {
        errors.password = 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'
      } else if (value.length > 100) {
        errors.password = 'كلمة المرور يجب أن لا تتجاوز 100 حرف'
      }
    }

    return errors
  }

  /**
   * Validate all fields
   */
  const validateForm = () => {
    const usernameErrors = validateField('username', credentials.username)
    const passwordErrors = validateField('password', credentials.password)
    
    const allErrors = { ...usernameErrors, ...passwordErrors }
    setValidationErrors(allErrors)
    
    return Object.keys(allErrors).length === 0
  }

  /**
   * Handle input change with validation
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target
    
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }))

    // Clear error when user starts typing
    if (error) setError('')

    // Validate field if it has been touched
    if (touched[name]) {
      const fieldErrors = validateField(name, value)
      setValidationErrors(prev => ({
        ...prev,
        ...fieldErrors,
        [name]: fieldErrors[name] || undefined
      }))
    }
  }

  /**
   * Handle field blur (mark as touched)
   */
  const handleBlur = (e) => {
    const { name, value } = e.target
    
    setTouched(prev => ({
      ...prev,
      [name]: true
    }))

    // Validate field on blur
    const fieldErrors = validateField(name, value)
    setValidationErrors(prev => ({
      ...prev,
      ...fieldErrors
    }))
  }

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Mark all fields as touched
    setTouched({
      username: true,
      password: true
    })

    // Validate form
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setError('')

    try {
      // Call login API
      const result = await login(credentials.username, credentials.password)

      if (isSuccess(result)) {
        // Save username if "Remember Me" is checked
        if (rememberMe) {
          localStorage.setItem('rememberedUsername', credentials.username)
        } else {
          localStorage.removeItem('rememberedUsername')
        }

        // Redirect to dashboard
        navigate('/dashboard')
      } else {
        setError(getErrorMessage(result, 'خطأ في تسجيل الدخول'))
      }
    } catch (error) {
      setError(error.message || 'حدث خطأ أثناء تسجيل الدخول')
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Quick demo login
   */
  const handleDemoLogin = () => {
    setCredentials({
      username: 'admin',
      password: 'admin123'
    })
    setTouched({})
    setValidationErrors({})
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-center">
            <div className="mx-auto h-20 w-20 bg-white rounded-2xl flex items-center justify-center mb-4 shadow-lg">
              <svg className="h-12 w-12 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-white mb-2">تسجيل الدخول</h2>
            <p className="text-blue-100">نظام إدارة المخزون</p>
          </div>

          {/* Form */}
          <div className="p-8" dir="rtl">
            {/* Global Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border-r-4 border-red-500 rounded-lg flex items-start">
                <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 ml-3" />
                <div>
                  <p className="text-red-800 font-medium">خطأ</p>
                  <p className="text-red-600 text-sm mt-1">{error}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Username Field */}
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                  اسم المستخدم <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <User className={`h-5 w-5 ${validationErrors.username ? 'text-red-400' : 'text-gray-400'}`} />
                  </div>
                  <input
                    id="username"
                    name="username"
                    type="text"
                    value={credentials.username}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
                    className={`block w-full pr-10 pl-3 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                      validationErrors.username
                        ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                    }`}
                    placeholder="أدخل اسم المستخدم"
                    disabled={isLoading}
                  />
                  {touched.username && !validationErrors.username && credentials.username && (
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                  )}
                </div>
                {touched.username && validationErrors.username && (
                  <p className="mt-2 text-sm text-red-600 flex items-center">
                    <AlertCircle className="h-4 w-4 ml-1" />
                    {validationErrors.username}
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  كلمة المرور <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <Lock className={`h-5 w-5 ${validationErrors.password ? 'text-red-400' : 'text-gray-400'}`} />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    value={credentials.password}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
                    className={`block w-full pr-10 pl-10 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                      validationErrors.password
                        ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                    }`}
                    placeholder="أدخل كلمة المرور"
                    disabled={isLoading}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 left-0 pl-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={isLoading}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                    )}
                  </button>
                </div>
                {touched.password && validationErrors.password && (
                  <p className="mt-2 text-sm text-red-600 flex items-center">
                    <AlertCircle className="h-4 w-4 ml-1" />
                    {validationErrors.password}
                  </p>
                )}
              </div>

              {/* Remember Me */}
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  disabled={isLoading}
                />
                <label htmlFor="remember-me" className="mr-2 block text-sm text-gray-700">
                  تذكرني
                </label>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-base font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white ml-2"></div>
                    جاري تسجيل الدخول...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <LogIn className="h-5 w-5 ml-2" />
                    تسجيل الدخول
                  </div>
                )}
              </button>
            </form>

            {/* Demo Credentials */}
            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">أو</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleDemoLogin}
                disabled={isLoading}
                className="mt-4 w-full flex justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                استخدام بيانات تجريبية (admin / admin123)
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            نظام إدارة المخزون © 2025
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginEnhanced

