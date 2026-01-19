/**
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/services/securityService.js
 * الوصف: خدمة الأمان للواجهة الأمامية
 * المؤلف: فريق Gaara ERP
 * تاريخ الإنشاء: 29 مايو 2025
 */

import { API_BASE_URL } from '@/config';
import axios from 'axios';

const API_URL = `${API_BASE_URL}/api/security`;

/**
 * خدمة الأمان للواجهة الأمامية
 * توفر واجهة للتفاعل مع خدمات الأمان في الواجهة الخلفية
 */
class SecurityService {
  /**
   * إلغاء حظر مستخدم
   * 
   * @param {string} userId - معرف المستخدم المراد إلغاء حظره
   * @returns {Promise} وعد يحتوي على نتيجة العملية
   */
  async unblockUser(userId) {
    return axios.post(`${API_URL}/unblock-user/${userId}`);
  }

  /**
   * الحصول على قائمة المستخدمين المحظورين
   * 
   * @returns {Promise} وعد يحتوي على قائمة المستخدمين المحظورين
   */
  async getBlockedUsers() {
    return axios.get(`${API_URL}/blocked-users`);
  }

  /**
   * التحقق مما إذا كان المستخدم محظوراً
   * 
   * @param {string} userId - معرف المستخدم
   * @returns {Promise} وعد يحتوي على حالة حظر المستخدم
   */
  async isUserBlocked(userId) {
    return axios.get(`${API_URL}/is-blocked/${userId}`);
  }

  /**
   * الحصول على إحصائيات الأمان
   * 
   * @returns {Promise} وعد يحتوي على إحصائيات الأمان
   */
  async getSecurityStats() {
    return axios.get(`${API_URL}/stats`);
  }

  /**
   * تسجيل حدث أمني
   * 
   * @param {Object} eventData - بيانات الحدث الأمني
   * @returns {Promise} وعد يحتوي على نتيجة العملية
   */
  async logSecurityEvent(eventData) {
    return axios.post(`${API_URL}/log-event`, eventData);
  }
}

export default new SecurityService();
