// FILE: frontend/utils/sanitize.js | PURPOSE: XSS sanitization utilities | OWNER: Frontend Team | LAST-AUDITED: 2025-11-18

/**
 * XSS Sanitization Utilities
 * 
 * Provides comprehensive XSS protection for user input and HTML content.
 * Uses DOMPurify for HTML sanitization.
 * 
 * Version: 1.0.0
 */

import DOMPurify from 'dompurify';

/**
 * Sanitize HTML content
 * 
 * @param {string} html - HTML content to sanitize
 * @param {Object} options - DOMPurify options
 * @returns {string} Sanitized HTML
 */
export function sanitizeHTML(html, options = {}) {
  if (!html) return '';
  
  const defaultOptions = {
    ALLOWED_TAGS: [
      'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'span', 'div'
    ],
    ALLOWED_ATTR: ['href', 'title', 'class', 'id', 'style'],
    ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i,
    KEEP_CONTENT: true,
    RETURN_TRUSTED_TYPE: false
  };
  
  const config = { ...defaultOptions, ...options };
  
  return DOMPurify.sanitize(html, config);
}

/**
 * Sanitize plain text (escape HTML entities)
 * 
 * @param {string} text - Text to sanitize
 * @returns {string} Sanitized text
 */
export function sanitizeText(text) {
  if (!text) return '';
  
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Sanitize URL
 * 
 * @param {string} url - URL to sanitize
 * @returns {string} Sanitized URL or empty string if invalid
 */
export function sanitizeURL(url) {
  if (!url) return '';
  
  // Remove javascript:, data:, vbscript: protocols
  const dangerous = /^(javascript|data|vbscript):/i;
  if (dangerous.test(url)) {
    return '';
  }
  
  // Only allow http, https, mailto, tel
  const allowed = /^(https?|mailto|tel):/i;
  if (!allowed.test(url) && !url.startsWith('/') && !url.startsWith('#')) {
    return '';
  }
  
  return url;
}

/**
 * Sanitize object (recursively sanitize all string values)
 * 
 * @param {Object} obj - Object to sanitize
 * @param {Array<string>} htmlFields - Fields that can contain HTML
 * @returns {Object} Sanitized object
 */
export function sanitizeObject(obj, htmlFields = []) {
  if (!obj || typeof obj !== 'object') return obj;
  
  const sanitized = Array.isArray(obj) ? [] : {};
  
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'string') {
      // If field is in htmlFields, sanitize as HTML
      if (htmlFields.includes(key)) {
        sanitized[key] = sanitizeHTML(value);
      } else {
        // Otherwise, sanitize as plain text
        sanitized[key] = sanitizeText(value);
      }
    } else if (typeof value === 'object' && value !== null) {
      // Recursively sanitize nested objects
      sanitized[key] = sanitizeObject(value, htmlFields);
    } else {
      // Keep other types as-is
      sanitized[key] = value;
    }
  }
  
  return sanitized;
}

/**
 * Sanitize form data
 * 
 * @param {FormData|Object} formData - Form data to sanitize
 * @param {Array<string>} htmlFields - Fields that can contain HTML
 * @returns {Object} Sanitized form data
 */
export function sanitizeFormData(formData, htmlFields = []) {
  const data = {};
  
  if (formData instanceof FormData) {
    for (const [key, value] of formData.entries()) {
      if (typeof value === 'string') {
        data[key] = htmlFields.includes(key) 
          ? sanitizeHTML(value) 
          : sanitizeText(value);
      } else {
        data[key] = value;
      }
    }
  } else {
    return sanitizeObject(formData, htmlFields);
  }
  
  return data;
}

/**
 * Create safe HTML component for React
 * 
 * @param {string} html - HTML content
 * @param {Object} options - Sanitization options
 * @returns {Object} Object with __html property for dangerouslySetInnerHTML
 */
export function createSafeHTML(html, options = {}) {
  return {
    __html: sanitizeHTML(html, options)
  };
}

/**
 * Sanitize filename
 * 
 * @param {string} filename - Filename to sanitize
 * @returns {string} Sanitized filename
 */
export function sanitizeFilename(filename) {
  if (!filename) return '';
  
  // Remove path separators
  filename = filename.replace(/[/\\]/g, '');
  
  // Remove dangerous characters
  filename = filename.replace(/[<>:"|?*\x00-\x1f]/g, '');
  
  // Remove leading dots
  filename = filename.replace(/^\.+/, '');
  
  // Limit length
  if (filename.length > 255) {
    const ext = filename.split('.').pop();
    const name = filename.substring(0, 250);
    filename = `${name}.${ext}`;
  }
  
  return filename;
}

/**
 * Validate and sanitize email
 * 
 * @param {string} email - Email to validate
 * @returns {string} Sanitized email or empty string if invalid
 */
export function sanitizeEmail(email) {
  if (!email) return '';
  
  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return '';
  }
  
  // Sanitize
  return email.toLowerCase().trim();
}

/**
 * Configure DOMPurify hooks
 * Call this once when app initializes
 */
export function configureDOMPurify() {
  // Add hook to remove target="_blank" without rel="noopener noreferrer"
  DOMPurify.addHook('afterSanitizeAttributes', (node) => {
    if (node.tagName === 'A' && node.hasAttribute('target')) {
      node.setAttribute('rel', 'noopener noreferrer');
    }
  });
  
  // Add hook to enforce HTTPS for images
  DOMPurify.addHook('afterSanitizeAttributes', (node) => {
    if (node.tagName === 'IMG' && node.hasAttribute('src')) {
      const src = node.getAttribute('src');
      if (src && src.startsWith('http:')) {
        node.setAttribute('src', src.replace('http:', 'https:'));
      }
    }
  });
}

// Initialize DOMPurify configuration
configureDOMPurify();

export default {
  sanitizeHTML,
  sanitizeText,
  sanitizeURL,
  sanitizeObject,
  sanitizeFormData,
  createSafeHTML,
  sanitizeFilename,
  sanitizeEmail,
  configureDOMPurify
};

