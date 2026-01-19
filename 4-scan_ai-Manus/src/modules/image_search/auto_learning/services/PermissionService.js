# /home/ubuntu/image_search_integration/auto_learning/services/PermissionService.js

/**
 * خدمة الصلاحيات للتحقق من صلاحيات المستخدم
 * 
 * هذه الخدمة توفر الوظائف اللازمة للتحقق من صلاحيات المستخدم للوصول إلى مختلف
 * الموارد والعمليات في نظام البحث الذاتي الذكي.
 */

import ApiService from './ApiService';

const BASE_PATH = '/auth/permissions';

export default {
  /**
   * التحقق من امتلاك المستخدم لصلاحية معينة على مورد محدد
   * @param {string} action - الإجراء المطلوب (read, create, update, delete, etc.)
   * @param {string} resource - المورد المستهدف (keyword, source, search_engine, etc.)
   * @param {string|number} resourceId - معرف المورد (اختياري)
   * @returns {Promise<boolean>} وعد بنتيجة التحقق
   */
  async hasPermission(action, resource, resourceId = null) {
    try {
      const params = {
        action,
        resource,
      };
      
      if (resourceId !== null) {
        params.resource_id = resourceId;
      }
      
      const response = await ApiService.get(`${BASE_PATH}/check`, params);
      return response.data.has_permission === true;
    } catch (error) {
      console.error(`Error checking permission ${action}:${resource}`, error);
      // في حالة الخطأ، نفترض عدم وجود الصلاحية للأمان
      return false;
    }
  },

  /**
   * الحصول على قائمة الصلاحيات المتاحة للمستخدم الحالي
   * @returns {Promise<Array>} وعد بقائمة الصلاحيات
   */
  async getUserPermissions() {
    try {
      const response = await ApiService.get(`${BASE_PATH}/user`);
      return response.data.permissions || [];
    } catch (error) {
      console.error('Error fetching user permissions', error);
      return [];
    }
  },

  /**
   * التحقق من امتلاك المستخدم لأي من الصلاحيات المحددة
   * @param {Array<Object>} permissionChecks - قائمة من الصلاحيات للتحقق منها
   * @returns {Promise<boolean>} وعد بنتيجة التحقق
   */
  async hasAnyPermission(permissionChecks) {
    try {
      const response = await ApiService.post(`${BASE_PATH}/check-any`, {
        permission_checks: permissionChecks
      });
      return response.data.has_any_permission === true;
    } catch (error) {
      console.error('Error checking multiple permissions', error);
      return false;
    }
  },

  /**
   * التحقق من امتلاك المستخدم لجميع الصلاحيات المحددة
   * @param {Array<Object>} permissionChecks - قائمة من الصلاحيات للتحقق منها
   * @returns {Promise<boolean>} وعد بنتيجة التحقق
   */
  async hasAllPermissions(permissionChecks) {
    try {
      const response = await ApiService.post(`${BASE_PATH}/check-all`, {
        permission_checks: permissionChecks
      });
      return response.data.has_all_permissions === true;
    } catch (error) {
      console.error('Error checking multiple permissions', error);
      return false;
    }
  },

  /**
   * الحصول على قائمة الأدوار المتاحة للمستخدم الحالي
   * @returns {Promise<Array>} وعد بقائمة الأدوار
   */
  async getUserRoles() {
    try {
      const response = await ApiService.get(`${BASE_PATH}/roles`);
      return response.data.roles || [];
    } catch (error) {
      console.error('Error fetching user roles', error);
      return [];
    }
  },

  /**
   * التحقق من امتلاك المستخدم لدور معين
   * @param {string} role - الدور المطلوب التحقق منه
   * @returns {Promise<boolean>} وعد بنتيجة التحقق
   */
  async hasRole(role) {
    try {
      const response = await ApiService.get(`${BASE_PATH}/check-role`, { role });
      return response.data.has_role === true;
    } catch (error) {
      console.error(`Error checking role ${role}`, error);
      return false;
    }
  },

  /**
   * تحويل قائمة الصلاحيات إلى هيكل بيانات سهل الاستخدام
   * @param {Array} permissions - قائمة الصلاحيات
   * @returns {Object} هيكل بيانات الصلاحيات
   */
  mapPermissionsToStructure(permissions) {
    const permissionMap = {};
    
    permissions.forEach(permission => {
      const [resource, action] = permission.split(':');
      
      if (!permissionMap[resource]) {
        permissionMap[resource] = {};
      }
      
      permissionMap[resource][action] = true;
    });
    
    return permissionMap;
  }
};
