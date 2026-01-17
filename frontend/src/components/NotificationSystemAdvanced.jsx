import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, Upload, Settings, CheckCircle, XCircle, AlertTriangle, Package, User, Calendar, Clock
} from 'lucide-react';

const NotificationSystemAdvanced = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifications, setShowNotifications] = useState(false);
  const [filter, setFilter] = useState('all'); // all, unread, alerts, info
  const [loading, setLoading] = useState(true);

  // بيانات تجريبية للإشعارات
  const demoNotifications = [
    {
      id: 1,
      type: 'alert',
      title: 'مخزون منخفض',
      message: 'المنتج "بذور طماطم هجين" وصل إلى الحد الأدنى (10 وحدات متبقية)',
      icon: 'package',
      priority: 'high',
      read: false,
      created_at: '2024-07-08 10:30:00',
      action_url: '/products/1',
      category: 'inventory'
    },
    {
      id: 2,
      type: 'warning',
      title: 'لوت قريب من الانتهاء',
      message: 'اللوت LOT-2024-003 للمنتج "مبيد حشري طبيعي" ينتهي خلال 7 أيام',
      icon: 'calendar',
      priority: 'medium',
      read: false,
      created_at: '2024-07-08 09:15:00',
      action_url: '/lots/3',
      category: 'expiry'
    },
    {
      id: 3,
      type: 'info',
      title: 'فاتورة جديدة',
      message: 'تم إنشاء فاتورة مبيعات جديدة INV-2024-001 للعميل "مزرعة الأمل"',
      icon: 'info',
      priority: 'low',
      read: true,
      created_at: '2024-07-08 08:45:00',
      action_url: '/invoices/1',
      category: 'sales'
    },
    {
      id: 4,
      type: 'success',
      title: 'تم استلام شحنة',
      message: 'تم استلام شحنة جديدة من المورد "شركة البذور المصرية" بنجاح',
      icon: 'check-circle',
      priority: 'low',
      read: true,
      created_at: '2024-07-07 16:20:00',
      action_url: '/stock-movements',
      category: 'receiving'
    },
    {
      id: 5,
      type: 'alert',
      title: 'فاتورة مستحقة',
      message: 'الفاتورة INV-2024-002 مستحقة الدفع منذ 5 أيام',
      icon: 'clock',
      priority: 'high',
      read: false,
      created_at: '2024-07-07 14:30:00',
      action_url: '/invoices/2',
      category: 'payment'
    },
    {
      id: 6,
      type: 'warning',
      title: 'تجاوز حد الائتمان',
      message: 'العميل "شركة الزراعة الحديثة" تجاوز حد الائتمان المسموح',
      icon: 'trending-down',
      priority: 'medium',
      read: false,
      created_at: '2024-07-07 12:15:00',
      action_url: '/customers/2',
      category: 'credit'
    }
  ];

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      setLoading(true);
      // محاكاة تحميل البيانات
      setTimeout(() => {
        setNotifications(demoNotifications);
        const unread = demoNotifications.filter(n => !n.read).length;
        setUnreadCount(unread);
        setLoading(false);
      }, 1000);
    } catch (error) {
      setLoading(false);
    }
  };

  const markAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read: true }
          : notification
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
    setUnreadCount(0);
  };

  const deleteNotification = (notificationId) => {
    setNotifications(prev => 
      prev.filter(notification => notification.id !== notificationId)
    );
    const notification = notifications.find(n => n.id === notificationId);
    if (notification && !notification.read) {
      setUnreadCount(prev => Math.max(0, prev - 1));
    }
  };

  const filteredNotifications = notifications.filter(notification => {
    switch (filter) {
      case 'unread':
        return !notification.read;
      case 'alerts':
        return notification.type === 'alert' || notification.type === 'warning';
      case 'info':
        return notification.type === 'info' || notification.type === 'success';
      default:
        return true;
    }
  });

  const getNotificationIcon = (iconType) => {
    const iconProps = { className: "h-5 w-5" };
    
    switch (iconType) {
      case 'package':
        return <Package {...iconProps} />;
      case 'calendar':
        return <Calendar {...iconProps} />;
      case 'info':
        return <Info {...iconProps} />;
      case 'check-circle':
        return <CheckCircle {...iconProps} />;
      case 'clock':
        return <Clock {...iconProps} />;
      case 'trending-down':
        return <TrendingDown {...iconProps} />;
      default:
        return <Bell {...iconProps} />;
    }
  };

  const getNotificationColor = (type, _priority) => {
    const baseClasses = "p-4 rounded-lg border-r-4 ";
    
    switch (type) {
      case 'alert':
        return baseClasses + "bg-destructive/10 border-red-400 text-red-800";
      case 'warning':
        return baseClasses + "bg-accent/10 border-orange-400 text-orange-800";
      case 'success':
        return baseClasses + "bg-primary/10 border-green-400 text-green-800";
      case 'info':
      default:
        return baseClasses + "bg-primary-50 border-primary-400 text-primary-800";
    }
  };

  const getPriorityBadge = (priority) => {
    const baseClasses = "inline-flex px-2 py-1 text-xs font-semibold rounded-full ";
    
    switch (priority) {
      case 'high':
        return baseClasses + "bg-destructive/20 text-red-800";
      case 'medium':
        return baseClasses + "bg-accent/20 text-orange-800";
      case 'low':
      default:
        return baseClasses + "bg-primary/20 text-green-800";
    }
  };

  const formatTimeAgo = (dateString) => {
    const now = new Date();
    const notificationDate = new Date(dateString);
    const diffInMinutes = Math.floor((now - notificationDate) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'الآن';
    if (diffInMinutes < 60) return `منذ ${diffInMinutes} دقيقة`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `منذ ${diffInHours} ساعة`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    return `منذ ${diffInDays} يوم`;
  };

  // مكون الإشعار الفردي
  const NotificationItem = ({ notification }) => (
    <div className={`${getNotificationColor(notification.type, notification.priority)} ${!notification.read ? 'shadow-md' : 'opacity-75'} mb-3 transition-all duration-200`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 space-x-reverse flex-1">
          <div className="flex-shrink-0 mt-1">
            {getNotificationIcon(notification.icon)}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h4 className="text-sm font-semibold">{notification.title}</h4>
              <div className="flex items-center space-x-2 space-x-reverse">
                <span className={getPriorityBadge(notification.priority)}>
                  {notification.priority === 'high' ? 'عالي' : 
                   notification.priority === 'medium' ? 'متوسط' : 'منخفض'}
                </span>
                {!notification.read && (
                  <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                )}
              </div>
            </div>
            
            <p className="text-sm mb-2">{notification.message}</p>
            
            <div className="flex items-center justify-between">
              <span className="text-xs opacity-75">
                {formatTimeAgo(notification.created_at)}
              </span>
              
              <div className="flex items-center space-x-2 space-x-reverse">
                {notification.action_url && (
                  <button className="text-xs underline hover:no-underline">
                    عرض التفاصيل
                  </button>
                )}
                
                {!notification.read && (
                  <button
                    onClick={() => markAsRead(notification.id)}
                    className="text-xs text-primary-600 hover:text-primary-800"
                  >
                    تحديد كمقروء
                  </button>
                )}
                
                <button
                  onClick={() => deleteNotification(notification.id)}
                  className="text-xs text-destructive hover:text-red-800"
                >
                  حذف
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="relative">
      {/* زر الإشعارات */}
      <button
        onClick={() => setShowNotifications(!showNotifications)}
        className="relative p-2 text-muted-foreground hover:text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md"
      >
        <Bell className="h-6 w-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-destructive/100 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* لوحة الإشعارات */}
      {showNotifications && (
        <div className="absolute left-0 mt-2 w-96 bg-white rounded-lg shadow-lg border border-border z-50 max-h-96 overflow-hidden">
          {/* رأس اللوحة */}
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-foreground">الإشعارات</h3>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            {/* أزرار الفلترة */}
            <div className="flex space-x-2 space-x-reverse">
              <button
                onClick={() => setFilter('all')}
                className={`px-3 py-1 text-xs rounded-full ${filter === 'all' ? 'bg-primary-100 text-primary-800' : 'bg-muted text-muted-foreground'}`}
              >
                الكل ({notifications.length})
              </button>
              <button
                onClick={() => setFilter('unread')}
                className={`px-3 py-1 text-xs rounded-full ${filter === 'unread' ? 'bg-primary-100 text-primary-800' : 'bg-muted text-muted-foreground'}`}
              >
                غير مقروء ({unreadCount})
              </button>
              <button
                onClick={() => setFilter('alerts')}
                className={`px-3 py-1 text-xs rounded-full ${filter === 'alerts' ? 'bg-primary-100 text-primary-800' : 'bg-muted text-muted-foreground'}`}
              >
                تنبيهات
              </button>
            </div>
            
            {/* زر تحديد الكل كمقروء */}
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="mt-2 text-xs text-primary-600 hover:text-primary-800"
              >
                تحديد الكل كمقروء
              </button>
            )}
          </div>

          {/* قائمة الإشعارات */}
          <div className="max-h-80 overflow-y-auto p-4">
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            ) : filteredNotifications.length > 0 ? (
              filteredNotifications.map(notification => (
                <NotificationItem key={notification.id} notification={notification} />
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Bell className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>لا توجد إشعارات</p>
              </div>
            )}
          </div>

          {/* تذييل اللوحة */}
          <div className="p-3 border-t border-border bg-muted/50">
            <button className="w-full text-center text-sm text-primary-600 hover:text-primary-800">
              عرض جميع الإشعارات
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationSystemAdvanced;

