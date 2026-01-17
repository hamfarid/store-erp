import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  ShoppingCart,
  Users,
  FileText,
  DollarSign,
  TrendingUp,
  Package,
  Clock,
  CheckCircle,
  XCircle,
  Eye,
  Printer,
  Send,
  Plus,
  User,
  Phone,
  Mail,
  MapPin,
  Building,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"

import { DataTable, FormModal, StatsCard } from "@/components/common"
import { formatCurrency, formatNumber, formatDate } from "@/lib/utils"

// Mock data
const mockCustomers = [
  {
    id: 1,
    code: "CUS-001",
    name: "شركة الفجر الزراعية",
    type: "شركة",
    contact: "أحمد محمد",
    phone: "0501234567",
    email: "info@alfajr.com",
    city: "الرياض",
    creditLimit: 50000,
    balance: 12500,
    status: "نشط",
    totalOrders: 25,
    totalSpent: 125000,
  },
  {
    id: 2,
    code: "CUS-002",
    name: "مزرعة النخيل",
    type: "مؤسسة",
    contact: "محمد علي",
    phone: "0559876543",
    email: "sales@nakheel.com",
    city: "جدة",
    creditLimit: 30000,
    balance: 5000,
    status: "نشط",
    totalOrders: 15,
    totalSpent: 75000,
  },
  {
    id: 3,
    code: "CUS-003",
    name: "علي أحمد",
    type: "فرد",
    contact: "علي أحمد",
    phone: "0541112233",
    email: "ali@gmail.com",
    city: "الدمام",
    creditLimit: 10000,
    balance: 8500,
    status: "معلق",
    totalOrders: 8,
    totalSpent: 32000,
  },
]

const mockOrders = [
  {
    id: 1,
    orderNo: "SO-2025-001",
    date: "2025-01-10",
    customer: "شركة الفجر الزراعية",
    items: 5,
    subtotal: 15000,
    tax: 2250,
    total: 17250,
    status: "مكتمل",
    paymentStatus: "مدفوع",
  },
  {
    id: 2,
    orderNo: "SO-2025-002",
    date: "2025-01-09",
    customer: "مزرعة النخيل",
    items: 3,
    subtotal: 8500,
    tax: 1275,
    total: 9775,
    status: "قيد التنفيذ",
    paymentStatus: "جزئي",
  },
  {
    id: 3,
    orderNo: "SO-2025-003",
    date: "2025-01-08",
    customer: "علي أحمد",
    items: 2,
    subtotal: 3200,
    tax: 480,
    total: 3680,
    status: "جديد",
    paymentStatus: "غير مدفوع",
  },
  {
    id: 4,
    orderNo: "SO-2025-004",
    date: "2025-01-07",
    customer: "شركة الفجر الزراعية",
    items: 8,
    subtotal: 22000,
    tax: 3300,
    total: 25300,
    status: "ملغي",
    paymentStatus: "مسترد",
  },
]

const mockInvoices = [
  {
    id: 1,
    invoiceNo: "INV-2025-001",
    date: "2025-01-10",
    dueDate: "2025-02-10",
    customer: "شركة الفجر الزراعية",
    orderNo: "SO-2025-001",
    subtotal: 15000,
    tax: 2250,
    total: 17250,
    paid: 17250,
    status: "مدفوعة",
  },
  {
    id: 2,
    invoiceNo: "INV-2025-002",
    date: "2025-01-09",
    dueDate: "2025-02-09",
    customer: "مزرعة النخيل",
    orderNo: "SO-2025-002",
    subtotal: 8500,
    tax: 1275,
    total: 9775,
    paid: 5000,
    status: "جزئية",
  },
  {
    id: 3,
    invoiceNo: "INV-2025-003",
    date: "2025-01-08",
    dueDate: "2025-02-08",
    customer: "علي أحمد",
    orderNo: "SO-2025-003",
    subtotal: 3200,
    tax: 480,
    total: 3680,
    paid: 0,
    status: "غير مدفوعة",
  },
]

const customerTypes = ["شركة", "مؤسسة", "فرد"]
const cities = ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "أخرى"]

