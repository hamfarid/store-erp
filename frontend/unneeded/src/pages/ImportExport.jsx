import React, { useState, useRef } from 'react'
import { Download, Printer, Upload } from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const ImportExport = () => {
  const [activeTab, setActiveTab] = useState('export')
  const [isLoading, setIsLoading] = useState(false)
  const [importData, setImportData] = useState(null)
  const [importProgress, setImportProgress] = useState(0)
  const [exportProgress, setExportProgress] = useState(0)
  const fileInputRef = useRef(null)
  // بيانات التصدير
  const [exportData, setExportData] = useState({
    type: 'products',
    format: 'excel',
    filters: {
      dateFrom: '',
      dateTo: '',
      category: '',
      warehouse: ''
    },
    options: {
      includeImages: false,
      includeHistory: false,
      compressFile: false
    }
  })

  // أنواع البيانات المدعومة
  const dataTypes = [
    { value: 'products', label: 'المنتجات', icon: '📦' },
    { value: 'customers', label: 'العملاء', icon: '👥' },
    { value: 'suppliers', label: 'الموردين', icon: '🚚' },
    { value: 'invoices', label: 'الفواتير', icon: '💰' },
    { value: 'inventory', label: 'المخزون', icon: '📊' },
    { value: 'movements', label: 'حركات المخزون', icon: '🔄' }
  ]

  // تنسيقات التصدير
  const exportFormats = [
    { value: 'excel', label: 'Excel (.xlsx)', icon: '📊' },
    { value: 'csv', label: 'CSV (.csv)', icon: '📄' },
    { value: 'pdf', label: 'PDF (.pdf)', icon: '📋' },
    { value: 'json', label: 'JSON (.json)', icon: '🔧' }
  ]

  // معالجة رفع الملف
  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      // التحقق من نوع الملف
      const allowedTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'text/csv',
        'application/json'
      ]
      
      if (!allowedTypes.includes(file.type)) {
        toast.error('نوع الملف غير مدعوم. يرجى اختيار ملف Excel أو CSV أو JSON')
        return
      }

      setImportData(prev => ({ ...prev, file }))
      toast.success(`تم اختيار الملف: ${file.name}`)
    }
  }

  // تنفيذ الاستيراد
  const handleImport = async () => {
    if (!importData.file) {
      toast.error('يرجى اختيار ملف للاستيراد')
      return
    }

    setIsLoading(true)
    setImportProgress({ status: 'uploading', progress: 0 })

    try {
      const formData = new FormData()
      formData.append('file', importData.file)
      formData.append('type', importData.type)
      formData.append('options', JSON.stringify(importData.options))

      // محاكاة تقدم الرفع
      setImportProgress({ status: 'uploading', progress: 30 })
      
      const response = await ApiService.importData(formData)
      
      setImportProgress({ status: 'processing', progress: 60 })
      
      // انتظار معالجة البيانات
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      setImportProgress({ status: 'completed', progress: 100 })
      
      toast.success(`تم استيراد ${response.imported_count || 0} عنصر بنجاح`)
      
      // إعادة تعيين النموذج
      setImportData(prev => ({ ...prev, file: null }))
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      
    } catch (error) {
      setImportProgress({ status: 'error', progress: 0 })
      toast.error(error.message || 'خطأ في استيراد البيانات')
    } finally {
      setIsLoading(false)
      setTimeout(() => setImportProgress(null), 3000)
    }
  }

  // تنفيذ التصدير
  const handleExport = async () => {
    setIsLoading(true)
    setExportProgress({ status: 'preparing', progress: 0 })

    try {
      setExportProgress({ status: 'generating', progress: 30 })
      
      const response = await ApiService.exportData({
        type: exportData.type,
        format: exportData.format,
        filters: exportData.filters,
        options: exportData.options
      })
      
      setExportProgress({ status: 'downloading', progress: 70 })
      
      // تحميل الملف
      const blob = new Blob([response.data], { 
        type: response.headers['content-type'] 
      })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = response.filename || `export_${exportData.type}_${Date.now()}.${exportData.format}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      setExportProgress({ status: 'completed', progress: 100 })
      toast.success('تم تصدير البيانات بنجاح')
      
    } catch (error) {
      setExportProgress({ status: 'error', progress: 0 })
      toast.error(error.message || 'خطأ في تصدير البيانات')
    } finally {
      setIsLoading(false)
      setTimeout(() => setExportProgress(null), 3000)
    }
  }

  // طباعة التقارير
  const handlePrint = async (reportType) => {
    try {
      setIsLoading(true)
      const response = await ApiService.generateReport({
        type: reportType,
        format: 'pdf',
        action: 'print'
      })
      
      // فتح نافذة الطباعة
      const printWindow = window.open('', '_blank')
      printWindow.document.write(`
        <html>
          <head><title>طباعة التقرير</title></head>
          <body>
            <embed src="${response.url}" width="100%" height="100%" type="application/pdf">
          </body>
        </html>
      `)
      printWindow.document.close()
      printWindow.focus()
      printWindow.print()
      
      toast.success('تم إعداد التقرير للطباعة')
    } catch (error) {
      toast.error('خطأ في إعداد التقرير للطباعة')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* العنوان الرئيسي */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          📤 الاستيراد والتصدير
        </h1>
        <p className="text-muted-foreground">
          إدارة استيراد وتصدير البيانات والتقارير
        </p>
      </div>

      {/* التبويبات */}
      <div className="mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {[
              { id: 'import', name: 'الاستيراد', icon: Upload },
              { id: 'export', name: 'التصدير', icon: Download },
              { id: 'print', name: 'الطباعة', icon: Printer }
            ].map((tab) => {
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
        {/* تبويب الاستيراد */}
        {activeTab === 'import' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Upload className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">استيراد البيانات</h2>
            </div>

            {/* نوع البيانات */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                نوع البيانات
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {dataTypes.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setImportData(prev => ({ ...prev, type: type.value }))}
                    className={`p-3 border rounded-lg text-center transition-colors ${
                      importData.type === type.value
                        ? 'border-primary/100 bg-primary/10 text-primary/90'
                        : 'border-border hover:border-border'
                    }`}
                  >
                    <div className="text-2xl mb-1">{type.icon}</div>
                    <div className="text-sm font-medium">{type.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* رفع الملف */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اختيار الملف
              </label>
              <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleFileUpload}
                  accept=".xlsx,.xls,.csv,.json"
                  className="hidden"
                />
                <FileSpreadsheet className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-muted-foreground mb-2">
                  {importData.file ? importData.file.name : 'اسحب الملف هنا أو انقر للاختيار'}
                </p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90"
                >
                  اختيار ملف
                </button>
                <p className="text-xs text-gray-500 mt-2">
                  الملفات المدعومة: Excel (.xlsx), CSV (.csv), JSON (.json)
                </p>
              </div>
            </div>

            {/* خيارات الاستيراد */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                خيارات الاستيراد
              </label>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={importData.options.skipFirstRow}
                    onChange={(e) => setImportData(prev => ({
                      ...prev,
                      options: { ...prev.options, skipFirstRow: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-primary/100"
                  />
                  <span className="mr-2 text-sm text-foreground">تجاهل الصف الأول (العناوين)</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={importData.options.updateExisting}
                    onChange={(e) => setImportData(prev => ({
                      ...prev,
                      options: { ...prev.options, updateExisting: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-primary/100"
                  />
                  <span className="mr-2 text-sm text-foreground">تحديث البيانات الموجودة</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={importData.options.validateData}
                    onChange={(e) => setImportData(prev => ({
                      ...prev,
                      options: { ...prev.options, validateData: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-primary/100"
                  />
                  <span className="mr-2 text-sm text-foreground">التحقق من صحة البيانات</span>
                </label>
              </div>
            </div>

            {/* شريط التقدم للاستيراد */}
            {importProgress && (
              <div className="bg-muted/50 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-foreground">
                    {importProgress.status === 'uploading' && 'جاري رفع الملف...'}
                    {importProgress.status === 'processing' && 'جاري معالجة البيانات...'}
                    {importProgress.status === 'completed' && 'تم الاستيراد بنجاح!'}
                    {importProgress.status === 'error' && 'حدث خطأ في الاستيراد'}
                  </span>
                  <span className="text-sm text-gray-500">{importProgress.progress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      importProgress.status === 'error' ? 'bg-destructive/100' : 'bg-primary'
                    }`}
                    style={{ width: `${importProgress.progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* زر الاستيراد */}
            <button
              onClick={handleImport}
              disabled={!importData.file || isLoading}
              className="w-full bg-primary text-white py-3 px-4 rounded-lg hover:bg-primary/90 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <Upload className="w-4 h-4" />
              {isLoading ? 'جاري الاستيراد...' : 'بدء الاستيراد'}
            </button>
          </div>
        )}

        {/* تبويب التصدير */}
        {activeTab === 'export' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Download className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">تصدير البيانات</h2>
            </div>

            {/* نوع البيانات */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                نوع البيانات
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {dataTypes.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setExportData(prev => ({ ...prev, type: type.value }))}
                    className={`p-3 border rounded-lg text-center transition-colors ${
                      exportData.type === type.value
                        ? 'border-green-500 bg-primary/10 text-primary'
                        : 'border-border hover:border-border'
                    }`}
                  >
                    <div className="text-2xl mb-1">{type.icon}</div>
                    <div className="text-sm font-medium">{type.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* تنسيق التصدير */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                تنسيق الملف
              </label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {exportFormats.map((format) => (
                  <button
                    key={format.value}
                    onClick={() => setExportData(prev => ({ ...prev, format: format.value }))}
                    className={`p-3 border rounded-lg text-center transition-colors ${
                      exportData.format === format.value
                        ? 'border-green-500 bg-primary/10 text-primary'
                        : 'border-border hover:border-border'
                    }`}
                  >
                    <div className="text-2xl mb-1">{format.icon}</div>
                    <div className="text-sm font-medium">{format.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* فلاتر التصدير */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                فلاتر البيانات
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs text-muted-foreground mb-1">من تاريخ</label>
                  <input
                    type="date"
                    value={exportData.filters.dateFrom}
                    onChange={(e) => setExportData(prev => ({
                      ...prev,
                      filters: { ...prev.filters, dateFrom: e.target.value }
                    }))}
                    className="w-full border border-border rounded-lg px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs text-muted-foreground mb-1">إلى تاريخ</label>
                  <input
                    type="date"
                    value={exportData.filters.dateTo}
                    onChange={(e) => setExportData(prev => ({
                      ...prev,
                      filters: { ...prev.filters, dateTo: e.target.value }
                    }))}
                    className="w-full border border-border rounded-lg px-3 py-2 text-sm"
                  />
                </div>
              </div>
            </div>

            {/* خيارات التصدير */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                خيارات التصدير
              </label>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={exportData.options.includeImages}
                    onChange={(e) => setExportData(prev => ({
                      ...prev,
                      options: { ...prev.options, includeImages: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-green-500"
                  />
                  <span className="mr-2 text-sm text-foreground">تضمين الصور</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={exportData.options.includeHistory}
                    onChange={(e) => setExportData(prev => ({
                      ...prev,
                      options: { ...prev.options, includeHistory: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-green-500"
                  />
                  <span className="mr-2 text-sm text-foreground">تضمين السجل التاريخي</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={exportData.options.compressFile}
                    onChange={(e) => setExportData(prev => ({
                      ...prev,
                      options: { ...prev.options, compressFile: e.target.checked }
                    }))}
                    className="rounded border-border text-primary focus:ring-green-500"
                  />
                  <span className="mr-2 text-sm text-foreground">ضغط الملف (ZIP)</span>
                </label>
              </div>
            </div>

            {/* شريط التقدم للتصدير */}
            {exportProgress && (
              <div className="bg-muted/50 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-foreground">
                    {exportProgress.status === 'preparing' && 'جاري تحضير البيانات...'}
                    {exportProgress.status === 'generating' && 'جاري إنشاء الملف...'}
                    {exportProgress.status === 'downloading' && 'جاري تحميل الملف...'}
                    {exportProgress.status === 'completed' && 'تم التصدير بنجاح!'}
                    {exportProgress.status === 'error' && 'حدث خطأ في التصدير'}
                  </span>
                  <span className="text-sm text-gray-500">{exportProgress.progress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      exportProgress.status === 'error' ? 'bg-destructive/100' : 'bg-primary'
                    }`}
                    style={{ width: `${exportProgress.progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* زر التصدير */}
            <button
              onClick={handleExport}
              disabled={isLoading}
              className="w-full bg-primary text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <Download className="w-4 h-4" />
              {isLoading ? 'جاري التصدير...' : 'بدء التصدير'}
            </button>
          </div>
        )}

        {/* تبويب الطباعة */}
        {activeTab === 'print' && (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Printer className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">طباعة التقارير</h2>
            </div>

            {/* التقارير المتاحة */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { id: 'inventory_summary', name: 'ملخص المخزون', icon: '📊', description: 'تقرير شامل عن حالة المخزون' },
                { id: 'sales_report', name: 'تقرير المبيعات', icon: '💰', description: 'تقرير المبيعات والإيرادات' },
                { id: 'purchase_report', name: 'تقرير المشتريات', icon: '🛒', description: 'تقرير المشتريات والموردين' },
                { id: 'customer_list', name: 'قائمة العملاء', icon: '👥', description: 'قائمة شاملة بالعملاء' },
                { id: 'supplier_list', name: 'قائمة الموردين', icon: '🚚', description: 'قائمة شاملة بالموردين' },
                { id: 'financial_summary', name: 'الملخص المالي', icon: '📈', description: 'ملخص الوضع المالي' }
              ].map((report) => (
                <div key={report.id} className="border border-border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-2xl">{report.icon}</span>
                    <div>
                      <h3 className="font-medium text-foreground">{report.name}</h3>
                      <p className="text-sm text-muted-foreground">{report.description}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handlePrint(report.id)}
                    disabled={isLoading}
                    className="w-full bg-purple-600 text-white py-2 px-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
                  >
                    <Printer className="w-4 h-4" />
                    طباعة
                  </button>
                </div>
              ))}
            </div>

            {/* معلومات إضافية */}
            <div className="bg-primary/10 border border-primary/30 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <h3 className="font-medium text-primary mb-1">معلومات الطباعة</h3>
                  <ul className="text-sm text-primary/95 space-y-1">
                    <li>• سيتم فتح التقرير في نافذة جديدة للطباعة</li>
                    <li>• يمكنك حفظ التقرير كملف PDF من نافذة الطباعة</li>
                    <li>• تأكد من إعدادات الطابعة قبل الطباعة</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ImportExport

