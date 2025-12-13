import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, TrendingDown, PieChart, RefreshCw
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import ApiService from '../services/ApiService'

const ProfitLoss = () => {
  const [loading, setLoading] = useState(false)
  const [plData, setPLData] = useState({
    revenue: {
      salesRevenue: 0,
      otherRevenue: 0,
      totalRevenue: 0
    },
    costOfGoodsSold: {
      directMaterials: 0,
      directLabor: 0,
      manufacturingOverhead: 0,
      totalCOGS: 0
    },
    grossProfit: 0,
    operatingExpenses: {
      salariesAndWages: 0,
      rent: 0,
      utilities: 0,
      marketing: 0,
      insurance: 0,
      depreciation: 0,
      otherExpenses: 0,
      totalOperatingExpenses: 0
    },
    operatingIncome: 0,
    otherIncomeExpenses: {
      interestIncome: 0,
      interestExpense: 0,
      otherIncome: 0,
      otherExpenses: 0,
      netOtherIncomeExpenses: 0
    },
    netIncomeBeforeTax: 0,
    incomeTax: 0,
    netIncome: 0
  })

  const [filters, setFilters] = useState({
    startDate: new Date(new Date().getFullYear(), 0, 1).toISOString().split('T')[0], // Start of year
    endDate: new Date().toISOString().split('T')[0],
    period: 'monthly',
    currency: 'EGP'
  })

  const [_comparisonData, _setComparisonData] = useState(null)
  const [showComparison, setShowComparison] = useState(false)

  useEffect(() => {
    loadProfitLossData()
  }, [filters])

  const loadProfitLossData = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/reports/profit-loss', { params: filters })
      if (response.success) {
        setPLData(response.data)
      } else {
        // Use mock data if API not available
        setPLData({
          revenue: {
            salesRevenue: 150000,
            otherRevenue: 5000,
            totalRevenue: 155000
          },
          costOfGoodsSold: {
            directMaterials: 60000,
            directLabor: 20000,
            manufacturingOverhead: 10000,
            totalCOGS: 90000
          },
          grossProfit: 65000,
          operatingExpenses: {
            salariesAndWages: 25000,
            rent: 8000,
            utilities: 3000,
            marketing: 5000,
            insurance: 2000,
            depreciation: 4000,
            otherExpenses: 3000,
            totalOperatingExpenses: 50000
          },
          operatingIncome: 15000,
          otherIncomeExpenses: {
            interestIncome: 1000,
            interestExpense: 2000,
            otherIncome: 500,
            otherExpenses: 1500,
            netOtherIncomeExpenses: -2000
          },
          netIncomeBeforeTax: 13000,
          incomeTax: 3000,
          netIncome: 10000
        })
      }
    } catch (error) {
      toast.error('خطأ في تحميل بيانات الأرباح والخسائر')
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
      const response = await ApiService.get(`/api/reports/profit-loss/export`, {
        params: { ...filters, format }
      })
      
      if (response.success) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `profit-loss-${new Date().toISOString().split('T')[0]}.${format}`)
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

  const calculatePercentage = (amount, total) => {
    if (total === 0) return 0
    return ((amount / total) * 100).toFixed(1)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Calculator className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">قائمة الأرباح والخسائر</h1>
              <p className="text-muted-foreground">تحليل مفصل للإيرادات والمصروفات والأرباح</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={() => setShowComparison(!showComparison)}
              className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50"
            >
              <Eye className="w-4 h-4 ml-2" />
              {showComparison ? 'إخفاء المقارنة' : 'عرض المقارنة'}
            </button>
            
            <button
              onClick={() => loadProfitLossData()}
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
              الفترة
            </label>
            <select
              value={filters.period}
              onChange={(e) => handleFilterChange('period', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="monthly">شهري</option>
              <option value="quarterly">ربع سنوي</option>
              <option value="yearly">سنوي</option>
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
                {formatCurrency(plData.revenue.totalRevenue)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-accent/20 rounded-lg">
              <BarChart3 className="w-6 h-6 text-accent" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">إجمالي التكاليف</p>
              <p className="text-2xl font-bold text-foreground">
                {formatCurrency(plData.costOfGoodsSold.totalCOGS)}
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
              <p className="text-sm font-medium text-muted-foreground">الربح الإجمالي</p>
              <p className="text-2xl font-bold text-foreground">
                {formatCurrency(plData.grossProfit)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${plData.netIncome >= 0 ? 'bg-primary/20' : 'bg-destructive/20'}`}>
              {plData.netIncome >= 0 ? (
                <TrendingUp className="w-6 h-6 text-primary" />
              ) : (
                <TrendingDown className="w-6 h-6 text-destructive" />
              )}
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">صافي الربح</p>
              <p className={`text-2xl font-bold ${plData.netIncome >= 0 ? 'text-primary' : 'text-destructive'}`}>
                {formatCurrency(plData.netIncome)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Profit & Loss Statement */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6">
        <div className="flex items-center mb-6">
          <FileText className="w-6 h-6 text-muted-foreground ml-2" />
          <h2 className="text-xl font-bold text-foreground">قائمة الأرباح والخسائر</h2>
        </div>

        <div className="space-y-6">
          {/* Revenue Section */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3 bg-primary-50 p-3 rounded-lg">الإيرادات</h3>
            <div className="space-y-2 mr-4">
              <div className="flex justify-between items-center py-2">
                <span>إيرادات المبيعات</span>
                <span className="font-medium">{formatCurrency(plData.revenue.salesRevenue)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>إيرادات أخرى</span>
                <span className="font-medium">{formatCurrency(plData.revenue.otherRevenue)}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-t border-border font-bold">
                <span>إجمالي الإيرادات</span>
                <span>{formatCurrency(plData.revenue.totalRevenue)}</span>
              </div>
            </div>
          </div>

          {/* Cost of Goods Sold */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3 bg-accent/10 p-3 rounded-lg">تكلفة البضاعة المباعة</h3>
            <div className="space-y-2 mr-4">
              <div className="flex justify-between items-center py-2">
                <span>المواد المباشرة</span>
                <span className="font-medium">{formatCurrency(plData.costOfGoodsSold.directMaterials)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>العمالة المباشرة</span>
                <span className="font-medium">{formatCurrency(plData.costOfGoodsSold.directLabor)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>المصروفات الصناعية غير المباشرة</span>
                <span className="font-medium">{formatCurrency(plData.costOfGoodsSold.manufacturingOverhead)}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-t border-border font-bold">
                <span>إجمالي تكلفة البضاعة المباعة</span>
                <span className="text-destructive">({formatCurrency(plData.costOfGoodsSold.totalCOGS)})</span>
              </div>
            </div>
          </div>

          {/* Gross Profit */}
          <div className="bg-primary/10 p-4 rounded-lg">
            <div className="flex justify-between items-center font-bold text-lg">
              <span>الربح الإجمالي</span>
              <span className="text-primary">{formatCurrency(plData.grossProfit)}</span>
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              هامش الربح الإجمالي: {calculatePercentage(plData.grossProfit, plData.revenue.totalRevenue)}%
            </div>
          </div>

          {/* Operating Expenses */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3 bg-destructive/10 p-3 rounded-lg">المصروفات التشغيلية</h3>
            <div className="space-y-2 mr-4">
              <div className="flex justify-between items-center py-2">
                <span>الرواتب والأجور</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.salariesAndWages)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>الإيجار</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.rent)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>المرافق</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.utilities)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>التسويق</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.marketing)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>التأمين</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.insurance)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>الإهلاك</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.depreciation)}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span>مصروفات أخرى</span>
                <span className="font-medium">{formatCurrency(plData.operatingExpenses.otherExpenses)}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-t border-border font-bold">
                <span>إجمالي المصروفات التشغيلية</span>
                <span className="text-destructive">({formatCurrency(plData.operatingExpenses.totalOperatingExpenses)})</span>
              </div>
            </div>
          </div>

          {/* Operating Income */}
          <div className="bg-primary-50 p-4 rounded-lg">
            <div className="flex justify-between items-center font-bold text-lg">
              <span>الدخل التشغيلي</span>
              <span className={plData.operatingIncome >= 0 ? 'text-primary-600' : 'text-destructive'}>
                {formatCurrency(plData.operatingIncome)}
              </span>
            </div>
          </div>

          {/* Net Income */}
          <div className={`p-4 rounded-lg ${plData.netIncome >= 0 ? 'bg-primary/10 border-2 border-primary/30' : 'bg-destructive/10 border-2 border-destructive/30'}`}>
            <div className="flex justify-between items-center font-bold text-xl">
              <span>صافي الربح (الخسارة)</span>
              <span className={plData.netIncome >= 0 ? 'text-primary' : 'text-destructive'}>
                {formatCurrency(plData.netIncome)}
              </span>
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              هامش صافي الربح: {calculatePercentage(plData.netIncome, plData.revenue.totalRevenue)}%
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfitLoss

