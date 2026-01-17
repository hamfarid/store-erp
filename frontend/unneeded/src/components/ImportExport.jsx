import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, Upload, Database, AlertTriangle, RefreshCw
} from 'lucide-react'

const ImportExport = () => {
  const [activeTab, setActiveTab] = useState('import')
  const [importHistory, setImportHistory] = useState([])
  const [exportHistory, setExportHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = () => {
    // بيانات تجريبية لسجل الاستيراد والتصدير
    const mockImportHistory = [
      {
        id: 1,
        fileName: 'products_import_2024_07_04.xlsx',
        type: 'منتجات',
        date: '2024-07-04 10:30',
        status: 'مكتمل',
        recordsProcessed: 156,
        recordsSuccess: 150,
        recordsError: 6,
        user: 'أحمد محمد'
      },
      {
        id: 2,
        fileName: 'customers_import_2024_07_03.xlsx',
        type: 'عملاء',
        date: '2024-07-03 14:15',
        status: 'مكتمل',
        recordsProcessed: 89,
        recordsSuccess: 89,
        recordsError: 0,
        user: 'سارة علي'
      },
      {
        id: 3,
        fileName: 'suppliers_import_2024_07_02.xlsx',
        type: 'موردين',
        date: '2024-07-02 09:45',
        status: 'فشل',
        recordsProcessed: 45,
        recordsSuccess: 0,
        recordsError: 45,
        user: 'محمد حسن'
      }
    ]

    const mockExportHistory = [
      {
        id: 1,
        fileName: 'inventory_report_2024_07_04.xlsx',
        type: 'تقرير المخزون',
        date: '2024-07-04 11:00',
        status: 'مكتمل',
        recordsCount: 234,
        fileSize: '2.5 MB',
        user: 'فاطمة أحمد'
      },
      {
        id: 2,
        fileName: 'sales_report_2024_07_03.pdf',
        type: 'تقرير المبيعات',
        date: '2024-07-03 16:30',
        status: 'مكتمل',
        recordsCount: 178,
        fileSize: '1.8 MB',
        user: 'علي حسين'
      },
      {
        id: 3,
        fileName: 'customers_list_2024_07_02.csv',
        type: 'قائمة العملاء',
        date: '2024-07-02 13:20',
        status: 'مكتمل',
        recordsCount: 89,
        fileSize: '0.5 MB',
        user: 'نور الدين'
      }
    ]

    setImportHistory(mockImportHistory)
    setExportHistory(mockExportHistory)
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleFileUpload = (event, dataType) => {
    const file = event.target.files[0]
    if (!file) return

    setLoading(true)
    setUploadProgress(0)

    // محاكاة رفع الملف
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setLoading(false)
          showNotification(`تم استيراد ${dataType} بنجاح!`)
          return 100
        }
        return prev + 10
      })
    }, 200)
  }

  const handleExport = (dataType, format) => {
    setLoading(true)
    
    // محاكاة تصدير البيانات
    setTimeout(() => {
      const fileName = `${dataType}_${new Date().toISOString().split('T')[0]}.${format}`
      
      // إنشاء رابط تحميل وهمي
      const link = document.createElement('a')
      link.href = '#'
      link.download = fileName
      link.click()
      
      setLoading(false)
      showNotification(`تم تصدير ${dataType} بصيغة ${format.toUpperCase()} بنجاح!`)
    }, 2000)
  }

  const downloadTemplate = (templateType) => {
    // محاكاة تحميل القالب
    const templates = {
      products: 'template_products.xlsx',
      customers: 'template_customers.xlsx',
      suppliers: 'template_suppliers.xlsx',
      invoices: 'template_invoices.xlsx'
    }
    
    const fileName = templates[templateType]
    showNotification(`تم تحميل قالب ${templateType} بنجاح!`)
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'مكتمل':
        return <CheckCircle className="h-5 w-5 text-primary" />
      case 'فشل':
        return <AlertCircle className="h-5 w-5 text-destructive" />
      default:
        return <RefreshCw className="h-5 w-5 text-accent animate-spin" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'مكتمل':
        return 'bg-primary/20 text-green-800'
      case 'فشل':
        return 'bg-destructive/20 text-red-800'
      default:
        return 'bg-accent/20 text-yellow-800'
    }
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">الاستيراد والتصدير</h1>
          <p className="text-muted-foreground">استيراد وتصدير البيانات من وإلى ملفات Excel و CSV</p>
        </div>
        <button
          onClick={loadHistory}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="border-b border-border">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('import')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === 'import'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
              }`}
            >
              <Upload className="w-5 h-5 ml-2" />
              استيراد البيانات
            </button>
            <button
              onClick={() => setActiveTab('export')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === 'export'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
              }`}
            >
              <Download className="w-5 h-5 ml-2" />
              تصدير البيانات
            </button>
          </nav>
        </div>
      </div>

      {/* Import Tab */}
      {activeTab === 'import' && (
        <div className="space-y-6">
          {/* Import Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-6 rounded-lg shadow border">
              <div className="flex items-center justify-between mb-4">
                <Package className="h-8 w-8 text-primary-600" />
                <button
                  onClick={() => downloadTemplate('products')}
                  className="text-sm text-primary-600 hover:text-primary-800"
                >
                  تحميل القالب
                </button>
              </div>
              <h3 className="text-lg font-semibold mb-2">المنتجات</h3>
              <p className="text-muted-foreground text-sm mb-4">استيراد بيانات المنتجات والفئات</p>
              <label className="block">
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={(e) => handleFileUpload(e, 'المنتجات')}
                  className="hidden"
                />
                <div className="bg-primary-50 border-2 border-dashed border-primary-300 rounded-lg p-4 text-center cursor-pointer hover:bg-primary-100">
                  <FileSpreadsheet className="h-8 w-8 text-primary-600 mx-auto mb-2" />
                  <span className="text-primary-600 font-medium">اختر ملف Excel</span>
                </div>
              </label>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <div className="flex items-center justify-between mb-4">
                <Users className="h-8 w-8 text-primary" />
                <button
                  onClick={() => downloadTemplate('customers')}
                  className="text-sm text-primary hover:text-green-800"
                >
                  تحميل القالب
                </button>
              </div>
              <h3 className="text-lg font-semibold mb-2">العملاء</h3>
              <p className="text-muted-foreground text-sm mb-4">استيراد بيانات العملاء والشركات</p>
              <label className="block">
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={(e) => handleFileUpload(e, 'العملاء')}
                  className="hidden"
                />
                <div className="bg-primary/10 border-2 border-dashed border-green-300 rounded-lg p-4 text-center cursor-pointer hover:bg-primary/20">
                  <FileSpreadsheet className="h-8 w-8 text-primary mx-auto mb-2" />
                  <span className="text-primary font-medium">اختر ملف Excel</span>
                </div>
              </label>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <div className="flex items-center justify-between mb-4">
                <Truck className="h-8 w-8 text-purple-600" />
                <button
                  onClick={() => downloadTemplate('suppliers')}
                  className="text-sm text-purple-600 hover:text-purple-800"
                >
                  تحميل القالب
                </button>
              </div>
              <h3 className="text-lg font-semibold mb-2">الموردين</h3>
              <p className="text-muted-foreground text-sm mb-4">استيراد بيانات الموردين والشركات</p>
              <label className="block">
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={(e) => handleFileUpload(e, 'الموردين')}
                  className="hidden"
                />
                <div className="bg-purple-50 border-2 border-dashed border-purple-300 rounded-lg p-4 text-center cursor-pointer hover:bg-purple-100">
                  <FileSpreadsheet className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <span className="text-purple-600 font-medium">اختر ملف Excel</span>
                </div>
              </label>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <div className="flex items-center justify-between mb-4">
                <ShoppingCart className="h-8 w-8 text-accent" />
                <button
                  onClick={() => downloadTemplate('invoices')}
                  className="text-sm text-accent hover:text-orange-800"
                >
                  تحميل القالب
                </button>
              </div>
              <h3 className="text-lg font-semibold mb-2">الفواتير</h3>
              <p className="text-muted-foreground text-sm mb-4">استيراد فواتير المبيعات والمشتريات</p>
              <label className="block">
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={(e) => handleFileUpload(e, 'الفواتير')}
                  className="hidden"
                />
                <div className="bg-accent/10 border-2 border-dashed border-orange-300 rounded-lg p-4 text-center cursor-pointer hover:bg-accent/20">
                  <FileSpreadsheet className="h-8 w-8 text-accent mx-auto mb-2" />
                  <span className="text-accent font-medium">اختر ملف Excel</span>
                </div>
              </label>
            </div>
          </div>

          {/* Upload Progress */}
          {loading && uploadProgress > 0 && (
            <div className="bg-white p-6 rounded-lg shadow border">
              <h3 className="text-lg font-semibold mb-4">جاري الاستيراد...</h3>
              <div className="w-full bg-muted rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p className="text-sm text-muted-foreground mt-2">{uploadProgress}% مكتمل</p>
            </div>
          )}

          {/* Import History */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-border">
              <h3 className="text-lg font-semibold">سجل الاستيراد</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الملف</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النتائج</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المستخدم</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {importHistory.map((record) => (
                    <tr key={record.id} className="hover:bg-muted/50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <FileSpreadsheet className="h-5 w-5 text-primary ml-2" />
                          <span className="text-sm font-medium text-foreground">{record.fileName}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <Calendar className="h-4 w-4 text-gray-400 ml-2" />
                          <span className="text-sm text-foreground">{record.date}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {getStatusIcon(record.status)}
                          <span className={`mr-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(record.status)}`}>
                            {record.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        <div>
                          <span className="text-primary">{record.recordsSuccess} نجح</span>
                          {record.recordsError > 0 && (
                            <span className="text-destructive mr-2">{record.recordsError} فشل</span>
                          )}
                        </div>
                        <div className="text-xs text-gray-500">من أصل {record.recordsProcessed}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.user}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className="text-primary-600 hover:text-primary-900" title="عرض التفاصيل">
                            <Eye className="h-4 w-4" />
                          </button>
                          <button className="text-destructive hover:text-red-900" title="حذف">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Export Tab */}
      {activeTab === 'export' && (
        <div className="space-y-6">
          {/* Export Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-6 rounded-lg shadow border">
              <BarChart3 className="h-8 w-8 text-primary-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">تقارير المخزون</h3>
              <p className="text-muted-foreground text-sm mb-4">تصدير تقارير المخزون والحركات</p>
              <div className="space-y-2">
                <button
                  onClick={() => handleExport('تقرير المخزون', 'xlsx')}
                  className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 text-sm"
                >
                  Excel
                </button>
                <button
                  onClick={() => handleExport('تقرير المخزون', 'pdf')}
                  className="w-full bg-destructive text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm"
                >
                  PDF
                </button>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <ShoppingCart className="h-8 w-8 text-primary mb-4" />
              <h3 className="text-lg font-semibold mb-2">تقارير المبيعات</h3>
              <p className="text-muted-foreground text-sm mb-4">تصدير فواتير وتقارير المبيعات</p>
              <div className="space-y-2">
                <button
                  onClick={() => handleExport('تقرير المبيعات', 'xlsx')}
                  className="w-full bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 text-sm"
                >
                  Excel
                </button>
                <button
                  onClick={() => handleExport('تقرير المبيعات', 'pdf')}
                  className="w-full bg-destructive text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm"
                >
                  PDF
                </button>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <Users className="h-8 w-8 text-purple-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">قوائم العملاء</h3>
              <p className="text-muted-foreground text-sm mb-4">تصدير بيانات العملاء والموردين</p>
              <div className="space-y-2">
                <button
                  onClick={() => handleExport('قائمة العملاء', 'xlsx')}
                  className="w-full bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 text-sm"
                >
                  Excel
                </button>
                <button
                  onClick={() => handleExport('قائمة العملاء', 'csv')}
                  className="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm"
                >
                  CSV
                </button>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <Database className="h-8 w-8 text-accent mb-4" />
              <h3 className="text-lg font-semibold mb-2">نسخة احتياطية</h3>
              <p className="text-muted-foreground text-sm mb-4">تصدير نسخة احتياطية كاملة</p>
              <div className="space-y-2">
                <button
                  onClick={() => handleExport('النسخة الاحتياطية', 'zip')}
                  className="w-full bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 text-sm"
                >
                  ZIP
                </button>
                <button
                  onClick={() => handleExport('النسخة الاحتياطية', 'sql')}
                  className="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm"
                >
                  SQL
                </button>
              </div>
            </div>
          </div>

          {/* Export History */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-border">
              <h3 className="text-lg font-semibold">سجل التصدير</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الملف</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">عدد السجلات</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">حجم الملف</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المستخدم</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {exportHistory.map((record) => (
                    <tr key={record.id} className="hover:bg-muted/50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <FileText className="h-5 w-5 text-primary-600 ml-2" />
                          <span className="text-sm font-medium text-foreground">{record.fileName}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <Calendar className="h-4 w-4 text-gray-400 ml-2" />
                          <span className="text-sm text-foreground">{record.date}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {getStatusIcon(record.status)}
                          <span className={`mr-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(record.status)}`}>
                            {record.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.recordsCount}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.fileSize}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{record.user}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className="text-primary hover:text-green-900" title="تحميل">
                            <Download className="h-4 w-4" />
                          </button>
                          <button className="text-destructive hover:text-red-900" title="حذف">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white z-50`}>
          {notification.message}
        </div>
      )}
    </div>
  )
}

export default ImportExport

