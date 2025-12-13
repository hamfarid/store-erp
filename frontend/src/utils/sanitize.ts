/**
 * P1.37: Frontend Input Sanitization Utilities
 * 
 * Provides comprehensive input sanitization to prevent XSS and injection attacks.
 * Should be used before displaying user-generated content or sending to API.
 */

// =============================================================================
// HTML Entity Encoding
// =============================================================================

const HTML_ENTITIES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#x27;',
  '/': '&#x2F;',
  '`': '&#x60;',
  '=': '&#x3D;',
};

const HTML_ENTITY_REGEX = /[&<>"'`=/]/g;

/**
 * Escape HTML entities to prevent XSS.
 */
export function escapeHtml(str: string): string {
  if (typeof str !== 'string') {
    return '';
  }
  return str.replace(HTML_ENTITY_REGEX, (char) => HTML_ENTITIES[char] || char);
}

/**
 * Unescape HTML entities (use with caution).
 */
export function unescapeHtml(str: string): string {
  if (typeof str !== 'string') {
    return '';
  }
  
  const doc = new DOMParser().parseFromString(str, 'text/html');
  return doc.documentElement.textContent || '';
}

// =============================================================================
// XSS Prevention
// =============================================================================

// Dangerous patterns that could indicate XSS attempts
const XSS_PATTERNS = [
  /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
  /javascript:/gi,
  /vbscript:/gi,
  /data:/gi,
  /on\w+\s*=/gi,
  /<iframe/gi,
  /<embed/gi,
  /<object/gi,
  /<link/gi,
  /<style/gi,
  /<meta/gi,
  /<base/gi,
  /expression\s*\(/gi,
  /url\s*\(/gi,
];

/**
 * Remove potentially dangerous content from a string.
 */
export function stripXss(str: string): string {
  if (typeof str !== 'string') {
    return '';
  }
  
  let result = str;
  
  // Remove dangerous patterns
  for (const pattern of XSS_PATTERNS) {
    result = result.replace(pattern, '');
  }
  
  // Remove null bytes
  result = result.replace(/\0/g, '');
  
  return result;
}

/**
 * Sanitize HTML content, keeping only safe tags.
 */
export function sanitizeHtml(
  html: string,
  allowedTags: string[] = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li']
): string {
  if (typeof html !== 'string') {
    return '';
  }
  
  // Create a temporary element
  const temp = document.createElement('div');
  temp.innerHTML = html;
  
  // Remove script tags and event handlers
  const scripts = temp.querySelectorAll('script');
  scripts.forEach((script) => script.remove());
  
  // Remove all elements not in allowed list
  const allElements = temp.querySelectorAll('*');
  allElements.forEach((el) => {
    const tagName = el.tagName.toLowerCase();
    
    if (!allowedTags.includes(tagName)) {
      // Replace with text content
      const text = document.createTextNode(el.textContent || '');
      el.parentNode?.replaceChild(text, el);
    } else {
      // Remove all attributes except safe ones
      const safeAttrs = ['href', 'title', 'alt'];
      const attrs = Array.from(el.attributes);
      
      attrs.forEach((attr) => {
        if (!safeAttrs.includes(attr.name.toLowerCase())) {
          el.removeAttribute(attr.name);
        } else if (attr.name.toLowerCase() === 'href') {
          // Validate href
          const href = attr.value.toLowerCase();
          if (href.startsWith('javascript:') || href.startsWith('data:')) {
            el.removeAttribute(attr.name);
          }
        }
      });
    }
  });
  
  return temp.innerHTML;
}

// =============================================================================
// Text Sanitization
// =============================================================================

/**
 * Sanitize plain text input.
 */
export function sanitizeText(str: string, options: {
  maxLength?: number;
  trim?: boolean;
  lowercase?: boolean;
  removeSpecialChars?: boolean;
} = {}): string {
  if (typeof str !== 'string') {
    return '';
  }
  
  const {
    maxLength,
    trim = true,
    lowercase = false,
    removeSpecialChars = false,
  } = options;
  
  let result = str;
  
  // Remove null bytes and control characters
  result = result.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  
  // Trim whitespace
  if (trim) {
    result = result.trim();
  }
  
  // Convert to lowercase
  if (lowercase) {
    result = result.toLowerCase();
  }
  
  // Remove special characters
  if (removeSpecialChars) {
    result = result.replace(/[^\w\s\u0600-\u06FF]/g, '');
  }
  
  // Limit length
  if (maxLength && result.length > maxLength) {
    result = result.substring(0, maxLength);
  }
  
  return result;
}

// =============================================================================
// URL Sanitization
// =============================================================================

const SAFE_URL_PROTOCOLS = ['http:', 'https:', 'mailto:', 'tel:'];

/**
 * Sanitize a URL, removing dangerous protocols.
 */
export function sanitizeUrl(url: string): string {
  if (typeof url !== 'string') {
    return '';
  }
  
  const trimmed = url.trim();
  
  // Check for dangerous protocols
  const lowercased = trimmed.toLowerCase();
  
  if (lowercased.startsWith('javascript:') ||
      lowercased.startsWith('vbscript:') ||
      lowercased.startsWith('data:')) {
    return '';
  }
  
  // Validate URL
  try {
    const parsed = new URL(trimmed, window.location.origin);
    
    if (!SAFE_URL_PROTOCOLS.includes(parsed.protocol)) {
      return '';
    }
    
    return parsed.href;
  } catch {
    // Relative URL - check for protocol injection
    if (lowercased.includes(':')) {
      const colonIndex = lowercased.indexOf(':');
      const beforeColon = lowercased.substring(0, colonIndex);
      if (!/^[a-z]+$/.test(beforeColon) || !SAFE_URL_PROTOCOLS.includes(beforeColon + ':')) {
        return '';
      }
    }
    
    return trimmed;
  }
}

// =============================================================================
// Form Input Sanitization
// =============================================================================

/**
 * Sanitize email address.
 */
export function sanitizeEmail(email: string): string {
  if (typeof email !== 'string') {
    return '';
  }
  
  // Remove whitespace and convert to lowercase
  let result = email.trim().toLowerCase();
  
  // Remove any HTML
  result = stripXss(result);
  
  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(result)) {
    return '';
  }
  
  return result;
}

/**
 * Sanitize phone number.
 */
export function sanitizePhone(phone: string): string {
  if (typeof phone !== 'string') {
    return '';
  }
  
  // Keep only digits, plus sign, spaces, and dashes
  return phone.replace(/[^\d+\-\s()]/g, '').trim();
}

/**
 * Sanitize numeric input.
 */
export function sanitizeNumber(
  value: string | number,
  options: {
    min?: number;
    max?: number;
    decimals?: number;
    allowNegative?: boolean;
  } = {}
): number | null {
  const { min, max, decimals, allowNegative = true } = options;
  
  let num: number;
  
  if (typeof value === 'number') {
    num = value;
  } else if (typeof value === 'string') {
    // Remove non-numeric characters except decimal point and minus
    const cleaned = value.replace(/[^\d.-]/g, '');
    num = parseFloat(cleaned);
  } else {
    return null;
  }
  
  if (isNaN(num) || !isFinite(num)) {
    return null;
  }
  
  // Check negative
  if (!allowNegative && num < 0) {
    num = Math.abs(num);
  }
  
  // Apply min/max
  if (min !== undefined && num < min) {
    num = min;
  }
  if (max !== undefined && num > max) {
    num = max;
  }
  
  // Apply decimal places
  if (decimals !== undefined) {
    num = parseFloat(num.toFixed(decimals));
  }
  
  return num;
}

/**
 * Sanitize search query.
 */
export function sanitizeSearchQuery(query: string): string {
  if (typeof query !== 'string') {
    return '';
  }
  
  // Remove XSS attempts
  let result = stripXss(query);
  
  // Remove SQL injection patterns
  result = result.replace(/['";\\]/g, '');
  
  // Remove excessive whitespace
  result = result.replace(/\s+/g, ' ').trim();
  
  // Limit length
  if (result.length > 200) {
    result = result.substring(0, 200);
  }
  
  return result;
}

// =============================================================================
// Object Sanitization
// =============================================================================

/**
 * Deep sanitize an object, escaping all string values.
 */
export function sanitizeObject<T extends Record<string, unknown>>(
  obj: T,
  options: {
    escapeHtml?: boolean;
    stripXss?: boolean;
    maxDepth?: number;
  } = {}
): T {
  const { escapeHtml: shouldEscape = true, stripXss: shouldStrip = true, maxDepth = 10 } = options;
  
  function sanitizeValue(value: unknown, depth: number): unknown {
    if (depth > maxDepth) {
      return value;
    }
    
    if (typeof value === 'string') {
      let result = value;
      if (shouldStrip) {
        result = stripXss(result);
      }
      if (shouldEscape) {
        result = escapeHtml(result);
      }
      return result;
    }
    
    if (Array.isArray(value)) {
      return value.map((item) => sanitizeValue(item, depth + 1));
    }
    
    if (value !== null && typeof value === 'object') {
      const sanitized: Record<string, unknown> = {};
      for (const [key, val] of Object.entries(value)) {
        sanitized[key] = sanitizeValue(val, depth + 1);
      }
      return sanitized;
    }
    
    return value;
  }
  
  return sanitizeValue(obj, 0) as T;
}

// =============================================================================
// React Component Helpers
// =============================================================================

/**
 * Create safe innerHTML object for React.
 */
export function createSafeHtml(html: string): { __html: string } {
  return { __html: sanitizeHtml(html) };
}

/**
 * Safe text display component helper.
 */
export function safeText(text: string): string {
  return escapeHtml(sanitizeText(text));
}

// =============================================================================
// Input Validation Helpers
// =============================================================================

/**
 * Check if a string contains any potential XSS.
 */
export function containsXss(str: string): boolean {
  if (typeof str !== 'string') {
    return false;
  }
  
  for (const pattern of XSS_PATTERNS) {
    if (pattern.test(str)) {
      return true;
    }
  }
  
  return false;
}

/**
 * Check if a string contains SQL injection patterns.
 */
export function containsSqlInjection(str: string): boolean {
  if (typeof str !== 'string') {
    return false;
  }
  
  const sqlPatterns = [
    /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)/gi,
    /(--|\bOR\b.*=|'\s*OR\s*')/gi,
    /(\bEXEC\b|\bEXECUTE\b|\bxp_)/gi,
  ];
  
  for (const pattern of sqlPatterns) {
    if (pattern.test(str)) {
      return true;
    }
  }
  
  return false;
}

// =============================================================================
// Exports
// =============================================================================

export default {
  escapeHtml,
  unescapeHtml,
  stripXss,
  sanitizeHtml,
  sanitizeText,
  sanitizeUrl,
  sanitizeEmail,
  sanitizePhone,
  sanitizeNumber,
  sanitizeSearchQuery,
  sanitizeObject,
  createSafeHtml,
  safeText,
  containsXss,
  containsSqlInjection,
};

