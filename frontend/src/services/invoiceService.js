/**
 * خدمة إدارة الفواتير (Invoice Management Service)
 * @file frontend/src/services/invoiceService.js
 */

import apiClient from './apiClient';

const invoiceService = {
  // ==================== CRUD Operations ====================

  /**
   * الحصول على جميع الفواتير
   * @param {Object} params - معلمات الترشيح
   */
  async getInvoices(params = {}) {
    return apiClient.get('/api/invoices', params);
  },

  /**
   * الحصول على فاتورة بواسطة ID
   * @param {number} id - معرف الفاتورة
   */
  async getInvoiceById(id) {
    return apiClient.get(`/api/invoices/${id}`);
  },

  /**
   * الحصول على فاتورة بواسطة الرقم
   * @param {string} invoiceNumber - رقم الفاتورة
   */
  async getInvoiceByNumber(invoiceNumber) {
    return apiClient.get(`/api/invoices/number/${invoiceNumber}`);
  },

  /**
   * إنشاء فاتورة جديدة
   * @param {Object} data - بيانات الفاتورة
   */
  async createInvoice(data) {
    return apiClient.post('/api/invoices', data);
  },

  /**
   * تحديث فاتورة
   * @param {number} id - معرف الفاتورة
   * @param {Object} data - البيانات المحدثة
   */
  async updateInvoice(id, data) {
    return apiClient.put(`/api/invoices/${id}`, data);
  },

  /**
   * حذف فاتورة
   * @param {number} id - معرف الفاتورة
   */
  async deleteInvoice(id) {
    return apiClient.delete(`/api/invoices/${id}`);
  },

  // ==================== Sales Invoices ====================

  /**
   * إنشاء فاتورة مبيعات
   * @param {Object} data - بيانات الفاتورة
   */
  async createSalesInvoice(data) {
    return apiClient.post('/api/invoices/sales', data);
  },

  /**
   * الحصول على فواتير المبيعات
   * @param {Object} params - معلمات الترشيح
   */
  async getSalesInvoices(params = {}) {
    return apiClient.get('/api/invoices/sales', params);
  },

  // ==================== Purchase Invoices ====================

  /**
   * إنشاء فاتورة مشتريات
   * @param {Object} data - بيانات الفاتورة
   */
  async createPurchaseInvoice(data) {
    return apiClient.post('/api/invoices/purchases', data);
  },

  /**
   * الحصول على فواتير المشتريات
   * @param {Object} params - معلمات الترشيح
   */
  async getPurchaseInvoices(params = {}) {
    return apiClient.get('/api/invoices/purchases', params);
  },

  // ==================== Returns ====================

  /**
   * إنشاء فاتورة مرتجعات
   * @param {Object} data - بيانات المرتجع
   */
  async createReturnInvoice(data) {
    return apiClient.post('/api/invoices/returns', data);
  },

  /**
   * معالجة مرتجع من فاتورة
   * @param {number} invoiceId - معرف الفاتورة
   * @param {Array} items - العناصر المرتجعة
   */
  async processReturn(invoiceId, items) {
    return apiClient.post(`/api/invoices/${invoiceId}/return`, { items });
  },

  // ==================== Status Operations ====================

  /**
   * تحديث حالة الفاتورة
   * @param {number} id - معرف الفاتورة
   * @param {string} status - الحالة الجديدة
   */
  async updateInvoiceStatus(id, status) {
    return apiClient.patch(`/api/invoices/${id}/status`, { status });
  },

  /**
   * إلغاء فاتورة
   * @param {number} id - معرف الفاتورة
   * @param {string} reason - سبب الإلغاء
   */
  async cancelInvoice(id, reason) {
    return apiClient.post(`/api/invoices/${id}/cancel`, { reason });
  },

  /**
   * تأكيد فاتورة
   * @param {number} id - معرف الفاتورة
   */
  async confirmInvoice(id) {
    return apiClient.post(`/api/invoices/${id}/confirm`);
  },

  // ==================== Payments ====================

  /**
   * إضافة دفعة للفاتورة
   * @param {number} invoiceId - معرف الفاتورة
   * @param {Object} paymentData - بيانات الدفعة
   */
  async addPayment(invoiceId, paymentData) {
    return apiClient.post(`/api/invoices/${invoiceId}/payments`, paymentData);
  },

  /**
   * الحصول على دفعات الفاتورة
   * @param {number} invoiceId - معرف الفاتورة
   */
  async getInvoicePayments(invoiceId) {
    return apiClient.get(`/api/invoices/${invoiceId}/payments`);
  },

  // ==================== Customer Invoices ====================

  /**
   * الحصول على فواتير عميل
   * @param {number} customerId - معرف العميل
   */
  async getCustomerInvoices(customerId) {
    return apiClient.get('/api/invoices', { customer_id: customerId });
  },

  /**
   * الحصول على رصيد العميل
   * @param {number} customerId - معرف العميل
   */
  async getCustomerBalance(customerId) {
    return apiClient.get(`/api/customers/${customerId}/balance`);
  },

  // ==================== Print & Export ====================

  /**
   * طباعة فاتورة
   * @param {number} id - معرف الفاتورة
   */
  async printInvoice(id) {
    return apiClient.get(`/api/invoices/${id}/print`);
  },

  /**
   * تصدير فاتورة إلى PDF
   * @param {number} id - معرف الفاتورة
   */
  async exportToPDF(id) {
    return apiClient.downloadFile(`/api/invoices/${id}/export/pdf`, `invoice_${id}.pdf`);
  },

  /**
   * تصدير الفواتير إلى Excel
   * @param {Object} filters - معلمات الترشيح
   */
  async exportToExcel(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    const endpoint = queryString ? `/api/invoices/export/excel?${queryString}` : '/api/invoices/export/excel';
    return apiClient.downloadFile(endpoint, 'invoices_export.xlsx');
  },

  // ==================== Statistics ====================

  /**
   * إحصائيات الفواتير
   * @param {Object} params - معلمات الفترة
   */
  async getInvoiceStats(params = {}) {
    return apiClient.get('/api/invoices/stats', params);
  },

  /**
   * ملخص فواتير اليوم
   */
  async getTodaySummary() {
    return apiClient.get('/api/invoices/today-summary');
  }
};

export default invoiceService;
