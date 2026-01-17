import { useState } from "react"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Settings,
  Moon,
  Sun,
  Globe,
  Bell,
  Shield,
  Database,
  Palette,
  Monitor,
  Smartphone,
  ChevronRight,
  Check,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { useTheme } from "@/contexts/ThemeContext"

const languages = [
  { value: "ar", label: "العربية", flag: "🇸🇦" },
  { value: "en", label: "English", flag: "🇺🇸" },
]

const currencies = [
  { value: "SAR", label: "ريال سعودي (ر.س)" },
  { value: "USD", label: "دولار أمريكي ($)" },
  { value: "EUR", label: "يورو (€)" },
  { value: "AED", label: "درهم إماراتي (د.إ)" },
]

const dateFormats = [
  { value: "dd/MM/yyyy", label: "31/12/2025" },
  { value: "MM/dd/yyyy", label: "12/31/2025" },
  { value: "yyyy-MM-dd", label: "2025-12-31" },
]

const SettingsPage = () => {
  const { theme, setTheme } = useTheme()
  const [settings, setSettings] = useState({
    language: "ar",
    currency: "SAR",
    dateFormat: "dd/MM/yyyy",
    timezone: "Asia/Riyadh",
    notifications: {
      email: true,
      push: true,
      sms: false,
      orders: true,
      inventory: true,
      reports: false,
    },
    security: {
      twoFactor: false,
      sessionTimeout: "30",
      loginAlerts: true,
    },
    display: {
      compactMode: false,
      animations: true,
      rtl: true,
    },
  })

  const handleSettingChange = (category, key, value) => {
    setSettings((prev) => ({
      ...prev,
      [category]: typeof prev[category] === "object"
        ? { ...prev[category], [key]: value }
        : value,
    }))
    toast.success("تم حفظ الإعداد")
  }

  const SettingRow = ({ icon: Icon, title, description, children }) => (
    <div className="flex items-center justify-between py-4">
      <div className="flex items-center gap-4">
        <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800">
          <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
        </div>
        <div>
          <p className="font-medium">{title}</p>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </div>
      {children}
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">الإعدادات</h1>
        <p className="text-slate-600 dark:text-slate-400">إدارة إعدادات التطبيق والتفضيلات</p>
      </div>

      {/* Appearance Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Palette className="w-5 h-5" />
            المظهر
          </CardTitle>
          <CardDescription>تخصيص مظهر التطبيق</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Theme Selection */}
          <div className="space-y-3">
            <Label>السمة</Label>
            <RadioGroup
              value={theme}
              onValueChange={setTheme}
              className="grid grid-cols-3 gap-4"
            >
              <Label
                htmlFor="light"
                className={`flex flex-col items-center gap-2 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  theme === "light"
                    ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
                    : "border-slate-200 dark:border-slate-700 hover:border-slate-300"
                }`}
              >
                <RadioGroupItem value="light" id="light" className="sr-only" />
                <Sun className="w-6 h-6" />
                <span className="text-sm font-medium">فاتح</span>
                {theme === "light" && (
                  <Check className="w-4 h-4 text-emerald-500 absolute top-2 right-2" />
                )}
              </Label>
              <Label
                htmlFor="dark"
                className={`flex flex-col items-center gap-2 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  theme === "dark"
                    ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
                    : "border-slate-200 dark:border-slate-700 hover:border-slate-300"
                }`}
              >
                <RadioGroupItem value="dark" id="dark" className="sr-only" />
                <Moon className="w-6 h-6" />
                <span className="text-sm font-medium">داكن</span>
              </Label>
              <Label
                htmlFor="system"
                className={`flex flex-col items-center gap-2 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  theme === "system"
                    ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
                    : "border-slate-200 dark:border-slate-700 hover:border-slate-300"
                }`}
              >
                <RadioGroupItem value="system" id="system" className="sr-only" />
                <Monitor className="w-6 h-6" />
                <span className="text-sm font-medium">تلقائي</span>
              </Label>
            </RadioGroup>
          </div>

          <Separator />

          <SettingRow
            icon={Smartphone}
            title="الوضع المضغوط"
            description="تقليل المسافات لعرض المزيد من المحتوى"
          >
            <Switch
              checked={settings.display.compactMode}
              onCheckedChange={(checked) =>
                handleSettingChange("display", "compactMode", checked)
              }
            />
          </SettingRow>

          <SettingRow
            icon={Palette}
            title="الرسوم المتحركة"
            description="تفعيل الرسوم المتحركة في الواجهة"
          >
            <Switch
              checked={settings.display.animations}
              onCheckedChange={(checked) =>
                handleSettingChange("display", "animations", checked)
              }
            />
          </SettingRow>
        </CardContent>
      </Card>

      {/* Regional Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="w-5 h-5" />
            الإعدادات الإقليمية
          </CardTitle>
          <CardDescription>تخصيص اللغة والعملة والتنسيق</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label>اللغة</Label>
              <Select
                value={settings.language}
                onValueChange={(value) => handleSettingChange("language", null, value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {languages.map((lang) => (
                    <SelectItem key={lang.value} value={lang.value}>
                      <span className="flex items-center gap-2">
                        <span>{lang.flag}</span>
                        <span>{lang.label}</span>
                      </span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>العملة</Label>
              <Select
                value={settings.currency}
                onValueChange={(value) => handleSettingChange("currency", null, value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {currencies.map((curr) => (
                    <SelectItem key={curr.value} value={curr.value}>
                      {curr.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>تنسيق التاريخ</Label>
              <Select
                value={settings.dateFormat}
                onValueChange={(value) => handleSettingChange("dateFormat", null, value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {dateFormats.map((format) => (
                    <SelectItem key={format.value} value={format.value}>
                      {format.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>المنطقة الزمنية</Label>
              <Select
                value={settings.timezone}
                onValueChange={(value) => handleSettingChange("timezone", null, value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Asia/Riyadh">الرياض (UTC+3)</SelectItem>
                  <SelectItem value="Asia/Dubai">دبي (UTC+4)</SelectItem>
                  <SelectItem value="Africa/Cairo">القاهرة (UTC+2)</SelectItem>
                  <SelectItem value="Europe/London">لندن (UTC+0)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notification Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="w-5 h-5" />
            الإشعارات
          </CardTitle>
          <CardDescription>تحكم في الإشعارات التي تتلقاها</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <SettingRow
            icon={Bell}
            title="إشعارات البريد الإلكتروني"
            description="استلام الإشعارات عبر البريد الإلكتروني"
          >
            <Switch
              checked={settings.notifications.email}
              onCheckedChange={(checked) =>
                handleSettingChange("notifications", "email", checked)
              }
            />
          </SettingRow>

          <Separator />

          <SettingRow
            icon={Smartphone}
            title="الإشعارات الفورية"
            description="استلام إشعارات فورية في المتصفح"
          >
            <Switch
              checked={settings.notifications.push}
              onCheckedChange={(checked) =>
                handleSettingChange("notifications", "push", checked)
              }
            />
          </SettingRow>

          <Separator />

          <SettingRow
            icon={Bell}
            title="تنبيهات الطلبات"
            description="إشعارات عند استلام طلبات جديدة"
          >
            <Switch
              checked={settings.notifications.orders}
              onCheckedChange={(checked) =>
                handleSettingChange("notifications", "orders", checked)
              }
            />
          </SettingRow>

          <Separator />

          <SettingRow
            icon={Database}
            title="تنبيهات المخزون"
            description="إشعارات عند انخفاض المخزون"
          >
            <Switch
              checked={settings.notifications.inventory}
              onCheckedChange={(checked) =>
                handleSettingChange("notifications", "inventory", checked)
              }
            />
          </SettingRow>
        </CardContent>
      </Card>

      {/* Security Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            الأمان
          </CardTitle>
          <CardDescription>إعدادات الأمان وحماية الحساب</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <SettingRow
            icon={Shield}
            title="المصادقة الثنائية"
            description="تفعيل طبقة إضافية من الأمان"
          >
            <Switch
              checked={settings.security.twoFactor}
              onCheckedChange={(checked) =>
                handleSettingChange("security", "twoFactor", checked)
              }
            />
          </SettingRow>

          <Separator />

          <SettingRow
            icon={Bell}
            title="تنبيهات تسجيل الدخول"
            description="إشعار عند تسجيل الدخول من جهاز جديد"
          >
            <Switch
              checked={settings.security.loginAlerts}
              onCheckedChange={(checked) =>
                handleSettingChange("security", "loginAlerts", checked)
              }
            />
          </SettingRow>

          <Separator />

          <div className="flex items-center justify-between py-4">
            <div className="flex items-center gap-4">
              <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                <Settings className="w-5 h-5 text-slate-600 dark:text-slate-400" />
              </div>
              <div>
                <p className="font-medium">مهلة الجلسة</p>
                <p className="text-sm text-muted-foreground">
                  تسجيل الخروج التلقائي بعد عدم النشاط
                </p>
              </div>
            </div>
            <Select
              value={settings.security.sessionTimeout}
              onValueChange={(value) =>
                handleSettingChange("security", "sessionTimeout", value)
              }
            >
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="15">15 دقيقة</SelectItem>
                <SelectItem value="30">30 دقيقة</SelectItem>
                <SelectItem value="60">ساعة</SelectItem>
                <SelectItem value="never">أبداً</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SettingsPage
