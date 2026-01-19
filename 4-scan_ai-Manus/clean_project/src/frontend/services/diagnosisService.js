// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/diagnosisService.js

/**
 * خدمة التشخيص
 * 
 * توفر هذه الخدمة واجهة برمجية للتفاعل مع واجهات API الخاصة بتشخيص الأمراض النباتية
 * وتتضمن وظائف للحصول على المحاصيل والأمراض وإجراء التشخيص وإدارة نتائج التشخيص
 */

import axios from 'axios';
import { getAuthHeader } from './authService';

const API_BASE_URL = '/api/disease-diagnosis';

/**
 * الحصول على قائمة المحاصيل
 * @returns {Promise} وعد بقائمة المحاصيل
 */
export const getCrops = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/crops`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error('خطأ في الحصول على المحاصيل:', error);
    throw error;
  }
};

/**
 * الحصول على محصول بواسطة المعرف
 * @param {Number} cropId - معرف المحصول
 * @returns {Promise} وعد بمعلومات المحصول
 */
export const getCropById = async (cropId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/crops/${cropId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في الحصول على المحصول ${cropId}:`, error);
    throw error;
  }
};

/**
 * إنشاء محصول جديد
 * @param {Object} cropData - بيانات المحصول
 * @returns {Promise} وعد بمعلومات المحصول المنشأ
 */
export const createCrop = async (cropData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/crops`, cropData, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error('خطأ في إنشاء محصول جديد:', error);
    throw error;
  }
};

/**
 * تحديث محصول موجود
 * @param {Number} cropId - معرف المحصول
 * @param {Object} cropData - بيانات المحصول المحدثة
 * @returns {Promise} وعد بمعلومات المحصول المحدث
 */
export const updateCrop = async (cropId, cropData) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/crops/${cropId}`, cropData, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في تحديث المحصول ${cropId}:`, error);
    throw error;
  }
};

/**
 * حذف محصول
 * @param {Number} cropId - معرف المحصول
 * @returns {Promise} وعد بنتيجة الحذف
 */
export const deleteCrop = async (cropId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/crops/${cropId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في حذف المحصول ${cropId}:`, error);
    throw error;
  }
};

/**
 * الحصول على قائمة الأمراض
 * @param {Number} cropId - معرف المحصول (اختياري)
 * @returns {Promise} وعد بقائمة الأمراض
 */
export const getDiseases = async (cropId = null) => {
  try {
    const url = cropId ? `${API_BASE_URL}/diseases?crop_id=${cropId}` : `${API_BASE_URL}/diseases`;
    const response = await axios.get(url, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error('خطأ في الحصول على الأمراض:', error);
    throw error;
  }
};

/**
 * الحصول على مرض بواسطة المعرف
 * @param {Number} diseaseId - معرف المرض
 * @returns {Promise} وعد بمعلومات المرض
 */
export const getDiseaseById = async (diseaseId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/diseases/${diseaseId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في الحصول على المرض ${diseaseId}:`, error);
    throw error;
  }
};

/**
 * إنشاء مرض جديد
 * @param {Object} diseaseData - بيانات المرض
 * @returns {Promise} وعد بمعلومات المرض المنشأ
 */
export const createDisease = async (diseaseData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/diseases`, diseaseData, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error('خطأ في إنشاء مرض جديد:', error);
    throw error;
  }
};

/**
 * تحديث مرض موجود
 * @param {Number} diseaseId - معرف المرض
 * @param {Object} diseaseData - بيانات المرض المحدثة
 * @returns {Promise} وعد بمعلومات المرض المحدث
 */
export const updateDisease = async (diseaseId, diseaseData) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/diseases/${diseaseId}`, diseaseData, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في تحديث المرض ${diseaseId}:`, error);
    throw error;
  }
};

/**
 * حذف مرض
 * @param {Number} diseaseId - معرف المرض
 * @returns {Promise} وعد بنتيجة الحذف
 */
export const deleteDisease = async (diseaseId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/diseases/${diseaseId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في حذف المرض ${diseaseId}:`, error);
    throw error;
  }
};

/**
 * تشخيص مرض بناءً على الأعراض و/أو الصور
 * @param {Object} diagnosisData - بيانات التشخيص
 * @param {Number} diagnosisData.cropId - معرف المحصول (اختياري)
 * @param {String} diagnosisData.symptoms - الأعراض (اختياري)
 * @param {Array} diagnosisData.images - الصور (اختياري)
 * @param {Object} diagnosisData.options - خيارات إضافية (اختياري)
 * @returns {Promise} وعد بنتائج التشخيص
 */
export const diagnoseDisease = async (diagnosisData) => {
  try {
    const formData = new FormData();

    if (diagnosisData.cropId) {
      formData.append('crop_id', diagnosisData.cropId);
    }

    if (diagnosisData.symptoms) {
      formData.append('symptoms', diagnosisData.symptoms);
    }

    if (diagnosisData.images && diagnosisData.images.length > 0) {
      diagnosisData.images.forEach(image => {
        formData.append('image', image);
      });
    }

    // إضافة الخيارات الإضافية
    if (diagnosisData.options) {
      Object.entries(diagnosisData.options).forEach(([key, value]) => {
        formData.append(key, value);
      });
    }

    const response = await axios.post(`${API_BASE_URL}/diagnose`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data.data;
  } catch (error) {
    console.error('خطأ في تشخيص المرض:', error);
    throw error;
  }
};

/**
 * الحصول على قائمة التشخيصات
 * @param {String} userId - معرف المستخدم (اختياري)
 * @returns {Promise} وعد بقائمة التشخيصات
 */
export const getDiagnoses = async (userId = null) => {
  try {
    const url = userId ? `${API_BASE_URL}/diagnoses?user_id=${userId}` : `${API_BASE_URL}/diagnoses`;
    const response = await axios.get(url, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error('خطأ في الحصول على التشخيصات:', error);
    throw error;
  }
};

/**
 * الحصول على تشخيص بواسطة المعرف
 * @param {Number} diagnosisId - معرف التشخيص
 * @returns {Promise} وعد بمعلومات التشخيص
 */
export const getDiagnosisById = async (diagnosisId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/diagnoses/${diagnosisId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في الحصول على التشخيص ${diagnosisId}:`, error);
    throw error;
  }
};

/**
 * حذف تشخيص
 * @param {Number} diagnosisId - معرف التشخيص
 * @returns {Promise} وعد بنتيجة الحذف
 */
export const deleteDiagnosis = async (diagnosisId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/diagnoses/${diagnosisId}`, {
      headers: getAuthHeader()
    });
    return response.data.data;
  } catch (error) {
    console.error(`خطأ في حذف التشخيص ${diagnosisId}:`, error);
    throw error;
  }
};

/**
 * البحث عن الأمراض
 * @param {String} query - استعلام البحث
 * @param {Number} cropId - معرف المحصول (اختياري)
 * @returns {Promise} وعد بنتائج البحث
 */
export const searchDiseases = async (query, cropId = null) => {
  try {
    const url = cropId
      ? `${API_BASE_URL}/search?query=${encodeURIComponent(query)}&crop_id=${cropId}`
      : `${API_BASE_URL}/search?query=${encodeURIComponent(query)}`;

    const response = await axios.get(url, {
      headers: getAuthHeader()
    });

    return response.data.data;
  } catch (error) {
    console.error('خطأ في البحث عن الأمراض:', error);
    throw error;
  }
};

/**
 * البحث عن الأمراض بواسطة الأعراض
 * @param {Array} symptoms - قائمة الأعراض
 * @param {Number} cropId - معرف المحصول (اختياري)
 * @returns {Promise} وعد بنتائج البحث
 */
export const searchBySymptoms = async (symptoms, cropId = null) => {
  try {
    const data = { symptoms };

    if (cropId) {
      data.crop_id = cropId;
    }

    const response = await axios.post(`${API_BASE_URL}/search-by-symptoms`, data, {
      headers: getAuthHeader()
    });

    return response.data.data;
  } catch (error) {
    console.error('خطأ في البحث عن الأمراض بواسطة الأعراض:', error);
    throw error;
  }
};

/**
 * استيراد قاعدة المعرفة من ملف
 * @param {File} file - ملف قاعدة المعرفة
 * @returns {Promise} وعد بنتيجة الاستيراد
 */
export const importKnowledgeBase = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/import-knowledge-base`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    console.error('خطأ في استيراد قاعدة المعرفة:', error);
    throw error;
  }
};

