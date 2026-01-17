import React, { createContext, useContext, useState, useCallback } from 'react'
import PropTypes from 'prop-types'
import './NotificationCenter.css'

// Notification Context
const NotificationContext = createContext()

// Notification Provider
export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([])
  const [isOpen, setIsOpen] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  const addNotification = useCallback((notification) => {
    const id = Date.now() + Math.random()
    const newNotification = {
      id,
      type: 'info',
      priority: 'normal',
      persistent: false,
      read: false,
      timestamp: new Date(),
      ...notification
    }

    setNotifications(prev => [newNotification, ...prev])
    setUnreadCount(prev => prev + 1)

    // Auto-remove non-persistent notifications
    if (!newNotification.persistent) {
      setTimeout(() => {
        removeNotification(id)
      }, newNotification.duration || 5000)
    }

    return id
  }, [])

  const removeNotification = useCallback((id) => {
    setNotifications(prev => {
      const notification = prev.find(n => n.id === id)
      if (notification && !notification.read) {
        setUnreadCount(count => Math.max(0, count - 1))
      }
      return prev.filter(n => n.id !== id)
    })
  }, [])

  const markAsRead = useCallback((id) => {
    setNotifications(prev => prev.map(notification => {
      if (notification.id === id && !notification.read) {
        setUnreadCount(count => Math.max(0, count - 1))
        return { ...notification, read: true }
      }
      return notification
    }))
  }, [])

  const markAllAsRead = useCallback(() => {
    setNotifications(prev => prev.map(notification => ({ ...notification, read: true })))
    setUnreadCount(0)
  }, [])

  const clearAll = useCallback(() => {
    setNotifications([])
    setUnreadCount(0)
  }, [])

  const clearRead = useCallback(() => {
    setNotifications(prev => prev.filter(n => !n.read))
  }, [])

  // Notification types
  const systemAlert = useCallback((message, options = {}) => {
    return addNotification({
      type: 'system',
      title: 'تنبيه النظام',
      message,
      icon: 'fas fa-cog',
      priority: 'high',
      persistent: true,
      ...options
    })
  }, [addNotification])

  const lowStockAlert = useCallback((productName, currentStock, minStock) => {
    return addNotification({
      type: 'warning',
      title: 'تنبيه مخزون منخفض',
      message: `مخزون ${productName} منخفض`,
      description: `المخزون الحالي: ${currentStock} | الحد الأدنى: ${minStock}`,
      icon: 'fas fa-exclamation-triangle',
      priority: 'high',
      persistent: true,
      action: {
        label: 'عرض المنتج',
        onClick: () => { /* View product */ }
      }
    })
  }, [addNotification])

  const orderNotification = useCallback((orderNumber, status) => {
    const statusConfig = {
      created: { type: 'info', title: 'طلب جديد', icon: 'fas fa-plus-circle' },
      confirmed: { type: 'success', title: 'تم تأكيد الطلب', icon: 'fas fa-check-circle' },
      shipped: { type: 'info', title: 'تم شحن الطلب', icon: 'fas fa-shipping-fast' },
      delivered: { type: 'success', title: 'تم تسليم الطلب', icon: 'fas fa-box-open' },
      cancelled: { type: 'error', title: 'تم إلغاء الطلب', icon: 'fas fa-times-circle' }
    }

    const config = statusConfig[status] || statusConfig.created

    return addNotification({
      ...config,
      message: `طلب رقم ${orderNumber}`,
      priority: 'normal',
      action: {
        label: 'عرض الطلب',
        onClick: () => { /* View order */ }
      }
    })
  }, [addNotification])

  const userActivity = useCallback((userName, action) => {
    return addNotification({
      type: 'info',
      title: 'نشاط المستخدم',
      message: `${userName} ${action}`,
      icon: 'fas fa-user',
      priority: 'low',
      duration: 3000
    })
  }, [addNotification])

  const value = {
    notifications,
    unreadCount,
    isOpen,
    setIsOpen,
    addNotification,
    removeNotification,
    markAsRead,
    markAllAsRead,
    clearAll,
    clearRead,
    systemAlert,
    lowStockAlert,
    orderNotification,
    userActivity
  }

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  )
}

