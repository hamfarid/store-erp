import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, User, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, UserPlus, Shield, Key, EyeOff,
  XCircle, Activity
} from 'lucide-react'
import DataTable from './ui/DataTable'
import DynamicForm from './ui/DynamicForm'
import { Notification, LoadingSpinner, Modal } from './ui/Notification'
import SearchFilter from './ui/SearchFilter'
// import apiClient from '../services/apiClient' // Currently unused

const UserManagementAdvanced = () => {
  const [activeTab, setActiveTab] = useState('users')
  const [users, setUsers] = useState([])
  const [roles, setRoles] = useState([])
  const [permissions, setPermissions] = useState([])
  const [userActivities, setUserActivities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('')
  const [selectedItem, setSelectedItem] = useState(null)
  const [filteredData, setFilteredData] = useState([])

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadData()
  }, [activeTab])

  const loadData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        loadUsers(),
        loadRoles(),
        loadPermissions(),
        loadUserActivities()
      ])
    } catch (error) {
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadUsers = async () => {
    try {
      const response = await fetch('/api/user/users', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setUsers(data.users)
          setFilteredData(data.users)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية
      const mockUsers = [
        {
          id: 1,
          username: 'admin',
          email: 'admin@system.com',
          full_name: 'مدير النظام',
          phone: '01234567890',
          role: 'مدير النظام',
          role_id: 1,
          is_active: true,
          last_login: '2024-07-03T10:30:00',
          login_count: 156,
          created_at: '2024-01-01T00:00:00',
          department: 'الإدارة',
          position: 'مدير عام',
          permissions: ['all'],
          status: 'online'
        },
        {
          id: 2,
          username: 'sales_manager',
          email: 'sales@company.com',
          full_name: 'أحمد محمد السيد',
          phone: '01234567891',
          role: 'مدير المبيعات',
          role_id: 2,
          is_active: true,
          last_login: '2024-07-03T09:15:00',
          login_count: 89,
          created_at: '2024-02-15T00:00:00',
          department: 'المبيعات',
          position: 'مدير المبيعات',
          permissions: ['sales_read', 'sales_write', 'customers_read'],
          status: 'online'
        },
        {
          id: 3,
          username: 'warehouse_keeper',
          email: 'warehouse@company.com',
          full_name: 'فاطمة أحمد محمود',
          phone: '01234567892',
          role: 'أمين المخزن',
          role_id: 3,
          is_active: true,
          last_login: '2024-07-02T16:45:00',
          login_count: 234,
          created_at: '2024-01-20T00:00:00',
          department: 'المخازن',
          position: 'أمين مخزن رئيسي',
          permissions: ['inventory_read', 'inventory_write', 'lots_read'],
          status: 'offline'
        },
        {
          id: 4,
          username: 'accountant',
          email: 'accounting@company.com',
          full_name: 'محمد علي حسن',
          phone: '01234567893',
          role: 'محاسب',
          role_id: 4,
          is_active: false,
          last_login: '2024-06-28T14:20:00',
          login_count: 67,
          created_at: '2024-03-10T00:00:00',
          department: 'المحاسبة',
          position: 'محاسب عام',
          permissions: ['accounting_read', 'reports_read'],
          status: 'inactive'
        }
      ]
      setUsers(mockUsers)
      setFilteredData(mockUsers)
    }
  }

  const loadRoles = async () => {
    const mockRoles = [
      {
        id: 1,
        name: 'مدير النظام',
        description: 'صلاحيات كاملة لجميع أجزاء النظام',
        permissions: ['all'],
        users_count: 1,
        is_active: true,
        created_at: '2024-01-01T00:00:00'
      },
      {
        id: 2,
        name: 'مدير المبيعات',
        description: 'إدارة المبيعات والعملاء والفواتير',
        permissions: ['sales_read', 'sales_write', 'customers_read', 'customers_write', 'invoices_read', 'invoices_write'],
        users_count: 3,
        is_active: true,
        created_at: '2024-01-01T00:00:00'
      },
      {
        id: 3,
        name: 'أمين المخزن',
        description: 'إدارة المخزون واللوطات والحركات',
        permissions: ['inventory_read', 'inventory_write', 'lots_read', 'lots_write', 'movements_read', 'movements_write'],
        users_count: 2,
        is_active: true,
        created_at: '2024-01-01T00:00:00'
      },
      {
        id: 4,
        name: 'محاسب',
        description: 'عرض التقارير المالية والمحاسبية',
        permissions: ['accounting_read', 'reports_read', 'financial_read'],
        users_count: 1,
        is_active: true,
        created_at: '2024-01-01T00:00:00'
      }
    ]
    setRoles(mockRoles)
  }

  const loadPermissions = async () => {
    const mockPermissions = [
      { id: 'all', name: 'جميع الصلاحيات', category: 'system' },
      { id: 'sales_read', name: 'عرض المبيعات', category: 'sales' },
      { id: 'sales_write', name: 'تعديل المبيعات', category: 'sales' },
      { id: 'customers_read', name: 'عرض العملاء', category: 'customers' },
      { id: 'customers_write', name: 'تعديل العملاء', category: 'customers' },
      { id: 'inventory_read', name: 'عرض المخزون', category: 'inventory' },
      { id: 'inventory_write', name: 'تعديل المخزون', category: 'inventory' },
      { id: 'lots_read', name: 'عرض اللوطات', category: 'inventory' },
      { id: 'lots_write', name: 'تعديل اللوطات', category: 'inventory' },
      { id: 'accounting_read', name: 'عرض المحاسبة', category: 'accounting' },
      { id: 'accounting_write', name: 'تعديل المحاسبة', category: 'accounting' },
      { id: 'reports_read', name: 'عرض التقارير', category: 'reports' },
      { id: 'users_read', name: 'عرض المستخدمين', category: 'admin' },
      { id: 'users_write', name: 'تعديل المستخدمين', category: 'admin' }
    ]
    setPermissions(mockPermissions)
  }

  const loadUserActivities = async () => {
    const mockActivities = [
      {
        id: 1,
        user_name: 'admin',
        action: 'تسجيل دخول',
        description: 'تسجيل دخول ناجح للنظام',
        ip_address: '192.168.1.100',
        user_agent: 'Chrome 126.0.0.0',
        timestamp: '2024-07-03T10:30:00',
        status: 'success'
      },
      {
        id: 2,
        user_name: 'sales_manager',
        action: 'إنشاء فاتورة',
        description: 'إنشاء فاتورة مبيعات رقم INV-2024-001',
        ip_address: '192.168.1.101',
        user_agent: 'Chrome 126.0.0.0',
        timestamp: '2024-07-03T09:45:00',
        status: 'success'
      },
      {
        id: 3,
        user_name: 'warehouse_keeper',
        action: 'تحديث مخزون',
        description: 'تحديث كمية المنتج: بذور طماطم',
        ip_address: '192.168.1.102',
        user_agent: 'Firefox 127.0',
        timestamp: '2024-07-03T08:20:00',
        status: 'success'
      },
      {
        id: 4,
        user_name: 'accountant',
        action: 'محاولة دخول فاشلة',
        description: 'محاولة دخول بكلمة مرور خاطئة',
        ip_address: '192.168.1.103',
        user_agent: 'Chrome 126.0.0.0',
        timestamp: '2024-07-02T14:15:00',
        status: 'failed'
      }
    ]
    setUserActivities(mockActivities)
  }

  const loadMockData = () => {
    loadUsers()
    loadRoles()
    loadPermissions()
    loadUserActivities()
  }

  // تعريف أعمدة جدول المستخدمين
  const userColumns = [
    {
      key: 'full_name',
      header: 'اسم المستخدم',
      sortable: true,
      filterable: true,
      render: (value, item) => (
        <div className="flex items-center">
          <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center ml-3">
            <User className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="font-medium text-foreground">{value}</div>
            <div className="text-sm text-gray-500">@{item.username}</div>
          </div>
        </div>
      )
    },
    {
      key: 'email',
      header: 'البريد الإلكتروني',
      sortable: true,
      filterable: true,
      render: (value) => (
        <div className="flex items-center">
          <Mail className="w-4 h-4 text-gray-400 ml-1" />
          <span className="text-sm">{value}</span>
        </div>
      )
    },
    {
      key: 'role',
      header: 'الدور',
      sortable: true,
      filterable: true,
      render: (value) => (
        <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
          {value}
        </span>
      )
    },
    {
      key: 'department',
      header: 'القسم',
      sortable: true,
      filterable: true
    },
    {
      key: 'last_login',
      header: 'آخر دخول',
      sortable: true,
      render: (value) => (
        <div className="text-sm text-muted-foreground">
          {new Date(value).toLocaleString('ar-EG')}
        </div>
      )
    },
    {
      key: 'status',
      header: 'الحالة',
      sortable: true,
      render: (value, item) => {
        const statusConfig = {
          online: { label: 'متصل', color: 'bg-primary/20 text-green-800', icon: CheckCircle },
          offline: { label: 'غير متصل', color: 'bg-muted text-foreground', icon: XCircle },
          inactive: { label: 'غير نشط', color: 'bg-destructive/20 text-red-800', icon: XCircle }
        }
        
        let status = item.is_active ? (value || 'offline') : 'inactive'
        const config = statusConfig[status] || statusConfig.offline
        const Icon = config.icon
        
        return (
          <div className="flex items-center">
            <Icon className="w-4 h-4 ml-1" />
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          </div>
        )
      }
    },
    {
      key: 'login_count',
      header: 'عدد مرات الدخول',
      sortable: true,
      render: (value) => (
        <span className="font-medium text-primary-600">{value}</span>
      )
    }
  ]

  // تعريف أعمدة جدول الأدوار
  const roleColumns = [
    {
      key: 'name',
      header: 'اسم الدور',
      sortable: true,
      filterable: true,
      render: (value) => (
        <div className="flex items-center">
          <Shield className="w-4 h-4 text-purple-500 ml-2" />
          <span className="font-medium">{value}</span>
        </div>
      )
    },
    {
      key: 'description',
      header: 'الوصف',
      render: (value) => (
        <span className="text-sm text-muted-foreground">{value}</span>
      )
    },
    {
      key: 'users_count',
      header: 'عدد المستخدمين',
      sortable: true,
      render: (value) => (
        <span className="font-medium text-primary-600">{value}</span>
      )
    },
    {
      key: 'permissions',
      header: 'الصلاحيات',
      render: (value) => (
        <div className="flex flex-wrap gap-1">
          {value.slice(0, 3).map((permission, index) => (
            <span key={index} className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs">
              {permission}
            </span>
          ))}
          {value.length > 3 && (
            <span className="px-2 py-1 bg-muted text-muted-foreground rounded-full text-xs">
              +{value.length - 3}
            </span>
          )}
        </div>
      )
    },
    {
      key: 'is_active',
      header: 'الحالة',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
        }`}>
          {value ? 'نشط' : 'غير نشط'}
        </span>
      )
    }
  ]

  // تعريف أعمدة جدول الأنشطة
  const activityColumns = [
    {
      key: 'user_name',
      header: 'المستخدم',
      sortable: true,
      filterable: true,
      render: (value) => (
        <div className="flex items-center">
          <User className="w-4 h-4 text-gray-400 ml-1" />
          <span className="font-medium">{value}</span>
        </div>
      )
    },
    {
      key: 'action',
      header: 'النشاط',
      sortable: true,
      filterable: true,
      render: (value) => (
        <span className="font-medium text-foreground">{value}</span>
      )
    },
    {
      key: 'description',
      header: 'التفاصيل',
      render: (value) => (
        <span className="text-sm text-muted-foreground">{value}</span>
      )
    },
    {
      key: 'timestamp',
      header: 'التوقيت',
      sortable: true,
      render: (value) => (
        <div className="text-sm text-muted-foreground">
          {new Date(value).toLocaleString('ar-EG')}
        </div>
      )
    },
    {
      key: 'status',
      header: 'النتيجة',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value === 'success' ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
        }`}>
          {value === 'success' ? 'نجح' : 'فشل'}
        </span>
      )
    }
  ]

  // إجراءات المستخدمين
  const userActions = [
    {
      icon: Eye,
      label: 'عرض التفاصيل',
      onClick: (item) => {
        setSelectedItem(item)
        setModalType('view-user')
        setShowModal(true)
      },
      className: 'text-primary-600 hover:text-primary-800 hover:bg-primary-50'
    },
    {
      icon: Edit,
      label: 'تعديل',
      onClick: (item) => {
        setSelectedItem(item)
        setModalType('edit-user')
        setShowModal(true)
      },
      className: 'text-primary hover:text-green-800 hover:bg-primary/10'
    },
    {
      icon: Key,
      label: 'تغيير كلمة المرور',
      onClick: (item) => {
        setSelectedItem(item)
        setModalType('change-password')
        setShowModal(true)
      },
      className: 'text-accent hover:text-orange-800 hover:bg-accent/10'
    },
    {
      icon: Lock,
      label: 'تعطيل/تفعيل',
      onClick: (item) => {
        handleToggleUserStatus(item.id, !item.is_active)
      },
      className: 'text-accent hover:text-yellow-800 hover:bg-accent/10'
    }
  ]

  // إجراءات الأدوار
  const roleActions = [
    {
      icon: Eye,
      label: 'عرض الصلاحيات',
      onClick: (item) => {
        setSelectedItem(item)
        setModalType('view-role')
        setShowModal(true)
      },
      className: 'text-primary-600 hover:text-primary-800 hover:bg-primary-50'
    },
    {
      icon: Edit,
      label: 'تعديل',
      onClick: (item) => {
        setSelectedItem(item)
        setModalType('edit-role')
        setShowModal(true)
      },
      className: 'text-primary hover:text-green-800 hover:bg-primary/10'
    },
    {
      icon: Trash2,
      label: 'حذف',
      onClick: (item) => {
        if (window.confirm(`هل أنت متأكد من حذف الدور "${item.name}"؟`)) {
          handleDeleteRole(item.id)
        }
      },
      className: 'text-destructive hover:text-red-800 hover:bg-destructive/10'
    }
  ]

  // معالجة العمليات
  const handleToggleUserStatus = async (userId, newStatus) => {
    try {
      setUsers(prev => prev.map(user => 
        user.id === userId ? { ...user, is_active: newStatus } : user
      ))
      setFilteredData(prev => prev.map(user => 
        user.id === userId ? { ...user, is_active: newStatus } : user
      ))
    } catch (error) {
      }
  }

  const handleDeleteRole = async (roleId) => {
    try {
      setRoles(prev => prev.filter(role => role.id !== roleId))
    } catch (error) {
      }
  }

  // معالجة البحث والتصفية
  const handleSearch = (searchTerm) => {
    const currentData = activeTab === 'users' ? users : 
                       activeTab === 'roles' ? roles : userActivities
    
    const filtered = currentData.filter(item => {
      if (activeTab === 'users') {
        return item.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               item.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
               item.email.toLowerCase().includes(searchTerm.toLowerCase())
      } else if (activeTab === 'roles') {
        return item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               item.description.toLowerCase().includes(searchTerm.toLowerCase())
      } else {
        return item.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               item.action.toLowerCase().includes(searchTerm.toLowerCase())
      }
    })
    setFilteredData(filtered)
  }

  const handleFilter = (filters) => {
    const currentData = activeTab === 'users' ? users : 
                       activeTab === 'roles' ? roles : userActivities
    let filtered = [...currentData]
    
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        filtered = filtered.filter(item =>
          item[key] && item[key].toString().toLowerCase().includes(filters[key].toLowerCase())
        )
      }
    })
    
    setFilteredData(filtered)
  }

  // التبويبات
  const tabs = [
    { id: 'users', label: 'المستخدمين', icon: Users, count: users.length },
    { id: 'roles', label: 'الأدوار', icon: Shield, count: roles.length },
    { id: 'activities', label: 'سجل الأنشطة', icon: Activity, count: userActivities.length }
  ]

  // حقول نماذج المستخدمين
  const userFormFields = [
    {
      name: 'username',
      label: 'اسم المستخدم',
      type: 'text',
      required: true,
      placeholder: 'أدخل اسم المستخدم'
    },
    {
      name: 'full_name',
      label: 'الاسم الكامل',
      type: 'text',
      required: true,
      placeholder: 'أدخل الاسم الكامل'
    },
    {
      name: 'email',
      label: 'البريد الإلكتروني',
      type: 'email',
      required: true,
      placeholder: 'example@domain.com'
    },
    {
      name: 'phone',
      label: 'رقم الهاتف',
      type: 'text',
      placeholder: '01xxxxxxxxx'
    },
    {
      name: 'role_id',
      label: 'الدور',
      type: 'select',
      required: true,
      options: roles.map(role => ({ value: role.id, label: role.name }))
    },
    {
      name: 'department',
      label: 'القسم',
      type: 'text',
      placeholder: 'اسم القسم'
    },
    {
      name: 'position',
      label: 'المنصب',
      type: 'text',
      placeholder: 'المنصب الوظيفي'
    },
    {
      name: 'password',
      label: 'كلمة المرور',
      type: 'password',
      required: true,
      placeholder: 'كلمة مرور قوية'
    }
  ]

  // حقول نماذج الأدوار
  const roleFormFields = [
    {
      name: 'name',
      label: 'اسم الدور',
      type: 'text',
      required: true,
      placeholder: 'أدخل اسم الدور'
    },
    {
      name: 'description',
      label: 'الوصف',
      type: 'textarea',
      rows: 3,
      placeholder: 'وصف الدور والمسؤوليات'
    },
    {
      name: 'permissions',
      label: 'الصلاحيات',
      type: 'checkbox-group',
      required: true,
      options: permissions.map(perm => ({
        value: perm.id,
        label: perm.name,
        category: perm.category
      }))
    }
  ]

  if (loading) {
    return <LoadingSpinner size="lg" text="جاري تحميل إدارة المستخدمين..." />
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground flex items-center">
              <Users className="w-6 h-6 ml-2 text-primary-600" />
              إدارة المستخدمين المتقدمة
            </h1>
            <p className="text-muted-foreground mt-1">إدارة شاملة للمستخدمين والأدوار والصلاحيات</p>
          </div>

          <div className="flex items-center space-x-3 space-x-reverse">
            <button
              onClick={loadData}
              className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4 ml-1" />
              تحديث
            </button>

            <button
              onClick={() => console.log('Export users')}
              className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4 ml-1" />
              تصدير
            </button>

            {activeTab === 'users' && (
              <button
                onClick={() => {
                  setSelectedItem(null)
                  setModalType('add-user')
                  setShowModal(true)
                }}
                className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <UserPlus className="w-4 h-4 ml-1" />
                إضافة مستخدم
              </button>
            )}

            {activeTab === 'roles' && (
              <button
                onClick={() => {
                  setSelectedItem(null)
                  setModalType('add-role')
                  setShowModal(true)
                }}
                className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                <Shield className="w-4 h-4 ml-1" />
                إضافة دور
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Notification
          type="error"
          title="خطأ في تحميل البيانات"
          message={error}
          className="mb-6"
          onDismiss={() => setError(null)}
        />
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold">{users.length}</p>
            </div>
            <Users className="w-8 h-8 text-primary-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">المستخدمين النشطين</p>
              <p className="text-2xl font-bold">
                {users.filter(user => user.is_active).length}
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">الأدوار المتاحة</p>
              <p className="text-2xl font-bold">{roles.length}</p>
            </div>
            <Shield className="w-8 h-8 text-purple-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100">المتصلين الآن</p>
              <p className="text-2xl font-bold">
                {users.filter(user => user.status === 'online').length}
              </p>
            </div>
            <Activity className="w-8 h-8 text-orange-200" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    const newData = tab.id === 'users' ? users :
                                   tab.id === 'roles' ? roles : userActivities
                    setFilteredData(newData)
                  }}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  }`}
                >
                  <Icon className="w-4 h-4 ml-1" />
                  {tab.label}
                  <span className={`mr-2 px-2 py-0.5 rounded-full text-xs ${
                    activeTab === tab.id ? 'bg-primary-100 text-primary-600' : 'bg-muted text-muted-foreground'
                  }`}>
                    {tab.count}
                  </span>
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Search and Filter */}
      <SearchFilter
        onSearch={handleSearch}
        onFilter={handleFilter}
        placeholder={`البحث في ${
          activeTab === 'users' ? 'المستخدمين' :
          activeTab === 'roles' ? 'الأدوار' : 'الأنشطة'
        }...`}
        filters={
          activeTab === 'users' ? [
            {
              key: 'role',
              label: 'الدور',
              type: 'select',
              options: roles.map(role => ({ value: role.name, label: role.name }))
            },
            {
              key: 'department',
              label: 'القسم',
              type: 'select',
              options: [
                { value: 'الإدارة', label: 'الإدارة' },
                { value: 'المبيعات', label: 'المبيعات' },
                { value: 'المخازن', label: 'المخازن' },
                { value: 'المحاسبة', label: 'المحاسبة' }
              ]
            },
            {
              key: 'is_active',
              label: 'الحالة',
              type: 'select',
              options: [
                { value: 'true', label: 'نشط' },
                { value: 'false', label: 'غير نشط' }
              ]
            }
          ] : activeTab === 'roles' ? [
            {
              key: 'is_active',
              label: 'الحالة',
              type: 'select',
              options: [
                { value: 'true', label: 'نشط' },
                { value: 'false', label: 'غير نشط' }
              ]
            }
          ] : [
            {
              key: 'status',
              label: 'النتيجة',
              type: 'select',
              options: [
                { value: 'success', label: 'نجح' },
                { value: 'failed', label: 'فشل' }
              ]
            }
          ]
        }
        className="mb-6"
      />

      {/* Data Table */}
      <DataTable
        data={filteredData}
        columns={
          activeTab === 'users' ? userColumns :
          activeTab === 'roles' ? roleColumns : activityColumns
        }
        actions={
          activeTab === 'users' ? userActions :
          activeTab === 'roles' ? roleActions : []
        }
        searchable={false}
        filterable={false}
        exportable={true}
        loading={loading}
        onRowClick={(item) => {
          setSelectedItem(item)
          setModalType(activeTab === 'users' ? 'view-user' :
                     activeTab === 'roles' ? 'view-role' : 'view-activity')
          setShowModal(true)
        }}
      />

      {/* Modals */}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={
          modalType === 'add-user' ? 'إضافة مستخدم جديد' :
          modalType === 'edit-user' ? 'تعديل المستخدم' :
          modalType === 'view-user' ? 'تفاصيل المستخدم' :
          modalType === 'add-role' ? 'إضافة دور جديد' :
          modalType === 'edit-role' ? 'تعديل الدور' :
          modalType === 'view-role' ? 'تفاصيل الدور' :
          modalType === 'change-password' ? 'تغيير كلمة المرور' :
          'عرض النشاط'
        }
        size={modalType.includes('view') ? 'xl' : 'lg'}
      >
        {modalType === 'add-user' && (
          <DynamicForm
            fields={userFormFields}
            onSubmit={(_data) => {
              setShowModal(false)
            }}
            onCancel={() => setShowModal(false)}
            submitText="إضافة المستخدم"
          />
        )}

        {modalType === 'edit-user' && (
          <DynamicForm
            fields={userFormFields.filter(field => field.name !== 'password')}
            initialData={selectedItem}
            onSubmit={(_data) => {
              setShowModal(false)
            }}
            onCancel={() => setShowModal(false)}
            submitText="حفظ التعديلات"
          />
        )}

        {modalType === 'add-role' && (
          <DynamicForm
            fields={roleFormFields}
            onSubmit={(_data) => {
              setShowModal(false)
            }}
            onCancel={() => setShowModal(false)}
            submitText="إضافة الدور"
          />
        )}

        {modalType === 'edit-role' && (
          <DynamicForm
            fields={roleFormFields}
            initialData={selectedItem}
            onSubmit={(_data) => {
              setShowModal(false)
            }}
            onCancel={() => setShowModal(false)}
            submitText="حفظ التعديلات"
          />
        )}

        {modalType === 'view-user' && selectedItem && (
          <div className="space-y-6">
            {/* User Info */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-semibold text-foreground">معلومات المستخدم</h3>
                  <div className="mt-2 space-y-2">
                    <p><span className="font-medium">الاسم:</span> {selectedItem.full_name}</p>
                    <p><span className="font-medium">اسم المستخدم:</span> {selectedItem.username}</p>
                    <p><span className="font-medium">البريد:</span> {selectedItem.email}</p>
                    <p><span className="font-medium">الهاتف:</span> {selectedItem.phone}</p>
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">معلومات العمل</h3>
                  <div className="mt-2 space-y-2">
                    <p><span className="font-medium">الدور:</span> {selectedItem.role}</p>
                    <p><span className="font-medium">القسم:</span> {selectedItem.department}</p>
                    <p><span className="font-medium">المنصب:</span> {selectedItem.position}</p>
                    <p><span className="font-medium">الحالة:</span>
                      <span className={`mr-1 px-2 py-1 rounded-full text-xs ${
                        selectedItem.is_active ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
                      }`}>
                        {selectedItem.is_active ? 'نشط' : 'غير نشط'}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Activity Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-primary-50 p-4 rounded-lg text-center">
                <p className="text-sm text-primary-600">عدد مرات الدخول</p>
                <p className="text-2xl font-bold text-primary-800">{selectedItem.login_count}</p>
              </div>
              <div className="bg-primary/10 p-4 rounded-lg text-center">
                <p className="text-sm text-primary">آخر دخول</p>
                <p className="text-sm font-medium text-green-800">
                  {new Date(selectedItem.last_login).toLocaleString('ar-EG')}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <p className="text-sm text-purple-600">تاريخ الإنشاء</p>
                <p className="text-sm font-medium text-purple-800">
                  {new Date(selectedItem.created_at).toLocaleDateString('ar-EG')}
                </p>
              </div>
            </div>

            {/* Permissions */}
            <div>
              <h3 className="font-semibold text-foreground mb-3">الصلاحيات</h3>
              <div className="flex flex-wrap gap-2">
                {selectedItem.permissions?.map((permission, index) => (
                  <span key={index} className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
                    {permission}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {modalType === 'view-role' && selectedItem && (
          <div className="space-y-6">
            {/* Role Info */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <h3 className="font-semibold text-foreground mb-2">{selectedItem.name}</h3>
              <p className="text-muted-foreground">{selectedItem.description}</p>
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div>
                  <span className="font-medium">عدد المستخدمين:</span>
                  <span className="mr-2 text-primary-600 font-bold">{selectedItem.users_count}</span>
                </div>
                <div>
                  <span className="font-medium">الحالة:</span>
                  <span className={`mr-2 px-2 py-1 rounded-full text-xs ${
                    selectedItem.is_active ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
                  }`}>
                    {selectedItem.is_active ? 'نشط' : 'غير نشط'}
                  </span>
                </div>
              </div>
            </div>

            {/* Permissions */}
            <div>
              <h3 className="font-semibold text-foreground mb-3">الصلاحيات المتاحة</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {permissions.filter(perm => selectedItem.permissions?.includes(perm.id)).map((permission) => (
                  <div key={permission.id} className="flex items-center p-3 bg-primary-50 rounded-lg">
                    <CheckCircle className="w-5 h-5 text-primary-600 ml-2" />
                    <div>
                      <p className="font-medium text-primary-900">{permission.name}</p>
                      <p className="text-sm text-primary-600">{permission.category}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {modalType === 'change-password' && (
          <DynamicForm
            fields={[
              {
                name: 'current_password',
                label: 'كلمة المرور الحالية',
                type: 'password',
                required: true
              },
              {
                name: 'new_password',
                label: 'كلمة المرور الجديدة',
                type: 'password',
                required: true
              },
              {
                name: 'confirm_password',
                label: 'تأكيد كلمة المرور',
                type: 'password',
                required: true
              }
            ]}
            onSubmit={(_data) => {
              setShowModal(false)
            }}
            onCancel={() => setShowModal(false)}
            submitText="تغيير كلمة المرور"
          />
        )}
      </Modal>
    </div>
  )
}

export default UserManagementAdvanced

