/**
 * System Health Page - صحة النظام
 * Gaara ERP v12
 *
 * System health monitoring and service status dashboard.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Activity,
  Server,
  Database,
  Globe,
  HardDrive,
  Cpu,
  MemoryStick,
  Wifi,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Clock,
  RefreshCw,
  Download,
  Settings,
  Zap,
  TrendingUp,
  TrendingDown,
  Timer,
  Shield,
  Mail,
  MessageSquare,
  Cloud,
  Bell,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"

// Service status configurations
const statusConfig = {
  healthy: { label: "سليم", color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  degraded: { label: "متدهور", color: "bg-yellow-100 text-yellow-700", icon: AlertTriangle },
  unhealthy: { label: "متعطل", color: "bg-red-100 text-red-700", icon: XCircle },
}

// Mock services data
const mockServices = [
  { id: 1, name: "API Gateway", type: "api", status: "healthy", uptime: "99.99%", responseTime: 45, lastCheck: "منذ 30 ثانية" },
  { id: 2, name: "Database Primary", type: "database", status: "healthy", uptime: "99.95%", responseTime: 12, lastCheck: "منذ 30 ثانية" },
  { id: 3, name: "Database Replica", type: "database", status: "healthy", uptime: "99.90%", responseTime: 15, lastCheck: "منذ 30 ثانية" },
  { id: 4, name: "Redis Cache", type: "cache", status: "healthy", uptime: "99.99%", responseTime: 2, lastCheck: "منذ 30 ثانية" },
  { id: 5, name: "File Storage", type: "storage", status: "degraded", uptime: "98.50%", responseTime: 150, lastCheck: "منذ 30 ثانية" },
  { id: 6, name: "Email Service", type: "email", status: "healthy", uptime: "99.80%", responseTime: 200, lastCheck: "منذ 30 ثانية" },
  { id: 7, name: "SMS Gateway", type: "sms", status: "healthy", uptime: "99.70%", responseTime: 180, lastCheck: "منذ 30 ثانية" },
  { id: 8, name: "Authentication Service", type: "auth", status: "healthy", uptime: "99.99%", responseTime: 25, lastCheck: "منذ 30 ثانية" },
  { id: 9, name: "Background Jobs", type: "jobs", status: "healthy", uptime: "99.95%", responseTime: 0, lastCheck: "منذ 30 ثانية" },
  { id: 10, name: "Notification Service", type: "notification", status: "unhealthy", uptime: "95.00%", responseTime: 0, lastCheck: "منذ 30 ثانية" },
]

const mockMetrics = {
  cpu: [65, 72, 68, 75, 70, 78, 72, 68, 65, 70, 75, 72],
  memory: [45, 48, 52, 55, 50, 48, 52, 55, 58, 55, 52, 50],
  disk: [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51],
  requests: [1200, 1500, 1800, 2200, 2500, 2800, 2400, 2000, 1600, 1400, 1200, 1000],
}

const mockIncidents = [
  { id: 1, title: "خدمة الإشعارات متعطلة", status: "investigating", time: "منذ 15 دقيقة", severity: "high" },
  { id: 2, title: "بطء في خدمة التخزين", status: "monitoring", time: "منذ ساعة", severity: "medium" },
  { id: 3, title: "صيانة مجدولة - قاعدة البيانات", status: "scheduled", time: "غداً 02:00", severity: "info" },
]

const SystemHealthPage = () => {
  const [services, setServices] = useState(mockServices)
  const [isLoading, setIsLoading] = useState(false)
  const [lastRefresh, setLastRefresh] = useState(new Date())
  const [activeTab, setActiveTab] = useState("overview")

  // Calculate stats
  const stats = {
    totalServices: services.length,
    healthyServices: services.filter(s => s.status === "healthy").length,
    degradedServices: services.filter(s => s.status === "degraded").length,
    unhealthyServices: services.filter(s => s.status === "unhealthy").length,
    avgResponseTime: Math.round(services.reduce((sum, s) => sum + s.responseTime, 0) / services.length),
    avgUptime: (services.reduce((sum, s) => sum + parseFloat(s.uptime), 0) / services.length).toFixed(2),
  }

  const overallStatus = stats.unhealthyServices > 0 ? "unhealthy" : stats.degradedServices > 0 ? "degraded" : "healthy"

  // Handlers
  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      setLastRefresh(new Date())
      setIsLoading(false)
      toast.success("تم تحديث حالة النظام")
    }, 1000)
  }

  const handleRestartService = (service) => {
    toast.info(`جاري إعادة تشغيل ${service.name}...`)
    setTimeout(() => {
      setServices(services.map(s => 
        s.id === service.id ? { ...s, status: "healthy" } : s
      ))
      toast.success(`تم إعادة تشغيل ${service.name}`)
    }, 2000)
  }

  const getServiceIcon = (type) => {
    switch (type) {
      case "api": return Globe
      case "database": return Database
      case "cache": return Zap
      case "storage": return HardDrive
      case "email": return Mail
      case "sms": return MessageSquare
      case "auth": return Shield
      case "jobs": return Clock
      case "notification": return Bell
      default: return Server
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Activity className="w-7 h-7 text-emerald-500" />
            صحة النظام
          </h1>
          <p className="text-slate-600 dark:text-slate-400">مراقبة حالة الخدمات والأداء</p>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground">
            آخر تحديث: {lastRefresh.toLocaleTimeString('ar-SA')}
          </span>
          <Button variant="outline" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? 'animate-spin' : ''}`} />
            تحديث
          </Button>
        </div>
      </div>

      {/* Overall Status Banner */}
      <Card className={`border-2 ${
        overallStatus === "healthy" ? "border-green-300 bg-green-50" :
        overallStatus === "degraded" ? "border-yellow-300 bg-yellow-50" :
        "border-red-300 bg-red-50"
      }`}>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
                overallStatus === "healthy" ? "bg-green-100" :
                overallStatus === "degraded" ? "bg-yellow-100" :
                "bg-red-100"
              }`}>
                {overallStatus === "healthy" ? (
                  <CheckCircle2 className="w-8 h-8 text-green-600" />
                ) : overallStatus === "degraded" ? (
                  <AlertTriangle className="w-8 h-8 text-yellow-600" />
                ) : (
                  <XCircle className="w-8 h-8 text-red-600" />
                )}
              </div>
              <div>
                <h2 className={`text-2xl font-bold ${
                  overallStatus === "healthy" ? "text-green-700" :
                  overallStatus === "degraded" ? "text-yellow-700" :
                  "text-red-700"
                }`}>
                  {overallStatus === "healthy" ? "جميع الأنظمة تعمل بشكل سليم" :
                   overallStatus === "degraded" ? "بعض الخدمات تعمل ببطء" :
                   "توجد مشاكل في بعض الخدمات"}
                </h2>
                <p className="text-muted-foreground">
                  {stats.healthyServices} من {stats.totalServices} خدمة تعمل بشكل طبيعي
                </p>
              </div>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-primary">{stats.avgUptime}%</p>
              <p className="text-sm text-muted-foreground">متوسط وقت التشغيل</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-xl font-bold text-green-600">{stats.healthyServices}</p>
              <p className="text-xs text-muted-foreground">خدمات سليمة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
            </div>
            <div>
              <p className="text-xl font-bold text-yellow-600">{stats.degradedServices}</p>
              <p className="text-xs text-muted-foreground">خدمات بطيئة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <p className="text-xl font-bold text-red-600">{stats.unhealthyServices}</p>
              <p className="text-xs text-muted-foreground">خدمات متعطلة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Timer className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.avgResponseTime}ms</p>
              <p className="text-xs text-muted-foreground">متوسط الاستجابة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
          <TabsTrigger value="services">الخدمات</TabsTrigger>
          <TabsTrigger value="incidents">الحوادث</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid lg:grid-cols-2 gap-6">
            {/* System Resources */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Server className="w-5 h-5" />
                  موارد النظام
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="flex items-center gap-2">
                      <Cpu className="w-4 h-4" />المعالج (CPU)
                    </span>
                    <span className="font-medium">72%</span>
                  </div>
                  <Progress value={72} className="h-3" />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="flex items-center gap-2">
                      <MemoryStick className="w-4 h-4" />الذاكرة (RAM)
                    </span>
                    <span className="font-medium">55%</span>
                  </div>
                  <Progress value={55} className="h-3" />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="flex items-center gap-2">
                      <HardDrive className="w-4 h-4" />التخزين
                    </span>
                    <span className="font-medium">51%</span>
                  </div>
                  <Progress value={51} className="h-3" />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="flex items-center gap-2">
                      <Wifi className="w-4 h-4" />عرض النطاق
                    </span>
                    <span className="font-medium">35%</span>
                  </div>
                  <Progress value={35} className="h-3" />
                </div>
              </CardContent>
            </Card>

            {/* Active Incidents */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5" />
                  الحوادث النشطة
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {mockIncidents.map((incident) => (
                    <div 
                      key={incident.id} 
                      className={`p-3 rounded-lg border ${
                        incident.severity === "high" ? "border-red-200 bg-red-50" :
                        incident.severity === "medium" ? "border-yellow-200 bg-yellow-50" :
                        "border-blue-200 bg-blue-50"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-medium">{incident.title}</h4>
                          <p className="text-sm text-muted-foreground">{incident.time}</p>
                        </div>
                        <Badge variant="outline">{
                          incident.status === "investigating" ? "قيد التحقيق" :
                          incident.status === "monitoring" ? "مراقبة" :
                          "مجدول"
                        }</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Services Tab */}
        <TabsContent value="services">
          <Card>
            <CardHeader>
              <CardTitle>حالة الخدمات</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {services.map((service) => {
                  const Icon = getServiceIcon(service.type)
                  const config = statusConfig[service.status]
                  const StatusIcon = config.icon
                  return (
                    <div key={service.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${config.color.split(' ')[0]}`}>
                          <Icon className={`w-5 h-5 ${config.color.split(' ')[1]}`} />
                        </div>
                        <div>
                          <p className="font-medium">{service.name}</p>
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <span>وقت التشغيل: {service.uptime}</span>
                            <span>•</span>
                            <span>الاستجابة: {service.responseTime}ms</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={config.color}>
                          <StatusIcon className="w-3 h-3 ml-1" />
                          {config.label}
                        </Badge>
                        {service.status !== "healthy" && (
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => handleRestartService(service)}
                          >
                            إعادة تشغيل
                          </Button>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Incidents Tab */}
        <TabsContent value="incidents">
          <Card>
            <CardHeader>
              <CardTitle>سجل الحوادث</CardTitle>
              <CardDescription>جميع الحوادث والأعطال السابقة والحالية</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockIncidents.map((incident) => (
                  <div key={incident.id} className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{incident.title}</h4>
                      <Badge variant={
                        incident.severity === "high" ? "destructive" :
                        incident.severity === "medium" ? "default" :
                        "secondary"
                      }>
                        {incident.severity === "high" ? "عالي" :
                         incident.severity === "medium" ? "متوسط" :
                         "معلومات"}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {incident.time}
                      </span>
                      <span>الحالة: {
                        incident.status === "investigating" ? "قيد التحقيق" :
                        incident.status === "monitoring" ? "مراقبة" :
                        "مجدول"
                      }</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default SystemHealthPage