/**
 * تصدير قاعدة المعرفة إلى ملف
 * @param {String} format - صيغة الملف (yaml أو json)
 * @returns {Promise} وعد برابط تنزيل الملف
 */
export const exportKnowledgeBase = async (format = 'yaml') => {
  try {
    const response = await axios.get(`${API_BASE_URL}/export-knowledge-base?format=${format}`, {
      headers: getAuthHeader(),
      responseType: 'blob'
    });

    // إنشاء رابط تنزيل للملف
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `knowledge_base.${format}`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    return url;
  } catch (error) {
    console.error('خطأ في تصدير قاعدة المعرفة:', error);
    throw error;
  }
};

/**
 * إنشاء تقرير تشخيص
 * @param {Number} diagnosisId - معرف التشخيص
 * @param {Object} options - خيارات التقرير
 * @returns {Promise} وعد برابط تنزيل التقرير
 */
export const generateDiagnosisReport = async (diagnosisId, options = {}) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/diagnoses/${diagnosisId}/report`, options, {
      headers: getAuthHeader(),
      responseType: 'blob'
    });

    // إنشاء رابط تنزيل للتقرير
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `diagnosis_report_${diagnosisId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    return url;
  } catch (error) {
    console.error(`خطأ في إنشاء تقرير التشخيص ${diagnosisId}:`, error);
    throw error;
  }
};

/**
 * تكامل مع مديول الذاكرة لحفظ نتائج التشخيص
 * @param {Object} diagnosisResult - نتيجة التشخيص
 * @param {Object} metadata - بيانات وصفية إضافية
 * @returns {Promise} وعد بنتيجة الحفظ
 */
export const saveDiagnosisToMemory = async (diagnosisResult, metadata = {}) => {
  try {
    const data = {
      type: 'diagnosis_result',
      content: diagnosisResult,
      metadata: {
        timestamp: new Date().toISOString(),
        ...metadata
      }
    };

    const response = await axios.post('/api/memory/store', data, {
      headers: getAuthHeader()
    });

    return response.data;
  } catch (error) {
    console.error('خطأ في حفظ نتيجة التشخيص في الذاكرة:', error);
    throw error;
  }
};

/**
 * استرجاع نتائج التشخيص السابقة من مديول الذاكرة
 * @param {Object} query - استعلام البحث
 * @returns {Promise} وعد بنتائج البحث
 */
export const retrieveDiagnosisFromMemory = async (query = {}) => {
  try {
    const params = {
      type: 'diagnosis_result',
      ...query
    };

    const response = await axios.get('/api/memory/retrieve', {
      params,
      headers: getAuthHeader()
    });

    return response.data;
  } catch (error) {
    console.error('خطأ في استرجاع نتائج التشخيص من الذاكرة:', error);
    throw error;
  }
};

/**
 * تكامل مع مديول البحث عن الصور للحصول على صور مشابهة
 * @param {File} imageFile - ملف الصورة
 * @param {Object} options - خيارات البحث
 * @returns {Promise} وعد بنتائج البحث
 */
export const findSimilarImages = async (imageFile, options = {}) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    // إضافة الخيارات
    Object.entries(options).forEach(([key, value]) => {
      formData.append(key, value);
    });

    const response = await axios.post('/api/image-search/find-similar', formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    console.error('خطأ في البحث عن صور مشابهة:', error);
    throw error;
  }
};

export default {
  getCrops,
  getCropById,
  createCrop,
  updateCrop,
  deleteCrop,
  getDiseases,
  getDiseaseById,
  createDisease,
  updateDisease,
  deleteDisease,
  diagnoseDisease,
  getDiagnoses,
  getDiagnosisById,
  deleteDiagnosis,
  searchDiseases,
  searchBySymptoms,
  importKnowledgeBase,
  exportKnowledgeBase,
  generateDiagnosisReport,
  saveDiagnosisToMemory,
  retrieveDiagnosisFromMemory,
  findSimilarImages
};
