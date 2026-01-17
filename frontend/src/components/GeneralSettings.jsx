import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Monitor, Database, Bell, Shield, Palette
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const GeneralSettings = () => {
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [settings, setSettings] = useState({
    // System Settings
    systemName: 'نظام إدارة المخزون',
    systemVersion: '1.0.0',
    language: 'ar',
    timezone: 'Africa/Cairo',
    dateFormat: 'DD/MM/YYYY',
    timeFormat: '24',
    
    // Currency Settings
    defaultCurrency: 'EGP',
    currencyPosition: 'after',
    decimalPlaces: 2,
    thousandSeparator: ',',
    decimalSeparator: '.',
    
    // Business Settings
    fiscalYearStart: '01-01',
    workingDays: ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday'],
    workingHoursStart: '08:00',
    workingHoursEnd: '17:00',
    
    // Notification Settings
    emailNotifications: true,
    smsNotifications: false,
    pushNotifications: true,
    lowStockAlert: true,
    lowStockThreshold: 10,
    
    // Security Settings
    sessionTimeout: 30,
    passwordMinLength: 8,
    requireSpecialChars: true,
    requireNumbers: true,
    maxLoginAttempts: 5,
    
    // UI Settings
    theme: 'light',
    sidebarCollapsed: false,
    showWelcomeMessage: true,
    itemsPerPage: 25,
    
    // Backup Settings
    autoBackup: true,
    backupFrequency: 'daily',
    backupRetention: 30
  })

  const [activeTab, setActiveTab] = useState('system')

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/settings/general')
      if (response.success) {
        setSettings(prev => ({ ...prev, ...response.data }))
      }
    } catch (error) {
      toast.error('خطأ في تحميل الإعدادات')
    } finally {
      setLoading(false)
    }
  }

  const handleSettingChange = (field, value) => {
    setSettings(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      const response = await ApiService.post('/api/settings/general', settings)
      if (response.success) {
        toast.success('تم حفظ الإعدادات بنجاح')
      } else {
        throw new Error(response.message || 'فشل في حفظ الإعدادات')
      }
    } catch (error) {
      toast.error('خطأ في حفظ الإعدادات')
    } finally {
      setSaving(false)
    }
  }

  const resetToDefaults = () => {
    if (window.confirm('هل أنت متأكد من إعادة تعيين جميع الإعدادات إلى القيم الافتراضية؟')) {
      setSettings({
        systemName: 'نظام إدارة المخزون',
        systemVersion: '1.0.0',
        language: 'ar',
        timezone: 'Africa/Cairo',
        dateFormat: 'DD/MM/YYYY',
        timeFormat: '24',
        defaultCurrency: 'EGP',
        currencyPosition: 'after',
        decimalPlaces: 2,
        thousandSeparator: ',',
        decimalSeparator: '.',
        fiscalYearStart: '01-01',
        workingDays: ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday'],
        workingHoursStart: '08:00',
        workingHoursEnd: '17:00',
        emailNotifications: true,
        smsNotifications: false,
        pushNotifications: true,
        lowStockAlert: true,
        lowStockThreshold: 10,
        sessionTimeout: 30,
        passwordMinLength: 8,
        requireSpecialChars: true,
        requireNumbers: true,
        maxLoginAttempts: 5,
        theme: 'light',
        sidebarCollapsed: false,
        showWelcomeMessage: true,
        itemsPerPage: 25,
        autoBackup: true,
        backupFrequency: 'daily',
        backupRetention: 30
      })
      toast.success('تم إعادة تعيين الإعدادات إلى القيم الافتراضية')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const tabs = [
    { id: 'system', name: 'النظام', icon: Monitor },
    { id: 'currency', name: 'العملة', icon: DollarSign },
    { id: 'business', name: 'الأعمال', icon: Database },
    { id: 'notifications', name: 'الإشعارات', icon: Bell },
    { id: 'security', name: 'الأمان', icon: Shield },
    { id: 'ui', name: 'الواجهة', icon: Palette }
  ]

  return (
    <div className="max-w-6xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Settings className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">الإعدادات العامة</h1>
              <p className="text-muted-foreground">إدارة إعدادات النظام والتفضيلات العامة</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={resetToDefaults}
              className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50"
            >
              <RefreshCw className="w-4 h-4 ml-2" />
              إعادة تعيين
            </button>
            
            <button
              onClick={handleSave}
              disabled={saving}
              className="inline-flex items-center px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
            >
              {saving ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white ml-2"></div>
              ) : (
                <Save className="w-4 h-4 ml-2" />
              )}
              {saving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
              >
                <tab.icon className="w-4 h-4 ml-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'system' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">إعدادات النظام</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    اسم النظام
                  </label>
                  <input
                    type="text"
                    value={settings.systemName}
                    onChange={(e) => handleSettingChange('systemName', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    إصدار النظام
                  </label>
                  <input
                    type="text"
                    value={settings.systemVersion}
                    onChange={(e) => handleSettingChange('systemVersion', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    اللغة الافتراضية
                  </label>
                  <select
                    value={settings.language}
                    onChange={(e) => handleSettingChange('language', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
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
                    value={settings.timezone}
                    onChange={(e) => handleSettingChange('timezone', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="Africa/Cairo">القاهرة (GMT+2)</option>
                    <option value="Asia/Riyadh">الرياض (GMT+3)</option>
                    <option value="Asia/Dubai">دبي (GMT+4)</option>
                    <option value="UTC">UTC (GMT+0)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    صيغة التاريخ
                  </label>
                  <select
                    value={settings.dateFormat}
                    onChange={(e) => handleSettingChange('dateFormat', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    صيغة الوقت
                  </label>
                  <select
                    value={settings.timeFormat}
                    onChange={(e) => handleSettingChange('timeFormat', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="24">24 ساعة</option>
                    <option value="12">12 ساعة</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'currency' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">إعدادات العملة</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    العملة الافتراضية
                  </label>
                  <select
                    value={settings.defaultCurrency}
                    onChange={(e) => handleSettingChange('defaultCurrency', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="EGP">جنيه مصري (EGP)</option>
                    <option value="EGP">ريال سعودي (EGP)</option>
                    <option value="AED">درهم إماراتي (AED)</option>
                    <option value="USD">دولار أمريكي (USD)</option>
                    <option value="EUR">يورو (EUR)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    موضع رمز العملة
                  </label>
                  <select
                    value={settings.currencyPosition}
                    onChange={(e) => handleSettingChange('currencyPosition', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="before">قبل المبلغ</option>
                    <option value="after">بعد المبلغ</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    عدد الخانات العشرية
                  </label>
                  <select
                    value={settings.decimalPlaces}
                    onChange={(e) => handleSettingChange('decimalPlaces', parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value={0}>0</option>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    فاصل الآلاف
                  </label>
                  <select
                    value={settings.thousandSeparator}
                    onChange={(e) => handleSettingChange('thousandSeparator', e.target.value)}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value=",">فاصلة (,)</option>
                    <option value=".">نقطة (.)</option>
                    <option value=" ">مسافة ( )</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default GeneralSettings

