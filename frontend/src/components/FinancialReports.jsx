import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, RefreshCw,
  PieChart
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const FinancialReports = () => {
  const [loading, setLoading] = useState(false)
  const [reportData, setReportData] = useState({
    summary: {
      totalRevenue: 0,
      totalExpenses: 0,
      netProfit: 0,
      profitMargin: 0
    },
    monthlyData: [],
    categoryBreakdown: [],
    topProducts: []
  })

  const [filters, setFilters] = useState({
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0],
    reportType: 'summary',
    currency: 'EGP'
  })

  const [activeTab, setActiveTab] = useState('summary')

  useEffect(() => {
    loadFinancialReports()
  }, [filters])

  const loadFinancialReports = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/reports/financial', { params: filters })
      if (response.success) {
        setReportData(response.data)
      } else {
        // Use mock data if API not available
        setReportData({
          summary: {
            totalRevenue: 125000,
            totalExpenses: 85000,
            netProfit: 40000,
            profitMargin: 32
          },
          monthlyData: [
            { month: 'يناير', revenue: 15000, expenses: 10000, profit: 5000 },
            { month: 'فبراير', revenue: 18000, expenses: 12000, profit: 6000 },
            { month: 'مارس', revenue: 22000, expenses: 15000, profit: 7000 },
            { month: 'أبريل', revenue: 20000, expenses: 13000, profit: 7000 },
            { month: 'مايو', revenue: 25000, expenses: 17000, profit: 8000 },
            { month: 'يونيو', revenue: 25000, expenses: 18000, profit: 7000 }
          ],
          categoryBreakdown: [
            { category: 'البذور', revenue: 45000, percentage: 36 },
            { category: 'الأسمدة', revenue: 35000, percentage: 28 },
            { category: 'المبيدات', revenue: 25000, percentage: 20 },
            { category: 'أدوات الزراعة', revenue: 20000, percentage: 16 }
          ],
          topProducts: [
            { name: 'بذور طماطم هجين', sales: 15000, quantity: 500 },
            { name: 'سماد NPK', sales: 12000, quantity: 300 },
            { name: 'مبيد حشري', sales: 10000, quantity: 200 },
            { name: 'بذور خيار', sales: 8000, quantity: 250 }
          ]
        })
      }
    } catch (error) {
      toast.error('خطأ في تحميل التقارير المالية')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const exportReport = async (format) => {
    try {
      const response = await ApiService.get(`/api/reports/financial/export`, {
        params: { ...filters, format }
      })
      
      if (response.success) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `financial-report-${new Date().toISOString().split('T')[0]}.${format}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        toast.success('تم تصدير التقرير بنجاح')
      }
    } catch (error) {
      toast.error('خطأ في تصدير التقرير')
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-EG', {
      style: 'currency',
      currency: filters.currency
    }).format(amount)
  }

  if (loading) {
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
            <BarChart3 className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">التقارير المالية</h1>
              <p className="text-muted-foreground">تحليل شامل للأداء المالي والأرباح</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={() => loadFinancialReports()}
              className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50"
            >
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </button>
            
            <button
              onClick={() => exportReport('pdf')}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              <Download className="w-4 h-4 ml-2" />
              تصدير PDF
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center mb-4">
          <Filter className="w-5 h-5 text-muted-foreground ml-2" />
          <h2 className="text-lg font-semibold text-foreground">فلاتر التقرير</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              من تاريخ
            </label>
            <input
              type="date"
              value={filters.startDate}
              onChange={(e) => handleFilterChange('startDate', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              إلى تاريخ
            </label>
            <input
              type="date"
              value={filters.endDate}
              onChange={(e) => handleFilterChange('endDate', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              نوع التقرير
            </label>
            <select
              value={filters.reportType}
              onChange={(e) => handleFilterChange('reportType', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="summary">ملخص عام</option>
              <option value="detailed">تفصيلي</option>
              <option value="comparative">مقارن</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              العملة
            </label>
            <select
              value={filters.currency}
              onChange={(e) => handleFilterChange('currency', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="EGP">جنيه مصري</option>
              <option value="USD">دولار أمريكي</option>
              <option value="EUR">يورو</option>
            </select>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary/20 rounded-lg">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الإيرادات</p>
              <p className="text-2xl font-bold text-foreground">
                {formatCurrency(reportData.summary.totalRevenue)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-destructive/20 rounded-lg">
              <TrendingDown className="w-6 h-6 text-destructive" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المصروفات</p>
              <p className="text-2xl font-bold text-foreground">
                {formatCurrency(reportData.summary.totalExpenses)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <DollarSign className="w-6 h-6 text-primary-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">صافي الربح</p>
              <p className="text-2xl font-bold text-foreground">
                {formatCurrency(reportData.summary.netProfit)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <PieChart className="w-6 h-6 text-purple-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">هامش الربح</p>
              <p className="text-2xl font-bold text-foreground">
                {reportData.summary.profitMargin}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'summary', name: 'الملخص', icon: BarChart3 },
              { id: 'monthly', name: 'التحليل الشهري', icon: Calendar },
              { id: 'categories', name: 'تحليل الفئات', icon: PieChart },
              { id: 'products', name: 'أفضل المنتجات', icon: TrendingUp }
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
          {activeTab === 'summary' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">الملخص المالي</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-muted/50 rounded-lg">
                  <span className="font-medium">إجمالي الإيرادات</span>
                  <span className="text-primary font-bold">{formatCurrency(reportData.summary.totalRevenue)}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-muted/50 rounded-lg">
                  <span className="font-medium">إجمالي المصروفات</span>
                  <span className="text-destructive font-bold">{formatCurrency(reportData.summary.totalExpenses)}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-primary-50 rounded-lg border-2 border-primary-200">
                  <span className="font-bold">صافي الربح</span>
                  <span className="text-primary-600 font-bold text-xl">{formatCurrency(reportData.summary.netProfit)}</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'monthly' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">التحليل الشهري</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الشهر</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإيرادات</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المصروفات</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الربح</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {reportData.monthlyData.map((month, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">{month.month}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-primary">{formatCurrency(month.revenue)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-destructive">{formatCurrency(month.expenses)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-primary-600 font-medium">{formatCurrency(month.profit)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'categories' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">تحليل الفئات</h3>
              <div className="space-y-4">
                {reportData.categoryBreakdown.map((category, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-primary-600 rounded-full ml-3"></div>
                      <span className="font-medium">{category.category}</span>
                    </div>
                    <div className="text-left">
                      <div className="font-bold text-foreground">{formatCurrency(category.revenue)}</div>
                      <div className="text-sm text-gray-500">{category.percentage}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'products' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">أفضل المنتجات مبيعاً</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المنتج</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المبيعات</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الكمية</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {reportData.topProducts.map((product, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">{product.name}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-primary">{formatCurrency(product.sales)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{product.quantity}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default FinancialReports

