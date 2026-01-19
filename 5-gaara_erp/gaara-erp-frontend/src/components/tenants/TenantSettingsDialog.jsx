/**
 * Tenant Settings Dialog - حوار إعدادات المستأجر
 * Gaara ERP v12
 *
 * Dialog component for managing tenant-specific settings.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 * @created 2026-01-17
 */

import { useState, useEffect, useCallback } from 'react'
import { toast } from 'sonner'
import {
  Settings,
  Save,
  Loader2,
  Palette,
  Globe,
  Bell,
  Shield,
  Mail,
  Phone,
  MapPin,
  Building,
  Clock,
  Languages,
  RefreshCw,
} from 'lucide-react'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

import tenantService from '@/services/tenantService'

/**
 * Default settings structure
 */
const defaultSettings = {
  // General
  language: 'ar',
  timezone: 'Asia/Riyadh',
  date_format: 'DD/MM/YYYY',
  currency: 'SAR',

  // Branding
  theme: 'light',
  primary_color: '#0ea5e9',
  logo_url: '',

  // Notifications
  email_notifications: true,
  sms_notifications: false,
  push_notifications: true,

  // Security
  require_2fa: false,
  session_timeout: 60,
  password_expiry_days: 90,
  ip_whitelist: '',

  // Contact
  support_email: '',
  support_phone: '',
  address: '',
}

/**
 * Timezone options
 */
const timezones = [
  { value: 'Asia/Riyadh', label: 'الرياض (GMT+3)' },
  { value: 'Asia/Dubai', label: 'دبي (GMT+4)' },
  { value: 'Asia/Kuwait', label: 'الكويت (GMT+3)' },
  { value: 'Africa/Cairo', label: 'القاهرة (GMT+2)' },
  { value: 'Europe/London', label: 'لندن (GMT+0)' },
  { value: 'America/New_York', label: 'نيويورك (GMT-5)' },
]

/**
 * Currency options
 */
const currencies = [
  { value: 'SAR', label: 'ريال سعودي (SAR)' },
  { value: 'AED', label: 'درهم إماراتي (AED)' },
  { value: 'KWD', label: 'دينار كويتي (KWD)' },
  { value: 'EGP', label: 'جنيه مصري (EGP)' },
  { value: 'USD', label: 'دولار أمريكي (USD)' },
  { value: 'EUR', label: 'يورو (EUR)' },
]

/**
 * Tenant Settings Dialog Component
 *
 * @param {Object} props
 * @param {Object} props.tenant - Tenant object
 * @param {boolean} props.open - Dialog open state
 * @param {Function} props.onClose - Close handler
 * @param {Function} props.onUpdate - Update callback
 */
