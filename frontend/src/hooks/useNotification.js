/**
 * useNotification Hook
 * @file frontend/src/hooks/useNotification.js
 * 
 * Hook لإدارة الإشعارات داخل التطبيق
 */

import { useState, useCallback, useEffect, useRef } from 'react';
import { toast } from 'react-hot-toast';

/**
 * أنواع الإشعارات
 */
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  LOADING: 'loading'
};

/**
 * Hook لإدارة الإشعارات
 */
export function useNotification() {
  const toastIdRef = useRef(null);

  /**
   * إظهار إشعار نجاح
   */
  const success = useCallback((message, options = {}) => {
    return toast.success(message, {
      duration: 3000,
      position: 'top-center',
      ...options
    });
  }, []);

  /**
   * إظهار إشعار خطأ
   */
  const error = useCallback((message, options = {}) => {
    return toast.error(message, {
      duration: 5000,
      position: 'top-center',
      ...options
    });
  }, []);

  /**
   * إظهار إشعار تحذير
   */
  const warning = useCallback((message, options = {}) => {
    return toast(message, {
      duration: 4000,
      position: 'top-center',
      icon: '⚠️',
      style: {
        background: '#fef3cd',
        color: '#856404',
        border: '1px solid #ffeeba'
      },
      ...options
    });
  }, []);

  /**
   * إظهار إشعار معلومات
   */
  const info = useCallback((message, options = {}) => {
    return toast(message, {
      duration: 3000,
      position: 'top-center',
      icon: 'ℹ️',
      style: {
        background: '#cce5ff',
        color: '#004085',
        border: '1px solid #b8daff'
      },
      ...options
    });
  }, []);

  /**
   * إظهار إشعار تحميل
   */
  const loading = useCallback((message = 'جاري التحميل...', options = {}) => {
    toastIdRef.current = toast.loading(message, {
      position: 'top-center',
      ...options
    });
    return toastIdRef.current;
  }, []);

  /**
   * إغلاق إشعار التحميل
   */
  const dismiss = useCallback((toastId) => {
    if (toastId) {
      toast.dismiss(toastId);
    } else if (toastIdRef.current) {
      toast.dismiss(toastIdRef.current);
      toastIdRef.current = null;
    }
  }, []);

  /**
   * تحديث إشعار التحميل إلى نجاح
   */
  const updateToSuccess = useCallback((message, toastId) => {
    const id = toastId || toastIdRef.current;
    if (id) {
      toast.success(message, { id });
      toastIdRef.current = null;
    }
  }, []);

  /**
   * تحديث إشعار التحميل إلى خطأ
   */
  const updateToError = useCallback((message, toastId) => {
    const id = toastId || toastIdRef.current;
    if (id) {
      toast.error(message, { id });
      toastIdRef.current = null;
    }
  }, []);

  /**
   * إشعار مخصص
   */
  const custom = useCallback((content, options = {}) => {
    return toast.custom(content, {
      position: 'top-center',
      ...options
    });
  }, []);

  /**
   * إظهار إشعار عملية (مع تحديث تلقائي)
   */
  const promise = useCallback(async (promiseFn, messages = {}) => {
    const {
      loading: loadingMsg = 'جاري المعالجة...',
      success: successMsg = 'تمت العملية بنجاح',
      error: errorMsg = 'حدث خطأ'
    } = messages;

    return toast.promise(promiseFn, {
      loading: loadingMsg,
      success: typeof successMsg === 'function' ? successMsg : () => successMsg,
      error: typeof errorMsg === 'function' ? errorMsg : (err) => err?.message || errorMsg
    });
  }, []);

  /**
   * إغلاق جميع الإشعارات
   */
  const dismissAll = useCallback(() => {
    toast.dismiss();
    toastIdRef.current = null;
  }, []);

  return {
    success,
    error,
    warning,
    info,
    loading,
    dismiss,
    dismissAll,
    updateToSuccess,
    updateToError,
    custom,
    promise
  };
}

/**
 * Hook لإدارة إشعارات النظام (Browser Notifications)
 */
export function useBrowserNotification() {
  const [permission, setPermission] = useState(
    typeof window !== 'undefined' && 'Notification' in window
      ? Notification.permission
      : 'denied'
  );

  /**
   * طلب إذن الإشعارات
   */
  const requestPermission = useCallback(async () => {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return 'denied';
    }

    const result = await Notification.requestPermission();
    setPermission(result);
    return result;
  }, []);

  /**
   * إرسال إشعار للمتصفح
   */
  const notify = useCallback((title, options = {}) => {
    if (permission !== 'granted') {
      console.warn('Notification permission not granted');
      return null;
    }

    const notification = new Notification(title, {
      icon: '/logo.png',
      badge: '/badge.png',
      dir: 'rtl',
      lang: 'ar',
      ...options
    });

    return notification;
  }, [permission]);

  return {
    permission,
    isSupported: 'Notification' in window,
    isGranted: permission === 'granted',
    isDenied: permission === 'denied',
    requestPermission,
    notify
  };
}

export default useNotification;
