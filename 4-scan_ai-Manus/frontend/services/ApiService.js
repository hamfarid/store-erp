/**
 * API Service
 * ============
 * 
 * Centralized API service for all backend communications.
 * 
 * Features:
 * - Token management
 * - Request/Response interceptors
 * - Error handling
 * - Retry logic
 * - Request caching
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:4001/api/v1';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  /**
   * Set auth token
   */
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  /**
   * Set refresh token
   */
  setRefreshToken(token) {
    this.refreshToken = token;
    if (token) {
      localStorage.setItem('refresh_token', token);
    } else {
      localStorage.removeItem('refresh_token');
    }
  }

  /**
   * Clear auth
   */
  clearAuth() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  /**
   * Build headers
   */
  getHeaders(customHeaders = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...customHeaders
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  /**
   * Make HTTP request
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      ...options,
      headers: this.getHeaders(options.headers)
    };

    try {
      const response = await fetch(url, config);
      
      // Handle 401 - try to refresh token
      if (response.status === 401 && this.refreshToken) {
        const refreshed = await this.tryRefreshToken();
        if (refreshed) {
          // Retry with new token
          config.headers = this.getHeaders(options.headers);
          const retryResponse = await fetch(url, config);
          return this.handleResponse(retryResponse);
        }
      }

      return this.handleResponse(response);
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  /**
   * Handle response
   */
  async handleResponse(response) {
    const contentType = response.headers.get('content-type');
    
    let data;
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      if (response.status === 401) {
        // Dispatch logout event
        window.dispatchEvent(new Event('auth:logout'));
        this.clearAuth();
      }
      
      const error = new Error(data.detail || data.message || 'API Error');
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  }

  /**
   * Try to refresh access token
   */
  async tryRefreshToken() {
    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: this.refreshToken })
      });

      if (response.ok) {
        const data = await response.json();
        this.setToken(data.access_token);
        if (data.refresh_token) {
          this.setRefreshToken(data.refresh_token);
        }
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    this.clearAuth();
    return false;
  }

  // ==================
  // Auth Endpoints
  // ==================

  /**
   * Login
   */
  async login({ email, password }) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username: email, password })
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
      if (response.refresh_token) {
        this.setRefreshToken(response.refresh_token);
      }
    }
    
    return response;
  }

  /**
   * Register
   */
  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }

  /**
   * Logout
   */
  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } finally {
      this.clearAuth();
    }
  }

  /**
   * Get current user profile
   */
  async getProfile() {
    return this.request('/users/me');
  }

  /**
   * Update profile
   */
  async updateProfile(data) {
    return this.request('/users/me', {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  /**
   * Change password
   */
  async changePassword(currentPassword, newPassword) {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    });
  }

  /**
   * Request password reset
   */
  async forgotPassword(email) {
    return this.request('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  }

  /**
   * Reset password
   */
  async resetPassword(token, newPassword) {
    return this.request('/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, new_password: newPassword })
    });
  }

  // ==================
  // Farms Endpoints
  // ==================

  async getFarms(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/farms${query ? `?${query}` : ''}`);
  }

  async getFarm(id) {
    return this.request(`/farms/${id}`);
  }

  async createFarm(data) {
    return this.request('/farms', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateFarm(id, data) {
    return this.request(`/farms/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteFarm(id) {
    return this.request(`/farms/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Crops Endpoints
  // ==================

  async getCrops(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/crops${query ? `?${query}` : ''}`);
  }

  async getCrop(id) {
    return this.request(`/crops/${id}`);
  }

  async createCrop(data) {
    return this.request('/crops', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateCrop(id, data) {
    return this.request(`/crops/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteCrop(id) {
    return this.request(`/crops/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Diseases Endpoints
  // ==================

  async getDiseases(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/diseases${query ? `?${query}` : ''}`);
  }

  async getDisease(id) {
    return this.request(`/diseases/${id}`);
  }

  async createDisease(data) {
    return this.request('/diseases', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateDisease(id, data) {
    return this.request(`/diseases/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteDisease(id) {
    return this.request(`/diseases/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Diagnosis Endpoints
  // ==================

  async getDiagnoses(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/diagnoses${query ? `?${query}` : ''}`);
  }

  async getDiagnosis(id) {
    return this.request(`/diagnoses/${id}`);
  }

  async createDiagnosis(imageFile, data = {}) {
    const formData = new FormData();
    formData.append('image', imageFile);
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });

    return fetch(`${this.baseUrl}/diagnoses`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`
      },
      body: formData
    }).then(res => this.handleResponse(res));
  }

  async deleteDiagnosis(id) {
    return this.request(`/diagnoses/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Users Endpoints
  // ==================

  async getUsers(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/users${query ? `?${query}` : ''}`);
  }

  async getUser(id) {
    return this.request(`/users/${id}`);
  }

  async createUser(data) {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateUser(id, data) {
    return this.request(`/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteUser(id) {
    return this.request(`/users/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Equipment Endpoints
  // ==================

  async getEquipment(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/equipment${query ? `?${query}` : ''}`);
  }

  async getEquipmentItem(id) {
    return this.request(`/equipment/${id}`);
  }

  async createEquipment(data) {
    return this.request('/equipment', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateEquipment(id, data) {
    return this.request(`/equipment/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteEquipment(id) {
    return this.request(`/equipment/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Inventory Endpoints
  // ==================

  async getInventory(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/inventory${query ? `?${query}` : ''}`);
  }

  async getInventoryItem(id) {
    return this.request(`/inventory/${id}`);
  }

  async createInventoryItem(data) {
    return this.request('/inventory', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateInventoryItem(id, data) {
    return this.request(`/inventory/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteInventoryItem(id) {
    return this.request(`/inventory/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Sensors Endpoints
  // ==================

  async getSensors(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/sensors${query ? `?${query}` : ''}`);
  }

  async getSensor(id) {
    return this.request(`/sensors/${id}`);
  }

  async getSensorReadings(id, params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/sensors/${id}/readings${query ? `?${query}` : ''}`);
  }

  async createSensor(data) {
    return this.request('/sensors', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateSensor(id, data) {
    return this.request(`/sensors/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteSensor(id) {
    return this.request(`/sensors/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Analytics Endpoints
  // ==================

  async getDashboardStats() {
    return this.request('/analytics/dashboard');
  }

  async getDiseaseTrends(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/analytics/disease-trends${query ? `?${query}` : ''}`);
  }

  async getCropHealth(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/analytics/crop-health${query ? `?${query}` : ''}`);
  }

  async getYieldPredictions(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/analytics/yield-predictions${query ? `?${query}` : ''}`);
  }

  // ==================
  // Reports Endpoints
  // ==================

  async getReports(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/reports${query ? `?${query}` : ''}`);
  }

  async getReport(id) {
    return this.request(`/reports/${id}`);
  }

  async generateReport(type, params = {}) {
    return this.request('/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ type, ...params })
    });
  }

  async downloadReport(id, format = 'pdf') {
    const response = await fetch(`${this.baseUrl}/reports/${id}/download?format=${format}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to download report');
    }

    return response.blob();
  }

  // ==================
  // ML Service Endpoints
  // ==================

  async getMLModels() {
    return this.request('/ml/models');
  }

  async getMLModelMetrics(modelId) {
    return this.request(`/ml/models/${modelId}/metrics`);
  }

  async retrainModel(modelId, params = {}) {
    return this.request(`/ml/models/${modelId}/retrain`, {
      method: 'POST',
      body: JSON.stringify(params)
    });
  }

  async getTrainingHistory() {
    return this.request('/ml/training-history');
  }

  // ==================
  // Image Crawler Endpoints
  // ==================

  async getCrawlerStatus() {
    return this.request('/crawler/status');
  }

  async getCrawlerJobs() {
    return this.request('/crawler/jobs');
  }

  async startCrawlerJob(params) {
    return this.request('/crawler/jobs', {
      method: 'POST',
      body: JSON.stringify(params)
    });
  }

  async stopCrawlerJob(jobId) {
    return this.request(`/crawler/jobs/${jobId}/stop`, {
      method: 'POST'
    });
  }

  // ==================
  // Companies Endpoints
  // ==================

  async getCompanies(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/companies${query ? `?${query}` : ''}`);
  }

  async getCompany(id) {
    return this.request(`/companies/${id}`);
  }

  async createCompany(data) {
    return this.request('/companies', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateCompany(id, data) {
    return this.request(`/companies/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteCompany(id) {
    return this.request(`/companies/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Breeding Programs Endpoints
  // ==================

  async getBreedingPrograms(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/breeding${query ? `?${query}` : ''}`);
  }

  async getBreedingProgram(id) {
    return this.request(`/breeding/${id}`);
  }

  async createBreedingProgram(data) {
    return this.request('/breeding', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateBreedingProgram(id, data) {
    return this.request(`/breeding/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async deleteBreedingProgram(id) {
    return this.request(`/breeding/${id}`, { method: 'DELETE' });
  }

  // ==================
  // Settings Endpoints
  // ==================

  async getSettings() {
    return this.request('/settings');
  }

  async updateSettings(data) {
    return this.request('/settings', {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async getNotificationSettings() {
    return this.request('/settings/notifications');
  }

  async updateNotificationSettings(data) {
    return this.request('/settings/notifications', {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  // ==================
  // Setup Wizard Endpoint
  // ==================

  async completeSetup(data) {
    return this.request('/setup/complete', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // ==================
  // 2FA Endpoints
  // ==================

  async enable2FA() {
    return this.request('/auth/2fa/enable', { method: 'POST' });
  }

  async verify2FA(code) {
    return this.request('/auth/2fa/verify', {
      method: 'POST',
      body: JSON.stringify({ code })
    });
  }

  async disable2FA(code) {
    return this.request('/auth/2fa/disable', {
      method: 'POST',
      body: JSON.stringify({ code })
    });
  }

  // ==================
  // File Upload
  // ==================

  async uploadFile(file, folder = 'uploads') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('folder', folder);

    return fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`
      },
      body: formData
    }).then(res => this.handleResponse(res));
  }

  async uploadAvatar(file) {
    const formData = new FormData();
    formData.append('avatar', file);

    return fetch(`${this.baseUrl}/users/me/avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`
      },
      body: formData
    }).then(res => this.handleResponse(res));
  }

  // ==================
  // Health Check
  // ==================

  async getHealth() {
    return this.request('/health');
  }

  async getSystemStatus() {
    return this.request('/system/status');
  }
}

// Export singleton instance
export default new ApiService();
