/**
 * Formatters Utility
 * @file frontend/src/utils/formatters.js
 * 
 * دوال تنسيق البيانات للعرض
 */

/**
 * تنسيق الأرقام بالعملة
 * @param {number} amount - المبلغ
 * @param {string} currency - رمز العملة (EGP)
 * @param {string} locale - اللغة (ar-SA)
 * @returns {string}
 */
export function formatCurrency(amount, currency = 'EGP', locale = 'ar-SA') {
  if (amount === null || amount === undefined) return '-';
  
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  } catch {
    return `${amount.toFixed(2)} ${currency}`;
  }
}

/**
 * تنسيق الأرقام مع الفواصل
 * @param {number} number - الرقم
 * @param {number} decimals - عدد الخانات العشرية
 * @returns {string}
 */
export function formatNumber(number, decimals = 0) {
  if (number === null || number === undefined) return '-';
  
  try {
    return new Intl.NumberFormat('ar-SA', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(number);
  } catch {
    return number.toFixed(decimals);
  }
}

/**
 * تنسيق النسبة المئوية
 * @param {number} value - القيمة
 * @param {number} decimals - عدد الخانات العشرية
 * @returns {string}
 */
export function formatPercentage(value, decimals = 1) {
  if (value === null || value === undefined) return '-';
  return `${formatNumber(value, decimals)}%`;
}

/**
 * تنسيق التاريخ
 * @param {Date|string} date - التاريخ
 * @param {string} format - صيغة التاريخ
 * @returns {string}
 */
export function formatDate(date, format = 'short') {
  if (!date) return '-';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) return '-';
  
  const options = {
    short: { day: '2-digit', month: '2-digit', year: 'numeric' },
    medium: { day: 'numeric', month: 'short', year: 'numeric' },
    long: { day: 'numeric', month: 'long', year: 'numeric' },
    full: { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
  };
  
  try {
    return new Intl.DateTimeFormat('ar-SA', options[format] || options.short).format(d);
  } catch {
    return d.toLocaleDateString();
  }
}

/**
 * تنسيق الوقت
 * @param {Date|string} date - التاريخ/الوقت
 * @param {boolean} showSeconds - إظهار الثواني
 * @returns {string}
 */
export function formatTime(date, showSeconds = false) {
  if (!date) return '-';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) return '-';
  
  const options = {
    hour: '2-digit',
    minute: '2-digit',
    ...(showSeconds && { second: '2-digit' }),
    hour12: true
  };
  
  try {
    return new Intl.DateTimeFormat('ar-SA', options).format(d);
  } catch {
    return d.toLocaleTimeString();
  }
}

/**
 * تنسيق التاريخ والوقت معاً
 * @param {Date|string} date - التاريخ/الوقت
 * @returns {string}
 */
export function formatDateTime(date) {
  if (!date) return '-';
  return `${formatDate(date)} ${formatTime(date)}`;
}

/**
 * تنسيق الوقت النسبي
 * @param {Date|string} date - التاريخ
 * @returns {string}
 */
export function formatRelativeTime(date) {
  if (!date) return '-';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  if (isNaN(d.getTime())) return '-';
  
  const now = new Date();
  const diffMs = now - d;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffSecs < 60) return 'الآن';
  if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
  if (diffHours < 24) return `منذ ${diffHours} ساعة`;
  if (diffDays < 7) return `منذ ${diffDays} يوم`;
  if (diffDays < 30) return `منذ ${Math.floor(diffDays / 7)} أسبوع`;
  if (diffDays < 365) return `منذ ${Math.floor(diffDays / 30)} شهر`;
  return `منذ ${Math.floor(diffDays / 365)} سنة`;
}

/**
 * تنسيق رقم الهاتف السعودي
 * @param {string} phone - رقم الهاتف
 * @returns {string}
 */
