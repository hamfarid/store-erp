/**
 * Session Security Service
 * حماية الجلسات من الاختراق والسرقة
 * 
 * Features:
 * - Session fingerprinting
 * - CSRF token management
 * - Token refresh mechanism
 * - Session timeout detection
 * - Activity monitoring
 * - Suspicious activity detection
 */

import apiClient from './apiClient';

// =====================================================
// Configuration
// =====================================================

const SESSION_CONFIG = {
  // Token refresh interval (14 minutes - before 15 min expiry)
  TOKEN_REFRESH_INTERVAL: 14 * 60 * 1000,
  
  // Session timeout (24 hours)
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000,
  
  // Activity check interval (1 minute)
  ACTIVITY_CHECK_INTERVAL: 60 * 1000,
  
  // Inactivity timeout (30 minutes)
  INACTIVITY_TIMEOUT: 30 * 60 * 1000,
  
  // Max failed refresh attempts
  MAX_REFRESH_ATTEMPTS: 3,
  
  // Storage keys
  KEYS: {
    TOKEN: 'token',
    REFRESH_TOKEN: 'refresh_token',
    USER: 'user',
    SESSION_ID: 'session_id',
    FINGERPRINT: 'session_fingerprint',
    LAST_ACTIVITY: 'last_activity',
    LOGIN_TIME: 'login_time',
    CSRF_TOKEN: 'csrf_token'
  }
};

// =====================================================
// Session Fingerprint
// =====================================================

/**
 * Generate a unique fingerprint for the current browser session
 * Used to detect session hijacking
 */
const generateFingerprint = () => {
  const components = [
    navigator.userAgent,
    navigator.language,
    screen.width + 'x' + screen.height,
    screen.colorDepth,
    new Date().getTimezoneOffset(),
    navigator.hardwareConcurrency || 'unknown',
    navigator.platform
  ];
  
  // Create a hash of the components
  const fingerprint = components.join('|');
  return btoa(fingerprint).substring(0, 32);
};

/**
 * Validate that the current fingerprint matches the stored one
 */
const validateFingerprint = () => {
  const storedFingerprint = localStorage.getItem(SESSION_CONFIG.KEYS.FINGERPRINT);
  if (!storedFingerprint) return true; // No fingerprint stored yet
  
  const currentFingerprint = generateFingerprint();
  return storedFingerprint === currentFingerprint;
};

// =====================================================
// CSRF Token Management
// =====================================================

/**
 * Get CSRF token from cookie or storage
 */
const getCSRFToken = () => {
  // Try to get from cookie first
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrf_token' || name === 'X-CSRF-Token') {
      return value;
    }
  }
  
  // Fallback to localStorage
  return localStorage.getItem(SESSION_CONFIG.KEYS.CSRF_TOKEN);
};

/**
 * Set CSRF token
 */
const setCSRFToken = (token) => {
  localStorage.setItem(SESSION_CONFIG.KEYS.CSRF_TOKEN, token);
};

/**
 * Fetch fresh CSRF token from server
 */
const refreshCSRFToken = async () => {
  try {
    const response = await apiClient.get('/api/auth/csrf-token');
    if (response.csrf_token) {
      setCSRFToken(response.csrf_token);
      return response.csrf_token;
    }
  } catch (error) {
    console.error('Failed to refresh CSRF token:', error);
  }
  return null;
};

// =====================================================
// Token Refresh Mechanism
// =====================================================

let refreshTokenTimeout = null;
let refreshAttempts = 0;

/**
 * Refresh the access token using the refresh token
 */
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem(SESSION_CONFIG.KEYS.REFRESH_TOKEN);
  
  if (!refreshToken) {
    console.warn('No refresh token available');
    return false;
  }
  
  try {
    const response = await apiClient.post('/api/auth/refresh', {
      refresh_token: refreshToken
    });
    
    if (response.success && response.data?.access_token) {
      localStorage.setItem(SESSION_CONFIG.KEYS.TOKEN, response.data.access_token);
      
      if (response.data.refresh_token) {
        localStorage.setItem(SESSION_CONFIG.KEYS.REFRESH_TOKEN, response.data.refresh_token);
      }
      
      refreshAttempts = 0;
      console.log('✅ Token refreshed successfully');
      return true;
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
    refreshAttempts++;
    
    if (refreshAttempts >= SESSION_CONFIG.MAX_REFRESH_ATTEMPTS) {
      console.error('Max refresh attempts reached, logging out');
      forceLogout('session_expired');
      return false;
    }
  }
  
  return false;
};

/**
 * Schedule automatic token refresh
 */
const scheduleTokenRefresh = () => {
  if (refreshTokenTimeout) {
    clearTimeout(refreshTokenTimeout);
  }
  
  refreshTokenTimeout = setTimeout(async () => {
    const success = await refreshAccessToken();
    if (success) {
      scheduleTokenRefresh();
    }
  }, SESSION_CONFIG.TOKEN_REFRESH_INTERVAL);
};

/**
 * Cancel scheduled token refresh
 */
const cancelTokenRefresh = () => {
  if (refreshTokenTimeout) {
    clearTimeout(refreshTokenTimeout);
    refreshTokenTimeout = null;
  }
};

// =====================================================
// Activity Monitoring
// =====================================================

let lastActivityTime = Date.now();
let activityCheckInterval = null;

/**
 * Update last activity time
 */
const updateActivity = () => {
  lastActivityTime = Date.now();
  localStorage.setItem(SESSION_CONFIG.KEYS.LAST_ACTIVITY, lastActivityTime.toString());
};

/**
 * Check for inactivity timeout
 */
const checkInactivity = () => {
  const storedLastActivity = localStorage.getItem(SESSION_CONFIG.KEYS.LAST_ACTIVITY);
  const lastActivity = storedLastActivity ? parseInt(storedLastActivity) : lastActivityTime;
  const now = Date.now();
  
  if (now - lastActivity > SESSION_CONFIG.INACTIVITY_TIMEOUT) {
    console.warn('Session inactive for too long');
    forceLogout('inactivity');
    return false;
  }
  
  return true;
};

/**
 * Start activity monitoring
 */
const startActivityMonitoring = () => {
  // Update activity on user interactions
  const events = ['mousedown', 'keydown', 'touchstart', 'scroll'];
  events.forEach(event => {
    document.addEventListener(event, updateActivity, { passive: true });
  });
  
  // Check for inactivity periodically
  activityCheckInterval = setInterval(() => {
    checkInactivity();
  }, SESSION_CONFIG.ACTIVITY_CHECK_INTERVAL);
  
  // Initial activity timestamp
  updateActivity();
};

/**
 * Stop activity monitoring
 */
const stopActivityMonitoring = () => {
  const events = ['mousedown', 'keydown', 'touchstart', 'scroll'];
  events.forEach(event => {
    document.removeEventListener(event, updateActivity);
  });
  
  if (activityCheckInterval) {
    clearInterval(activityCheckInterval);
    activityCheckInterval = null;
  }
};

// =====================================================
// Session Management
// =====================================================

/**
 * Initialize secure session after login
 */
const initializeSession = (userData, tokens) => {
  // Generate and store fingerprint
  const fingerprint = generateFingerprint();
  localStorage.setItem(SESSION_CONFIG.KEYS.FINGERPRINT, fingerprint);
  
  // Store session data
  localStorage.setItem(SESSION_CONFIG.KEYS.USER, JSON.stringify(userData));
  localStorage.setItem(SESSION_CONFIG.KEYS.TOKEN, tokens.access_token);
  localStorage.setItem(SESSION_CONFIG.KEYS.LOGIN_TIME, Date.now().toString());
  
  if (tokens.refresh_token) {
    localStorage.setItem(SESSION_CONFIG.KEYS.REFRESH_TOKEN, tokens.refresh_token);
  }
  
  if (tokens.session_id) {
    localStorage.setItem(SESSION_CONFIG.KEYS.SESSION_ID, tokens.session_id);
  }
  
  // Start security features
  scheduleTokenRefresh();
  startActivityMonitoring();
  
  console.log('✅ Secure session initialized');
};

/**
 * Validate current session security
 */
