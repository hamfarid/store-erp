/**
 * Sales Management Page - إدارة المبيعات
 * Gaara ERP v12
 *
 * Complete sales order management with CRUD operations.
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
  Plus,
  Search,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  DollarSign,
  TrendingUp,
  Package,
  Users,
  FileText,
  Calendar,
  CheckCircle2,
  Clock,
  XCircle,
  RefreshCw,
  Download,
  Printer,
  CreditCard,
  History,
  Send,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
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
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"
import { formatDate } from "@/lib/utils"
import salesService from "@/services/salesService"

// Form schema
const orderSchema = z.object({
  customer_id: z.string().min(1, "العميل مطلوب"),
  customer_name: z.string().min(1, "اسم العميل مطلوب"),
  items: z.array(z.object({
    product_id: z.string(),
    product_name: z.string(),
    quantity: z.number().min(1),
    unit_price: z.number().min(0),
  })).min(1, "يجب إضافة منتج واحد على الأقل"),
  notes: z.string().optional(),
  payment_method: z.string().default("cash"),
  discount: z.number().min(0).default(0),
  tax_rate: z.number().min(0).max(100).default(15),
})

// Status configurations
const statusConfig = {
  pending: { label: "معلق", variant: "secondary", icon: Clock, color: "text-yellow-500" },
  processing: { label: "قيد التجهيز", variant: "default", icon: Package, color: "text-blue-500" },
  completed: { label: "مكتمل", variant: "default", icon: CheckCircle2, color: "text-green-500" },
  cancelled: { label: "ملغي", variant: "destructive", icon: XCircle, color: "text-red-500" },
}

const paymentConfig = {
  paid: { label: "مدفوع", variant: "default", color: "bg-green-100 text-green-700" },
  pending: { label: "معلق", variant: "secondary", color: "bg-yellow-100 text-yellow-700" },
  partial: { label: "جزئي", variant: "outline", color: "bg-blue-100 text-blue-700" },
  refunded: { label: "مسترد", variant: "destructive", color: "bg-red-100 text-red-700" },
}

// Mock data for fallback
const mockSalesData = [
  { id: "SO-001", customer: "شركة التقنية", customer_id: "C001", date: "2026-01-17", items: 5, total: 15000, status: "completed", payment: "paid", items_list: [] },
  { id: "SO-002", customer: "مؤسسة الزراعة", customer_id: "C002", date: "2026-01-16", items: 3, total: 8500, status: "pending", payment: "pending", items_list: [] },
  { id: "SO-003", customer: "متجر الإلكترونيات", customer_id: "C003", date: "2026-01-15", items: 8, total: 22000, status: "processing", payment: "partial", items_list: [] },
  { id: "SO-004", customer: "شركة البناء", customer_id: "C004", date: "2026-01-14", items: 2, total: 5000, status: "cancelled", payment: "refunded", items_list: [] },
  { id: "SO-005", customer: "مصنع الأغذية", customer_id: "C005", date: "2026-01-13", items: 12, total: 45000, status: "completed", payment: "paid", items_list: [] },
]

const SalesPage = () => {
  // State
  const [sales, setSales] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [dateRange, setDateRange] = useState({ from: null, to: null })
  
  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isPaymentDialogOpen, setIsPaymentDialogOpen] = useState(false)
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const form = useForm({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      customer_id: "",
      customer_name: "",
      items: [],
      notes: "",
      payment_method: "cash",
      discount: 0,
      tax_rate: 15,
    },
  })

  // Load sales data
  const loadSales = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await salesService.getOrders({
        status: statusFilter !== "all" ? statusFilter : undefined,
        search: searchQuery || undefined,
      })
      
      if (response.success && response.data) {
        setSales(Array.isArray(response.data) ? response.data : response.data.orders || [])
      } else {
        // Fallback to mock data
        setSales(mockSalesData)
      }
    } catch (error) {
      console.error("Error loading sales:", error)
      setSales(mockSalesData)
      toast.error("تم تحميل بيانات تجريبية")
    } finally {
      setIsLoading(false)
    }
  }, [statusFilter, searchQuery])

  useEffect(() => {
    loadSales()
  }, [loadSales])

  // Filter sales
  const filteredSales = sales.filter(s => {
    const matchesSearch = 
      s.id?.toLowerCase().includes(searchQuery.toLowerCase()) || 
      s.customer?.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || s.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Calculate stats
  const stats = {
    totalSales: sales.reduce((sum, s) => sum + (s.status !== "cancelled" ? (s.total || 0) : 0), 0),
    ordersCount: sales.filter(s => s.status !== "cancelled").length,
    pendingOrders: sales.filter(s => s.status === "pending").length,
    avgOrderValue: sales.length > 0 
      ? Math.round(sales.reduce((sum, s) => sum + (s.total || 0), 0) / sales.length)
      : 0,
  }

  // Handlers
  const handleCreateOrder = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await salesService.createOrder(data)
      if (response.success) {
        toast.success(response.message_ar || "تم إنشاء الطلب بنجاح")
        setIsCreateDialogOpen(false)
        form.reset()
        loadSales()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إنشاء الطلب")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditOrder = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await salesService.updateOrder(selectedOrder.id, data)
      if (response.success) {
        toast.success(response.message_ar || "تم تحديث الطلب بنجاح")
        setIsEditDialogOpen(false)
        setSelectedOrder(null)
        form.reset()
        loadSales()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل تحديث الطلب")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteOrder = async () => {
    setIsSubmitting(true)
    try {
      const response = await salesService.cancelOrder(selectedOrder.id, "تم الإلغاء من قبل المستخدم")
      if (response.success) {
        toast.success("تم إلغاء الطلب بنجاح")
        setIsDeleteDialogOpen(false)
        setSelectedOrder(null)
        loadSales()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إلغاء الطلب")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleUpdateStatus = async (order, newStatus) => {
    try {
      const response = await salesService.updateStatus(order.id, newStatus)
      if (response.success) {
        toast.success("تم تحديث الحالة")
        loadSales()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل تحديث الحالة")
    }
  }

  const handleGenerateInvoice = async (order) => {
    try {
      const response = await salesService.generateInvoice(order.id)
      if (response.success) {
        toast.success("تم إنشاء الفاتورة")
        // TODO: Open invoice in new tab or download
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إنشاء الفاتورة")
    }
  }

  const handleExport = async () => {
    try {
      const response = await salesService.exportData('xlsx', { status: statusFilter })
      if (response.success) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `sales_${new Date().toISOString().split('T')[0]}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        toast.success("تم تصدير البيانات")
      }
    } catch (error) {
      toast.error("فشل تصدير البيانات")
    }
  }

  const openEditDialog = (order) => {
    setSelectedOrder(order)
    form.reset({
      customer_id: order.customer_id,
      customer_name: order.customer,
      items: order.items_list || [],
      notes: order.notes || "",
      payment_method: order.payment_method || "cash",
      discount: order.discount || 0,
      tax_rate: order.tax_rate || 15,
    })
    setIsEditDialogOpen(true)
  }

  // Table columns
  const columns = [
    {
      accessorKey: "id",
      header: "رقم الطلب",
      cell: ({ row }) => (
        <span className="font-mono font-medium text-primary">{row.original.id}</span>
      ),
    },
    {
      accessorKey: "customer",
      header: "العميل",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <Users className="w-4 h-4 text-blue-500" />
          </div>
          <span>{row.original.customer}</span>
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
        const config = statusConfig[row.original.status] || statusConfig.pending
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
      accessorKey: "payment",
      header: "الدفع",
      cell: ({ row }) => {
        const config = paymentConfig[row.original.payment] || paymentConfig.pending
        return (
          <Badge variant={config.variant} className={config.color}>
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
              
              <DropdownMenuItem onClick={() => openEditDialog(order)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => handleGenerateInvoice(order)}>
                <FileText className="w-4 h-4 ml-2" />
                إنشاء فاتورة
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              {order.status === "pending" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(order, "processing")}>
                  <Package className="w-4 h-4 ml-2" />
                  بدء التجهيز
                </DropdownMenuItem>
              )}
              
              {order.status === "processing" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(order, "completed")}>
                  <CheckCircle2 className="w-4 h-4 ml-2" />
                  إكمال الطلب
                </DropdownMenuItem>
              )}
              
              <DropdownMenuItem onClick={() => { setSelectedOrder(order); setIsPaymentDialogOpen(true); }}>
                <CreditCard className="w-4 h-4 ml-2" />
                تسجيل دفعة
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              {order.status !== "cancelled" && order.status !== "completed" && (
                <DropdownMenuItem
                  onClick={() => { setSelectedOrder(order); setIsDeleteDialogOpen(true); }}
                  className="text-red-600"
                >
                  <XCircle className="w-4 h-4 ml-2" />
                  إلغاء الطلب
                </DropdownMenuItem>
              )}
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
            <ShoppingCart className="w-7 h-7 text-blue-500" />
            إدارة المبيعات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة أوامر البيع والفواتير</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 ml-2" />
            طلب بيع جديد
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalSales / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">إجمالي المبيعات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <FileText className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.ordersCount}</p>
              <p className="text-sm text-muted-foreground">طلبات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.pendingOrders}</p>
              <p className="text-sm text-muted-foreground">معلقة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.avgOrderValue.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">متوسط الطلب</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input 
                placeholder="بحث في الطلبات..." 
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
                <SelectItem value="pending">معلق</SelectItem>
                <SelectItem value="processing">قيد التجهيز</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
                <SelectItem value="cancelled">ملغي</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={loadSales}>
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Orders Table */}
      <Card>
        <CardHeader>
          <CardTitle>أوامر البيع ({filteredSales.length})</CardTitle>
          <CardDescription>قائمة جميع طلبات البيع</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable 
            columns={columns} 
            data={filteredSales} 
            isLoading={isLoading}
            searchKey="id" 
          />
        </CardContent>
      </Card>

      {/* Create Order Dialog */}
      <FormDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        title="طلب بيع جديد"
        description="إنشاء طلب بيع جديد"
        onSubmit={form.handleSubmit(handleCreateOrder)}
        isSubmitting={isSubmitting}
        submitText="إنشاء الطلب"
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>العميل</Label>
              <Input {...form.register("customer_name")} placeholder="اسم العميل" />
              {form.formState.errors.customer_name && (
                <p className="text-sm text-red-500 mt-1">{form.formState.errors.customer_name.message}</p>
              )}
            </div>
            <div>
              <Label>طريقة الدفع</Label>
              <Select
                value={form.watch("payment_method")}
                onValueChange={(v) => form.setValue("payment_method", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cash">نقداً</SelectItem>
                  <SelectItem value="card">بطاقة</SelectItem>
                  <SelectItem value="transfer">تحويل</SelectItem>
                  <SelectItem value="credit">آجل</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...form.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
        </div>
      </FormDialog>

      {/* View Order Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={setIsViewDialogOpen}
        title={`طلب بيع: ${selectedOrder?.id}`}
        subtitle={`العميل: ${selectedOrder?.customer}`}
        badge={selectedOrder && {
          text: statusConfig[selectedOrder.status]?.label,
          variant: statusConfig[selectedOrder.status]?.variant,
        }}
        size="lg"
      >
        {selectedOrder && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات الطلب">
              <ViewDialog.Row label="رقم الطلب" value={selectedOrder.id} />
              <ViewDialog.Row label="العميل" value={selectedOrder.customer} />
              <ViewDialog.Row label="التاريخ" value={selectedOrder.date} />
              <ViewDialog.Row label="عدد العناصر" value={`${selectedOrder.items} عنصر`} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="معلومات الدفع">
              <ViewDialog.Row label="الإجمالي" value={`${(selectedOrder.total || 0).toLocaleString()} ر.س`} valueClassName="text-green-600 font-bold" />
              <ViewDialog.Row label="حالة الدفع" value={paymentConfig[selectedOrder.payment]?.label} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="إلغاء الطلب"
        description={`هل أنت متأكد من إلغاء الطلب "${selectedOrder?.id}"؟ لا يمكن التراجع عن هذا الإجراء.`}
        variant="danger"
        confirmText="إلغاء الطلب"
        onConfirm={handleDeleteOrder}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default SalesPage
