/**
 * خدمة المصادقة (Authentication Service)
 * @file frontend/src/services/authService.js
 */

import apiClient from './apiClient';

const authService = {
  // ==================== Authentication ====================

  /**
   * تسجيل الدخول
   * @param {string} username - اسم المستخدم
   * @param {string} password - كلمة المرور
   */
  async login(username, password) {
    const response = await apiClient.post('/api/auth/login', {
      username,
      password
    });

    // حفظ التوكن في حالة النجاح
    if (response.access_token) {
      apiClient.setToken(response.access_token, response.refresh_token);
    }

    return response;
  },

  /**
   * تسجيل الخروج
   */
  async logout() {
    try {
      await apiClient.post('/api/auth/logout');
    } finally {
      apiClient.clearToken();
    }
  },

  /**
   * تجديد التوكن
   */
  async refreshToken() {
    const refreshToken = apiClient.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post('/api/auth/refresh', {
      refresh_token: refreshToken
    });

    if (response.access_token) {
      apiClient.setToken(response.access_token, response.refresh_token);
    }

    return response;
  },

  /**
   * الحصول على بيانات المستخدم الحالي
   */
  async getCurrentUser() {
    return apiClient.get('/api/auth/me');
  },

  /**
   * تحديث بيانات المستخدم الحالي
   * @param {Object} data - البيانات المحدثة
   */
  async updateCurrentUser(data) {
    return apiClient.put('/api/auth/me', data);
  },

  // ==================== Password ====================

  /**
   * تغيير كلمة المرور
   * @param {string} currentPassword - كلمة المرور الحالية
   * @param {string} newPassword - كلمة المرور الجديدة
   */
  async changePassword(currentPassword, newPassword) {
    return apiClient.post('/api/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });
  },

  /**
   * طلب إعادة تعيين كلمة المرور
   * @param {string} email - البريد الإلكتروني
   */
  async forgotPassword(email) {
    return apiClient.post('/api/auth/forgot-password', { email });
  },

  /**
   * إعادة تعيين كلمة المرور
   * @param {string} token - رمز إعادة التعيين
   * @param {string} newPassword - كلمة المرور الجديدة
   */
  async resetPassword(token, newPassword) {
    return apiClient.post('/api/auth/reset-password', {
      token,
      new_password: newPassword
    });
  },

  // ==================== Two-Factor Authentication ====================

  /**
   * تفعيل المصادقة الثنائية
   */
  async enable2FA() {
    return apiClient.post('/api/auth/2fa/enable');
  },

  /**
   * إلغاء المصادقة الثنائية
   * @param {string} code - رمز التحقق
   */
  async disable2FA(code) {
    return apiClient.post('/api/auth/2fa/disable', { code });
  },

  /**
   * التحقق من رمز المصادقة الثنائية
   * @param {string} code - رمز التحقق
   */
  async verify2FA(code) {
    const response = await apiClient.post('/api/auth/2fa/verify', { code });

    if (response.access_token) {
      apiClient.setToken(response.access_token, response.refresh_token);
    }

    return response;
  },

  /**
   * الحصول على رموز الاسترداد
   */
  async getBackupCodes() {
    return apiClient.get('/api/auth/2fa/backup-codes');
  },

  /**
   * إعادة توليد رموز الاسترداد
   */
  async regenerateBackupCodes() {
    return apiClient.post('/api/auth/2fa/backup-codes/regenerate');
  },

  // ==================== Sessions ====================

  /**
   * الحصول على الجلسات النشطة
   */
  async getActiveSessions() {
    return apiClient.get('/api/auth/sessions');
  },

  /**
   * إنهاء جلسة محددة
   * @param {string} sessionId - معرف الجلسة
   */
  async terminateSession(sessionId) {
    return apiClient.delete(`/api/auth/sessions/${sessionId}`);
  },

  /**
   * إنهاء جميع الجلسات الأخرى
   */
  async terminateOtherSessions() {
    return apiClient.post('/api/auth/sessions/terminate-others');
  },

  // ==================== Verification ====================

  /**
   * التحقق من صحة التوكن
   */
  async verifyToken() {
    return apiClient.get('/api/auth/verify');
  },

  /**
   * فحص حالة المصادقة
   */
  isAuthenticated() {
    return apiClient.isAuthenticated();
  },

  /**
   * الحصول على معلومات المستخدم من التوكن
   */
  getUserFromToken() {
    return apiClient.getUserFromToken();
  },

  // ==================== Audit ====================

  /**
   * الحصول على سجل تسجيل الدخول
   * @param {Object} params - معلمات الترشيح
   */
  async getLoginHistory(params = {}) {
    return apiClient.get('/api/auth/login-history', params);
  },

  /**
   * الحصول على سجل النشاط
   * @param {Object} params - معلمات الترشيح
   */
  async getActivityLog(params = {}) {
    return apiClient.get('/api/auth/activity-log', params);
  },

  // ==================== Registration ====================

  /**
   * تسجيل مستخدم جديد
   * @param {Object} userData - بيانات المستخدم الجديد
   */
  async register(userData) {
    return apiClient.post('/api/auth/register', userData);
  }
};

export default authService;
