/**
 * Backup Management Page - إدارة النسخ الاحتياطي
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Database,
  Plus,
  Download,
  Upload,
  Trash2,
  Clock,
  HardDrive,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Calendar,
  Settings,
  Play,
  Pause,
  AlertTriangle,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"

import { DataTable } from "@/components/common"
import { formatDate, formatFileSize } from "@/lib/utils"

// Mock data
const mockBackups = [
  {
    id: 1,
    name: "backup_2026_01_16_103000.sql",
    type: "full",
    size: 256000000,
    status: "completed",
    created_at: "2026-01-16T10:30:00Z",
    created_by: "أحمد محمد",
    storage_location: "local",
    tables_count: 150,
    records_count: 50000,
  },
  {
    id: 2,
    name: "backup_2026_01_15_220000.sql",
    type: "full",
    size: 245000000,
    status: "completed",
    created_at: "2026-01-15T22:00:00Z",
    created_by: "النظام (تلقائي)",
    storage_location: "cloud",
    tables_count: 150,
    records_count: 49500,
  },
  {
    id: 3,
    name: "backup_2026_01_14_220000.sql",
    type: "incremental",
    size: 15000000,
    status: "completed",
    created_at: "2026-01-14T22:00:00Z",
    created_by: "النظام (تلقائي)",
    storage_location: "cloud",
    tables_count: 25,
    records_count: 1500,
  },
  {
    id: 4,
    name: "backup_2026_01_13_103000.sql",
    type: "full",
    size: 240000000,
    status: "failed",
    created_at: "2026-01-13T10:30:00Z",
    created_by: "سارة أحمد",
    storage_location: "local",
    error_message: "نفاد مساحة القرص",
  },
]

const BackupPage = () => {
  const [backups, setBackups] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [createProgress, setCreateProgress] = useState(0)
  
  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isRestoreDialogOpen, setIsRestoreDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isScheduleDialogOpen, setIsScheduleDialogOpen] = useState(false)
  const [selectedBackup, setSelectedBackup] = useState(null)
  
  // Backup options
  const [backupType, setBackupType] = useState("full")
  const [storageLocation, setStorageLocation] = useState("local")
  
  // Schedule settings
  const [scheduleEnabled, setScheduleEnabled] = useState(true)
  const [scheduleFrequency, setScheduleFrequency] = useState("daily")
  const [scheduleTime, setScheduleTime] = useState("22:00")

  useEffect(() => {
    loadBackups()
  }, [])

  const loadBackups = async () => {
    setIsLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setBackups(mockBackups)
    } catch (error) {
      toast.error("فشل تحميل النسخ الاحتياطية")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateBackup = async () => {
    setIsCreating(true)
    setCreateProgress(0)
    
    // Simulate backup progress
    const interval = setInterval(() => {
      setCreateProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 10
      })
    }, 500)
    
    setTimeout(() => {
      const newBackup = {
        id: backups.length + 1,
        name: `backup_${new Date().toISOString().replace(/[-:T.]/g, "_").slice(0, 15)}.sql`,
        type: backupType,
        size: Math.floor(Math.random() * 100000000) + 200000000,
        status: "completed",
        created_at: new Date().toISOString(),
        created_by: "المستخدم الحالي",
        storage_location: storageLocation,
        tables_count: 150,
        records_count: Math.floor(Math.random() * 10000) + 45000,
      }
      setBackups([newBackup, ...backups])
      setIsCreating(false)
      setIsCreateDialogOpen(false)
      toast.success("تم إنشاء النسخة الاحتياطية بنجاح")
    }, 5000)
  }

  const handleRestore = async () => {
    toast.info("جاري استعادة النسخة الاحتياطية...")
    setTimeout(() => {
      toast.success("تم استعادة النسخة الاحتياطية بنجاح")
      setIsRestoreDialogOpen(false)
    }, 3000)
  }

  const handleDelete = async () => {
    setBackups(backups.filter((b) => b.id !== selectedBackup.id))
    setIsDeleteDialogOpen(false)
    toast.success("تم حذف النسخة الاحتياطية")
  }

  const handleDownload = (backup) => {
    toast.success(`جاري تحميل ${backup.name}`)
  }

  const handleSaveSchedule = () => {
    toast.success("تم حفظ إعدادات الجدولة")
    setIsScheduleDialogOpen(false)
  }

  const typeLabels = {
    full: "كاملة",
    incremental: "تزايدية",
    differential: "تفاضلية",
  }

  const statusConfig = {
    completed: { label: "مكتمل", color: "default", icon: CheckCircle2 },
    failed: { label: "فشل", color: "destructive", icon: XCircle },
    in_progress: { label: "قيد التنفيذ", color: "secondary", icon: RefreshCw },
  }

  const columns = [
    {
      accessorKey: "name",
      header: "اسم النسخة",
      cell: ({ row }) => {
        const backup = row.original
        return (
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              backup.status === "completed" 
                ? "bg-green-100 dark:bg-green-900" 
                : "bg-red-100 dark:bg-red-900"
            }`}>
              <Database className={`w-5 h-5 ${
                backup.status === "completed" 
                  ? "text-green-600 dark:text-green-400" 
                  : "text-red-600 dark:text-red-400"
              }`} />
            </div>
            <div>
              <p className="font-medium font-mono text-sm">{backup.name}</p>
              <p className="text-xs text-muted-foreground">
                {backup.tables_count} جدول • {backup.records_count?.toLocaleString()} سجل
              </p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => (
        <Badge variant="outline">{typeLabels[row.original.type]}</Badge>
      ),
    },
    {
      accessorKey: "size",
      header: "الحجم",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <HardDrive className="w-4 h-4" />
          {formatFileSize(row.original.size)}
        </div>
      ),
    },
    {
      accessorKey: "storage_location",
      header: "الموقع",
      cell: ({ row }) => (
        <Badge variant="secondary">
          {row.original.storage_location === "local" ? "محلي" : "سحابي"}
        </Badge>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <Badge variant={config.color}>
            <Icon className="w-3 h-3 ml-1" />
            {config.label}
          </Badge>
        )
      },
    },
    {
      accessorKey: "created_at",
      header: "التاريخ",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <Clock className="w-4 h-4" />
          {formatDate(row.original.created_at, "PPp")}
        </div>
      ),
    },
    {
      accessorKey: "created_by",
      header: "بواسطة",
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const backup = row.original
        return (
          <div className="flex items-center gap-2">
            {backup.status === "completed" && (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDownload(backup)}
                >
                  <Download className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => { setSelectedBackup(backup); setIsRestoreDialogOpen(true); }}
                >
                  <Upload className="w-4 h-4" />
                </Button>
              </>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => { setSelectedBackup(backup); setIsDeleteDialogOpen(true); }}
              className="text-red-600"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        )
      },
    },
  ]

  // Stats
  const stats = {
    total: backups.length,
    completed: backups.filter(b => b.status === "completed").length,
    totalSize: backups.reduce((sum, b) => sum + (b.size || 0), 0),
    lastBackup: backups.find(b => b.status === "completed")?.created_at,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Database className="w-7 h-7 text-green-500" />
            النسخ الاحتياطي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة النسخ الاحتياطية واستعادة البيانات
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={() => setIsScheduleDialogOpen(true)}>
            <Calendar className="w-4 h-4 ml-2" />
            الجدولة
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 ml-2" />
            نسخة جديدة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Database className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي النسخ</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.completed}</p>
              <p className="text-sm text-muted-foreground">نسخ ناجحة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{formatFileSize(stats.totalSize)}</p>
              <p className="text-sm text-muted-foreground">الحجم الكلي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-sm font-bold">
                {stats.lastBackup ? formatDate(stats.lastBackup, "PPp") : "لا يوجد"}
              </p>
              <p className="text-sm text-muted-foreground">آخر نسخة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Schedule Status */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                scheduleEnabled ? "bg-green-100 dark:bg-green-900" : "bg-gray-100 dark:bg-gray-900"
              }`}>
                {scheduleEnabled ? (
                  <Play className="w-5 h-5 text-green-500" />
                ) : (
                  <Pause className="w-5 h-5 text-gray-500" />
                )}
              </div>
              <div>
                <p className="font-medium">النسخ التلقائي</p>
                <p className="text-sm text-muted-foreground">
                  {scheduleEnabled ? `كل يوم الساعة ${scheduleTime}` : "متوقف"}
                </p>
              </div>
            </div>
            <Switch
              checked={scheduleEnabled}
              onCheckedChange={setScheduleEnabled}
            />
          </div>
        </CardContent>
      </Card>

      {/* Backups Table */}
      <Card>
        <CardHeader>
          <CardTitle>النسخ الاحتياطية ({backups.length})</CardTitle>
          <CardDescription>قائمة جميع النسخ الاحتياطية</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={backups}
            isLoading={isLoading}
            searchKey="name"
            defaultPageSize={10}
          />
        </CardContent>
      </Card>

      {/* Create Backup Dialog */}
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>إنشاء نسخة احتياطية</DialogTitle>
            <DialogDescription>
              اختر خيارات النسخة الاحتياطية الجديدة
            </DialogDescription>
          </DialogHeader>
          {isCreating ? (
            <div className="space-y-4 py-4">
              <div className="flex items-center justify-center">
                <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
              </div>
              <p className="text-center">جاري إنشاء النسخة الاحتياطية...</p>
              <Progress value={createProgress} />
              <p className="text-center text-sm text-muted-foreground">{createProgress}%</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <Label>نوع النسخة</Label>
                <Select value={backupType} onValueChange={setBackupType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="full">نسخة كاملة</SelectItem>
                    <SelectItem value="incremental">نسخة تزايدية</SelectItem>
                    <SelectItem value="differential">نسخة تفاضلية</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>موقع التخزين</Label>
                <Select value={storageLocation} onValueChange={setStorageLocation}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="local">تخزين محلي</SelectItem>
                    <SelectItem value="cloud">تخزين سحابي</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  إلغاء
                </Button>
                <Button onClick={handleCreateBackup}>
                  <Database className="w-4 h-4 ml-2" />
                  إنشاء النسخة
                </Button>
              </DialogFooter>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Restore Dialog */}
      <AlertDialog open={isRestoreDialogOpen} onOpenChange={setIsRestoreDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
              استعادة النسخة الاحتياطية
            </AlertDialogTitle>
            <AlertDialogDescription>
              <span className="block mb-2">
                هل أنت متأكد من استعادة النسخة "{selectedBackup?.name}"؟
              </span>
              <span className="block text-red-600 font-medium">
                تحذير: سيتم استبدال جميع البيانات الحالية بالبيانات من هذه النسخة.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleRestore} className="bg-yellow-600 hover:bg-yellow-700">
              <Upload className="w-4 h-4 ml-2" />
              استعادة
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Delete Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>حذف النسخة الاحتياطية</AlertDialogTitle>
            <AlertDialogDescription>
              هل أنت متأكد من حذف النسخة "{selectedBackup?.name}"؟
              لا يمكن التراجع عن هذا الإجراء.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              حذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Schedule Dialog */}
      <Dialog open={isScheduleDialogOpen} onOpenChange={setIsScheduleDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>إعدادات الجدولة</DialogTitle>
            <DialogDescription>
              تحديد أوقات النسخ الاحتياطي التلقائي
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label>تفعيل النسخ التلقائي</Label>
              <Switch
                checked={scheduleEnabled}
                onCheckedChange={setScheduleEnabled}
              />
            </div>
            <Separator />
            <div>
              <Label>التكرار</Label>
              <Select value={scheduleFrequency} onValueChange={setScheduleFrequency}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
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
              <Select value={scheduleTime} onValueChange={setScheduleTime}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="00:00">12:00 ص</SelectItem>
                  <SelectItem value="06:00">6:00 ص</SelectItem>
                  <SelectItem value="12:00">12:00 م</SelectItem>
                  <SelectItem value="18:00">6:00 م</SelectItem>
                  <SelectItem value="22:00">10:00 م</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsScheduleDialogOpen(false)}>
                إلغاء
              </Button>
              <Button onClick={handleSaveSchedule}>
                <Settings className="w-4 h-4 ml-2" />
                حفظ
              </Button>
            </DialogFooter>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default BackupPage
