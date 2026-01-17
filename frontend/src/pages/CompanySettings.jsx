import React, { useState, useEffect } from 'react'
import { Building2, Settings, Package, CreditCard } from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const CompanySettings = () => {
  const [activeTab, setActiveTab] = useState('company')
  const [isLoading, setIsLoading] = useState(false)
  const [companyData, setCompanyData] = useState({
    nameAr: '',
    nameEn: '',
    description: '',
    phone: '',
    mobile: '',
    email: '',
    website: '',
    address: '',
    city: '',
    country: '',
    postalCode: '',
    taxNumber: '',
    commercialRegister: '',
    logo: null
  })

  // إعدادات النظام
  const [systemSettings, setSystemSettings] = useState({
    defaultCurrency: 'EGP',
    defaultLanguage: 'ar',
    dateFormat: 'DD/MM/YYYY',
    timeFormat: '24h',
    timezone: 'Africa/Cairo',
    fiscalYearStart: '01/01',
    lowStockThreshold: 10,
    autoBackup: true,
    backupFrequency: 'daily',
    emailNotifications: true,
    smsNotifications: false
  })

  // إعدادات المخزون
  const [inventorySettings, setInventorySettings] = useState({
    allowNegativeStock: false,
    autoCalculateCost: true,
    costMethod: 'FIFO', // FIFO, LIFO, Average
    trackSerialNumbers: false,
    trackExpiryDates: true,
    defaultWarehouse: '',
    autoReorderPoint: true,
    reorderQuantity: 50,
    enableBarcodes: true,
    printLabelsOnReceive: false
  })

  // إعدادات المالية
  const [financialSettings, setFinancialSettings] = useState({
    defaultPaymentTerms: 30,
    lateFeePercentage: 2,
    discountPercentage: 0,
    taxRate: 14, // ضريبة القيمة المضافة في مصر
    enableMultiCurrency: true,
    autoExchangeRates: false,
    roundingMethod: 'nearest', // up, down, nearest
    decimalPlaces: 2,
    invoicePrefix: 'INV',
    receiptPrefix: 'REC',
    creditNotePrefix: 'CN'
  })

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setIsLoading(true)
      const response = await ApiService.getCompanySettings()

      if (response.company) setCompanyData(response.company)
      if (response.system) setSystemSettings(response.system)
      if (response.inventory) setInventorySettings(response.inventory)
      if (response.financial) setFinancialSettings(response.financial)

    } catch (error) {
      toast.error('خطأ في تحميل الإعدادات')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setIsLoading(true)

      const settingsData = {
        company: companyData,
        system: systemSettings,
        inventory: inventorySettings,
        financial: financialSettings
      }

      await ApiService.updateCompanySettings(settingsData)
      toast.success('تم حفظ الإعدادات بنجاح')

    } catch (error) {
      toast.error('خطأ في حفظ الإعدادات')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogoUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (file.size > 2 * 1024 * 1024) { // 2MB
        toast.error('حجم الملف كبير جداً. الحد الأقصى 2 ميجابايت')
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        setCompanyData(prev => ({ ...prev, logo: e.target.result }))
      }
      reader.readAsDataURL(file)
    }
  }

  const tabs = [
    { id: 'company', name: 'بيانات الشركة', icon: Building2 },
    { id: 'system', name: 'إعدادات النظام', icon: Settings },
    { id: 'inventory', name: 'إعدادات المخزون', icon: Package },
    { id: 'financial', name: 'الإعدادات المالية', icon: CreditCard }
  ]

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* العنوان الرئيسي */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          🏢 إعدادات الشركة
        </h1>
        <p className="text-muted-foreground">
          إدارة بيانات الشركة وإعدادات النظام
        </p>
      </div>

      {/* التبويبات */}
      <div className="mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`${
                    activeTab === tab.id
                      ? 'border-primary/100 text-primary'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  } whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.name}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* محتوى التبويبات */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        {/* تبويب بيانات الشركة */}
        {activeTab === 'company' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Building2 className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">بيانات الشركة</h2>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* شعار الشركة */}
              <div className="lg:col-span-1">
                <label className="block text-sm font-medium text-foreground mb-2">
                  شعار الشركة
                </label>
                <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                  {companyData.logo ? (
                    <div className="space-y-3">
                      <img
                        src={companyData.logo}
                        alt="شعار الشركة"
                        className="w-24 h-24 object-contain mx-auto"
                      />
                      <button
                        onClick={() => setCompanyData(prev => ({ ...prev, logo: null }))}
                        className="text-destructive text-sm hover:text-destructive"
                      >
                        حذف الشعار
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <ImageIcon className="w-12 h-12 text-gray-400 mx-auto" />
                      <p className="text-muted-foreground">رفع شعار الشركة</p>
                    </div>
                  )}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleLogoUpload}
                    className="hidden"
                    id="logo-upload"
                  />
                  <label
                    htmlFor="logo-upload"
                    className="mt-3 inline-block bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 cursor-pointer"
                  >
                    <Upload className="w-4 h-4 inline mr-2" />
                    اختيار ملف
                  </label>
                  <p className="text-xs text-gray-500 mt-2">
                    PNG, JPG, GIF حتى 2MB
                  </p>
                </div>
              </div>

              {/* بيانات الشركة */}
              <div className="lg:col-span-2 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      اسم الشركة (عربي) *
                    </label>
                    <input
                      type="text"
                      value={companyData.name}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, name: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="اسم الشركة"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      اسم الشركة (إنجليزي)
                    </label>
                    <input
                      type="text"
                      value={companyData.nameEn}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, nameEn: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="Company Name"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    وصف الشركة
                  </label>
                  <textarea
                    value={companyData.description}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, description: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    rows="3"
                    placeholder="وصف مختصر عن الشركة ونشاطها"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      <Phone className="w-4 h-4 inline mr-1" />
                      الهاتف
                    </label>
                    <input
                      type="tel"
                      value={companyData.phone}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, phone: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="+20 2 1234567"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      📱 الموبايل
                    </label>
                    <input
                      type="tel"
                      value={companyData.mobile}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, mobile: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="+20 10 12345678"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      <Mail className="w-4 h-4 inline mr-1" />
                      البريد الإلكتروني
                    </label>
                    <input
                      type="email"
                      value={companyData.email}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, email: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="info@company.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      <Globe className="w-4 h-4 inline mr-1" />
                      الموقع الإلكتروني
                    </label>
                    <input
                      type="url"
                      value={companyData.website}
                      onChange={(e) => setCompanyData(prev => ({ ...prev, website: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2"
                      placeholder="https://www.company.com"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* العنوان */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-medium text-foreground mb-4 flex items-center gap-2">
                <MapPin className="w-5 h-5" />
                العنوان
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-foreground mb-1">
                    العنوان التفصيلي
                  </label>
                  <input
                    type="text"
                    value={companyData.address}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, address: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    placeholder="الشارع والحي والمنطقة"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    المدينة
                  </label>
                  <input
                    type="text"
                    value={companyData.city}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, city: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    placeholder="القاهرة"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    الرمز البريدي
                  </label>
                  <input
                    type="text"
                    value={companyData.postalCode}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, postalCode: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    placeholder="12345"
                  />
                </div>
              </div>
            </div>

            {/* البيانات القانونية */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-medium text-foreground mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                البيانات القانونية
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    الرقم الضريبي
                  </label>
                  <input
                    type="text"
                    value={companyData.taxNumber}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, taxNumber: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    placeholder="123-456-789"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    السجل التجاري
                  </label>
                  <input
                    type="text"
                    value={companyData.commercialRegister}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, commercialRegister: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    placeholder="987654321"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    تاريخ التأسيس
                  </label>
                  <input
                    type="date"
                    value={companyData.establishedDate}
                    onChange={(e) => setCompanyData(prev => ({ ...prev, establishedDate: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* تبويب إعدادات النظام */}
        {activeTab === 'system' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Settings className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">إعدادات النظام</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* الإعدادات العامة */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">الإعدادات العامة</h3>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    العملة الافتراضية
                  </label>
                  <select
                    value={systemSettings.defaultCurrency}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, defaultCurrency: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="EGP">جنيه مصري (EGP)</option>
                    <option value="USD">دولار أمريكي (USD)</option>
                    <option value="EUR">يورو (EUR)</option>
                    <option value="EGP">ريال سعودي (EGP)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    اللغة الافتراضية
                  </label>
                  <select
                    value={systemSettings.defaultLanguage}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, defaultLanguage: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    تنسيق التاريخ
                  </label>
                  <select
                    value={systemSettings.dateFormat}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, dateFormat: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    المنطقة الزمنية
                  </label>
                  <select
                    value={systemSettings.timezone}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, timezone: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="Africa/Cairo">القاهرة (GMT+2)</option>
                    <option value="Asia/Riyadh">الرياض (GMT+3)</option>
                    <option value="Asia/Dubai">دبي (GMT+4)</option>
                  </select>
                </div>
              </div>

              {/* إعدادات النسخ الاحتياطي والإشعارات */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">النسخ الاحتياطي والإشعارات</h3>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    حد المخزون المنخفض
                  </label>
                  <input
                    type="number"
                    value={systemSettings.lowStockThreshold}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, lowStockThreshold: parseInt(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="1"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    تكرار النسخ الاحتياطي
                  </label>
                  <select
                    value={systemSettings.backupFrequency}
                    onChange={(e) => setSystemSettings(prev => ({ ...prev, backupFrequency: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="daily">يومي</option>
                    <option value="weekly">أسبوعي</option>
                    <option value="monthly">شهري</option>
                  </select>
                </div>

                <div className="space-y-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={systemSettings.autoBackup}
                      onChange={(e) => setSystemSettings(prev => ({ ...prev, autoBackup: e.target.checked }))}
                      className="rounded border-border text-primary focus:ring-green-500"
                    />
                    <span className="mr-2 text-sm text-foreground">تفعيل النسخ الاحتياطي التلقائي</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={systemSettings.emailNotifications}
                      onChange={(e) => setSystemSettings(prev => ({ ...prev, emailNotifications: e.target.checked }))}
                      className="rounded border-border text-primary focus:ring-green-500"
                    />
                    <span className="mr-2 text-sm text-foreground">إشعارات البريد الإلكتروني</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={systemSettings.smsNotifications}
                      onChange={(e) => setSystemSettings(prev => ({ ...prev, smsNotifications: e.target.checked }))}
                      className="rounded border-border text-primary focus:ring-green-500"
                    />
                    <span className="mr-2 text-sm text-foreground">إشعارات الرسائل النصية</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* تبويب إعدادات المخزون */}
        {activeTab === 'inventory' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Package className="w-5 h-5 text-accent" />
              <h2 className="text-xl font-semibold">إعدادات المخزون</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* إعدادات التكلفة والتقييم */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">التكلفة والتقييم</h3>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    طريقة حساب التكلفة
                  </label>
                  <select
                    value={inventorySettings.costMethod}
                    onChange={(e) => setInventorySettings(prev => ({ ...prev, costMethod: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="FIFO">الوارد أولاً صادر أولاً (FIFO)</option>
                    <option value="LIFO">الوارد أخيراً صادر أولاً (LIFO)</option>
                    <option value="Average">المتوسط المرجح</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    كمية إعادة الطلب
                  </label>
                  <input
                    type="number"
                    value={inventorySettings.reorderQuantity}
                    onChange={(e) => setInventorySettings(prev => ({ ...prev, reorderQuantity: parseInt(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="1"
                  />
                </div>

                <div className="space-y-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.allowNegativeStock}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, allowNegativeStock: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">السماح بالمخزون السالب</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.autoCalculateCost}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, autoCalculateCost: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">حساب التكلفة تلقائياً</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.autoReorderPoint}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, autoReorderPoint: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">نقطة إعادة الطلب التلقائية</span>
                  </label>
                </div>
              </div>

              {/* إعدادات التتبع والباركود */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">التتبع والباركود</h3>

                <div className="space-y-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.trackSerialNumbers}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, trackSerialNumbers: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">تتبع الأرقام التسلسلية</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.trackExpiryDates}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, trackExpiryDates: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">تتبع تواريخ الانتهاء</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.enableBarcodes}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, enableBarcodes: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">تفعيل الباركود</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={inventorySettings.printLabelsOnReceive}
                      onChange={(e) => setInventorySettings(prev => ({ ...prev, printLabelsOnReceive: e.target.checked }))}
                      className="rounded border-border text-accent focus:ring-orange-500"
                    />
                    <span className="mr-2 text-sm text-foreground">طباعة الملصقات عند الاستلام</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* تبويب الإعدادات المالية */}
        {activeTab === 'financial' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <CreditCard className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">الإعدادات المالية</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* إعدادات الدفع والضرائب */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">الدفع والضرائب</h3>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    شروط الدفع الافتراضية (أيام)
                  </label>
                  <input
                    type="number"
                    value={financialSettings.defaultPaymentTerms}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, defaultPaymentTerms: parseInt(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    معدل الضريبة (%)
                  </label>
                  <input
                    type="number"
                    value={financialSettings.taxRate}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, taxRate: parseFloat(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="0"
                    max="100"
                    step="0.1"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    رسوم التأخير (%)
                  </label>
                  <input
                    type="number"
                    value={financialSettings.lateFeePercentage}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, lateFeePercentage: parseFloat(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="0"
                    max="100"
                    step="0.1"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    خصم افتراضي (%)
                  </label>
                  <input
                    type="number"
                    value={financialSettings.discountPercentage}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, discountPercentage: parseFloat(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                    min="0"
                    max="100"
                    step="0.1"
                  />
                </div>
              </div>

              {/* إعدادات العملة والترقيم */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-foreground">العملة والترقيم</h3>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    طريقة التقريب
                  </label>
                  <select
                    value={financialSettings.roundingMethod}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, roundingMethod: e.target.value }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="nearest">الأقرب</option>
                    <option value="up">للأعلى</option>
                    <option value="down">للأسفل</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    عدد المنازل العشرية
                  </label>
                  <select
                    value={financialSettings.decimalPlaces}
                    onChange={(e) => setFinancialSettings(prev => ({ ...prev, decimalPlaces: parseInt(e.target.value) }))}
                    className="w-full border border-border rounded-lg px-3 py-2"
                  >
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                  </select>
                </div>

                <div className="space-y-3">
                  <h4 className="text-sm font-medium text-foreground">بادئات المستندات</h4>

                  <div>
                    <label className="block text-xs text-muted-foreground mb-1">بادئة الفواتير</label>
                    <input
                      type="text"
                      value={financialSettings.invoicePrefix}
                      onChange={(e) => setFinancialSettings(prev => ({ ...prev, invoicePrefix: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2 text-sm"
                      placeholder="INV"
                    />
                  </div>

                  <div>
                    <label className="block text-xs text-muted-foreground mb-1">بادئة الإيصالات</label>
                    <input
                      type="text"
                      value={financialSettings.receiptPrefix}
                      onChange={(e) => setFinancialSettings(prev => ({ ...prev, receiptPrefix: e.target.value }))}
                      className="w-full border border-border rounded-lg px-3 py-2 text-sm"
                      placeholder="REC"
                    />
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={financialSettings.enableMultiCurrency}
                      onChange={(e) => setFinancialSettings(prev => ({ ...prev, enableMultiCurrency: e.target.checked }))}
                      className="rounded border-border text-purple-600 focus:ring-purple-500"
                    />
                    <span className="mr-2 text-sm text-foreground">تفعيل العملات المتعددة</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={financialSettings.autoExchangeRates}
                      onChange={(e) => setFinancialSettings(prev => ({ ...prev, autoExchangeRates: e.target.checked }))}
                      className="rounded border-border text-purple-600 focus:ring-purple-500"
                    />
                    <span className="mr-2 text-sm text-foreground">أسعار الصرف التلقائية</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* زر الحفظ */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={handleSave}
          disabled={isLoading}
          className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          {isLoading ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
        </button>
      </div>
    </div>
  )
}

export default CompanySettings