export function formatPhoneNumber(phone) {
  if (!phone) return '-';
  
  // Remove non-digits
  const digits = phone.replace(/\D/g, '');
  
  // Format Saudi number
  if (digits.length === 10 && digits.startsWith('05')) {
    return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`;
  }
  if (digits.length === 12 && digits.startsWith('966')) {
    return `+${digits.slice(0, 3)} ${digits.slice(3, 5)} ${digits.slice(5, 8)} ${digits.slice(8)}`;
  }
  
  return phone;
}

/**
 * تنسيق رقم الفاتورة
 * @param {string|number} number - رقم الفاتورة
 * @param {string} prefix - البادئة
 * @param {number} padding - عدد الأصفار
 * @returns {string}
 */
export function formatInvoiceNumber(number, prefix = 'INV', padding = 6) {
  if (!number) return '-';
  const num = String(number).padStart(padding, '0');
  return `${prefix}-${num}`;
}

/**
 * تنسيق الباركود
 * @param {string} barcode - الباركود
 * @returns {string}
 */
export function formatBarcode(barcode) {
  if (!barcode) return '-';
  return barcode.replace(/(\d{4})(?=\d)/g, '$1-');
}

/**
 * تنسيق حجم الملف
 * @param {number} bytes - الحجم بالبايت
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 بايت';
  
  const units = ['بايت', 'ك.ب', 'م.ب', 'ج.ب', 'ت.ب'];
  const k = 1024;
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${units[i]}`;
}

/**
 * اقتطاع النص
 * @param {string} text - النص
 * @param {number} maxLength - الحد الأقصى
 * @param {string} suffix - اللاحقة
 * @returns {string}
 */
export function truncateText(text, maxLength = 50, suffix = '...') {
  if (!text) return '-';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - suffix.length) + suffix;
}

/**
 * تنسيق رقم الهوية/السجل التجاري
 * @param {string} id - الرقم
 * @returns {string}
 */
export function formatIdNumber(id) {
  if (!id) return '-';
  // Remove non-digits and format
  const digits = id.replace(/\D/g, '');
  if (digits.length === 10) {
    return `${digits.slice(0, 1)}-${digits.slice(1, 5)}-${digits.slice(5)}`;
  }
  return id;
}

/**
 * تحويل الحالة إلى نص عربي
 * @param {string} status - الحالة
 * @returns {string}
 */
export function formatStatus(status) {
  const statusMap = {
    active: 'نشط',
    inactive: 'غير نشط',
    pending: 'قيد الانتظار',
    completed: 'مكتمل',
    cancelled: 'ملغي',
    paid: 'مدفوع',
    unpaid: 'غير مدفوع',
    partial: 'جزئي',
    overdue: 'متأخر',
    draft: 'مسودة',
    approved: 'معتمد',
    rejected: 'مرفوض',
    in_stock: 'متوفر',
    out_of_stock: 'نفذ',
    low_stock: 'منخفض',
    expired: 'منتهي',
    valid: 'صالح'
  };
  
  return statusMap[status?.toLowerCase()] || status || '-';
}

/**
 * تنسيق قيمة منطقية
 * @param {boolean} value - القيمة
 * @returns {string}
 */
export function formatBoolean(value) {
  if (value === null || value === undefined) return '-';
  return value ? 'نعم' : 'لا';
}

/**
 * تنسيق المدة الزمنية
 * @param {number} minutes - الدقائق
 * @returns {string}
 */
export function formatDuration(minutes) {
  if (!minutes) return '-';
  
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours === 0) return `${mins} دقيقة`;
  if (mins === 0) return `${hours} ساعة`;
  return `${hours} ساعة و ${mins} دقيقة`;
}

export default {
  formatCurrency,
  formatNumber,
  formatPercentage,
  formatDate,
  formatTime,
  formatDateTime,
  formatRelativeTime,
  formatPhoneNumber,
  formatInvoiceNumber,
  formatBarcode,
  formatFileSize,
  truncateText,
  formatIdNumber,
  formatStatus,
  formatBoolean,
  formatDuration
};
