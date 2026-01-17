/**
 * Authentication Management Page - إدارة المصادقة
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Shield,
  Key,
  Smartphone,
  Mail,
  Lock,
  Users,
  RefreshCw,
  Settings,
  Clock,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Eye,
  EyeOff,
  Copy,
  RotateCcw,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState("settings")
  const [isLoading, setIsLoading] = useState(false)

  // Auth Settings
  const [authSettings, setAuthSettings] = useState({
    jwt_expiry: 60,
    refresh_token_expiry: 7,
    max_login_attempts: 5,
    lockout_duration: 30,
    password_min_length: 8,
    require_uppercase: true,
    require_lowercase: true,
    require_numbers: true,
    require_special: true,
    password_history: 5,
    session_timeout: 30,
    allow_remember_me: true,
    mfa_enabled: true,
    mfa_methods: ["totp", "email"],
  })

  // Active Sessions
  const [sessions, setSessions] = useState([
    { id: 1, user: "أحمد محمد", ip: "192.168.1.100", device: "Chrome / Windows", location: "الرياض، السعودية", last_activity: "منذ 5 دقائق", status: "active" },
    { id: 2, user: "سارة أحمد", ip: "192.168.1.101", device: "Safari / MacOS", location: "جدة، السعودية", last_activity: "منذ 15 دقيقة", status: "active" },
    { id: 3, user: "محمد علي", ip: "10.0.0.50", device: "Firefox / Linux", location: "الدمام، السعودية", last_activity: "منذ ساعة", status: "idle" },
    { id: 4, user: "فاطمة خالد", ip: "172.16.0.20", device: "Mobile / iOS", location: "مكة، السعودية", last_activity: "منذ 30 دقيقة", status: "active" },
  ])

  // Login Attempts
  const [loginAttempts, setLoginAttempts] = useState([
    { id: 1, username: "admin", ip: "192.168.1.100", time: "2026-01-17 10:30:00", status: "success", location: "الرياض" },
    { id: 2, username: "user123", ip: "10.0.0.55", time: "2026-01-17 10:25:00", status: "failed", reason: "كلمة مرور خاطئة", location: "جدة" },
    { id: 3, username: "manager", ip: "192.168.1.101", time: "2026-01-17 10:20:00", status: "success", location: "الدمام" },
    { id: 4, username: "test", ip: "Unknown", time: "2026-01-17 10:15:00", status: "blocked", reason: "حساب مقفل", location: "غير معروف" },
    { id: 5, username: "admin", ip: "192.168.1.100", time: "2026-01-17 10:10:00", status: "success", location: "الرياض" },
  ])

  const handleSaveSettings = () => {
    toast.success("تم حفظ إعدادات المصادقة بنجاح")
  }

  const handleRevokeSession = (sessionId) => {
    setSessions(sessions.filter(s => s.id !== sessionId))
    toast.success("تم إنهاء الجلسة بنجاح")
  }

  const handleRevokeAllSessions = () => {
    setSessions([])
    toast.success("تم إنهاء جميع الجلسات بنجاح")
  }

  const stats = {
    activeSessions: sessions.filter(s => s.status === "active").length,
    totalSessions: sessions.length,
    failedAttempts: loginAttempts.filter(a => a.status === "failed").length,
    blockedAttempts: loginAttempts.filter(a => a.status === "blocked").length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Shield className="w-7 h-7 text-emerald-500" />
            إدارة المصادقة
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إعدادات المصادقة والجلسات ومحاولات الدخول
          </p>
        </div>
        <Button onClick={handleSaveSettings}>
          <CheckCircle2 className="w-4 h-4 ml-2" />
          حفظ الإعدادات
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Users className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.activeSessions}</p>
              <p className="text-sm text-muted-foreground">جلسة نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalSessions}</p>
              <p className="text-sm text-muted-foreground">إجمالي الجلسات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.failedAttempts}</p>
              <p className="text-sm text-muted-foreground">محاولة فاشلة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.blockedAttempts}</p>
              <p className="text-sm text-muted-foreground">محاولة محظورة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="settings" className="gap-2">
            <Settings className="w-4 h-4" />
            الإعدادات
          </TabsTrigger>
          <TabsTrigger value="sessions" className="gap-2">
            <Users className="w-4 h-4" />
            الجلسات النشطة
          </TabsTrigger>
          <TabsTrigger value="attempts" className="gap-2">
            <Clock className="w-4 h-4" />
            سجل المحاولات
          </TabsTrigger>
          <TabsTrigger value="mfa" className="gap-2">
            <Smartphone className="w-4 h-4" />
            المصادقة الثنائية
          </TabsTrigger>
        </TabsList>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* JWT Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Key className="w-5 h-5" />
                  إعدادات JWT
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>مدة صلاحية التوكن (دقائق)</Label>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[authSettings.jwt_expiry]}
                      onValueChange={([v]) => setAuthSettings({ ...authSettings, jwt_expiry: v })}
                      max={1440}
                      min={5}
                      step={5}
                      className="flex-1"
                    />
                    <span className="w-16 text-center font-medium">{authSettings.jwt_expiry}</span>
                  </div>
                </div>
                <div>
                  <Label>مدة صلاحية Refresh Token (أيام)</Label>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[authSettings.refresh_token_expiry]}
                      onValueChange={([v]) => setAuthSettings({ ...authSettings, refresh_token_expiry: v })}
                      max={30}
                      min={1}
                      step={1}
                      className="flex-1"
                    />
                    <span className="w-16 text-center font-medium">{authSettings.refresh_token_expiry}</span>
                  </div>
                </div>
                <div>
                  <Label>مهلة انتهاء الجلسة (دقائق)</Label>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[authSettings.session_timeout]}
                      onValueChange={([v]) => setAuthSettings({ ...authSettings, session_timeout: v })}
                      max={120}
                      min={5}
                      step={5}
                      className="flex-1"
                    />
                    <span className="w-16 text-center font-medium">{authSettings.session_timeout}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <Label>السماح بـ "تذكرني"</Label>
                  <Switch
                    checked={authSettings.allow_remember_me}
                    onCheckedChange={(v) => setAuthSettings({ ...authSettings, allow_remember_me: v })}
                  />
                </div>
              </CardContent>
            </Card>

            {/* Login Protection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lock className="w-5 h-5" />
                  حماية تسجيل الدخول
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>الحد الأقصى لمحاولات الدخول</Label>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[authSettings.max_login_attempts]}
                      onValueChange={([v]) => setAuthSettings({ ...authSettings, max_login_attempts: v })}
                      max={10}
                      min={3}
                      step={1}
                      className="flex-1"
                    />
                    <span className="w-16 text-center font-medium">{authSettings.max_login_attempts}</span>
                  </div>
                </div>
                <div>
                  <Label>مدة القفل (دقائق)</Label>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[authSettings.lockout_duration]}
                      onValueChange={([v]) => setAuthSettings({ ...authSettings, lockout_duration: v })}
                      max={120}
                      min={5}
                      step={5}
                      className="flex-1"
                    />
                    <span className="w-16 text-center font-medium">{authSettings.lockout_duration}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Password Policy */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Key className="w-5 h-5" />
                  سياسة كلمات المرور
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label>الحد الأدنى للطول</Label>
                      <div className="flex items-center gap-4">
                        <Slider
                          value={[authSettings.password_min_length]}
                          onValueChange={([v]) => setAuthSettings({ ...authSettings, password_min_length: v })}
                          max={32}
                          min={6}
                          step={1}
                          className="flex-1"
                        />
                        <span className="w-16 text-center font-medium">{authSettings.password_min_length}</span>
                      </div>
                    </div>
                    <div>
                      <Label>حفظ سجل كلمات المرور</Label>
                      <div className="flex items-center gap-4">
                        <Slider
                          value={[authSettings.password_history]}
                          onValueChange={([v]) => setAuthSettings({ ...authSettings, password_history: v })}
                          max={10}
                          min={0}
                          step={1}
                          className="flex-1"
                        />
                        <span className="w-16 text-center font-medium">{authSettings.password_history}</span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <Label>تطلب حروف كبيرة</Label>
                      <Switch
                        checked={authSettings.require_uppercase}
                        onCheckedChange={(v) => setAuthSettings({ ...authSettings, require_uppercase: v })}
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <Label>تطلب حروف صغيرة</Label>
                      <Switch
                        checked={authSettings.require_lowercase}
                        onCheckedChange={(v) => setAuthSettings({ ...authSettings, require_lowercase: v })}
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <Label>تطلب أرقام</Label>
                      <Switch
                        checked={authSettings.require_numbers}
                        onCheckedChange={(v) => setAuthSettings({ ...authSettings, require_numbers: v })}
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <Label>تطلب رموز خاصة</Label>
                      <Switch
                        checked={authSettings.require_special}
                        onCheckedChange={(v) => setAuthSettings({ ...authSettings, require_special: v })}
                      />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Sessions Tab */}
        <TabsContent value="sessions">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>الجلسات النشطة</CardTitle>
                <CardDescription>إدارة جلسات المستخدمين النشطة</CardDescription>
              </div>
              <Button variant="destructive" size="sm" onClick={handleRevokeAllSessions}>
                <XCircle className="w-4 h-4 ml-2" />
                إنهاء جميع الجلسات
              </Button>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المستخدم</TableHead>
                    <TableHead>الجهاز</TableHead>
                    <TableHead>الموقع</TableHead>
                    <TableHead>IP</TableHead>
                    <TableHead>آخر نشاط</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sessions.map(session => (
                    <TableRow key={session.id}>
                      <TableCell className="font-medium">{session.user}</TableCell>
                      <TableCell>{session.device}</TableCell>
                      <TableCell>{session.location}</TableCell>
                      <TableCell dir="ltr" className="font-mono text-sm">{session.ip}</TableCell>
                      <TableCell>{session.last_activity}</TableCell>
                      <TableCell>
                        <Badge variant={session.status === "active" ? "default" : "secondary"}>
                          {session.status === "active" ? "نشط" : "خامل"}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRevokeSession(session.id)}
                          className="text-red-600"
                        >
                          <XCircle className="w-4 h-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Login Attempts Tab */}
        <TabsContent value="attempts">
          <Card>
            <CardHeader>
              <CardTitle>سجل محاولات الدخول</CardTitle>
              <CardDescription>آخر 50 محاولة دخول للنظام</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المستخدم</TableHead>
                    <TableHead>الوقت</TableHead>
                    <TableHead>الموقع</TableHead>
                    <TableHead>IP</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>السبب</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {loginAttempts.map(attempt => (
                    <TableRow key={attempt.id}>
                      <TableCell className="font-medium">{attempt.username}</TableCell>
                      <TableCell dir="ltr" className="text-sm">{attempt.time}</TableCell>
                      <TableCell>{attempt.location}</TableCell>
                      <TableCell dir="ltr" className="font-mono text-sm">{attempt.ip}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            attempt.status === "success" ? "default" :
                            attempt.status === "failed" ? "secondary" :
                            "destructive"
                          }
                        >
                          {attempt.status === "success" ? (
                            <><CheckCircle2 className="w-3 h-3 ml-1" />نجح</>
                          ) : attempt.status === "failed" ? (
                            <><XCircle className="w-3 h-3 ml-1" />فشل</>
                          ) : (
                            <><AlertTriangle className="w-3 h-3 ml-1" />محظور</>
                          )}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {attempt.reason || "-"}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* MFA Tab */}
        <TabsContent value="mfa">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Smartphone className="w-5 h-5" />
                  إعدادات المصادقة الثنائية
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Shield className="w-8 h-8 text-emerald-500" />
                    <div>
                      <p className="font-medium">تفعيل المصادقة الثنائية</p>
                      <p className="text-sm text-muted-foreground">إلزام المستخدمين باستخدام MFA</p>
                    </div>
                  </div>
                  <Switch
                    checked={authSettings.mfa_enabled}
                    onCheckedChange={(v) => setAuthSettings({ ...authSettings, mfa_enabled: v })}
                  />
                </div>
                <Separator />
                <div className="space-y-3">
                  <Label>طرق المصادقة المسموحة</Label>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <div className="flex items-center gap-2">
                        <Smartphone className="w-4 h-4" />
                        <span>تطبيق المصادقة (TOTP)</span>
                      </div>
                      <Switch
                        checked={authSettings.mfa_methods.includes("totp")}
                        onCheckedChange={(v) => {
                          const methods = v
                            ? [...authSettings.mfa_methods, "totp"]
                            : authSettings.mfa_methods.filter(m => m !== "totp")
                          setAuthSettings({ ...authSettings, mfa_methods: methods })
                        }}
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4" />
                        <span>البريد الإلكتروني</span>
                      </div>
                      <Switch
                        checked={authSettings.mfa_methods.includes("email")}
                        onCheckedChange={(v) => {
                          const methods = v
                            ? [...authSettings.mfa_methods, "email"]
                            : authSettings.mfa_methods.filter(m => m !== "email")
                          setAuthSettings({ ...authSettings, mfa_methods: methods })
                        }}
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <div className="flex items-center gap-2">
                        <Smartphone className="w-4 h-4" />
                        <span>رسالة SMS</span>
                      </div>
                      <Switch
                        checked={authSettings.mfa_methods.includes("sms")}
                        onCheckedChange={(v) => {
                          const methods = v
                            ? [...authSettings.mfa_methods, "sms"]
                            : authSettings.mfa_methods.filter(m => m !== "sms")
                          setAuthSettings({ ...authSettings, mfa_methods: methods })
                        }}
                      />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>إحصائيات MFA</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg text-center">
                    <p className="text-3xl font-bold text-green-600">78%</p>
                    <p className="text-sm text-muted-foreground">مستخدمون مع MFA</p>
                  </div>
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-center">
                    <p className="text-3xl font-bold text-blue-600">156</p>
                    <p className="text-sm text-muted-foreground">إجمالي المستخدمين</p>
                  </div>
                </div>
                <Separator />
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">TOTP</span>
                    <div className="flex items-center gap-2">
                      <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500 rounded-full" style={{ width: "65%" }} />
                      </div>
                      <span className="text-sm font-medium">65%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Email</span>
                    <div className="flex items-center gap-2">
                      <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div className="h-full bg-blue-500 rounded-full" style={{ width: "25%" }} />
                      </div>
                      <span className="text-sm font-medium">25%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">SMS</span>
                    <div className="flex items-center gap-2">
                      <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div className="h-full bg-purple-500 rounded-full" style={{ width: "10%" }} />
                      </div>
                      <span className="text-sm font-medium">10%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AuthPage
