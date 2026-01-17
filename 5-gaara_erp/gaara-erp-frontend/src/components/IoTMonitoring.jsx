import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Wifi,
  WifiOff,
  Thermometer,
  Droplets,
  Wind,
  Sun,
  Zap,
  AlertTriangle,
  CheckCircle,
  Settings,
  RefreshCw,
  MapPin,
  Activity,
  Bell,
  BarChart3,
  Gauge,
  Power,
} from "lucide-react"
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"

import { DataTable, StatsCard } from "@/components/common"
import { formatNumber } from "@/lib/utils"

// Mock sensor data
const mockDevices = [
  {
    id: 1,
    name: "مستشعر درجة الحرارة - المخزن أ",
    type: "temperature",
    location: "المخزن أ",
    status: "online",
    value: 24.5,
    unit: "°C",
    min: 18,
    max: 30,
    lastUpdate: "منذ دقيقة",
    battery: 85,
  },
  {
    id: 2,
    name: "مستشعر الرطوبة - المخزن أ",
    type: "humidity",
    location: "المخزن أ",
    status: "online",
    value: 45,
    unit: "%",
    min: 30,
    max: 60,
    lastUpdate: "منذ دقيقة",
    battery: 72,
  },
  {
    id: 3,
    name: "مستشعر الإضاءة - البيوت البلاستيكية",
    type: "light",
    location: "البيوت البلاستيكية",
    status: "online",
    value: 850,
    unit: "lux",
    min: 500,
    max: 1500,
    lastUpdate: "منذ 2 دقيقة",
    battery: 90,
  },
  {
    id: 4,
    name: "عداد الطاقة - المبنى الرئيسي",
    type: "energy",
    location: "المبنى الرئيسي",
    status: "online",
    value: 2.4,
    unit: "kW",
    min: 0,
    max: 10,
    lastUpdate: "منذ دقيقة",
    battery: 100,
  },
  {
    id: 5,
    name: "مستشعر حركة الهواء",
    type: "wind",
    location: "الحقل الشرقي",
    status: "offline",
    value: 0,
    unit: "m/s",
    min: 0,
    max: 20,
    lastUpdate: "منذ 3 ساعات",
    battery: 15,
  },
  {
    id: 6,
    name: "مستشعر رطوبة التربة",
    type: "soil",
    location: "الحقل الغربي",
    status: "warning",
    value: 25,
    unit: "%",
    min: 40,
    max: 80,
    lastUpdate: "منذ 5 دقائق",
    battery: 45,
  },
]

const mockAlerts = [
  {
    id: 1,
    device: "مستشعر رطوبة التربة",
    type: "تحذير",
    message: "رطوبة التربة منخفضة - يوصى بالري",
    time: "منذ 5 دقائق",
    status: "نشط",
    severity: "warning",
  },
  {
    id: 2,
    device: "مستشعر حركة الهواء",
    type: "خطأ",
    message: "فقدان الاتصال بالجهاز",
    time: "منذ 3 ساعات",
    status: "نشط",
    severity: "error",
  },
  {
    id: 3,
    device: "عداد الطاقة",
    type: "تنبيه",
    message: "استهلاك الطاقة يتجاوز المتوسط",
    time: "منذ ساعة",
    status: "معالج",
    severity: "info",
  },
]

// Generate chart data
const generateChartData = () => {
  const data = []
  for (let i = 23; i >= 0; i--) {
    data.push({
      time: `${String(23 - i).padStart(2, "0")}:00`,
      temperature: 22 + Math.random() * 6,
      humidity: 40 + Math.random() * 20,
      energy: 1.5 + Math.random() * 2,
    })
  }
  return data
}

const chartData = generateChartData()

