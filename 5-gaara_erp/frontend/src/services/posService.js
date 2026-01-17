/**
 * خدمة نظام نقطة البيع (POS)
 */
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

const posService = {
  // ==================== Shifts ====================
  
  /**
   * الحصول على قائمة الورديات
   */
  async getShifts(params = {}) {
    const response = await axios.get(`${API_URL}/api/pos/shifts`, { params });
    return response.data;
  },

  /**
   * الحصول على تفاصيل وردية
   */
  async getShift(shiftId) {
    const response = await axios.get(`${API_URL}/api/pos/shifts/${shiftId}`);
    return response.data;
  },

  /**
   * فتح وردية جديدة
   */
  async openShift(data) {
    const response = await axios.post(`${API_URL}/api/pos/shifts/open`, data);
    return response.data;
  },

  /**
   * إغلاق وردية
   */
  async closeShift(shiftId, data) {
    const response = await axios.post(`${API_URL}/api/pos/shifts/${shiftId}/close`, data);
    return response.data;
  },

  /**
   * الحصول على الوردية الحالية
   */
  async getCurrentShift(userId) {
    const response = await axios.get(`${API_URL}/api/pos/shifts/current`, {
      params: { user_id: userId }
    });
    return response.data;
  },

  // ==================== Sales ====================
  
  /**
   * إنشاء عملية بيع
   */
  async createSale(data) {
    const response = await axios.post(`${API_URL}/api/pos/sales`, data);
    return response.data;
  },

  /**
   * الحصول على تفاصيل عملية بيع
   */
  async getSale(saleId) {
    const response = await axios.get(`${API_URL}/api/pos/sales/${saleId}`);
    return response.data;
  },

  /**
   * إرجاع عملية بيع
   */
  async refundSale(saleId, data) {
    const response = await axios.post(`${API_URL}/api/pos/sales/${saleId}/refund`, data);
    return response.data;
  },

  // ==================== Products ====================
  
  /**
   * البحث عن المنتجات
   */
  async searchProducts(query) {
    const response = await axios.get(`${API_URL}/api/pos/products/search`, {
      params: { q: query }
    });
    return response.data;
  },

  // ==================== Stats ====================
  
  /**
   * إحصائيات نقطة البيع
   */
  async getStats(shiftId) {
    const response = await axios.get(`${API_URL}/api/pos/stats`, {
      params: { shift_id: shiftId }
    });
    return response.data;
  }
};

export default posService;
