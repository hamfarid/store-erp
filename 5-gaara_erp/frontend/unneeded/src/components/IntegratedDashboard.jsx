import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'
import { dashboardAPI } from '../services/api'
import LoadingSpinner from './common/LoadingSpinner'
import { useToast } from './common/EnhancedToast'

const IntegratedDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState('month')
  const [alerts, setAlerts] = useState([])
  const toast = useToast()

  // تحميل بيانات لوحة التحكم من الخلفية
  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [dashboardResponse, alertsResponse] = await Promise.all([
        dashboardAPI.getDashboardData(selectedPeriod),
        dashboardAPI.getAlerts()
      ])

      if (dashboardResponse.success) {
        setDashboardData(dashboardResponse.data)
      }

      if (alertsResponse.success) {
        setAlerts(alertsResponse.data)
      }
    } catch (error) {
      toast.error('فشل في تحميل بيانات لوحة التحكم')

      // استخدام البيانات الاحتياطية
      setDashboardData(mockDashboardData)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboardData()
  }, [selectedPeriod])

  // بيانات احتياطية للوحة المتكاملة
  const mockDashboardData = {
    summary: {
      total_products: 150,
      total_inventory_value: 125000,
      low_stock_alerts: 5,
      pending_orders: 12,
      monthly_sales: 85000,
      monthly_purchases: 45000,
      profit_margin: 32.5,
      inventory_turnover: 4.2
    },
    inventory_trends: [
      { month: 'يناير', value: 120000, quantity: 4800 },
      { month: 'فبراير', value: 115000, quantity: 4600 },
      { month: 'مارس', value: 125000, quantity: 5000 },
      { month: 'أبريل', value: 130000, quantity: 5200 },
      { month: 'مايو', value: 128000, quantity: 5100 },
      { month: 'يونيو', value: 125000, quantity: 5000 }
    ],
    category_distribution: [
      { name: 'بذور', value: 48, amount: 60000 },
      { name: 'أسمدة', value: 36, amount: 45000 },
      { name: 'مبيدات', value: 16, amount: 20000 }
    ],
    warehouse_performance: [
      { name: 'المخزن الرئيسي', utilization: 75, value: 80000 },
      { name: 'مخزن الفرع الأول', utilization: 60, value: 30000 },
      { name: 'مخزن الفرع الثاني', utilization: 45, value: 15000 }
    ],
    recent_activities: [
      {
        id: 1,
        type: 'stock_movement',
        description: 'استلام دفعة بذور طماطم - 100 كيلو',
        timestamp: '2024-12-01 14:30',
        user: 'أحمد محمد'
      },
      {
        id: 2,
        type: 'sale_order',
        description: 'أمر بيع جديد - العميل: مزرعة النيل',
        timestamp: '2024-12-01 13:15',
        user: 'فاطمة علي'
      },
      {
        id: 3,
        type: 'low_stock',
        description: 'تنبيه: مخزون بذور الخيار منخفض',
        timestamp: '2024-12-01 12:00',
        user: 'النظام'
      }
    ]
  }

  const mockAlerts = [
    {
      id: 1,
      type: 'low_stock',
      title: 'مخزون منخفض',
      message: '5 منتجات تحتاج إعادة طلب',
      urgency: 'high',
      timestamp: '2024-12-01 10:00'
    },
    {
      id: 2,
      type: 'expiring_lots',
      title: 'لوط قريبة الانتهاء',
      message: '3 لوط تنتهي خلال 30 يوم',
      urgency: 'medium',
      timestamp: '2024-12-01 09:30'
    },
    {
      id: 3,
      type: 'accounting_variance',
      title: 'تباين محاسبي',
      message: 'فرق 150 ج.م بين المخزون والمحاسبة',
      urgency: 'low',
      timestamp: '2024-12-01 08:00'
    }
  ]

  useEffect(() => {
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setDashboardData(mockDashboardData)
      setAlerts(mockAlerts)
      setLoading(false)
    }, 1500)
  }, [selectedPeriod])

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'high': return 'bg-destructive/20 border-red-500 text-destructive'
      case 'medium': return 'bg-accent/20 border-yellow-500 text-yellow-700'
      case 'low': return 'bg-primary-100 border-primary-500 text-primary-700'
      default: return 'bg-muted border-gray-500 text-foreground'
    }
  }

  const getActivityIcon = (type) => {
    switch (type) {
      case 'stock_movement': return <Package className="w-4 h-4" />
      case 'sale_order': return <DollarSign className="w-4 h-4" />
      case 'low_stock': return <AlertTriangle className="w-4 h-4" />
      default: return <Activity className="w-4 h-4" />
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        <LoadingSpinner
          size="large"
          text="جاري تحميل لوحة التحكم المتكاملة..."
          fullScreen={false}
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس لوحة التحكم */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">لوحة التحكم المتكاملة</h1>
          <p className="text-muted-foreground">نظرة شاملة على المخزون والمبيعات والمحاسبة</p>
        </div>
        <div className="flex gap-2">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="week">هذا الأسبوع</option>
            <option value="month">هذا الشهر</option>
            <option value="quarter">هذا الربع</option>
            <option value="year">هذا العام</option>
          </select>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center">
            <FileText className="w-4 h-4 ml-2" />
            تصدير التقرير
          </button>
        </div>
      </div>

      {/* الإحصائيات الرئيسية */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">قيمة المخزون</p>
              <p className="text-2xl font-bold text-foreground">
                {dashboardData.summary.total_inventory_value.toLocaleString()} ج.م
              </p>
              <div className="flex items-center mt-2">
                <ArrowUp className="w-4 h-4 text-green-500" />
                <span className="text-sm text-primary">+5.2% من الشهر الماضي</span>
              </div>
            </div>
            <Package className="w-12 h-12 text-primary-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">المبيعات الشهرية</p>
              <p className="text-2xl font-bold text-foreground">
                {dashboardData.summary.monthly_sales.toLocaleString()} ج.م
              </p>
              <div className="flex items-center mt-2">
                <ArrowUp className="w-4 h-4 text-green-500" />
                <span className="text-sm text-primary">+12.8% من الشهر الماضي</span>
              </div>
            </div>
            <TrendingUp className="w-12 h-12 text-primary" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">هامش الربح</p>
              <p className="text-2xl font-bold text-foreground">
                {dashboardData.summary.profit_margin}%
              </p>
              <div className="flex items-center mt-2">
                <ArrowDown className="w-4 h-4 text-red-500" />
                <span className="text-sm text-destructive">-2.1% من الشهر الماضي</span>
              </div>
            </div>
            <DollarSign className="w-12 h-12 text-purple-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">تنبيهات المخزون</p>
              <p className="text-2xl font-bold text-foreground">
                {dashboardData.summary.low_stock_alerts}
              </p>
              <div className="flex items-center mt-2">
                <AlertTriangle className="w-4 h-4 text-orange-500" />
                <span className="text-sm text-accent">يحتاج متابعة</span>
              </div>
            </div>
            <Bell className="w-12 h-12 text-accent" />
          </div>
        </div>
      </div>

      {/* الرسوم البيانية */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* اتجاهات المخزون */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">اتجاهات قيمة المخزون</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dashboardData.inventory_trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => [`${value.toLocaleString()} ج.م`, 'القيمة']} />
              <Area type="monotone" dataKey="value" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* توزيع الفئات */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">توزيع المخزون حسب الفئة</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={dashboardData.category_distribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {dashboardData.category_distribution.map((entry, index) => (
                  <Cell key={`cell-${entry.name}-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}%`, 'النسبة']} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* أداء المخازن والتنبيهات */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* أداء المخازن */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">أداء المخازن</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dashboardData.warehouse_performance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="utilization" fill="#10B981" name="نسبة الاستخدام %" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* التنبيهات */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">التنبيهات الحديثة</h3>
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-3 rounded-lg border-r-4 ${getUrgencyColor(alert.urgency)}`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium">{alert.title}</h4>
                    <p className="text-sm mt-1">{alert.message}</p>
                  </div>
                  <span className="text-xs">{alert.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* الأنشطة الحديثة */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">الأنشطة الحديثة</h3>
        <div className="space-y-3">
          {dashboardData.recent_activities.map((activity) => (
            <div key={activity.id} className="flex items-center p-3 hover:bg-muted/50 rounded-lg">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600">
                {getActivityIcon(activity.type)}
              </div>
              <div className="mr-3 flex-1">
                <p className="text-sm font-medium text-foreground">{activity.description}</p>
                <p className="text-xs text-gray-500">بواسطة {activity.user} - {activity.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default IntegratedDashboard

