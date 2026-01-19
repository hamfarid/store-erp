// ملف: /home/ubuntu/gaara-ai-system/gaara_ai_integrated/frontend/src/services/ApiServiceEnhanced.js
// خدمة API محسنة ومطورة لنظام Gaara AI
// الإصدار: 3.0.0
// تم التحديث: 2025-01-21

import axios from 'axios';

// إعداد الـ Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:4001/api';

class ApiServiceEnhanced {
  constructor() {
    // إنشاء instance من axios
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // إضافة interceptor للطلبات
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken') || localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // إضافة interceptor للاستجابات
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // دوال مساعدة
  async request(method, endpoint, data = null, config = {}) {
    try {
      const response = await this.client.request({
        method,
        url: endpoint,
        data,
        ...config
      });
      return response.data;
    } catch (error) {
      console.error(`خطأ في طلب ${method.toUpperCase()}:`, error);
      throw this.handleError(error);
    }
  }

  async get(endpoint, params = {}) {
    return this.request('GET', endpoint, null, { params });
  }

  async post(endpoint, data) {
    return this.request('POST', endpoint, data);
  }

  async put(endpoint, data) {
    return this.request('PUT', endpoint, data);
  }

  async delete(endpoint) {
    return this.request('DELETE', endpoint);
  }

  // معالجة الأخطاء
  handleError(error) {
    if (error.response) {
      return {
        type: 'server',
        message: error.response.data?.message || 'حدث خطأ في الخادم',
        status: error.response.status,
        data: error.response.data
      };
    } else if (error.request) {
      return {
        type: 'network',
        message: 'فشل في الاتصال بالخادم',
        error
      };
    } else {
      return {
        type: 'client',
        message: error.message || 'حدث خطأ غير متوقع',
        error
      };
    }
  }

  // إدارة التوكن
  setToken(token) {
    localStorage.setItem('authToken', token);
    localStorage.setItem('token', token); // للتوافق مع النسخة القديمة
  }

  removeToken() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // ===== خدمات المصادقة =====
  async login(credentials) {
    const response = await this.post('/auth/login', credentials);
    if (response.token) {
      this.setToken(response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  }

  async register(userData) {
    return this.post('/auth/register', userData);
  }

  async logout() {
    try {
      await this.post('/auth/logout');
    } finally {
      this.removeToken();
    }
  }

  async getCurrentUser() {
    return this.get('/auth/me');
  }

  async refreshToken() {
    const response = await this.post('/auth/refresh');
    if (response.token) {
      this.setToken(response.token);
    }
    return response;
  }

  // ===== خدمات المزارع =====
  async getFarms(params = {}) {
    return this.get('/farms', params);
  }

  async getFarm(farmId) {
    return this.get(`/farms/${farmId}`);
  }

  async createFarm(farmData) {
    return this.post('/farms', farmData);
  }

  async updateFarm(farmId, farmData) {
    return this.put(`/farms/${farmId}`, farmData);
  }

  async deleteFarm(farmId) {
    return this.delete(`/farms/${farmId}`);
  }

  async getFarmStatistics(farmId) {
    return this.get(`/farms/${farmId}/statistics`);
  }

  // ===== خدمات النباتات =====
  async getPlants(params = {}) {
    return this.get('/plants', params);
  }

  async getPlant(plantId) {
    return this.get(`/plants/${plantId}`);
  }

  async createPlant(plantData) {
    return this.post('/plants', plantData);
  }

  async updatePlant(plantId, plantData) {
    return this.put(`/plants/${plantId}`, plantData);
  }

  async deletePlant(plantId) {
    return this.delete(`/plants/${plantId}`);
  }

  async getPlantsByFarm(farmId) {
    return this.get(`/farms/${farmId}/plants`);
  }

  // ===== خدمات المحاصيل =====
  async getCrops(params = {}) {
    return this.get('/crops', params);
  }

  async getCrop(cropId) {
    return this.get(`/crops/${cropId}`);
  }

  async createCrop(cropData) {
    return this.post('/crops', cropData);
  }

  async updateCrop(cropId, cropData) {
    return this.put(`/crops/${cropId}`, cropData);
  }

  async deleteCrop(cropId) {
    return this.delete(`/crops/${cropId}`);
  }

  // ===== خدمات الأمراض =====
  async getDiseases(params = {}) {
    return this.get('/diseases', params);
  }

  async getDisease(diseaseId) {
    return this.get(`/diseases/${diseaseId}`);
  }

  async createDisease(diseaseData) {
    return this.post('/diseases', diseaseData);
  }

  async updateDisease(diseaseId, diseaseData) {
    return this.put(`/diseases/${diseaseId}`, diseaseData);
  }

  async deleteDisease(diseaseId) {
    return this.delete(`/diseases/${diseaseId}`);
  }

  // ===== خدمات التشخيص =====
  async getDiagnoses(params = {}) {
    return this.get('/diagnosis', params);
  }

  async getDiagnosis(diagnosisId) {
    return this.get(`/diagnosis/${diagnosisId}`);
  }

  async createDiagnosis(diagnosisData) {
    return this.post('/diagnosis', diagnosisData);
  }

  async updateDiagnosis(diagnosisId, diagnosisData) {
    return this.put(`/diagnosis/${diagnosisId}`, diagnosisData);
  }

  async deleteDiagnosis(diagnosisId) {
    return this.delete(`/diagnosis/${diagnosisId}`);
  }

  async diagnoseImage(imageFile, plantType = null) {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (plantType) {
      formData.append('plant_type', plantType);
    }

    return this.request('POST', '/diagnosis/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async getDiagnosisHistory(params = {}) {
    return this.get('/diagnosis/history', params);
  }

  // ===== خدمات التهجين =====
  async getBreedingPrograms(params = {}) {
    return this.get('/breeding', params);
  }

  async getBreedingProgram(programId) {
    return this.get(`/breeding/${programId}`);
  }

  async createBreedingProgram(programData) {
    return this.post('/breeding', programData);
  }

  async updateBreedingProgram(programId, programData) {
    return this.put(`/breeding/${programId}`, programData);
  }

  async deleteBreedingProgram(programId) {
    return this.delete(`/breeding/${programId}`);
  }

  // ===== خدمات أجهزة الاستشعار =====
  async getSensors(params = {}) {
    return this.get('/sensors', params);
  }

  async getSensor(sensorId) {
    return this.get(`/sensors/${sensorId}`);
  }

  async createSensor(sensorData) {
    return this.post('/sensors', sensorData);
  }

  async updateSensor(sensorId, sensorData) {
    return this.put(`/sensors/${sensorId}`, sensorData);
  }

  async deleteSensor(sensorId) {
    return this.delete(`/sensors/${sensorId}`);
  }

  async getSensorData(farmId = null, sensorType = null) {
    const params = {};
    if (farmId) params.farm_id = farmId;
    if (sensorType) params.type = sensorType;
    return this.get('/sensors', params);
  }

  async addSensorData(sensorData) {
    return this.post('/sensors', sensorData);
  }

  async getSensorReadings(sensorId, params = {}) {
    return this.get(`/sensors/${sensorId}/readings`, params);
  }

  async getLatestSensorReadings(farmId) {
    return this.get(`/farms/${farmId}/sensors/latest`);
  }

  // ===== خدمات التقارير =====
  async getReports(params = {}) {
    return this.get('/reports', params);
  }

  async getReport(reportId) {
    return this.get(`/reports/${reportId}`);
  }

  async createReport(reportData) {
    return this.post('/reports', reportData);
  }

  async generateReport(reportType, params = {}) {
    return this.post('/reports/generate', {
      type: reportType,
      ...params
    });
  }

  async downloadReport(reportId) {
    return this.request('GET', `/reports/${reportId}/download`, null, {
      responseType: 'blob'
    });
  }

  async getFarmReport(farmId, params = {}) {
    return this.get(`/farms/${farmId}/report`, params);
  }

  // ===== خدمات التحليلات =====
  async getAnalytics(params = {}) {
    return this.get('/analytics', params);
  }

  async getDashboardData() {
    return this.get('/analytics/dashboard');
  }

  async getFarmAnalytics(farmId, period = '30d') {
    return this.get(`/analytics/farms/${farmId}`, { period });
  }

  async getProductionAnalytics(params = {}) {
    return this.get('/analytics/production', params);
  }

  async getDiseaseAnalytics(params = {}) {
    return this.get('/analytics/diseases', params);
  }

  async getWeatherAnalytics(farmId, days = 7) {
    return this.get(`/analytics/weather/${farmId}`, { days });
  }

  // ===== خدمات المستخدمين =====
  async getUsers(params = {}) {
    return this.get('/users', params);
  }

  async getUser(userId) {
    return this.get(`/users/${userId}`);
  }

  async createUser(userData) {
    return this.post('/users', userData);
  }

  async updateUser(userId, userData) {
    return this.put(`/users/${userId}`, userData);
  }

  async deleteUser(userId) {
    return this.delete(`/users/${userId}`);
  }

  async updateProfile(userData) {
    return this.put('/users/profile', userData);
  }

  async changePassword(passwordData) {
    return this.put('/users/password', passwordData);
  }

  // ===== خدمات الشركات =====
  async getCompanies(params = {}) {
    return this.get('/companies', params);
  }

  async getCompany(companyId) {
    return this.get(`/companies/${companyId}`);
  }

  async createCompany(companyData) {
    return this.post('/companies', companyData);
  }

  async updateCompany(companyId, companyData) {
    return this.put(`/companies/${companyId}`, companyData);
  }

  async deleteCompany(companyId) {
    return this.delete(`/companies/${companyId}`);
  }

  // ===== خدمات الإعدادات =====
  async getSettings(params = {}) {
    return this.get('/settings', params);
  }

  async getSetting(settingId) {
    return this.get(`/settings/${settingId}`);
  }

  async createSetting(settingData) {
    return this.post('/settings', settingData);
  }

  async updateSetting(settingId, settingData) {
    return this.put(`/settings/${settingId}`, settingData);
  }

  async deleteSetting(settingId) {
    return this.delete(`/settings/${settingId}`);
  }

  async getSystemInfo() {
    return this.get('/settings/system-info');
  }

  // ===== خدمات الإشعارات =====
  async getNotifications(params = {}) {
    return this.get('/notifications', params);
  }

  async markNotificationAsRead(notificationId) {
    return this.put(`/notifications/${notificationId}/read`);
  }

  async markAllNotificationsAsRead() {
    return this.put('/notifications/read-all');
  }

  async deleteNotification(notificationId) {
    return this.delete(`/notifications/${notificationId}`);
  }

  // ===== معالج الإعداد =====
  async setupWizard(setupData) {
    return this.post('/setup-wizard', setupData);
  }

  // ===== فحص صحة النظام =====
  async healthCheck() {
    return this.get('/health');
  }

  // ===== خدمات التجارة الإلكترونية =====
  async getProducts(params = {}) {
    return this.get('/ecommerce/products', params);
  }

  async getProduct(productId) {
    return this.get(`/ecommerce/products/${productId}`);
  }

  async createProduct(productData) {
    return this.post('/ecommerce/products', productData);
  }

  async updateProduct(productId, productData) {
    return this.put(`/ecommerce/products/${productId}`, productData);
  }

  async deleteProduct(productId) {
    return this.delete(`/ecommerce/products/${productId}`);
  }

  async getOrders(params = {}) {
    return this.get('/ecommerce/orders', params);
  }

  async getOrder(orderId) {
    return this.get(`/ecommerce/orders/${orderId}`);
  }

  async createOrder(orderData) {
    return this.post('/ecommerce/orders', orderData);
  }

  async updateOrderStatus(orderId, status) {
    return this.put(`/ecommerce/orders/${orderId}/status`, { status });
  }

  // ===== خدمات الذكاء الاصطناعي =====
  async predictYield(farmId, cropType, params = {}) {
    return this.post('/ai/predict-yield', {
      farm_id: farmId,
      crop_type: cropType,
      ...params
    });
  }

  async detectDisease(imageFile, plantType = null) {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (plantType) {
      formData.append('plant_type', plantType);
    }

    return this.request('POST', '/ai/detect-disease', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async getWeatherPrediction(farmId, days = 7) {
    return this.get(`/ai/weather-prediction/${farmId}`, { days });
  }

  async optimizeIrrigation(farmId, params = {}) {
    return this.post('/ai/optimize-irrigation', {
      farm_id: farmId,
      ...params
    });
  }
}

// إنشاء مثيل واحد للاستخدام
const apiServiceEnhanced = new ApiServiceEnhanced();

export default apiServiceEnhanced;
