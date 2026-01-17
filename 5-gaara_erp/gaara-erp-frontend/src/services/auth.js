/**
 * Authentication Service
 * Handles user authentication, registration, and session management
 */

import api, { setTokens, clearTokens } from "./api"

export const authService = {
  /**
   * Login user with email and password
   */
  login: async (email, password) => {
    const data = await api.post("/auth/login/", { email, password })
    if (data.access) {
      setTokens(data.access, data.refresh)
      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user))
      }
    }
    return data
  },

  /**
   * Register new user
   */
  register: async (userData) => {
    const data = await api.post("/auth/register/", userData)
    if (data.access) {
      setTokens(data.access, data.refresh)
      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user))
      }
    }
    return data
  },

  /**
   * Logout user - clear all tokens and session data
   */
  logout: async () => {
    try {
      await api.post("/auth/logout/")
    } catch {
      // Ignore logout errors
    } finally {
      clearTokens()
      localStorage.removeItem("user")
    }
  },

  /**
   * Request password reset email
   */
  forgotPassword: async (email) => {
    return api.post("/auth/forgot-password/", { email })
  },

  /**
   * Reset password with token
   */
  resetPassword: async (token, password, passwordConfirm) => {
    return api.post("/auth/reset-password/", {
      token,
      password,
      password_confirm: passwordConfirm,
    })
  },

  /**
   * Verify email with token
   */
  verifyEmail: async (token) => {
    return api.post("/auth/verify-email/", { token })
  },

  /**
   * Resend verification email
   */
  resendVerification: async (email) => {
    return api.post("/auth/resend-verification/", { email })
  },

  /**
   * Get current user profile
   */
  getProfile: async () => {
    return api.get("/auth/profile/")
  },

  /**
   * Update user profile
   */
  updateProfile: async (profileData) => {
    return api.patch("/auth/profile/", profileData)
  },

  /**
   * Change password
   */
  changePassword: async (currentPassword, newPassword, confirmPassword) => {
    return api.post("/auth/change-password/", {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    })
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    const token = localStorage.getItem("access_token")
    return !!token
  },

  /**
   * Get stored user data
   */
  getUser: () => {
    try {
      const user = localStorage.getItem("user")
      return user ? JSON.parse(user) : null
    } catch {
      return null
    }
  },
}

export default authService
