/**
 * Notification Settings Page
 * صفحة إعدادات الإشعارات
 * 
 * @file frontend/src/pages/NotificationSettings.jsx
 * @author Store ERP v2.0.0
 */

import React, { useState, useEffect } from 'react';
import {
  Bell, Mail, MessageSquare, Smartphone, Volume2, VolumeX,
  Save, RefreshCw, Clock, AlertTriangle, Package, DollarSign,
  Users, Calendar, Shield, CheckCircle
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

/**
 * Toggle Switch Component
 */
const Toggle = ({ enabled, onChange, label, description }) => (
  <div className="flex items-center justify-between py-3 border-b border-border last:border-0">
    <div className="flex-1">
      <span className="font-medium text-foreground">{label}</span>
      {description && (
        <p className="text-sm text-muted-foreground mt-0.5">{description}</p>
      )}
    </div>
    <button
      type="button"
      onClick={() => onChange(!enabled)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
        enabled ? 'bg-primary' : 'bg-muted'
      }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
          enabled ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  </div>
);

/**
 * صفحة إعدادات الإشعارات
 */
const NotificationSettings = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [settings, setSettings] = useState({
    // قنوات الإشعارات
    channels: {
      email: true,
      sms: false,
      push: true,
      inApp: true
    },
    // إعدادات البريد الإلكتروني
    email: {
      address: '',
      ccAddresses: '',
      dailyDigest: false,
      digestTime: '08:00'
    },
    // إعدادات الرسائل القصيرة
    sms: {
      phoneNumber: '',
      criticalOnly: true
    },
    // إشعارات المخزون
    inventory: {
      lowStock: true,
      lowStockThreshold: 10,
      outOfStock: true,
      expiryAlerts: true,
      expiryDays: 30
    },
    // إشعارات المالية
    financial: {
      newSales: true,
      largeTransactions: true,
      largeTransactionAmount: 10000,
      overduePayments: true,
      dailySummary: true
    },
    // إشعارات النظام
    system: {
      securityAlerts: true,
      backupComplete: true,
      maintenanceScheduled: true,
      systemErrors: true,
      userActivity: false
    },
    // إعدادات الوقت
    timing: {
      quietHoursEnabled: false,
      quietHoursStart: '22:00',
      quietHoursEnd: '07:00',
      timezone: 'Asia/Riyadh'
    },
    // الأصوات
    sounds: {
      enabled: true,
      volume: 70,
      newNotificationSound: 'default'
    }
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/settings/notifications');
      if (response.status === 'success' && response.data) {
        setSettings(prev => ({ ...prev, ...response.data }));
      }
    } catch (error) {
      console.log('Using default settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await apiClient.put('/api/settings/notifications', settings);
      toast.success('تم حفظ إعدادات الإشعارات بنجاح');
    } catch (error) {
      toast.error('فشل حفظ الإعدادات');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    if (window.confirm('هل أنت متأكد من إعادة تعيين الإعدادات الافتراضية؟')) {
      fetchSettings();
      toast.success('تم إعادة تعيين الإعدادات');
    }
  };

  const updateSetting = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل الإعدادات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Bell className="w-8 h-8" />
            إعدادات الإشعارات
          </h1>
          <p className="text-muted-foreground mt-1">إدارة طريقة تلقي الإشعارات والتنبيهات</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            إعادة تعيين
          </button>
          <button 
            onClick={handleSave}
            disabled={isSaving}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* قنوات الإشعارات */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              قنوات الإشعارات
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Toggle
              enabled={settings.channels.email}
              onChange={(v) => updateSetting('channels', 'email', v)}
              label="البريد الإلكتروني"
              description="استلام الإشعارات عبر البريد"
            />
            <Toggle
              enabled={settings.channels.sms}
              onChange={(v) => updateSetting('channels', 'sms', v)}
              label="الرسائل القصيرة (SMS)"
              description="استلام التنبيهات المهمة عبر SMS"
            />
            <Toggle
              enabled={settings.channels.push}
              onChange={(v) => updateSetting('channels', 'push', v)}
              label="إشعارات الدفع"
              description="إشعارات فورية على المتصفح"
            />
            <Toggle
              enabled={settings.channels.inApp}
              onChange={(v) => updateSetting('channels', 'inApp', v)}
              label="داخل التطبيق"
              description="إشعارات داخل النظام"
            />
          </CardContent>
        </Card>

        {/* إعدادات البريد الإلكتروني */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="w-5 h-5" />
              إعدادات البريد الإلكتروني
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="email">البريد الإلكتروني الرئيسي</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@company.com"
                value={settings.email.address}
                onChange={(e) => updateSetting('email', 'address', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="ccEmails">نسخة إلى (CC)</Label>
              <Input
                id="ccEmails"
                placeholder="email1@company.com, email2@company.com"
                value={settings.email.ccAddresses}
                onChange={(e) => updateSetting('email', 'ccAddresses', e.target.value)}
              />
              <p className="text-xs text-muted-foreground mt-1">افصل بين العناوين بفاصلة</p>
            </div>
            <Toggle
              enabled={settings.email.dailyDigest}
              onChange={(v) => updateSetting('email', 'dailyDigest', v)}
              label="ملخص يومي"
              description="استلام ملخص يومي بدلاً من إشعارات متفرقة"
            />
            {settings.email.dailyDigest && (
              <div>
                <Label htmlFor="digestTime">وقت الملخص</Label>
                <Input
                  id="digestTime"
                  type="time"
                  value={settings.email.digestTime}
                  onChange={(e) => updateSetting('email', 'digestTime', e.target.value)}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* إشعارات المخزون */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="w-5 h-5" />
              إشعارات المخزون
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Toggle
              enabled={settings.inventory.lowStock}
              onChange={(v) => updateSetting('inventory', 'lowStock', v)}
              label="تنبيه انخفاض المخزون"
              description="تنبيه عند وصول المنتج للحد الأدنى"
            />
            {settings.inventory.lowStock && (
              <div>
                <Label htmlFor="lowStockThreshold">الحد الأدنى للتنبيه</Label>
                <Input
                  id="lowStockThreshold"
                  type="number"
                  min="1"
                  value={settings.inventory.lowStockThreshold}
                  onChange={(e) => updateSetting('inventory', 'lowStockThreshold', parseInt(e.target.value))}
                />
              </div>
            )}
            <Toggle
              enabled={settings.inventory.outOfStock}
              onChange={(v) => updateSetting('inventory', 'outOfStock', v)}
              label="تنبيه نفاد المخزون"
              description="تنبيه عند نفاد المنتج من المخزون"
            />
            <Toggle
              enabled={settings.inventory.expiryAlerts}
              onChange={(v) => updateSetting('inventory', 'expiryAlerts', v)}
              label="تنبيه انتهاء الصلاحية"
              description="تنبيه قبل انتهاء صلاحية اللوتات"
            />
            {settings.inventory.expiryAlerts && (
              <div>
                <Label htmlFor="expiryDays">أيام قبل الانتهاء</Label>
                <Select
                  value={String(settings.inventory.expiryDays)}
                  onValueChange={(v) => updateSetting('inventory', 'expiryDays', parseInt(v))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="7">7 أيام</SelectItem>
                    <SelectItem value="14">14 يوم</SelectItem>
                    <SelectItem value="30">30 يوم</SelectItem>
                    <SelectItem value="60">60 يوم</SelectItem>
                    <SelectItem value="90">90 يوم</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}
          </CardContent>
        </Card>

        {/* إشعارات المالية */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="w-5 h-5" />
              إشعارات المالية
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Toggle
              enabled={settings.financial.newSales}
              onChange={(v) => updateSetting('financial', 'newSales', v)}
              label="عمليات البيع الجديدة"
              description="إشعار عند كل عملية بيع جديدة"
            />
            <Toggle
              enabled={settings.financial.largeTransactions}
              onChange={(v) => updateSetting('financial', 'largeTransactions', v)}
              label="المعاملات الكبيرة"
              description="تنبيه عند المعاملات التي تتجاوز مبلغ معين"
            />
            {settings.financial.largeTransactions && (
              <div>
                <Label htmlFor="largeAmount">الحد الأدنى للمبلغ (ج.م)</Label>
                <Input
                  id="largeAmount"
                  type="number"
                  min="0"
                  step="1000"
                  value={settings.financial.largeTransactionAmount}
                  onChange={(e) => updateSetting('financial', 'largeTransactionAmount', parseInt(e.target.value))}
                />
              </div>
            )}
            <Toggle
              enabled={settings.financial.overduePayments}
              onChange={(v) => updateSetting('financial', 'overduePayments', v)}
              label="المدفوعات المتأخرة"
              description="تنبيه عند تأخر سداد الفواتير"
            />
            <Toggle
              enabled={settings.financial.dailySummary}
              onChange={(v) => updateSetting('financial', 'dailySummary', v)}
              label="ملخص مالي يومي"
              description="تقرير يومي بإجمالي المبيعات والمصروفات"
            />
          </CardContent>
        </Card>

        {/* إشعارات النظام */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              إشعارات النظام
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Toggle
              enabled={settings.system.securityAlerts}
              onChange={(v) => updateSetting('system', 'securityAlerts', v)}
              label="تنبيهات الأمان"
              description="محاولات تسجيل دخول فاشلة وتغييرات أمنية"
            />
            <Toggle
              enabled={settings.system.backupComplete}
              onChange={(v) => updateSetting('system', 'backupComplete', v)}
              label="اكتمال النسخ الاحتياطي"
              description="إشعار عند اكتمال النسخ الاحتياطي"
            />
            <Toggle
              enabled={settings.system.maintenanceScheduled}
              onChange={(v) => updateSetting('system', 'maintenanceScheduled', v)}
              label="صيانة مجدولة"
              description="تنبيه قبل فترات الصيانة المجدولة"
            />
            <Toggle
              enabled={settings.system.systemErrors}
              onChange={(v) => updateSetting('system', 'systemErrors', v)}
              label="أخطاء النظام"
              description="تنبيه عند حدوث أخطاء في النظام"
            />
            <Toggle
              enabled={settings.system.userActivity}
              onChange={(v) => updateSetting('system', 'userActivity', v)}
              label="نشاط المستخدمين"
              description="إشعارات تسجيل الدخول/الخروج"
            />
          </CardContent>
        </Card>

        {/* ساعات الهدوء */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              ساعات الهدوء
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Toggle
              enabled={settings.timing.quietHoursEnabled}
              onChange={(v) => updateSetting('timing', 'quietHoursEnabled', v)}
              label="تفعيل ساعات الهدوء"
              description="إيقاف الإشعارات غير الحرجة خلال أوقات محددة"
            />
            {settings.timing.quietHoursEnabled && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="quietStart">من الساعة</Label>
                  <Input
                    id="quietStart"
                    type="time"
                    value={settings.timing.quietHoursStart}
                    onChange={(e) => updateSetting('timing', 'quietHoursStart', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="quietEnd">إلى الساعة</Label>
                  <Input
                    id="quietEnd"
                    type="time"
                    value={settings.timing.quietHoursEnd}
                    onChange={(e) => updateSetting('timing', 'quietHoursEnd', e.target.value)}
                  />
                </div>
              </div>
            )}
            <div>
              <Label htmlFor="timezone">المنطقة الزمنية</Label>
              <Select
                value={settings.timing.timezone}
                onValueChange={(v) => updateSetting('timing', 'timezone', v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Asia/Riyadh">الرياض (GMT+3)</SelectItem>
                  <SelectItem value="Asia/Dubai">دبي (GMT+4)</SelectItem>
                  <SelectItem value="Asia/Kuwait">الكويت (GMT+3)</SelectItem>
                  <SelectItem value="Africa/Cairo">القاهرة (GMT+2)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* إعدادات الصوت */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {settings.sounds.enabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
              إعدادات الصوت
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Toggle
              enabled={settings.sounds.enabled}
              onChange={(v) => updateSetting('sounds', 'enabled', v)}
              label="تفعيل الأصوات"
              description="تشغيل صوت عند وصول إشعار جديد"
            />
            {settings.sounds.enabled && (
              <>
                <div>
                  <Label htmlFor="volume">مستوى الصوت: {settings.sounds.volume}%</Label>
                  <input
                    id="volume"
                    type="range"
                    min="0"
                    max="100"
                    value={settings.sounds.volume}
                    onChange={(e) => updateSetting('sounds', 'volume', parseInt(e.target.value))}
                    className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer"
                  />
                </div>
                <div>
                  <Label htmlFor="soundType">نوع الصوت</Label>
                  <Select
                    value={settings.sounds.newNotificationSound}
                    onValueChange={(v) => updateSetting('sounds', 'newNotificationSound', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="default">الافتراضي</SelectItem>
                      <SelectItem value="chime">رنين</SelectItem>
                      <SelectItem value="bell">جرس</SelectItem>
                      <SelectItem value="pop">فقاعة</SelectItem>
                      <SelectItem value="none">بدون صوت</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Summary */}
      <Card className="bg-muted/50">
        <CardContent className="p-4">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span className="text-sm">
                القنوات النشطة: {Object.values(settings.channels).filter(Boolean).length}/4
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Bell className="w-4 h-4 text-blue-500" />
              <span className="text-sm">
                إشعارات المخزون: {settings.inventory.lowStock || settings.inventory.outOfStock || settings.inventory.expiryAlerts ? 'مفعلة' : 'معطلة'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-yellow-500" />
              <span className="text-sm">
                ساعات الهدوء: {settings.timing.quietHoursEnabled ? `${settings.timing.quietHoursStart} - ${settings.timing.quietHoursEnd}` : 'معطلة'}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default NotificationSettings;
