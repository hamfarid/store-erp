/**
 * Cart Service
 * @file frontend/src/services/cartService.js
 * 
 * خدمة سلة المشتريات - API calls
 */

import apiClient from './apiClient';

const BASE_URL = '/api/pos';

/**
 * Cart Service - عمليات سلة المشتريات
 */
const cartService = {
  /**
   * إنشاء فاتورة مبيعات من السلة
   */
  async createSaleInvoice(cartData) {
    const response = await apiClient.post(`${BASE_URL}/sales`, {
      items: cartData.items.map(item => ({
        product_id: item.product_id,
        lot_id: item.lot_id,
        quantity: item.quantity,
        unit_price: item.price,
        discount: item.discount || 0
      })),
      customer_id: cartData.customer?.id,
      payment_method: cartData.paymentMethod,
      discount_type: cartData.discount?.type,
      discount_value: cartData.discount?.value || 0,
      notes: cartData.notes,
      warehouse_id: cartData.warehouse_id
    });
    return response.data;
  },

  /**
   * البحث عن منتج بالباركود
   */
  async findByBarcode(barcode, warehouseId = null) {
    const params = { barcode };
    if (warehouseId) params.warehouse_id = warehouseId;
    
    const response = await apiClient.get(`${BASE_URL}/products/barcode`, { params });
    return response.data;
  },

  /**
   * البحث عن منتجات
   */
  async searchProducts(query, warehouseId = null, limit = 20) {
    const params = { q: query, limit };
    if (warehouseId) params.warehouse_id = warehouseId;
    
    const response = await apiClient.get(`${BASE_URL}/products/search`, { params });
    return response.data;
  },

  /**
   * البحث عن عملاء
   */
  async searchCustomers(query, limit = 10) {
    const response = await apiClient.get(`${BASE_URL}/customers/search`, {
      params: { q: query, limit }
    });
    return response.data;
  },

  /**
   * الحصول على لوتات المنتج المتاحة
   */
  async getProductLots(productId, warehouseId = null) {
    const params = {};
    if (warehouseId) params.warehouse_id = warehouseId;
    
    const response = await apiClient.get(`${BASE_URL}/products/${productId}/lots`, { params });
    return response.data;
  },

  /**
   * التحقق من توفر المخزون
   */
  async checkStock(items, warehouseId) {
    const response = await apiClient.post(`${BASE_URL}/check-stock`, {
      items: items.map(item => ({
        product_id: item.product_id,
        lot_id: item.lot_id,
        quantity: item.quantity
      })),
      warehouse_id: warehouseId
    });
    return response.data;
  },

  /**
   * حفظ السلة المعلقة
   */
  async saveHeldCart(cartData) {
    const response = await apiClient.post(`${BASE_URL}/held-carts`, cartData);
    return response.data;
  },

  /**
   * جلب السلات المعلقة
   */
  async getHeldCarts() {
    const response = await apiClient.get(`${BASE_URL}/held-carts`);
    return response.data;
  },

  /**
   * حذف سلة معلقة
   */
  async deleteHeldCart(cartId) {
    const response = await apiClient.delete(`${BASE_URL}/held-carts/${cartId}`);
    return response.data;
  },

  /**
   * تطبيق كوبون خصم
   */
  async applyCoupon(code, subtotal) {
    const response = await apiClient.post(`${BASE_URL}/coupons/apply`, {
      code,
      subtotal
    });
    return response.data;
  },

  /**
   * الحصول على إعدادات نقطة البيع
   */
  async getPOSSettings() {
    const response = await apiClient.get(`${BASE_URL}/settings`);
    return response.data;
  },

  /**
   * فتح/إغلاق الدرج النقدي
   */
  async openCashDrawer() {
    const response = await apiClient.post(`${BASE_URL}/cash-drawer/open`);
    return response.data;
  },

  /**
   * جلب ملخص المبيعات اليومية
   */
  async getDailySummary() {
    const response = await apiClient.get(`${BASE_URL}/summary/daily`);
    return response.data;
  },

  /**
   * إغلاق الوردية
   */
  async closeShift(data) {
    const response = await apiClient.post(`${BASE_URL}/shift/close`, data);
    return response.data;
  },

  /**
   * فتح وردية جديدة
   */
  async openShift(data) {
    const response = await apiClient.post(`${BASE_URL}/shift/open`, data);
    return response.data;
  },

  /**
   * جلب حالة الوردية الحالية
   */
  async getCurrentShift() {
    const response = await apiClient.get(`${BASE_URL}/shift/current`);
    return response.data;
  },

  /**
   * طباعة إيصال
   */
  async printReceipt(invoiceId) {
    const response = await apiClient.post(`${BASE_URL}/receipts/${invoiceId}/print`);
    return response.data;
  },

  /**
   * إرسال الإيصال بالبريد الإلكتروني
   */
  async emailReceipt(invoiceId, email) {
    const response = await apiClient.post(`${BASE_URL}/receipts/${invoiceId}/email`, { email });
    return response.data;
  },

  /**
   * معالجة الدفع
   */
  async processPayment(invoiceId, paymentData) {
    const response = await apiClient.post(`${BASE_URL}/payments`, {
      invoice_id: invoiceId,
      ...paymentData
    });
    return response.data;
  },

  /**
   * إلغاء فاتورة
   */
  async cancelInvoice(invoiceId, reason) {
    const response = await apiClient.post(`${BASE_URL}/invoices/${invoiceId}/cancel`, { reason });
    return response.data;
  },

  /**
   * مرتجع جزئي
   */
  async createPartialReturn(invoiceId, items, reason) {
    const response = await apiClient.post(`${BASE_URL}/returns`, {
      invoice_id: invoiceId,
      items,
      reason
    });
    return response.data;
  }
};

export default cartService;
