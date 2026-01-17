import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Brain,
  TrendingUp,
  TrendingDown,
  Target,
  Lightbulb,
  AlertCircle,
  CheckCircle2,
  BarChart3,
  PieChart,
  LineChart as LineChartIcon,
  Sparkles,
  RefreshCw,
  Download,
  Calendar,
  DollarSign,
  Package,
  Users,
  ShoppingCart,
  ArrowUpRight,
  ArrowDownRight,
  Zap,
} from "lucide-react"
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart as RechartsPie,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"

import { StatsCard } from "@/components/common"
import { formatCurrency, formatNumber, formatPercent } from "@/lib/utils"

// Mock prediction data
const salesPredictions = [
  { month: "يناير", actual: 120000, predicted: 115000 },
  { month: "فبراير", actual: 135000, predicted: 128000 },
  { month: "مارس", actual: 142000, predicted: 145000 },
  { month: "أبريل", actual: 158000, predicted: 152000 },
  { month: "مايو", actual: 165000, predicted: 168000 },
  { month: "يونيو", actual: 172000, predicted: 175000 },
  { month: "يوليو", actual: null, predicted: 185000 },
  { month: "أغسطس", actual: null, predicted: 192000 },
  { month: "سبتمبر", actual: null, predicted: 188000 },
]

const demandForecast = [
  { product: "بذور طماطم", current: 500, predicted: 650, trend: "up" },
  { product: "سماد NPK", current: 300, predicted: 280, trend: "down" },
  { product: "مبيدات", current: 200, predicted: 350, trend: "up" },
  { product: "شتلات فراولة", current: 1000, predicted: 1200, trend: "up" },
  { product: "أدوات ري", current: 150, predicted: 120, trend: "down" },
]

const customerSegments = [
  { name: "عملاء VIP", value: 15, color: "#10b981" },
  { name: "عملاء نشطين", value: 35, color: "#3b82f6" },
  { name: "عملاء عاديين", value: 30, color: "#8b5cf6" },
  { name: "عملاء جدد", value: 20, color: "#f59e0b" },
]

const performanceRadar = [
  { metric: "المبيعات", value: 85 },
  { metric: "رضا العملاء", value: 92 },
  { metric: "كفاءة المخزون", value: 78 },
  { metric: "الربحية", value: 88 },
  { metric: "النمو", value: 75 },
  { metric: "الابتكار", value: 70 },
]

const insights = [
  {
    id: 1,
    type: "opportunity",
    title: "فرصة زيادة المبيعات",
    description: "تحليل البيانات يشير إلى إمكانية زيادة المبيعات بنسبة 15% من خلال استهداف قطاع الزراعة العضوية",
    impact: "high",
    confidence: 87,
    action: "إنشاء حملة تسويقية موجهة",
  },
  {
    id: 2,
    type: "warning",
    title: "انخفاض متوقع في الطلب",
    description: "التنبؤات تشير إلى انخفاض الطلب على السماد بنسبة 10% الشهر القادم بسبب الموسمية",
    impact: "medium",
    confidence: 82,
    action: "تعديل خطة المشتريات",
  },
  {
    id: 3,
    type: "success",
    title: "أداء ممتاز في المبيعات",
    description: "تجاوزت المبيعات التوقعات بنسبة 8% هذا الشهر، مع تحسن ملحوظ في معدل التحويل",
    impact: "positive",
    confidence: 95,
    action: "الاستمرار في الاستراتيجية الحالية",
  },
  {
    id: 4,
    type: "recommendation",
    title: "تحسين إدارة المخزون",
    description: "يوصى بتقليل مخزون 3 منتجات بطيئة الحركة وزيادة مخزون المنتجات الأكثر طلباً",
    impact: "medium",
    confidence: 79,
    action: "مراجعة سياسة المخزون",
  },
]

const AIAnalytics = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState("predictions")
  const [isLoading, setIsLoading] = useState(false)
  const [selectedPeriod, setSelectedPeriod] = useState("month")

  // Set active tab based on URL
  useEffect(() => {
    if (location.pathname.includes("/predictions")) setActiveTab("predictions")
    else if (location.pathname.includes("/data-analysis")) setActiveTab("analysis")
    else if (location.pathname.includes("/smart-reports")) setActiveTab("reports")
  }, [location])

  // Stats
  const predictionAccuracy = 92
  const insightsGenerated = 156
  const decisionsOptimized = 89
  const timeSaved = 120

  // Refresh predictions
  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
      toast.success("تم تحديث التنبؤات بنجاح")
    }, 2000)
  }

  // Insight Card Component
  const InsightCard = ({ insight }) => {
    const icons = {
      opportunity: Lightbulb,
      warning: AlertCircle,
      success: CheckCircle2,
      recommendation: Target,
    }
    const colors = {
      opportunity: "text-blue-500 bg-blue-100 dark:bg-blue-900/30",
      warning: "text-amber-500 bg-amber-100 dark:bg-amber-900/30",
      success: "text-emerald-500 bg-emerald-100 dark:bg-emerald-900/30",
      recommendation: "text-purple-500 bg-purple-100 dark:bg-purple-900/30",
    }
    const Icon = icons[insight.type]

    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-4 border rounded-lg hover:shadow-md transition-shadow"
      >
        <div className="flex items-start gap-4">
          <div className={`p-2 rounded-lg ${colors[insight.type]}`}>
            <Icon className="w-5 h-5" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="font-medium">{insight.title}</h4>
              <Badge variant="outline" className="text-xs">
                ثقة {insight.confidence}%
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">{insight.description}</p>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                الإجراء المقترح: {insight.action}
              </span>
              <Button variant="ghost" size="sm">
                تطبيق
              </Button>
            </div>
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Brain className="w-7 h-7 text-purple-500" />
            التحليلات الذكية
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            تحليلات متقدمة مدعومة بالذكاء الاصطناعي
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="week">أسبوع</SelectItem>
              <SelectItem value="month">شهر</SelectItem>
              <SelectItem value="quarter">ربع سنة</SelectItem>
              <SelectItem value="year">سنة</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? "animate-spin" : ""}`} />
            تحديث
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="دقة التنبؤات"
          value={predictionAccuracy}
          format="percent"
          icon={Target}
          color="emerald"
          delay={0}
        />
        <StatsCard
          title="رؤى مُولّدة"
          value={insightsGenerated}
          change={23}
          icon={Lightbulb}
          color="blue"
          delay={0.1}
        />
        <StatsCard
          title="قرارات محسّنة"
          value={decisionsOptimized}
          icon={Sparkles}
          color="purple"
          delay={0.2}
        />
        <StatsCard
          title="وقت موفّر (ساعة)"
          value={timeSaved}
          icon={Zap}
          color="amber"
          delay={0.3}
        />
      </div>

      {/* AI Insights Banner */}
      <Card className="bg-gradient-to-r from-purple-500/10 via-blue-500/10 to-emerald-500/10 border-purple-200 dark:border-purple-800">
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">رؤى الذكاء الاصطناعي اليوم</h3>
                <p className="text-sm text-muted-foreground">
                  تم تحليل {formatNumber(15420)} نقطة بيانات وتوليد {insights.length} رؤى جديدة
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="gap-1">
                <Sparkles className="w-3 h-3" />
                تحديث مباشر
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="predictions" className="gap-2">
            <TrendingUp className="w-4 h-4" />
            التنبؤات
          </TabsTrigger>
          <TabsTrigger value="analysis" className="gap-2">
            <BarChart3 className="w-4 h-4" />
            تحليل البيانات
          </TabsTrigger>
          <TabsTrigger value="reports" className="gap-2">
            <LineChartIcon className="w-4 h-4" />
            التقارير الذكية
          </TabsTrigger>
        </TabsList>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="mt-6 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sales Forecast Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-emerald-500" />
                  توقعات المبيعات
                </CardTitle>
                <CardDescription>المبيعات الفعلية مقابل التوقعات</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                  <AreaChart data={salesPredictions}>
                    <defs>
                      <linearGradient id="actualGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="predictedGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis dataKey="month" className="text-xs" />
                    <YAxis className="text-xs" tickFormatter={(val) => `${val / 1000}k`} />
                    <Tooltip
                      formatter={(val) => formatCurrency(val)}
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="actual"
                      name="الفعلي"
                      stroke="#10b981"
                      fill="url(#actualGradient)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="predicted"
                      name="المتوقع"
                      stroke="#8b5cf6"
                      fill="url(#predictedGradient)"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Demand Forecast */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Package className="w-5 h-5 text-blue-500" />
                  توقعات الطلب
                </CardTitle>
                <CardDescription>التغير المتوقع في الطلب</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {demandForecast.map((item, index) => (
                  <motion.div
                    key={item.product}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium">{item.product}</p>
                      <p className="text-sm text-muted-foreground">
                        الحالي: {formatNumber(item.current)} → المتوقع: {formatNumber(item.predicted)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      {item.trend === "up" ? (
                        <ArrowUpRight className="w-5 h-5 text-emerald-500" />
                      ) : (
                        <ArrowDownRight className="w-5 h-5 text-red-500" />
                      )}
                      <span
                        className={`font-medium ${
                          item.trend === "up" ? "text-emerald-600" : "text-red-600"
                        }`}
                      >
                        {formatPercent(Math.abs((item.predicted - item.current) / item.current) * 100)}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </CardContent>
            </Card>

            {/* Customer Segments */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-purple-500" />
                  تصنيف العملاء
                </CardTitle>
                <CardDescription>توزيع العملاء حسب الفئة</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <RechartsPie>
                    <Pie
                      data={customerSegments}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {customerSegments.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(val) => `${val}%`} />
                    <Legend />
                  </RechartsPie>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Data Analysis Tab */}
        <TabsContent value="analysis" className="mt-6 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Performance Radar */}
            <Card>
              <CardHeader>
                <CardTitle>تحليل الأداء</CardTitle>
                <CardDescription>مؤشرات الأداء الرئيسية</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={performanceRadar}>
                    <PolarGrid className="stroke-muted" />
                    <PolarAngleAxis dataKey="metric" className="text-xs" />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} />
                    <Radar
                      name="الأداء"
                      dataKey="value"
                      stroke="#8b5cf6"
                      fill="#8b5cf6"
                      fillOpacity={0.3}
                    />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* AI Insights */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-amber-500" />
                  الرؤى الذكية
                </CardTitle>
                <CardDescription>توصيات مبنية على التحليل</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 max-h-[400px] overflow-y-auto">
                {insights.map((insight) => (
                  <InsightCard key={insight.id} insight={insight} />
                ))}
              </CardContent>
            </Card>

            {/* Key Metrics */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>المقاييس الرئيسية</CardTitle>
                <CardDescription>تحليل مقارن للأداء</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { label: "معدل التحويل", value: 12.5, target: 15, unit: "%" },
                    { label: "متوسط قيمة الطلب", value: 2450, target: 2800, unit: "ر.س" },
                    { label: "معدل الاحتفاظ", value: 78, target: 85, unit: "%" },
                    { label: "رضا العملاء", value: 4.2, target: 4.5, unit: "/5" },
                  ].map((metric, index) => (
                    <motion.div
                      key={metric.label}
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 }}
                      className="p-4 border rounded-lg"
                    >
                      <p className="text-sm text-muted-foreground mb-2">{metric.label}</p>
                      <div className="flex items-end gap-1 mb-2">
                        <span className="text-2xl font-bold">{metric.value}</span>
                        <span className="text-sm text-muted-foreground">{metric.unit}</span>
                      </div>
                      <div className="space-y-1">
                        <Progress value={(metric.value / metric.target) * 100} className="h-2" />
                        <p className="text-xs text-muted-foreground">
                          الهدف: {metric.target}{metric.unit}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Smart Reports Tab */}
        <TabsContent value="reports" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { title: "تقرير المبيعات الذكي", icon: ShoppingCart, color: "emerald", description: "تحليل شامل للمبيعات مع توصيات" },
              { title: "تقرير العملاء", icon: Users, color: "blue", description: "تصنيف وتحليل سلوك العملاء" },
              { title: "تقرير المخزون", icon: Package, color: "purple", description: "تحسين مستويات المخزون" },
              { title: "تقرير الأرباح", icon: DollarSign, color: "amber", description: "تحليل الربحية والهوامش" },
              { title: "تقرير التنبؤات", icon: TrendingUp, color: "cyan", description: "توقعات الأداء المستقبلي" },
              { title: "تقرير مخصص", icon: Sparkles, color: "pink", description: "إنشاء تقرير حسب الطلب" },
            ].map((report, index) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="cursor-pointer hover:shadow-lg transition-all group">
                  <CardContent className="p-6">
                    <div className="flex items-start gap-4">
                      <div className={`p-3 rounded-xl bg-${report.color}-100 dark:bg-${report.color}-900/30 group-hover:scale-110 transition-transform`}>
                        <report.icon className={`w-6 h-6 text-${report.color}-600`} />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium mb-1">{report.title}</h3>
                        <p className="text-sm text-muted-foreground mb-3">{report.description}</p>
                        <div className="flex items-center gap-2">
                          <Button variant="outline" size="sm" className="gap-1">
                            <Download className="w-3 h-3" />
                            PDF
                          </Button>
                          <Button variant="outline" size="sm" className="gap-1">
                            <Download className="w-3 h-3" />
                            Excel
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AIAnalytics
