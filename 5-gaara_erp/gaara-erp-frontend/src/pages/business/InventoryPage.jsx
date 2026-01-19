/**
 * Inventory Management Page - إدارة المخزون
 * Gaara ERP v12
 *
 * Complete inventory and product management with CRUD operations.
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
  Package,
  Plus,
  Search,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  AlertTriangle,
  CheckCircle2,
  BarChart3,
  ArrowUpDown,
  Warehouse,
  RefreshCw,
  Download,
  Upload,
  QrCode,
  ArrowRightLeft,
  History,
  Settings,
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
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"
import inventoryService from "@/services/inventoryService"

// Form schema
const productSchema = z.object({
  name: z.string().min(2, "اسم المنتج مطلوب"),
  name_ar: z.string().optional(),
  sku: z.string().min(2, "رمز SKU مطلوب"),
  category: z.string().min(1, "التصنيف مطلوب"),
  unit: z.string().min(1, "الوحدة مطلوبة"),
  stock: z.number().min(0).default(0),
  min_stock: z.number().min(0).default(0),
  max_stock: z.number().min(0).optional(),
  price: z.number().min(0, "السعر مطلوب"),
  cost: z.number().min(0).default(0),
  warehouse_id: z.string().optional(),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
})

// Status configurations
const statusConfig = {
  in_stock: { label: "متوفر", variant: "default", color: "bg-green-100 text-green-700" },
  low_stock: { label: "منخفض", variant: "secondary", color: "bg-yellow-100 text-yellow-700" },
  out_of_stock: { label: "نفد", variant: "destructive", color: "bg-red-100 text-red-700" },
}

// Mock data
const mockInventory = [
  { id: "PRD-001", name: "قمح فاخر", sku: "WHT-001", category: "حبوب", stock: 5000, min_stock: 1000, unit: "كجم", warehouse: "المستودع الرئيسي", price: 15, cost: 10, status: "in_stock" },
  { id: "PRD-002", name: "سماد NPK", sku: "FRT-001", category: "أسمدة", stock: 250, min_stock: 500, unit: "كجم", warehouse: "المستودع الفرعي", price: 45, cost: 30, status: "low_stock" },
  { id: "PRD-003", name: "بذور طماطم", sku: "SED-001", category: "بذور", stock: 0, min_stock: 100, unit: "عبوة", warehouse: "المستودع الرئيسي", price: 120, cost: 80, status: "out_of_stock" },
  { id: "PRD-004", name: "مبيد حشري", sku: "PST-001", category: "مبيدات", stock: 150, min_stock: 50, unit: "لتر", warehouse: "المستودع الفرعي", price: 85, cost: 60, status: "in_stock" },
  { id: "PRD-005", name: "شتلات فلفل", sku: "SED-002", category: "شتلات", stock: 800, min_stock: 200, unit: "شتلة", warehouse: "المشتل", price: 5, cost: 3, status: "in_stock" },
]

const mockCategories = [
  { id: 1, name: "حبوب", count: 15 },
  { id: 2, name: "أسمدة", count: 8 },
  { id: 3, name: "بذور", count: 25 },
  { id: 4, name: "مبيدات", count: 12 },
  { id: 5, name: "شتلات", count: 30 },
]

const mockWarehouses = [
  { id: 1, name: "المستودع الرئيسي", location: "الرياض" },
  { id: 2, name: "المستودع الفرعي", location: "جدة" },
  { id: 3, name: "المشتل", location: "الدمام" },
]

const InventoryPage = () => {
  // State
  const [inventory, setInventory] = useState([])
  const [categories, setCategories] = useState(mockCategories)
  const [warehouses, setWarehouses] = useState(mockWarehouses)
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")
  const [warehouseFilter, setWarehouseFilter] = useState("all")

  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isAdjustDialogOpen, setIsAdjustDialogOpen] = useState(false)
  const [isTransferDialogOpen, setIsTransferDialogOpen] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const form = useForm({
    resolver: zodResolver(productSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      sku: "",
      category: "",
      unit: "كجم",
      stock: 0,
      min_stock: 0,
      max_stock: 0,
      price: 0,
      cost: 0,
      warehouse_id: "",
      description: "",
      is_active: true,
    },
  })

  // Load inventory
  const loadInventory = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await inventoryService.getProducts({
        category: categoryFilter !== "all" ? categoryFilter : undefined,
        status: statusFilter !== "all" ? statusFilter : undefined,
        warehouse: warehouseFilter !== "all" ? warehouseFilter : undefined,
        search: searchQuery || undefined,
      })
      
      if (response.success && response.data) {
        setInventory(Array.isArray(response.data) ? response.data : response.data.products || [])
      } else {
        setInventory(mockInventory)
      }
    } catch (error) {
      console.error("Error loading inventory:", error)
      setInventory(mockInventory)
    } finally {
      setIsLoading(false)
    }
  }, [categoryFilter, statusFilter, warehouseFilter, searchQuery])

  useEffect(() => {
    loadInventory()
  }, [loadInventory])

  // Filter inventory
  const filteredInventory = inventory.filter(item => {
    const matchesSearch = 
      item.name?.toLowerCase().includes(searchQuery.toLowerCase()) || 
      item.sku?.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = categoryFilter === "all" || item.category === categoryFilter
    const matchesStatus = statusFilter === "all" || item.status === statusFilter
    const matchesWarehouse = warehouseFilter === "all" || item.warehouse === warehouseFilter
    return matchesSearch && matchesCategory && matchesStatus && matchesWarehouse
  })

  // Calculate stats
  const stats = {
    totalProducts: inventory.length,
    totalValue: inventory.reduce((sum, i) => sum + ((i.stock || 0) * (i.price || 0)), 0),
    lowStock: inventory.filter(i => i.status === "low_stock").length,
    outOfStock: inventory.filter(i => i.status === "out_of_stock").length,
  }

  // Handlers
  const handleCreateProduct = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await inventoryService.createProduct(data)
      if (response.success) {
        toast.success(response.message_ar || "تم إضافة المنتج بنجاح")
        setIsCreateDialogOpen(false)
        form.reset()
        loadInventory()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إضافة المنتج")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditProduct = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await inventoryService.updateProduct(selectedProduct.id, data)
      if (response.success) {
        toast.success(response.message_ar || "تم تحديث المنتج بنجاح")
        setIsEditDialogOpen(false)
        setSelectedProduct(null)
        form.reset()
        loadInventory()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل تحديث المنتج")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteProduct = async () => {
    setIsSubmitting(true)
    try {
      const response = await inventoryService.deleteProduct(selectedProduct.id)
      if (response.success) {
        toast.success("تم حذف المنتج بنجاح")
        setIsDeleteDialogOpen(false)
        setSelectedProduct(null)
        loadInventory()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل حذف المنتج")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleAdjustStock = async (adjustmentData) => {
    setIsSubmitting(true)
    try {
      const response = await inventoryService.adjustStock(selectedProduct.id, adjustmentData)
      if (response.success) {
        toast.success("تم تعديل المخزون")
        setIsAdjustDialogOpen(false)
        setSelectedProduct(null)
        loadInventory()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل تعديل المخزون")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleExport = async () => {
    try {
      const response = await inventoryService.exportData('xlsx')
      if (response.success) {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `inventory_${new Date().toISOString().split('T')[0]}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        toast.success("تم تصدير البيانات")
      }
    } catch (error) {
      toast.error("فشل تصدير البيانات")
    }
  }

  const openEditDialog = (product) => {
    setSelectedProduct(product)
    form.reset({
      name: product.name,
      name_ar: product.name_ar || "",
      sku: product.sku,
      category: product.category,
      unit: product.unit,
      stock: product.stock,
      min_stock: product.min_stock,
      max_stock: product.max_stock || 0,
      price: product.price,
      cost: product.cost || 0,
      warehouse_id: product.warehouse_id || "",
      description: product.description || "",
      is_active: product.is_active !== false,
    })
    setIsEditDialogOpen(true)
  }

  // Generate SKU
  const generateSKU = () => {
    const prefix = form.watch("category")?.slice(0, 3).toUpperCase() || "PRD"
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
    form.setValue("sku", `${prefix}-${random}`)
  }

  // Table columns
  const columns = [
    {
      accessorKey: "name",
      header: "المنتج",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <Package className="w-5 h-5 text-blue-500" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground font-mono">{row.original.sku}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "category",
      header: "التصنيف",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.category}</Badge>
      ),
    },
    {
      accessorKey: "stock",
      header: "المخزون",
      cell: ({ row }) => {
        const stockPercent = Math.min((row.original.stock / (row.original.min_stock * 2)) * 100, 100)
        return (
          <div className="w-32">
            <div className="flex justify-between text-sm mb-1">
              <span className="font-medium">{row.original.stock}</span>
              <span className="text-muted-foreground">/ {row.original.min_stock} {row.original.unit}</span>
            </div>
            <Progress 
              value={stockPercent}
              className={`h-2 ${stockPercent < 30 ? '[&>div]:bg-red-500' : stockPercent < 60 ? '[&>div]:bg-yellow-500' : ''}`}
            />
          </div>
        )
      },
    },
    {
      accessorKey: "warehouse",
      header: "المستودع",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <Warehouse className="w-4 h-4" />
          {row.original.warehouse}
        </div>
      ),
    },
    {
      accessorKey: "price",
      header: "السعر",
      cell: ({ row }) => (
        <span className="font-bold text-green-600">
          {(row.original.price || 0).toLocaleString()} ر.س
        </span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.in_stock
        return (
          <Badge className={config.color}>
            {config.label}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const product = row.original
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
              
              <DropdownMenuItem onClick={() => { setSelectedProduct(product); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => openEditDialog(product)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem onClick={() => { setSelectedProduct(product); setIsAdjustDialogOpen(true); }}>
                <ArrowUpDown className="w-4 h-4 ml-2" />
                تعديل المخزون
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => { setSelectedProduct(product); setIsTransferDialogOpen(true); }}>
                <ArrowRightLeft className="w-4 h-4 ml-2" />
                نقل إلى مستودع آخر
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري إنشاء الباركود...")}>
                <QrCode className="w-4 h-4 ml-2" />
                إنشاء باركود
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل السجل...")}>
                <History className="w-4 h-4 ml-2" />
                سجل الحركات
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem
                onClick={() => { setSelectedProduct(product); setIsDeleteDialogOpen(true); }}
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
            <Package className="w-7 h-7 text-indigo-500" />
            إدارة المخزون
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المنتجات والمخازن</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button variant="outline" onClick={() => toast.info("قريباً...")}>
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 ml-2" />
            منتج جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
              <Package className="w-6 h-6 text-indigo-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalProducts}</p>
              <p className="text-sm text-muted-foreground">منتج</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalValue / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">قيمة المخزون</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.lowStock}</p>
              <p className="text-sm text-muted-foreground">مخزون منخفض</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <Warehouse className="w-6 h-6 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.outOfStock}</p>
              <p className="text-sm text-muted-foreground">نفد المخزون</p>
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
                placeholder="بحث في المنتجات..." 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)} 
                className="pr-10" 
              />
            </div>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="التصنيف" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع التصنيفات</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.name}>{cat.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الحالة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="in_stock">متوفر</SelectItem>
                <SelectItem value="low_stock">منخفض</SelectItem>
                <SelectItem value="out_of_stock">نفد</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={loadInventory}>
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Products Table */}
      <Card>
        <CardHeader>
          <CardTitle>المنتجات ({filteredInventory.length})</CardTitle>
          <CardDescription>قائمة جميع المنتجات والمخزون</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable 
            columns={columns} 
            data={filteredInventory} 
            isLoading={isLoading}
            searchKey="name" 
          />
        </CardContent>
      </Card>

      {/* Create Product Dialog */}
      <FormDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        title="إضافة منتج جديد"
        description="إضافة منتج جديد إلى المخزون"
        onSubmit={form.handleSubmit(handleCreateProduct)}
        isSubmitting={isSubmitting}
        submitText="إضافة المنتج"
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>اسم المنتج</Label>
              <Input {...form.register("name")} placeholder="اسم المنتج" />
              {form.formState.errors.name && (
                <p className="text-sm text-red-500 mt-1">{form.formState.errors.name.message}</p>
              )}
            </div>
            <div>
              <Label>رمز SKU</Label>
              <div className="flex gap-2">
                <Input {...form.register("sku")} placeholder="SKU-001" />
                <Button type="button" variant="outline" onClick={generateSKU}>
                  توليد
                </Button>
              </div>
              {form.formState.errors.sku && (
                <p className="text-sm text-red-500 mt-1">{form.formState.errors.sku.message}</p>
              )}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>التصنيف</Label>
              <Select
                value={form.watch("category")}
                onValueChange={(v) => form.setValue("category", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="اختر التصنيف" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.name}>{cat.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الوحدة</Label>
              <Select
                value={form.watch("unit")}
                onValueChange={(v) => form.setValue("unit", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="كجم">كجم</SelectItem>
                  <SelectItem value="لتر">لتر</SelectItem>
                  <SelectItem value="عبوة">عبوة</SelectItem>
                  <SelectItem value="شتلة">شتلة</SelectItem>
                  <SelectItem value="قطعة">قطعة</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>الكمية الحالية</Label>
              <Input 
                type="number" 
                {...form.register("stock", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
            <div>
              <Label>الحد الأدنى</Label>
              <Input 
                type="number" 
                {...form.register("min_stock", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
            <div>
              <Label>الحد الأقصى</Label>
              <Input 
                type="number" 
                {...form.register("max_stock", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>سعر البيع</Label>
              <Input 
                type="number" 
                {...form.register("price", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
            <div>
              <Label>سعر التكلفة</Label>
              <Input 
                type="number" 
                {...form.register("cost", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
          </div>
          <div>
            <Label>المستودع</Label>
            <Select
              value={form.watch("warehouse_id")}
              onValueChange={(v) => form.setValue("warehouse_id", v)}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر المستودع" />
              </SelectTrigger>
              <SelectContent>
                {warehouses.map((wh) => (
                  <SelectItem key={wh.id} value={wh.id.toString()}>{wh.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>الوصف</Label>
            <Textarea {...form.register("description")} placeholder="وصف المنتج..." />
          </div>
        </div>
      </FormDialog>

      {/* View Product Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={setIsViewDialogOpen}
        title={selectedProduct?.name}
        subtitle={`SKU: ${selectedProduct?.sku}`}
        badge={selectedProduct && {
          text: statusConfig[selectedProduct.status]?.label,
          variant: statusConfig[selectedProduct.status]?.variant,
        }}
        size="lg"
      >
        {selectedProduct && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات المنتج">
              <ViewDialog.Row label="اسم المنتج" value={selectedProduct.name} />
              <ViewDialog.Row label="رمز SKU" value={selectedProduct.sku} />
              <ViewDialog.Row label="التصنيف" value={selectedProduct.category} />
              <ViewDialog.Row label="الوحدة" value={selectedProduct.unit} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="معلومات المخزون">
              <ViewDialog.Row label="الكمية الحالية" value={`${selectedProduct.stock} ${selectedProduct.unit}`} />
              <ViewDialog.Row label="الحد الأدنى" value={`${selectedProduct.min_stock} ${selectedProduct.unit}`} />
              <ViewDialog.Row label="المستودع" value={selectedProduct.warehouse} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="الأسعار">
              <ViewDialog.Row label="سعر البيع" value={`${(selectedProduct.price || 0).toLocaleString()} ر.س`} valueClassName="text-green-600 font-bold" />
              <ViewDialog.Row label="سعر التكلفة" value={`${(selectedProduct.cost || 0).toLocaleString()} ر.س`} />
              <ViewDialog.Row label="هامش الربح" value={`${(((selectedProduct.price - selectedProduct.cost) / selectedProduct.price) * 100).toFixed(1)}%`} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف المنتج"
        description={`هل أنت متأكد من حذف "${selectedProduct?.name}"؟ سيتم حذف جميع البيانات المرتبطة.`}
        variant="danger"
        onConfirm={handleDeleteProduct}
        isLoading={isSubmitting}
      />

      {/* Stock Adjustment Dialog */}
      <FormDialog
        open={isAdjustDialogOpen}
        onOpenChange={setIsAdjustDialogOpen}
        title="تعديل المخزون"
        description={`تعديل مخزون: ${selectedProduct?.name}`}
        onSubmit={(e) => {
          e.preventDefault()
          const formData = new FormData(e.target)
          handleAdjustStock({
            quantity: Number(formData.get('quantity')),
            type: formData.get('type'),
            reason: formData.get('reason'),
          })
        }}
        isSubmitting={isSubmitting}
        submitText="تأكيد التعديل"
      >
        <div className="space-y-4">
          <div>
            <Label>الكمية الحالية</Label>
            <Input value={selectedProduct?.stock || 0} disabled />
          </div>
          <div>
            <Label>نوع التعديل</Label>
            <Select name="type" defaultValue="add">
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="add">إضافة</SelectItem>
                <SelectItem value="subtract">خصم</SelectItem>
                <SelectItem value="set">تعيين</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>الكمية</Label>
            <Input name="quantity" type="number" min="0" placeholder="0" required />
          </div>
          <div>
            <Label>السبب</Label>
            <Textarea name="reason" placeholder="سبب التعديل..." />
          </div>
        </div>
      </FormDialog>
    </div>
  )
}

export default InventoryPage
