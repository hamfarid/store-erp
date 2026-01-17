import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Building, Warehouse, Bell
} from 'lucide-react'
import DataTable from './ui/DataTable'
import DynamicForm from './ui/DynamicForm'
import { Notification, LoadingSpinner, Modal } from './ui/Notification'

const SystemSettings = () => {
  const [activeTab, setActiveTab] = useState('company')
  const [settings, setSettings] = useState({})
  const [warehouses, setWarehouses] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(null)

  const [error, setError] = useState(null)

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadData()
  }, [activeTab])

  const loadData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        loadSettings(),
        loadWarehouses()
      ])
    } catch (error) {
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadSettings = async () => {
    try {
      const response = await fetch('http://localhost:8000/settings/company')
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setSettings(data.data)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // الإعدادات التجريبية
      const mockSettings = {
        company: {
          name: 'شركة المخزون المتقدم',
          name_en: 'Advanced Inventory Company',
          address: 'شارع التحرير، القاهرة، مصر',
          phone: '02-12345678',
          mobile: '01234567890',
          email: 'info@inventory.com',
          website: 'www.inventory.com',
          tax_number: 'TAX123456789',
          commercial_register: 'CR987654321',
          logo: null,
          currency: 'EGP',
          language: 'ar',
          timezone: 'Africa/Cairo'
        },
        inventory: {
          auto_reorder: false,
          low_stock_alert: true,
          default_warehouse_id: 1,
          decimal_places: 2,
          barcode_generation: true,
          track_expiry_dates: true,
          allow_negative_stock: false,
          auto_lot_generation: true,
          require_lot_numbers: true
        },
        system: {
          backup_frequency: 'daily',
          session_timeout: 30,
          max_login_attempts: 5,
          password_policy: 'medium',
          two_factor_auth: false,
          audit_logging: true,
          email_notifications: true,
          sms_notifications: false
        },
        notifications: {
          low_stock_alerts: true,
          expiry_alerts: true,
          payment_reminders: true,
          system_updates: true,
          email_reports: false,
          daily_summary: true
        }
      }
      setSettings(mockSettings)
    }
  }

  // Removed unused loadCategories function

  const loadWarehouses = async () => {
    const mockWarehouses = [
      {
        id: 1,
        name: 'المخزن الرئيسي',
        code: 'MAIN-001',
        location: 'القاهرة، مصر',
        manager: 'أحمد محمد',
        capacity: 1000,
        current_usage: 750,
        is_active: true
      },
      {
        id: 2,
        name: 'مخزن الأسمدة',
        code: 'FERT-001',
        location: 'الجيزة، مصر',
        manager: 'فاطمة أحمد',
        capacity: 500,
        current_usage: 320,
        is_active: true
      },
      {
        id: 3,
        name: 'مخزن المبيدات',
        code: 'PEST-001',
        location: 'الإسكندرية، مصر',
        manager: 'محمد علي',
        capacity: 200,
        current_usage: 150,
        is_active: true
      }
    ]
    setWarehouses(mockWarehouses)
  }

  const loadMockData = () => {
    loadSettings()
    loadWarehouses()
  }

  // حفظ الإعدادات
  const handleSaveSettings = async (tabSettings) => {
    setSaving(true)
    try {
      const response = await fetch(`http://localhost:8000/settings/${activeTab}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(tabSettings)
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setSettings(prev => ({ ...prev, [activeTab]: tabSettings }))
          setSuccess('تم حفظ الإعدادات بنجاح')
          setTimeout(() => setSuccess(null), 3000)
        } else {
          throw new Error(data.message)
        }
      } else {
        throw new Error('فشل في حفظ الإعدادات')
      }
    } catch (error) {
      setSettings(prev => ({ ...prev, [activeTab]: tabSettings }))
      setSuccess('تم حفظ الإعدادات محلياً (وضع تجريبي)')
      setTimeout(() => setSuccess(null), 3000)
    } finally {
      setSaving(false)
    }
  }

  // مكون إعدادات الشركة
  const CompanySettings = () => {
    const [companyData, setCompanyData] = useState(settings.company || {})

    const handleSubmit = (e) => {
      e.preventDefault()
      handleSaveSettings(companyData)
    }

    return (
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              اسم الشركة (عربي)
            </label>
            <input
              type="text"
              value={companyData.name || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              اسم الشركة (إنجليزي)
            </label>
            <input
              type="text"
              value={companyData.name_en || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, name_en: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-foreground mb-2">
              العنوان
            </label>
            <textarea
              value={companyData.address || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, address: e.target.value }))}
              rows={3}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              الهاتف الثابت
            </label>
            <input
              type="text"
              value={companyData.phone || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, phone: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              الهاتف المحمول
            </label>
            <input
              type="text"
              value={companyData.mobile || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, mobile: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              البريد الإلكتروني
            </label>
            <input
              type="email"
              value={companyData.email || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, email: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              الموقع الإلكتروني
            </label>
            <input
              type="url"
              value={companyData.website || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, website: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              الرقم الضريبي
            </label>
            <input
              type="text"
              value={companyData.tax_number || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, tax_number: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              السجل التجاري
            </label>
            <input
              type="text"
              value={companyData.commercial_register || ''}
              onChange={(e) => setCompanyData(prev => ({ ...prev, commercial_register: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              العملة الافتراضية
            </label>
            <select
              value={companyData.currency || 'EGP'}
              onChange={(e) => setCompanyData(prev => ({ ...prev, currency: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="EGP">الجنيه المصري (EGP)</option>
              <option value="USD">الدولار الأمريكي (USD)</option>
              <option value="EUR">اليورو (EUR)</option>
              <option value="EGP">جنيه مصري (EGP)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              اللغة الافتراضية
            </label>
            <select
              value={companyData.language || 'ar'}
              onChange={(e) => setCompanyData(prev => ({ ...prev, language: e.target.value }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="ar">العربية</option>
              <option value="en">English</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
          >
            {saving ? (
              <RefreshCw className="w-4 h-4 ml-1 animate-spin" />
            ) : (
              <Save className="w-4 h-4 ml-1" />
            )}
            {saving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
          </button>
        </div>
      </form>
    )
  }

  // مكون إعدادات المخزون
  const InventorySettings = () => {
    const [inventoryData, setInventoryData] = useState(settings.inventory || {})

    const handleSubmit = (e) => {
      e.preventDefault()
      handleSaveSettings(inventoryData)
    }

    return (
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">إعدادات عامة</h3>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">إعادة الطلب التلقائي</label>
                <p className="text-sm text-muted-foreground">طلب المنتجات تلقائياً عند نفاد المخزون</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.auto_reorder || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, auto_reorder: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">تنبيهات المخزون المنخفض</label>
                <p className="text-sm text-muted-foreground">إرسال تنبيهات عند انخفاض المخزون</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.low_stock_alert || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, low_stock_alert: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">السماح بالمخزون السالب</label>
                <p className="text-sm text-muted-foreground">السماح ببيع أكثر من المخزون المتاح</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.allow_negative_stock || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, allow_negative_stock: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">إعدادات اللوطات</h3>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">تتبع تواريخ الانتهاء</label>
                <p className="text-sm text-muted-foreground">تتبع تواريخ انتهاء صلاحية المنتجات</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.track_expiry_dates || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, track_expiry_dates: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">إنشاء اللوطات تلقائياً</label>
                <p className="text-sm text-muted-foreground">إنشاء أرقام لوتات تلقائياً للمنتجات الجديدة</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.auto_lot_generation || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, auto_lot_generation: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>

            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <label className="font-medium text-foreground">إلزامية أرقام اللوطات</label>
                <p className="text-sm text-muted-foreground">جعل أرقام اللوطات إلزامية لجميع المنتجات</p>
              </div>
              <input
                type="checkbox"
                checked={inventoryData.require_lot_numbers || false}
                onChange={(e) => setInventoryData(prev => ({ ...prev, require_lot_numbers: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              المخزن الافتراضي
            </label>
            <select
              value={inventoryData.default_warehouse_id || ''}
              onChange={(e) => setInventoryData(prev => ({ ...prev, default_warehouse_id: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">اختر المخزن الافتراضي</option>
              {warehouses.map(warehouse => (
                <option key={warehouse.id} value={warehouse.id}>
                  {warehouse.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              عدد المنازل العشرية
            </label>
            <select
              value={inventoryData.decimal_places || 2}
              onChange={(e) => setInventoryData(prev => ({ ...prev, decimal_places: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value={0}>0 منازل</option>
              <option value={1}>1 منزلة</option>
              <option value={2}>2 منزلة</option>
              <option value={3}>3 منازل</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
          >
            {saving ? (
              <RefreshCw className="w-4 h-4 ml-1 animate-spin" />
            ) : (
              <Save className="w-4 h-4 ml-1" />
            )}
            {saving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
          </button>
        </div>
      </form>
    )
  }

  // التبويبات
  const tabs = [
    { id: 'company', label: 'معلومات الشركة', icon: Building },
    { id: 'inventory', label: 'إعدادات المخزون', icon: Package },
    { id: 'categories', label: 'إدارة الفئات', icon: Package },
    { id: 'warehouses', label: 'إدارة المخازن', icon: Warehouse },
    { id: 'system', label: 'إعدادات النظام', icon: Settings },
    { id: 'notifications', label: 'التنبيهات', icon: Bell }
  ]

  if (loading) {
    return <LoadingSpinner size="lg" text="جاري تحميل إعدادات النظام..." />
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground flex items-center">
              <Settings className="w-6 h-6 ml-2 text-primary-600" />
              إعدادات النظام الشاملة
            </h1>
            <p className="text-muted-foreground mt-1">إدارة جميع إعدادات النظام والشركة</p>
          </div>

          <div className="flex items-center space-x-3 space-x-reverse">
            <button
              onClick={loadData}
              className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4 ml-1" />
              تحديث
            </button>

            <button
              onClick={() => handleExportSettings()}
              className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4 ml-1" />
              تصدير
            </button>
          </div>
        </div>
      </div>

      {/* Success/Error Messages */}
      {success && (
        <Notification
          type="success"
          title="نجح الحفظ"
          message={success}
          className="mb-6"
          onDismiss={() => setSuccess(null)}
        />
      )}

      {error && (
        <Notification
          type="error"
          title="خطأ في تحميل البيانات"
          message={error}
          className="mb-6"
          onDismiss={() => setError(null)}
        />
      )}

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse overflow-x-auto">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  }`}
                >
                  <Icon className="w-4 h-4 ml-1" />
                  {tab.label}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6">
        {activeTab === 'company' && <CompanySettings />}
        {activeTab === 'inventory' && <InventorySettings />}
        {activeTab === 'categories' && <div>إدارة الفئات قريباً...</div>}
        {activeTab === 'warehouses' && <div>إدارة المخازن قريباً...</div>}
        {activeTab === 'system' && <div>إعدادات النظام قريباً...</div>}
        {activeTab === 'notifications' && <div>إعدادات التنبيهات قريباً...</div>}
      </div>
    </div>
  )
}

export default SystemSettings

