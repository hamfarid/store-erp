/**
 * خدمة Axios المحسنة - ربط APIs
 * Enhanced Axios Service - API Integration
 */

import axios from 'axios'
import { useAuthStore, useSystemStore } from '../store/index.js'

// إعداد Axios الأساسي
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Interceptor للطلبات
apiClient.interceptors.request.use(
  (config) => {
    // إضافة token المصادقة
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // إضافة loading
    const systemStore = useSystemStore()
    systemStore.setLoading(true)
    
    return config
  },
  (error) => {
    const systemStore = useSystemStore()
    systemStore.setLoading(false)
    return Promise.reject(error)
  }
)

// Interceptor للاستجابات
apiClient.interceptors.response.use(
  (response) => {
    const systemStore = useSystemStore()
    systemStore.setLoading(false)
    return response
  },
  (error) => {
    const systemStore = useSystemStore()
    systemStore.setLoading(false)
    
    // معالجة أخطاء المصادقة
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    
    // إضافة إشعار خطأ
    systemStore.addNotification({
      type: 'error',
      title: 'خطأ في الاتصال',
      message: error.response?.data?.message || 'حدث خطأ غير متوقع'
    })
    
    return Promise.reject(error)
  }
)

// خدمات API المختلفة

// خدمة المصادقة
export const authAPI = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  logout: () => apiClient.post('/auth/logout'),
  register: (userData) => apiClient.post('/auth/register', userData),
  getUser: () => apiClient.get('/auth/user'),
  refreshToken: () => apiClient.post('/auth/refresh'),
  changePassword: (data) => apiClient.put('/auth/change-password', data)
}

// خدمة لوحة التحكم
export const dashboardAPI = {
  getStats: () => apiClient.get('/dashboard/stats'),
  getChartData: (type) => apiClient.get(`/dashboard/charts/${type}`),
  getRecentActivities: () => apiClient.get('/dashboard/activities'),
  getSystemHealth: () => apiClient.get('/dashboard/health')
}

// خدمة الذكاء الاصطناعي
export const aiAPI = {
  // إدارة النماذج
  getModels: () => apiClient.get('/ai-management/models'),
  createModel: (modelData) => apiClient.post('/ai-management/models', modelData),
  updateModel: (id, modelData) => apiClient.put(`/ai-management/models/${id}`, modelData),
  deleteModel: (id) => apiClient.delete(`/ai-management/models/${id}`),
  
  // المساعد الذكي
  sendMessage: (message, modelId) => apiClient.post('/ai-agent/chat', { message, model_id: modelId }),
  getChatHistory: () => apiClient.get('/ai-agent/history'),
  clearChatHistory: () => apiClient.delete('/ai-agent/history'),
  
  // تقارير الاستخدام
  getUsageReports: (params) => apiClient.get('/ai-agent/reports', { params }),
  getUserQuestions: (userId) => apiClient.get(`/ai-agent/reports/user/${userId}`),
  getQuestionsAnalysis: () => apiClient.get('/ai-agent/reports/analysis'),
  exportUsageReport: (format) => apiClient.get(`/ai-agent/reports/export?format=${format}`, {
    responseType: 'blob'
  })
}

