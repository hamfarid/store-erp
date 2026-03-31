/**
 * خدمة المهام الآلية (Automation Service)
 * @file frontend/src/services/automationService.js
 */

import apiClient from './apiClient';

export const automationService = {
  // ==================== المهام الآلية ====================

  /**
   * الحصول على جميع المهام الآلية
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        status: params.status || '',
        type: params.type || '',
        ...params
      };

      const response = await apiClient.get('/api/automation/tasks', queryParams);
      return {
        tasks: response.tasks || response.data || [],
        total: response.total || 0,
        page: response.page || 1
      };
    } catch (error) {
      throw new Error(`فشل في تحميل المهام الآلية: ${error.message}`);
    }
  },

  /**
   * الحصول على مهمة بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/automation/tasks/${id}`);
      return response.task || response;
    } catch (error) {
      throw new Error(`فشل في تحميل المهمة: ${error.message}`);
    }
  },

  /**
   * إنشاء مهمة آلية
   */
  async create(taskData) {
    try {
      const response = await apiClient.post('/api/automation/tasks', taskData);
      return response.task || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء المهمة: ${error.message}`);
    }
  },

  /**
   * تحديث مهمة
   */
  async update(id, taskData) {
    try {
      const response = await apiClient.put(`/api/automation/tasks/${id}`, taskData);
      return response.task || response;
    } catch (error) {
      throw new Error(`فشل في تحديث المهمة: ${error.message}`);
    }
  },

  /**
   * حذف مهمة
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/automation/tasks/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف المهمة: ${error.message}`);
    }
  },

  // ==================== التحكم في المهام ====================

  /**
   * تشغيل مهمة يدوياً
   */
  async run(id) {
    try {
      const response = await apiClient.post(`/api/automation/tasks/${id}/run`);
      return response;
    } catch (error) {
      throw new Error(`فشل في تشغيل المهمة: ${error.message}`);
    }
  },

  /**
   * إيقاف مهمة
   */
  async stop(id) {
    try {
      const response = await apiClient.post(`/api/automation/tasks/${id}/stop`);
      return response;
    } catch (error) {
      throw new Error(`فشل في إيقاف المهمة: ${error.message}`);
    }
  },

  /**
   * تفعيل/إلغاء تفعيل مهمة
   */
  async toggle(id, enabled) {
    try {
      const response = await apiClient.patch(`/api/automation/tasks/${id}/toggle`, { enabled });
      return response;
    } catch (error) {
      throw new Error(`فشل في تبديل حالة المهمة: ${error.message}`);
    }
  },

  // ==================== أنواع المهام المحددة ====================

  /**
   * مهمة تنبيه انتهاء الصلاحية
   */
  async createExpiryAlert(config) {
    try {
      const response = await apiClient.post('/api/automation/tasks/expiry-alert', config);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء تنبيه الصلاحية: ${error.message}`);
    }
  },

  /**
   * مهمة تنبيه المخزون المنخفض
   */
  async createLowStockAlert(config) {
    try {
      const response = await apiClient.post('/api/automation/tasks/low-stock-alert', config);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء تنبيه المخزون: ${error.message}`);
    }
  },

  /**
   * مهمة النسخ الاحتياطي التلقائي
   */
  async createAutoBackup(config) {
    try {
      const response = await apiClient.post('/api/automation/tasks/auto-backup', config);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مهمة النسخ الاحتياطي: ${error.message}`);
    }
  },

  /**
   * مهمة التقرير الدوري
   */
  async createPeriodicReport(config) {
    try {
      const response = await apiClient.post('/api/automation/tasks/periodic-report', config);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مهمة التقرير: ${error.message}`);
    }
  },

  /**
   * مهمة تنظيف البيانات
   */
  async createDataCleanup(config) {
    try {
      const response = await apiClient.post('/api/automation/tasks/data-cleanup', config);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مهمة التنظيف: ${error.message}`);
    }
  },

  // ==================== سجل التنفيذ ====================

  /**
   * الحصول على سجل تنفيذ المهمة
   */
  async getExecutionHistory(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/automation/tasks/${id}/history`, params);
      return response.history || [];
    } catch (error) {
      throw new Error(`فشل في تحميل سجل التنفيذ: ${error.message}`);
    }
  },

  /**
   * الحصول على آخر نتيجة تنفيذ
   */
  async getLastExecution(id) {
    try {
      const response = await apiClient.get(`/api/automation/tasks/${id}/last-execution`);
      return response.execution || null;
    } catch (error) {
      throw new Error(`فشل في تحميل آخر تنفيذ: ${error.message}`);
    }
  },

  // ==================== الجدولة ====================

  /**
   * الحصول على المهام المجدولة
   */
  async getScheduledTasks(params = {}) {
    try {
      const response = await apiClient.get('/api/automation/scheduled', params);
      return response.tasks || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المهام المجدولة: ${error.message}`);
    }
  },

  /**
   * الحصول على المهام قيد التشغيل
   */
  async getRunningTasks() {
    try {
      const response = await apiClient.get('/api/automation/running');
      return response.tasks || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المهام قيد التشغيل: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات المهام الآلية
   */
  async getStats() {
    try {
      const response = await apiClient.get('/api/automation/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * أنواع المهام المتاحة
   */
  async getTaskTypes() {
    try {
      const response = await apiClient.get('/api/automation/task-types');
      return response.types || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أنواع المهام: ${error.message}`);
    }
  }
};

export default automationService;
