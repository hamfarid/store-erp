import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  ShoppingCart,
  Package,
  Users,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Wifi,
  Brain,
  MoreHorizontal,
  RefreshCw,
} from "lucide-react"
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { formatCurrency, formatNumber, formatPercent } from "@/lib/utils"

// Mock data - Replace with API calls
const statsData = [
  {
    title: "إجمالي المبيعات",
    value: 245680,
    change: 12.5,
    icon: DollarSign,
    color: "emerald",
    format: "currency",
  },
  {
    title: "الطلبات الجديدة",
    value: 1234,
    change: 8.2,
    icon: ShoppingCart,
    color: "blue",
    format: "number",
  },
  {
    title: "المنتجات في المخزون",
    value: 5678,
    change: -3.1,
    icon: Package,
    color: "purple",
    format: "number",
  },
  {
    title: "العملاء النشطين",
    value: 892,
    change: 15.3,
    icon: Users,
    color: "orange",
    format: "number",
  },
]

const salesChartData = [
  { month: "يناير", sales: 4000, orders: 240 },
  { month: "فبراير", sales: 3000, orders: 198 },
  { month: "مارس", sales: 5000, orders: 320 },
  { month: "أبريل", sales: 4500, orders: 278 },
  { month: "مايو", sales: 6000, orders: 389 },
  { month: "يونيو", sales: 5500, orders: 350 },
  { month: "يوليو", sales: 7000, orders: 420 },
]

const revenueData = [
  { name: "المبيعات", value: 45000, color: "#10b981" },
  { name: "الخدمات", value: 25000, color: "#3b82f6" },
  { name: "الاشتراكات", value: 15000, color: "#8b5cf6" },
  { name: "أخرى", value: 5000, color: "#f59e0b" },
]

const topProducts = [
  { name: "منتج أ", sales: 1234, revenue: 45680, growth: 12.5 },
  { name: "منتج ب", sales: 987, revenue: 32450, growth: 8.3 },
  { name: "منتج ج", sales: 756, revenue: 28900, growth: -2.1 },
  { name: "منتج د", sales: 654, revenue: 21340, growth: 15.7 },
  { name: "منتج هـ", sales: 543, revenue: 18760, growth: 5.9 },
]

const recentActivities = [
  { id: 1, type: "order", message: "طلب جديد #12345 من أحمد محمد", time: "منذ 5 دقائق", status: "new" },
  { id: 2, type: "payment", message: "تم استلام دفعة 5,000 ر.س", time: "منذ 15 دقيقة", status: "success" },
  { id: 3, type: "stock", message: "تنبيه: انخفاض مخزون منتج X", time: "منذ 30 دقيقة", status: "warning" },
  { id: 4, type: "customer", message: "عميل جديد: شركة ABC", time: "منذ ساعة", status: "info" },
  { id: 5, type: "order", message: "تم شحن الطلب #12340", time: "منذ 2 ساعة", status: "success" },
]

const iotDevices = [
  { id: 1, name: "مستشعر درجة الحرارة", status: "online", value: "24°C", location: "المخزن أ" },
  { id: 2, name: "مستشعر الرطوبة", status: "online", value: "45%", location: "المخزن أ" },
  { id: 3, name: "عداد الطاقة", status: "online", value: "2.4kW", location: "المبنى الرئيسي" },
  { id: 4, name: "كاميرا مراقبة", status: "offline", value: "—", location: "المدخل" },
]

const StatCard = ({ title, value, change, icon: Icon, color, format }) => {
  const isPositive = change >= 0
  const colorClasses = {
    emerald: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400",
    blue: "bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400",
    purple: "bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400",
    orange: "bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400",
  }

  const formattedValue = format === "currency" ? formatCurrency(value) : formatNumber(value)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="hover:shadow-lg transition-shadow duration-300">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold">{formattedValue}</p>
              <div className={`flex items-center gap-1 text-sm ${isPositive ? "text-emerald-600" : "text-red-600"}`}>
                {isPositive ? (
                  <ArrowUpRight className="w-4 h-4" />
                ) : (
                  <ArrowDownRight className="w-4 h-4" />
                )}
                <span>{formatPercent(Math.abs(change))}</span>
                <span className="text-muted-foreground">من الشهر الماضي</span>
              </div>
            </div>
            <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
              <Icon className="w-6 h-6" />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [period, setPeriod] = useState("month")

  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => setIsLoading(false), 1500)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white">لوحة التحكم</h1>
          <p className="text-slate-600 dark:text-slate-400">مرحباً! إليك نظرة عامة على أداء عملك</p>
        </div>
        <div className="flex items-center gap-3">
          <Tabs value={period} onValueChange={setPeriod} className="w-auto">
            <TabsList className="bg-slate-100 dark:bg-slate-800">
              <TabsTrigger value="week">أسبوع</TabsTrigger>
              <TabsTrigger value="month">شهر</TabsTrigger>
              <TabsTrigger value="year">سنة</TabsTrigger>
            </TabsList>
          </Tabs>
          <Button variant="outline" size="icon" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsData.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sales Chart */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <div>
              <CardTitle className="text-lg">تحليل المبيعات</CardTitle>
              <CardDescription>مقارنة المبيعات والطلبات</CardDescription>
            </div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                  <MoreHorizontal className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>تصدير CSV</DropdownMenuItem>
                <DropdownMenuItem>تصدير PDF</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={salesChartData}>
                <defs>
                  <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorOrders" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="month" className="text-xs" />
                <YAxis className="text-xs" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="sales"
                  name="المبيعات"
                  stroke="#10b981"
                  fillOpacity={1}
                  fill="url(#colorSales)"
                />
                <Area
                  type="monotone"
                  dataKey="orders"
                  name="الطلبات"
                  stroke="#3b82f6"
                  fillOpacity={1}
                  fill="url(#colorOrders)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Revenue Pie Chart */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">توزيع الإيرادات</CardTitle>
            <CardDescription>حسب مصدر الدخل</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={revenueData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {revenueData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value) => formatCurrency(value)}
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Products */}
        <Card className="lg:col-span-2">
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">أفضل المنتجات مبيعاً</CardTitle>
            <CardDescription>الأداء خلال الفترة المحددة</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topProducts.map((product, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500 to-blue-500 flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <p className="font-medium">{product.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {formatNumber(product.sales)} مبيعة
                      </p>
                    </div>
                  </div>
                  <div className="text-left">
                    <p className="font-medium">{formatCurrency(product.revenue)}</p>
                    <p className={`text-sm flex items-center gap-1 ${product.growth >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                      {product.growth >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                      {formatPercent(Math.abs(product.growth))}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity & IoT Status */}
        <div className="space-y-6">
          {/* Recent Activity */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Activity className="w-5 h-5" />
                النشاط الأخير
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentActivities.slice(0, 4).map((activity) => (
                  <div key={activity.id} className="flex items-start gap-3 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.status === "success" ? "bg-emerald-500" :
                      activity.status === "warning" ? "bg-amber-500" :
                      activity.status === "new" ? "bg-blue-500" : "bg-slate-400"
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm truncate">{activity.message}</p>
                      <p className="text-xs text-muted-foreground">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* IoT Status */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Wifi className="w-5 h-5" />
                حالة أجهزة IoT
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {iotDevices.slice(0, 3).map((device) => (
                  <div key={device.id} className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${device.status === "online" ? "bg-emerald-500" : "bg-red-500"}`} />
                      <span className="text-sm font-medium">{device.name}</span>
                    </div>
                    <Badge variant={device.status === "online" ? "default" : "destructive"}>
                      {device.value}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* AI Insights Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card className="bg-gradient-to-r from-purple-500/10 via-blue-500/10 to-emerald-500/10 border-purple-200 dark:border-purple-800">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">رؤى الذكاء الاصطناعي</h3>
                  <p className="text-sm text-muted-foreground">
                    بناءً على تحليل البيانات، نتوقع زيادة المبيعات بنسبة 15% الشهر القادم
                  </p>
                </div>
              </div>
              <Button className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600">
                عرض التفاصيل
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export default Dashboard
