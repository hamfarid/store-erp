/**
 * خدمة حركات المخزون (Stock Movement Service)
 * @file frontend/src/services/stockMovementService.js
 */

import apiClient from './apiClient';

export const stockMovementService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع حركات المخزون
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        movement_type: params.movementType || '',
        product_id: params.productId || '',
        warehouse_id: params.warehouseId || '',
        start_date: params.startDate || '',
        end_date: params.endDate || '',
        ...params
      };

      const response = await apiClient.get('/api/stock-movements', queryParams);
      return {
        movements: response.movements || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل حركات المخزون: ${error.message}`);
    }
  },

  /**
   * الحصول على حركة بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/stock-movements/${id}`);
      return response.movement || response;
    } catch (error) {
      throw new Error(`فشل في تحميل الحركة: ${error.message}`);
    }
  },

  // ==================== إنشاء الحركات ====================

  /**
   * إنشاء حركة وارد
   */
  async createIncoming(data) {
    try {
      const response = await apiClient.post('/api/stock-movements/incoming', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء حركة الوارد: ${error.message}`);
    }
  },

  /**
   * إنشاء حركة صادر
   */
  async createOutgoing(data) {
    try {
      const response = await apiClient.post('/api/stock-movements/outgoing', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء حركة الصادر: ${error.message}`);
    }
  },

  /**
   * إنشاء تحويل بين المخازن
   */
  async createTransfer(data) {
    try {
      const response = await apiClient.post('/api/stock-movements/transfer', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء التحويل: ${error.message}`);
    }
  },

  /**
   * إنشاء تعديل مخزون
   */
  async createAdjustment(data) {
    try {
      const response = await apiClient.post('/api/stock-movements/adjustment', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء التعديل: ${error.message}`);
    }
  },

  // ==================== حركات المنتج ====================

  /**
   * الحصول على حركات منتج معين
   */
  async getProductMovements(productId, params = {}) {
    try {
      const response = await apiClient.get(`/api/stock-movements/product/${productId}`, params);
      return response.movements || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل حركات المنتج: ${error.message}`);
    }
  },

  /**
   * الحصول على حركات مخزن معين
   */
  async getWarehouseMovements(warehouseId, params = {}) {
    try {
      const response = await apiClient.get(`/api/stock-movements/warehouse/${warehouseId}`, params);
      return response.movements || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل حركات المخزن: ${error.message}`);
    }
  },

  /**
   * الحصول على حركات اللوت
   */
  async getLotMovements(lotId, params = {}) {
    try {
      const response = await apiClient.get(`/api/stock-movements/lot/${lotId}`, params);
      return response.movements || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل حركات اللوت: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير حركات المخزون
   */
  async getMovementsReport(params = {}) {
    try {
      const response = await apiClient.get('/api/stock-movements/reports/movements', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * ملخص الحركات اليومية
   */
  async getDailySummary(params = {}) {
    try {
      const response = await apiClient.get('/api/stock-movements/reports/daily-summary', params);
      return response.summary || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الملخص اليومي: ${error.message}`);
    }
  },

  /**
   * تقرير التحويلات
   */
  async getTransferReport(params = {}) {
    try {
      const response = await apiClient.get('/api/stock-movements/reports/transfers', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير التحويلات: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات حركات المخزون
   */
  async getStats(params = {}) {
    try {
      const response = await apiClient.get('/api/stock-movements/stats', params);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير حركات المخزون إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/stock-movements/export/excel', 'stock_movements.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  /**
   * تصدير إلى PDF
   */
  async exportToPDF(params = {}) {
    try {
      await apiClient.downloadFile('/api/stock-movements/export/pdf', 'stock_movements.pdf');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  }
};

export default stockMovementService;
