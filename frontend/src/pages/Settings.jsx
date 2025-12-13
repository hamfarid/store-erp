/**
 * صفحة الإعدادات الرئيسية - Enhanced with shadcn/ui
 * Settings Page with modern UI components
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Settings as SettingsIcon, Users, Shield, Building2, Warehouse, CreditCard,
  FolderTree, Scale, RefreshCcw, FileText, Palette, Globe,
  Bell, Mail, Printer, Database, CloudUpload, HardDrive,
  MonitorCheck, Activity, Server, UserPlus, Download, Zap,
  ChevronLeft, LayoutGrid, TrendingUp, TrendingDown
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert';
import { usePermissions } from '../contexts/PermissionContext';

/**
 * System Stats Card Component
 */
const StatCard = ({ icon: Icon, title, value, subtitle, color = 'primary', trend, trendValue }) => {
  const colorClasses = {
    primary: 'from-primary-500 to-primary-600',
    success: 'from-green-500 to-green-600',
    warning: 'from-amber-500 to-amber-600',
    info: 'from-blue-500 to-blue-600',
    error: 'from-red-500 to-red-600',
  };

  return (
    <Card className="hover:shadow-lg transition-all duration-300 border-0 shadow-md">
      <CardContent className="p-6">
        <div className="flex items-center gap-4">
          <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center shadow-lg`}>
            <Icon className="text-white" size={24} />
          </div>
          <div className="flex-1">
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          </div>
          {trend && (
            <div className={`flex items-center gap-1 ${trend === 'up' ? 'text-green-600' : 'text-red-500'}`}>
              {trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              <span className="text-sm font-medium">{trendValue}</span>
            </div>
          )}
        </div>
        {subtitle && (
          <div className="mt-3 flex items-center gap-2">
            {subtitle}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

/**
 * Settings Category Card Component
 */
const CategoryCard = ({ title, icon: Icon, color, items, onNavigate }) => {
  const colorClasses = {
    error: 'from-red-500 to-red-600',
    primary: 'from-primary-500 to-primary-600',
    success: 'from-green-500 to-green-600',
    warning: 'from-amber-500 to-amber-600',
    info: 'from-blue-500 to-blue-600',
    secondary: 'from-purple-500 to-purple-600',
  };

  return (
    <Card className="hover:shadow-lg transition-all duration-300">
      <CardHeader className="pb-3">
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center shadow-lg`}>
            <Icon className="text-white" size={22} />
          </div>
          <CardTitle className="text-lg">{title}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-1">
          {items.map((item, index) => (
            <button
              key={index}
              onClick={() => onNavigate(item.path)}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-start hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
            >
              <div className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center group-hover:bg-primary-100 dark:group-hover:bg-primary-900 transition-colors">
                <item.icon size={18} className="text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">{item.title}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{item.description}</p>
              </div>
              <ChevronLeft size={16} className="text-gray-400 group-hover:text-primary-500 transition-colors" />
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

/**
 * Quick Action Button Component
 */
const QuickAction = ({ icon: Icon, label, color, onClick }) => {
  const colorClasses = {
    primary: 'text-primary-600 bg-primary-100 hover:bg-primary-200 dark:bg-primary-900/50 dark:hover:bg-primary-800/50',
    success: 'text-green-600 bg-green-100 hover:bg-green-200 dark:bg-green-900/50 dark:hover:bg-green-800/50',
    warning: 'text-amber-600 bg-amber-100 hover:bg-amber-200 dark:bg-amber-900/50 dark:hover:bg-amber-800/50',
    info: 'text-blue-600 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/50 dark:hover:bg-blue-800/50',
  };

  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center justify-center p-6 rounded-2xl transition-all duration-200 hover:scale-105 ${colorClasses[color]}`}
    >
      <Icon size={36} className="mb-3" />
      <span className="text-sm font-medium text-center">{label}</span>
    </button>
  );
};

/**
 * Main Settings Component
 */
const Settings = () => {
  const navigate = useNavigate();
  const { hasPermission } = usePermissions();

  // System Stats State
  const [systemStats, setSystemStats] = useState({
    users: { total: 0, active: 0, online: 0 },
    storage: { used: 0, total: 0, percentage: 0 },
    performance: { cpu: 0, memory: 0, disk: 0 },
    lastBackup: null,
    systemVersion: '1.1.0'
  });

  // Load system stats on mount
  useEffect(() => {
    loadSystemStats();
  }, []);

  const loadSystemStats = async () => {
    try {
      // In production, load from API
      // const stats = await systemService.getStats();
      // setSystemStats(stats);

      // Demo data
      setSystemStats({
        users: { total: 25, active: 18, online: 7 },
        storage: { used: 2.4, total: 10, percentage: 24 },
        performance: { cpu: 45, memory: 62, disk: 78 },
        lastBackup: new Date().toISOString(),
        systemVersion: '1.1.0'
      });
    } catch (error) {
      console.error('Failed to load system stats:', error);
    }
  };

  // Settings Categories Configuration
  const settingsCategories = [
    {
      title: 'إدارة النظام',
      icon: Shield,
      color: 'error',
      requiredPermission: 'admin',
      items: [
        {
          title: 'إدارة المستخدمين',
          description: 'إضافة وتعديل وحذف المستخدمين',
          icon: Users,
          path: '/users',
          requiredPermission: 'manage_users'
        },
        {
          title: 'الأدوار والصلاحيات',
          description: 'إدارة الأدوار وتحديد الصلاحيات',
          icon: Shield,
          path: '/admin/roles',
          requiredPermission: 'manage_roles'
        },
        {
          title: 'إعدادات الأمان',
          description: 'سياسة كلمات المرور والجلسات',
          icon: Shield,
          path: '/security-dashboard',
          requiredPermission: 'manage_security'
        },
        {
          title: 'مراقبة النظام',
          description: 'مراقبة الأداء والإحصائيات',
          icon: Activity,
          path: '/system-status',
          requiredPermission: 'view_monitoring'
        }
      ]
    },
    {
      title: 'إعدادات الشركة',
      icon: Building2,
      color: 'primary',
      requiredPermission: 'manage_company',
      items: [
        {
          title: 'معلومات الشركة',
          description: 'اسم الشركة والعنوان ومعلومات الاتصال',
          icon: Building2,
          path: '/company',
          requiredPermission: 'manage_company'
        },
        {
          title: 'الفروع والمخازن',
          description: 'إدارة الفروع والمخازن والمواقع',
          icon: Warehouse,
          path: '/warehouses',
          requiredPermission: 'manage_warehouses'
        },
        {
          title: 'العملات والضرائب',
          description: 'إعداد العملات وأسعار الصرف',
          icon: CreditCard,
          path: '/accounting/currencies',
          requiredPermission: 'manage_currencies'
        }
      ]
    },
    {
      title: 'إعدادات المخزون',
      icon: LayoutGrid,
      color: 'success',
      requiredPermission: 'manage_inventory_settings',
      items: [
        {
          title: 'فئات المنتجات',
          description: 'إدارة فئات وتصنيفات المنتجات',
          icon: FolderTree,
          path: '/categories',
          requiredPermission: 'manage_categories'
        },
        {
          title: 'وحدات القياس',
          description: 'إدارة وحدات القياس والتحويلات',
          icon: Scale,
          path: '/products',
          requiredPermission: 'manage_units'
        },
        {
          title: 'تنبيهات المخزون',
          description: 'إعداد تنبيهات المخزون المنخفض',
          icon: Bell,
          path: '/inventory-alerts',
          requiredPermission: 'manage_reorder_rules'
        }
      ]
    },
    {
      title: 'إعدادات المبيعات',
      icon: FileText,
      color: 'warning',
      requiredPermission: 'manage_sales_settings',
      items: [
        {
          title: 'شروط الدفع',
          description: 'إدارة شروط وطرق الدفع',
          icon: CreditCard,
          path: '/payments',
          requiredPermission: 'manage_payment_terms'
        },
        {
          title: 'قوالب الفواتير',
          description: 'تصميم وإدارة قوالب الفواتير',
          icon: FileText,
          path: '/invoices',
          requiredPermission: 'manage_templates'
        },
        {
          title: 'إدارة الخصومات',
          description: 'قوائم الأسعار والخصومات',
          icon: RefreshCcw,
          path: '/discounts',
          requiredPermission: 'manage_pricing'
        }
      ]
    },
    {
      title: 'إعدادات النظام العامة',
      icon: SettingsIcon,
      color: 'info',
      requiredPermission: 'manage_system_settings',
      items: [
        {
          title: 'اللغة والتوطين',
          description: 'إعدادات اللغة والمنطقة الزمنية',
          icon: Globe,
          path: '/modern/settings',
          requiredPermission: 'manage_localization'
        },
        {
          title: 'الإشعارات',
          description: 'إعدادات الإشعارات والتنبيهات',
          icon: Bell,
          path: '/notifications-center',
          requiredPermission: 'manage_notifications'
        },
        {
          title: 'المظهر',
          description: 'تخصيص مظهر التطبيق والألوان',
          icon: Palette,
          path: '/modern/settings',
          requiredPermission: 'manage_appearance'
        },
        {
          title: 'الطباعة',
          description: 'إعدادات الطابعات والتقارير',
          icon: Printer,
          path: '/reports',
          requiredPermission: 'manage_printing'
        }
      ]
    },
    {
      title: 'النسخ الاحتياطي والصيانة',
      icon: Database,
      color: 'secondary',
      requiredPermission: 'manage_backup',
      items: [
        {
          title: 'النسخ الاحتياطي',
          description: 'إنشاء واستعادة النسخ الاحتياطية',
          icon: Download,
          path: '/backup-restore',
          requiredPermission: 'manage_backup'
        },
        {
          title: 'حالة النظام',
          description: 'فحص وتثبيت تحديثات النظام',
          icon: Server,
          path: '/system-status',
          requiredPermission: 'manage_updates'
        },
        {
          title: 'المزامنة السحابية',
          description: 'إعدادات المزامنة مع السحابة',
          icon: CloudUpload,
          path: '/backup-restore',
          requiredPermission: 'manage_cloud_sync'
        },
        {
          title: 'صيانة قاعدة البيانات',
          description: 'تحسين وصيانة قاعدة البيانات',
          icon: HardDrive,
          path: '/system-status',
          requiredPermission: 'manage_database'
        }
      ]
    }
  ];

  // Helper Functions
  const formatBytes = (gb) => {
    return `${gb.toFixed(1)} GB`;
  };

  const getPerformanceColor = (value) => {
    if (value < 50) return 'success';
    if (value < 80) return 'warning';
    return 'error';
  };

  // Check permission helper
  const checkPermission = (permission) => {
    if (!permission) return true;
    return hasPermission ? hasPermission(permission) : true;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">إعدادات النظام</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">إدارة وتخصيص جميع إعدادات النظام</p>
      </div>

      {/* System Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          icon={Users}
          title="إجمالي المستخدمين"
          value={systemStats.users.total}
          color="primary"
          subtitle={
            <div className="flex gap-2">
              <Badge variant="success" className="text-xs">{systemStats.users.active} نشط</Badge>
              <Badge variant="info" className="text-xs">{systemStats.users.online} متصل</Badge>
            </div>
          }
        />
        
        <StatCard
          icon={HardDrive}
          title="استخدام التخزين"
          value={`${systemStats.storage.percentage}%`}
          color="success"
          subtitle={
            <p className="text-xs text-gray-500">
              {formatBytes(systemStats.storage.used)} / {formatBytes(systemStats.storage.total)}
            </p>
          }
        />
        
        <StatCard
          icon={Activity}
          title="استخدام المعالج"
          value={`${systemStats.performance.cpu}%`}
          color={getPerformanceColor(systemStats.performance.cpu)}
          subtitle={
            <p className="text-xs text-gray-500">
              الذاكرة: {systemStats.performance.memory}%
            </p>
          }
        />
        
        <StatCard
          icon={Server}
          title="إصدار النظام"
          value={`v${systemStats.systemVersion}`}
          color="info"
          subtitle={
            <p className="text-xs text-gray-500">
              آخر نسخة احتياطية: اليوم
            </p>
          }
        />
      </div>

      {/* Settings Categories Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {settingsCategories.map((category, index) => (
          checkPermission(category.requiredPermission) && (
            <CategoryCard
              key={index}
              title={category.title}
              icon={category.icon}
              color={category.color}
              items={category.items.filter(item => checkPermission(item.requiredPermission))}
              onNavigate={navigate}
            />
          )
        ))}
      </div>

      {/* Quick Actions */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Zap size={20} className="text-amber-500" />
            إجراءات سريعة
          </CardTitle>
          <CardDescription>وصول سريع للإجراءات الأكثر استخداماً</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {checkPermission('manage_backup') && (
              <QuickAction
                icon={Download}
                label="إنشاء نسخة احتياطية"
                color="primary"
                onClick={() => navigate('/backup-restore')}
              />
            )}
            {checkPermission('view_monitoring') && (
              <QuickAction
                icon={MonitorCheck}
                label="فحص حالة النظام"
                color="success"
                onClick={() => navigate('/system-status')}
              />
            )}
            {checkPermission('manage_users') && (
              <QuickAction
                icon={UserPlus}
                label="إضافة مستخدم جديد"
                color="warning"
                onClick={() => navigate('/users')}
              />
            )}
            {checkPermission('manage_updates') && (
              <QuickAction
                icon={RefreshCcw}
                label="فحص التحديثات"
                color="info"
                onClick={() => navigate('/system-status')}
              />
            )}
          </div>
        </CardContent>
      </Card>

      {/* System Alerts */}
      <div className="space-y-4">
        <Alert variant="info">
          <Bell className="h-4 w-4" />
          <AlertTitle>نصيحة</AlertTitle>
          <AlertDescription>
            يمكنك الوصول السريع للإعدادات المختلفة من خلال لوحة الأوامر (Ctrl+K)
          </AlertDescription>
        </Alert>

        {systemStats.performance.cpu > 80 && (
          <Alert variant="warning">
            <Activity className="h-4 w-4" />
            <AlertTitle>تحذير</AlertTitle>
            <AlertDescription>
              استخدام المعالج مرتفع ({systemStats.performance.cpu}%). يُنصح بمراجعة العمليات الجارية.
            </AlertDescription>
          </Alert>
        )}

        {systemStats.storage.percentage > 85 && (
          <Alert variant="destructive">
            <HardDrive className="h-4 w-4" />
            <AlertTitle>تنبيه هام</AlertTitle>
            <AlertDescription>
              مساحة التخزين ممتلئة تقريباً ({systemStats.storage.percentage}%). يُرجى تنظيف الملفات أو زيادة المساحة.
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default Settings;
