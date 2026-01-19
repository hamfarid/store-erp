// FILE: frontend/utils/csrf.js | PURPOSE: CSRF protection utilities | OWNER: Frontend Team | LAST-AUDITED: 2025-11-18

/**
 * CSRF Protection Utilities
 * 
 * Provides client-side CSRF token management for API requests.
 * Works with backend CSRF middleware to prevent CSRF attacks.
 * 
 * Version: 1.0.0
 */

/**
 * Get CSRF token from cookie
 * 
 * @returns {string|null} CSRF token or null if not found
 */
export function getCSRFToken() {
  const name = 'csrf_token';
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  
  return null;
}

/**
 * Set CSRF token in cookie
 * 
 * @param {string} token - CSRF token
 * @param {number} maxAge - Max age in seconds (default: 3600)
 */
export function setCSRFToken(token, maxAge = 3600) {
  document.cookie = `csrf_token=${token}; path=/; max-age=${maxAge}; SameSite=Strict; Secure`;
}

/**
 * Add CSRF token to request headers
 * 
 * @param {Object} headers - Existing headers object
 * @returns {Object} Headers with CSRF token added
 */
export function addCSRFHeader(headers = {}) {
  const token = getCSRFToken();
  
  if (token) {
    return {
      ...headers,
      'X-CSRF-Token': token
    };
  }
  
  return headers;
}

/**
 * Fetch CSRF token from server
 * 
 * @param {string} apiUrl - API base URL
 * @returns {Promise<string>} CSRF token
 */
export async function fetchCSRFToken(apiUrl = import.meta.env.VITE_API_URL) {
  try {
    const response = await fetch(`${apiUrl}/csrf-token`, {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data.csrf_token) {
        setCSRFToken(data.csrf_token);
        return data.csrf_token;
      }
    }
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error);
  }
  
  return null;
}

/**
 * Initialize CSRF protection
 * Call this when the app starts
 * 
 * @param {string} apiUrl - API base URL
 * @returns {Promise<void>}
 */
export async function initCSRFProtection(apiUrl = import.meta.env.VITE_API_URL) {
  // Check if token already exists
  let token = getCSRFToken();
  
  // If not, fetch from server
  if (!token) {
    token = await fetchCSRFToken(apiUrl);
  }
  
  // Set up automatic token refresh
  setInterval(async () => {
    await fetchCSRFToken(apiUrl);
  }, 30 * 60 * 1000); // Refresh every 30 minutes
}

/**
 * Make CSRF-protected API request
 * 
 * @param {string} url - Request URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} Fetch response
 */
export async function csrfFetch(url, options = {}) {
  // Add CSRF token to headers
  const headers = addCSRFHeader(options.headers || {});
  
  // Make request
  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include'
  });
  
  // If CSRF token is invalid, try to refresh and retry once
  if (response.status === 403) {
    const data = await response.json();
    if (data.code === 'CSRF_TOKEN_INVALID' || data.code === 'CSRF_TOKEN_MISSING') {
      // Fetch new token
      await fetchCSRFToken();
      
      // Retry request with new token
      const newHeaders = addCSRFHeader(options.headers || {});
      return fetch(url, {
        ...options,
        headers: newHeaders,
        credentials: 'include'
      });
    }
  }
  
  return response;
}

/**
 * CSRF-protected axios interceptor
 * Use this with axios instance
 * 
 * @param {Object} axiosInstance - Axios instance
 */
export function setupCSRFInterceptor(axiosInstance) {
  // Request interceptor - add CSRF token
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = getCSRFToken();
      if (token) {
        config.headers['X-CSRF-Token'] = token;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // Response interceptor - handle CSRF errors
  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      
      // If CSRF error and haven't retried yet
      if (
        error.response?.status === 403 &&
        error.response?.data?.code?.includes('CSRF') &&
        !originalRequest._retry
      ) {
        originalRequest._retry = true;
        
        // Fetch new token
        await fetchCSRFToken();
        
        // Retry request
        const token = getCSRFToken();
        if (token) {
          originalRequest.headers['X-CSRF-Token'] = token;
        }
        
        return axiosInstance(originalRequest);
      }
      
      return Promise.reject(error);
    }
  );
}

export default {
  getCSRFToken,
  setCSRFToken,
  addCSRFHeader,
  fetchCSRFToken,
  initCSRFProtection,
  csrfFetch,
  setupCSRFInterceptor
};

