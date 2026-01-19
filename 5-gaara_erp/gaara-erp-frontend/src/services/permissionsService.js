/**
 * Permissions Service - خدمة الصلاحيات
 * Gaara ERP v12
 *
 * API service for permissions management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api from './api'

const baseEndpoint = '/permissions'

/**
 * Permissions Service
 */
const permissionsService = {
  /**
   * Get all permissions
   */
  getPermissions: async (params = {}) => {
    try {
      const response = await api.get(baseEndpoint, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get permissions grouped by module
   */
  getGroupedPermissions: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/grouped`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: {} }
    }
  },

  /**
   * Get permission modules
   */
  getModules: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/modules`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Check user permission
   */
  checkPermission: async (permissionCode) => {
    try {
      const response = await api.get(`${baseEndpoint}/check/${permissionCode}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: { hasPermission: false } }
    }
  },

  /**
   * Check multiple permissions
   */
  checkPermissions: async (permissionCodes) => {
    try {
      const response = await api.post(`${baseEndpoint}/check-multiple`, { permissions: permissionCodes })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: {} }
    }
  },

  /**
   * Get my permissions
   */
  getMyPermissions: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/me`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },
}

export default permissionsService
