/**
 * Audit Logs Page - سجل التدقيق
 * Gaara ERP v12
 *
 * Audit trail viewer with user activity tracking.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  ClipboardList,
  Search,
  Filter,
  RefreshCw,
  Download,
  Eye,
  Calendar,
  Clock,
  User,
  FileText,
  Edit,
  Trash2,
  Plus,
  Shield,
  Key,
  Settings,
  LogIn,
  LogOut,
  ChevronDown,
  ChevronUp,
  MoreVertical,
  Database,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
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
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ViewDialog } from "@/components/dialogs"

// Action configurations
const actionConfig = {
  create: { label: "إنشاء", color: "bg-green-100 text-green-700", icon: Plus },
  update: { label: "تحديث", color: "bg-blue-100 text-blue-700", icon: Edit },
  delete: { label: "حذف", color: "bg-red-100 text-red-700", icon: Trash2 },
  login: { label: "تسجيل دخول", color: "bg-purple-100 text-purple-700", icon: LogIn },
  logout: { label: "تسجيل خروج", color: "bg-gray-100 text-gray-700", icon: LogOut },
  export: { label: "تصدير", color: "bg-amber-100 text-amber-700", icon: Download },
  settings: { label: "إعدادات", color: "bg-indigo-100 text-indigo-700", icon: Settings },
  permission: { label: "صلاحيات", color: "bg-pink-100 text-pink-700", icon: Shield },
}

const moduleConfig = {
  users: { label: "المستخدمين", icon: User },
  sales: { label: "المبيعات", icon: FileText },
  inventory: { label: "المخزون", icon: Database },
  settings: { label: "الإعدادات", icon: Settings },
  auth: { label: "المصادقة", icon: Key },
  system: { label: "النظام", icon: Globe },
}

// Mock audit data
const mockAuditLogs = [
  {
    id: 1,
    timestamp: "2026-01-17 14:35:22",
    user: { name: "أحمد محمد", email: "ahmed@company.com", avatar: "AM" },
    action: "update",
    module: "sales",
    entity: "Invoice",
    entity_id: "INV-2026-0125",
    description: "تحديث فاتورة المبيعات",
    ip_address: "192.168.1.50",
    user_agent: "Chrome/120.0 Windows 10",
    changes: [
      { field: "status", old_value: "draft", new_value: "confirmed" },
      { field: "total", old_value: "5000", new_value: "5500" },
    ],
  },
  {
    id: 2,
    timestamp: "2026-01-17 14:30:15",
    user: { name: "سارة علي", email: "sara@company.com", avatar: "SA" },
    action: "create",
    module: "users",
    entity: "User",
    entity_id: "USR-0050",
    description: "إضافة مستخدم جديد",
    ip_address: "192.168.1.55",
    user_agent: "Firefox/121.0 Mac OS",
    changes: null,
  },
  {
    id: 3,
    timestamp: "2026-01-17 14:25:00",
    user: { name: "خالد سعيد", email: "khalid@company.com", avatar: "KS" },
    action: "login",
    module: "auth",
    entity: "Session",
    entity_id: "SES-12345",
    description: "تسجيل دخول ناجح",
    ip_address: "192.168.1.60",
    user_agent: "Safari/17.0 iOS",
    changes: null,
  },
  {
    id: 4,
    timestamp: "2026-01-17 14:20:00",
    user: { name: "مريم أحمد", email: "maryam@company.com", avatar: "MA" },
    action: "delete",
    module: "inventory",
    entity: "Product",
    entity_id: "PRD-0089",
    description: "حذف منتج من المخزون",
    ip_address: "192.168.1.70",
    user_agent: "Chrome/120.0 Windows 11",
    changes: [
      { field: "name", old_value: "منتج قديم", new_value: null },
    ],
  },
  {
    id: 5,
    timestamp: "2026-01-17 14:15:00",
    user: { name: "النظام", email: "system", avatar: "SY" },
    action: "settings",
    module: "system",
    entity: "Configuration",
    entity_id: "CFG-001",
    description: "تحديث إعدادات النظام",
    ip_address: "localhost",
    user_agent: "System Scheduler",
    changes: [
      { field: "backup_enabled", old_value: "false", new_value: "true" },
    ],
  },
  {
    id: 6,
    timestamp: "2026-01-17 14:10:00",
    user: { name: "أحمد محمد", email: "ahmed@company.com", avatar: "AM" },
    action: "export",
    module: "sales",
    entity: "Report",
    entity_id: "RPT-0025",
    description: "تصدير تقرير المبيعات الشهري",
    ip_address: "192.168.1.50",
    user_agent: "Chrome/120.0 Windows 10",
    changes: null,
  },
  {
    id: 7,
    timestamp: "2026-01-17 14:00:00",
    user: { name: "المدير", email: "admin@company.com", avatar: "AD" },
    action: "permission",
    module: "users",
    entity: "Role",
    entity_id: "ROL-003",
    description: "تحديث صلاحيات دور المحاسب",
    ip_address: "192.168.1.10",
    user_agent: "Chrome/120.0 Windows 10",
    changes: [
      { field: "can_delete_invoices", old_value: "false", new_value: "true" },
      { field: "can_export_reports", old_value: "false", new_value: "true" },
    ],
  },
]

const AuditLogsPage = () => {
  // State
  const [logs, setLogs] = useState(mockAuditLogs)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [actionFilter, setActionFilter] = useState("all")
  const [moduleFilter, setModuleFilter] = useState("all")
  const [dateFilter, setDateFilter] = useState("today")
  const [expandedLog, setExpandedLog] = useState(null)

  // Dialog states
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [selectedLog, setSelectedLog] = useState(null)

  // Filter logs
  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.description.includes(searchQuery) || 
                         log.user.name.includes(searchQuery) ||
                         log.entity_id?.includes(searchQuery)
    const matchesAction = actionFilter === "all" || log.action === actionFilter
    const matchesModule = moduleFilter === "all" || log.module === moduleFilter
    return matchesSearch && matchesAction && matchesModule
  })

  // Statistics
  const stats = {
    total: logs.length,
    creates: logs.filter(l => l.action === "create").length,
    updates: logs.filter(l => l.action === "update").length,
    deletes: logs.filter(l => l.action === "delete").length,
    logins: logs.filter(l => l.action === "login").length,
  }

  // Handlers
  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
      toast.success("تم تحديث السجلات")
    }, 1000)
  }

  const handleExport = () => {
    const dataStr = JSON.stringify(filteredLogs, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    const exportFileDefaultName = `audit-logs-${new Date().toISOString().split('T')[0]}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
    toast.success("تم تصدير السجلات")
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <ClipboardList className="w-7 h-7 text-indigo-500" />
            سجل التدقيق
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تتبع جميع التغييرات والأنشطة في النظام</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button variant="outline" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? 'animate-spin' : ''}`} />
            تحديث
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center">
              <ClipboardList className="w-5 h-5 text-slate-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.total}</p>
              <p className="text-xs text-muted-foreground">إجمالي السجلات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <Plus className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.creates}</p>
              <p className="text-xs text-muted-foreground">إنشاء</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Edit className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.updates}</p>
              <p className="text-xs text-muted-foreground">تحديث</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <Trash2 className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.deletes}</p>
              <p className="text-xs text-muted-foreground">حذف</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <LogIn className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.logins}</p>
              <p className="text-xs text-muted-foreground">تسجيل دخول</p>
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
                placeholder="بحث في السجلات..." 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)} 
                className="pr-10" 
              />
            </div>
            <Select value={actionFilter} onValueChange={setActionFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الإجراء" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الإجراءات</SelectItem>
                <SelectItem value="create">إنشاء</SelectItem>
                <SelectItem value="update">تحديث</SelectItem>
                <SelectItem value="delete">حذف</SelectItem>
                <SelectItem value="login">تسجيل دخول</SelectItem>
                <SelectItem value="logout">تسجيل خروج</SelectItem>
                <SelectItem value="export">تصدير</SelectItem>
              </SelectContent>
            </Select>
            <Select value={moduleFilter} onValueChange={setModuleFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الوحدة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الوحدات</SelectItem>
                <SelectItem value="users">المستخدمين</SelectItem>
                <SelectItem value="sales">المبيعات</SelectItem>
                <SelectItem value="inventory">المخزون</SelectItem>
                <SelectItem value="settings">الإعدادات</SelectItem>
                <SelectItem value="auth">المصادقة</SelectItem>
              </SelectContent>
            </Select>
            <Select value={dateFilter} onValueChange={setDateFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="الفترة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="today">اليوم</SelectItem>
                <SelectItem value="week">هذا الأسبوع</SelectItem>
                <SelectItem value="month">هذا الشهر</SelectItem>
                <SelectItem value="all">الكل</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Audit Logs List */}
      <Card>
        <CardHeader>
          <CardTitle>سجلات التدقيق ({filteredLogs.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[600px]">
            <div className="space-y-3">
              {filteredLogs.map((log) => {
                const actionConf = actionConfig[log.action]
                const moduleConf = moduleConfig[log.module]
                const ActionIcon = actionConf?.icon || Edit
                const ModuleIcon = moduleConf?.icon || Globe
                const isExpanded = expandedLog === log.id

                return (
                  <div key={log.id} className="border rounded-lg p-4">
                    <div className="flex items-start gap-4">
                      <Avatar>
                        <AvatarFallback className="bg-primary/10 text-primary">
                          {log.user.avatar}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium">{log.user.name}</span>
                          <Badge className={actionConf?.color}>
                            <ActionIcon className="w-3 h-3 ml-1" />
                            {actionConf?.label}
                          </Badge>
                          <Badge variant="outline" className="flex items-center gap-1">
                            <ModuleIcon className="w-3 h-3" />
                            {moduleConf?.label}
                          </Badge>
                        </div>
                        <p className="text-sm">{log.description}</p>
                        <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {log.timestamp}
                          </span>
                          <span className="font-mono">{log.entity_id}</span>
                          <span>IP: {log.ip_address}</span>
                        </div>
                        
                        {/* Changes Section */}
                        {isExpanded && log.changes && log.changes.length > 0 && (
                          <div className="mt-3 p-3 rounded-lg bg-muted">
                            <p className="text-xs font-medium mb-2">التغييرات:</p>
                            <div className="space-y-1">
                              {log.changes.map((change, idx) => (
                                <div key={idx} className="flex items-center gap-2 text-xs">
                                  <span className="font-medium">{change.field}:</span>
                                  <span className="text-red-500 line-through">{change.old_value || "—"}</span>
                                  <span>→</span>
                                  <span className="text-green-600">{change.new_value || "—"}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {isExpanded && (
                          <div className="mt-2 text-xs text-muted-foreground">
                            <span>المتصفح: {log.user_agent}</span>
                          </div>
                        )}
                      </div>
                      <div className="flex items-center gap-1">
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => setExpandedLog(isExpanded ? null : log.id)}
                        >
                          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </Button>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => { setSelectedLog(log); setIsViewDialogOpen(true); }}>
                              <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </div>
                  </div>
                )
              })}
              {filteredLogs.length === 0 && (
                <div className="text-center py-10 text-muted-foreground">
                  <ClipboardList className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>لا توجد سجلات</p>
                </div>
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedLog(null); }}
        title="تفاصيل السجل"
        subtitle={selectedLog?.timestamp}
        size="lg"
      >
        {selectedLog && (
          <div className="space-y-4">
            <ViewDialog.Section title="المستخدم">
              <ViewDialog.Row label="الاسم" value={selectedLog.user.name} />
              <ViewDialog.Row label="البريد الإلكتروني" value={selectedLog.user.email} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الإجراء">
              <ViewDialog.Row label="النوع" value={actionConfig[selectedLog.action]?.label} />
              <ViewDialog.Row label="الوحدة" value={moduleConfig[selectedLog.module]?.label} />
              <ViewDialog.Row label="الكيان" value={`${selectedLog.entity} (${selectedLog.entity_id})`} />
              <ViewDialog.Row label="الوصف" value={selectedLog.description} />
            </ViewDialog.Section>
            {selectedLog.changes && selectedLog.changes.length > 0 && (
              <ViewDialog.Section title="التغييرات">
                {selectedLog.changes.map((change, idx) => (
                  <ViewDialog.Row 
                    key={idx} 
                    label={change.field} 
                    value={`${change.old_value || "—"} → ${change.new_value || "—"}`}
                  />
                ))}
              </ViewDialog.Section>
            )}
            <ViewDialog.Section title="معلومات تقنية">
              <ViewDialog.Row label="عنوان IP" value={selectedLog.ip_address} />
              <ViewDialog.Row label="المتصفح" value={selectedLog.user_agent} />
              <ViewDialog.Row label="التوقيت" value={selectedLog.timestamp} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>
    </div>
  )
}

export default AuditLogsPage
