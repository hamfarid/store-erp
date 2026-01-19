// FILE: frontend/services/AuthService.js | PURPOSE: Authentication service | OWNER: Frontend Team | LAST-AUDITED: 2025-11-18

import apiService from './ApiService';

class AuthService {
  /**
   * Login user with email and password
   * @param {Object} credentials - { email, password }
   * @returns {Promise<Object>} - { access_token, refresh_token, user }
   */
  async login(credentials) {
    try {
      const response = await apiService.post('/v1/auth/login', credentials);
      
      if (response.access_token) {
        // Store tokens
        localStorage.setItem('access_token', response.access_token);
        if (response.refresh_token) {
          localStorage.setItem('refresh_token', response.refresh_token);
        }
        
        // Set token in API service
        apiService.setToken(response.access_token);
      }
      
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Register new user
   * @param {Object} userData - { email, password, name }
   * @returns {Promise<Object>} - { access_token, user }
   */
  async register(userData) {
    try {
      const response = await apiService.post('/v1/auth/register', userData);
      
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        apiService.setToken(response.access_token);
      }
      
      return response;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      // Clear tokens
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      // Remove token from API service
      apiService.removeToken();
      
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  /**
   * Get current user profile
   * @returns {Promise<Object>} - { user }
   */
  async getProfile() {
    try {
      const response = await apiService.get('/v1/auth/me');
      return response;
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  }

  /**
   * Update user profile
   * @param {Object} profileData - { name, email, phone, etc. }
   * @returns {Promise<Object>} - { user }
   */
  async updateProfile(profileData) {
    try {
      const response = await apiService.put('/v1/auth/me', profileData);
      return response;
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  }

  /**
   * Change password
   * @param {Object} passwordData - { old_password, new_password }
   * @returns {Promise<Object>}
   */
  async changePassword(passwordData) {
    try {
      const response = await apiService.put('/v1/auth/password', passwordData);
      return response;
    } catch (error) {
      console.error('Change password error:', error);
      throw error;
    }
  }

  /**
   * Setup MFA
   * @returns {Promise<Object>} - { qr_code, secret }
   */
  async setupMFA() {
    try {
      const response = await apiService.post('/v1/auth/mfa/setup');
      return response;
    } catch (error) {
      console.error('Setup MFA error:', error);
      throw error;
    }
  }

  /**
   * Enable MFA
   * @param {Object} mfaData - { code }
   * @returns {Promise<Object>}
   */
  async enableMFA(mfaData) {
    try {
      const response = await apiService.post('/v1/auth/mfa/enable', mfaData);
      return response;
    } catch (error) {
      console.error('Enable MFA error:', error);
      throw error;
    }
  }

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  /**
   * Get access token
   * @returns {string|null}
   */
  getToken() {
    return localStorage.getItem('access_token');
  }
}

// Export singleton instance
export default new AuthService();

// Also export the class for testing
export { AuthService };

