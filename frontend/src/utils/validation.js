/**
 * Validation Utilities
 * Common validation functions for forms and data.
 */

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate phone number (Saudi/Egyptian format)
 * @param {string} phone - Phone number to validate
 * @returns {boolean} True if valid
 */
export const isValidPhone = (phone) => {
  // Saudi: 05xxxxxxxx or +9665xxxxxxxx
  // Egyptian: 01xxxxxxxx or +201xxxxxxxx
  const phoneRegex = /^(\+?966|0)?5\d{8}$|^(\+?20|0)?1[0125]\d{8}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};

/**
 * Validate Saudi National ID
 * @param {string} id - National ID to validate
 * @returns {boolean} True if valid
 */
export const isValidNationalId = (id) => {
  if (!id || id.length !== 10) return false;
  
  // Saudi ID starts with 1 or 2
  if (!/^[12]\d{9}$/.test(id)) return false;
  
  // Luhn algorithm validation
  let sum = 0;
  for (let i = 0; i < 10; i++) {
    let digit = parseInt(id[i]);
    if (i % 2 === 0) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    sum += digit;
  }
  
  return sum % 10 === 0;
};

/**
 * Validate Commercial Registration (CR) number
 * @param {string} cr - CR number to validate
 * @returns {boolean} True if valid
 */
export const isValidCR = (cr) => {
  // Saudi CR is 10 digits starting with 10
  return /^10\d{8}$/.test(cr);
};

/**
 * Validate VAT number
 * @param {string} vat - VAT number to validate
 * @returns {boolean} True if valid
 */
export const isValidVAT = (vat) => {
  // Saudi VAT is 15 digits starting with 3
  return /^3\d{14}$/.test(vat);
};

/**
 * Validate barcode (EAN-13 or EAN-8)
 * @param {string} barcode - Barcode to validate
 * @returns {boolean} True if valid
 */
export const isValidBarcode = (barcode) => {
  if (!barcode) return false;
  
  // EAN-8 or EAN-13
  if (!/^\d{8}$|^\d{13}$/.test(barcode)) return false;
  
  // Check digit validation
  const digits = barcode.split('').map(Number);
  const checkDigit = digits.pop();
  
  let sum = 0;
  const isEAN13 = digits.length === 12;
  
  digits.forEach((digit, index) => {
    if (isEAN13) {
      sum += digit * (index % 2 === 0 ? 1 : 3);
    } else {
      sum += digit * (index % 2 === 0 ? 3 : 1);
    }
  });
  
  const calculatedCheck = (10 - (sum % 10)) % 10;
  return calculatedCheck === checkDigit;
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} Validation result with score and issues
 */
export const validatePassword = (password) => {
  const issues = [];
  let score = 0;
  
  if (!password) {
    return { valid: false, score: 0, issues: ['كلمة المرور مطلوبة'] };
  }
  
  if (password.length >= 8) score += 1;
  else issues.push('يجب أن تكون 8 أحرف على الأقل');
  
  if (/[A-Z]/.test(password)) score += 1;
  else issues.push('يجب أن تحتوي على حرف كبير');
  
  if (/[a-z]/.test(password)) score += 1;
  else issues.push('يجب أن تحتوي على حرف صغير');
  
  if (/[0-9]/.test(password)) score += 1;
  else issues.push('يجب أن تحتوي على رقم');
  
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1;
  else issues.push('يجب أن تحتوي على رمز خاص');
  
  return {
    valid: score >= 4,
    score,
    strength: score <= 2 ? 'weak' : score <= 3 ? 'medium' : 'strong',
    issues
  };
};

/**
 * Validate required field
 * @param {any} value - Value to check
 * @param {string} fieldName - Field name for error message
 * @returns {string|null} Error message or null if valid
 */
export const validateRequired = (value, fieldName = 'هذا الحقل') => {
  if (value === null || value === undefined || value === '') {
    return `${fieldName} مطلوب`;
  }
  return null;
};

/**
 * Validate minimum length
 * @param {string} value - Value to check
 * @param {number} min - Minimum length
 * @param {string} fieldName - Field name for error message
 * @returns {string|null} Error message or null if valid
 */
export const validateMinLength = (value, min, fieldName = 'هذا الحقل') => {
  if (value && value.length < min) {
    return `${fieldName} يجب أن يكون ${min} أحرف على الأقل`;
  }
  return null;
};

/**
 * Validate maximum length
 * @param {string} value - Value to check
 * @param {number} max - Maximum length
 * @param {string} fieldName - Field name for error message
 * @returns {string|null} Error message or null if valid
 */
export const validateMaxLength = (value, max, fieldName = 'هذا الحقل') => {
  if (value && value.length > max) {
    return `${fieldName} يجب ألا يتجاوز ${max} حرف`;
  }
  return null;
};

/**
 * Validate number range
 * @param {number} value - Value to check
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @param {string} fieldName - Field name for error message
 * @returns {string|null} Error message or null if valid
 */
export const validateRange = (value, min, max, fieldName = 'القيمة') => {
  const num = parseFloat(value);
  if (isNaN(num)) {
    return `${fieldName} يجب أن يكون رقماً`;
  }
  if (num < min) {
    return `${fieldName} يجب أن يكون ${min} على الأقل`;
  }
  if (num > max) {
    return `${fieldName} يجب ألا يتجاوز ${max}`;
  }
  return null;
};

/**
 * Validate date
 * @param {string|Date} date - Date to validate
 * @returns {boolean} True if valid
 */
export const isValidDate = (date) => {
  if (!date) return false;
  const d = new Date(date);
  return !isNaN(d.getTime());
};

/**
 * Validate date is in future
 * @param {string|Date} date - Date to validate
 * @returns {boolean} True if in future
 */
export const isFutureDate = (date) => {
  if (!isValidDate(date)) return false;
  return new Date(date) > new Date();
};

/**
 * Validate date is in past
 * @param {string|Date} date - Date to validate
 * @returns {boolean} True if in past
 */
export const isPastDate = (date) => {
  if (!isValidDate(date)) return false;
  return new Date(date) < new Date();
};

/**
 * Validate quantity is positive
 * @param {number} quantity - Quantity to validate
 * @returns {string|null} Error message or null if valid
 */
export const validateQuantity = (quantity) => {
  const num = parseFloat(quantity);
  if (isNaN(num)) {
    return 'الكمية يجب أن تكون رقماً';
  }
  if (num <= 0) {
    return 'الكمية يجب أن تكون أكبر من صفر';
  }
  return null;
};

/**
 * Validate price
 * @param {number} price - Price to validate
 * @returns {string|null} Error message or null if valid
 */
export const validatePrice = (price) => {
  const num = parseFloat(price);
  if (isNaN(num)) {
    return 'السعر يجب أن يكون رقماً';
  }
  if (num < 0) {
    return 'السعر يجب أن يكون صفر أو أكبر';
  }
  return null;
};

export default {
  isValidEmail,
  isValidPhone,
  isValidNationalId,
  isValidCR,
  isValidVAT,
  isValidBarcode,
  validatePassword,
  validateRequired,
  validateMinLength,
  validateMaxLength,
  validateRange,
  isValidDate,
  isFutureDate,
  isPastDate,
  validateQuantity,
  validatePrice
};
