/**
 * Warehouse Management Page - إدارة المستودعات
 * Gaara ERP v12
 *
 * Complete warehouse and location management with stock tracking and transfers.
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
  Warehouse,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Package,
  MapPin,
  BarChart3,
  ArrowRightLeft,
  RefreshCw,
  Download,
  QrCode,
  Boxes,
  CheckCircle2,
  AlertTriangle,
  Clock,
  TrendingUp,
  TrendingDown,
  Users,
  Settings,
  History,
  Target,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
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
import { Checkbox } from "@/components/ui/checkbox"
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"

// Form schemas
const warehouseSchema = z.object({
  name: z.string().min(2, "اسم المستودع مطلوب"),
  code: z.string().min(2, "رمز المستودع مطلوب"),
  type: z.enum(["main", "branch", "temporary", "cold"]),
  address: z.string().optional(),
  city: z.string().optional(),
  manager: z.string().optional(),
  phone: z.string().optional(),
  capacity: z.number().min(0).default(0),
  is_active: z.boolean().default(true),
})

const transferSchema = z.object({
  from_warehouse: z.string().min(1, "المستودع المصدر مطلوب"),
  to_warehouse: z.string().min(1, "المستودع الوجهة مطلوب"),
  products: z.array(z.object({
    product_id: z.string(),
    product_name: z.string(),
    quantity: z.number().min(1),
  })).min(1, "يجب إضافة منتج واحد على الأقل"),
  notes: z.string().optional(),
})

// Status configurations
const statusConfig = {
  active: { label: "نشط", variant: "default", color: "bg-green-100 text-green-700" },
  inactive: { label: "غير نشط", variant: "secondary", color: "bg-gray-100 text-gray-700" },
  maintenance: { label: "صيانة", variant: "destructive", color: "bg-yellow-100 text-yellow-700" },
}

const typeConfig = {
  main: { label: "رئيسي", variant: "default" },
  branch: { label: "فرعي", variant: "outline" },
  temporary: { label: "مؤقت", variant: "secondary" },
  cold: { label: "تبريد", variant: "default" },
}

// Mock data
const mockWarehouses = [
  {
    id: "WH001",
    name: "المستودع الرئيسي - الرياض",
    code: "WH-RYD-01",
    type: "main",
    address: "حي العليا، شارع الملك فهد",
    city: "الرياض",
    manager: "أحمد محمد",
    phone: "0501234567",
    capacity: 10000,
    used_capacity: 7500,
    status: "active",
    products_count: 250,
    total_value: 850000,
    locations: 120,
  },
  {
    id: "WH002",
    name: "مستودع جدة",
    code: "WH-JED-01",
    type: "branch",
    address: "حي الصناعية",
    city: "جدة",
    manager: "خالد علي",
    phone: "0559876543",
    capacity: 5000,
    used_capacity: 3200,
    status: "active",
    products_count: 180,
    total_value: 450000,
    locations: 60,
  },
  {
    id: "WH003",
    name: "مستودع التبريد",
    code: "WH-RYD-CL",
    type: "cold",
    address: "المنطقة الصناعية",
    city: "الرياض",
    manager: "سارة أحمد",
    phone: "0541234567",
    capacity: 2000,
    used_capacity: 1800,
    status: "active",
    products_count: 50,
    total_value: 320000,
    locations: 30,
  },
]

const mockLocations = [
  { id: "LOC001", warehouse_id: "WH001", code: "A-01-01", zone: "A", row: "01", level: "01", type: "shelf", capacity: 100, used: 85, products: ["P001", "P002"] },
  { id: "LOC002", warehouse_id: "WH001", code: "A-01-02", zone: "A", row: "01", level: "02", type: "shelf", capacity: 100, used: 60, products: ["P003"] },
  { id: "LOC003", warehouse_id: "WH001", code: "B-01-01", zone: "B", row: "01", level: "01", type: "pallet", capacity: 500, used: 450, products: ["P004", "P005", "P006"] },
  { id: "LOC004", warehouse_id: "WH001", code: "B-02-01", zone: "B", row: "02", level: "01", type: "pallet", capacity: 500, used: 200, products: ["P007"] },
]

const mockTransfers = [
  { id: "TRF001", date: "2026-01-17", from: "المستودع الرئيسي", to: "مستودع جدة", products: 5, status: "completed", created_by: "أحمد محمد" },
  { id: "TRF002", date: "2026-01-16", from: "مستودع جدة", to: "المستودع الرئيسي", products: 3, status: "in_transit", created_by: "خالد علي" },
  { id: "TRF003", date: "2026-01-15", from: "المستودع الرئيسي", to: "مستودع التبريد", products: 2, status: "pending", created_by: "سارة أحمد" },
]

const WarehousePage = () => {
  // State
  const [activeTab, setActiveTab] = useState("warehouses")
  const [warehouses, setWarehouses] = useState(mockWarehouses)
  const [locations, setLocations] = useState(mockLocations)
  const [transfers, setTransfers] = useState(mockTransfers)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")
  const [selectedWarehouse, setSelectedWarehouse] = useState(null)

  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isTransferDialogOpen, setIsTransferDialogOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const warehouseForm = useForm({
    resolver: zodResolver(warehouseSchema),
    defaultValues: {
      name: "",
      code: "",
      type: "main",
      address: "",
      city: "",
      manager: "",
      phone: "",
      capacity: 0,
      is_active: true,
    },
  })

  const transferForm = useForm({
    resolver: zodResolver(transferSchema),
    defaultValues: {
      from_warehouse: "",
      to_warehouse: "",
      products: [],
      notes: "",
    },
  })

  // Filter warehouses
  const filteredWarehouses = warehouses.filter(w => {
    const matchesSearch = w.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         w.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = typeFilter === "all" || w.type === typeFilter
    return matchesSearch && matchesType
  })

  // Statistics
  const stats = {
    totalWarehouses: warehouses.length,
    activeWarehouses: warehouses.filter(w => w.status === "active").length,
    totalCapacity: warehouses.reduce((sum, w) => sum + w.capacity, 0),
    usedCapacity: warehouses.reduce((sum, w) => sum + w.used_capacity, 0),
    totalValue: warehouses.reduce((sum, w) => sum + w.total_value, 0),
    totalProducts: warehouses.reduce((sum, w) => sum + w.products_count, 0),
  }

  // Handlers
  const handleCreate = async (data) => {
    setIsSubmitting(true)
    try {
      const newWarehouse = {
        id: `WH${String(warehouses.length + 1).padStart(3, '0')}`,
        ...data,
        used_capacity: 0,
        status: data.is_active ? "active" : "inactive",
        products_count: 0,
        total_value: 0,
        locations: 0,
      }
      setWarehouses([...warehouses, newWarehouse])
      toast.success("تم إضافة المستودع بنجاح")
      setIsCreateDialogOpen(false)
      warehouseForm.reset()
    } catch (error) {
      toast.error("فشل إضافة المستودع")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEdit = async (data) => {
    setIsSubmitting(true)
    try {
      setWarehouses(warehouses.map(w => w.id === selectedWarehouse.id ? {
        ...w,
        ...data,
        status: data.is_active ? "active" : "inactive",
      } : w))
      toast.success("تم تحديث المستودع")
      setIsEditDialogOpen(false)
      setSelectedWarehouse(null)
      warehouseForm.reset()
    } catch (error) {
      toast.error("فشل تحديث المستودع")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setWarehouses(warehouses.filter(w => w.id !== selectedWarehouse.id))
      toast.success("تم حذف المستودع")
      setIsDeleteDialogOpen(false)
      setSelectedWarehouse(null)
    } catch (error) {
      toast.error("فشل حذف المستودع")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCreateTransfer = async (data) => {
    setIsSubmitting(true)
    try {
      const newTransfer = {
        id: `TRF${String(transfers.length + 1).padStart(3, '0')}`,
        date: new Date().toISOString().split('T')[0],
        from: warehouses.find(w => w.id === data.from_warehouse)?.name,
        to: warehouses.find(w => w.id === data.to_warehouse)?.name,
        products: data.products.length,
        status: "pending",
        created_by: "المستخدم الحالي",
      }
      setTransfers([...transfers, newTransfer])
      toast.success("تم إنشاء طلب النقل")
      setIsTransferDialogOpen(false)
      transferForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء طلب النقل")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openEditDialog = (warehouse) => {
    setSelectedWarehouse(warehouse)
    warehouseForm.reset({
      name: warehouse.name,
      code: warehouse.code,
      type: warehouse.type,
      address: warehouse.address || "",
      city: warehouse.city || "",
      manager: warehouse.manager || "",
      phone: warehouse.phone || "",
      capacity: warehouse.capacity,
      is_active: warehouse.status === "active",
    })
    setIsEditDialogOpen(true)
  }

  // Generate warehouse code
  const generateCode = () => {
    const city = warehouseForm.watch("city")?.slice(0, 3).toUpperCase() || "XXX"
    const num = String(warehouses.length + 1).padStart(2, '0')
    warehouseForm.setValue("code", `WH-${city}-${num}`)
  }

  // Table columns for warehouses
  const warehouseColumns = [
    {
      accessorKey: "name",
      header: "المستودع",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
            row.original.type === "cold" ? "bg-blue-100" : 
            row.original.type === "main" ? "bg-emerald-100" : "bg-amber-100"
          }`}>
            <Warehouse className={`w-5 h-5 ${
              row.original.type === "cold" ? "text-blue-600" : 
              row.original.type === "main" ? "text-emerald-600" : "text-amber-600"
            }`} />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground font-mono">{row.original.code}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => {
        const config = typeConfig[row.original.type] || typeConfig.main
        return <Badge variant={config.variant}>{config.label}</Badge>
      },
    },
    {
      accessorKey: "city",
      header: "المدينة",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <MapPin className="w-4 h-4 text-muted-foreground" />
          {row.original.city}
        </div>
      ),
    },
    {
      accessorKey: "capacity",
      header: "السعة",
      cell: ({ row }) => {
        const percentage = (row.original.used_capacity / row.original.capacity) * 100
        return (
          <div className="w-28">
            <div className="flex justify-between text-sm mb-1">
              <span>{row.original.used_capacity.toLocaleString()}</span>
              <span className="text-muted-foreground">/ {row.original.capacity.toLocaleString()}</span>
            </div>
            <Progress 
              value={percentage}
              className={`h-2 ${percentage > 90 ? '[&>div]:bg-red-500' : percentage > 70 ? '[&>div]:bg-yellow-500' : ''}`}
            />
          </div>
        )
      },
    },
    {
      accessorKey: "products_count",
      header: "المنتجات",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.products_count} منتج</Badge>
      ),
    },
    {
      accessorKey: "total_value",
      header: "القيمة",
      cell: ({ row }) => (
        <span className="font-bold">{(row.original.total_value / 1000).toFixed(0)}K ر.س</span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.active
        return <Badge className={config.color}>{config.label}</Badge>
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const warehouse = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedWarehouse(warehouse); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(warehouse)}>
                <Edit className="w-4 h-4 ml-2" />تعديل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("جاري عرض المواقع...")}>
                <Target className="w-4 h-4 ml-2" />إدارة المواقع
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("جاري عرض التقرير...")}>
                <BarChart3 className="w-4 h-4 ml-2" />تقرير المخزون
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedWarehouse(warehouse); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Transfer columns
  const transferColumns = [
    {
      accessorKey: "id",
      header: "رقم النقل",
      cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span>,
    },
    { accessorKey: "date", header: "التاريخ" },
    { accessorKey: "from", header: "من" },
    { accessorKey: "to", header: "إلى" },
    {
      accessorKey: "products",
      header: "المنتجات",
      cell: ({ row }) => <Badge variant="outline">{row.original.products} منتج</Badge>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        const config = {
          pending: { label: "معلق", color: "bg-yellow-100 text-yellow-700" },
          in_transit: { label: "في الطريق", color: "bg-blue-100 text-blue-700" },
          completed: { label: "مكتمل", color: "bg-green-100 text-green-700" },
        }
        return <Badge className={config[status]?.color}>{config[status]?.label}</Badge>
      },
    },
    { accessorKey: "created_by", header: "بواسطة" },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Warehouse className="w-7 h-7 text-amber-500" />
            إدارة المستودعات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المستودعات والمواقع وحركات النقل</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setIsTransferDialogOpen(true)}>
            <ArrowRightLeft className="w-4 h-4 ml-2" />نقل مخزون
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 ml-2" />مستودع جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Warehouse className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalWarehouses}</p>
              <p className="text-xs text-muted-foreground">مستودع</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeWarehouses}</p>
              <p className="text-xs text-muted-foreground">نشط</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Boxes className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{((stats.usedCapacity / stats.totalCapacity) * 100).toFixed(0)}%</p>
              <p className="text-xs text-muted-foreground">نسبة الإشغال</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Package className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalProducts}</p>
              <p className="text-xs text-muted-foreground">منتج</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.totalValue / 1000000).toFixed(1)}M</p>
              <p className="text-xs text-muted-foreground">قيمة المخزون</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center">
              <ArrowRightLeft className="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{transfers.filter(t => t.status === "pending").length}</p>
              <p className="text-xs text-muted-foreground">نقل معلق</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="warehouses" className="flex items-center gap-2">
            <Warehouse className="w-4 h-4" />المستودعات
          </TabsTrigger>
          <TabsTrigger value="locations" className="flex items-center gap-2">
            <Target className="w-4 h-4" />المواقع
          </TabsTrigger>
          <TabsTrigger value="transfers" className="flex items-center gap-2">
            <ArrowRightLeft className="w-4 h-4" />حركات النقل
          </TabsTrigger>
        </TabsList>

        {/* Warehouses Tab */}
        <TabsContent value="warehouses" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={typeFilter} onValueChange={setTypeFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="النوع" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الأنواع</SelectItem>
                    <SelectItem value="main">رئيسي</SelectItem>
                    <SelectItem value="branch">فرعي</SelectItem>
                    <SelectItem value="temporary">مؤقت</SelectItem>
                    <SelectItem value="cold">تبريد</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>المستودعات ({filteredWarehouses.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={warehouseColumns} data={filteredWarehouses} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Locations Tab */}
        <TabsContent value="locations" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>مواقع التخزين</CardTitle>
              <Button onClick={() => toast.info("جاري إضافة موقع...")}><Plus className="w-4 h-4 ml-2" />موقع جديد</Button>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                {locations.map((loc) => (
                  <Card key={loc.id} className="cursor-pointer hover:border-primary">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-mono font-bold">{loc.code}</span>
                        <Badge variant="outline">{loc.type === "shelf" ? "رف" : "باليت"}</Badge>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>المنطقة</span>
                          <span className="font-medium">{loc.zone}</span>
                        </div>
                        <Progress value={(loc.used / loc.capacity) * 100} className="h-2" />
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>الإشغال</span>
                          <span>{loc.used}/{loc.capacity}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Transfers Tab */}
        <TabsContent value="transfers" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>حركات النقل ({transfers.length})</CardTitle>
              <Button onClick={() => setIsTransferDialogOpen(true)}>
                <ArrowRightLeft className="w-4 h-4 ml-2" />نقل جديد
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={transferColumns} data={transfers} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Create/Edit Warehouse Dialog */}
      <FormDialog
        open={isCreateDialogOpen || isEditDialogOpen}
        onOpenChange={(open) => {
          if (!open) { setIsCreateDialogOpen(false); setIsEditDialogOpen(false); setSelectedWarehouse(null); warehouseForm.reset(); }
        }}
        title={isEditDialogOpen ? "تعديل المستودع" : "إضافة مستودع جديد"}
        description={isEditDialogOpen ? "تعديل بيانات المستودع" : "إضافة مستودع جديد للنظام"}
        onSubmit={warehouseForm.handleSubmit(isEditDialogOpen ? handleEdit : handleCreate)}
        isSubmitting={isSubmitting}
        submitText={isEditDialogOpen ? "حفظ" : "إضافة"}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>اسم المستودع</Label>
              <Input {...warehouseForm.register("name")} placeholder="المستودع الرئيسي" />
            </div>
            <div>
              <Label>رمز المستودع</Label>
              <div className="flex gap-2">
                <Input {...warehouseForm.register("code")} placeholder="WH-RYD-01" />
                <Button type="button" variant="outline" size="icon" onClick={generateCode}><RefreshCw className="w-4 h-4" /></Button>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>نوع المستودع</Label>
              <Select value={warehouseForm.watch("type")} onValueChange={(v) => warehouseForm.setValue("type", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="main">رئيسي</SelectItem>
                  <SelectItem value="branch">فرعي</SelectItem>
                  <SelectItem value="temporary">مؤقت</SelectItem>
                  <SelectItem value="cold">تبريد</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>المدينة</Label>
              <Input {...warehouseForm.register("city")} placeholder="الرياض" />
            </div>
          </div>
          <div>
            <Label>العنوان</Label>
            <Textarea {...warehouseForm.register("address")} placeholder="العنوان الكامل..." />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>مدير المستودع</Label>
              <Input {...warehouseForm.register("manager")} placeholder="الاسم" />
            </div>
            <div>
              <Label>رقم الهاتف</Label>
              <Input {...warehouseForm.register("phone")} placeholder="0501234567" />
            </div>
            <div>
              <Label>السعة الكلية</Label>
              <Input type="number" {...warehouseForm.register("capacity", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="flex items-center space-x-2 space-x-reverse">
            <Checkbox id="is_active" checked={warehouseForm.watch("is_active")} onCheckedChange={(checked) => warehouseForm.setValue("is_active", checked)} />
            <Label htmlFor="is_active">مستودع نشط</Label>
          </div>
        </div>
      </FormDialog>

      {/* Transfer Dialog */}
      <FormDialog
        open={isTransferDialogOpen}
        onOpenChange={setIsTransferDialogOpen}
        title="نقل مخزون"
        description="نقل منتجات بين المستودعات"
        onSubmit={transferForm.handleSubmit(handleCreateTransfer)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>من مستودع</Label>
              <Select value={transferForm.watch("from_warehouse")} onValueChange={(v) => transferForm.setValue("from_warehouse", v)}>
                <SelectTrigger><SelectValue placeholder="اختر المستودع" /></SelectTrigger>
                <SelectContent>
                  {warehouses.map((w) => <SelectItem key={w.id} value={w.id}>{w.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>إلى مستودع</Label>
              <Select value={transferForm.watch("to_warehouse")} onValueChange={(v) => transferForm.setValue("to_warehouse", v)}>
                <SelectTrigger><SelectValue placeholder="اختر المستودع" /></SelectTrigger>
                <SelectContent>
                  {warehouses.map((w) => <SelectItem key={w.id} value={w.id}>{w.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...transferForm.register("notes")} placeholder="ملاحظات النقل..." />
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedWarehouse(null); }}
        title={selectedWarehouse?.name}
        subtitle={selectedWarehouse?.code}
        badge={selectedWarehouse && { text: statusConfig[selectedWarehouse.status]?.label, variant: statusConfig[selectedWarehouse.status]?.variant }}
        size="lg"
      >
        {selectedWarehouse && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات المستودع">
              <ViewDialog.Row label="النوع" value={typeConfig[selectedWarehouse.type]?.label} />
              <ViewDialog.Row label="المدينة" value={selectedWarehouse.city} />
              <ViewDialog.Row label="العنوان" value={selectedWarehouse.address || "—"} />
              <ViewDialog.Row label="المدير" value={selectedWarehouse.manager} />
              <ViewDialog.Row label="الهاتف" value={selectedWarehouse.phone} />
            </ViewDialog.Section>
            <ViewDialog.Section title="إحصائيات">
              <ViewDialog.Row label="السعة الكلية" value={`${selectedWarehouse.capacity.toLocaleString()} وحدة`} />
              <ViewDialog.Row label="المستخدم" value={`${selectedWarehouse.used_capacity.toLocaleString()} وحدة`} />
              <ViewDialog.Row label="نسبة الإشغال" value={`${((selectedWarehouse.used_capacity / selectedWarehouse.capacity) * 100).toFixed(1)}%`} />
              <ViewDialog.Row label="عدد المنتجات" value={`${selectedWarehouse.products_count} منتج`} />
              <ViewDialog.Row label="القيمة الإجمالية" value={`${selectedWarehouse.total_value.toLocaleString()} ر.س`} valueClassName="text-green-600 font-bold" />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف المستودع"
        description={`هل أنت متأكد من حذف "${selectedWarehouse?.name}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default WarehousePage
