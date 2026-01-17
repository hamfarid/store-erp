import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const AdminRoles = () => {
  const [roles, setRoles] = useState([])
  const [filteredRoles, setFilteredRoles] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingRole, setEditingRole] = useState(null)
  const [notification, setNotification] = useState(null)

  const permissions = [
    { id: 'dashboard', name: 'لوحة المعلومات', category: 'عام' },
    { id: 'products', name: 'إدارة المنتجات', category: 'المخزون' },
    { id: 'categories', name: 'إدارة الفئات', category: 'المخزون' },
    { id: 'warehouses', name: 'إدارة المخازن', category: 'المخزون' },
    { id: 'stock_movements', name: 'حركات المخزون', category: 'المخزون' },
    { id: 'lots', name: 'إدارة اللوطات', category: 'المخزون' },
    { id: 'customers', name: 'إدارة العملاء', category: 'المبيعات' },
    { id: 'suppliers', name: 'إدارة الموردين', category: 'المشتريات' },
    { id: 'sales', name: 'فواتير المبيعات', category: 'المبيعات' },
    { id: 'purchases', name: 'فواتير المشتريات', category: 'المشتريات' },
    { id: 'accounting', name: 'النظام المحاسبي', category: 'المحاسبة' },
    { id: 'reports', name: 'التقارير', category: 'التقارير' },
    { id: 'users', name: 'إدارة المستخدمين', category: 'الإدارة' },
    { id: 'roles', name: 'إدارة الأدوار', category: 'الإدارة' },
    { id: 'settings', name: 'إعدادات النظام', category: 'الإدارة' }
  ]

  useEffect(() => {
    loadRoles()
  }, [])

  useEffect(() => {
    filterRoles()
  }, [roles, searchTerm])

  const loadRoles = async () => {
    setLoading(true)
    try {
      // بيانات تجريبية للأدوار
      const mockRoles = [
        {
          id: 1,
          name: 'مدير النظام',
          nameEn: 'System Administrator',
          description: 'صلاحيات كاملة لجميع أجزاء النظام',
          permissions: permissions.map(p => p.id),
          usersCount: 1,
          isActive: true,
          isSystem: true,
          createdAt: '2024-01-01'
        },
        {
          id: 2,
          name: 'مدير المبيعات',
          nameEn: 'Sales Manager',
          description: 'إدارة المبيعات والعملاء والتقارير',
          permissions: ['dashboard', 'customers', 'sales', 'reports'],
          usersCount: 1,
          isActive: true,
          isSystem: false,
          createdAt: '2024-02-15'
        },
        {
          id: 3,
          name: 'مدير المخزن',
          nameEn: 'Warehouse Manager',
          description: 'إدارة المخزون والمخازن وحركات المخزون',
          permissions: ['dashboard', 'products', 'categories', 'warehouses', 'stock_movements', 'lots'],
          usersCount: 1,
          isActive: true,
          isSystem: false,
          createdAt: '2024-03-01'
        },
        {
          id: 4,
          name: 'محاسب',
          nameEn: 'Accountant',
          description: 'إدارة النظام المحاسبي والتقارير المالية',
          permissions: ['dashboard', 'accounting', 'sales', 'purchases', 'reports'],
          usersCount: 1,
          isActive: true,
          isSystem: false,
          createdAt: '2024-04-10'
        },
        {
          id: 5,
          name: 'مهندس مبيعات',
          nameEn: 'Sales Engineer',
          description: 'التعامل مع العملاء وإدخال طلبات المبيعات',
          permissions: ['dashboard', 'customers', 'sales'],
          usersCount: 1,
          isActive: true,
          isSystem: false,
          createdAt: '2024-05-20'
        }
      ]
      setRoles(mockRoles)
    } catch (error) {
      showNotification('فشل في تحميل الأدوار', 'error')
    } finally {
      setLoading(false)
    }
  }

  const filterRoles = () => {
    if (searchTerm) {
      const filtered = roles.filter(role =>
        role.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        role.nameEn.toLowerCase().includes(searchTerm.toLowerCase()) ||
        role.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredRoles(filtered)
    } else {
      setFilteredRoles(roles)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddRole = () => {
    setEditingRole(null)
    setShowModal(true)
  }

  const handleEditRole = (role) => {
    setEditingRole(role)
    setShowModal(true)
  }

  const handleDeleteRole = async (roleId) => {
    const role = roles.find(r => r.id === roleId)
    if (role?.isSystem) {
      showNotification('لا يمكن حذف الأدوار الأساسية للنظام', 'error')
      return
    }
    
    if (window.confirm('هل أنت متأكد من حذف هذا الدور؟')) {
      try {
        setRoles(prev => prev.filter(r => r.id !== roleId))
        showNotification('تم حذف الدور بنجاح')
      } catch (error) {
        showNotification('فشل في حذف الدور', 'error')
      }
    }
  }

  const handleToggleStatus = async (roleId) => {
    const role = roles.find(r => r.id === roleId)
    if (role?.isSystem) {
      showNotification('لا يمكن تعطيل الأدوار الأساسية للنظام', 'error')
      return
    }
    
    try {
      setRoles(prev => prev.map(r => 
        r.id === roleId ? { ...r, isActive: !r.isActive } : r
      ))
      showNotification('تم تحديث حالة الدور بنجاح')
    } catch (error) {
      showNotification('فشل في تحديث حالة الدور', 'error')
    }
  }

  const getPermissionsByCategory = () => {
    const categories = {}
    permissions.forEach(permission => {
      if (!categories[permission.category]) {
        categories[permission.category] = []
      }
      categories[permission.category].push(permission)
    })
    return categories
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">الأدوار والصلاحيات</h1>
          <p className="text-muted-foreground">إدارة أدوار المستخدمين وصلاحياتهم</p>
        </div>
        <button
          onClick={handleAddRole}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة دور جديد
        </button>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في الأدوار..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadRoles}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الأدوار</p>
              <p className="text-2xl font-bold text-foreground">{roles.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Unlock className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الأدوار النشطة</p>
              <p className="text-2xl font-bold text-foreground">
                {roles.filter(r => r.isActive).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Lock className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الأدوار المعطلة</p>
              <p className="text-2xl font-bold text-foreground">
                {roles.filter(r => !r.isActive).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-foreground">
                {roles.reduce((sum, r) => sum + (r.usersCount || 0), 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Roles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRoles.map((role) => (
          <div key={role.id} className="bg-white rounded-lg shadow border hover:shadow-md transition-shadow">
            <div className="p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Shield className="h-8 w-8 text-primary-600 ml-3" />
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">{role.name}</h3>
                    <p className="text-sm text-gray-500">{role.nameEn}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {role.isSystem && (
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-accent/20 text-yellow-800">
                      نظام
                    </span>
                  )}
                  <button
                    onClick={() => handleToggleStatus(role.id)}
                    className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      role.isActive 
                        ? 'bg-primary/20 text-green-800 hover:bg-green-200' 
                        : 'bg-destructive/20 text-red-800 hover:bg-red-200'
                    } transition-colors`}
                    disabled={role.isSystem}
                  >
                    {role.isActive ? 'نشط' : 'معطل'}
                  </button>
                </div>
              </div>

              {/* Description */}
              <p className="text-sm text-muted-foreground mb-4">{role.description}</p>

              {/* Permissions Count */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Settings className="h-4 w-4 text-gray-400 ml-2" />
                  <span className="text-sm text-muted-foreground">
                    {role.permissions.length} صلاحية
                  </span>
                </div>
                <div className="flex items-center">
                  <Users className="h-4 w-4 text-gray-400 ml-2" />
                  <span className="text-sm text-muted-foreground">
                    {role.usersCount} مستخدم
                  </span>
                </div>
              </div>

              {/* Permissions Preview */}
              <div className="mb-4">
                <p className="text-xs font-medium text-foreground mb-2">الصلاحيات:</p>
                <div className="flex flex-wrap gap-1">
                  {role.permissions.slice(0, 3).map(permissionId => {
                    const permission = permissions.find(p => p.id === permissionId)
                    return permission ? (
                      <span key={permissionId} className="inline-flex px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded">
                        {permission.name}
                      </span>
                    ) : null
                  })}
                  {role.permissions.length > 3 && (
                    <span className="inline-flex px-2 py-1 text-xs bg-muted text-muted-foreground rounded">
                      +{role.permissions.length - 3} أخرى
                    </span>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => handleEditRole(role)}
                  className="text-primary-600 hover:text-primary-900 p-1"
                  title="تعديل"
                >
                  <Edit className="h-4 w-4" />
                </button>
                {!role.isSystem && (
                  <button
                    onClick={() => handleDeleteRole(role.id)}
                    className="text-destructive hover:text-red-900 p-1"
                    title="حذف"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-medium mb-4">
              {editingRole ? 'تعديل الدور' : 'إضافة دور جديد'}
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Basic Info */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground">المعلومات الأساسية</h4>
                <input
                  type="text"
                  placeholder="اسم الدور"
                  className="w-full p-2 border border-border rounded-lg"
                  defaultValue={editingRole?.name || ''}
                />
                <input
                  type="text"
                  placeholder="الاسم بالإنجليزية"
                  className="w-full p-2 border border-border rounded-lg"
                  defaultValue={editingRole?.nameEn || ''}
                />
                <textarea
                  placeholder="وصف الدور"
                  className="w-full p-2 border border-border rounded-lg"
                  rows="3"
                  defaultValue={editingRole?.description || ''}
                />
              </div>

              {/* Permissions */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground">الصلاحيات</h4>
                <div className="max-h-96 overflow-y-auto border border-border rounded-lg p-4">
                  {Object.entries(getPermissionsByCategory()).map(([category, categoryPermissions]) => (
                    <div key={category} className="mb-4">
                      <h5 className="font-medium text-foreground mb-2">{category}</h5>
                      <div className="space-y-2">
                        {categoryPermissions.map(permission => (
                          <label key={permission.id} className="flex items-center">
                            <input
                              type="checkbox"
                              className="rounded border-border text-primary-600 focus:ring-primary-500"
                              defaultChecked={editingRole?.permissions.includes(permission.id)}
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

            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                onClick={() => {
                  showNotification(editingRole ? 'تم تحديث الدور بنجاح' : 'تم إضافة الدور بنجاح')
                  setShowModal(false)
                }}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                حفظ
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminRoles

