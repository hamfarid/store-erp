import { useState } from "react"
import { motion } from "framer-motion"
import {
  TestTube2,
  FlaskConical,
  Plus,
  Search,
  Filter,
  Download,
  Eye,
  Edit,
  BarChart3,
  Calendar,
  MapPin,
  Thermometer,
  Droplets,
  Sun,
  CheckCircle,
  Clock,
  AlertTriangle,
  TrendingUp,
  Leaf,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"

const VarietyTrialsPage = () => {
  const [activeTab, setActiveTab] = useState("trials")
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const summaryStats = [
    {
      title: "التجارب الجارية",
      value: "١٥",
      icon: TestTube2,
      color: "emerald",
    },
    {
      title: "الأصناف قيد الاختبار",
      value: "٤٢",
      icon: Leaf,
      color: "blue",
    },
    {
      title: "المواقع التجريبية",
      value: "٨",
      icon: MapPin,
      color: "amber",
    },
    {
      title: "التجارب المكتملة",
      value: "٢٣",
      icon: CheckCircle,
      color: "green",
    },
  ]

  const trials = [
    {
      id: "VT-2025-001",
      name: "تجربة طماطم هجين",
      variety: "طماطم - سوبر ريد",
      location: "مزرعة الشمال",
      startDate: "2025-01-01",
      endDate: "2025-06-30",
      status: "جاري",
      progress: 35,
      parameters: { temp: "25°C", humidity: "65%", light: "جيد" },
    },
    {
      id: "VT-2025-002",
      name: "اختبار مقاومة الجفاف",
      variety: "قمح - نوع أ",
      location: "مزرعة الجنوب",
      startDate: "2024-10-15",
      endDate: "2025-04-15",
      status: "جاري",
      progress: 60,
      parameters: { temp: "22°C", humidity: "40%", light: "ممتاز" },
    },
    {
      id: "VT-2024-015",
      name: "تجربة إنتاجية الفلفل",
      variety: "فلفل - كاليفورنيا",
      location: "مزرعة الشرق",
      startDate: "2024-08-01",
      endDate: "2024-12-31",
      status: "مكتمل",
      progress: 100,
      parameters: { temp: "28°C", humidity: "55%", light: "جيد" },
    },
  ]

  const getStatusBadge = (status) => {
    const config = {
      "جاري": { color: "bg-blue-500", icon: Clock },
      "مكتمل": { color: "bg-emerald-500", icon: CheckCircle },
      "معلق": { color: "bg-amber-500", icon: AlertTriangle },
      "ملغي": { color: "bg-red-500", icon: AlertTriangle },
    }
    const { color, icon: Icon } = config[status] || config["جاري"]
    return (
      <Badge className={color}>
        <Icon className="w-3 h-3 ml-1" />
        {status}
      </Badge>
    )
  }

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <TestTube2 className="w-8 h-8 text-emerald-500" />
            تجارب الأصناف
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة تجارب واختبارات الأصناف الزراعية
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 ml-2" />
            تصدير البيانات
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <Plus className="w-4 h-4 ml-2" />
            تجربة جديدة
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="border-0 shadow-lg bg-white dark:bg-slate-900">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`w-12 h-12 rounded-xl bg-${stat.color}-100 dark:bg-${stat.color}-900/30 flex items-center justify-center`}>
                    <stat.icon className={`w-6 h-6 text-${stat.color}-500`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800 p-1">
          <TabsTrigger value="trials" className="flex items-center gap-2">
            <FlaskConical className="w-4 h-4" />
            التجارب
          </TabsTrigger>
          <TabsTrigger value="results" className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4" />
            النتائج
          </TabsTrigger>
          <TabsTrigger value="compare" className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            المقارنة
          </TabsTrigger>
        </TabsList>

        {/* Trials Tab */}
        <TabsContent value="trials" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle>قائمة التجارب</CardTitle>
                <div className="flex gap-3">
                  <div className="relative">
                    <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="بحث..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pr-9 w-64"
                    />
                  </div>
                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger className="w-40">
                      <SelectValue placeholder="الحالة" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">الكل</SelectItem>
                      <SelectItem value="active">جاري</SelectItem>
                      <SelectItem value="completed">مكتمل</SelectItem>
                      <SelectItem value="pending">معلق</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {trials.map((trial, index) => (
                  <motion.div
                    key={trial.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-emerald-300 transition-colors"
                  >
                    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                          <FlaskConical className="w-6 h-6 text-emerald-500" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium text-slate-800 dark:text-white">
                              {trial.name}
                            </h4>
                            <span className="text-xs text-slate-400 font-mono">
                              {trial.id}
                            </span>
                          </div>
                          <p className="text-sm text-slate-500 mt-1">
                            <Leaf className="w-3 h-3 inline ml-1" />
                            {trial.variety}
                          </p>
                          <div className="flex items-center gap-4 mt-2 text-xs text-slate-400">
                            <span>
                              <MapPin className="w-3 h-3 inline ml-1" />
                              {trial.location}
                            </span>
                            <span>
                              <Calendar className="w-3 h-3 inline ml-1" />
                              {trial.startDate} - {trial.endDate}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        {getStatusBadge(trial.status)}
                        <div className="flex items-center gap-4 text-xs">
                          <span className="flex items-center gap-1 text-slate-500">
                            <Thermometer className="w-3 h-3" />
                            {trial.parameters.temp}
                          </span>
                          <span className="flex items-center gap-1 text-slate-500">
                            <Droplets className="w-3 h-3" />
                            {trial.parameters.humidity}
                          </span>
                          <span className="flex items-center gap-1 text-slate-500">
                            <Sun className="w-3 h-3" />
                            {trial.parameters.light}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-slate-500">التقدم</span>
                        <span className="text-xs font-medium">{trial.progress}%</span>
                      </div>
                      <Progress value={trial.progress} className="h-2" />
                    </div>
                    <div className="flex justify-end gap-2 mt-4">
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 ml-1" />
                        عرض
                      </Button>
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4 ml-1" />
                        تعديل
                      </Button>
                      <Button variant="outline" size="sm">
                        <BarChart3 className="w-4 h-4 ml-1" />
                        النتائج
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Results Tab */}
        <TabsContent value="results" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>نتائج التجارب</CardTitle>
              <CardDescription>
                تحليل ومقارنة نتائج التجارب المكتملة
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [رسوم بيانية لنتائج التجارب]
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Compare Tab */}
        <TabsContent value="compare" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>مقارنة الأصناف</CardTitle>
              <CardDescription>
                مقارنة أداء الأصناف المختلفة
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [جدول مقارنة الأصناف]
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default VarietyTrialsPage
