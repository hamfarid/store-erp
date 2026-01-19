# /home/ubuntu/image_search_integration/auto_learning/services/ApiService.js

/**
 * خدمة API الأساسية للتعامل مع طلبات HTTP
 * 
 * هذه الخدمة توفر الوظائف الأساسية للتعامل مع طلبات HTTP وإدارة الأخطاء والتوثيق
 * وتستخدم كأساس لجميع خدمات API المتخصصة في النظام.
 */

import axios from 'axios';

// تكوين الإعدادات الافتراضية لـ axios
const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '/api/v1',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// اعتراض الطلبات لإضافة رمز التوثيق
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// اعتراض الاستجابات للتعامل مع الأخطاء الشائعة
apiClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // التعامل مع أخطاء التوثيق
    if (error.response && error.response.status === 401) {
      // تسجيل الخروج وإعادة التوجيه إلى صفحة تسجيل الدخول
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    
    // التعامل مع أخطاء الصلاحيات
    if (error.response && error.response.status === 403) {
      console.error('Access forbidden: Insufficient permissions');
      // يمكن إضافة إجراءات إضافية هنا
    }
    
    return Promise.reject(error);
  }
);

export default {
  /**
   * إرسال طلب GET
   * @param {string} url - مسار URL النسبي
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  get(url, params = {}) {
    return apiClient.get(url, { params });
  },

  /**
   * إرسال طلب POST
   * @param {string} url - مسار URL النسبي
   * @param {Object} data - البيانات المرسلة
   * @returns {Promise} وعد بالاستجابة
   */
  post(url, data = {}) {
    return apiClient.post(url, data);
  },

  /**
   * إرسال طلب PUT
   * @param {string} url - مسار URL النسبي
   * @param {Object} data - البيانات المرسلة
   * @returns {Promise} وعد بالاستجابة
   */
  put(url, data = {}) {
    return apiClient.put(url, data);
  },

  /**
   * إرسال طلب PATCH
   * @param {string} url - مسار URL النسبي
   * @param {Object} data - البيانات المرسلة
   * @returns {Promise} وعد بالاستجابة
   */
  patch(url, data = {}) {
    return apiClient.patch(url, data);
  },

  /**
   * إرسال طلب DELETE
   * @param {string} url - مسار URL النسبي
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  delete(url, params = {}) {
    return apiClient.delete(url, { params });
  },

  /**
   * تحميل ملف
   * @param {string} url - مسار URL النسبي
   * @param {FormData} formData - بيانات النموذج مع الملف
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  uploadFile(url, formData, progressCallback = null) {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    };
    
    if (progressCallback) {
      config.onUploadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        progressCallback(percentCompleted);
      };
    }
    
    return apiClient.post(url, formData, config);
  },

  /**
   * تنزيل ملف
   * @param {string} url - مسار URL النسبي
   * @param {Object} params - معلمات الاستعلام
   * @param {string} filename - اسم الملف للتنزيل
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  downloadFile(url, params = {}, filename = null, progressCallback = null) {
    const config = {
      params,
      responseType: 'blob',
    };
    
    if (progressCallback) {
      config.onDownloadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        progressCallback(percentCompleted);
      };
    }
    
    return apiClient.get(url, config).then(response => {
      // إنشاء رابط تنزيل وتنزيل الملف
      const blob = new Blob([response.data]);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename || this.getFilenameFromResponse(response);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
      return response;
    });
  },

  /**
   * استخراج اسم الملف من رأس الاستجابة
   * @param {Object} response - كائن الاستجابة
   * @returns {string} اسم الملف
   */
  getFilenameFromResponse(response) {
    const contentDisposition = response.headers['content-disposition'];
    if (!contentDisposition) return 'downloaded_file';
    
    const filenameMatch = contentDisposition.match(/filename="(.+)"/);
    return filenameMatch ? filenameMatch[1] : 'downloaded_file';
  }
};
