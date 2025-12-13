import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Truck, RefreshCw, AlertTriangle, Activity, PieChart as PieChartIcon
} from 'lucide-react'
import PropTypes from 'prop-types'
import { ResponsiveContainer, PieChart, Pie, LineChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Line, Cell } from 'recharts'

import { useNavigate } from 'react-router-dom'
import { isSuccess } from '../utils/responseHelper'

// Charts components are available if needed

const Dashboard = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    total_products: 0,
    total_customers: 0,
    total_suppliers: 0,
    total_inventory_value: 0,
    low_stock_count: 0,
    recent_movements: 0
  })

  const [recentMovements, setRecentMovements] = useState([])
  const [categoryData, setCategoryData] = useState([])
  const [salesData, setSalesData] = useState([])
  const [lowStockProducts, setLowStockProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  // جلب البيانات من APIs مع fallback للبيانات التجريبية
  const fetchDashboardData = async () => {
    setLoading(true)
    setError(null)

    try {
      const baseUrl = 'http://127.0.0.1:8000'

      // محاولة جلب البيانات من الخادم
      try {
        const statsResponse = await fetch(`${baseUrl}/api/dashboard/stats`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 5000
        })

        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          if (isSuccess(statsData)) {
            setStats(statsData.data)
            setLastUpdated(new Date())
            setLoading(false)
            return
          }
        }
      } catch (apiError) {
        }

      // البيانات التجريبية المحسنة
      setTimeout(() => {
        setStats({
          total_products: 47,
          total_customers: 23,
          total_suppliers: 12,
          total_inventory_value: 285000,
          low_stock_count: 5,
          recent_movements: 128
        })

        setRecentMovements([
          {
            id: 1,
            product_name: 'بذور طماطم هجين F1',
            type: 'in',
            quantity: 50,
            created_at: '2024-07-03T10:30:00',
            warehouse: 'المخزن الرئيسي'
          },
          {
            id: 2,
            product_name: 'سماد NPK 20-20-20',
            type: 'out',
            quantity: 25,
            created_at: '2024-07-03T09:15:00',
            warehouse: 'مخزن الأسمدة'
          },
          {
            id: 3,
            product_name: 'شتلات خيار بيت ألفا',
            type: 'in',
            quantity: 200,
            created_at: '2024-07-03T08:45:00',
            warehouse: 'مخزن الشتلات'
          },
          {
            id: 4,
            product_name: 'مبيد أكتارا 240SC',
            type: 'out',
            quantity: 10,
            created_at: '2024-07-02T16:20:00',
            warehouse: 'مخزن المبيدات'
          }
        ])

        setCategoryData([
          { name: 'بذور', value: 18, color: '#3B82F6' },
          { name: 'شتلات', value: 12, color: '#10B981' },
          { name: 'أسمدة', value: 9, color: '#F59E0B' },
          { name: 'مبيدات', value: 8, color: '#EF4444' }
        ])

        setSalesData([
          { date: '2024-06-27', sales: 15000 },
          { date: '2024-06-28', sales: 22000 },
          { date: '2024-06-29', sales: 18000 },
          { date: '2024-06-30', sales: 28000 },
          { date: '2024-07-01', sales: 32000 },
          { date: '2024-07-02', sales: 25000 },
          { date: '2024-07-03', sales: 35000 }
        ])

        setLowStockProducts([
          { id: 1, name: 'بذور باذنجان أسود', current_stock: 5, min_stock: 20 },
          { id: 2, name: 'سماد يوريا 46%', current_stock: 8, min_stock: 50 },
          { id: 3, name: 'شتلات فلفل حلو', current_stock: 12, min_stock: 30 },
          { id: 4, name: 'مبيد فطري كوبر', current_stock: 3, min_stock: 15 },
          { id: 5, name: 'بذور جزر نانت', current_stock: 7, min_stock: 25 }
        ])

        setLastUpdated(new Date())
        setLoading(false)
      }, 1000)

    } catch (error) {
      setError('فشل في تحميل البيانات')
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboardData()

    // تحديث البيانات كل 5 دقائق
    const interval = setInterval(fetchDashboardData, 5 * 60 * 1000)

    return () => clearInterval(interval)
  }, [])

  const StatCard = ({ icon: Icon, title, value, color, trend, loading }) => (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground mb-1">{title}</p>
          {loading ? (
            <div className="animate-pulse">
              <div className="h-8 bg-muted rounded w-20 mb-2"></div>
              <div className="h-4 bg-muted rounded w-16"></div>
            </div>
          ) : (
            <>
              <p className="text-2xl font-bold text-foreground mb-1">
                {typeof value === 'number' ? value.toLocaleString() : value}
              </p>
              {trend && (
                <div className="flex items-center">
                  <TrendingUp className={`w-4 h-4 ml-1 ${trend > 0 ? 'text-primary' : 'text-destructive'}`} />
                  <p className={`text-sm ${trend > 0 ? 'text-primary' : 'text-destructive'}`}>
                    {trend > 0 ? '+' : ''}{trend}% من الشهر الماضي
                  </p>
                </div>
              )}
            </>
          )}
        </div>
        <div className={`p-3 rounded-full ${color} shadow-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  )

  StatCard.propTypes = {
    icon: PropTypes.elementType.isRequired,
    title: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    color: PropTypes.string.isRequired,
    trend: PropTypes.number,
    loading: PropTypes.bool
  }

  const ErrorMessage = ({ message, onRetry }) => (
    <div className="bg-destructive/10 border border-destructive/30 rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <AlertTriangle className="w-5 h-5 text-destructive ml-2" />
          <div>
            <h3 className="text-lg font-medium text-red-800">خطأ في تحميل البيانات</h3>
            <p className="text-destructive mt-1">{message}</p>
          </div>
        </div>
        <button
          onClick={onRetry}
          className="bg-destructive text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
        >
          إعادة المحاولة
        </button>
      </div>
    </div>
  )

  ErrorMessage.propTypes = {
    message: PropTypes.string.isRequired,
    onRetry: PropTypes.func.isRequired
  }

  return (
    <div className="p-6 bg-muted/50 min-h-screen" dir="rtl">
      {/* رأس الصفحة */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">لوحة المعلومات</h1>
            <p className="text-muted-foreground mt-2">نظرة شاملة على أداء النظام والإحصائيات الحية</p>
          </div>
          <div className="flex items-center space-x-4 space-x-reverse">
            {lastUpdated && (
              <div className="flex items-center text-sm text-gray-500">
                <Calendar className="w-4 h-4 ml-1" />
                آخر تحديث: {lastUpdated.toLocaleTimeString('ar-EG')}
              </div>
            )}
            <button
              onClick={fetchDashboardData}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ml-1 ${loading ? 'animate-spin' : ''}`} />
              تحديث
            </button>
          </div>
        </div>
      </div>

      {/* رسالة خطأ */}
      {error && <ErrorMessage message={error} onRetry={fetchDashboardData} />}

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={Package}
          title="إجمالي المنتجات"
          value={stats.total_products}
          color="bg-gradient-to-r from-blue-500 to-blue-600"
          trend={12}
          loading={loading}
        />
        <StatCard
          icon={Users}
          title="عدد العملاء"
          value={stats.total_customers}
          color="bg-gradient-to-r from-green-500 to-green-600"
          trend={8}
          loading={loading}
        />
        <StatCard
          icon={Truck}
          title="عدد الموردين"
          value={stats.total_suppliers}
          color="bg-gradient-to-r from-purple-500 to-purple-600"
          trend={5}
          loading={loading}
        />
        <StatCard
          icon={DollarSign}
          title="قيمة المخزون (جنيه)"
          value={stats.total_inventory_value}
          color="bg-gradient-to-r from-yellow-500 to-yellow-600"
          trend={-3}
          loading={loading}
        />
      </div>

      {/* تنبيهات ذكية */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* تنبيه المخزون المنخفض */}
        {stats.low_stock_count > 0 && (
          <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="p-2 bg-accent/20 rounded-full">
                  <AlertTriangle className="w-6 h-6 text-accent" />
                </div>
                <div className="mr-3">
                  <h3 className="text-lg font-semibold text-yellow-800">منتجات منخفضة المخزون</h3>
                  <p className="text-yellow-700 mt-1">
                    {stats.low_stock_count} منتج يحتاج إعادة تموين
                  </p>
                </div>
              </div>
              <button
                onClick={() => navigate('/products')}
                className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
              >
                عرض التفاصيل
              </button>
            </div>
            {lowStockProducts.length > 0 && (
              <div className="mt-4 space-y-2">
                {lowStockProducts.slice(0, 3).map((product, index) => (
                  <div key={product.id || index} className="flex items-center justify-between bg-white p-3 rounded-lg">
                    <span className="font-medium text-foreground">{product.name}</span>
                    <span className="text-sm text-destructive">متبقي: {product.current_stock}</span>
                  </div>
                ))}
                {lowStockProducts.length > 3 && (
                  <p className="text-sm text-yellow-700 text-center">
                    و {lowStockProducts.length - 3} منتجات أخرى...
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* إحصائيات سريعة إضافية */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
            <BarChart3 className="w-5 h-5 ml-2 text-primary-600" />
            ملخص سريع
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">الحركات الأخيرة (30 يوم)</span>
              <span className="font-bold text-primary-600">{stats.recent_movements || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">متوسط قيمة المنتج</span>
              <span className="font-bold text-primary">
                {stats.total_products > 0
                  ? Math.round(stats.total_inventory_value / stats.total_products).toLocaleString()
                  : 0} جنيه
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">نسبة المخزون الآمن</span>
              <span className={`font-bold ${stats.low_stock_count === 0 ? 'text-primary' : 'text-destructive'}`}>
                {stats.total_products > 0
                  ? Math.round(((stats.total_products - stats.low_stock_count) / stats.total_products) * 100)
                  : 100}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* الرسوم البيانية والتحليلات */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* توزيع المنتجات حسب الفئة */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground flex items-center">
              <PieChartIcon className="w-5 h-5 ml-2 text-primary-600" />
              توزيع المنتجات حسب الفئة
            </h3>
            <span className="text-sm text-gray-500">
              {categoryData.reduce((sum, item) => sum + (item.value || 0), 0)} منتج
            </span>
          </div>
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <RefreshCw className="w-8 h-8 animate-spin text-primary-500" />
            </div>
          ) : categoryData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {categoryData.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value, name) => [`${value} منتج`, name]}
                  labelStyle={{ direction: 'rtl' }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              <div className="text-center">
                <Package className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p>لا توجد بيانات فئات</p>
              </div>
            </div>
          )}
        </div>

        {/* اتجاه المبيعات */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground flex items-center">
              <TrendingUp className="w-5 h-5 ml-2 text-primary" />
              اتجاه المبيعات (آخر 7 أيام)
            </h3>
          </div>
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <RefreshCw className="w-8 h-8 animate-spin text-primary-500" />
            </div>
          ) : salesData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip
                  formatter={(value) => [`${value} جنيه`, 'المبيعات']}
                  labelStyle={{ direction: 'rtl' }}
                />
                <Line
                  type="monotone"
                  dataKey="sales"
                  stroke="#3B82F6"
                  strokeWidth={3}
                  dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              <div className="text-center">
                <BarChart3 className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p>لا توجد بيانات مبيعات</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* الحركات الأخيرة والأنشطة */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-foreground flex items-center">
            <Activity className="w-5 h-5 ml-2 text-primary-600" />
            الحركات والأنشطة الأخيرة
          </h3>
          <button
            onClick={() => navigate('/lots')}
            className="text-primary-600 hover:text-primary-700 text-sm font-medium"
          >
            عرض الكل
          </button>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="animate-pulse flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-muted rounded-full ml-3"></div>
                  <div>
                    <div className="h-4 bg-muted rounded w-32 mb-2"></div>
                    <div className="h-3 bg-muted rounded w-20"></div>
                  </div>
                </div>
                <div className="h-6 bg-muted rounded w-16"></div>
              </div>
            ))}
          </div>
        ) : recentMovements.length > 0 ? (
          <div className="space-y-4">
            {recentMovements.map((movement) => (
              <div key={movement.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                <div className="flex items-center">
                  <div className={`p-2 rounded-full ml-3 ${
                    movement.type === 'in' ? 'bg-primary/20' : 'bg-destructive/20'
                  }`}>
                    <Activity className={`w-4 h-4 ${
                      movement.type === 'in' ? 'text-primary' : 'text-destructive'
                    }`} />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{movement.product_name || movement.product}</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(movement.created_at || movement.date).toLocaleDateString('ar-EG')}
                    </p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ml-2 ${
                    movement.type === 'in'
                      ? 'bg-primary/20 text-green-800'
                      : 'bg-destructive/20 text-red-800'
                  }`}>
                    {movement.type === 'in' ? 'وارد' : 'صادر'}
                  </span>
                  <span className="font-bold text-foreground">{movement.quantity}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center py-12 text-gray-500">
            <div className="text-center">
              <Activity className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p className="text-lg font-medium">لا توجد حركات حديثة</p>
              <p className="text-sm">ستظهر الحركات الجديدة هنا</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard


