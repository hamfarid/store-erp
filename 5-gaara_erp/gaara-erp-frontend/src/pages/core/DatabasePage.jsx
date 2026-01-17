/**
 * Database Management Page - إدارة قاعدة البيانات
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Database,
  HardDrive,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Trash2,
  Download,
  Upload,
  Play,
  Clock,
  Zap,
  Table,
  BarChart3,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Table as UITable,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { ScrollArea } from "@/components/ui/scroll-area"

const DatabasePage = () => {
  const [activeTab, setActiveTab] = useState("overview")
  const [isOptimizing, setIsOptimizing] = useState(false)

  // Database Info
  const dbInfo = {
    name: "gaara_erp_db",
    engine: "PostgreSQL 15.4",
    size: "2.4 GB",
    tables: 180,
    connections: 45,
    max_connections: 100,
    uptime: "15 days 4 hours",
    cache_hit_ratio: 98.5,
    avg_query_time: "12ms",
  }

  // Tables List
  const tables = [
    { name: "users", rows: 1250, size: "45 MB", lastModified: "منذ دقيقتين", indexes: 5 },
    { name: "companies", rows: 85, size: "12 MB", lastModified: "منذ ساعة", indexes: 3 },
    { name: "products", rows: 15420, size: "320 MB", lastModified: "منذ 5 دقائق", indexes: 8 },
    { name: "orders", rows: 45000, size: "890 MB", lastModified: "منذ دقيقة", indexes: 12 },
    { name: "inventory", rows: 28500, size: "450 MB", lastModified: "منذ 3 دقائق", indexes: 6 },
    { name: "audit_logs", rows: 125000, size: "650 MB", lastModified: "منذ ثانية", indexes: 4 },
    { name: "sessions", rows: 320, size: "8 MB", lastModified: "منذ دقيقة", indexes: 2 },
    { name: "api_keys", rows: 156, size: "2 MB", lastModified: "منذ يوم", indexes: 2 },
  ]

  // Recent Queries
  const queries = [
    { query: "SELECT * FROM users WHERE status = 'active'", time: "8ms", rows: 1150, status: "success" },
    { query: "UPDATE orders SET status = 'shipped' WHERE id = 4521", time: "15ms", rows: 1, status: "success" },
    { query: "INSERT INTO audit_logs (action, user_id, ...) VALUES (...)", time: "5ms", rows: 1, status: "success" },
    { query: "SELECT COUNT(*) FROM products WHERE stock < 10", time: "120ms", rows: 45, status: "slow" },
    { query: "DELETE FROM sessions WHERE expires_at < NOW()", time: "35ms", rows: 25, status: "success" },
  ]

  const handleOptimize = async () => {
    setIsOptimizing(true)
    await new Promise(r => setTimeout(r, 2000))
    setIsOptimizing(false)
    toast.success("تم تحسين قاعدة البيانات بنجاح")
  }

  const handleBackup = () => {
    toast.success("جاري إنشاء نسخة احتياطية...")
  }

  const handleVacuum = () => {
    toast.success("جاري تنظيف قاعدة البيانات...")
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Database className="w-7 h-7 text-blue-500" />
            إدارة قاعدة البيانات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            مراقبة وإدارة قاعدة البيانات والجداول
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleBackup}>
            <Download className="w-4 h-4 ml-2" />
            نسخ احتياطي
          </Button>
          <Button onClick={handleOptimize} disabled={isOptimizing}>
            <Zap className="w-4 h-4 ml-2" />
            {isOptimizing ? "جاري التحسين..." : "تحسين"}
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
              <p className="text-2xl font-bold">{dbInfo.size}</p>
              <p className="text-sm text-muted-foreground">حجم قاعدة البيانات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Table className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{dbInfo.tables}</p>
              <p className="text-sm text-muted-foreground">جدول</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Zap className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{dbInfo.cache_hit_ratio}%</p>
              <p className="text-sm text-muted-foreground">نسبة إصابة الكاش</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{dbInfo.avg_query_time}</p>
              <p className="text-sm text-muted-foreground">متوسط وقت الاستعلام</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
          <TabsTrigger value="tables">الجداول</TabsTrigger>
          <TabsTrigger value="queries">الاستعلامات</TabsTrigger>
          <TabsTrigger value="maintenance">الصيانة</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>معلومات قاعدة البيانات</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-muted-foreground">الاسم</span>
                  <span className="font-medium font-mono">{dbInfo.name}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-muted-foreground">المحرك</span>
                  <span className="font-medium">{dbInfo.engine}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-muted-foreground">وقت التشغيل</span>
                  <span className="font-medium">{dbInfo.uptime}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-muted-foreground">الحالة</span>
                  <Badge variant="default"><CheckCircle2 className="w-3 h-3 ml-1" />متصل</Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>استخدام الاتصالات</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span>الاتصالات النشطة</span>
                    <span>{dbInfo.connections} / {dbInfo.max_connections}</span>
                  </div>
                  <Progress value={(dbInfo.connections / dbInfo.max_connections) * 100} />
                </div>
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="p-3 bg-muted rounded-lg text-center">
                    <p className="text-2xl font-bold text-green-600">45</p>
                    <p className="text-sm text-muted-foreground">نشط</p>
                  </div>
                  <div className="p-3 bg-muted rounded-lg text-center">
                    <p className="text-2xl font-bold text-gray-600">55</p>
                    <p className="text-sm text-muted-foreground">متاح</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Tables Tab */}
        <TabsContent value="tables">
          <Card>
            <CardHeader>
              <CardTitle>جداول قاعدة البيانات</CardTitle>
              <CardDescription>قائمة بجميع الجداول وحجمها</CardDescription>
            </CardHeader>
            <CardContent>
              <UITable>
                <TableHeader>
                  <TableRow>
                    <TableHead>الجدول</TableHead>
                    <TableHead>الصفوف</TableHead>
                    <TableHead>الحجم</TableHead>
                    <TableHead>الفهارس</TableHead>
                    <TableHead>آخر تعديل</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {tables.map((table, i) => (
                    <TableRow key={i}>
                      <TableCell className="font-mono font-medium">{table.name}</TableCell>
                      <TableCell>{table.rows.toLocaleString()}</TableCell>
                      <TableCell>{table.size}</TableCell>
                      <TableCell>{table.indexes}</TableCell>
                      <TableCell className="text-muted-foreground">{table.lastModified}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="sm"><BarChart3 className="w-4 h-4" /></Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </UITable>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Queries Tab */}
        <TabsContent value="queries">
          <Card>
            <CardHeader>
              <CardTitle>الاستعلامات الأخيرة</CardTitle>
            </CardHeader>
            <CardContent>
              <UITable>
                <TableHeader>
                  <TableRow>
                    <TableHead>الاستعلام</TableHead>
                    <TableHead>الوقت</TableHead>
                    <TableHead>الصفوف</TableHead>
                    <TableHead>الحالة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {queries.map((q, i) => (
                    <TableRow key={i}>
                      <TableCell className="font-mono text-sm max-w-md truncate">{q.query}</TableCell>
                      <TableCell>{q.time}</TableCell>
                      <TableCell>{q.rows}</TableCell>
                      <TableCell>
                        <Badge variant={q.status === "slow" ? "secondary" : "default"}>
                          {q.status === "slow" ? <AlertTriangle className="w-3 h-3 ml-1" /> : <CheckCircle2 className="w-3 h-3 ml-1" />}
                          {q.status === "slow" ? "بطيء" : "ناجح"}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </UITable>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Maintenance Tab */}
        <TabsContent value="maintenance">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><RefreshCw className="w-5 h-5" />تحسين</CardTitle>
                <CardDescription>تحسين أداء قاعدة البيانات</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" onClick={handleOptimize} disabled={isOptimizing}>
                  {isOptimizing ? "جاري التحسين..." : "بدء التحسين"}
                </Button>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Trash2 className="w-5 h-5" />تنظيف</CardTitle>
                <CardDescription>تنظيف البيانات المحذوفة</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" onClick={handleVacuum}>تشغيل VACUUM</Button>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Download className="w-5 h-5" />نسخ احتياطي</CardTitle>
                <CardDescription>إنشاء نسخة احتياطية</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline" onClick={handleBackup}>إنشاء نسخة</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default DatabasePage
