/**
 * User Rights Configuration Page
 * 
 * Manage user roles and permissions assignments.
 */

import React, { useState } from 'react';
import {
  Search, Users, Shield, Key, Plus, Edit, Trash2, Eye, Save,
  CheckCircle, XCircle, Crown, Briefcase, ShoppingCart, Calculator,
  Warehouse, Lock, Unlock, UserPlus, UserMinus, RefreshCw, Filter
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

// Sample users data
const sampleUsers = [
  { id: 1, name: 'أحمد محمد', username: 'ahmed', email: 'ahmed@company.com', status: 'active', roles: ['super_admin'], lastLogin: '2024-12-01 10:30' },
  { id: 2, name: 'سارة العلي', username: 'sara', email: 'sara@company.com', status: 'active', roles: ['admin'], lastLogin: '2024-12-01 09:15' },
  { id: 3, name: 'محمد الخالد', username: 'mohammed', email: 'mohammed@company.com', status: 'active', roles: ['manager'], lastLogin: '2024-11-30 16:45' },
  { id: 4, name: 'فاطمة أحمد', username: 'fatima', email: 'fatima@company.com', status: 'inactive', roles: ['accountant'], lastLogin: '2024-11-25 11:20' },
  { id: 5, name: 'خالد السعيد', username: 'khaled', email: 'khaled@company.com', status: 'active', roles: ['sales'], lastLogin: '2024-12-01 08:00' },
  { id: 6, name: 'نورة الحربي', username: 'noura', email: 'noura@company.com', status: 'active', roles: ['warehouse'], lastLogin: '2024-11-30 14:30' },
  { id: 7, name: 'عبدالله العتيبي', username: 'abdullah', email: 'abdullah@company.com', status: 'active', roles: ['sales', 'viewer'], lastLogin: '2024-11-29 09:00' },
];

// Available roles
const availableRoles = [
  { code: 'super_admin', name: 'مدير النظام', color: 'rose', icon: Crown, isSystem: true },
  { code: 'admin', name: 'مدير', color: 'purple', icon: Shield, isSystem: true },
  { code: 'manager', name: 'مدير فرع', color: 'blue', icon: Briefcase, isSystem: false },
  { code: 'sales', name: 'مبيعات', color: 'teal', icon: ShoppingCart, isSystem: false },
  { code: 'accountant', name: 'محاسب', color: 'emerald', icon: Calculator, isSystem: false },
  { code: 'warehouse', name: 'أمين مستودع', color: 'amber', icon: Warehouse, isSystem: false },
  { code: 'viewer', name: 'مشاهد', color: 'gray', icon: Eye, isSystem: false },
];

const colorMap = {
  rose: 'bg-rose-100 text-rose-700 border-rose-200',
  purple: 'bg-purple-100 text-purple-700 border-purple-200',
  blue: 'bg-blue-100 text-blue-700 border-blue-200',
  teal: 'bg-teal-100 text-teal-700 border-teal-200',
  emerald: 'bg-emerald-100 text-emerald-700 border-emerald-200',
  amber: 'bg-amber-100 text-amber-700 border-amber-200',
  gray: 'status-badge--neutral',
};

const RoleBadge = ({ roleCode }) => {
  const role = availableRoles.find(r => r.code === roleCode);
  if (!role) return null;
  const Icon = role.icon;
  
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${colorMap[role.color]}`}>
      <Icon size={12} />
      {role.name}
    </span>
  );
};

const UserRow = ({ user, onEdit, onManageRoles }) => (
  <tr className="hover:bg-hover transition-colors">
    <td className="px-6 py-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center text-white font-bold">
          {user.name.charAt(0)}
        </div>
        <div>
          <p className="font-medium text-primary">{user.name}</p>
          <p className="text-sm text-secondary">@{user.username}</p>
        </div>
      </div>
    </td>
    <td className="px-6 py-4 text-secondary">{user.email}</td>
    <td className="px-6 py-4">
      <div className="flex flex-wrap gap-1">
        {user.roles.map(role => (
          <RoleBadge key={role} roleCode={role} />
        ))}
      </div>
    </td>
    <td className="px-6 py-4">
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
        user.status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'status-badge--neutral'
      }`}>
        {user.status === 'active' ? <CheckCircle size={12} /> : <XCircle size={12} />}
        {user.status === 'active' ? 'نشط' : 'غير نشط'}
      </span>
    </td>
    <td className="px-6 py-4 text-sm text-secondary">{user.lastLogin}</td>
    <td className="px-6 py-4">
      <div className="flex items-center gap-2">
        <button
          onClick={() => onManageRoles(user)}
          className="p-2 hover:bg-purple-50 rounded-lg text-purple-600"
          title="إدارة الصلاحيات"
        >
          <Key size={16} />
        </button>
        <button
          onClick={() => onEdit(user)}
          className="p-2 hover:bg-hover rounded-lg text-secondary"
          title="تعديل"
        >
          <Edit size={16} />
        </button>
      </div>
    </td>
  </tr>
);

