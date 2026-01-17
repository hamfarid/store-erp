/**
 * دوال مساعدة للتعامل مع ردود API الموحدة
 * 
 * يدعم كلاً من:
 * - الصيغة الجديدة: { status: 'success'|'error', ... }
 * - الصيغة القديمة: { success: true|false, ... }
 */

/**
 * التحقق من نجاح الرد
 * @param {Object} response - رد API
 * @returns {boolean} - true إذا كان الرد ناجحاً
 */
export const isSuccess = (response) => {
  if (!response || typeof response !== 'object') {
    return false;
  }
  
  // الصيغة الجديدة
  if ('status' in response) {
    return response.status === 'success';
  }
  
  // الصيغة القديمة (للتوافق العكسي)
  if ('success' in response) {
    return response.success === true;
  }
  
  return false;
};

/**
 * التحقق من فشل الرد
 * @param {Object} response - رد API
 * @returns {boolean} - true إذا كان الرد فاشلاً
 */
export const isError = (response) => {
  if (!response || typeof response !== 'object') {
    return true;
  }
  
  // الصيغة الجديدة
  if ('status' in response) {
    return response.status === 'error';
  }
  
  // الصيغة القديمة (للتوافق العكسي)
  if ('success' in response) {
    return response.success === false;
  }
  
  return false;
};

/**
 * الحصول على رسالة الخطأ من الرد
 * @param {Object} response - رد API
 * @param {string} defaultMessage - رسالة افتراضية
 * @returns {string} - رسالة الخطأ
 */
export const getErrorMessage = (response, defaultMessage = 'حدث خطأ غير متوقع') => {
  if (!response || typeof response !== 'object') {
    return defaultMessage;
  }
  
  return response.message || response.error || defaultMessage;
};

/**
 * الحصول على البيانات من الرد
 * @param {Object} response - رد API
 * @param {*} defaultValue - قيمة افتراضية
 * @returns {*} - البيانات
 */
export const getData = (response, defaultValue = null) => {
  if (!response || typeof response !== 'object') {
    return defaultValue;
  }
  
  return response.data !== undefined ? response.data : defaultValue;
};

/**
 * تطبيع الرد إلى الصيغة الجديدة
 * @param {Object} response - رد API
 * @returns {Object} - رد منسق بالصيغة الجديدة
 */
export const normalizeResponse = (response) => {
  if (!response || typeof response !== 'object') {
    return {
      status: 'error',
      message: 'رد غير صالح'
    };
  }
  
  // إذا كان بالفعل بالصيغة الجديدة
  if ('status' in response) {
    return response;
  }
  
  // تحويل من الصيغة القديمة إلى الجديدة
  if ('success' in response) {
    const { success, ...rest } = response;
    return {
      status: success ? 'success' : 'error',
      ...rest
    };
  }
  
  return response;
};

/**
 * معالج عام للردود مع callback
 * @param {Object} response - رد API
 * @param {Object} callbacks - { onSuccess, onError }
 */
export const handleResponse = (response, { onSuccess, onError }) => {
  const normalized = normalizeResponse(response);
  
  if (isSuccess(normalized)) {
    if (onSuccess && typeof onSuccess === 'function') {
      onSuccess(getData(normalized), normalized);
    }
  } else {
    if (onError && typeof onError === 'function') {
      onError(getErrorMessage(normalized), normalized);
    }
  }
};

/**
 * معالج للردود مع Promise
 * @param {Promise} promise - Promise من API call
 * @param {Object} callbacks - { onSuccess, onError, onFinally }
 * @returns {Promise}
 */
export const handleApiCall = async (promise, { onSuccess, onError, onFinally } = {}) => {
  try {
    const response = await promise;
    const normalized = normalizeResponse(response);
    
    if (isSuccess(normalized)) {
      if (onSuccess && typeof onSuccess === 'function') {
        onSuccess(getData(normalized), normalized);
      }
      return normalized;
    } else {
      const errorMsg = getErrorMessage(normalized);
      if (onError && typeof onError === 'function') {
        onError(errorMsg, normalized);
      }
      throw new Error(errorMsg);
    }
  } catch (error) {
    const errorMsg = error.message || 'حدث خطأ في الاتصال';
    if (onError && typeof onError === 'function') {
      onError(errorMsg, error);
    }
    throw error;
  } finally {
    if (onFinally && typeof onFinally === 'function') {
      onFinally();
    }
  }
};

/**
 * دالة مساعدة للتحقق السريع في الشروط
 * @param {Object} response - رد API
 * @returns {boolean}
 */
export const ok = (response) => isSuccess(response);

/**
 * دالة مساعدة للحصول على الحالة
 * @param {Object} response - رد API
 * @returns {string} - 'success' | 'error' | 'unknown'
 */
export const getStatus = (response) => {
  if (!response || typeof response !== 'object') {
    return 'unknown';
  }
  
  if ('status' in response) {
    return response.status;
  }
  
  if ('success' in response) {
    return response.success ? 'success' : 'error';
  }
  
  return 'unknown';
};

// تصدير جميع الدوال
export default {
  isSuccess,
  isError,
  getErrorMessage,
  getData,
  normalizeResponse,
  handleResponse,
  handleApiCall,
  ok,
  getStatus
};

