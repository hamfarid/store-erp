import React, { useState, useEffect, useContext, createContext } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

// Notification Context
const NotificationContext = createContext()

export const useNotifications = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotifications must be used within a NotificationProvider')
  }
  return context
}

// Notification Provider
export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [settings, setSettings] = useState({
    sound: true,
    desktop: true,
    email: false,
    lowStock: true,
    newOrders: true,
    systemUpdates: true
  })

  useEffect(() => {
    loadNotifications()
    loadSettings()
    
    // Set up real-time notifications (WebSocket or polling)
    const interval = setInterval(checkForNewNotifications, 30000) // Check every 30 seconds
    
    return () => clearInterval(interval)
  }, [])

  const loadNotifications = async () => {
    try {
      const response = await ApiService.get('/api/notifications')
      if (response.success) {
        setNotifications(response.data)
        setUnreadCount(response.data.filter(n => !n.read).length)
      }
    } catch (error) {
      // Use mock data
      const mockNotifications = [
        {
          id: 1,
          type: 'warning',
          title: 'مخزون منخفض',
          message: 'بذور الطماطم - الكمية المتبقية: 5 وحدات',
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          read: false,
          category: 'inventory'
        },
        {
          id: 2,
          type: 'success',
          title: 'طلب جديد',
          message: 'تم استلام طلب جديد من العميل أحمد محمد',
          timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          read: false,
          category: 'orders'
        },
        {
          id: 3,
          type: 'info',
          title: 'تحديث النظام',
          message: 'تم تحديث النظام إلى الإصدار 1.2.0',
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
          read: true,
          category: 'system'
        }
      ]
      setNotifications(mockNotifications)
      setUnreadCount(mockNotifications.filter(n => !n.read).length)
    }
  }

  const loadSettings = async () => {
    try {
      const response = await ApiService.get('/api/notifications/settings')
      if (response.success) {
        setSettings(response.data)
      }
    } catch (error) {
      }
  }

  const checkForNewNotifications = async () => {
    try {
      const response = await ApiService.get('/api/notifications/new')
      if (response.success && response.data.length > 0) {
        const newNotifications = response.data
        setNotifications(prev => [...newNotifications, ...prev])
        setUnreadCount(prev => prev + newNotifications.length)
        
        // Show toast for new notifications
        newNotifications.forEach(notification => {
          showNotificationToast(notification)
        })
        
        // Play sound if enabled
        if (settings.sound) {
          playNotificationSound()
        }
        
        // Show desktop notification if enabled
        if (settings.desktop && 'Notification' in window) {
          showDesktopNotification(newNotifications[0])
        }
      }
    } catch (error) {
      }
  }

  const showNotificationToast = (notification) => {
    const toastOptions = {
      duration: 5000,
      position: 'top-right'
    }

    switch (notification.type) {
      case 'success':
        toast.success(notification.message, toastOptions)
        break
      case 'warning':
        toast.error(notification.message, toastOptions)
        break
      case 'error':
        toast.error(notification.message, toastOptions)
        break
      default:
        toast(notification.message, toastOptions)
    }
  }

  const playNotificationSound = () => {
    try {
      const audio = new Audio('/notification-sound.mp3')
      audio.volume = 0.5
      audio.play().catch(_e => { /* Audio play failed silently */ })
    } catch (_) {
      /* Fallback for audio errors */
    }
  }

  const showDesktopNotification = (notification) => {
    if (Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        tag: notification.id
      })
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          showDesktopNotification(notification)
        }
      })
    }
  }

  const markAsRead = async (notificationId) => {
    try {
      await ApiService.post(`/api/notifications/${notificationId}/read`)
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      )
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (error) {
      }
  }

  const markAllAsRead = async () => {
    try {
      await ApiService.post('/api/notifications/mark-all-read')
      setNotifications(prev => prev.map(n => ({ ...n, read: true })))
      setUnreadCount(0)
    } catch (error) {
      }
  }

  const deleteNotification = async (notificationId) => {
    try {
      await ApiService.delete(`/api/notifications/${notificationId}`)
      setNotifications(prev => prev.filter(n => n.id !== notificationId))
      const notification = notifications.find(n => n.id === notificationId)
      if (notification && !notification.read) {
        setUnreadCount(prev => Math.max(0, prev - 1))
      }
    } catch (error) {
      }
  }

  const updateSettings = async (newSettings) => {
    try {
      await ApiService.post('/api/notifications/settings', newSettings)
      setSettings(newSettings)
      toast.success('تم حفظ إعدادات الإشعارات')
    } catch (error) {
      toast.error('خطأ في حفظ إعدادات الإشعارات')
    }
  }

  const addNotification = (notification) => {
    const newNotification = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      read: false,
      ...notification
    }
    setNotifications(prev => [newNotification, ...prev])
    setUnreadCount(prev => prev + 1)
    showNotificationToast(newNotification)
  }

  const value = {
    notifications,
    unreadCount,
    settings,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    updateSettings,
    addNotification,
    loadNotifications
  }

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  )
}

