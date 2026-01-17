/**
 * API Client موحد للتواصل مع الواجهة الخلفية
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/services/apiClient.js
 */

class ApiClient {
  constructor() {
    const V = (typeof import.meta !== 'undefined' && import.meta.env) || {}
    this.baseURL = V.VITE_API_BASE || '';
  }

  /**
   * الحصول على التوكن من localStorage بشكل ديناميكي
   */
  getToken() {
    return localStorage.getItem('token');
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  /**
   * تحديث التوكن
   */
  setToken(token, refreshToken = null) {
    localStorage.setItem('token', token);
    
    if (refreshToken) {
      localStorage.setItem('refresh_token', refreshToken);
    }
  }

  /**
   * إزالة التوكن (تسجيل الخروج)
   */
  clearToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
  }

  /**
   * طلب HTTP أساسي
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // إضافة التوكن إذا كان متوفراً
    const token = this.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      
      // معالجة انتهاء صلاحية التوكن
      if (response.status === 401 && this.getRefreshToken()) {
        const newToken = await this.refreshAuthToken();
        if (newToken) {
          // إعادة المحاولة مع التوكن الجديد
          config.headers['Authorization'] = `Bearer ${newToken}`;
          const retryResponse = await fetch(url, config);
          return this.handleResponse(retryResponse);
        }
      }
      
      return this.handleResponse(response);
      
    } catch (error) {
      throw new Error(`خطأ في الاتصال: ${error.message}`);
    }
  }

  /**
   * معالجة الاستجابة
   */
  async handleResponse(response) {
    const contentType = response.headers.get('content-type');
    
    if (!response.ok) {
      let errorMessage = `خطأ HTTP: ${response.status}`;
      
      try {
        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json();
          errorMessage = errorData.error || errorData.message || errorMessage;
        } else {
          errorMessage = await response.text() || errorMessage;
        }
      } catch {
        // استخدام الرسالة الافتراضية إذا فشل تحليل الخطأ
      }
      
      throw new Error(errorMessage);
    }

    // إرجاع البيانات حسب نوع المحتوى
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    } else if (contentType && contentType.includes('text/')) {
      return response.text();
    } else {
      return response.blob();
    }
  }

  /**
   * تجديد التوكن
   */
  async refreshAuthToken() {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: this.getRefreshToken()
        })
      });

      if (response.ok) {
        const data = await response.json();
        this.setToken(data.access_token, data.refresh_token);
        return data.access_token;
      } else {
        // فشل تجديد التوكن - تسجيل خروج
        this.clearToken();
        window.location.href = '/login';
        return null;
      }
    } catch (error) {
      this.clearToken();
      window.location.href = '/login';
      return null;
    }
  }

  // ==================== CRUD Operations ====================

  /**
   * طلب GET
   */
  get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    return this.request(url, {
      method: 'GET',
    });
  }

  /**
   * طلب POST
   */
  post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * طلب PUT
   */
  put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * طلب PATCH
   */
  patch(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  /**
   * طلب DELETE
   */
  delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  // ==================== File Upload ====================

  /**
   * رفع ملف
   */
  uploadFile(endpoint, file, additionalData = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    // إضافة بيانات إضافية
    Object.keys(additionalData).forEach(key => {
      formData.append(key, additionalData[key]);
    });

    return this.request(endpoint, {
      method: 'POST',
      body: formData,
      headers: {
        // لا نضع Content-Type للـ FormData - المتصفح يضعه تلقائياً
      },
    });
  }

  /**
   * تحميل ملف
   */
  async downloadFile(endpoint, filename = null) {
    const response = await this.request(endpoint, {
      method: 'GET',
      headers: {
        'Accept': '*/*',
      },
    });

    // إنشاء رابط تحميل
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || 'download';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  // ==================== Batch Operations ====================

  /**
   * طلبات متعددة متوازية
   */
  async batchRequests(requests) {
    const promises = requests.map(req => 
      this.request(req.endpoint, req.options)
    );
    
    const results = await Promise.allSettled(promises);
    
    return results.map((result, index) => ({
      request: requests[index],
      success: result.status === 'fulfilled',
      data: result.status === 'fulfilled' ? result.value : null,
      error: result.status === 'rejected' ? result.reason : null,
    }));
  }

  // ==================== Health Check ====================

  /**
   * فحص حالة الخادم
   */
  async healthCheck() {
    try {
      const response = await this.get('/api/health');
      return {
        status: 'healthy',
        data: response,
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
      };
    }
  }

  // ==================== Utility Methods ====================

  /**
   * إنشاء URL كامل
   */
  getFullUrl(endpoint) {
    return `${this.baseURL}${endpoint}`;
  }

  /**
   * فحص حالة الاتصال
   */
  isAuthenticated() {
    return !!this.getToken();
  }

  /**
   * الحصول على معلومات المستخدم من التوكن
   */
  getUserFromToken() {
    const token = this.getToken();
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload;
    } catch (error) {
      return null;
    }
  }
}

// إنشاء instance واحد للاستخدام في التطبيق
const apiClient = new ApiClient();

export default apiClient;

