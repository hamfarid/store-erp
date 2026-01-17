import { useState } from "react"
import { motion } from "framer-motion"
import {
  Plug,
  Link2,
  CheckCircle,
  XCircle,
  Settings,
  RefreshCw,
  Plus,
  Search,
  ExternalLink,
  Key,
  Shield,
  Zap,
  Clock,
  AlertTriangle,
  Database,
  Cloud,
  Mail,
  MessageSquare,
  CreditCard,
  Truck,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"

const IntegrationsPage = () => {
  const [activeTab, setActiveTab] = useState("all")
  const [searchTerm, setSearchTerm] = useState("")

  const integrationCategories = [
    {
      name: "الدفع الإلكتروني",
      icon: CreditCard,
      integrations: [
        {
          name: "Stripe",
          description: "بوابة دفع عالمية",
          status: "متصل",
          lastSync: "منذ 5 دقائق",
          enabled: true,
        },
        {
          name: "PayPal",
          description: "دفع عبر PayPal",
          status: "غير متصل",
          lastSync: "-",
          enabled: false,
        },
        {
          name: "Mada",
          description: "نظام الدفع المحلي",
          status: "متصل",
          lastSync: "منذ ساعة",
          enabled: true,
        },
      ],
    },
    {
      name: "الشحن والتوصيل",
      icon: Truck,
      integrations: [
        {
          name: "Aramex",
          description: "خدمات الشحن الدولي",
          status: "متصل",
          lastSync: "منذ 10 دقائق",
          enabled: true,
        },
        {
          name: "SMSA",
          description: "شحن محلي سريع",
          status: "متصل",
          lastSync: "منذ 30 دقيقة",
          enabled: true,
        },
      ],
    },
    {
      name: "التواصل والإشعارات",
      icon: MessageSquare,
      integrations: [
        {
          name: "Twilio",
          description: "إرسال SMS",
          status: "متصل",
          lastSync: "منذ ساعتين",
          enabled: true,
        },
        {
          name: "SendGrid",
          description: "خدمة البريد الإلكتروني",
          status: "متصل",
          lastSync: "منذ 15 دقيقة",
          enabled: true,
        },
        {
          name: "WhatsApp Business",
          description: "رسائل WhatsApp",
          status: "قيد الإعداد",
          lastSync: "-",
          enabled: false,
        },
      ],
    },
    {
      name: "الخدمات السحابية",
      icon: Cloud,
      integrations: [
        {
          name: "AWS S3",
          description: "تخزين الملفات",
          status: "متصل",
          lastSync: "منذ دقيقة",
          enabled: true,
        },
        {
          name: "Google Cloud",
          description: "خدمات سحابية",
          status: "غير متصل",
          lastSync: "-",
          enabled: false,
        },
      ],
    },
    {
      name: "قواعد البيانات",
      icon: Database,
      integrations: [
        {
          name: "PostgreSQL",
          description: "قاعدة البيانات الرئيسية",
          status: "متصل",
          lastSync: "مباشر",
          enabled: true,
        },
        {
          name: "Redis",
          description: "التخزين المؤقت",
          status: "متصل",
          lastSync: "مباشر",
          enabled: true,
        },
      ],
    },
  ]

  const apiStats = [
    { name: "طلبات API اليوم", value: "15,248", change: "+12%" },
    { name: "معدل النجاح", value: "99.8%", change: "+0.2%" },
    { name: "متوسط الاستجابة", value: "145ms", change: "-15ms" },
    { name: "التكاملات النشطة", value: "12", change: "+2" },
  ]

  const getStatusBadge = (status) => {
    const config = {
      "متصل": { color: "bg-emerald-500", icon: CheckCircle },
      "غير متصل": { color: "bg-slate-400", icon: XCircle },
      "قيد الإعداد": { color: "bg-amber-500", icon: Clock },
      "خطأ": { color: "bg-red-500", icon: AlertTriangle },
    }
    const { color, icon: Icon } = config[status] || config["غير متصل"]
    return (
      <Badge className={color}>
        <Icon className="w-3 h-3 ml-1" />
        {status}
      </Badge>
    )
  }

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <Plug className="w-8 h-8 text-emerald-500" />
            التكاملات
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة تكاملات النظام مع الخدمات الخارجية
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث الحالة
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <Plus className="w-4 h-4 ml-2" />
            إضافة تكامل
          </Button>
        </div>
      </div>

      {/* API Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {apiStats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="border-0 shadow-lg bg-white dark:bg-slate-900">
              <CardContent className="p-6">
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  {stat.name}
                </p>
                <div className="flex items-end justify-between mt-2">
                  <p className="text-2xl font-bold text-slate-800 dark:text-white">
                    {stat.value}
                  </p>
                  <span className="text-sm text-emerald-500">{stat.change}</span>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800 p-1">
          <TabsTrigger value="all" className="flex items-center gap-2">
            <Link2 className="w-4 h-4" />
            جميع التكاملات
          </TabsTrigger>
          <TabsTrigger value="active" className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            النشطة
          </TabsTrigger>
          <TabsTrigger value="api" className="flex items-center gap-2">
            <Key className="w-4 h-4" />
            مفاتيح API
          </TabsTrigger>
          <TabsTrigger value="logs" className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            السجلات
          </TabsTrigger>
        </TabsList>

        {/* All Integrations Tab */}
        <TabsContent value="all" className="space-y-6 mt-6">
          {/* Search */}
          <div className="relative w-full max-w-md">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              placeholder="بحث في التكاملات..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pr-10"
            />
          </div>

          {/* Integration Categories */}
          <div className="space-y-6">
            {integrationCategories.map((category, catIndex) => (
              <motion.div
                key={category.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: catIndex * 0.1 }}
              >
                <Card className="border-0 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <category.icon className="w-5 h-5 text-emerald-500" />
                      {category.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {category.integrations.map((integration, intIndex) => (
                        <motion.div
                          key={integration.name}
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: intIndex * 0.05 }}
                          className={`p-4 rounded-lg border ${
                            integration.enabled
                              ? "border-emerald-200 bg-emerald-50/50 dark:bg-emerald-900/10"
                              : "border-slate-200 bg-slate-50 dark:bg-slate-800"
                          }`}
                        >
                          <div className="flex items-start justify-between mb-3">
                            <div>
                              <h4 className="font-medium text-slate-800 dark:text-white">
                                {integration.name}
                              </h4>
                              <p className="text-sm text-slate-500">
                                {integration.description}
                              </p>
                            </div>
                            <Switch checked={integration.enabled} />
                          </div>
                          <div className="flex items-center justify-between">
                            {getStatusBadge(integration.status)}
                            <span className="text-xs text-slate-400">
                              {integration.lastSync}
                            </span>
                          </div>
                          <div className="flex gap-2 mt-3">
                            <Button variant="outline" size="sm" className="flex-1">
                              <Settings className="w-4 h-4 ml-1" />
                              إعدادات
                            </Button>
                            <Button variant="outline" size="sm">
                              <ExternalLink className="w-4 h-4" />
                            </Button>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {/* Active Integrations Tab */}
        <TabsContent value="active" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>التكاملات النشطة</CardTitle>
              <CardDescription>
                جميع التكاملات المتصلة والعاملة حالياً
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {integrationCategories
                  .flatMap((cat) =>
                    cat.integrations.filter((i) => i.enabled && i.status === "متصل")
                  )
                  .map((integration, index) => (
                    <motion.div
                      key={integration.name}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-center justify-between p-4 rounded-lg border border-emerald-200 bg-emerald-50/50 dark:bg-emerald-900/10"
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                          <Zap className="w-5 h-5 text-emerald-500" />
                        </div>
                        <div>
                          <h4 className="font-medium text-slate-800 dark:text-white">
                            {integration.name}
                          </h4>
                          <p className="text-sm text-slate-500">
                            آخر مزامنة: {integration.lastSync}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        {getStatusBadge(integration.status)}
                        <Button variant="ghost" size="sm">
                          <Settings className="w-4 h-4" />
                        </Button>
                      </div>
                    </motion.div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* API Keys Tab */}
        <TabsContent value="api" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>مفاتيح API</CardTitle>
                  <CardDescription>
                    إدارة مفاتيح الوصول للتكاملات الخارجية
                  </CardDescription>
                </div>
                <Button className="bg-emerald-500 hover:bg-emerald-600">
                  <Key className="w-4 h-4 ml-2" />
                  مفتاح جديد
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { name: "Production API Key", created: "2025-01-01", requests: 15248 },
                  { name: "Development API Key", created: "2024-12-15", requests: 3421 },
                  { name: "Mobile App Key", created: "2024-11-20", requests: 8756 },
                ].map((key, index) => (
                  <div
                    key={key.name}
                    className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                        <Key className="w-5 h-5 text-amber-500" />
                      </div>
                      <div>
                        <h4 className="font-medium text-slate-800 dark:text-white">
                          {key.name}
                        </h4>
                        <p className="text-sm text-slate-500">
                          أنشئ في: {key.created} • {key.requests.toLocaleString()} طلب
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        <Shield className="w-4 h-4 ml-1" />
                        عرض
                      </Button>
                      <Button variant="outline" size="sm">
                        <RefreshCw className="w-4 h-4 ml-1" />
                        تجديد
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Logs Tab */}
        <TabsContent value="logs" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>سجلات التكاملات</CardTitle>
              <CardDescription>
                سجل آخر العمليات والأحداث
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-slate-400">
                [جدول سجلات التكاملات]
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default IntegrationsPage
