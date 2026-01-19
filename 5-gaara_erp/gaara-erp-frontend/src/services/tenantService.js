/**
 * Tenant Service - API Client for Multi-Tenancy
 * خدمة المستأجر - عميل API لتعدد المستأجرين
 *
 * This service provides methods to interact with the tenant API endpoints.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 * @created 2026-01-17
 */

import axios from 'axios';

// Base API URL - configure based on environment
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Tenant Service object containing all tenant-related API methods.
 * كائن خدمة المستأجر يحتوي على جميع طرق API المتعلقة بالمستأجر.
 */
const tenantService = {
  /**
   * Get all tenants the current user has access to.
   * الحصول على جميع المستأجرين الذين يمكن للمستخدم الحالي الوصول إليهم.
   *
   * @returns {Promise<Object>} API response with tenants array
   *
   * @example
   * const response = await tenantService.getTenants();
   * console.log(response.data); // Array of tenants
   */
  async getTenants() {
    try {
      const response = await apiClient.get('/tenants/');
      return response.data;
    } catch (error) {
      console.error('Error fetching tenants:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Get a single tenant by ID.
   * الحصول على مستأجر واحد بواسطة المعرف.
   *
   * @param {string} tenantId - UUID of the tenant
   * @returns {Promise<Object>} API response with tenant details
   *
   * @example
   * const response = await tenantService.getTenant('uuid-here');
   * console.log(response.data.name);
   */
  async getTenant(tenantId) {
    try {
      const response = await apiClient.get(`/tenants/${tenantId}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Create a new tenant.
   * إنشاء مستأجر جديد.
   *
   * @param {Object} tenantData - Tenant creation data
   * @param {string} tenantData.name - Organization name
   * @param {string} tenantData.slug - URL-safe identifier
   * @param {string} [tenantData.name_ar] - Arabic name
   * @param {string} [tenantData.plan_code] - Subscription plan code
   * @param {string} [tenantData.custom_domain] - Custom domain
   * @returns {Promise<Object>} API response with created tenant
   *
   * @example
   * const response = await tenantService.createTenant({
   *   name: 'Acme Corp',
   *   slug: 'acme-corp',
   *   plan_code: 'pro'
   * });
   */
  async createTenant(tenantData) {
    try {
      const response = await apiClient.post('/tenants/', tenantData);
      return response.data;
    } catch (error) {
      console.error('Error creating tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Update an existing tenant.
   * تحديث مستأجر موجود.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {Object} updateData - Fields to update
   * @returns {Promise<Object>} API response with updated tenant
   *
   * @example
   * const response = await tenantService.updateTenant('uuid', {
   *   name: 'New Name',
   *   logo: 'https://...'
   * });
   */
  async updateTenant(tenantId, updateData) {
    try {
      const response = await apiClient.put(`/tenants/${tenantId}/`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Deactivate a tenant (soft delete).
   * إلغاء تنشيط مستأجر (حذف ناعم).
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} [reason] - Reason for deactivation
   * @returns {Promise<Object>} API response
   *
   * @example
   * await tenantService.deleteTenant('uuid', 'No longer needed');
   */
  async deleteTenant(tenantId, reason = '') {
    try {
      const response = await apiClient.delete(`/tenants/${tenantId}/`, {
        data: { reason },
      });
      return response.data;
    } catch (error) {
      console.error('Error deleting tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Get tenant settings.
   * الحصول على إعدادات المستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @returns {Promise<Object>} API response with settings
   */
  async getTenantSettings(tenantId) {
    try {
      const response = await apiClient.get(`/tenants/${tenantId}/settings/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching tenant settings:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Update tenant settings.
   * تحديث إعدادات المستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {Object} settingsData - Settings to update
   * @returns {Promise<Object>} API response
   */
  async updateTenantSettings(tenantId, settingsData) {
    try {
      const response = await apiClient.put(
        `/tenants/${tenantId}/settings/`,
        settingsData
      );
      return response.data;
    } catch (error) {
      console.error('Error updating tenant settings:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Get all users in a tenant.
   * الحصول على جميع المستخدمين في مستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @returns {Promise<Object>} API response with users array
   */
  async getTenantUsers(tenantId) {
    try {
      const response = await apiClient.get(`/tenants/${tenantId}/users/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching tenant users:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Add a user to a tenant.
   * إضافة مستخدم إلى مستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} userId - UUID of the user to add
   * @param {string} [role='member'] - Role to assign
   * @returns {Promise<Object>} API response
   */
  async addUserToTenant(tenantId, userId, role = 'member') {
    try {
      const response = await apiClient.post(`/tenants/${tenantId}/users/`, {
        user_id: userId,
        role,
      });
      return response.data;
    } catch (error) {
      console.error('Error adding user to tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Update a user's role in a tenant.
   * تحديث دور مستخدم في مستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} userId - UUID of the user
   * @param {Object} updateData - Data to update (role, permissions, etc.)
   * @returns {Promise<Object>} API response
   */
  async updateTenantUser(tenantId, userId, updateData) {
    try {
      const response = await apiClient.put(
        `/tenants/${tenantId}/users/${userId}/`,
        updateData
      );
      return response.data;
    } catch (error) {
      console.error('Error updating tenant user:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Remove a user from a tenant.
   * إزالة مستخدم من مستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} userId - UUID of the user
   * @returns {Promise<Object>} API response
   */
  async removeUserFromTenant(tenantId, userId) {
    try {
      const response = await apiClient.delete(
        `/tenants/${tenantId}/users/${userId}/`
      );
      return response.data;
    } catch (error) {
      console.error('Error removing user from tenant:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Get available subscription plans.
   * الحصول على خطط الاشتراك المتاحة.
   *
   * @returns {Promise<Object>} API response with plans array
   */
  async getPlans() {
    try {
      const response = await apiClient.get('/tenants/plans/');
      return response.data;
    } catch (error) {
      console.error('Error fetching plans:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Change tenant's subscription plan.
   * تغيير خطة اشتراك المستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} planCode - Code of the new plan
   * @returns {Promise<Object>} API response
   */
  async changePlan(tenantId, planCode) {
    try {
      const response = await apiClient.post(`/tenants/${tenantId}/change-plan/`, {
        plan_code: planCode,
      });
      return response.data;
    } catch (error) {
      console.error('Error changing plan:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Send invitation to join tenant.
   * إرسال دعوة للانضمام إلى مستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} email - Email to invite
   * @param {string} [role='member'] - Role to assign
   * @param {string} [message=''] - Optional message
   * @returns {Promise<Object>} API response
   */
  async sendInvitation(tenantId, email, role = 'member', message = '') {
    try {
      const response = await apiClient.post(`/tenants/${tenantId}/invitations/`, {
        email,
        role,
        message,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending invitation:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Get pending invitations for a tenant.
   * الحصول على الدعوات المعلقة لمستأجر.
   *
   * @param {string} tenantId - UUID of the tenant
   * @returns {Promise<Object>} API response with invitations array
   */
  async getInvitations(tenantId) {
    try {
      const response = await apiClient.get(`/tenants/${tenantId}/invitations/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching invitations:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Accept an invitation.
   * قبول دعوة.
   *
   * @param {string} token - Invitation token
   * @returns {Promise<Object>} API response
   */
  async acceptInvitation(token) {
    try {
      const response = await apiClient.post('/tenants/invitations/accept/', {
        token,
      });
      return response.data;
    } catch (error) {
      console.error('Error accepting invitation:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Cancel/revoke an invitation.
   * إلغاء دعوة.
   *
   * @param {string} tenantId - UUID of the tenant
   * @param {string} invitationId - UUID of the invitation
   * @returns {Promise<Object>} API response
   */
  async cancelInvitation(tenantId, invitationId) {
    try {
      const response = await apiClient.delete(
        `/tenants/${tenantId}/invitations/${invitationId}/`
      );
      return response.data;
    } catch (error) {
      console.error('Error canceling invitation:', error);
      throw this._handleError(error);
    }
  },

  /**
   * Check if a slug is available.
   * التحقق من توفر معرف.
   *
   * @param {string} slug - Slug to check
   * @returns {Promise<boolean>} True if available
   */
  async checkSlugAvailability(slug) {
    try {
      const response = await apiClient.get('/tenants/check-slug/', {
        params: { slug },
      });
      return response.data.available;
    } catch (error) {
      console.error('Error checking slug:', error);
      return false;
    }
  },

  /**
   * Set current tenant for API requests (via header).
   * تعيين المستأجر الحالي لطلبات API.
   *
   * @param {string} tenantId - UUID of the tenant
   */
  setCurrentTenant(tenantId) {
    apiClient.defaults.headers.common['X-Tenant-ID'] = tenantId;
    localStorage.setItem('current_tenant_id', tenantId);
  },

  /**
   * Set current tenant by slug.
   * تعيين المستأجر الحالي بواسطة المعرف.
   *
   * @param {string} slug - Slug of the tenant
   */
  setCurrentTenantBySlug(slug) {
    apiClient.defaults.headers.common['X-Tenant-Slug'] = slug;
    localStorage.setItem('current_tenant_slug', slug);
  },

  /**
   * Get current tenant ID from storage.
   * الحصول على معرف المستأجر الحالي من التخزين.
   *
   * @returns {string|null} Current tenant ID
   */
  getCurrentTenantId() {
    return localStorage.getItem('current_tenant_id');
  },

  /**
   * Clear current tenant.
   * مسح المستأجر الحالي.
   */
  clearCurrentTenant() {
    delete apiClient.defaults.headers.common['X-Tenant-ID'];
    delete apiClient.defaults.headers.common['X-Tenant-Slug'];
    localStorage.removeItem('current_tenant_id');
    localStorage.removeItem('current_tenant_slug');
  },

  /**
   * Handle API errors and format them consistently.
   * معالجة أخطاء API وتنسيقها بشكل متسق.
   *
   * @private
   * @param {Error} error - Axios error object
   * @returns {Object} Formatted error object
   */
  _handleError(error) {
    if (error.response) {
      // Server responded with error
      return {
        success: false,
        status: error.response.status,
        error: error.response.data.error || 'UNKNOWN_ERROR',
        message: error.response.data.message || 'An error occurred',
        message_ar: error.response.data.message_ar || 'حدث خطأ',
      };
    } else if (error.request) {
      // Request made but no response
      return {
        success: false,
        status: 0,
        error: 'NETWORK_ERROR',
        message: 'Unable to connect to server',
        message_ar: 'تعذر الاتصال بالخادم',
      };
    } else {
      // Something else went wrong
      return {
        success: false,
        status: 0,
        error: 'CLIENT_ERROR',
        message: error.message,
        message_ar: 'خطأ في العميل',
      };
    }
  },
};

export default tenantService;

// Named exports for specific functions
export const {
  getTenants,
  getTenant,
  createTenant,
  updateTenant,
  deleteTenant,
  getTenantSettings,
  updateTenantSettings,
  getTenantUsers,
  addUserToTenant,
  removeUserFromTenant,
  setCurrentTenant,
  clearCurrentTenant,
} = tenantService;
