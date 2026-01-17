/**
 * FILE: frontend/src/utils/traceId.js
 * PURPOSE: Generate and manage traceIds for distributed tracing across frontend and backend
 * OWNER: Frontend Team
 * RELATED: logger.js, api.js, apiClient.js, secureApi.js
 * LAST-AUDITED: 2025-10-23
 */

/**
 * Generate a unique traceId (UUID v4 format)
 * Used for distributed tracing across frontend and backend
 * @returns {string} UUID v4 format traceId
 */
export function generateTraceId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * Get or create traceId for current session
 * Stores in sessionStorage to maintain across page navigation
 * @returns {string} Current session traceId
 */
export function getSessionTraceId() {
  let traceId = sessionStorage.getItem('_trace_id');
  if (!traceId) {
    traceId = generateTraceId();
    sessionStorage.setItem('_trace_id', traceId);
  }
  return traceId;
}

/**
 * Create a new traceId for a specific operation/request
 * @param {string} operation - Operation name (e.g., 'login', 'fetch_products')
 * @returns {string} New traceId for this operation
 */
export function createOperationTraceId(operation = '') {
  const traceId = generateTraceId();
  const timestamp = Date.now();
  return `${traceId}-${operation}-${timestamp}`;
}

/**
 * Extract traceId from response headers
 * Backend may return X-Trace-Id or X-Request-Id header
 * @param {Headers|Object} headers - Response headers
 * @returns {string|null} TraceId from headers or null
 */
export function extractTraceIdFromHeaders(headers) {
  if (!headers) return null;
  
  // Try different header names (case-insensitive)
  const headerNames = ['x-trace-id', 'x-request-id', 'traceid', 'trace-id'];
  
  for (const name of headerNames) {
    const value = headers.get ? headers.get(name) : headers[name];
    if (value) return value;
  }
  
  return null;
}

/**
 * Store traceId in context for current request
 * @param {string} traceId - TraceId to store
 */
export function setCurrentTraceId(traceId) {
  sessionStorage.setItem('_current_trace_id', traceId);
}

/**
 * Get current traceId for ongoing request
 * @returns {string} Current traceId or session traceId
 */
export function getCurrentTraceId() {
  return sessionStorage.getItem('_current_trace_id') || getSessionTraceId();
}

/**
 * Clear current traceId (call after request completes)
 */
export function clearCurrentTraceId() {
  sessionStorage.removeItem('_current_trace_id');
}

/**
 * Create traceId context object for logging
 * @param {Object} options - Additional context options
 * @returns {Object} TraceId context with metadata
 */
export function createTraceContext(options = {}) {
  return {
    traceId: getCurrentTraceId(),
    sessionTraceId: getSessionTraceId(),
    timestamp: new Date().toISOString(),
    url: window.location.href,
    pathname: window.location.pathname,
    userAgent: navigator.userAgent,
    ...options
  };
}

/**
 * Format traceId for logging output
 * @param {string} traceId - TraceId to format
 * @returns {string} Formatted traceId for display
 */
export function formatTraceId(traceId) {
  if (!traceId) return 'NO_TRACE_ID';
  // Show first 8 chars and last 4 chars: xxxxxxxx...xxxx
  if (traceId.length > 16) {
    return `${traceId.substring(0, 8)}...${traceId.substring(traceId.length - 4)}`;
  }
  return traceId;
}

/**
 * Initialize traceId system on app startup
 * Call this in App.jsx or main.jsx
 */
export function initializeTraceIdSystem() {
  // Generate session traceId
  const sessionTraceId = getSessionTraceId();
  
  // Log initialization in development
  if (import.meta.env?.DEV) {
    console.debug(`[TraceId] Session initialized: ${formatTraceId(sessionTraceId)}`);
  }
  
  // Store in window for global access
  window.__TRACE_ID__ = {
    getSessionTraceId,
    getCurrentTraceId,
    generateTraceId,
    createOperationTraceId,
    createTraceContext,
    formatTraceId
  };
  
  return sessionTraceId;
}

export default {
  generateTraceId,
  getSessionTraceId,
  createOperationTraceId,
  extractTraceIdFromHeaders,
  setCurrentTraceId,
  getCurrentTraceId,
  clearCurrentTraceId,
  createTraceContext,
  formatTraceId,
  initializeTraceIdSystem
};

