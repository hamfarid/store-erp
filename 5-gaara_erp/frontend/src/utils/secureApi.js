/**
 * نظام API آمن للواجهة الأمامية
 * ملف: secureApi.js
 */

import axios from 'axios'
import encryption from './encryption.js'

class SecureApiClient {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
    this.timeout = 30000 // 30 ثانية
    this.retryAttempts = 3
    
    // إنشاء مثيل axios
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
    
    // إعداد interceptors
    this.setupRequestInterceptor()
    this.setupResponseInterceptor()
  }

  /**
   * إعداد معترض الطلبات
   */
  setupRequestInterceptor() {
    this.client.interceptors.request.use(
      (config) => {
        // إضافة مفتاح API
        const apiKey = localStorage.getItem('api_key')
        if (apiKey) {
          config.headers['X-API-Key'] = apiKey
        }

        // إضافة رؤوس الأمان
        config.headers['X-Requested-With'] = 'XMLHttpRequest'
        config.headers['X-Client-Version'] = '1.0.0'
        
        // إضافة CSRF token إذا كان متاحاً
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
        if (csrfToken) {
          config.headers['X-CSRF-Token'] = csrfToken
        }

        // تشفير البيانات الحساسة
        if (config.data && this.shouldEncryptRequest(config.url)) {
          const encryptedData = encryption.encryptApiRequest(config.data)
          if (encryptedData) {
            config.data = encryptedData
          }
        }

        // إضافة توقيع الطلب
        if (this.shouldSignRequest(config.url)) {
          this.addRequestSignature(config)
        }

        console.debug(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )
  }

  /**
   * إعداد معترض الاستجابات
   */
  setupResponseInterceptor() {
    this.client.interceptors.response.use(
      (response) => {
        // فك تشفير البيانات إذا كانت مشفرة
        if (response.data && response.data.encrypted_data) {
          const decryptedData = encryption.decryptApiResponse(response.data)
          if (decryptedData) {
            response.data = decryptedData
          }
        }

        return response
      },
      async (error) => {
        const originalRequest = error.config

        // إعادة المحاولة في حالة فشل الشبكة
        if (error.code === 'NETWORK_ERROR' && !originalRequest._retry) {
          originalRequest._retry = true
          
          if (originalRequest._retryCount < this.retryAttempts) {
            originalRequest._retryCount = (originalRequest._retryCount || 0) + 1
            
            // انتظار قبل إعادة المحاولة
            await new Promise(resolve => setTimeout(resolve, 1000 * originalRequest._retryCount))
            
            return this.client(originalRequest)
          }
        }

        // معالجة أخطاء المصادقة
        if (error.response?.status === 401) {
          this.handleAuthenticationError()
        }

        // معالجة أخطاء تجاوز الحد المسموح
        if (error.response?.status === 429) {
          this.handleRateLimitError()
        }

        return Promise.reject(error)
      }
    )
  }

  /**
   * فحص إذا كان يجب تشفير الطلب
   */
  shouldEncryptRequest(url) {
    const encryptedEndpoints = [
      '/api/auth/login',
      '/api/auth/register',
      '/api/users',
      '/api/customers',
      '/api/suppliers',
      '/api/accounting'
    ]
    
    return encryptedEndpoints.some(endpoint => url.includes(endpoint))
  }

  /**
   * فحص إذا كان يجب توقيع الطلب
   */
  shouldSignRequest(url) {
    const signedEndpoints = [
      '/api/auth',
      '/api/accounting',
      '/api/admin'
    ]
    
    return signedEndpoints.some(endpoint => url.includes(endpoint))
  }

  /**
   * إضافة توقيع الطلب
   */
  addRequestSignature(config) {
    try {
      const timestamp = Date.now().toString()
      const method = config.method?.toUpperCase() || 'GET'
      const url = config.url || ''
      const body = config.data ? JSON.stringify(config.data) : ''
      
      const signature = encryption.createRequestSignature(method, url, body, timestamp)
      
      if (signature) {
        config.headers['X-Signature'] = signature
        config.headers['X-Timestamp'] = timestamp
      }
    } catch (error) {
      }
  }

  /**
   * معالجة خطأ المصادقة
   */
  handleAuthenticationError() {
    // مسح بيانات المصادقة
    localStorage.removeItem('api_key')
    localStorage.removeItem('api_secret')
    localStorage.removeItem('user_token')
    
    // مسح البيانات الحساسة
    encryption.clearSensitiveData()
    
    // إعادة توجيه لصفحة تسجيل الدخول
    if (window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
  }

  /**
   * معالجة خطأ تجاوز الحد المسموح
   */
  handleRateLimitError() {
    // عرض رسالة للمستخدم
    if (window.showNotification) {
      window.showNotification('تم تجاوز الحد المسموح من الطلبات. يرجى المحاولة لاحقاً.', 'warning')
    }
  }

  /**
   * طلب GET آمن
   */
  async get(url, config = {}) {
    try {
      const response = await this.client.get(url, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * طلب POST آمن
   */
  async post(url, data = {}, config = {}) {
    try {
      const response = await this.client.post(url, data, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * طلب PUT آمن
   */
  async put(url, data = {}, config = {}) {
    try {
      const response = await this.client.put(url, data, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * طلب DELETE آمن
   */
  async delete(url, config = {}) {
    try {
      const response = await this.client.delete(url, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * رفع ملف آمن
   */
  async uploadFile(url, file, onProgress = null) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            )
            onProgress(percentCompleted)
          }
        }
      }
      
      const response = await this.client.post(url, formData, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * تحميل ملف آمن
   */
  async downloadFile(url, filename) {
    try {
      const response = await this.client.get(url, {
        responseType: 'blob'
      })
      
      // إنشاء رابط التحميل
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      window.URL.revokeObjectURL(downloadUrl)
      
      return true
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * معالجة الأخطاء
   */
  handleError(error) {
    const errorInfo = {
      message: 'حدث خطأ غير متوقع',
      status: null,
      code: null,
      details: null
    }

    if (error.response) {
      // خطأ من الخادم
      errorInfo.status = error.response.status
      errorInfo.message = error.response.data?.message || `خطأ ${error.response.status}`
      errorInfo.details = error.response.data
    } else if (error.request) {
      // خطأ في الشبكة
      errorInfo.message = 'خطأ في الاتصال بالخادم'
      errorInfo.code = 'NETWORK_ERROR'
    } else {
      // خطأ في الإعداد
      errorInfo.message = error.message || 'خطأ في إعداد الطلب'
    }

    return errorInfo
  }

  /**
   * فحص حالة الاتصال
   */
  async checkConnection() {
    try {
      const response = await this.get('/api/health')
      return response.status === 'healthy'
    } catch (error) {
      return false
    }
  }

  /**
   * تعيين مفاتيح API
   */
  setApiCredentials(apiKey, apiSecret) {
    localStorage.setItem('api_key', apiKey)
    localStorage.setItem('api_secret', apiSecret)
    
    // تحديث رؤوس الطلبات
    this.client.defaults.headers['X-API-Key'] = apiKey
  }

  /**
   * مسح مفاتيح API
   */
  clearApiCredentials() {
    localStorage.removeItem('api_key')
    localStorage.removeItem('api_secret')
    
    delete this.client.defaults.headers['X-API-Key']
  }
}

// إنشاء مثيل عام
const secureApi = new SecureApiClient()

export default secureApi
export { SecureApiClient }
