/**
 * خدمة إدارة المستودعات (Warehouse Management Service)
 * @file frontend/src/services/warehouseService.js
 */

import apiClient from './apiClient';

const warehouseService = {
  // ==================== CRUD Operations ====================

  /**
   * الحصول على جميع المستودعات
   * @param {Object} params - معلمات الترشيح
   */
  async getWarehouses(params = {}) {
    return apiClient.get('/api/warehouses', params);
  },

  /**
   * الحصول على مستودع بواسطة ID
   * @param {number} id - معرف المستودع
   */
  async getWarehouseById(id) {
    return apiClient.get(`/api/warehouses/${id}`);
  },

  /**
   * إنشاء مستودع جديد
   * @param {Object} data - بيانات المستودع
   */
  async createWarehouse(data) {
    return apiClient.post('/api/warehouses', data);
  },

  /**
   * تحديث مستودع
   * @param {number} id - معرف المستودع
   * @param {Object} data - البيانات المحدثة
   */
  async updateWarehouse(id, data) {
    return apiClient.put(`/api/warehouses/${id}`, data);
  },

  /**
   * حذف مستودع
   * @param {number} id - معرف المستودع
   */
  async deleteWarehouse(id) {
    return apiClient.delete(`/api/warehouses/${id}`);
  },

  // ==================== Status Operations ====================

  /**
   * تفعيل/إلغاء تفعيل مستودع
   * @param {number} id - معرف المستودع
   * @param {boolean} isActive - حالة التفعيل
   */
  async toggleWarehouseActive(id, isActive) {
    return apiClient.patch(`/api/warehouses/${id}/active`, { is_active: isActive });
  },

  /**
   * تعيين مستودع كافتراضي
   * @param {number} id - معرف المستودع
   */
  async setDefaultWarehouse(id) {
    return apiClient.post(`/api/warehouses/${id}/set-default`);
  },

  // ==================== Stock Operations ====================

  /**
   * الحصول على مخزون المستودع
   * @param {number} warehouseId - معرف المستودع
   * @param {Object} params - معلمات الترشيح
   */
  async getWarehouseStock(warehouseId, params = {}) {
    return apiClient.get(`/api/warehouses/${warehouseId}/stock`, params);
  },

  /**
   * الحصول على مخزون منتج في جميع المستودعات
   * @param {number} productId - معرف المنتج
   */
  async getProductStockAcrossWarehouses(productId) {
    return apiClient.get(`/api/products/${productId}/warehouses-stock`);
  },

  /**
   * الحصول على المنتجات ذات المخزون المنخفض في مستودع
   * @param {number} warehouseId - معرف المستودع
   */
  async getLowStockProducts(warehouseId) {
    return apiClient.get(`/api/warehouses/${warehouseId}/low-stock`);
  },

  // ==================== Transfer Operations ====================

  /**
   * إنشاء تحويل مخزون
   * @param {Object} data - بيانات التحويل
   */
  async createTransfer(data) {
    return apiClient.post('/api/warehouse-transfers', data);
  },

  /**
   * الحصول على تحويلات المخزون
   * @param {Object} params - معلمات الترشيح
   */
  async getTransfers(params = {}) {
    return apiClient.get('/api/warehouse-transfers', params);
  },

  /**
   * الحصول على تحويل بواسطة ID
   * @param {number} id - معرف التحويل
   */
  async getTransferById(id) {
    return apiClient.get(`/api/warehouse-transfers/${id}`);
  },

  /**
   * تأكيد تحويل مخزون
   * @param {number} id - معرف التحويل
   */
  async confirmTransfer(id) {
    return apiClient.post(`/api/warehouse-transfers/${id}/confirm`);
  },

  /**
   * إلغاء تحويل مخزون
   * @param {number} id - معرف التحويل
   * @param {string} reason - سبب الإلغاء
   */
  async cancelTransfer(id, reason) {
    return apiClient.post(`/api/warehouse-transfers/${id}/cancel`, { reason });
  },

  // ==================== Adjustment Operations ====================

  /**
   * إنشاء تسوية مخزون
   * @param {Object} data - بيانات التسوية
   */
  async createAdjustment(data) {
    return apiClient.post('/api/warehouse-adjustments', data);
  },

  /**
   * الحصول على تسويات المخزون
   * @param {Object} params - معلمات الترشيح
   */
  async getAdjustments(params = {}) {
    return apiClient.get('/api/warehouse-adjustments', params);
  },

  /**
   * الحصول على تسوية بواسطة ID
   * @param {number} id - معرف التسوية
   */
  async getAdjustmentById(id) {
    return apiClient.get(`/api/warehouse-adjustments/${id}`);
  },

  // ==================== Constraints ====================

  /**
   * الحصول على قيود المستودع
   * @param {number} warehouseId - معرف المستودع
   */
  async getWarehouseConstraints(warehouseId) {
    return apiClient.get(`/api/warehouses/${warehouseId}/constraints`);
  },

  /**
   * تحديث قيود المستودع
   * @param {number} warehouseId - معرف المستودع
   * @param {Object} constraints - القيود
   */
  async updateWarehouseConstraints(warehouseId, constraints) {
    return apiClient.put(`/api/warehouses/${warehouseId}/constraints`, constraints);
  },

  // ==================== Reports ====================

  /**
   * تقرير مخزون المستودعات
   */
  async getWarehouseStockReport() {
    return apiClient.get('/api/reports/warehouse-stock');
  },

  /**
   * تقرير حركات المستودع
   * @param {number} warehouseId - معرف المستودع
   * @param {Object} params - معلمات الفترة
   */
  async getWarehouseMovementsReport(warehouseId, params = {}) {
    return apiClient.get(`/api/warehouses/${warehouseId}/movements-report`, params);
  },

  /**
   * تقرير التحويلات
   * @param {Object} params - معلمات الترشيح
   */
  async getTransfersReport(params = {}) {
    return apiClient.get('/api/reports/warehouse-transfers', params);
  },

  // ==================== Export ====================

  /**
   * تصدير مخزون المستودع إلى Excel
   * @param {number} warehouseId - معرف المستودع
   */
  async exportStockToExcel(warehouseId) {
    return apiClient.downloadFile(
      `/api/warehouses/${warehouseId}/stock/export/excel`,
      `warehouse_${warehouseId}_stock.xlsx`
    );
  },

  /**
   * تصدير التحويلات إلى Excel
   * @param {Object} filters - معلمات الترشيح
   */
  async exportTransfersToExcel(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    const endpoint = queryString 
      ? `/api/warehouse-transfers/export/excel?${queryString}` 
      : '/api/warehouse-transfers/export/excel';
    return apiClient.downloadFile(endpoint, 'warehouse_transfers.xlsx');
  }
};

export default warehouseService;