const SalesModule = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState("customers")
  const [customers, setCustomers] = useState(mockCustomers)
  const [orders, setOrders] = useState(mockOrders)
  const [invoices, setInvoices] = useState(mockInvoices)
  const [isLoading, setIsLoading] = useState(false)

  // Modals
  const [customerModal, setCustomerModal] = useState(false)
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [formData, setFormData] = useState({
    name: "",
    type: "",
    contact: "",
    phone: "",
    email: "",
    city: "",
    address: "",
    creditLimit: "",
    notes: "",
  })

  // Set active tab based on URL
  useEffect(() => {
    if (location.pathname.includes("/customers")) setActiveTab("customers")
    else if (location.pathname.includes("/orders")) setActiveTab("orders")
    else if (location.pathname.includes("/invoices")) setActiveTab("invoices")
    else if (location.pathname.includes("/reports")) setActiveTab("reports")
  }, [location])

  // Stats
  const totalCustomers = customers.length
  const activeCustomers = customers.filter((c) => c.status === "نشط").length
  const totalSales = orders
    .filter((o) => o.status !== "ملغي")
    .reduce((sum, o) => sum + o.total, 0)
  const pendingAmount = invoices
    .filter((i) => i.status !== "مدفوعة")
    .reduce((sum, i) => sum + (i.total - i.paid), 0)

  // Customer columns
  const customerColumns = [
    { key: "code", header: "الكود", sortable: true },
    {
      key: "name",
      header: "اسم العميل",
      sortable: true,
      render: (val, row) => (
        <div>
          <p className="font-medium">{val}</p>
          <p className="text-sm text-muted-foreground">{row.contact}</p>
        </div>
      ),
    },
    {
      key: "type",
      header: "النوع",
      render: (val) => (
        <Badge variant="outline">{val}</Badge>
      ),
    },
    { key: "phone", header: "الجوال" },
    { key: "city", header: "المدينة" },
    {
      key: "balance",
      header: "الرصيد",
      sortable: true,
      render: (val, row) => (
        <div>
          <p className={val > row.creditLimit * 0.8 ? "text-red-600 font-medium" : ""}>
            {formatCurrency(val)}
          </p>
          <p className="text-xs text-muted-foreground">
            من {formatCurrency(row.creditLimit)}
          </p>
        </div>
      ),
    },
    {
      key: "status",
      header: "الحالة",
      render: (val) => (
        <Badge variant={val === "نشط" ? "default" : "secondary"}>
          {val}
        </Badge>
      ),
    },
  ]

  // Order columns
  const orderColumns = [
    { key: "orderNo", header: "رقم الطلب", sortable: true },
    { key: "date", header: "التاريخ", sortable: true },
    { key: "customer", header: "العميل", sortable: true },
    {
      key: "items",
      header: "المنتجات",
      render: (val) => `${val} منتج`,
    },
    {
      key: "total",
      header: "الإجمالي",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "status",
      header: "الحالة",
      render: (val) => {
        const variants = {
          "مكتمل": "default",
          "قيد التنفيذ": "secondary",
          "جديد": "outline",
          "ملغي": "destructive",
        }
        return <Badge variant={variants[val]}>{val}</Badge>
      },
    },
    {
      key: "paymentStatus",
      header: "الدفع",
      render: (val) => {
        const colors = {
          "مدفوع": "text-emerald-600",
          "جزئي": "text-amber-600",
          "غير مدفوع": "text-red-600",
          "مسترد": "text-slate-600",
        }
        return <span className={colors[val]}>{val}</span>
      },
    },
  ]

  // Invoice columns
  const invoiceColumns = [
    { key: "invoiceNo", header: "رقم الفاتورة", sortable: true },
    { key: "date", header: "التاريخ", sortable: true },
    { key: "dueDate", header: "تاريخ الاستحقاق", sortable: true },
    { key: "customer", header: "العميل" },
    { key: "orderNo", header: "رقم الطلب" },
    {
      key: "total",
      header: "الإجمالي",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "paid",
      header: "المدفوع",
      render: (val, row) => (
        <div className="space-y-1">
          <div className="flex justify-between text-sm">
            <span>{formatCurrency(val)}</span>
            <span className="text-muted-foreground">
              {Math.round((val / row.total) * 100)}%
            </span>
          </div>
          <Progress value={(val / row.total) * 100} className="h-1.5" />
        </div>
      ),
    },
    {
      key: "status",
      header: "الحالة",
      render: (val) => {
        const variants = {
          "مدفوعة": "default",
          "جزئية": "secondary",
          "غير مدفوعة": "destructive",
        }
        return <Badge variant={variants[val]}>{val}</Badge>
      },
    },
  ]

  // Handlers
  const handleAddCustomer = () => {
    setSelectedCustomer(null)
    setFormData({
      name: "",
      type: "",
      contact: "",
      phone: "",
      email: "",
      city: "",
      address: "",
      creditLimit: "",
      notes: "",
    })
    setCustomerModal(true)
  }

  const handleEditCustomer = (customer) => {
    setSelectedCustomer(customer)
    setFormData({
      name: customer.name,
      type: customer.type,
      contact: customer.contact,
      phone: customer.phone,
      email: customer.email,
      city: customer.city,
      address: customer.address || "",
      creditLimit: customer.creditLimit.toString(),
      notes: customer.notes || "",
    })
    setCustomerModal(true)
  }

  const handleSubmitCustomer = (e) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      if (selectedCustomer) {
        setCustomers((prev) =>
          prev.map((c) =>
            c.id === selectedCustomer.id
              ? {
                  ...c,
                  ...formData,
                  creditLimit: Number(formData.creditLimit),
                }
              : c
          )
        )
        toast.success("تم تحديث بيانات العميل بنجاح!")
      } else {
        const newCustomer = {
          id: customers.length + 1,
          code: `CUS-${String(customers.length + 1).padStart(3, "0")}`,
          ...formData,
          creditLimit: Number(formData.creditLimit),
          balance: 0,
          status: "نشط",
          totalOrders: 0,
          totalSpent: 0,
        }
        setCustomers((prev) => [...prev, newCustomer])
        toast.success("تم إضافة العميل بنجاح!")
      }

      setIsLoading(false)
      setCustomerModal(false)
    }, 1000)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">
          إدارة المبيعات
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          إدارة العملاء والطلبات والفواتير
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="إجمالي العملاء"
          value={totalCustomers}
          change={12}
          icon={Users}
          color="blue"
          delay={0}
        />
        <StatsCard
          title="العملاء النشطين"
          value={activeCustomers}
          icon={CheckCircle}
          color="emerald"
          delay={0.1}
        />
        <StatsCard
          title="إجمالي المبيعات"
          value={totalSales}
          format="currency"
          change={8.5}
          icon={DollarSign}
          color="purple"
          delay={0.2}
        />
        <StatsCard
          title="المستحقات المعلقة"
          value={pendingAmount}
          format="currency"
          icon={Clock}
          color="amber"
          delay={0.3}
        />
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="customers" className="gap-2">
            <Users className="w-4 h-4" />
            العملاء
          </TabsTrigger>
          <TabsTrigger value="orders" className="gap-2">
            <ShoppingCart className="w-4 h-4" />
            الطلبات
          </TabsTrigger>
          <TabsTrigger value="invoices" className="gap-2">
            <FileText className="w-4 h-4" />
            الفواتير
          </TabsTrigger>
          <TabsTrigger value="reports" className="gap-2">
            <TrendingUp className="w-4 h-4" />
            التقارير
          </TabsTrigger>
        </TabsList>

        {/* Customers Tab */}
        <TabsContent value="customers" className="mt-6">
          <DataTable
            data={customers}
            columns={customerColumns}
            searchKey="name"
            searchPlaceholder="البحث عن عميل..."
            addButtonText="إضافة عميل"
            onAdd={handleAddCustomer}
            onEdit={handleEditCustomer}
            onDelete={(row) => toast.error(`حذف: ${row.name}`)}
            onView={(row) => toast.info(`عرض: ${row.name}`)}
            onRefresh={() => toast.info("تم تحديث البيانات")}
          />
        </TabsContent>

        {/* Orders Tab */}
        <TabsContent value="orders" className="mt-6">
          <DataTable
            data={orders}
            columns={orderColumns}
            searchKey="orderNo"
            searchPlaceholder="البحث عن طلب..."
            addButtonText="طلب جديد"
            onAdd={() => toast.info("إنشاء طلب جديد")}
            onEdit={(row) => toast.info(`تعديل: ${row.orderNo}`)}
            onView={(row) => toast.info(`عرض: ${row.orderNo}`)}
            onRefresh={() => toast.info("تم تحديث البيانات")}
          />
        </TabsContent>

        {/* Invoices Tab */}
        <TabsContent value="invoices" className="mt-6">
          <DataTable
            data={invoices}
            columns={invoiceColumns}
            searchKey="invoiceNo"
            searchPlaceholder="البحث عن فاتورة..."
            addButtonText="فاتورة جديدة"
            showAdd={false}
            onView={(row) => toast.info(`عرض: ${row.invoiceNo}`)}
            onRefresh={() => toast.info("تم تحديث البيانات")}
          />
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { title: "تقرير المبيعات", icon: TrendingUp, color: "emerald" },
              { title: "تقرير العملاء", icon: Users, color: "blue" },
              { title: "تقرير الفواتير", icon: FileText, color: "purple" },
              { title: "تقرير المستحقات", icon: Clock, color: "amber" },
              { title: "تقرير الأرباح", icon: DollarSign, color: "cyan" },
              { title: "تقرير تحليلي", icon: TrendingUp, color: "orange" },
            ].map((report, index) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="cursor-pointer hover:shadow-lg transition-shadow">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className={`p-3 rounded-xl bg-${report.color}-100 dark:bg-${report.color}-900/30`}>
                      <report.icon className={`w-6 h-6 text-${report.color}-600`} />
                    </div>
                    <div>
                      <h3 className="font-medium">{report.title}</h3>
                      <p className="text-sm text-muted-foreground">تصدير PDF / Excel</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Customer Form Modal */}
      <FormModal
        open={customerModal}
        onOpenChange={setCustomerModal}
        title={selectedCustomer ? "تعديل العميل" : "إضافة عميل جديد"}
        description={selectedCustomer ? "قم بتعديل بيانات العميل" : "أدخل بيانات العميل الجديد"}
        onSubmit={handleSubmitCustomer}
        isLoading={isLoading}
        size="xl"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="name">اسم العميل *</Label>
            <div className="relative">
              <Building className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="pr-9"
                placeholder="اسم الشركة أو العميل"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="type">نوع العميل *</Label>
            <Select
              value={formData.type}
              onValueChange={(value) => setFormData({ ...formData, type: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر النوع" />
              </SelectTrigger>
              <SelectContent>
                {customerTypes.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="contact">جهة الاتصال *</Label>
            <div className="relative">
              <User className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="contact"
                value={formData.contact}
                onChange={(e) => setFormData({ ...formData, contact: e.target.value })}
                className="pr-9"
                placeholder="اسم المسؤول"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">رقم الجوال *</Label>
            <div className="relative">
              <Phone className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="phone"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="pr-9"
                placeholder="05XXXXXXXX"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">البريد الإلكتروني</Label>
            <div className="relative">
              <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="pr-9"
                placeholder="email@example.com"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="city">المدينة *</Label>
            <Select
              value={formData.city}
              onValueChange={(value) => setFormData({ ...formData, city: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر المدينة" />
              </SelectTrigger>
              <SelectContent>
                {cities.map((city) => (
                  <SelectItem key={city} value={city}>
                    {city}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="creditLimit">الحد الائتماني *</Label>
            <div className="relative">
              <DollarSign className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="creditLimit"
                type="number"
                value={formData.creditLimit}
                onChange={(e) => setFormData({ ...formData, creditLimit: e.target.value })}
                className="pr-9"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="address">العنوان</Label>
            <div className="relative">
              <MapPin className="absolute right-3 top-3 w-4 h-4 text-slate-400" />
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                className="pr-9"
                placeholder="العنوان التفصيلي"
              />
            </div>
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="notes">ملاحظات</Label>
            <Textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="ملاحظات إضافية (اختياري)"
              rows={3}
            />
          </div>
        </div>
      </FormModal>
    </div>
  )
}

export default SalesModule
