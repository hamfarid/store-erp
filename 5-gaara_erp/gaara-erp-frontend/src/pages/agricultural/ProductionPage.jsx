/**
 * Production Management Page - إدارة الإنتاج الزراعي
 * Gaara ERP v12
 *
 * Complete agricultural production tracking with harvest management.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Tractor,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Clock,
  RefreshCw,
  Download,
  Wheat,
  Target,
  BarChart3,
  TrendingUp,
  Map,
  Droplets,
  Sun,
  Thermometer,
  Scale,
  Package,
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
const productionSchema = z.object({
  crop: z.string().min(1, "المحصول مطلوب"),
  variety: z.string().optional(),
  farm_id: z.string().min(1, "المزرعة مطلوبة"),
  field_id: z.string().optional(),
  area: z.number().min(0).default(0),
  planting_date: z.string().min(1, "تاريخ الزراعة مطلوب"),
  expected_harvest: z.string().optional(),
  expected_yield: z.number().min(0).optional(),
  notes: z.string().optional(),
})

const harvestSchema = z.object({
  production_id: z.string().min(1),
  harvest_date: z.string().min(1, "تاريخ الحصاد مطلوب"),
  quantity: z.number().min(0, "الكمية مطلوبة"),
  quality_grade: z.string().optional(),
  storage_location: z.string().optional(),
  notes: z.string().optional(),
})

// Status configurations
const statusConfig = {
  planning: { label: "تخطيط", color: "bg-gray-100 text-gray-700" },
  planted: { label: "مزروع", color: "bg-blue-100 text-blue-700" },
  growing: { label: "في النمو", color: "bg-emerald-100 text-emerald-700" },
  flowering: { label: "تزهير", color: "bg-pink-100 text-pink-700" },
  fruiting: { label: "إثمار", color: "bg-orange-100 text-orange-700" },
  ready: { label: "جاهز للحصاد", color: "bg-amber-100 text-amber-700" },
  harvested: { label: "تم الحصاد", color: "bg-green-100 text-green-700" },
  completed: { label: "مكتمل", color: "bg-purple-100 text-purple-700" },
}

// Mock data
const mockProductions = [
  {
    id: "PRD001",
    crop: "قمح",
    variety: "سخا 94",
    farm: "مزرعة الواحة",
    farm_id: "FRM001",
    field: "حقل A-1",
    area: 50,
    planting_date: "2025-11-15",
    expected_harvest: "2026-04-15",
    expected_yield: 150,
    actual_yield: null,
    status: "growing",
    progress: 65,
    weather: { temp: 22, humidity: 45, rain: 2 },
  },
  {
    id: "PRD002",
    crop: "طماطم",
    variety: "هجين GS-12",
    farm: "مزرعة النخيل",
    farm_id: "FRM002",
    field: "صوب 1-3",
    area: 2,
    planting_date: "2025-12-01",
    expected_harvest: "2026-02-15",
    expected_yield: 20,
    actual_yield: null,
    status: "fruiting",
    progress: 80,
    weather: { temp: 28, humidity: 70, rain: 0 },
  },
  {
    id: "PRD003",
    crop: "برسيم",
    variety: "حجازي",
    farm: "مزرعة الفردوس",
    farm_id: "FRM003",
    field: "حقل C-2",
    area: 100,
    planting_date: "2025-10-01",
    expected_harvest: "2026-01-20",
    expected_yield: 400,
    actual_yield: 420,
    status: "harvested",
    progress: 100,
    weather: { temp: 18, humidity: 50, rain: 5 },
  },
]

const mockHarvests = [
  { id: "HRV001", production_id: "PRD003", crop: "برسيم", harvest_date: "2026-01-15", quantity: 200, quality: "A", storage: "مستودع 1" },
  { id: "HRV002", production_id: "PRD003", crop: "برسيم", harvest_date: "2026-01-18", quantity: 220, quality: "A", storage: "مستودع 1" },
]

const mockFarms = [
  { id: "FRM001", name: "مزرعة الواحة" },
  { id: "FRM002", name: "مزرعة النخيل" },
  { id: "FRM003", name: "مزرعة الفردوس" },
]

const ProductionPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("productions")
  const [productions, setProductions] = useState(mockProductions)
  const [harvests, setHarvests] = useState(mockHarvests)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isProductionDialogOpen, setIsProductionDialogOpen] = useState(false)
  const [isHarvestDialogOpen, setIsHarvestDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedProduction, setSelectedProduction] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const productionForm = useForm({
    resolver: zodResolver(productionSchema),
    defaultValues: {
      crop: "",
      variety: "",
      farm_id: "",
      field_id: "",
      area: 0,
      planting_date: "",
      expected_harvest: "",
      expected_yield: 0,
      notes: "",
    },
  })

  const harvestForm = useForm({
    resolver: zodResolver(harvestSchema),
    defaultValues: {
      production_id: "",
      harvest_date: new Date().toISOString().split('T')[0],
      quantity: 0,
      quality_grade: "A",
      storage_location: "",
      notes: "",
    },
  })

  // Filter productions
  const filteredProductions = productions.filter(p => {
    const matchesSearch = p.crop.includes(searchQuery) || p.farm.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || p.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Statistics
  const stats = {
    totalProductions: productions.length,
    activeProductions: productions.filter(p => !["harvested", "completed"].includes(p.status)).length,
    totalArea: productions.reduce((sum, p) => sum + p.area, 0),
    expectedYield: productions.reduce((sum, p) => sum + (p.expected_yield || 0), 0),
    actualYield: productions.reduce((sum, p) => sum + (p.actual_yield || 0), 0),
    readyToHarvest: productions.filter(p => p.status === "ready").length,
  }

  // Handlers
  const handleCreateProduction = async (data) => {
    setIsSubmitting(true)
    try {
      const farm = mockFarms.find(f => f.id === data.farm_id)
      const newProduction = {
        id: `PRD${String(productions.length + 1).padStart(3, '0')}`,
        ...data,
        farm: farm?.name || "",
        actual_yield: null,
        status: "planning",
        progress: 0,
        weather: { temp: 25, humidity: 50, rain: 0 },
      }
      setProductions([...productions, newProduction])
      toast.success("تم إضافة دورة الإنتاج بنجاح")
      setIsProductionDialogOpen(false)
      productionForm.reset()
    } catch (error) {
      toast.error("فشل إضافة دورة الإنتاج")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCreateHarvest = async (data) => {
    setIsSubmitting(true)
    try {
      const newHarvest = {
        id: `HRV${String(harvests.length + 1).padStart(3, '0')}`,
        ...data,
        crop: selectedProduction?.crop || "",
        quality: data.quality_grade,
        storage: data.storage_location,
      }
      setHarvests([...harvests, newHarvest])
      
      // Update production actual yield
      setProductions(productions.map(p => {
        if (p.id === data.production_id) {
          return {
            ...p,
            actual_yield: (p.actual_yield || 0) + data.quantity,
            status: "harvested",
          }
        }
        return p
      }))
      
      toast.success("تم تسجيل الحصاد بنجاح")
      setIsHarvestDialogOpen(false)
      harvestForm.reset()
    } catch (error) {
      toast.error("فشل تسجيل الحصاد")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setProductions(productions.filter(p => p.id !== selectedProduction.id))
      toast.success("تم حذف دورة الإنتاج")
      setIsDeleteDialogOpen(false)
      setSelectedProduction(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openHarvestDialog = (production) => {
    setSelectedProduction(production)
    harvestForm.reset({
      production_id: production.id,
      harvest_date: new Date().toISOString().split('T')[0],
    })
    setIsHarvestDialogOpen(true)
  }

  // Production columns
  const productionColumns = [
    {
      accessorKey: "crop",
      header: "المحصول",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
            <Wheat className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.crop}</p>
            <p className="text-sm text-muted-foreground">{row.original.variety}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "farm",
      header: "المزرعة",
      cell: ({ row }) => (
        <div>
          <p>{row.original.farm}</p>
          <p className="text-sm text-muted-foreground">{row.original.field}</p>
        </div>
      ),
    },
    {
      accessorKey: "area",
      header: "المساحة",
      cell: ({ row }) => `${row.original.area} هكتار`,
    },
    {
      accessorKey: "dates",
      header: "التواريخ",
      cell: ({ row }) => (
        <div className="text-sm">
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            زراعة: {row.original.planting_date}
          </div>
          <div className="flex items-center gap-1 text-muted-foreground">
            <Target className="w-3 h-3" />
            حصاد: {row.original.expected_harvest}
          </div>
        </div>
      ),
    },
    {
      accessorKey: "progress",
      header: "التقدم",
      cell: ({ row }) => (
        <div className="w-24">
          <div className="flex justify-between text-sm mb-1">
            <span>{row.original.progress}%</span>
          </div>
          <Progress value={row.original.progress} className="h-2" />
        </div>
      ),
    },
    {
      accessorKey: "yield",
      header: "الإنتاج",
      cell: ({ row }) => (
        <div className="text-sm">
          <p>متوقع: {row.original.expected_yield} طن</p>
          {row.original.actual_yield && (
            <p className="text-green-600">فعلي: {row.original.actual_yield} طن</p>
          )}
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        return <Badge className={config?.color}>{config?.label}</Badge>
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const production = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedProduction(production); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => { setSelectedProduction(production); setDialogMode("edit"); setIsProductionDialogOpen(true); }}>
                <Edit className="w-4 h-4 ml-2" />تعديل
              </DropdownMenuItem>
              {!["harvested", "completed"].includes(production.status) && (
                <DropdownMenuItem onClick={() => openHarvestDialog(production)}>
                  <Scale className="w-4 h-4 ml-2" />تسجيل حصاد
                </DropdownMenuItem>
              )}
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedProduction(production); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Harvest columns
  const harvestColumns = [
    { accessorKey: "id", header: "رقم الحصاد", cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span> },
    { accessorKey: "crop", header: "المحصول" },
    { accessorKey: "harvest_date", header: "تاريخ الحصاد" },
    { accessorKey: "quantity", header: "الكمية", cell: ({ row }) => `${row.original.quantity} طن` },
    { accessorKey: "quality", header: "الجودة", cell: ({ row }) => <Badge variant="outline">{row.original.quality}</Badge> },
    { accessorKey: "storage", header: "التخزين" },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Tractor className="w-7 h-7 text-green-500" />
            إدارة الإنتاج الزراعي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">متابعة دورات الإنتاج والحصاد</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsProductionDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />دورة إنتاج جديدة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <Tractor className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalProductions}</p>
              <p className="text-xs text-muted-foreground">دورة إنتاج</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Wheat className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeProductions}</p>
              <p className="text-xs text-muted-foreground">نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <Map className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalArea}</p>
              <p className="text-xs text-muted-foreground">هكتار</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Target className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.expectedYield}</p>
              <p className="text-xs text-muted-foreground">طن متوقع</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Scale className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.actualYield}</p>
              <p className="text-xs text-muted-foreground">طن فعلي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.readyToHarvest}</p>
              <p className="text-xs text-muted-foreground">جاهز للحصاد</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="productions" className="flex items-center gap-2">
            <Tractor className="w-4 h-4" />دورات الإنتاج
          </TabsTrigger>
          <TabsTrigger value="harvests" className="flex items-center gap-2">
            <Scale className="w-4 h-4" />سجل الحصاد
          </TabsTrigger>
        </TabsList>

        {/* Productions Tab */}
        <TabsContent value="productions" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[180px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="planning">تخطيط</SelectItem>
                    <SelectItem value="planted">مزروع</SelectItem>
                    <SelectItem value="growing">في النمو</SelectItem>
                    <SelectItem value="ready">جاهز للحصاد</SelectItem>
                    <SelectItem value="harvested">تم الحصاد</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>دورات الإنتاج ({filteredProductions.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={productionColumns} data={filteredProductions} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Harvests Tab */}
        <TabsContent value="harvests" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>سجل الحصاد ({harvests.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={harvestColumns} data={harvests} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Production Dialog */}
      <FormDialog
        open={isProductionDialogOpen}
        onOpenChange={setIsProductionDialogOpen}
        title={dialogMode === "add" ? "إضافة دورة إنتاج" : "تعديل دورة الإنتاج"}
        description="تسجيل دورة إنتاج زراعي جديدة"
        onSubmit={productionForm.handleSubmit(handleCreateProduction)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المحصول</Label>
              <Input {...productionForm.register("crop")} placeholder="قمح" />
            </div>
            <div>
              <Label>الصنف</Label>
              <Input {...productionForm.register("variety")} placeholder="سخا 94" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المزرعة</Label>
              <Select value={productionForm.watch("farm_id")} onValueChange={(v) => productionForm.setValue("farm_id", v)}>
                <SelectTrigger><SelectValue placeholder="اختر المزرعة" /></SelectTrigger>
                <SelectContent>
                  {mockFarms.map((f) => <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>المساحة (هكتار)</Label>
              <Input type="number" {...productionForm.register("area", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ الزراعة</Label>
              <Input type="date" {...productionForm.register("planting_date")} />
            </div>
            <div>
              <Label>تاريخ الحصاد المتوقع</Label>
              <Input type="date" {...productionForm.register("expected_harvest")} />
            </div>
          </div>
          <div>
            <Label>الإنتاج المتوقع (طن)</Label>
            <Input type="number" {...productionForm.register("expected_yield", { valueAsNumber: true })} />
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...productionForm.register("notes")} placeholder="ملاحظات..." />
          </div>
        </div>
      </FormDialog>

      {/* Harvest Dialog */}
      <FormDialog
        open={isHarvestDialogOpen}
        onOpenChange={setIsHarvestDialogOpen}
        title="تسجيل حصاد"
        description={`تسجيل حصاد لـ ${selectedProduction?.crop}`}
        onSubmit={harvestForm.handleSubmit(handleCreateHarvest)}
        isSubmitting={isSubmitting}
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ الحصاد</Label>
              <Input type="date" {...harvestForm.register("harvest_date")} />
            </div>
            <div>
              <Label>الكمية (طن)</Label>
              <Input type="number" {...harvestForm.register("quantity", { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>درجة الجودة</Label>
              <Select value={harvestForm.watch("quality_grade")} onValueChange={(v) => harvestForm.setValue("quality_grade", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="A">A - ممتاز</SelectItem>
                  <SelectItem value="B">B - جيد</SelectItem>
                  <SelectItem value="C">C - مقبول</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>موقع التخزين</Label>
              <Input {...harvestForm.register("storage_location")} placeholder="مستودع 1" />
            </div>
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...harvestForm.register("notes")} placeholder="ملاحظات..." />
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedProduction(null); }}
        title={`${selectedProduction?.crop} - ${selectedProduction?.variety}`}
        subtitle={selectedProduction?.farm}
        badge={selectedProduction && { text: statusConfig[selectedProduction.status]?.label }}
        size="lg"
      >
        {selectedProduction && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات الإنتاج">
              <ViewDialog.Row label="المحصول" value={selectedProduction.crop} />
              <ViewDialog.Row label="الصنف" value={selectedProduction.variety} />
              <ViewDialog.Row label="المزرعة" value={selectedProduction.farm} />
              <ViewDialog.Row label="الحقل" value={selectedProduction.field} />
              <ViewDialog.Row label="المساحة" value={`${selectedProduction.area} هكتار`} />
            </ViewDialog.Section>
            <ViewDialog.Section title="التواريخ">
              <ViewDialog.Row label="تاريخ الزراعة" value={selectedProduction.planting_date} />
              <ViewDialog.Row label="الحصاد المتوقع" value={selectedProduction.expected_harvest} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الإنتاج">
              <ViewDialog.Row label="المتوقع" value={`${selectedProduction.expected_yield} طن`} />
              <ViewDialog.Row label="الفعلي" value={selectedProduction.actual_yield ? `${selectedProduction.actual_yield} طن` : "—"} valueClassName={selectedProduction.actual_yield ? "text-green-600" : ""} />
              <ViewDialog.Row label="التقدم" value={`${selectedProduction.progress}%`} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف دورة الإنتاج"
        description={`هل أنت متأكد من حذف دورة إنتاج "${selectedProduction?.crop}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default ProductionPage