const IoTMonitoring = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState("devices")
  const [devices, setDevices] = useState(mockDevices)
  const [alerts, setAlerts] = useState(mockAlerts)
  const [isRefreshing, setIsRefreshing] = useState(false)

  // Set active tab based on URL
  useEffect(() => {
    if (location.pathname.includes("/devices")) setActiveTab("devices")
    else if (location.pathname.includes("/sensors")) setActiveTab("sensors")
    else if (location.pathname.includes("/alerts")) setActiveTab("alerts")
    else if (location.pathname.includes("/analytics")) setActiveTab("analytics")
  }, [location])

  // Stats
  const totalDevices = devices.length
  const onlineDevices = devices.filter((d) => d.status === "online").length
  const offlineDevices = devices.filter((d) => d.status === "offline").length
  const activeAlerts = alerts.filter((a) => a.status === "نشط").length

  // Refresh handler
  const handleRefresh = () => {
    setIsRefreshing(true)
    setTimeout(() => {
      setDevices((prev) =>
        prev.map((d) => ({
          ...d,
          value: d.status === "online" ? d.value + (Math.random() - 0.5) * 2 : d.value,
          lastUpdate: "الآن",
        }))
      )
      setIsRefreshing(false)
      toast.success("تم تحديث البيانات")
    }, 1500)
  }

  // Get icon for device type
  const getDeviceIcon = (type) => {
    switch (type) {
      case "temperature":
        return Thermometer
      case "humidity":
        return Droplets
      case "light":
        return Sun
      case "energy":
        return Zap
      case "wind":
        return Wind
      case "soil":
        return Droplets
      default:
        return Wifi
    }
  }

  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case "online":
        return "text-emerald-500"
      case "offline":
        return "text-red-500"
      case "warning":
        return "text-amber-500"
      default:
        return "text-slate-500"
    }
  }

  // Device Card Component
  const DeviceCard = ({ device }) => {
    const Icon = getDeviceIcon(device.type)
    const isNormal = device.value >= device.min && device.value <= device.max
    const percentage = ((device.value - device.min) / (device.max - device.min)) * 100

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Card className={`hover:shadow-lg transition-all ${device.status === "offline" ? "opacity-60" : ""}`}>
          <CardContent className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div
                  className={`p-3 rounded-xl ${
                    device.status === "online"
                      ? "bg-emerald-100 dark:bg-emerald-900/30"
                      : device.status === "warning"
                      ? "bg-amber-100 dark:bg-amber-900/30"
                      : "bg-slate-100 dark:bg-slate-800"
                  }`}
                >
                  <Icon
                    className={`w-6 h-6 ${
                      device.status === "online"
                        ? "text-emerald-600"
                        : device.status === "warning"
                        ? "text-amber-600"
                        : "text-slate-400"
                    }`}
                  />
                </div>
                <div>
                  <h3 className="font-medium text-sm">{device.name}</h3>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <MapPin className="w-3 h-3" />
                    {device.location}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1">
                {device.status === "online" ? (
                  <Wifi className="w-4 h-4 text-emerald-500" />
                ) : (
                  <WifiOff className="w-4 h-4 text-red-500" />
                )}
              </div>
            </div>

            <div className="text-center mb-4">
              <span className={`text-4xl font-bold ${!isNormal ? "text-amber-600" : ""}`}>
                {device.value.toFixed(1)}
              </span>
              <span className="text-xl text-muted-foreground mr-1">{device.unit}</span>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>{device.min}{device.unit}</span>
                <span>{device.max}{device.unit}</span>
              </div>
              <Progress
                value={Math.max(0, Math.min(100, percentage))}
                className={`h-2 ${!isNormal ? "[&>div]:bg-amber-500" : ""}`}
              />
            </div>

            <div className="flex items-center justify-between mt-4 pt-4 border-t text-xs text-muted-foreground">
              <span>{device.lastUpdate}</span>
              <div className="flex items-center gap-1">
                <Gauge className="w-3 h-3" />
                {device.battery}%
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    )
  }

  // Alert columns
  const alertColumns = [
    { key: "device", header: "الجهاز" },
    {
      key: "type",
      header: "النوع",
      render: (val, row) => (
        <Badge
          variant={
            row.severity === "error"
              ? "destructive"
              : row.severity === "warning"
              ? "secondary"
              : "outline"
          }
        >
          {val}
        </Badge>
      ),
    },
    { key: "message", header: "الرسالة" },
    { key: "time", header: "الوقت" },
    {
      key: "status",
      header: "الحالة",
      render: (val) => (
        <Badge variant={val === "نشط" ? "destructive" : "default"}>{val}</Badge>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white">
            مراقبة إنترنت الأشياء (IoT)
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            مراقبة الأجهزة والمستشعرات في الوقت الفعلي
          </p>
        </div>
        <Button onClick={handleRefresh} disabled={isRefreshing}>
          <RefreshCw className={`w-4 h-4 ml-2 ${isRefreshing ? "animate-spin" : ""}`} />
          تحديث البيانات
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="إجمالي الأجهزة"
          value={totalDevices}
          icon={Wifi}
          color="blue"
          delay={0}
        />
        <StatsCard
          title="متصل"
          value={onlineDevices}
          icon={CheckCircle}
          color="emerald"
          delay={0.1}
        />
        <StatsCard
          title="غير متصل"
          value={offlineDevices}
          icon={WifiOff}
          color="red"
          delay={0.2}
        />
        <StatsCard
          title="تنبيهات نشطة"
          value={activeAlerts}
          icon={AlertTriangle}
          color="amber"
          delay={0.3}
        />
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="devices" className="gap-2">
            <Wifi className="w-4 h-4" />
            الأجهزة
          </TabsTrigger>
          <TabsTrigger value="sensors" className="gap-2">
            <Activity className="w-4 h-4" />
            المستشعرات
          </TabsTrigger>
          <TabsTrigger value="alerts" className="gap-2">
            <Bell className="w-4 h-4" />
            التنبيهات
          </TabsTrigger>
          <TabsTrigger value="analytics" className="gap-2">
            <BarChart3 className="w-4 h-4" />
            التحليلات
          </TabsTrigger>
        </TabsList>

        {/* Devices Tab */}
        <TabsContent value="devices" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {devices.map((device) => (
              <DeviceCard key={device.id} device={device} />
            ))}
          </div>
        </TabsContent>

        {/* Sensors Tab */}
        <TabsContent value="sensors" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Temperature Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Thermometer className="w-5 h-5 text-red-500" />
                  درجة الحرارة
                </CardTitle>
                <CardDescription>آخر 24 ساعة</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="tempGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis dataKey="time" className="text-xs" />
                    <YAxis className="text-xs" domain={[15, 35]} />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="temperature"
                      stroke="#ef4444"
                      fill="url(#tempGradient)"
                      name="°C"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Humidity Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Droplets className="w-5 h-5 text-blue-500" />
                  الرطوبة
                </CardTitle>
                <CardDescription>آخر 24 ساعة</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="humidGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis dataKey="time" className="text-xs" />
                    <YAxis className="text-xs" domain={[0, 100]} />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="humidity"
                      stroke="#3b82f6"
                      fill="url(#humidGradient)"
                      name="%"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Energy Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-500" />
                  استهلاك الطاقة
                </CardTitle>
                <CardDescription>آخر 24 ساعة</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis dataKey="time" className="text-xs" />
                    <YAxis className="text-xs" />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="energy"
                      stroke="#f59e0b"
                      strokeWidth={2}
                      dot={false}
                      name="kW"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Alerts Tab */}
        <TabsContent value="alerts" className="mt-6">
          <DataTable
            data={alerts}
            columns={alertColumns}
            searchKey="message"
            searchPlaceholder="البحث في التنبيهات..."
            showAdd={false}
            showSelection={false}
            onView={(row) => toast.info(`عرض: ${row.message}`)}
          />
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="md:col-span-3">
              <CardHeader>
                <CardTitle>التحليلات والتقارير</CardTitle>
                <CardDescription>تحليل بيانات المستشعرات</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { title: "تقرير درجة الحرارة", icon: Thermometer, color: "red" },
                    { title: "تقرير الرطوبة", icon: Droplets, color: "blue" },
                    { title: "تقرير الطاقة", icon: Zap, color: "amber" },
                    { title: "تقرير شامل", icon: BarChart3, color: "emerald" },
                  ].map((report, index) => (
                    <motion.div
                      key={report.title}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Button
                        variant="outline"
                        className="w-full h-auto py-6 flex flex-col items-center gap-2"
                        onClick={() => toast.info(`فتح: ${report.title}`)}
                      >
                        <report.icon className={`w-8 h-8 text-${report.color}-500`} />
                        <span className="text-sm">{report.title}</span>
                      </Button>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default IoTMonitoring
