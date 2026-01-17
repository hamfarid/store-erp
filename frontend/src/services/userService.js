/**
 * خدمة إدارة المستخدمين (User Management Service)
 * @file frontend/src/services/userService.js
 */

import apiClient from './apiClient';

const userService = {
  // ==================== CRUD Operations ====================

  /**
   * الحصول على جميع المستخدمين
   * @param {Object} params - معلمات الترشيح والترتيب
   */
  async getUsers(params = {}) {
    return apiClient.get('/api/users', params);
  },

  /**
   * الحصول على مستخدم بواسطة ID
   * @param {number} id - معرف المستخدم
   */
  async getUserById(id) {
    return apiClient.get(`/api/users/${id}`);
  },

  /**
   * إنشاء مستخدم جديد
   * @param {Object} data - بيانات المستخدم
   */
  async createUser(data) {
    return apiClient.post('/api/users', data);
  },

  /**
   * تحديث مستخدم
   * @param {number} id - معرف المستخدم
   * @param {Object} data - البيانات المحدثة
   */
  async updateUser(id, data) {
    return apiClient.put(`/api/users/${id}`, data);
  },

  /**
   * حذف مستخدم
   * @param {number} id - معرف المستخدم
   */
  async deleteUser(id) {
    return apiClient.delete(`/api/users/${id}`);
  },

  // ==================== Status Operations ====================

  /**
   * تفعيل/إلغاء تفعيل مستخدم
   * @param {number} id - معرف المستخدم
   * @param {boolean} isActive - حالة التفعيل
   */
  async toggleUserActive(id, isActive) {
    return apiClient.patch(`/api/users/${id}/active`, { is_active: isActive });
  },

  /**
   * قفل/فتح حساب مستخدم
   * @param {number} id - معرف المستخدم
   * @param {boolean} isLocked - حالة القفل
   */
  async toggleUserLocked(id, isLocked) {
    return apiClient.patch(`/api/users/${id}/locked`, { is_locked: isLocked });
  },

  // ==================== Role Operations ====================

  /**
   * الحصول على جميع الأدوار
   */
  async getRoles() {
    return apiClient.get('/api/roles');
  },

  /**
   * الحصول على دور بواسطة ID
   * @param {number} id - معرف الدور
   */
  async getRoleById(id) {
    return apiClient.get(`/api/roles/${id}`);
  },

  /**
   * إنشاء دور جديد
   * @param {Object} data - بيانات الدور
   */
  async createRole(data) {
    return apiClient.post('/api/roles', data);
  },

  /**
   * تحديث دور
   * @param {number} id - معرف الدور
   * @param {Object} data - البيانات المحدثة
   */
  async updateRole(id, data) {
    return apiClient.put(`/api/roles/${id}`, data);
  },

  /**
   * حذف دور
   * @param {number} id - معرف الدور
   */
  async deleteRole(id) {
    return apiClient.delete(`/api/roles/${id}`);
  },

  /**
   * تعيين دور لمستخدم
   * @param {number} userId - معرف المستخدم
   * @param {number} roleId - معرف الدور
   */
  async assignRole(userId, roleId) {
    return apiClient.post(`/api/users/${userId}/role`, { role_id: roleId });
  },

  // ==================== Permission Operations ====================

  /**
   * الحصول على جميع الصلاحيات
   */
  async getPermissions() {
    return apiClient.get('/api/permissions');
  },

  /**
   * الحصول على صلاحيات دور
   * @param {number} roleId - معرف الدور
   */
  async getRolePermissions(roleId) {
    return apiClient.get(`/api/roles/${roleId}/permissions`);
  },

  /**
   * تحديث صلاحيات دور
   * @param {number} roleId - معرف الدور
   * @param {Array} permissions - الصلاحيات
   */
  async updateRolePermissions(roleId, permissions) {
    return apiClient.put(`/api/roles/${roleId}/permissions`, { permissions });
  },

  /**
   * الحصول على صلاحيات مستخدم
   * @param {number} userId - معرف المستخدم
   */
  async getUserPermissions(userId) {
    return apiClient.get(`/api/users/${userId}/permissions`);
  },

  /**
   * فحص صلاحية مستخدم
   * @param {number} userId - معرف المستخدم
   * @param {string} permission - الصلاحية
   */
  async checkPermission(userId, permission) {
    return apiClient.get(`/api/users/${userId}/check-permission`, { permission });
  },

  // ==================== Profile Operations ====================

  /**
   * رفع صورة المستخدم
   * @param {number} userId - معرف المستخدم
   * @param {File} file - ملف الصورة
   */
  async uploadAvatar(userId, file) {
    return apiClient.uploadFile(`/api/users/${userId}/avatar`, file);
  },

  /**
   * حذف صورة المستخدم
   * @param {number} userId - معرف المستخدم
   */
  async deleteAvatar(userId) {
    return apiClient.delete(`/api/users/${userId}/avatar`);
  },

  // ==================== Password Operations ====================

  /**
   * إعادة تعيين كلمة مرور مستخدم (بواسطة المدير)
   * @param {number} userId - معرف المستخدم
   * @param {string} newPassword - كلمة المرور الجديدة
   */
  async resetUserPassword(userId, newPassword) {
    return apiClient.post(`/api/users/${userId}/reset-password`, {
      new_password: newPassword
    });
  },

  /**
   * إرسال رابط إعادة تعيين كلمة المرور
   * @param {number} userId - معرف المستخدم
   */
  async sendPasswordResetLink(userId) {
    return apiClient.post(`/api/users/${userId}/send-password-reset`);
  },

  // ==================== 2FA Operations ====================

  /**
   * إلغاء المصادقة الثنائية لمستخدم (بواسطة المدير)
   * @param {number} userId - معرف المستخدم
   */
  async disable2FAForUser(userId) {
    return apiClient.post(`/api/users/${userId}/disable-2fa`);
  },

  // ==================== Activity Operations ====================

  /**
   * الحصول على سجل نشاط المستخدم
   * @param {number} userId - معرف المستخدم
   * @param {Object} params - معلمات الترشيح
   */
  async getUserActivityLog(userId, params = {}) {
    return apiClient.get(`/api/users/${userId}/activity-log`, params);
  },

  /**
   * الحصول على جلسات المستخدم
   * @param {number} userId - معرف المستخدم
   */
  async getUserSessions(userId) {
    return apiClient.get(`/api/users/${userId}/sessions`);
  },

  /**
   * إنهاء جميع جلسات مستخدم
   * @param {number} userId - معرف المستخدم
   */
  async terminateUserSessions(userId) {
    return apiClient.post(`/api/users/${userId}/terminate-sessions`);
  },

  // ==================== Statistics ====================

  /**
   * إحصائيات المستخدمين
   */
  async getUserStats() {
    return apiClient.get('/api/users/stats');
  },

  /**
   * المستخدمون النشطون حالياً
   */
  async getOnlineUsers() {
    return apiClient.get('/api/users/online');
  },

  // ==================== Export ====================

  /**
   * تصدير المستخدمين إلى Excel
   * @param {Object} filters - معلمات الترشيح
   */
  async exportToExcel(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    const endpoint = queryString ? `/api/users/export/excel?${queryString}` : '/api/users/export/excel';
    return apiClient.downloadFile(endpoint, 'users_export.xlsx');
  }
};

export default userService;
