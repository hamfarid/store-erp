/**
 * Admin Dashboard Page - لوحة تحكم المدير
 * Gaara ERP v12
 *
 * System administration dashboard with monitoring and quick actions.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  LayoutDashboard,
  Users,
  Building2,
  Shield,
  Server,
  Database,
  Activity,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Clock,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Settings,
  FileText,
  Bell,
  HardDrive,
  Cpu,
  MemoryStick,
  Wifi,
  Lock,
  Unlock,
  UserPlus,
  UserMinus,
  Eye,
  Calendar,
  BarChart3,
  PieChart,
  ArrowUpRight,
  ArrowDownRight,
  Zap,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"

// Mock data
const systemStats = {
  cpu: { usage: 45, cores: 8, temp: 52 },
  memory: { used: 12.5, total: 32, percentage: 39 },
  disk: { used: 450, total: 1000, percentage: 45 },
  network: { in: 125, out: 85, connections: 1250 },
}

const userStats = {
  totalUsers: 1250,
  activeUsers: 342,
  newToday: 15,
  onlineNow: 89,
  admins: 5,
  managers: 25,
}

const tenantStats = {
  totalTenants: 45,
  activeTenants: 42,
  trialTenants: 8,
  suspendedTenants: 3,
}

const recentActivities = [
  { id: 1, user: "أحمد محمد", action: "تسجيل دخول", time: "منذ 5 دقائق", type: "login", status: "success" },
  { id: 2, user: "سارة علي", action: "تحديث إعدادات النظام", time: "منذ 15 دقيقة", type: "settings", status: "success" },
  { id: 3, user: "خالد سعيد", action: "محاولة دخول فاشلة", time: "منذ 30 دقيقة", type: "security", status: "warning" },
  { id: 4, user: "مريم أحمد", action: "إضافة مستخدم جديد", time: "منذ ساعة", type: "user", status: "success" },
  { id: 5, user: "النظام", action: "نسخ احتياطي تلقائي", time: "منذ ساعتين", type: "backup", status: "success" },
  { id: 6, user: "النظام", action: "تحديث الأمان", time: "منذ 3 ساعات", type: "security", status: "info" },
]

const alerts = [
  { id: 1, title: "استخدام CPU مرتفع", message: "وصل استخدام المعالج إلى 85% على الخادم الرئيسي", severity: "warning", time: "منذ 10 دقائق" },
  { id: 2, title: "فشل النسخ الاحتياطي", message: "فشل النسخ الاحتياطي لقاعدة البيانات الثانوية", severity: "error", time: "منذ ساعة" },
  { id: 3, title: "تحديث متاح", message: "يتوفر تحديث جديد للنظام v12.1.0", severity: "info", time: "منذ يوم" },
]

const quickActions = [
  { id: 1, label: "إضافة مستخدم", icon: UserPlus, action: () => toast.info("جاري فتح نموذج إضافة مستخدم...") },
  { id: 2, label: "إدارة الأدوار", icon: Shield, action: () => toast.info("جاري فتح إدارة الأدوار...") },
  { id: 3, label: "نسخ احتياطي", icon: Database, action: () => toast.info("جاري بدء النسخ الاحتياطي...") },
  { id: 4, label: "سجل النظام", icon: FileText, action: () => toast.info("جاري فتح سجل النظام...") },
  { id: 5, label: "إعدادات الأمان", icon: Lock, action: () => toast.info("جاري فتح إعدادات الأمان...") },
  { id: 6, label: "الإشعارات", icon: Bell, action: () => toast.info("جاري فتح الإشعارات...") },
]

const AdminDashboardPage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      setLastUpdate(new Date())
      setIsLoading(false)
      toast.success("تم تحديث البيانات")
    }, 1000)
  }

  // Get severity color
  const getSeverityColor = (severity) => {
    switch (severity) {
      case "error": return "bg-red-100 text-red-700 border-red-200"
      case "warning": return "bg-yellow-100 text-yellow-700 border-yellow-200"
      case "info": return "bg-blue-100 text-blue-700 border-blue-200"
      default: return "bg-gray-100 text-gray-700 border-gray-200"
    }
  }

  const getActivityIcon = (type) => {
    switch (type) {
      case "login": return Users
      case "settings": return Settings
      case "security": return Shield
      case "user": return UserPlus
      case "backup": return Database
      default: return Activity
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <LayoutDashboard className="w-7 h-7 text-indigo-500" />
            لوحة تحكم المدير
          </h1>
          <p className="text-slate-600 dark:text-slate-400">مراقبة وإدارة النظام</p>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground">
            آخر تحديث: {lastUpdate.toLocaleTimeString('ar-SA')}
          </span>
          <Button variant="outline" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? 'animate-spin' : ''}`} />
            تحديث
          </Button>
        </div>
      </div>

      {/* System Status Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <Cpu className="w-5 h-5 text-blue-600" />
              </div>
              <Badge variant={systemStats.cpu.usage > 80 ? "destructive" : "secondary"}>
                {systemStats.cpu.usage}%
              </Badge>
            </div>
            <h3 className="font-medium mb-1">المعالج (CPU)</h3>
            <Progress value={systemStats.cpu.usage} className={`h-2 ${systemStats.cpu.usage > 80 ? '[&>div]:bg-red-500' : ''}`} />
            <p className="text-xs text-muted-foreground mt-2">{systemStats.cpu.cores} أنوية • {systemStats.cpu.temp}°C</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                <MemoryStick className="w-5 h-5 text-purple-600" />
              </div>
              <Badge variant="secondary">{systemStats.memory.percentage}%</Badge>
            </div>
            <h3 className="font-medium mb-1">الذاكرة (RAM)</h3>
            <Progress value={systemStats.memory.percentage} className="h-2" />
            <p className="text-xs text-muted-foreground mt-2">{systemStats.memory.used} / {systemStats.memory.total} GB</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
                <HardDrive className="w-5 h-5 text-amber-600" />
              </div>
              <Badge variant="secondary">{systemStats.disk.percentage}%</Badge>
            </div>
            <h3 className="font-medium mb-1">التخزين</h3>
            <Progress value={systemStats.disk.percentage} className="h-2" />
            <p className="text-xs text-muted-foreground mt-2">{systemStats.disk.used} / {systemStats.disk.total} GB</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                <Wifi className="w-5 h-5 text-green-600" />
              </div>
              <Badge variant="default" className="bg-green-500">متصل</Badge>
            </div>
            <h3 className="font-medium mb-1">الشبكة</h3>
            <div className="flex gap-4 text-sm">
              <span className="text-green-600">↓ {systemStats.network.in} MB/s</span>
              <span className="text-blue-600">↑ {systemStats.network.out} MB/s</span>
            </div>
            <p className="text-xs text-muted-foreground mt-2">{systemStats.network.connections} اتصال نشط</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - Stats */}
        <div className="lg:col-span-2 space-y-6">
          {/* User & Tenant Stats */}
          <div className="grid md:grid-cols-2 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  إحصائيات المستخدمين
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <p className="text-2xl font-bold text-primary">{userStats.totalUsers}</p>
                    <p className="text-xs text-muted-foreground">إجمالي المستخدمين</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-green-50">
                    <p className="text-2xl font-bold text-green-600">{userStats.onlineNow}</p>
                    <p className="text-xs text-muted-foreground">متصل الآن</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-blue-50">
                    <p className="text-2xl font-bold text-blue-600">{userStats.activeUsers}</p>
                    <p className="text-xs text-muted-foreground">نشط اليوم</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-purple-50">
                    <p className="text-2xl font-bold text-purple-600">+{userStats.newToday}</p>
                    <p className="text-xs text-muted-foreground">جديد اليوم</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Building2 className="w-5 h-5" />
                  إحصائيات المستأجرين
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <p className="text-2xl font-bold text-primary">{tenantStats.totalTenants}</p>
                    <p className="text-xs text-muted-foreground">إجمالي المستأجرين</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-green-50">
                    <p className="text-2xl font-bold text-green-600">{tenantStats.activeTenants}</p>
                    <p className="text-xs text-muted-foreground">نشط</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-amber-50">
                    <p className="text-2xl font-bold text-amber-600">{tenantStats.trialTenants}</p>
                    <p className="text-xs text-muted-foreground">تجريبي</p>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-red-50">
                    <p className="text-2xl font-bold text-red-600">{tenantStats.suspendedTenants}</p>
                    <p className="text-xs text-muted-foreground">معلق</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activities */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                النشاط الأخير
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[300px]">
                <div className="space-y-3">
                  {recentActivities.map((activity) => {
                    const Icon = getActivityIcon(activity.type)
                    return (
                      <div key={activity.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          activity.status === "success" ? "bg-green-100" :
                          activity.status === "warning" ? "bg-yellow-100" : "bg-blue-100"
                        }`}>
                          <Icon className={`w-5 h-5 ${
                            activity.status === "success" ? "text-green-600" :
                            activity.status === "warning" ? "text-yellow-600" : "text-blue-600"
                          }`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="font-medium truncate">{activity.action}</p>
                          <p className="text-sm text-muted-foreground">{activity.user}</p>
                        </div>
                        <span className="text-xs text-muted-foreground whitespace-nowrap">{activity.time}</span>
                      </div>
                    )
                  })}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Alerts & Actions */}
        <div className="space-y-6">
          {/* System Alerts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                تنبيهات النظام
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div key={alert.id} className={`p-3 rounded-lg border ${getSeverityColor(alert.severity)}`}>
                    <div className="flex items-start justify-between">
                      <h4 className="font-medium">{alert.title}</h4>
                      <span className="text-xs">{alert.time}</span>
                    </div>
                    <p className="text-sm mt-1 opacity-80">{alert.message}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="w-5 h-5" />
                إجراءات سريعة
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2">
                {quickActions.map((action) => (
                  <Button
                    key={action.id}
                    variant="outline"
                    className="h-auto py-3 flex-col gap-1"
                    onClick={action.action}
                  >
                    <action.icon className="w-5 h-5" />
                    <span className="text-xs">{action.label}</span>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* System Info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="w-5 h-5" />
                معلومات النظام
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">إصدار النظام</span>
                  <span className="font-medium">v12.0.0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">وقت التشغيل</span>
                  <span className="font-medium">15 يوم، 4 ساعات</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">آخر نسخ احتياطي</span>
                  <span className="font-medium">منذ 6 ساعات</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">حالة الخدمات</span>
                  <Badge variant="default" className="bg-green-500">جميعها تعمل</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboardPage
