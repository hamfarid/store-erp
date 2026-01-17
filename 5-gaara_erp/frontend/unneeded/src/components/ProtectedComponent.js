/**
 * مكونات الحماية بالصلاحيات
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/components/ProtectedComponent.js
 */

import React from 'react'
import { AlertTriangle as WarningIcon, Lock as LockIcon } from 'lucide-react';
import { Alert, Box, CircularProgress, Typography } from '@mui/material';
;
import { usePermissions } from '../contexts/PermissionContext';

// ==================== مكون الحماية الأساسي ====================

export const ProtectedComponent = ({ 
  children, 
  requiredPermission = 'view',
  warehouseId = null,
  customerId = null,
  generalPermission = null,
  requiredRole = null,
  requireAdmin = false,
  fallback = null,
  showFallback = true,
  className = '',
  ...props 
}) => {
  const {
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission,
    hasRole,
    isAdmin,
    loading,
    error
  } = usePermissions();

  // عرض حالة التحميل
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={2}>
        <CircularProgress size={24} />
        <Typography variant="body2" sx={{ ml: 1 }}>
          جاري التحقق من الصلاحيات...
        </Typography>
      </Box>
    );
  }

  // عرض خطأ في تحميل الصلاحيات
  if (error) {
    return (
      <Alert severity="error" icon={<WarningIcon />}>
        خطأ في تحميل الصلاحيات: {error}
      </Alert>
    );
  }

  // فحص الصلاحيات
  let hasPermission = false;

  // فحص صلاحية الأدمن
  if (requireAdmin) {
    hasPermission = isAdmin;
  }
  // فحص الدور المطلوب
  else if (requiredRole) {
    hasPermission = hasRole(requiredRole);
  }
  // فحص صلاحية المخزن
  else if (warehouseId) {
    hasPermission = canAccessWarehouse(warehouseId, requiredPermission);
  }
  // فحص صلاحية العميل
  else if (customerId) {
    hasPermission = canAccessCustomer(customerId, requiredPermission);
  }
  // فحص الصلاحية العامة
  else if (generalPermission) {
    hasPermission = hasGeneralPermission(generalPermission);
  }
  // إذا لم يتم تحديد أي شرط، السماح بالوصول
  else {
    hasPermission = true;
  }

  // عرض المحتوى أو البديل
  if (hasPermission) {
    return (
      <div className={className} {...props}>
        {children}
      </div>
    );
  } else {
    // عرض البديل المخصص
    if (fallback) {
      return fallback;
    }
    
    // عرض البديل الافتراضي
    if (showFallback) {
      return (
        <Alert 
          severity="warning" 
          icon={<LockIcon />}
          sx={{ my: 1 }}
        >
          <Typography variant="body2">
            غير مصرح لك بالوصول إلى هذا المحتوى
          </Typography>
        </Alert>
      );
    }
    
    // عدم عرض أي شيء
    return null;
  }
};

// ==================== مكونات متخصصة ====================

/**
 * مكون حماية المخزن
 */
export const WarehouseProtected = ({ 
  warehouseId, 
  permission = 'view', 
  children, 
  ...props 
}) => {
  return (
    <ProtectedComponent
      warehouseId={warehouseId}
      requiredPermission={permission}
      {...props}
    >
      {children}
    </ProtectedComponent>
  );
};

/**
 * مكون حماية العميل
 */
export const CustomerProtected = ({ 
  customerId, 
  permission = 'view', 
  children, 
  ...props 
}) => {
  return (
    <ProtectedComponent
      customerId={customerId}
      requiredPermission={permission}
      {...props}
    >
      {children}
    </ProtectedComponent>
  );
};

/**
 * مكون حماية الأدمن فقط
 */
export const AdminOnly = ({ children, ...props }) => {
  return (
    <ProtectedComponent
      requireAdmin={true}
      {...props}
    >
      {children}
    </ProtectedComponent>
  );
};

/**
 * مكون حماية بالدور
 */
export const RoleProtected = ({ role, children, ...props }) => {
  return (
    <ProtectedComponent
      requiredRole={role}
      {...props}
    >
      {children}
    </ProtectedComponent>
  );
};

// ==================== مكونات الأزرار المحمية ====================

/**
 * زر محمي بالصلاحيات
 */
export const ProtectedButton = ({ 
  children,
  onClick,
  disabled = false,
  requiredPermission = 'view',
  warehouseId = null,
  customerId = null,
  generalPermission = null,
  requiredRole = null,
  requireAdmin = false,
  hideIfNoPermission = false,
  disableIfNoPermission = true,
  component: ButtonComponent = 'button',
  ...props 
}) => {
  const {
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission,
    hasRole,
    isAdmin,
    loading
  } = usePermissions();

  // فحص الصلاحيات
  let hasPermission = false;

  if (requireAdmin) {
    hasPermission = isAdmin;
  } else if (requiredRole) {
    hasPermission = hasRole(requiredRole);
  } else if (warehouseId) {
    hasPermission = canAccessWarehouse(warehouseId, requiredPermission);
  } else if (customerId) {
    hasPermission = canAccessCustomer(customerId, requiredPermission);
  } else if (generalPermission) {
    hasPermission = hasGeneralPermission(generalPermission);
  } else {
    hasPermission = true;
  }

  // إخفاء الزر إذا لم تكن هناك صلاحية
  if (!hasPermission && hideIfNoPermission) {
    return null;
  }

  // تحديد حالة التعطيل
  const isDisabled = disabled || loading || (!hasPermission && disableIfNoPermission);

  // تحديد دالة النقر
  const handleClick = hasPermission ? onClick : undefined;

  // عرض الزر
  if (typeof ButtonComponent === 'string') {
    return (
      <ButtonComponent
        {...props}
        disabled={isDisabled}
        onClick={handleClick}
        title={!hasPermission ? 'غير مصرح لك بهذا الإجراء' : props.title}
      >
        {children}
      </ButtonComponent>
    );
  } else {
    return (
      <ButtonComponent
        {...props}
        disabled={isDisabled}
        onClick={handleClick}
        title={!hasPermission ? 'غير مصرح لك بهذا الإجراء' : props.title}
      >
        {children}
      </ButtonComponent>
    );
  }
};

// ==================== مكونات النماذج المحمية ====================

/**
 * حقل نموذج محمي
 */
export const ProtectedField = ({ 
  children,
  requiredPermission = 'edit',
  warehouseId = null,
  customerId = null,
  generalPermission = null,
  readOnlyIfNoPermission = true,
  hideIfNoPermission = false,
  ...props 
}) => {
  const {
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission
  } = usePermissions();

  // فحص الصلاحيات
  let hasPermission = false;

  if (warehouseId) {
    hasPermission = canAccessWarehouse(warehouseId, requiredPermission);
  } else if (customerId) {
    hasPermission = canAccessCustomer(customerId, requiredPermission);
  } else if (generalPermission) {
    hasPermission = hasGeneralPermission(generalPermission);
  } else {
    hasPermission = true;
  }

  // إخفاء الحقل إذا لم تكن هناك صلاحية
  if (!hasPermission && hideIfNoPermission) {
    return null;
  }

  // تعديل خصائص الحقل حسب الصلاحية
  const fieldProps = {
    ...props,
    readOnly: !hasPermission && readOnlyIfNoPermission,
    disabled: !hasPermission && readOnlyIfNoPermission,
  };

  return React.cloneElement(children, fieldProps);
};

// ==================== مكونات القوائم المحمية ====================

/**
 * عنصر قائمة محمي
 */
export const ProtectedMenuItem = ({ 
  children,
  requiredPermission = 'view',
  warehouseId = null,
  customerId = null,
  generalPermission = null,
  requiredRole = null,
  requireAdmin = false,
  hideIfNoPermission = true,
  ...props 
}) => {
  const {
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission,
    hasRole,
    isAdmin
  } = usePermissions();

  // فحص الصلاحيات
  let hasPermission = false;

  if (requireAdmin) {
    hasPermission = isAdmin;
  } else if (requiredRole) {
    hasPermission = hasRole(requiredRole);
  } else if (warehouseId) {
    hasPermission = canAccessWarehouse(warehouseId, requiredPermission);
  } else if (customerId) {
    hasPermission = canAccessCustomer(customerId, requiredPermission);
  } else if (generalPermission) {
    hasPermission = hasGeneralPermission(generalPermission);
  } else {
    hasPermission = true;
  }

  // إخفاء العنصر إذا لم تكن هناك صلاحية
  if (!hasPermission && hideIfNoPermission) {
    return null;
  }

  return (
    <div {...props}>
      {children}
    </div>
  );
};

// ==================== Hook مساعد ====================

/**
 * Hook للحصول على حالة الصلاحية
 */
export const usePermissionCheck = ({
  requiredPermission = 'view',
  warehouseId = null,
  customerId = null,
  generalPermission = null,
  requiredRole = null,
  requireAdmin = false
}) => {
  const {
    canAccessWarehouse,
    canAccessCustomer,
    hasGeneralPermission,
    hasRole,
    isAdmin,
    loading
  } = usePermissions();

  // فحص الصلاحيات
  let hasPermission = false;

  if (requireAdmin) {
    hasPermission = isAdmin;
  } else if (requiredRole) {
    hasPermission = hasRole(requiredRole);
  } else if (warehouseId) {
    hasPermission = canAccessWarehouse(warehouseId, requiredPermission);
  } else if (customerId) {
    hasPermission = canAccessCustomer(customerId, requiredPermission);
  } else if (generalPermission) {
    hasPermission = hasGeneralPermission(generalPermission);
  } else {
    hasPermission = true;
  }

  return {
    hasPermission,
    loading,
    canAccess: hasPermission,
    isChecking: loading
  };
};

export default ProtectedComponent;

