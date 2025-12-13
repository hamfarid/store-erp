import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Shield
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const AdvancedPermissions = () => {
  const [loading, setLoading] = useState(false)
  const [roles, setRoles] = useState([])
  const [permissions, setPermissions] = useState([])
  const [users, setUsers] = useState([])
  const [activeTab, setActiveTab] = useState('roles')
  const [selectedRole, setSelectedRole] = useState(null)
  const [isEditingRole, setIsEditingRole] = useState(false)
  const [newRole, setNewRole] = useState({
    name: '',
    description: '',
    permissions: []
  })

  // Permission categories and their permissions
  const permissionCategories = {
    'المنتجات': [
      { id: 'products.view', name: 'عرض المنتجات', description: 'عرض قائمة المنتجات والتفاصيل' },
      { id: 'products.create', name: 'إضافة منتجات', description: 'إضافة منتجات جديدة' },
      { id: 'products.edit', name: 'تعديل المنتجات', description: 'تعديل بيانات المنتجات' },
      { id: 'products.delete', name: 'حذف المنتجات', description: 'حذف المنتجات من النظام' },
      { id: 'products.import', name: 'استيراد المنتجات', description: 'استيراد المنتجات من ملفات خارجية' }
    ],
    'المخزون': [
      { id: 'inventory.view', name: 'عرض المخزون', description: 'عرض مستويات المخزون' },
      { id: 'inventory.adjust', name: 'تعديل المخزون', description: 'تعديل كميات المخزون' },
      { id: 'inventory.transfer', name: 'نقل المخزون', description: 'نقل البضائع بين المخازن' },
      { id: 'inventory.reports', name: 'تقارير المخزون', description: 'عرض وتصدير تقارير المخزون' }
    ],
    'الفواتير': [
      { id: 'invoices.view', name: 'عرض الفواتير', description: 'عرض قائمة الفواتير' },
      { id: 'invoices.create', name: 'إنشاء فواتير', description: 'إنشاء فواتير جديدة' },
      { id: 'invoices.edit', name: 'تعديل الفواتير', description: 'تعديل الفواتير الموجودة' },
      { id: 'invoices.delete', name: 'حذف الفواتير', description: 'حذف الفواتير' },
      { id: 'invoices.approve', name: 'اعتماد الفواتير', description: 'اعتماد الفواتير للدفع' }
    ],
    'العملاء والموردين': [
      { id: 'customers.view', name: 'عرض العملاء', description: 'عرض قائمة العملاء' },
      { id: 'customers.manage', name: 'إدارة العملاء', description: 'إضافة وتعديل وحذف العملاء' },
      { id: 'suppliers.view', name: 'عرض الموردين', description: 'عرض قائمة الموردين' },
      { id: 'suppliers.manage', name: 'إدارة الموردين', description: 'إضافة وتعديل وحذف الموردين' }
    ],
    'التقارير': [
      { id: 'reports.financial', name: 'التقارير المالية', description: 'عرض التقارير المالية' },
      { id: 'reports.inventory', name: 'تقارير المخزون', description: 'عرض تقارير المخزون' },
      { id: 'reports.sales', name: 'تقارير المبيعات', description: 'عرض تقارير المبيعات' },
      { id: 'reports.export', name: 'تصدير التقارير', description: 'تصدير التقارير بصيغ مختلفة' }
    ],
    'الإدارة': [
      { id: 'admin.users', name: 'إدارة المستخدمين', description: 'إضافة وتعديل وحذف المستخدمين' },
      { id: 'admin.roles', name: 'إدارة الأدوار', description: 'إنشاء وتعديل أدوار المستخدمين' },
      { id: 'admin.settings', name: 'إعدادات النظام', description: 'تعديل إعدادات النظام العامة' },
      { id: 'admin.backup', name: 'النسخ الاحتياطي', description: 'إنشاء واستعادة النسخ الاحتياطية' },
      { id: 'admin.logs', name: 'سجلات النظام', description: 'عرض سجلات النظام والأنشطة' }
    ]
  }

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [rolesResponse, usersResponse] = await Promise.all([
        ApiService.get('/api/admin/roles'),
        ApiService.get('/api/admin/users')
      ])

      if (rolesResponse.success) {
        setRoles(rolesResponse.data)
      } else {
        // Mock data
        setRoles([
          {
            id: 1,
            name: 'مدير النظام',
            description: 'صلاحيات كاملة لجميع وظائف النظام',
            permissions: Object.values(permissionCategories).flat().map(p => p.id),
            userCount: 2,
            isSystem: true
          },
          {
            id: 2,
            name: 'مدير المخزون',
            description: 'إدارة المخزون والمنتجات',
            permissions: ['products.view', 'products.create', 'products.edit', 'inventory.view', 'inventory.adjust', 'inventory.transfer'],
            userCount: 5,
            isSystem: false
          },
          {
            id: 3,
            name: 'محاسب',
            description: 'إدارة الفواتير والتقارير المالية',
            permissions: ['invoices.view', 'invoices.create', 'invoices.edit', 'reports.financial', 'reports.sales'],
            userCount: 3,
            isSystem: false
          }
        ])
      }

      if (usersResponse.success) {
        setUsers(usersResponse.data)
      } else {
        // Mock data
        setUsers([
          { id: 1, name: 'أحمد محمد', email: 'ahmed@example.com', role: 'مدير النظام', status: 'active' },
          { id: 2, name: 'فاطمة علي', email: 'fatima@example.com', role: 'مدير المخزون', status: 'active' },
          { id: 3, name: 'محمد حسن', email: 'mohamed@example.com', role: 'محاسب', status: 'inactive' }
        ])
      }

      // Extract all permissions
      const allPermissions = Object.values(permissionCategories).flat()
      setPermissions(allPermissions)

    } catch (error) {
      toast.error('خطأ في تحميل البيانات')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRole = async () => {
    try {
      if (!newRole.name.trim()) {
        toast.error('اسم الدور مطلوب')
        return
      }

      const response = await ApiService.post('/api/admin/roles', newRole)
      if (response.success) {
        setRoles(prev => [...prev, { ...newRole, id: Date.now(), userCount: 0, isSystem: false }])
        setNewRole({ name: '', description: '', permissions: [] })
        setIsEditingRole(false)
        toast.success('تم إنشاء الدور بنجاح')
      }
    } catch (error) {
      toast.error('خطأ في إنشاء الدور')
    }
  }

  const handleUpdateRole = async (roleId, updatedRole) => {
    try {
      const response = await ApiService.put(`/api/admin/roles/${roleId}`, updatedRole)
      if (response.success) {
        setRoles(prev => prev.map(role => 
          role.id === roleId ? { ...role, ...updatedRole } : role
        ))
        setSelectedRole(null)
        toast.success('تم تحديث الدور بنجاح')
      }
    } catch (error) {
      toast.error('خطأ في تحديث الدور')
    }
  }

  const handleDeleteRole = async (roleId) => {
    try {
      const role = roles.find(r => r.id === roleId)
      if (role?.isSystem) {
        toast.error('لا يمكن حذف أدوار النظام')
        return
      }

      if (role?.userCount > 0) {
        toast.error('لا يمكن حذف دور مرتبط بمستخدمين')
        return
      }

      if (window.confirm('هل أنت متأكد من حذف هذا الدور؟')) {
        const response = await ApiService.delete(`/api/admin/roles/${roleId}`)
        if (response.success) {
          setRoles(prev => prev.filter(role => role.id !== roleId))
          toast.success('تم حذف الدور بنجاح')
        }
      }
    } catch (error) {
      toast.error('خطأ في حذف الدور')
    }
  }

  const handleDuplicateRole = (role) => {
    setNewRole({
      name: `${role.name} - نسخة`,
      description: role.description,
      permissions: [...role.permissions]
    })
    setIsEditingRole(true)
  }

  const togglePermission = (permissionId) => {
    setNewRole(prev => ({
      ...prev,
      permissions: prev.permissions.includes(permissionId)
        ? prev.permissions.filter(p => p !== permissionId)
        : [...prev.permissions, permissionId]
    }))
  }

  const selectAllPermissions = (category) => {
    const categoryPermissions = permissionCategories[category].map(p => p.id)
    const hasAll = categoryPermissions.every(p => newRole.permissions.includes(p))
    
    if (hasAll) {
      // Remove all category permissions
      setNewRole(prev => ({
        ...prev,
        permissions: prev.permissions.filter(p => !categoryPermissions.includes(p))
      }))
    } else {
      // Add all category permissions
      setNewRole(prev => ({
        ...prev,
        permissions: [...new Set([...prev.permissions, ...categoryPermissions])]
      }))
    }
  }

  // eslint-disable-next-line no-unused-vars
  const getPermissionName = (permissionId) => {
    const permission = permissions.find(p => p.id === permissionId)
    return permission ? permission.name : permissionId
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Shield className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">إدارة الصلاحيات المتقدمة</h1>
              <p className="text-muted-foreground">إدارة أدوار المستخدمين والصلاحيات بشكل تفصيلي</p>
            </div>
          </div>
          
          <button
            onClick={() => setIsEditingRole(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
          >
            <Plus className="w-4 h-4 ml-2" />
            إضافة دور جديد
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'roles', name: 'الأدوار', icon: Shield },
              { id: 'permissions', name: 'الصلاحيات', icon: Lock },
              { id: 'users', name: 'المستخدمون', icon: Users }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
              >
                <tab.icon className="w-4 h-4 ml-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'roles' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">أدوار المستخدمين</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {roles.map((role) => (
                  <div key={role.id} className="bg-muted/50 rounded-lg p-6 border border-border">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-medium text-foreground">{role.name}</h4>
                      <div className="flex items-center space-x-2 space-x-reverse">
                        <button
                          onClick={() => handleDuplicateRole(role)}
                          className="text-muted-foreground hover:text-foreground"
                          title="نسخ"
                        >
                          <Copy className="w-4 h-4" />
                        </button>
                        {!role.isSystem && (
                          <>
                            <button
                              onClick={() => setSelectedRole(role)}
                              className="text-primary-600 hover:text-primary-900"
                              title="تعديل"
                            >
                              <Edit className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteRole(role.id)}
                              className="text-destructive hover:text-red-900"
                              title="حذف"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-4">{role.description}</p>
                    
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">
                        {role.permissions.length} صلاحية
                      </span>
                      <span className="text-gray-500">
                        {role.userCount} مستخدم
                      </span>
                    </div>
                    
                    {role.isSystem && (
                      <div className="mt-2">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                          دور النظام
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'permissions' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">جميع الصلاحيات</h3>
              
              <div className="space-y-6">
                {Object.entries(permissionCategories).map(([category, categoryPermissions]) => (
                  <div key={category} className="bg-muted/50 rounded-lg p-6">
                    <h4 className="text-lg font-medium text-foreground mb-4">{category}</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {categoryPermissions.map((permission) => (
                        <div key={permission.id} className="bg-white rounded-lg p-4 border border-border">
                          <div className="flex items-center justify-between mb-2">
                            <h5 className="font-medium text-foreground">{permission.name}</h5>
                            <Lock className="w-4 h-4 text-gray-400" />
                          </div>
                          <p className="text-sm text-muted-foreground">{permission.description}</p>
                          <p className="text-xs text-gray-400 mt-2">ID: {permission.id}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'users' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">المستخدمون وأدوارهم</h3>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        المستخدم
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        البريد الإلكتروني
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        الدور
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        الحالة
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        الإجراءات
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10">
                              <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                                <span className="text-sm font-medium text-primary-600">
                                  {user.name.charAt(0)}
                                </span>
                              </div>
                            </div>
                            <div className="mr-4">
                              <div className="text-sm font-medium text-foreground">{user.name}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {user.email}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                            {user.role}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            user.status === 'active' 
                              ? 'bg-primary/20 text-green-800' 
                              : 'bg-destructive/20 text-red-800'
                          }`}>
                            {user.status === 'active' ? 'نشط' : 'غير نشط'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex items-center space-x-2 space-x-reverse">
                            <button className="text-primary-600 hover:text-primary-900">
                              <Edit className="w-4 h-4" />
                            </button>
                            <button className="text-muted-foreground hover:text-foreground">
                              {user.status === 'active' ? <UserX className="w-4 h-4" /> : <UserCheck className="w-4 h-4" />}
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Create/Edit Role Modal */}
      {isEditingRole && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-foreground">
                  {selectedRole ? 'تعديل الدور' : 'إضافة دور جديد'}
                </h3>
                <button
                  onClick={() => {
                    setIsEditingRole(false)
                    setSelectedRole(null)
                    setNewRole({ name: '', description: '', permissions: [] })
                  }}
                  className="text-gray-400 hover:text-muted-foreground"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    اسم الدور
                  </label>
                  <input
                    type="text"
                    value={newRole.name}
                    onChange={(e) => setNewRole(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="أدخل اسم الدور"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    الوصف
                  </label>
                  <textarea
                    value={newRole.description}
                    onChange={(e) => setNewRole(prev => ({ ...prev, description: e.target.value }))}
                    rows={3}
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="أدخل وصف الدور"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-4">
                    الصلاحيات
                  </label>
                  
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {Object.entries(permissionCategories).map(([category, categoryPermissions]) => (
                      <div key={category} className="border border-border rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-medium text-foreground">{category}</h4>
                          <button
                            onClick={() => selectAllPermissions(category)}
                            className="text-sm text-primary-600 hover:text-primary-800"
                          >
                            {categoryPermissions.every(p => newRole.permissions.includes(p.id)) 
                              ? 'إلغاء تحديد الكل' 
                              : 'تحديد الكل'
                            }
                          </button>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {categoryPermissions.map((permission) => (
                            <label key={permission.id} className="flex items-center">
                              <input
                                type="checkbox"
                                checked={newRole.permissions.includes(permission.id)}
                                onChange={() => togglePermission(permission.id)}
                                className="rounded border-border text-primary-600 focus:ring-primary-500"
                              />
                              <span className="mr-2 text-sm text-foreground">{permission.name}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-3 space-x-reverse mt-6">
                <button
                  onClick={() => {
                    setIsEditingRole(false)
                    setSelectedRole(null)
                    setNewRole({ name: '', description: '', permissions: [] })
                  }}
                  className="px-4 py-2 border border-border rounded-md text-sm font-medium text-foreground hover:bg-muted/50"
                >
                  إلغاء
                </button>
                <button
                  onClick={selectedRole ? () => handleUpdateRole(selectedRole.id, newRole) : handleCreateRole}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                >
                  <Save className="w-4 h-4 ml-2 inline" />
                  {selectedRole ? 'تحديث' : 'إنشاء'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdvancedPermissions

