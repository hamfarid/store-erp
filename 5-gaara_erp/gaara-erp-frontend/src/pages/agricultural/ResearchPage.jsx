/**
 * Research Page - البحث العلمي
 * Gaara ERP v12
 *
 * Agricultural research projects management.
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
  GraduationCap,
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
  Users,
  BookOpen,
  Award,
  Target,
  Lightbulb,
  Microscope,
  BarChart3,
  LinkIcon,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
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
const projectSchema = z.object({
  title: z.string().min(5, "العنوان مطلوب"),
  code: z.string().optional(),
  type: z.enum(["basic", "applied", "development"]),
  field: z.string().min(1, "مجال البحث مطلوب"),
  objectives: z.string().min(20, "الأهداف مطلوبة"),
  start_date: z.string().min(1, "تاريخ البدء مطلوب"),
  end_date: z.string().optional(),
  budget: z.number().min(0).optional(),
  lead_researcher: z.string().optional(),
  funding_source: z.string().optional(),
})

// Status configurations
const statusConfig = {
  proposal: { label: "مقترح", color: "bg-gray-100 text-gray-700", icon: Lightbulb },
  approved: { label: "معتمد", color: "bg-blue-100 text-blue-700", icon: CheckCircle2 },
  active: { label: "جاري", color: "bg-green-100 text-green-700", icon: Microscope },
  completed: { label: "مكتمل", color: "bg-purple-100 text-purple-700", icon: Award },
  suspended: { label: "موقف", color: "bg-yellow-100 text-yellow-700", icon: Clock },
}

const typeConfig = {
  basic: { label: "بحث أساسي", color: "bg-indigo-100 text-indigo-700" },
  applied: { label: "بحث تطبيقي", color: "bg-emerald-100 text-emerald-700" },
  development: { label: "تطوير", color: "bg-amber-100 text-amber-700" },
}

// Mock data
const mockProjects = [
  {
    id: "RSH001",
    title: "تطوير أصناف طماطم مقاومة للجفاف",
    code: "AGR-2026-001",
    type: "applied",
    field: "تربية النبات",
    objectives: "تطوير أصناف طماطم جديدة تتحمل ظروف الجفاف مع الحفاظ على الإنتاجية العالية",
    start_date: "2025-09-01",
    end_date: "2027-08-31",
    status: "active",
    progress: 35,
    budget: 500000,
    spent: 175000,
    lead_researcher: "د. أحمد محمد",
    team: ["د. سارة علي", "م. خالد سعيد", "م. مريم أحمد"],
    funding_source: "وزارة الزراعة",
    publications: 2,
    patents: 0,
  },
  {
    id: "RSH002",
    title: "دراسة تأثير المخصبات الحيوية على إنتاجية القمح",
    code: "AGR-2026-002",
    type: "basic",
    field: "خصوبة التربة",
    objectives: "دراسة تأثير استخدام المخصبات الحيوية على نمو وإنتاجية القمح في الأراضي المستصلحة",
    start_date: "2025-11-01",
    end_date: "2026-10-31",
    status: "active",
    progress: 60,
    budget: 200000,
    spent: 120000,
    lead_researcher: "د. سارة علي",
    team: ["م. فاطمة حسن", "م. عمر يوسف"],
    funding_source: "جامعة القاهرة",
    publications: 1,
    patents: 0,
  },
  {
    id: "RSH003",
    title: "تقنيات الزراعة الذكية في البيوت المحمية",
    code: "AGR-2025-010",
    type: "development",
    field: "تقنيات زراعية",
    objectives: "تطوير نظام متكامل للزراعة الذكية يعتمد على إنترنت الأشياء والذكاء الاصطناعي",
    start_date: "2025-01-01",
    end_date: "2025-12-31",
    status: "completed",
    progress: 100,
    budget: 750000,
    spent: 720000,
    lead_researcher: "د. محمد أحمد",
    team: ["م. علي حسين", "م. نورا محمد", "م. أحمد سمير"],
    funding_source: "شركة الواحة للتنمية",
    publications: 5,
    patents: 1,
  },
]

const mockPublications = [
  { id: 1, title: "تأثير الإجهاد المائي على أصناف الطماطم", project_id: "RSH001", type: "journal", year: 2026, authors: "أحمد محمد وآخرون", journal: "مجلة البحوث الزراعية" },
  { id: 2, title: "دور البكتيريا النافعة في تحسين خصوبة التربة", project_id: "RSH002", type: "conference", year: 2026, authors: "سارة علي", journal: "مؤتمر الزراعة المستدامة" },
  { id: 3, title: "نظام IoT للري الذكي", project_id: "RSH003", type: "journal", year: 2025, authors: "محمد أحمد وآخرون", journal: "مجلة التقنيات الزراعية" },
]

const ResearchPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("projects")
  const [projects, setProjects] = useState(mockProjects)
  const [publications, setPublications] = useState(mockPublications)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedProject, setSelectedProject] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const projectForm = useForm({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      title: "",
      code: "",
      type: "applied",
      field: "",
      objectives: "",
      start_date: new Date().toISOString().split('T')[0],
      end_date: "",
      budget: 0,
      lead_researcher: "",
      funding_source: "",
    },
  })

  // Filter projects
  const filteredProjects = projects.filter(p => {
    const matchesSearch = p.title.includes(searchQuery) || 
                         p.code?.includes(searchQuery) ||
                         p.lead_researcher?.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || p.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Statistics
  const stats = {
    totalProjects: projects.length,
    activeProjects: projects.filter(p => p.status === "active").length,
    completedProjects: projects.filter(p => p.status === "completed").length,
    totalBudget: projects.reduce((sum, p) => sum + (p.budget || 0), 0),
    totalPublications: projects.reduce((sum, p) => sum + (p.publications || 0), 0),
    totalPatents: projects.reduce((sum, p) => sum + (p.patents || 0), 0),
  }

  // Handlers
  const handleCreateProject = async (data) => {
    setIsSubmitting(true)
    try {
      const newProject = {
        id: `RSH${String(projects.length + 1).padStart(3, '0')}`,
        code: data.code || `AGR-${new Date().getFullYear()}-${String(projects.length + 1).padStart(3, '0')}`,
        ...data,
        status: "proposal",
        progress: 0,
        spent: 0,
        team: [],
        publications: 0,
        patents: 0,
      }
      setProjects([...projects, newProject])
      toast.success("تم إنشاء المشروع البحثي بنجاح")
      setIsProjectDialogOpen(false)
      projectForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء المشروع")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleUpdateStatus = (project, newStatus) => {
    setProjects(projects.map(p => 
      p.id === project.id ? { ...p, status: newStatus } : p
    ))
    toast.success(`تم تحديث الحالة إلى ${statusConfig[newStatus].label}`)
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setProjects(projects.filter(p => p.id !== selectedProject.id))
      toast.success("تم حذف المشروع")
      setIsDeleteDialogOpen(false)
      setSelectedProject(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  // Project columns
  const projectColumns = [
    {
      accessorKey: "title",
      header: "المشروع",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
            <GraduationCap className="w-5 h-5 text-indigo-600" />
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
    {
      accessorKey: "lead_researcher",
      header: "الباحث الرئيسي",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <Avatar className="w-6 h-6">
            <AvatarFallback className="text-xs bg-primary/10 text-primary">
              {row.original.lead_researcher?.split(' ').map(n => n[0]).join('') || '—'}
            </AvatarFallback>
          </Avatar>
          <span>{row.original.lead_researcher || "—"}</span>
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
      accessorKey: "budget",
      header: "الميزانية",
      cell: ({ row }) => (
        <span className="font-mono">{row.original.budget?.toLocaleString()} ج.م</span>
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const project = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedProject(project); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              {project.status === "proposal" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(project, "approved")}>
                  <CheckCircle2 className="w-4 h-4 ml-2" />اعتماد
                </DropdownMenuItem>
              )}
              {project.status === "approved" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(project, "active")}>
                  <Microscope className="w-4 h-4 ml-2" />بدء التنفيذ
                </DropdownMenuItem>
              )}
              {project.status === "active" && (
                <DropdownMenuItem onClick={() => handleUpdateStatus(project, "completed")}>
                  <Award className="w-4 h-4 ml-2" />إكمال
                </DropdownMenuItem>
              )}
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل التقرير...")}>
                <FileText className="w-4 h-4 ml-2" />تقرير المشروع
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedProject(project); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Publications columns
  const publicationsColumns = [
    { accessorKey: "title", header: "العنوان" },
    { accessorKey: "authors", header: "المؤلفين" },
    { accessorKey: "type", header: "النوع", cell: ({ row }) => (
      <Badge variant="outline">{row.original.type === "journal" ? "مجلة علمية" : "مؤتمر"}</Badge>
    )},
    { accessorKey: "journal", header: "المجلة/المؤتمر" },
    { accessorKey: "year", header: "السنة" },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <GraduationCap className="w-7 h-7 text-indigo-500" />
            البحث العلمي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المشاريع البحثية والمنشورات</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button onClick={() => { setDialogMode("add"); setIsProjectDialogOpen(true); }}>
            <Plus className="w-4 h-4 ml-2" />مشروع جديد
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-indigo-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalProjects}</p>
              <p className="text-xs text-muted-foreground">إجمالي المشاريع</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <Microscope className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeProjects}</p>
              <p className="text-xs text-muted-foreground">مشاريع جارية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Award className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.completedProjects}</p>
              <p className="text-xs text-muted-foreground">مكتملة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.totalBudget / 1000000).toFixed(1)}M</p>
              <p className="text-xs text-muted-foreground">الميزانية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalPublications}</p>
              <p className="text-xs text-muted-foreground">منشورات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <LinkIcon className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalPatents}</p>
              <p className="text-xs text-muted-foreground">براءات اختراع</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="projects" className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />المشاريع البحثية
          </TabsTrigger>
          <TabsTrigger value="publications" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />المنشورات
          </TabsTrigger>
        </TabsList>

        {/* Projects Tab */}
        <TabsContent value="projects" className="space-y-4">
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
                    <SelectItem value="proposal">مقترح</SelectItem>
                    <SelectItem value="approved">معتمد</SelectItem>
                    <SelectItem value="active">جاري</SelectItem>
                    <SelectItem value="completed">مكتمل</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>المشاريع البحثية ({filteredProjects.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={projectColumns} data={filteredProjects} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Publications Tab */}
        <TabsContent value="publications" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>المنشورات العلمية</CardTitle>
                <CardDescription>الأوراق البحثية والمؤتمرات</CardDescription>
              </div>
              <Button onClick={() => toast.info("جاري إضافة منشور...")}>
                <Plus className="w-4 h-4 ml-2" />إضافة منشور
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={publicationsColumns} data={publications} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Project Dialog */}
      <FormDialog
        open={isProjectDialogOpen}
        onOpenChange={setIsProjectDialogOpen}
        title="مشروع بحثي جديد"
        description="إنشاء مشروع بحثي جديد"
        onSubmit={projectForm.handleSubmit(handleCreateProject)}
        isSubmitting={isSubmitting}
        size="xl"
      >
        <div className="space-y-4">
          <div>
            <Label>عنوان المشروع</Label>
            <Input {...projectForm.register("title")} placeholder="تطوير أصناف طماطم مقاومة للجفاف" />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>النوع</Label>
              <Select value={projectForm.watch("type")} onValueChange={(v) => projectForm.setValue("type", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="basic">بحث أساسي</SelectItem>
                  <SelectItem value="applied">بحث تطبيقي</SelectItem>
                  <SelectItem value="development">تطوير</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>مجال البحث</Label>
              <Input {...projectForm.register("field")} placeholder="تربية النبات" />
            </div>
            <div>
              <Label>رمز المشروع (اختياري)</Label>
              <Input {...projectForm.register("code")} placeholder="AGR-2026-001" />
            </div>
          </div>
          <div>
            <Label>أهداف البحث</Label>
            <Textarea {...projectForm.register("objectives")} placeholder="وصف تفصيلي لأهداف البحث..." rows={4} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>تاريخ البدء</Label>
              <Input type="date" {...projectForm.register("start_date")} />
            </div>
            <div>
              <Label>تاريخ الانتهاء المتوقع</Label>
              <Input type="date" {...projectForm.register("end_date")} />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>الميزانية (ج.م)</Label>
              <Input type="number" {...projectForm.register("budget", { valueAsNumber: true })} />
            </div>
            <div>
              <Label>الباحث الرئيسي</Label>
              <Input {...projectForm.register("lead_researcher")} placeholder="د. أحمد محمد" />
            </div>
            <div>
              <Label>جهة التمويل</Label>
              <Input {...projectForm.register("funding_source")} placeholder="وزارة الزراعة" />
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedProject(null); }}
        title={selectedProject?.title}
        subtitle={selectedProject?.code}
        badge={selectedProject && { text: statusConfig[selectedProject.status]?.label }}
        size="lg"
      >
        {selectedProject && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات المشروع">
              <ViewDialog.Row label="النوع" value={typeConfig[selectedProject.type]?.label} />
              <ViewDialog.Row label="المجال" value={selectedProject.field} />
              <ViewDialog.Row label="الباحث الرئيسي" value={selectedProject.lead_researcher || "—"} />
              <ViewDialog.Row label="جهة التمويل" value={selectedProject.funding_source || "—"} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الأهداف">
              <p className="text-sm">{selectedProject.objectives}</p>
            </ViewDialog.Section>
            <ViewDialog.Section title="فريق العمل">
              <div className="flex flex-wrap gap-2">
                {selectedProject.team?.map((member, idx) => (
                  <Badge key={idx} variant="secondary">{member}</Badge>
                ))}
              </div>
            </ViewDialog.Section>
            <ViewDialog.Section title="الميزانية والتقدم">
              <ViewDialog.Row label="الميزانية" value={`${selectedProject.budget?.toLocaleString()} ج.م`} />
              <ViewDialog.Row label="المصروف" value={`${selectedProject.spent?.toLocaleString()} ج.م`} />
              <ViewDialog.Row label="التقدم" value={`${selectedProject.progress}%`} />
            </ViewDialog.Section>
            <ViewDialog.Section title="المخرجات">
              <ViewDialog.Row label="المنشورات" value={selectedProject.publications} />
              <ViewDialog.Row label="براءات الاختراع" value={selectedProject.patents} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف المشروع"
        description={`هل أنت متأكد من حذف المشروع "${selectedProject?.title}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default ResearchPage
