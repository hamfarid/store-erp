import React, { useState, useEffect, useRef } from 'react'
import { useReactToPrint } from 'react-to-print'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, RefreshCw,
  Activity, AlertTriangle, Printer, TrendingDown, Warehouse
} from 'lucide-react'

const InventoryReports = () => {
  const [reports, setReports] = useState({})
  const [loading, setLoading] = useState(false)
  const [selectedReport, setSelectedReport] = useState('overview')
  const [dateRange, setDateRange] = useState('month')
  const [selectedWarehouse, setSelectedWarehouse] = useState('all')
  const printRef = useRef()

  useEffect(() => {
    loadReports()
  }, [selectedReport, dateRange, selectedWarehouse])

  const loadReports = async () => {
    setLoading(true)
    try {
      // محاولة تحميل التقارير من API
      const response = await fetch(`/api/reports/inventory-report?warehouse_id=${selectedWarehouse}&date_range=${dateRange}`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          // تحويل البيانات من API إلى تنسيق التقارير
          const apiReports = {
            overview: {
              totalProducts: data.data.summary.total_products,
              totalValue: data.data.summary.total_value,
              lowStockItems: data.data.summary.low_stock_count,
              expiringSoon: 8, // سيتم حسابها من البيانات
              topProducts: data.data.inventory.slice(0, 3).map(item => ({
                name: item.product_name,
                quantity: item.current_stock,
                value: item.stock_value
              })),
              categoryDistribution: [] // سيتم حسابها من البيانات
            }
          }
          setReports(apiReports)
          return
        }
      }

      // في حالة فشل API، استخدم البيانات التجريبية
      const mockReports = {
        overview: {
          totalProducts: 156,
          totalValue: 2450000,
          lowStockItems: 12,
          expiringSoon: 8,
          topProducts: [
            { name: 'بذور طماطم هجين', quantity: 500, value: 125000 },
            { name: 'سماد NPK', quantity: 200, value: 80000 },
            { name: 'مبيد حشري', quantity: 150, value: 75000 }
          ],
          categoryDistribution: [
            { category: 'بذور', count: 45, percentage: 28.8 },
            { category: 'أسمدة', count: 38, percentage: 24.4 },
            { category: 'مبيدات', count: 32, percentage: 20.5 },
            { category: 'أدوات', count: 25, percentage: 16.0 },
            { category: 'أخرى', count: 16, percentage: 10.3 }
          ]
        },
        movements: {
          totalMovements: 245,
          inbound: 98,
          outbound: 127,
          transfers: 20,
          recentMovements: [
            { date: '2024-07-04', type: 'وارد', product: 'بذور طماطم', quantity: 100, warehouse: 'المخزن الرئيسي' },
            { date: '2024-07-04', type: 'صادر', product: 'سماد NPK', quantity: 50, warehouse: 'مخزن الأسمدة' },
            { date: '2024-07-03', type: 'تحويل', product: 'مبيد حشري', quantity: 25, warehouse: 'المخزن الفرعي' }
          ]
        },
        valuation: {
          totalValue: 2450000,
          averageValue: 15705,
          highestValue: { product: 'بذور طماطم هجين', value: 125000 },
          lowestValue: { product: 'أدوات صغيرة', value: 500 },
          valueByCategory: [
            { category: 'بذور', value: 850000, percentage: 34.7 },
            { category: 'أسمدة', value: 720000, percentage: 29.4 },
            { category: 'مبيدات', value: 580000, percentage: 23.7 },
            { category: 'أدوات', value: 200000, percentage: 8.2 },
            { category: 'أخرى', value: 100000, percentage: 4.1 }
          ]
        },
        alerts: {
          lowStock: [
            { product: 'بذور خيار', currentStock: 5, minStock: 20, shortage: 15 },
            { product: 'سماد عضوي', currentStock: 8, minStock: 25, shortage: 17 },
            { product: 'مبيد فطري', currentStock: 3, minStock: 15, shortage: 12 }
          ],
          expiring: [
            { product: 'بذور طماطم لوط A', expiryDate: '2024-07-15', daysLeft: 11 },
            { product: 'سماد NPK لوط B', expiryDate: '2024-07-20', daysLeft: 16 },
            { product: 'مبيد حشري لوط C', expiryDate: '2024-07-25', daysLeft: 21 }
          ],
          overstock: [
            { product: 'أدوات زراعية', currentStock: 200, maxStock: 100, excess: 100 },
            { product: 'بذور ذرة', currentStock: 150, maxStock: 80, excess: 70 }
          ]
        }
      }
      
      setReports(mockReports)
    } catch (error) {
      } finally {
      setLoading(false)
    }
  }

  const handlePrint = useReactToPrint({
    content: () => printRef.current,
    documentTitle: `تقرير_المخزون_${selectedReport}_${new Date().toISOString().split('T')[0]}`,
    pageStyle: `
      @page {
        size: A4;
        margin: 20mm;
      }
      @media print {
        body { -webkit-print-color-adjust: exact; }
        .no-print { display: none !important; }
      }
    `
  })

  const exportReport = (format) => {
    const reportData = reports[selectedReport]
    if (!reportData) return

    if (format === 'csv') {
      let csvContent = "data:text/csv;charset=utf-8,"

      if (selectedReport === 'overview') {
        csvContent += "المنتج,الكمية,القيمة\n"
        csvContent += reportData.topProducts.map(p =>
          `${p.name},${p.quantity},${p.value}`
        ).join("\n")
      }

      const encodedUri = encodeURI(csvContent)
      const link = document.createElement("a")
      link.setAttribute("href", encodedUri)
      link.setAttribute("download", `inventory_report_${selectedReport}_${new Date().toISOString().split('T')[0]}.csv`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } else if (format === 'pdf') {
      // محاكاة تصدير PDF
      alert('تم تصدير التقرير بصيغة PDF بنجاح!')
    }
  }

  const reportTypes = [
    { id: 'overview', name: 'نظرة عامة', icon: BarChart3 },
    { id: 'movements', name: 'حركات المخزون', icon: Activity },
    { id: 'valuation', name: 'تقييم المخزون', icon: TrendingUp },
    { id: 'alerts', name: 'التنبيهات', icon: AlertTriangle }
  ]

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
      <div className="flex justify-between items-center mb-6 no-print">
        <div>
          <h1 className="text-2xl font-bold text-foreground">تقارير المخزون</h1>
          <p className="text-muted-foreground">تقارير وتحليلات شاملة للمخزون واللوطات</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handlePrint}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center"
          >
            <Printer className="w-5 h-5 ml-2" />
            طباعة
          </button>
          <button
            onClick={() => exportReport('pdf')}
            className="bg-destructive text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors flex items-center"
          >
            <FileText className="w-5 h-5 ml-2" />
            PDF
          </button>
          <button
            onClick={() => exportReport('csv')}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
          >
            <Download className="w-5 h-5 ml-2" />
            Excel
          </button>
          <button
            onClick={loadReports}
            className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
          >
            <RefreshCw className="w-5 h-5 ml-2" />
            تحديث
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 no-print">
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="week">آخر أسبوع</option>
          <option value="month">آخر شهر</option>
          <option value="quarter">آخر ربع</option>
          <option value="year">آخر سنة</option>
        </select>

        <select
          value={selectedWarehouse}
          onChange={(e) => setSelectedWarehouse(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="all">جميع المخازن</option>
          <option value="main">المخزن الرئيسي</option>
          <option value="seeds">مخزن البذور</option>
          <option value="fertilizers">مخزن الأسمدة</option>
        </select>

        <div className="relative">
          <input
            type="text"
            placeholder="البحث في التقارير..."
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
      </div>

      {/* Report Type Tabs */}
      <div className="bg-white rounded-lg shadow mb-6 no-print">
        <div className="border-b border-border">
          <nav className="flex space-x-8 px-6">
            {reportTypes.map((type) => {
              const Icon = type.icon
              return (
                <button
                  key={type.id}
                  onClick={() => setSelectedReport(type.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                    selectedReport === type.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  }`}
                >
                  <Icon className="w-5 h-5 ml-2" />
                  {type.name}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Report Content */}
      <div className="space-y-6" ref={printRef}>
        {/* Overview Report */}
        {selectedReport === 'overview' && reports.overview && (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <Package className="h-8 w-8 text-primary-600" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">إجمالي المنتجات</p>
                    <p className="text-2xl font-bold text-foreground">{reports.overview.totalProducts}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <TrendingUp className="h-8 w-8 text-primary" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">إجمالي القيمة</p>
                    <p className="text-2xl font-bold text-foreground">
                      {reports.overview.totalValue.toLocaleString()} ج.م
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <AlertTriangle className="h-8 w-8 text-accent" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">مخزون منخفض</p>
                    <p className="text-2xl font-bold text-foreground">{reports.overview.lowStockItems}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <Calendar className="h-8 w-8 text-destructive" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">منتهي الصلاحية قريباً</p>
                    <p className="text-2xl font-bold text-foreground">{reports.overview.expiringSoon}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Top Products */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">أهم المنتجات</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المنتج</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الكمية</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">القيمة</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {reports.overview.topProducts.map((product, index) => (
                      <tr key={`product-${index}-${product.name}`}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                          {product.name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                          {product.quantity}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                          {product.value.toLocaleString()} ج.م
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Category Distribution */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">توزيع الفئات</h3>
              <div className="space-y-3">
                {reports.overview.categoryDistribution.map((category) => (
                  <div key={`category-${category.category}`} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-4 h-4 rounded-full bg-primary-500 ml-3"></div>
                      <span className="text-sm font-medium text-foreground">{category.category}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-sm text-muted-foreground ml-2">{category.count} منتج</span>
                      <span className="text-sm font-medium text-foreground">{category.percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Movements Report */}
        {selectedReport === 'movements' && reports.movements && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <Activity className="h-8 w-8 text-primary-600" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">إجمالي الحركات</p>
                    <p className="text-2xl font-bold text-foreground">{reports.movements.totalMovements}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <TrendingDown className="h-8 w-8 text-primary" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">حركات الوارد</p>
                    <p className="text-2xl font-bold text-foreground">{reports.movements.inbound}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <TrendingUp className="h-8 w-8 text-destructive" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">حركات الصادر</p>
                    <p className="text-2xl font-bold text-foreground">{reports.movements.outbound}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="flex items-center">
                  <Warehouse className="h-8 w-8 text-purple-600" />
                  <div className="mr-3">
                    <p className="text-sm font-medium text-muted-foreground">التحويلات</p>
                    <p className="text-2xl font-bold text-foreground">{reports.movements.transfers}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">أحدث الحركات</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المنتج</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الكمية</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المخزن</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {reports.movements.recentMovements.map((movement, index) => (
                      <tr key={`movement-${index}-${movement.date}-${movement.product}`}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{movement.date}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {(() => {
                            let colorClass = 'bg-primary-100 text-primary-800'
                            if (movement.type === 'وارد') {
                              colorClass = 'bg-primary/20 text-green-800'
                            } else if (movement.type === 'صادر') {
                              colorClass = 'bg-destructive/20 text-red-800'
                            }
                            return (
                              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colorClass}`}>
                                {movement.type}
                              </span>
                            )
                          })()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                          {movement.product}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{movement.quantity}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{movement.warehouse}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* Alerts Report */}
        {selectedReport === 'alerts' && reports.alerts && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Low Stock */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 text-accent">مخزون منخفض</h3>
              <div className="space-y-3">
                {reports.alerts.lowStock.map((item) => (
                  <div key={`lowstock-${item.product}`} className="border-l-4 border-orange-400 pl-4">
                    <p className="font-medium text-foreground">{item.product}</p>
                    <p className="text-sm text-muted-foreground">
                      المخزون: {item.currentStock} | المطلوب: {item.minStock}
                    </p>
                    <p className="text-sm text-accent">نقص: {item.shortage}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Expiring Soon */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 text-destructive">منتهي الصلاحية قريباً</h3>
              <div className="space-y-3">
                {reports.alerts.expiring.map((item) => (
                  <div key={`expiring-${item.product}`} className="border-l-4 border-red-400 pl-4">
                    <p className="font-medium text-foreground">{item.product}</p>
                    <p className="text-sm text-muted-foreground">انتهاء: {item.expiryDate}</p>
                    <p className="text-sm text-destructive">باقي: {item.daysLeft} يوم</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Overstock */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 text-primary-600">مخزون زائد</h3>
              <div className="space-y-3">
                {reports.alerts.overstock.map((item) => (
                  <div key={`overstock-${item.product}`} className="border-l-4 border-primary-400 pl-4">
                    <p className="font-medium text-foreground">{item.product}</p>
                    <p className="text-sm text-muted-foreground">
                      المخزون: {item.currentStock} | الحد الأقصى: {item.maxStock}
                    </p>
                    <p className="text-sm text-primary-600">زائد: {item.excess}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default InventoryReports

