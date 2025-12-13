import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Building, Bell, Shield
} from 'lucide-react'

const SystemSettingsAdvanced = () => {
  const [settings, setSettings] = useState({
    // إعدادات الشركة
    company: {
      name: 'Gaara Seeds',
      nameEn: 'Gaara Seeds Company',
      address: 'القاهرة، مصر',
      phone: '+20-1001234567',
      email: 'info@gaaraseeds.com',
      website: 'www.gaaraseeds.com',
      logo: '',
      taxNumber: '123456789',
      commercialRegister: 'CR-123456'
    },
    
    // إعدادات النظام
    system: {
      language: 'ar',
      timezone: 'Africa/Cairo',
      dateFormat: 'DD/MM/YYYY',
      currency: 'EGP',
      currencySymbol: 'ج.م',
      decimalPlaces: 2,
      backupFrequency: 'daily',
      sessionTimeout: 30
    },
    
    // إعدادات الإشعارات
    notifications: {
      emailNotifications: true,
      smsNotifications: false,
      lowStockAlert: true,
      expiryAlert: true,
      invoiceReminders: true,
      systemUpdates: true
    },
    
    // إعدادات الأمان
    security: {
      passwordMinLength: 8,
      passwordComplexity: true,
      twoFactorAuth: false,
      sessionSecurity: true,
      loginAttempts: 3,
      accountLockout: 15
    }
  })

  const [activeTab, setActiveTab] = useState('company')
  const [loading, setLoading] = useState(false)
  const [notification, setNotification] = useState(null)

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      // محاكاة حفظ الإعدادات
      await new Promise(resolve => setTimeout(resolve, 1000))
      showNotification('تم حفظ الإعدادات بنجاح')
    } catch (error) {
      showNotification('فشل في حفظ الإعدادات', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  const tabs = [
    { id: 'company', name: 'معلومات الشركة', icon: Building },
    { id: 'system', name: 'إعدادات النظام', icon: Settings },
    { id: 'notifications', name: 'الإشعارات', icon: Bell },
    { id: 'security', name: 'الأمان', icon: Shield }
  ]

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إعدادات النظام</h1>
          <p className="text-muted-foreground">إدارة إعدادات النظام والشركة</p>
        </div>
        <button
          onClick={handleSave}
          disabled={loading}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center disabled:opacity-50"
        >
          {loading ? (
            <RefreshCw className="w-5 h-5 ml-2 animate-spin" />
          ) : (
            <Save className="w-5 h-5 ml-2" />
          )}
          حفظ الإعدادات
        </button>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-border">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  }`}
                >
                  <Icon className="w-5 h-5 ml-2" />
                  {tab.name}
                </button>
              )
            })}
          </nav>
        </div>

        <div className="p-6">
          {/* Company Settings */}
          {activeTab === 'company' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-foreground">معلومات الشركة</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    اسم الشركة
                  </label>
                  <input
                    type="text"
                    value={settings.company.name}
                    onChange={(e) => handleInputChange('company', 'name', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    الاسم بالإنجليزية
                  </label>
                  <input
                    type="text"
                    value={settings.company.nameEn}
                    onChange={(e) => handleInputChange('company', 'nameEn', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    العنوان
                  </label>
                  <input
                    type="text"
                    value={settings.company.address}
                    onChange={(e) => handleInputChange('company', 'address', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    رقم الهاتف
                  </label>
                  <input
                    type="tel"
                    value={settings.company.phone}
                    onChange={(e) => handleInputChange('company', 'phone', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    البريد الإلكتروني
                  </label>
                  <input
                    type="email"
                    value={settings.company.email}
                    onChange={(e) => handleInputChange('company', 'email', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    الموقع الإلكتروني
                  </label>
                  <input
                    type="url"
                    value={settings.company.website}
                    onChange={(e) => handleInputChange('company', 'website', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    الرقم الضريبي
                  </label>
                  <input
                    type="text"
                    value={settings.company.taxNumber}
                    onChange={(e) => handleInputChange('company', 'taxNumber', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    السجل التجاري
                  </label>
                  <input
                    type="text"
                    value={settings.company.commercialRegister}
                    onChange={(e) => handleInputChange('company', 'commercialRegister', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          )}

          {/* System Settings */}
          {activeTab === 'system' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-foreground">إعدادات النظام</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    اللغة
                  </label>
                  <select
                    value={settings.system.language}
                    onChange={(e) => handleInputChange('system', 'language', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    المنطقة الزمنية
                  </label>
                  <select
                    value={settings.system.timezone}
                    onChange={(e) => handleInputChange('system', 'timezone', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="Africa/Cairo">القاهرة</option>
                    <option value="Asia/Riyadh">الرياض</option>
                    <option value="Asia/Dubai">دبي</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    تنسيق التاريخ
                  </label>
                  <select
                    value={settings.system.dateFormat}
                    onChange={(e) => handleInputChange('system', 'dateFormat', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    العملة
                  </label>
                  <select
                    value={settings.system.currency}
                    onChange={(e) => handleInputChange('system', 'currency', e.target.value)}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="EGP">الجنيه المصري</option>
                    <option value="USD">الدولار الأمريكي</option>
                    <option value="EUR">اليورو</option>
                    <option value="SAR">الريال السعودي</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Notifications Settings */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-foreground">إعدادات الإشعارات</h3>
              
              <div className="space-y-4">
                {Object.entries(settings.notifications).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">
                      {key === 'emailNotifications' && 'إشعارات البريد الإلكتروني'}
                      {key === 'smsNotifications' && 'إشعارات الرسائل النصية'}
                      {key === 'lowStockAlert' && 'تنبيهات نفاد المخزون'}
                      {key === 'expiryAlert' && 'تنبيهات انتهاء الصلاحية'}
                      {key === 'invoiceReminders' && 'تذكيرات الفواتير'}
                      {key === 'systemUpdates' && 'تحديثات النظام'}
                    </span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value}
                        onChange={(e) => handleInputChange('notifications', key, e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Security Settings */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-foreground">إعدادات الأمان</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    الحد الأدنى لطول كلمة المرور
                  </label>
                  <input
                    type="number"
                    min="6"
                    max="20"
                    value={settings.security.passwordMinLength}
                    onChange={(e) => handleInputChange('security', 'passwordMinLength', parseInt(e.target.value))}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    عدد محاولات تسجيل الدخول
                  </label>
                  <input
                    type="number"
                    min="3"
                    max="10"
                    value={settings.security.loginAttempts}
                    onChange={(e) => handleInputChange('security', 'loginAttempts', parseInt(e.target.value))}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    مدة قفل الحساب (دقيقة)
                  </label>
                  <input
                    type="number"
                    min="5"
                    max="60"
                    value={settings.security.accountLockout}
                    onChange={(e) => handleInputChange('security', 'accountLockout', parseInt(e.target.value))}
                    className="w-full p-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">تعقيد كلمة المرور</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.security.passwordComplexity}
                      onChange={(e) => handleInputChange('security', 'passwordComplexity', e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">المصادقة الثنائية</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.security.twoFactorAuth}
                      onChange={(e) => handleInputChange('security', 'twoFactorAuth', e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}
    </div>
  )
}

export default SystemSettingsAdvanced

