/**
 * خدمة الإعدادات (Settings Service)
 * @file frontend/src/services/settingsService.js
 */

import apiClient from './apiClient';

const settingsService = {
  // ==================== General Settings ====================

  /**
   * الحصول على جميع الإعدادات
   */
  async getAllSettings() {
    return apiClient.get('/api/settings');
  },

  /**
   * الحصول على إعداد محدد
   * @param {string} key - مفتاح الإعداد
   */
  async getSetting(key) {
    return apiClient.get(`/api/settings/${key}`);
  },

  /**
   * تحديث إعداد
   * @param {string} key - مفتاح الإعداد
   * @param {any} value - القيمة الجديدة
   */
  async updateSetting(key, value) {
    return apiClient.put(`/api/settings/${key}`, { value });
  },

  /**
   * تحديث إعدادات متعددة
   * @param {Object} settings - كائن الإعدادات
   */
  async updateMultipleSettings(settings) {
    return apiClient.put('/api/settings/bulk', { settings });
  },

  // ==================== Company Settings ====================

  /**
   * الحصول على إعدادات الشركة
   */
  async getCompanySettings() {
    return apiClient.get('/api/settings/company');
  },

  /**
   * تحديث إعدادات الشركة
   * @param {Object} data - بيانات الشركة
   */
  async updateCompanySettings(data) {
    return apiClient.put('/api/settings/company', data);
  },

  /**
   * رفع شعار الشركة
   * @param {File} file - ملف الشعار
   */
  async uploadCompanyLogo(file) {
    return apiClient.uploadFile('/api/settings/company/logo', file);
  },

  // ==================== Tax Settings ====================

  /**
   * الحصول على إعدادات الضرائب
   */
  async getTaxSettings() {
    return apiClient.get('/api/settings/tax');
  },

  /**
   * تحديث إعدادات الضرائب
   * @param {Object} data - بيانات الضرائب
   */
  async updateTaxSettings(data) {
    return apiClient.put('/api/settings/tax', data);
  },

  /**
   * الحصول على أنواع الضرائب
   */
  async getTaxTypes() {
    return apiClient.get('/api/settings/tax/types');
  },

  /**
   * إضافة نوع ضريبة
   * @param {Object} data - بيانات نوع الضريبة
   */
  async addTaxType(data) {
    return apiClient.post('/api/settings/tax/types', data);
  },

  /**
   * تحديث نوع ضريبة
   * @param {number} id - معرف نوع الضريبة
   * @param {Object} data - البيانات المحدثة
   */
  async updateTaxType(id, data) {
    return apiClient.put(`/api/settings/tax/types/${id}`, data);
  },

  /**
   * حذف نوع ضريبة
   * @param {number} id - معرف نوع الضريبة
   */
  async deleteTaxType(id) {
    return apiClient.delete(`/api/settings/tax/types/${id}`);
  },

  // ==================== ZATCA Settings ====================

  /**
   * الحصول على إعدادات الزاتكا
   */
  async getZatcaSettings() {
    return apiClient.get('/api/settings/zatca');
  },

  /**
   * تحديث إعدادات الزاتكا
   * @param {Object} data - بيانات الزاتكا
   */
  async updateZatcaSettings(data) {
    return apiClient.put('/api/settings/zatca', data);
  },

  /**
   * اختبار اتصال الزاتكا
   */
  async testZatcaConnection() {
    return apiClient.post('/api/settings/zatca/test');
  },

  // ==================== Notification Settings ====================

  /**
   * الحصول على إعدادات الإشعارات
   */
  async getNotificationSettings() {
    return apiClient.get('/api/settings/notifications');
  },

  /**
   * تحديث إعدادات الإشعارات
   * @param {Object} data - بيانات الإشعارات
   */
  async updateNotificationSettings(data) {
    return apiClient.put('/api/settings/notifications', data);
  },

  // ==================== Email Settings ====================

  /**
   * الحصول على إعدادات البريد الإلكتروني
   */
  async getEmailSettings() {
    return apiClient.get('/api/settings/email');
  },

  /**
   * تحديث إعدادات البريد الإلكتروني
   * @param {Object} data - بيانات البريد
   */
  async updateEmailSettings(data) {
    return apiClient.put('/api/settings/email', data);
  },

  /**
   * اختبار إعدادات البريد
   * @param {string} testEmail - بريد الاختبار
   */
  async testEmailSettings(testEmail) {
    return apiClient.post('/api/settings/email/test', { email: testEmail });
  },

  // ==================== Backup Settings ====================

  /**
   * الحصول على إعدادات النسخ الاحتياطي
   */
  async getBackupSettings() {
    return apiClient.get('/api/settings/backup');
  },

  /**
   * تحديث إعدادات النسخ الاحتياطي
   * @param {Object} data - بيانات النسخ الاحتياطي
   */
  async updateBackupSettings(data) {
    return apiClient.put('/api/settings/backup', data);
  },

  /**
   * إنشاء نسخة احتياطية
   */
  async createBackup() {
    return apiClient.post('/api/backup/create');
  },

  /**
   * الحصول على قائمة النسخ الاحتياطية
   */
  async getBackupList() {
    return apiClient.get('/api/backup/list');
  },

  /**
   * استعادة نسخة احتياطية
   * @param {string} backupId - معرف النسخة
   */
  async restoreBackup(backupId) {
    return apiClient.post(`/api/backup/restore/${backupId}`);
  },

  /**
   * حذف نسخة احتياطية
   * @param {string} backupId - معرف النسخة
   */
  async deleteBackup(backupId) {
    return apiClient.delete(`/api/backup/${backupId}`);
  },

  /**
   * تحميل نسخة احتياطية
   * @param {string} backupId - معرف النسخة
   */
  async downloadBackup(backupId) {
    return apiClient.downloadFile(`/api/backup/download/${backupId}`, `backup_${backupId}.zip`);
  },

  // ==================== System Settings ====================

  /**
   * الحصول على إعدادات النظام
   */
  async getSystemSettings() {
    return apiClient.get('/api/settings/system');
  },

  /**
   * تحديث إعدادات النظام
   * @param {Object} data - بيانات النظام
   */
  async updateSystemSettings(data) {
    return apiClient.put('/api/settings/system', data);
  },

  /**
   * الحصول على حالة النظام
   */
  async getSystemStatus() {
    return apiClient.get('/api/system/status');
  },

  /**
   * تنظيف ذاكرة التخزين المؤقت
   */
  async clearCache() {
    return apiClient.post('/api/system/clear-cache');
  },

  // ==================== Currency Settings ====================

  /**
   * الحصول على العملات
   */
  async getCurrencies() {
    return apiClient.get('/api/settings/currencies');
  },

  /**
   * تحديث العملة الافتراضية
   * @param {string} currencyCode - رمز العملة
   */
  async setDefaultCurrency(currencyCode) {
    return apiClient.put('/api/settings/currency/default', { currency: currencyCode });
  },

  // ==================== Print Settings ====================

  /**
   * الحصول على إعدادات الطباعة
   */
  async getPrintSettings() {
    return apiClient.get('/api/settings/print');
  },

  /**
   * تحديث إعدادات الطباعة
   * @param {Object} data - بيانات الطباعة
   */
  async updatePrintSettings(data) {
    return apiClient.put('/api/settings/print', data);
  }
};

export default settingsService;
