import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, Building, Save, Upload, MapPin, Phone, Mail, Globe
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const CompanySettings = () => {
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [companyData, setCompanyData] = useState({
    name: '',
    nameEn: '',
    address: '',
    addressEn: '',
    phone: '',
    mobile: '',
    email: '',
    website: '',
    taxNumber: '',
    commercialRegister: '',
    logo: null,
    currency: 'EGP',
    language: 'ar',
    timezone: 'Africa/Cairo',
    fiscalYearStart: '01-01',
    description: '',
    descriptionEn: ''
  })

  const [logoPreview, setLogoPreview] = useState(null)

  useEffect(() => {
    loadCompanySettings()
  }, [])

  const loadCompanySettings = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/settings/company')
      if (response.success) {
        setCompanyData(response.data)
        if (response.data.logo) {
          setLogoPreview(response.data.logo)
        }
      }
    } catch (error) {
      toast.error('خطأ في تحميل إعدادات الشركة')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setCompanyData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleLogoChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      if (file.size > 2 * 1024 * 1024) { // 2MB limit
        toast.error('حجم الملف يجب أن يكون أقل من 2 ميجابايت')
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        setLogoPreview(e.target.result)
        setCompanyData(prev => ({
          ...prev,
          logo: file
        }))
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      
      // Validate required fields
      if (!companyData.name.trim()) {
        toast.error('اسم الشركة مطلوب')
        return
      }

      const formData = new FormData()
      Object.keys(companyData).forEach(key => {
        if (companyData[key] !== null && companyData[key] !== '') {
          formData.append(key, companyData[key])
        }
      })

      const response = await ApiService.post('/api/settings/company', formData)
      if (response.success) {
        toast.success('تم حفظ إعدادات الشركة بنجاح')
        loadCompanySettings() // Reload to get updated data
      } else {
        throw new Error(response.message || 'فشل في حفظ الإعدادات')
      }
    } catch (error) {
      toast.error('خطأ في حفظ إعدادات الشركة')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center">
          <Building2 className="w-8 h-8 text-primary-600 ml-3" />
          <div>
            <h1 className="text-2xl font-bold text-foreground">إعدادات الشركة</h1>
            <p className="text-muted-foreground">إدارة معلومات وإعدادات الشركة الأساسية</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Logo Section */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-border p-6">
            <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center">
              <Camera className="w-5 h-5 ml-2" />
              شعار الشركة
            </h2>
            
            <div className="text-center">
              <div className="w-32 h-32 mx-auto mb-4 border-2 border-dashed border-border rounded-lg flex items-center justify-center bg-muted/50">
                {logoPreview ? (
                  <img 
                    src={logoPreview} 
                    alt="Company Logo" 
                    className="w-full h-full object-contain rounded-lg"
                  />
                ) : (
                  <Camera className="w-12 h-12 text-gray-400" />
                )}
              </div>
              
              <input
                type="file"
                accept="image/*"
                onChange={handleLogoChange}
                className="hidden"
                id="logo-upload"
              />
              <label
                htmlFor="logo-upload"
                className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50 cursor-pointer"
              >
                <Upload className="w-4 h-4 ml-2" />
                رفع شعار
              </label>
              <p className="text-xs text-gray-500 mt-2">
                PNG, JPG حتى 2MB
              </p>
            </div>
          </div>
        </div>

        {/* Company Information */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-border p-6">
            <h2 className="text-lg font-semibold text-foreground mb-6 flex items-center">
              <Settings className="w-5 h-5 ml-2" />
              معلومات الشركة
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Company Name Arabic */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  اسم الشركة (عربي) *
                </label>
                <input
                  type="text"
                  value={companyData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="اسم الشركة"
                  required
                />
              </div>

              {/* Company Name English */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  اسم الشركة (إنجليزي)
                </label>
                <input
                  type="text"
                  value={companyData.nameEn}
                  onChange={(e) => handleInputChange('nameEn', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Company Name"
                />
              </div>

              {/* Phone */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                  <Phone className="w-4 h-4 ml-1" />
                  الهاتف
                </label>
                <input
                  type="tel"
                  value={companyData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="رقم الهاتف"
                />
              </div>

              {/* Mobile */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                  <Phone className="w-4 h-4 ml-1" />
                  الجوال
                </label>
                <input
                  type="tel"
                  value={companyData.mobile}
                  onChange={(e) => handleInputChange('mobile', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="رقم الجوال"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                  <Mail className="w-4 h-4 ml-1" />
                  البريد الإلكتروني
                </label>
                <input
                  type="email"
                  value={companyData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="البريد الإلكتروني"
                />
              </div>

              {/* Website */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                  <Globe className="w-4 h-4 ml-1" />
                  الموقع الإلكتروني
                </label>
                <input
                  type="url"
                  value={companyData.website}
                  onChange={(e) => handleInputChange('website', e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="https://example.com"
                />
              </div>
            </div>

            {/* Address */}
            <div className="mt-6">
              <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                <MapPin className="w-4 h-4 ml-1" />
                العنوان (عربي)
              </label>
              <textarea
                value={companyData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="عنوان الشركة"
              />
            </div>

            <div className="mt-4">
              <label className="block text-sm font-medium text-foreground mb-2 flex items-center">
                <MapPin className="w-4 h-4 ml-1" />
                العنوان (إنجليزي)
              </label>
              <textarea
                value={companyData.addressEn}
                onChange={(e) => handleInputChange('addressEn', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Company Address"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Legal Information */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mt-6">
        <h2 className="text-lg font-semibold text-foreground mb-6 flex items-center">
          <FileText className="w-5 h-5 ml-2" />
          المعلومات القانونية
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              الرقم الضريبي
            </label>
            <input
              type="text"
              value={companyData.taxNumber}
              onChange={(e) => handleInputChange('taxNumber', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="الرقم الضريبي"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              السجل التجاري
            </label>
            <input
              type="text"
              value={companyData.commercialRegister}
              onChange={(e) => handleInputChange('commercialRegister', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="رقم السجل التجاري"
            />
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end mt-6">
        <button
          onClick={handleSave}
          disabled={saving}
          className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          {saving ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white ml-2"></div>
          ) : (
            <Save className="w-5 h-5 ml-2" />
          )}
          {saving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
        </button>
      </div>
    </div>
  )
}

export default CompanySettings

