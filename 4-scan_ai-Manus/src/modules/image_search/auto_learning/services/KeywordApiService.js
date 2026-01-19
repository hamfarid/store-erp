# /home/ubuntu/image_search_integration/auto_learning/services/KeywordApiService.js

/**
 * خدمة API للتعامل مع إدارة الكلمات المفتاحية
 * 
 * هذه الخدمة توفر الوظائف اللازمة للتفاعل مع واجهة API الخاصة بإدارة الكلمات المفتاحية
 * بما في ذلك عمليات الإضافة والتعديل والحذف والاستعلام.
 */

import ApiService from './ApiService';

const BASE_PATH = '/auto_learning/keywords';

export default {
  /**
   * الحصول على قائمة الكلمات المفتاحية مع دعم التصفية والترتيب والصفحات
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getKeywords(params = {}) {
    return ApiService.get(BASE_PATH, params);
  },

  /**
   * الحصول على كلمة مفتاحية محددة بواسطة المعرف
   * @param {number|string} id - معرف الكلمة المفتاحية
   * @returns {Promise} وعد بالاستجابة
   */
  getKeyword(id) {
    return ApiService.get(`${BASE_PATH}/${id}`);
  },

  /**
   * إنشاء كلمة مفتاحية جديدة
   * @param {Object} keywordData - بيانات الكلمة المفتاحية
   * @returns {Promise} وعد بالاستجابة
   */
  createKeyword(keywordData) {
    return ApiService.post(BASE_PATH, keywordData);
  },

  /**
   * تحديث كلمة مفتاحية موجودة
   * @param {number|string} id - معرف الكلمة المفتاحية
   * @param {Object} keywordData - بيانات الكلمة المفتاحية المحدثة
   * @returns {Promise} وعد بالاستجابة
   */
  updateKeyword(id, keywordData) {
    return ApiService.put(`${BASE_PATH}/${id}`, keywordData);
  },

  /**
   * حذف كلمة مفتاحية
   * @param {number|string} id - معرف الكلمة المفتاحية
   * @returns {Promise} وعد بالاستجابة
   */
  deleteKeyword(id) {
    return ApiService.delete(`${BASE_PATH}/${id}`);
  },

  /**
   * الحصول على الكلمات المفتاحية المرتبطة
   * @param {number|string} id - معرف الكلمة المفتاحية
   * @returns {Promise} وعد بالاستجابة
   */
  getRelatedKeywords(id) {
    return ApiService.get(`${BASE_PATH}/${id}/related`);
  },

  /**
   * إضافة علاقة بين كلمتين مفتاحيتين
   * @param {number|string} id - معرف الكلمة المفتاحية الأولى
   * @param {number|string} relatedId - معرف الكلمة المفتاحية الثانية
   * @param {string} relationType - نوع العلاقة
   * @returns {Promise} وعد بالاستجابة
   */
  addKeywordRelation(id, relatedId, relationType) {
    return ApiService.post(`${BASE_PATH}/${id}/related`, {
      related_id: relatedId,
      relation_type: relationType
    });
  },

  /**
   * حذف علاقة بين كلمتين مفتاحيتين
   * @param {number|string} id - معرف الكلمة المفتاحية الأولى
   * @param {number|string} relatedId - معرف الكلمة المفتاحية الثانية
   * @returns {Promise} وعد بالاستجابة
   */
  removeKeywordRelation(id, relatedId) {
    return ApiService.delete(`${BASE_PATH}/${id}/related/${relatedId}`);
  },

  /**
   * الحصول على إحصائيات الكلمات المفتاحية
   * @param {Object} params - معلمات الاستعلام
   * @returns {Promise} وعد بالاستجابة
   */
  getKeywordStats(params = {}) {
    return ApiService.get(`${BASE_PATH}/stats`, params);
  },

  /**
   * البحث عن كلمات مفتاحية
   * @param {string} query - نص البحث
   * @param {Object} params - معلمات إضافية
   * @returns {Promise} وعد بالاستجابة
   */
  searchKeywords(query, params = {}) {
    return ApiService.get(`${BASE_PATH}/search`, { ...params, query });
  },

  /**
   * استيراد كلمات مفتاحية من ملف
   * @param {File} file - ملف الاستيراد
   * @param {Object} options - خيارات الاستيراد
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  importKeywords(file, options = {}, progressCallback = null) {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.overwrite !== undefined) {
      formData.append('overwrite', options.overwrite);
    }
    
    if (options.category_id) {
      formData.append('category_id', options.category_id);
    }
    
    return ApiService.uploadFile(`${BASE_PATH}/import`, formData, progressCallback);
  },

  /**
   * تصدير كلمات مفتاحية إلى ملف
   * @param {Object} params - معلمات التصدير
   * @param {string} format - صيغة الملف (csv, json, xlsx)
   * @param {Function} progressCallback - دالة رد الاتصال لتتبع التقدم
   * @returns {Promise} وعد بالاستجابة
   */
  exportKeywords(params = {}, format = 'csv', progressCallback = null) {
    return ApiService.downloadFile(
      `${BASE_PATH}/export`, 
      { ...params, format }, 
      `keywords_export.${format}`,
      progressCallback
    );
  },

  /**
   * الحصول على فئات الكلمات المفتاحية
   * @returns {Promise} وعد بالاستجابة
   */
  getKeywordCategories() {
    return ApiService.get(`${BASE_PATH}/categories`);
  },

  /**
   * تحليل أداء الكلمات المفتاحية
   * @param {Object} params - معلمات التحليل
   * @returns {Promise} وعد بالاستجابة
   */
  analyzeKeywordPerformance(params = {}) {
    return ApiService.get(`${BASE_PATH}/analyze`, params);
  }
};
