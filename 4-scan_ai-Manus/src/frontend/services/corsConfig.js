// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/corsConfig.js

/**
 * تكوين CORS للاتصال بخدمات الذكاء الاصطناعي
 * 
 * يوفر هذا الملف إعدادات CORS وإعادة توجيه الطلبات لخدمات الذكاء الاصطناعي
 */

import axios from 'axios';

/**
 * تهيئة إعدادات CORS وإعادة توجيه الطلبات
 */
export const setupCorsConfig = () => {
  // تعيين عنوان الخدمة الأساسي
  const baseURL = window.location.origin;

  // تكوين الطلبات الافتراضية
  axios.defaults.baseURL = baseURL;

  // إضافة معلومات الاعتماد للطلبات عبر المجالات
  axios.defaults.withCredentials = true;

  // إضافة معترض للطلبات
  axios.interceptors.request.use(
    config => {
      // إضافة رأس CORS إذا كان الطلب لخدمة خارجية
      if (!config.url.startsWith(baseURL) && !config.url.startsWith('/')) {
        config.headers['Access-Control-Allow-Origin'] = '*';
        config.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS';
        config.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization';
      }

      // تعديل مسارات API للذكاء الاصطناعي
      if (config.url.includes('/api/ai-service') || config.url.includes('/api/disease-diagnosis')) {
        // إضافة معلمة لتجنب التخزين المؤقت
        const separator = config.url.includes('?') ? '&' : '?';
        config.url = `${config.url}${separator}_=${new Date().getTime()}`;
      }

      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );

  // إضافة معترض للاستجابات
  axios.interceptors.response.use(
    response => {
      return response;
    },
    error => {
      // معالجة أخطاء CORS
      if (error.message && error.message.includes('Network Error')) {
        console.error('خطأ في الشبكة - قد يكون بسبب إعدادات CORS:', error);

        // إعادة المحاولة باستخدام وسيط محلي إذا كان الطلب لخدمة خارجية
        const originalRequest = error.config;
        if (!originalRequest._retry && !originalRequest.url.startsWith(baseURL) && !originalRequest.url.startsWith('/')) {
          originalRequest._retry = true;

          // استخدام وسيط محلي
          const proxyUrl = `/api/proxy?url=${encodeURIComponent(originalRequest.url)}`;
          return axios(proxyUrl, originalRequest);
        }
      }

      return Promise.reject(error);
    }
  );
};

export default {
  setupCorsConfig
};
