// /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/SetupWizard.jsx

import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, Upload, Settings, CheckCircle, XCircle, AlertTriangle, Package, User, Calendar, Clock,
  Building as BusinessIcon, User as PersonIcon, Settings as SettingsIcon, Database as StorageIcon, Shield as SecurityIcon, CheckCircle as CheckCircleIcon
} from 'lucide-react';

const SetupWizard = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [setupProgress, setSetupProgress] = useState(0);
  const [errors, setErrors] = useState({});
  // const [showConfirmDialog, setShowConfirmDialog] = useState(false); // Currently unused

  // بيانات الشركة
  const [companyData, setCompanyData] = useState({
    name: '',
    address: '',
    phone: '',
    email: '',
    website: '',
    taxNumber: '',
    industry: '',
    size: '',
    logo: null
  });

  // بيانات المدير الأول
  const [adminData, setAdminData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    phone: '',
    role: 'admin'
  });

  // إعدادات النظام
  const [systemSettings, setSystemSettings] = useState({
    language: 'ar',
    currency: 'EGP',
    timezone: 'Africa/Cairo',
    dateFormat: 'DD/MM/YYYY',
    theme: 'light',
    enableNotifications: true,
    enableBackups: true,
    backupFrequency: 'daily'
  });

  // إعدادات قاعدة البيانات
  const [databaseSettings, setDatabaseSettings] = useState({
    type: 'sqlite',
    host: 'localhost',
    port: '',
    name: 'inventory_system',
    username: '',
    password: '',
    enableSSL: false
  });

  const steps = [
    {
      id: 0,
      title: 'معلومات الشركة',
      description: 'أدخل المعلومات الأساسية للشركة',
      icon: BusinessIcon,
      component: 'CompanyInfo'
    },
    {
      id: 1,
      title: 'حساب المدير',
      description: 'إنشاء حساب المدير الأول',
      icon: PersonIcon,
      component: 'AdminAccount'
    },
    {
      id: 2,
      title: 'إعدادات النظام',
      description: 'تكوين الإعدادات العامة للنظام',
      icon: SettingsIcon,
      component: 'SystemSettings'
    },
    {
      id: 3,
      title: 'قاعدة البيانات',
      description: 'تكوين اتصال قاعدة البيانات',
      icon: StorageIcon,
      component: 'DatabaseConfig'
    },
    {
      id: 4,
      title: 'الأمان',
      description: 'إعدادات الأمان والصلاحيات',
      icon: SecurityIcon,
      component: 'SecuritySettings'
    },
    {
      id: 5,
      title: 'اكتمال الإعداد',
      description: 'مراجعة نهائية وإكمال الإعداد',
      icon: CheckCircleIcon,
      component: 'Completion'
    }
  ];

  // التحقق من صحة البيانات
  const validateStep = (stepIndex) => {
    const newErrors = {};
    
    switch (stepIndex) {
      case 0: // معلومات الشركة
        if (!companyData.name.trim()) newErrors.companyName = 'اسم الشركة مطلوب';
        if (!companyData.email.trim()) newErrors.companyEmail = 'البريد الإلكتروني مطلوب';
        if (!companyData.phone.trim()) newErrors.companyPhone = 'رقم الهاتف مطلوب';
        break;
        
      case 1: // حساب المدير
        if (!adminData.firstName.trim()) newErrors.firstName = 'الاسم الأول مطلوب';
        if (!adminData.lastName.trim()) newErrors.lastName = 'الاسم الأخير مطلوب';
        if (!adminData.email.trim()) newErrors.adminEmail = 'البريد الإلكتروني مطلوب';
        if (!adminData.username.trim()) newErrors.username = 'اسم المستخدم مطلوب';
        if (!adminData.password.trim()) newErrors.password = 'كلمة المرور مطلوبة';
        if (adminData.password !== adminData.confirmPassword) {
          newErrors.confirmPassword = 'كلمات المرور غير متطابقة';
        }
        break;
        
      case 3: // قاعدة البيانات
        if (databaseSettings.type !== 'sqlite') {
          if (!databaseSettings.host.trim()) newErrors.dbHost = 'عنوان الخادم مطلوب';
          if (!databaseSettings.name.trim()) newErrors.dbName = 'اسم قاعدة البيانات مطلوب';
        }
        break;
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // الانتقال للخطوة التالية
  const handleNext = () => {
    if (validateStep(activeStep)) {
      if (activeStep < steps.length - 1) {
        setActiveStep(activeStep + 1);
        setSetupProgress(((activeStep + 1) / steps.length) * 100);
      }
    }
  };

  // الانتقال للخطوة السابقة
  const handleBack = () => {
    if (activeStep > 0) {
      setActiveStep(activeStep - 1);
      setSetupProgress((activeStep / steps.length) * 100);
    }
  };

  // إكمال الإعداد
  const handleComplete = async () => {
    setLoading(true);
    try {
      const setupData = {
        company: companyData,
        admin: adminData,
        system: systemSettings,
        database: databaseSettings
      };

      const response = await fetch('/api/setup/complete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(setupData)
      });

      if (response.ok) {
        setSetupProgress(100);
        // إعادة توجيه إلى لوحة التحكم
        setTimeout(() => {
          window.location.href = '/dashboard';
        }, 2000);
      } else {
        throw new Error('فشل في إكمال الإعداد');
      }
    } catch (error) {
      setErrors({ general: 'حدث خطأ أثناء إكمال الإعداد' });
    } finally {
      setLoading(false);
    }
  };

  // مكون معلومات الشركة
  const CompanyInfoStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <BusinessIcon className="mx-auto h-16 w-16 text-primary mb-4" />
        <h2 className="text-2xl font-bold text-foreground">معلومات الشركة</h2>
        <p className="text-muted-foreground mt-2">أدخل المعلومات الأساسية لشركتك</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            اسم الشركة *
          </label>
          <input
            type="text"
            value={companyData.name}
            onChange={(e) => setCompanyData({...companyData, name: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/100"
            placeholder="أدخل اسم الشركة"
          />
          {errors.companyName && (
            <p className="text-red-500 text-sm mt-1">{errors.companyName}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            البريد الإلكتروني *
          </label>
          <input
            type="email"
            value={companyData.email}
            onChange={(e) => setCompanyData({...companyData, email: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/100"
            placeholder="company@example.com"
          />
          {errors.companyEmail && (
            <p className="text-red-500 text-sm mt-1">{errors.companyEmail}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            رقم الهاتف *
          </label>
          <input
            type="tel"
            value={companyData.phone}
            onChange={(e) => setCompanyData({...companyData, phone: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/100"
            placeholder="+20 xxx xxx xxxx"
          />
          {errors.companyPhone && (
            <p className="text-red-500 text-sm mt-1">{errors.companyPhone}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            الموقع الإلكتروني
          </label>
          <input
            type="url"
            value={companyData.website}
            onChange={(e) => setCompanyData({...companyData, website: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/100"
            placeholder="https://www.example.com"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-foreground mb-2">
            العنوان
          </label>
          <textarea
            value={companyData.address}
            onChange={(e) => setCompanyData({...companyData, address: e.target.value})}
            rows={3}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/100"
            placeholder="أدخل عنوان الشركة"
          />
        </div>
      </div>
    </div>
  );

  // مكون حساب المدير
  const AdminAccountStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <PersonIcon className="mx-auto h-16 w-16 text-primary mb-4" />
        <h2 className="text-2xl font-bold text-foreground">حساب المدير الأول</h2>
        <p className="text-muted-foreground mt-2">إنشاء حساب المدير الرئيسي للنظام</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            الاسم الأول *
          </label>
          <input
            type="text"
            value={adminData.firstName}
            onChange={(e) => setAdminData({...adminData, firstName: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="أدخل الاسم الأول"
          />
          {errors.firstName && (
            <p className="text-red-500 text-sm mt-1">{errors.firstName}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            الاسم الأخير *
          </label>
          <input
            type="text"
            value={adminData.lastName}
            onChange={(e) => setAdminData({...adminData, lastName: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="أدخل الاسم الأخير"
          />
          {errors.lastName && (
            <p className="text-red-500 text-sm mt-1">{errors.lastName}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            البريد الإلكتروني *
          </label>
          <input
            type="email"
            value={adminData.email}
            onChange={(e) => setAdminData({...adminData, email: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="admin@example.com"
          />
          {errors.adminEmail && (
            <p className="text-red-500 text-sm mt-1">{errors.adminEmail}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            اسم المستخدم *
          </label>
          <input
            type="text"
            value={adminData.username}
            onChange={(e) => setAdminData({...adminData, username: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="admin"
          />
          {errors.username && (
            <p className="text-red-500 text-sm mt-1">{errors.username}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            كلمة المرور *
          </label>
          <input
            type="password"
            value={adminData.password}
            onChange={(e) => setAdminData({...adminData, password: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="أدخل كلمة مرور قوية"
          />
          {errors.password && (
            <p className="text-red-500 text-sm mt-1">{errors.password}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            تأكيد كلمة المرور *
          </label>
          <input
            type="password"
            value={adminData.confirmPassword}
            onChange={(e) => setAdminData({...adminData, confirmPassword: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="أعد إدخال كلمة المرور"
          />
          {errors.confirmPassword && (
            <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>
          )}
        </div>
      </div>
    </div>
  );

  // مكون إعدادات النظام
  const SystemSettingsStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <SettingsIcon className="mx-auto h-16 w-16 text-purple-600 mb-4" />
        <h2 className="text-2xl font-bold text-foreground">إعدادات النظام</h2>
        <p className="text-muted-foreground mt-2">تكوين الإعدادات العامة للنظام</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            اللغة الافتراضية
          </label>
          <select
            value={systemSettings.language}
            onChange={(e) => setSystemSettings({...systemSettings, language: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="ar">العربية</option>
            <option value="en">English</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            العملة الافتراضية
          </label>
          <select
            value={systemSettings.currency}
            onChange={(e) => setSystemSettings({...systemSettings, currency: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="EGP">جنيه مصري (EGP)</option>
            <option value="USD">دولار أمريكي (USD)</option>
            <option value="EUR">يورو (EUR)</option>
            <option value="EGP">ريال سعودي (EGP)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            المنطقة الزمنية
          </label>
          <select
            value={systemSettings.timezone}
            onChange={(e) => setSystemSettings({...systemSettings, timezone: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="Africa/Cairo">القاهرة (GMT+2)</option>
            <option value="Asia/Riyadh">الرياض (GMT+3)</option>
            <option value="Asia/Dubai">دبي (GMT+4)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            تنسيق التاريخ
          </label>
          <select
            value={systemSettings.dateFormat}
            onChange={(e) => setSystemSettings({...systemSettings, dateFormat: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="DD/MM/YYYY">DD/MM/YYYY</option>
            <option value="MM/DD/YYYY">MM/DD/YYYY</option>
            <option value="YYYY-MM-DD">YYYY-MM-DD</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-foreground">تفعيل الإشعارات</h3>
            <p className="text-sm text-muted-foreground">استقبال إشعارات النظام والتنبيهات</p>
          </div>
          <input
            type="checkbox"
            checked={systemSettings.enableNotifications}
            onChange={(e) => setSystemSettings({...systemSettings, enableNotifications: e.target.checked})}
            className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-border rounded"
          />
        </div>

        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-foreground">النسخ الاحتياطي التلقائي</h3>
            <p className="text-sm text-muted-foreground">إنشاء نسخ احتياطية تلقائية من البيانات</p>
          </div>
          <input
            type="checkbox"
            checked={systemSettings.enableBackups}
            onChange={(e) => setSystemSettings({...systemSettings, enableBackups: e.target.checked})}
            className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-border rounded"
          />
        </div>
      </div>
    </div>
  );

  // مكون إعدادات قاعدة البيانات
  const DatabaseConfigStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <StorageIcon className="mx-auto h-16 w-16 text-indigo-600 mb-4" />
        <h2 className="text-2xl font-bold text-foreground">إعدادات قاعدة البيانات</h2>
        <p className="text-muted-foreground mt-2">تكوين اتصال قاعدة البيانات</p>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            نوع قاعدة البيانات
          </label>
          <select
            value={databaseSettings.type}
            onChange={(e) => setDatabaseSettings({...databaseSettings, type: e.target.value})}
            className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="sqlite">SQLite (موصى به للبداية)</option>
            <option value="mysql">MySQL</option>
            <option value="postgresql">PostgreSQL</option>
          </select>
        </div>

        {databaseSettings.type !== 'sqlite' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                عنوان الخادم *
              </label>
              <input
                type="text"
                value={databaseSettings.host}
                onChange={(e) => setDatabaseSettings({...databaseSettings, host: e.target.value})}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="localhost"
              />
              {errors.dbHost && (
                <p className="text-red-500 text-sm mt-1">{errors.dbHost}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                المنفذ
              </label>
              <input
                type="number"
                value={databaseSettings.port}
                onChange={(e) => setDatabaseSettings({...databaseSettings, port: e.target.value})}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder={databaseSettings.type === 'mysql' ? '3306' : '5432'}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم قاعدة البيانات *
              </label>
              <input
                type="text"
                value={databaseSettings.name}
                onChange={(e) => setDatabaseSettings({...databaseSettings, name: e.target.value})}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="inventory_system"
              />
              {errors.dbName && (
                <p className="text-red-500 text-sm mt-1">{errors.dbName}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم المستخدم
              </label>
              <input
                type="text"
                value={databaseSettings.username}
                onChange={(e) => setDatabaseSettings({...databaseSettings, username: e.target.value})}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="database_user"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-foreground mb-2">
                كلمة المرور
              </label>
              <input
                type="password"
                value={databaseSettings.password}
                onChange={(e) => setDatabaseSettings({...databaseSettings, password: e.target.value})}
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="كلمة مرور قاعدة البيانات"
              />
            </div>
          </div>
        )}

        {databaseSettings.type === 'sqlite' && (
          <div className="bg-primary/10 border border-primary/30 rounded-md p-4">
            <div className="flex">
              <InfoIcon className="h-5 w-5 text-primary/50 mt-0.5" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-primary/95">
                  SQLite Database
                </h3>
                <div className="mt-2 text-sm text-primary/90">
                  <p>
                    سيتم إنشاء قاعدة بيانات SQLite محلية تلقائياً. هذا الخيار مناسب للبداية 
                    ويمكن ترقيته لاحقاً إلى MySQL أو PostgreSQL.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // مكون إعدادات الأمان
  const SecuritySettingsStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <SecurityIcon className="mx-auto h-16 w-16 text-destructive mb-4" />
        <h2 className="text-2xl font-bold text-foreground">إعدادات الأمان</h2>
        <p className="text-muted-foreground mt-2">تكوين إعدادات الأمان والحماية</p>
      </div>

      <div className="space-y-6">
        <div className="bg-accent/10 border border-yellow-200 rounded-md p-4">
          <div className="flex">
            <WarningIcon className="h-5 w-5 text-yellow-400 mt-0.5" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                تنبيه أمني مهم
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>
                  تأكد من استخدام كلمات مرور قوية وتفعيل جميع إعدادات الأمان المناسبة 
                  لحماية نظامك من التهديدات الأمنية.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-foreground">سياسة كلمات المرور</h3>
            
            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل
                </span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  يجب أن تحتوي على أحرف كبيرة وصغيرة
                </span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  يجب أن تحتوي على أرقام ورموز خاصة
                </span>
              </label>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-medium text-foreground">إعدادات الجلسة</h3>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                مدة انتهاء الجلسة (بالدقائق)
              </label>
              <select className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-red-500">
                <option value="30">30 دقيقة</option>
                <option value="60">60 دقيقة</option>
                <option value="120">120 دقيقة</option>
                <option value="480">8 ساعات</option>
              </select>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-medium text-foreground">إعدادات إضافية</h3>
            
            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  تسجيل محاولات تسجيل الدخول
                </span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  حظر IP بعد محاولات فاشلة متعددة
                </span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="h-4 w-4 text-destructive focus:ring-red-500 border-border rounded"
                />
                <span className="ml-2 text-sm text-foreground">
                  تفعيل المصادقة الثنائية (2FA)
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // مكون إكمال الإعداد
  const CompletionStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <CheckCircleIcon className="mx-auto h-16 w-16 text-primary mb-4" />
        <h2 className="text-2xl font-bold text-foreground">إكمال الإعداد</h2>
        <p className="text-muted-foreground mt-2">مراجعة نهائية قبل إكمال إعداد النظام</p>
      </div>

      <div className="bg-muted/50 rounded-lg p-6">
        <h3 className="text-lg font-medium text-foreground mb-4">ملخص الإعدادات</h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium text-foreground">اسم الشركة:</span>
            <span className="text-sm text-foreground">{companyData.name}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium text-foreground">المدير:</span>
            <span className="text-sm text-foreground">{adminData.firstName} {adminData.lastName}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium text-foreground">اللغة:</span>
            <span className="text-sm text-foreground">{systemSettings.language === 'ar' ? 'العربية' : 'English'}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium text-foreground">العملة:</span>
            <span className="text-sm text-foreground">{systemSettings.currency}</span>
          </div>
          
          <div className="flex justify-between items-center py-2">
            <span className="text-sm font-medium text-foreground">قاعدة البيانات:</span>
            <span className="text-sm text-foreground">{databaseSettings.type.toUpperCase()}</span>
          </div>
        </div>
      </div>

      <div className="bg-primary/10 border border-primary/30 rounded-md p-4">
        <div className="flex">
          <CheckCircleIcon className="h-5 w-5 text-green-400 mt-0.5" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-green-800">
              جاهز للإكمال
            </h3>
            <div className="mt-2 text-sm text-primary">
              <p>
                تم تكوين جميع الإعدادات بنجاح. اضغط على "إكمال الإعداد" لبدء استخدام النظام.
              </p>
            </div>
          </div>
        </div>
      </div>

      {errors.general && (
        <div className="bg-destructive/10 border border-destructive/30 rounded-md p-4">
          <div className="flex">
            <WarningIcon className="h-5 w-5 text-red-400 mt-0.5" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">خطأ</h3>
              <div className="mt-2 text-sm text-destructive">
                <p>{errors.general}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  // عرض المكون المناسب حسب الخطوة الحالية
  const renderStepContent = () => {
    switch (activeStep) {
      case 0: return <CompanyInfoStep />;
      case 1: return <AdminAccountStep />;
      case 2: return <SystemSettingsStep />;
      case 3: return <DatabaseConfigStep />;
      case 4: return <SecuritySettingsStep />;
      case 5: return <CompletionStep />;
      default: return <CompanyInfoStep />;
    }
  };

  return (
    <div className="min-h-screen bg-muted/50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground">معالج إعداد النظام</h1>
          <p className="text-muted-foreground mt-2">إعداد نظام إدارة المخزون المتقدم</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-foreground">
              الخطوة {activeStep + 1} من {steps.length}
            </span>
            <span className="text-sm font-medium text-foreground">
              {Math.round(setupProgress)}%
            </span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div 
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${setupProgress}%` }}
            />
          </div>
        </div>

        {/* Steps Navigation */}
        <div className="mb-8">
          <nav className="flex justify-center">
            <ol className="flex items-center space-x-4 rtl:space-x-reverse">
              {steps.map((step, index) => {
                const Icon = step.icon;
                const isActive = index === activeStep;
                const isCompleted = index < activeStep;
                
                return (
                  <li key={step.id} className="flex items-center">
                    <div className={`
                      flex items-center justify-center w-10 h-10 rounded-full border-2 
                      ${isActive ? 'border-primary bg-primary text-white' : 
                        isCompleted ? 'border-green-600 bg-primary text-white' : 
                        'border-border bg-white text-gray-400'}
                    `}>
                      <Icon className="w-5 h-5" />
                    </div>
                    {index < steps.length - 1 && (
                      <div className={`
                        w-16 h-0.5 mx-4
                        ${isCompleted ? 'bg-primary' : 'bg-gray-300'}
                      `} />
                    )}
                  </li>
                );
              })}
            </ol>
          </nav>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm border border-border p-8 mb-8">
          {renderStepContent()}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between">
          <button
            onClick={handleBack}
            disabled={activeStep === 0}
            className={`
              flex items-center px-6 py-3 rounded-md font-medium
              ${activeStep === 0 
                ? 'bg-muted text-gray-400 cursor-not-allowed' 
                : 'bg-muted text-foreground hover:bg-gray-300'}
            `}
          >
            <ArrowBackIcon className="w-4 h-4 ml-2" />
            السابق
          </button>

          {activeStep === steps.length - 1 ? (
            <button
              onClick={handleComplete}
              disabled={loading}
              className="flex items-center px-6 py-3 bg-primary text-white rounded-md font-medium hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white ml-2" />
                  جاري الإعداد...
                </>
              ) : (
                <>
                  <DoneIcon className="w-4 h-4 ml-2" />
                  إكمال الإعداد
                </>
              )}
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="flex items-center px-6 py-3 bg-primary text-white rounded-md font-medium hover:bg-primary/90"
            >
              التالي
              <ArrowForwardIcon className="w-4 h-4 mr-2" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default SetupWizard;

