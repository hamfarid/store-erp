/**
 * Notification Context
 * @file frontend/src/contexts/NotificationContext.jsx
 * 
 * سياق الإشعارات للتطبيق
 */

import React, { createContext, useContext, useReducer, useCallback, useEffect, useRef } from 'react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// ============================================
// Actions
// ============================================
const NOTIFICATION_ACTIONS = {
  SET_NOTIFICATIONS: 'SET_NOTIFICATIONS',
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  MARK_AS_READ: 'MARK_AS_READ',
  MARK_ALL_AS_READ: 'MARK_ALL_AS_READ',
  REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
  SET_LOADING: 'SET_LOADING',
  SET_UNREAD_COUNT: 'SET_UNREAD_COUNT'
};

// ============================================
// Initial State
// ============================================
const initialState = {
  notifications: [],
  unreadCount: 0,
  isLoading: false
};

// ============================================
// Reducer
// ============================================
function notificationReducer(state, action) {
  switch (action.type) {
    case NOTIFICATION_ACTIONS.SET_NOTIFICATIONS:
      return {
        ...state,
        notifications: action.payload,
        unreadCount: action.payload.filter(n => !n.read).length
      };

    case NOTIFICATION_ACTIONS.ADD_NOTIFICATION:
      return {
        ...state,
        notifications: [action.payload, ...state.notifications],
        unreadCount: state.unreadCount + (action.payload.read ? 0 : 1)
      };

    case NOTIFICATION_ACTIONS.MARK_AS_READ:
      return {
        ...state,
        notifications: state.notifications.map(n =>
          n.id === action.payload ? { ...n, read: true } : n
        ),
        unreadCount: Math.max(0, state.unreadCount - 1)
      };

    case NOTIFICATION_ACTIONS.MARK_ALL_AS_READ:
      return {
        ...state,
        notifications: state.notifications.map(n => ({ ...n, read: true })),
        unreadCount: 0
      };

    case NOTIFICATION_ACTIONS.REMOVE_NOTIFICATION:
      const removed = state.notifications.find(n => n.id === action.payload);
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload),
        unreadCount: removed && !removed.read 
          ? Math.max(0, state.unreadCount - 1) 
          : state.unreadCount
      };

    case NOTIFICATION_ACTIONS.SET_LOADING:
      return { ...state, isLoading: action.payload };

    case NOTIFICATION_ACTIONS.SET_UNREAD_COUNT:
      return { ...state, unreadCount: action.payload };

    default:
      return state;
  }
}

// ============================================
// Context
// ============================================
const NotificationContext = createContext(null);

export function NotificationProvider({ children }) {
  const [state, dispatch] = useReducer(notificationReducer, initialState);
  const pollingRef = useRef(null);

  // Fetch notifications
  const fetchNotifications = useCallback(async () => {
    dispatch({ type: NOTIFICATION_ACTIONS.SET_LOADING, payload: true });
    try {
      const response = await apiClient.get('/api/notifications');
      dispatch({
        type: NOTIFICATION_ACTIONS.SET_NOTIFICATIONS,
        payload: response.data.notifications || response.data || []
      });
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    } finally {
      dispatch({ type: NOTIFICATION_ACTIONS.SET_LOADING, payload: false });
    }
  }, []);

  // Fetch unread count only
  const fetchUnreadCount = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/notifications/unread-count');
      dispatch({
        type: NOTIFICATION_ACTIONS.SET_UNREAD_COUNT,
        payload: response.data.count || 0
      });
    } catch (error) {
      console.error('Failed to fetch unread count:', error);
    }
  }, []);

  // Mark as read
  const markAsRead = useCallback(async (notificationId) => {
    try {
      await apiClient.patch(`/api/notifications/${notificationId}/read`);
      dispatch({
        type: NOTIFICATION_ACTIONS.MARK_AS_READ,
        payload: notificationId
      });
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  }, []);

  // Mark all as read
  const markAllAsRead = useCallback(async () => {
    try {
      await apiClient.patch('/api/notifications/read-all');
      dispatch({ type: NOTIFICATION_ACTIONS.MARK_ALL_AS_READ });
    } catch (error) {
      console.error('Failed to mark all as read:', error);
    }
  }, []);

  // Remove notification
  const removeNotification = useCallback(async (notificationId) => {
    try {
      await apiClient.delete(`/api/notifications/${notificationId}`);
      dispatch({
        type: NOTIFICATION_ACTIONS.REMOVE_NOTIFICATION,
        payload: notificationId
      });
    } catch (error) {
      console.error('Failed to remove notification:', error);
    }
  }, []);

  // Add local notification (for real-time)
  const addNotification = useCallback((notification) => {
    dispatch({
      type: NOTIFICATION_ACTIONS.ADD_NOTIFICATION,
      payload: notification
    });

    // Show toast based on type
    const toastOptions = { duration: 5000 };
    switch (notification.type) {
      case 'success':
        toast.success(notification.message, toastOptions);
        break;
      case 'error':
        toast.error(notification.message, toastOptions);
        break;
      case 'warning':
        toast(notification.message, { ...toastOptions, icon: '⚠️' });
        break;
      default:
        toast(notification.message, { ...toastOptions, icon: 'ℹ️' });
    }
  }, []);

  // Show toast notification
  const showToast = useCallback((message, type = 'info') => {
    switch (type) {
      case 'success':
        toast.success(message);
        break;
      case 'error':
        toast.error(message);
        break;
      case 'warning':
        toast(message, { icon: '⚠️' });
        break;
      case 'loading':
        return toast.loading(message);
      default:
        toast(message, { icon: 'ℹ️' });
    }
  }, []);

  // Start polling for notifications
  const startPolling = useCallback((intervalMs = 60000) => {
    if (pollingRef.current) return;
    
    pollingRef.current = setInterval(() => {
      fetchUnreadCount();
    }, intervalMs);
  }, [fetchUnreadCount]);

  // Stop polling
  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  // Initial fetch
  useEffect(() => {
    fetchNotifications();
    startPolling();

    return () => {
      stopPolling();
    };
  }, [fetchNotifications, startPolling, stopPolling]);

  // Context value
  const value = {
    // State
    notifications: state.notifications,
    unreadCount: state.unreadCount,
    isLoading: state.isLoading,

    // Actions
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead,
    removeNotification,
    addNotification,
    showToast,
    startPolling,
    stopPolling,

    // Helpers
    hasUnread: state.unreadCount > 0
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

// ============================================
// Hook
// ============================================
export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within a NotificationProvider');
  }
  return context;
}

export default NotificationContext;
