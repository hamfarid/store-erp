/**
 * Sales Service - خدمة المبيعات
 * Gaara ERP v12
 *
 * API service for sales order management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/sales'

// Base CRUD operations
const baseCrud = createCrudService(baseEndpoint)

/**
 * Sales Service
 */
const salesService = {
  ...baseCrud,

  /**
   * Get sales orders with filters
   */
  getOrders: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/orders`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single order with details
   */
  getOrder: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/orders/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create sales order
   */
  createOrder: async (orderData) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders`, orderData)
      return { success: true, data: response.data || response, message_ar: 'تم إنشاء الطلب بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update sales order
   */
  updateOrder: async (id, orderData) => {
    try {
      const response = await api.put(`${baseEndpoint}/orders/${id}`, orderData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الطلب بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Cancel sales order
   */
  cancelOrder: async (id, reason) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${id}/cancel`, { reason })
      return { success: true, data: response.data || response, message_ar: 'تم إلغاء الطلب' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update order status
   */
  updateStatus: async (id, status) => {
    try {
      const response = await api.patch(`${baseEndpoint}/orders/${id}/status`, { status })
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الحالة' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Generate invoice for order
   */
  generateInvoice: async (orderId) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${orderId}/invoice`)
      return { success: true, data: response.data || response, message_ar: 'تم إنشاء الفاتورة' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get sales statistics
   */
  getStats: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/stats`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get sales report
   */
  getReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/report`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Export sales data
   */
  exportData: async (format = 'xlsx', params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/export`, {
        params: { ...params, format },
        responseType: 'blob',
      })
      return { success: true, data: response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get order history
   */
  getOrderHistory: async (orderId) => {
    try {
      const response = await api.get(`${baseEndpoint}/orders/${orderId}/history`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Add payment to order
   */
  addPayment: async (orderId, paymentData) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${orderId}/payments`, paymentData)
      return { success: true, data: response.data || response, message_ar: 'تم تسجيل الدفعة' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },
}

export default salesService
