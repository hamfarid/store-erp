/**
 * Purchasing Management Page - إدارة المشتريات
 * Gaara ERP v12
 *
 * Complete purchasing and supplier management with CRUD operations.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect, useCallback } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  ShoppingCart,
  Package,
  Truck,
  Building2,
  FileText,
  Clock,
  CheckCircle2,
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
  RefreshCw,
  MoreVertical,
  Send,
  PackageCheck,
  Receipt,
  Users,
  Calendar,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
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
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"
import purchasingService from "@/services/purchasingService"

// Form schemas
const orderSchema = z.object({
  supplier_id: z.string().min(1, "المورد مطلوب"),
  supplier_name: z.string().min(1, "اسم المورد مطلوب"),
  items: z.array(z.object({
    product_id: z.string(),
    product_name: z.string(),
    quantity: z.number().min(1),
    unit_price: z.number().min(0),
  })).optional(),
  expected_date: z.string().optional(),
  notes: z.string().optional(),
  payment_terms: z.string().default("net30"),
})

const supplierSchema = z.object({
  name: z.string().min(2, "اسم المورد مطلوب"),
  name_ar: z.string().optional(),
  email: z.string().email("البريد الإلكتروني غير صحيح").optional().or(z.literal("")),
  phone: z.string().min(10, "رقم الهاتف غير صحيح"),
  address: z.string().optional(),
  city: z.string().optional(),
  tax_number: z.string().optional(),
  category: z.string().optional(),
  payment_terms: z.string().default("net30"),
  is_active: z.boolean().default(true),
})

// Status configurations
const statusConfig = {
  draft: { label: "مسودة", variant: "outline", icon: FileText, color: "text-gray-500" },
  pending: { label: "معلق", variant: "secondary", icon: Clock, color: "text-yellow-500" },
  approved: { label: "معتمد", variant: "default", icon: CheckCircle2, color: "text-blue-500" },
  ordered: { label: "تم الطلب", variant: "default", icon: Send, color: "text-indigo-500" },
  shipped: { label: "في الطريق", variant: "default", icon: Truck, color: "text-purple-500" },
  received: { label: "مستلم", variant: "default", icon: PackageCheck, color: "text-green-500" },
  cancelled: { label: "ملغي", variant: "destructive", icon: XCircle, color: "text-red-500" },
}

// Mock data
const mockOrders = [
  { id: "PO-001", supplier: "مؤسسة البذور الذهبية", supplier_id: "S001", date: "2026-01-17", items: 5, total: 45000, status: "received", payment_status: "paid", expected_date: "2026-01-20" },
  { id: "PO-002", supplier: "شركة الأسمدة المتحدة", supplier_id: "S002", date: "2026-01-16", items: 3, total: 28000, status: "shipped", payment_status: "pending", expected_date: "2026-01-22" },
  { id: "PO-003", supplier: "مصنع المبيدات الحديث", supplier_id: "S003", date: "2026-01-15", items: 8, total: 65000, status: "approved", payment_status: "pending", expected_date: "2026-01-25" },
  { id: "PO-004", supplier: "مؤسسة المعدات الزراعية", supplier_id: "S004", date: "2026-01-14", items: 2, total: 120000, status: "pending", payment_status: "pending", expected_date: "2026-02-01" },
  { id: "PO-005", supplier: "شركة التغليف والتعبئة", supplier_id: "S005", date: "2026-01-13", items: 10, total: 15000, status: "draft", payment_status: "pending", expected_date: "2026-01-30" },
]

const mockSuppliers = [
  { id: "S001", name: "مؤسسة البذور الذهبية", email: "info@goldenseeds.sa", phone: "0501234567", city: "الرياض", orders: 25, total: 450000, status: "active" },
  { id: "S002", name: "شركة الأسمدة المتحدة", email: "sales@unifert.com", phone: "0559876543", city: "جدة", orders: 18, total: 320000, status: "active" },
  { id: "S003", name: "مصنع المبيدات الحديث", email: "order@modernpest.sa", phone: "0561234567", city: "الدمام", orders: 12, total: 180000, status: "active" },
  { id: "S004", name: "مؤسسة المعدات الزراعية", email: "info@agriequip.sa", phone: "0541234567", city: "الخبر", orders: 8, total: 250000, status: "inactive" },
]

const PurchasingPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("orders")
  const [orders, setOrders] = useState(mockOrders)
  const [suppliers, setSuppliers] = useState(mockSuppliers)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isOrderDialogOpen, setIsOrderDialogOpen] = useState(false)
  const [isSupplierDialogOpen, setIsSupplierDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isReceiveDialogOpen, setIsReceiveDialogOpen] = useState(false)
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [selectedSupplier, setSelectedSupplier] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const orderForm = useForm({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      supplier_id: "",
      supplier_name: "",
      items: [],
      expected_date: "",
      notes: "",
      payment_terms: "net30",
    },
  })

  const supplierForm = useForm({
    resolver: zodResolver(supplierSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      email: "",
      phone: "",
      address: "",
      city: "",
      tax_number: "",
      category: "",
      payment_terms: "net30",
      is_active: true,
    },
  })

  // Load data
  const loadData = useCallback(async () => {
    setIsLoading(true)
    try {
      const [ordersRes, suppliersRes] = await Promise.all([
        purchasingService.getOrders({ status: statusFilter !== "all" ? statusFilter : undefined }),
        purchasingService.getSuppliers(),
      ])

      if (ordersRes.success) setOrders(ordersRes.data || mockOrders)
      if (suppliersRes.success) setSuppliers(suppliersRes.data || mockSuppliers)
    } catch (error) {
      console.error("Error loading data:", error)
    } finally {
      setIsLoading(false)
    }
  }, [statusFilter])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Filter orders
  const filteredOrders = orders.filter(o => {
    const matchesSearch = o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         o.supplier.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || o.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Filter suppliers
  const filteredSuppliers = suppliers.filter(s => {
    return s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
           s.email?.toLowerCase().includes(searchQuery.toLowerCase())
  })

  // Statistics
  const orderStats = {
    totalPurchases: orders.reduce((sum, o) => sum + (o.status !== "cancelled" ? o.total : 0), 0),
    pendingOrders: orders.filter(o => o.status === "pending").length,
    inTransit: orders.filter(o => o.status === "shipped").length,
    totalSuppliers: suppliers.filter(s => s.status === "active").length,
  }

  // Handlers
  const handleCreateOrder = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.createOrder(data)
      if (response.success) {
        toast.success("تم إنشاء أمر الشراء بنجاح")
        setIsOrderDialogOpen(false)
        orderForm.reset()
        loadData()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إنشاء أمر الشراء")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditOrder = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.updateOrder(selectedOrder.id, data)
      if (response.success) {
        toast.success("تم تحديث أمر الشراء")
        setIsOrderDialogOpen(false)
        setSelectedOrder(null)
        orderForm.reset()
        loadData()
      }
    } catch (error) {
      toast.error("فشل تحديث أمر الشراء")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteOrder = async () => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.cancelOrder(selectedOrder.id, "إلغاء من المستخدم")
      if (response.success) {
        toast.success("تم إلغاء أمر الشراء")
        setIsDeleteDialogOpen(false)
        setSelectedOrder(null)
        loadData()
      }
    } catch (error) {
      toast.error("فشل إلغاء أمر الشراء")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleApproveOrder = async (order) => {
    try {
      const response = await purchasingService.approveOrder(order.id)
      if (response.success) {
        toast.success("تم اعتماد أمر الشراء")
        loadData()
      }
    } catch (error) {
      toast.error("فشل اعتماد الأمر")
    }
  }

  const handleReceiveOrder = async (order) => {
    try {
      const response = await purchasingService.receiveOrder(order.id, { received_date: new Date().toISOString() })
      if (response.success) {
        toast.success("تم استلام الطلب")
        loadData()
      }
    } catch (error) {
      toast.error("فشل تأكيد الاستلام")
    }
  }

  const handleCreateSupplier = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.createSupplier(data)
      if (response.success) {
        toast.success("تم إضافة المورد بنجاح")
        setIsSupplierDialogOpen(false)
        supplierForm.reset()
        loadData()
      }
    } catch (error) {
      toast.error("فشل إضافة المورد")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditSupplier = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.updateSupplier(selectedSupplier.id, data)
      if (response.success) {
        toast.success("تم تحديث المورد")
        setIsSupplierDialogOpen(false)
        setSelectedSupplier(null)
        supplierForm.reset()
        loadData()
      }
    } catch (error) {
      toast.error("فشل تحديث المورد")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteSupplier = async () => {
    setIsSubmitting(true)
    try {
      const response = await purchasingService.deleteSupplier(selectedSupplier.id)
      if (response.success) {
        toast.success("تم حذف المورد")
        setIsDeleteDialogOpen(false)
        setSelectedSupplier(null)
        loadData()
      }
    } catch (error) {
      toast.error("فشل حذف المورد")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openOrderEditDialog = (order) => {
    setSelectedOrder(order)
    setDialogMode("edit")
    orderForm.reset({
      supplier_id: order.supplier_id,
      supplier_name: order.supplier,
      expected_date: order.expected_date,
      notes: order.notes || "",
      payment_terms: order.payment_terms || "net30",
    })
    setIsOrderDialogOpen(true)
  }

  const openSupplierEditDialog = (supplier) => {
    setSelectedSupplier(supplier)
    setDialogMode("edit")
    supplierForm.reset({
      name: supplier.name,
      email: supplier.email || "",
      phone: supplier.phone || "",
      city: supplier.city || "",
      is_active: supplier.status === "active",
    })
    setIsSupplierDialogOpen(true)
  }

  // Table columns for orders
  const orderColumns = [
    {
      accessorKey: "id",
      header: "رقم الأمر",
      cell: ({ row }) => (
        <span className="font-mono font-medium text-primary">{row.original.id}</span>
      ),
    },
    {
      accessorKey: "supplier",
      header: "المورد",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <Building2 className="w-4 h-4 text-blue-500" />
          </div>
          <span>{row.original.supplier}</span>
        </div>
      ),
    },
    {
      accessorKey: "date",
      header: "التاريخ",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <Calendar className="w-4 h-4" />
          {row.original.date}
        </div>
      ),
    },
    {
      accessorKey: "items",
      header: "العناصر",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.items} عنصر</Badge>
      ),
    },
    {
      accessorKey: "total",
      header: "الإجمالي",
      cell: ({ row }) => (
        <span className="font-bold text-green-600">
          {(row.original.total || 0).toLocaleString()} ر.س
        </span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.draft
        const Icon = config.icon
        return (
          <Badge variant={config.variant} className="gap-1">
            <Icon className="w-3 h-3" />
            {config.label}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const order = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              
              <DropdownMenuItem onClick={() => { setSelectedOrder(order); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              
              {order.status === "draft" && (
                <DropdownMenuItem onClick={() => openOrderEditDialog(order)}>
                  <Edit className="w-4 h-4 ml-2" />
                  تعديل
                </DropdownMenuItem>
              )}
              
              {order.status === "pending" && (
                <DropdownMenuItem onClick={() => handleApproveOrder(order)}>
                  <CheckCircle2 className="w-4 h-4 ml-2" />
                  اعتماد
                </DropdownMenuItem>
              )}
              
              {order.status === "shipped" && (
                <DropdownMenuItem onClick={() => handleReceiveOrder(order)}>
                  <PackageCheck className="w-4 h-4 ml-2" />
                  تأكيد الاستلام
                </DropdownMenuItem>
              )}
              
              <DropdownMenuItem onClick={() => toast.info("جاري إنشاء الفاتورة...")}>
                <Receipt className="w-4 h-4 ml-2" />
                إنشاء فاتورة
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              {!["received", "cancelled"].includes(order.status) && (
                <DropdownMenuItem
                  onClick={() => { setSelectedOrder(order); setIsDeleteDialogOpen(true); }}
                  className="text-red-600"
                >
                  <XCircle className="w-4 h-4 ml-2" />
                  إلغاء الأمر
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Table columns for suppliers
  const supplierColumns = [
    {
      accessorKey: "name",
      header: "المورد",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
            <Building2 className="w-5 h-5 text-emerald-500" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground">{row.original.email}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "phone",
      header: "الهاتف",
    },
    {
      accessorKey: "city",
      header: "المدينة",
    },
    {
      accessorKey: "orders",
      header: "الطلبات",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.orders} طلب</Badge>
      ),
    },
    {
      accessorKey: "total",
      header: "إجمالي التعاملات",
      cell: ({ row }) => (
        <span className="font-bold">{(row.original.total || 0).toLocaleString()} ر.س</span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => (
        <Badge variant={row.original.status === "active" ? "default" : "secondary"}>
          {row.original.status === "active" ? "نشط" : "غير نشط"}
        </Badge>
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const supplier = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedSupplier(supplier); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openSupplierEditDialog(supplier)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => { setSelectedSupplier(supplier); setIsDeleteDialogOpen(true); }}
                className="text-red-600"
              >
                <Trash2 className="w-4 h-4 ml-2" />
                حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <ShoppingCart className="w-7 h-7 text-emerald-500" />
            إدارة المشتريات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة أوامر الشراء والموردين</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsOrderDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />
            أمر شراء جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(orderStats.totalPurchases / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">إجمالي المشتريات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{orderStats.pendingOrders}</p>
              <p className="text-sm text-muted-foreground">أوامر معلقة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Truck className="w-6 h-6 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{orderStats.inTransit}</p>
              <p className="text-sm text-muted-foreground">في الطريق</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Building2 className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{orderStats.totalSuppliers}</p>
              <p className="text-sm text-muted-foreground">موردين نشطين</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="orders" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            أوامر الشراء
          </TabsTrigger>
          <TabsTrigger value="suppliers" className="flex items-center gap-2">
            <Building2 className="w-4 h-4" />
            الموردين
          </TabsTrigger>
        </TabsList>

        {/* Orders Tab */}
        <TabsContent value="orders" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="بحث في أوامر الشراء..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pr-10"
                  />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="الحالة" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="draft">مسودة</SelectItem>
                    <SelectItem value="pending">معلق</SelectItem>
                    <SelectItem value="approved">معتمد</SelectItem>
                    <SelectItem value="shipped">في الطريق</SelectItem>
                    <SelectItem value="received">مستلم</SelectItem>
                    <SelectItem value="cancelled">ملغي</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline" onClick={loadData}>
                  <RefreshCw className="w-4 h-4 ml-2" />
                  تحديث
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>أوامر الشراء ({filteredOrders.length})</CardTitle>
              <CardDescription>قائمة جميع أوامر الشراء</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={orderColumns} data={filteredOrders} isLoading={isLoading} searchKey="id" />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Suppliers Tab */}
        <TabsContent value="suppliers" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4 justify-between">
                <div className="flex-1 relative max-w-md">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="بحث في الموردين..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pr-10"
                  />
                </div>
                <Button onClick={() => { setDialogMode("add"); setIsSupplierDialogOpen(true); }}>
                  <Plus className="w-4 h-4 ml-2" />
                  إضافة مورد
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>الموردين ({filteredSuppliers.length})</CardTitle>
              <CardDescription>قائمة جميع الموردين</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={supplierColumns} data={filteredSuppliers} isLoading={isLoading} searchKey="name" />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Order Dialog */}
      <FormDialog
        open={isOrderDialogOpen}
        onOpenChange={setIsOrderDialogOpen}
        title={dialogMode === "add" ? "أمر شراء جديد" : "تعديل أمر الشراء"}
        description={dialogMode === "add" ? "إنشاء أمر شراء جديد" : "تعديل بيانات أمر الشراء"}
        onSubmit={orderForm.handleSubmit(dialogMode === "add" ? handleCreateOrder : handleEditOrder)}
        isSubmitting={isSubmitting}
        submitText={dialogMode === "add" ? "إنشاء" : "حفظ"}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المورد</Label>
              <Select
                value={orderForm.watch("supplier_id")}
                onValueChange={(v) => {
                  const supplier = suppliers.find(s => s.id === v)
                  orderForm.setValue("supplier_id", v)
                  orderForm.setValue("supplier_name", supplier?.name || "")
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="اختر المورد" />
                </SelectTrigger>
                <SelectContent>
                  {suppliers.map((s) => (
                    <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>تاريخ التسليم المتوقع</Label>
              <Input type="date" {...orderForm.register("expected_date")} />
            </div>
          </div>
          <div>
            <Label>شروط الدفع</Label>
            <Select
              value={orderForm.watch("payment_terms")}
              onValueChange={(v) => orderForm.setValue("payment_terms", v)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cash">نقدي</SelectItem>
                <SelectItem value="net15">صافي 15 يوم</SelectItem>
                <SelectItem value="net30">صافي 30 يوم</SelectItem>
                <SelectItem value="net60">صافي 60 يوم</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...orderForm.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
        </div>
      </FormDialog>

      {/* Supplier Dialog */}
      <FormDialog
        open={isSupplierDialogOpen}
        onOpenChange={setIsSupplierDialogOpen}
        title={dialogMode === "add" ? "إضافة مورد جديد" : "تعديل بيانات المورد"}
        description={dialogMode === "add" ? "إضافة مورد جديد للنظام" : "تعديل بيانات المورد"}
        onSubmit={supplierForm.handleSubmit(dialogMode === "add" ? handleCreateSupplier : handleEditSupplier)}
        isSubmitting={isSubmitting}
        submitText={dialogMode === "add" ? "إضافة" : "حفظ"}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>اسم المورد</Label>
              <Input {...supplierForm.register("name")} placeholder="اسم المورد" />
              {supplierForm.formState.errors.name && (
                <p className="text-sm text-red-500 mt-1">{supplierForm.formState.errors.name.message}</p>
              )}
            </div>
            <div>
              <Label>رقم الهاتف</Label>
              <Input {...supplierForm.register("phone")} placeholder="0501234567" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>البريد الإلكتروني</Label>
              <Input {...supplierForm.register("email")} type="email" placeholder="email@example.com" />
            </div>
            <div>
              <Label>المدينة</Label>
              <Input {...supplierForm.register("city")} placeholder="الرياض" />
            </div>
          </div>
          <div>
            <Label>العنوان</Label>
            <Textarea {...supplierForm.register("address")} placeholder="العنوان الكامل..." />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>الرقم الضريبي</Label>
              <Input {...supplierForm.register("tax_number")} placeholder="300000000000003" />
            </div>
            <div>
              <Label>شروط الدفع الافتراضية</Label>
              <Select
                value={supplierForm.watch("payment_terms")}
                onValueChange={(v) => supplierForm.setValue("payment_terms", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cash">نقدي</SelectItem>
                  <SelectItem value="net15">صافي 15 يوم</SelectItem>
                  <SelectItem value="net30">صافي 30 يوم</SelectItem>
                  <SelectItem value="net60">صافي 60 يوم</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Order Dialog */}
      <ViewDialog
        open={isViewDialogOpen && selectedOrder !== null}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedOrder(null); }}
        title={`أمر شراء: ${selectedOrder?.id}`}
        subtitle={`المورد: ${selectedOrder?.supplier}`}
        badge={selectedOrder && {
          text: statusConfig[selectedOrder.status]?.label,
          variant: statusConfig[selectedOrder.status]?.variant,
        }}
        size="lg"
      >
        {selectedOrder && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات الأمر">
              <ViewDialog.Row label="رقم الأمر" value={selectedOrder.id} />
              <ViewDialog.Row label="المورد" value={selectedOrder.supplier} />
              <ViewDialog.Row label="التاريخ" value={selectedOrder.date} />
              <ViewDialog.Row label="تاريخ التسليم المتوقع" value={selectedOrder.expected_date} />
              <ViewDialog.Row label="عدد العناصر" value={`${selectedOrder.items} عنصر`} />
            </ViewDialog.Section>
            <ViewDialog.Section title="معلومات مالية">
              <ViewDialog.Row label="الإجمالي" value={`${(selectedOrder.total || 0).toLocaleString()} ر.س`} valueClassName="text-green-600 font-bold" />
              <ViewDialog.Row label="حالة الدفع" value={selectedOrder.payment_status === "paid" ? "مدفوع" : "معلق"} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title={selectedSupplier ? "حذف المورد" : "إلغاء أمر الشراء"}
        description={
          selectedSupplier
            ? `هل أنت متأكد من حذف المورد "${selectedSupplier?.name}"؟`
            : `هل أنت متأكد من إلغاء أمر الشراء "${selectedOrder?.id}"؟`
        }
        variant="danger"
        confirmText={selectedSupplier ? "حذف" : "إلغاء الأمر"}
        onConfirm={selectedSupplier ? handleDeleteSupplier : handleDeleteOrder}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default PurchasingPage
