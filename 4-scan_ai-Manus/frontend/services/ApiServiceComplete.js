// ملف: /home/ubuntu/gaara_ai_FINAL_INTEGRATED_SYSTEM_20250708_040611/gaara_ai_integrated/frontend/src/services/ApiServiceComplete.js
// خدمة API كاملة ومتكاملة لنظام Gaara AI
// الإصدار: 2.0.0
// تم الإنشاء: 2025-01-08
// المطور: Gaara Group & Manus AI

import axios from 'axios';
import toast from 'react-hot-toast';

// إعداد الـ Base URL
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:4001/api';

// إنشاء instance من axios
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000, // 30 ثانية
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Interceptor للطلبات - إضافة التوكن
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // إضافة timestamp لمنع الكاش
    config.params = {
      ...config.params,
      _t: Date.now()
    };
    
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Interceptor للاستجابات - معالجة الأخطاء
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', error);
    
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // انتهاء صلاحية التوكن
          localStorage.removeItem('access_token');
          window.location.href = '/login';
          toast.error('انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى');
          break;
        case 403:
          toast.error('ليس لديك صلاحية للوصول لهذا المورد');
          break;
        case 404:
          toast.error('المورد المطلوب غير موجود');
          break;
        case 422:
          // أخطاء التحقق
          if (data.errors) {
            Object.values(data.errors).forEach(errorArray => {
              errorArray.forEach(errorMsg => toast.error(errorMsg));
            });
          } else {
            toast.error(data.message || 'بيانات غير صحيحة');
          }
          break;
        case 500:
          toast.error('خطأ في الخادم، يرجى المحاولة لاحقاً');
          break;
        default:
          toast.error(data.message || 'حدث خطأ غير متوقع');
      }
    } else if (error.request) {
      toast.error('لا يمكن الاتصال بالخادم، تحقق من اتصال الإنترنت');
    } else {
      toast.error('حدث خطأ في الطلب');
    }
    
    return Promise.reject(error);
  }
);

// فئة خدمة API الرئيسية
class ApiServiceComplete {
  // ===== طرق HTTP الأساسية =====
  
