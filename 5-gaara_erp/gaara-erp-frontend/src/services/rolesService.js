/**
 * Roles Service - خدمة الأدوار
 * Gaara ERP v12
 *
 * API service for roles and permissions management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/roles'
const baseCrud = createCrudService(baseEndpoint)

/**
 * Roles Service
 */
const rolesService = {
  ...baseCrud,

  /**
   * Get all roles
   */
  getRoles: async (params = {}) => {
    try {
      const response = await api.get(baseEndpoint, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single role with permissions
   */
  getRole: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create role
   */
  createRole: async (roleData) => {
    try {
      const response = await api.post(baseEndpoint, roleData)
      return { success: true, data: response.data || response, message_ar: 'تم إنشاء الدور بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update role
   */
  updateRole: async (id, roleData) => {
    try {
      const response = await api.put(`${baseEndpoint}/${id}`, roleData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الدور' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete role
   */
  deleteRole: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف الدور' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get role permissions
   */
  getRolePermissions: async (roleId) => {
    try {
      const response = await api.get(`${baseEndpoint}/${roleId}/permissions`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update role permissions
   */
  updateRolePermissions: async (roleId, permissionIds) => {
    try {
      const response = await api.put(`${baseEndpoint}/${roleId}/permissions`, { permissions: permissionIds })
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الصلاحيات' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get role users
   */
  getRoleUsers: async (roleId) => {
    try {
      const response = await api.get(`${baseEndpoint}/${roleId}/users`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Clone role
   */
  cloneRole: async (roleId, newName) => {
    try {
      const response = await api.post(`${baseEndpoint}/${roleId}/clone`, { name: newName })
      return { success: true, data: response.data || response, message_ar: 'تم نسخ الدور بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get roles statistics
   */
  getStats: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/stats`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },
}

export default rolesService
