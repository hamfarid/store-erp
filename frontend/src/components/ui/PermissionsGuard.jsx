import React, { createContext, useContext, useState, useEffect } from 'react'
import { AlertTriangle, Lock, Shield } from 'lucide-react'

// سياق الصلاحيات
const PermissionsContext = createContext()

// مزود الصلاحيات
export const PermissionsProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [permissions, setPermissions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUserPermissions()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const loadUserPermissions = async () => {
    try {
      // استخدام بيانات تجريبية مباشرة بدلاً من API
      loadMockPermissions()
    } catch (error) {
      loadMockPermissions()
    } finally {
      setLoading(false)
    }
  }

  const loadMockPermissions = () => {
    // بيانات تجريبية للمستخدم والصلاحيات
    const mockUser = {
      id: 1,
      username: 'admin',
      role: 'مدير النظام',
      permissions: [
        'all', // صلاحية كاملة
        'products_read',
        'products_write',
        'customers_read',
        'customers_write',
        'suppliers_read',
        'suppliers_write',
        'invoices_read',
        'invoices_write',
        'inventory_read',
        'inventory_write',
        'lots_read',
        'lots_write',
        'accounting_read',
        'accounting_write',
        'reports_read',
        'users_read',
        'users_write',
        'settings_read',
        'settings_write'
      ]
    }
    
    setUser(mockUser)
    setPermissions(mockUser.permissions)
  }

  const hasPermission = (permission) => {
    if (!permissions || permissions.length === 0) return false
    
    // إذا كان لديه صلاحية 'all' فله كل الصلاحيات
    if (permissions.includes('all')) return true
    
    // التحقق من الصلاحية المحددة
    return permissions.includes(permission)
  }

  const hasAnyPermission = (permissionsList) => {
    return permissionsList.some(permission => hasPermission(permission))
  }

  const hasAllPermissions = (permissionsList) => {
    return permissionsList.every(permission => hasPermission(permission))
  }

  const value = {
    user,
    permissions,
    loading,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    refreshPermissions: loadUserPermissions
  }

  return (
    <PermissionsContext.Provider value={value}>
      {children}
    </PermissionsContext.Provider>
  )
}

// Hook لاستخدام الصلاحيات
export const usePermissions = () => {
  const context = useContext(PermissionsContext)
  if (!context) {
    throw new Error('usePermissions must be used within a PermissionsProvider')
  }
  return context
}