// خدمة التشخيص
export const diagnosisAPI = {
  // رفع الصور
  uploadImage: (file) => {
    const formData = new FormData()
    formData.append('image', file)
    return apiClient.post('/diagnosis/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // التشخيص
  analyzeImage: (imageId, options) => apiClient.post('/diagnosis/analyze', { image_id: imageId, ...options }),
  getDiagnosisHistory: () => apiClient.get('/diagnosis/history'),
  getDiagnosisResult: (id) => apiClient.get(`/diagnosis/result/${id}`),
  
  // تحسين الصور
  enhanceImage: (imageId, enhancement) => apiClient.post('/image-enhancement/enhance', {
    image_id: imageId,
    enhancement_type: enhancement
  }),
  getEnhancementOptions: () => apiClient.get('/image-enhancement/options'),
  
  // كشف YOLO
  detectObjects: (imageId, model) => apiClient.post('/yolo-detection/detect', {
    image_id: imageId,
    model: model
  }),
  getDetectionModels: () => apiClient.get('/yolo-detection/models'),
  
  // تهجين النباتات
  simulateHybridization: (parent1, parent2, options) => apiClient.post('/plant-hybridization/simulate', {
    parent1,
    parent2,
    ...options
  }),
  getPlantVarieties: () => apiClient.get('/plant-hybridization/varieties'),
  getHybridizationHistory: () => apiClient.get('/plant-hybridization/history')
}

// خدمة إدارة البيانات
export const dataAPI = {
  // سجل الأنشطة
  getActivityLog: (params) => apiClient.get('/activity-log', { params }),
  exportActivityLog: (format) => apiClient.get(`/activity-log/export?format=${format}`, {
    responseType: 'blob'
  }),
  
  // الاستيراد والتصدير
  importData: (file, type) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type)
    return apiClient.post('/data/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  exportData: (type, format) => apiClient.get(`/data/export?type=${type}&format=${format}`, {
    responseType: 'blob'
  }),
  
  // التحقق من البيانات
  validateData: (type) => apiClient.post('/data/validate', { type }),
  getValidationReport: () => apiClient.get('/data/validation-report'),
  fixDataIssues: (issues) => apiClient.post('/data/fix-issues', { issues })
}

// خدمة Docker
export const dockerAPI = {
  // إدارة الحاويات
  getContainers: () => apiClient.get('/docker/containers'),
  startContainer: (id) => apiClient.post(`/docker/containers/${id}/start`),
  stopContainer: (id) => apiClient.post(`/docker/containers/${id}/stop`),
  restartContainer: (id) => apiClient.post(`/docker/containers/${id}/restart`),
  removeContainer: (id) => apiClient.delete(`/docker/containers/${id}`),
  
  // مراقبة الحاويات
  getContainerStats: (id) => apiClient.get(`/docker/containers/${id}/stats`),
  getContainerLogs: (id) => apiClient.get(`/docker/containers/${id}/logs`),
  
  // إدارة الصور
  getImages: () => apiClient.get('/docker/images'),
  pullImage: (name) => apiClient.post('/docker/images/pull', { name }),
  removeImage: (id) => apiClient.delete(`/docker/images/${id}`)
}

// خدمة الإدارة (للمديرين)
export const adminAPI = {
  // إعدادات النظام
  getSettings: () => apiClient.get('/admin/settings'),
  updateSettings: (settings) => apiClient.put('/admin/settings', settings),
  
  // إدارة المستخدمين
  getUsers: (params) => apiClient.get('/admin/users', { params }),
  createUser: (userData) => apiClient.post('/admin/users', userData),
  updateUser: (id, userData) => apiClient.put(`/admin/users/${id}`, userData),
  deleteUser: (id) => apiClient.delete(`/admin/users/${id}`),
  
  // مراقبة النظام
  getSystemMetrics: () => apiClient.get('/admin/monitoring/metrics'),
  getPerformanceData: () => apiClient.get('/admin/monitoring/performance'),
  getErrorLogs: () => apiClient.get('/admin/monitoring/errors'),
  
  // النسخ الاحتياطي
  createBackup: () => apiClient.post('/admin/backup/create'),
  getBackups: () => apiClient.get('/admin/backup/list'),
  restoreBackup: (id) => apiClient.post(`/admin/backup/restore/${id}`),
  deleteBackup: (id) => apiClient.delete(`/admin/backup/${id}`),
  
  // إدارة الأمان
  getSecuritySettings: () => apiClient.get('/admin/security/settings'),
  updateSecuritySettings: (settings) => apiClient.put('/admin/security/settings', settings),
  getSecurityLogs: () => apiClient.get('/admin/security/logs'),
  getLoginAttempts: () => apiClient.get('/admin/security/login-attempts')
}

// خدمة فحص الصحة
export const healthAPI = {
  checkHealth: () => apiClient.get('/health'),
  checkServiceHealth: (service) => apiClient.get(`/health/${service}`),
  getSystemStatus: () => apiClient.get('/health/system'),
  getDatabaseStatus: () => apiClient.get('/health/database')
}

// تصدير العميل الرئيسي
export default apiClient

