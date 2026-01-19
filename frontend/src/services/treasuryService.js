/**
 * خدمة إدارة الخزينة (Treasury Service)
 * @file frontend/src/services/treasuryService.js
 */

import apiClient from './apiClient';

export const treasuryService = {
  // ==================== إدارة الصناديق ====================

  /**
   * الحصول على جميع الصناديق
   */
  async getCashBoxes(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/cash-boxes', params);
      return response.cashBoxes || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الصناديق: ${error.message}`);
    }
  },

  /**
   * الحصول على صندوق بالمعرف
   */
  async getCashBoxById(id) {
    try {
      const response = await apiClient.get(`/api/treasury/cash-boxes/${id}`);
      return response.cashBox || response;
    } catch (error) {
      throw new Error(`فشل في تحميل الصندوق: ${error.message}`);
    }
  },

  /**
   * إنشاء صندوق جديد
   */
  async createCashBox(data) {
    try {
      const response = await apiClient.post('/api/treasury/cash-boxes', data);
      return response.cashBox || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء الصندوق: ${error.message}`);
    }
  },

  /**
   * تحديث صندوق
   */
  async updateCashBox(id, data) {
    try {
      const response = await apiClient.put(`/api/treasury/cash-boxes/${id}`, data);
      return response.cashBox || response;
    } catch (error) {
      throw new Error(`فشل في تحديث الصندوق: ${error.message}`);
    }
  },

  /**
   * حذف صندوق
   */
  async deleteCashBox(id) {
    try {
      const response = await apiClient.delete(`/api/treasury/cash-boxes/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف الصندوق: ${error.message}`);
    }
  },

  // ==================== العمليات المالية ====================

  /**
   * إيداع في الصندوق
   */
  async deposit(cashBoxId, data) {
    try {
      const response = await apiClient.post(`/api/treasury/cash-boxes/${cashBoxId}/deposit`, data);
      return response;
    } catch (error) {
      throw new Error(`فشل في الإيداع: ${error.message}`);
    }
  },

  /**
   * سحب من الصندوق
   */
  async withdraw(cashBoxId, data) {
    try {
      const response = await apiClient.post(`/api/treasury/cash-boxes/${cashBoxId}/withdraw`, data);
      return response;
    } catch (error) {
      throw new Error(`فشل في السحب: ${error.message}`);
    }
  },

  /**
   * تحويل بين الصناديق
   */
  async transfer(data) {
    try {
      const response = await apiClient.post('/api/treasury/transfer', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في التحويل: ${error.message}`);
    }
  },

  // ==================== سندات القبض والصرف ====================

  /**
   * الحصول على جميع السندات
   */
  async getVouchers(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/vouchers', params);
      return {
        vouchers: response.vouchers || response.data || [],
        total: response.total || 0,
        page: response.page || 1
      };
    } catch (error) {
      throw new Error(`فشل في تحميل السندات: ${error.message}`);
    }
  },

  /**
   * إنشاء سند قبض
   */
  async createReceiptVoucher(data) {
    try {
      const response = await apiClient.post('/api/treasury/vouchers/receipt', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء سند القبض: ${error.message}`);
    }
  },

  /**
   * إنشاء سند صرف
   */
  async createPaymentVoucher(data) {
    try {
      const response = await apiClient.post('/api/treasury/vouchers/payment', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء سند الصرف: ${error.message}`);
    }
  },

  /**
   * الحصول على سند بالمعرف
   */
  async getVoucherById(id) {
    try {
      const response = await apiClient.get(`/api/treasury/vouchers/${id}`);
      return response.voucher || response;
    } catch (error) {
      throw new Error(`فشل في تحميل السند: ${error.message}`);
    }
  },

  /**
   * إلغاء سند
   */
  async cancelVoucher(id, reason) {
    try {
      const response = await apiClient.post(`/api/treasury/vouchers/${id}/cancel`, { reason });
      return response;
    } catch (error) {
      throw new Error(`فشل في إلغاء السند: ${error.message}`);
    }
  },

  // ==================== الأرصدة الافتتاحية ====================

  /**
   * الحصول على الأرصدة الافتتاحية
   */
  async getOpeningBalances(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/opening-balances', params);
      return response.balances || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الأرصدة الافتتاحية: ${error.message}`);
    }
  },

  /**
   * تعيين رصيد افتتاحي
   */
  async setOpeningBalance(data) {
    try {
      const response = await apiClient.post('/api/treasury/opening-balances', data);
      return response;
    } catch (error) {
      throw new Error(`فشل في تعيين الرصيد الافتتاحي: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير حركات الصندوق
   */
  async getCashBoxMovements(cashBoxId, params = {}) {
    try {
      const response = await apiClient.get(`/api/treasury/cash-boxes/${cashBoxId}/movements`, params);
      return response.movements || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل حركات الصندوق: ${error.message}`);
    }
  },

  /**
   * تقرير ملخص الخزينة
   */
  async getTreasurySummary(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/summary', params);
      return response.summary || response;
    } catch (error) {
      throw new Error(`فشل في تحميل ملخص الخزينة: ${error.message}`);
    }
  },

  /**
   * تقرير التدفق النقدي
   */
  async getCashFlowReport(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/reports/cash-flow', params);
      return response.cashFlow || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير التدفق النقدي: ${error.message}`);
    }
  },

  /**
   * تقرير الإيرادات والمصروفات
   */
  async getIncomeExpenseReport(params = {}) {
    try {
      const response = await apiClient.get('/api/treasury/reports/income-expense', params);
      return response.report || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير الإيرادات والمصروفات: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات الخزينة
   */
  async getStats() {
    try {
      const response = await apiClient.get('/api/treasury/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * إجمالي الأرصدة
   */
  async getTotalBalance() {
    try {
      const response = await apiClient.get('/api/treasury/total-balance');
      return response.totalBalance || 0;
    } catch (error) {
      throw new Error(`فشل في تحميل إجمالي الأرصدة: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير حركات الخزينة إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/treasury/export/excel', 'treasury_report.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  /**
   * طباعة سند
   */
  async printVoucher(id) {
    try {
      const response = await apiClient.get(`/api/treasury/vouchers/${id}/print`);
      return response;
    } catch (error) {
      throw new Error(`فشل في الطباعة: ${error.message}`);
    }
  }
};

export default treasuryService;
