/**
 * Helper Utilities
 * @file frontend/src/utils/helpers.js
 * 
 * دوال مساعدة عامة
 */

/**
 * توليد معرف فريد
 * @returns {string}
 */
export function generateId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * توليد UUID
 * @returns {string}
 */
export function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * تأخير تنفيذ (Promise)
 * @param {number} ms - المللي ثانية
 * @returns {Promise}
 */
export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * نسخ نص للحافظة
 * @param {string} text - النص
 * @returns {Promise<boolean>}
 */
export async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    const success = document.execCommand('copy');
    document.body.removeChild(textArea);
    return success;
  } catch {
    return false;
  }
}

/**
 * تنزيل ملف
 * @param {string} filename - اسم الملف
 * @param {string|Blob} content - المحتوى
 * @param {string} mimeType - نوع الملف
 */
export function downloadFile(filename, content, mimeType = 'text/plain') {
  const blob = content instanceof Blob 
    ? content 
    : new Blob([content], { type: mimeType });
  
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * قراءة ملف كنص
 * @param {File} file - الملف
 * @returns {Promise<string>}
 */
export function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

/**
 * قراءة ملف كـ Data URL
 * @param {File} file - الملف
 * @returns {Promise<string>}
 */
export function readFileAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * دمج كائنين بعمق
 * @param {object} target - الهدف
 * @param {object} source - المصدر
 * @returns {object}
 */
export function deepMerge(target, source) {
  const output = { ...target };
  
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          output[key] = source[key];
        } else {
          output[key] = deepMerge(target[key], source[key]);
        }
      } else {
        output[key] = source[key];
      }
    });
  }
  
  return output;
}

/**
 * نسخ عميق لكائن
 * @param {any} obj - الكائن
 * @returns {any}
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  
  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof Array) return obj.map((item) => deepClone(item));
  
  if (obj instanceof Object) {
    const copy = {};
    Object.keys(obj).forEach((key) => {
      copy[key] = deepClone(obj[key]);
    });
    return copy;
  }
  
  return obj;
}

/**
 * التحقق من كون القيمة كائن
 * @param {any} item - القيمة
 * @returns {boolean}
 */
export function isObject(item) {
  return item && typeof item === 'object' && !Array.isArray(item);
}

/**
 * التحقق من كائن فارغ
 * @param {object} obj - الكائن
 * @returns {boolean}
 */
export function isEmptyObject(obj) {
  return obj && Object.keys(obj).length === 0 && obj.constructor === Object;
}

/**
 * الحصول على قيمة من مسار متداخل
 * @param {object} obj - الكائن
 * @param {string} path - المسار (مثل 'user.address.city')
 * @param {any} defaultValue - القيمة الافتراضية
 * @returns {any}
 */
export function getNestedValue(obj, path, defaultValue = undefined) {
  const keys = path.split('.');
  let result = obj;
  
  for (const key of keys) {
    if (result === null || result === undefined) return defaultValue;
    result = result[key];
  }
  
  return result === undefined ? defaultValue : result;
}

/**
 * تعيين قيمة في مسار متداخل
 * @param {object} obj - الكائن
 * @param {string} path - المسار
 * @param {any} value - القيمة
 * @returns {object}
 */
export function setNestedValue(obj, path, value) {
  const keys = path.split('.');
  const result = deepClone(obj);
  let current = result;
  
  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i];
    if (!current[key] || typeof current[key] !== 'object') {
      current[key] = {};
    }
    current = current[key];
  }
  
  current[keys[keys.length - 1]] = value;
  return result;
}

/**
 * إزالة القيم الفارغة من كائن
 * @param {object} obj - الكائن
 * @returns {object}
 */
export function removeEmptyValues(obj) {
  return Object.fromEntries(
    Object.entries(obj).filter(([_, v]) => v !== null && v !== undefined && v !== '')
  );
}

