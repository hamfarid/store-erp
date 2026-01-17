import { useState } from "react"
import { motion } from "framer-motion"
import {
  ShoppingCart,
  Package,
  Truck,
  Building2,
  FileText,
  Clock,
  CheckCircle,
  XCircle,
  Plus,
  Search,
  Filter,
  Download,
  Eye,
  Edit,
  Trash2,
  ArrowUpRight,
  AlertTriangle,
  DollarSign,
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

const PurchasingPage = () => {
  const [activeTab, setActiveTab] = useState("orders")
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  // Mock data
  const summaryStats = [
    {
      title: "إجمالي المشتريات",
      value: "٢٤٥,٠٠٠",
      subtext: "هذا الشهر",
      icon: ShoppingCart,
      color: "emerald",
    },
    {
      title: "أوامر الشراء المعلقة",
      value: "١٢",
      subtext: "بانتظار الموافقة",
      icon: Clock,
      color: "amber",
    },
    {
      title: "الشحنات الواردة",
      value: "٨",
      subtext: "في الطريق",
      icon: Truck,
      color: "blue",
    },
    {
      title: "موردون نشطون",
      value: "٣٤",
      subtext: "مسجلون",
      icon: Building2,
      color: "purple",
    },
  ]

  const purchaseOrders = [
    {
      id: "PO-2025-001",
      supplier: "شركة البذور العالمية",
      date: "2025-01-15",
      items: 5,
      total: 45000,
      status: "مكتمل",
      delivery: "2025-01-20",
    },
    {
      id: "PO-2025-002",
      supplier: "مؤسسة الأسمدة",
      date: "2025-01-16",
      items: 3,
      total: 28500,
      status: "قيد التنفيذ",
      delivery: "2025-01-25",
    },
    {
      id: "PO-2025-003",
      supplier: "شركة المعدات الزراعية",
      date: "2025-01-17",
      items: 2,
      total: 85000,
      status: "معلق",
      delivery: "-",
    },
    {
      id: "PO-2025-004",
      supplier: "مصنع التعبئة والتغليف",
      date: "2025-01-17",
      items: 8,
      total: 15000,
      status: "ملغي",
      delivery: "-",
    },
  ]

  const suppliers = [
    {
      id: 1,
      name: "شركة البذور العالمية",
      category: "بذور",
      rating: 4.8,
      orders: 25,
      total: 450000,
      status: "نشط",
    },
    {
      id: 2,
      name: "مؤسسة الأسمدة",
      category: "أسمدة",
      rating: 4.5,
      orders: 18,
      total: 320000,
      status: "نشط",
    },
    {
      id: 3,
      name: "شركة المعدات الزراعية",
      category: "معدات",
      rating: 4.2,
      orders: 8,
      total: 580000,
      status: "نشط",
    },
  ]

  const getStatusBadge = (status) => {
    const statusConfig = {
      "مكتمل": { variant: "default", icon: CheckCircle, className: "bg-emerald-500" },
      "قيد التنفيذ": { variant: "default", icon: Truck, className: "bg-blue-500" },
      "معلق": { variant: "default", icon: Clock, className: "bg-amber-500" },
      "ملغي": { variant: "destructive", icon: XCircle },
    }
    const config = statusConfig[status] || statusConfig["معلق"]
    return (
      <Badge variant={config.variant} className={config.className}>
        <config.icon className="w-3 h-3 ml-1" />
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
            <ShoppingCart className="w-8 h-8 text-emerald-500" />
            المشتريات
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة أوامر الشراء والموردين والمخزون
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <Plus className="w-4 h-4 ml-2" />
            أمر شراء جديد
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
                      {stat.title === "إجمالي المشتريات" && " ر.س"}
                    </p>
                    <p className="text-xs text-slate-400 mt-1">{stat.subtext}</p>
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
          <TabsTrigger value="orders" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            أوامر الشراء
          </TabsTrigger>
          <TabsTrigger value="suppliers" className="flex items-center gap-2">
            <Building2 className="w-4 h-4" />
            الموردون
          </TabsTrigger>
          <TabsTrigger value="receiving" className="flex items-center gap-2">
            <Package className="w-4 h-4" />
            الاستلام
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center gap-2">
            <DollarSign className="w-4 h-4" />
            التقارير
          </TabsTrigger>
        </TabsList>

        {/* Purchase Orders Tab */}
        <TabsContent value="orders" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle>أوامر الشراء</CardTitle>
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
                      <SelectItem value="pending">معلق</SelectItem>
                      <SelectItem value="progress">قيد التنفيذ</SelectItem>
                      <SelectItem value="completed">مكتمل</SelectItem>
                      <SelectItem value="cancelled">ملغي</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>رقم الأمر</TableHead>
                    <TableHead>المورد</TableHead>
                    <TableHead>التاريخ</TableHead>
                    <TableHead>الأصناف</TableHead>
                    <TableHead>الإجمالي</TableHead>
                    <TableHead>التسليم</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {purchaseOrders.map((order) => (
                    <TableRow key={order.id}>
                      <TableCell className="font-mono font-medium">
                        {order.id}
                      </TableCell>
                      <TableCell>{order.supplier}</TableCell>
                      <TableCell>{order.date}</TableCell>
                      <TableCell>{order.items} أصناف</TableCell>
                      <TableCell>{order.total.toLocaleString()} ر.س</TableCell>
                      <TableCell>{order.delivery}</TableCell>
                      <TableCell>{getStatusBadge(order.status)}</TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Edit className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Suppliers Tab */}
        <TabsContent value="suppliers" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>قائمة الموردين</CardTitle>
                <Button className="bg-emerald-500 hover:bg-emerald-600">
                  <Plus className="w-4 h-4 ml-2" />
                  إضافة مورد
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المورد</TableHead>
                    <TableHead>التصنيف</TableHead>
                    <TableHead>التقييم</TableHead>
                    <TableHead>الطلبات</TableHead>
                    <TableHead>إجمالي المشتريات</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {suppliers.map((supplier) => (
                    <TableRow key={supplier.id}>
                      <TableCell className="font-medium">{supplier.name}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{supplier.category}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <span className="text-amber-500">★</span>
                          {supplier.rating}
                        </div>
                      </TableCell>
                      <TableCell>{supplier.orders}</TableCell>
                      <TableCell>{supplier.total.toLocaleString()} ر.س</TableCell>
                      <TableCell>
                        <Badge className="bg-emerald-500">{supplier.status}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Edit className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Receiving Tab */}
        <TabsContent value="receiving" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>الشحنات الواردة</CardTitle>
              <CardDescription>
                متابعة الشحنات وتأكيد الاستلام
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-emerald-300 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                          <Truck className="w-5 h-5 text-blue-500" />
                        </div>
                        <div>
                          <h4 className="font-medium text-slate-800 dark:text-white">
                            شحنة #{i}0{i}
                          </h4>
                          <p className="text-sm text-slate-500">
                            من شركة البذور العالمية
                          </p>
                        </div>
                      </div>
                      <Badge className="bg-blue-500">في الطريق</Badge>
                    </div>
                    <Progress value={60 + i * 10} className="h-2" />
                    <p className="text-xs text-slate-500 mt-2">
                      الوصول المتوقع: 2025-01-2{i}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { title: "تقرير المشتريات الشهري", icon: FileText },
              { title: "تحليل الموردين", icon: Building2 },
              { title: "تقرير الأسعار", icon: DollarSign },
              { title: "تقرير التأخيرات", icon: AlertTriangle },
              { title: "تقرير الجودة", icon: CheckCircle },
              { title: "تقرير المقارنة", icon: ArrowUpRight },
            ].map((report, index) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-xl bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                        <report.icon className="w-6 h-6 text-emerald-500" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-slate-800 dark:text-white">
                          {report.title}
                        </h3>
                        <p className="text-sm text-slate-500">
                          عرض وتصدير
                        </p>
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

export default PurchasingPage
