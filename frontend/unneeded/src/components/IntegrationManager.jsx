import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'
import { toast } from 'react-hot-toast'

const IntegrationManager = () => {
  const [integrationStatus, setIntegrationStatus] = useState({})
  const [syncHistory, setSyncHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [syncing, setSyncing] = useState(false)

  // بيانات تجريبية لحالة التكامل
  const mockIntegrationStatus = {
    inventory_accounting: {
      name: 'تكامل المخزون والمحاسبة',
      status: 'connected',
      last_sync: '2024-12-01 14:30:00',
      sync_frequency: 'real_time',
      records_synced: 1250,
      errors: 0,
      health_score: 98
    },
    sales_inventory: {
      name: 'تكامل المبيعات والمخزون',
      status: 'connected',
      last_sync: '2024-12-01 14:25:00',
      sync_frequency: 'real_time',
      records_synced: 856,
      errors: 2,
      health_score: 95
    },
    purchases_inventory: {
      name: 'تكامل المشتريات والمخزون',
      status: 'warning',
      last_sync: '2024-12-01 13:45:00',
      sync_frequency: 'hourly',
      records_synced: 432,
      errors: 5,
      health_score: 87
    },
    user_permissions: {
      name: 'تكامل الصلاحيات والمستخدمين',
      status: 'connected',
      last_sync: '2024-12-01 14:00:00',
      sync_frequency: 'daily',
      records_synced: 125,
      errors: 0,
      health_score: 100
    }
  }

  const mockSyncHistory = [
    {
      id: 1,
      integration: 'inventory_accounting',
      type: 'automatic',
      status: 'success',
      records_processed: 45,
      duration: '2.3s',
      timestamp: '2024-12-01 14:30:00',
      message: 'تم مزامنة القيود المحاسبية بنجاح'
    },
    {
      id: 2,
      integration: 'sales_inventory',
      type: 'manual',
      status: 'success',
      records_processed: 12,
      duration: '1.8s',
      timestamp: '2024-12-01 14:25:00',
      message: 'تم مزامنة أوامر البيع'
    },
    {
      id: 3,
      integration: 'purchases_inventory',
      type: 'automatic',
      status: 'warning',
      records_processed: 8,
      duration: '5.2s',
      timestamp: '2024-12-01 13:45:00',
      message: 'تمت المزامنة مع تحذيرات بسيطة'
    },
    {
      id: 4,
      integration: 'inventory_accounting',
      type: 'automatic',
      status: 'error',
      records_processed: 0,
      duration: '0.5s',
      timestamp: '2024-12-01 12:15:00',
      message: 'فشل في الاتصال بنظام المحاسبة'
    }
  ]

  useEffect(() => {
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setIntegrationStatus(mockIntegrationStatus)
      setSyncHistory(mockSyncHistory)
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected': return 'text-primary bg-primary/20'
      case 'warning': return 'text-accent bg-accent/20'
      case 'error': return 'text-destructive bg-destructive/20'
      case 'disconnected': return 'text-muted-foreground bg-muted'
      default: return 'text-muted-foreground bg-muted'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'connected': return <CheckCircle className="w-5 h-5" />
      case 'warning': return <AlertCircle className="w-5 h-5" />
      case 'error': return <XCircle className="w-5 h-5" />
      case 'disconnected': return <XCircle className="w-5 h-5" />
      default: return <AlertCircle className="w-5 h-5" />
    }
  }

  const getSyncStatusColor = (status) => {
    switch (status) {
      case 'success': return 'text-primary'
      case 'warning': return 'text-accent'
      case 'error': return 'text-destructive'
      default: return 'text-muted-foreground'
    }
  }

  const getIntegrationIcon = (key) => {
    switch (key) {
      case 'inventory_accounting': return <DollarSign className="w-6 h-6" />
      case 'sales_inventory': return <Package className="w-6 h-6" />
      case 'purchases_inventory': return <FileText className="w-6 h-6" />
      case 'user_permissions': return <Users className="w-6 h-6" />
      default: return <Database className="w-6 h-6" />
    }
  }

  const handleManualSync = async (integrationKey) => {
    setSyncing(true)
    try {
      // محاكاة عملية المزامنة
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // تحديث حالة التكامل
      setIntegrationStatus(prev => ({
        ...prev,
        [integrationKey]: {
          ...prev[integrationKey],
          last_sync: new Date().toLocaleString('ar-EG'),
          errors: 0
        }
      }))

      // إضافة سجل جديد للمزامنة
      const newSyncRecord = {
        id: Date.now(),
        integration: integrationKey,
        type: 'manual',
        status: 'success',
        records_processed: Math.floor(Math.random() * 50) + 1,
        duration: `${(Math.random() * 3 + 1).toFixed(1)}s`,
        timestamp: new Date().toLocaleString('ar-EG'),
        message: 'تمت المزامنة اليدوية بنجاح'
      }

      setSyncHistory(prev => [newSyncRecord, ...prev.slice(0, 9)])
      toast.success('تمت المزامنة بنجاح')
      
    } catch (error) {
      toast.error('فشل في المزامنة')
    } finally {
      setSyncing(false)
    }
  }

  const handleSyncAll = async () => {
    setSyncing(true)
    try {
      // محاكاة مزامنة جميع التكاملات
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // تحديث جميع حالات التكامل
      const updatedStatus = { ...integrationStatus }
      Object.keys(updatedStatus).forEach(key => {
        updatedStatus[key] = {
          ...updatedStatus[key],
          last_sync: new Date().toLocaleString('ar-EG'),
          errors: 0,
          status: 'connected'
        }
      })
      setIntegrationStatus(updatedStatus)
      
      toast.success('تمت مزامنة جميع التكاملات بنجاح')
      
    } catch (error) {
      toast.error('فشل في المزامنة الشاملة')
    } finally {
      setSyncing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="mr-3 text-muted-foreground">جاري تحميل حالة التكامل...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة التكامل</h1>
          <p className="text-muted-foreground">مراقبة وإدارة التكامل بين المديولات المختلفة</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleSyncAll}
            disabled={syncing}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
          >
            <Sync className={`w-4 h-4 ml-2 ${syncing ? 'animate-spin' : ''}`} />
            مزامنة شاملة
          </button>
          <button className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center">
            <Settings className="w-4 h-4 ml-2" />
            إعدادات التكامل
          </button>
        </div>
      </div>

      {/* نظرة عامة على حالة التكامل */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Object.entries(integrationStatus).map(([key, integration]) => (
          <div key={key} className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="text-primary-600">
                  {getIntegrationIcon(key)}
                </div>
                <h3 className="text-sm font-medium text-foreground mr-2">{integration.name}</h3>
              </div>
              <div className={`flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(integration.status)}`}>
                {getStatusIcon(integration.status)}
                <span className="mr-1">
                  {integration.status === 'connected' ? 'متصل' : 
                   integration.status === 'warning' ? 'تحذير' : 
                   integration.status === 'error' ? 'خطأ' : 'منقطع'}
                </span>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">آخر مزامنة:</span>
                <span className="text-foreground">{integration.last_sync}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">السجلات:</span>
                <span className="text-foreground">{integration.records_synced}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">الأخطاء:</span>
                <span className={integration.errors > 0 ? 'text-destructive' : 'text-primary'}>
                  {integration.errors}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">نقاط الصحة:</span>
                <span className="text-foreground">{integration.health_score}%</span>
              </div>
            </div>
            
            <button
              onClick={() => handleManualSync(key)}
              disabled={syncing}
              className="w-full mt-4 bg-primary-50 text-primary-600 px-3 py-2 rounded-md hover:bg-primary-100 disabled:opacity-50 flex items-center justify-center text-sm"
            >
              <RefreshCw className={`w-4 h-4 ml-1 ${syncing ? 'animate-spin' : ''}`} />
              مزامنة يدوية
            </button>
          </div>
        ))}
      </div>

      {/* سجل المزامنة */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">سجل المزامنة</h3>
          <p className="text-muted-foreground text-sm">آخر عمليات المزامنة والتكامل</p>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التكامل</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">السجلات</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المدة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التوقيت</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الرسالة</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {syncHistory.map((record) => (
                <tr key={record.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="text-primary-600">
                        {getIntegrationIcon(record.integration)}
                      </div>
                      <span className="mr-2 text-sm font-medium text-foreground">
                        {integrationStatus[record.integration]?.name}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      record.type === 'automatic' ? 'bg-primary-100 text-primary-800' : 'bg-purple-100 text-purple-800'
                    }`}>
                      {record.type === 'automatic' ? 'تلقائي' : 'يدوي'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`text-sm font-medium ${getSyncStatusColor(record.status)}`}>
                      {record.status === 'success' ? 'نجح' : 
                       record.status === 'warning' ? 'تحذير' : 'فشل'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {record.records_processed}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {record.duration}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {record.timestamp}
                  </td>
                  <td className="px-6 py-4 text-sm text-foreground">
                    {record.message}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default IntegrationManager

