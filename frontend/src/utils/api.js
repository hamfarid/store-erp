/**
 * API Utility Functions
 * Centralized API configuration and request handling
 * 
 * Environment Variables:
 * - VITE_API_BASE_URL: Base URL for API (includes /api)
 * 
 * Usage:
 * import { apiRequest, API_BASE_URL } from '../utils/api'
 * const data = await apiRequest('/products')
 */

// Get API base URL from environment variable
// Default to localhost:5005/api if not set
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5005/api'

/**
 * Make an API request
 * @param {string} endpoint - API endpoint (e.g., '/products', '/customers')
 * @param {object} options - Fetch options (method, headers, body, etc.)
 * @returns {Promise<any>} - Response data
 * @throws {Error} - If request fails
 */
export const apiRequest = async (endpoint, options = {}) => {
  // Ensure endpoint starts with /
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  
  // Build full URL
  const url = `${API_BASE_URL}${normalizedEndpoint}`
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })
    
    // Check if response is ok
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `API Error: ${response.status} ${response.statusText}`)
    }
    
    // Parse JSON response
    return await response.json()
  } catch (error) {
    console.error(`API Request Failed: ${url}`, error)
    throw error
  }
}

/**
 * Make a GET request
 * @param {string} endpoint - API endpoint
 * @param {object} options - Additional fetch options
 * @returns {Promise<any>} - Response data
 */
export const apiGet = async (endpoint, options = {}) => {
  return apiRequest(endpoint, {
    method: 'GET',
    ...options,
  })
}

/**
 * Make a POST request
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body data
 * @param {object} options - Additional fetch options
 * @returns {Promise<any>} - Response data
 */
export const apiPost = async (endpoint, data, options = {}) => {
  return apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
    ...options,
  })
}

/**
 * Make a PUT request
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body data
 * @param {object} options - Additional fetch options
 * @returns {Promise<any>} - Response data
 */
export const apiPut = async (endpoint, data, options = {}) => {
  return apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
    ...options,
  })
}

/**
 * Make a DELETE request
 * @param {string} endpoint - API endpoint
 * @param {object} options - Additional fetch options
 * @returns {Promise<any>} - Response data
 */
export const apiDelete = async (endpoint, options = {}) => {
  return apiRequest(endpoint, {
    method: 'DELETE',
    ...options,
  })
}

/**
 * Build query string from object
 * @param {object} params - Query parameters
 * @returns {string} - Query string (e.g., '?key1=value1&key2=value2')
 */
export const buildQueryString = (params) => {
  const searchParams = new URLSearchParams()
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      searchParams.append(key, value)
    }
  })
  
  const queryString = searchParams.toString()
  return queryString ? `?${queryString}` : ''
}

// Export API_BASE_URL for direct use if needed
export { API_BASE_URL }

// Export default object with all functions
export default {
  apiRequest,
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  buildQueryString,
  API_BASE_URL,
}

