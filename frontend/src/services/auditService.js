/**
 * خدمة سجل التدقيق (Audit Service)
 * @file frontend/src/services/auditService.js
 */

import apiClient from './apiClient';

export const auditService = {
  // ==================== سجلات التدقيق ====================

  /**
   * الحصول على جميع سجلات التدقيق
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 100,
        action_type: params.actionType || '',
        user_id: params.userId || '',
        entity_type: params.entityType || '',
        entity_id: params.entityId || '',
        start_date: params.startDate || '',
        end_date: params.endDate || '',
        ...params
      };

      const response = await apiClient.get('/api/audit-logs', queryParams);
      return {
        logs: response.logs || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 100)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل سجلات التدقيق: ${error.message}`);
    }
  },

  /**
   * الحصول على سجل بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/audit-logs/${id}`);
      return response.log || response;
    } catch (error) {
      throw new Error(`فشل في تحميل السجل: ${error.message}`);
    }
  },

  // ==================== فلترة السجلات ====================

  /**
   * الحصول على سجلات مستخدم
   */
  async getUserLogs(userId, params = {}) {
    try {
      const response = await apiClient.get(`/api/audit-logs/user/${userId}`, params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل سجلات المستخدم: ${error.message}`);
    }
  },

  /**
   * الحصول على سجلات كيان
   */
  async getEntityLogs(entityType, entityId, params = {}) {
    try {
      const response = await apiClient.get(`/api/audit-logs/entity/${entityType}/${entityId}`, params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل سجلات الكيان: ${error.message}`);
    }
  },

  /**
   * الحصول على سجلات حسب نوع العملية
   */
  async getByActionType(actionType, params = {}) {
    try {
      const response = await apiClient.get(`/api/audit-logs/action/${actionType}`, params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل السجلات: ${error.message}`);
    }
  },

  // ==================== سجلات الأمان ====================

  /**
   * الحصول على سجلات تسجيل الدخول
   */
  async getLoginLogs(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/security/logins', params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل سجلات تسجيل الدخول: ${error.message}`);
    }
  },

  /**
   * الحصول على محاولات الدخول الفاشلة
   */
  async getFailedLogins(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/security/failed-logins', params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المحاولات الفاشلة: ${error.message}`);
    }
  },

  /**
   * الحصول على سجلات الصلاحيات
   */
  async getPermissionLogs(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/security/permissions', params);
      return response.logs || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل سجلات الصلاحيات: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير نشاط المستخدمين
   */
  async getUserActivityReport(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/reports/user-activity', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * تقرير العمليات
   */
  async getOperationsReport(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/reports/operations', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * تقرير أمني شامل
   */
  async getSecurityReport(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/reports/security', params);
      return response.report || {};
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير الأمني: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات السجلات
   */
  async getStats(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/stats', params);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * ملخص النشاط اليومي
   */
  async getDailySummary(params = {}) {
    try {
      const response = await apiClient.get('/api/audit-logs/daily-summary', params);
      return response.summary || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الملخص اليومي: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير السجلات إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/audit-logs/export/excel', 'audit_logs.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  /**
   * تصدير إلى PDF
   */
  async exportToPDF(params = {}) {
    try {
      await apiClient.downloadFile('/api/audit-logs/export/pdf', 'audit_logs.pdf');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  // ==================== أنواع العمليات ====================

  /**
   * الحصول على أنواع العمليات
   */
  async getActionTypes() {
    try {
      const response = await apiClient.get('/api/audit-logs/action-types');
      return response.types || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أنواع العمليات: ${error.message}`);
    }
  },

  /**
   * الحصول على أنواع الكيانات
   */
  async getEntityTypes() {
    try {
      const response = await apiClient.get('/api/audit-logs/entity-types');
      return response.types || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أنواع الكيانات: ${error.message}`);
    }
  }
};

export default auditService;