const RoleAssignmentModal = ({ user, isOpen, onClose, onSave }) => {
  const [selectedRoles, setSelectedRoles] = useState(user?.roles || []);

  if (!isOpen || !user) return null;

  const toggleRole = (roleCode) => {
    if (selectedRoles.includes(roleCode)) {
      setSelectedRoles(selectedRoles.filter(r => r !== roleCode));
    } else {
      setSelectedRoles([...selectedRoles, roleCode]);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-primary rounded-2xl w-full max-w-lg overflow-hidden">
        <div className="p-6 border-b border-light">
          <h2 className="text-xl font-bold text-primary">إدارة صلاحيات المستخدم</h2>
          <p className="text-secondary mt-1">تعيين الأدوار لـ {user.name}</p>
        </div>

        <div className="p-6">
          <div className="flex items-center gap-4 mb-6 p-4 bg-secondary rounded-xl">
            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center text-white text-xl font-bold">
              {user.name.charAt(0)}
            </div>
            <div>
              <h3 className="font-bold text-primary">{user.name}</h3>
              <p className="text-sm text-secondary">{user.email}</p>
            </div>
          </div>

          <h4 className="font-semibold text-primary mb-3">اختر الأدوار:</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {availableRoles.map(role => {
              const Icon = role.icon;
              const isSelected = selectedRoles.includes(role.code);

              return (
                <button
                  key={role.code}
                  onClick={() => toggleRole(role.code)}
                  className={`w-full flex items-center gap-4 p-4 rounded-xl border-2 transition-all ${
                    isSelected
                      ? 'border-teal-500 bg-teal-50'
                      : 'border-light hover:border-default'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                    isSelected ? 'bg-teal-500 text-white' : 'bg-secondary text-secondary'
                  }`}>
                    <Icon size={20} />
                  </div>
                  <div className="flex-1 text-right">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-primary">{role.name}</span>
                      {role.isSystem && <Lock size={12} className="text-tertiary" />}
                    </div>
                    <span className="text-sm text-secondary">{role.code}</span>
                  </div>
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    isSelected ? 'border-teal-500 bg-teal-500' : 'border-default'
                  }`}>
                    {isSelected && <CheckCircle size={14} className="text-white" />}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-6 border-t border-light flex items-center justify-end gap-3">
          <Button variant="secondary" onClick={onClose}>إلغاء</Button>
          <Button variant="primary" icon={Save} onClick={() => onSave(user.id, selectedRoles)}>
            حفظ التغييرات
          </Button>
        </div>
      </div>
    </div>
  );
};

const UserRightsPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedUser, setSelectedUser] = useState(null);
  const [showRoleModal, setShowRoleModal] = useState(false);

  const handleManageRoles = (user) => {
    setSelectedUser(user);
    setShowRoleModal(true);
  };

  const handleSaveRoles = (userId, roles) => {
    console.log('Save roles for user:', userId, roles);
    setShowRoleModal(false);
    setSelectedUser(null);
  };

  const filteredUsers = sampleUsers.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.username.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = roleFilter === 'all' || user.roles.includes(roleFilter);
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    return matchesSearch && matchesRole && matchesStatus;
  });

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="page-title">إدارة صلاحيات المستخدمين</h1>
          <p className="text-secondary">تعيين الأدوار والصلاحيات للمستخدمين</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" icon={RefreshCw}>تحديث</Button>
          <Button variant="primary" icon={UserPlus}>مستخدم جديد</Button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid grid-cols-1 md:grid-cols-4">
        <div className="stats-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stats-card-title">إجمالي المستخدمين</p>
              <p className="stats-card-value">{sampleUsers.length}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Users className="text-teal-600" size={24} />
            </div>
          </div>
        </div>
        <div className="stats-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stats-card-title">المستخدمين النشطين</p>
              <p className="text-2xl font-bold text-emerald-600">
                {sampleUsers.filter(u => u.status === 'active').length}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle className="text-emerald-600" size={24} />
            </div>
          </div>
        </div>
        <div className="stats-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stats-card-title">المدراء</p>
              <p className="text-2xl font-bold text-purple-600">
                {sampleUsers.filter(u => u.roles.includes('admin') || u.roles.includes('super_admin')).length}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Shield className="text-purple-600" size={24} />
            </div>
          </div>
        </div>
        <div className="stats-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stats-card-title">الأدوار المتاحة</p>
              <p className="text-2xl font-bold text-blue-600">{availableRoles.length}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <Key className="text-blue-600" size={24} />
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="entity-card shadow-sm mb-8">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-tertiary" size={20} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="بحث بالاسم أو البريد..."
              className="w-full pr-12 pl-4 py-3 bg-secondary border-0 rounded-xl focus:ring-2 focus:ring-teal-500"
            />
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-secondary text-sm">الدور:</span>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-4 py-2 bg-secondary border border-light rounded-lg focus:ring-2 focus:ring-teal-500"
            >
              <option value="all">الكل</option>
              {availableRoles.map(role => (
                <option key={role.code} value={role.code}>{role.name}</option>
              ))}
            </select>
            <span className="text-secondary text-sm mr-4">الحالة:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 bg-secondary border border-light rounded-lg focus:ring-2 focus:ring-teal-500"
            >
              <option value="all">الكل</option>
              <option value="active">نشط</option>
              <option value="inactive">غير نشط</option>
            </select>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="entity-card overflow-hidden shadow-sm p-0">
        <table className="w-full">
          <thead className="bg-secondary border-b border-light">
            <tr>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">المستخدم</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">البريد الإلكتروني</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">الأدوار</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">الحالة</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">آخر دخول</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-secondary">إجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-light">
            {filteredUsers.map(user => (
              <UserRow
                key={user.id}
                user={user}
                onEdit={(u) => console.log('Edit:', u)}
                onManageRoles={handleManageRoles}
              />
            ))}
          </tbody>
        </table>
      </div>

      {/* Role Assignment Modal */}
      <RoleAssignmentModal
        user={selectedUser}
        isOpen={showRoleModal}
        onClose={() => { setShowRoleModal(false); setSelectedUser(null); }}
        onSave={handleSaveRoles}
      />
    </div>
  );
};

export default UserRightsPage;

