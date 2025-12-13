import React, { useState } from 'react'
import {
  BarChart3, Calendar, Download, FileText,
  Filter, PieChart, TrendingUp
} from 'lucide-react'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart as RechartsPieChart, Pie, Cell } from 'recharts'

const Reports = () => {
  const [selectedReport, setSelectedReport] = useState('inventory')
  const [dateRange, setDateRange] = useState({ from: '', to: '' })

  // بيانات تجريبية للتقارير
  const inventoryData = [
    { name: 'بذور طماطم', quantity: 100, value: 7500 },
    { name: 'بذور خيار', quantity: 80, value: 4800 },
    { name: 'شتلات طماطم', quantity: 5, value: 200 },
    { name: 'سماد NPK', quantity: 50, value: 7500 },
    { name: 'مبيد حشري', quantity: 2, value: 200 }
  ]

  const salesData = [
    { month: 'يناير', sales: 45000, profit: 12000 },
    { month: 'فبراير', sales: 52000, profit: 15000 },
    { month: 'مارس', sales: 48000, profit: 13500 },
    { month: 'أبريل', sales: 61000, profit: 18000 },
    { month: 'مايو', sales: 55000, profit: 16500 },
    { month: 'يونيو', sales: 67000, profit: 20000 }
  ]

  const categoryDistribution = [
    { name: 'بذور', value: 40, color: '#3B82F6' },
    { name: 'شتلات', value: 30, color: '#10B981' },
    { name: 'أسمدة', value: 20, color: '#F59E0B' },
    { name: 'مبيدات', value: 10, color: '#EF4444' }
  ]

  const movementData = [
    { date: '2025-06-01', in: 150, out: 80 },
    { date: '2025-06-02', in: 120, out: 95 },
    { date: '2025-06-03', in: 200, out: 110 },
    { date: '2025-06-04', in: 180, out: 75 },
    { date: '2025-06-05', in: 160, out: 120 },
    { date: '2025-06-06', in: 140, out: 90 },
    { date: '2025-06-07', in: 190, out: 105 }
  ]

  const reportTypes = [
    { id: 'inventory', name: 'تقرير المخزون', icon: BarChart3, description: 'حالة المخزون الحالية وقيم المنتجات' },
    { id: 'sales', name: 'تقرير المبيعات', icon: TrendingUp, description: 'تحليل المبيعات والأرباح الشهرية' },
    { id: 'movements', name: 'حركات المخزون', icon: FileText, description: 'تتبع حركات الدخول والخروج' },
    { id: 'categories', name: 'توزيع الفئات', icon: PieChart, description: 'توزيع المنتجات حسب الفئات' }
  ]

  const handleExport = (format) => {
    // محاكاة تصدير التقرير
    const reportName = reportTypes.find(r => r.id === selectedReport)?.name || 'تقرير'
    alert(`سيتم تصدير ${reportName} بصيغة ${format}`)
  }

  const ReportCard = ({ report, isSelected, onClick }) => {
    const Icon = report.icon
    return (
      <div
        onClick={onClick}
        className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
          isSelected 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-border hover:border-border bg-white'
        }`}
      >
        <div className="flex items-center mb-2">
          <Icon className={`w-6 h-6 ml-2 ${isSelected ? 'text-primary-600' : 'text-muted-foreground'}`} />
          <h3 className={`font-semibold ${isSelected ? 'text-primary-900' : 'text-foreground'}`}>
            {report.name}
          </h3>
        </div>
        <p className="text-sm text-muted-foreground">{report.description}</p>
      </div>
    )
  }

  const renderReportContent = () => {
    switch (selectedReport) {
      case 'inventory':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">حالة المخزون الحالية</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={inventoryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="quantity" fill="#3B82F6" name="الكمية" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">تفاصيل المخزون</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-2 text-right">المنتج</th>
                      <th className="px-4 py-2 text-right">الكمية</th>
                      <th className="px-4 py-2 text-right">القيمة (جنيه)</th>
                      <th className="px-4 py-2 text-right">الحالة</th>
                    </tr>
                  </thead>
                  <tbody>
                    {inventoryData.map((item, index) => (
                      <tr key={index} className="border-b">
                        <td className="px-4 py-2">{item.name}</td>
                        <td className="px-4 py-2">{item.quantity}</td>
                        <td className="px-4 py-2">{item.value.toLocaleString()}</td>
                        <td className="px-4 py-2">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            item.quantity < 10 ? 'bg-destructive/20 text-red-800' : 'bg-primary/20 text-green-800'
                          }`}>
                            {item.quantity < 10 ? 'مخزون منخفض' : 'متوفر'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )

      case 'sales':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">تطور المبيعات والأرباح</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="sales" stroke="#3B82F6" name="المبيعات" />
                  <Line type="monotone" dataKey="profit" stroke="#10B981" name="الأرباح" />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded-lg shadow-md">
                <h4 className="font-semibold text-foreground">إجمالي المبيعات</h4>
                <p className="text-2xl font-bold text-primary-600">
                  {salesData.reduce((sum, item) => sum + item.sales, 0).toLocaleString()} جنيه
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-md">
                <h4 className="font-semibold text-foreground">إجمالي الأرباح</h4>
                <p className="text-2xl font-bold text-primary">
                  {salesData.reduce((sum, item) => sum + item.profit, 0).toLocaleString()} جنيه
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-md">
                <h4 className="font-semibold text-foreground">هامش الربح</h4>
                <p className="text-2xl font-bold text-purple-600">
                  {((salesData.reduce((sum, item) => sum + item.profit, 0) / 
                     salesData.reduce((sum, item) => sum + item.sales, 0)) * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        )

      case 'movements':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">حركات المخزون اليومية</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={movementData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="in" fill="#10B981" name="وارد" />
                  <Bar dataKey="out" fill="#EF4444" name="صادر" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )

      case 'categories':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">توزيع المنتجات حسب الفئات</h3>
              <ResponsiveContainer width="100%" height={300}>
                <RechartsPieChart>
                  <Pie
                    data={categoryDistribution}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {categoryDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">تفاصيل الفئات</h3>
              <div className="space-y-3">
                {categoryDistribution.map((category, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                    <div className="flex items-center">
                      <div 
                        className="w-4 h-4 rounded-full ml-3"
                        style={{ backgroundColor: category.color }}
                      ></div>
                      <span className="font-medium">{category.name}</span>
                    </div>
                    <span className="text-muted-foreground">{category.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">التقارير والتحليلات</h1>
        <p className="text-muted-foreground mt-2">تقارير شاملة وتحليلات مفصلة لأداء النظام</p>
      </div>

      {/* فلاتر التاريخ والتصدير */}
      <div className="bg-white p-4 rounded-lg shadow-md mb-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-4 space-x-reverse">
            <div className="flex items-center">
              <Calendar className="w-4 h-4 ml-2 text-gray-500" />
              <label className="text-sm font-medium text-foreground ml-2">من:</label>
              <input
                type="date"
                value={dateRange.from}
                onChange={(e) => setDateRange({...dateRange, from: e.target.value})}
                className="border border-border rounded-md px-3 py-1 text-sm"
              />
            </div>
            <div className="flex items-center">
              <label className="text-sm font-medium text-foreground ml-2">إلى:</label>
              <input
                type="date"
                value={dateRange.to}
                onChange={(e) => setDateRange({...dateRange, to: e.target.value})}
                className="border border-border rounded-md px-3 py-1 text-sm"
              />
            </div>
            <button className="bg-primary-600 text-white px-4 py-1 rounded-md text-sm hover:bg-primary-700 flex items-center">
              <Filter className="w-4 h-4 ml-1" />
              تطبيق
            </button>
          </div>
          
          <div className="flex space-x-2 space-x-reverse">
            <button
              onClick={() => handleExport('PDF')}
              className="bg-destructive text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 flex items-center"
            >
              <Download className="w-4 h-4 ml-1" />
              PDF
            </button>
            <button
              onClick={() => handleExport('Excel')}
              className="bg-primary text-white px-4 py-2 rounded-md text-sm hover:bg-green-700 flex items-center"
            >
              <Download className="w-4 h-4 ml-1" />
              Excel
            </button>
          </div>
        </div>
      </div>

      {/* اختيار نوع التقرير */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {reportTypes.map((report) => (
          <ReportCard
            key={report.id}
            report={report}
            isSelected={selectedReport === report.id}
            onClick={() => setSelectedReport(report.id)}
          />
        ))}
      </div>

      {/* محتوى التقرير */}
      {renderReportContent()}
    </div>
  )
}

export default Reports


