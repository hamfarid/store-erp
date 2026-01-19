/**
 * Agricultural Experiments Page - التجارب الزراعية
 * Gaara ERP v12
 *
 * Agricultural experiments management with data collection and analysis.
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
  FlaskConical,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Calendar,
  CheckCircle2,
  Clock,
  RefreshCw,
  Download,
  FileText,
  BarChart3,
  Target,
  Users,
  Beaker,
  Clipboard,
  TrendingUp,
  AlertTriangle,
  Play,
  Pause,
  Square,
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
const experimentSchema = z.object({
  title: z.string().min(5, "عنوان التجربة مطلوب"),
  code: z.string().optional(),
  type: z.enum(["variety_trial", "fertilizer_trial", "pest_control", "irrigation", "other"]),
  objective: z.string().min(10, "الهدف مطلوب"),
  crop: z.string().min(1, "المحصول مطلوب"),
  location: z.string().optional(),
  start_date: z.string().min(1, "تاريخ البدء مطلوب"),
  expected_end: z.string().optional(),
  researcher: z.string().optional(),
  treatments: z.number().min(1).default(1),
  replications: z.number().min(1).default(3),
  design: z.string().optional(),
})

// Status configurations
const statusConfig = {
  planning: { label: "تخطيط", color: "bg-gray-100 text-gray-700", icon: Clipboard },
  active: { label: "جاري التنفيذ", color: "bg-blue-100 text-blue-700", icon: Play },
  paused: { label: "متوقف", color: "bg-yellow-100 text-yellow-700", icon: Pause },
  completed: { label: "مكتمل", color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  cancelled: { label: "ملغي", color: "bg-red-100 text-red-700", icon: Square },
}

const typeConfig = {
  variety_trial: { label: "تجارب أصناف", color: "bg-emerald-100 text-emerald-700" },
  fertilizer_trial: { label: "تجارب أسمدة", color: "bg-blue-100 text-blue-700" },
  pest_control: { label: "مكافحة آفات", color: "bg-orange-100 text-orange-700" },
  irrigation: { label: "تجارب ري", color: "bg-cyan-100 text-cyan-700" },
  other: { label: "أخرى", color: "bg-gray-100 text-gray-700" },
}

// Mock data
const mockExperiments = [
  {
    id: "EXP001",
    title: "تقييم أصناف الطماطم الجديدة",
    code: "VT-2026-001",
    type: "variety_trial",
    objective: "مقارنة إنتاجية وجودة 5 أصناف طماطم هجينة جديدة",
    crop: "طماطم",
    location: "مزرعة الواحة - صوب التجارب",
    start_date: "2026-01-01",
    expected_end: "2026-04-30",
    researcher: "د. أحمد محمد",
    treatments: 5,
    replications: 4,
    design: "RCBD",
    status: "active",
    progress: 45,
    data_entries: 120,
  },
  {
    id: "EXP002",
    title: "تأثير مستويات النيتروجين على القمح",
    code: "FT-2026-002",
    type: "fertilizer_trial",
    objective: "دراسة تأثير 4 مستويات من النيتروجين على إنتاجية القمح",
    crop: "قمح",
    location: "مزرعة الفردوس - حقل A",
    start_date: "2025-11-15",
    expected_end: "2026-05-01",
    researcher: "د. سارة علي",
    treatments: 4,
    replications: 3,
    design: "RCBD",
    status: "active",
    progress: 60,
    data_entries: 85,
  },
  {
    id: "EXP003",
    title: "مقارنة طرق الري بالتنقيط",
    code: "IR-2025-010",
    type: "irrigation",
    objective: "مقارنة كفاءة 3 أنظمة ري بالتنقيط على الخيار",
    crop: "خيار",
    location: "مزرعة النخيل",
    start_date: "2025-09-01",
    expected_end: "2025-12-31",
    researcher: "م. خالد سعيد",
    treatments: 3,
    replications: 4,
    design: "CRD",
    status: "completed",
    progress: 100,
    data_entries: 200,
  },
]

const mockDataEntries = [
  { id: 1, experiment_id: "EXP001", date: "2026-01-15", treatment: "صنف A", rep: 1, measurement: "ارتفاع", value: 45, unit: "سم" },
  { id: 2, experiment_id: "EXP001", date: "2026-01-15", treatment: "صنف A", rep: 2, measurement: "ارتفاع", value: 48, unit: "سم" },
  { id: 3, experiment_id: "EXP001", date: "2026-01-15", treatment: "صنف B", rep: 1, measurement: "ارتفاع", value: 42, unit: "سم" },
]

const ExperimentsPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("experiments")
  const [experiments, setExperiments] = useState(mockExperiments)
  const [dataEntries, setDataEntries] = useState(mockDataEntries)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isExperimentDialogOpen, setIsExperimentDialogOpen] = useState(false)
  const [isDataEntryDialogOpen, setIsDataEntryDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedExperiment, setSelectedExperiment] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const experimentForm = useForm({
    resolver: zodResolver(experimentSchema),
    defaultValues: {
      title: "",
      code: "",
      type: "variety_trial",
      objective: "",
      crop: "",
      location: "",
      start_date: new Date().toISOString().split('T')[0],
      expected_end: "",
      researcher: "",
      treatments: 3,
      replications: 3,
      design: "RCBD",
    },
  })

  // Filter experiments
  const filteredExperiments = experiments.filter(e => {
    const matchesSearch = e.title.includes(searchQuery) || 
                         e.code?.includes(searchQuery) ||
                         e.crop.includes(searchQuery)
    const matchesType = typeFilter === "all" || e.type === typeFilter
    const matchesStatus = statusFilter === "all" || e.status === statusFilter
    return matchesSearch && matchesType && matchesStatus
  })

  // Statistics
  const stats = {
    totalExperiments: experiments.length,
    activeExperiments: experiments.filter(e => e.status === "active").length,
    completedExperiments: experiments.filter(e => e.status === "completed").length,
    totalDataEntries: experiments.reduce((sum, e) => sum + e.data_entries, 0),
    avgProgress: Math.round(experiments.reduce((sum, e) => sum + e.progress, 0) / experiments.length),
  }

  // Handlers
  const handleCreateExperiment = async (data) => {
    setIsSubmitting(true)
    try {
      const newExperiment = {
        id: `EXP${String(experiments.length + 1).padStart(3, '0')}`,
        ...data,
        status: "planning",
        progress: 0,
        data_entries: 0,
      }
      setExperiments([...experiments, newExperiment])
      toast.success("تم إنشاء التجربة بنجاح")
      setIsExperimentDialogOpen(false)
      experimentForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء التجربة")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleStartExperiment = (experiment) => {
    setExperiments(experiments.map(e => 
      e.id === experiment.id ? { ...e, status: "active" } : e
    ))
    toast.success("تم بدء التجربة")
  }

  const handlePauseExperiment = (experiment) => {
    setExperiments(experiments.map(e => 
      e.id === experiment.id ? { ...e, status: "paused" } : e
    ))
    toast.success("تم إيقاف التجربة")
  }

  const handleCompleteExperiment = (experiment) => {
    setExperiments(experiments.map(e => 
      e.id === experiment.id ? { ...e, status: "completed", progress: 100 } : e
    ))
    toast.success("تم إكمال التجربة")
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setExperiments(experiments.filter(e => e.id !== selectedExperiment.id))
      toast.success("تم حذف التجربة")
      setIsDeleteDialogOpen(false)
      setSelectedExperiment(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  const generateCode = () => {
    const type = experimentForm.watch("type")
    const prefixes = { variety_trial: "VT", fertilizer_trial: "FT", pest_control: "PC", irrigation: "IR", other: "OT" }
    const year = new Date().getFullYear()
    const num = String(experiments.length + 1).padStart(3, '0')
    experimentForm.setValue("code", `${prefixes[type] || "EX"}-${year}-${num}`)
  }

  // Experiment columns
  const experimentColumns = [
    {
      accessorKey: "title",
      header: "التجربة",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
            <FlaskConical className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.title}</p>
            <p className="text-sm text-muted-foreground font-mono">{row.original.code}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => {
        const config = typeConfig[row.original.type]
        return <Badge className={config?.color}>{config?.label}</Badge>
      },
    },
    { accessorKey: "crop", header: "المحصول" },
    { accessorKey: "researcher", header: "الباحث" },
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
      accessorKey: "data_entries",
      header: "البيانات",
      cell: ({ row }) => <Badge variant="outline">{row.original.data_entries} سجل</Badge>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <Badge className={config?.color}>
            <Icon className="w-3 h-3 ml-1" />
            {config?.label}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const experiment = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedExperiment(experiment); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              {experiment.status === "planning" && (
                <DropdownMenuItem onClick={() => handleStartExperiment(experiment)}>
                  <Play className="w-4 h-4 ml-2" />بدء التجربة
                </DropdownMenuItem>
              )}
              {experiment.status === "active" && (
                <>
                  <DropdownMenuItem onClick={() => { setSelectedExperiment(experiment); setIsDataEntryDialogOpen(true); }}>
                    <Clipboard className="w-4 h-4 ml-2" />إدخال بيانات
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handlePauseExperiment(experiment)}>
                    <Pause className="w-4 h-4 ml-2" />إيقاف مؤقت
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleCompleteExperiment(experiment)}>
                    <CheckCircle2 className="w-4 h-4 ml-2" />إنهاء التجربة
                  </DropdownMenuItem>
                </>
              )}
              {experiment.status === "paused" && (
                <DropdownMenuItem onClick={() => handleStartExperiment(experiment)}>
                  <Play className="w-4 h-4 ml-2" />استئناف
                </DropdownMenuItem>
              )}
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل التقرير...")}>
                <FileText className="w-4 h-4 ml-2" />تقرير التجربة
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("جاري عرض التحليل...")}>
                <BarChart3 className="w-4 h-4 ml-2" />تحليل إحصائي
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedExperiment(experiment); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
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
            <FlaskConical className="w-7 h-7 text-purple-500" />
            التجارب الزراعية
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة وتتبع التجارب البحثية</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsExperimentDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />تجربة جديدة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <FlaskConical className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalExperiments}</p>
              <p className="text-xs text-muted-foreground">إجمالي التجارب</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Play className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeExperiments}</p>
              <p className="text-xs text-muted-foreground">جارية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.completedExperiments}</p>
              <p className="text-xs text-muted-foreground">مكتملة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Clipboard className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalDataEntries}</p>
              <p className="text-xs text-muted-foreground">سجل بيانات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.avgProgress}%</p>
              <p className="text-xs text-muted-foreground">متوسط التقدم</p>
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
              <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
            </div>
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-[180px]"><SelectValue placeholder="النوع" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الأنواع</SelectItem>
                <SelectItem value="variety_trial">تجارب أصناف</SelectItem>
                <SelectItem value="fertilizer_trial">تجارب أسمدة</SelectItem>
                <SelectItem value="pest_control">مكافحة آفات</SelectItem>
                <SelectItem value="irrigation">تجارب ري</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="planning">تخطيط</SelectItem>
                <SelectItem value="active">جاري</SelectItem>
                <SelectItem value="paused">متوقف</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
          </div>
        </CardContent>
      </Card>

      {/* Experiments Table */}
      <Card>
        <CardHeader>
          <CardTitle>التجارب ({filteredExperiments.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={experimentColumns} data={filteredExperiments} isLoading={isLoading} />
        </CardContent>
      </Card>

      {/* Experiment Dialog */}
      <FormDialog
        open={isExperimentDialogOpen}
        onOpenChange={setIsExperimentDialogOpen}
        title="تجربة جديدة"
        description="إنشاء تجربة زراعية جديدة"
        onSubmit={experimentForm.handleSubmit(handleCreateExperiment)}
        isSubmitting={isSubmitting}
        size="xl"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <Label>عنوان التجربة</Label>
              <Input {...experimentForm.register("title")} placeholder="تقييم أصناف الطماطم الجديدة" />
            </div>
            <div>
              <Label>نوع التجربة</Label>
              <Select value={experimentForm.watch("type")} onValueChange={(v) => experimentForm.setValue("type", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="variety_trial">تجارب أصناف</SelectItem>
                  <SelectItem value="fertilizer_trial">تجارب أسمدة</SelectItem>
                  <SelectItem value="pest_control">مكافحة آفات</SelectItem>
                  <SelectItem value="irrigation">تجارب ري</SelectItem>
                  <SelectItem value="other">أخرى</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>رمز التجربة</Label>
              <div className="flex gap-2">
                <Input {...experimentForm.register("code")} placeholder="VT-2026-001" />
                <Button type="button" variant="outline" onClick={generateCode}>توليد</Button>
              </div>
            </div>
          </div>
          <div>
            <Label>هدف التجربة</Label>
            <Textarea {...experimentForm.register("objective")} placeholder="وصف الهدف الرئيسي للتجربة..." rows={3} />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>المحصول</Label>
              <Input {...experimentForm.register("crop")} placeholder="طماطم" />
            </div>
            <div>
              <Label>الموقع</Label>
              <Input {...experimentForm.register("location")} placeholder="مزرعة الواحة" />
            </div>
            <div>
              <Label>الباحث المسؤول</Label>
              <Input {...experimentForm.register("researcher")} placeholder="د. أحمد محمد" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ البدء</Label>
              <Input type="date" {...experimentForm.register("start_date")} />
            </div>
            <div>
              <Label>تاريخ الانتهاء المتوقع</Label>
              <Input type="date" {...experimentForm.register("expected_end")} />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>عدد المعاملات</Label>
              <Input type="number" {...experimentForm.register("treatments", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>عدد المكررات</Label>
              <Input type="number" {...experimentForm.register("replications", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>التصميم التجريبي</Label>
              <Select value={experimentForm.watch("design")} onValueChange={(v) => experimentForm.setValue("design", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="CRD">CRD - تصميم عشوائي كامل</SelectItem>
                  <SelectItem value="RCBD">RCBD - قطاعات عشوائية كاملة</SelectItem>
                  <SelectItem value="LSD">LSD - مربع لاتيني</SelectItem>
                  <SelectItem value="Split">تصميم القطع المنشقة</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedExperiment(null); }}
        title={selectedExperiment?.title}
        subtitle={selectedExperiment?.code}
        badge={selectedExperiment && { text: statusConfig[selectedExperiment.status]?.label }}
        size="lg"
      >
        {selectedExperiment && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات التجربة">
              <ViewDialog.Row label="النوع" value={typeConfig[selectedExperiment.type]?.label} />
              <ViewDialog.Row label="المحصول" value={selectedExperiment.crop} />
              <ViewDialog.Row label="الموقع" value={selectedExperiment.location || "—"} />
              <ViewDialog.Row label="الباحث" value={selectedExperiment.researcher || "—"} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الهدف">
              <p className="text-sm">{selectedExperiment.objective}</p>
            </ViewDialog.Section>
            <ViewDialog.Section title="التصميم التجريبي">
              <ViewDialog.Row label="عدد المعاملات" value={selectedExperiment.treatments} />
              <ViewDialog.Row label="عدد المكررات" value={selectedExperiment.replications} />
              <ViewDialog.Row label="التصميم" value={selectedExperiment.design} />
            </ViewDialog.Section>
            <ViewDialog.Section title="التقدم">
              <ViewDialog.Row label="نسبة الإنجاز" value={`${selectedExperiment.progress}%`} />
              <ViewDialog.Row label="سجلات البيانات" value={`${selectedExperiment.data_entries} سجل`} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف التجربة"
        description={`هل أنت متأكد من حذف التجربة "${selectedExperiment?.title}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default ExperimentsPage
