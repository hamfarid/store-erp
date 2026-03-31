/**
 * Storage Utilities
 * Safe localStorage and sessionStorage operations with fallbacks.
 */

const STORAGE_PREFIX = 'store_erp_';

/**
 * Check if localStorage is available
 * @returns {boolean} True if available
 */
const isLocalStorageAvailable = () => {
  try {
    const test = '__storage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
};

/**
 * In-memory fallback storage
 */
const memoryStorage = new Map();

/**
 * Get item from storage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if not found
 * @returns {any} Stored value or default
 */
export const getItem = (key, defaultValue = null) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    if (isLocalStorageAvailable()) {
      const item = localStorage.getItem(prefixedKey);
      if (item === null) return defaultValue;
      return JSON.parse(item);
    } else {
      return memoryStorage.get(prefixedKey) ?? defaultValue;
    }
  } catch (error) {
    console.warn(`Error reading from storage: ${key}`, error);
    return defaultValue;
  }
};

/**
 * Set item in storage
 * @param {string} key - Storage key
 * @param {any} value - Value to store
 * @returns {boolean} True if successful
 */
export const setItem = (key, value) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    const serialized = JSON.stringify(value);
    
    if (isLocalStorageAvailable()) {
      localStorage.setItem(prefixedKey, serialized);
    } else {
      memoryStorage.set(prefixedKey, value);
    }
    return true;
  } catch (error) {
    console.warn(`Error writing to storage: ${key}`, error);
    return false;
  }
};

/**
 * Remove item from storage
 * @param {string} key - Storage key
 * @returns {boolean} True if successful
 */
export const removeItem = (key) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    if (isLocalStorageAvailable()) {
      localStorage.removeItem(prefixedKey);
    } else {
      memoryStorage.delete(prefixedKey);
    }
    return true;
  } catch (error) {
    console.warn(`Error removing from storage: ${key}`, error);
    return false;
  }
};

/**
 * Clear all items with prefix
 * @returns {boolean} True if successful
 */
export const clearAll = () => {
  try {
    if (isLocalStorageAvailable()) {
      Object.keys(localStorage)
        .filter(key => key.startsWith(STORAGE_PREFIX))
        .forEach(key => localStorage.removeItem(key));
    } else {
      memoryStorage.clear();
    }
    return true;
  } catch (error) {
    console.warn('Error clearing storage', error);
    return false;
  }
};

/**
 * Get all keys with prefix
 * @returns {string[]} Array of keys
 */
export const getAllKeys = () => {
  try {
    if (isLocalStorageAvailable()) {
      return Object.keys(localStorage)
        .filter(key => key.startsWith(STORAGE_PREFIX))
        .map(key => key.replace(STORAGE_PREFIX, ''));
    } else {
      return Array.from(memoryStorage.keys())
        .map(key => key.replace(STORAGE_PREFIX, ''));
    }
  } catch (error) {
    console.warn('Error getting storage keys', error);
    return [];
  }
};

// Session Storage Functions

/**
 * Get item from session storage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if not found
 * @returns {any} Stored value or default
 */
export const getSessionItem = (key, defaultValue = null) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    const item = sessionStorage.getItem(prefixedKey);
    if (item === null) return defaultValue;
    return JSON.parse(item);
  } catch (error) {
    console.warn(`Error reading from session storage: ${key}`, error);
    return defaultValue;
  }
};

/**
 * Set item in session storage
 * @param {string} key - Storage key
 * @param {any} value - Value to store
 * @returns {boolean} True if successful
 */
export const setSessionItem = (key, value) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    sessionStorage.setItem(prefixedKey, JSON.stringify(value));
    return true;
  } catch (error) {
    console.warn(`Error writing to session storage: ${key}`, error);
    return false;
  }
};

/**
 * Remove item from session storage
 * @param {string} key - Storage key
 * @returns {boolean} True if successful
 */
export const removeSessionItem = (key) => {
  const prefixedKey = STORAGE_PREFIX + key;
  
  try {
    sessionStorage.removeItem(prefixedKey);
    return true;
  } catch (error) {
    console.warn(`Error removing from session storage: ${key}`, error);
    return false;
  }
};

// Convenience functions for common items

/**
 * Get auth token
 * @returns {string|null} Auth token or null
 */
export const getToken = () => getItem('access_token');

/**
 * Set auth token
 * @param {string} token - Auth token
 */
export const setToken = (token) => setItem('access_token', token);

/**
 * Remove auth token
 */
export const removeToken = () => removeItem('access_token');

/**
 * Get refresh token
 * @returns {string|null} Refresh token or null
 */
export const getRefreshToken = () => getItem('refresh_token');

/**
 * Set refresh token
 * @param {string} token - Refresh token
 */
export const setRefreshToken = (token) => setItem('refresh_token', token);

/**
 * Remove refresh token
 */
export const removeRefreshToken = () => removeItem('refresh_token');

/**
 * Get user data
 * @returns {Object|null} User data or null
 */
export const getUser = () => getItem('user');

/**
 * Set user data
 * @param {Object} user - User data
 */
export const setUser = (user) => setItem('user', user);

/**
 * Remove user data
 */
export const removeUser = () => removeItem('user');

/**
 * Get theme preference
 * @returns {string} Theme ('light' or 'dark')
 */
export const getTheme = () => getItem('theme', 'light');

/**
 * Set theme preference
 * @param {string} theme - Theme ('light' or 'dark')
 */
export const setTheme = (theme) => setItem('theme', theme);

/**
 * Get language preference
 * @returns {string} Language code
 */
export const getLanguage = () => getItem('language', 'ar');

/**
 * Set language preference
 * @param {string} language - Language code
 */
export const setLanguage = (language) => setItem('language', language);

/**
 * Clear auth data (logout)
 */
export const clearAuthData = () => {
  removeToken();
  removeRefreshToken();
  removeUser();
  removeSessionItem('cart');
};

export default {
  getItem,
  setItem,
  removeItem,
  clearAll,
  getAllKeys,
  getSessionItem,
  setSessionItem,
  removeSessionItem,
  getToken,
  setToken,
  removeToken,
  getRefreshToken,
  setRefreshToken,
  removeRefreshToken,
  getUser,
  setUser,
  removeUser,
  getTheme,
  setTheme,
  getLanguage,
  setLanguage,
  clearAuthData
};
