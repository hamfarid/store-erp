/**
 * Permission Context - إدارة الصلاحيات في الواجهة الأمامية
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/contexts/PermissionContext.js
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import apiClient from '../services/apiClient';

// إنشاء Context
const PermissionContext = createContext();

// Hook للوصول للصلاحيات
export const usePermissions = () => {
  const context = useContext(PermissionContext);
  if (!context) {
    throw new Error('usePermissions must be used within PermissionProvider');
  }
  return context;
};

// Provider Component
export const PermissionProvider = ({ children }) => {
  // ==================== State Management ====================
  
  const [permissions, setPermissions] = useState({
    warehouses: {},
    customers: {},
    general: {},
  });
  
  const [userWarehouses, setUserWarehouses] = useState([]);
  const [userCustomers, setUserCustomers] = useState([]);
  const [userRole, setUserRole] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ==================== Data Loading ====================

  /**
   * تحميل صلاحيات المستخدم
   */
  const loadUserPermissions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // التحقق من وجود توكن
      if (!apiClient.isAuthenticated()) {
        setLoading(false);
        return;
      }

      // تحميل صلاحيات المستخدم
      const response = await apiClient.get('/api/user/permissions');
      
      // تحديث البيانات
      setPermissions(response.permissions || {});
      setUserWarehouses(response.warehouses || []);
      setUserCustomers(response.customers || []);
      setUserRole(response.role || null);
      setIsAdmin(response.is_admin || false);

    } catch (error) {
      setError(error.message);
      
      // في حالة خطأ 401، مسح البيانات
      if (error.message.includes('401')) {
        apiClient.clearToken();
        setPermissions({ warehouses: {}, customers: {}, general: {} });
        setUserWarehouses([]);
        setUserCustomers([]);
        setUserRole(null);
        setIsAdmin(false);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * تحديث الصلاحيات
   */
  const refreshPermissions = useCallback(() => {
    return loadUserPermissions();
  }, [loadUserPermissions]);

  // تحميل الصلاحيات عند بدء التطبيق
  useEffect(() => {
    loadUserPermissions();
  }, [loadUserPermissions]);

  // ==================== Permission Checking Functions ====================

  /**
   * فحص صلاحية المخزن
   */
  const canAccessWarehouse = useCallback((warehouseId, permissionType = 'view') => {
    // الأدمن له صلاحية على كل شيء
    if (isAdmin) return true;
    
    // التحقق من وجود الصلاحية
    const warehousePermissions = permissions.warehouses?.[warehouseId];
    if (!warehousePermissions) return false;
    
    // فحص نوع الصلاحية المطلوبة
    const permissionMap = {
      'view': warehousePermissions.can_view,
      'edit': warehousePermissions.can_edit,
      'create': warehousePermissions.can_create,
      'delete': warehousePermissions.can_delete,
      'reports': warehousePermissions.can_view_reports,
      'financial': warehousePermissions.can_view_financial,
      'approve': warehousePermissions.can_approve,
      'manage_stock': warehousePermissions.can_manage_stock,
      'view_cost_prices': warehousePermissions.can_view_cost_prices,
      'edit_prices': warehousePermissions.can_edit_prices,
      'view_profit_margins': warehousePermissions.can_view_profit_margins,
      'access_analytics': warehousePermissions.can_access_analytics,
    };
    
    return permissionMap[permissionType] || false;
  }, [permissions.warehouses, isAdmin]);

  /**
   * فحص صلاحية العميل
   */
  const canAccessCustomer = useCallback((customerId, permissionType = 'view') => {
    // الأدمن له صلاحية على كل شيء
    if (isAdmin) return true;
    
    // التحقق من وجود الصلاحية
    const customerPermissions = permissions.customers?.[customerId];
    if (!customerPermissions) return false;
    
    // فحص نوع الصلاحية المطلوبة
    const permissionMap = {
      'view': customerPermissions.can_view,
      'edit': customerPermissions.can_edit,
      'create_invoices': customerPermissions.can_create_invoices,
      'financial': customerPermissions.can_view_financial,
      'approve_credit': customerPermissions.can_approve_credit,
      'modify_prices': customerPermissions.can_modify_prices,
    };
    
    return permissionMap[permissionType] || false;
  }, [permissions.customers, isAdmin]);

  /**
   * فحص الصلاحيات العامة
   */
  const hasGeneralPermission = useCallback((permissionType) => {
    // الأدمن له صلاحية على كل شيء
    if (isAdmin) return true;
    
    return permissions.general?.[permissionType] || false;
  }, [permissions.general, isAdmin]);

  /**
   * فحص صلاحية الدور
   */
  const hasRole = useCallback((roleName) => {
    if (Array.isArray(roleName)) {
      return roleName.includes(userRole?.name);
    }
    return userRole?.name === roleName;
  }, [userRole]);

  // ==================== Utility Functions ====================

  /**
   * الحصول على المخازن المصرح بها
   */
  const getAccessibleWarehouses = useCallback((permissionType = 'view') => {
    if (isAdmin) return userWarehouses;
    
    return userWarehouses.filter(warehouse => 
      canAccessWarehouse(warehouse.id, permissionType)
    );
  }, [userWarehouses, canAccessWarehouse, isAdmin]);

  /**
   * الحصول على العملاء المصرح بهم
   */
  const getAccessibleCustomers = useCallback((permissionType = 'view') => {
    if (isAdmin) return userCustomers;
    
    return userCustomers.filter(customer => 
      canAccessCustomer(customer.id, permissionType)
    );
  }, [userCustomers, canAccessCustomer, isAdmin]);

  /**
   * الحصول على معرفات المخازن المصرح بها
   */
  const getAccessibleWarehouseIds = useCallback((permissionType = 'view') => {
    return getAccessibleWarehouses(permissionType).map(w => w.id);
  }, [getAccessibleWarehouses]);

  /**
   * الحصول على معرفات العملاء المصرح بهم
   */
  const getAccessibleCustomerIds = useCallback((permissionType = 'view') => {
    return getAccessibleCustomers(permissionType).map(c => c.id);
  }, [getAccessibleCustomers]);

  /**
   * فحص ما إذا كان المستخدم له صلاحية على أي مخزن
   */
  const hasAnyWarehouseAccess = useCallback((permissionType = 'view') => {
    if (isAdmin) return userWarehouses.length > 0;
    return getAccessibleWarehouses(permissionType).length > 0;
  }, [isAdmin, userWarehouses, getAccessibleWarehouses]);

  /**
   * فحص ما إذا كان المستخدم له صلاحية على أي عميل
   */
  const hasAnyCustomerAccess = useCallback((permissionType = 'view') => {
    if (isAdmin) return userCustomers.length > 0;
    return getAccessibleCustomers(permissionType).length > 0;
  }, [isAdmin, userCustomers, getAccessibleCustomers]);

  // ==================== Permission Summary ====================

  /**
   * الحصول على ملخص الصلاحيات
   */
  const getPermissionSummary = useCallback(() => {
    return {
      isAdmin,
      role: userRole,
      warehouseCount: userWarehouses.length,
      customerCount: userCustomers.length,
      accessibleWarehouses: getAccessibleWarehouses().length,
      accessibleCustomers: getAccessibleCustomers().length,
      permissions: {
        warehouses: Object.keys(permissions.warehouses || {}).length,
        customers: Object.keys(permissions.customers || {}).length,
        general: Object.keys(permissions.general || {}).length,
      }
    };
  }, [
    isAdmin, 
    userRole, 
    userWarehouses, 
    userCustomers, 
    getAccessibleWarehouses, 
    getAccessibleCustomers, 
    permissions
  ]);

  // ==================== Context Value ====================

  const contextValue = {
    // البيانات الأساسية
    permissions,
    userWarehouses,
    userCustomers,
    userRole,
    isAdmin,
    loading,
    error,

    // وظائف فحص الصلاحيات
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission,
    hasRole,

    // وظائف الحصول على البيانات المصرح بها
    getAccessibleWarehouses,
    getAccessibleCustomers,
    getAccessibleWarehouseIds,
    getAccessibleCustomerIds,

    // وظائف فحص وجود صلاحيات
    hasAnyWarehouseAccess,
    hasAnyCustomerAccess,

    // وظائف مساعدة
    getPermissionSummary,
    refreshPermissions,
    
    // حالة التحميل والأخطاء
    isLoading: loading,
    hasError: !!error,
    errorMessage: error,
  };

  return (
    <PermissionContext.Provider value={contextValue}>
      {children}
    </PermissionContext.Provider>
  );
};

// ==================== Higher Order Components ====================

/**
 * HOC للحماية بالصلاحيات
 */
export const withPermissions = (WrappedComponent, permissionConfig = {}) => {
  return function PermissionWrappedComponent(props) {
    const permissions = usePermissions();
    
    // تمرير الصلاحيات كـ props
    const enhancedProps = {
      ...props,
      permissions,
      ...permissionConfig,
    };
    
    return <WrappedComponent {...enhancedProps} />;
  };
};

/**
 * HOC للتحقق من صلاحية معينة
 */
export const requirePermission = (permissionCheck, fallbackComponent = null) => {
  return function (_WrappedComponent) {
    return function PermissionCheckedComponent(props) {
      const permissions = usePermissions();
      
      // فحص الصلاحية
      let hasPermission = false;
      
      if (typeof permissionCheck === 'function') {
        hasPermission = permissionCheck(permissions);
      } else if (typeof permissionCheck === 'string') {
        hasPermission = permissions.hasGeneralPermission(permissionCheck);
      }
      
      // عرض المكون أو البديل
      if (hasPermission) {
        return <WrappedComponent {...props} permissions={permissions} />;
      } else {
        return fallbackComponent || <div>غير مصرح بالوصول</div>;
      }
    };
  };
};

export default PermissionContext;

