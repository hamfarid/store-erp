/**
 * Nurseries Management Page - إدارة المشاتل
 * Gaara ERP v12
 *
 * Complete nursery management with seedlings tracking and production monitoring.
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
  Leaf,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Thermometer,
  Droplets,
  Sun,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Clock,
  RefreshCw,
  Download,
  Upload,
  Sprout,
  TreeDeciduous,
  Map,
  Activity,
  BarChart3,
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
const nurserySchema = z.object({
  name: z.string().min(2, "اسم المشتل مطلوب"),
  code: z.string().min(2, "رمز المشتل مطلوب"),
  type: z.enum(["seedlings", "grafting", "tissue_culture", "mixed"]),
  location: z.string().optional(),
  area: z.number().min(0).default(0),
  capacity: z.number().min(0).default(0),
  manager: z.string().optional(),
  phone: z.string().optional(),
  is_active: z.boolean().default(true),
})

const batchSchema = z.object({
  seed_type: z.string().min(1, "نوع البذور مطلوب"),
  quantity: z.number().min(1, "الكمية مطلوبة"),
  sowing_date: z.string().min(1, "تاريخ الزراعة مطلوب"),
  expected_transplant: z.string().optional(),
  tray_type: z.string().optional(),
  location_in_nursery: z.string().optional(),
})

// Status configurations
const statusConfig = {
  active: { label: "نشط", variant: "default", color: "bg-green-100 text-green-700" },
  inactive: { label: "غير نشط", variant: "secondary", color: "bg-gray-100 text-gray-700" },
  maintenance: { label: "صيانة", variant: "destructive", color: "bg-yellow-100 text-yellow-700" },
}

const batchStatusConfig = {
  sowing: { label: "في الزراعة", color: "bg-blue-100 text-blue-700" },
  germination: { label: "إنبات", color: "bg-emerald-100 text-emerald-700" },
  growing: { label: "نمو", color: "bg-green-100 text-green-700" },
  ready: { label: "جاهز للشتل", color: "bg-amber-100 text-amber-700" },
  transplanted: { label: "تم الشتل", color: "bg-purple-100 text-purple-700" },
}

// Mock data
const mockNurseries = [
  {
    id: "NUR001",
    name: "مشتل الواحة الرئيسي",
    code: "NUR-RYD-01",
    type: "mixed",
    location: "الرياض - حي العليا",
    area: 5000,
    capacity: 100000,
    current_load: 75000,
    manager: "محمد أحمد",
    phone: "0501234567",
    status: "active",
    batches: 12,
    temperature: 28,
    humidity: 65,
  },
  {
    id: "NUR002",
    name: "مشتل الشتلات الخضرية",
    code: "NUR-RYD-02",
    type: "seedlings",
    location: "الرياض - المنطقة الصناعية",
    area: 3000,
    capacity: 60000,
    current_load: 45000,
    manager: "خالد سعيد",
    phone: "0559876543",
    status: "active",
    batches: 8,
    temperature: 26,
    humidity: 70,
  },
  {
    id: "NUR003",
    name: "مشتل التطعيم",
    code: "NUR-JED-01",
    type: "grafting",
    location: "جدة - المنطقة الزراعية",
    area: 2000,
    capacity: 30000,
    current_load: 28000,
    manager: "سارة علي",
    phone: "0541234567",
    status: "active",
    batches: 5,
    temperature: 25,
    humidity: 60,
  },
]

const mockBatches = [
  { id: "BAT001", nursery_id: "NUR001", seed_type: "طماطم هجين", quantity: 5000, sowing_date: "2026-01-10", expected_transplant: "2026-02-15", current_stage: "growing", germination_rate: 92, survival_rate: 88 },
  { id: "BAT002", nursery_id: "NUR001", seed_type: "خيار بيتي", quantity: 3000, sowing_date: "2026-01-12", expected_transplant: "2026-02-10", current_stage: "germination", germination_rate: 85, survival_rate: null },
  { id: "BAT003", nursery_id: "NUR002", seed_type: "فلفل حار", quantity: 4000, sowing_date: "2026-01-05", expected_transplant: "2026-02-20", current_stage: "ready", germination_rate: 90, survival_rate: 85 },
  { id: "BAT004", nursery_id: "NUR001", seed_type: "باذنجان", quantity: 2500, sowing_date: "2026-01-08", expected_transplant: "2026-02-18", current_stage: "growing", germination_rate: 88, survival_rate: 82 },
]

const NurseriesPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("nurseries")
  const [nurseries, setNurseries] = useState(mockNurseries)
  const [batches, setBatches] = useState(mockBatches)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")

  // Dialog states
  const [isNurseryDialogOpen, setIsNurseryDialogOpen] = useState(false)
  const [isBatchDialogOpen, setIsBatchDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedNursery, setSelectedNursery] = useState(null)
  const [selectedBatch, setSelectedBatch] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const nurseryForm = useForm({
    resolver: zodResolver(nurserySchema),
    defaultValues: {
      name: "",
      code: "",
      type: "mixed",
      location: "",
      area: 0,
      capacity: 0,
      manager: "",
      phone: "",
      is_active: true,
    },
  })

  const batchForm = useForm({
    resolver: zodResolver(batchSchema),
    defaultValues: {
      seed_type: "",
      quantity: 0,
      sowing_date: new Date().toISOString().split('T')[0],
      expected_transplant: "",
      tray_type: "",
      location_in_nursery: "",
    },
  })

  // Filter nurseries
  const filteredNurseries = nurseries.filter(n => {
    const matchesSearch = n.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         n.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = typeFilter === "all" || n.type === typeFilter
    return matchesSearch && matchesType
  })

  // Statistics
  const stats = {
    totalNurseries: nurseries.length,
    activeNurseries: nurseries.filter(n => n.status === "active").length,
    totalCapacity: nurseries.reduce((sum, n) => sum + n.capacity, 0),
    currentLoad: nurseries.reduce((sum, n) => sum + n.current_load, 0),
    totalBatches: batches.length,
    readyBatches: batches.filter(b => b.current_stage === "ready").length,
  }

  // Handlers
  const handleCreateNursery = async (data) => {
    setIsSubmitting(true)
    try {
      const newNursery = {
        id: `NUR${String(nurseries.length + 1).padStart(3, '0')}`,
        ...data,
        current_load: 0,
        status: data.is_active ? "active" : "inactive",
        batches: 0,
        temperature: 25,
        humidity: 60,
      }
      setNurseries([...nurseries, newNursery])
      toast.success("تم إضافة المشتل بنجاح")
      setIsNurseryDialogOpen(false)
      nurseryForm.reset()
    } catch (error) {
      toast.error("فشل إضافة المشتل")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCreateBatch = async (data) => {
    setIsSubmitting(true)
    try {
      const newBatch = {
        id: `BAT${String(batches.length + 1).padStart(3, '0')}`,
        nursery_id: selectedNursery?.id || nurseries[0]?.id,
        ...data,
        current_stage: "sowing",
        germination_rate: 0,
        survival_rate: null,
      }
      setBatches([...batches, newBatch])
      toast.success("تم إضافة الدفعة بنجاح")
      setIsBatchDialogOpen(false)
      batchForm.reset()
    } catch (error) {
      toast.error("فشل إضافة الدفعة")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      if (selectedNursery) {
        setNurseries(nurseries.filter(n => n.id !== selectedNursery.id))
        toast.success("تم حذف المشتل")
      }
      setIsDeleteDialogOpen(false)
      setSelectedNursery(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openEditDialog = (nursery) => {
    setSelectedNursery(nursery)
    setDialogMode("edit")
    nurseryForm.reset({
      name: nursery.name,
      code: nursery.code,
      type: nursery.type,
      location: nursery.location,
      area: nursery.area,
      capacity: nursery.capacity,
      manager: nursery.manager,
      phone: nursery.phone,
      is_active: nursery.status === "active",
    })
    setIsNurseryDialogOpen(true)
  }

  // Nursery columns
  const nurseryColumns = [
    {
      accessorKey: "name",
      header: "المشتل",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
            <Leaf className="w-5 h-5 text-emerald-600" />
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
        const types = {
          seedlings: "شتلات",
          grafting: "تطعيم",
          tissue_culture: "زراعة أنسجة",
          mixed: "متعدد",
        }
        return <Badge variant="outline">{types[row.original.type]}</Badge>
      },
    },
    {
      accessorKey: "location",
      header: "الموقع",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Map className="w-4 h-4 text-muted-foreground" />
          {row.original.location}
        </div>
      ),
    },
    {
      accessorKey: "capacity",
      header: "السعة",
      cell: ({ row }) => {
        const percentage = (row.original.current_load / row.original.capacity) * 100
        return (
          <div className="w-28">
            <div className="flex justify-between text-sm mb-1">
              <span>{(row.original.current_load / 1000).toFixed(0)}K</span>
              <span className="text-muted-foreground">/ {(row.original.capacity / 1000).toFixed(0)}K</span>
            </div>
            <Progress value={percentage} className={`h-2 ${percentage > 90 ? '[&>div]:bg-red-500' : ''}`} />
          </div>
        )
      },
    },
    {
      accessorKey: "environment",
      header: "البيئة",
      cell: ({ row }) => (
        <div className="flex items-center gap-3 text-sm">
          <span className="flex items-center gap-1">
            <Thermometer className="w-4 h-4 text-red-500" />
            {row.original.temperature}°C
          </span>
          <span className="flex items-center gap-1">
            <Droplets className="w-4 h-4 text-blue-500" />
            {row.original.humidity}%
          </span>
        </div>
      ),
    },
    {
      accessorKey: "batches",
      header: "الدفعات",
      cell: ({ row }) => <Badge variant="outline">{row.original.batches} دفعة</Badge>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        return <Badge className={config.color}>{config.label}</Badge>
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const nursery = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedNursery(nursery); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(nursery)}>
                <Edit className="w-4 h-4 ml-2" />تعديل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => { setSelectedNursery(nursery); setIsBatchDialogOpen(true); }}>
                <Sprout className="w-4 h-4 ml-2" />إضافة دفعة
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedNursery(nursery); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Batch columns
  const batchColumns = [
    {
      accessorKey: "id",
      header: "رقم الدفعة",
      cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span>,
    },
    { accessorKey: "seed_type", header: "نوع البذور" },
    {
      accessorKey: "quantity",
      header: "الكمية",
      cell: ({ row }) => `${row.original.quantity.toLocaleString()} شتلة`,
    },
    { accessorKey: "sowing_date", header: "تاريخ الزراعة" },
    { accessorKey: "expected_transplant", header: "موعد الشتل المتوقع" },
    {
      accessorKey: "germination_rate",
      header: "نسبة الإنبات",
      cell: ({ row }) => (
        <span className={`font-medium ${row.original.germination_rate >= 85 ? "text-green-600" : "text-yellow-600"}`}>
          {row.original.germination_rate}%
        </span>
      ),
    },
    {
      accessorKey: "current_stage",
      header: "المرحلة",
      cell: ({ row }) => {
        const config = batchStatusConfig[row.original.current_stage]
        return <Badge className={config?.color}>{config?.label}</Badge>
      },
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Leaf className="w-7 h-7 text-emerald-500" />
            إدارة المشاتل
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المشاتل والشتلات والدفعات</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsNurseryDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />مشتل جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalNurseries}</p>
              <p className="text-xs text-muted-foreground">مشتل</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeNurseries}</p>
              <p className="text-xs text-muted-foreground">نشط</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <TreeDeciduous className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.totalCapacity / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">السعة الكلية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Sprout className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.currentLoad / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">شتلة حالية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Activity className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalBatches}</p>
              <p className="text-xs text-muted-foreground">دفعة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.readyBatches}</p>
              <p className="text-xs text-muted-foreground">جاهز للشتل</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="nurseries" className="flex items-center gap-2">
            <Leaf className="w-4 h-4" />المشاتل
          </TabsTrigger>
          <TabsTrigger value="batches" className="flex items-center gap-2">
            <Sprout className="w-4 h-4" />الدفعات
          </TabsTrigger>
        </TabsList>

        {/* Nurseries Tab */}
        <TabsContent value="nurseries" className="space-y-4">
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
                    <SelectItem value="seedlings">شتلات</SelectItem>
                    <SelectItem value="grafting">تطعيم</SelectItem>
                    <SelectItem value="tissue_culture">زراعة أنسجة</SelectItem>
                    <SelectItem value="mixed">متعدد</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>المشاتل ({filteredNurseries.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={nurseryColumns} data={filteredNurseries} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Batches Tab */}
        <TabsContent value="batches" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>دفعات الشتلات ({batches.length})</CardTitle>
              <Button onClick={() => setIsBatchDialogOpen(true)}>
                <Plus className="w-4 h-4 ml-2" />دفعة جديدة
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={batchColumns} data={batches} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Nursery Dialog */}
      <FormDialog
        open={isNurseryDialogOpen}
        onOpenChange={setIsNurseryDialogOpen}
        title={dialogMode === "add" ? "إضافة مشتل جديد" : "تعديل المشتل"}
        description={dialogMode === "add" ? "إضافة مشتل جديد للنظام" : "تعديل بيانات المشتل"}
        onSubmit={nurseryForm.handleSubmit(handleCreateNursery)}
        isSubmitting={isSubmitting}
        submitText={dialogMode === "add" ? "إضافة" : "حفظ"}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>اسم المشتل</Label>
              <Input {...nurseryForm.register("name")} placeholder="مشتل الواحة" />
            </div>
            <div>
              <Label>الرمز</Label>
              <Input {...nurseryForm.register("code")} placeholder="NUR-RYD-01" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>النوع</Label>
              <Select value={nurseryForm.watch("type")} onValueChange={(v) => nurseryForm.setValue("type", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="seedlings">شتلات</SelectItem>
                  <SelectItem value="grafting">تطعيم</SelectItem>
                  <SelectItem value="tissue_culture">زراعة أنسجة</SelectItem>
                  <SelectItem value="mixed">متعدد</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الموقع</Label>
              <Input {...nurseryForm.register("location")} placeholder="الرياض - حي العليا" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المساحة (م²)</Label>
              <Input type="number" {...nurseryForm.register("area", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>السعة (شتلة)</Label>
              <Input type="number" {...nurseryForm.register("capacity", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المدير</Label>
              <Input {...nurseryForm.register("manager")} placeholder="الاسم" />
            </div>
            <div>
              <Label>الهاتف</Label>
              <Input {...nurseryForm.register("phone")} placeholder="0501234567" />
            </div>
          </div>
        </div>
      </FormDialog>

      {/* Batch Dialog */}
      <FormDialog
        open={isBatchDialogOpen}
        onOpenChange={setIsBatchDialogOpen}
        title="إضافة دفعة شتلات"
        description="إضافة دفعة شتلات جديدة للمشتل"
        onSubmit={batchForm.handleSubmit(handleCreateBatch)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>نوع البذور</Label>
              <Input {...batchForm.register("seed_type")} placeholder="طماطم هجين" />
            </div>
            <div>
              <Label>الكمية</Label>
              <Input type="number" {...batchForm.register("quantity", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ الزراعة</Label>
              <Input type="date" {...batchForm.register("sowing_date")} />
            </div>
            <div>
              <Label>موعد الشتل المتوقع</Label>
              <Input type="date" {...batchForm.register("expected_transplant")} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>نوع الصواني</Label>
              <Input {...batchForm.register("tray_type")} placeholder="84 خلية" />
            </div>
            <div>
              <Label>الموقع في المشتل</Label>
              <Input {...batchForm.register("location_in_nursery")} placeholder="قسم A - صف 1" />
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedNursery(null); }}
        title={selectedNursery?.name}
        subtitle={selectedNursery?.code}
        badge={selectedNursery && { text: statusConfig[selectedNursery.status]?.label, variant: "default" }}
        size="lg"
      >
        {selectedNursery && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات المشتل">
              <ViewDialog.Row label="النوع" value={selectedNursery.type} />
              <ViewDialog.Row label="الموقع" value={selectedNursery.location} />
              <ViewDialog.Row label="المساحة" value={`${selectedNursery.area.toLocaleString()} م²`} />
              <ViewDialog.Row label="المدير" value={selectedNursery.manager} />
              <ViewDialog.Row label="الهاتف" value={selectedNursery.phone} />
            </ViewDialog.Section>
            <ViewDialog.Section title="إحصائيات">
              <ViewDialog.Row label="السعة الكلية" value={`${selectedNursery.capacity.toLocaleString()} شتلة`} />
              <ViewDialog.Row label="الحمل الحالي" value={`${selectedNursery.current_load.toLocaleString()} شتلة`} />
              <ViewDialog.Row label="نسبة الإشغال" value={`${((selectedNursery.current_load / selectedNursery.capacity) * 100).toFixed(1)}%`} />
              <ViewDialog.Row label="عدد الدفعات" value={`${selectedNursery.batches} دفعة`} />
            </ViewDialog.Section>
            <ViewDialog.Section title="البيئة">
              <ViewDialog.Row label="درجة الحرارة" value={`${selectedNursery.temperature}°C`} />
              <ViewDialog.Row label="الرطوبة" value={`${selectedNursery.humidity}%`} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف المشتل"
        description={`هل أنت متأكد من حذف "${selectedNursery?.name}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default NurseriesPage
