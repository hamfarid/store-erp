import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, PieChart, RefreshCw,
  AlertTriangle, Truck
} from 'lucide-react'
import DataTable from './ui/DataTable'
import { Notification, LoadingSpinner, Modal } from './ui/Notification'
import SearchFilter from './ui/SearchFilter'

const ReportsSystem = () => {
  const [activeCategory, setActiveCategory] = useState('sales')
  const [reports, setReports] = useState([])
  const [reportData, setReportData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showReportModal, setShowReportModal] = useState(false)
  const [selectedReport, setSelectedReport] = useState(null)
  const [dateRange, setDateRange] = useState({
    start: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  })

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadReports()
  }, [activeCategory])

  const loadReports = async () => {
    setLoading(true)
    try {
      // محاولة جلب التقارير من API
      const response = await fetch(`http://172.16.16.27:8000/reports/${activeCategory}`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setReports(data.reports)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      loadMockReports()
    } finally {
      setLoading(false)
    }
  }

  const loadMockReports = () => {
    const mockReports = {
      sales: [
        {
          id: 1,
          name: 'تقرير المبيعات اليومية',
          description: 'تقرير تفصيلي للمبيعات اليومية مع تحليل الأداء',
          type: 'daily_sales',
          category: 'sales',
          icon: TrendingUp,
          color: 'bg-primary/100',
          data: {
            total_sales: 125000,
            total_invoices: 45,
            average_invoice: 2777.78,
            top_products: ['بذور طماطم', 'سماد NPK', 'مبيد أكتارا'],
            growth_rate: 12.5
          }
        },
        {
          id: 2,
          name: 'تقرير المبيعات الشهرية',
          description: 'تحليل شامل للمبيعات الشهرية والاتجاهات',
          type: 'monthly_sales',
          category: 'sales',
          icon: BarChart3,
          color: 'bg-primary-500',
          data: {
            total_sales: 3500000,
            total_invoices: 1250,
            best_month: 'يوليو',
            growth_rate: 18.3
          }
        },
        {
          id: 3,
          name: 'تقرير أداء مهندسي المبيعات',
          description: 'تقييم أداء فريق المبيعات والعمولات',
          type: 'sales_performance',
          category: 'sales',
          icon: Users,
          color: 'bg-purple-500',
          data: {
            top_engineer: 'أحمد محمد',
            total_commission: 45000,
            engineers_count: 8
          }
        }
      ],
      inventory: [
        {
          id: 4,
          name: 'تقرير حالة المخزون',
          description: 'تقرير شامل لحالة المخزون والكميات المتاحة',
          type: 'stock_status',
          category: 'inventory',
          icon: Package,
          color: 'bg-accent/100',
          data: {
            total_products: 247,
            low_stock_items: 23,
            out_of_stock: 5,
            total_value: 2850000
          }
        },
        {
          id: 5,
          name: 'تقرير حركات المخزون',
          description: 'تتبع جميع حركات المخزون (دخول، خروج، تحويل)',
          type: 'stock_movements',
          category: 'inventory',
          icon: TrendingUp,
          color: 'bg-secondary/100',
          data: {
            total_movements: 1850,
            inbound: 750,
            outbound: 980,
            transfers: 120
          }
        },
        {
          id: 6,
          name: 'تقرير اللوطات منتهية الصلاحية',
          description: 'تقرير اللوطات المنتهية والقاربة على الانتهاء',
          type: 'expiry_report',
          category: 'inventory',
          icon: AlertTriangle,
          color: 'bg-destructive/100',
          data: {
            expired_lots: 12,
            expiring_soon: 28,
            total_loss: 85000
          }
        }
      ],
      financial: [
        {
          id: 7,
          name: 'تقرير الأرباح والخسائر',
          description: 'تحليل مالي شامل للأرباح والخسائر',
          type: 'profit_loss',
          category: 'financial',
          icon: DollarSign,
          color: 'bg-primary',
          data: {
            total_revenue: 3500000,
            total_costs: 2100000,
            net_profit: 1400000,
            profit_margin: 40
          }
        },
        {
          id: 8,
          name: 'تقرير التدفق النقدي',
          description: 'تتبع التدفقات النقدية الداخلة والخارجة',
          type: 'cash_flow',
          category: 'financial',
          icon: TrendingUp,
          color: 'bg-primary-600',
          data: {
            cash_inflow: 2800000,
            cash_outflow: 2200000,
            net_cash_flow: 600000,
            cash_balance: 1250000
          }
        },
        {
          id: 9,
          name: 'تقرير أرصدة العملاء',
          description: 'تقرير مستحقات العملاء والديون',
          type: 'customer_balances',
          category: 'financial',
          icon: Users,
          color: 'bg-yellow-600',
          data: {
            total_receivables: 850000,
            overdue_amount: 125000,
            customers_count: 156
          }
        }
      ]
    }
    
    setReports(mockReports[activeCategory] || [])
  }

  // فئات التقارير
  const reportCategories = [
    {
      id: 'sales',
      label: 'تقارير المبيعات',
      icon: TrendingUp,
      color: 'text-primary',
      description: 'تقارير المبيعات والعملاء'
    },
    {
      id: 'inventory',
      label: 'تقارير المخزون',
      icon: Package,
      color: 'text-primary-600',
      description: 'تقارير المخزون واللوطات'
    },
    {
      id: 'financial',
      label: 'التقارير المالية',
      icon: DollarSign,
      color: 'text-purple-600',
      description: 'التقارير المالية والمحاسبية'
    },
    {
      id: 'purchases',
      label: 'تقارير المشتريات',
      icon: Truck,
      color: 'text-accent',
      description: 'تقارير المشتريات والموردين'
    },
    {
      id: 'analytics',
      label: 'التحليلات المتقدمة',
      icon: BarChart3,
      color: 'text-indigo-600',
      description: 'تحليلات وإحصائيات متقدمة'
    }
  ]

  // معالجة عرض التقرير
  const handleViewReport = async (report) => {
    setSelectedReport(report)
    setLoading(true)
    
    try {
      // محاولة جلب بيانات التقرير من API
      const response = await fetch(`http://172.16.16.27:8000/reports/${report.type}?start=${dateRange.start}&end=${dateRange.end}`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setReportData(data.data)
        } else {
          throw new Error(data.message)
        }
      } else {
        throw new Error('فشل في جلب بيانات التقرير')
      }
    } catch (error) {
      // استخدام البيانات التجريبية
      setReportData(report.data)
    } finally {
      setLoading(false)
      setShowReportModal(true)
    }
  }

  // معالجة تصدير التقرير
  const handleExportReport = async (report, format) => {
    try {
      const response = await fetch(`http://172.16.16.27:8000/reports/${report.type}/export?format=${format}&start=${dateRange.start}&end=${dateRange.end}`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${report.name}_${new Date().toISOString().split('T')[0]}.${format}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        throw new Error('فشل في تصدير التقرير')
      }
    } catch (error) {
      // محاكاة التصدير
      }
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground flex items-center">
              <BarChart3 className="w-6 h-6 ml-2 text-primary-600" />
              نظام التقارير الشامل
            </h1>
            <p className="text-muted-foreground mt-1">تقارير وتحليلات شاملة لجميع أجزاء النظام</p>
          </div>
          
          <div className="flex items-center space-x-3 space-x-reverse">
            {/* Date Range Selector */}
            <div className="flex items-center space-x-2 space-x-reverse bg-white border border-border rounded-lg px-3 py-2">
              <Calendar className="w-4 h-4 text-gray-400" />
              <input
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange(prev => ({ ...prev, start: e.target.value }))}
                className="border-none outline-none text-sm"
              />
              <span className="text-gray-400">إلى</span>
              <input
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange(prev => ({ ...prev, end: e.target.value }))}
                className="border-none outline-none text-sm"
              />
            </div>
            
            <button
              onClick={loadReports}
              className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4 ml-1" />
              تحديث
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Notification
          type="error"
          title="خطأ في تحميل التقارير"
          message={error}
          className="mb-6"
          onDismiss={() => setError(null)}
        />
      )}

      {/* Report Categories */}
      <div className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {reportCategories.map((category) => {
            const Icon = category.icon
            return (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  activeCategory === category.id
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-border bg-white hover:border-border hover:bg-muted/50'
                }`}
              >
                <div className="flex flex-col items-center text-center">
                  <Icon className={`w-8 h-8 mb-2 ${
                    activeCategory === category.id ? 'text-primary-600' : category.color
                  }`} />
                  <h3 className={`font-medium ${
                    activeCategory === category.id ? 'text-primary-900' : 'text-foreground'
                  }`}>
                    {category.label}
                  </h3>
                  <p className="text-xs text-muted-foreground mt-1">{category.description}</p>
                </div>
              </button>
            )
          })}
        </div>
      </div>

      {/* Reports Grid */}
      {loading ? (
        <LoadingSpinner size="lg" text="جاري تحميل التقارير..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => {
            const Icon = report.icon
            return (
              <div
                key={report.id}
                className="bg-white rounded-lg shadow-sm border border-border overflow-hidden hover:shadow-md transition-shadow"
              >
                {/* Report Header */}
                <div className={`${report.color} p-4 text-white`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Icon className="w-6 h-6 ml-2" />
                      <h3 className="font-semibold">{report.name}</h3>
                    </div>
                  </div>
                </div>

                {/* Report Content */}
                <div className="p-4">
                  <p className="text-muted-foreground text-sm mb-4">{report.description}</p>
                  
                  {/* Quick Stats */}
                  {report.data && (
                    <div className="space-y-2 mb-4">
                      {Object.entries(report.data).slice(0, 3).map(([key, value]) => (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-muted-foreground capitalize">
                            {key.replace(/_/g, ' ')}:
                          </span>
                          <span className="font-medium">
                            {typeof value === 'number' ? value.toLocaleString() : value}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                    <button
                      onClick={() => handleViewReport(report)}
                      className="flex items-center px-3 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
                    >
                      <Eye className="w-4 h-4 ml-1" />
                      عرض
                    </button>
                    
                    <div className="flex items-center space-x-1 space-x-reverse">
                      <button
                        onClick={() => handleExportReport(report, 'pdf')}
                        className="p-2 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
                        title="تصدير PDF"
                      >
                        <FileText className="w-4 h-4" />
                      </button>
                      
                      <button
                        onClick={() => handleExportReport(report, 'xlsx')}
                        className="p-2 text-muted-foreground hover:text-primary hover:bg-primary/10 rounded-lg transition-colors"
                        title="تصدير Excel"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      
                      <button
                        onClick={() => console.log('Print report')}
                        className="p-2 text-muted-foreground hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                        title="طباعة"
                      >
                        <Printer className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Report Details Modal */}
      <Modal
        isOpen={showReportModal}
        onClose={() => setShowReportModal(false)}
        title={selectedReport?.name}
        size="xl"
      >
        {selectedReport && reportData && (
          <div className="space-y-6">
            {/* Report Summary */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <h3 className="font-semibold text-foreground mb-3">ملخص التقرير</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.entries(reportData).map(([key, value]) => (
                  <div key={key} className="text-center">
                    <p className="text-sm text-muted-foreground capitalize">
                      {key.replace(/_/g, ' ')}
                    </p>
                    <p className="text-lg font-bold text-foreground">
                      {typeof value === 'number' ? value.toLocaleString() : value}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Chart Placeholder */}
            <div className="bg-muted rounded-lg p-8 text-center">
              <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-muted-foreground">الرسوم البيانية قريباً...</p>
            </div>

            {/* Export Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-border">
              <div className="text-sm text-muted-foreground">
                تاريخ التقرير: {dateRange.start} إلى {dateRange.end}
              </div>
              
              <div className="flex items-center space-x-2 space-x-reverse">
                <button
                  onClick={() => handleExportReport(selectedReport, 'pdf')}
                  className="flex items-center px-4 py-2 bg-destructive text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  <FileText className="w-4 h-4 ml-1" />
                  تصدير PDF
                </button>
                
                <button
                  onClick={() => handleExportReport(selectedReport, 'xlsx')}
                  className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Download className="w-4 h-4 ml-1" />
                  تصدير Excel
                </button>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}

export default ReportsSystem

