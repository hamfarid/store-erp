/**
 * خدمة تشخيص أمراض النباتات
 * توفر هذه الخدمة واجهة برمجية للتفاعل مع نظام تشخيص أمراض النباتات
 * وتتيح للمستخدمين تحميل الصور واختبار النماذج ومقارنتها
 * 
 * المؤلف: فريق تطوير Gaara ERP
 * تاريخ الإنشاء: 30 مايو 2025
 */

import axios from 'axios';

/**
 * خدمة تشخيص أمراض النباتات
 */
class PlantDiseaseService {
  /**
   * الحصول على قائمة النماذج المتاحة
   * @returns {Promise<Object>} قائمة النماذج المتاحة
   */
  async getAvailableModels() {
    try {
      const response = await axios.get('/api/plant-disease/models');
      return response.data;
    } catch (error) {
      console.error('خطأ في الحصول على النماذج المتاحة:', error);
      throw error;
    }
  }

  /**
   * الحصول على تفاصيل نموذج محدد
   * @param {string} modelName اسم النموذج
   * @returns {Promise<Object>} تفاصيل النموذج
   */
  async getModelDetails(modelName) {
    try {
      const response = await axios.get(`/api/plant-disease/models/${modelName}`);
      return response.data;
    } catch (error) {
      console.error(`خطأ في الحصول على تفاصيل النموذج ${modelName}:`, error);
      throw error;
    }
  }

  /**
   * تحميل صور للاختبار
   * @param {FormData} formData نموذج البيانات الذي يحتوي على الصور والتسميات
   * @returns {Promise<Object>} نتيجة تحميل الصور
   */
  async uploadTestImages(formData) {
    try {
      const response = await axios.post('/api/plant-disease/upload-test-images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('خطأ في تحميل صور الاختبار:', error);
      throw error;
    }
  }

  /**
   * تشغيل اختبار للنماذج
   * @param {Object} params معلمات الاختبار
   * @param {Array<string>} params.image_paths مسارات الصور
   * @param {Array<number>} params.ground_truth التسميات الصحيحة
   * @param {Array<string>} [params.models] قائمة النماذج للاختبار (اختياري)
   * @param {number} [params.iterations=3] عدد تكرارات الاختبار
   * @param {boolean} [params.monitor_resources=true] مراقبة استهلاك الموارد
   * @param {boolean} [params.generate_visualizations=true] إنشاء مخططات بيانية
   * @param {boolean} [params.learn_from_results=false] التعلم من النتائج
   * @returns {Promise<Object>} نتائج الاختبار
   */
  async runBenchmark(params) {
    try {
      const response = await axios.post('/api/plant-disease/benchmark', params);
      return response.data;
    } catch (error) {
      console.error('خطأ في تشغيل الاختبار:', error);
      throw error;
    }
  }

  /**
   * الحصول على قائمة الاختبارات السابقة
   * @returns {Promise<Object>} قائمة الاختبارات السابقة
   */
  async getPreviousBenchmarks() {
    try {
      const response = await axios.get('/api/plant-disease/benchmarks');
      return response.data;
    } catch (error) {
      console.error('خطأ في الحصول على الاختبارات السابقة:', error);
      throw error;
    }
  }

  /**
   * الحصول على تفاصيل اختبار محدد
   * @param {string} benchmarkId معرف الاختبار
   * @returns {Promise<Object>} تفاصيل الاختبار
   */
  async getBenchmarkDetails(benchmarkId) {
    try {
      const response = await axios.get(`/api/plant-disease/benchmarks/${benchmarkId}`);
      return response.data;
    } catch (error) {
      console.error(`خطأ في الحصول على تفاصيل الاختبار ${benchmarkId}:`, error);
      throw error;
    }
  }

  /**
   * التنبؤ باستخدام نموذج محدد
   * @param {FormData} formData نموذج البيانات الذي يحتوي على الصورة
   * @param {string} modelName اسم النموذج
   * @returns {Promise<Object>} نتيجة التنبؤ
   */
  async predictWithModel(formData, modelName) {
    try {
      const response = await axios.post(`/api/plant-disease/predict/${modelName}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error(`خطأ في التنبؤ باستخدام النموذج ${modelName}:`, error);
      throw error;
    }
  }

  /**
   * التنبؤ باستخدام مجموعة نماذج
   * @param {FormData} formData نموذج البيانات الذي يحتوي على الصورة
   * @param {Array<string>} [models] قائمة النماذج (اختياري)
   * @returns {Promise<Object>} نتيجة التنبؤ المجمع
   */
  async predictWithEnsemble(formData, models = null) {
    try {
      const url = models ? 
        `/api/plant-disease/predict-ensemble?models=${models.join(',')}` : 
        '/api/plant-disease/predict-ensemble';
      
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('خطأ في التنبؤ المجمع:', error);
      throw error;
    }
  }

  /**
   * تحميل تقرير الاختبار
   * @param {string} reportPath مسار التقرير
   * @returns {Promise<Blob>} محتوى التقرير
   */
  async downloadBenchmarkReport(reportPath) {
    try {
      const response = await axios.get(`/api/files?path=${encodeURIComponent(reportPath)}`, {
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      console.error('خطأ في تحميل تقرير الاختبار:', error);
      throw error;
    }
  }

  /**
   * التعلم من نتائج الاختبار
   * @param {Object} benchmarkResults نتائج الاختبار
   * @returns {Promise<Object>} نتائج التعلم
   */
  async learnFromResults(benchmarkResults) {
    try {
      const response = await axios.post('/api/plant-disease/learn', { results: benchmarkResults });
      return response.data;
    } catch (error) {
      console.error('خطأ في التعلم من النتائج:', error);
      throw error;
    }
  }
}

// تصدير نسخة واحدة من الخدمة
export const plantDiseaseService = new PlantDiseaseService();
