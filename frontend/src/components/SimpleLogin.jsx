import React, { useState } from 'react'
import { Eye, EyeOff, Lock, LogIn, User } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const SimpleLogin = () => {
  const [credentials, setCredentials] = useState({
    username: 'admin',
    password: 'admin123'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      // استخدام وظيفة login من AuthContext
      const result = await login(credentials.username, credentials.password)

      if (result.success) {
        // تم تسجيل الدخول بنجاح
        } else {
        setError(result.error || 'خطأ في تسجيل الدخول')
      }
    } catch (error) {
      setError('حدث خطأ أثناء تسجيل الدخول')
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-secondary-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="bg-primary-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <User className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-2">نظام إدارة المخزون</h1>
          <p className="text-muted-foreground">Gaara Seeds - نظام إدارة البذور والمخزون</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center text-foreground mb-6" dir="rtl">
            تسجيل الدخول
          </h2>

          {error && (
            <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg mb-4" dir="rtl">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username Field */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                اسم المستخدم
              </label>
              <div className="relative">
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={credentials.username}
                  onChange={handleInputChange}
                  className="w-full pl-10 pr-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="أدخل اسم المستخدم"
                  dir="ltr"
                />
                <User className="absolute right-3 top-3.5 h-5 w-5 text-gray-400" />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                كلمة المرور
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={credentials.password}
                  onChange={handleInputChange}
                  className="w-full pl-10 pr-10 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="أدخل كلمة المرور"
                  dir="ltr"
                />
                <Lock className="absolute right-3 top-3.5 h-5 w-5 text-gray-400" />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-3 top-3.5 text-gray-400 hover:text-muted-foreground"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  <LogIn className="w-5 h-5 ml-2" />
                  <span dir="rtl">تسجيل الدخول</span>
                </>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-muted/50 rounded-lg" dir="rtl">
            <h3 className="text-sm font-medium text-foreground mb-2">بيانات تجريبية:</h3>
            <div className="text-sm text-muted-foreground space-y-1">
              <p><strong>اسم المستخدم:</strong> admin</p>
              <p><strong>كلمة المرور:</strong> admin123</p>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center text-sm text-gray-500" dir="rtl">
            <p>© 2024 Gaara Seeds. جميع الحقوق محفوظة.</p>
          </div>
        </div>

        {/* System Info */}
        <div className="mt-6 text-center text-sm text-muted-foreground">
          <p>نظام إدارة المخزون المتقدم</p>
          <p>الإصدار 1.0.0</p>
        </div>
      </div>
    </div>
  )
}

export default SimpleLogin

