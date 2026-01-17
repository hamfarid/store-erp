import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Link, Shield, Database
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import { settingsAPI } from '../services/api'

const AdvancedSettings = () => {
  const [activeTab, setActiveTab] = useState('inventory')
  const [settings, setSettings] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)

  const settingsTabs = [
    {
      id: 'inventory',
      name: 'إعدادات المخزون',
      icon: Package,
      description: 'إعدادات إدارة المخزون والمنتجات'
    },
    {
      id: 'integration',
      name: 'إعدادات التكامل',
      icon: Link,
      description: 'إعدادات التكامل مع الأنظمة الأخرى'
    },
    {
      id: 'quality',
      name: 'إعدادات الجودة',
      icon: BarChart3,
      description: 'معايير ومقاييس الجودة'
    },
    {
      id: 'system',
      name: 'إعدادات النظام',
      icon: Settings,
      description: 'الإعدادات العامة للنظام'
    },
    {
      id: 'security',
      name: 'إعدادات الأمان',
      icon: Shield,
      description: 'إعدادات الأمان والصلاحيات'
    },
    {
      id: 'reporting',
      name: 'إعدادات التقارير',
      icon: Database,
      description: 'إعدادات التقارير والتصدير'
    }
  ]

  // بيانات تجريبية للإعدادات
  const mockSettings = {
    inventory: {
      default_warehouse_id: 1,
      auto_create_lots: true,
      lot_number_format: 'LOT-{YYYY}{MM}{DD}-{###}',
      require_lot_for_expiry_products: true,
      default_shelf_life_days: 365,
      low_stock_threshold_percentage: 20,
      reorder_point_calculation: 'automatic',
      inventory_valuation_method: 'fifo',
      allow_negative_stock: false,
      auto_reserve_stock_on_sale: true,
      quality_control_required: true,
      temperature_tracking_enabled: true,
      humidity_tracking_enabled: true,
      barcode_generation_enabled: true,
      qr_code_generation_enabled: true,
      rfid_tracking_enabled: false
    },
    integration: {
      accounting_integration: {
        enabled: true,
        auto_create_journal_entries: true,
        inventory_account_code: '1001',
        cogs_account_code: '5001',
        sync_frequency: 'real_time'
      },
      sales_integration: {
        enabled: true,
        auto_create_stock_movements: true,
        auto_reserve_stock: true,
        allow_overselling: false
      },
      notifications: {
        low_stock_alerts: true,
        expiry_alerts: true,
        email_notifications: true,
        sms_notifications: false
      }
    },
    quality: {
      quality_grades: [
        { code: 'premium', name: 'ممتاز', min_score: 90 },
        { code: 'standard', name: 'عادي', min_score: 70 },
        { code: 'economy', name: 'اقتصادي', min_score: 50 }
      ],
      auto_quality_scoring: true,
      require_quality_certificates: true,
      quarantine_period_days: 7,
      expiry_warning_days: {
        seeds: 60,
        fertilizers: 90,
        pesticides: 30,
        default: 30
      }
    },
    system: {
      company_info: {
        name: 'شركة البذور المتقدمة',
        name_en: 'Advanced Seeds Company',
        address: 'القاهرة، مصر',
        phone: '+20123456789',
        email: 'info@advancedseeds.com'
      },
      localization: {
        default_language: 'ar',
        default_currency: 'EGP',
        timezone: 'Africa/Cairo',
        date_format: 'DD/MM/YYYY'
      }
    },
    security: {
      password_min_length: 8,
      password_require_uppercase: true,
      password_require_numbers: true,
      session_timeout_minutes: 120,
      max_login_attempts: 5,
      two_factor_auth_enabled: false
    },
    reporting: {
      default_formats: ['pdf', 'excel'],
      auto_generate_reports: {
        daily_stock_summary: true,
        weekly_low_stock_report: true,
        monthly_valuation_report: true
      },
      email_reports: {
        enabled: true,
        recipients: ['manager@company.com']
      }
    }
  }

  useEffect(() => {
    loadSettings()
  }, [loadSettings])

  const loadSettings = async () => {
    try {
      setLoading(true)
      // محاكاة تحميل الإعدادات
      setTimeout(() => {
        setSettings(mockSettings)
        setLoading(false)
      }, 1000)
    } catch (error) {
      setLoading(false)
    }
  }

  const handleSettingChange = (section, key, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }))
    setHasChanges(true)
  }

  const handleNestedSettingChange = (section, parentKey, key, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [parentKey]: {
          ...prev[section][parentKey],
          [key]: value
        }
      }
    }))
    setHasChanges(true)
  }

  const handleSaveSettings = async () => {
    try {
      setSaving(true)
      // محاكاة حفظ الإعدادات
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      toast.success('تم حفظ الإعدادات بنجاح')
      setHasChanges(false)
    } catch (error) {
      toast.error('خطأ في حفظ الإعدادات')
      } finally {
      setSaving(false)
    }
  }

  const handleResetSettings = async () => {
    if (window.confirm('هل أنت متأكد من إعادة تعيين الإعدادات للقيم الافتراضية؟')) {
      try {
        await loadSettings()
        toast.success('تم إعادة تعيين الإعدادات')
        setHasChanges(false)
      } catch {
        toast.error('خطأ في إعادة تعيين الإعدادات')
      }
    }
  }

  const handleExportSettings = async () => {
    try {
      const data = await settingsAPI.exportSettings()
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `settings_${new Date().toISOString().split('T')[0]}.json`
      link.click()
      toast.success('تم تصدير الإعدادات')
    } catch {
      toast.error('خطأ في تصدير الإعدادات')
    }
  }

  const handleImportSettings = async (event) => {
    const file = event.target.files[0]
    if (file) {
      try {
        await settingsAPI.importSettings(file)
        await loadSettings()
        toast.success('تم استيراد الإعدادات بنجاح')
      } catch {
        toast.error('خطأ في استيراد الإعدادات')
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="mr-3 text-muted-foreground">جاري تحميل الإعدادات...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">الإعدادات المتقدمة</h1>
          <p className="text-muted-foreground">إدارة شاملة لجميع إعدادات النظام</p>
        </div>
        <div className="flex gap-2">
          <input
            type="file"
            accept=".json"
            onChange={handleImportSettings}
            className="hidden"
            id="import-settings"
          />
          <label
            htmlFor="import-settings"
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 cursor-pointer flex items-center"
          >
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </label>
          <button
            onClick={handleExportSettings}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center"
          >
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </button>
          <button
            onClick={handleResetSettings}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center"
          >
            <RefreshCw className="w-4 h-4 ml-2" />
            إعادة تعيين
          </button>
          <button
            onClick={handleSaveSettings}
            disabled={!hasChanges || saving}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
          >
            <Save className={`w-4 h-4 ml-2 ${saving ? 'animate-spin' : ''}`} />
            {saving ? 'جاري الحفظ...' : 'حفظ التغييرات'}
          </button>
        </div>
      </div>

      {/* تنبيه التغييرات غير المحفوظة */}
      {hasChanges && (
        <div className="bg-accent/10 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-accent ml-2" />
            <span className="text-yellow-800">لديك تغييرات غير محفوظة. تأكد من حفظ التغييرات قبل المغادرة.</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* قائمة التبويبات */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b">
              <h3 className="font-medium text-foreground">أقسام الإعدادات</h3>
            </div>
            <nav className="space-y-1 p-2">
              {settingsTabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-right px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                  }`}
                >
                  <div className="flex items-center">
                    <tab.icon className="w-4 h-4 ml-2" />
                    <div className="text-right">
                      <div>{tab.name}</div>
                      <div className="text-xs opacity-75">{tab.description}</div>
                    </div>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* محتوى الإعدادات */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6">
              <div className="flex items-center mb-6">
                {(() => {
                  const currentTab = settingsTabs.find(tab => tab.id === activeTab);
                  const IconComponent = currentTab?.icon;
                  return IconComponent ? <IconComponent className="w-6 h-6 ml-2 text-primary-600" /> : null;
                })()}
                <h3 className="text-lg font-semibold">
                  {settingsTabs.find(tab => tab.id === activeTab)?.name}
                </h3>
              </div>

              {/* إعدادات المخزون */}
              {activeTab === 'inventory' && settings.inventory && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        المخزن الافتراضي
                      </label>
                      <select
                        value={settings.inventory.default_warehouse_id}
                        onChange={(e) => handleSettingChange('inventory', 'default_warehouse_id', parseInt(e.target.value))}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        <option value={1}>المخزن الرئيسي</option>
                        <option value={2}>مخزن الفرع الأول</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        نسبة المخزون المنخفض (%)
                      </label>
                      <input
                        type="number"
                        min="0"
                        max="100"
                        value={settings.inventory.low_stock_threshold_percentage}
                        onChange={(e) => handleSettingChange('inventory', 'low_stock_threshold_percentage', parseInt(e.target.value))}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        طريقة تقييم المخزون
                      </label>
                      <select
                        value={settings.inventory.inventory_valuation_method}
                        onChange={(e) => handleSettingChange('inventory', 'inventory_valuation_method', e.target.value)}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        <option value="fifo">FIFO - الوارد أولاً صادر أولاً</option>
                        <option value="lifo">LIFO - الوارد أخيراً صادر أولاً</option>
                        <option value="average">متوسط التكلفة</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        مدة الصلاحية الافتراضية (أيام)
                      </label>
                      <input
                        type="number"
                        min="1"
                        value={settings.inventory.default_shelf_life_days}
                        onChange={(e) => handleSettingChange('inventory', 'default_shelf_life_days', parseInt(e.target.value))}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground border-b pb-2">خيارات متقدمة</h4>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.inventory.auto_create_lots}
                          onChange={(e) => handleSettingChange('inventory', 'auto_create_lots', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">إنشاء اللوط تلقائياً</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.inventory.allow_negative_stock}
                          onChange={(e) => handleSettingChange('inventory', 'allow_negative_stock', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">السماح بالمخزون السالب</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.inventory.quality_control_required}
                          onChange={(e) => handleSettingChange('inventory', 'quality_control_required', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">مراقبة الجودة مطلوبة</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.inventory.temperature_tracking_enabled}
                          onChange={(e) => handleSettingChange('inventory', 'temperature_tracking_enabled', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">تتبع درجة الحرارة</span>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {/* إعدادات التكامل */}
              {activeTab === 'integration' && settings.integration && (
                <div className="space-y-6">
                  <div>
                    <h4 className="font-medium text-foreground border-b pb-2 mb-4">تكامل المحاسبة</h4>
                    <div className="space-y-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.integration.accounting_integration.enabled}
                          onChange={(e) => handleNestedSettingChange('integration', 'accounting_integration', 'enabled', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">تفعيل تكامل المحاسبة</span>
                      </label>

                      {settings.integration.accounting_integration.enabled && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mr-6">
                          <div>
                            <label className="block text-sm font-medium text-foreground mb-2">
                              كود حساب المخزون
                            </label>
                            <input
                              type="text"
                              value={settings.integration.accounting_integration.inventory_account_code}
                              onChange={(e) => handleNestedSettingChange('integration', 'accounting_integration', 'inventory_account_code', e.target.value)}
                              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-foreground mb-2">
                              كود حساب تكلفة البضاعة المباعة
                            </label>
                            <input
                              type="text"
                              value={settings.integration.accounting_integration.cogs_account_code}
                              onChange={(e) => handleNestedSettingChange('integration', 'accounting_integration', 'cogs_account_code', e.target.value)}
                              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium text-foreground border-b pb-2 mb-4">الإشعارات</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.integration.notifications.low_stock_alerts}
                          onChange={(e) => handleNestedSettingChange('integration', 'notifications', 'low_stock_alerts', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">تنبيهات المخزون المنخفض</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.integration.notifications.email_notifications}
                          onChange={(e) => handleNestedSettingChange('integration', 'notifications', 'email_notifications', e.target.checked)}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm text-foreground">إشعارات البريد الإلكتروني</span>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {/* باقي الإعدادات */}
              {activeTab !== 'inventory' && activeTab !== 'integration' && (
                <div className="text-center py-12">
                  <Settings className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-foreground mb-2">
                    {settingsTabs.find(tab => tab.id === activeTab)?.name}
                  </h3>
                  <p className="text-gray-500">هذا القسم قيد التطوير</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdvancedSettings

