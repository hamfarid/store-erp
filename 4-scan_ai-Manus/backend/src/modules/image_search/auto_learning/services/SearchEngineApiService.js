# /home/ubuntu/image_search_integration/auto_learning/services/SearchEngineApiService.js

/**
 * خدمة API للتعامل مع إدارة محركات البحث
 * 
 * هذه الخدمة توفر الوظائف اللازمة للتفاعل مع واجهة API الخاصة بإدارة محركات البحث
 * بما في ذلك عمليات الإضافة والتعديل والحذف والاستعلام واختبار المحركات.
 */

import ApiService from './ApiService';

const BASE_PATH = '/auto_learning/search_engines';

export default {
  /**
   * الحصول على قائمة محركات البحث مع دعم التصفية والترتيب والصفحات
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getSearchEngines(params = {}) {
    return ApiService.get(BASE_PATH, params);
  },

  /**
   * الحصول على محرك بحث محدد بواسطة المعرف
   * @param {number|string} id - معرف محرك البحث
   * @returns {Promise} وعد بالاستجابة
   */
  getSearchEngine(id) {
    return ApiService.get(`${BASE_PATH}/${id}`);
  },

  /**
   * إنشاء محرك بحث جديد
   * @param {Object} engineData - بيانات محرك البحث
   * @returns {Promise} وعد بالاستجابة
   */
  createSearchEngine(engineData) {
    return ApiService.post(BASE_PATH, engineData);
  },

  /**
   * تحديث محرك بحث موجود
   * @param {number|string} id - معرف محرك البحث
   * @param {Object} engineData - بيانات محرك البحث المحدثة
   * @returns {Promise} وعد بالاستجابة
   */
  updateSearchEngine(id, engineData) {
    return ApiService.put(`${BASE_PATH}/${id}`, engineData);
  },

  /**
   * حذف محرك بحث
   * @param {number|string} id - معرف محرك البحث
   * @returns {Promise} وعد بالاستجابة
   */
  deleteSearchEngine(id) {
    return ApiService.delete(`${BASE_PATH}/${id}`);
  },

  /**
   * اختبار محرك بحث
   * @param {number|string} id - معرف محرك البحث
   * @param {string} query - استعلام الاختبار
   * @param {number} limit - عدد النتائج المطلوبة
   * @returns {Promise} وعد بالاستجابة
   */
  testSearchEngine(id, query, limit = 5) {
    return ApiService.post(`${BASE_PATH}/${id}/test`, { query, limit });
  },

  /**
   * تحديث حالة محرك بحث (نشط/غير نشط)
   * @param {number|string} id - معرف محرك البحث
   * @param {boolean} isActive - الحالة الجديدة
   * @returns {Promise} وعد بالاستجابة
   */
  updateEngineStatus(id, isActive) {
    return ApiService.patch(`${BASE_PATH}/${id}/status`, { is_active: isActive });
  },

  /**
   * تحديث أولوية محرك بحث
   * @param {number|string} id - معرف محرك البحث
   * @param {number} priority - الأولوية الجديدة
   * @returns {Promise} وعد بالاستجابة
   */
  updateEnginePriority(id, priority) {
    return ApiService.patch(`${BASE_PATH}/${id}/priority`, { priority });
  },

  /**
   * الحصول على إحصائيات محركات البحث
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getEngineStats(params = {}) {
    return ApiService.get(`${BASE_PATH}/stats`, params);
  },

  /**
   * البحث عن محركات بحث
   * @param {string} query - نص البحث
   * @param {Object} params - معلمات إضافية
   * @returns {Promise} وعد بالاستجابة
   */
  searchEngines(query, params = {}) {
    return ApiService.get(`${BASE_PATH}/search`, { ...params, query });
  },

  /**
   * استيراد محركات بحث من ملف
   * @param {File} file - ملف الاستيراد
   * @param {Object} options - خيارات الاستيراد
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  importEngines(file, options = {}, progressCallback = null) {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.overwrite !== undefined) {
      formData.append('overwrite', options.overwrite);
    }
    
    return ApiService.uploadFile(`${BASE_PATH}/import`, formData, progressCallback);
  },

  /**
   * تصدير محركات بحث إلى ملف
   * @param {Object} params - معلمات التصدير
   * @param {string} format - صيغة الملف (csv, json, xlsx)
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  exportEngines(params = {}, format = 'csv', progressCallback = null) {
    return ApiService.downloadFile(
      `${BASE_PATH}/export`, 
      { ...params, format }, 
      `search_engines_export.${format}`,
      progressCallback
    );
  },

  /**
   * تحليل أداء محركات البحث
   * @param {Object} params - معلمات التحليل
   * @returns {Promise} وعد بالاستجابة
   */
  analyzeEnginePerformance(params = {}) {
    return ApiService.get(`${BASE_PATH}/analyze`, params);
  }
};
