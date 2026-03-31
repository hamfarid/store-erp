/**
 * خدمة الإشعارات (Notification Service)
 * @file frontend/src/services/notificationService.js
 */

import apiClient from './apiClient';

export const notificationService = {
  // ==================== الإشعارات ====================

  /**
   * الحصول على جميع الإشعارات
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        is_read: params.isRead !== undefined ? params.isRead : '',
        type: params.type || '',
        priority: params.priority || '',
        ...params
      };

      const response = await apiClient.get('/api/notifications', queryParams);
      return {
        notifications: response.notifications || response.data || [],
        total: response.total || 0,
        unreadCount: response.unread_count || 0,
        page: response.page || 1
      };
    } catch (error) {
      throw new Error(`فشل في تحميل الإشعارات: ${error.message}`);
    }
  },

  /**
   * الحصول على إشعار بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/notifications/${id}`);
      return response.notification || response;
    } catch (error) {
      throw new Error(`فشل في تحميل الإشعار: ${error.message}`);
    }
  },

  /**
   * الحصول على الإشعارات غير المقروءة
   */
  async getUnread(params = {}) {
    try {
      const response = await apiClient.get('/api/notifications/unread', params);
      return {
        notifications: response.notifications || response.data || [],
        count: response.count || 0
      };
    } catch (error) {
      throw new Error(`فشل في تحميل الإشعارات غير المقروءة: ${error.message}`);
    }
  },

  // ==================== إدارة الإشعارات ====================

  /**
   * تحديد إشعار كمقروء
   */
  async markAsRead(id) {
    try {
      const response = await apiClient.patch(`/api/notifications/${id}/read`);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث الإشعار: ${error.message}`);
    }
  },

  /**
   * تحديد جميع الإشعارات كمقروءة
   */
  async markAllAsRead() {
    try {
      const response = await apiClient.post('/api/notifications/mark-all-read');
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث الإشعارات: ${error.message}`);
    }
  },

  /**
   * حذف إشعار
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/notifications/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف الإشعار: ${error.message}`);
    }
  },

  /**
   * حذف جميع الإشعارات
   */
  async deleteAll() {
    try {
      const response = await apiClient.delete('/api/notifications/all');
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف الإشعارات: ${error.message}`);
    }
  },

  /**
   * أرشفة الإشعارات القديمة
   */
  async archiveOld(daysOld = 30) {
    try {
      const response = await apiClient.post('/api/notifications/archive', { days_old: daysOld });
      return response;
    } catch (error) {
      throw new Error(`فشل في الأرشفة: ${error.message}`);
    }
  },

  // ==================== إعدادات الإشعارات ====================

  /**
   * الحصول على إعدادات الإشعارات
   */
  async getSettings() {
    try {
      const response = await apiClient.get('/api/notifications/settings');
      return response.settings || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإعدادات: ${error.message}`);
    }
  },

  /**
   * تحديث إعدادات الإشعارات
   */
  async updateSettings(settings) {
    try {
      const response = await apiClient.put('/api/notifications/settings', settings);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث الإعدادات: ${error.message}`);
    }
  },

  /**
   * تفعيل/إلغاء تفعيل نوع إشعار
   */
  async toggleNotificationType(type, enabled) {
    try {
      const response = await apiClient.patch(`/api/notifications/settings/type/${type}`, { enabled });
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث إعداد الإشعار: ${error.message}`);
    }
  },

  // ==================== إرسال الإشعارات ====================

  /**
   * إرسال إشعار لمستخدم
   */
  async sendToUser(userId, notification) {
    try {
      const response = await apiClient.post('/api/notifications/send/user', {
        user_id: userId,
        ...notification
      });
      return response;
    } catch (error) {
      throw new Error(`فشل في إرسال الإشعار: ${error.message}`);
    }
  },

  /**
   * إرسال إشعار لجميع المستخدمين
   */
  async sendBroadcast(notification) {
    try {
      const response = await apiClient.post('/api/notifications/send/broadcast', notification);
      return response;
    } catch (error) {
      throw new Error(`فشل في إرسال الإشعار: ${error.message}`);
    }
  },

  /**
   * إرسال إشعار لدور معين
   */
  async sendToRole(roleId, notification) {
    try {
      const response = await apiClient.post('/api/notifications/send/role', {
        role_id: roleId,
        ...notification
      });
      return response;
    } catch (error) {
      throw new Error(`فشل في إرسال الإشعار: ${error.message}`);
    }
  },

  // ==================== الإحصائيات ====================

  /**
   * إحصائيات الإشعارات
   */
  async getStats() {
    try {
      const response = await apiClient.get('/api/notifications/stats');
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  /**
   * عدد الإشعارات غير المقروءة
   */
  async getUnreadCount() {
    try {
      const response = await apiClient.get('/api/notifications/unread-count');
      return response.count || 0;
    } catch (error) {
      return 0;
    }
  },

  // ==================== أنواع الإشعارات ====================

  /**
   * الحصول على أنواع الإشعارات
   */
  async getNotificationTypes() {
    try {
      const response = await apiClient.get('/api/notifications/types');
      return response.types || [];
    } catch (error) {
      throw new Error(`فشل في تحميل أنواع الإشعارات: ${error.message}`);
    }
  }
};

export default notificationService;
