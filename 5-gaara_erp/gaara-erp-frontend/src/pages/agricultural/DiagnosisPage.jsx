/**
 * Plant Diagnosis Page - تشخيص أمراض النباتات
 * Gaara ERP v12
 *
 * Plant disease diagnosis with AI-powered detection and treatment recommendations.
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
  Microscope,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Camera,
  Upload,
  AlertTriangle,
  CheckCircle2,
  Clock,
  RefreshCw,
  Download,
  Bug,
  Leaf,
  Pill,
  FileText,
  Image,
  Zap,
  History,
  ThermometerSun,
  Droplets,
  Activity,
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
const diagnosisSchema = z.object({
  crop: z.string().min(1, "المحصول مطلوب"),
  farm_id: z.string().min(1, "المزرعة مطلوبة"),
  field_id: z.string().optional(),
  symptoms: z.string().min(10, "وصف الأعراض مطلوب (10 أحرف على الأقل)"),
  affected_area: z.number().min(0).optional(),
  severity: z.enum(["low", "medium", "high", "critical"]),
  first_noticed: z.string().optional(),
  images: z.array(z.string()).optional(),
})

const treatmentSchema = z.object({
  diagnosis_id: z.string(),
  treatment_type: z.string().min(1, "نوع العلاج مطلوب"),
  product: z.string().optional(),
  dosage: z.string().optional(),
  application_method: z.string().optional(),
  frequency: z.string().optional(),
  notes: z.string().optional(),
})

// Status configurations
const severityConfig = {
  low: { label: "منخفض", color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  medium: { label: "متوسط", color: "bg-yellow-100 text-yellow-700", icon: AlertTriangle },
  high: { label: "مرتفع", color: "bg-orange-100 text-orange-700", icon: AlertTriangle },
  critical: { label: "حرج", color: "bg-red-100 text-red-700", icon: Bug },
}

const statusConfig = {
  pending: { label: "قيد التشخيص", color: "bg-blue-100 text-blue-700" },
  diagnosed: { label: "تم التشخيص", color: "bg-purple-100 text-purple-700" },
  treating: { label: "قيد العلاج", color: "bg-yellow-100 text-yellow-700" },
  resolved: { label: "تم الحل", color: "bg-green-100 text-green-700" },
  monitoring: { label: "مراقبة", color: "bg-gray-100 text-gray-700" },
}

// Mock data
const mockDiagnoses = [
  {
    id: "DGN001",
    crop: "طماطم",
    farm: "مزرعة الواحة",
    farm_id: "FRM001",
    field: "صوب 1",
    symptoms: "بقع صفراء على الأوراق مع ذبول تدريجي",
    disease: "اللفحة المتأخرة",
    disease_en: "Late Blight",
    pathogen: "Phytophthora infestans",
    severity: "high",
    affected_area: 15,
    status: "treating",
    diagnosis_date: "2026-01-15",
    confidence: 92,
    treatment: "مبيد فطري نحاسي",
    images: [],
  },
  {
    id: "DGN002",
    crop: "قمح",
    farm: "مزرعة الفردوس",
    farm_id: "FRM002",
    field: "حقل A-2",
    symptoms: "بقع بنية على السيقان وتلون الأوراق",
    disease: "الصدأ البرتقالي",
    disease_en: "Orange Rust",
    pathogen: "Puccinia striiformis",
    severity: "medium",
    affected_area: 8,
    status: "monitoring",
    diagnosis_date: "2026-01-12",
    confidence: 88,
    treatment: "مبيد فطري جهازي",
    images: [],
  },
  {
    id: "DGN003",
    crop: "خيار",
    farm: "مزرعة النخيل",
    farm_id: "FRM003",
    field: "صوب 3",
    symptoms: "تجعد الأوراق وتوقف النمو",
    disease: "البياض الدقيقي",
    disease_en: "Powdery Mildew",
    pathogen: "Erysiphe cichoracearum",
    severity: "low",
    affected_area: 5,
    status: "resolved",
    diagnosis_date: "2026-01-10",
    confidence: 95,
    treatment: "كبريت ميكروني",
    images: [],
  },
]

const mockDiseases = [
  { id: 1, name: "اللفحة المتأخرة", name_en: "Late Blight", category: "فطري", crops: ["طماطم", "بطاطس"] },
  { id: 2, name: "البياض الدقيقي", name_en: "Powdery Mildew", category: "فطري", crops: ["خيار", "كوسة", "عنب"] },
  { id: 3, name: "الصدأ البرتقالي", name_en: "Orange Rust", category: "فطري", crops: ["قمح", "شعير"] },
  { id: 4, name: "الذبول الفيوزاريومي", name_en: "Fusarium Wilt", category: "فطري", crops: ["طماطم", "فلفل"] },
  { id: 5, name: "فيروس موزاييك", name_en: "Mosaic Virus", category: "فيروسي", crops: ["خيار", "كوسة"] },
]

const mockFarms = [
  { id: "FRM001", name: "مزرعة الواحة" },
  { id: "FRM002", name: "مزرعة الفردوس" },
  { id: "FRM003", name: "مزرعة النخيل" },
]

const DiagnosisPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("diagnoses")
  const [diagnoses, setDiagnoses] = useState(mockDiagnoses)
  const [diseases, setDiseases] = useState(mockDiseases)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [severityFilter, setSeverityFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isDiagnosisDialogOpen, setIsDiagnosisDialogOpen] = useState(false)
  const [isTreatmentDialogOpen, setIsTreatmentDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const diagnosisForm = useForm({
    resolver: zodResolver(diagnosisSchema),
    defaultValues: {
      crop: "",
      farm_id: "",
      field_id: "",
      symptoms: "",
      affected_area: 0,
      severity: "medium",
      first_noticed: new Date().toISOString().split('T')[0],
      images: [],
    },
  })

  const treatmentForm = useForm({
    resolver: zodResolver(treatmentSchema),
    defaultValues: {
      diagnosis_id: "",
      treatment_type: "",
      product: "",
      dosage: "",
      application_method: "",
      frequency: "",
      notes: "",
    },
  })

  // Filter diagnoses
  const filteredDiagnoses = diagnoses.filter(d => {
    const matchesSearch = d.crop.includes(searchQuery) || 
                         d.farm.includes(searchQuery) ||
                         d.disease?.includes(searchQuery) ||
                         d.symptoms.includes(searchQuery)
    const matchesSeverity = severityFilter === "all" || d.severity === severityFilter
    const matchesStatus = statusFilter === "all" || d.status === statusFilter
    return matchesSearch && matchesSeverity && matchesStatus
  })

  // Statistics
  const stats = {
    totalDiagnoses: diagnoses.length,
    activeCases: diagnoses.filter(d => !["resolved"].includes(d.status)).length,
    criticalCases: diagnoses.filter(d => d.severity === "critical" || d.severity === "high").length,
    resolvedCases: diagnoses.filter(d => d.status === "resolved").length,
    avgConfidence: Math.round(diagnoses.reduce((sum, d) => sum + d.confidence, 0) / diagnoses.length),
    totalAffectedArea: diagnoses.reduce((sum, d) => sum + (d.affected_area || 0), 0),
  }

  // Handlers
  const handleCreateDiagnosis = async (data) => {
    setIsSubmitting(true)
    try {
      const farm = mockFarms.find(f => f.id === data.farm_id)
      const newDiagnosis = {
        id: `DGN${String(diagnoses.length + 1).padStart(3, '0')}`,
        ...data,
        farm: farm?.name || "",
        field: data.field_id || "",
        disease: null,
        disease_en: null,
        pathogen: null,
        status: "pending",
        diagnosis_date: new Date().toISOString().split('T')[0],
        confidence: 0,
        treatment: null,
      }
      setDiagnoses([...diagnoses, newDiagnosis])
      toast.success("تم إرسال حالة للتشخيص")
      setIsDiagnosisDialogOpen(false)
      diagnosisForm.reset()
    } catch (error) {
      toast.error("فشل إرسال الحالة")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleAIDiagnosis = async (diagnosis) => {
    toast.info("جاري تحليل الصور بالذكاء الاصطناعي...")
    // Simulate AI diagnosis
    setTimeout(() => {
      const randomDisease = mockDiseases[Math.floor(Math.random() * mockDiseases.length)]
      setDiagnoses(diagnoses.map(d => {
        if (d.id === diagnosis.id) {
          return {
            ...d,
            disease: randomDisease.name,
            disease_en: randomDisease.name_en,
            status: "diagnosed",
            confidence: Math.floor(Math.random() * 15) + 85,
          }
        }
        return d
      }))
      toast.success("تم التشخيص بنجاح")
    }, 2000)
  }

  const handleAddTreatment = async (data) => {
    setIsSubmitting(true)
    try {
      setDiagnoses(diagnoses.map(d => {
        if (d.id === data.diagnosis_id) {
          return {
            ...d,
            treatment: data.product,
            status: "treating",
          }
        }
        return d
      }))
      toast.success("تم إضافة العلاج")
      setIsTreatmentDialogOpen(false)
      treatmentForm.reset()
    } catch (error) {
      toast.error("فشل إضافة العلاج")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleMarkResolved = (diagnosis) => {
    setDiagnoses(diagnoses.map(d => 
      d.id === diagnosis.id ? { ...d, status: "resolved" } : d
    ))
    toast.success("تم تحديد الحالة كمحلولة")
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setDiagnoses(diagnoses.filter(d => d.id !== selectedDiagnosis.id))
      toast.success("تم حذف التشخيص")
      setIsDeleteDialogOpen(false)
      setSelectedDiagnosis(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openTreatmentDialog = (diagnosis) => {
    setSelectedDiagnosis(diagnosis)
    treatmentForm.reset({ diagnosis_id: diagnosis.id })
    setIsTreatmentDialogOpen(true)
  }

  // Diagnosis columns
  const diagnosisColumns = [
    {
      accessorKey: "id",
      header: "رقم الحالة",
      cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span>,
    },
    {
      accessorKey: "crop",
      header: "المحصول",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
            <Leaf className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.crop}</p>
            <p className="text-sm text-muted-foreground">{row.original.farm}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "disease",
      header: "المرض",
      cell: ({ row }) => (
        <div>
          <p className="font-medium">{row.original.disease || "قيد التشخيص"}</p>
          {row.original.disease_en && (
            <p className="text-sm text-muted-foreground">{row.original.disease_en}</p>
          )}
        </div>
      ),
    },
    {
      accessorKey: "severity",
      header: "الخطورة",
      cell: ({ row }) => {
        const config = severityConfig[row.original.severity]
        const Icon = config.icon
        return (
          <Badge className={config.color}>
            <Icon className="w-3 h-3 ml-1" />
            {config.label}
          </Badge>
        )
      },
    },
    {
      accessorKey: "confidence",
      header: "دقة التشخيص",
      cell: ({ row }) => (
        row.original.confidence > 0 ? (
          <div className="w-20">
            <div className="flex justify-between text-sm mb-1">
              <span className={row.original.confidence >= 85 ? "text-green-600" : "text-yellow-600"}>
                {row.original.confidence}%
              </span>
            </div>
            <Progress value={row.original.confidence} className="h-2" />
          </div>
        ) : <span className="text-muted-foreground">—</span>
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
      accessorKey: "diagnosis_date",
      header: "التاريخ",
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const diagnosis = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedDiagnosis(diagnosis); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              {diagnosis.status === "pending" && (
                <DropdownMenuItem onClick={() => handleAIDiagnosis(diagnosis)}>
                  <Zap className="w-4 h-4 ml-2" />تشخيص AI
                </DropdownMenuItem>
              )}
              {diagnosis.status === "diagnosed" && (
                <DropdownMenuItem onClick={() => openTreatmentDialog(diagnosis)}>
                  <Pill className="w-4 h-4 ml-2" />إضافة علاج
                </DropdownMenuItem>
              )}
              {diagnosis.status === "treating" && (
                <DropdownMenuItem onClick={() => handleMarkResolved(diagnosis)}>
                  <CheckCircle2 className="w-4 h-4 ml-2" />تحديد كمحلول
                </DropdownMenuItem>
              )}
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل التقرير...")}>
                <FileText className="w-4 h-4 ml-2" />تقرير التشخيص
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedDiagnosis(diagnosis); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Disease database columns
  const diseaseColumns = [
    { accessorKey: "name", header: "المرض" },
    { accessorKey: "name_en", header: "الاسم الإنجليزي" },
    { accessorKey: "category", header: "التصنيف", cell: ({ row }) => <Badge variant="outline">{row.original.category}</Badge> },
    { accessorKey: "crops", header: "المحاصيل المتأثرة", cell: ({ row }) => row.original.crops.join("، ") },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Microscope className="w-7 h-7 text-purple-500" />
            تشخيص أمراض النباتات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تشخيص الأمراض بالذكاء الاصطناعي وتوصيات العلاج</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsDiagnosisDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />حالة جديدة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Microscope className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalDiagnoses}</p>
              <p className="text-xs text-muted-foreground">إجمالي الحالات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Activity className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeCases}</p>
              <p className="text-xs text-muted-foreground">حالات نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <Bug className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.criticalCases}</p>
              <p className="text-xs text-muted-foreground">حالات حرجة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.resolvedCases}</p>
              <p className="text-xs text-muted-foreground">تم حلها</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Zap className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.avgConfidence}%</p>
              <p className="text-xs text-muted-foreground">متوسط الدقة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalAffectedArea}</p>
              <p className="text-xs text-muted-foreground">هكتار متأثر</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="diagnoses" className="flex items-center gap-2">
            <Microscope className="w-4 h-4" />حالات التشخيص
          </TabsTrigger>
          <TabsTrigger value="diseases" className="flex items-center gap-2">
            <Bug className="w-4 h-4" />قاعدة بيانات الأمراض
          </TabsTrigger>
        </TabsList>

        {/* Diagnoses Tab */}
        <TabsContent value="diagnoses" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={severityFilter} onValueChange={setSeverityFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="الخطورة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع المستويات</SelectItem>
                    <SelectItem value="low">منخفض</SelectItem>
                    <SelectItem value="medium">متوسط</SelectItem>
                    <SelectItem value="high">مرتفع</SelectItem>
                    <SelectItem value="critical">حرج</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="pending">قيد التشخيص</SelectItem>
                    <SelectItem value="diagnosed">تم التشخيص</SelectItem>
                    <SelectItem value="treating">قيد العلاج</SelectItem>
                    <SelectItem value="resolved">تم الحل</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>حالات التشخيص ({filteredDiagnoses.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={diagnosisColumns} data={filteredDiagnoses} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Diseases Database Tab */}
        <TabsContent value="diseases" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>قاعدة بيانات الأمراض</CardTitle>
                <CardDescription>قائمة الأمراض الزراعية المعروفة</CardDescription>
              </div>
              <Button onClick={() => toast.info("جاري إضافة مرض جديد...")}>
                <Plus className="w-4 h-4 ml-2" />إضافة مرض
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={diseaseColumns} data={diseases} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Diagnosis Dialog */}
      <FormDialog
        open={isDiagnosisDialogOpen}
        onOpenChange={setIsDiagnosisDialogOpen}
        title="حالة تشخيص جديدة"
        description="إرسال حالة للتشخيص"
        onSubmit={diagnosisForm.handleSubmit(handleCreateDiagnosis)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المحصول</Label>
              <Input {...diagnosisForm.register("crop")} placeholder="طماطم" />
            </div>
            <div>
              <Label>المزرعة</Label>
              <Select value={diagnosisForm.watch("farm_id")} onValueChange={(v) => diagnosisForm.setValue("farm_id", v)}>
                <SelectTrigger><SelectValue placeholder="اختر المزرعة" /></SelectTrigger>
                <SelectContent>
                  {mockFarms.map((f) => <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>درجة الخطورة</Label>
              <Select value={diagnosisForm.watch("severity")} onValueChange={(v) => diagnosisForm.setValue("severity", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">منخفض</SelectItem>
                  <SelectItem value="medium">متوسط</SelectItem>
                  <SelectItem value="high">مرتفع</SelectItem>
                  <SelectItem value="critical">حرج</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>المساحة المتأثرة (هكتار)</Label>
              <Input type="number" {...diagnosisForm.register("affected_area", { valueAsNumber: true })} />
            </div>
          </div>
          <div>
            <Label>وصف الأعراض</Label>
            <Textarea {...diagnosisForm.register("symptoms")} placeholder="صف الأعراض التي تلاحظها على النباتات..." rows={4} />
          </div>
          <div>
            <Label>تاريخ ملاحظة الأعراض</Label>
            <Input type="date" {...diagnosisForm.register("first_noticed")} />
          </div>
          <div>
            <Label>صور (اختياري)</Label>
            <div className="border-2 border-dashed rounded-lg p-8 text-center">
              <Camera className="w-10 h-10 mx-auto text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground">اسحب الصور هنا أو اضغط للرفع</p>
              <Button variant="outline" className="mt-2" onClick={() => toast.info("سيتم إضافة رفع الصور قريباً")}>
                <Upload className="w-4 h-4 ml-2" />رفع صور
              </Button>
            </div>
          </div>
        </div>
      </FormDialog>

      {/* Treatment Dialog */}
      <FormDialog
        open={isTreatmentDialogOpen}
        onOpenChange={setIsTreatmentDialogOpen}
        title="إضافة علاج"
        description={`إضافة علاج لـ ${selectedDiagnosis?.disease}`}
        onSubmit={treatmentForm.handleSubmit(handleAddTreatment)}
        isSubmitting={isSubmitting}
      >
        <div className="space-y-4">
          <div>
            <Label>نوع العلاج</Label>
            <Select value={treatmentForm.watch("treatment_type")} onValueChange={(v) => treatmentForm.setValue("treatment_type", v)}>
              <SelectTrigger><SelectValue placeholder="اختر نوع العلاج" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="fungicide">مبيد فطري</SelectItem>
                <SelectItem value="insecticide">مبيد حشري</SelectItem>
                <SelectItem value="herbicide">مبيد أعشاب</SelectItem>
                <SelectItem value="biological">علاج بيولوجي</SelectItem>
                <SelectItem value="cultural">ممارسات زراعية</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>المنتج</Label>
            <Input {...treatmentForm.register("product")} placeholder="اسم المنتج" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>الجرعة</Label>
              <Input {...treatmentForm.register("dosage")} placeholder="مثال: 2 مل/لتر" />
            </div>
            <div>
              <Label>طريقة التطبيق</Label>
              <Input {...treatmentForm.register("application_method")} placeholder="رش ورقي" />
            </div>
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...treatmentForm.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedDiagnosis(null); }}
        title={`حالة: ${selectedDiagnosis?.id}`}
        subtitle={`${selectedDiagnosis?.crop} - ${selectedDiagnosis?.farm}`}
        badge={selectedDiagnosis && { text: statusConfig[selectedDiagnosis.status]?.label }}
        size="lg"
      >
        {selectedDiagnosis && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات الحالة">
              <ViewDialog.Row label="المحصول" value={selectedDiagnosis.crop} />
              <ViewDialog.Row label="المزرعة" value={selectedDiagnosis.farm} />
              <ViewDialog.Row label="الحقل" value={selectedDiagnosis.field || "—"} />
              <ViewDialog.Row label="المساحة المتأثرة" value={`${selectedDiagnosis.affected_area} هكتار`} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الأعراض">
              <p className="text-sm">{selectedDiagnosis.symptoms}</p>
            </ViewDialog.Section>
            {selectedDiagnosis.disease && (
              <ViewDialog.Section title="التشخيص">
                <ViewDialog.Row label="المرض" value={selectedDiagnosis.disease} />
                <ViewDialog.Row label="الاسم العلمي" value={selectedDiagnosis.disease_en || "—"} />
                <ViewDialog.Row label="المسبب" value={selectedDiagnosis.pathogen || "—"} />
                <ViewDialog.Row label="دقة التشخيص" value={`${selectedDiagnosis.confidence}%`} valueClassName="text-green-600" />
              </ViewDialog.Section>
            )}
            {selectedDiagnosis.treatment && (
              <ViewDialog.Section title="العلاج">
                <ViewDialog.Row label="العلاج المقترح" value={selectedDiagnosis.treatment} />
              </ViewDialog.Section>
            )}
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف التشخيص"
        description={`هل أنت متأكد من حذف الحالة "${selectedDiagnosis?.id}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default DiagnosisPage
