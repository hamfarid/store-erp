import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, Edit, Trash2, Eye, RefreshCw, User, Shield, CheckCircle, XCircle, UserX, UserCheck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import apiClient from '../services/apiClient';

const UserManagementComplete = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPermissionsModal, setShowPermissionsModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const { user: currentUser, hasPermission, PERMISSIONS, ROLES } = useAuth();

  // بيانات تجريبية للمستخدمين
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      console.log('🔄 Loading users from API...');
      const response = await apiClient.get('/api/users');
      console.log('📥 API Response:', response.data);
      
      if (response.data.success && response.data.data) {
        // Handle both array and object with users property
        const usersData = Array.isArray(response.data.data) 
          ? response.data.data 
          : response.data.data.users || [];
        console.log('✅ Users loaded:', usersData.length, 'users');
        console.log('First user:', usersData[0]);
        setUsers(usersData);
      } else {
        console.warn('⚠️ No data in response');
      }
      setLoading(false);
    } catch (error) {
      console.error('❌ Error loading users:', error);
      console.error('Error details:', error.response?.data);
      setLoading(false);
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = !roleFilter || user.role === roleFilter;
    const matchesStatus = statusFilter === '' || 
                         (statusFilter === 'active' && user.is_active) ||
                         (statusFilter === 'inactive' && !user.is_active);
    
    return matchesSearch && matchesRole && matchesStatus;
  });

  const getRoleText = (role) => {
    return ROLES[role]?.name || role;
  };

  const getRoleColor = (role) => {
    const colors = {
      admin: 'bg-destructive/20 text-red-800',
      manager: 'bg-primary-100 text-primary-800',
      user: 'bg-primary/20 text-green-800',
      viewer: 'bg-muted text-foreground'
    };
    return colors[role] || 'bg-muted text-foreground';
  };

  const getStatusColor = (isActive) => {
    return isActive ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800';
  };

  const toggleUserStatus = (userId) => {
    setUsers(prev => 
      prev.map(user => 
        user.id === userId 
          ? { ...user, is_active: !user.is_active }
          : user
      )
    );
  };

  const editUser = (user) => {
    setSelectedUser(user);
    setShowEditModal(true);
  };

  const managePermissions = (user) => {
    setSelectedUser(user);
    setShowPermissionsModal(true);
  };

  const deleteUser = (userId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
      setUsers(prev => prev.filter(user => user.id !== userId));
    }
  };

  // مكون إضافة/تعديل مستخدم
  const UserFormModal = ({ isEdit = false }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">
            {isEdit ? 'تعديل مستخدم' : 'إضافة مستخدم جديد'}
          </h3>
          <button
            onClick={() => {
              setShowAddModal(false);
              setShowEditModal(false);
              setSelectedUser(null);
            }}
            className="text-gray-500 hover:text-foreground"
          >
            ✕
          </button>
        </div>
        
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              اسم المستخدم *
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue={isEdit ? selectedUser?.username : ''}
              placeholder="username"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              الاسم الكامل *
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue={isEdit ? selectedUser?.name : ''}
              placeholder="الاسم الكامل"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              البريد الإلكتروني *
            </label>
            <input
              type="email"
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue={isEdit ? selectedUser?.email : ''}
              placeholder="email@example.com"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              رقم الهاتف
            </label>
            <input
              type="tel"
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue={isEdit ? selectedUser?.phone : ''}
              placeholder="01234567890"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              الدور *
            </label>
            <select 
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue={isEdit ? selectedUser?.role : ''}
              required
            >
              <option value="">اختر الدور</option>
              {Object.entries(ROLES).map(([key, role]) => (
                <option key={key} value={key}>{role.name}</option>
              ))}
            </select>
          </div>
          
          {!isEdit && (
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                كلمة المرور *
              </label>
              <input
                type="password"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="كلمة المرور"
                required
              />
            </div>
          )}
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_active"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-border rounded"
              defaultChecked={isEdit ? selectedUser?.is_active : true}
            />
            <label htmlFor="is_active" className="mr-2 block text-sm text-foreground">
              مستخدم نشط
            </label>
          </div>
          
          <div className="flex justify-end space-x-2 space-x-reverse">
            <button
              type="button"
              onClick={() => {
                setShowAddModal(false);
                setShowEditModal(false);
                setSelectedUser(null);
              }}
              className="px-4 py-2 text-muted-foreground bg-muted rounded-md hover:bg-muted"
            >
              إلغاء
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              {isEdit ? 'تحديث' : 'إنشاء'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // مكون إدارة الصلاحيات
  const PermissionsModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">
            إدارة صلاحيات: {selectedUser?.name}
          </h3>
          <button
            onClick={() => {
              setShowPermissionsModal(false);
              setSelectedUser(null);
            }}
            className="text-gray-500 hover:text-foreground"
          >
            ✕
          </button>
        </div>
        
        <div className="mb-4 p-3 bg-primary-50 rounded-lg">
          <p className="text-sm text-primary-800">
            <strong>الدور الحالي:</strong> {getRoleText(selectedUser?.role)}
          </p>
          <p className="text-xs text-primary-600 mt-1">
            الصلاحيات أدناه مبنية على الدور المحدد للمستخدم
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(PERMISSIONS).map(([key, description]) => {
            const hasPermission = ROLES[selectedUser?.role]?.permissions.includes(key);
            return (
              <div key={key} className={`p-3 rounded-lg border ${
                hasPermission ? 'bg-primary/10 border-primary/30' : 'bg-muted/50 border-border'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {hasPermission ? (
                      <CheckCircle className="h-4 w-4 text-primary ml-2" />
                    ) : (
                      <XCircle className="h-4 w-4 text-gray-400 ml-2" />
                    )}
                    <div>
                      <p className="text-sm font-medium text-foreground">{description}</p>
                      <p className="text-xs text-gray-500">{key}</p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={() => {
              setShowPermissionsModal(false);
              setSelectedUser(null);
            }}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            إغلاق
          </button>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة المستخدمين والصلاحيات</h1>
          <p className="text-muted-foreground">إدارة شاملة للمستخدمين وصلاحياتهم في النظام</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 flex items-center"
        >
          <Plus className="h-4 w-4 ml-2" />
          إضافة مستخدم جديد
        </button>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-primary-500">
          <div className="flex items-center">
            <User className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-foreground">{users.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-green-500">
          <div className="flex items-center">
            <UserCheck className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المستخدمين النشطين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => u.is_active).length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-red-500">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المديرين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => u.role === 'admin').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-orange-500">
          <div className="flex items-center">
            <UserX className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">غير النشطين</p>
              <p className="text-2xl font-bold text-foreground">
                {users.filter(u => !u.is_active).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* أدوات البحث والفلترة */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="البحث بالاسم أو البريد..."
              className="w-full pr-10 pl-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
          >
            <option value="">جميع الأدوار</option>
            {Object.entries(ROLES).map(([key, role]) => (
              <option key={key} value={key}>{role.name}</option>
            ))}
          </select>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">جميع الحالات</option>
            <option value="active">نشط</option>
            <option value="inactive">غير نشط</option>
          </select>
          
          <button
            onClick={() => {
              setSearchTerm('');
              setRoleFilter('');
              setStatusFilter('');
            }}
            className="px-4 py-2 bg-muted text-foreground rounded-md hover:bg-muted"
          >
            إعادة تعيين
          </button>
        </div>
      </div>

      {/* جدول المستخدمين */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
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
                  الحالة
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  آخر دخول
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  تاريخ الإنشاء
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
                        <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                          <User className="h-6 w-6 text-muted-foreground" />
                        </div>
                      </div>
                      <div className="mr-4">
                        <div className="text-sm font-medium text-foreground">{user.name}</div>
                        <div className="text-sm text-gray-500">{user.email}</div>
                        <div className="text-xs text-gray-400">@{user.username}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(user.role)}`}>
                      {getRoleText(user.role)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(user.is_active)}`}>
                      {user.is_active ? (
                        <>
                          <CheckCircle className="h-3 w-3 ml-1" />
                          نشط
                        </>
                      ) : (
                        <>
                          <XCircle className="h-3 w-3 ml-1" />
                          غير نشط
                        </>
                      )}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {user.last_login ? new Date(user.last_login).toLocaleDateString('ar-EG') : 'لم يدخل بعد'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {new Date(user.created_at).toLocaleDateString('ar-EG')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2 space-x-reverse">
                      <button
                        onClick={() => managePermissions(user)}
                        className="text-purple-600 hover:text-purple-900"
                        title="إدارة الصلاحيات"
                      >
                        <Shield className="h-4 w-4" />
                      </button>
                      
                      {hasPermission('users.edit') && (
                        <button
                          onClick={() => editUser(user)}
                          className="text-primary-600 hover:text-primary-900"
                          title="تعديل"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                      )}
                      
                      {hasPermission('users.edit') && user.id !== currentUser?.id && (
                        <button
                          onClick={() => toggleUserStatus(user.id)}
                          className={`${user.is_active ? 'text-destructive hover:text-red-900' : 'text-primary hover:text-green-900'}`}
                          title={user.is_active ? 'إلغاء التفعيل' : 'تفعيل'}
                        >
                          {user.is_active ? <UserX className="h-4 w-4" /> : <UserCheck className="h-4 w-4" />}
                        </button>
                      )}
                      
                      {hasPermission('users.delete') && user.id !== currentUser?.id && (
                        <button
                          onClick={() => deleteUser(user.id)}
                          className="text-destructive hover:text-red-900"
                          title="حذف"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* النوافذ المنبثقة */}
      {showAddModal && <UserFormModal />}
      {showEditModal && <UserFormModal isEdit={true} />}
      {showPermissionsModal && <PermissionsModal />}
    </div>
  );
};

export default UserManagementComplete;

