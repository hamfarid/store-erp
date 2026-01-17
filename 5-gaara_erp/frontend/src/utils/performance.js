/**
 * أدوات تحسين الأداء
 * Performance Optimization Utils
 */

import React from 'react';

// تحسين lazy loading للصور
export const lazyLoadImage = (src, placeholder = '/placeholder.jpg') => {
  return new Promise((resolve, _reject) => {
    const img = new Image();
    img.onload = () => resolve(src);
    img.onerror = () => resolve(placeholder);
    img.src = src;
  });
};

// تحسين debounce للبحث
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// تحسين throttle للأحداث
export const throttle = (func, limit) => {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// تحسين تخزين مؤقت للبيانات
class DataCache {
  constructor(maxSize = 100, ttl = 300000) { // 5 دقائق افتراضي
    this.cache = new Map();
    this.maxSize = maxSize;
    this.ttl = ttl;
  }
  
  set(key, value) {
    // حذف أقدم عنصر إذا تجاوز الحد الأقصى
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
  }
  
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    // فحص انتهاء الصلاحية
    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }
  
  clear() {
    this.cache.clear();
  }
}

export const dataCache = new DataCache();

// تحسين تحميل المكونات
export const loadComponent = async (componentPath) => {
  try {
    const module = await import(componentPath);
    return module.default;
  } catch (error) {
    console.error(`فشل في تحميل المكون: ${componentPath}`, error);
    return null;
  }
};

// تحسين معالجة الأخطاء
export const withErrorBoundary = (Component, fallback = null) => {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = { hasError: false };
    }
    
    static getDerivedStateFromError(_error) {
      return { hasError: true };
    }
    
    componentDidCatch(error, errorInfo) {
      console.error('خطأ في المكون:', error, errorInfo);
    }
    
    render() {
      if (this.state.hasError) {
        return fallback || <div>حدث خطأ في تحميل المكون</div>;
      }
      
      return <Component {...this.props} />;
    }
  };
};

// تحسين قياس الأداء
export const measurePerformance = (name, fn) => {
  return async (...args) => {
    const start = performance.now();
    try {
      const result = await fn(...args);
      const end = performance.now();
      console.log(`⏱️ ${name}: ${(end - start).toFixed(2)}ms`);
      return result;
    } catch (error) {
      const end = performance.now();
      console.error(`❌ ${name} فشل في ${(end - start).toFixed(2)}ms:`, error);
      throw error;
    }
  };
};

// تحسين تحميل البيانات
export const optimizedFetch = async (url, options = {}) => {
  const cacheKey = `${url}_${JSON.stringify(options)}`;
  
  // محاولة جلب من التخزين المؤقت
  const cached = dataCache.get(cacheKey);
  if (cached) {
    return cached;
  }
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // حفظ في التخزين المؤقت
    dataCache.set(cacheKey, data);
    
    return data;
  } catch (error) {
    console.error('خطأ في جلب البيانات:', error);
    throw error;
  }
};