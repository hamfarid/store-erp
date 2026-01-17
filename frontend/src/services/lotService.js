/**
 * خدمة إدارة اللوتات (Lot Management Service)
 * @file frontend/src/services/lotService.js
 */

import apiClient from './apiClient';

const lotService = {
  // ==================== CRUD Operations ====================

  /**
   * الحصول على جميع اللوتات
   * @param {Object} params - معلمات الترشيح والترتيب
   */
  async getLots(params = {}) {
    return apiClient.get('/api/lots', params);
  },

  /**
   * الحصول على لوت بواسطة ID
   * @param {number} id - معرف اللوت
   */
  async getLotById(id) {
    return apiClient.get(`/api/lots/${id}`);
  },

  /**
   * إنشاء لوت جديد
   * @param {Object} data - بيانات اللوت
   */
  async createLot(data) {
    return apiClient.post('/api/lots', data);
  },

  /**
   * تحديث لوت
   * @param {number} id - معرف اللوت
   * @param {Object} data - البيانات المحدثة
   */
  async updateLot(id, data) {
    return apiClient.put(`/api/lots/${id}`, data);
  },

  /**
   * حذف لوت
   * @param {number} id - معرف اللوت
   */
  async deleteLot(id) {
    return apiClient.delete(`/api/lots/${id}`);
  },

  // ==================== Status Operations ====================

  /**
   * تحديث حالة اللوت
   * @param {number} id - معرف اللوت
   * @param {string} status - الحالة الجديدة (available, reserved, sold, expired)
   */
  async updateLotStatus(id, status) {
    return apiClient.patch(`/api/lots/${id}/status`, { status });
  },

  /**
   * تفعيل/إلغاء تفعيل لوت
   * @param {number} id - معرف اللوت
   * @param {boolean} isActive - حالة التفعيل
   */
  async toggleLotActive(id, isActive) {
    return apiClient.patch(`/api/lots/${id}/active`, { is_active: isActive });
  },

  // ==================== Query Operations ====================

  /**
   * الحصول على اللوتات حسب المنتج
   * @param {number} productId - معرف المنتج
   */
  async getLotsByProduct(productId) {
    return apiClient.get('/api/lots', { product_id: productId });
  },

  /**
   * الحصول على اللوتات حسب المستودع
   * @param {number} warehouseId - معرف المستودع
   */
  async getLotsByWarehouse(warehouseId) {
    return apiClient.get('/api/lots', { warehouse_id: warehouseId });
  },

  /**
   * الحصول على اللوتات المتاحة (FIFO)
   * @param {number} productId - معرف المنتج
   */
  async getAvailableLots(productId) {
    return apiClient.get(`/api/lots/available/${productId}`);
  },

  /**
   * الحصول على اللوتات قريبة الانتهاء
   * @param {number} days - عدد الأيام
   */
  async getExpiringLots(days = 30) {
    return apiClient.get('/api/lots/expiring', { days });
  },

  /**
   * الحصول على اللوتات منتهية الصلاحية
   */
  async getExpiredLots() {
    return apiClient.get('/api/lots/expired');
  },

  /**
   * الحصول على اللوتات ذات المخزون المنخفض
   */
  async getLowStockLots() {
    return apiClient.get('/api/lots/low-stock');
  },

  // ==================== Reservation Operations ====================

  /**
   * حجز كمية من لوت
   * @param {number} lotId - معرف اللوت
   * @param {number} quantity - الكمية المراد حجزها
   */
  async reserveLotQuantity(lotId, quantity) {
    return apiClient.post(`/api/lots/${lotId}/reserve`, { quantity });
  },

  /**
   * إلغاء حجز كمية من لوت
   * @param {number} lotId - معرف اللوت
   * @param {number} quantity - الكمية المراد إلغاء حجزها
   */
  async releaseLotQuantity(lotId, quantity) {
    return apiClient.post(`/api/lots/${lotId}/release`, { quantity });
  },

  // ==================== Quality Operations ====================

  /**
   * تحديث بيانات الجودة
   * @param {number} lotId - معرف اللوت
   * @param {Object} qualityData - بيانات الجودة
   */
  async updateQualityData(lotId, qualityData) {
    return apiClient.patch(`/api/lots/${lotId}/quality`, qualityData);
  },

  // ==================== Reports ====================

  /**
   * تقرير اللوتات حسب الحالة
   */
  async getLotStatusReport() {
    return apiClient.get('/api/reports/lot-status');
  },

  /**
   * تقرير انتهاء الصلاحية
   * @param {number} days - عدد الأيام القادمة
   */
  async getExpiryReport(days = 30) {
    return apiClient.get('/api/reports/lot-expiry', { days });
  },

  // ==================== Export ====================

  /**
   * تصدير اللوتات إلى Excel
   * @param {Object} filters - معلمات الترشيح
   */
  async exportToExcel(filters = {}) {
    return apiClient.downloadFile('/api/lots/export/excel', 'lots_export.xlsx');
  },

  /**
   * تصدير اللوتات إلى CSV
   * @param {Object} filters - معلمات الترشيح
   */
  async exportToCSV(filters = {}) {
    return apiClient.downloadFile('/api/lots/export/csv', 'lots_export.csv');
  }
};

export default lotService;
