/*
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/modelTrainingService.js
 * الوصف: خدمة تدريب النماذج وتحميل بيانات التعلم
 * المؤلف: فريق تطوير Gaara ERP
 * تاريخ الإنشاء: 30 مايو 2025
 */

import { API_BASE_URL } from '@/config';
import axios from 'axios';

/**
 * خدمة تدريب النماذج وتحميل بيانات التعلم
 */
class ModelTrainingService {
  /**
   * تحميل بيانات التعلم من مصدر خارجي
   * @param {Object} options خيارات التحميل
   * @param {string} options.source مصدر البيانات (plantvillage, plantdoc, custom)
   * @param {string} options.datasetName اسم مجموعة البيانات
   * @param {string} options.datasetUrl رابط مجموعة البيانات (اختياري)
   * @param {File} options.datasetFile ملف مجموعة البيانات (اختياري)
   * @returns {Promise} وعد بنتيجة التحميل
   */
  async importDataset(options) {
    const formData = new FormData();
    formData.append('source', options.source);
    formData.append('datasetName', options.datasetName);

    if (options.datasetUrl) {
      formData.append('datasetUrl', options.datasetUrl);
    }

    if (options.datasetFile) {
      formData.append('datasetFile', options.datasetFile);
    }

    return axios.post(`${API_BASE_URL}/api/ml/datasets/import`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  /**
   * الحصول على قائمة مجموعات البيانات المتاحة
   * @returns {Promise} وعد بقائمة مجموعات البيانات
   */
  async getDatasets() {
    return axios.get(`${API_BASE_URL}/api/ml/datasets`);
  }

  /**
   * الحصول على تفاصيل مجموعة بيانات محددة
   * @param {string} datasetId معرف مجموعة البيانات
   * @returns {Promise} وعد بتفاصيل مجموعة البيانات
   */
  async getDatasetDetails(datasetId) {
    return axios.get(`${API_BASE_URL}/api/ml/datasets/${datasetId}`);
  }

  /**
   * توسيع مجموعة بيانات باستخدام تقنيات متقدمة
   * @param {Object} options خيارات التوسيع
   * @param {string} options.datasetId معرف مجموعة البيانات
   * @param {string} options.method طريقة التوسيع (gan, smart_augmentation, traditional)
   * @param {number} options.factor عامل التوسيع
   * @param {Object} options.config إعدادات إضافية للتوسيع
   * @returns {Promise} وعد بنتيجة التوسيع
   */
  async augmentDataset(options) {
    return axios.post(`${API_BASE_URL}/api/ml/datasets/${options.datasetId}/augment`, {
      method: options.method,
      factor: options.factor,
      config: options.config
    });
  }

  /**
   * تدريب نموذج جديد
   * @param {Object} options خيارات التدريب
   * @param {string} options.datasetId معرف مجموعة البيانات
   * @param {string} options.modelType نوع النموذج (vit, efficientnet, regnet, hybrid)
   * @param {string} options.modelVariant متغير النموذج (base, large, b4, y32, etc.)
   * @param {Object} options.trainingConfig إعدادات التدريب
   * @param {boolean} options.useGPU استخدام GPU للتدريب
   * @returns {Promise} وعد بنتيجة التدريب
   */
  async trainModel(options) {
    return axios.post(`${API_BASE_URL}/api/ml/models/train`, {
      datasetId: options.datasetId,
      modelType: options.modelType,
      modelVariant: options.modelVariant,
      trainingConfig: options.trainingConfig,
      useGPU: options.useGPU
    });
  }

  /**
   * الحصول على حالة تدريب نموذج
   * @param {string} trainingId معرف عملية التدريب
   * @returns {Promise} وعد بحالة التدريب
   */
  async getTrainingStatus(trainingId) {
    return axios.get(`${API_BASE_URL}/api/ml/models/training/${trainingId}/status`);
  }

  /**
   * الحصول على قائمة النماذج المتاحة
   * @returns {Promise} وعد بقائمة النماذج
   */
  async getModels() {
    return axios.get(`${API_BASE_URL}/api/ml/models`);
  }

  /**
   * الحصول على تفاصيل نموذج محدد
   * @param {string} modelId معرف النموذج
   * @returns {Promise} وعد بتفاصيل النموذج
   */
  async getModelDetails(modelId) {
    return axios.get(`${API_BASE_URL}/api/ml/models/${modelId}`);
  }

  /**
   * تقييم أداء نموذج على مجموعة بيانات
   * @param {string} modelId معرف النموذج
   * @param {string} datasetId معرف مجموعة البيانات
   * @returns {Promise} وعد بنتائج التقييم
   */
  async evaluateModel(modelId, datasetId) {
    return axios.post(`${API_BASE_URL}/api/ml/models/${modelId}/evaluate`, {
      datasetId
    });
  }

  /**
   * تصدير نموذج بصيغة محددة
   * @param {string} modelId معرف النموذج
   * @param {string} format صيغة التصدير (onnx, tflite, pytorch, etc.)
   * @returns {Promise} وعد برابط تحميل النموذج المصدر
   */
  async exportModel(modelId, format) {
    return axios.post(`${API_BASE_URL}/api/ml/models/${modelId}/export`, {
      format
    });
  }

  /**
   * تحسين نموذج باستخدام تقنيات متقدمة
   * @param {string} modelId معرف النموذج
   * @param {string} method طريقة التحسين (pruning, quantization, distillation)
   * @param {Object} config إعدادات التحسين
   * @returns {Promise} وعد بنتيجة التحسين
   */
  async optimizeModel(modelId, method, config) {
    return axios.post(`${API_BASE_URL}/api/ml/models/${modelId}/optimize`, {
      method,
      config
    });
  }

  /**
   * استخدام نموذج للتنبؤ
   * @param {string} modelId معرف النموذج
   * @param {File|string} input الصورة المدخلة (ملف أو رابط)
   * @returns {Promise} وعد بنتيجة التنبؤ
   */
  async predict(modelId, input) {
    const formData = new FormData();

    if (typeof input === 'string') {
      formData.append('imageUrl', input);
    } else {
      formData.append('image', input);
    }

    return axios.post(`${API_BASE_URL}/api/ml/models/${modelId}/predict`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  /**
   * البحث عن صور مشابهة
   * @param {File|string} input الصورة المدخلة (ملف أو رابط)
   * @param {Object} options خيارات البحث
   * @param {number} options.limit عدد النتائج
   * @param {number} options.threshold عتبة التشابه
   * @returns {Promise} وعد بنتائج البحث
   */
  async searchSimilarImages(input, options = {}) {
    const formData = new FormData();

    if (typeof input === 'string') {
      formData.append('imageUrl', input);
    } else {
      formData.append('image', input);
    }

    formData.append('limit', options.limit || 10);
    formData.append('threshold', options.threshold || 0.7);

    return axios.post(`${API_BASE_URL}/api/ml/search/similar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  /**
   * تحليل إجهاد النبات
   * @param {File|string} input الصورة المدخلة (ملف أو رابط)
   * @returns {Promise} وعد بنتائج التحليل
   */
  async analyzeStress(input) {
    const formData = new FormData();

    if (typeof input === 'string') {
      formData.append('imageUrl', input);
    } else {
      formData.append('image', input);
    }

    return axios.post(`${API_BASE_URL}/api/ml/analyze/stress`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  /**
   * تقسيم صورة النبات
   * @param {File|string} input الصورة المدخلة (ملف أو رابط)
   * @param {string} method طريقة التقسيم (sam2, deeplabv3, unet)
   * @returns {Promise} وعد بنتائج التقسيم
   */
  async segmentPlant(input, method = 'sam2') {
    const formData = new FormData();

    if (typeof input === 'string') {
      formData.append('imageUrl', input);
    } else {
      formData.append('image', input);
    }

    formData.append('method', method);

    return axios.post(`${API_BASE_URL}/api/ml/segment`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
}

export default new ModelTrainingService();
