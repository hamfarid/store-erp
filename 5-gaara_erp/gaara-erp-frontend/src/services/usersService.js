/**
 * Users Service - خدمة المستخدمين
 * Gaara ERP v12
 *
 * API service for user management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api, { createCrudService } from './api'

const baseEndpoint = '/users'
const baseCrud = createCrudService(baseEndpoint)

/**
 * Users Service
 */
const usersService = {
  ...baseCrud,

  /**
   * Get all users with filters
   */
  getUsers: async (params = {}) => {
    try {
      const response = await api.get(baseEndpoint, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message, data: [] }
    }
  },

  /**
   * Get single user
   */
  getUser: async (id) => {
    try {
      const response = await api.get(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Create user
   */
  createUser: async (userData) => {
    try {
      const response = await api.post(baseEndpoint, userData)
      return { success: true, data: response.data || response, message_ar: 'تم إنشاء المستخدم بنجاح' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update user
   */
  updateUser: async (id, userData) => {
    try {
      const response = await api.put(`${baseEndpoint}/${id}`, userData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث المستخدم' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Delete user
   */
  deleteUser: async (id) => {
    try {
      const response = await api.delete(`${baseEndpoint}/${id}`)
      return { success: true, data: response.data || response, message_ar: 'تم حذف المستخدم' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Activate user
   */
  activateUser: async (id) => {
    try {
      const response = await api.post(`${baseEndpoint}/${id}/activate`)
      return { success: true, data: response.data || response, message_ar: 'تم تفعيل المستخدم' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Deactivate user
   */
  deactivateUser: async (id) => {
    try {
      const response = await api.post(`${baseEndpoint}/${id}/deactivate`)
      return { success: true, data: response.data || response, message_ar: 'تم إيقاف المستخدم' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Reset user password
   */
  resetPassword: async (id) => {
    try {
      const response = await api.post(`${baseEndpoint}/${id}/reset-password`)
      return { success: true, data: response.data || response, message_ar: 'تم إرسال رابط إعادة تعيين كلمة المرور' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update user roles
   */
  updateRoles: async (id, roleIds) => {
    try {
      const response = await api.put(`${baseEndpoint}/${id}/roles`, { roles: roleIds })
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الأدوار' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get user activity log
   */
  getActivityLog: async (id, params = {}) => {
    try {
      const response = await api.get(`${baseEndpoint}/${id}/activity`, { params })
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get current user profile
   */
  getProfile: async () => {
    try {
      const response = await api.get(`${baseEndpoint}/me`)
      return { success: true, data: response.data || response }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Update profile
   */
  updateProfile: async (profileData) => {
    try {
      const response = await api.put(`${baseEndpoint}/me`, profileData)
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الملف الشخصي' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Change password
   */
  changePassword: async (passwordData) => {
    try {
      const response = await api.post(`${baseEndpoint}/me/change-password`, passwordData)
      return { success: true, data: response.data || response, message_ar: 'تم تغيير كلمة المرور' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Upload avatar
   */
  uploadAvatar: async (file) => {
    try {
      const formData = new FormData()
      formData.append('avatar', file)
      const response = await api.post(`${baseEndpoint}/me/avatar`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return { success: true, data: response.data || response, message_ar: 'تم تحديث الصورة' }
    } catch (error) {
      return { success: false, message: error.message }
    }
  },

  /**
   * Get users statistics
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
   * Export users
   */
  exportUsers: async (format = 'xlsx', params = {}) => {
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

export default usersService
