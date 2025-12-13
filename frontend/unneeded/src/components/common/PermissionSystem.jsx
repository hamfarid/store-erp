import React, { createContext, useContext, useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { useAuth } from '../../contexts/AuthContext'
import './PermissionSystem.css'

// Permission Context
const PermissionContext = createContext()

// Permission Provider
export const PermissionProvider = ({ children }) => {
  const { user } = useAuth()
  const [permissions, setPermissions] = useState([])
  const [roles, setRoles] = useState([])
  const [loading, setLoading] = useState(true)

  // Load user permissions and roles
  useEffect(() => {
    if (user) {
      loadUserPermissions()
    }
  }, [user])

  const loadUserPermissions = async () => {
    try {
      setLoading(true)
      // Load from API or use default permissions
      const userPermissions = user?.permissions || []
      const userRoles = user?.roles || []
      
      setPermissions(userPermissions)
      setRoles(userRoles)
    } catch (error) {
      } finally {
      setLoading(false)
    }
  }

  const hasPermission = (permission) => {
    if (!user) return false
    if (user.is_admin) return true
    return permissions.includes(permission)
  }

  const hasRole = (role) => {
    if (!user) return false
    if (user.is_admin) return true
    return roles.includes(role)
  }

  const hasAnyPermission = (permissionList) => {
    return permissionList.some(permission => hasPermission(permission))
  }

  const hasAllPermissions = (permissionList) => {
    return permissionList.every(permission => hasPermission(permission))
  }

  const value = {
    permissions,
    roles,
    loading,
    hasPermission,
    hasRole,
    hasAnyPermission,
    hasAllPermissions,
    isAdmin: user?.is_admin || false
  }

  return (
    <PermissionContext.Provider value={value}>
      {children}
    </PermissionContext.Provider>
  )
}

// Permission Hook
export const usePermissions = () => {
  const context = useContext(PermissionContext)
  if (!context) {
    throw new Error('usePermissions must be used within a PermissionProvider')
  }
  return context
}

// Permission Guard Component
export const PermissionGuard = ({ 
  permission, 
  role, 
  permissions, 
  roles,
  requireAll = false,
  fallback = null,
  children 
}) => {
  const { hasPermission, hasRole, hasAnyPermission, hasAllPermissions, isAdmin } = usePermissions()

  // Admin bypass
  if (isAdmin) {
    return children
  }

  // Check single permission
  if (permission && !hasPermission(permission)) {
    return fallback
  }

  // Check single role
  if (role && !hasRole(role)) {
    return fallback
  }

  // Check multiple permissions
  if (permissions) {
    const hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
    
    if (!hasAccess) {
      return fallback
    }
  }

  // Check multiple roles
  if (roles) {
    const hasAccess = requireAll
      ? roles.every(r => hasRole(r))
      : roles.some(r => hasRole(r))
    
    if (!hasAccess) {
      return fallback
    }
  }

  return children
}

// Permission Button Component
export const PermissionButton = ({ 
  permission, 
  role, 
  permissions, 
  roles,
  requireAll = false,
  children,
  ...props 
}) => {
  return (
    <PermissionGuard
      permission={permission}
      role={role}
      permissions={permissions}
      roles={roles}
      requireAll={requireAll}
      fallback={null}
    >
      <button {...props}>
        {children}
      </button>
    </PermissionGuard>
  )
}

// Role Management Component
export const RoleManager = () => {
  const [roles, setRoles] = useState([])
  const [selectedRole, setSelectedRole] = useState(null)
  const [permissions, setPermissions] = useState([])
  const [loading, setLoading] = useState(true)

  const defaultPermissions = [
    { id: 'products.view', name: 'عرض المنتجات', category: 'المنتجات' },
    { id: 'products.create', name: 'إنشاء منتجات', category: 'المنتجات' },
    { id: 'products.edit', name: 'تعديل المنتجات', category: 'المنتجات' },
    { id: 'products.delete', name: 'حذف المنتجات', category: 'المنتجات' },
    
    { id: 'inventory.view', name: 'عرض المخزون', category: 'المخزون' },
    { id: 'inventory.manage', name: 'إدارة المخزون', category: 'المخزون' },
    { id: 'inventory.transfer', name: 'نقل المخزون', category: 'المخزون' },
    
    { id: 'sales.view', name: 'عرض المبيعات', category: 'المبيعات' },
    { id: 'sales.create', name: 'إنشاء فواتير', category: 'المبيعات' },
    { id: 'sales.edit', name: 'تعديل الفواتير', category: 'المبيعات' },
    { id: 'sales.delete', name: 'حذف الفواتير', category: 'المبيعات' },
    
    { id: 'reports.view', name: 'عرض التقارير', category: 'التقارير' },
    { id: 'reports.export', name: 'تصدير التقارير', category: 'التقارير' },
    
    { id: 'users.view', name: 'عرض المستخدمين', category: 'المستخدمين' },
    { id: 'users.create', name: 'إنشاء مستخدمين', category: 'المستخدمين' },
    { id: 'users.edit', name: 'تعديل المستخدمين', category: 'المستخدمين' },
    { id: 'users.delete', name: 'حذف المستخدمين', category: 'المستخدمين' },
    
    { id: 'settings.view', name: 'عرض الإعدادات', category: 'الإعدادات' },
    { id: 'settings.edit', name: 'تعديل الإعدادات', category: 'الإعدادات' }
  ]

  const defaultRoles = [
    {
      id: 1,
      name: 'مدير النظام',
      description: 'صلاحيات كاملة لجميع أجزاء النظام',
      permissions: defaultPermissions.map(p => p.id),
      is_admin: true
    },
    {
      id: 2,
      name: 'مدير المخزون',
      description: 'إدارة المنتجات والمخزون والتقارير',
      permissions: [
        'products.view', 'products.create', 'products.edit',
        'inventory.view', 'inventory.manage', 'inventory.transfer',
        'reports.view', 'reports.export'
      ]
    },
    {
      id: 3,
      name: 'موظف المبيعات',
      description: 'إدارة المبيعات وعرض المنتجات',
      permissions: [
        'products.view',
        'sales.view', 'sales.create', 'sales.edit',
        'reports.view'
      ]
    },
    {
      id: 4,
      name: 'مستخدم عادي',
      description: 'عرض البيانات الأساسية فقط',
      permissions: [
        'products.view',
        'inventory.view',
        'sales.view',
        'reports.view'
      ]
    }
  ]

  useEffect(() => {
    // Load roles and permissions
    setRoles(defaultRoles)
    setPermissions(defaultPermissions)
    setLoading(false)
  }, [])

  const groupedPermissions = permissions.reduce((groups, permission) => {
    const category = permission.category
    if (!groups[category]) {
      groups[category] = []
    }
    groups[category].push(permission)
    return groups
  }, {})

  if (loading) {
    return <div className="role-manager-loading">جاري التحميل...</div>
  }

  return (
    <div className="role-manager">
      <div className="role-manager__header">
        <h2>إدارة الأدوار والصلاحيات</h2>
        <p>تحكم في صلاحيات المستخدمين وأدوارهم في النظام</p>
      </div>

      <div className="role-manager__content">
        <div className="roles-list">
          <h3>الأدوار المتاحة</h3>
          {roles.map(role => (
            <div 
              key={role.id} 
              className={`role-item ${selectedRole?.id === role.id ? 'role-item--selected' : ''}`}
              onClick={() => setSelectedRole(role)}
            >
              <div className="role-item__header">
                <h4>{role.name}</h4>
                {role.is_admin && <span className="admin-badge">مدير</span>}
              </div>
              <p className="role-item__description">{role.description}</p>
              <div className="role-item__stats">
                {role.permissions.length} صلاحية
              </div>
            </div>
          ))}
        </div>

        <div className="permissions-panel">
          {selectedRole ? (
            <>
              <h3>صلاحيات الدور: {selectedRole.name}</h3>
              <div className="permissions-grid">
                {Object.entries(groupedPermissions).map(([category, categoryPermissions]) => (
                  <div key={category} className="permission-category">
                    <h4 className="permission-category__title">{category}</h4>
                    <div className="permission-list">
                      {categoryPermissions.map(permission => (
                        <label key={permission.id} className="permission-item">
                          <input
                            type="checkbox"
                            checked={selectedRole.permissions.includes(permission.id)}
                            readOnly
                          />
                          <span className="permission-item__name">{permission.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="no-role-selected">
              <p>اختر دوراً لعرض صلاحياته</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// User Management Component
export const UserManager = () => {
  const [users, setUsers] = useState([])
  const [roles] = useState([])
  const [loading, setLoading] = useState(true)

  // Mock users data
  const mockUsers = [
    {
      id: 1,
      username: 'admin',
      email: 'admin@company.com',
      full_name: 'مدير النظام',
      role_id: 1,
      is_active: true,
      last_login: '2024-12-01 10:30:00'
    },
    {
      id: 2,
      username: 'inventory_manager',
      email: 'inventory@company.com',
      full_name: 'أحمد محمد',
      role_id: 2,
      is_active: true,
      last_login: '2024-12-01 09:15:00'
    },
    {
      id: 3,
      username: 'sales_user',
      email: 'sales@company.com',
      full_name: 'فاطمة علي',
      role_id: 3,
      is_active: true,
      last_login: '2024-12-01 08:45:00'
    }
  ]

  useEffect(() => {
    // Load users and roles
    setUsers(mockUsers)
    setLoading(false)
  }, [])

  if (loading) {
    return <div className="user-manager-loading">جاري التحميل...</div>
  }

  return (
    <div className="user-manager">
      <div className="user-manager__header">
        <h2>إدارة المستخدمين</h2>
        <button className="btn btn-primary">إضافة مستخدم جديد</button>
      </div>

      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>اسم المستخدم</th>
              <th>الاسم الكامل</th>
              <th>البريد الإلكتروني</th>
              <th>الدور</th>
              <th>الحالة</th>
              <th>آخر دخول</th>
              <th>الإجراءات</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.username}</td>
                <td>{user.full_name}</td>
                <td>{user.email}</td>
                <td>
                  <span className="role-badge">
                    {user.role_id === 1 ? 'مدير النظام' : 
                     user.role_id === 2 ? 'مدير المخزون' :
                     user.role_id === 3 ? 'موظف المبيعات' : 'مستخدم عادي'}
                  </span>
                </td>
                <td>
                  <span className={`status-badge ${user.is_active ? 'status-active' : 'status-inactive'}`}>
                    {user.is_active ? 'نشط' : 'غير نشط'}
                  </span>
                </td>
                <td>{new Date(user.last_login).toLocaleDateString('ar-EG')}</td>
                <td>
                  <div className="action-buttons">
                    <button className="btn btn-sm btn-secondary">تعديل</button>
                    <button className="btn btn-sm btn-danger">حذف</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default { PermissionProvider, usePermissions, PermissionGuard, RoleManager, UserManager }
