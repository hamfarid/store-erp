// Enhanced API Service - New Implementation
// خدمة API محسنة - تطبيق جديد

import axios from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5002';
const API_TIMEOUT = 30000; // 30 seconds

// Create axios instance
const enhancedAPI = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// Request interceptor
enhancedAPI.interceptors.request.use(
  (config) => {
    // Add auth token
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken) {
      config.headers['X-CSRF-TOKEN'] = csrfToken;
    }

    // Add request timestamp
    config.headers['X-Request-Time'] = new Date().toISOString();

    // Add request ID for tracking
    config.headers['X-Request-ID'] = generateRequestId();

    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
enhancedAPI.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      return Promise.reject({
        message: 'خطأ في الاتصال بالخادم',
        type: 'network_error',
        originalError: error
      });
    }

    // Handle 401 Unauthorized
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
      return Promise.reject({
        message: 'انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى',
        type: 'session_expired'
      });
    }

    // Handle other errors
    return Promise.reject(error);
  }
);

// Utility functions
function generateRequestId() {
  return Math.random().toString(36).substr(2, 9);
}

// Enhanced API methods
const enhancedAPIService = {
  // Generic methods
  get: (url, config = {}) => enhancedAPI.get(url, config),
  post: (url, data = {}, config = {}) => enhancedAPI.post(url, data, config),
  put: (url, data = {}, config = {}) => enhancedAPI.put(url, data, config),
  patch: (url, data = {}, config = {}) => enhancedAPI.patch(url, data, config),
  delete: (url, config = {}) => enhancedAPI.delete(url, config),

  // File upload with progress
  upload: (url, formData, onUploadProgress = null) => {
    return enhancedAPI.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: onUploadProgress ? (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onUploadProgress(percentCompleted);
      } : undefined
    });
  },

  // Download file
  download: async (url, filename = null) => {
    try {
      const response = await enhancedAPI.get(url, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data]);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename || 'download';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
      
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Batch requests
  batch: (requests) => {
    return Promise.allSettled(requests.map(request => {
      const { method, url, data, config } = request;
      return enhancedAPI[method](url, data, config);
    }));
  },

  // Health check
  healthCheck: () => enhancedAPI.get('/health'),

  // Cancel token
  cancelToken: () => axios.CancelToken.source(),

  // Check if error is cancellation
  isCancel: (error) => axios.isCancel(error)
};

// Enhanced Authentication API
export const enhancedAuthAPI = {
  login: (credentials) => enhancedAPIService.post('/auth/login', credentials),
  register: (userData) => enhancedAPIService.post('/auth/register', userData),
  logout: () => enhancedAPIService.post('/auth/logout'),
  refreshToken: () => enhancedAPIService.post('/auth/refresh'),
  forgotPassword: (email) => enhancedAPIService.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => enhancedAPIService.post('/auth/reset-password', { token, password }),
  verifyEmail: (token) => enhancedAPIService.post('/auth/verify-email', { token }),
  changePassword: (data) => enhancedAPIService.post('/auth/change-password', data),
  updateProfile: (data) => enhancedAPIService.put('/auth/profile', data),
  getProfile: () => enhancedAPIService.get('/auth/profile'),
  verifyMFA: (token, code) => enhancedAPIService.post('/auth/verify-mfa', { token, code }),
  setupMFA: () => enhancedAPIService.post('/auth/setup-mfa'),
  disableMFA: (code) => enhancedAPIService.post('/auth/disable-mfa', { code })
};

// Enhanced Products API
export const enhancedProductsAPI = {
  getAll: (params = {}) => enhancedAPIService.get('/products', { params }),
  getById: (id) => enhancedAPIService.get(`/products/${id}`),
  create: (data) => enhancedAPIService.post('/products', data),
  update: (id, data) => enhancedAPIService.put(`/products/${id}`, data),
  delete: (id) => enhancedAPIService.delete(`/products/${id}`),
  search: (query, filters = {}) => enhancedAPIService.get('/products/search', { 
    params: { q: query, ...filters } 
  }),
  getCategories: () => enhancedAPIService.get('/products/categories'),
  getBrands: () => enhancedAPIService.get('/products/brands'),
  uploadImage: (id, formData, onProgress) => enhancedAPIService.upload(
    `/products/${id}/images`, 
    formData, 
    onProgress
  ),
  deleteImage: (productId, imageId) => enhancedAPIService.delete(
    `/products/${productId}/images/${imageId}`
  ),
  bulkUpdate: (data) => enhancedAPIService.post('/products/bulk-update', data),
  bulkDelete: (ids) => enhancedAPIService.post('/products/bulk-delete', { ids }),
  export: (format = 'xlsx', filters = {}) => enhancedAPIService.download(
    `/products/export?format=${format}`, 
    `products.${format}`, 
    { params: filters }
  ),
  import: (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    return enhancedAPIService.upload('/products/import', formData, onProgress);
  }
};

