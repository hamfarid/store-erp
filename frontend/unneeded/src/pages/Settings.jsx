/**
 * صفحة الإعدادات الرئيسية
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/Settings.js
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'

import { usePermissions } from '../contexts/PermissionContext';

const Settings = () => {
  const navigate = useNavigate();
  const { user, hasPermission } = usePermissions();

  // ==================== State Management ====================

  const [systemStats, setSystemStats] = useState({
    users: { total: 0, active: 0, online: 0 },
    storage: { used: 0, total: 0, percentage: 0 },
    performance: { cpu: 0, memory: 0, disk: 0 },
    lastBackup: null,
    systemVersion: '1.1.0'
  });

  // ==================== Data Loading ====================

  useEffect(() => {
    loadSystemStats();
  }, []);

  const loadSystemStats = async () => {
    try {
      // هنا يمكن تحميل إحصائيات النظام من API
      // const stats = await systemService.getStats();
      // setSystemStats(stats);

      // بيانات تجريبية للعرض
      setSystemStats({
        users: { total: 25, active: 18, online: 7 },
        storage: { used: 2.4, total: 10, percentage: 24 },
        performance: { cpu: 45, memory: 62, disk: 78 },
        lastBackup: new Date().toISOString(),
        systemVersion: '1.1.0'
      });
    } catch (error) {
      }
  };

  // ==================== Settings Categories ====================

  const settingsCategories = [
    {
      title: 'إدارة النظام',
      icon: <AdminIcon />,
      color: 'error',
      requiredPermission: 'admin',
      items: [
        {
          title: 'إدارة المستخدمين',
          description: 'إضافة وتعديل وحذف المستخدمين وتحديد الصلاحيات',
          icon: <PeopleIcon />,
          path: '/settings/users',
          requiredPermission: 'manage_users'
        },
        {
          title: 'الأدوار والصلاحيات',
          description: 'إدارة الأدوار وتحديد الصلاحيات التفصيلية',
          icon: <SecurityIcon />,
          path: '/settings/roles',
          requiredPermission: 'manage_roles'
        },
        {
          title: 'إعدادات الأمان',
          description: 'سياسة كلمات المرور ومدة صلاحية الجلسات',
          icon: <SecurityIcon />,
          path: '/settings/security',
          requiredPermission: 'manage_security'
        },
        {
          title: 'مراقبة النظام',
          description: 'مراقبة الأداء وحالة الخادم والإحصائيات',
          icon: <DashboardIcon />,
          path: '/settings/monitoring',
          requiredPermission: 'view_monitoring'
        }
      ]
    },
    {
      title: 'إعدادات الشركة',
      icon: <BusinessIcon />,
      color: 'primary',
      requiredPermission: 'manage_company',
      items: [
        {
          title: 'معلومات الشركة',
          description: 'اسم الشركة والعنوان ومعلومات الاتصال',
          icon: <BusinessIcon />,
          path: '/company',
          requiredPermission: 'manage_company'
        },
        {
          title: 'الفروع والمخازن',
          description: 'إدارة الفروع والمخازن والمواقع',
          icon: <StorageIcon />,
          path: '/settings/warehouses',
          requiredPermission: 'manage_warehouses'
        },
        {
          title: 'العملات والضرائب',
          description: 'إعداد العملات وأسعار الصرف والضرائب',
          icon: <PaymentIcon />,
          path: '/settings/currencies',
          requiredPermission: 'manage_currencies'
        }
      ]
    },
    {
      title: 'إعدادات المخزون',
      icon: <InventoryIcon />,
      color: 'success',
      requiredPermission: 'manage_inventory_settings',
      items: [
        {
          title: 'فئات المنتجات',
          description: 'إدارة فئات وتصنيفات المنتجات',
          icon: <CategoryIcon />,
          path: '/settings/product-categories',
          requiredPermission: 'manage_categories'
        },
        {
          title: 'وحدات القياس',
          description: 'إدارة وحدات القياس والتحويلات',
          icon: <InventoryIcon />,
          path: '/settings/units',
          requiredPermission: 'manage_units'
        },
        {
          title: 'قواعد إعادة الطلب',
          description: 'إعداد قواعد إعادة الطلب التلقائي',
          icon: <LocalShippingIcon />,
          path: '/settings/reorder-rules',
          requiredPermission: 'manage_reorder_rules'
        }
      ]
    },
    {
      title: 'إعدادات المبيعات',
      icon: <ReceiptIcon />,
      color: 'warning',
      requiredPermission: 'manage_sales_settings',
      items: [
        {
          title: 'شروط الدفع',
          description: 'إدارة شروط وطرق الدفع',
          icon: <PaymentIcon />,
          path: '/settings/payment-terms',
          requiredPermission: 'manage_payment_terms'
        },
        {
          title: 'قوالب الفواتير',
          description: 'تصميم وإدارة قوالب الفواتير',
          icon: <ReceiptIcon />,
          path: '/settings/invoice-templates',
          requiredPermission: 'manage_templates'
        },
        {
          title: 'إعدادات الأسعار',
          description: 'قوائم الأسعار والخصومات',
          icon: <AssessmentIcon />,
          path: '/settings/pricing',
          requiredPermission: 'manage_pricing'
        }
      ]
    },
    {
      title: 'إعدادات النظام العامة',
      icon: <SettingsIcon />,
      color: 'info',
      requiredPermission: 'manage_system_settings',
      items: [
        {
          title: 'اللغة والتوطين',
          description: 'إعدادات اللغة والمنطقة الزمنية',
          icon: <LanguageIcon />,
          path: '/settings/localization',
          requiredPermission: 'manage_localization'
        },
        {
          title: 'الإشعارات',
          description: 'إعدادات الإشعارات والتنبيهات',
          icon: <NotificationsIcon />,
          path: '/settings/notifications',
          requiredPermission: 'manage_notifications'
        },
        {
          title: 'البريد الإلكتروني',
          description: 'إعدادات خادم البريد الإلكتروني',
          icon: <EmailIcon />,
          path: '/settings/email',
          requiredPermission: 'manage_email'
        },
        {
          title: 'الطباعة',
          description: 'إعدادات الطابعات والتقارير',
          icon: <PrintIcon />,
          path: '/settings/printing',
          requiredPermission: 'manage_printing'
        }
      ]
    },
    {
      title: 'النسخ الاحتياطي والصيانة',
      icon: <BackupIcon />,
      color: 'secondary',
      requiredPermission: 'manage_backup',
      items: [
        {
          title: 'النسخ الاحتياطي',
          description: 'إنشاء واستعادة النسخ الاحتياطية',
          icon: <BackupIcon />,
          path: '/settings/backup',
          requiredPermission: 'manage_backup'
        },
        {
          title: 'تحديثات النظام',
          description: 'فحص وتثبيت تحديثات النظام',
          icon: <UpdateIcon />,
          path: '/settings/updates',
          requiredPermission: 'manage_updates'
        },
        {
          title: 'المزامنة السحابية',
          description: 'إعدادات المزامنة مع الخدمات السحابية',
          icon: <CloudSyncIcon />,
          path: '/settings/cloud-sync',
          requiredPermission: 'manage_cloud_sync'
        },
        {
          title: 'صيانة قاعدة البيانات',
          description: 'تحسين وصيانة قاعدة البيانات',
          icon: <StorageIcon />,
          path: '/settings/database-maintenance',
          requiredPermission: 'manage_database'
        }
      ]
    }
  ];

  // ==================== Helper Functions ====================

  const getPerformanceColor = (value) => {
    if (value < 50) return 'success';
    if (value < 80) return 'warning';
    return 'error';
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // ==================== Render Functions ====================

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          إعدادات النظام
        </Typography>
        <Typography variant="body1" color="text.secondary">
          إدارة وتخصيص جميع إعدادات النظام
        </Typography>
      </Box>

      {/* System Overview */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <PeopleIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{systemStats.users.total}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    إجمالي المستخدمين
                  </Typography>
                </Box>
              </Box>
              <Box display="flex" gap={1}>
                <Chip label={`${systemStats.users.active} نشط`} size="small" color="success" />
                <Chip label={`${systemStats.users.online} متصل`} size="small" color="info" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <StorageIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{systemStats.storage.percentage}%</Typography>
                  <Typography variant="body2" color="text.secondary">
                    استخدام التخزين
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2">
                {formatBytes(systemStats.storage.used * 1024 * 1024 * 1024)} / {formatBytes(systemStats.storage.total * 1024 * 1024 * 1024)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Avatar sx={{ bgcolor: getPerformanceColor(systemStats.performance.cpu), mr: 2 }}>
                  <SpeedIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{systemStats.performance.cpu}%</Typography>
                  <Typography variant="body2" color="text.secondary">
                    استخدام المعالج
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2">
                ذاكرة: {systemStats.performance.memory}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <BackupIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">v{systemStats.systemVersion}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    إصدار النظام
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2">
                آخر نسخة احتياطية: اليوم
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Settings Categories */}
      <Grid container spacing={3}>
        {settingsCategories.map((category, categoryIndex) => (
          <ProtectedComponent
            key={categoryIndex}
            requiredPermission={category.requiredPermission}
          >
            <Grid item xs={12} lg={6}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar sx={{ bgcolor: `${category.color}.main`, mr: 2 }}>
                      {category.icon}
                    </Avatar>
                    <Typography variant="h6">
                      {category.title}
                    </Typography>
                  </Box>

                  <List disablePadding>
                    {category.items.map((item, itemIndex) => (
                      <ProtectedComponent
                        key={itemIndex}
                        requiredPermission={item.requiredPermission}
                      >
                        <ListItem disablePadding>
                          <ListItemButton
                            onClick={() => navigate(item.path)}
                            sx={{ borderRadius: 1, mb: 1 }}
                          >
                            <ListItemIcon>
                              {item.icon}
                            </ListItemIcon>
                            <ListItemText
                              primary={item.title}
                              secondary={item.description}
                            />
                          </ListItemButton>
                        </ListItem>
                        {itemIndex < category.items.length - 1 && <Divider />}
                      </ProtectedComponent>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </ProtectedComponent>
        ))}
      </Grid>

      {/* Quick Actions */}
      <Grid container spacing={3} mt={2}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                إجراءات سريعة
              </Typography>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <ProtectedComponent requiredPermission="manage_backup">
                    <Paper
                      sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                      onClick={() => navigate('/settings/backup')}
                    >
                      <BackupIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                      <Typography variant="body2">
                        إنشاء نسخة احتياطية
                      </Typography>
                    </Paper>
                  </ProtectedComponent>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <ProtectedComponent requiredPermission="view_monitoring">
                    <Paper
                      sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                      onClick={() => navigate('/settings/monitoring')}
                    >
                      <NetworkIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                      <Typography variant="body2">
                        فحص حالة النظام
                      </Typography>
                    </Paper>
                  </ProtectedComponent>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <ProtectedComponent requiredPermission="manage_users">
                    <Paper
                      sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                      onClick={() => navigate('/settings/users/add')}
                    >
                      <PeopleIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                      <Typography variant="body2">
                        إضافة مستخدم جديد
                      </Typography>
                    </Paper>
                  </ProtectedComponent>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <ProtectedComponent requiredPermission="manage_updates">
                    <Paper
                      sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                      onClick={() => navigate('/settings/updates')}
                    >
                      <UpdateIcon sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                      <Typography variant="body2">
                        فحص التحديثات
                      </Typography>
                    </Paper>
                  </ProtectedComponent>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* System Alerts */}
      <Grid container spacing={3} mt={2}>
        <Grid item xs={12}>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              💡 نصيحة: يمكنك الوصول السريع للإعدادات المختلفة من خلال شريط البحث في الأعلى
            </Typography>
          </Alert>

          {systemStats.performance.cpu > 80 && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <Typography variant="body2">
                ⚠️ تحذير: استخدام المعالج مرتفع ({systemStats.performance.cpu}%). يُنصح بمراجعة العمليات الجارية.
              </Typography>
            </Alert>
          )}

          {systemStats.storage.percentage > 85 && (
            <Alert severity="error">
              <Typography variant="body2">
                🚨 تنبيه: مساحة التخزين ممتلئة تقريباً ({systemStats.storage.percentage}%). يُرجى تنظيف الملفات أو زيادة المساحة.
              </Typography>
            </Alert>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;

