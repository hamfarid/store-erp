/**
 * Seeds Management Page - إدارة البذور
 * Gaara ERP v12
 *
 * Complete seed inventory management with quality testing and CRUD operations.
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
  Wheat,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Package,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Dna,
  RefreshCw,
  Download,
  Upload,
  TestTube,
  Leaf,
  Droplets,
  ThermometerSun,
  Timer,
  FileText,
  BarChart3,
  History,
  QrCode,
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

// Form schema
const seedSchema = z.object({
  name: z.string().min(2, "اسم البذور مطلوب"),
  name_ar: z.string().optional(),
  scientific_name: z.string().optional(),
  category: z.string().min(1, "التصنيف مطلوب"),
  variety: z.string().optional(),
  origin: z.string().optional(),
  supplier_id: z.string().optional(),
  lot_number: z.string().optional(),
  stock: z.number().min(0).default(0),
  unit: z.string().default("كجم"),
  min_stock: z.number().min(0).default(0),
  price: z.number().min(0).default(0),
  purity: z.number().min(0).max(100).default(0),
  germination: z.number().min(0).max(100).default(0),
  moisture: z.number().min(0).max(100).optional(),
  expiry_date: z.string().optional(),
  production_date: z.string().optional(),
  storage_conditions: z.string().optional(),
  notes: z.string().optional(),
  is_certified: z.boolean().default(false),
  certification_number: z.string().optional(),
})

const testSchema = z.object({
  test_type: z.string().min(1, "نوع الاختبار مطلوب"),
  purity: z.number().min(0).max(100),
  germination: z.number().min(0).max(100),
  moisture: z.number().min(0).max(100).optional(),
  test_date: z.string(),
  tester: z.string().optional(),
  notes: z.string().optional(),
})

// Status configurations
const statusConfig = {
  available: { label: "متاح", variant: "default", color: "bg-green-100 text-green-700" },
  low_stock: { label: "مخزون منخفض", variant: "secondary", color: "bg-yellow-100 text-yellow-700" },
  expired: { label: "منتهي الصلاحية", variant: "destructive", color: "bg-red-100 text-red-700" },
  reserved: { label: "محجوز", variant: "outline", color: "bg-blue-100 text-blue-700" },
  testing: { label: "قيد الفحص", variant: "default", color: "bg-purple-100 text-purple-700" },
}

// Mock data
const mockSeeds = [
  { 
    id: "SED-001", 
    name: "قمح سخا 94", 
    scientific_name: "Triticum aestivum",
    category: "حبوب", 
    variety: "سخا 94",
    origin: "محلي", 
    lot_number: "LOT-2026-001",
    stock: 5000, 
    min_stock: 1000,
    unit: "كجم", 
    price: 15,
    purity: 98.5, 
    germination: 95, 
    moisture: 12,
    expiry_date: "2026-06-01", 
    production_date: "2025-06-01",
    status: "available",
    is_certified: true,
    certification_number: "CERT-2025-001",
    supplier: "مؤسسة البذور الذهبية",
  },
  { 
    id: "SED-002", 
    name: "طماطم هجين GS-12", 
    scientific_name: "Solanum lycopersicum",
    category: "خضروات", 
    variety: "GS-12",
    origin: "هولندا", 
    lot_number: "LOT-2025-045",
    stock: 250, 
    min_stock: 500,
    unit: "كجم", 
    price: 450,
    purity: 99.2, 
    germination: 92, 
    moisture: 8,
    expiry_date: "2025-12-15", 
    production_date: "2024-12-01",
    status: "low_stock",
    is_certified: true,
    certification_number: "NL-CERT-2024-789",
    supplier: "شركة البذور الهولندية",
  },
  { 
    id: "SED-003", 
    name: "ذرة هجين 10", 
    scientific_name: "Zea mays",
    category: "حبوب", 
    variety: "هجين 10",
    origin: "محلي", 
    lot_number: "LOT-2026-012",
    stock: 8000, 
    min_stock: 2000,
    unit: "كجم", 
    price: 25,
    purity: 97.8, 
    germination: 94, 
    moisture: 13,
    expiry_date: "2026-09-01", 
    production_date: "2025-09-01",
    status: "available",
    is_certified: true,
    certification_number: "CERT-2025-034",
    supplier: "مؤسسة البذور الذهبية",
  },
  { 
    id: "SED-004", 
    name: "فلفل كاليفورنيا", 
    scientific_name: "Capsicum annuum",
    category: "خضروات", 
    variety: "كاليفورنيا",
    origin: "إسبانيا", 
    lot_number: "LOT-2024-089",
    stock: 50, 
    min_stock: 100,
    unit: "كجم", 
    price: 380,
    purity: 98.0, 
    germination: 88, 
    moisture: 7,
    expiry_date: "2025-08-01", 
    production_date: "2024-02-01",
    status: "expired",
    is_certified: true,
    certification_number: "ES-CERT-2024-456",
    supplier: "شركة البذور الإسبانية",
  },
  { 
    id: "SED-005", 
    name: "برسيم حجازي", 
    scientific_name: "Medicago sativa",
    category: "علف", 
    variety: "حجازي",
    origin: "محلي", 
    lot_number: "LOT-2026-005",
    stock: 12000, 
    min_stock: 3000,
    unit: "كجم", 
    price: 18,
    purity: 96.5, 
    germination: 90, 
    moisture: 10,
    expiry_date: "2026-03-01", 
    production_date: "2025-03-01",
    status: "available",
    is_certified: false,
    supplier: "مزرعة الواحة",
  },
]

const mockCategories = [
  { id: 1, name: "حبوب", count: 15 },
  { id: 2, name: "خضروات", count: 25 },
  { id: 3, name: "فواكه", count: 10 },
  { id: 4, name: "علف", count: 8 },
  { id: 5, name: "نباتات زينة", count: 12 },
]

const SeedsPage = () => {
  // State
  const [seeds, setSeeds] = useState(mockSeeds)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isTestDialogOpen, setIsTestDialogOpen] = useState(false)
  const [selectedSeed, setSelectedSeed] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const seedForm = useForm({
    resolver: zodResolver(seedSchema),
    defaultValues: {
      name: "",
      scientific_name: "",
      category: "",
      variety: "",
      origin: "",
      lot_number: "",
      stock: 0,
      unit: "كجم",
      min_stock: 0,
      price: 0,
      purity: 0,
      germination: 0,
      moisture: 0,
      expiry_date: "",
      production_date: "",
      storage_conditions: "",
      notes: "",
      is_certified: false,
      certification_number: "",
    },
  })

  const testForm = useForm({
    resolver: zodResolver(testSchema),
    defaultValues: {
      test_type: "standard",
      purity: 0,
      germination: 0,
      moisture: 0,
      test_date: new Date().toISOString().split('T')[0],
      tester: "",
      notes: "",
    },
  })

  // Filter seeds
  const filteredSeeds = seeds.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         s.lot_number?.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = categoryFilter === "all" || s.category === categoryFilter
    const matchesStatus = statusFilter === "all" || s.status === statusFilter
    return matchesSearch && matchesCategory && matchesStatus
  })

  // Statistics
  const stats = {
    total: seeds.length,
    totalStock: seeds.reduce((sum, s) => sum + s.stock, 0),
    lowStock: seeds.filter(s => s.status === "low_stock").length,
    expired: seeds.filter(s => s.status === "expired").length,
    avgGermination: Math.round(seeds.reduce((sum, s) => sum + s.germination, 0) / seeds.length),
  }

  // Handlers
  const handleCreate = async (data) => {
    setIsSubmitting(true)
    try {
      // Simulate API call
      const newSeed = {
        id: `SED-${String(seeds.length + 1).padStart(3, '0')}`,
        ...data,
        status: data.stock <= data.min_stock ? "low_stock" : "available",
      }
      setSeeds([...seeds, newSeed])
      toast.success("تم إضافة البذور بنجاح")
      setIsCreateDialogOpen(false)
      seedForm.reset()
    } catch (error) {
      toast.error("فشل إضافة البذور")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEdit = async (data) => {
    setIsSubmitting(true)
    try {
      setSeeds(seeds.map(s => s.id === selectedSeed.id ? {
        ...s,
        ...data,
        status: data.stock <= data.min_stock ? "low_stock" : "available",
      } : s))
      toast.success("تم تحديث البذور")
      setIsEditDialogOpen(false)
      setSelectedSeed(null)
      seedForm.reset()
    } catch (error) {
      toast.error("فشل تحديث البذور")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setSeeds(seeds.filter(s => s.id !== selectedSeed.id))
      toast.success("تم حذف البذور")
      setIsDeleteDialogOpen(false)
      setSelectedSeed(null)
    } catch (error) {
      toast.error("فشل حذف البذور")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleQualityTest = async (data) => {
    setIsSubmitting(true)
    try {
      setSeeds(seeds.map(s => s.id === selectedSeed.id ? {
        ...s,
        purity: data.purity,
        germination: data.germination,
        moisture: data.moisture,
        last_test_date: data.test_date,
      } : s))
      toast.success("تم تسجيل نتائج الفحص")
      setIsTestDialogOpen(false)
      setSelectedSeed(null)
      testForm.reset()
    } catch (error) {
      toast.error("فشل تسجيل الفحص")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openEditDialog = (seed) => {
    setSelectedSeed(seed)
    seedForm.reset({
      name: seed.name,
      scientific_name: seed.scientific_name || "",
      category: seed.category,
      variety: seed.variety || "",
      origin: seed.origin || "",
      lot_number: seed.lot_number || "",
      stock: seed.stock,
      unit: seed.unit,
      min_stock: seed.min_stock,
      price: seed.price,
      purity: seed.purity,
      germination: seed.germination,
      moisture: seed.moisture || 0,
      expiry_date: seed.expiry_date || "",
      production_date: seed.production_date || "",
      is_certified: seed.is_certified,
      certification_number: seed.certification_number || "",
    })
    setIsEditDialogOpen(true)
  }

  const openTestDialog = (seed) => {
    setSelectedSeed(seed)
    testForm.reset({
      test_type: "standard",
      purity: seed.purity,
      germination: seed.germination,
      moisture: seed.moisture || 0,
      test_date: new Date().toISOString().split('T')[0],
    })
    setIsTestDialogOpen(true)
  }

  // Generate lot number
  const generateLotNumber = () => {
    const year = new Date().getFullYear()
    const num = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
    seedForm.setValue("lot_number", `LOT-${year}-${num}`)
  }

  // Table columns
  const columns = [
    {
      accessorKey: "name",
      header: "البذور",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
            <Wheat className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground">{row.original.lot_number}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "category",
      header: "التصنيف",
      cell: ({ row }) => <Badge variant="outline">{row.original.category}</Badge>,
    },
    {
      accessorKey: "origin",
      header: "المنشأ",
    },
    {
      accessorKey: "stock",
      header: "المخزون",
      cell: ({ row }) => (
        <div className="w-24">
          <div className="flex justify-between text-sm mb-1">
            <span className="font-medium">{row.original.stock.toLocaleString()}</span>
            <span className="text-muted-foreground">{row.original.unit}</span>
          </div>
          <Progress 
            value={Math.min((row.original.stock / (row.original.min_stock * 2)) * 100, 100)}
            className={`h-2 ${row.original.stock < row.original.min_stock ? '[&>div]:bg-red-500' : ''}`}
          />
        </div>
      ),
    },
    {
      accessorKey: "purity",
      header: "النقاوة",
      cell: ({ row }) => (
        <span className={`font-medium ${row.original.purity >= 98 ? "text-green-600" : row.original.purity >= 95 ? "text-yellow-600" : "text-red-600"}`}>
          {row.original.purity}%
        </span>
      ),
    },
    {
      accessorKey: "germination",
      header: "الإنبات",
      cell: ({ row }) => (
        <span className={`font-medium ${row.original.germination >= 90 ? "text-green-600" : row.original.germination >= 80 ? "text-yellow-600" : "text-red-600"}`}>
          {row.original.germination}%
        </span>
      ),
    },
    {
      accessorKey: "expiry_date",
      header: "انتهاء الصلاحية",
      cell: ({ row }) => {
        const expiry = new Date(row.original.expiry_date)
        const now = new Date()
        const isExpired = expiry < now
        const isNearExpiry = !isExpired && (expiry - now) / (1000 * 60 * 60 * 24) < 90
        return (
          <div className={`flex items-center gap-1 ${isExpired ? "text-red-600" : isNearExpiry ? "text-yellow-600" : "text-muted-foreground"}`}>
            <Calendar className="w-4 h-4" />
            {row.original.expiry_date}
          </div>
        )
      },
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.available
        return <Badge className={config.color}>{config.label}</Badge>
      },
    },
    {
      accessorKey: "is_certified",
      header: "معتمد",
      cell: ({ row }) => (
        row.original.is_certified ? (
          <Badge variant="default" className="bg-green-100 text-green-700">
            <CheckCircle2 className="w-3 h-3 ml-1" />
            معتمد
          </Badge>
        ) : (
          <Badge variant="secondary">غير معتمد</Badge>
        )
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const seed = row.original
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
              
              <DropdownMenuItem onClick={() => { setSelectedSeed(seed); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => openEditDialog(seed)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem onClick={() => openTestDialog(seed)}>
                <TestTube className="w-4 h-4 ml-2" />
                فحص الجودة
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري إنشاء الباركود...")}>
                <QrCode className="w-4 h-4 ml-2" />
                إنشاء باركود
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل السجل...")}>
                <History className="w-4 h-4 ml-2" />
                سجل الفحوصات
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري إنشاء الشهادة...")}>
                <FileText className="w-4 h-4 ml-2" />
                شهادة الجودة
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem
                onClick={() => { setSelectedSeed(seed); setIsDeleteDialogOpen(true); }}
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
            <Wheat className="w-7 h-7 text-green-500" />
            إدارة البذور
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة مخزون البذور وفحص الجودة</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button variant="outline" onClick={() => toast.info("جاري الاستيراد...")}>
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 ml-2" />
            إضافة بذور
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Wheat className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">صنف بذور</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalStock / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">إجمالي المخزون</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.lowStock}</p>
              <p className="text-sm text-muted-foreground">مخزون منخفض</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.expired}</p>
              <p className="text-sm text-muted-foreground">منتهي الصلاحية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.avgGermination}%</p>
              <p className="text-sm text-muted-foreground">متوسط الإنبات</p>
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
                placeholder="بحث بالاسم أو رقم الدفعة..."
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
                {mockCategories.map((cat) => (
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
                <SelectItem value="available">متاح</SelectItem>
                <SelectItem value="low_stock">مخزون منخفض</SelectItem>
                <SelectItem value="expired">منتهي الصلاحية</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={() => setIsLoading(true)}>
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Seeds Table */}
      <Card>
        <CardHeader>
          <CardTitle>البذور ({filteredSeeds.length})</CardTitle>
          <CardDescription>قائمة جميع أصناف البذور</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredSeeds} isLoading={isLoading} searchKey="name" />
        </CardContent>
      </Card>

      {/* Create/Edit Dialog */}
      <FormDialog
        open={isCreateDialogOpen || isEditDialogOpen}
        onOpenChange={(open) => {
          if (!open) {
            setIsCreateDialogOpen(false)
            setIsEditDialogOpen(false)
            setSelectedSeed(null)
            seedForm.reset()
          }
        }}
        title={isEditDialogOpen ? "تعديل بيانات البذور" : "إضافة بذور جديدة"}
        description={isEditDialogOpen ? "تعديل بيانات البذور" : "إضافة صنف بذور جديد للمخزون"}
        onSubmit={seedForm.handleSubmit(isEditDialogOpen ? handleEdit : handleCreate)}
        isSubmitting={isSubmitting}
        submitText={isEditDialogOpen ? "حفظ" : "إضافة"}
        size="xl"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>اسم البذور</Label>
              <Input {...seedForm.register("name")} placeholder="قمح سخا 94" />
              {seedForm.formState.errors.name && (
                <p className="text-sm text-red-500 mt-1">{seedForm.formState.errors.name.message}</p>
              )}
            </div>
            <div>
              <Label>الاسم العلمي</Label>
              <Input {...seedForm.register("scientific_name")} placeholder="Triticum aestivum" />
            </div>
            <div>
              <Label>الصنف</Label>
              <Input {...seedForm.register("variety")} placeholder="سخا 94" />
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>التصنيف</Label>
              <Select
                value={seedForm.watch("category")}
                onValueChange={(v) => seedForm.setValue("category", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="اختر التصنيف" />
                </SelectTrigger>
                <SelectContent>
                  {mockCategories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.name}>{cat.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>المنشأ</Label>
              <Input {...seedForm.register("origin")} placeholder="محلي / مستورد" />
            </div>
            <div>
              <Label>رقم الدفعة</Label>
              <div className="flex gap-2">
                <Input {...seedForm.register("lot_number")} placeholder="LOT-2026-001" />
                <Button type="button" variant="outline" size="icon" onClick={generateLotNumber}>
                  <RefreshCw className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-4 gap-4">
            <div>
              <Label>الكمية</Label>
              <Input type="number" {...seedForm.register("stock", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>الوحدة</Label>
              <Select
                value={seedForm.watch("unit")}
                onValueChange={(v) => seedForm.setValue("unit", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="كجم">كجم</SelectItem>
                  <SelectItem value="جرام">جرام</SelectItem>
                  <SelectItem value="عبوة">عبوة</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الحد الأدنى</Label>
              <Input type="number" {...seedForm.register("min_stock", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>السعر (ر.س)</Label>
              <Input type="number" {...seedForm.register("price", { valueAsNumber: true })} />
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>النقاوة %</Label>
              <Input type="number" step="0.1" max="100" {...seedForm.register("purity", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>نسبة الإنبات %</Label>
              <Input type="number" step="0.1" max="100" {...seedForm.register("germination", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>الرطوبة %</Label>
              <Input type="number" step="0.1" max="100" {...seedForm.register("moisture", { valueAsNumber: true })} />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ الإنتاج</Label>
              <Input type="date" {...seedForm.register("production_date")} />
            </div>
            <div>
              <Label>تاريخ انتهاء الصلاحية</Label>
              <Input type="date" {...seedForm.register("expiry_date")} />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2 space-x-reverse">
              <input
                type="checkbox"
                id="is_certified"
                {...seedForm.register("is_certified")}
                className="rounded border-gray-300"
              />
              <Label htmlFor="is_certified">بذور معتمدة</Label>
            </div>
            <div>
              <Label>رقم الشهادة</Label>
              <Input {...seedForm.register("certification_number")} placeholder="CERT-2025-001" />
            </div>
          </div>
          
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...seedForm.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
        </div>
      </FormDialog>

      {/* Quality Test Dialog */}
      <FormDialog
        open={isTestDialogOpen}
        onOpenChange={(open) => { setIsTestDialogOpen(open); if (!open) setSelectedSeed(null); }}
        title={`فحص جودة: ${selectedSeed?.name}`}
        description="تسجيل نتائج فحص جودة البذور"
        onSubmit={testForm.handleSubmit(handleQualityTest)}
        isSubmitting={isSubmitting}
        submitText="حفظ النتائج"
      >
        <div className="space-y-4">
          <div>
            <Label>نوع الفحص</Label>
            <Select
              value={testForm.watch("test_type")}
              onValueChange={(v) => testForm.setValue("test_type", v)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="standard">فحص قياسي</SelectItem>
                <SelectItem value="detailed">فحص تفصيلي</SelectItem>
                <SelectItem value="certification">فحص اعتماد</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>النقاوة %</Label>
              <Input type="number" step="0.1" max="100" {...testForm.register("purity", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>نسبة الإنبات %</Label>
              <Input type="number" step="0.1" max="100" {...testForm.register("germination", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>الرطوبة %</Label>
              <Input type="number" step="0.1" max="100" {...testForm.register("moisture", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ الفحص</Label>
              <Input type="date" {...testForm.register("test_date")} />
            </div>
            <div>
              <Label>الفاحص</Label>
              <Input {...testForm.register("tester")} placeholder="اسم الفاحص" />
            </div>
          </div>
          <div>
            <Label>ملاحظات الفحص</Label>
            <Textarea {...testForm.register("notes")} placeholder="ملاحظات..." />
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedSeed(null); }}
        title={selectedSeed?.name}
        subtitle={`${selectedSeed?.scientific_name} - ${selectedSeed?.lot_number}`}
        badge={selectedSeed && {
          text: statusConfig[selectedSeed.status]?.label,
          variant: statusConfig[selectedSeed.status]?.variant,
        }}
        size="lg"
      >
        {selectedSeed && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات البذور">
              <ViewDialog.Row label="الاسم" value={selectedSeed.name} />
              <ViewDialog.Row label="الاسم العلمي" value={selectedSeed.scientific_name || "—"} />
              <ViewDialog.Row label="التصنيف" value={selectedSeed.category} />
              <ViewDialog.Row label="الصنف" value={selectedSeed.variety || "—"} />
              <ViewDialog.Row label="المنشأ" value={selectedSeed.origin} />
              <ViewDialog.Row label="المورد" value={selectedSeed.supplier || "—"} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="معلومات المخزون">
              <ViewDialog.Row label="الكمية الحالية" value={`${selectedSeed.stock.toLocaleString()} ${selectedSeed.unit}`} />
              <ViewDialog.Row label="الحد الأدنى" value={`${selectedSeed.min_stock.toLocaleString()} ${selectedSeed.unit}`} />
              <ViewDialog.Row label="السعر" value={`${selectedSeed.price} ر.س / ${selectedSeed.unit}`} />
              <ViewDialog.Row label="رقم الدفعة" value={selectedSeed.lot_number} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="الجودة">
              <ViewDialog.Row label="النقاوة" value={`${selectedSeed.purity}%`} valueClassName={selectedSeed.purity >= 98 ? "text-green-600" : "text-yellow-600"} />
              <ViewDialog.Row label="نسبة الإنبات" value={`${selectedSeed.germination}%`} valueClassName={selectedSeed.germination >= 90 ? "text-green-600" : "text-yellow-600"} />
              <ViewDialog.Row label="الرطوبة" value={`${selectedSeed.moisture || 0}%`} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="التواريخ">
              <ViewDialog.Row label="تاريخ الإنتاج" value={selectedSeed.production_date || "—"} />
              <ViewDialog.Row label="تاريخ انتهاء الصلاحية" value={selectedSeed.expiry_date} />
            </ViewDialog.Section>
            
            {selectedSeed.is_certified && (
              <ViewDialog.Section title="الاعتماد">
                <ViewDialog.Row label="معتمد" value="نعم" valueClassName="text-green-600" />
                <ViewDialog.Row label="رقم الشهادة" value={selectedSeed.certification_number} />
              </ViewDialog.Section>
            )}
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف البذور"
        description={`هل أنت متأكد من حذف "${selectedSeed?.name}"؟ سيتم حذف جميع البيانات المرتبطة.`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default SeedsPage
