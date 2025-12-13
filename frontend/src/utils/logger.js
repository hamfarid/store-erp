/**
 * نظام التسجيل للواجهة الأمامية
 * Frontend Logging System
 */

import api from '../services/api';

class FrontendLogger {
  constructor() {
    this.isEnabled = true;
    this.queue = [];
    this.batchSize = 10;
    this.flushInterval = 5000; // 5 ثوان
    
    // بدء التسجيل التلقائي
    this.startAutoFlush();
    
    // تسجيل أحداث النظام
    this.setupSystemListeners();
  }

  /**
   * تسجيل النقرة على زر
   */
  logClick(buttonId, buttonText = '', additionalData = {}) {
    if (!this.isEnabled) return;

    const clickData = {
      type: 'click',
      button_id: buttonId,
      button_text: buttonText,
      page: window.location.pathname,
      timestamp: new Date().toISOString(),
      user_agent: navigator.userAgent,
      screen_resolution: `${screen.width}x${screen.height}`,
      additional_data: {
        ...additionalData,
        url: window.location.href,
        referrer: document.referrer
      }
    };

    this.addToQueue(clickData);
    
    // تسجيل محلي للتطوير (معطل في الإنتاج)
  }

  /**
   * تسجيل تغيير المسار
   */
  logRoute(route, method = 'GET', additionalData = {}) {
    if (!this.isEnabled) return;

    const routeData = {
      type: 'route',
      route: route,
      method: method,
      timestamp: new Date().toISOString(),
      additional_data: {
        ...additionalData,
        previous_url: document.referrer,
        session_storage_size: this.getStorageSize('sessionStorage'),
        local_storage_size: this.getStorageSize('localStorage')
      }
    };

    this.addToQueue(routeData);
    
  }

  /**
   * تسجيل الأخطاء
   */
  logError(error, context = {}) {
    if (!this.isEnabled) return;

    const errorData = {
      type: 'error',
      error_message: error.message || String(error),
      error_stack: error.stack || '',
      timestamp: new Date().toISOString(),
      page: window.location.pathname,
      context: context
    };

    this.addToQueue(errorData);
    
    // إرسال الأخطاء فوراً
    this.sendToServer([errorData]);
    
    }

  /**
   * تسجيل أحداث مخصصة
   */
  logEvent(eventType, eventData = {}) {
    if (!this.isEnabled) return;

    const customEventData = {
      type: 'custom_event',
      event_type: eventType,
      timestamp: new Date().toISOString(),
      page: window.location.pathname,
      data: eventData
    };

    this.addToQueue(customEventData);
    
  }

  /**
   * إضافة إلى قائمة الانتظار
   */
  addToQueue(data) {
    this.queue.push(data);
    
    // إرسال فوري إذا امتلأت القائمة
    if (this.queue.length >= this.batchSize) {
      this.flush();
    }
  }

  /**
   * إرسال البيانات المتراكمة
   */
  async flush() {
    if (this.queue.length === 0) return;

    const dataToSend = [...this.queue];
    this.queue = [];

    await this.sendToServer(dataToSend);
  }

  /**
   * إرسال البيانات للخادم
   */
  async sendToServer(data) {
    try {
      // إرسال النقرات
      const clicks = data.filter(item => item.type === 'click');
      if (clicks.length > 0) {
        for (const click of clicks) {
          await api.post('/log/click', click);
        }
      }

      // يمكن إضافة endpoints أخرى للأنواع المختلفة
      
    } catch (error) {
      // إعادة البيانات للقائمة في حالة الفشل
      this.queue.unshift(...data);
    }
  }

  /**
   * بدء التسجيل التلقائي
   */
  startAutoFlush() {
    setInterval(() => {
      this.flush();
    }, this.flushInterval);

    // إرسال البيانات عند إغلاق الصفحة
    window.addEventListener('beforeunload', () => {
      this.flush();
    });
  }

  /**
   * إعداد مستمعي أحداث النظام
   */
  setupSystemListeners() {
    // تسجيل الأخطاء التلقائي
    window.addEventListener('error', (event) => {
      this.logError(event.error || new Error(event.message), {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      });
    });

    // تسجيل الأخطاء غير المعالجة في Promise
    window.addEventListener('unhandledrejection', (event) => {
      this.logError(event.reason, {
        type: 'unhandled_promise_rejection'
      });
    });

    // تسجيل تغييرات المسار (للـ SPA)
    let currentPath = window.location.pathname;
    const observer = new MutationObserver(() => {
      if (window.location.pathname !== currentPath) {
        this.logRoute(window.location.pathname);
        currentPath = window.location.pathname;
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  /**
   * حساب حجم التخزين
   */
  getStorageSize(storageType) {
    try {
      const storage = window[storageType];
      let size = 0;
      for (let key in storage) {
        if (Object.prototype.hasOwnProperty.call(storage, key)) {
          size += storage[key].length + key.length;
        }
      }
      return size;
    } catch {
      return 0;
    }
  }

  /**
   * تمكين/تعطيل التسجيل
   */
  setEnabled(enabled) {
    this.isEnabled = enabled;
  }

  /**
   * مسح قائمة الانتظار
   */
  clearQueue() {
    this.queue = [];
  }
}

// إنشاء instance عام
const logger = new FrontendLogger();

// دوال مساعدة سريعة
export const logClick = (buttonId, buttonText, additionalData) => {
  logger.logClick(buttonId, buttonText, additionalData);
};

export const logRoute = (route, method, additionalData) => {
  logger.logRoute(route, method, additionalData);
};

export const logError = (error, context) => {
  logger.logError(error, context);
};

export const logEvent = (eventType, eventData) => {
  logger.logEvent(eventType, eventData);
};

// Hook للاستخدام مع React
export const useLogger = () => {
  return {
    logClick,
    logRoute,
    logError,
    logEvent
  };
};

export default logger;
