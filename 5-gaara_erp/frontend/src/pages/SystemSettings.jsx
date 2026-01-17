import React, { useState } from 'react';
import {
  Settings, Shield, Bell, Save, RefreshCw, Download, Upload, Eye, EyeOff, Globe, HardDrive
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const SystemSettings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState({
    general: {
      companyName: 'شركة إدارة المخزون المتقدم',
      companyEmail: 'info@inventory-system.com',
      companyPhone: '+966501234567',
      companyAddress: 'الرياض، المملكة العربية السعودية',
      defaultLanguage: 'ar',
      defaultCurrency: 'SAR',
      timezone: 'Asia/Riyadh',
      dateFormat: 'dd/mm/yyyy',
      fiscalYearStart: '01/01'
    },
    security: {
      passwordMinLength: 8,
      passwordRequireUppercase: true,
      passwordRequireNumbers: true,
      passwordRequireSymbols: true,
      sessionTimeout: 30,
      maxLoginAttempts: 5,
      twoFactorAuth: false,
      ipWhitelist: '',
      auditLogging: true
    },
    notifications: {
      emailNotifications: true,
      smsNotifications: false,
      pushNotifications: true,
      lowStockAlerts: true,
      overduePaymentAlerts: true,
      systemMaintenanceAlerts: true,
      notificationEmail: 'admin@inventory-system.com'
    },
    backup: {
      autoBackup: true,
      backupFrequency: 'daily',
      backupTime: '02:00',
      retentionDays: 30,
      cloudBackup: false,
      backupLocation: '/backups'
    },
    integration: {
      apiEnabled: true,
      webhooksEnabled: false,
      rateLimitPerHour: 1000,
      allowedOrigins: '*',
      apiVersion: 'v1'
    }
  });

  const tabs = [
    { id: 'general', label: 'عام', icon: Settings },
    { id: 'security', label: 'الأمان', icon: Shield },
    { id: 'notifications', label: 'الإشعارات', icon: Bell },
    { id: 'backup', label: 'النسخ الاحتياطي', icon: HardDrive },
    { id: 'integration', label: 'التكامل', icon: Globe }
  ];

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const handleSaveSettings = async () => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success('تم حفظ الإعدادات بنجاح');
    } catch (error) {
      toast.error('حدث خطأ أثناء حفظ الإعدادات');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetSettings = () => {
    if (window.confirm('هل أنت متأكد من إعادة تعيين الإعدادات؟')) {
      // Reset to default values
      toast.info('تم إعادة تعيين الإعدادات');
    }
  };

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            معلومات الشركة
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="companyName">اسم الشركة</Label>
              <Input
                id="companyName"
                value={settings.general.companyName}
                onChange={(e) => handleSettingChange('general', 'companyName', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="companyEmail">البريد الإلكتروني</Label>
              <Input
                id="companyEmail"
                type="email"
                value={settings.general.companyEmail}
                onChange={(e) => handleSettingChange('general', 'companyEmail', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="companyPhone">رقم الهاتف</Label>
              <Input
                id="companyPhone"
                value={settings.general.companyPhone}
                onChange={(e) => handleSettingChange('general', 'companyPhone', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="timezone">المنطقة الزمنية</Label>
              <Select value={settings.general.timezone} onValueChange={(value) => handleSettingChange('general', 'timezone', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Asia/Riyadh">الرياض (GMT+3)</SelectItem>
                  <SelectItem value="Asia/Dubai">دبي (GMT+4)</SelectItem>
                  <SelectItem value="Asia/Kuwait">الكويت (GMT+3)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label htmlFor="companyAddress">عنوان الشركة</Label>
            <Input
              id="companyAddress"
              value={settings.general.companyAddress}
              onChange={(e) => handleSettingChange('general', 'companyAddress', e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="w-5 h-5" />
            الإعدادات الإقليمية
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="defaultLanguage">اللغة الافتراضية</Label>
              <Select value={settings.general.defaultLanguage} onValueChange={(value) => handleSettingChange('general', 'defaultLanguage', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ar">العربية</SelectItem>
                  <SelectItem value="en">English</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="defaultCurrency">العملة الافتراضية</Label>
              <Select value={settings.general.defaultCurrency} onValueChange={(value) => handleSettingChange('general', 'defaultCurrency', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="SAR">ريال سعودي (SAR)</SelectItem>
                  <SelectItem value="USD">دولار أمريكي (USD)</SelectItem>
                  <SelectItem value="EUR">يورو (EUR)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="dateFormat">تنسيق التاريخ</Label>
              <Select value={settings.general.dateFormat} onValueChange={(value) => handleSettingChange('general', 'dateFormat', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="dd/mm/yyyy">يوم/شهر/سنة</SelectItem>
                  <SelectItem value="mm/dd/yyyy">شهر/يوم/سنة</SelectItem>
                  <SelectItem value="yyyy-mm-dd">سنة-شهر-يوم</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="fiscalYearStart">بداية السنة المالية</Label>
              <Input
                id="fiscalYearStart"
                value={settings.general.fiscalYearStart}
                onChange={(e) => handleSettingChange('general', 'fiscalYearStart', e.target.value)}
                placeholder="01/01"
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lock className="w-5 h-5" />
            سياسة كلمات المرور
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="passwordMinLength">الحد الأدنى لطول كلمة المرور</Label>
              <Input
                id="passwordMinLength"
                type="number"
                value={settings.security.passwordMinLength}
                onChange={(e) => handleSettingChange('security', 'passwordMinLength', parseInt(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="maxLoginAttempts">الحد الأقصى لمحاولات تسجيل الدخول</Label>
              <Input
                id="maxLoginAttempts"
                type="number"
                value={settings.security.maxLoginAttempts}
                onChange={(e) => handleSettingChange('security', 'maxLoginAttempts', parseInt(e.target.value))}
              />
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>يجب أن تحتوي على أحرف كبيرة</Label>
              <input
                type="checkbox"
                checked={settings.security.passwordRequireUppercase}
                onChange={(e) => handleSettingChange('security', 'passwordRequireUppercase', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>يجب أن تحتوي على أرقام</Label>
              <input
                type="checkbox"
                checked={settings.security.passwordRequireNumbers}
                onChange={(e) => handleSettingChange('security', 'passwordRequireNumbers', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>يجب أن تحتوي على رموز خاصة</Label>
              <input
                type="checkbox"
                checked={settings.security.passwordRequireSymbols}
                onChange={(e) => handleSettingChange('security', 'passwordRequireSymbols', e.target.checked)}
                className="rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            أمان الجلسة
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="sessionTimeout">انتهاء صلاحية الجلسة (بالدقائق)</Label>
            <Input
              id="sessionTimeout"
              type="number"
              value={settings.security.sessionTimeout}
              onChange={(e) => handleSettingChange('security', 'sessionTimeout', parseInt(e.target.value))}
            />
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>تفعيل المصادقة الثنائية</Label>
              <input
                type="checkbox"
                checked={settings.security.twoFactorAuth}
                onChange={(e) => handleSettingChange('security', 'twoFactorAuth', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>تسجيل عمليات التدقيق</Label>
              <input
                type="checkbox"
                checked={settings.security.auditLogging}
                onChange={(e) => handleSettingChange('security', 'auditLogging', e.target.checked)}
                className="rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="w-5 h-5" />
            أنواع الإشعارات
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>إشعارات البريد الإلكتروني</Label>
              <input
                type="checkbox"
                checked={settings.notifications.emailNotifications}
                onChange={(e) => handleSettingChange('notifications', 'emailNotifications', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>إشعارات الرسائل القصيرة</Label>
              <input
                type="checkbox"
                checked={settings.notifications.smsNotifications}
                onChange={(e) => handleSettingChange('notifications', 'smsNotifications', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>الإشعارات الفورية</Label>
              <input
                type="checkbox"
                checked={settings.notifications.pushNotifications}
                onChange={(e) => handleSettingChange('notifications', 'pushNotifications', e.target.checked)}
                className="rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            تنبيهات النظام
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>تنبيهات نفاد المخزون</Label>
              <input
                type="checkbox"
                checked={settings.notifications.lowStockAlerts}
                onChange={(e) => handleSettingChange('notifications', 'lowStockAlerts', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>تنبيهات المدفوعات المتأخرة</Label>
              <input
                type="checkbox"
                checked={settings.notifications.overduePaymentAlerts}
                onChange={(e) => handleSettingChange('notifications', 'overduePaymentAlerts', e.target.checked)}
                className="rounded"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>تنبيهات صيانة النظام</Label>
              <input
                type="checkbox"
                checked={settings.notifications.systemMaintenanceAlerts}
                onChange={(e) => handleSettingChange('notifications', 'systemMaintenanceAlerts', e.target.checked)}
                className="rounded"
              />
            </div>
          </div>
          
          <div>
            <Label htmlFor="notificationEmail">بريد الإشعارات</Label>
            <Input
              id="notificationEmail"
              type="email"
              value={settings.notifications.notificationEmail}
              onChange={(e) => handleSettingChange('notifications', 'notificationEmail', e.target.value)}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderBackupSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <HardDrive className="w-5 h-5" />
            النسخ الاحتياطي التلقائي
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <Label>تفعيل النسخ الاحتياطي التلقائي</Label>
            <input
              type="checkbox"
              checked={settings.backup.autoBackup}
              onChange={(e) => handleSettingChange('backup', 'autoBackup', e.target.checked)}
              className="rounded"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="backupFrequency">تكرار النسخ الاحتياطي</Label>
              <Select value={settings.backup.backupFrequency} onValueChange={(value) => handleSettingChange('backup', 'backupFrequency', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="hourly">كل ساعة</SelectItem>
                  <SelectItem value="daily">يومي</SelectItem>
                  <SelectItem value="weekly">أسبوعي</SelectItem>
                  <SelectItem value="monthly">شهري</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="backupTime">وقت النسخ الاحتياطي</Label>
              <Input
                id="backupTime"
                type="time"
                value={settings.backup.backupTime}
                onChange={(e) => handleSettingChange('backup', 'backupTime', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="retentionDays">مدة الاحتفاظ (بالأيام)</Label>
              <Input
                id="retentionDays"
                type="number"
                value={settings.backup.retentionDays}
                onChange={(e) => handleSettingChange('backup', 'retentionDays', parseInt(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="backupLocation">مجلد النسخ الاحتياطي</Label>
              <Input
                id="backupLocation"
                value={settings.backup.backupLocation}
                onChange={(e) => handleSettingChange('backup', 'backupLocation', e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <Label>النسخ الاحتياطي السحابي</Label>
            <input
              type="checkbox"
              checked={settings.backup.cloudBackup}
              onChange={(e) => handleSettingChange('backup', 'cloudBackup', e.target.checked)}
              className="rounded"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderIntegrationSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="w-5 h-5" />
            إعدادات API
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <Label>تفعيل API</Label>
            <input
              type="checkbox"
              checked={settings.integration.apiEnabled}
              onChange={(e) => handleSettingChange('integration', 'apiEnabled', e.target.checked)}
              className="rounded"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="rateLimitPerHour">حد الطلبات في الساعة</Label>
              <Input
                id="rateLimitPerHour"
                type="number"
                value={settings.integration.rateLimitPerHour}
                onChange={(e) => handleSettingChange('integration', 'rateLimitPerHour', parseInt(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="apiVersion">إصدار API</Label>
              <Select value={settings.integration.apiVersion} onValueChange={(value) => handleSettingChange('integration', 'apiVersion', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="v1">الإصدار 1</SelectItem>
                  <SelectItem value="v2">الإصدار 2</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div>
            <Label htmlFor="allowedOrigins">المصادر المسموحة</Label>
            <Input
              id="allowedOrigins"
              value={settings.integration.allowedOrigins}
              onChange={(e) => handleSettingChange('integration', 'allowedOrigins', e.target.value)}
              placeholder="* أو قائمة بالمصادر مفصولة بفواصل"
            />
          </div>
          
          <div className="flex items-center justify-between">
            <Label>تفعيل Webhooks</Label>
            <input
              type="checkbox"
              checked={settings.integration.webhooksEnabled}
              onChange={(e) => handleSettingChange('integration', 'webhooksEnabled', e.target.checked)}
              className="rounded"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return renderGeneralSettings();
      case 'security':
        return renderSecuritySettings();
      case 'notifications':
        return renderNotificationSettings();
      case 'backup':
        return renderBackupSettings();
      case 'integration':
        return renderIntegrationSettings();
      default:
        return renderGeneralSettings();
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إعدادات النظام</h1>
          <p className="text-muted-foreground mt-1">إدارة إعدادات النظام والتكوين العام</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleResetSettings} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            إعادة تعيين
          </Button>
          <Button onClick={handleSaveSettings} disabled={isLoading}>
            <Save className="w-4 h-4 mr-2" />
            {isLoading ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <Card>
        <CardContent className="p-0">
          <div className="flex border-b">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary/100 text-primary bg-primary/10'
                      : 'border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/50'
                  }`}
                >
                  <IconComponent className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Tab Content */}
      {renderTabContent()}
    </div>
  );
};

export default SystemSettings;