// Enhanced Inventory API
export const enhancedInventoryAPI = {
  getAll: (params = {}) => enhancedAPIService.get('/inventory', { params }),
  getById: (id) => enhancedAPIService.get(`/inventory/${id}`),
  updateStock: (id, data) => enhancedAPIService.patch(`/inventory/${id}/stock`, data),
  getMovements: (params = {}) => enhancedAPIService.get('/inventory/movements', { params }),
  createMovement: (data) => enhancedAPIService.post('/inventory/movements', data),
  getLowStock: (threshold = 10) => enhancedAPIService.get('/inventory/low-stock', { 
    params: { threshold } 
  }),
  getOutOfStock: () => enhancedAPIService.get('/inventory/out-of-stock'),
  bulkUpdate: (data) => enhancedAPIService.post('/inventory/bulk-update', data),
  getValuation: (date = null) => enhancedAPIService.get('/inventory/valuation', { 
    params: date ? { date } : {} 
  }),
  getAging: () => enhancedAPIService.get('/inventory/aging'),
  reconcile: (data) => enhancedAPIService.post('/inventory/reconcile', data),
  export: (format = 'xlsx') => enhancedAPIService.download(
    `/inventory/export?format=${format}`, 
    `inventory.${format}`
  )
};

// Enhanced Orders API
export const enhancedOrdersAPI = {
  getAll: (params = {}) => enhancedAPIService.get('/orders', { params }),
  getById: (id) => enhancedAPIService.get(`/orders/${id}`),
  create: (data) => enhancedAPIService.post('/orders', data),
  update: (id, data) => enhancedAPIService.put(`/orders/${id}`, data),
  updateStatus: (id, status, notes = '') => enhancedAPIService.patch(`/orders/${id}/status`, { 
    status, 
    notes 
  }),
  cancel: (id, reason) => enhancedAPIService.post(`/orders/${id}/cancel`, { reason }),
  fulfill: (id, items) => enhancedAPIService.post(`/orders/${id}/fulfill`, { items }),
  getInvoice: (id) => enhancedAPIService.get(`/orders/${id}/invoice`),
  downloadInvoice: (id, format = 'pdf') => enhancedAPIService.download(
    `/orders/${id}/invoice/${format}`, 
    `invoice-${id}.${format}`
  ),
  getShipping: (id) => enhancedAPIService.get(`/orders/${id}/shipping`),
  updateShipping: (id, data) => enhancedAPIService.put(`/orders/${id}/shipping`, data),
  getPayments: (id) => enhancedAPIService.get(`/orders/${id}/payments`),
  addPayment: (id, data) => enhancedAPIService.post(`/orders/${id}/payments`, data),
  export: (params = {}, format = 'xlsx') => enhancedAPIService.download(
    `/orders/export?format=${format}`, 
    `orders.${format}`, 
    { params }
  )
};

// Enhanced Customers API
export const enhancedCustomersAPI = {
  getAll: (params = {}) => enhancedAPIService.get('/customers', { params }),
  getById: (id) => enhancedAPIService.get(`/customers/${id}`),
  create: (data) => enhancedAPIService.post('/customers', data),
  update: (id, data) => enhancedAPIService.put(`/customers/${id}`, data),
  delete: (id) => enhancedAPIService.delete(`/customers/${id}`),
  getOrders: (id, params = {}) => enhancedAPIService.get(`/customers/${id}/orders`, { params }),
  getPayments: (id, params = {}) => enhancedAPIService.get(`/customers/${id}/payments`, { params }),
  getStatistics: (id) => enhancedAPIService.get(`/customers/${id}/statistics`),
  search: (query) => enhancedAPIService.get('/customers/search', { params: { q: query } }),
  bulkUpdate: (data) => enhancedAPIService.post('/customers/bulk-update', data),
  export: (format = 'xlsx') => enhancedAPIService.download(
    `/customers/export?format=${format}`, 
    `customers.${format}`
  ),
  import: (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    return enhancedAPIService.upload('/customers/import', formData, onProgress);
  }
};