const validateSession = () => {
  const errors = [];
  
  // Check fingerprint
  if (!validateFingerprint()) {
    errors.push('fingerprint_mismatch');
  }
  
  // Check token existence
  if (!localStorage.getItem(SESSION_CONFIG.KEYS.TOKEN)) {
    errors.push('no_token');
  }
  
  // Check session timeout
  const loginTime = localStorage.getItem(SESSION_CONFIG.KEYS.LOGIN_TIME);
  if (loginTime && Date.now() - parseInt(loginTime) > SESSION_CONFIG.SESSION_TIMEOUT) {
    errors.push('session_expired');
  }
  
  // Check inactivity
  if (!checkInactivity()) {
    errors.push('inactive');
  }
  
  if (errors.length > 0) {
    console.warn('Session validation failed:', errors);
    return { valid: false, errors };
  }
  
  return { valid: true, errors: [] };
};

/**
 * Force logout due to security issue
 */
const forceLogout = (reason = 'unknown') => {
  console.warn('Force logout triggered:', reason);
  
  // Stop all background processes
  cancelTokenRefresh();
  stopActivityMonitoring();
  
  // Clear all session data
  Object.values(SESSION_CONFIG.KEYS).forEach(key => {
    localStorage.removeItem(key);
  });
  
  // Log security event
  logSecurityEvent('force_logout', { reason });
  
  // Redirect to login
  window.location.href = `/login?reason=${reason}`;
};

/**
 * Clean logout
 */
const cleanLogout = async () => {
  try {
    // Notify server
    await apiClient.post('/api/auth/logout');
  } catch (error) {
    console.error('Logout API error:', error);
  }
  
  // Stop background processes
  cancelTokenRefresh();
  stopActivityMonitoring();
  
  // Clear session data
  Object.values(SESSION_CONFIG.KEYS).forEach(key => {
    localStorage.removeItem(key);
  });
  
  console.log('✅ Clean logout completed');
};

// =====================================================
// Security Event Logging
// =====================================================

/**
 * Log security-related events
 */
const logSecurityEvent = async (eventType, details = {}) => {
  const event = {
    type: eventType,
    timestamp: new Date().toISOString(),
    fingerprint: generateFingerprint(),
    userAgent: navigator.userAgent,
    ...details
  };
  
  try {
    await apiClient.post('/api/security/log-event', event);
  } catch (error) {
    // Store locally if API fails
    const localLogs = JSON.parse(localStorage.getItem('security_logs') || '[]');
    localLogs.push(event);
    // Keep only last 100 events
    if (localLogs.length > 100) {
      localLogs.shift();
    }
    localStorage.setItem('security_logs', JSON.stringify(localLogs));
  }
};

// =====================================================
// Active Sessions Management
// =====================================================

/**
 * Get all active sessions for current user
 */
const getActiveSessions = async () => {
  try {
    const response = await apiClient.get('/api/auth/sessions');
    return response.sessions || [];
  } catch (error) {
    console.error('Failed to get active sessions:', error);
    return [];
  }
};

/**
 * Terminate a specific session
 */
const terminateSession = async (sessionId) => {
  try {
    await apiClient.delete(`/api/auth/sessions/${sessionId}`);
    return true;
  } catch (error) {
    console.error('Failed to terminate session:', error);
    return false;
  }
};

/**
 * Terminate all other sessions
 */
const terminateOtherSessions = async () => {
  try {
    await apiClient.post('/api/auth/sessions/terminate-others');
    return true;
  } catch (error) {
    console.error('Failed to terminate other sessions:', error);
    return false;
  }
};

// =====================================================
// Exports
// =====================================================

const sessionSecurity = {
  // Configuration
  CONFIG: SESSION_CONFIG,
  
  // Fingerprinting
  generateFingerprint,
  validateFingerprint,
  
  // CSRF
  getCSRFToken,
  setCSRFToken,
  refreshCSRFToken,
  
  // Token refresh
  refreshAccessToken,
  scheduleTokenRefresh,
  cancelTokenRefresh,
  
  // Activity monitoring
  updateActivity,
  checkInactivity,
  startActivityMonitoring,
  stopActivityMonitoring,
  
  // Session management
  initializeSession,
  validateSession,
  forceLogout,
  cleanLogout,
  
  // Security logging
  logSecurityEvent,
  
  // Active sessions
  getActiveSessions,
  terminateSession,
  terminateOtherSessions
};

export default sessionSecurity;

