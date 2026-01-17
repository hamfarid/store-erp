/**
 * Admin Service
 * 
 * API service for admin operations including roles, permissions, and setup.
 */

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

// Create axios instance with auth headers
const api = axios.create({
  baseURL: `${API_BASE}/admin`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============================================================================
// Setup APIs
// ============================================================================

export const setupService = {
  /**
   * Get system setup status
   */
  getStatus: async () => {
    const response = await api.get('/setup/status');
    return response.data;
  },

  /**
   * Initialize system with default data
   */
  initialize: async () => {
    const response = await api.post('/setup/init');
    return response.data;
  },

  /**
   * Save company information
   */
  saveCompany: async (companyData) => {
    const response = await api.post('/setup/company', companyData);
    return response.data;
  },

  /**
   * Create admin user
   */
  createAdmin: async (adminData) => {
    const response = await api.post('/setup/admin', adminData);
    return response.data;
  },

  /**
   * Complete setup
   */
  complete: async () => {
    const response = await api.post('/setup/complete');
    return response.data;
  },
};

// ============================================================================
// Permission APIs
// ============================================================================

export const permissionService = {
  /**
   * Get all permissions
   */
  getAll: async () => {
    const response = await api.get('/permissions');
    return response.data;
  },

  /**
   * Get permissions grouped by module
   */
  getGrouped: async () => {
    const response = await api.get('/permissions');
    return response.data.data.grouped;
  },
};

// ============================================================================
// Role APIs
// ============================================================================

export const roleService = {
  /**
   * Get all roles
   */
  getAll: async () => {
    const response = await api.get('/roles');
    return response.data;
  },

  /**
   * Get a single role
   */
  getById: async (roleId) => {
    const response = await api.get(`/roles/${roleId}`);
    return response.data;
  },

  /**
   * Create a new role
   */
  create: async (roleData) => {
    const response = await api.post('/roles', roleData);
    return response.data;
  },

  /**
   * Update a role
   */
  update: async (roleId, roleData) => {
    const response = await api.put(`/roles/${roleId}`, roleData);
    return response.data;
  },

  /**
   * Delete a role
   */
  delete: async (roleId) => {
    const response = await api.delete(`/roles/${roleId}`);
    return response.data;
  },
};

// ============================================================================
// User-Role APIs
// ============================================================================

export const userRoleService = {
  /**
   * Get user roles
   */
  getUserRoles: async (userId) => {
    const response = await api.get(`/users/${userId}/roles`);
    return response.data;
  },

  /**
   * Assign roles to user
   */
  assignRoles: async (userId, roleIds) => {
    const response = await api.put(`/users/${userId}/roles`, { role_ids: roleIds });
    return response.data;
  },
};

// ============================================================================
// Audit Log APIs
// ============================================================================

export const auditService = {
  /**
   * Get audit logs
   */
  getLogs: async (params = {}) => {
    const response = await api.get('/audit-logs', { params });
    return response.data;
  },
};

// ============================================================================
// Admin Stats APIs
// ============================================================================

export const statsService = {
  /**
   * Get admin statistics
   */
  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

// ============================================================================
// Permission Check API
// ============================================================================

export const checkPermission = async (permissionCode) => {
  const response = await api.post('/check-permission', { permission: permissionCode });
  return response.data.data.has_permission;
};

// ============================================================================
// Export all services
// ============================================================================

export default {
  setup: setupService,
  permissions: permissionService,
  roles: roleService,
  userRoles: userRoleService,
  audit: auditService,
  stats: statsService,
  checkPermission,
};

