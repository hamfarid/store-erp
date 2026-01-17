import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'
import { toast } from 'react-hot-toast'

const LoginAdvanced = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    company: '',
    remember: false
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [_selectedCompany, _setSelectedCompany] = useState('')

  // بيانات تجريبية للشركات
  const companies = [
    { id: 1, name: 'الشركة الرئيسية', name_en: 'Main Company', active: true },
    { id: 2, name: 'فرع القاهرة', name_en: 'Cairo Branch', active: true },
    { id: 3, name: 'فرع الإسكندرية', name_en: 'Alexandria Branch', active: true }
  ]

  // بيانات تجريبية للمستخدمين
  const demoUsers = [
    { username: 'admin', password: 'admin123', name: 'مدير النظام', role: 'مدير عام', company_id: 1 },
    { username: 'manager', password: 'manager123', name: 'مدير المخزون', role: 'مدير مخزون', company_id: 1 },
    { username: 'user', password: 'user123', name: 'موظف المبيعات', role: 'موظف', company_id: 1 }
  ]

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // التحقق من البيانات
      if (!formData.username || !formData.password) {
        toast.error('يرجى إدخال اسم المستخدم وكلمة المرور')
        return
      }

      // محاكاة تسجيل الدخول
      await new Promise(resolve => setTimeout(resolve, 1500))

      // البحث عن المستخدم
      const user = demoUsers.find(u => 
        u.username === formData.username && u.password === formData.password
      )

      if (!user) {
        toast.error('اسم المستخدم أو كلمة المرور غير صحيحة')
        return
      }

      // البحث عن الشركة
      const company = companies.find(c => c.id === user.company_id)

      // إنشاء بيانات المستخدم
      const userData = {
        id: user.username === 'admin' ? 1 : user.username === 'manager' ? 2 : 3,
        username: user.username,
        name: user.name,
        role: user.role,
        company: company,
        permissions: user.username === 'admin' ? ['all'] : ['read', 'write'],
        last_login: new Date().toISOString(),
        avatar: null
      }

      // إنشاء توكن وهمي
      const token = `token_${user.username}_${Date.now()}`

      // تسجيل الدخول
      onLogin(userData, token)
      toast.success(`مرحباً ${user.name}`)

    } catch (error) {
      toast.error('حدث خطأ أثناء تسجيل الدخول')
      } finally {
      setLoading(false)
    }
  }

  const handleDemoLogin = (username) => {
    setFormData(prev => ({
      ...prev,
      username,
      password: `${username}123`
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* شعار النظام */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
            <Package className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-2">نظام ERP المتقدم</h1>
          <p className="text-muted-foreground">إدارة شاملة ومتكاملة للمخزون والمبيعات</p>
        </div>

        {/* نموذج تسجيل الدخول */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-foreground mb-2">تسجيل الدخول</h2>
            <p className="text-muted-foreground">أدخل بياناتك للوصول إلى النظام</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* اسم المستخدم */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم المستخدم
              </label>
              <div className="relative">
                <User className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className="w-full pr-10 pl-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="أدخل اسم المستخدم"
                  required
                />
              </div>
            </div>

            {/* كلمة المرور */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                كلمة المرور
              </label>
              <div className="relative">
                <Lock className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className="w-full pr-10 pl-12 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="أدخل كلمة المرور"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-3 top-3 text-gray-400 hover:text-muted-foreground"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>

            {/* تذكرني */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="remember"
                  checked={formData.remember}
                  onChange={handleInputChange}
                  className="rounded border-border text-primary-600 focus:ring-primary-500"
                />
                <span className="mr-2 text-sm text-foreground">تذكرني</span>
              </label>
              <a href="#" className="text-sm text-primary-600 hover:text-primary-500">
                نسيت كلمة المرور؟
              </a>
            </div>

            {/* زر تسجيل الدخول */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white ml-2"></div>
                  جاري تسجيل الدخول...
                </div>
              ) : (
                'تسجيل الدخول'
              )}
            </button>
          </form>

          {/* حسابات تجريبية */}
          <div className="mt-8 pt-6 border-t border-border">
            <h3 className="text-sm font-medium text-foreground mb-4">حسابات تجريبية:</h3>
            <div className="space-y-2">
              {demoUsers.map((user) => (
                <button
                  key={user.username}
                  onClick={() => handleDemoLogin(user.username)}
                  className="w-full text-right p-3 bg-muted/50 hover:bg-muted rounded-lg transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium text-foreground">{user.name}</div>
                      <div className="text-xs text-gray-500">{user.role}</div>
                    </div>
                    <div className="text-xs text-gray-400">
                      {user.username} / {user.password}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ميزات النظام */}
        <div className="mt-8 grid grid-cols-2 gap-4">
          <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 text-center">
            <Shield className="w-8 h-8 text-primary-600 mx-auto mb-2" />
            <h3 className="font-medium text-foreground mb-1">أمان متقدم</h3>
            <p className="text-xs text-muted-foreground">حماية شاملة للبيانات</p>
          </div>
          <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 text-center">
            <Globe className="w-8 h-8 text-primary mx-auto mb-2" />
            <h3 className="font-medium text-foreground mb-1">تكامل شامل</h3>
            <p className="text-xs text-muted-foreground">ربط جميع الأنظمة</p>
          </div>
        </div>

        {/* معلومات النظام */}
        <div className="mt-6 text-center">
          <div className="flex items-center justify-center mb-2">
            <CheckCircle className="w-4 h-4 text-green-500 ml-1" />
            <span className="text-sm text-muted-foreground">النظام متاح ويعمل بكفاءة</span>
          </div>
          <p className="text-xs text-gray-500">
            الإصدار 2.0.0 | آخر تحديث: ديسمبر 2024
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginAdvanced

