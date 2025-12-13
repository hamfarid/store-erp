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
  AlertTriangle,
  Clock,
  Activity,
  Shield,
  Database
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const AdminDashboard = () => {
  const [loading, setLoading] = useState(false)
  const [dashboardData, setDashboardData] = useState({
    systemStats: {
      totalUsers: 0,
      activeUsers: 0,
      totalSessions: 0,
      systemUptime: '0 days',
      lastBackup: null
    },
    systemHealth: {
      cpu: 0,
      memory: 0,
      disk: 0,
      network: 'good'
    },
    recentActivities: [],
    securityAlerts: [],
    systemLogs: []
  })

  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadDashboardData()
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/admin/dashboard')
      if (response.success) {
        setDashboardData(response.data)
      } else {
        // Use mock data if API not available
        setDashboardData({
          systemStats: {
            totalUsers: 25,
            activeUsers: 12,
            totalSessions: 45,
            systemUptime: '15 days, 8 hours',
            lastBackup: '2024-01-15T02:00:00Z'
          },
          systemHealth: {
            cpu: 35,
            memory: 68,
            disk: 45,
            network: 'good'
          },
          recentActivities: [
            {
              id: 1,
              user: 'أحمد محمد',
              action: 'تسجيل دخول',
              timestamp: '2024-01-15T10:30:00Z',
              ip: '192.168.1.100'
            },
            {
              id: 2,
              user: 'فاطمة علي',
              action: 'إضافة منتج جديد',
              timestamp: '2024-01-15T10:25:00Z',
              ip: '192.168.1.101'
            },
            {
              id: 3,
              user: 'محمد حسن',
              action: 'تحديث فاتورة',
              timestamp: '2024-01-15T10:20:00Z',
              ip: '192.168.1.102'
            }
          ],
          securityAlerts: [
            {
              id: 1,
              type: 'warning',
              message: 'محاولات تسجيل دخول فاشلة متعددة من IP: 192.168.1.200',
              timestamp: '2024-01-15T09:45:00Z'
            },
            {
              id: 2,
              type: 'info',
              message: 'تم تحديث كلمة مرور المستخدم: أحمد محمد',
              timestamp: '2024-01-15T08:30:00Z'
            }
          ],
          systemLogs: [
            {
              id: 1,
              level: 'info',
              message: 'تم بدء تشغيل النظام بنجاح',
              timestamp: '2024-01-15T00:00:00Z'
            },
            {
              id: 2,
              level: 'warning',
              message: 'استخدام الذاكرة مرتفع: 68%',
              timestamp: '2024-01-15T10:15:00Z'
            },
            {
              id: 3,
              level: 'error',
              message: 'فشل في الاتصال بقاعدة البيانات الخارجية',
              timestamp: '2024-01-15T09:30:00Z'
            }
          ]
        })
      }
    } catch (error) {
      toast.error('خطأ في تحميل لوحة تحكم الإدارة')
    } finally {
      setLoading(false)
    }
  }

  const getHealthColor = (percentage) => {
    if (percentage < 50) return 'text-primary'
    if (percentage < 80) return 'text-accent'
    return 'text-destructive'
  }

  const getHealthBgColor = (percentage) => {
    if (percentage < 50) return 'bg-primary'
    if (percentage < 80) return 'bg-yellow-600'
    return 'bg-destructive'
  }

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error':
        return <AlertTriangle className="w-5 h-5 text-destructive" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-accent" />
      case 'info':
        return <CheckCircle className="w-5 h-5 text-primary-600" />
      default:
        return <CheckCircle className="w-5 h-5 text-muted-foreground" />
    }
  }

  const getLogIcon = (level) => {
    switch (level) {
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-destructive" />
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-accent" />
      case 'info':
        return <CheckCircle className="w-4 h-4 text-primary-600" />
      default:
        return <CheckCircle className="w-4 h-4 text-muted-foreground" />
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('ar-EG')
  }

  if (loading && !dashboardData.systemStats.totalUsers) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Shield className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">لوحة تحكم الإدارة</h1>
              <p className="text-muted-foreground">مراقبة النظام والمستخدمين والأمان</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <div className="flex items-center text-sm text-gray-500">
              <Clock className="w-4 h-4 ml-1" />
              آخر تحديث: {formatTimestamp(new Date().toISOString())}
            </div>
          </div>
        </div>
      </div>

      {/* System Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Users className="w-6 h-6 text-primary-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-foreground">{dashboardData.systemStats.totalUsers}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary/20 rounded-lg">
              <Activity className="w-6 h-6 text-primary" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">المستخدمون النشطون</p>
              <p className="text-2xl font-bold text-foreground">{dashboardData.systemStats.activeUsers}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Wifi className="w-6 h-6 text-purple-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">الجلسات النشطة</p>
              <p className="text-2xl font-bold text-foreground">{dashboardData.systemStats.totalSessions}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-accent/20 rounded-lg">
              <Server className="w-6 h-6 text-accent" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">وقت التشغيل</p>
              <p className="text-lg font-bold text-foreground">{dashboardData.systemStats.systemUptime}</p>
            </div>
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Activity className="w-5 h-5 ml-2" />
          صحة النظام
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-foreground flex items-center">
                <Cpu className="w-4 h-4 ml-1" />
                المعالج
              </span>
              <span className={`text-sm font-bold ${getHealthColor(dashboardData.systemHealth.cpu)}`}>
                {dashboardData.systemHealth.cpu}%
              </span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getHealthBgColor(dashboardData.systemHealth.cpu)}`}
                style={{ width: `${dashboardData.systemHealth.cpu}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-foreground flex items-center">
                <Database className="w-4 h-4 ml-1" />
                الذاكرة
              </span>
              <span className={`text-sm font-bold ${getHealthColor(dashboardData.systemHealth.memory)}`}>
                {dashboardData.systemHealth.memory}%
              </span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getHealthBgColor(dashboardData.systemHealth.memory)}`}
                style={{ width: `${dashboardData.systemHealth.memory}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-foreground flex items-center">
                <HardDrive className="w-4 h-4 ml-1" />
                القرص الصلب
              </span>
              <span className={`text-sm font-bold ${getHealthColor(dashboardData.systemHealth.disk)}`}>
                {dashboardData.systemHealth.disk}%
              </span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getHealthBgColor(dashboardData.systemHealth.disk)}`}
                style={{ width: `${dashboardData.systemHealth.disk}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'overview', name: 'نظرة عامة', icon: Activity },
              { id: 'activities', name: 'الأنشطة الحديثة', icon: Clock },
              { id: 'security', name: 'تنبيهات الأمان', icon: Shield },
              { id: 'logs', name: 'سجلات النظام', icon: Database }
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
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-foreground">نظرة عامة على النظام</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-muted/50 rounded-lg p-4">
                  <h4 className="font-medium text-foreground mb-2">آخر نسخة احتياطية</h4>
                  <p className="text-sm text-muted-foreground">
                    {dashboardData.systemStats.lastBackup 
                      ? formatTimestamp(dashboardData.systemStats.lastBackup)
                      : 'لم يتم إنشاء نسخة احتياطية بعد'
                    }
                  </p>
                </div>
                <div className="bg-muted/50 rounded-lg p-4">
                  <h4 className="font-medium text-foreground mb-2">حالة الشبكة</h4>
                  <p className="text-sm text-muted-foreground flex items-center">
                    <CheckCircle className="w-4 h-4 text-primary ml-1" />
                    {dashboardData.systemHealth.network === 'good' ? 'جيدة' : 'ضعيفة'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'activities' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">الأنشطة الحديثة</h3>
              <div className="space-y-4">
                {dashboardData.recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-center">
                      <Activity className="w-5 h-5 text-primary-600 ml-3" />
                      <div>
                        <p className="font-medium text-foreground">{activity.user}</p>
                        <p className="text-sm text-muted-foreground">{activity.action}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="text-sm text-gray-500">{formatTimestamp(activity.timestamp)}</p>
                      <p className="text-xs text-gray-400">{activity.ip}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">تنبيهات الأمان</h3>
              <div className="space-y-4">
                {dashboardData.securityAlerts.map((alert) => (
                  <div key={alert.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-center">
                      {getAlertIcon(alert.type)}
                      <div className="mr-3">
                        <p className="font-medium text-foreground">{alert.message}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="text-sm text-gray-500">{formatTimestamp(alert.timestamp)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'logs' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">سجلات النظام</h3>
              <div className="space-y-2">
                {dashboardData.systemLogs.map((log) => (
                  <div key={log.id} className="flex items-center justify-between p-3 border-b border-border">
                    <div className="flex items-center">
                      {getLogIcon(log.level)}
                      <div className="mr-3">
                        <p className="text-sm text-foreground">{log.message}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="text-xs text-gray-500">{formatTimestamp(log.timestamp)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard

