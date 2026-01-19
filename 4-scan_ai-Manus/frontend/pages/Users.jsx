/**
 * Users Page - User Management System
 * ====================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Plus, Search, Users as UsersIcon, Shield, ShieldCheck, ShieldAlert,
  Edit, Trash2, RefreshCw, MoreVertical, Eye, Mail, Phone, Calendar,
  Lock, Unlock, UserCheck, UserX, Building, Crown, User
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Input, Select, TextArea } from '../src/components/Form';
import DataTable from '../src/components/DataTable';
import { StatCard } from '../src/components/Card';

// ============================================
// Constants
// ============================================
const ROLES = [
  { value: 'admin', label: 'Admin', labelAr: 'مدير', color: 'red', icon: Crown },
  { value: 'manager', label: 'Manager', labelAr: 'مشرف', color: 'amber', icon: ShieldCheck },
  { value: 'user', label: 'User', labelAr: 'مستخدم', color: 'blue', icon: User }
];

// ============================================
// User Form
// ============================================
const UserForm = ({ user, companies, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    role: user?.role || 'user',
    company_id: user?.company_id || '',
    is_active: user?.is_active ?? true,
    is_verified: user?.is_verified ?? false,
    ...(user ? {} : { password: '', confirm_password: '' })
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
    if (!formData.email) newErrors.email = isRTL ? 'البريد مطلوب' : 'Email is required';
    if (!user && !formData.password) newErrors.password = isRTL ? 'كلمة المرور مطلوبة' : 'Password is required';
    if (!user && formData.password !== formData.confirm_password) {
      newErrors.confirm_password = isRTL ? 'كلمات المرور غير متطابقة' : 'Passwords do not match';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      const data = { ...formData };
      delete data.confirm_password;
      onSubmit(data);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: null }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الاسم' : 'Name'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Input
          label={isRTL ? 'البريد الإلكتروني' : 'Email'}
          type="email"
          value={formData.email}
          onChange={(v) => handleChange('email', v)}
          error={errors.email}
          icon={Mail}
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الهاتف' : 'Phone'}
          value={formData.phone}
          onChange={(v) => handleChange('phone', v)}
          icon={Phone}
        />
        <Select
          label={isRTL ? 'الدور' : 'Role'}
          value={formData.role}
          onChange={(v) => handleChange('role', v)}
          options={ROLES}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label={isRTL ? 'الشركة' : 'Company'}
          value={formData.company_id}
          onChange={(v) => handleChange('company_id', v)}
          options={[
            { value: '', label: isRTL ? 'بدون شركة' : 'No Company' },
            ...companies.map(c => ({ value: c.id, label: c.name }))
          ]}
        />
        <div className="space-y-3 pt-6">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={formData.is_active}
              onChange={(e) => handleChange('is_active', e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
            />
            <span className="text-sm">{isRTL ? 'نشط' : 'Active'}</span>
          </label>
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={formData.is_verified}
              onChange={(e) => handleChange('is_verified', e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
            />
            <span className="text-sm">{isRTL ? 'موثق' : 'Verified'}</span>
          </label>
        </div>
      </div>

      {!user && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label={isRTL ? 'كلمة المرور' : 'Password'}
            type="password"
            value={formData.password}
            onChange={(v) => handleChange('password', v)}
            error={errors.password}
            icon={Lock}
            required
          />
          <Input
            label={isRTL ? 'تأكيد كلمة المرور' : 'Confirm Password'}
            type="password"
            value={formData.confirm_password}
            onChange={(v) => handleChange('confirm_password', v)}
            error={errors.confirm_password}
            icon={Lock}
            required
          />
        </div>
      )}

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {user ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// User Card
// ============================================
const UserCard = ({ user, onView, onEdit, onDelete, onToggleStatus }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  const role = ROLES.find(r => r.value === user.role);
  const RoleIcon = role?.icon || User;

  return (
    <Card hover onClick={() => onView(user)} className="relative">
      {/* Status indicator */}
      <div className={`absolute top-4 right-4 rtl:right-auto rtl:left-4 w-3 h-3 rounded-full ${user.is_active ? 'bg-emerald-500' : 'bg-gray-400'}`} />

      {/* Menu */}
      <div className="absolute top-4 left-4 rtl:left-auto rtl:right-4">
        <div className="relative">
          <button
            onClick={(e) => { e.stopPropagation(); setShowMenu(!showMenu); }}
            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <MoreVertical className="w-5 h-5 text-gray-400" />
          </button>
          {showMenu && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setShowMenu(false)} />
              <div className="absolute z-20 top-full mt-1 left-0 rtl:left-auto rtl:right-0 w-44 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button onClick={(e) => { e.stopPropagation(); onView(user); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onEdit(user); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onToggleStatus(user); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  {user.is_active ? <UserX className="w-4 h-4" /> : <UserCheck className="w-4 h-4" />}
                  {user.is_active ? (isRTL ? 'تعطيل' : 'Deactivate') : (isRTL ? 'تفعيل' : 'Activate')}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onDelete(user); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="pt-8 text-center">
        {/* Avatar */}
        <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-gradient-to-br from-emerald-100 to-teal-100 dark:from-emerald-900/40 dark:to-teal-900/40 flex items-center justify-center">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt={user.name} className="w-full h-full rounded-full object-cover" />
          ) : (
            <span className="text-2xl font-bold text-emerald-600">{user.name.charAt(0).toUpperCase()}</span>
          )}
        </div>

        <h3 className="text-lg font-semibold text-gray-800 dark:text-white">{user.name}</h3>
        <p className="text-sm text-gray-500 mb-3">{user.email}</p>

        <Badge variant={role?.color} className="mb-4">
          <RoleIcon className="w-3 h-3 mr-1" />
          {isRTL ? role?.labelAr : role?.label}
        </Badge>

        <div className="pt-3 border-t flex justify-around text-xs">
          <div>
            <span className="text-gray-500">{isRTL ? 'المزارع' : 'Farms'}</span>
            <p className="font-semibold text-gray-800 dark:text-white">{user.farm_count || 0}</p>
          </div>
          <div>
            <span className="text-gray-500">{isRTL ? 'التشخيصات' : 'Diagnoses'}</span>
            <p className="font-semibold text-gray-800 dark:text-white">{user.diagnosis_count || 0}</p>
          </div>
        </div>

        {/* Badges */}
        <div className="flex justify-center gap-2 mt-3">
          {user.is_verified && (
            <span className="text-xs px-2 py-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-full flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" />
              {isRTL ? 'موثق' : 'Verified'}
            </span>
          )}
          {!user.is_active && (
            <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-500 rounded-full">
              {isRTL ? 'معطل' : 'Inactive'}
            </span>
          )}
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Main Users Page
// ============================================
const Users = () => {
  const isRTL = document.documentElement.dir === 'rtl';

  const [users, setUsers] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0, totalPages: 0 });

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, admins: 0, active: 0, verified: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [usersRes, companiesRes] = await Promise.all([
        ApiService.getUsers({ page: pagination.page, limit: pagination.limit, search: searchQuery, role: roleFilter }),
        ApiService.getCompanies({ limit: 100 })
      ]);

      const items = usersRes.items || usersRes;
      setUsers(items);
      setCompanies(companiesRes.items || companiesRes);
      setPagination(prev => ({
        ...prev,
        total: usersRes.total || items.length,
        totalPages: usersRes.total_pages || Math.ceil((usersRes.total || items.length) / prev.limit)
      }));

      setStats({
        total: items.length,
        admins: items.filter(u => u.role === 'admin').length,
        active: items.filter(u => u.is_active).length,
        verified: items.filter(u => u.is_verified).length
      });
    } catch (err) {
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, roleFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try { setFormLoading(true); await ApiService.createUser(data); setShowCreateModal(false); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try { setFormLoading(true); await ApiService.updateUser(selectedUser.id, data); setShowEditModal(false); setSelectedUser(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try { setFormLoading(true); await ApiService.deleteUser(selectedUser.id); setShowDeleteModal(false); setSelectedUser(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleToggleStatus = async (user) => {
    try {
      await ApiService.updateUser(user.id, { is_active: !user.is_active });
      loadData();
    } catch (err) {
      console.error('Error toggling user status:', err);
    }
  };

  const handleView = (user) => { setSelectedUser(user); setShowEditModal(true); };
  const handleEdit = (user) => { setSelectedUser(user); setShowEditModal(true); };
  const handleDeleteClick = (user) => { setSelectedUser(user); setShowDeleteModal(true); };

  const columns = [
    { key: 'name', label: 'Name', labelAr: 'الاسم', sortable: true },
    { key: 'email', label: 'Email', labelAr: 'البريد' },
    { key: 'role', label: 'Role', labelAr: 'الدور', render: (v) => {
      const r = ROLES.find(r => r.value === v);
      return <Badge variant={r?.color}>{isRTL ? r?.labelAr : r?.label}</Badge>;
    }},
    { key: 'company_name', label: 'Company', labelAr: 'الشركة' },
    { key: 'is_active', label: 'Status', labelAr: 'الحالة', render: (v) => (
      <Badge variant={v ? 'emerald' : 'gray'}>{v ? (isRTL ? 'نشط' : 'Active') : (isRTL ? 'معطل' : 'Inactive')}</Badge>
    )},
    { key: 'created_at', label: 'Joined', labelAr: 'الانضمام', render: (v) => new Date(v).toLocaleDateString() }
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'المستخدمون' : 'Users'}
        description={isRTL ? 'إدارة المستخدمين والصلاحيات' : 'Manage users and permissions'}
        icon={UsersIcon}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'مستخدم جديد' : 'New User'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي المستخدمين' : 'Total Users'} value={stats.total} icon={UsersIcon} iconColor="blue" />
        <StatCard title={isRTL ? 'المدراء' : 'Admins'} value={stats.admins} icon={Crown} iconColor="red" />
        <StatCard title={isRTL ? 'النشطون' : 'Active'} value={stats.active} icon={UserCheck} iconColor="emerald" />
        <StatCard title={isRTL ? 'الموثقون' : 'Verified'} value={stats.verified} icon={ShieldCheck} iconColor="purple" />
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3 flex-1">
            <div className="relative flex-1 max-w-xs">
              <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={isRTL ? 'بحث...' : 'Search...'}
                className="w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm"
              />
            </div>
            <Select value={roleFilter} onChange={setRoleFilter} className="w-40"
              options={[{ value: '', label: isRTL ? 'كل الأدوار' : 'All Roles' }, ...ROLES]}
            />
          </div>
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-56" />)}
        </div>
      ) : users.length === 0 ? (
        <Card className="p-12 text-center">
          <UsersIcon className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا يوجد مستخدمون' : 'No Users'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {users.map(user => <UserCard key={user.id} user={user} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} onToggleStatus={handleToggleStatus} />)}
        </div>
      )}

      {/* Modals */}
      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة مستخدم' : 'Add User'} size="xl">
        <UserForm companies={companies} onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedUser(null); }} title={isRTL ? 'تعديل المستخدم' : 'Edit User'} size="xl">
        <UserForm user={selectedUser} companies={companies} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedUser(null); }} loading={formLoading} />
      </Modal>

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedUser(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف المستخدم' : 'Delete User'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedUser?.name}"؟` : `Delete "${selectedUser?.name}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedUser(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Users;
