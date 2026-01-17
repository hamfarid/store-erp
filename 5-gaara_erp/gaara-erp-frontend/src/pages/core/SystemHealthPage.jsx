/**
 * System Health Page - صحة النظام
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Activity,
  Server,
  Database,
  HardDrive,
  Cpu,
  MemoryStick,
  Wifi,
  Clock,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  RefreshCw,
  TrendingUp,
  TrendingDown,
  Zap,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"

const SystemHealthPage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(new Date())
  
  // System metrics
  const [metrics, setMetrics] = useState({
    cpu: { usage: 45, cores: 8, temperature: 52 },
    memory: { used: 12.5, total: 32, percentage: 39 },
    disk: { used: 450, total: 1000, percentage: 45 },
    network: { upload: 25, download: 150, latency: 12 },
  })

  // Services status
  const [services, setServices] = useState([
    { name: "خادم الويب", name_en: "Web Server", status: "healthy", uptime: "15 يوم", responseTime: 45 },
    { name: "قاعدة البيانات", name_en: "Database", status: "healthy", uptime: "15 يوم", responseTime: 12 },
    { name: "خادم الملفات", name_en: "File Server", status: "healthy", uptime: "15 يوم", responseTime: 8 },
    { name: "خدمة البريد", name_en: "Email Service", status: "healthy", uptime: "15 يوم", responseTime: 120 },
    { name: "خدمة الكاش", name_en: "Cache Service", status: "healthy", uptime: "10 يوم", responseTime: 3 },
    { name: "خدمة البحث", name_en: "Search Service", status: "warning", uptime: "5 يوم", responseTime: 250 },
    { name: "خدمة الذكاء الاصطناعي", name_en: "AI Service", status: "healthy", uptime: "7 يوم", responseTime: 450 },
    { name: "خدمة الإشعارات", name_en: "Notification Service", status: "healthy", uptime: "15 يوم", responseTime: 15 },
  ])

  // Recent alerts
  const [alerts, setAlerts] = useState([
    { id: 1, type: "warning", message: "استخدام ذاكرة عالي في خدمة البحث", time: "منذ 5 دقائق" },
    { id: 2, type: "info", message: "تم تحديث قاعدة البيانات بنجاح", time: "منذ 30 دقيقة" },
    { id: 3, type: "success", message: "تم استعادة خدمة الكاش", time: "منذ ساعة" },
  ])

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setMetrics(prev => ({
        cpu: { ...prev.cpu, usage: Math.min(100, Math.max(20, prev.cpu.usage + (Math.random() - 0.5) * 10)) },
        memory: { ...prev.memory, percentage: Math.min(100, Math.max(20, prev.memory.percentage + (Math.random() - 0.5) * 5)) },
        disk: prev.disk,
        network: { 
          ...prev.network, 
          upload: Math.max(0, prev.network.upload + (Math.random() - 0.5) * 20),
          download: Math.max(0, prev.network.download + (Math.random() - 0.5) * 50),
        },
      }))
      setLastUpdate(new Date())
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const handleRefresh = async () => {
    setIsLoading(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsLoading(false)
    setLastUpdate(new Date())
    toast.success("تم تحديث حالة النظام")
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case "healthy":
        return <CheckCircle2 className="w-5 h-5 text-green-500" />
      case "warning":
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />
      case "error":
        return <XCircle className="w-5 h-5 text-red-500" />
      default:
        return <Activity className="w-5 h-5 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "healthy": return "bg-green-100 dark:bg-green-900 border-green-200 dark:border-green-800"
      case "warning": return "bg-yellow-100 dark:bg-yellow-900 border-yellow-200 dark:border-yellow-800"
      case "error": return "bg-red-100 dark:bg-red-900 border-red-200 dark:border-red-800"
      default: return "bg-gray-100 dark:bg-gray-900"
    }
  }

  const getProgressColor = (value) => {
    if (value < 50) return "bg-green-500"
    if (value < 80) return "bg-yellow-500"
    return "bg-red-500"
  }

  // Overall status
  const healthyServices = services.filter(s => s.status === "healthy").length
  const overallStatus = healthyServices === services.length ? "healthy" : healthyServices > services.length * 0.8 ? "warning" : "error"

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Activity className="w-7 h-7 text-blue-500" />
            صحة النظام
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            مراقبة حالة النظام والخدمات في الوقت الفعلي
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground flex items-center gap-1">
            <Clock className="w-4 h-4" />
            آخر تحديث: {lastUpdate.toLocaleTimeString("ar-SA")}
          </span>
          <Button variant="outline" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ml-2 ${isLoading ? "animate-spin" : ""}`} />
            تحديث
          </Button>
        </div>
      </div>

      {/* Overall Status */}
      <Card className={`border-2 ${getStatusColor(overallStatus)}`}>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${
                overallStatus === "healthy" ? "bg-green-500" : 
                overallStatus === "warning" ? "bg-yellow-500" : "bg-red-500"
              }`}>
                {overallStatus === "healthy" ? (
                  <CheckCircle2 className="w-8 h-8 text-white" />
                ) : overallStatus === "warning" ? (
                  <AlertTriangle className="w-8 h-8 text-white" />
                ) : (
                  <XCircle className="w-8 h-8 text-white" />
                )}
              </div>
              <div>
                <h2 className="text-2xl font-bold">
                  {overallStatus === "healthy" ? "النظام يعمل بشكل طبيعي" :
                   overallStatus === "warning" ? "بعض الخدمات تحتاج انتباه" :
                   "مشاكل حرجة في النظام"}
                </h2>
                <p className="text-muted-foreground">
                  {healthyServices} من {services.length} خدمة تعمل بشكل طبيعي
                </p>
              </div>
            </div>
            <div className="text-left">
              <div className="text-4xl font-bold text-green-500">
                {Math.round((healthyServices / services.length) * 100)}%
              </div>
              <p className="text-sm text-muted-foreground">نسبة التشغيل</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* System Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* CPU */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Cpu className="w-4 h-4 text-blue-500" />
              المعالج (CPU)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-end justify-between">
                <span className="text-3xl font-bold">{Math.round(metrics.cpu.usage)}%</span>
                <span className="text-sm text-muted-foreground">{metrics.cpu.cores} أنوية</span>
              </div>
              <Progress value={metrics.cpu.usage} className={getProgressColor(metrics.cpu.usage)} />
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>درجة الحرارة</span>
                <span>{metrics.cpu.temperature}°C</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Memory */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <MemoryStick className="w-4 h-4 text-purple-500" />
              الذاكرة (RAM)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-end justify-between">
                <span className="text-3xl font-bold">{Math.round(metrics.memory.percentage)}%</span>
                <span className="text-sm text-muted-foreground">{metrics.memory.used}/{metrics.memory.total} GB</span>
              </div>
              <Progress value={metrics.memory.percentage} className={getProgressColor(metrics.memory.percentage)} />
            </div>
          </CardContent>
        </Card>

        {/* Disk */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <HardDrive className="w-4 h-4 text-green-500" />
              التخزين
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-end justify-between">
                <span className="text-3xl font-bold">{metrics.disk.percentage}%</span>
                <span className="text-sm text-muted-foreground">{metrics.disk.used}/{metrics.disk.total} GB</span>
              </div>
              <Progress value={metrics.disk.percentage} className={getProgressColor(metrics.disk.percentage)} />
            </div>
          </CardContent>
        </Card>

        {/* Network */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Wifi className="w-4 h-4 text-cyan-500" />
              الشبكة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className="text-sm">{Math.round(metrics.network.upload)} Mbps</span>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingDown className="w-4 h-4 text-blue-500" />
                  <span className="text-sm">{Math.round(metrics.network.download)} Mbps</span>
                </div>
              </div>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>زمن الاستجابة</span>
                <span>{metrics.network.latency} ms</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Services Status */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="w-5 h-5" />
              حالة الخدمات
            </CardTitle>
            <CardDescription>
              مراقبة حالة جميع الخدمات في النظام
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {services.map((service, index) => (
                <div
                  key={index}
                  className={`flex items-center justify-between p-3 rounded-lg border ${getStatusColor(service.status)}`}
                >
                  <div className="flex items-center gap-3">
                    {getStatusIcon(service.status)}
                    <div>
                      <p className="font-medium">{service.name}</p>
                      <p className="text-xs text-muted-foreground">{service.name_en}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <div className="text-left">
                      <p className="text-muted-foreground">وقت التشغيل</p>
                      <p className="font-medium">{service.uptime}</p>
                    </div>
                    <div className="text-left">
                      <p className="text-muted-foreground">الاستجابة</p>
                      <p className={`font-medium ${
                        service.responseTime < 100 ? "text-green-600" :
                        service.responseTime < 300 ? "text-yellow-600" : "text-red-600"
                      }`}>
                        {service.responseTime} ms
                      </p>
                    </div>
                    <Badge variant={
                      service.status === "healthy" ? "default" :
                      service.status === "warning" ? "secondary" : "destructive"
                    }>
                      {service.status === "healthy" ? "يعمل" :
                       service.status === "warning" ? "تحذير" : "متوقف"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              التنبيهات الأخيرة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-3 rounded-lg border ${
                    alert.type === "warning" ? "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800" :
                    alert.type === "success" ? "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800" :
                    "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {alert.type === "warning" ? (
                      <AlertTriangle className="w-4 h-4 text-yellow-600 mt-0.5" />
                    ) : alert.type === "success" ? (
                      <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5" />
                    ) : (
                      <Zap className="w-4 h-4 text-blue-600 mt-0.5" />
                    )}
                    <div>
                      <p className="text-sm">{alert.message}</p>
                      <p className="text-xs text-muted-foreground mt-1">{alert.time}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>إجراءات سريعة</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button variant="outline">
              <Database className="w-4 h-4 ml-2" />
              تحسين قاعدة البيانات
            </Button>
            <Button variant="outline">
              <HardDrive className="w-4 h-4 ml-2" />
              تنظيف الملفات المؤقتة
            </Button>
            <Button variant="outline">
              <RefreshCw className="w-4 h-4 ml-2" />
              إعادة تشغيل الكاش
            </Button>
            <Button variant="outline">
              <Globe className="w-4 h-4 ml-2" />
              فحص الاتصال
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SystemHealthPage