// Notification Bell Component
export const NotificationBell = () => {
  const { notifications, unreadCount, markAsRead, markAllAsRead, deleteNotification } = useNotifications()
  const [isOpen, setIsOpen] = useState(false)

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-primary" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-accent" />
      case 'error':
        return <AlertTriangle className="w-5 h-5 text-destructive" />
      default:
        return <Info className="w-5 h-5 text-primary-600" />
    }
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInMinutes = Math.floor((now - date) / (1000 * 60))
    
    if (diffInMinutes < 1) return 'الآن'
    if (diffInMinutes < 60) return `منذ ${diffInMinutes} دقيقة`
    if (diffInMinutes < 1440) return `منذ ${Math.floor(diffInMinutes / 60)} ساعة`
    return `منذ ${Math.floor(diffInMinutes / 1440)} يوم`
  }

  return (
    <div className="relative">
      {/* Bell Icon */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-muted-foreground hover:text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-destructive/100 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute left-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-border z-50" dir="rtl">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <h3 className="text-lg font-semibold text-foreground">الإشعارات</h3>
            <div className="flex items-center space-x-2 space-x-reverse">
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-sm text-primary-600 hover:text-primary-800"
                >
                  تحديد الكل كمقروء
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Notifications List */}
          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-4 text-center text-gray-500">
                لا توجد إشعارات
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 border-b border-gray-100 hover:bg-muted/50 ${
                    !notification.read ? 'bg-primary-50' : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 space-x-reverse flex-1">
                      {getNotificationIcon(notification.type)}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground">
                          {notification.title}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">
                          {notification.message}
                        </p>
                        <p className="text-xs text-gray-400 mt-2">
                          {formatTimestamp(notification.timestamp)}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-1 space-x-reverse">
                      {!notification.read && (
                        <button
                          onClick={() => markAsRead(notification.id)}
                          className="text-primary-600 hover:text-primary-800"
                          title="تحديد كمقروء"
                        >
                          <Check className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={() => deleteNotification(notification.id)}
                        className="text-destructive hover:text-red-800"
                        title="حذف"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          {notifications.length > 0 && (
            <div className="p-3 border-t border-border text-center">
              <button className="text-sm text-primary-600 hover:text-primary-800">
                عرض جميع الإشعارات
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Notification Settings Component
export const NotificationSettings = () => {
  const { settings, updateSettings } = useNotifications()
  const [localSettings, setLocalSettings] = useState(settings)

  useEffect(() => {
    setLocalSettings(settings)
  }, [settings])

  const handleSettingChange = (key, value) => {
    setLocalSettings(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleSave = () => {
    updateSettings(localSettings)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-border p-6" dir="rtl">
      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
        <Settings className="w-5 h-5 ml-2" />
        إعدادات الإشعارات
      </h3>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {localSettings.sound ? (
              <Volume2 className="w-5 h-5 text-muted-foreground ml-2" />
            ) : (
              <VolumeX className="w-5 h-5 text-muted-foreground ml-2" />
            )}
            <span className="text-sm font-medium text-foreground">الصوت</span>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={localSettings.sound}
              onChange={(e) => handleSettingChange('sound', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">إشعارات سطح المكتب</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={localSettings.desktop}
              onChange={(e) => handleSettingChange('desktop', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">المخزون المنخفض</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={localSettings.lowStock}
              onChange={(e) => handleSettingChange('lowStock', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">الطلبات الجديدة</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={localSettings.newOrders}
              onChange={(e) => handleSettingChange('newOrders', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">تحديثات النظام</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={localSettings.systemUpdates}
              onChange={(e) => handleSettingChange('systemUpdates', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>
      </div>

      <div className="mt-6">
        <button
          onClick={handleSave}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors"
        >
          حفظ الإعدادات
        </button>
      </div>
    </div>
  )
}

