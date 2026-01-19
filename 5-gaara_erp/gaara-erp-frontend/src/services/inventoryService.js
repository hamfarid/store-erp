/**
 * Inventory Service - خدمة المخزون
 * Gaara ERP v12
 *
 * API service for inventory and product management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/inventory'

// Base CRUD for products
const productsCrud = createCrudService(`${baseEndpoint}/products`)

/**
 * Inventory Service
 */
const inventoryService = {
  // Products
  products: productsCrud,

  /**
   * Get all products with filters
   */
  getProducts: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/products`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single product
   */
  getProduct: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/products/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create product
   */
  createProduct: async (productData) => {
    try {
      const response = await api.post(`${baseEndpoint}/products`, productData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة المنتج بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update product
   */
  updateProduct: async (id, productData) => {
    try {
      const response = await api.put(`${baseEndpoint}/products/${id}`, productData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث المنتج بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete product
   */
  deleteProduct: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/products/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف المنتج' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  // Categories
  /**
   * Get categories
   */
  getCategories: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/categories`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Create category
   */
  createCategory: async (categoryData) => {
    try {
      const response = await api.post(`${baseEndpoint}/categories`, categoryData)
      return { success: true, data: response.data || response, message_ar: 'تم إضافة التصنيف' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  // Warehouses
  /**
   * Get warehouses
   */
  getWarehouses: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/warehouses`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get warehouse stock
   */
  getWarehouseStock: async (warehouseId) => {
    try {
      const response = await api.get(`${baseEndpoint}/warehouses/${warehouseId}/stock`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  // Stock operations
  /**
   * Adjust stock
   */
  adjustStock: async (productId, adjustmentData) => {
    try {
      const response = await api.post(`${baseEndpoint}/products/${productId}/adjust`, adjustmentData)
      return { success: true, data: response.data || response, message_ar: 'تم تعديل المخزون' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Transfer stock between warehouses
   */
  transferStock: async (transferData) => {
    try {
      const response = await api.post(`${baseEndpoint}/transfers`, transferData)
      return { success: true, data: response.data || response, message_ar: 'تم نقل المخزون' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get stock movements history
   */
  getStockMovements: async (productId, params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/products/${productId}/movements`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get low stock alerts
   */
  getLowStockAlerts: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/alerts/low-stock`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get inventory statistics
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
   * Get inventory valuation report
   */
  getValuationReport: async (params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/reports/valuation`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Export inventory data
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
   * Import products from file
   */
  importProducts: async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await api.post(`${baseEndpoint}/import`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return { success: true, data: response.data || response, message_ar: 'تم استيراد المنتجات' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Generate barcode
   */
  generateBarcode: async (productId) => {
    try {
      const response = await api.get(`${baseEndpoint}/products/${productId}/barcode`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },
}

export default inventoryService
