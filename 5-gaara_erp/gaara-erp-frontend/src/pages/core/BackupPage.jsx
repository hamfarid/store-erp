/**
 * Backup Management Page - إدارة النسخ الاحتياطي
 * Gaara ERP v12
 *
 * Backup and restore management with scheduling capabilities.
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
  Database,
  Download,
  Upload,
  Plus,
  Search,
  MoreVertical,
  Trash2,
  Eye,
  Calendar,
  CheckCircle2,
  Clock,
  RefreshCw,
  HardDrive,
  Cloud,
  Server,
  FileArchive,
  Settings,
  Play,
  Pause,
  AlertTriangle,
  Shield,
  History,
  Loader2,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Switch } from "@/components/ui/switch"
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
const scheduleSchema = z.object({
  name: z.string().min(1, "الاسم مطلوب"),
  frequency: z.enum(["hourly", "daily", "weekly", "monthly"]),
  time: z.string().optional(),
  day: z.string().optional(),
  retention: z.number().min(1).default(30),
  type: z.enum(["full", "incremental", "differential"]),
  destination: z.enum(["local", "cloud", "both"]),
  compression: z.boolean().default(true),
  encryption: z.boolean().default(true),
})

// Status configurations
const statusConfig = {
  completed: { label: "مكتمل", color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  running: { label: "جاري", color: "bg-blue-100 text-blue-700", icon: Loader2 },
  failed: { label: "فشل", color: "bg-red-100 text-red-700", icon: AlertTriangle },
  pending: { label: "معلق", color: "bg-yellow-100 text-yellow-700", icon: Clock },
}

const typeConfig = {
  full: { label: "كامل", color: "bg-purple-100 text-purple-700" },
  incremental: { label: "تزايدي", color: "bg-blue-100 text-blue-700" },
  differential: { label: "تفاضلي", color: "bg-cyan-100 text-cyan-700" },
}

// Mock data
const mockBackups = [
  {
    id: "BKP001",
    name: "نسخة يومية - قاعدة البيانات",
    type: "full",
    status: "completed",
    size: "2.5 GB",
    created_at: "2026-01-17 02:00:00",
    duration: "5m 32s",
    destination: "cloud",
    compressed: true,
    encrypted: true,
  },
  {
    id: "BKP002",
    name: "نسخة ساعية تزايدية",
    type: "incremental",
    status: "completed",
    size: "150 MB",
    created_at: "2026-01-17 10:00:00",
    duration: "45s",
    destination: "local",
    compressed: true,
    encrypted: true,
  },
  {
    id: "BKP003",
    name: "نسخة أسبوعية كاملة",
    type: "full",
    status: "running",
    size: "—",
    created_at: "2026-01-17 14:00:00",
    duration: "جاري...",
    destination: "both",
    compressed: true,
    encrypted: true,
    progress: 65,
  },
  {
    id: "BKP004",
    name: "نسخة الطوارئ",
    type: "full",
    status: "failed",
    size: "—",
    created_at: "2026-01-16 23:00:00",
    duration: "فشل بعد 2m 15s",
    destination: "cloud",
    compressed: true,
    encrypted: true,
    error: "فشل الاتصال بخادم التخزين السحابي",
  },
]

const mockSchedules = [
  { id: 1, name: "نسخة يومية", frequency: "daily", time: "02:00", type: "full", destination: "cloud", retention: 30, enabled: true, lastRun: "2026-01-17 02:00" },
  { id: 2, name: "نسخة ساعية", frequency: "hourly", time: ":00", type: "incremental", destination: "local", retention: 24, enabled: true, lastRun: "2026-01-17 10:00" },
  { id: 3, name: "نسخة أسبوعية", frequency: "weekly", time: "03:00", day: "friday", type: "full", destination: "both", retention: 12, enabled: true, lastRun: "2026-01-10 03:00" },
  { id: 4, name: "نسخة شهرية", frequency: "monthly", time: "04:00", day: "1", type: "full", destination: "cloud", retention: 12, enabled: false, lastRun: "2026-01-01 04:00" },
]

const BackupPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("backups")
  const [backups, setBackups] = useState(mockBackups)
  const [schedules, setSchedules] = useState(mockSchedules)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [isBackupRunning, setIsBackupRunning] = useState(false)

  // Dialog states
  const [isScheduleDialogOpen, setIsScheduleDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isRestoreDialogOpen, setIsRestoreDialogOpen] = useState(false)
  const [selectedBackup, setSelectedBackup] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const scheduleForm = useForm({
    resolver: zodResolver(scheduleSchema),
    defaultValues: {
      name: "",
      frequency: "daily",
      time: "02:00",
      type: "full",
      destination: "cloud",
      retention: 30,
      compression: true,
      encryption: true,
    },
  })

  // Statistics
  const stats = {
    totalBackups: backups.length,
    totalSize: "45.2 GB",
    lastBackup: "منذ ساعة",
    successRate: "95%",
    activeSchedules: schedules.filter(s => s.enabled).length,
    storageUsed: 65,
  }

  // Handlers
  const handleCreateBackup = () => {
    setIsBackupRunning(true)
    toast.info("جاري إنشاء نسخة احتياطية...")
    
    setTimeout(() => {
      const newBackup = {
        id: `BKP${String(backups.length + 1).padStart(3, '0')}`,
        name: "نسخة يدوية",
        type: "full",
        status: "completed",
        size: "2.8 GB",
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
        duration: "6m 15s",
        destination: "local",
        compressed: true,
        encrypted: true,
      }
      setBackups([newBackup, ...backups])
      setIsBackupRunning(false)
      toast.success("تم إنشاء النسخة الاحتياطية بنجاح")
    }, 3000)
  }

  const handleCreateSchedule = async (data) => {
    setIsSubmitting(true)
    try {
      const newSchedule = {
        id: schedules.length + 1,
        ...data,
        enabled: true,
        lastRun: "—",
      }
      setSchedules([...schedules, newSchedule])
      toast.success("تم إنشاء الجدولة بنجاح")
      setIsScheduleDialogOpen(false)
      scheduleForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء الجدولة")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleToggleSchedule = (schedule) => {
    setSchedules(schedules.map(s => 
      s.id === schedule.id ? { ...s, enabled: !s.enabled } : s
    ))
    toast.success(schedule.enabled ? "تم تعطيل الجدولة" : "تم تفعيل الجدولة")
  }

  const handleRestore = () => {
    toast.info(`جاري استعادة النسخة ${selectedBackup?.id}...`)
    setTimeout(() => {
      setIsRestoreDialogOpen(false)
      toast.success("تم استعادة النسخة الاحتياطية بنجاح")
    }, 3000)
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      setBackups(backups.filter(b => b.id !== selectedBackup.id))
      toast.success("تم حذف النسخة الاحتياطية")
      setIsDeleteDialogOpen(false)
      setSelectedBackup(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDownload = (backup) => {
    toast.info(`جاري تحميل ${backup.name}...`)
  }

  // Backup columns
  const backupColumns = [
    {
      accessorKey: "name",
      header: "النسخة",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
            row.original.destination === "cloud" ? "bg-blue-100" : 
            row.original.destination === "both" ? "bg-purple-100" : "bg-gray-100"
          }`}>
            {row.original.destination === "cloud" ? (
              <Cloud className="w-5 h-5 text-blue-600" />
            ) : row.original.destination === "both" ? (
              <Server className="w-5 h-5 text-purple-600" />
            ) : (
              <HardDrive className="w-5 h-5 text-gray-600" />
            )}
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground font-mono">{row.original.id}</p>
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
      accessorKey: "size",
      header: "الحجم",
      cell: ({ row }) => (
        <span className="font-mono">{row.original.size}</span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <div className="flex items-center gap-2">
            <Badge className={config?.color}>
              <Icon className={`w-3 h-3 ml-1 ${row.original.status === 'running' ? 'animate-spin' : ''}`} />
              {config?.label}
            </Badge>
            {row.original.progress && (
              <span className="text-sm text-muted-foreground">{row.original.progress}%</span>
            )}
          </div>
        )
      },
    },
    {
      accessorKey: "created_at",
      header: "التاريخ",
    },
    {
      accessorKey: "duration",
      header: "المدة",
    },
    {
      id: "features",
      header: "الميزات",
      cell: ({ row }) => (
        <div className="flex gap-1">
          {row.original.compressed && <Badge variant="outline" className="text-xs">مضغوط</Badge>}
          {row.original.encrypted && <Badge variant="outline" className="text-xs"><Shield className="w-3 h-3" /></Badge>}
        </div>
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const backup = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedBackup(backup); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
              </DropdownMenuItem>
              {backup.status === "completed" && (
                <>
                  <DropdownMenuItem onClick={() => handleDownload(backup)}>
                    <Download className="w-4 h-4 ml-2" />تحميل
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => { setSelectedBackup(backup); setIsRestoreDialogOpen(true); }}>
                    <History className="w-4 h-4 ml-2" />استعادة
                  </DropdownMenuItem>
                </>
              )}
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedBackup(backup); setIsDeleteDialogOpen(true); }} className="text-red-600">
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
            <Database className="w-7 h-7 text-emerald-500" />
            إدارة النسخ الاحتياطي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">النسخ الاحتياطي والاستعادة</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري فتح الإعدادات...")}>
            <Settings className="w-4 h-4 ml-2" />الإعدادات
          </Button>
          <Button onClick={handleCreateBackup} disabled={isBackupRunning}>
            {isBackupRunning ? (
              <Loader2 className="w-4 h-4 ml-2 animate-spin" />
            ) : (
              <Plus className="w-4 h-4 ml-2" />
            )}
            نسخة احتياطية
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <FileArchive className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalBackups}</p>
              <p className="text-xs text-muted-foreground">إجمالي النسخ</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.totalSize}</p>
              <p className="text-xs text-muted-foreground">الحجم الكلي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.lastBackup}</p>
              <p className="text-xs text-muted-foreground">آخر نسخة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.successRate}</p>
              <p className="text-xs text-muted-foreground">نسبة النجاح</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.activeSchedules}</p>
              <p className="text-xs text-muted-foreground">جدولات نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex justify-between mb-2">
              <span className="text-sm">التخزين</span>
              <span className="text-sm font-medium">{stats.storageUsed}%</span>
            </div>
            <Progress value={stats.storageUsed} className="h-2" />
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="backups" className="flex items-center gap-2">
            <FileArchive className="w-4 h-4" />النسخ الاحتياطية
          </TabsTrigger>
          <TabsTrigger value="schedules" className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />الجدولة
          </TabsTrigger>
        </TabsList>

        {/* Backups Tab */}
        <TabsContent value="backups" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>النسخ الاحتياطية ({backups.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={backupColumns} data={backups} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Schedules Tab */}
        <TabsContent value="schedules" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>جدولة النسخ الاحتياطي</CardTitle>
                <CardDescription>إدارة جدولات النسخ الاحتياطي التلقائية</CardDescription>
              </div>
              <Button onClick={() => setIsScheduleDialogOpen(true)}>
                <Plus className="w-4 h-4 ml-2" />جدولة جديدة
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {schedules.map((schedule) => (
                  <div key={schedule.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <Switch checked={schedule.enabled} onCheckedChange={() => handleToggleSchedule(schedule)} />
                      <div>
                        <p className="font-medium">{schedule.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {schedule.frequency === "hourly" ? "كل ساعة" :
                           schedule.frequency === "daily" ? `يومياً الساعة ${schedule.time}` :
                           schedule.frequency === "weekly" ? `أسبوعياً - ${schedule.day} الساعة ${schedule.time}` :
                           `شهرياً - اليوم ${schedule.day} الساعة ${schedule.time}`}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge className={typeConfig[schedule.type]?.color}>{typeConfig[schedule.type]?.label}</Badge>
                      <div className="text-sm text-muted-foreground">آخر تشغيل: {schedule.lastRun}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Schedule Dialog */}
      <FormDialog
        open={isScheduleDialogOpen}
        onOpenChange={setIsScheduleDialogOpen}
        title="جدولة جديدة"
        description="إنشاء جدولة نسخ احتياطي تلقائية"
        onSubmit={scheduleForm.handleSubmit(handleCreateSchedule)}
        isSubmitting={isSubmitting}
      >
        <div className="space-y-4">
          <div>
            <Label>اسم الجدولة</Label>
            <Input {...scheduleForm.register("name")} placeholder="نسخة يومية" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>التكرار</Label>
              <Select value={scheduleForm.watch("frequency")} onValueChange={(v) => scheduleForm.setValue("frequency", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="hourly">كل ساعة</SelectItem>
                  <SelectItem value="daily">يومياً</SelectItem>
                  <SelectItem value="weekly">أسبوعياً</SelectItem>
                  <SelectItem value="monthly">شهرياً</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الوقت</Label>
              <Input type="time" {...scheduleForm.register("time")} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>نوع النسخة</Label>
              <Select value={scheduleForm.watch("type")} onValueChange={(v) => scheduleForm.setValue("type", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="full">كامل</SelectItem>
                  <SelectItem value="incremental">تزايدي</SelectItem>
                  <SelectItem value="differential">تفاضلي</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>مكان التخزين</Label>
              <Select value={scheduleForm.watch("destination")} onValueChange={(v) => scheduleForm.setValue("destination", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="local">محلي</SelectItem>
                  <SelectItem value="cloud">سحابي</SelectItem>
                  <SelectItem value="both">كلاهما</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>فترة الاحتفاظ (أيام)</Label>
            <Input type="number" {...scheduleForm.register("retention", { valueAsNumber: true })} />
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Switch checked={scheduleForm.watch("compression")} onCheckedChange={(v) => scheduleForm.setValue("compression", v)} />
              <Label>ضغط</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch checked={scheduleForm.watch("encryption")} onCheckedChange={(v) => scheduleForm.setValue("encryption", v)} />
              <Label>تشفير</Label>
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedBackup(null); }}
        title={selectedBackup?.name}
        subtitle={selectedBackup?.id}
        badge={selectedBackup && { text: statusConfig[selectedBackup.status]?.label }}
        size="lg"
      >
        {selectedBackup && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات النسخة">
              <ViewDialog.Row label="النوع" value={typeConfig[selectedBackup.type]?.label} />
              <ViewDialog.Row label="الحجم" value={selectedBackup.size} />
              <ViewDialog.Row label="المدة" value={selectedBackup.duration} />
              <ViewDialog.Row label="التاريخ" value={selectedBackup.created_at} />
            </ViewDialog.Section>
            <ViewDialog.Section title="التخزين">
              <ViewDialog.Row label="الوجهة" value={
                selectedBackup.destination === "cloud" ? "سحابي" :
                selectedBackup.destination === "both" ? "محلي + سحابي" : "محلي"
              } />
              <ViewDialog.Row label="ضغط" value={selectedBackup.compressed ? "نعم" : "لا"} />
              <ViewDialog.Row label="تشفير" value={selectedBackup.encrypted ? "نعم" : "لا"} />
            </ViewDialog.Section>
            {selectedBackup.error && (
              <ViewDialog.Section title="الخطأ">
                <p className="text-sm text-red-600">{selectedBackup.error}</p>
              </ViewDialog.Section>
            )}
          </div>
        )}
      </ViewDialog>

      {/* Restore Confirmation */}
      <ConfirmDialog
        open={isRestoreDialogOpen}
        onOpenChange={setIsRestoreDialogOpen}
        title="استعادة النسخة الاحتياطية"
        description={`هل أنت متأكد من استعادة النسخة "${selectedBackup?.name}"؟ سيتم استبدال البيانات الحالية.`}
        variant="danger"
        onConfirm={handleRestore}
      />

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف النسخة الاحتياطية"
        description={`هل أنت متأكد من حذف النسخة "${selectedBackup?.name}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default BackupPage