// Notification Bell Component
export const NotificationBell = () => {
  const { unreadCount, isOpen, setIsOpen } = useContext(NotificationContext)

  return (
    <div className="notification-bell">
      <button
        className={`notification-bell__button ${isOpen ? 'notification-bell__button--active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={`الإشعارات ${unreadCount > 0 ? `(${unreadCount} غير مقروء)` : ''}`}
      >
        <i className="fas fa-bell"></i>
        {unreadCount > 0 && (
          <span className="notification-bell__badge">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>
    </div>
  )
}

// Notification Panel Component
export const NotificationPanel = () => {
  const {
    notifications,
    unreadCount,
    isOpen,
    setIsOpen,
    markAsRead,
    markAllAsRead,
    clearAll,
    clearRead,
    removeNotification
  } = useContext(NotificationContext)

  if (!isOpen) return null

  const handleNotificationClick = (notification) => {
    if (!notification.read) {
      markAsRead(notification.id)
    }
    if (notification.action && notification.action.onClick) {
      notification.action.onClick()
      setIsOpen(false)
    }
  }

  return (
    <div className="notification-panel">
      <div className="notification-panel__header">
        <h3 className="notification-panel__title">
          الإشعارات
          {unreadCount > 0 && (
            <span className="notification-panel__count">({unreadCount})</span>
          )}
        </h3>
        <div className="notification-panel__actions">
          {unreadCount > 0 && (
            <button
              className="notification-panel__action"
              onClick={markAllAsRead}
              title="تحديد الكل كمقروء"
            >
              <i className="fas fa-check-double"></i>
            </button>
          )}
          <button
            className="notification-panel__action"
            onClick={clearRead}
            title="حذف المقروءة"
          >
            <i className="fas fa-trash-alt"></i>
          </button>
          <button
            className="notification-panel__action"
            onClick={() => setIsOpen(false)}
            title="إغلاق"
          >
            <i className="fas fa-times"></i>
          </button>
        </div>
      </div>

      <div className="notification-panel__body">
        {notifications.length === 0 ? (
          <div className="notification-panel__empty">
            <i className="fas fa-bell-slash"></i>
            <p>لا توجد إشعارات</p>
          </div>
        ) : (
          <div className="notification-list">
            {notifications.map(notification => (
              <NotificationItem
                key={notification.id}
                notification={notification}
                onClick={() => handleNotificationClick(notification)}
                onRemove={() => removeNotification(notification.id)}
              />
            ))}
          </div>
        )}
      </div>

      {notifications.length > 0 && (
        <div className="notification-panel__footer">
          <button
            className="notification-panel__clear-all"
            onClick={clearAll}
          >
            حذف جميع الإشعارات
          </button>
        </div>
      )}
    </div>
  )
}

// Individual Notification Item
const NotificationItem = ({ notification, onClick, onRemove }) => {
  const formatTime = (timestamp) => {
    const now = new Date()
    const diff = now - timestamp
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 1) return 'الآن'
    if (minutes < 60) return `منذ ${minutes} دقيقة`
    if (hours < 24) return `منذ ${hours} ساعة`
    return `منذ ${days} يوم`
  }

  const itemClass = `
    notification-item
    notification-item--${notification.type}
    notification-item--${notification.priority}
    ${!notification.read ? 'notification-item--unread' : ''}
    ${notification.action ? 'notification-item--clickable' : ''}
  `.trim()

  return (
    <div className={itemClass} onClick={onClick}>
      <div className="notification-item__content">
        {notification.icon && (
          <div className="notification-item__icon">
            <i className={notification.icon}></i>
          </div>
        )}
        
        <div className="notification-item__body">
          <div className="notification-item__header">
            <h4 className="notification-item__title">{notification.title}</h4>
            <span className="notification-item__time">
              {formatTime(notification.timestamp)}
            </span>
          </div>
          
          <p className="notification-item__message">{notification.message}</p>
          
          {notification.description && (
            <p className="notification-item__description">{notification.description}</p>
          )}
          
          {notification.action && (
            <button className="notification-item__action">
              {notification.action.label}
            </button>
          )}
        </div>
      </div>

      <button
        className="notification-item__remove"
        onClick={(e) => {
          e.stopPropagation()
          onRemove()
        }}
        title="حذف الإشعار"
      >
        <i className="fas fa-times"></i>
      </button>
    </div>
  )
}

// Hook to use notifications
export const useNotifications = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotifications must be used within a NotificationProvider')
  }
  return context
}

export default NotificationProvider
