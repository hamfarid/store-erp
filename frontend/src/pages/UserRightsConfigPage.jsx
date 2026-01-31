/**
 * User Rights Configuration Page
 * 
 * Allows administrators to configure user permissions and roles
 */

import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Users, 
  Key, 
  Save, 
  Plus, 
  Trash2, 
  Edit2, 
  Check, 
  X,
  Search,
  Filter,
  ChevronDown,
  ChevronRight,
  AlertCircle,
  CheckCircle2,
  Lock,
  Unlock,
  UserCog,
  Settings
} from 'lucide-react';
import { useAuth, PERMISSIONS, ROLES } from '../contexts/AuthContext';
import { apiRequest, API_ENDPOINTS } from '../config/api';
import toast from 'react-hot-toast';

// Permission categories for organization
const PERMISSION_CATEGORIES = {
  products: {
    name: 'المنتجات',
    nameEn: 'Products',
    icon: '📦',
    permissions: ['products.view', 'products.create', 'products.edit', 'products.delete']
  },
  inventory: {
    name: 'المخزون',
    nameEn: 'Inventory',
    icon: '📊',
    permissions: ['inventory.view', 'inventory.edit', 'inventory.adjust']
  },
  lots: {
    name: 'اللوتات',
    nameEn: 'Lots',
    icon: '📋',
    permissions: ['lots.view', 'lots.create', 'lots.edit', 'lots.delete']
  },
  stock_movements: {
    name: 'حركات المخزون',
    nameEn: 'Stock Movements',
    icon: '🔄',
    permissions: ['stock_movements.view', 'stock_movements.create', 'stock_movements.edit']
  },
  customers: {
    name: 'العملاء',
    nameEn: 'Customers',
    icon: '👥',
    permissions: ['customers.view', 'customers.create', 'customers.edit', 'customers.delete']
  },
  suppliers: {
    name: 'الموردين',
    nameEn: 'Suppliers',
    icon: '🚚',
    permissions: ['suppliers.view', 'suppliers.create', 'suppliers.edit', 'suppliers.delete']
  },
  invoices: {
    name: 'الفواتير',
    nameEn: 'Invoices',
    icon: '📄',
    permissions: ['invoices.view', 'invoices.create', 'invoices.edit', 'invoices.delete', 'invoices.print']
  },
  warehouses: {
    name: 'المخازن',
    nameEn: 'Warehouses',
    icon: '🏭',
    permissions: ['warehouses.view', 'warehouses.create', 'warehouses.edit', 'warehouses.delete']
  },
  categories: {
    name: 'الفئات',
    nameEn: 'Categories',
    icon: '📁',
    permissions: ['categories.view', 'categories.create', 'categories.edit', 'categories.delete']
  },
  reports: {
    name: 'التقارير',
    nameEn: 'Reports',
    icon: '📈',
    permissions: ['reports.view', 'reports.export', 'reports.print']
  },
  users: {
    name: 'المستخدمين',
    nameEn: 'Users',
    icon: '👤',
    permissions: ['users.view', 'users.create', 'users.edit', 'users.delete', 'users.permissions']
  },
  settings: {
    name: 'الإعدادات',
    nameEn: 'Settings',
    icon: '⚙️',
    permissions: ['company.view', 'company.edit', 'settings.view', 'settings.edit']
  },
  system: {
    name: 'النظام',
    nameEn: 'System',
    icon: '🔧',
    permissions: ['system.backup', 'system.restore', 'system.logs']
  }
};

