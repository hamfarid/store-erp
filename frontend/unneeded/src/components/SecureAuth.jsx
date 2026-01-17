/**
 * مكون المصادقة الآمنة
 * ملف: SecureAuth.jsx
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import encryption from '../utils/encryption.js'
import secureApi from '../utils/secureApi.js'

const SecureAuth = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [passwordStrength, setPasswordStrength] = useState(null)
  const [showPassword, setShowPassword] = useState(false)
  const [attempts, setAttempts] = useState(0)
  const [lockoutTime, setLockoutTime] = useState(null)
  
  const navigate = useNavigate()
  const maxAttempts = 5
  const lockoutDuration = 15 * 60 * 1000 // 15 دقيقة

  useEffect(() => {
    // فحص إذا كان المستخدم مسجل دخول مسبقاً
    checkExistingAuth()
    
    // فحص حالة القفل
    checkLockoutStatus()
  }, [])

  /**
   * فحص المصادقة الموجودة
   */
  const checkExistingAuth = () => {
    const token = localStorage.getItem('user_token')
    const encryptedUserData = encryption.getSecureStorage('user_data')
    
    if (token && encryptedUserData) {
      // التحقق من صحة الرمز المميز
      verifyToken(token)
    }
  }

  /**
   * التحقق من صحة الرمز المميز
   */
  const verifyToken = async (token) => {
    try {
      const response = await secureApi.post('/api/auth/verify-token', { token })
      
      if (response.success) {
        // إعادة توجيه للوحة التحكم
        navigate('/dashboard')
      } else {
        // مسح البيانات غير الصحيحة
        clearAuthData()
      }
    } catch (error) {
      clearAuthData()
    }
  }

  /**
   * فحص حالة القفل
   */
  const checkLockoutStatus = () => {
    const lockoutData = localStorage.getItem('auth_lockout')
    
    if (lockoutData) {
      const { timestamp, attempts: savedAttempts } = JSON.parse(lockoutData)
      const currentTime = Date.now()
      
      if (currentTime - timestamp < lockoutDuration) {
        setLockoutTime(timestamp + lockoutDuration)
        setAttempts(savedAttempts)
      } else {
        // انتهت فترة القفل
        localStorage.removeItem('auth_lockout')
        setAttempts(0)
      }
    }
  }

  /**
   * معالجة تغيير الحقول
   */
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))

    // فحص قوة كلمة المرور
    if (name === 'password') {
      const strength = encryption.checkPasswordStrength(value)
      setPasswordStrength(strength)
    }

    // مسح رسالة الخطأ عند الكتابة
    if (error) {
      setError('')
    }
  }

  /**
   * معالجة تسجيل الدخول
   */
  const handleLogin = async (e) => {
    e.preventDefault()
    
    // فحص حالة القفل
    if (lockoutTime && Date.now() < lockoutTime) {
      const remainingTime = Math.ceil((lockoutTime - Date.now()) / 60000)
      setError(`تم قفل الحساب. يرجى المحاولة بعد ${remainingTime} دقيقة`)
      return
    }

    // التحقق من صحة البيانات
    if (!formData.username || !formData.password) {
      setError('يرجى إدخال اسم المستخدم وكلمة المرور')
      return
    }

    setLoading(true)
    setError('')

    try {
      // تشفير بيانات تسجيل الدخول
      const encryptedCredentials = encryption.encryptFormData({
        username: formData.username,
        password: formData.password,
        timestamp: Date.now(),
        fingerprint: await generateDeviceFingerprint()
      })

      // إرسال طلب تسجيل الدخول
      const response = await secureApi.post('/api/auth/login', encryptedCredentials)

      if (response.success) {
        // حفظ بيانات المصادقة
        await saveAuthData(response)
        
        // مسح محاولات الفشل
        localStorage.removeItem('auth_lockout')
        setAttempts(0)
        
        // إعادة توجيه للوحة التحكم
        navigate('/dashboard')
      } else {
        handleLoginFailure(response.message || 'فشل في تسجيل الدخول')
      }
    } catch (error) {
      handleLoginFailure(error.message || 'خطأ في الاتصال بالخادم')
    } finally {
      setLoading(false)
    }
  }

  /**
   * معالجة فشل تسجيل الدخول
   */
  const handleLoginFailure = (message) => {
    const newAttempts = attempts + 1
    setAttempts(newAttempts)
    setError(message)

    if (newAttempts >= maxAttempts) {
      // قفل الحساب
      const lockoutData = {
        timestamp: Date.now(),
        attempts: newAttempts
      }
      
      localStorage.setItem('auth_lockout', JSON.stringify(lockoutData))
      setLockoutTime(Date.now() + lockoutDuration)
      
      setError(`تم تجاوز الحد المسموح من المحاولات. تم قفل الحساب لمدة 15 دقيقة`)
    } else {
      setError(`${message}. المحاولات المتبقية: ${maxAttempts - newAttempts}`)
    }
  }

  /**
   * حفظ بيانات المصادقة
   */
  const saveAuthData = async (response) => {
    try {
      // حفظ الرمز المميز
      localStorage.setItem('user_token', response.token)
      
      // حفظ مفاتيح API
      if (response.api_key && response.api_secret) {
        secureApi.setApiCredentials(response.api_key, response.api_secret)
      }
      
      // حفظ بيانات المستخدم مشفرة
      if (response.user) {
        encryption.setSecureStorage('user_data', response.user)
      }
      
      // حفظ إعدادات الجلسة
      const sessionData = {
        loginTime: Date.now(),
        rememberMe: formData.rememberMe,
        deviceFingerprint: await generateDeviceFingerprint()
      }
      
      encryption.setSecureStorage('session_data', sessionData)
      
    } catch (error) {
      }
  }

  /**
   * مسح بيانات المصادقة
   */
  const clearAuthData = () => {
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_data')
    localStorage.removeItem('session_data')
    secureApi.clearApiCredentials()
    encryption.clearSensitiveData()
  }

  /**
   * إنشاء بصمة الجهاز
   */
  const generateDeviceFingerprint = async () => {
    try {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      ctx.textBaseline = 'top'
      ctx.font = '14px Arial'
      ctx.fillText('Device fingerprint', 2, 2)
      
      const fingerprint = {
        screen: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: navigator.language,
        platform: navigator.platform,
        userAgent: navigator.userAgent.substring(0, 100),
        canvas: canvas.toDataURL().substring(0, 100)
      }
      
      return btoa(JSON.stringify(fingerprint))
    } catch (error) {
      return 'unknown'
    }
  }

  /**
   * تبديل إظهار كلمة المرور
   */
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword)
  }

  /**
   * إنشاء كلمة مرور قوية
   */
  // eslint-disable-next-line no-unused-vars
  const generateStrongPassword = () => {
    const strongPassword = encryption.generateSecurePassword(12)
    setFormData(prev => ({ ...prev, password: strongPassword }))
    
    const strength = encryption.checkPasswordStrength(strongPassword)
    setPasswordStrength(strength)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-secondary-100">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-2xl">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-foreground mb-2">
            تسجيل دخول آمن
          </h2>
          <p className="text-muted-foreground">
            نظام إدارة المخزون المحمي
          </p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          {/* حقل اسم المستخدم */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-foreground mb-2">
              اسم المستخدم
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              value={formData.username}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="أدخل اسم المستخدم"
              disabled={loading || (lockoutTime && Date.now() < lockoutTime)}
            />
          </div>

          {/* حقل كلمة المرور */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
              كلمة المرور
            </label>
            <div className="relative">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                required
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent pr-10"
                placeholder="أدخل كلمة المرور"
                disabled={loading || (lockoutTime && Date.now() < lockoutTime)}
              />
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
            
            {/* مؤشر قوة كلمة المرور */}
            {passwordStrength && formData.password && (
              <div className="mt-2">
                <div className="flex items-center space-x-2">
                  <div className={`h-2 w-full rounded ${
                    passwordStrength.strength === 'قوي' ? 'bg-primary/100' :
                    passwordStrength.strength === 'متوسط' ? 'bg-accent/100' : 'bg-destructive/100'
                  }`}></div>
                  <span className={`text-sm ${
                    passwordStrength.strength === 'قوي' ? 'text-primary' :
                    passwordStrength.strength === 'متوسط' ? 'text-accent' : 'text-destructive'
                  }`}>
                    {passwordStrength.strength}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* تذكرني */}
          <div className="flex items-center">
            <input
              id="rememberMe"
              name="rememberMe"
              type="checkbox"
              checked={formData.rememberMe}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-border rounded"
              disabled={loading}
            />
            <label htmlFor="rememberMe" className="mr-2 block text-sm text-foreground">
              تذكرني
            </label>
          </div>

          {/* رسالة الخطأ */}
          {error && (
            <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* زر تسجيل الدخول */}
          <button
            type="submit"
            disabled={loading || (lockoutTime && Date.now() < lockoutTime)}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                جاري تسجيل الدخول...
              </div>
            ) : (
              'تسجيل الدخول'
            )}
          </button>
        </form>

        {/* معلومات الأمان */}
        <div className="text-center text-xs text-gray-500">
          <p>🔐 محمي بتشفير AES-256</p>
          <p>🛡️ مصادقة ثنائية العامل متاحة</p>
        </div>
      </div>
    </div>
  )
}

export default SecureAuth

