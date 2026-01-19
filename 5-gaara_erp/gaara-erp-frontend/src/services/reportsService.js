/**
 * Reports Service - خدمة التقارير
 * Gaara ERP v12
 *
 * API service for reports generation and analytics.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api from './api'

const baseEndpoint = '/reports'

/**
 * Reports Service
 */
const reportsService = {
  /**
   * Get dashboard statistics
   */
  getDashboardStats: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/dashboard`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get sales report
   */
  getSalesReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/sales`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get purchasing report
   */
  getPurchasingReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/purchasing`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get inventory report
   */
  getInventoryReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/inventory`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get financial report
   */
  getFinancialReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/financial`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get customer report
   */
  getCustomerReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/customers`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get agricultural report
   */
  getAgriculturalReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/agricultural`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get profit/loss report
   */
  getProfitLossReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/profit-loss`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get tax report
   */
  getTaxReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/tax`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get aging report (receivables/payables)
   */
  getAgingReport: async (type = 'receivables', params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/aging/${type}`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Export report to file
   */
  exportReport: async (reportType, format = 'xlsx', params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/${reportType}/export`, {
        params: { ...params, format },
        responseType: 'blob',
      })
      return { success: true, data: response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Generate custom report
   */
  generateCustomReport: async (reportConfig) => {
    try {
      const response = await api.post(`${baseEndpoint}/custom`, reportConfig)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get saved reports
   */
  getSavedReports: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/saved`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Save report configuration
   */
  saveReport: async (reportData) => {
    try {
      const response = await api.post(`${baseEndpoint}/saved`, reportData)
      return { success: true, data: response.data || response, message_ar: 'تم حفظ التقرير' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete saved report
   */
  deleteSavedReport: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/saved/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف التقرير' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Schedule report
   */
  scheduleReport: async (scheduleData) => {
    try {
      const response = await api.post(`${baseEndpoint}/schedule`, scheduleData)
      return { success: true, data: response.data || response, message_ar: 'تم جدولة التقرير' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get report templates
   */
  getTemplates: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/templates`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },
}

export default reportsService