  async get(url, params = {}) {
    try {
      const response = await apiClient.get(url, { params });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  async post(url, data = {}) {
    try {
      const response = await apiClient.post(url, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  async put(url, data = {}) {
    try {
      const response = await apiClient.put(url, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  async patch(url, data = {}) {
    try {
      const response = await apiClient.patch(url, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  async delete(url) {
    try {
      const response = await apiClient.delete(url);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  // رفع الملفات
  async upload(url, formData, onProgress = null) {
    try {
      const response = await apiClient.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        },
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  // ===== خدمات المصادقة =====
  
  async login(credentials) {
    const response = await this.post('/auth/login', credentials);
    if (response.success && response.access_token) {
      this.setAuthToken(response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  }
  
  async register(userData) {
    return await this.post('/auth/register', userData);
  }
  
  async logout() {
    try {
      await this.post('/auth/logout');
    } catch (error) {
      console.warn('Logout API call failed:', error);
    } finally {
      this.clearAuth();
    }
  }
  
  async getProfile() {
    return await this.get('/auth/profile');
  }
  
  async updateProfile(profileData) {
    return await this.put('/auth/profile', profileData);
  }
  
  async changePassword(passwordData) {
    return await this.put('/auth/change-password', passwordData);
  }
  
  async forgotPassword(email) {
    return await this.post('/auth/forgot-password', { email });
  }
  
  async resetPassword(resetData) {
    return await this.post('/auth/reset-password', resetData);
  }
  
  // ===== خدمات المزارع =====
  
  async getFarms(params = {}) {
    return await this.get('/farms', params);
  }
  
  async getFarm(farmId) {
    return await this.get(`/farms/${farmId}`);
  }
  
  async createFarm(farmData) {
    return await this.post('/farms', farmData);
  }
  
  async updateFarm(farmId, farmData) {
    return await this.put(`/farms/${farmId}`, farmData);
  }
  
  async deleteFarm(farmId) {
    return await this.delete(`/farms/${farmId}`);
  }
  
  async getFarmStatistics(farmId) {
    return await this.get(`/farms/${farmId}/statistics`);
  }
  
  async getFarmPlants(farmId, params = {}) {
    return await this.get(`/farms/${farmId}/plants`, params);
  }
  
  async getFarmSensors(farmId, params = {}) {
    return await this.get(`/farms/${farmId}/sensors`, params);
  }
  
  // ===== خدمات النباتات =====
  
  async getPlants(params = {}) {
    return await this.get('/plants', params);
  }
  
  async getPlant(plantId) {
    return await this.get(`/plants/${plantId}`);
  }
  
  async createPlant(plantData) {
    return await this.post('/plants', plantData);
  }
  
  async updatePlant(plantId, plantData) {
    return await this.put(`/plants/${plantId}`, plantData);
  }
  
  async deletePlant(plantId) {
    return await this.delete(`/plants/${plantId}`);
  }
  
  async getPlantHistory(plantId) {
    return await this.get(`/plants/${plantId}/history`);
  }
  
  async getPlantDiagnoses(plantId, params = {}) {
    return await this.get(`/plants/${plantId}/diagnoses`, params);
  }
  
  // ===== خدمات التشخيص =====
  
  async getDiagnoses(params = {}) {
    return await this.get('/diagnosis', params);
  }
  
  async getDiagnosis(diagnosisId) {
    return await this.get(`/diagnosis/${diagnosisId}`);
  }
  
  async createDiagnosis(diagnosisData) {
    return await this.upload('/diagnosis', diagnosisData);
  }
  
  async updateDiagnosis(diagnosisId, diagnosisData) {
    return await this.put(`/diagnosis/${diagnosisId}`, diagnosisData);
  }
  
  async deleteDiagnosis(diagnosisId) {
    return await this.delete(`/diagnosis/${diagnosisId}`);
  }
  
  async getDiagnosisImage(diagnosisId) {
    return await this.get(`/diagnosis/${diagnosisId}/image`);
  }
  
  async rerunDiagnosis(diagnosisId) {
    return await this.post(`/diagnosis/${diagnosisId}/rerun`);
  }
  
  // ===== خدمات الأمراض =====
  
  async getDiseases(params = {}) {
    return await this.get('/diseases', params);
  }
  
  async getDisease(diseaseId) {
    return await this.get(`/diseases/${diseaseId}`);
  }
  
  async createDisease(diseaseData) {
    return await this.post('/diseases', diseaseData);
  }
  
  async updateDisease(diseaseId, diseaseData) {
    return await this.put(`/diseases/${diseaseId}`, diseaseData);
  }
  
  async deleteDisease(diseaseId) {
    return await this.delete(`/diseases/${diseaseId}`);
  }
  
  async getDiseaseSymptoms(diseaseId) {
    return await this.get(`/diseases/${diseaseId}/symptoms`);
  }
  
  async getDiseaseTreatments(diseaseId) {
    return await this.get(`/diseases/${diseaseId}/treatments`);
  }
  
  // ===== خدمات المحاصيل =====
  
  async getCrops(params = {}) {
    return await this.get('/crops', params);
  }
  
  async getCrop(cropId) {
    return await this.get(`/crops/${cropId}`);
  }
  
  async createCrop(cropData) {
    return await this.post('/crops', cropData);
  }
  
  async updateCrop(cropId, cropData) {
    return await this.put(`/crops/${cropId}`, cropData);
  }
  
  async deleteCrop(cropId) {
    return await this.delete(`/crops/${cropId}`);
  }
  
  async getCropVarieties(cropId) {
    return await this.get(`/crops/${cropId}/varieties`);
  }
  
  // ===== خدمات أجهزة الاستشعار =====
  
  async getSensors(params = {}) {
    return await this.get('/sensors', params);
  }
  
  async getSensor(sensorId) {
    return await this.get(`/sensors/${sensorId}`);
  }
  
  async createSensor(sensorData) {
    return await this.post('/sensors', sensorData);
  }
  
  async updateSensor(sensorId, sensorData) {
    return await this.put(`/sensors/${sensorId}`, sensorData);
  }
  
  async deleteSensor(sensorId) {
    return await this.delete(`/sensors/${sensorId}`);
  }
  
  async getSensorReadings(sensorId, params = {}) {
    return await this.get(`/sensors/${sensorId}/readings`, params);
  }
  
  async addSensorReading(sensorId, readingData) {
    return await this.post(`/sensors/${sensorId}/readings`, readingData);
  }
  
  // ===== خدمات التقارير =====
  
  async getReports(params = {}) {
    return await this.get('/reports', params);
  }
  
  async getFarmsReport(params = {}) {
    return await this.get('/reports/farms', params);
  }
  
  async getPlantsReport(params = {}) {
    return await this.get('/reports/plants', params);
  }
  
  async getDiagnosisReport(params = {}) {
    return await this.get('/reports/diagnosis', params);
  }
  
  async getProductivityReport(params = {}) {
    return await this.get('/reports/productivity', params);
  }
  
  async generateCustomReport(reportConfig) {
    return await this.post('/reports/custom', reportConfig);
  }
  
  async exportReport(reportId, format = 'pdf') {
    return await this.get(`/reports/${reportId}/export?format=${format}`);
  }
  
  // ===== خدمات التحليلات =====
  
  async getAnalytics(params = {}) {
    return await this.get('/analytics', params);
  }
  
  async getDashboardAnalytics() {
    return await this.get('/analytics/dashboard');
  }
  
  async getFarmAnalytics(farmId, params = {}) {
    return await this.get(`/analytics/farms/${farmId}`, params);
  }
  
  async getPlantAnalytics(plantId, params = {}) {
    return await this.get(`/analytics/plants/${plantId}`, params);
  }
  
  async getDiseaseAnalytics(params = {}) {
    return await this.get('/analytics/diseases', params);
  }
  
  async getProductivityAnalytics(params = {}) {
    return await this.get('/analytics/productivity', params);
  }
  
  // ===== خدمات الإحصائيات =====
  
  async getStatistics() {
    return await this.get('/statistics');
  }
  
  async getDashboardStatistics() {
    return await this.get('/statistics/dashboard');
  }
  
  async getFarmStatistics(farmId) {
    return await this.get(`/statistics/farms/${farmId}`);
  }
  
  async getUserStatistics() {
    return await this.get('/statistics/user');
  }
  
  async getSystemStatistics() {
    return await this.get('/statistics/system');
  }
  
  // ===== خدمات إدارة المستخدمين =====
  
  async getUsers(params = {}) {
    return await this.get('/admin/users', params);
  }
  
  async getUser(userId) {
    return await this.get(`/admin/users/${userId}`);
  }
  
  async createUser(userData) {
    return await this.post('/admin/users', userData);
  }
  
  async updateUser(userId, userData) {
    return await this.put(`/admin/users/${userId}`, userData);
  }
  
  async deleteUser(userId) {
    return await this.delete(`/admin/users/${userId}`);
  }
  
  async activateUser(userId) {
    return await this.post(`/admin/users/${userId}/activate`);
  }
  
  async deactivateUser(userId) {
    return await this.post(`/admin/users/${userId}/deactivate`);
  }
  
  async resetUserPassword(userId) {
    return await this.post(`/admin/users/${userId}/reset-password`);
  }
  
  // ===== خدمات الصلاحيات =====
  
  async getPermissions() {
    return await this.get('/admin/permissions');
  }
  
  async getRoles() {
    return await this.get('/admin/roles');
  }
  
  async createRole(roleData) {
    return await this.post('/admin/roles', roleData);
  }
  
  async updateRole(roleId, roleData) {
    return await this.put(`/admin/roles/${roleId}`, roleData);
  }
  
  async deleteRole(roleId) {
    return await this.delete(`/admin/roles/${roleId}`);
  }
  
  async getUserPermissions(userId) {
    return await this.get(`/admin/users/${userId}/permissions`);
  }
  
  async updateUserPermissions(userId, permissions) {
    return await this.put(`/admin/users/${userId}/permissions`, { permissions });
  }
  
  // ===== خدمات الشركات =====
  
  async getCompanies(params = {}) {
    return await this.get('/admin/companies', params);
  }
  
  async getCompany(companyId) {
    return await this.get(`/admin/companies/${companyId}`);
  }
  
  async createCompany(companyData) {
    return await this.post('/admin/companies', companyData);
  }
  
  async updateCompany(companyId, companyData) {
    return await this.put(`/admin/companies/${companyId}`, companyData);
  }
  
  async deleteCompany(companyId) {
    return await this.delete(`/admin/companies/${companyId}`);
  }
  
  // ===== خدمات الإعدادات =====
  
  async getSettings() {
    return await this.get('/settings');
  }
  
  async updateSettings(settings) {
    return await this.put('/settings', settings);
  }
  
  async getSystemSettings() {
    return await this.get('/admin/settings');
  }
  
  async updateSystemSettings(settings) {
    return await this.put('/admin/settings', settings);
  }
  
  async getNotificationSettings() {
    return await this.get('/settings/notifications');
  }
  
  async updateNotificationSettings(settings) {
    return await this.put('/settings/notifications', settings);
  }
  
  // ===== خدمات الإشعارات =====
  
  async getNotifications(params = {}) {
    return await this.get('/notifications', params);
  }
  
  async markNotificationAsRead(notificationId) {
    return await this.put(`/notifications/${notificationId}/read`);
  }
  
  async markAllNotificationsAsRead() {
    return await this.put('/notifications/read-all');
  }
  
  async deleteNotification(notificationId) {
    return await this.delete(`/notifications/${notificationId}`);
  }
  
  async getUnreadNotificationsCount() {
    return await this.get('/notifications/unread-count');
  }
  
  // ===== خدمات البحث =====
  
  async search(query, filters = {}) {
    return await this.get('/search', { q: query, ...filters });
  }
  
  async searchFarms(query, params = {}) {
    return await this.get('/search/farms', { q: query, ...params });
  }
  
  async searchPlants(query, params = {}) {
    return await this.get('/search/plants', { q: query, ...params });
  }
  
  async searchDiseases(query, params = {}) {
    return await this.get('/search/diseases', { q: query, ...params });
  }
  
  async searchUsers(query, params = {}) {
    return await this.get('/search/users', { q: query, ...params });
  }
  
  // ===== خدمات النسخ الاحتياطي =====
  
  async getBackups() {
    return await this.get('/admin/backups');
  }
  
  async createBackup(backupData) {
    return await this.post('/admin/backups', backupData);
  }
  
  async restoreBackup(backupId) {
    return await this.post(`/admin/backups/${backupId}/restore`);
  }
  
  async deleteBackup(backupId) {
    return await this.delete(`/admin/backups/${backupId}`);
  }
  
  async downloadBackup(backupId) {
    return await this.get(`/admin/backups/${backupId}/download`);
  }
  
  // ===== خدمات السجلات =====
  
  async getLogs(params = {}) {
    return await this.get('/admin/logs', params);
  }
  
  async getActivityLogs(params = {}) {
    return await this.get('/admin/logs/activity', params);
  }
  
  async getErrorLogs(params = {}) {
    return await this.get('/admin/logs/errors', params);
  }
  
  async clearLogs(logType = 'all') {
    return await this.delete(`/admin/logs?type=${logType}`);
  }
  
  // ===== خدمات مساعدة =====
  
  setAuthToken(token) {
    localStorage.setItem('access_token', token);
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
  
  clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    delete apiClient.defaults.headers.common['Authorization'];
  }
  
  getAuthToken() {
    return localStorage.getItem('access_token');
  }
  
  isAuthenticated() {
    return !!this.getAuthToken();
  }
  
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
  
  handleError(error) {
    if (error.response?.data) {
      return error.response.data;
    }
    return {
      success: false,
      message: error.message || 'حدث خطأ غير متوقع'
    };
  }
  
  // تحديث URL الأساسي
  setBaseURL(url) {
    apiClient.defaults.baseURL = url;
  }
  
  // الحصول على URL الأساسي
  getBaseURL() {
    return apiClient.defaults.baseURL;
  }
  
  // إعداد timeout
  setTimeout(timeout) {
    apiClient.defaults.timeout = timeout;
  }
  
  // إضافة header مخصص
  setHeader(name, value) {
    apiClient.defaults.headers.common[name] = value;
  }
  
  // إزالة header
  removeHeader(name) {
    delete apiClient.defaults.headers.common[name];
  }
  
  // تحقق من حالة الخادم
  async healthCheck() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      return { status: 'error', message: 'الخادم غير متاح' };
    }
  }
  
  // إعادة تجربة الطلب
  async retry(requestFn, maxRetries = 3, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await requestFn();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
      }
    }
  }
}

// إنشاء instance واحد من الخدمة
const apiService = new ApiServiceComplete();

// تصدير الخدمة والـ client
export default apiService;
export { apiClient };

// تصدير الطرق المهمة للاستخدام المباشر
export const {
  // المصادقة
  login,
  logout,
  register,
  getProfile,
  updateProfile,
  
  // المزارع
  getFarms,
  getFarm,
  createFarm,
  updateFarm,
  deleteFarm,
  
  // النباتات
  getPlants,
  getPlant,
  createPlant,
  updatePlant,
  deletePlant,
  
  // التشخيص
  getDiagnoses,
  getDiagnosis,
  createDiagnosis,
  updateDiagnosis,
  deleteDiagnosis,
  
  // الإحصائيات
  getStatistics,
  getDashboardStatistics,
  
  // التقارير
  getReports,
  getFarmsReport,
  
  // الإدارة
  getUsers,
  createUser,
  updateUser,
  deleteUser,
  
  // المساعدة
  setAuthToken,
  clearAuth,
  isAuthenticated,
  getCurrentUser
} = apiService;

