/**
 * System Logs Page - سجلات النظام
 * Gaara ERP v12
 *
 * System logs viewer with filtering and search capabilities.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  FileText,
  Search,
  Filter,
  RefreshCw,
  Download,
  Trash2,
  Eye,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Info,
  Bug,
  Server,
  Database,
  Shield,
  Users,
  Calendar,
  Clock,
  MoreVertical,
  ChevronDown,
  ChevronUp,
  Copy,
  ExternalLink,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
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
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Checkbox } from "@/components/ui/checkbox"
import { ConfirmDialog, ViewDialog } from "@/components/dialogs"

// Log level configurations
const logLevelConfig = {
  error: { label: "خطأ", color: "bg-red-100 text-red-700 border-red-200", icon: XCircle },
  warning: { label: "تحذير", color: "bg-yellow-100 text-yellow-700 border-yellow-200", icon: AlertTriangle },
  info: { label: "معلومات", color: "bg-blue-100 text-blue-700 border-blue-200", icon: Info },
  debug: { label: "تصحيح", color: "bg-gray-100 text-gray-700 border-gray-200", icon: Bug },
  success: { label: "نجاح", color: "bg-green-100 text-green-700 border-green-200", icon: CheckCircle2 },
}

const sourceConfig = {
  api: { label: "API", icon: Server },
  database: { label: "قاعدة البيانات", icon: Database },
  auth: { label: "المصادقة", icon: Shield },
  user: { label: "المستخدم", icon: Users },
  system: { label: "النظام", icon: Server },
}

// Mock logs data
const mockLogs = [
  {
    id: 1,
    timestamp: "2026-01-17 14:35:22",
    level: "error",
    source: "api",
    message: "فشل الاتصال بقاعدة البيانات - Connection timeout",
    details: "Connection to database server 'db-prod-01' timed out after 30 seconds. Retrying...",
    user: "system",
    ip: "192.168.1.100",
    request_id: "req_abc123",
  },
  {
    id: 2,
    timestamp: "2026-01-17 14:34:15",
    level: "warning",
    source: "auth",
    message: "محاولة تسجيل دخول فاشلة متعددة للمستخدم admin@example.com",
    details: "5 failed login attempts detected in the last 10 minutes",
    user: "admin@example.com",
    ip: "203.0.113.42",
    request_id: "req_def456",
  },
  {
    id: 3,
    timestamp: "2026-01-17 14:33:00",
    level: "info",
    source: "user",
    message: "تم تسجيل دخول المستخدم ahmed@company.com",
    details: "User logged in successfully via web interface",
    user: "ahmed@company.com",
    ip: "192.168.1.50",
    request_id: "req_ghi789",
  },
  {
    id: 4,
    timestamp: "2026-01-17 14:30:45",
    level: "success",
    source: "database",
    message: "تم إنشاء نسخة احتياطية بنجاح",
    details: "Database backup completed. Size: 2.5GB, Duration: 5m 32s",
    user: "system",
    ip: "localhost",
    request_id: "req_jkl012",
  },
  {
    id: 5,
    timestamp: "2026-01-17 14:28:30",
    level: "debug",
    source: "api",
    message: "طلب API: GET /api/v1/users",
    details: "Response time: 125ms, Status: 200, Cache: HIT",
    user: "sara@company.com",
    ip: "192.168.1.55",
    request_id: "req_mno345",
  },
  {
    id: 6,
    timestamp: "2026-01-17 14:25:00",
    level: "error",
    source: "system",
    message: "نفاد مساحة القرص على خادم التخزين",
    details: "Disk usage reached 95% on storage server. Immediate action required.",
    user: "system",
    ip: "localhost",
    request_id: "req_pqr678",
  },
  {
    id: 7,
    timestamp: "2026-01-17 14:20:00",
    level: "info",
    source: "auth",
    message: "تم تحديث صلاحيات المستخدم khalid@company.com",
    details: "Role changed from 'viewer' to 'editor' by admin",
    user: "admin@company.com",
    ip: "192.168.1.10",
    request_id: "req_stu901",
  },
]

const SystemLogsPage = () => {
  // State
  const [logs, setLogs] = useState(mockLogs)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [levelFilter, setLevelFilter] = useState("all")
  const [sourceFilter, setSourceFilter] = useState("all")
  const [selectedLogs, setSelectedLogs] = useState([])
  const [expandedLog, setExpandedLog] = useState(null)
  const [autoRefresh, setAutoRefresh] = useState(false)

  // Dialog states
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedLog, setSelectedLog] = useState(null)

  // Filter logs
  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.includes(searchQuery) || 
                         log.details?.includes(searchQuery) ||
                         log.user?.includes(searchQuery)
    const matchesLevel = levelFilter === "all" || log.level === levelFilter
    const matchesSource = sourceFilter === "all" || log.source === sourceFilter
    return matchesSearch && matchesLevel && matchesSource
  })

  // Statistics
  const stats = {
    total: logs.length,
    errors: logs.filter(l => l.level === "error").length,
    warnings: logs.filter(l => l.level === "warning").length,
    info: logs.filter(l => l.level === "info" || l.level === "success").length,
  }

  // Handlers
  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      // Simulate adding new log
      const newLog = {
        id: Date.now(),
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
        level: "info",
        source: "system",
        message: "تم تحديث السجلات",
        details: "Logs refreshed manually",
        user: "admin",
        ip: "localhost",
        request_id: `req_${Date.now()}`,
      }
      setLogs([newLog, ...logs])
      setIsLoading(false)
      toast.success("تم تحديث السجلات")
    }, 1000)
  }

  const handleExport = () => {
    const dataStr = JSON.stringify(filteredLogs, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    const exportFileDefaultName = `system-logs-${new Date().toISOString().split('T')[0]}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
    toast.success("تم تصدير السجلات")
  }

  const handleClearLogs = () => {
    setLogs([])
    setIsDeleteDialogOpen(false)
    toast.success("تم حذف جميع السجلات")
  }

  const handleCopyLog = (log) => {
    navigator.clipboard.writeText(JSON.stringify(log, null, 2))
    toast.success("تم نسخ السجل")
  }

  const toggleLogSelection = (logId) => {
    setSelectedLogs(prev => 
      prev.includes(logId) 
        ? prev.filter(id => id !== logId)
        : [...prev, logId]
    )
  }

  const toggleAllLogs = () => {
    setSelectedLogs(
      selectedLogs.length === filteredLogs.length 
        ? [] 
        : filteredLogs.map(l => l.id)
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <FileText className="w-7 h-7 text-indigo-500" />
            سجلات النظام
          </h1>
          <p className="text-slate-600 dark:text-slate-400">عرض وتحليل سجلات النظام</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
          <Button variant="outline" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? 'animate-spin' : ''}`} />
            تحديث
          </Button>
          <Button variant="destructive" onClick={() => setIsDeleteDialogOpen(true)}>
            <Trash2 className="w-4 h-4 ml-2" />مسح الكل
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center">
              <FileText className="w-5 h-5 text-slate-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.total}</p>
              <p className="text-xs text-muted-foreground">إجمالي السجلات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.errors}</p>
              <p className="text-xs text-muted-foreground">أخطاء</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.warnings}</p>
              <p className="text-xs text-muted-foreground">تحذيرات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Info className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.info}</p>
              <p className="text-xs text-muted-foreground">معلومات</p>
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
            <Select value={levelFilter} onValueChange={setLevelFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="المستوى" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع المستويات</SelectItem>
                <SelectItem value="error">أخطاء</SelectItem>
                <SelectItem value="warning">تحذيرات</SelectItem>
                <SelectItem value="info">معلومات</SelectItem>
                <SelectItem value="success">نجاح</SelectItem>
                <SelectItem value="debug">تصحيح</SelectItem>
              </SelectContent>
            </Select>
            <Select value={sourceFilter} onValueChange={setSourceFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="المصدر" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع المصادر</SelectItem>
                <SelectItem value="api">API</SelectItem>
                <SelectItem value="database">قاعدة البيانات</SelectItem>
                <SelectItem value="auth">المصادقة</SelectItem>
                <SelectItem value="user">المستخدم</SelectItem>
                <SelectItem value="system">النظام</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Logs List */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>السجلات ({filteredLogs.length})</CardTitle>
          <div className="flex items-center gap-2">
            <Checkbox 
              checked={selectedLogs.length === filteredLogs.length && filteredLogs.length > 0}
              onCheckedChange={toggleAllLogs}
            />
            <span className="text-sm text-muted-foreground">تحديد الكل</span>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[600px]">
            <div className="space-y-2">
              {filteredLogs.map((log) => {
                const levelConf = logLevelConfig[log.level]
                const sourceConf = sourceConfig[log.source]
                const LevelIcon = levelConf?.icon || Info
                const SourceIcon = sourceConf?.icon || Server
                const isExpanded = expandedLog === log.id

                return (
                  <div 
                    key={log.id} 
                    className={`border rounded-lg ${levelConf?.color.replace('text-', 'border-').split(' ')[2]} ${
                      selectedLogs.includes(log.id) ? 'ring-2 ring-primary' : ''
                    }`}
                  >
                    <div className="p-3">
                      <div className="flex items-start gap-3">
                        <Checkbox 
                          checked={selectedLogs.includes(log.id)}
                          onCheckedChange={() => toggleLogSelection(log.id)}
                        />
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${levelConf?.color.split(' ').slice(0, 2).join(' ')}`}>
                          <LevelIcon className="w-4 h-4" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <Badge className={levelConf?.color} variant="outline">{levelConf?.label}</Badge>
                            <Badge variant="outline" className="flex items-center gap-1">
                              <SourceIcon className="w-3 h-3" />
                              {sourceConf?.label}
                            </Badge>
                            <span className="text-xs text-muted-foreground">{log.timestamp}</span>
                          </div>
                          <p className="font-medium">{log.message}</p>
                          {isExpanded && log.details && (
                            <div className="mt-2 p-2 rounded bg-muted text-sm font-mono">
                              {log.details}
                            </div>
                          )}
                          {isExpanded && (
                            <div className="mt-2 flex gap-4 text-xs text-muted-foreground">
                              <span>المستخدم: {log.user}</span>
                              <span>IP: {log.ip}</span>
                              <span>Request ID: {log.request_id}</span>
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
                              <DropdownMenuItem onClick={() => handleCopyLog(log)}>
                                <Copy className="w-4 h-4 ml-2" />نسخ
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
              {filteredLogs.length === 0 && (
                <div className="text-center py-10 text-muted-foreground">
                  <FileText className="w-12 h-12 mx-auto mb-3 opacity-50" />
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
            <ViewDialog.Section title="المعلومات الأساسية">
              <ViewDialog.Row label="المستوى" value={logLevelConfig[selectedLog.level]?.label} />
              <ViewDialog.Row label="المصدر" value={sourceConfig[selectedLog.source]?.label} />
              <ViewDialog.Row label="الوقت" value={selectedLog.timestamp} />
            </ViewDialog.Section>
            <ViewDialog.Section title="الرسالة">
              <p className="text-sm">{selectedLog.message}</p>
            </ViewDialog.Section>
            {selectedLog.details && (
              <ViewDialog.Section title="التفاصيل">
                <pre className="text-sm font-mono p-2 bg-muted rounded whitespace-pre-wrap">
                  {selectedLog.details}
                </pre>
              </ViewDialog.Section>
            )}
            <ViewDialog.Section title="معلومات إضافية">
              <ViewDialog.Row label="المستخدم" value={selectedLog.user} />
              <ViewDialog.Row label="عنوان IP" value={selectedLog.ip} />
              <ViewDialog.Row label="Request ID" value={selectedLog.request_id} />
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="مسح جميع السجلات"
        description="هل أنت متأكد من مسح جميع سجلات النظام؟ لا يمكن التراجع عن هذا الإجراء."
        variant="danger"
        onConfirm={handleClearLogs}
      />
    </div>
  )
}

export default SystemLogsPage
