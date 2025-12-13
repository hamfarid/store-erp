import React, { useState, useEffect } from 'react';
import {
  Bell, Search, Download, CheckCircle, AlertTriangle, Info, X,
  Trash2, Check, CheckCheck, Filter, Calendar, User, Settings
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

/**
 * مركز الإشعارات
 * Notifications Center Page
 */
const NotificationsCenter = () => {
  const [notifications, setNotifications] = useState([]);
  const [filteredNotifications, setFilteredNotifications] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterRead, setFilterRead] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedNotifications, setSelectedNotifications] = useState([]);

  // بيانات نموذجية
  const sampleNotifications = [
    {
      id: 1,
      title: 'تنبيه انخفاض المخزون',
      message: 'مخزون المنتج "لابتوب HP ProBook" وصل إلى الحد الأدنى (5 وحدات)',
      type: 'warning',
      category: 'inventory',
      isRead: false,
      createdAt: '2024-01-15T14:30:00',
      actionUrl: '/inventory?search=HP+ProBook'
    },
    {
      id: 2,
      title: 'طلب جديد',
      message: 'تم استلام طلب جديد #ORD-2024-1250 بقيمة 5,500 ر.س',
      type: 'info',
      category: 'orders',
      isRead: false,
      createdAt: '2024-01-15T13:45:00',
      actionUrl: '/orders/ORD-2024-1250'
    },
    {
      id: 3,
      title: 'دفعة مستحقة',
      message: 'دفعة بقيمة 12,000 ر.س من العميل "شركة التقنية المتقدمة" مستحقة اليوم',
      type: 'warning',
      category: 'finance',
      isRead: false,
      createdAt: '2024-01-15T09:00:00',
      actionUrl: '/debt-management'
    },
    {
      id: 4,
      title: 'نجاح النسخ الاحتياطي',
      message: 'تم إنشاء نسخة احتياطية يومية بنجاح',
      type: 'success',
      category: 'system',
      isRead: true,
      createdAt: '2024-01-15T02:00:00',
      actionUrl: null
    },
    {
      id: 5,
      title: 'خطأ في المزامنة',
      message: 'فشل تحديث أسعار الصرف - تعذر الاتصال بالخادم الخارجي',
      type: 'error',
      category: 'system',
      isRead: false,
      createdAt: '2024-01-15T10:00:00',
      actionUrl: '/automation-tasks'
    },
    {
      id: 6,
      title: 'مستخدم جديد',
      message: 'تم إضافة المستخدم "محمد علي" إلى النظام',
      type: 'info',
      category: 'users',
      isRead: true,
      createdAt: '2024-01-14T16:20:00',
      actionUrl: '/system/user-management'
    },
    {
      id: 7,
      title: 'تقرير جاهز',
      message: 'تقرير المبيعات الأسبوعي جاهز للتنزيل',
      type: 'success',
      category: 'reports',
      isRead: true,
      createdAt: '2024-01-14T08:00:00',
      actionUrl: '/reports/comprehensive'
    },
    {
      id: 8,
      title: 'تحذير أمني',
      message: 'تم تسجيل محاولة دخول فاشلة من عنوان IP غير معروف',
      type: 'error',
      category: 'security',
      isRead: false,
      createdAt: '2024-01-14T22:15:00',
      actionUrl: '/audit-logs'
    }
  ];

  const notificationTypes = [
    { value: 'info', label: 'معلومات', icon: Info, color: 'blue' },
    { value: 'warning', label: 'تحذير', icon: AlertTriangle, color: 'yellow' },
    { value: 'success', label: 'نجاح', icon: CheckCircle, color: 'green' },
    { value: 'error', label: 'خطأ', icon: X, color: 'red' }
  ];

  const categories = [
    { value: 'inventory', label: 'المخزون' },
    { value: 'orders', label: 'الطلبات' },
    { value: 'finance', label: 'المالية' },
    { value: 'system', label: 'النظام' },
    { value: 'users', label: 'المستخدمين' },
    { value: 'reports', label: 'التقارير' },
    { value: 'security', label: 'الأمان' }
  ];

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/notifications');
      if (response.status === 'success' && response.notifications?.length > 0) {
        setNotifications(response.notifications);
        setFilteredNotifications(response.notifications);
      } else {
        setNotifications(sampleNotifications);
        setFilteredNotifications(sampleNotifications);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setNotifications(sampleNotifications);
      setFilteredNotifications(sampleNotifications);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = notifications;

    if (searchTerm) {
      filtered = filtered.filter(notif =>
        notif.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        notif.message.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(notif => notif.type === filterType);
    }

    if (filterRead !== 'all') {
      filtered = filtered.filter(notif => 
        filterRead === 'read' ? notif.isRead : !notif.isRead
      );
    }

    setFilteredNotifications(filtered);
  }, [notifications, searchTerm, filterType, filterRead]);

  const getTypeIcon = (type) => {
    const typeConfig = notificationTypes.find(t => t.value === type);
    if (!typeConfig) return <Bell className="w-5 h-5" />;
    
    const Icon = typeConfig.icon;
    const colorClass = {
      blue: 'text-blue-500',
      yellow: 'text-yellow-500',
      green: 'text-green-500',
      red: 'text-red-500'
    }[typeConfig.color];
    
    return <Icon className={`w-5 h-5 ${colorClass}`} />;
  };

  const getTypeBadge = (type) => {
    const typeConfig = notificationTypes.find(t => t.value === type);
    if (!typeConfig) return <Badge>{type}</Badge>;
    
    const variants = {
      info: 'default',
      warning: 'warning',
      success: 'success',
      error: 'destructive'
    };
    
    return (
      <Badge variant={variants[type] || 'default'}>
        {typeConfig.label}
      </Badge>
    );
  };

  const getCategoryLabel = (category) => {
    const found = categories.find(c => c.value === category);
    return found ? found.label : category;
  };

  const handleMarkAsRead = (notifId) => {
    setNotifications(notifications.map(n =>
      n.id === notifId ? { ...n, isRead: true } : n
    ));
    toast.success('تم تعليم الإشعار كمقروء');
  };

  const handleMarkAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, isRead: true })));
    toast.success('تم تعليم جميع الإشعارات كمقروءة');
  };

  const handleDeleteNotification = (notifId) => {
    setNotifications(notifications.filter(n => n.id !== notifId));
    toast.success('تم حذف الإشعار');
  };

  const handleDeleteSelected = () => {
    if (selectedNotifications.length === 0) {
      toast.error('الرجاء تحديد إشعارات للحذف');
      return;
    }
    setNotifications(notifications.filter(n => !selectedNotifications.includes(n.id)));
    setSelectedNotifications([]);
    toast.success(`تم حذف ${selectedNotifications.length} إشعارات`);
  };

  const handleSelectNotification = (notifId) => {
    setSelectedNotifications(prev =>
      prev.includes(notifId)
        ? prev.filter(id => id !== notifId)
        : [...prev, notifId]
    );
  };

  const handleSelectAll = () => {
    if (selectedNotifications.length === filteredNotifications.length) {
      setSelectedNotifications([]);
    } else {
      setSelectedNotifications(filteredNotifications.map(n => n.id));
    }
  };

  const handleNotificationClick = (notif) => {
    if (!notif.isRead) {
      handleMarkAsRead(notif.id);
    }
    if (notif.actionUrl) {
      window.location.href = notif.actionUrl;
    }
  };

  const getSummary = () => {
    return {
      total: notifications.length,
      unread: notifications.filter(n => !n.isRead).length,
      warnings: notifications.filter(n => n.type === 'warning' && !n.isRead).length,
      errors: notifications.filter(n => n.type === 'error' && !n.isRead).length
    };
  };

  const summary = getSummary();

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) return `منذ ${minutes} دقيقة`;
    if (hours < 24) return `منذ ${hours} ساعة`;
    if (days < 7) return `منذ ${days} أيام`;
    return date.toLocaleDateString('ar-SA');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل الإشعارات...</p>
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
            مركز الإشعارات
          </h1>
          <p className="text-muted-foreground mt-1">إدارة جميع إشعاراتك في مكان واحد</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleMarkAllAsRead}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <CheckCheck className="w-4 h-4" />
            تعليم الكل كمقروء
          </button>
          {selectedNotifications.length > 0 && (
            <button 
              onClick={handleDeleteSelected}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              حذف المحدد ({selectedNotifications.length})
            </button>
          )}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الإشعارات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Bell className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">غير مقروءة</p>
                <p className="text-2xl font-bold text-blue-600">{summary.unread}</p>
              </div>
              <Info className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تحذيرات</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.warnings}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">أخطاء</p>
                <p className="text-2xl font-bold text-red-600">{summary.errors}</p>
              </div>
              <X className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-64">
              <Label htmlFor="search">البحث</Label>
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث في الإشعارات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="type-filter">النوع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر النوع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  {notificationTypes.map(type => (
                    <SelectItem key={type.value} value={type.value}>{type.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="read-filter">الحالة</Label>
              <Select value={filterRead} onValueChange={setFilterRead}>
                <SelectTrigger>
                  <SelectValue placeholder="الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="unread">غير مقروء</SelectItem>
                  <SelectItem value="read">مقروء</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications List */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>الإشعارات ({filteredNotifications.length})</CardTitle>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={selectedNotifications.length === filteredNotifications.length && filteredNotifications.length > 0}
              onChange={handleSelectAll}
              className="w-4 h-4"
            />
            <span className="text-sm text-muted-foreground">تحديد الكل</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {filteredNotifications.map((notif) => (
              <div
                key={notif.id}
                className={`flex items-start gap-4 p-4 rounded-lg border transition-colors cursor-pointer ${
                  notif.isRead 
                    ? 'bg-muted/30 border-border' 
                    : 'bg-background border-primary/30 shadow-sm'
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedNotifications.includes(notif.id)}
                  onChange={() => handleSelectNotification(notif.id)}
                  onClick={(e) => e.stopPropagation()}
                  className="w-4 h-4 mt-1"
                />
                
                <div className="flex-shrink-0 mt-1">
                  {getTypeIcon(notif.type)}
                </div>

                <div 
                  className="flex-1 min-w-0"
                  onClick={() => handleNotificationClick(notif)}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className={`font-medium ${notif.isRead ? 'text-muted-foreground' : 'text-foreground'}`}>
                      {notif.title}
                    </h4>
                    {!notif.isRead && (
                      <span className="w-2 h-2 bg-primary rounded-full"></span>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground">{notif.message}</p>
                  <div className="flex items-center gap-3 mt-2">
                    {getTypeBadge(notif.type)}
                    <Badge variant="outline">{getCategoryLabel(notif.category)}</Badge>
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {formatTimeAgo(notif.createdAt)}
                    </span>
                  </div>
                </div>

                <div className="flex gap-1 flex-shrink-0">
                  {!notif.isRead && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleMarkAsRead(notif.id);
                      }}
                      className="p-2 hover:bg-muted rounded-lg"
                      title="تعليم كمقروء"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteNotification(notif.id);
                    }}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    title="حذف"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {filteredNotifications.length === 0 && (
            <div className="text-center py-8">
              <Bell className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد إشعارات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default NotificationsCenter;

