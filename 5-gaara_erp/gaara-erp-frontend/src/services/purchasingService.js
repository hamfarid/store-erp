/**
 * Purchasing Service - خدمة المشتريات
 * Gaara ERP v12
 *
 * API service for purchasing and supplier management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/purchasing'

/**
 * Purchasing Service
 */
const purchasingService = {
  // Purchase Orders
  /**
   * Get purchase orders
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
   * Get single order
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
   * Create purchase order
   */
  createOrder: async (orderData) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders`, orderData)
      return { success: true, data: response.data || response, message_ar: 'تم إنشاء أمر الشراء' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update purchase order
   */
  updateOrder: async (id, orderData) => {
    try {
      const response = await api.put(`${baseEndpoint}/orders/${id}`, orderData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث أمر الشراء' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Cancel purchase order
   */
  cancelOrder: async (id, reason) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${id}/cancel`, { reason })
      return { success: true, data: response.data || response, message_ar: 'تم إلغاء أمر الشراء' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Approve purchase order
   */
  approveOrder: async (id) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${id}/approve`)
      return { success: true, data: response.data || response, message_ar: 'تم اعتماد أمر الشراء' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Receive order items
   */
  receiveOrder: async (id, receiveData) => {
    try {
      const response = await api.post(`${baseEndpoint}/orders/${id}/receive`, receiveData)
      return { success: true, data: response.data || response, message_ar: 'تم استلام الطلب' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  // Suppliers
  /**
   * Get suppliers
   */
  getSuppliers: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/suppliers`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single supplier
   */
  getSupplier: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/suppliers/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create supplier
   */
  createSupplier: async (supplierData) => {
    try {
      const response = await api.post(`${baseEndpoint}/suppliers`, supplierData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة المورد' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update supplier
   */
  updateSupplier: async (id, supplierData) => {
    try {
      const response = await api.put(`${baseEndpoint}/suppliers/${id}`, supplierData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث المورد' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete supplier
   */
  deleteSupplier: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/suppliers/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف المورد' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get supplier products
   */
  getSupplierProducts: async (supplierId) => {
    try {
      const response = await api.get(`${baseEndpoint}/suppliers/${supplierId}/products`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get purchasing statistics
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
   * Export purchasing data
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
}

export default purchasingService
