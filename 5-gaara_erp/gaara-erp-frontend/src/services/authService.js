/**
 * Auth Service - خدمة المصادقة
 * Gaara ERP v12
 *
 * Authentication service for login, logout, and token management.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import api from './api'

const authService = {
  /**
   * Login user
   */
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials)
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token)
        if (response.refresh_token) {
          localStorage.setItem('refresh_token', response.refresh_token)
        }
      }
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Logout user
   */
  logout: async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      // Ignore errors on logout
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('current_tenant_id')
    }
  },

  /**
   * Get current user
   */
  getCurrentUser: async () => {
    try {
      return await api.get('/auth/me')
    } catch (error) {
      throw error
    }
  },

  /**
   * Refresh token
   */
  refreshToken: async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token')
      }
      const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token)
      }
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token')
  },

  /**
   * Get access token
   */
  getAccessToken: () => {
    return localStorage.getItem('access_token')
  },

  /**
   * Register user
   */
  register: async (userData) => {
    try {
      return await api.post('/auth/register', userData)
    } catch (error) {
      throw error
    }
  },

  /**
   * Request password reset
   */
  requestPasswordReset: async (email) => {
    try {
      return await api.post('/auth/password-reset', { email })
    } catch (error) {
      throw error
    }
  },

  /**
   * Reset password
   */
  resetPassword: async (token, newPassword) => {
    try {
      return await api.post('/auth/password-reset/confirm', { token, new_password: newPassword })
    } catch (error) {
      throw error
    }
  }
}

export default authService