// Enhanced Reports API
export const enhancedReportsAPI = {
  getSales: (params = {}) => enhancedAPIService.get('/reports/sales', { params }),
  getInventory: (params = {}) => enhancedAPIService.get('/reports/inventory', { params }),
  getCustomers: (params = {}) => enhancedAPIService.get('/reports/customers', { params }),
  getFinancial: (params = {}) => enhancedAPIService.get('/reports/financial', { params }),
  getPerformance: (params = {}) => enhancedAPIService.get('/reports/performance', { params }),
  getAnalytics: (params = {}) => enhancedAPIService.get('/reports/analytics', { params }),
  
  // Export reports
  exportSales: (params = {}, format = 'xlsx') => enhancedAPIService.download(
    `/reports/sales/export?format=${format}`, 
    `sales-report.${format}`, 
    { params }
  ),
  exportInventory: (params = {}, format = 'xlsx') => enhancedAPIService.download(
    `/reports/inventory/export?format=${format}`, 
    `inventory-report.${format}`, 
    { params }
  ),
  exportCustomers: (params = {}, format = 'xlsx') => enhancedAPIService.download(
    `/reports/customers/export?format=${format}`, 
    `customers-report.${format}`, 
    { params }
  ),
  exportFinancial: (params = {}, format = 'xlsx') => enhancedAPIService.download(
    `/reports/financial/export?format=${format}`, 
    `financial-report.${format}`, 
    { params }
  ),
  
  // Dashboard data
  getDashboard: (period = 'month') => enhancedAPIService.get('/reports/dashboard', { 
    params: { period } 
  }),
  getKPIs: () => enhancedAPIService.get('/reports/kpis'),
  getAlerts: () => enhancedAPIService.get('/reports/alerts'),
  getActivities: (limit = 10) => enhancedAPIService.get('/reports/activities', { 
    params: { limit } 
  })
};

// Enhanced Settings API
export const enhancedSettingsAPI = {
  getAll: () => enhancedAPIService.get('/settings'),
  getByCategory: (category) => enhancedAPIService.get(`/settings/${category}`),
  update: (category, data) => enhancedAPIService.put(`/settings/${category}`, data),
  reset: (category) => enhancedAPIService.post(`/settings/${category}/reset`),
  export: () => enhancedAPIService.download('/settings/export', 'settings.json'),
  import: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return enhancedAPIService.upload('/settings/import', formData);
  },
  backup: () => enhancedAPIService.post('/settings/backup'),
  restore: (backupId) => enhancedAPIService.post(`/settings/restore/${backupId}`)
};

// Enhanced Notifications API
export const enhancedNotificationsAPI = {
  getAll: (params = {}) => enhancedAPIService.get('/notifications', { params }),
  getUnread: () => enhancedAPIService.get('/notifications/unread'),
  markAsRead: (id) => enhancedAPIService.patch(`/notifications/${id}/read`),
  markAllAsRead: () => enhancedAPIService.patch('/notifications/read-all'),
  delete: (id) => enhancedAPIService.delete(`/notifications/${id}`),
  deleteAll: () => enhancedAPIService.delete('/notifications'),
  getSettings: () => enhancedAPIService.get('/notifications/settings'),
  updateSettings: (data) => enhancedAPIService.put('/notifications/settings', data)
};

// Enhanced System API
export const enhancedSystemAPI = {
  getHealth: () => enhancedAPIService.get('/system/health'),
  getStatus: () => enhancedAPIService.get('/system/status'),
  getVersion: () => enhancedAPIService.get('/system/version'),
  getLogs: (params = {}) => enhancedAPIService.get('/system/logs', { params }),
  getMetrics: () => enhancedAPIService.get('/system/metrics'),
  backup: () => enhancedAPIService.post('/system/backup'),
  maintenance: (mode) => enhancedAPIService.post('/system/maintenance', { mode }),
  clearCache: () => enhancedAPIService.post('/system/cache/clear'),
  optimize: () => enhancedAPIService.post('/system/optimize')
};

export default enhancedAPIService;
