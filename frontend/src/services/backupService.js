/**
 * خدمة النسخ الاحتياطي (Backup Service)
 * @file frontend/src/services/backupService.js
 */

import apiClient from './apiClient';

export const backupService = {
  // ==================== النسخ الاحتياطية ====================

  /**
   * الحصول على جميع النسخ الاحتياطية
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        type: params.type || '',
        status: params.status || '',
        ...params
      };

      const response = await apiClient.get('/api/backups', queryParams);
      return {
        backups: response.backups || response.data || [],
        total: response.total || 0,
        page: response.page || 1
      };
    } catch (error) {
      throw new Error(`فشل في تحميل النسخ الاحتياطية: ${error.message}`);
    }
  },

  /**
   * الحصول على نسخة احتياطية بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/backups/${id}`);
      return response.backup || response;
    } catch (error) {
      throw new Error(`فشل في تحميل النسخة الاحتياطية: ${error.message}`);
    }
  },

  // ==================== إنشاء النسخ ====================

  /**
   * إنشاء نسخة احتياطية كاملة
   */
  async createFull() {
    try {
      const response = await apiClient.post('/api/backups/create/full');
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء النسخة الاحتياطية: ${error.message}`);
    }
  },

  /**
   * إنشاء نسخة احتياطية للبيانات فقط
   */
  async createDataOnly() {
    try {
      const response = await apiClient.post('/api/backups/create/data');
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء نسخة البيانات: ${error.message}`);
    }
  },

  /**
   * إنشاء نسخة احتياطية مخصصة
   */
  async createCustom(options) {
    try {
      const response = await apiClient.post('/api/backups/create/custom', options);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء النسخة المخصصة: ${error.message}`);
    }
  },

  // ==================== الاستعادة ====================

  /**
   * استعادة من نسخة احتياطية
   */
  async restore(backupId, options = {}) {
    try {
      const response = await apiClient.post(`/api/backups/${backupId}/restore`, options);
      return response;
    } catch (error) {
      throw new Error(`فشل في الاستعادة: ${error.message}`);
    }
  },

  /**
   * استعادة من ملف
   */
  async restoreFromFile(file) {
    try {
      const response = await apiClient.uploadFile('/api/backups/restore/file', file);
      return response;
    } catch (error) {
      throw new Error(`فشل في الاستعادة من الملف: ${error.message}`);
    }
  },

  /**
   * معاينة الاستعادة
   */
  async previewRestore(backupId) {
    try {
      const response = await apiClient.get(`/api/backups/${backupId}/preview`);
      return response.preview || {};
    } catch (error) {
      throw new Error(`فشل في المعاينة: ${error.message}`);
    }
  },

  // ==================== إدارة النسخ ====================

  /**
   * تحميل نسخة احتياطية
   */
  async download(backupId) {
    try {
      await apiClient.downloadFile(`/api/backups/${backupId}/download`, `backup_${backupId}.zip`);
    } catch (error) {
      throw new Error(`فشل في التحميل: ${error.message}`);
    }
  },

  /**
   * حذف نسخة احتياطية
   */
  async delete(backupId) {
    try {
      const response = await apiClient.delete(`/api/backups/${backupId}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في الحذف: ${error.message}`);
    }
  },

  /**
   * التحقق من صحة النسخة
   */
  async verify(backupId) {
    try {
      const response = await apiClient.post(`/api/backups/${backupId}/verify`);
      return response;
    } catch (error) {
      throw new Error(`فشل في التحقق: ${error.message}`);
    }
  },

  // ==================== الجدولة ====================

  /**
   * الحصول على جدول النسخ الاحتياطي
   */
  async getSchedule() {
    try {
      const response = await apiClient.get('/api/backups/schedule');
      return response.schedule || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الجدول: ${error.message}`);
    }
  },

  /**
   * تحديث جدول النسخ الاحتياطي
   */
  async updateSchedule(scheduleData) {
    try {
      const response = await apiClient.put('/api/backups/schedule', scheduleData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث الجدول: ${error.message}`);
    }
  },

  /**
   * تفعيل/إلغاء تفعيل الجدولة
   */
  async toggleSchedule(enabled) {
    try {
      const response = await apiClient.post('/api/backups/schedule/toggle', { enabled });
      return response;
    } catch (error) {
      throw new Error(`فشل في تبديل حالة الجدولة: ${error.message}`);
    }
  },

  // ==================== التخزين السحابي ====================

  /**
   * رفع نسخة إلى السحابة
   */
  async uploadToCloud(backupId, provider) {
    try {
      const response = await apiClient.post(`/api/backups/${backupId}/upload-cloud`, { provider });
      return response;
    } catch (error) {
      throw new Error(`فشل في الرفع إلى السحابة: ${error.message}`);
    }
  },

  /**
   * تحميل من السحابة
   */
  async downloadFromCloud(cloudBackupId) {
    try {
      const response = await apiClient.post('/api/backups/download-cloud', { cloud_backup_id: cloudBackupId });
      return response;
    } catch (error) {
      throw new Error(`فشل في التحميل من السحابة: ${error.message}`);
    }
  },

  /**
   * الحصول على النسخ السحابية
   */
  async getCloudBackups() {
    try {
      const response = await apiClient.get('/api/backups/cloud');
      return response.backups || [];
    } catch (error) {
      throw new Error(`فشل في تحميل النسخ السحابية: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات النسخ الاحتياطي
   */
  async getStats() {
    try {
      const response = await apiClient.get('/api/backups/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * مساحة التخزين المستخدمة
   */
  async getStorageUsage() {
    try {
      const response = await apiClient.get('/api/backups/storage-usage');
      return response.usage || {};
    } catch (error) {
      throw new Error(`فشل في تحميل معلومات التخزين: ${error.message}`);
    }
  },

  // ==================== التنظيف ====================

  /**
   * تنظيف النسخ القديمة
   */
  async cleanOldBackups(daysToKeep = 30) {
    try {
      const response = await apiClient.post('/api/backups/clean', { days_to_keep: daysToKeep });
      return response;
    } catch (error) {
      throw new Error(`فشل في التنظيف: ${error.message}`);
    }
  }
};

export default backupService;