export function TenantSettingsDialog({ tenant, open, onClose, onUpdate }) {
  // State
  const [settings, setSettings] = useState(defaultSettings)
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)
  const [activeTab, setActiveTab] = useState('general')

  /**
   * Load tenant settings
   */
  const loadSettings = useCallback(async () => {
    if (!tenant?.id) return

    setIsLoading(true)
    try {
      const response = await tenantService.getTenantSettings(tenant.id)
      if (response.success && response.data) {
        setSettings({ ...defaultSettings, ...response.data })
      }
    } catch (error) {
      console.error('Error loading settings:', error)
      toast.error('فشل في تحميل الإعدادات')
    } finally {
      setIsLoading(false)
    }
  }, [tenant?.id])

  // Load settings when dialog opens
  useEffect(() => {
    if (open && tenant?.id) {
      loadSettings()
      setHasChanges(false)
    }
  }, [open, tenant?.id, loadSettings])

  /**
   * Update a setting value
   */
  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
    setHasChanges(true)
  }

  /**
   * Save settings
   */
  const handleSave = async () => {
    if (!tenant?.id) return

    setIsSaving(true)
    try {
      const response = await tenantService.updateTenantSettings(tenant.id, settings)

      if (response.success) {
        toast.success('تم حفظ الإعدادات بنجاح')
        setHasChanges(false)
        onUpdate?.()
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (error) {
      console.error('Error saving settings:', error)
      toast.error(error.message_ar || 'فشل في حفظ الإعدادات')
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Reset to defaults
   */
  const handleReset = () => {
    setSettings(defaultSettings)
    setHasChanges(true)
    toast.info('تم إعادة تعيين الإعدادات للقيم الافتراضية')
  }

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[85vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            إعدادات المستأجر
          </DialogTitle>
          <DialogDescription>
            إعدادات {tenant?.name_ar || tenant?.name}
          </DialogDescription>
        </DialogHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="general">عام</TabsTrigger>
              <TabsTrigger value="branding">المظهر</TabsTrigger>
              <TabsTrigger value="notifications">الإشعارات</TabsTrigger>
              <TabsTrigger value="security">الأمان</TabsTrigger>
            </TabsList>

            {/* General Settings */}
            <TabsContent value="general" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Globe className="w-4 h-4" />
                    الإعدادات الإقليمية
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>اللغة</Label>
                      <Select
                        value={settings.language}
                        onValueChange={(v) => updateSetting('language', v)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="ar">العربية</SelectItem>
                          <SelectItem value="en">English</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>المنطقة الزمنية</Label>
                      <Select
                        value={settings.timezone}
                        onValueChange={(v) => updateSetting('timezone', v)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {timezones.map(tz => (
                            <SelectItem key={tz.value} value={tz.value}>{tz.label}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>العملة</Label>
                      <Select
                        value={settings.currency}
                        onValueChange={(v) => updateSetting('currency', v)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {currencies.map(c => (
                            <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>تنسيق التاريخ</Label>
                      <Select
                        value={settings.date_format}
                        onValueChange={(v) => updateSetting('date_format', v)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="DD/MM/YYYY">DD/MM/YYYY</SelectItem>
                          <SelectItem value="MM/DD/YYYY">MM/DD/YYYY</SelectItem>
                          <SelectItem value="YYYY-MM-DD">YYYY-MM-DD</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Building className="w-4 h-4" />
                    معلومات الاتصال
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>بريد الدعم</Label>
                      <Input
                        type="email"
                        value={settings.support_email}
                        onChange={(e) => updateSetting('support_email', e.target.value)}
                        placeholder="support@company.com"
                        dir="ltr"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>هاتف الدعم</Label>
                      <Input
                        value={settings.support_phone}
                        onChange={(e) => updateSetting('support_phone', e.target.value)}
                        placeholder="+966 XX XXX XXXX"
                        dir="ltr"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>العنوان</Label>
                    <Input
                      value={settings.address}
                      onChange={(e) => updateSetting('address', e.target.value)}
                      placeholder="العنوان الكامل"
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Branding Settings */}
            <TabsContent value="branding" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Palette className="w-4 h-4" />
                    المظهر والألوان
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>السمة</Label>
                      <Select
                        value={settings.theme}
                        onValueChange={(v) => updateSetting('theme', v)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="light">فاتح</SelectItem>
                          <SelectItem value="dark">داكن</SelectItem>
                          <SelectItem value="system">تلقائي</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>اللون الرئيسي</Label>
                      <div className="flex gap-2">
                        <Input
                          type="color"
                          value={settings.primary_color}
                          onChange={(e) => updateSetting('primary_color', e.target.value)}
                          className="w-12 h-10 p-1 cursor-pointer"
                        />
                        <Input
                          value={settings.primary_color}
                          onChange={(e) => updateSetting('primary_color', e.target.value)}
                          placeholder="#0ea5e9"
                          dir="ltr"
                          className="flex-1"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>رابط الشعار</Label>
                    <Input
                      value={settings.logo_url}
                      onChange={(e) => updateSetting('logo_url', e.target.value)}
                      placeholder="https://example.com/logo.png"
                      dir="ltr"
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Notifications Settings */}
            <TabsContent value="notifications" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Bell className="w-4 h-4" />
                    إعدادات الإشعارات
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>إشعارات البريد الإلكتروني</Label>
                      <p className="text-sm text-muted-foreground">استلام الإشعارات عبر البريد</p>
                    </div>
                    <Switch
                      checked={settings.email_notifications}
                      onCheckedChange={(v) => updateSetting('email_notifications', v)}
                    />
                  </div>

                  <Separator />

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>إشعارات SMS</Label>
                      <p className="text-sm text-muted-foreground">استلام الإشعارات عبر الرسائل النصية</p>
                    </div>
                    <Switch
                      checked={settings.sms_notifications}
                      onCheckedChange={(v) => updateSetting('sms_notifications', v)}
                    />
                  </div>

                  <Separator />

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>إشعارات التطبيق</Label>
                      <p className="text-sm text-muted-foreground">إشعارات فورية في المتصفح</p>
                    </div>
                    <Switch
                      checked={settings.push_notifications}
                      onCheckedChange={(v) => updateSetting('push_notifications', v)}
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Security Settings */}
            <TabsContent value="security" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    إعدادات الأمان
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>التحقق الثنائي (2FA)</Label>
                      <p className="text-sm text-muted-foreground">طلب التحقق الثنائي لجميع المستخدمين</p>
                    </div>
                    <Switch
                      checked={settings.require_2fa}
                      onCheckedChange={(v) => updateSetting('require_2fa', v)}
                    />
                  </div>

                  <Separator />

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>مهلة الجلسة (بالدقائق)</Label>
                      <Input
                        type="number"
                        value={settings.session_timeout}
                        onChange={(e) => updateSetting('session_timeout', parseInt(e.target.value) || 60)}
                        min={15}
                        max={480}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label>انتهاء كلمة المرور (بالأيام)</Label>
                      <Input
                        type="number"
                        value={settings.password_expiry_days}
                        onChange={(e) => updateSetting('password_expiry_days', parseInt(e.target.value) || 90)}
                        min={0}
                        max={365}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>قائمة IP البيضاء (اختياري)</Label>
                    <Input
                      value={settings.ip_whitelist}
                      onChange={(e) => updateSetting('ip_whitelist', e.target.value)}
                      placeholder="192.168.1.1, 10.0.0.0/24"
                      dir="ltr"
                    />
                    <p className="text-xs text-muted-foreground">
                      فصل العناوين بفواصل. اتركه فارغاً للسماح بجميع العناوين.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        <DialogFooter className="gap-2">
          <Button
            variant="outline"
            onClick={handleReset}
            disabled={isSaving}
          >
            <RefreshCw className="w-4 h-4 ml-2" />
            إعادة تعيين
          </Button>
          <Button variant="outline" onClick={onClose} disabled={isSaving}>
            إلغاء
          </Button>
          <Button onClick={handleSave} disabled={isSaving || !hasChanges}>
            {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
            <Save className="w-4 h-4 ml-2" />
            حفظ الإعدادات
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default TenantSettingsDialog
