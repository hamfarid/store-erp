/**
 * خدمة سجل الأسعار (Price History Service)
 * @file frontend/src/services/priceHistoryService.js
 */

import apiClient from './apiClient';

export const priceHistoryService = {
  // ==================== الحصول على سجل الأسعار ====================

  /**
   * الحصول على سجل أسعار منتج
   */
  async getProductPriceHistory(productId, params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        start_date: params.startDate || '',
        end_date: params.endDate || '',
        ...params
      };

      const response = await apiClient.get(`/api/price-history/product/${productId}`, queryParams);
      return {
        history: response.history || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        product: response.product || null
      };
    } catch (error) {
      throw new Error(`فشل في تحميل سجل الأسعار: ${error.message}`);
    }
  },

  /**
   * الحصول على جميع تغييرات الأسعار
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        start_date: params.startDate || '',
        end_date: params.endDate || '',
        product_id: params.productId || '',
        category_id: params.categoryId || '',
        change_type: params.changeType || '',
        ...params
      };

      const response = await apiClient.get('/api/price-history', queryParams);
      return {
        history: response.history || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50))
      };
    } catch (error) {
      throw new Error(`فشل في تحميل سجل الأسعار: ${error.message}`);
    }
  },

  // ==================== تسجيل تغيير السعر ====================

  /**
   * تسجيل تغيير سعر يدوي
   */
  async recordPriceChange(productId, data) {
    try {
      const response = await apiClient.post(`/api/price-history/product/${productId}`, data);
      return response;
    } catch (error) {
      throw new Error(`فشل في تسجيل تغيير السعر: ${error.message}`);
    }
  },

  /**
   * تحديث سعر المنتج مع التسجيل
   */
  async updatePrice(productId, newPrice, reason = '') {
    try {
      const response = await apiClient.post(`/api/price-history/product/${productId}/update`, {
        new_price: newPrice,
        reason: reason
      });
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث السعر: ${error.message}`);
    }
  },

  // ==================== التحليلات ====================

  /**
   * تحليل تغييرات الأسعار
   */
  async getPriceAnalytics(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/analytics', params);
      return response.analytics || {};
    } catch (error) {
      throw new Error(`فشل في تحميل التحليلات: ${error.message}`);
    }
  },

  /**
   * اتجاه الأسعار لمنتج
   */
  async getPriceTrend(productId, params = {}) {
    try {
      const response = await apiClient.get(`/api/price-history/product/${productId}/trend`, params);
      return response.trend || [];
    } catch (error) {
      throw new Error(`فشل في تحميل اتجاه الأسعار: ${error.message}`);
    }
  },

  /**
   * مقارنة أسعار المنتجات
   */
  async comparePrices(productIds, params = {}) {
    try {
      const response = await apiClient.post('/api/price-history/compare', {
        product_ids: productIds,
        ...params
      });
      return response.comparison || [];
    } catch (error) {
      throw new Error(`فشل في مقارنة الأسعار: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير تغييرات الأسعار
   */
  async getPriceChangesReport(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/reports/changes', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * تقرير تأثير الأسعار على المبيعات
   */
  async getPriceImpactReport(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/reports/impact', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * ملخص تغييرات الأسعار
   */
  async getPriceChangesSummary(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/summary', params);
      return response.summary || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الملخص: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير سجل الأسعار إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/price-history/export/excel', 'price_history.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  /**
   * تصدير سجل أسعار منتج
   */
  async exportProductHistory(productId) {
    try {
      await apiClient.downloadFile(
        `/api/price-history/product/${productId}/export`, 
        `price_history_product_${productId}.xlsx`
      );
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات تغييرات الأسعار
   */
  async getStats(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/stats', params);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * المنتجات الأكثر تغييراً في السعر
   */
  async getMostChangedProducts(params = {}) {
    try {
      const response = await apiClient.get('/api/price-history/most-changed', params);
      return response.products || [];
    } catch (error) {
      throw new Error(`فشل في تحميل البيانات: ${error.message}`);
    }
  }
};

export default priceHistoryService;
