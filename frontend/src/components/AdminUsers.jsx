import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  UserX
} from 'lucide-react'

const AdminUsers = () => {
  const [users, setUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadUsers()
  }, [])

  useEffect(() => {
    filterUsers()
  }, [users, searchTerm])

  const loadUsers = async () => {
    setLoading(true)
    try {
      // بيانات تجريبية للمستخدمين
      const mockUsers = [
        {
          id: 1,
          username: 'admin',
          name: 'مدير النظام',
          email: 'admin@gaaraseeds.com',
          phone: '+20-1001234567',
          role: 'admin',
          isActive: true,
          lastLogin: '2024-07-04 10:30',
          createdAt: '2024-01-01',
          permissions: ['all']
        },
        {
          id: 2,
          username: 'sales_manager',
          name: 'أحمد محمد - مدير المبيعات',
          email: 'ahmed@gaaraseeds.com',
          phone: '+20-1009876543',
          role: 'sales_manager',
          isActive: true,
          lastLogin: '2024-07-04 09:15',
          createdAt: '2024-02-15',
          permissions: ['sales', 'customers', 'reports']
        },
        {
          id: 3,
          username: 'warehouse_manager',
          name: 'سارة علي - مدير المخزن',
          email: 'sara@gaaraseeds.com',
          phone: '+20-1005555555',
          role: 'warehouse_manager',
          isActive: true,
          lastLogin: '2024-07-03 16:45',
          createdAt: '2024-03-01',
          permissions: ['inventory', 'warehouses', 'stock_movements']
        },
        {
          id: 4,
          username: 'accountant',
          name: 'محمد حسن - محاسب',
          email: 'mohamed@gaaraseeds.com',
          phone: '+20-1007777777',
          role: 'accountant',
          isActive: true,
          lastLogin: '2024-07-04 08:00',
          createdAt: '2024-04-10',
          permissions: ['accounting', 'reports', 'invoices']
        },
        {
          id: 5,
          username: 'sales_engineer',
          name: 'فاطمة أحمد - مهندس مبيعات',
          email: 'fatma@gaaraseeds.com',
          phone: '+20-1008888888',
          role: 'sales_engineer',
          isActive: false,
          lastLogin: '2024-07-01 14:20',
          createdAt: '2024-05-20',
          permissions: ['customers', 'sales']
        }
      ]
      setUsers(mockUsers)
    } catch (err) {
      showNotification('فشل في تحميل المستخدمين', 'error')
    } finally {
      setLoading(false)
    }
  }

  const filterUsers = () => {
    if (searchTerm) {
      const filtered = users.filter(user =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.role.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredUsers(filtered)
    } else {
      setFilteredUsers(users)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddUser = () => {
    setEditingUser(null)
    setShowModal(true)
  }

  const handleEditUser = (user) => {
    setEditingUser(user)
    setShowModal(true)
  }

  const handleDeleteUser = async (userId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
      try {
        setUsers(prev => prev.filter(u => u.id !== userId))
        showNotification('تم حذف المستخدم بنجاح')
      } catch (err) {
        showNotification('فشل في حذف المستخدم', 'error')
      }
    }
  }

  const handleToggleStatus = async (userId) => {
    try {
      setUsers(prev => prev.map(u => 
        u.id === userId ? { ...u, isActive: !u.isActive } : u
      ))
      showNotification('تم تحديث حالة المستخدم بنجاح')
    } catch (err) {
      showNotification('فشل في تحديث حالة المستخدم', 'error')
    }
  }

  const getRoleLabel = (role) => {
    const roles = {
      'admin': 'مدير النظام',
      'sales_manager': 'مدير المبيعات',
      'warehouse_manager': 'مدير المخزن',
      'accountant': 'محاسب',
      'sales_engineer': 'مهندس مبيعات',
      'user': 'مستخدم عادي'
    }
    return roles[role] || role
  }

  const getRoleColor = (role) => {
    const colors = {
      'admin': 'bg-destructive/20 text-red-800',
      'sales_manager': 'bg-primary-100 text-primary-800',
      'warehouse_manager': 'bg-primary/20 text-green-800',
      'accountant': 'bg-purple-100 text-purple-800',
      'sales_engineer': 'bg-accent/20 text-orange-800',
      'user': 'bg-muted text-foreground'
    }
    return colors[role] || 'bg-muted text-foreground'
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
          <h1 className="text-2xl font-bold text-foreground">إدارة المستخدمين</h1>
          <p className="text-muted-foreground">إدارة حسابات المستخدمين والصلاحيات</p>
        </div>
        <button
          onClick={handleAddUser}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة مستخدم جديد
        </button>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في المستخدمين..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadUsers}
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
            <Users className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-foreground">{users.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <UserCheck className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المستخدمين النشطين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => u.isActive).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <UserX className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المستخدمين المعطلين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => !u.isActive).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المديرين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => u.role.includes('admin') || u.role.includes('manager')).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المستخدم
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الدور
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                معلومات الاتصال
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                آخر دخول
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
            {filteredUsers.map((user) => (
              <tr key={user.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                        <Users className="h-5 w-5 text-primary-600" />
                      </div>
                    </div>
                    <div className="mr-4">
                      <div className="text-sm font-medium text-foreground">{user.name}</div>
                      <div className="text-sm text-gray-500">@{user.username}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(user.role)}`}>
                    {getRoleLabel(user.role)}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div className="flex items-center mb-1">
                    <Mail className="h-4 w-4 text-gray-400 ml-2" />
                    {user.email}
                  </div>
                  <div className="flex items-center">
                    <Phone className="h-4 w-4 text-gray-400 ml-2" />
                    {user.phone}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 text-gray-400 ml-2" />
                    {user.lastLogin}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={() => handleToggleStatus(user.id)}
                    className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      user.isActive 
                        ? 'bg-primary/20 text-green-800 hover:bg-green-200' 
                        : 'bg-destructive/20 text-red-800 hover:bg-red-200'
                    } transition-colors`}
                  >
                    {user.isActive ? 'نشط' : 'معطل'}
                  </button>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEditUser(user)}
                      className="text-primary-600 hover:text-primary-900"
                      title="تعديل"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteUser(user.id)}
                      className="text-destructive hover:text-red-900"
                      title="حذف"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}

      {/* Add/Edit Modal - Simplified */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium mb-4">
              {editingUser ? 'تعديل المستخدم' : 'إضافة مستخدم جديد'}
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="الاسم الكامل"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingUser?.name || ''}
              />
              <input
                type="text"
                placeholder="اسم المستخدم"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingUser?.username || ''}
              />
              <input
                type="email"
                placeholder="البريد الإلكتروني"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingUser?.email || ''}
              />
              <input
                type="tel"
                placeholder="رقم الهاتف"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingUser?.phone || ''}
              />
              <select className="w-full p-2 border border-border rounded-lg">
                <option value="">اختر الدور</option>
                <option value="admin">مدير النظام</option>
                <option value="sales_manager">مدير المبيعات</option>
                <option value="warehouse_manager">مدير المخزن</option>
                <option value="accountant">محاسب</option>
                <option value="sales_engineer">مهندس مبيعات</option>
                <option value="user">مستخدم عادي</option>
              </select>
              {!editingUser && (
                <input
                  type="password"
                  placeholder="كلمة المرور"
                  className="w-full p-2 border border-border rounded-lg"
                />
              )}
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
                  showNotification(editingUser ? 'تم تحديث المستخدم بنجاح' : 'تم إضافة المستخدم بنجاح')
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

export default AdminUsers

