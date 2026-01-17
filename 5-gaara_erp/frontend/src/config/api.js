/**
 * إعدادات API المركزية
 * Central API Configuration
 * 
 * Port Configuration:
 * - Frontend: 5505
 * - Backend: 5506
 * - Redis: 5606 (Backend + 100)
 * - Database: 5605 (Frontend + 100)
 */

// Port Configuration
export const PORTS = {
  FRONTEND: 5505,
  BACKEND: 5506,
  REDIS: 5606,    // Backend + 100
  DATABASE: 5605  // Frontend + 100
};

// عنوان الخادم الأساسي
export const API_BASE_URL = import.meta.env.VITE_API_URL ||
  import.meta.env.VITE_BACKEND_URL ||
  `http://localhost:${PORTS.BACKEND}`;

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
    GET: (id) => `/api/users/${id}`,
    RIGHTS: '/api/users/rights',
    ASSIGN_ROLE: (id) => `/api/users/${id}/role`,
    ASSIGN_PERMISSIONS: (id) => `/api/users/${id}/permissions`
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
    LIST: '/api/reports',
    INVENTORY: '/api/reports/inventory',
    SALES: '/api/reports/sales',
    PURCHASES: '/api/reports/purchases',
    PROFIT_LOSS: '/api/reports/profit-loss',
    CUSTOM: '/api/reports/custom',
    SETUP: '/api/reports/setup',
    TEMPLATES: '/api/reports/templates',
    ADVANCED: '/api/reports/advanced'
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
    PERMISSIONS: '/api/settings/permissions',
    GENERAL: '/api/settings/general'
  },
  
  // الإدارة
  ADMIN: {
    SETUP: '/api/admin/setup',
    PERMISSIONS: '/api/admin/permissions',
    ROLES: '/api/admin/roles',
    CREATE_ROLE: '/api/admin/roles',
    UPDATE_ROLE: (id) => `/api/admin/roles/${id}`,
    DELETE_ROLE: (id) => `/api/admin/roles/${id}`,
    ASSIGN_USER_ROLE: (userId) => `/api/admin/users/${userId}/role`,
    AUDIT_LOGS: '/api/admin/audit-logs',
    STATS: '/api/admin/stats'
  },
  
  // المشتريات
  PURCHASES: {
    LIST: '/api/purchases',
    CREATE: '/api/purchases',
    UPDATE: (id) => `/api/purchases/${id}`,
    DELETE: (id) => `/api/purchases/${id}`,
    GET: (id) => `/api/purchases/${id}`,
    APPROVE: (id) => `/api/purchases/${id}/approve`,
    RECEIVE: (id) => `/api/purchases/${id}/receive`,
    STATISTICS: '/api/purchases/statistics'
  },
  
  // نظام نقطة البيع (POS)
  POS: {
    SHIFTS: '/api/pos/shifts',
    OPEN_SHIFT: '/api/pos/shifts/open',
    CLOSE_SHIFT: (id) => `/api/pos/shifts/${id}/close`,
    CURRENT_SHIFT: '/api/pos/shifts/current',
    SALES: '/api/pos/sales',
    CREATE_SALE: '/api/pos/sales',
    REFUND: (id) => `/api/pos/sales/${id}/refund`,
    STATISTICS: '/api/pos/statistics',
    SEARCH_PRODUCT: '/api/pos/products/search'
  },
  
  // نظام التقارير المتقدم
  REPORTS_SYSTEM: {
    SALES_SUMMARY: '/api/reports-system/sales/summary',
    SALES_BY_PRODUCT: '/api/reports-system/sales/by-product',
    SALES_BY_CUSTOMER: '/api/reports-system/sales/by-customer',
    STOCK_LEVELS: '/api/reports-system/inventory/stock-levels',
    EXPIRING_LOTS: '/api/reports-system/inventory/expiring-lots',
    PROFIT_LOSS: '/api/reports-system/financial/profit-loss',
    SHIFTS_PERFORMANCE: '/api/reports-system/pos/shifts-performance',
    EXPORT: '/api/reports-system/export'
  },
  
  // الأذونات والأدوار
  PERMISSIONS: {
    LIST: '/api/permissions',
    ROLES: '/api/roles',
    CREATE_ROLE: '/api/roles',
    UPDATE_ROLE: (id) => `/api/roles/${id}`,
    DELETE_ROLE: (id) => `/api/roles/${id}`,
    ASSIGN_PERMISSIONS: (id) => `/api/roles/${id}/permissions`,
    USER_PERMISSIONS: (userId) => `/api/users/${userId}/permissions`
  }
};

