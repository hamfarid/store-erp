/**
 * Permission Service
 * خدمة الأذونات والأدوار
 */

import api from './api';

const permissionService = {
  /**
   * الحصول على قائمة الأدوار
   */
  async getRoles() {
    try {
      const response = await api.get('/permissions/roles');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على تفاصيل دور
   */
  async getRole(roleId) {
    try {
      const response = await api.get(`/permissions/roles/${roleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * إنشاء دور جديد
   */
  async createRole(data) {
    try {
      const response = await api.post('/permissions/roles', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * تحديث دور
   */
  async updateRole(roleId, data) {
    try {
      const response = await api.put(`/permissions/roles/${roleId}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * حذف دور
   */
  async deleteRole(roleId) {
    try {
      const response = await api.delete(`/permissions/roles/${roleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على قائمة الأذونات
   */
  async getPermissions() {
    try {
      const response = await api.get('/permissions');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على الأذونات مجمعة حسب المورد
   */
  async getPermissionsGrouped() {
    try {
      const response = await api.get('/permissions/grouped');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * تعيين دور لمستخدم
   */
  async assignRole(userId, roleId) {
    try {
      const response = await api.post(`/permissions/users/${userId}/roles`, {
        role_id: roleId
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * إزالة دور من مستخدم
   */
  async removeRole(userId, roleId) {
    try {
      const response = await api.delete(`/permissions/users/${userId}/roles/${roleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على أدوار مستخدم
   */
  async getUserRoles(userId) {
    try {
      const response = await api.get(`/permissions/users/${userId}/roles`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على أذونات مستخدم
   */
  async getUserPermissions(userId) {
    try {
      const response = await api.get(`/permissions/users/${userId}/permissions`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * التحقق من إذن معين
   */
  async checkPermission(resource, action) {
    try {
      const response = await api.get('/permissions/check', {
        params: { resource, action }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * منح أذونات لدور
   */
  async grantPermissions(roleId, permissions) {
    try {
      const response = await api.post(`/permissions/roles/${roleId}/grant`, {
        permissions
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * سحب أذونات من دور
   */
  async revokePermissions(roleId, permissions) {
    try {
      const response = await api.post(`/permissions/roles/${roleId}/revoke`, {
        permissions
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * التحقق من إذن محلياً (من الذاكرة المؤقتة)
   */
  hasPermission(resource, action) {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    // المسؤول الكامل
    if (user.is_superuser) {
      return true;
    }
    
    // التحقق من الأدوار
    const roles = user.roles || [];
    const permissionName = `${resource}.${action}`;
    
    for (const role of roles) {
      const permissions = role.permissions || [];
      
      // التحقق المباشر
      if (permissions.includes(permissionName)) {
        return true;
      }
      
      // التحقق من الإذن الشامل
      if (permissions.includes(`${resource}.*`)) {
        return true;
      }
      
      // التحقق من الإذن الكامل
      if (permissions.includes('*') || permissions.includes('all')) {
        return true;
      }
    }
    
    return false;
  },

  /**
   * التحقق من عدة أذونات
   */
  hasAnyPermission(permissions) {
    return permissions.some(perm => {
      const [resource, action] = perm.split('.');
      return this.hasPermission(resource, action);
    });
  },

  /**
   * التحقق من جميع الأذونات
   */
  hasAllPermissions(permissions) {
    return permissions.every(perm => {
      const [resource, action] = perm.split('.');
      return this.hasPermission(resource, action);
    });
  },

  /**
   * التحقق من دور معين
   */
  hasRole(roleName) {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const roles = user.roles || [];
    
    return roles.some(role => role.name === roleName);
  },

  /**
   * التحقق من أي دور من القائمة
   */
  hasAnyRole(roleNames) {
    return roleNames.some(roleName => this.hasRole(roleName));
  },

  /**
   * الحصول على أسماء أدوار المستخدم الحالي
   */
  getCurrentUserRoles() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const roles = user.roles || [];
    return roles.map(role => role.name);
  },

  /**
   * الحصول على أذونات المستخدم الحالي
   */
  getCurrentUserPermissions() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const roles = user.roles || [];
    
    const allPermissions = new Set();
    
    roles.forEach(role => {
      const permissions = role.permissions || [];
      permissions.forEach(perm => allPermissions.add(perm));
    });
    
    return Array.from(allPermissions);
  },

  /**
   * تنسيق اسم الإذن للعرض
   */
  formatPermissionName(permissionName) {
    const names = {
      // المنتجات
      'products.create': 'إنشاء منتج',
      'products.read': 'عرض المنتجات',
      'products.update': 'تعديل منتج',
      'products.delete': 'حذف منتج',
      
      // اللوطات
      'batches.create': 'إنشاء لوط',
      'batches.read': 'عرض اللوطات',
      'batches.update': 'تعديل لوط',
      'batches.delete': 'حذف لوط',
      
      // المبيعات
      'sales.create': 'إنشاء فاتورة بيع',
      'sales.read': 'عرض المبيعات',
      'sales.update': 'تعديل فاتورة',
      'sales.delete': 'حذف فاتورة',
      
      // المشتريات
      'purchases.create': 'إنشاء أمر شراء',
      'purchases.read': 'عرض المشتريات',
      'purchases.update': 'تعديل أمر شراء',
      'purchases.delete': 'حذف أمر شراء',
      
      // نقطة البيع
      'pos.access': 'الوصول لنقطة البيع',
      'pos.open_session': 'فتح جلسة',
      'pos.close_session': 'إغلاق جلسة',
      
      // التقارير
      'reports.sales': 'تقارير المبيعات',
      'reports.purchases': 'تقارير المشتريات',
      'reports.inventory': 'تقارير المخزون',
      'reports.financial': 'تقارير مالية'
    };
    
    return names[permissionName] || permissionName;
  },

  /**
   * تنسيق اسم المورد للعرض
   */
  formatResourceName(resource) {
    const names = {
      'products': 'المنتجات',
      'batches': 'اللوطات',
      'sales': 'المبيعات',
      'purchases': 'المشتريات',
      'pos': 'نقطة البيع',
      'customers': 'العملاء',
      'suppliers': 'الموردين',
      'warehouses': 'المخازن',
      'reports': 'التقارير',
      'users': 'المستخدمين',
      'roles': 'الأدوار',
      'settings': 'الإعدادات',
      'quality': 'الجودة'
    };
    
    return names[resource] || resource;
  },

  /**
   * تنسيق اسم الإجراء للعرض
   */
  formatActionName(action) {
    const names = {
      'create': 'إنشاء',
      'read': 'عرض',
      'update': 'تعديل',
      'delete': 'حذف',
      'approve': 'اعتماد',
      'cancel': 'إلغاء',
      'access': 'الوصول',
      'export': 'تصدير',
      'import': 'استيراد'
    };
    
    return names[action] || action;
  }
};

export default permissionService;
