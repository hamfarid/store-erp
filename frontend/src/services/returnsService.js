/**
 * خدمة إدارة المرتجعات (Returns Service)
 * @file frontend/src/services/returnsService.js
 */

import apiClient from './apiClient';

export const returnsService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع المرتجعات
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        return_type: params.returnType || '',
        status: params.status || '',
        customer_id: params.customerId || '',
        supplier_id: params.supplierId || '',
        start_date: params.startDate || '',
        end_date: params.endDate || '',
        ...params
      };

      const response = await apiClient.get('/api/returns', queryParams);
      return {
        returns: response.returns || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل المرتجعات: ${error.message}`);
    }
  },

  /**
   * الحصول على مرتجع بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/returns/${id}`);
      return response.return || response;
    } catch (error) {
      throw new Error(`فشل في تحميل المرتجع: ${error.message}`);
    }
  },

  // ==================== مرتجعات المبيعات ====================

  /**
   * إنشاء مرتجع مبيعات
   */
  async createSalesReturn(data) {
    try {
      const response = await apiClient.post('/api/returns/sales', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مرتجع المبيعات: ${error.message}`);
    }
  },

  /**
   * الحصول على مرتجعات المبيعات
   */
  async getSalesReturns(params = {}) {
    try {
      const response = await apiClient.get('/api/returns/sales', params);
      return response.returns || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل مرتجعات المبيعات: ${error.message}`);
    }
  },

  // ==================== مرتجعات المشتريات ====================

  /**
   * إنشاء مرتجع مشتريات
   */
  async createPurchaseReturn(data) {
    try {
      const response = await apiClient.post('/api/returns/purchases', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مرتجع المشتريات: ${error.message}`);
    }
  },

  /**
   * الحصول على مرتجعات المشتريات
   */
  async getPurchaseReturns(params = {}) {
    try {
      const response = await apiClient.get('/api/returns/purchases', params);
      return response.returns || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل مرتجعات المشتريات: ${error.message}`);
    }
  },

  // ==================== حالة المرتجع ====================

  /**
   * تحديث حالة المرتجع
   */
  async updateStatus(id, status) {
    try {
      const response = await apiClient.patch(`/api/returns/${id}/status`, { status });
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث الحالة: ${error.message}`);
    }
  },

  /**
   * الموافقة على المرتجع
   */
  async approve(id) {
    try {
      const response = await apiClient.post(`/api/returns/${id}/approve`);
      return response;
    } catch (error) {
      throw new Error(`فشل في الموافقة: ${error.message}`);
    }
  },

  /**
   * رفض المرتجع
   */
  async reject(id, reason) {
    try {
      const response = await apiClient.post(`/api/returns/${id}/reject`, { reason });
      return response;
    } catch (error) {
      throw new Error(`فشل في الرفض: ${error.message}`);
    }
  },

  /**
   * إتمام المرتجع
   */
  async complete(id) {
    try {
      const response = await apiClient.post(`/api/returns/${id}/complete`);
      return response;
    } catch (error) {
      throw new Error(`فشل في الإتمام: ${error.message}`);
    }
  },

  // ==================== استرداد المبالغ ====================

  /**
   * معالجة استرداد المبلغ
   */
  async processRefund(id, refundData) {
    try {
      const response = await apiClient.post(`/api/returns/${id}/refund`, refundData);
      return response;
    } catch (error) {
      throw new Error(`فشل في معالجة الاسترداد: ${error.message}`);
    }
  },

  /**
   * الحصول على حالة الاسترداد
   */
  async getRefundStatus(id) {
    try {
      const response = await apiClient.get(`/api/returns/${id}/refund-status`);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحميل حالة الاسترداد: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير المرتجعات
   */
  async getReturnsReport(params = {}) {
    try {
      const response = await apiClient.get('/api/returns/reports/summary', params);
      return response.report || {};
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * تقرير أسباب المرتجعات
   */
  async getReasonsReport(params = {}) {
    try {
      const response = await apiClient.get('/api/returns/reports/reasons', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات المرتجعات
   */
  async getStats(params = {}) {
    try {
      const response = await apiClient.get('/api/returns/stats', params);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير المرتجعات إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/returns/export/excel', 'returns.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  /**
   * طباعة إيصال المرتجع
   */
  async printReceipt(id) {
    try {
      const response = await apiClient.get(`/api/returns/${id}/print`);
      return response;
    } catch (error) {
      throw new Error(`فشل في الطباعة: ${error.message}`);
    }
  }
};

export default returnsService;