// إعدادات الطلبات الافتراضية
export const DEFAULT_REQUEST_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 ثانية
  credentials: 'include', // Include cookies for session
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

// Error types for better handling
export const API_ERROR_TYPES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  AUTH_ERROR: 'AUTH_ERROR',
  FORBIDDEN_ERROR: 'FORBIDDEN_ERROR',
  NOT_FOUND_ERROR: 'NOT_FOUND_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
};

// دالة مساعدة لمعالجة الأخطاء
export const handleApiError = (error) => {
  // Check for network errors (Failed to fetch)
  if (error instanceof TypeError && error.message === 'Failed to fetch') {
    return {
      type: API_ERROR_TYPES.NETWORK_ERROR,
      message: 'لا يمكن الاتصال بالخادم. تأكد من تشغيل الخادم على المنفذ ' + PORTS.BACKEND,
      messageEn: 'Cannot connect to server. Make sure the server is running on port ' + PORTS.BACKEND,
      canRetry: true,
      showErrorPage: true
    };
  }

  if (error.response) {
    // الخادم رد بكود خطأ
    const { status, data } = error.response;
    
    if (status === 401) {
      // غير مصرح - إزالة token وإعادة توجيه لتسجيل الدخول
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      return {
        type: API_ERROR_TYPES.AUTH_ERROR,
        message: 'انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى',
        messageEn: 'Session expired, please login again',
        redirect: '/login',
        canRetry: false
      };
    }
    
    if (status === 403) {
      return {
        type: API_ERROR_TYPES.FORBIDDEN_ERROR,
        message: 'ليس لديك صلاحية للوصول إلى هذا المورد',
        messageEn: 'You do not have permission to access this resource',
        redirect: '/403',
        canRetry: false
      };
    }
    
    if (status === 404) {
      return {
        type: API_ERROR_TYPES.NOT_FOUND_ERROR,
        message: 'المورد المطلوب غير موجود',
        messageEn: 'The requested resource was not found',
        canRetry: false
      };
    }
    
    if (status === 422) {
      return {
        type: API_ERROR_TYPES.VALIDATION_ERROR,
        message: data?.message || 'خطأ في البيانات المدخلة',
        messageEn: data?.messageEn || 'Invalid input data',
        errors: data?.errors || [],
        canRetry: false
      };
    }
    
    if (status >= 500) {
      return {
        type: API_ERROR_TYPES.SERVER_ERROR,
        message: 'خطأ في الخادم، يرجى المحاولة لاحقاً',
        messageEn: 'Server error, please try again later',
        canRetry: true,
        showErrorPage: true
      };
    }
    
    return {
      type: API_ERROR_TYPES.UNKNOWN_ERROR,
      message: data?.message || data?.error || 'حدث خطأ غير متوقع',
      messageEn: data?.messageEn || 'An unexpected error occurred',
      canRetry: true
    };
  }
  
  if (error.request) {
    // لم يتم الحصول على رد من الخادم
    return {
      type: API_ERROR_TYPES.NETWORK_ERROR,
      message: 'لا يمكن الاتصال بالخادم، تحقق من اتصال الإنترنت',
      messageEn: 'Cannot connect to server, check your internet connection',
      canRetry: true,
      showErrorPage: true
    };
  }
  
  // خطأ في إعداد الطلب
  return {
    type: API_ERROR_TYPES.UNKNOWN_ERROR,
    message: error.message || 'حدث خطأ غير متوقع',
    messageEn: error.messageEn || 'An unexpected error occurred',
    canRetry: true
  };
};

// دالة مساعدة لإجراء طلبات API مع معالجة أفضل للأخطاء
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
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), config.timeout || 30000);
    
    const response = await fetch(url, {
      ...config,
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const error = new Error(errorData.message || errorData.error || `HTTP ${response.status}`);
      error.response = { status: response.status, data: errorData };
      throw error;
    }
    
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return response;
  } catch (error) {
    if (error.name === 'AbortError') {
      const timeoutError = {
        type: API_ERROR_TYPES.TIMEOUT_ERROR,
        message: 'انتهت مهلة الاتصال بالخادم',
        messageEn: 'Connection to server timed out',
        canRetry: true
      };
      throw timeoutError;
    }
    
    const handledError = handleApiError(error);
    throw handledError;
  }
};

// دالة للتحقق من حالة الاتصال بالخادم
export const checkServerStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    return response.ok;
  } catch {
    return false;
  }
};

// Export port configuration for use in other files
export const getPortConfig = () => ({
  frontend: PORTS.FRONTEND,
  backend: PORTS.BACKEND,
  redis: PORTS.REDIS,
  database: PORTS.DATABASE,
  apiUrl: API_BASE_URL
});
