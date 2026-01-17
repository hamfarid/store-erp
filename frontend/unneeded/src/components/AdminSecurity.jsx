import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Monitor, Shield
} from 'lucide-react'

const AdminSecurity = () => {
  const [securityLogs, setSecurityLogs] = useState([])
  const [filteredLogs, setFilteredLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [activeTab, setActiveTab] = useState('logs')

  useEffect(() => {
    loadSecurityLogs()
  }, [])

  useEffect(() => {
    filterLogs()
  }, [securityLogs, searchTerm, filterType])

  const loadSecurityLogs = async () => {
    setLoading(true)
    try {
      // بيانات تجريبية لسجلات الأمان
      const mockLogs = [
        {
          id: 1,
          type: 'login_success',
          user: 'admin',
          userName: 'مدير النظام',
          action: 'تسجيل دخول ناجح',
          ipAddress: '192.168.1.100',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'القاهرة، مصر',
          timestamp: '2024-07-04 10:30:15',
          severity: 'info'
        },
        {
          id: 2,
          type: 'login_failed',
          user: 'unknown',
          userName: 'غير معروف',
          action: 'محاولة تسجيل دخول فاشلة',
          ipAddress: '192.168.1.150',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'غير محدد',
          timestamp: '2024-07-04 09:45:22',
          severity: 'warning'
        },
        {
          id: 3,
          type: 'password_change',
          user: 'sales_manager',
          userName: 'أحمد محمد',
          action: 'تغيير كلمة المرور',
          ipAddress: '192.168.1.105',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'الجيزة، مصر',
          timestamp: '2024-07-04 08:15:30',
          severity: 'info'
        },
        {
          id: 4,
          type: 'suspicious_activity',
          user: 'warehouse_manager',
          userName: 'سارة علي',
          action: 'محاولة الوصول لصفحة غير مصرح بها',
          ipAddress: '192.168.1.110',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'الإسكندرية، مصر',
          timestamp: '2024-07-03 16:20:45',
          severity: 'error'
        },
        {
          id: 5,
          type: 'data_export',
          user: 'accountant',
          userName: 'محمد حسن',
          action: 'تصدير بيانات التقارير المالية',
          ipAddress: '192.168.1.115',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'القاهرة، مصر',
          timestamp: '2024-07-03 14:30:12',
          severity: 'info'
        },
        {
          id: 6,
          type: 'account_locked',
          user: 'sales_engineer',
          userName: 'فاطمة أحمد',
          action: 'قفل الحساب بسبب محاولات دخول متعددة فاشلة',
          ipAddress: '192.168.1.120',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          location: 'المنيا، مصر',
          timestamp: '2024-07-03 12:45:18',
          severity: 'warning'
        }
      ]
      setSecurityLogs(mockLogs)
    } catch (error) {
      } finally {
      setLoading(false)
    }
  }

  const filterLogs = () => {
    let filtered = securityLogs

    if (searchTerm) {
      filtered = filtered.filter(log =>
        log.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.userName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.ipAddress.includes(searchTerm)
      )
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(log => log.type === filterType)
    }

    setFilteredLogs(filtered)
  }

  const getLogIcon = (type) => {
    switch (type) {
      case 'login_success':
        return <CheckCircle className="h-5 w-5 text-primary" />
      case 'login_failed':
        return <XCircle className="h-5 w-5 text-destructive" />
      case 'password_change':
        return <Lock className="h-5 w-5 text-primary-600" />
      case 'suspicious_activity':
        return <AlertTriangle className="h-5 w-5 text-accent" />
      case 'data_export':
        return <Download className="h-5 w-5 text-purple-600" />
      case 'account_locked':
        return <Shield className="h-5 w-5 text-destructive" />
      default:
        return <Activity className="h-5 w-5 text-muted-foreground" />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'info':
        return 'bg-primary-100 text-primary-800'
      case 'warning':
        return 'bg-accent/20 text-yellow-800'
      case 'error':
        return 'bg-destructive/20 text-red-800'
      default:
        return 'bg-muted text-foreground'
    }
  }

  const getSeverityLabel = (severity) => {
    switch (severity) {
      case 'info':
        return 'معلومات'
      case 'warning':
        return 'تحذير'
      case 'error':
        return 'خطأ'
      default:
        return 'عام'
    }
  }

  const tabs = [
    { id: 'logs', name: 'سجلات الأمان', icon: Eye },
    { id: 'monitoring', name: 'المراقبة المباشرة', icon: Monitor },
    { id: 'settings', name: 'إعدادات الأمان', icon: Shield }
  ]

  const handleExportLogs = () => {
    // تصدير السجلات
    const csvContent = "data:text/csv;charset=utf-8,"
      + "التاريخ,النوع,المستخدم,الوصف,عنوان IP\n"
      + securityLogs.map(log =>
          `${log.timestamp},${log.type},${log.user},${log.description},${log.ip}`
        ).join("\n")

    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", `security_logs_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    alert('تم تصدير السجلات بنجاح!')
  }

  const handleSaveSettings = () => {
    // حفظ إعدادات الأمان
    alert('تم حفظ إعدادات الأمان بنجاح!')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">الأمان والمراقبة</h1>
          <p className="text-muted-foreground">مراقبة أنشطة النظام وسجلات الأمان</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleExportLogs}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
          >
            <Download className="w-5 h-5 ml-2" />
            تصدير السجلات
          </button>
          <button
            onClick={loadSecurityLogs}
            className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
          >
            <RefreshCw className="w-5 h-5 ml-2" />
            تحديث
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
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
      </div>

      {/* Security Logs Tab */}
      {activeTab === 'logs' && (
        <>
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg shadow border">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-primary" />
                <div className="mr-3">
                  <p className="text-sm font-medium text-muted-foreground">تسجيل دخول ناجح</p>
                  <p className="text-2xl font-bold text-foreground">
                    {securityLogs.filter(log => log.type === 'login_success').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border">
              <div className="flex items-center">
                <XCircle className="h-8 w-8 text-destructive" />
                <div className="mr-3">
                  <p className="text-sm font-medium text-muted-foreground">محاولات فاشلة</p>
                  <p className="text-2xl font-bold text-foreground">
                    {securityLogs.filter(log => log.type === 'login_failed').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border">
              <div className="flex items-center">
                <AlertTriangle className="h-8 w-8 text-accent" />
                <div className="mr-3">
                  <p className="text-sm font-medium text-muted-foreground">أنشطة مشبوهة</p>
                  <p className="text-2xl font-bold text-foreground">
                    {securityLogs.filter(log => log.type === 'suspicious_activity').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border">
              <div className="flex items-center">
                <Shield className="h-8 w-8 text-primary-600" />
                <div className="mr-3">
                  <p className="text-sm font-medium text-muted-foreground">إجمالي السجلات</p>
                  <p className="text-2xl font-bold text-foreground">{securityLogs.length}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="البحث في السجلات..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>

            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">جميع الأنواع</option>
              <option value="login_success">تسجيل دخول ناجح</option>
              <option value="login_failed">محاولة دخول فاشلة</option>
              <option value="password_change">تغيير كلمة المرور</option>
              <option value="suspicious_activity">نشاط مشبوه</option>
              <option value="data_export">تصدير بيانات</option>
              <option value="account_locked">قفل حساب</option>
            </select>

            <select className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              <option value="all">جميع الفترات</option>
              <option value="today">اليوم</option>
              <option value="week">آخر أسبوع</option>
              <option value="month">آخر شهر</option>
            </select>
          </div>

          {/* Security Logs Table */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    النوع
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    المستخدم
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الإجراء
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    عنوان IP
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الموقع
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الوقت
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الخطورة
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-muted/50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getLogIcon(log.type)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-foreground">{log.userName}</div>
                      <div className="text-sm text-gray-500">@{log.user}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                      {log.action}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                      {log.ipAddress}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 text-gray-400 ml-2" />
                        {log.location}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 text-gray-400 ml-2" />
                        {log.timestamp}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(log.severity)}`}>
                        {getSeverityLabel(log.severity)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Monitoring Tab */}
      {activeTab === 'monitoring' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-foreground mb-4">المراقبة المباشرة</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-border rounded-lg p-4">
              <h4 className="font-medium text-foreground mb-2">المستخدمين المتصلين حالياً</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">مدير النظام</span>
                  <span className="inline-flex px-2 py-1 text-xs bg-primary/20 text-green-800 rounded-full">
                    متصل
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">أحمد محمد</span>
                  <span className="inline-flex px-2 py-1 text-xs bg-primary/20 text-green-800 rounded-full">
                    متصل
                  </span>
                </div>
              </div>
            </div>

            <div className="border border-border rounded-lg p-4">
              <h4 className="font-medium text-foreground mb-2">إحصائيات الأمان</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">محاولات الدخول اليوم</span>
                  <span className="text-sm font-medium text-foreground">15</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">محاولات فاشلة</span>
                  <span className="text-sm font-medium text-destructive">2</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Settings Tab */}
      {activeTab === 'settings' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-foreground mb-4">إعدادات الأمان</h3>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="session-timeout" className="block text-sm font-medium text-foreground mb-2">
                  مدة انتهاء الجلسة (دقيقة)
                </label>
                <input
                  id="session-timeout"
                  type="number"
                  defaultValue="30"
                  className="w-full p-2 border border-border rounded-lg"
                />
              </div>
              <div>
                <label htmlFor="login-attempts" className="block text-sm font-medium text-foreground mb-2">
                  عدد محاولات تسجيل الدخول المسموحة
                </label>
                <input
                  id="login-attempts"
                  type="number"
                  defaultValue="3"
                  className="w-full p-2 border border-border rounded-lg"
                />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label htmlFor="two-factor-auth" className="text-sm font-medium text-foreground">تفعيل المصادقة الثنائية</label>
                <label htmlFor="two-factor-auth" className="relative inline-flex items-center cursor-pointer">
                  <input id="two-factor-auth" type="checkbox" className="sr-only peer" />
                  <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="log-activities" className="text-sm font-medium text-foreground">تسجيل جميع الأنشطة</label>
                <label htmlFor="log-activities" className="relative inline-flex items-center cursor-pointer">
                  <input id="log-activities" type="checkbox" defaultChecked className="sr-only peer" />
                  <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>

            <button
              onClick={handleSaveSettings}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
            >
              حفظ الإعدادات
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminSecurity

