/**
 * خدمة إدارة مهندسي المبيعات (Sales Engineer Service)
 * @file frontend/src/services/salesEngineerService.js
 */

import apiClient from './apiClient';

export const salesEngineerService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع مهندسي المبيعات
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        is_active: params.isActive !== undefined ? params.isActive : '',
        region_id: params.regionId || '',
        ...params
      };

      const response = await apiClient.get('/api/sales-engineers', queryParams);
      return {
        engineers: response.engineers || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل مهندسي المبيعات: ${error.message}`);
    }
  },

  /**
   * الحصول على مهندس مبيعات بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}`);
      return response.engineer || response;
    } catch (error) {
      throw new Error(`فشل في تحميل مهندس المبيعات: ${error.message}`);
    }
  },

  /**
   * إنشاء مهندس مبيعات جديد
   */
  async create(engineerData) {
    try {
      const response = await apiClient.post('/api/sales-engineers', engineerData);
      return response.engineer || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء مهندس المبيعات: ${error.message}`);
    }
  },

  /**
   * تحديث مهندس مبيعات
   */
  async update(id, engineerData) {
    try {
      const response = await apiClient.put(`/api/sales-engineers/${id}`, engineerData);
      return response.engineer || response;
    } catch (error) {
      throw new Error(`فشل في تحديث مهندس المبيعات: ${error.message}`);
    }
  },

  /**
   * حذف مهندس مبيعات
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/sales-engineers/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف مهندس المبيعات: ${error.message}`);
    }
  },

  // ==================== إدارة العملاء ====================

  /**
   * الحصول على عملاء المهندس
   */
  async getCustomers(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/customers`, params);
      return response.customers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل العملاء: ${error.message}`);
    }
  },

  /**
   * تعيين عميل للمهندس
   */
  async assignCustomer(id, customerId) {
    try {
      const response = await apiClient.post(`/api/sales-engineers/${id}/assign-customer`, { customer_id: customerId });
      return response;
    } catch (error) {
      throw new Error(`فشل في تعيين العميل: ${error.message}`);
    }
  },

  /**
   * إلغاء تعيين عميل
   */
  async unassignCustomer(id, customerId) {
    try {
      const response = await apiClient.post(`/api/sales-engineers/${id}/unassign-customer`, { customer_id: customerId });
      return response;
    } catch (error) {
      throw new Error(`فشل في إلغاء تعيين العميل: ${error.message}`);
    }
  },

  // ==================== المبيعات ====================

  /**
   * الحصول على مبيعات المهندس
   */
  async getSales(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/sales`, params);
      return response.sales || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المبيعات: ${error.message}`);
    }
  },

  /**
   * ملخص مبيعات المهندس
   */
  async getSalesSummary(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/sales-summary`, params);
      return response.summary || {};
    } catch (error) {
      throw new Error(`فشل في تحميل ملخص المبيعات: ${error.message}`);
    }
  },

  // ==================== الأهداف والعمولات ====================

  /**
   * الحصول على أهداف المهندس
   */
  async getTargets(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/targets`, params);
      return response.targets || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الأهداف: ${error.message}`);
    }
  },

  /**
   * تعيين هدف للمهندس
   */
  async setTarget(id, targetData) {
    try {
      const response = await apiClient.post(`/api/sales-engineers/${id}/targets`, targetData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تعيين الهدف: ${error.message}`);
    }
  },

  /**
   * الحصول على العمولات
   */
  async getCommissions(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/commissions`, params);
      return response.commissions || [];
    } catch (error) {
      throw new Error(`فشل في تحميل العمولات: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير أداء المهندس
   */
  async getPerformanceReport(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/performance`, params);
      return response.report || {};
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير الأداء: ${error.message}`);
    }
  },

  /**
   * تقرير مقارنة الأداء
   */
  async getComparisonReport(params = {}) {
    try {
      const response = await apiClient.get('/api/sales-engineers/reports/comparison', params);
      return response.report || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير المقارنة: ${error.message}`);
    }
  },

  /**
   * تصنيف المهندسين
   */
  async getRanking(params = {}) {
    try {
      const response = await apiClient.get('/api/sales-engineers/ranking', params);
      return response.ranking || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التصنيف: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات المهندس
   */
  async getStats(id) {
    try {
      const response = await apiClient.get(`/api/sales-engineers/${id}/stats`);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * إحصائيات عامة
   */
  async getGeneralStats() {
    try {
      const response = await apiClient.get('/api/sales-engineers/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات العامة: ${error.message}`);
    }
  },

  // ==================== التصدير ====================

  /**
   * تصدير إلى Excel
   */
  async exportToExcel(params = {}) {
    try {
      await apiClient.downloadFile('/api/sales-engineers/export/excel', 'sales_engineers.xlsx');
    } catch (error) {
      throw new Error(`فشل في التصدير: ${error.message}`);
    }
  }
};

export default salesEngineerService;
