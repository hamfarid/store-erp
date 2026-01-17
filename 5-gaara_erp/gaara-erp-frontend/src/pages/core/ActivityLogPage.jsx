/**
 * Activity Log Page - سجل الأنشطة
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Activity,
  Search,
  Filter,
  RefreshCw,
  Download,
  Calendar,
  User,
  FileText,
  Eye,
  ChevronRight,
  AlertCircle,
  CheckCircle2,
  Info,
  AlertTriangle,
  Clock,
  Monitor,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"

import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"
import { api } from "@/services/api"

// Mock data
const mockActivities = [
  {
    id: 1,
    action: "LOGIN",
    action_ar: "تسجيل دخول",
    user_id: 1,
    user_name: "أحمد محمد",
    user_email: "ahmed@gaara.com",
    module: "auth",
    module_ar: "المصادقة",
    description: "تسجيل دخول ناجح",
    ip_address: "192.168.1.100",
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    device: "Desktop",
    browser: "Chrome 120",
    os: "Windows 10",
    location: "الرياض، السعودية",
    status: "success",
    metadata: { session_id: "sess_123456" },
    created_at: "2026-01-16T10:30:00Z",
  },
  {
    id: 2,
    action: "CREATE",
    action_ar: "إنشاء",
    user_id: 1,
    user_name: "أحمد محمد",
    user_email: "ahmed@gaara.com",
    module: "companies",
    module_ar: "الشركات",
    description: "إنشاء شركة جديدة: شركة الزراعة المتقدمة",
    ip_address: "192.168.1.100",
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    device: "Desktop",
    browser: "Chrome 120",
    os: "Windows 10",
    location: "الرياض، السعودية",
    status: "success",
    metadata: { company_id: 5, company_name: "شركة الزراعة المتقدمة" },
    created_at: "2026-01-16T10:35:00Z",
  },
  {
    id: 3,
    action: "UPDATE",
    action_ar: "تحديث",
    user_id: 2,
    user_name: "سارة أحمد",
    user_email: "sara@gaara.com",
    module: "inventory",
    module_ar: "المخزون",
    description: "تحديث كمية المنتج: بذور القمح",
    ip_address: "192.168.1.101",
    user_agent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)",
    device: "Mobile",
    browser: "Safari 17",
    os: "iOS 17",
    location: "جدة، السعودية",
    status: "success",
    metadata: { product_id: 10, old_qty: 100, new_qty: 150 },
    created_at: "2026-01-16T11:00:00Z",
  },
  {
    id: 4,
    action: "DELETE",
    action_ar: "حذف",
    user_id: 1,
    user_name: "أحمد محمد",
    user_email: "ahmed@gaara.com",
    module: "contacts",
    module_ar: "جهات الاتصال",
    description: "حذف جهة اتصال: مورد قديم",
    ip_address: "192.168.1.100",
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    device: "Desktop",
    browser: "Chrome 120",
    os: "Windows 10",
    location: "الرياض، السعودية",
    status: "success",
    metadata: { contact_id: 25 },
    created_at: "2026-01-16T11:30:00Z",
  },
  {
    id: 5,
    action: "EXPORT",
    action_ar: "تصدير",
    user_id: 3,
    user_name: "محمد علي",
    user_email: "mohammed@gaara.com",
    module: "reports",
    module_ar: "التقارير",
    description: "تصدير تقرير المبيعات الشهري",
    ip_address: "192.168.1.102",
    user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    device: "Desktop",
    browser: "Safari 17",
    os: "macOS Sonoma",
    location: "الدمام، السعودية",
    status: "success",
    metadata: { report_type: "sales", format: "xlsx" },
    created_at: "2026-01-16T12:00:00Z",
  },
  {
    id: 6,
    action: "LOGIN_FAILED",
    action_ar: "فشل تسجيل الدخول",
    user_id: null,
    user_name: "غير معروف",
    user_email: "unknown@test.com",
    module: "auth",
    module_ar: "المصادقة",
    description: "محاولة تسجيل دخول فاشلة - كلمة مرور خاطئة",
    ip_address: "10.0.0.50",
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0",
    device: "Desktop",
    browser: "Firefox 121",
    os: "Windows 10",
    location: "غير معروف",
    status: "failed",
    metadata: { reason: "invalid_password", attempts: 3 },
    created_at: "2026-01-16T12:30:00Z",
  },
]

const ActivityLogPage = () => {
  const [activities, setActivities] = useState([])
  const [filteredActivities, setFilteredActivities] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [moduleFilter, setModuleFilter] = useState("all")
  const [actionFilter, setActionFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")
  const [dateFilter, setDateFilter] = useState("all")
  const [selectedActivity, setSelectedActivity] = useState(null)
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)

  // Load data
  useEffect(() => {
    loadActivities()
  }, [])

  // Filter activities
  useEffect(() => {
    let filtered = [...activities]

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (activity) =>
          activity.user_name.toLowerCase().includes(query) ||
          activity.description.toLowerCase().includes(query) ||
          activity.module_ar.includes(query)
      )
    }

    // Module filter
    if (moduleFilter !== "all") {
      filtered = filtered.filter((activity) => activity.module === moduleFilter)
    }

    // Action filter
    if (actionFilter !== "all") {
      filtered = filtered.filter((activity) => activity.action === actionFilter)
    }

    // Status filter
    if (statusFilter !== "all") {
      filtered = filtered.filter((activity) => activity.status === statusFilter)
    }

    setFilteredActivities(filtered)
  }, [activities, searchQuery, moduleFilter, actionFilter, statusFilter])

  const loadActivities = async () => {
    setIsLoading(true)
    try {
      // In production: const data = await api.get("/activity-log/")
      await new Promise((resolve) => setTimeout(resolve, 500))
      setActivities(mockActivities)
      setFilteredActivities(mockActivities)
    } catch (error) {
      toast.error("فشل تحميل سجل الأنشطة")
    } finally {
      setIsLoading(false)
    }
  }

  const handleExport = () => {
    toast.success("جاري تصدير السجل...")
    // Implement export logic
  }

  // Action icons and colors
  const actionConfig = {
    LOGIN: { icon: User, color: "text-blue-500", bg: "bg-blue-100 dark:bg-blue-900" },
    LOGIN_FAILED: { icon: AlertCircle, color: "text-red-500", bg: "bg-red-100 dark:bg-red-900" },
    LOGOUT: { icon: User, color: "text-gray-500", bg: "bg-gray-100 dark:bg-gray-900" },
    CREATE: { icon: CheckCircle2, color: "text-green-500", bg: "bg-green-100 dark:bg-green-900" },
    UPDATE: { icon: Info, color: "text-yellow-500", bg: "bg-yellow-100 dark:bg-yellow-900" },
    DELETE: { icon: AlertTriangle, color: "text-red-500", bg: "bg-red-100 dark:bg-red-900" },
    EXPORT: { icon: Download, color: "text-purple-500", bg: "bg-purple-100 dark:bg-purple-900" },
    IMPORT: { icon: FileText, color: "text-indigo-500", bg: "bg-indigo-100 dark:bg-indigo-900" },
  }

  // Table columns
  const columns = [
    {
      accessorKey: "action",
      header: "النشاط",
      cell: ({ row }) => {
        const activity = row.original
        const config = actionConfig[activity.action] || actionConfig.UPDATE
        const Icon = config.icon
        return (
          <div className="flex items-center gap-3">
            <div className={`w-9 h-9 rounded-lg ${config.bg} flex items-center justify-center`}>
              <Icon className={`w-4 h-4 ${config.color}`} />
            </div>
            <div>
              <p className="font-medium">{activity.action_ar}</p>
              <p className="text-sm text-muted-foreground">{activity.module_ar}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "user_name",
      header: "المستخدم",
      cell: ({ row }) => (
        <div>
          <p className="font-medium">{row.original.user_name}</p>
          <p className="text-sm text-muted-foreground">{row.original.user_email}</p>
        </div>
      ),
    },
    {
      accessorKey: "description",
      header: "الوصف",
      cell: ({ row }) => (
        <p className="max-w-[300px] truncate">{row.original.description}</p>
      ),
    },
    {
      accessorKey: "ip_address",
      header: "IP",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <Globe className="w-4 h-4" />
          <span className="font-mono text-sm">{row.original.ip_address}</span>
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        return (
          <Badge variant={status === "success" ? "default" : "destructive"}>
            {status === "success" ? "ناجح" : "فاشل"}
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
          <span>{formatDate(row.original.created_at, "PPpp")}</span>
        </div>
      ),
    },
    {
      id: "actions",
      header: "",
      cell: ({ row }) => (
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            setSelectedActivity(row.original)
            setIsDetailDialogOpen(true)
          }}
        >
          <Eye className="w-4 h-4" />
        </Button>
      ),
    },
  ]

  // Statistics
  const stats = {
    total: activities.length,
    success: activities.filter((a) => a.status === "success").length,
    failed: activities.filter((a) => a.status === "failed").length,
    today: activities.filter((a) => {
      const today = new Date().toDateString()
      return new Date(a.created_at).toDateString() === today
    }).length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Activity className="w-7 h-7 text-blue-500" />
            سجل الأنشطة
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            متابعة جميع الأنشطة والعمليات في النظام
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button variant="outline" size="sm" onClick={loadActivities}>
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Activity className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي الأنشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.success}</p>
              <p className="text-sm text-muted-foreground">ناجحة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.failed}</p>
              <p className="text-sm text-muted-foreground">فاشلة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.today}</p>
              <p className="text-sm text-muted-foreground">اليوم</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="بحث في السجل..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            <Select value={moduleFilter} onValueChange={setModuleFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الوحدة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الوحدات</SelectItem>
                <SelectItem value="auth">المصادقة</SelectItem>
                <SelectItem value="companies">الشركات</SelectItem>
                <SelectItem value="inventory">المخزون</SelectItem>
                <SelectItem value="contacts">جهات الاتصال</SelectItem>
                <SelectItem value="reports">التقارير</SelectItem>
              </SelectContent>
            </Select>
            <Select value={actionFilter} onValueChange={setActionFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الإجراء" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الإجراءات</SelectItem>
                <SelectItem value="LOGIN">تسجيل دخول</SelectItem>
                <SelectItem value="CREATE">إنشاء</SelectItem>
                <SelectItem value="UPDATE">تحديث</SelectItem>
                <SelectItem value="DELETE">حذف</SelectItem>
                <SelectItem value="EXPORT">تصدير</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الحالة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="success">ناجح</SelectItem>
                <SelectItem value="failed">فاشل</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Activities Table */}
      <Card>
        <CardHeader>
          <CardTitle>سجل الأنشطة ({filteredActivities.length})</CardTitle>
          <CardDescription>جميع الأنشطة والعمليات المسجلة في النظام</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={filteredActivities}
            isLoading={isLoading}
            searchKey="description"
            defaultPageSize={15}
          />
        </CardContent>
      </Card>

      {/* Activity Detail Dialog */}
      <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>تفاصيل النشاط</DialogTitle>
            <DialogDescription>
              معلومات تفصيلية عن النشاط المحدد
            </DialogDescription>
          </DialogHeader>
          {selectedActivity && (
            <div className="space-y-4">
              {/* Activity Header */}
              <div className="flex items-center gap-4">
                {(() => {
                  const config = actionConfig[selectedActivity.action] || actionConfig.UPDATE
                  const Icon = config.icon
                  return (
                    <div className={`w-12 h-12 rounded-lg ${config.bg} flex items-center justify-center`}>
                      <Icon className={`w-6 h-6 ${config.color}`} />
                    </div>
                  )
                })()}
                <div className="flex-1">
                  <h3 className="text-lg font-semibold">{selectedActivity.action_ar}</h3>
                  <p className="text-muted-foreground">{selectedActivity.description}</p>
                </div>
                <Badge variant={selectedActivity.status === "success" ? "default" : "destructive"}>
                  {selectedActivity.status === "success" ? "ناجح" : "فاشل"}
                </Badge>
              </div>

              <Separator />

              {/* User Info */}
              <div>
                <h4 className="font-medium mb-2 flex items-center gap-2">
                  <User className="w-4 h-4" />
                  معلومات المستخدم
                </h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">الاسم</p>
                    <p className="font-medium">{selectedActivity.user_name}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">البريد الإلكتروني</p>
                    <p className="font-medium">{selectedActivity.user_email}</p>
                  </div>
                </div>
              </div>

              <Separator />

              {/* Device Info */}
              <div>
                <h4 className="font-medium mb-2 flex items-center gap-2">
                  <Monitor className="w-4 h-4" />
                  معلومات الجهاز
                </h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">نوع الجهاز</p>
                    <p className="font-medium">{selectedActivity.device}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">المتصفح</p>
                    <p className="font-medium">{selectedActivity.browser}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">نظام التشغيل</p>
                    <p className="font-medium">{selectedActivity.os}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">عنوان IP</p>
                    <p className="font-medium font-mono">{selectedActivity.ip_address}</p>
                  </div>
                  <div className="col-span-2">
                    <p className="text-muted-foreground">الموقع</p>
                    <p className="font-medium">{selectedActivity.location}</p>
                  </div>
                </div>
              </div>

              <Separator />

              {/* Metadata */}
              {selectedActivity.metadata && Object.keys(selectedActivity.metadata).length > 0 && (
                <div>
                  <h4 className="font-medium mb-2 flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    بيانات إضافية
                  </h4>
                  <ScrollArea className="h-[100px]">
                    <pre className="text-sm bg-muted p-3 rounded-lg overflow-x-auto">
                      {JSON.stringify(selectedActivity.metadata, null, 2)}
                    </pre>
                  </ScrollArea>
                </div>
              )}

              {/* Timestamp */}
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="w-4 h-4" />
                <span>التاريخ والوقت: {formatDate(selectedActivity.created_at, "PPPPpppp")}</span>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default ActivityLogPage
