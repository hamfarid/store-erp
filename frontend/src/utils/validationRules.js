/**
 * Form Validation Utilities
 * Provides comprehensive validation rules and error handling
 */
export const validationRules = {
  // Required field validation
  required: (value) => {
    if (typeof value === 'string') {
      return value.trim().length > 0 || 'هذا الحقل مطلوب';
    }
    return value !== null && value !== undefined || 'هذا الحقل مطلوب';
  },

  // Email validation
  email: (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value) || 'يرجى إدخال بريد إلكتروني صحيح';
  },

  // Phone validation (Saudi format)
  phone: (value) => {
    const phoneRegex = /^(\+966|0)(5|9)\d{8}$/;
    return phoneRegex.test(value.replace(/\s/g, '')) || 'يرجى إدخال رقم جوال صحيح';
  },

  // Password validation
  password: (value) => {
    if (value.length < 8) return 'كلمة المرور يجب أن تكون 8 أحرف على الأقل';
    if (!/[A-Z]/.test(value)) return 'يجب أن تحتوي على حرف كبير واحد على الأقل';
    if (!/[a-z]/.test(value)) return 'يجب أن تحتوي على حرف صغير واحد على الأقل';
    if (!/[0-9]/.test(value)) return 'يجب أن تحتوي على رقم واحد على الأقل';
    return true;
  },

  // Number validation
  number: (value) => {
    return !isNaN(value) && value !== '' || 'يجب إدخال رقم صحيح';
  },

  // Positive number
  positiveNumber: (value) => {
    const num = parseFloat(value);
    return (!isNaN(num) && num > 0) || 'يجب إدخال رقم موجب';
  },

  // URL validation
  url: (value) => {
    try {
      new URL(value);
      return true;
    } catch {
      return 'يرجى إدخال عنوان URL صحيح';
    }
  },

  // Date validation
  date: (value) => {
    const date = new Date(value);
    return (!isNaN(date.getTime())) || 'يرجى إدخال تاريخ صحيح';
  },

  // Min length
  minLength: (min) => (value) => {
    return value.length >= min || `يجب أن يكون الطول ${min} أحرف على الأقل`;
  },

  // Max length
  maxLength: (max) => (value) => {
    return value.length <= max || `يجب ألا يتجاوز الطول ${max} أحرف`;
  },

  // Min value
  min: (minVal) => (value) => {
    return parseFloat(value) >= minVal || `يجب أن تكون القيمة ${minVal} على الأقل`;
  },

  // Max value
  max: (maxVal) => (value) => {
    return parseFloat(value) <= maxVal || `يجب ألا تتجاوز القيمة ${maxVal}`;
  },

  // Range value
  range: (min, max) => (value) => {
    const num = parseFloat(value);
    return (num >= min && num <= max) || `يجب أن تكون القيمة بين ${min} و ${max}`;
  },

  // Username validation
  username: (value) => {
    const usernameRegex = /^[a-zA-Z0-9_-]{3,20}$/;
    return usernameRegex.test(value) || 'اسم المستخدم يجب أن يكون بين 3-20 حرف وأرقام وشرطة سفلية فقط';
  },

  // Specific value match
  match: (matchValue) => (value) => {
    return value === matchValue || 'القيمتان غير متطابقتان';
  },

  // Custom regex
  pattern: (pattern, message) => (value) => {
    return pattern.test(value) || message;
  },
};

/**
 * Validate a value against multiple validators
 * @param {*} value - The value to validate
 * @param {Array<Function>} validators - Array of validator functions
 * @returns {true|string} - True if valid, error message if invalid
 */
export const validateValue = (value, validators) => {
  if (!validators || validators.length === 0) {
    return true;
  }

  for (const validator of validators) {
    const result = validator(value);
    if (result !== true) {
      return result;
    }
  }

  return true;
};

/**
 * Validate all form fields
 * @param {Object} values - Form values object
 * @param {Object} fieldValidators - Object with field names as keys and validator arrays as values
 * @returns {Object} - Object with field names and error messages
 */
export const validateForm = (values, fieldValidators) => {
  const errors = {};

  for (const [fieldName, validators] of Object.entries(fieldValidators)) {
    const result = validateValue(values[fieldName], validators);
    if (result !== true) {
      errors[fieldName] = result;
    }
  }

  return errors;
};

export default validationRules;