// مكون حماية الصلاحيات
export const PermissionGuard = ({ 
  permission, 
  permissions, 
  requireAll = false,
  fallback = null,
  children 
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions, loading } = usePermissions()

  if (loading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  let hasAccess = false

  if (permission) {
    hasAccess = hasPermission(permission)
  } else if (permissions) {
    hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
  }

  if (!hasAccess) {
    return fallback || <AccessDenied />
  }

  return children
}

// مكون رفض الوصول
const AccessDenied = ({ message = "ليس لديك صلاحية للوصول إلى هذا المحتوى" }) => (
  <div className="flex flex-col items-center justify-center p-8 bg-muted/50 rounded-lg border border-border">
    <Lock className="w-16 h-16 text-gray-400 mb-4" />
    <h3 className="text-lg font-semibold text-foreground mb-2">وصول مرفوض</h3>
    <p className="text-muted-foreground text-center">{message}</p>
  </div>
)

// مكون زر محمي بالصلاحيات
export const PermissionButton = ({ 
  permission, 
  permissions,
  requireAll = false,
  children,
  fallback = null,
  disabled = false,
  className = "",
  ...props 
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermissions()

  let hasAccess = false

  if (permission) {
    hasAccess = hasPermission(permission)
  } else if (permissions) {
    hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
  }

  if (!hasAccess) {
    return fallback
  }

  return (
    <button
      disabled={disabled}
      className={`${className} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      {...props}
    >
      {children}
    </button>
  )
}

// مكون رابط محمي بالصلاحيات
export const PermissionLink = ({ 
  permission, 
  permissions,
  requireAll = false,
  children,
  fallback = null,
  className = "",
  ...props 
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermissions()

  let hasAccess = false

  if (permission) {
    hasAccess = hasPermission(permission)
  } else if (permissions) {
    hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
  }

  if (!hasAccess) {
    return fallback
  }

  return (
    <a className={className} {...props}>
      {children}
    </a>
  )
}

// مكون عنصر قائمة محمي بالصلاحيات
export const PermissionMenuItem = ({ 
  permission, 
  permissions,
  requireAll = false,
  children,
  icon: Icon,
  badge,
  onClick,
  className = ""
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermissions()

  let hasAccess = false

  if (permission) {
    hasAccess = hasPermission(permission)
  } else if (permissions) {
    hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
  }

  if (!hasAccess) {
    return null
  }

  return (
    <div 
      onClick={onClick}
      className={`flex items-center justify-between p-3 hover:bg-muted/50 cursor-pointer transition-colors ${className}`}
    >
      <div className="flex items-center">
        {Icon && <Icon className="w-5 h-5 text-gray-400 ml-3" />}
        <span>{children}</span>
      </div>
      {badge && (
        <span className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs">
          {badge}
        </span>
      )}
    </div>
  )
}

// Hook للتحقق من الصلاحيات في المكونات
export const usePermissionCheck = () => {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermissions()

  const canAccess = (permission) => hasPermission(permission)
  
  const canAccessAny = (permissions) => hasAnyPermission(permissions)
  
  const canAccessAll = (permissions) => hasAllPermissions(permissions)

  const canRead = (module) => hasPermission(`${module}_read`)
  
  const canWrite = (module) => hasPermission(`${module}_write`)
  
  const canDelete = (module) => hasPermission(`${module}_delete`)
  
  const canManage = (module) => hasAnyPermission([
    `${module}_write`, 
    `${module}_delete`, 
    'all'
  ])

  return {
    canAccess,
    canAccessAny,
    canAccessAll,
    canRead,
    canWrite,
    canDelete,
    canManage
  }
}

// مكون عرض معلومات الصلاحيات (للتطوير)
export const PermissionsDebug = () => {
  const { user, permissions, loading } = usePermissions()

  if (loading) return <div>جاري التحميل...</div>

  return (
    <div className="bg-muted p-4 rounded-lg border border-border text-sm">
      <h4 className="font-semibold mb-2 flex items-center">
        <Shield className="w-4 h-4 ml-1" />
        معلومات الصلاحيات
      </h4>
      <div className="space-y-2">
        <p><strong>المستخدم:</strong> {user?.username || 'غير محدد'}</p>
        <p><strong>الدور:</strong> {user?.role || 'غير محدد'}</p>
        <p><strong>عدد الصلاحيات:</strong> {permissions.length}</p>
        <details>
          <summary className="cursor-pointer font-medium">عرض الصلاحيات</summary>
          <div className="mt-2 max-h-32 overflow-y-auto">
            {permissions.map((permission, index) => (
              <div key={index} className="text-xs bg-white px-2 py-1 rounded mb-1">
                {permission}
              </div>
            ))}
          </div>
        </details>
      </div>
    </div>
  )
}

// قائمة الصلاحيات المتاحة
export const PERMISSIONS = {
  // صلاحيات المنتجات
  PRODUCTS_READ: 'products_read',
  PRODUCTS_WRITE: 'products_write',
  PRODUCTS_DELETE: 'products_delete',

  // صلاحيات العملاء
  CUSTOMERS_READ: 'customers_read',
  CUSTOMERS_WRITE: 'customers_write',
  CUSTOMERS_DELETE: 'customers_delete',

  // صلاحيات الموردين
  SUPPLIERS_READ: 'suppliers_read',
  SUPPLIERS_WRITE: 'suppliers_write',
  SUPPLIERS_DELETE: 'suppliers_delete',

  // صلاحيات الفواتير
  INVOICES_READ: 'invoices_read',
  INVOICES_WRITE: 'invoices_write',
  INVOICES_DELETE: 'invoices_delete',

  // صلاحيات المخزون
  INVENTORY_READ: 'inventory_read',
  INVENTORY_WRITE: 'inventory_write',

  // صلاحيات اللوطات
  LOTS_READ: 'lots_read',
  LOTS_WRITE: 'lots_write',

  // صلاحيات المحاسبة
  ACCOUNTING_READ: 'accounting_read',
  ACCOUNTING_WRITE: 'accounting_write',

  // صلاحيات التقارير
  REPORTS_READ: 'reports_read',

  // صلاحيات المستخدمين
  USERS_READ: 'users_read',
  USERS_WRITE: 'users_write',
  USERS_DELETE: 'users_delete',

  // صلاحيات الإعدادات
  SETTINGS_READ: 'settings_read',
  SETTINGS_WRITE: 'settings_write',

  // صلاحية كاملة
  ALL: 'all'
}