const UserRightsConfigPage = () => {
  // const { user, hasPermission } = useAuth(); // Currently unused
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedRole, setSelectedRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('users'); // users, roles
  const [expandedCategories, setExpandedCategories] = useState({});
  const [userPermissions, setUserPermissions] = useState([]);
  const [userRole, setUserRole] = useState('');

  // Load users and roles
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // Load users
      const usersData = await apiRequest(API_ENDPOINTS.USERS.LIST);
      setUsers(usersData.data || usersData || []);

      // Load roles from API or use defaults
      try {
        const rolesData = await apiRequest(API_ENDPOINTS.ADMIN.ROLES);
        setRoles(rolesData.data || rolesData || Object.entries(ROLES).map(([key, value]) => ({
          id: key,
          name: value.name,
          permissions: value.permissions
        })));
      } catch {
        // Use default roles if API not available
        setRoles(Object.entries(ROLES).map(([key, value]) => ({
          id: key,
          name: value.name,
          permissions: value.permissions
        })));
      }
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('خطأ في تحميل البيانات');
      
      // Use mock data for demo
      setUsers([
        { id: 1, username: 'admin', name: 'المدير العام', role: 'admin', email: 'admin@store.com' },
        { id: 2, username: 'manager', name: 'مدير المخزون', role: 'manager', email: 'manager@store.com' },
        { id: 3, username: 'user1', name: 'موظف مبيعات', role: 'user', email: 'user1@store.com' }
      ]);
    }
    setLoading(false);
  };

  const handleSelectUser = (userItem) => {
    setSelectedUser(userItem);
    setUserRole(userItem.role || 'user');
    setUserPermissions(userItem.permissions || ROLES[userItem.role]?.permissions || []);
    setSelectedRole(null);
  };

  const handleSelectRole = (role) => {
    setSelectedRole(role);
    setSelectedUser(null);
  };

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const togglePermission = (permission) => {
    setUserPermissions(prev => {
      if (prev.includes(permission)) {
        return prev.filter(p => p !== permission);
      }
      return [...prev, permission];
    });
  };

  const toggleAllInCategory = (category) => {
    const categoryPermissions = PERMISSION_CATEGORIES[category].permissions;
    const allSelected = categoryPermissions.every(p => userPermissions.includes(p));
    
    if (allSelected) {
      setUserPermissions(prev => prev.filter(p => !categoryPermissions.includes(p)));
    } else {
      setUserPermissions(prev => [...new Set([...prev, ...categoryPermissions])]);
    }
  };

  const handleRoleChange = (newRole) => {
    setUserRole(newRole);
    // Set default permissions for the role
    const rolePermissions = ROLES[newRole]?.permissions || [];
    setUserPermissions(rolePermissions);
  };

  const handleSaveUserRights = async () => {
    if (!selectedUser) return;
    
    setSaving(true);
    try {
      // Update user role
      await apiRequest(API_ENDPOINTS.ADMIN.ASSIGN_USER_ROLE(selectedUser.id), {
        method: 'PUT',
        body: JSON.stringify({ role: userRole })
      });

      // Update user permissions
      await apiRequest(API_ENDPOINTS.USERS.ASSIGN_PERMISSIONS(selectedUser.id), {
        method: 'PUT',
        body: JSON.stringify({ permissions: userPermissions })
      });

      toast.success('تم حفظ صلاحيات المستخدم بنجاح');
      loadData();
    } catch (error) {
      console.error('Error saving user rights:', error);
      toast.error(error.message || 'خطأ في حفظ الصلاحيات');
    }
    setSaving(false);
  };

  const filteredUsers = users.filter(u => 
    u.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="page-title flex items-center gap-3">
          <Shield className="w-8 h-8 text-primary-500" />
          إعدادات صلاحيات المستخدمين
        </h1>
        <p className="text-secondary mt-2">
          إدارة أدوار وصلاحيات المستخدمين في النظام
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab('users')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
            activeTab === 'users'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'bg-secondary text-secondary hover:bg-hover'
          }`}
        >
          <Users className="w-5 h-5" />
          المستخدمين
        </button>
        <button
          onClick={() => setActiveTab('roles')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
            activeTab === 'roles'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'bg-secondary text-secondary hover:bg-hover'
          }`}
        >
          <Key className="w-5 h-5" />
          الأدوار
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Users/Roles List */}
        <div className="lg:col-span-1">
          <div className="entity-card overflow-hidden p-0">
            {/* Search */}
            <div className="p-4 border-b border-light">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-tertiary" />
                <input
                  type="text"
                  placeholder="بحث..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pr-10 pl-4 py-2 border border-light rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-secondary"
                />
              </div>
            </div>

            {/* List */}
            <div className="max-h-[600px] overflow-y-auto">
              {activeTab === 'users' ? (
                filteredUsers.map(userItem => (
                  <button
                    key={userItem.id}
                    onClick={() => handleSelectUser(userItem)}
                    className={`w-full p-4 flex items-center gap-3 border-b border-light hover:bg-hover transition-colors ${
                      selectedUser?.id === userItem.id ? 'bg-primary-50 border-r-4 border-r-primary-500' : ''
                    }`}
                  >
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold">
                      {userItem.name?.charAt(0) || userItem.username?.charAt(0)}
                    </div>
                    <div className="flex-1 text-right">
                      <p className="font-medium text-primary">{userItem.name || userItem.username}</p>
                      <p className="text-sm text-secondary">{userItem.email}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      userItem.role === 'admin' ? 'bg-red-100 text-red-700' :
                      userItem.role === 'manager' ? 'bg-blue-100 text-blue-700' :
                      'status-badge--neutral'
                    }`}>
                      {ROLES[userItem.role]?.name || userItem.role}
                    </span>
                  </button>
                ))
              ) : (
                roles.map(role => (
                  <button
                    key={role.id}
                    onClick={() => handleSelectRole(role)}
                    className={`w-full p-4 flex items-center gap-3 border-b border-light hover:bg-hover transition-colors ${
                      selectedRole?.id === role.id ? 'bg-primary-50 border-r-4 border-r-primary-500' : ''
                    }`}
                  >
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-secondary-400 to-secondary-600 flex items-center justify-center text-white">
                      <Key className="w-5 h-5" />
                    </div>
                    <div className="flex-1 text-right">
                      <p className="font-medium text-primary">{role.name}</p>
                      <p className="text-sm text-secondary">{role.permissions?.length || 0} صلاحية</p>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Permissions Panel */}
        <div className="lg:col-span-2">
          {selectedUser ? (
            <div className="entity-card overflow-hidden p-0">
              {/* User Header */}
              <div className="p-6 bg-gradient-to-l from-primary-500 to-primary-600 text-white">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-full bg-white/20 flex items-center justify-center text-2xl font-bold">
                    {selectedUser.name?.charAt(0) || selectedUser.username?.charAt(0)}
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">{selectedUser.name || selectedUser.username}</h2>
                    <p className="text-primary-100">{selectedUser.email}</p>
                  </div>
                </div>
              </div>

              {/* Role Selection */}
              <div className="p-6 border-b border-light">
                <label className="block text-sm font-medium text-secondary mb-2">
                  الدور الوظيفي
                </label>
                <select
                  value={userRole}
                  onChange={(e) => handleRoleChange(e.target.value)}
                  className="w-full p-3 border border-light rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-secondary"
                >
                  {Object.entries(ROLES).map(([key, value]) => (
                    <option key={key} value={key}>{value.name}</option>
                  ))}
                </select>
              </div>

              {/* Permissions Grid */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-primary mb-4 flex items-center gap-2">
                  <Lock className="w-5 h-5 text-primary-500" />
                  الصلاحيات التفصيلية
                </h3>

                <div className="space-y-4">
                  {Object.entries(PERMISSION_CATEGORIES).map(([key, category]) => {
                    const isExpanded = expandedCategories[key];
                    const categoryPerms = category.permissions;
                    const selectedCount = categoryPerms.filter(p => userPermissions.includes(p)).length;
                    const allSelected = selectedCount === categoryPerms.length;

                    return (
                      <div key={key} className="border border-light rounded-xl overflow-hidden">
                        {/* Category Header */}
                        <button
                          onClick={() => toggleCategory(key)}
                          className="w-full p-4 flex items-center justify-between bg-secondary hover:bg-hover transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-2xl">{category.icon}</span>
                            <span className="font-medium text-primary">{category.name}</span>
                            <span className="text-sm text-secondary">
                              ({selectedCount}/{categoryPerms.length})
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                toggleAllInCategory(key);
                              }}
                              className={`p-2 rounded-lg transition-colors ${
                                allSelected
                                  ? 'bg-primary-100 text-primary-700'
                                  : 'bg-secondary text-secondary hover:bg-hover'
                              }`}
                            >
                              {allSelected ? <CheckCircle2 className="w-4 h-4" /> : <Check className="w-4 h-4" />}
                            </button>
                            {isExpanded ? (
                              <ChevronDown className="w-5 h-5 text-tertiary" />
                            ) : (
                              <ChevronRight className="w-5 h-5 text-tertiary" />
                            )}
                          </div>
                        </button>

                        {/* Permissions List */}
                        {isExpanded && (
                          <div className="p-4 grid grid-cols-2 gap-3">
                            {categoryPerms.map(permission => {
                              const isSelected = userPermissions.includes(permission);
                              const permName = PERMISSIONS[permission] || permission;

                              return (
                                <button
                                  key={permission}
                                  onClick={() => togglePermission(permission)}
                                  className={`p-3 rounded-xl flex items-center gap-2 transition-all ${
                                    isSelected
                                      ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
                                      : 'bg-secondary text-secondary border-2 border-transparent hover:border-light'
                                  }`}
                                >
                                  {isSelected ? (
                                    <Unlock className="w-4 h-4" />
                                  ) : (
                                    <Lock className="w-4 h-4" />
                                  )}
                                  <span className="text-sm font-medium">{permName}</span>
                                </button>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Save Button */}
              <div className="p-6 bg-secondary border-t border-light">
                <button
                  onClick={handleSaveUserRights}
                  disabled={saving}
                  className="w-full flex items-center justify-center gap-2 bg-gradient-to-l from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white py-4 px-6 rounded-xl font-medium transition-all shadow-lg hover:shadow-primary-500/30 disabled:opacity-50"
                >
                  {saving ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      جاري الحفظ...
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      حفظ التغييرات
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : selectedRole ? (
            <div className="entity-card overflow-hidden p-0">
              {/* Role Header */}
              <div className="p-6 bg-gradient-to-l from-secondary-500 to-secondary-600 text-white">
                <h2 className="text-2xl font-bold flex items-center gap-3">
                  <Key className="w-8 h-8" />
                  {selectedRole.name}
                </h2>
                <p className="text-secondary-100 mt-1">
                  {selectedRole.permissions?.length || 0} صلاحية
                </p>
              </div>

              {/* Role Permissions */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-primary mb-4">
                  صلاحيات هذا الدور:
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {selectedRole.permissions?.map(permission => (
                    <div
                      key={permission}
                      className="p-3 bg-secondary-50 text-secondary-700 rounded-xl flex items-center gap-2"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="text-sm">{PERMISSIONS[permission] || permission}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="entity-card p-12 flex flex-col items-center justify-center text-center">
              <UserCog className="w-16 h-16 text-tertiary mb-4" />
              <h3 className="text-xl font-semibold text-primary mb-2">
                اختر مستخدم أو دور
              </h3>
              <p className="text-secondary">
                اختر مستخدم من القائمة لتعديل صلاحياته، أو دور لعرض تفاصيله
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserRightsConfigPage;

