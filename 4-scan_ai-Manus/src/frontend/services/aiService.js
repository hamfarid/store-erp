// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/aiService.js

/**
 * خدمة الذكاء الاصطناعي
 * 
 * توفر هذه الخدمة واجهة برمجية للتفاعل مع واجهات API الخاصة بخدمات الذكاء الاصطناعي
 * وتتضمن وظائف للحصول على معلومات الوكلاء، الأفاتار، والتنبؤات والتحليلات
 */

import axios from 'axios';
import { getAuthHeader } from './authService';

// تعيين عنوان API الأساسي
const AI_SERVICE_URL = '/api/ai-service';
const DISEASE_SERVICE_URL = '/api/disease-diagnosis';

/**
 * الحصول على معلومات الوكيل الذكي
 * @returns {Promise} وعد بمعلومات الوكيل الذكي
 */
export const getAgentInfo = async () => {
  try {
    const response = await axios.get(`${AI_SERVICE_URL}/info`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على معلومات الوكيل الذكي:', error);
    throw error;
  }
};

/**
 * الحصول على صورة الأفاتار للوكيل الذكي
 * @param {String} agentId - معرف الوكيل (اختياري)
 * @returns {Promise} وعد برابط صورة الأفاتار
 */
export const getAgentAvatar = async (agentId = 'default') => {
  try {
    // محاولة الحصول على الأفاتار من الخدمة
    const response = await axios.get(`${AI_SERVICE_URL}/avatar/${agentId}`, {
      headers: getAuthHeader(),
      responseType: 'blob'
    });

    // إنشاء رابط للصورة
    const avatarUrl = URL.createObjectURL(response.data);
    return avatarUrl;
  } catch (error) {
    console.error('خطأ في الحصول على صورة الأفاتار:', error);

    // في حالة الفشل، استخدام صورة افتراضية محلية
    return '/assets/images/default_ai_avatar.png';
  }
};

/**
 * إرسال طلب تنبؤ إلى الوكيل الذكي
 * @param {Object} data - بيانات التنبؤ
 * @returns {Promise} وعد بنتيجة التنبؤ
 */
export const predict = async (data) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/predict`, data, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في إرسال طلب التنبؤ:', error);
    throw error;
  }
};

/**
 * الحصول على قائمة النماذج المتاحة
 * @returns {Promise} وعد بقائمة النماذج
 */
export const getModels = async () => {
  try {
    const response = await axios.get(`${AI_SERVICE_URL}/models`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على قائمة النماذج:', error);
    throw error;
  }
};

/**
 * إرسال طلب تحليل إلى الوكيل الذكي
 * @param {Object} data - بيانات التحليل
 * @returns {Promise} وعد بنتيجة التحليل
 */
export const analyze = async (data) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/analyze`, data, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في إرسال طلب التحليل:', error);
    throw error;
  }
};

/**
 * التحقق من حالة خدمة الذكاء الاصطناعي
 * @returns {Promise} وعد بحالة الخدمة
 */
export const checkAIServiceHealth = async () => {
  try {
    const response = await axios.get(`${AI_SERVICE_URL}/health`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في التحقق من حالة خدمة الذكاء الاصطناعي:', error);
    throw error;
  }
};

/**
 * التحقق من حالة خدمة تشخيص الأمراض
 * @returns {Promise} وعد بحالة الخدمة
 */
export const checkDiseaseServiceHealth = async () => {
  try {
    const response = await axios.get(`${DISEASE_SERVICE_URL}/health`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في التحقق من حالة خدمة تشخيص الأمراض:', error);
    throw error;
  }
};

/**
 * تكوين إعدادات الوكيل الذكي
 * @param {Object} config - إعدادات الوكيل
 * @returns {Promise} وعد بنتيجة التكوين
 */
export const configureAgent = async (config) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/configure`, config, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في تكوين إعدادات الوكيل الذكي:', error);
    throw error;
  }
};

/**
 * تحميل صورة أفاتار مخصصة للوكيل الذكي
 * @param {File} imageFile - ملف الصورة
 * @param {String} agentId - معرف الوكيل (اختياري)
 * @returns {Promise} وعد بنتيجة التحميل
 */
export const uploadAgentAvatar = async (imageFile, agentId = 'default') => {
  try {
    const formData = new FormData();
    formData.append('avatar', imageFile);

    const response = await axios.post(`${AI_SERVICE_URL}/avatar/${agentId}`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    console.error('خطأ في تحميل صورة الأفاتار:', error);
    throw error;
  }
};

export default {
  getAgentInfo,
  getAgentAvatar,
  predict,
  getModels,
  analyze,
  checkAIServiceHealth,
  checkDiseaseServiceHealth,
  configureAgent,
  uploadAgentAvatar
};
