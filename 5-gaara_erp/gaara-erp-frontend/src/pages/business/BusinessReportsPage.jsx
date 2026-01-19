/**
 * Business Reports Page - التقارير التجارية
 * Gaara ERP v12
 *
 * Comprehensive business reporting with charts, analytics, and export options.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  BarChart3,
  PieChart,
  TrendingUp,
  TrendingDown,
  Download,
  Calendar,
  Filter,
  RefreshCw,
  FileText,
  DollarSign,
  ShoppingCart,
  Users,
  Package,
  ArrowUpRight,
  ArrowDownRight,
  Clock,
  Target,
  Eye,
  Printer,
  Mail,
  Share2,
  FileSpreadsheet,
  FilePlus,
  LayoutGrid,
  List,
  Settings,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"

// Mock data
const mockSalesData = {
  daily: [
    { date: "السبت", sales: 12500, orders: 15, profit: 3750 },
    { date: "الأحد", sales: 18200, orders: 22, profit: 5460 },
    { date: "الإثنين", sales: 15800, orders: 18, profit: 4740 },
    { date: "الثلاثاء", sales: 22100, orders: 28, profit: 6630 },
    { date: "الأربعاء", sales: 19500, orders: 24, profit: 5850 },
    { date: "الخميس", sales: 25800, orders: 32, profit: 7740 },
    { date: "الجمعة", sales: 8500, orders: 10, profit: 2550 },
  ],
  topProducts: [
    { name: "قمح سخا 94", sales: 45000, quantity: 3000, trend: 12 },
    { name: "سماد يوريا", sales: 35000, quantity: 1400, trend: 8 },
    { name: "مبيد حشري نيم", sales: 28000, quantity: 350, trend: -5 },
    { name: "بذور طماطم هجين", sales: 22500, quantity: 50, trend: 15 },
    { name: "سماد NPK مركب", sales: 18000, quantity: 600, trend: 3 },
  ],
  topCustomers: [
    { name: "شركة الزراعة الحديثة", total: 125000, orders: 45, growth: 18 },
    { name: "مزرعة النخيل الذهبي", total: 98000, orders: 38, growth: 12 },
    { name: "أحمد محمد العلي", total: 75000, orders: 25, growth: -3 },
    { name: "مؤسسة الواحة", total: 62000, orders: 22, growth: 8 },
    { name: "مزرعة الفردوس", total: 48000, orders: 18, growth: 22 },
  ],
}

const mockKPIs = {
  totalSales: { value: 585000, change: 12.5, target: 600000 },
  totalOrders: { value: 245, change: 8.3, target: 250 },
  avgOrderValue: { value: 2388, change: 3.8, target: 2500 },
  grossProfit: { value: 175500, change: 15.2, target: 180000 },
  profitMargin: { value: 30, change: 2.4, target: 32 },
  customerCount: { value: 128, change: 18.5, target: 150 },
}

const reportTypes = [
  { id: "sales", name: "تقرير المبيعات", icon: ShoppingCart, description: "تحليل شامل للمبيعات" },
  { id: "purchases", name: "تقرير المشتريات", icon: Package, description: "تحليل المشتريات والموردين" },
  { id: "inventory", name: "تقرير المخزون", icon: Package, description: "حالة المخزون والحركات" },
  { id: "financial", name: "التقرير المالي", icon: DollarSign, description: "الإيرادات والمصروفات" },
  { id: "customers", name: "تقرير العملاء", icon: Users, description: "تحليل العملاء والولاء" },
  { id: "products", name: "تقرير المنتجات", icon: Package, description: "أداء المنتجات والفئات" },
]

const BusinessReportsPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("overview")
  const [dateRange, setDateRange] = useState("month")
  const [viewMode, setViewMode] = useState("cards")
  const [isLoading, setIsLoading] = useState(false)
  const [selectedReport, setSelectedReport] = useState(null)

  // Helpers
  const formatCurrency = (value) => `${(value || 0).toLocaleString()} ر.س`
  const formatPercentage = (value) => `${(value || 0).toFixed(1)}%`

  // Calculate progress to target
  const getProgress = (current, target) => Math.min((current / target) * 100, 100)

  // Export handlers
  const handleExport = (format) => {
    toast.success(`جاري تصدير التقرير بصيغة ${format}...`)
  }

  const handlePrint = () => {
    toast.info("جاري تحضير الطباعة...")
    window.print()
  }

  const handleSchedule = () => {
    toast.info("سيتم إضافة جدولة التقارير قريباً")
  }

  // Render KPI Card
  const KPICard = ({ title, value, change, target, icon: Icon, format = "number" }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-muted-foreground">{title}</span>
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${change >= 0 ? "bg-green-100" : "bg-red-100"}`}>
            <Icon className={`w-4 h-4 ${change >= 0 ? "text-green-600" : "text-red-600"}`} />
          </div>
        </div>
        <div className="flex items-end justify-between">
          <div>
            <p className="text-2xl font-bold">
              {format === "currency" ? formatCurrency(value) : format === "percentage" ? formatPercentage(value) : value.toLocaleString()}
            </p>
            <div className={`flex items-center gap-1 text-sm ${change >= 0 ? "text-green-600" : "text-red-600"}`}>
              {change >= 0 ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
              <span>{Math.abs(change).toFixed(1)}%</span>
            </div>
          </div>
          <div className="w-20 text-left">
            <p className="text-xs text-muted-foreground mb-1">الهدف</p>
            <Progress value={getProgress(value, target)} className="h-2" />
          </div>
        </div>
      </CardContent>
    </Card>
  )

  // Render simple bar chart
  const SimpleBarChart = ({ data, valueKey, labelKey }) => {
    const maxValue = Math.max(...data.map(d => d[valueKey]))
    return (
      <div className="space-y-3">
        {data.map((item, index) => (
          <div key={index} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span>{item[labelKey]}</span>
              <span className="font-medium">{(item[valueKey] / 1000).toFixed(1)}K</span>
            </div>
            <Progress value={(item[valueKey] / maxValue) * 100} className="h-2" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <BarChart3 className="w-7 h-7 text-indigo-500" />
            التقارير والتحليلات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تحليل شامل لأداء الأعمال</p>
        </div>
        <div className="flex gap-2">
          <Select value={dateRange} onValueChange={setDateRange}>
            <SelectTrigger className="w-[140px]">
              <Calendar className="w-4 h-4 ml-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="today">اليوم</SelectItem>
              <SelectItem value="week">هذا الأسبوع</SelectItem>
              <SelectItem value="month">هذا الشهر</SelectItem>
              <SelectItem value="quarter">هذا الربع</SelectItem>
              <SelectItem value="year">هذه السنة</SelectItem>
              <SelectItem value="custom">فترة مخصصة</SelectItem>
            </SelectContent>
          </Select>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                <Download className="w-4 h-4 ml-2" />
                تصدير
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => handleExport("PDF")}>
                <FileText className="w-4 h-4 ml-2" />تصدير PDF
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleExport("Excel")}>
                <FileSpreadsheet className="w-4 h-4 ml-2" />تصدير Excel
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handlePrint}>
                <Printer className="w-4 h-4 ml-2" />طباعة
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("جاري الإرسال...")}>
                <Mail className="w-4 h-4 ml-2" />إرسال بالبريد
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Button variant="outline" onClick={() => setIsLoading(true)}>
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث
          </Button>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <KPICard title="إجمالي المبيعات" value={mockKPIs.totalSales.value} change={mockKPIs.totalSales.change} target={mockKPIs.totalSales.target} icon={DollarSign} format="currency" />
        <KPICard title="الطلبات" value={mockKPIs.totalOrders.value} change={mockKPIs.totalOrders.change} target={mockKPIs.totalOrders.target} icon={ShoppingCart} />
        <KPICard title="متوسط الطلب" value={mockKPIs.avgOrderValue.value} change={mockKPIs.avgOrderValue.change} target={mockKPIs.avgOrderValue.target} icon={Target} format="currency" />
        <KPICard title="إجمالي الربح" value={mockKPIs.grossProfit.value} change={mockKPIs.grossProfit.change} target={mockKPIs.grossProfit.target} icon={TrendingUp} format="currency" />
        <KPICard title="هامش الربح" value={mockKPIs.profitMargin.value} change={mockKPIs.profitMargin.change} target={mockKPIs.profitMargin.target} icon={PieChart} format="percentage" />
        <KPICard title="العملاء" value={mockKPIs.customerCount.value} change={mockKPIs.customerCount.change} target={mockKPIs.customerCount.target} icon={Users} />
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <LayoutGrid className="w-4 h-4" />نظرة عامة
          </TabsTrigger>
          <TabsTrigger value="sales" className="flex items-center gap-2">
            <ShoppingCart className="w-4 h-4" />المبيعات
          </TabsTrigger>
          <TabsTrigger value="customers" className="flex items-center gap-2">
            <Users className="w-4 h-4" />العملاء
          </TabsTrigger>
          <TabsTrigger value="products" className="flex items-center gap-2">
            <Package className="w-4 h-4" />المنتجات
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />التقارير
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            {/* Sales Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  المبيعات اليومية
                </CardTitle>
                <CardDescription>مبيعات آخر 7 أيام</CardDescription>
              </CardHeader>
              <CardContent>
                <SimpleBarChart data={mockSalesData.daily} valueKey="sales" labelKey="date" />
              </CardContent>
            </Card>

            {/* Top Products */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Package className="w-5 h-5" />
                  أفضل المنتجات
                </CardTitle>
                <CardDescription>المنتجات الأكثر مبيعاً</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockSalesData.topProducts.map((product, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-full bg-primary/10 text-primary text-sm flex items-center justify-center font-medium">
                        {index + 1}
                      </span>
                      <div className="flex-1">
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-muted-foreground">{product.quantity} وحدة</p>
                      </div>
                      <div className="text-left">
                        <p className="font-bold">{formatCurrency(product.sales)}</p>
                        <span className={`text-xs ${product.trend >= 0 ? "text-green-600" : "text-red-600"}`}>
                          {product.trend >= 0 ? "+" : ""}{product.trend}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Stats */}
          <div className="grid md:grid-cols-4 gap-4">
            <Card className="bg-gradient-to-br from-emerald-500 to-emerald-600 text-white">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-emerald-100">أعلى مبيعات</p>
                    <p className="text-2xl font-bold">الخميس</p>
                    <p className="text-sm text-emerald-100">25,800 ر.س</p>
                  </div>
                  <TrendingUp className="w-10 h-10 text-emerald-200" />
                </div>
              </CardContent>
            </Card>
            <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100">معدل التحويل</p>
                    <p className="text-2xl font-bold">68.5%</p>
                    <p className="text-sm text-blue-100">+5.2% من الشهر الماضي</p>
                  </div>
                  <Target className="w-10 h-10 text-blue-200" />
                </div>
              </CardContent>
            </Card>
            <Card className="bg-gradient-to-br from-purple-500 to-purple-600 text-white">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-purple-100">عملاء جدد</p>
                    <p className="text-2xl font-bold">24</p>
                    <p className="text-sm text-purple-100">هذا الشهر</p>
                  </div>
                  <Users className="w-10 h-10 text-purple-200" />
                </div>
              </CardContent>
            </Card>
            <Card className="bg-gradient-to-br from-amber-500 to-amber-600 text-white">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-amber-100">طلبات معلقة</p>
                    <p className="text-2xl font-bold">8</p>
                    <p className="text-sm text-amber-100">بانتظار المعالجة</p>
                  </div>
                  <Clock className="w-10 h-10 text-amber-200" />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Sales Tab */}
        <TabsContent value="sales" className="space-y-4">
          <div className="grid md:grid-cols-3 gap-4">
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>تحليل المبيعات</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {mockSalesData.daily.map((day, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between">
                        <span className="font-medium">{day.date}</span>
                        <div className="flex gap-4 text-sm">
                          <span>{formatCurrency(day.sales)}</span>
                          <span className="text-muted-foreground">{day.orders} طلب</span>
                          <span className="text-green-600">{formatCurrency(day.profit)} ربح</span>
                        </div>
                      </div>
                      <Progress value={(day.sales / 30000) * 100} className="h-3" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>ملخص المبيعات</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 rounded-lg bg-muted">
                    <p className="text-sm text-muted-foreground">إجمالي المبيعات</p>
                    <p className="text-2xl font-bold">{formatCurrency(mockSalesData.daily.reduce((s, d) => s + d.sales, 0))}</p>
                  </div>
                  <div className="p-4 rounded-lg bg-muted">
                    <p className="text-sm text-muted-foreground">إجمالي الطلبات</p>
                    <p className="text-2xl font-bold">{mockSalesData.daily.reduce((s, d) => s + d.orders, 0)}</p>
                  </div>
                  <div className="p-4 rounded-lg bg-green-50">
                    <p className="text-sm text-green-600">إجمالي الأرباح</p>
                    <p className="text-2xl font-bold text-green-600">{formatCurrency(mockSalesData.daily.reduce((s, d) => s + d.profit, 0))}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Customers Tab */}
        <TabsContent value="customers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>أفضل العملاء</CardTitle>
              <CardDescription>العملاء الأكثر تعاملاً</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockSalesData.topCustomers.map((customer, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 rounded-lg border">
                    <span className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold">
                      {index + 1}
                    </span>
                    <div className="flex-1">
                      <p className="font-medium">{customer.name}</p>
                      <p className="text-sm text-muted-foreground">{customer.orders} طلب</p>
                    </div>
                    <div className="text-left">
                      <p className="font-bold">{formatCurrency(customer.total)}</p>
                      <span className={`text-sm ${customer.growth >= 0 ? "text-green-600" : "text-red-600"}`}>
                        {customer.growth >= 0 ? "+" : ""}{customer.growth}% نمو
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Products Tab */}
        <TabsContent value="products" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>أداء المنتجات</CardTitle>
              <CardDescription>تحليل مبيعات المنتجات</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockSalesData.topProducts.map((product, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 rounded-lg border">
                    <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
                      <Package className="w-6 h-6 text-muted-foreground" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium">{product.name}</p>
                      <p className="text-sm text-muted-foreground">{product.quantity} وحدة مباعة</p>
                    </div>
                    <div className="w-32">
                      <Progress value={(product.sales / mockSalesData.topProducts[0].sales) * 100} className="h-2 mb-1" />
                      <p className="text-xs text-muted-foreground text-left">{((product.sales / mockSalesData.topProducts.reduce((s, p) => s + p.sales, 0)) * 100).toFixed(1)}% من الإجمالي</p>
                    </div>
                    <div className="text-left">
                      <p className="font-bold">{formatCurrency(product.sales)}</p>
                      <span className={`text-sm ${product.trend >= 0 ? "text-green-600" : "text-red-600"}`}>
                        {product.trend >= 0 ? "+" : ""}{product.trend}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>التقارير المتاحة</CardTitle>
                <CardDescription>اختر التقرير المطلوب لعرضه أو تصديره</CardDescription>
              </div>
              <Button onClick={() => toast.info("سيتم إضافة التقارير المخصصة قريباً")}>
                <FilePlus className="w-4 h-4 ml-2" />
                تقرير مخصص
              </Button>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {reportTypes.map((report) => (
                  <Card key={report.id} className="cursor-pointer hover:border-primary transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-start gap-3">
                        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                          <report.icon className="w-5 h-5 text-primary" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium">{report.name}</p>
                          <p className="text-sm text-muted-foreground">{report.description}</p>
                        </div>
                      </div>
                      <div className="flex gap-2 mt-4">
                        <Button size="sm" variant="outline" className="flex-1" onClick={() => toast.info(`جاري عرض ${report.name}...`)}>
                          <Eye className="w-3 h-3 ml-1" />عرض
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleExport("PDF")}>
                          <Download className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Scheduled Reports */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>التقارير المجدولة</CardTitle>
                <CardDescription>التقارير التي يتم إرسالها تلقائياً</CardDescription>
              </div>
              <Button variant="outline" onClick={handleSchedule}>
                <Settings className="w-4 h-4 ml-2" />
                إدارة الجدولة
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex items-center gap-3">
                    <Clock className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium">تقرير المبيعات الأسبوعي</p>
                      <p className="text-sm text-muted-foreground">كل أحد الساعة 8:00 صباحاً</p>
                    </div>
                  </div>
                  <Badge variant="default">نشط</Badge>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex items-center gap-3">
                    <Clock className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium">التقرير المالي الشهري</p>
                      <p className="text-sm text-muted-foreground">أول كل شهر الساعة 9:00 صباحاً</p>
                    </div>
                  </div>
                  <Badge variant="default">نشط</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default BusinessReportsPage
