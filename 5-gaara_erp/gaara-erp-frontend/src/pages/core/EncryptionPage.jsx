/**
 * Encryption Management Page - إدارة التشفير
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Lock,
  Key,
  Shield,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Copy,
  Eye,
  EyeOff,
  Download,
  Upload,
  FileKey,
  Database,
  Server,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const EncryptionPage = () => {
  const [activeTab, setActiveTab] = useState("overview")
  const [showKey, setShowKey] = useState(false)
  const [isRegenerateDialogOpen, setIsRegenerateDialogOpen] = useState(false)

  // Encryption Settings
  const [settings, setSettings] = useState({
    algorithm: "AES-256-GCM",
    key_rotation_days: 90,
    auto_rotate: true,
    encrypt_at_rest: true,
    encrypt_in_transit: true,
    encrypt_backups: true,
  })

  // Keys Info
  const [keys, setKeys] = useState([
    { id: 1, name: "مفتاح رئيسي", type: "master", algorithm: "AES-256", created: "2025-10-15", expires: "2026-01-15", status: "active", usage: 85 },
    { id: 2, name: "مفتاح قاعدة البيانات", type: "database", algorithm: "AES-256", created: "2025-11-01", expires: "2026-02-01", status: "active", usage: 72 },
    { id: 3, name: "مفتاح API", type: "api", algorithm: "RSA-4096", created: "2025-12-01", expires: "2026-03-01", status: "active", usage: 45 },
    { id: 4, name: "مفتاح النسخ الاحتياطي", type: "backup", algorithm: "AES-256", created: "2025-09-01", expires: "2025-12-01", status: "expired", usage: 0 },
  ])

  // Encrypted Fields
  const encryptedFields = [
    { model: "User", field: "password", type: "hash", algorithm: "Argon2id" },
    { model: "User", field: "phone", type: "encrypt", algorithm: "AES-256" },
    { model: "User", field: "email", type: "encrypt", algorithm: "AES-256" },
    { model: "Company", field: "tax_number", type: "encrypt", algorithm: "AES-256" },
    { model: "ApiKey", field: "key", type: "hash", algorithm: "SHA-256" },
    { model: "Session", field: "token", type: "encrypt", algorithm: "AES-256" },
  ]

  const handleRegenerateKey = () => {
    toast.success("تم تجديد المفتاح بنجاح")
    setIsRegenerateDialogOpen(false)
  }

  const handleCopyKey = () => {
    navigator.clipboard.writeText("sk-xxxxxxxxxxxxxxxxxxxxx")
    toast.success("تم نسخ المفتاح")
  }

  const handleExportKeys = () => {
    toast.success("تم تصدير المفاتيح بنجاح")
  }

  const stats = {
    activeKeys: keys.filter(k => k.status === "active").length,
    expiredKeys: keys.filter(k => k.status === "expired").length,
    encryptedModels: new Set(encryptedFields.map(f => f.model)).size,
    encryptedFields: encryptedFields.length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Lock className="w-7 h-7 text-amber-500" />
            إدارة التشفير
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إعدادات التشفير ومفاتيح الأمان
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExportKeys}>
            <Download className="w-4 h-4 ml-2" />
            تصدير المفاتيح
          </Button>
          <Button onClick={() => toast.success("تم حفظ الإعدادات")}>
            <CheckCircle2 className="w-4 h-4 ml-2" />
            حفظ
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Key className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.activeKeys}</p>
              <p className="text-sm text-muted-foreground">مفتاح نشط</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.expiredKeys}</p>
              <p className="text-sm text-muted-foreground">مفتاح منتهي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Database className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.encryptedModels}</p>
              <p className="text-sm text-muted-foreground">موديل مشفر</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Shield className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.encryptedFields}</p>
              <p className="text-sm text-muted-foreground">حقل مشفر</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview" className="gap-2">
            <Shield className="w-4 h-4" />
            نظرة عامة
          </TabsTrigger>
          <TabsTrigger value="keys" className="gap-2">
            <Key className="w-4 h-4" />
            المفاتيح
          </TabsTrigger>
          <TabsTrigger value="fields" className="gap-2">
            <Database className="w-4 h-4" />
            الحقول المشفرة
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>إعدادات التشفير</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>خوارزمية التشفير</Label>
                  <Select value={settings.algorithm} onValueChange={(v) => setSettings({ ...settings, algorithm: v })}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="AES-256-GCM">AES-256-GCM (موصى به)</SelectItem>
                      <SelectItem value="AES-256-CBC">AES-256-CBC</SelectItem>
                      <SelectItem value="ChaCha20-Poly1305">ChaCha20-Poly1305</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>دورة تجديد المفاتيح (أيام)</Label>
                  <Input
                    type="number"
                    value={settings.key_rotation_days}
                    onChange={(e) => setSettings({ ...settings, key_rotation_days: parseInt(e.target.value) })}
                  />
                </div>
                <Separator />
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>التجديد التلقائي للمفاتيح</Label>
                      <p className="text-sm text-muted-foreground">تجديد المفاتيح تلقائياً عند انتهاء صلاحيتها</p>
                    </div>
                    <Switch checked={settings.auto_rotate} onCheckedChange={(v) => setSettings({ ...settings, auto_rotate: v })} />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>حالة التشفير</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Database className="w-6 h-6 text-blue-500" />
                    <div>
                      <p className="font-medium">تشفير البيانات الساكنة</p>
                      <p className="text-sm text-muted-foreground">Data at Rest</p>
                    </div>
                  </div>
                  <Switch checked={settings.encrypt_at_rest} onCheckedChange={(v) => setSettings({ ...settings, encrypt_at_rest: v })} />
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Globe className="w-6 h-6 text-green-500" />
                    <div>
                      <p className="font-medium">تشفير البيانات المنقولة</p>
                      <p className="text-sm text-muted-foreground">Data in Transit (TLS/SSL)</p>
                    </div>
                  </div>
                  <Switch checked={settings.encrypt_in_transit} onCheckedChange={(v) => setSettings({ ...settings, encrypt_in_transit: v })} />
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileKey className="w-6 h-6 text-purple-500" />
                    <div>
                      <p className="font-medium">تشفير النسخ الاحتياطية</p>
                      <p className="text-sm text-muted-foreground">Backup Encryption</p>
                    </div>
                  </div>
                  <Switch checked={settings.encrypt_backups} onCheckedChange={(v) => setSettings({ ...settings, encrypt_backups: v })} />
                </div>
              </CardContent>
            </Card>

            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>تقييم الأمان</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-6">
                  <div className="relative w-32 h-32">
                    <svg className="w-32 h-32 transform -rotate-90">
                      <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="none" className="text-gray-200 dark:text-gray-700" />
                      <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="none" strokeDasharray={`${92 * 3.52} 352`} className="text-green-500" strokeLinecap="round" />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-3xl font-bold">92%</span>
                    </div>
                  </div>
                  <div className="flex-1 space-y-3">
                    <div className="flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                      <span>تشفير AES-256 مفعل</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                      <span>TLS 1.3 للاتصالات</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                      <span>تجديد تلقائي للمفاتيح</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <AlertTriangle className="w-5 h-5 text-yellow-500" />
                      <span>يوجد مفتاح منتهي الصلاحية يحتاج تجديد</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Keys Tab */}
        <TabsContent value="keys">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>مفاتيح التشفير</CardTitle>
                <CardDescription>إدارة مفاتيح التشفير والأمان</CardDescription>
              </div>
              <Button onClick={() => setIsRegenerateDialogOpen(true)}>
                <RefreshCw className="w-4 h-4 ml-2" />
                تجديد المفاتيح
              </Button>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المفتاح</TableHead>
                    <TableHead>النوع</TableHead>
                    <TableHead>الخوارزمية</TableHead>
                    <TableHead>تاريخ الإنشاء</TableHead>
                    <TableHead>تاريخ الانتهاء</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>الاستخدام</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {keys.map(key => (
                    <TableRow key={key.id}>
                      <TableCell className="font-medium">{key.name}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{key.type}</Badge>
                      </TableCell>
                      <TableCell className="font-mono text-sm">{key.algorithm}</TableCell>
                      <TableCell>{key.created}</TableCell>
                      <TableCell>{key.expires}</TableCell>
                      <TableCell>
                        <Badge variant={key.status === "active" ? "default" : "destructive"}>
                          {key.status === "active" ? "نشط" : "منتهي"}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="w-20">
                          <Progress value={key.usage} className="h-2" />
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-1">
                          <Button variant="ghost" size="sm" onClick={handleCopyKey}>
                            <Copy className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <RefreshCw className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Encrypted Fields Tab */}
        <TabsContent value="fields">
          <Card>
            <CardHeader>
              <CardTitle>الحقول المشفرة</CardTitle>
              <CardDescription>قائمة الحقول المشفرة في قاعدة البيانات</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>الموديل</TableHead>
                    <TableHead>الحقل</TableHead>
                    <TableHead>نوع التشفير</TableHead>
                    <TableHead>الخوارزمية</TableHead>
                    <TableHead>الحالة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {encryptedFields.map((field, index) => (
                    <TableRow key={index}>
                      <TableCell className="font-medium">{field.model}</TableCell>
                      <TableCell className="font-mono text-sm">{field.field}</TableCell>
                      <TableCell>
                        <Badge variant={field.type === "hash" ? "secondary" : "default"}>
                          {field.type === "hash" ? "تجزئة" : "تشفير"}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-mono text-sm">{field.algorithm}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-green-600">
                          <CheckCircle2 className="w-3 h-3 ml-1" />
                          مفعل
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Regenerate Key Dialog */}
      <AlertDialog open={isRegenerateDialogOpen} onOpenChange={setIsRegenerateDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>تجديد المفاتيح</AlertDialogTitle>
            <AlertDialogDescription>
              سيؤدي تجديد المفاتيح إلى إنشاء مفاتيح تشفير جديدة. تأكد من حفظ نسخة احتياطية قبل المتابعة.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleRegenerateKey}>
              تجديد المفاتيح
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

export default EncryptionPage