/**
 * تحويل مصفوفة إلى خريطة
 * @param {Array} array - المصفوفة
 * @param {string} key - المفتاح
 * @returns {object}
 */
export function arrayToMap(array, key = 'id') {
  return array.reduce((map, item) => {
    map[item[key]] = item;
    return map;
  }, {});
}

/**
 * تجميع مصفوفة حسب مفتاح
 * @param {Array} array - المصفوفة
 * @param {string|Function} key - المفتاح أو دالة
 * @returns {object}
 */
export function groupBy(array, key) {
  return array.reduce((groups, item) => {
    const groupKey = typeof key === 'function' ? key(item) : item[key];
    if (!groups[groupKey]) groups[groupKey] = [];
    groups[groupKey].push(item);
    return groups;
  }, {});
}

/**
 * ترتيب مصفوفة حسب مفتاح
 * @param {Array} array - المصفوفة
 * @param {string} key - المفتاح
 * @param {string} direction - الاتجاه (asc | desc)
 * @returns {Array}
 */
export function sortBy(array, key, direction = 'asc') {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return direction === 'asc' ? 1 : -1;
    return 0;
  });
}

/**
 * إزالة المكررات من مصفوفة
 * @param {Array} array - المصفوفة
 * @param {string} key - المفتاح (اختياري)
 * @returns {Array}
 */
export function uniqueBy(array, key = null) {
  if (!key) return [...new Set(array)];
  
  const seen = new Set();
  return array.filter((item) => {
    const val = item[key];
    if (seen.has(val)) return false;
    seen.add(val);
    return true;
  });
}

/**
 * حساب المجموع
 * @param {Array} array - المصفوفة
 * @param {string|Function} key - المفتاح أو دالة
 * @returns {number}
 */
export function sumBy(array, key) {
  return array.reduce((sum, item) => {
    const value = typeof key === 'function' ? key(item) : item[key];
    return sum + (Number(value) || 0);
  }, 0);
}

/**
 * إنشاء debounce لدالة
 * @param {Function} func - الدالة
 * @param {number} wait - وقت الانتظار
 * @returns {Function}
 */
export function debounce(func, wait = 300) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * إنشاء throttle لدالة
 * @param {Function} func - الدالة
 * @param {number} limit - الحد الزمني
 * @returns {Function}
 */
export function throttle(func, limit = 300) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * التحقق من صحة البريد الإلكتروني
 * @param {string} email - البريد
 * @returns {boolean}
 */
export function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

/**
 * التحقق من صحة رقم الهاتف السعودي
 * @param {string} phone - رقم الهاتف
 * @returns {boolean}
 */
export function isValidSaudiPhone(phone) {
  const re = /^(05|5|009665|9665|\+9665)\d{8}$/;
  return re.test(phone.replace(/\s|-/g, ''));
}

/**
 * تحويل الأرقام العربية إلى إنجليزية
 * @param {string} str - النص
 * @returns {string}
 */
export function arabicToEnglishNumbers(str) {
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return str.replace(/[٠-٩]/g, (d) => arabicNumbers.indexOf(d));
}

/**
 * تحويل الأرقام الإنجليزية إلى عربية
 * @param {string} str - النص
 * @returns {string}
 */
export function englishToArabicNumbers(str) {
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return str.replace(/[0-9]/g, (d) => arabicNumbers[parseInt(d)]);
}

export default {
  generateId,
  generateUUID,
  sleep,
  copyToClipboard,
  downloadFile,
  readFileAsText,
  readFileAsDataURL,
  deepMerge,
  deepClone,
  isObject,
  isEmptyObject,
  getNestedValue,
  setNestedValue,
  removeEmptyValues,
  arrayToMap,
  groupBy,
  sortBy,
  uniqueBy,
  sumBy,
  debounce,
  throttle,
  isValidEmail,
  isValidSaudiPhone,
  arabicToEnglishNumbers,
  englishToArabicNumbers
};
