/**
 * خدمة إدارة العملاء
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/services/customerService.js
 */

import apiClient from './apiClient';

export const customerService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع العملاء
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        search: params.search || '',
        customer_type: params.customerType || '',
        sales_engineer_id: params.salesEngineerId || '',
        is_active: params.isActive !== undefined ? params.isActive : '',
        sort_by: params.sortBy || 'name',
        sort_order: params.sortOrder || 'asc',
        ...params
      };

      const response = await apiClient.get('/api/customers', queryParams);
      return {
        customers: response.customers || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل العملاء: ${error.message}`);
    }
  },

  /**
   * الحصول على عميل بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/customers/${id}`);
      return response.customer || response;
    } catch (error) {
      throw new Error(`فشل في تحميل العميل: ${error.message}`);
    }
  },

  /**
   * إنشاء عميل جديد
   */
  async create(customerData) {
    try {
      const response = await apiClient.post('/api/customers', customerData);
      return response.customer || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء العميل: ${error.message}`);
    }
  },

  /**
   * تحديث عميل
   */
  async update(id, customerData) {
    try {
      const response = await apiClient.put(`/api/customers/${id}`, customerData);
      return response.customer || response;
    } catch (error) {
      throw new Error(`فشل في تحديث العميل: ${error.message}`);
    }
  },

  /**
   * حذف عميل
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/customers/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف العميل: ${error.message}`);
    }
  },

  // ==================== العمليات المتقدمة ====================

  /**
   * البحث في العملاء
   */
  async search(query, filters = {}) {
    try {
      const params = {
        q: query,
        customer_type: filters.customerType,
        sales_engineer_id: filters.salesEngineerId,
        city: filters.city,
        is_vip: filters.isVip,
        ...filters
      };

      const response = await apiClient.get('/api/customers/search', params);
      return response.customers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في البحث: ${error.message}`);
    }
  },

  /**
   * الحصول على عملاء مهندس المبيعات
   */
  async getBySalesEngineer(salesEngineerId, params = {}) {
    try {
      const response = await apiClient.get(`/api/customers/sales-engineer/${salesEngineerId}`, params);
      return response.customers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل عملاء مهندس المبيعات: ${error.message}`);
    }
  },

  /**
   * الحصول على العملاء المميزين (VIP)
   */
  async getVipCustomers(params = {}) {
    try {
      const response = await apiClient.get('/api/customers/vip', params);
      return response.customers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل العملاء المميزين: ${error.message}`);
    }
  },

  // ==================== إدارة الفواتير ====================

  /**
   * الحصول على فواتير العميل
   */
  async getInvoices(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/invoices`, params);
      return response.invoices || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل فواتير العميل: ${error.message}`);
    }
  },

  /**
   * الحصول على كشف حساب العميل
   */
  async getAccountStatement(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/account-statement`, params);
      return response.statement || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل كشف الحساب: ${error.message}`);
    }
  },

  /**
   * الحصول على رصيد العميل
   */
  async getBalance(id) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/balance`);
      return response.balance || 0;
    } catch (error) {
      throw new Error(`فشل في تحميل رصيد العميل: ${error.message}`);
    }
  },

  // ==================== إدارة الائتمان ====================

  /**
   * تحديث حد الائتمان
   */
  async updateCreditLimit(id, creditData) {
    try {
      const response = await apiClient.post(`/api/customers/${id}/credit-limit`, creditData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث حد الائتمان: ${error.message}`);
    }
  },

  /**
   * الحصول على تاريخ الائتمان
   */
  async getCreditHistory(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/credit-history`, params);
      return response.history || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تاريخ الائتمان: ${error.message}`);
    }
  },

  /**
   * فحص الائتمان المتاح
   */
  async checkAvailableCredit(id) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/available-credit`);
      return response.available_credit || 0;
    } catch (error) {
      throw new Error(`فشل في فحص الائتمان المتاح: ${error.message}`);
    }
  },

  // ==================== إدارة المدفوعات ====================

  /**
   * تسجيل دفعة جديدة
   */
  async addPayment(id, paymentData) {
    try {
      const response = await apiClient.post(`/api/customers/${id}/payments`, paymentData);
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
      const response = await apiClient.get(`/api/customers/${id}/payments`, params);
      return response.payments || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تاريخ المدفوعات: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير أفضل العملاء
   */
  async getTopCustomers(params = {}) {
    try {
      const response = await apiClient.get('/api/customers/reports/top-customers', params);
      return response.customers || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أفضل العملاء: ${error.message}`);
    }
  },

  /**
   * تقرير أعمار الديون
   */
  async getAgingReport(params = {}) {
    try {
      const response = await apiClient.get('/api/customers/reports/aging', params);
      return response.aging || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير أعمار الديون: ${error.message}`);
    }
  },

  /**
   * تقرير المبيعات حسب العميل
   */
  async getSalesReport(params = {}) {
    try {
      const response = await apiClient.get('/api/customers/reports/sales', params);
      return response.sales || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير المبيعات: ${error.message}`);
    }
  },

  // ==================== الاستيراد والتصدير ====================

  /**
   * تصدير العملاء إلى Excel
   */
  async exportToExcel(_params = {}) {
    try {
      await apiClient.downloadFile('/api/customers/export/excel', 'customers.xlsx');
    } catch (error) {
      throw new Error(`فشل في تصدير العملاء: ${error.message}`);
    }
  },

  /**
   * استيراد العملاء من Excel
   */
  async importFromExcel(file) {
    try {
      const response = await apiClient.uploadFile('/api/customers/import/excel', file);
      return response;
    } catch (error) {
      throw new Error(`فشل في استيراد العملاء: ${error.message}`);
    }
  },

  /**
   * تحميل قالب Excel للاستيراد
   */
  async downloadImportTemplate() {
    try {
      await apiClient.downloadFile('/api/customers/import/template', 'customers_template.xlsx');
    } catch (error) {
      throw new Error(`فشل في تحميل القالب: ${error.message}`);
    }
  },

  // ==================== إدارة جهات الاتصال ====================

  /**
   * إضافة جهة اتصال للعميل
   */
  async addContact(id, contactData) {
    try {
      const response = await apiClient.post(`/api/customers/${id}/contacts`, contactData);
      return response;
    } catch (error) {
      throw new Error(`فشل في إضافة جهة الاتصال: ${error.message}`);
    }
  },

  /**
   * تحديث جهة اتصال
   */
  async updateContact(id, contactId, contactData) {
    try {
      const response = await apiClient.put(`/api/customers/${id}/contacts/${contactId}`, contactData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث جهة الاتصال: ${error.message}`);
    }
  },

  /**
   * حذف جهة اتصال
   */
  async deleteContact(id, contactId) {
    try {
      const response = await apiClient.delete(`/api/customers/${id}/contacts/${contactId}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف جهة الاتصال: ${error.message}`);
    }
  },

  // ==================== إدارة العناوين ====================

  /**
   * إضافة عنوان للعميل
   */
  async addAddress(id, addressData) {
    try {
      const response = await apiClient.post(`/api/customers/${id}/addresses`, addressData);
      return response;
    } catch (error) {
      throw new Error(`فشل في إضافة العنوان: ${error.message}`);
    }
  },

  /**
   * تحديث عنوان
   */
  async updateAddress(id, addressId, addressData) {
    try {
      const response = await apiClient.put(`/api/customers/${id}/addresses/${addressId}`, addressData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث العنوان: ${error.message}`);
    }
  },

  /**
   * حذف عنوان
   */
  async deleteAddress(id, addressId) {
    try {
      const response = await apiClient.delete(`/api/customers/${id}/addresses/${addressId}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف العنوان: ${error.message}`);
    }
  },

  // ==================== العمليات المجمعة ====================

  /**
   * تحديث عدة عملاء
   */
  async bulkUpdate(updates) {
    try {
      const response = await apiClient.post('/api/customers/bulk-update', { updates });
      return response;
    } catch (error) {
      throw new Error(`فشل في التحديث المجمع: ${error.message}`);
    }
  },

  /**
   * حذف عدة عملاء
   */
  async bulkDelete(ids) {
    try {
      const response = await apiClient.post('/api/customers/bulk-delete', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في الحذف المجمع: ${error.message}`);
    }
  },

  /**
   * تعيين مهندس مبيعات لعدة عملاء
   */
  async bulkAssignSalesEngineer(customerIds, salesEngineerId) {
    try {
      const response = await apiClient.post('/api/customers/bulk-assign-sales-engineer', {
        customer_ids: customerIds,
        sales_engineer_id: salesEngineerId
      });
      return response;
    } catch (error) {
      throw new Error(`فشل في تعيين مهندس المبيعات: ${error.message}`);
    }
  },

  // ==================== التحقق من صحة البيانات ====================

  /**
   * التحقق من وجود رقم هاتف
   */
  async checkPhoneExists(phone, excludeId = null) {
    try {
      const params = { phone };
      if (excludeId) params.exclude_id = excludeId;
      
      const response = await apiClient.get('/api/customers/check-phone', params);
      return response.exists || false;
    } catch (error) {
      return false;
    }
  },

  /**
   * التحقق من وجود بريد إلكتروني
   */
  async checkEmailExists(email, excludeId = null) {
    try {
      const params = { email };
      if (excludeId) params.exclude_id = excludeId;
      
      const response = await apiClient.get('/api/customers/check-email', params);
      return response.exists || false;
    } catch (error) {
      return false;
    }
  },

  /**
   * التحقق من صحة بيانات العميل
   */
  async validateCustomer(customerData) {
    try {
      const response = await apiClient.post('/api/customers/validate', customerData);
      return response;
    } catch (error) {
      throw new Error(`فشل في التحقق من البيانات: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * الحصول على إحصائيات العميل
   */
  async getCustomerStats(id) {
    try {
      const response = await apiClient.get(`/api/customers/${id}/stats`);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل إحصائيات العميل: ${error.message}`);
    }
  },

  /**
   * الحصول على إحصائيات عامة للعملاء
   */
  async getGeneralStats() {
    try {
      const response = await apiClient.get('/api/customers/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات العامة: ${error.message}`);
    }
  }
};

export default customerService;

