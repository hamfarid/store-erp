/**
 * خدمة إدارة الموردين (Supplier Service)
 * @file frontend/src/services/supplierService.js
 */

import apiClient from './apiClient';

export const supplierService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع الموردين
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        search: params.search || '',
        is_active: params.isActive !== undefined ? params.isActive : '',
        sort_by: params.sortBy || 'name',
        sort_order: params.sortOrder || 'asc',
        ...params
      };

      const response = await apiClient.get('/api/suppliers', queryParams);
      return {
        suppliers: response.suppliers || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل الموردين: ${error.message}`);
    }
  },

  /**
   * الحصول على مورد بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}`);
      return response.supplier || response;
    } catch (error) {
      throw new Error(`فشل في تحميل المورد: ${error.message}`);
    }
  },

  /**
   * إنشاء مورد جديد
   */
  async create(supplierData) {
    try {
      const response = await apiClient.post('/api/suppliers', supplierData);
      return response.supplier || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء المورد: ${error.message}`);
    }
  },

  /**
   * تحديث مورد
   */
  async update(id, supplierData) {
    try {
      const response = await apiClient.put(`/api/suppliers/${id}`, supplierData);
      return response.supplier || response;
    } catch (error) {
      throw new Error(`فشل في تحديث المورد: ${error.message}`);
    }
  },

  /**
   * حذف مورد
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/suppliers/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف المورد: ${error.message}`);
    }
  },

  // ==================== العمليات المتقدمة ====================

  /**
   * البحث في الموردين
   */
  async search(query, filters = {}) {
    try {
      const params = {
        q: query,
        city: filters.city,
        is_active: filters.isActive,
        ...filters
      };

      const response = await apiClient.get('/api/suppliers/search', params);
      return response.suppliers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في البحث: ${error.message}`);
    }
  },

  // ==================== إدارة الفواتير ====================

  /**
   * الحصول على فواتير المورد
   */
  async getInvoices(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/invoices`, params);
      return response.invoices || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل فواتير المورد: ${error.message}`);
    }
  },

  /**
   * الحصول على كشف حساب المورد
   */
  async getAccountStatement(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/account-statement`, params);
      return response.statement || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل كشف الحساب: ${error.message}`);
    }
  },

  /**
   * الحصول على رصيد المورد
   */
  async getBalance(id) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/balance`);
      return response.balance || 0;
    } catch (error) {
      throw new Error(`فشل في تحميل رصيد المورد: ${error.message}`);
    }
  },

  // ==================== إدارة المدفوعات ====================

  /**
   * تسجيل دفعة للمورد
   */
  async addPayment(id, paymentData) {
    try {
      const response = await apiClient.post(`/api/suppliers/${id}/payments`, paymentData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تسجيل الدفعة: ${error.message}`);
    }
  },

  /**
   * الحصول على تاريخ المدفوعات
   */
  async getPaymentHistory(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/payments`, params);
      return response.payments || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تاريخ المدفوعات: ${error.message}`);
    }
  },

  // ==================== أوامر الشراء ====================

  /**
   * الحصول على أوامر الشراء من المورد
   */
  async getPurchaseOrders(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/purchase-orders`, params);
      return response.orders || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أوامر الشراء: ${error.message}`);
    }
  },

  /**
   * إنشاء أمر شراء جديد
   */
  async createPurchaseOrder(id, orderData) {
    try {
      const response = await apiClient.post(`/api/suppliers/${id}/purchase-orders`, orderData);
      return response;
    } catch (error) {
      throw new Error(`فشل في إنشاء أمر الشراء: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير أفضل الموردين
   */
  async getTopSuppliers(params = {}) {
    try {
      const response = await apiClient.get('/api/suppliers/reports/top-suppliers', params);
      return response.suppliers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أفضل الموردين: ${error.message}`);
    }
  },

  /**
   * تقرير أعمار الذمم
   */
  async getAgingReport(params = {}) {
    try {
      const response = await apiClient.get('/api/suppliers/reports/aging', params);
      return response.aging || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير أعمار الذمم: ${error.message}`);
    }
  },

  // ==================== الاستيراد والتصدير ====================

  /**
   * تصدير الموردين إلى Excel
   */
  async exportToExcel(_params = {}) {
    try {
      await apiClient.downloadFile('/api/suppliers/export/excel', 'suppliers.xlsx');
    } catch (error) {
      throw new Error(`فشل في تصدير الموردين: ${error.message}`);
    }
  },

  /**
   * استيراد الموردين من Excel
   */
  async importFromExcel(file) {
    try {
      const response = await apiClient.uploadFile('/api/suppliers/import/excel', file);
      return response;
    } catch (error) {
      throw new Error(`فشل في استيراد الموردين: ${error.message}`);
    }
  },

  // ==================== العمليات المجمعة ====================

  /**
   * تحديث عدة موردين
   */
  async bulkUpdate(updates) {
    try {
      const response = await apiClient.post('/api/suppliers/bulk-update', { updates });
      return response;
    } catch (error) {
      throw new Error(`فشل في التحديث المجمع: ${error.message}`);
    }
  },

  /**
   * حذف عدة موردين
   */
  async bulkDelete(ids) {
    try {
      const response = await apiClient.post('/api/suppliers/bulk-delete', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في الحذف المجمع: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * الحصول على إحصائيات المورد
   */
  async getSupplierStats(id) {
    try {
      const response = await apiClient.get(`/api/suppliers/${id}/stats`);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل إحصائيات المورد: ${error.message}`);
    }
  },

  /**
   * الحصول على إحصائيات عامة للموردين
   */
  async getGeneralStats() {
    try {
      const response = await apiClient.get('/api/suppliers/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات العامة: ${error.message}`);
    }
  }
};

export default supplierService;
