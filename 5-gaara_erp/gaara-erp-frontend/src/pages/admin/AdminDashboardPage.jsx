import { useState } from "react"
import { motion } from "framer-motion"
import {
  Shield,
  Users,
  Settings,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  Server,
  Database,
  HardDrive,
  Cpu,
  MemoryStick,
  Globe,
  Lock,
  Key,
  FileText,
  TrendingUp,
  Eye,
  UserCog,
  Bell,
  RefreshCw,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const AdminDashboardPage = () => {
  const [activeTab, setActiveTab] = useState("overview")

  // Mock data
  const systemStats = [
    {
      title: "المستخدمون النشطون",
      value: "١٢٨",
      change: "+12%",
      icon: Users,
      color: "emerald",
    },
    {
      title: "الجلسات النشطة",
      value: "٨٥",
      change: "+5%",
      icon: Activity,
      color: "blue",
    },
    {
      title: "التنبيهات",
      value: "٣",
      change: "-2",
      icon: AlertTriangle,
      color: "amber",
    },
    {
      title: "وقت التشغيل",
      value: "99.9%",
      change: "مستقر",
      icon: CheckCircle,
      color: "green",
    },
  ]

  const resourceUsage = [
    { name: "المعالج", value: 45, icon: Cpu, color: "blue" },
    { name: "الذاكرة", value: 68, icon: MemoryStick, color: "emerald" },
    { name: "التخزين", value: 52, icon: HardDrive, color: "amber" },
    { name: "الشبكة", value: 32, icon: Globe, color: "purple" },
  ]

  const recentActivities = [
    {
      user: "أحمد محمد",
      action: "تسجيل دخول",
      time: "منذ 5 دقائق",
      status: "success",
    },
    {
      user: "سارة أحمد",
      action: "تعديل صلاحيات",
      time: "منذ 15 دقيقة",
      status: "warning",
    },
    {
      user: "النظام",
      action: "نسخ احتياطي تلقائي",
      time: "منذ ساعة",
      status: "success",
    },
    {
      user: "محمد علي",
      action: "محاولة وصول غير مصرح",
      time: "منذ ساعتين",
      status: "error",
    },
  ]

  const securityAlerts = [
    {
      title: "محاولات تسجيل دخول فاشلة",
      count: 5,
      severity: "متوسط",
      color: "amber",
    },
    {
      title: "جلسات منتهية الصلاحية",
      count: 12,
      severity: "منخفض",
      color: "blue",
    },
    {
      title: "تغييرات صلاحيات",
      count: 3,
      severity: "معلومات",
      color: "green",
    },
  ]

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <Shield className="w-8 h-8 text-emerald-500" />
            لوحة تحكم المسؤول
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            مراقبة النظام وإدارة الأمان
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <FileText className="w-4 h-4 ml-2" />
            تقرير النظام
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {systemStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="border-0 shadow-lg bg-white dark:bg-slate-900">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
                      {stat.value}
                    </p>
                    <p className="text-xs text-emerald-500 mt-1">{stat.change}</p>
                  </div>
                  <div className={`w-12 h-12 rounded-xl bg-${stat.color}-100 dark:bg-${stat.color}-900/30 flex items-center justify-center`}>
                    <stat.icon className={`w-6 h-6 text-${stat.color}-500`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800 p-1">
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            نظرة عامة
          </TabsTrigger>
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            الأمان
          </TabsTrigger>
          <TabsTrigger value="users" className="flex items-center gap-2">
            <UserCog className="w-4 h-4" />
            المستخدمون
          </TabsTrigger>
          <TabsTrigger value="logs" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            السجلات
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Resource Usage */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Server className="w-5 h-5 text-emerald-500" />
                  استخدام الموارد
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {resourceUsage.map((resource) => (
                  <div key={resource.name} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <resource.icon className={`w-4 h-4 text-${resource.color}-500`} />
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          {resource.name}
                        </span>
                      </div>
                      <span className="text-sm font-medium text-slate-800 dark:text-white">
                        {resource.value}%
                      </span>
                    </div>
                    <Progress value={resource.value} className="h-2" />
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Recent Activities */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-blue-500" />
                  النشاطات الأخيرة
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivities.map((activity, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.status === "success"
                              ? "bg-emerald-500"
                              : activity.status === "warning"
                              ? "bg-amber-500"
                              : "bg-red-500"
                          }`}
                        />
                        <div>
                          <p className="text-sm font-medium text-slate-800 dark:text-white">
                            {activity.user}
                          </p>
                          <p className="text-xs text-slate-500">{activity.action}</p>
                        </div>
                      </div>
                      <span className="text-xs text-slate-400">{activity.time}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { title: "إدارة المستخدمين", icon: Users, color: "blue" },
              { title: "الصلاحيات", icon: Key, color: "amber" },
              { title: "إعدادات الأمان", icon: Lock, color: "emerald" },
              { title: "النسخ الاحتياطي", icon: Database, color: "purple" },
            ].map((action, index) => (
              <motion.div
                key={action.title}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
                  <CardContent className="p-4 flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg bg-${action.color}-100 dark:bg-${action.color}-900/30 flex items-center justify-center`}>
                      <action.icon className={`w-5 h-5 text-${action.color}-500`} />
                    </div>
                    <span className="font-medium text-slate-700 dark:text-slate-200">
                      {action.title}
                    </span>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {securityAlerts.map((alert, index) => (
              <motion.div
                key={alert.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <Badge className={`bg-${alert.color}-500`}>{alert.severity}</Badge>
                      <span className="text-2xl font-bold text-slate-800 dark:text-white">
                        {alert.count}
                      </span>
                    </div>
                    <p className="text-slate-600 dark:text-slate-400">{alert.title}</p>
                    <Button variant="link" className="p-0 mt-2 h-auto">
                      <Eye className="w-4 h-4 ml-1" />
                      عرض التفاصيل
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>إعدادات الأمان السريعة</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  { title: "تفعيل المصادقة الثنائية", enabled: true },
                  { title: "تشفير البيانات", enabled: true },
                  { title: "سجل النشاطات", enabled: true },
                  { title: "حماية CSRF", enabled: true },
                  { title: "تحديد معدل الطلبات", enabled: false },
                  { title: "قفل IP", enabled: false },
                ].map((setting, index) => (
                  <div
                    key={setting.title}
                    className={`p-4 rounded-lg border ${
                      setting.enabled
                        ? "border-emerald-200 bg-emerald-50 dark:bg-emerald-900/20"
                        : "border-slate-200 bg-slate-50 dark:bg-slate-800"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">{setting.title}</span>
                      {setting.enabled ? (
                        <CheckCircle className="w-5 h-5 text-emerald-500" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-slate-400" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Users Tab */}
        <TabsContent value="users" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>إحصائيات المستخدمين</CardTitle>
              <CardDescription>نظرة عامة على نشاط المستخدمين</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-slate-400">
                [جدول إحصائيات المستخدمين]
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Logs Tab */}
        <TabsContent value="logs" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>سجلات النظام</CardTitle>
              <CardDescription>سجلات الأحداث والأخطاء</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-slate-400">
                [جدول سجلات النظام]
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AdminDashboardPage
