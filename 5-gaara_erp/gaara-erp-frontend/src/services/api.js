/**
 * API Service - خدمة API المركزية
 * Gaara ERP v12
 *
 * Central API client with interceptors, error handling, and tenant support.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import axios from 'axios'
import { toast } from 'sonner'

// Base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/**
 * Create axios instance with default config
 */
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor - Add auth token and tenant header
 */
api.interceptors.request.use(
  (config) => {
    // Add auth token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Add tenant ID
    const tenantId = localStorage.getItem('current_tenant_id')
    if (tenantId) {
      config.headers['X-Tenant-ID'] = tenantId
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor - Handle errors and token refresh
 */
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config

    // Handle 401 - Try token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          })

          if (response.data.access_token) {
            localStorage.setItem('access_token', response.data.access_token)
            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`
            return api(originalRequest)
          }
        }
      } catch (refreshError) {
        // Refresh failed - logout
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    // Handle other errors
    const errorMessage = error.response?.data?.message_ar ||
                         error.response?.data?.message ||
                         error.message ||
                         'حدث خطأ غير متوقع'

    // Don't show toast for certain endpoints
    const silentEndpoints = ['/auth/check', '/health']
    const isSilent = silentEndpoints.some(ep => originalRequest.url?.includes(ep))

    if (!isSilent && error.response?.status !== 401) {
      toast.error(errorMessage)
    }

    return Promise.reject({
      success: false,
      status: error.response?.status,
      message: errorMessage,
      message_ar: error.response?.data?.message_ar,
      data: error.response?.data,
    })
  }
)

/**
 * API Helper Functions
 */
export const apiHelpers = {
  /**
   * Standard success response
   */
  success: (data, message = '', messageAr = '') => ({
    success: true,
    data,
    message,
    message_ar: messageAr,
  }),

  /**
   * Standard error response
   */
  error: (message, messageAr = '', status = 400) => ({
    success: false,
    message,
    message_ar: messageAr || message,
    status,
  }),
}

/**
 * Generic CRUD service factory
 */
export const createCrudService = (endpoint) => ({
  /**
   * Get all items
   */
  getAll: async (params = {}) => {
    try {
      return await api.get(endpoint, { params })
    } catch (error) {
      throw error
    }
  },

  /**
   * Get single item by ID
   */
  getById: async (id) => {
    try {
      return await api.get(`${endpoint}/${id}`)
    } catch (error) {
      throw error
    }
  },

  /**
   * Create new item
   */
  create: async (data) => {
    try {
      return await api.post(endpoint, data)
    } catch (error) {
      throw error
    }
  },

  /**
   * Update item
   */
  update: async (id, data) => {
    try {
      return await api.put(`${endpoint}/${id}`, data)
    } catch (error) {
      throw error
    }
  },

  /**
   * Delete item
   */
  delete: async (id) => {
    try {
      return await api.delete(`${endpoint}/${id}`)
    } catch (error) {
      throw error
    }
  },

  /**
   * Patch item (partial update)
   */
  patch: async (id, data) => {
    try {
      return await api.patch(`${endpoint}/${id}`, data)
    } catch (error) {
      throw error
    }
  },
})

export default api
