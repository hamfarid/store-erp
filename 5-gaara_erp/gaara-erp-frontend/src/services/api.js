/**
 * API Service - Centralized HTTP client for backend communication
 * Provides consistent error handling, authentication, and request/response processing
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5001/api"

// Token management
const getToken = () => localStorage.getItem("access_token")
const getRefreshToken = () => localStorage.getItem("refresh_token")
const setTokens = (access, refresh) => {
  localStorage.setItem("access_token", access)
  if (refresh) localStorage.setItem("refresh_token", refresh)
}
const clearTokens = () => {
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
  localStorage.removeItem("user")
}

// Custom error class
class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.data = data
  }
}

// Request interceptor
const buildHeaders = (customHeaders = {}) => {
  const headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Language": "ar",
    ...customHeaders,
  }

  const token = getToken()
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  return headers
}

// Response handler
const handleResponse = async (response) => {
  const contentType = response.headers.get("content-type")
  let data = null

  if (contentType && contentType.includes("application/json")) {
    data = await response.json()
  } else {
    data = await response.text()
  }

  if (!response.ok) {
    // Handle specific error codes
    if (response.status === 401) {
      // Token expired, try to refresh
      const refreshed = await refreshAccessToken()
      if (!refreshed) {
        clearTokens()
        window.location.href = "/login"
      }
      throw new ApiError("جلستك انتهت. يرجى تسجيل الدخول مرة أخرى.", response.status, data)
    }

    if (response.status === 403) {
      throw new ApiError("ليس لديك صلاحية للوصول إلى هذا المورد.", response.status, data)
    }

    if (response.status === 404) {
      throw new ApiError("المورد المطلوب غير موجود.", response.status, data)
    }

    if (response.status === 422) {
      throw new ApiError(data.detail || "بيانات غير صالحة.", response.status, data)
    }

    if (response.status >= 500) {
      throw new ApiError("حدث خطأ في الخادم. يرجى المحاولة لاحقاً.", response.status, data)
    }

    throw new ApiError(
      data.message || data.detail || "حدث خطأ غير متوقع.",
      response.status,
      data
    )
  }

  return data
}

// Refresh token handler
const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return false

  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    })

    if (response.ok) {
      const data = await response.json()
      setTokens(data.access, data.refresh)
      return true
    }
    return false
  } catch {
    return false
  }
}

// Main request function
const request = async (endpoint, options = {}) => {
  const { method = "GET", body, headers = {}, params = {} } = options

  // Build URL with query params
  const url = new URL(`${API_BASE_URL}${endpoint}`)
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value)
    }
  })

  const config = {
    method,
    headers: buildHeaders(headers),
  }

  if (body && method !== "GET") {
    config.body = JSON.stringify(body)
  }

  const response = await fetch(url.toString(), config)
  return handleResponse(response)
}

// HTTP methods
export const api = {
  get: (endpoint, params = {}, headers = {}) =>
    request(endpoint, { method: "GET", params, headers }),

  post: (endpoint, body = {}, headers = {}) =>
    request(endpoint, { method: "POST", body, headers }),

  put: (endpoint, body = {}, headers = {}) =>
    request(endpoint, { method: "PUT", body, headers }),

  patch: (endpoint, body = {}, headers = {}) =>
    request(endpoint, { method: "PATCH", body, headers }),

  delete: (endpoint, headers = {}) =>
    request(endpoint, { method: "DELETE", headers }),
}

// File upload helper
export const uploadFile = async (endpoint, file, fieldName = "file", additionalData = {}) => {
  const formData = new FormData()
  formData.append(fieldName, file)

  Object.entries(additionalData).forEach(([key, value]) => {
    formData.append(key, value)
  })

  const token = getToken()
  const headers = {}
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers,
    body: formData,
  })

  return handleResponse(response)
}

// Export utilities
export { ApiError, getToken, setTokens, clearTokens, API_BASE_URL }
export default api
