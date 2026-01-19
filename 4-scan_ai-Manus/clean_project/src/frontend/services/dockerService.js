/*
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/dockerService.js
 * الوصف: خدمة إدارة حاويات Docker من واجهة المستخدم
 * المؤلف: فريق تطوير Gaara ERP
 * تاريخ الإنشاء: 30 مايو 2025
 */

import { API_BASE_URL } from '@/frontend/config/api';
import axios from 'axios';

const API_URL = `${API_BASE_URL}/docker`;

/**
 * خدمة إدارة حاويات Docker
 */
const dockerService = {
  /**
   * الحصول على جميع الحاويات
   * @returns {Promise<Object>} الحاويات مقسمة حسب النوع
   */
  async getContainers() {
    try {
      const response = await axios.get(`${API_URL}/containers`);
      return response.data;
    } catch (error) {
      console.error('Error fetching containers:', error);
      throw error;
    }
  },

  /**
   * الحصول على الحاويات المتاحة للتثبيت
   * @param {string} type نوع الحاوية
   * @returns {Promise<Array>} قائمة الحاويات المتاحة
   */
  async getAvailableContainers(type) {
    try {
      const response = await axios.get(`${API_URL}/available`, {
        params: { type }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching available containers:', error);
      throw error;
    }
  },

  /**
   * تشغيل حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} نتيجة العملية
   */
  async startContainer(containerId) {
    try {
      const response = await axios.post(`${API_URL}/containers/${containerId}/start`);
      return response.data;
    } catch (error) {
      console.error('Error starting container:', error);
      throw error;
    }
  },

  /**
   * إيقاف حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} نتيجة العملية
   */
  async stopContainer(containerId) {
    try {
      const response = await axios.post(`${API_URL}/containers/${containerId}/stop`);
      return response.data;
    } catch (error) {
      console.error('Error stopping container:', error);
      throw error;
    }
  },

  /**
   * إعادة تشغيل حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} نتيجة العملية
   */
  async restartContainer(containerId) {
    try {
      const response = await axios.post(`${API_URL}/containers/${containerId}/restart`);
      return response.data;
    } catch (error) {
      console.error('Error restarting container:', error);
      throw error;
    }
  },

  /**
   * الحصول على سجلات حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<string>} سجلات الحاوية
   */
  async getContainerLogs(containerId) {
    try {
      const response = await axios.get(`${API_URL}/containers/${containerId}/logs`);
      return response.data;
    } catch (error) {
      console.error('Error fetching container logs:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاوية جديدة
   * @param {Object} containerData بيانات الحاوية
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installContainer(containerData) {
    try {
      const response = await axios.post(`${API_URL}/install`, containerData);
      return response.data;
    } catch (error) {
      console.error('Error installing container:', error);
      throw error;
    }
  },

  /**
   * حذف حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} نتيجة العملية
   */
  async removeContainer(containerId) {
    try {
      const response = await axios.delete(`${API_URL}/containers/${containerId}`);
      return response.data;
    } catch (error) {
      console.error('Error removing container:', error);
      throw error;
    }
  },

  /**
   * تحديث إعدادات حاوية
   * @param {string} containerId معرف الحاوية
   * @param {Object} config الإعدادات الجديدة
   * @returns {Promise<Object>} نتيجة العملية
   */
  async updateContainerConfig(containerId, config) {
    try {
      const response = await axios.put(`${API_URL}/containers/${containerId}/config`, config);
      return response.data;
    } catch (error) {
      console.error('Error updating container config:', error);
      throw error;
    }
  },

  /**
   * الحصول على معلومات حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} معلومات الحاوية
   */
  async getContainerInfo(containerId) {
    try {
      const response = await axios.get(`${API_URL}/containers/${containerId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching container info:', error);
      throw error;
    }
  },

  /**
   * الحصول على إحصائيات حاوية
   * @param {string} containerId معرف الحاوية
   * @returns {Promise<Object>} إحصائيات الحاوية
   */
  async getContainerStats(containerId) {
    try {
      const response = await axios.get(`${API_URL}/containers/${containerId}/stats`);
      return response.data;
    } catch (error) {
      console.error('Error fetching container stats:', error);
      throw error;
    }
  },

  /**
   * تنفيذ أمر في حاوية
   * @param {string} containerId معرف الحاوية
   * @param {string} command الأمر المراد تنفيذه
   * @returns {Promise<Object>} نتيجة تنفيذ الأمر
   */
  async execCommand(containerId, command) {
    try {
      const response = await axios.post(`${API_URL}/containers/${containerId}/exec`, { command });
      return response.data;
    } catch (error) {
      console.error('Error executing command:', error);
      throw error;
    }
  },

  /**
   * الحصول على قائمة الصور المتاحة
   * @returns {Promise<Array>} قائمة الصور
   */
  async getImages() {
    try {
      const response = await axios.get(`${API_URL}/images`);
      return response.data;
    } catch (error) {
      console.error('Error fetching images:', error);
      throw error;
    }
  },

  /**
   * سحب صورة جديدة
   * @param {string} imageName اسم الصورة
   * @param {string} tag الإصدار
   * @returns {Promise<Object>} نتيجة العملية
   */
  async pullImage(imageName, tag = 'latest') {
    try {
      const response = await axios.post(`${API_URL}/images/pull`, { name: imageName, tag });
      return response.data;
    } catch (error) {
      console.error('Error pulling image:', error);
      throw error;
    }
  },

  /**
   * حذف صورة
   * @param {string} imageId معرف الصورة
   * @returns {Promise<Object>} نتيجة العملية
   */
  async removeImage(imageId) {
    try {
      const response = await axios.delete(`${API_URL}/images/${imageId}`);
      return response.data;
    } catch (error) {
      console.error('Error removing image:', error);
      throw error;
    }
  },

  /**
   * الحصول على حالة نظام Docker
   * @returns {Promise<Object>} حالة النظام
   */
  async getSystemInfo() {
    try {
      const response = await axios.get(`${API_URL}/system/info`);
      return response.data;
    } catch (error) {
      console.error('Error fetching system info:', error);
      throw error;
    }
  },

  /**
   * الحصول على استخدام الموارد
   * @returns {Promise<Object>} استخدام الموارد
   */
  async getResourceUsage() {
    try {
      const response = await axios.get(`${API_URL}/system/resources`);
      return response.data;
    } catch (error) {
      console.error('Error fetching resource usage:', error);
      throw error;
    }
  },

  /**
   * تنفيذ ملف docker-compose
   * @param {string} composeFile محتوى ملف docker-compose
   * @param {Object} options خيارات التنفيذ
   * @returns {Promise<Object>} نتيجة العملية
   */
  async composeUp(composeFile, options = {}) {
    try {
      const response = await axios.post(`${API_URL}/compose/up`, {
        composeFile,
        options
      });
      return response.data;
    } catch (error) {
      console.error('Error executing docker-compose up:', error);
      throw error;
    }
  },

  /**
   * إيقاف خدمات docker-compose
   * @param {string} composeFile محتوى ملف docker-compose
   * @param {Object} options خيارات التنفيذ
   * @returns {Promise<Object>} نتيجة العملية
   */
  async composeDown(composeFile, options = {}) {
    try {
      const response = await axios.post(`${API_URL}/compose/down`, {
        composeFile,
        options
      });
      return response.data;
    } catch (error) {
      console.error('Error executing docker-compose down:', error);
      throw error;
    }
  },

  /**
   * الحصول على حالة خدمات docker-compose
   * @param {string} composeFile محتوى ملف docker-compose
   * @returns {Promise<Object>} حالة الخدمات
   */
  async composeStatus(composeFile) {
    try {
      const response = await axios.post(`${API_URL}/compose/status`, { composeFile });
      return response.data;
    } catch (error) {
      console.error('Error fetching docker-compose status:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاويات البحث المتقدمة
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installAdvancedSearchContainers() {
    try {
      const response = await axios.post(`${API_URL}/install/advanced-search`);
      return response.data;
    } catch (error) {
      console.error('Error installing advanced search containers:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاويات GPU
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installGpuContainers() {
    try {
      const response = await axios.post(`${API_URL}/install/gpu`);
      return response.data;
    } catch (error) {
      console.error('Error installing GPU containers:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاويات تشخيص الأمراض
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installDiseaseDetectionContainers() {
    try {
      const response = await axios.post(`${API_URL}/install/disease-detection`);
      return response.data;
    } catch (error) {
      console.error('Error installing disease detection containers:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاويات التعلم الآلي والبحث عن الصور
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installMlImageSearchContainers() {
    try {
      const response = await axios.post(`${API_URL}/install/ml-image-search`);
      return response.data;
    } catch (error) {
      console.error('Error installing ML and image search containers:', error);
      throw error;
    }
  },

  /**
   * التحقق من توفر GPU
   * @returns {Promise<Object>} معلومات GPU
   */
  async checkGpuAvailability() {
    try {
      const response = await axios.get(`${API_URL}/system/gpu`);
      return response.data;
    } catch (error) {
      console.error('Error checking GPU availability:', error);
      throw error;
    }
  },

  /**
   * الحصول على قائمة الحاويات المثبتة من مصادر خارجية
   * @returns {Promise<Array>} قائمة الحاويات
   */
  async getExternalContainers() {
    try {
      const response = await axios.get(`${API_URL}/external`);
      return response.data;
    } catch (error) {
      console.error('Error fetching external containers:', error);
      throw error;
    }
  },

  /**
   * تثبيت حاوية من مصدر خارجي
   * @param {string} repoUrl رابط المستودع
   * @param {Object} options خيارات التثبيت
   * @returns {Promise<Object>} نتيجة العملية
   */
  async installExternalContainer(repoUrl, options = {}) {
    try {
      const response = await axios.post(`${API_URL}/external/install`, {
        repoUrl,
        options
      });
      return response.data;
    } catch (error) {
      console.error('Error installing external container:', error);
      throw error;
    }
  }
};

export default dockerService;
