import api from "./api"

/**
 * Users Service
 * Handles all user management API calls
 */

// Get all users with filters
export const getUsers = async (params = {}) => {
  const { page = 1, limit = 10, search = "", role = "", status = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(search && { search }),
    ...(role && { role }),
    ...(status && { status }),
  })

  return api.get(`/users?${queryParams}`)
}

// Get single user by ID
export const getUserById = async (userId) => {
  return api.get(`/users/${userId}`)
}

// Create new user
export const createUser = async (userData) => {
  return api.post("/users", userData)
}

// Update user
export const updateUser = async (userId, userData) => {
  return api.put(`/users/${userId}`, userData)
}

// Delete user
export const deleteUser = async (userId) => {
  return api.delete(`/users/${userId}`)
}

// Activate/Deactivate user
export const toggleUserStatus = async (userId, isActive) => {
  return api.patch(`/users/${userId}/status`, { isActive })
}

// Reset user password
export const resetUserPassword = async (userId, newPassword) => {
  return api.post(`/users/${userId}/reset-password`, { password: newPassword })
}

// Assign role to user
export const assignRole = async (userId, roleId) => {
  return api.post(`/users/${userId}/roles`, { roleId })
}

// Remove role from user
export const removeRole = async (userId, roleId) => {
  return api.delete(`/users/${userId}/roles/${roleId}`)
}

// Get user permissions
export const getUserPermissions = async (userId) => {
  return api.get(`/users/${userId}/permissions`)
}

// Get user activity log
export const getUserActivity = async (userId, params = {}) => {
  const { page = 1, limit = 20 } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
  })

  return api.get(`/users/${userId}/activity?${queryParams}`)
}

// Bulk operations
export const bulkDeleteUsers = async (userIds) => {
  return api.post("/users/bulk-delete", { userIds })
}

export const bulkUpdateUsers = async (userIds, updates) => {
  return api.post("/users/bulk-update", { userIds, updates })
}

// Mock data for development
export const mockUsers = [
  {
    id: 1,
    firstName: "أحمد",
    lastName: "محمد",
    email: "ahmed@example.com",
    phone: "+966501234567",
    role: "admin",
    status: "active",
    lastLogin: "2024-01-15T10:30:00Z",
    createdAt: "2023-06-01T08:00:00Z",
    avatar: null,
    permissions: ["users.read", "users.write", "inventory.read"],
  },
  {
    id: 2,
    firstName: "فاطمة",
    lastName: "علي",
    email: "fatima@example.com",
    phone: "+966502345678",
    role: "manager",
    status: "active",
    lastLogin: "2024-01-14T15:20:00Z",
    createdAt: "2023-07-15T09:30:00Z",
    avatar: null,
    permissions: ["inventory.read", "inventory.write", "sales.read"],
  },
  {
    id: 3,
    firstName: "خالد",
    lastName: "سعيد",
    email: "khalid@example.com",
    phone: "+966503456789",
    role: "user",
    status: "active",
    lastLogin: "2024-01-13T11:45:00Z",
    createdAt: "2023-08-20T10:15:00Z",
    avatar: null,
    permissions: ["inventory.read"],
  },
  {
    id: 4,
    firstName: "سارة",
    lastName: "حسن",
    email: "sara@example.com",
    phone: "+966504567890",
    role: "user",
    status: "inactive",
    lastLogin: "2023-12-10T14:00:00Z",
    createdAt: "2023-09-05T12:00:00Z",
    avatar: null,
    permissions: ["sales.read"],
  },
  {
    id: 5,
    firstName: "محمد",
    lastName: "عبدالله",
    email: "mohammed@example.com",
    phone: "+966505678901",
    role: "accountant",
    status: "active",
    lastLogin: "2024-01-15T09:00:00Z",
    createdAt: "2023-10-12T08:30:00Z",
    avatar: null,
    permissions: ["accounting.read", "accounting.write", "reports.read"],
  },
]

export default {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  toggleUserStatus,
  resetUserPassword,
  assignRole,
  removeRole,
  getUserPermissions,
  getUserActivity,
  bulkDeleteUsers,
  bulkUpdateUsers,
  mockUsers,
}
