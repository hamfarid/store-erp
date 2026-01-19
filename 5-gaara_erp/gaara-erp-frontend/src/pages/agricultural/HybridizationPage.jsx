/**
 * Hybridization Page - التهجين
 * Gaara ERP v12
 *
 * Crop hybridization management for breeding programs.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Dna,
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
  Target,
  Leaf,
  Beaker,
  GitBranch,
  Activity,
  AlertTriangle,
  ArrowRight,
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
const crossSchema = z.object({
  code: z.string().optional(),
  parent_female: z.string().min(1, "الأم الأنثى مطلوبة"),
  parent_male: z.string().min(1, "الأب الذكر مطلوب"),
  crop: z.string().min(1, "المحصول مطلوب"),
  objective: z.string().min(10, "الهدف مطلوب"),
  cross_date: z.string().min(1, "تاريخ التهجين مطلوب"),
  location: z.string().optional(),
  breeder: z.string().optional(),
})

// Status configurations
const statusConfig = {
  planned: { label: "مخطط", color: "bg-gray-100 text-gray-700", icon: Clock },
  crossed: { label: "تم التهجين", color: "bg-blue-100 text-blue-700", icon: GitBranch },
  germinating: { label: "إنبات", color: "bg-green-100 text-green-700", icon: Leaf },
  evaluating: { label: "تقييم", color: "bg-purple-100 text-purple-700", icon: Beaker },
  selected: { label: "مختار", color: "bg-emerald-100 text-emerald-700", icon: CheckCircle2 },
  rejected: { label: "مرفوض", color: "bg-red-100 text-red-700", icon: AlertTriangle },
}

// Mock data
const mockCrosses = [
  {
    id: "HYB001",
    code: "TOM-HY-2026-001",
    parent_female: "طماطم سوبر سترين",
    parent_male: "طماطم هجين 82",
    crop: "طماطم",
    objective: "تحسين مقاومة الأمراض وزيادة الإنتاجية",
    cross_date: "2026-01-05",
    location: "مزرعة الواحة",
    breeder: "د. أحمد محمد",
    status: "evaluating",
    f1_seeds: 150,
    germination_rate: 85,
    selected_plants: 12,
    traits: ["مقاومة للذبول", "ثمار كبيرة", "إنتاجية عالية"],
  },
  {
    id: "HYB002",
    code: "WHT-HY-2026-001",
    parent_female: "قمح جيزة 171",
    parent_male: "قمح سخا 95",
    crop: "قمح",
    objective: "تحسين تحمل الجفاف والملوحة",
    cross_date: "2025-11-15",
    location: "مزرعة الفردوس",
    breeder: "د. سارة علي",
    status: "germinating",
    f1_seeds: 500,
    germination_rate: 92,
    selected_plants: 0,
    traits: ["تحمل الجفاف", "مقاومة الملوحة"],
  },
  {
    id: "HYB003",
    code: "CUC-HY-2026-001",
    parent_female: "خيار بيتا ألفا",
    parent_male: "خيار هولندي",
    crop: "خيار",
    objective: "إنتاج صنف مناسب للزراعة المحمية",
    cross_date: "2026-01-10",
    location: "مزرعة النخيل",
    breeder: "م. خالد سعيد",
    status: "crossed",
    f1_seeds: 80,
    germination_rate: 0,
    selected_plants: 0,
    traits: ["نمو قوي", "ثمار متجانسة"],
  },
]

const mockParents = [
  { id: 1, name: "طماطم سوبر سترين", crop: "طماطم", type: "variety", origin: "محلي" },
  { id: 2, name: "طماطم هجين 82", crop: "طماطم", type: "hybrid", origin: "مستورد" },
  { id: 3, name: "قمح جيزة 171", crop: "قمح", type: "variety", origin: "محلي" },
  { id: 4, name: "قمح سخا 95", crop: "قمح", type: "variety", origin: "محلي" },
  { id: 5, name: "خيار بيتا ألفا", crop: "خيار", type: "variety", origin: "محلي" },
  { id: 6, name: "خيار هولندي", crop: "خيار", type: "hybrid", origin: "مستورد" },
]

const HybridizationPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("crosses")
  const [crosses, setCrosses] = useState(mockCrosses)
  const [parents, setParents] = useState(mockParents)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isCrossDialogOpen, setIsCrossDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedCross, setSelectedCross] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const crossForm = useForm({
    resolver: zodResolver(crossSchema),
    defaultValues: {
      code: "",
      parent_female: "",
      parent_male: "",
      crop: "",
      objective: "",
      cross_date: new Date().toISOString().split('T')[0],
      location: "",
      breeder: "",
    },
  })

  // Filter crosses
  const filteredCrosses = crosses.filter(c => {
    const matchesSearch = c.code?.includes(searchQuery) || 
                         c.crop.includes(searchQuery) ||
                         c.parent_female.includes(searchQuery) ||
                         c.parent_male.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || c.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Statistics
  const stats = {
    totalCrosses: crosses.length,
    activeCrosses: crosses.filter(c => !["rejected", "selected"].includes(c.status)).length,
    successfulCrosses: crosses.filter(c => c.status === "selected").length,
    totalF1Seeds: crosses.reduce((sum, c) => sum + (c.f1_seeds || 0), 0),
    avgGermination: Math.round(
      crosses.filter(c => c.germination_rate > 0).reduce((sum, c) => sum + c.germination_rate, 0) / 
      crosses.filter(c => c.germination_rate > 0).length || 0
    ),
  }

  // Handlers
  const handleCreateCross = async (data) => {
    setIsSubmitting(true)
    try {
      const cropPrefix = { "طماطم": "TOM", "قمح": "WHT", "خيار": "CUC" }[data.crop] || "CRP"
      const newCross = {
        id: `HYB${String(crosses.length + 1).padStart(3, '0')}`,
        code: data.code || `${cropPrefix}-HY-${new Date().getFullYear()}-${String(crosses.length + 1).padStart(3, '0')}`,
        ...data,
        status: "planned",
        f1_seeds: 0,
        germination_rate: 0,
        selected_plants: 0,
        traits: [],
      }
      setCrosses([...crosses, newCross])
      toast.success("تم إنشاء التهجين بنجاح")
      setIsCrossDialogOpen(false)
      crossForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء التهجين")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleUpdateStatus = (cross, newStatus) => {
    setCrosses(crosses.map(c => 
      c.id === cross.id ? { ...c, status: newStatus } : c
    ))
    toast.success(`تم تحديث الحالة إلى ${statusConfig[newStatus].label}`)
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setCrosses(crosses.filter(c => c.id !== selectedCross.id))
      toast.success("تم حذف التهجين")
      setIsDeleteDialogOpen(false)
      setSelectedCross(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  // Cross columns
  const crossColumns = [
    {
      accessorKey: "code",
      header: "الرمز",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-green-100 to-emerald-100 flex items-center justify-center">
            <Dna className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <p className="font-mono text-primary font-medium">{row.original.code}</p>
            <p className="text-sm text-muted-foreground">{row.original.crop}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "parents",
      header: "الآباء",
      cell: ({ row }) => (
        <div className="flex items-center gap-2 text-sm">
          <span className="text-pink-600">♀ {row.original.parent_female}</span>
          <ArrowRight className="w-4 h-4 text-muted-foreground" />
          <span className="text-blue-600">♂ {row.original.parent_male}</span>
        </div>
      ),
    },
    {
      accessorKey: "f1_seeds",
      header: "بذور F1",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.f1_seeds} بذرة</Badge>
      ),
    },
    {
      accessorKey: "germination_rate",
      header: "نسبة الإنبات",
      cell: ({ row }) => (
        row.original.germination_rate > 0 ? (
          <div className="w-20">
            <span className="text-sm">{row.original.germination_rate}%</span>
            <Progress value={row.original.germination_rate} className="h-2 mt-1" />
          </div>
        ) : <span className="text-muted-foreground">—</span>
      ),
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
      accessorKey: "cross_date",
      header: "تاريخ التهجين",
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const cross = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedCross(cross); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              {cross.status === "planned" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(cross, "crossed")}>
                  <GitBranch className="w-4 h-4 ml-2" />تأكيد التهجين
                </DropdownMenuItem>
              )}
              {cross.status === "crossed" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(cross, "germinating")}>
                  <Leaf className="w-4 h-4 ml-2" />بدء الإنبات
                </DropdownMenuItem>
              )}
              {cross.status === "germinating" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(cross, "evaluating")}>
                  <Beaker className="w-4 h-4 ml-2" />بدء التقييم
                </DropdownMenuItem>
              )}
              {cross.status === "evaluating" && (
                <>
                  <DropdownMenuItem onClick={() => handleUpdateStatus(cross, "selected")}>
                    <CheckCircle2 className="w-4 h-4 ml-2" />اختيار للمتابعة
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleUpdateStatus(cross, "rejected")}>
                    <AlertTriangle className="w-4 h-4 ml-2" />رفض
                  </DropdownMenuItem>
                </>
              )}
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل التقرير...")}>
                <FileText className="w-4 h-4 ml-2" />تقرير التهجين
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedCross(cross); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Parents columns
  const parentsColumns = [
    { accessorKey: "name", header: "الاسم" },
    { accessorKey: "crop", header: "المحصول" },
    { accessorKey: "type", header: "النوع", cell: ({ row }) => (
      <Badge variant="outline">{row.original.type === "variety" ? "صنف" : "هجين"}</Badge>
    )},
    { accessorKey: "origin", header: "المصدر" },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Dna className="w-7 h-7 text-emerald-500" />
            برامج التهجين
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة عمليات التهجين وتطوير الأصناف</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsCrossDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />تهجين جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <Dna className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalCrosses}</p>
              <p className="text-xs text-muted-foreground">إجمالي التهجينات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Activity className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeCrosses}</p>
              <p className="text-xs text-muted-foreground">تهجينات نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.successfulCrosses}</p>
              <p className="text-xs text-muted-foreground">ناجحة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalF1Seeds}</p>
              <p className="text-xs text-muted-foreground">بذور F1</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Target className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.avgGermination}%</p>
              <p className="text-xs text-muted-foreground">متوسط الإنبات</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="crosses" className="flex items-center gap-2">
            <GitBranch className="w-4 h-4" />التهجينات
          </TabsTrigger>
          <TabsTrigger value="parents" className="flex items-center gap-2">
            <Leaf className="w-4 h-4" />مخزون الآباء
          </TabsTrigger>
        </TabsList>

        {/* Crosses Tab */}
        <TabsContent value="crosses" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="planned">مخطط</SelectItem>
                    <SelectItem value="crossed">تم التهجين</SelectItem>
                    <SelectItem value="germinating">إنبات</SelectItem>
                    <SelectItem value="evaluating">تقييم</SelectItem>
                    <SelectItem value="selected">مختار</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>التهجينات ({filteredCrosses.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={crossColumns} data={filteredCrosses} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Parents Tab */}
        <TabsContent value="parents" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>مخزون الآباء</CardTitle>
                <CardDescription>الأصناف والهجن المستخدمة في برامج التهجين</CardDescription>
              </div>
              <Button onClick={() => toast.info("جاري إضافة أب جديد...")}>
                <Plus className="w-4 h-4 ml-2" />إضافة أب
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={parentsColumns} data={parents} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Cross Dialog */}
      <FormDialog
        open={isCrossDialogOpen}
        onOpenChange={setIsCrossDialogOpen}
        title="تهجين جديد"
        description="إنشاء عملية تهجين جديدة"
        onSubmit={crossForm.handleSubmit(handleCreateCross)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المحصول</Label>
              <Select value={crossForm.watch("crop")} onValueChange={(v) => crossForm.setValue("crop", v)}>
                <SelectTrigger><SelectValue placeholder="اختر المحصول" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="طماطم">طماطم</SelectItem>
                  <SelectItem value="قمح">قمح</SelectItem>
                  <SelectItem value="خيار">خيار</SelectItem>
                  <SelectItem value="فلفل">فلفل</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>رمز التهجين (اختياري)</Label>
              <Input {...crossForm.register("code")} placeholder="TOM-HY-2026-001" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>الأم (♀)</Label>
              <Select value={crossForm.watch("parent_female")} onValueChange={(v) => crossForm.setValue("parent_female", v)}>
                <SelectTrigger><SelectValue placeholder="اختر الأم" /></SelectTrigger>
                <SelectContent>
                  {parents.map(p => <SelectItem key={p.id} value={p.name}>{p.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الأب (♂)</Label>
              <Select value={crossForm.watch("parent_male")} onValueChange={(v) => crossForm.setValue("parent_male", v)}>
                <SelectTrigger><SelectValue placeholder="اختر الأب" /></SelectTrigger>
                <SelectContent>
                  {parents.map(p => <SelectItem key={p.id} value={p.name}>{p.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>هدف التهجين</Label>
            <Textarea {...crossForm.register("objective")} placeholder="وصف الهدف من التهجين والصفات المستهدفة..." rows={3} />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>تاريخ التهجين</Label>
              <Input type="date" {...crossForm.register("cross_date")} />
            </div>
            <div>
              <Label>الموقع</Label>
              <Input {...crossForm.register("location")} placeholder="مزرعة الواحة" />
            </div>
            <div>
              <Label>المربي</Label>
              <Input {...crossForm.register("breeder")} placeholder="د. أحمد محمد" />
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedCross(null); }}
        title={selectedCross?.code}
        subtitle={`${selectedCross?.crop} - ${selectedCross?.cross_date}`}
        badge={selectedCross && { text: statusConfig[selectedCross.status]?.label }}
        size="lg"
      >
        {selectedCross && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات التهجين">
              <ViewDialog.Row label="الأم (♀)" value={selectedCross.parent_female} />
              <ViewDialog.Row label="الأب (♂)" value={selectedCross.parent_male} />
              <ViewDialog.Row label="الموقع" value={selectedCross.location || "—"} />
              <ViewDialog.Row label="المربي" value={selectedCross.breeder || "—"} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الهدف">
              <p className="text-sm">{selectedCross.objective}</p>
            </ViewDialog.Section>
            <ViewDialog.Section title="النتائج">
              <ViewDialog.Row label="بذور F1" value={`${selectedCross.f1_seeds} بذرة`} />
              <ViewDialog.Row label="نسبة الإنبات" value={`${selectedCross.germination_rate}%`} />
              <ViewDialog.Row label="نباتات مختارة" value={selectedCross.selected_plants} />
            </ViewDialog.Section>
            {selectedCross.traits.length > 0 && (
              <ViewDialog.Section title="الصفات المرصودة">
                <div className="flex flex-wrap gap-2">
                  {selectedCross.traits.map((trait, idx) => (
                    <Badge key={idx} variant="secondary">{trait}</Badge>
                  ))}
                </div>
              </ViewDialog.Section>
            )}
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف التهجين"
        description={`هل أنت متأكد من حذف التهجين "${selectedCross?.code}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default HybridizationPage
