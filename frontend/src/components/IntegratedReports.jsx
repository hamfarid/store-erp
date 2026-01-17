import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  AlertTriangle, Clock, Building
} from 'lucide-react'
import { reportsAPI } from '../services/api'
import { useToast } from './common/EnhancedToast'
import LoadingSpinner from './common/LoadingSpinner'
import { ExportButton, PrintButton } from './common/EnhancedButton'
import { useProgress } from './common/ProgressBar'

const IntegratedReports = () => {
  const [activeReport, setActiveReport] = useState('comprehensive')
  const [reportData, setReportData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    date_from: '',
    date_to: '',
    warehouse_id: '',
    category_id: '',
    product_id: ''
  })

  const _toast = useToast()
  const { startOperation: _startOperation, updateOperation: _updateOperation, completeOperation: _completeOperation } = useProgress()

  const reportTypes = [
    {
      id: 'comprehensive',
      name: 'التقرير الشامل',
      description: 'تقرير متكامل يشمل المخزون والمحاسبة والمبيعات',
      icon: BarChart3,
      color: 'blue'
    },
    {
      id: 'stock_valuation',
      name: 'تقييم المخزون',
      description: 'تقرير تقييم المخزون بالتكلفة والقيمة السوقية',
      icon: DollarSign,
      color: 'green'
    },
    {
      id: 'low_stock',
      name: 'المخزون المنخفض',
      description: 'تقرير المنتجات التي تحتاج إعادة طلب',
      icon: AlertTriangle,
      color: 'orange'
    },
    {
      id: 'expiry_analysis',
      name: 'تحليل انتهاء الصلاحية',
      description: 'تقرير اللوط قريبة الانتهاء والمنتهية الصلاحية',
      icon: Clock,
      color: 'red'
    },
    {
      id: 'movement_analysis',
      name: 'تحليل الحركات',
      description: 'تقرير تحليل حركات المخزون والاتجاهات',
      icon: TrendingUp,
      color: 'purple'
    },
    {
      id: 'warehouse_performance',
      name: 'أداء المخازن',
      description: 'تقرير أداء المخازن ومعدلات الاستخدام',
      icon: Building,
      color: 'indigo'
    }
  ]

  // بيانات تجريبية للتقرير الشامل
  const mockComprehensiveData = {
    summary: {
      total_products: 150,
      total_quantity: 5000.0,
      total_value: 125000.0,
      low_stock_products: 5,
      expiring_lots: 3,
      inactive_products: 10,
      last_updated: new Date().toISOString()
    },
    inventory_by_category: [
      { category: 'بذور', products_count: 50, total_quantity: 2000.0, total_value: 60000.0, percentage: 48.0 },
      { category: 'أسمدة', products_count: 30, total_quantity: 1500.0, total_value: 45000.0, percentage: 36.0 },
      { category: 'مبيدات', products_count: 20, total_quantity: 800.0, total_value: 20000.0, percentage: 16.0 }
    ],
    inventory_by_warehouse: [
      { warehouse_name: 'المخزن الرئيسي', products_count: 100, total_value: 80000.0, utilization: 75.0 },
      { warehouse_name: 'مخزن الفرع الأول', products_count: 50, total_value: 45000.0, utilization: 60.0 }
    ],
    monthly_trends: [
      { month: 'يناير', value: 120000, movements: 45 },
      { month: 'فبراير', value: 115000, movements: 38 },
      { month: 'مارس', value: 125000, movements: 52 },
      { month: 'أبريل', value: 130000, movements: 48 },
      { month: 'مايو', value: 128000, movements: 55 },
      { month: 'يونيو', value: 125000, movements: 50 }
    ],
    accounting_integration: {
      inventory_account_balance: 124850.0,
      variance: 150.0,
      variance_percentage: 0.12,
      last_reconciliation: '2024-11-30'
    },
    alerts: [
      { type: 'low_stock', message: '5 منتجات تحتاج إعادة طلب', urgency: 'high' },
      { type: 'expiring_lots', message: '3 لوط قريبة الانتهاء', urgency: 'medium' },
      { type: 'accounting_variance', message: 'فرق 150 ج.م مع المحاسبة', urgency: 'low' }
    ]
  }

  useEffect(() => {
    loadReportData()
  }, [activeReport, filters])

  const loadReportData = async () => {
    setLoading(true)
    try {
      // محاكاة تحميل البيانات
      setTimeout(() => {
        if (activeReport === 'comprehensive') {
          setReportData(mockComprehensiveData)
        } else {
          // محاكاة بيانات التقارير الأخرى
          setReportData({
            summary: { message: `بيانات تقرير ${reportTypes.find(r => r.id === activeReport)?.name}` }
          })
        }
        setLoading(false)
      }, 1000)
    } catch (error) {
      setLoading(false)
    }
  }

  const handleExportReport = async (format) => {
    try {
      await reportsAPI.exportReport(activeReport, format, filters)
    } catch (error) {
      }
  }

  const getReportColor = (color) => {
    const colors = {
      blue: 'bg-primary-100 text-primary-800 border-primary-200',
      green: 'bg-primary/20 text-green-800 border-primary/30',
      orange: 'bg-accent/20 text-orange-800 border-orange-200',
      red: 'bg-destructive/20 text-red-800 border-destructive/30',
      purple: 'bg-purple-100 text-purple-800 border-purple-200',
      indigo: 'bg-secondary/20 text-indigo-800 border-indigo-200'
    }
    return colors[color] || colors.blue
  }

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#6366F1']

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">التقارير المتكاملة</h1>
          <p className="text-muted-foreground">تقارير شاملة ومتكاملة للمخزون والمحاسبة والمبيعات</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleExportReport('pdf')}
            className="bg-destructive text-white px-4 py-2 rounded-lg hover:bg-red-700 flex items-center"
          >
            <FileText className="w-4 h-4 ml-2" />
            PDF
          </button>
          <button
            onClick={() => handleExportReport('excel')}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center"
          >
            <Download className="w-4 h-4 ml-2" />
            Excel
          </button>
          <button
            onClick={() => window.print()}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center"
          >
            <Printer className="w-4 h-4 ml-2" />
            طباعة
          </button>
        </div>
      </div>

      {/* أنواع التقارير */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {reportTypes.map((report) => (
          <div
            key={report.id}
            onClick={() => setActiveReport(report.id)}
            className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
              activeReport === report.id
                ? getReportColor(report.color)
                : 'bg-white border-border hover:border-border'
            }`}
          >
            <div className="flex items-center mb-2">
              <report.icon className="w-6 h-6 ml-2" />
              <h3 className="font-medium">{report.name}</h3>
            </div>
            <p className="text-sm opacity-75">{report.description}</p>
          </div>
        ))}
      </div>

      {/* فلاتر التقرير */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="flex items-center mb-4">
          <Filter className="w-5 h-5 ml-2 text-muted-foreground" />
          <h3 className="font-medium text-foreground">فلاتر التقرير</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => setFilters({...filters, date_from: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="من تاريخ"
          />
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => setFilters({...filters, date_to: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="إلى تاريخ"
          />
          <select
            value={filters.warehouse_id}
            onChange={(e) => setFilters({...filters, warehouse_id: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">جميع المخازن</option>
            <option value="1">المخزن الرئيسي</option>
            <option value="2">مخزن الفرع الأول</option>
          </select>
          <select
            value={filters.category_id}
            onChange={(e) => setFilters({...filters, category_id: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">جميع الفئات</option>
            <option value="1">بذور</option>
            <option value="2">أسمدة</option>
            <option value="3">مبيدات</option>
          </select>
          <button
            onClick={loadReportData}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 flex items-center justify-center"
          >
            <BarChart3 className="w-4 h-4 ml-2" />
            تحديث التقرير
          </button>
        </div>
      </div>

      {/* محتوى التقرير */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <span className="mr-3 text-muted-foreground">جاري تحميل التقرير...</span>
        </div>
      ) : (
        <div className="space-y-6">
          {activeReport === 'comprehensive' && reportData && (
            <>
              {/* ملخص التقرير */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-sm border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">إجمالي المنتجات</p>
                      <p className="text-2xl font-bold text-foreground">{reportData.summary.total_products}</p>
                    </div>
                    <Package className="w-8 h-8 text-primary-600" />
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg shadow-sm border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">قيمة المخزون</p>
                      <p className="text-2xl font-bold text-primary">
                        {reportData.summary.total_value.toLocaleString()} ج.م
                      </p>
                    </div>
                    <DollarSign className="w-8 h-8 text-primary" />
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg shadow-sm border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">مخزون منخفض</p>
                      <p className="text-2xl font-bold text-accent">{reportData.summary.low_stock_products}</p>
                    </div>
                    <AlertTriangle className="w-8 h-8 text-accent" />
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg shadow-sm border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">لوط قريبة الانتهاء</p>
                      <p className="text-2xl font-bold text-destructive">{reportData.summary.expiring_lots}</p>
                    </div>
                    <Clock className="w-8 h-8 text-destructive" />
                  </div>
                </div>
              </div>

              {/* الرسوم البيانية */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* توزيع المخزون حسب الفئة */}
                <div className="bg-white p-6 rounded-lg shadow-sm border">
                  <h3 className="text-lg font-semibold mb-4">توزيع المخزون حسب الفئة</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <RechartsPieChart>
                      <Pie
                        data={reportData.inventory_by_category}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ category, percentage }) => `${category}: ${percentage}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="percentage"
                      >
                        {reportData.inventory_by_category.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value}%`, 'النسبة']} />
                    </RechartsPieChart>
                  </ResponsiveContainer>
                </div>

                {/* اتجاهات المخزون الشهرية */}
                <div className="bg-white p-6 rounded-lg shadow-sm border">
                  <h3 className="text-lg font-semibold mb-4">اتجاهات قيمة المخزون</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={reportData.monthly_trends}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`${value.toLocaleString()} ج.م`, 'القيمة']} />
                      <Area type="monotone" dataKey="value" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* أداء المخازن */}
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h3 className="text-lg font-semibold mb-4">أداء المخازن</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={reportData.inventory_by_warehouse}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="warehouse_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="utilization" fill="#10B981" name="نسبة الاستخدام %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* التنبيهات والتوصيات */}
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h3 className="text-lg font-semibold mb-4">التنبيهات والتوصيات</h3>
                <div className="space-y-3">
                  {reportData.alerts.map((alert, index) => (
                    <div
                      key={index}
                      className={`p-3 rounded-lg border-r-4 ${
                        alert.urgency === 'high' ? 'bg-destructive/10 border-red-500' :
                        alert.urgency === 'medium' ? 'bg-accent/10 border-yellow-500' :
                        'bg-primary-50 border-primary-500'
                      }`}
                    >
                      <div className="flex items-center">
                        {alert.urgency === 'high' ? (
                          <AlertTriangle className="w-5 h-5 text-destructive ml-2" />
                        ) : alert.urgency === 'medium' ? (
                          <Clock className="w-5 h-5 text-accent ml-2" />
                        ) : (
                          <CheckCircle className="w-5 h-5 text-primary-600 ml-2" />
                        )}
                        <span className="font-medium">{alert.message}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* التقارير الأخرى */}
          {activeReport !== 'comprehensive' && reportData && (
            <div className="bg-white p-6 rounded-lg shadow-sm border text-center">
              <div className="text-gray-500 mb-4">
                <FileText className="w-16 h-16 mx-auto mb-2" />
                <h3 className="text-lg font-medium">
                  {reportTypes.find(r => r.id === activeReport)?.name}
                </h3>
                <p className="text-sm mt-2">هذا التقرير قيد التطوير</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default IntegratedReports

