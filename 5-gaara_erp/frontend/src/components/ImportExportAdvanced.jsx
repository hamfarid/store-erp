import React, { useState, useEffect } from 'react'
import {
  Plus,
  Search,
  Filter,
  Download,
  Edit,
  Trash2,
  Eye,
  Calendar,
  DollarSign,
  FileText,
  Settings,
  Users,
  Package,
  ShoppingCart,
  BarChart3,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  X,
  Menu,
  Upload,
  Database,
  AlertTriangle,
  RefreshCw,
  Archive,
  FileSpreadsheet
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const ImportExportAdvanced = () => {
  const [activeTab, setActiveTab] = useState('import')
  const [loading, setLoading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [importHistory, setImportHistory] = useState([])
  const [exportHistory, setExportHistory] = useState([])

  const [importSettings, setImportSettings] = useState({
    dataType: 'products',
    fileFormat: 'excel',
    validateData: true,
    skipDuplicates: true,
    updateExisting: false
  })

  const [exportSettings, setExportSettings] = useState({
    dataType: 'products',
    fileFormat: 'excel',
    includeImages: false,
    dateRange: 'all',
    startDate: '',
    endDate: ''
  })

  const dataTypes = [
    { value: 'products', label: 'المنتجات', icon: FileText },
    { value: 'customers', label: 'العملاء', icon: Database },
    { value: 'suppliers', label: 'الموردين', icon: Database },
    { value: 'invoices', label: 'الفواتير', icon: FileText },
    { value: 'inventory', label: 'المخزون', icon: Archive },
    { value: 'transactions', label: 'المعاملات', icon: Database }
  ]

  const fileFormats = [
    { value: 'excel', label: 'Excel (.xlsx)', icon: FileSpreadsheet },
    { value: 'csv', label: 'CSV (.csv)', icon: FileText },
    { value: 'json', label: 'JSON (.json)', icon: FileText }
  ]

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const [importResponse, exportResponse] = await Promise.all([
        ApiService.get('/api/import-export/history/import'),
        ApiService.get('/api/import-export/history/export')
      ])

      if (importResponse.success) {
        setImportHistory(importResponse.data)
      } else {
        // Mock data
        setImportHistory([
          {
            id: 1,
            type: 'products',
            filename: 'products_2024.xlsx',
            status: 'completed',
            recordsProcessed: 150,
            recordsSuccess: 145,
            recordsError: 5,
            createdAt: '2024-01-15T10:30:00Z'
          },
          {
            id: 2,
            type: 'customers',
            filename: 'customers.csv',
            status: 'failed',
            recordsProcessed: 50,
            recordsSuccess: 0,
            recordsError: 50,
            createdAt: '2024-01-14T14:20:00Z'
          }
        ])
      }

      if (exportResponse.success) {
        setExportHistory(exportResponse.data)
      } else {
        // Mock data
        setExportHistory([
          {
            id: 1,
            type: 'products',
            filename: 'products_export_2024.xlsx',
            status: 'completed',
            recordsCount: 200,
            fileSize: '2.5 MB',
            createdAt: '2024-01-15T16:45:00Z'
          }
        ])
      }
    } catch (error) {
      }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    const allowedTypes = {
      excel: ['.xlsx', '.xls'],
      csv: ['.csv'],
      json: ['.json']
    }

    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    if (!allowedTypes[importSettings.fileFormat].includes(fileExtension)) {
      toast.error(`نوع الملف غير مدعوم. يرجى اختيار ملف ${allowedTypes[importSettings.fileFormat].join(' أو ')}`)
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('حجم الملف يجب أن يكون أقل من 10 ميجابايت')
      return
    }

    try {
      setLoading(true)
      setUploadProgress(0)

      const formData = new FormData()
      formData.append('file', file)
      formData.append('dataType', importSettings.dataType)
      formData.append('fileFormat', importSettings.fileFormat)
      formData.append('validateData', importSettings.validateData)
      formData.append('skipDuplicates', importSettings.skipDuplicates)
      formData.append('updateExisting', importSettings.updateExisting)

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return prev
          }
          return prev + 10
        })
      }, 200)

      const response = await ApiService.post('/api/import-export/import', formData)

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (response.success) {
        toast.success('تم رفع الملف وبدء عملية الاستيراد بنجاح')
        loadHistory()
      } else {
        throw new Error(response.message || 'فشل في رفع الملف')
      }
    } catch (error) {
      toast.error('خطأ في رفع الملف')
    } finally {
      setLoading(false)
      setUploadProgress(0)
      // Reset file input
      event.target.value = ''
    }
  }

  const handleExport = async () => {
    try {
      setLoading(true)

      const params = {
        dataType: exportSettings.dataType,
        fileFormat: exportSettings.fileFormat,
        includeImages: exportSettings.includeImages,
        dateRange: exportSettings.dateRange
      }

      if (exportSettings.dateRange === 'custom') {
        params.startDate = exportSettings.startDate
        params.endDate = exportSettings.endDate
      }

      const response = await ApiService.get('/api/import-export/export', { params })

      if (response.success) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url

        const timestamp = new Date().toISOString().split('T')[0]
        const filename = `${exportSettings.dataType}_export_${timestamp}.${exportSettings.fileFormat === 'excel' ? 'xlsx' : exportSettings.fileFormat}`

        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        link.remove()

        toast.success('تم تصدير البيانات بنجاح')
        loadHistory()
      } else {
        throw new Error(response.message || 'فشل في تصدير البيانات')
      }
    } catch (error) {
      toast.error('خطأ في تصدير البيانات')
    } finally {
      setLoading(false)
    }
  }

  const downloadTemplate = async (dataType) => {
    try {
      const response = await ApiService.get(`/api/import-export/template/${dataType}`)

      if (response.success) {
        // Create download link for template
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${dataType}_template.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()

        toast.success('تم تحميل القالب بنجاح')
      }
    } catch (error) {
      toast.error('خطأ في تحميل القالب')
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-primary" />
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-destructive" />
      case 'processing':
        return <RefreshCw className="w-5 h-5 text-primary-600 animate-spin" />
      default:
        return <AlertCircle className="w-5 h-5 text-muted-foreground" />
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'مكتمل'
      case 'failed':
        return 'فشل'
      case 'processing':
        return 'قيد المعالجة'
      default:
        return 'غير معروف'
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center">
          <Archive className="w-8 h-8 text-primary-600 ml-3" />
          <div>
            <h1 className="text-2xl font-bold text-foreground">الاستيراد والتصدير</h1>
            <p className="text-muted-foreground">إدارة استيراد وتصدير البيانات من وإلى النظام</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'import', name: 'الاستيراد', icon: Upload },
              { id: 'export', name: 'التصدير', icon: Download },
              { id: 'history', name: 'السجل', icon: History }
            ].map((tab) => (
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
          {activeTab === 'import' && (
            <div className="space-y-6">
              {/* Import Settings */}
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
                  <Settings className="w-5 h-5 ml-2" />
                  إعدادات الاستيراد
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">
                      نوع البيانات
                    </label>
                    <select
                      value={importSettings.dataType}
                      onChange={(e) => setImportSettings(prev => ({ ...prev, dataType: e.target.value }))}
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      {dataTypes.map(type => (
                        <option key={type.value} value={type.value}>{type.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">
                      صيغة الملف
                    </label>
                    <select
                      value={importSettings.fileFormat}
                      onChange={(e) => setImportSettings(prev => ({ ...prev, fileFormat: e.target.value }))}
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      {fileFormats.map(format => (
                        <option key={format.value} value={format.value}>{format.label}</option>
                      ))}
                    </select>
                  </div>

                  <div className="flex items-center space-y-2">
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={importSettings.validateData}
                          onChange={(e) => setImportSettings(prev => ({ ...prev, validateData: e.target.checked }))}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm">التحقق من صحة البيانات</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={importSettings.skipDuplicates}
                          onChange={(e) => setImportSettings(prev => ({ ...prev, skipDuplicates: e.target.checked }))}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm">تخطي المكررات</span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={importSettings.updateExisting}
                          onChange={(e) => setImportSettings(prev => ({ ...prev, updateExisting: e.target.checked }))}
                          className="rounded border-border text-primary-600 focus:ring-primary-500"
                        />
                        <span className="mr-2 text-sm">تحديث الموجود</span>
                      </label>
                    </div>
                  </div>
                </div>

                {/* Template Download */}
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-primary-900">تحميل قالب البيانات</h4>
                      <p className="text-sm text-primary-700">قم بتحميل القالب المناسب لنوع البيانات المحدد</p>
                    </div>
                    <button
                      onClick={() => downloadTemplate(importSettings.dataType)}
                      className="inline-flex items-center px-4 py-2 border border-primary-300 rounded-md shadow-sm text-sm font-medium text-primary-700 bg-white hover:bg-primary-50"
                    >
                      <Download className="w-4 h-4 ml-2" />
                      تحميل القالب
                    </button>
                  </div>
                </div>
              </div>

              {/* File Upload */}
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4">رفع الملف</h3>

                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
                  <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <div className="space-y-2">
                    <p className="text-lg font-medium text-foreground">اختر ملف للاستيراد</p>
                    <p className="text-sm text-gray-500">
                      يدعم النظام ملفات Excel (.xlsx)، CSV (.csv)، JSON (.json)
                    </p>
                    <p className="text-xs text-gray-400">الحد الأقصى لحجم الملف: 10 ميجابايت</p>
                  </div>

                  <div className="mt-6">
                    <input
                      type="file"
                      onChange={handleFileUpload}
                      accept=".xlsx,.xls,.csv,.json"
                      className="hidden"
                      id="file-upload"
                      disabled={loading}
                    />
                    <label
                      htmlFor="file-upload"
                      className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 cursor-pointer ${
                        loading ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                    >
                      {loading ? (
                        <RefreshCw className="w-5 h-5 ml-2 animate-spin" />
                      ) : (
                        <Upload className="w-5 h-5 ml-2" />
                      )}
                      {loading ? 'جاري الرفع...' : 'اختيار ملف'}
                    </label>
                  </div>

                  {/* Upload Progress */}
                  {uploadProgress > 0 && (
                    <div className="mt-4">
                      <div className="bg-muted rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${uploadProgress}%` }}
                        ></div>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">{uploadProgress}% مكتمل</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'export' && (
            <div className="space-y-6">
              {/* Export Settings */}
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
                  <Settings className="w-5 h-5 ml-2" />
                  إعدادات التصدير
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">
                      نوع البيانات
                    </label>
                    <select
                      value={exportSettings.dataType}
                      onChange={(e) => setExportSettings(prev => ({ ...prev, dataType: e.target.value }))}
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      {dataTypes.map(type => (
                        <option key={type.value} value={type.value}>{type.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">
                      صيغة الملف
                    </label>
                    <select
                      value={exportSettings.fileFormat}
                      onChange={(e) => setExportSettings(prev => ({ ...prev, fileFormat: e.target.value }))}
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      {fileFormats.map(format => (
                        <option key={format.value} value={format.value}>{format.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">
                      نطاق التاريخ
                    </label>
                    <select
                      value={exportSettings.dateRange}
                      onChange={(e) => setExportSettings(prev => ({ ...prev, dateRange: e.target.value }))}
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="all">جميع البيانات</option>
                      <option value="today">اليوم</option>
                      <option value="week">هذا الأسبوع</option>
                      <option value="month">هذا الشهر</option>
                      <option value="year">هذا العام</option>
                      <option value="custom">نطاق مخصص</option>
                    </select>
                  </div>
                </div>

                {/* Custom Date Range */}
                {exportSettings.dateRange === 'custom' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        من تاريخ
                      </label>
                      <input
                        type="date"
                        value={exportSettings.startDate}
                        onChange={(e) => setExportSettings(prev => ({ ...prev, startDate: e.target.value }))}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">
                        إلى تاريخ
                      </label>
                      <input
                        type="date"
                        value={exportSettings.endDate}
                        onChange={(e) => setExportSettings(prev => ({ ...prev, endDate: e.target.value }))}
                        className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                  </div>
                )}

                {/* Additional Options */}
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={exportSettings.includeImages}
                      onChange={(e) => setExportSettings(prev => ({ ...prev, includeImages: e.target.checked }))}
                      className="rounded border-border text-primary-600 focus:ring-primary-500"
                    />
                    <span className="mr-2 text-sm">تضمين الصور (إن وجدت)</span>
                  </label>
                </div>
              </div>

              {/* Export Button */}
              <div className="bg-primary/10 border border-primary/30 rounded-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-green-900">تصدير البيانات</h4>
                    <p className="text-sm text-primary">
                      سيتم تصدير البيانات المحددة بالصيغة المختارة
                    </p>
                  </div>
                  <button
                    onClick={handleExport}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary hover:bg-green-700 disabled:opacity-50"
                  >
                    {loading ? (
                      <RefreshCw className="w-5 h-5 ml-2 animate-spin" />
                    ) : (
                      <Download className="w-5 h-5 ml-2" />
                    )}
                    {loading ? 'جاري التصدير...' : 'تصدير البيانات'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div className="space-y-6">
              {/* Import History */}
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4">سجل الاستيراد</h3>
                <div className="bg-white border border-border rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-muted/50">
                        <tr>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            الملف
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            النوع
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            الحالة
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            السجلات
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            التاريخ
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {importHistory.map((record) => (
                          <tr key={record.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                              {record.filename}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {dataTypes.find(t => t.value === record.type)?.label || record.type}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                {getStatusIcon(record.status)}
                                <span className="mr-2 text-sm">{getStatusText(record.status)}</span>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              <div>
                                <div className="text-primary">نجح: {record.recordsSuccess}</div>
                                {record.recordsError > 0 && (
                                  <div className="text-destructive">فشل: {record.recordsError}</div>
                                )}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(record.createdAt).toLocaleDateString('ar-EG')}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Export History */}
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4">سجل التصدير</h3>
                <div className="bg-white border border-border rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-muted/50">
                        <tr>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            الملف
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            النوع
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            الحالة
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            عدد السجلات
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            حجم الملف
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            التاريخ
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {exportHistory.map((record) => (
                          <tr key={record.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                              {record.filename}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {dataTypes.find(t => t.value === record.type)?.label || record.type}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                {getStatusIcon(record.status)}
                                <span className="mr-2 text-sm">{getStatusText(record.status)}</span>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {record.recordsCount}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {record.fileSize}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(record.createdAt).toLocaleDateString('ar-EG')}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ImportExportAdvanced
