/**
 * Customers Service - خدمة العملاء
 * Gaara ERP v12
 *
 * API service for customer management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/customers'
const baseCrud = createCrudService(baseEndpoint)

/**
 * Customers Service
 */
const customersService = {
  ...baseCrud,

  /**
   * Get all customers
   */
  getCustomers: async (params = {}) => {
    try {
      const response = await api.get(baseEndpoint, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single customer
   */
  getCustomer: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create customer
   */
  createCustomer: async (customerData) => {
    try {
      const response = await api.post(baseEndpoint, customerData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة العميل بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update customer
   */
  updateCustomer: async (id, customerData) => {
    try {
      const response = await api.put(`${baseEndpoint}/${id}`, customerData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث العميل' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete customer
   */
  deleteCustomer: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف العميل' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer orders
   */
  getCustomerOrders: async (customerId, params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/${customerId}/orders`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer invoices
   */
  getCustomerInvoices: async (customerId, params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/${customerId}/invoices`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer balance
   */
  getCustomerBalance: async (customerId) => {
    try {
      const response = await api.get(`${baseEndpoint}/${customerId}/balance`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Add customer payment
   */
  addPayment: async (customerId, paymentData) => {
    try {
      const response = await api.post(`${baseEndpoint}/${customerId}/payments`, paymentData)
      return { success: true, data: response.data || response, message_ar: 'تم تسجيل الدفعة' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer contacts
   */
  getContacts: async (customerId) => {
    try {
      const response = await api.get(`${baseEndpoint}/${customerId}/contacts`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Add customer contact
   */
  addContact: async (customerId, contactData) => {
    try {
      const response = await api.post(`${baseEndpoint}/${customerId}/contacts`, contactData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة جهة الاتصال' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer addresses
   */
  getAddresses: async (customerId) => {
    try {
      const response = await api.get(`${baseEndpoint}/${customerId}/addresses`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Add customer address
   */
  addAddress: async (customerId, addressData) => {
    try {
      const response = await api.post(`${baseEndpoint}/${customerId}/addresses`, addressData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة العنوان' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer statistics
   */
  getStats: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/stats`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Export customers
   */
  exportCustomers: async (format = 'xlsx', params = {}) => {
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
   * Search customers
   */
  searchCustomers: async (query) => {
    try {
      const response = await api.get(`${baseEndpoint}/search`, { params: { q: query } })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },
}

export default customersService
