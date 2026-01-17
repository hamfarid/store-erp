import { useState } from "react"
import { motion } from "framer-motion"
import {
  FileText,
  Download,
  Calendar,
  Filter,
  PieChart,
  BarChart3,
  TrendingUp,
  FileSpreadsheet,
  Printer,
  Mail,
  Clock,
  CheckCircle,
  Eye,
  Settings,
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
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const ReportsPage = () => {
  const [activeTab, setActiveTab] = useState("all")
  const [dateRange, setDateRange] = useState("month")

  const reportCategories = [
    {
      title: "التقارير المالية",
      icon: TrendingUp,
      color: "emerald",
      reports: [
        { name: "الميزانية العمومية", type: "مالي" },
        { name: "قائمة الدخل", type: "مالي" },
        { name: "التدفق النقدي", type: "مالي" },
        { name: "تقرير الأرباح والخسائر", type: "مالي" },
      ],
    },
    {
      title: "تقارير المبيعات",
      icon: BarChart3,
      color: "blue",
      reports: [
        { name: "المبيعات اليومية", type: "مبيعات" },
        { name: "أداء المنتجات", type: "مبيعات" },
        { name: "تحليل العملاء", type: "مبيعات" },
        { name: "تقرير الفواتير", type: "مبيعات" },
      ],
    },
    {
      title: "تقارير المخزون",
      icon: FileSpreadsheet,
      color: "amber",
      reports: [
        { name: "جرد المخزون", type: "مخزون" },
        { name: "حركة المخزون", type: "مخزون" },
        { name: "المنتجات منخفضة المخزون", type: "مخزون" },
        { name: "تقرير التلف والفاقد", type: "مخزون" },
      ],
    },
    {
      title: "تقارير الإنتاج",
      icon: PieChart,
      color: "purple",
      reports: [
        { name: "أوامر الإنتاج", type: "إنتاج" },
        { name: "كفاءة الإنتاج", type: "إنتاج" },
        { name: "تقرير الجودة", type: "إنتاج" },
        { name: "تكاليف الإنتاج", type: "إنتاج" },
      ],
    },
  ]

  const recentReports = [
    {
      name: "تقرير المبيعات الشهري",
      date: "2025-01-17",
      status: "جاهز",
      size: "2.5 MB",
    },
    {
      name: "جرد المخزون Q4",
      date: "2025-01-15",
      status: "جاهز",
      size: "4.8 MB",
    },
    {
      name: "تقرير الأرباح السنوي",
      date: "2025-01-10",
      status: "قيد المعالجة",
      size: "-",
    },
  ]

  const scheduledReports = [
    { name: "تقرير المبيعات اليومي", frequency: "يومياً", time: "08:00" },
    { name: "تقرير المخزون الأسبوعي", frequency: "أسبوعياً", time: "الأحد 09:00" },
    { name: "الميزانية العمومية", frequency: "شهرياً", time: "١ من كل شهر" },
  ]

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <FileText className="w-8 h-8 text-emerald-500" />
            التقارير
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إنشاء وإدارة التقارير
          </p>
        </div>
        <div className="flex gap-3">
          <Select value={dateRange} onValueChange={setDateRange}>
            <SelectTrigger className="w-40">
              <Calendar className="w-4 h-4 ml-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="today">اليوم</SelectItem>
              <SelectItem value="week">هذا الأسبوع</SelectItem>
              <SelectItem value="month">هذا الشهر</SelectItem>
              <SelectItem value="quarter">هذا الربع</SelectItem>
              <SelectItem value="year">هذه السنة</SelectItem>
            </SelectContent>
          </Select>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <FileText className="w-4 h-4 ml-2" />
            تقرير جديد
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800 p-1">
          <TabsTrigger value="all" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            جميع التقارير
          </TabsTrigger>
          <TabsTrigger value="recent" className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            الأخيرة
          </TabsTrigger>
          <TabsTrigger value="scheduled" className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            المجدولة
          </TabsTrigger>
          <TabsTrigger value="custom" className="flex items-center gap-2">
            <Settings className="w-4 h-4" />
            مخصصة
          </TabsTrigger>
        </TabsList>

        {/* All Reports Tab */}
        <TabsContent value="all" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {reportCategories.map((category, index) => (
              <motion.div
                key={category.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <category.icon className={`w-5 h-5 text-${category.color}-500`} />
                      {category.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {category.reports.map((report) => (
                        <div
                          key={report.name}
                          className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors cursor-pointer"
                        >
                          <div className="flex items-center gap-3">
                            <FileText className="w-4 h-4 text-slate-400" />
                            <span className="text-slate-700 dark:text-slate-200">
                              {report.name}
                            </span>
                          </div>
                          <div className="flex gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Download className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {/* Recent Reports Tab */}
        <TabsContent value="recent" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>التقارير الأخيرة</CardTitle>
              <CardDescription>التقارير التي تم إنشاؤها مؤخراً</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentReports.map((report, index) => (
                  <motion.div
                    key={report.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                        <FileText className="w-5 h-5 text-emerald-500" />
                      </div>
                      <div>
                        <h4 className="font-medium text-slate-800 dark:text-white">
                          {report.name}
                        </h4>
                        <p className="text-sm text-slate-500">
                          {report.date} • {report.size}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge
                        className={
                          report.status === "جاهز"
                            ? "bg-emerald-500"
                            : "bg-amber-500"
                        }
                      >
                        {report.status === "جاهز" ? (
                          <CheckCircle className="w-3 h-3 ml-1" />
                        ) : (
                          <Clock className="w-3 h-3 ml-1" />
                        )}
                        {report.status}
                      </Badge>
                      {report.status === "جاهز" && (
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Eye className="w-4 h-4 ml-1" />
                            عرض
                          </Button>
                          <Button variant="outline" size="sm">
                            <Download className="w-4 h-4 ml-1" />
                            تحميل
                          </Button>
                          <Button variant="outline" size="sm">
                            <Printer className="w-4 h-4 ml-1" />
                            طباعة
                          </Button>
                          <Button variant="outline" size="sm">
                            <Mail className="w-4 h-4 ml-1" />
                            إرسال
                          </Button>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Scheduled Reports Tab */}
        <TabsContent value="scheduled" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>التقارير المجدولة</CardTitle>
                  <CardDescription>التقارير التي يتم إنشاؤها تلقائياً</CardDescription>
                </div>
                <Button className="bg-emerald-500 hover:bg-emerald-600">
                  <Calendar className="w-4 h-4 ml-2" />
                  جدولة تقرير
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {scheduledReports.map((report, index) => (
                  <motion.div
                    key={report.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                        <Calendar className="w-5 h-5 text-blue-500" />
                      </div>
                      <div>
                        <h4 className="font-medium text-slate-800 dark:text-white">
                          {report.name}
                        </h4>
                        <p className="text-sm text-slate-500">
                          {report.frequency} • {report.time}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">{report.frequency}</Badge>
                      <Button variant="ghost" size="sm">
                        <Settings className="w-4 h-4" />
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Custom Reports Tab */}
        <TabsContent value="custom" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>إنشاء تقرير مخصص</CardTitle>
              <CardDescription>
                اختر البيانات والفترة الزمنية لإنشاء تقرير مخصص
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [نموذج إنشاء تقرير مخصص]
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ReportsPage
