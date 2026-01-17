import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, Upload, Settings, CheckCircle, XCircle, AlertTriangle, Package, User, Calendar, Clock,
  TrendingUp, DollarSign, Users, FileText, Printer, BarChart3, PieChart
} from 'lucide-react';

const AdvancedReportsSystem = () => {
  const [selectedReport, setSelectedReport] = useState('inventory');
  const [dateRange, setDateRange] = useState('month');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);

  // أنواع التقارير المتاحة
  const reportTypes = [
    {
      id: 'inventory',
      name: 'تقرير المخزون',
      description: 'تقرير شامل عن حالة المخزون الحالية',
      icon: Package,
      color: 'blue'
    },
    {
      id: 'sales',
      name: 'تقرير المبيعات',
      description: 'تحليل المبيعات والأداء التجاري',
      icon: TrendingUp,
      color: 'green'
    },
    {
      id: 'financial',
      name: 'التقرير المالي',
      description: 'الأرباح والخسائر والتدفق النقدي',
      icon: DollarSign,
      color: 'purple'
    },
    {
      id: 'customers',
      name: 'تقرير العملاء',
      description: 'تحليل أداء العملاء والمديونيات',
      icon: Users,
      color: 'orange'
    },
    {
      id: 'suppliers',
      name: 'تقرير الموردين',
      description: 'تقييم أداء الموردين والمشتريات',
      icon: FileText,
      color: 'indigo'
    },
    {
      id: 'expiry',
      name: 'تقرير انتهاء الصلاحية',
      description: 'المنتجات قريبة الانتهاء والمنتهية',
      icon: AlertTriangle,
      color: 'red'
    }
  ];

  // بيانات تجريبية للتقارير
  const demoReportData = {
    inventory: {
      summary: {
        total_products: 156,
        total_value: 2850000,
        low_stock_items: 12,
        out_of_stock: 3,
        categories: 8
      },
      charts: {
        category_distribution: [
          { name: 'بذور', value: 45, count: 67 },
          { name: 'أسمدة', value: 30, count: 34 },
          { name: 'مبيدات', value: 15, count: 28 },
          { name: 'أدوات', value: 10, count: 27 }
        ],
        value_distribution: [
          { name: 'أقل من 1000 ج.م', count: 45 },
          { name: '1000 - 5000 ج.م', count: 67 },
          { name: '5000 - 10000 ج.م', count: 32 },
          { name: 'أكثر من 10000 ج.م', count: 12 }
        ]
      },
      details: [
        {
          product: 'بذور طماطم هجين',
          sku: 'TOM-HYB-001',
          current_stock: 150,
          min_quantity: 10,
          value: 3825,
          status: 'جيد'
        },
        {
          product: 'سماد NPK متوازن',
          sku: 'NPK-BAL-001',
          current_stock: 8,
          min_quantity: 10,
          value: 480,
          status: 'منخفض'
        }
      ]
    },
    sales: {
      summary: {
        total_sales: 1250000,
        total_orders: 89,
        avg_order_value: 14045,
        growth_rate: 12.5
      },
      charts: {
        monthly_sales: [
          { month: 'يناير', sales: 180000, orders: 15 },
          { month: 'فبراير', sales: 220000, orders: 18 },
          { month: 'مارس', sales: 195000, orders: 16 },
          { month: 'أبريل', sales: 240000, orders: 20 },
          { month: 'مايو', sales: 210000, orders: 17 },
          { month: 'يونيو', sales: 205000, orders: 3 }
        ],
        top_products: [
          { name: 'بذور طماطم هجين', sales: 125000, quantity: 500 },
          { name: 'سماد NPK متوازن', sales: 98000, quantity: 200 },
          { name: 'مبيد حشري طبيعي', sales: 87000, quantity: 150 }
        ]
      }
    },
    financial: {
      summary: {
        revenue: 1250000,
        cost_of_goods: 875000,
        gross_profit: 375000,
        expenses: 125000,
        net_profit: 250000,
        profit_margin: 20
      },
      charts: {
        profit_trend: [
          { month: 'يناير', revenue: 180000, profit: 36000 },
          { month: 'فبراير', revenue: 220000, profit: 44000 },
          { month: 'مارس', revenue: 195000, profit: 39000 },
          { month: 'أبريل', revenue: 240000, profit: 48000 },
          { month: 'مايو', revenue: 210000, profit: 42000 },
          { month: 'يونيو', revenue: 205000, profit: 41000 }
        ]
      }
    }
  };

  useEffect(() => {
    generateReport();
  }, [selectedReport, dateRange]);

  const generateReport = async () => {
    setLoading(true);
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setReportData(demoReportData[selectedReport] || {});
      setLoading(false);
    }, 1500);
  };

  const exportReport = (format) => {
    // محاكاة تصدير التقرير
    alert(`سيتم تصدير التقرير بصيغة ${format}`);
  };

  const printReport = () => {
    window.print();
  };

  // Removed unused function - icon is already available in reportTypes

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-primary-100 text-primary-800 border-primary-200',
      green: 'bg-primary/20 text-green-800 border-primary/30',
      purple: 'bg-purple-100 text-purple-800 border-purple-200',
      orange: 'bg-accent/20 text-orange-800 border-orange-200',
      indigo: 'bg-secondary/20 text-indigo-800 border-indigo-200',
      red: 'bg-destructive/20 text-red-800 border-destructive/30'
    };
    return colors[color] || colors.blue;
  };

  const StatCard = ({ title, value, subtitle, icon: IconComponent, color = 'blue' }) => (
    <div className={`p-4 rounded-lg border ${getColorClasses(color)}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-75">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
          {subtitle && <p className="text-xs opacity-60">{subtitle}</p>}
        </div>
        <IconComponent className="h-8 w-8 opacity-60" />
      </div>
    </div>
  );

  const ChartPlaceholder = ({ title, type = 'bar' }) => (
    <div className="bg-white p-4 rounded-lg border border-border">
      <h4 className="text-lg font-semibold mb-4">{title}</h4>
      <div className="h-64 bg-muted rounded-lg flex items-center justify-center">
        {type === 'bar' ? (
          <BarChart3 className="h-16 w-16 text-gray-400" />
        ) : (
          <PieChart className="h-16 w-16 text-gray-400" />
        )}
        <div className="mr-4 text-gray-500">
          <p className="font-medium">رسم بياني - {title}</p>
          <p className="text-sm">البيانات ستظهر هنا</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="p-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">نظام التقارير المتقدم</h1>
          <p className="text-muted-foreground">تقارير شاملة وتحليلات متقدمة للنظام</p>
        </div>
        
        <div className="flex space-x-2 space-x-reverse">
          <button
            onClick={printReport}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 flex items-center"
          >
            <Printer className="h-4 w-4 ml-2" />
            طباعة
          </button>
          <button
            onClick={() => exportReport('PDF')}
            className="bg-destructive text-white px-4 py-2 rounded-md hover:bg-red-700 flex items-center"
          >
            <Download className="h-4 w-4 ml-2" />
            PDF
          </button>
          <button
            onClick={() => exportReport('Excel')}
            className="bg-primary text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center"
          >
            <Download className="h-4 w-4 ml-2" />
            Excel
          </button>
        </div>
      </div>

      {/* أنواع التقارير */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {reportTypes.map(report => {
          const Icon = report.icon;
          return (
            <button
              key={report.id}
              onClick={() => setSelectedReport(report.id)}
              className={`p-4 rounded-lg border-2 text-right transition-all ${
                selectedReport === report.id
                  ? `border-${report.color}-500 bg-${report.color}-50`
                  : 'border-border hover:border-border'
              }`}
            >
              <div className="flex items-center mb-2">
                <Icon className={`h-6 w-6 ml-3 ${selectedReport === report.id ? `text-${report.color}-600` : 'text-muted-foreground'}`} />
                <h3 className={`font-semibold ${selectedReport === report.id ? `text-${report.color}-900` : 'text-foreground'}`}>
                  {report.name}
                </h3>
              </div>
              <p className="text-sm text-muted-foreground">{report.description}</p>
            </button>
          );
        })}
      </div>

      {/* أدوات التحكم */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              الفترة الزمنية
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="today">اليوم</option>
              <option value="week">هذا الأسبوع</option>
              <option value="month">هذا الشهر</option>
              <option value="quarter">هذا الربع</option>
              <option value="year">هذا العام</option>
              <option value="custom">فترة مخصصة</option>
            </select>
          </div>
          
          {dateRange === 'custom' && (
            <>
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  من تاريخ
                </label>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  إلى تاريخ
                </label>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </>
          )}
          
          <div className="flex items-end">
            <button
              onClick={generateReport}
              disabled={loading}
              className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 flex items-center justify-center"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <>
                  <BarChart3 className="h-4 w-4 ml-2" />
                  إنشاء التقرير
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* محتوى التقرير */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-muted-foreground">جاري إنشاء التقرير...</p>
          </div>
        </div>
      ) : reportData ? (
        <div className="space-y-6">
          {/* الإحصائيات السريعة */}
          {reportData.summary && (
            <div>
              <h2 className="text-xl font-bold text-foreground mb-4">الملخص التنفيذي</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {selectedReport === 'inventory' && (
                  <>
                    <StatCard
                      title="إجمالي المنتجات"
                      value={reportData.summary.total_products?.toLocaleString()}
                      icon={Package}
                      color="blue"
                    />
                    <StatCard
                      title="قيمة المخزون"
                      value={`${reportData.summary.total_value?.toLocaleString()} ج.م`}
                      icon={DollarSign}
                      color="green"
                    />
                    <StatCard
                      title="مخزون منخفض"
                      value={reportData.summary.low_stock_items}
                      icon={AlertTriangle}
                      color="orange"
                    />
                    <StatCard
                      title="نفد المخزون"
                      value={reportData.summary.out_of_stock}
                      icon={AlertTriangle}
                      color="red"
                    />
                  </>
                )}
                
                {selectedReport === 'sales' && (
                  <>
                    <StatCard
                      title="إجمالي المبيعات"
                      value={`${reportData.summary.total_sales?.toLocaleString()} ج.م`}
                      icon={DollarSign}
                      color="green"
                    />
                    <StatCard
                      title="عدد الطلبات"
                      value={reportData.summary.total_orders}
                      icon={FileText}
                      color="blue"
                    />
                    <StatCard
                      title="متوسط قيمة الطلب"
                      value={`${reportData.summary.avg_order_value?.toLocaleString()} ج.م`}
                      icon={TrendingUp}
                      color="purple"
                    />
                    <StatCard
                      title="معدل النمو"
                      value={`${reportData.summary.growth_rate}%`}
                      icon={TrendingUp}
                      color="green"
                    />
                  </>
                )}
                
                {selectedReport === 'financial' && (
                  <>
                    <StatCard
                      title="الإيرادات"
                      value={`${reportData.summary.revenue?.toLocaleString()} ج.م`}
                      icon={DollarSign}
                      color="green"
                    />
                    <StatCard
                      title="الربح الإجمالي"
                      value={`${reportData.summary.gross_profit?.toLocaleString()} ج.م`}
                      icon={TrendingUp}
                      color="blue"
                    />
                    <StatCard
                      title="الربح الصافي"
                      value={`${reportData.summary.net_profit?.toLocaleString()} ج.م`}
                      icon={CheckCircle}
                      color="green"
                    />
                    <StatCard
                      title="هامش الربح"
                      value={`${reportData.summary.profit_margin}%`}
                      icon={TrendingUp}
                      color="purple"
                    />
                  </>
                )}
              </div>
            </div>
          )}

          {/* الرسوم البيانية */}
          {reportData.charts && (
            <div>
              <h2 className="text-xl font-bold text-foreground mb-4">التحليل البياني</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {selectedReport === 'inventory' && (
                  <>
                    <ChartPlaceholder title="توزيع المنتجات حسب الفئة" type="pie" />
                    <ChartPlaceholder title="توزيع القيمة" type="bar" />
                  </>
                )}
                
                {selectedReport === 'sales' && (
                  <>
                    <ChartPlaceholder title="المبيعات الشهرية" type="bar" />
                    <ChartPlaceholder title="أفضل المنتجات مبيعاً" type="bar" />
                  </>
                )}
                
                {selectedReport === 'financial' && (
                  <>
                    <ChartPlaceholder title="اتجاه الأرباح" type="bar" />
                    <ChartPlaceholder title="توزيع المصروفات" type="pie" />
                  </>
                )}
              </div>
            </div>
          )}

          {/* التفاصيل */}
          {reportData.details && (
            <div>
              <h2 className="text-xl font-bold text-foreground mb-4">التفاصيل</h2>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-muted/50">
                      <tr>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          المنتج
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          رمز المنتج
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          المخزون الحالي
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          الحد الأدنى
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          القيمة
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          الحالة
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {reportData.details.map((item, index) => (
                        <tr key={index} className="hover:bg-muted/50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                            {item.product}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.sku}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                            {item.current_stock}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                            {item.min_quantity}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                            {item.value?.toLocaleString()} ج.م
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              item.status === 'جيد' ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
                            }`}>
                              {item.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-muted-foreground">اختر نوع التقرير وانقر على "إنشاء التقرير"</p>
        </div>
      )}
    </div>
  );
};

export default AdvancedReportsSystem;

