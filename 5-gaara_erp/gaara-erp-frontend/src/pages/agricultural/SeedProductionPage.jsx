import { useState } from "react"
import { motion } from "framer-motion"
import {
  Wheat,
  Sprout,
  Plus,
  Search,
  Download,
  Eye,
  Edit,
  Calendar,
  Package,
  CheckCircle,
  Clock,
  AlertTriangle,
  TrendingUp,
  BarChart3,
  Boxes,
  Scale,
  TestTube2,
  Truck,
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
import { Progress } from "@/components/ui/progress"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const SeedProductionPage = () => {
  const [activeTab, setActiveTab] = useState("batches")
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const summaryStats = [
    {
      title: "دفعات الإنتاج النشطة",
      value: "١٢",
      icon: Boxes,
      color: "emerald",
    },
    {
      title: "إجمالي الإنتاج (كجم)",
      value: "٤٥,٠٠٠",
      icon: Scale,
      color: "blue",
    },
    {
      title: "الأصناف المنتجة",
      value: "١٨",
      icon: Sprout,
      color: "amber",
    },
    {
      title: "معدل الإنبات",
      value: "٩٢%",
      icon: TrendingUp,
      color: "green",
    },
  ]

  const productionBatches = [
    {
      id: "SP-2025-001",
      variety: "طماطم سوبر",
      quantity: 5000,
      unit: "كجم",
      startDate: "2025-01-05",
      expectedDate: "2025-03-15",
      status: "قيد الإنتاج",
      progress: 45,
      germination: 94,
      purity: 98.5,
    },
    {
      id: "SP-2025-002",
      variety: "فلفل حلو",
      quantity: 2500,
      unit: "كجم",
      startDate: "2024-12-20",
      expectedDate: "2025-02-28",
      status: "اختبار الجودة",
      progress: 80,
      germination: 91,
      purity: 97.8,
    },
    {
      id: "SP-2024-045",
      variety: "باذنجان",
      quantity: 3000,
      unit: "كجم",
      startDate: "2024-10-01",
      expectedDate: "2024-12-30",
      status: "مكتمل",
      progress: 100,
      germination: 93,
      purity: 99.1,
    },
  ]

  const qualityTests = [
    { test: "اختبار الإنبات", standard: "85%", min: "80%", method: "ISTA" },
    { test: "نقاوة البذور", standard: "98%", min: "95%", method: "ISTA" },
    { test: "رطوبة البذور", standard: "8%", min: "6%", method: "قياس مباشر" },
    { test: "فحص الأمراض", standard: "0%", min: "0%", method: "PCR" },
  ]

  const getStatusBadge = (status) => {
    const config = {
      "قيد الإنتاج": { color: "bg-blue-500", icon: Clock },
      "اختبار الجودة": { color: "bg-amber-500", icon: TestTube2 },
      "مكتمل": { color: "bg-emerald-500", icon: CheckCircle },
      "جاهز للشحن": { color: "bg-purple-500", icon: Truck },
    }
    const { color, icon: Icon } = config[status] || config["قيد الإنتاج"]
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
            <Wheat className="w-8 h-8 text-emerald-500" />
            إنتاج البذور
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة عمليات إنتاج وتجهيز البذور
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <Plus className="w-4 h-4 ml-2" />
            دفعة إنتاج جديدة
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
          <TabsTrigger value="batches" className="flex items-center gap-2">
            <Boxes className="w-4 h-4" />
            دفعات الإنتاج
          </TabsTrigger>
          <TabsTrigger value="quality" className="flex items-center gap-2">
            <TestTube2 className="w-4 h-4" />
            الجودة
          </TabsTrigger>
          <TabsTrigger value="inventory" className="flex items-center gap-2">
            <Package className="w-4 h-4" />
            المخزون
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4" />
            التقارير
          </TabsTrigger>
        </TabsList>

        {/* Batches Tab */}
        <TabsContent value="batches" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle>دفعات الإنتاج</CardTitle>
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
                      <SelectItem value="production">قيد الإنتاج</SelectItem>
                      <SelectItem value="testing">اختبار الجودة</SelectItem>
                      <SelectItem value="completed">مكتمل</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {productionBatches.map((batch, index) => (
                  <motion.div
                    key={batch.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-emerald-300 transition-colors"
                  >
                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                          <Sprout className="w-6 h-6 text-emerald-500" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium text-slate-800 dark:text-white">
                              {batch.variety}
                            </h4>
                            <span className="text-xs text-slate-400 font-mono">
                              {batch.id}
                            </span>
                          </div>
                          <div className="flex items-center gap-4 mt-2 text-sm text-slate-500">
                            <span>
                              <Scale className="w-3 h-3 inline ml-1" />
                              {batch.quantity.toLocaleString()} {batch.unit}
                            </span>
                            <span>
                              <Calendar className="w-3 h-3 inline ml-1" />
                              {batch.startDate} → {batch.expectedDate}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        {getStatusBadge(batch.status)}
                        <div className="flex items-center gap-4 text-xs text-slate-500">
                          <span>إنبات: {batch.germination}%</span>
                          <span>نقاوة: {batch.purity}%</span>
                        </div>
                      </div>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-slate-500">التقدم</span>
                        <span className="text-xs font-medium">{batch.progress}%</span>
                      </div>
                      <Progress value={batch.progress} className="h-2" />
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
                        <TestTube2 className="w-4 h-4 ml-1" />
                        فحص الجودة
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Quality Tab */}
        <TabsContent value="quality" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>معايير الجودة</CardTitle>
              <CardDescription>
                معايير واختبارات جودة البذور
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>الاختبار</TableHead>
                    <TableHead>المعيار المطلوب</TableHead>
                    <TableHead>الحد الأدنى</TableHead>
                    <TableHead>طريقة الفحص</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {qualityTests.map((test) => (
                    <TableRow key={test.test}>
                      <TableCell className="font-medium">{test.test}</TableCell>
                      <TableCell>
                        <Badge className="bg-emerald-500">{test.standard}</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{test.min}</Badge>
                      </TableCell>
                      <TableCell>{test.method}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Inventory Tab */}
        <TabsContent value="inventory" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>مخزون البذور</CardTitle>
              <CardDescription>
                جرد وإدارة مخزون البذور الجاهزة
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [جدول مخزون البذور]
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>تقارير الإنتاج</CardTitle>
              <CardDescription>
                تقارير وإحصائيات إنتاج البذور
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [رسوم بيانية لإنتاج البذور]
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default SeedProductionPage
