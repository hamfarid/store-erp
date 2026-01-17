// /home/ubuntu/upload/store_v1.5/complete_inventory_system/frontend/src/config/api.js
/**
 * إعدادات API المركزية
 * Central API Configuration
 */

// عنوان الخادم الأساسي - Use backend URL directly
export const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production'
    ? 'http://localhost:5002'
    : 'http://localhost:5002');

// نقاط النهاية للـ API
export const API_ENDPOINTS = {
  // المصادقة
  AUTH: {
    LOGIN: '/api/auth/login',
    LOGOUT: '/api/auth/logout',
    REFRESH: '/api/auth/refresh',
    STATUS: '/api/auth/status',
    REGISTER: '/api/auth/register'
  },
  
  // المستخدمين
  USERS: {
    LIST: '/api/users',
    CREATE: '/api/users',
    UPDATE: (id) => `/api/users/${id}`,
    DELETE: (id) => `/api/users/${id}`,
    GET: (id) => `/api/users/${id}`
  },
  
  // المنتجات
  PRODUCTS: {
    LIST: '/api/products',
    CREATE: '/api/products',
    UPDATE: (id) => `/api/products/${id}`,
    DELETE: (id) => `/api/products/${id}`,
    GET: (id) => `/api/products/${id}`,
    SEARCH: '/api/products/search'
  },
  
  // المخزون
  INVENTORY: {
    LIST: '/api/inventory',
    UPDATE: (id) => `/api/inventory/${id}`,
    MOVEMENTS: '/api/inventory/movements',
    ADJUST: '/api/inventory/adjust'
  },
  
  // العملاء
  CUSTOMERS: {
    LIST: '/api/customers',
    CREATE: '/api/customers',
    UPDATE: (id) => `/api/customers/${id}`,
    DELETE: (id) => `/api/customers/${id}`,
    GET: (id) => `/api/customers/${id}`
  },
  
  // الموردين
  SUPPLIERS: {
    LIST: '/api/suppliers',
    CREATE: '/api/suppliers',
    UPDATE: (id) => `/api/suppliers/${id}`,
    DELETE: (id) => `/api/suppliers/${id}`,
    GET: (id) => `/api/suppliers/${id}`
  },
  
  // الفواتير
  INVOICES: {
    LIST: '/api/invoices',
    CREATE: '/api/invoices',
    UPDATE: (id) => `/api/invoices/${id}`,
    DELETE: (id) => `/api/invoices/${id}`,
    GET: (id) => `/api/invoices/${id}`,
    PRINT: (id) => `/api/invoices/${id}/print`
  },
  
  // المخازن
  WAREHOUSES: {
    LIST: '/api/warehouses',
    CREATE: '/api/warehouses',
    UPDATE: (id) => `/api/warehouses/${id}`,
    DELETE: (id) => `/api/warehouses/${id}`,
    GET: (id) => `/api/warehouses/${id}`
  },
  
  // الفئات
  CATEGORIES: {
    LIST: '/api/categories',
    CREATE: '/api/categories',
    UPDATE: (id) => `/api/categories/${id}`,
    DELETE: (id) => `/api/categories/${id}`,
    GET: (id) => `/api/categories/${id}`
  },
  
  // التقارير
  REPORTS: {
    INVENTORY: '/api/reports/inventory',
    SALES: '/api/reports/sales',
    PURCHASES: '/api/reports/purchases',
    PROFIT_LOSS: '/api/reports/profit-loss',
    CUSTOM: '/api/reports/custom'
  },
  
  // المحاسبة
  ACCOUNTING: {
    ACCOUNTS: '/api/accounting/accounts',
    ENTRIES: '/api/accounting/entries',
    BALANCE: '/api/accounting/balance',
    TRIAL_BALANCE: '/api/accounting/trial-balance'
  },
  
  // الإعدادات
  SETTINGS: {
    COMPANY: '/api/settings/company',
    SYSTEM: '/api/settings/system',
    PERMISSIONS: '/api/settings/permissions'
  }
};

// إعدادات الطلبات الافتراضية
export const DEFAULT_REQUEST_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 ثانية
};

// دالة مساعدة لبناء URL كامل
export const buildApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

// دالة مساعدة للحصول على headers مع token
export const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    ...DEFAULT_REQUEST_CONFIG.headers,
    ...(token && { Authorization: `Bearer ${token}` })
  };
};

// دالة مساعدة لمعالجة الأخطاء
export const handleApiError = (error) => {
  if (error.response) {
    // الخادم رد بكود خطأ
    const { status, data } = error.response;
    
    if (status === 401) {
      // غير مصرح - إزالة token وإعادة توجيه لتسجيل الدخول
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
      return 'انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى';
    }
    
    if (status === 403) {
      return 'ليس لديك صلاحية للوصول إلى هذا المورد';
    }
    
    if (status === 404) {
      return 'المورد المطلوب غير موجود';
    }
    
    if (status >= 500) {
      return 'خطأ في الخادم، يرجى المحاولة لاحقاً';
    }
    
    return data?.message || data?.error || 'حدث خطأ غير متوقع';
  }
  
  if (error.request) {
    // لم يتم الحصول على رد من الخادم
    return 'لا يمكن الاتصال بالخادم، تحقق من اتصال الإنترنت';
  }
  
  // خطأ في إعداد الطلب
  return error.message || 'حدث خطأ غير متوقع';
};

// دالة مساعدة لإجراء طلبات API
export const apiRequest = async (endpoint, options = {}) => {
  const url = buildApiUrl(endpoint);
  const config = {
    ...DEFAULT_REQUEST_CONFIG,
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers
    }
  };
  
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || errorData.error || `HTTP ${response.status}`);
    }
    
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return response;
  } catch (error) {
    throw new Error(handleApiError(error));
  }
};

