# /home/ubuntu/image_search_integration/auto_learning/services/SourceApiService.js

/**
 * خدمة API للتعامل مع إدارة المصادر الموثوقة
 * 
 * هذه الخدمة توفر الوظائف اللازمة للتفاعل مع واجهة API الخاصة بإدارة المصادر الموثوقة
 * بما في ذلك عمليات الإضافة والتعديل والحذف والاستعلام وتقييم الثقة.
 */

import ApiService from './ApiService';

const BASE_PATH = '/auto_learning/sources';

export default {
  /**
   * الحصول على قائمة المصادر مع دعم التصفية والترتيب والصفحات
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getSources(params = {}) {
    return ApiService.get(BASE_PATH, params);
  },

  /**
   * الحصول على مصدر محدد بواسطة المعرف
   * @param {number|string} id - معرف المصدر
   * @returns {Promise} وعد بالاستجابة
   */
  getSource(id) {
    return ApiService.get(`${BASE_PATH}/${id}`);
  },

  /**
   * إنشاء مصدر جديد
   * @param {Object} sourceData - بيانات المصدر
   * @returns {Promise} وعد بالاستجابة
   */
  createSource(sourceData) {
    return ApiService.post(BASE_PATH, sourceData);
  },

  /**
   * تحديث مصدر موجود
   * @param {number|string} id - معرف المصدر
   * @param {Object} sourceData - بيانات المصدر المحدثة
   * @returns {Promise} وعد بالاستجابة
   */
  updateSource(id, sourceData) {
    return ApiService.put(`${BASE_PATH}/${id}`, sourceData);
  },

  /**
   * حذف مصدر
   * @param {number|string} id - معرف المصدر
   * @returns {Promise} وعد بالاستجابة
   */
  deleteSource(id) {
    return ApiService.delete(`${BASE_PATH}/${id}`);
  },

  /**
   * التحقق من مصدر
   * @param {number|string} id - معرف المصدر
   * @returns {Promise} وعد بالاستجابة
   */
  verifySource(id) {
    return ApiService.post(`${BASE_PATH}/${id}/verify`);
  },

  /**
   * إضافة مصدر إلى القائمة السوداء
   * @param {number|string} id - معرف المصدر
   * @param {string} reason - سبب الإضافة للقائمة السوداء
   * @returns {Promise} وعد بالاستجابة
   */
  blacklistSource(id, reason = '') {
    return ApiService.post(`${BASE_PATH}/${id}/blacklist`, { reason });
  },

  /**
   * إزالة مصدر من القائمة السوداء
   * @param {number|string} id - معرف المصدر
   * @returns {Promise} وعد بالاستجابة
   */
  removeFromBlacklist(id) {
    return ApiService.delete(`${BASE_PATH}/${id}/blacklist`);
  },

  /**
   * الحصول على قائمة المصادر في القائمة السوداء
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getBlacklistedSources(params = {}) {
    return ApiService.get(`${BASE_PATH}/blacklist`, params);
  },

  /**
   * تحديث مستوى الثقة لمصدر
   * @param {number|string} id - معرف المصدر
   * @param {number} trustLevel - مستوى الثقة الجديد (0-100)
   * @returns {Promise} وعد بالاستجابة
   */
  updateTrustLevel(id, trustLevel) {
    return ApiService.patch(`${BASE_PATH}/${id}/trust-level`, { trust_level: trustLevel });
  },

  /**
   * الحصول على إحصائيات المصادر
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getSourceStats(params = {}) {
    return ApiService.get(`${BASE_PATH}/stats`, params);
  },

  /**
   * البحث عن مصادر
   * @param {string} query - نص البحث
   * @param {Object} params - معلمات إضافية
   * @returns {Promise} وعد بالاستجابة
   */
  searchSources(query, params = {}) {
    return ApiService.get(`${BASE_PATH}/search`, { ...params, query });
  },

  /**
   * استيراد مصادر من ملف
   * @param {File} file - ملف الاستيراد
   * @param {Object} options - خيارات الاستيراد
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  importSources(file, options = {}, progressCallback = null) {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.overwrite !== undefined) {
      formData.append('overwrite', options.overwrite);
    }
    
    if (options.default_trust_level) {
      formData.append('default_trust_level', options.default_trust_level);
    }
    
    return ApiService.uploadFile(`${BASE_PATH}/import`, formData, progressCallback);
  },

  /**
   * تصدير مصادر إلى ملف
   * @param {Object} params - معلمات التصدير
   * @param {string} format - صيغة الملف (csv, json, xlsx)
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  exportSources(params = {}, format = 'csv', progressCallback = null) {
    return ApiService.downloadFile(
      `${BASE_PATH}/export`, 
      { ...params, format }, 
      `sources_export.${format}`,
      progressCallback
    );
  },

  /**
   * تحليل أداء المصادر
   * @param {Object} params - معلمات التحليل
   * @returns {Promise} وعد بالاستجابة
   */
  analyzeSourcePerformance(params = {}) {
    return ApiService.get(`${BASE_PATH}/analyze`, params);
  }
};
