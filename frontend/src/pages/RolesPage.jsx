/**
 * Roles & Permissions Management Page
 */

import React, { useState } from 'react';
import {
  Shield, Users, Key, Plus, Edit, Trash2, Eye, Search,
  CheckCircle, XCircle, Lock, Crown, Briefcase, ShoppingCart,
  Calculator, Warehouse, ChevronDown, ChevronUp, Save
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

// Sample roles data
const sampleRoles = [
  {
    id: 1,
    code: 'super_admin',
    name: 'مدير النظام',
    description: 'وصول كامل لجميع ميزات النظام',
    color: 'rose',
    icon: 'crown',
    isSystem: true,
    usersCount: 2,
    permissions: ['*']
  },
  {
    id: 2,
    code: 'admin',
    name: 'مدير',
    description: 'وصول إداري مع بعض القيود',
    color: 'purple',
    icon: 'shield',
    isSystem: true,
    usersCount: 3,
    permissions: ['dashboard.*', 'products.*', 'invoices.*']
  },
  {
    id: 3,
    code: 'manager',
    name: 'مدير فرع',
    description: 'مدير فرع مع وصول تشغيلي',
    color: 'blue',
    icon: 'briefcase',
    isSystem: false,
    usersCount: 5,
    permissions: ['dashboard.view', 'products.*', 'invoices.*']
  },
  {
    id: 4,
    code: 'sales',
    name: 'مبيعات',
    description: 'موظف مبيعات مع وصول محدود',
    color: 'teal',
    icon: 'shopping-cart',
    isSystem: false,
    usersCount: 8,
    permissions: ['dashboard.view', 'products.view', 'invoices.create']
  },
  {
    id: 5,
    code: 'accountant',
    name: 'محاسب',
    description: 'وصول مالي ومحاسبي',
    color: 'emerald',
    icon: 'calculator',
    isSystem: false,
    usersCount: 3,
    permissions: ['dashboard.view', 'invoices.*', 'reports.*']
  },
  {
    id: 6,
    code: 'warehouse',
    name: 'أمين مستودع',
    description: 'إدارة المستودع والمخزون',
    color: 'amber',
    icon: 'warehouse',
    isSystem: false,
    usersCount: 4,
    permissions: ['dashboard.view', 'products.view', 'inventory.*']
  },
];

// Permission modules
const permissionModules = [
  {
    id: 'dashboard',
    name: 'لوحة التحكم',
    permissions: [
      { code: 'dashboard.view', name: 'عرض لوحة التحكم' },
      { code: 'dashboard.widgets', name: 'إدارة الودجات' },
    ]
  },
  {
    id: 'products',
    name: 'المنتجات',
    permissions: [
      { code: 'products.view', name: 'عرض المنتجات' },
      { code: 'products.create', name: 'إنشاء المنتجات' },
      { code: 'products.edit', name: 'تعديل المنتجات' },
      { code: 'products.delete', name: 'حذف المنتجات' },
    ]
  },
  {
    id: 'inventory',
    name: 'المخزون',
    permissions: [
      { code: 'inventory.view', name: 'عرض المخزون' },
      { code: 'inventory.adjust', name: 'تعديل المخزون' },
      { code: 'inventory.transfer', name: 'تحويل المخزون' },
    ]
  },
  {
    id: 'invoices',
    name: 'الفواتير',
    permissions: [
      { code: 'invoices.view', name: 'عرض الفواتير' },
      { code: 'invoices.create', name: 'إنشاء الفواتير' },
      { code: 'invoices.edit', name: 'تعديل الفواتير' },
      { code: 'invoices.delete', name: 'حذف الفواتير' },
    ]
  },
  {
    id: 'customers',
    name: 'العملاء',
    permissions: [
      { code: 'customers.view', name: 'عرض العملاء' },
      { code: 'customers.create', name: 'إنشاء العملاء' },
      { code: 'customers.edit', name: 'تعديل العملاء' },
      { code: 'customers.delete', name: 'حذف العملاء' },
    ]
  },
  {
    id: 'reports',
    name: 'التقارير',
    permissions: [
      { code: 'reports.view', name: 'عرض التقارير' },
      { code: 'reports.export', name: 'تصدير التقارير' },
      { code: 'reports.financial', name: 'التقارير المالية' },
    ]
  },
  {
    id: 'users',
    name: 'المستخدمين',
    permissions: [
      { code: 'users.view', name: 'عرض المستخدمين' },
      { code: 'users.create', name: 'إنشاء المستخدمين' },
      { code: 'users.edit', name: 'تعديل المستخدمين' },
      { code: 'users.delete', name: 'حذف المستخدمين' },
    ]
  },
  {
    id: 'settings',
    name: 'الإعدادات',
    permissions: [
      { code: 'settings.view', name: 'عرض الإعدادات' },
      { code: 'settings.edit', name: 'تعديل الإعدادات' },
    ]
  },
];

const iconMap = {
  crown: Crown,
  shield: Shield,
  briefcase: Briefcase,
  'shopping-cart': ShoppingCart,
  calculator: Calculator,
  warehouse: Warehouse,
};

const colorMap = {
  rose: 'from-rose-500 to-rose-600',
  purple: 'from-purple-500 to-purple-600',
  blue: 'from-blue-500 to-blue-600',
  teal: 'from-teal-500 to-teal-600',
  emerald: 'from-emerald-500 to-emerald-600',
  amber: 'from-amber-500 to-amber-600',
};

const RoleCard = ({ role, onEdit, onDelete, onView }) => {
  const Icon = iconMap[role.icon] || Shield;
  const gradient = colorMap[role.color] || colorMap.blue;

  return (
    <div className="entity-card group">
      <div className="entity-card__header">
        <div className="flex items-center gap-4">
          <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white shadow-lg`}>
            <Icon size={24} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="entity-card__name">{role.name}</h3>
              {role.isSystem && (
                <Lock size={14} className="text-tertiary" />
              )}
            </div>
            <p className="entity-card__meta">{role.code}</p>
          </div>
        </div>
        <span className="status-badge status-badge--neutral">
          {role.usersCount} مستخدم
        </span>
      </div>

      <p className="text-secondary text-sm mb-4">{role.description}</p>

      <div className="entity-card__actions">
        <button
          onClick={() => onView(role)}
          className="entity-card__action entity-card__action--primary"
        >
          <Eye size={16} className="inline ml-1" />
          عرض
        </button>
        {!role.isSystem && (
          <>
            <button
              onClick={() => onEdit(role)}
              className="entity-card__action entity-card__action--secondary"
            >
              <Edit size={16} className="inline ml-1" />
              تعديل
            </button>
            <button
              onClick={() => onDelete(role)}
              className="entity-card__action entity-card__action--danger p-2"
            >
              <Trash2 size={16} />
            </button>
          </>
        )}
      </div>
    </div>
  );
};

const PermissionModule = ({ module, selectedPermissions, onToggle, expanded, onExpand }) => {
  const allSelected = module.permissions.every(p => selectedPermissions.includes(p.code));
  const someSelected = module.permissions.some(p => selectedPermissions.includes(p.code));

  return (
    <div className="border border-gray-100 rounded-xl overflow-hidden">
      <button
        onClick={() => onExpand(module.id)}
        className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
      >
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={allSelected}
            ref={el => el && (el.indeterminate = someSelected && !allSelected)}
            onChange={() => {
              // const newPerms = allSelected // Currently unused
              //   ? selectedPermissions.filter(p => !module.permissions.some(mp => mp.code === p))
              //   : [...selectedPermissions, ...module.permissions.map(p => p.code)];
              module.permissions.forEach(p => onToggle(p.code, !allSelected));
            }}
            className="w-5 h-5 rounded border-gray-300 text-teal-600 focus:ring-teal-500"
          />
          <span className="font-semibold text-gray-900">{module.name}</span>
          <span className="text-sm text-gray-500">
            ({module.permissions.filter(p => selectedPermissions.includes(p.code)).length}/{module.permissions.length})
          </span>
        </div>
        {expanded ? <ChevronUp size={20} className="text-gray-400" /> : <ChevronDown size={20} className="text-gray-400" />}
      </button>
      
      {expanded && (
        <div className="p-4 space-y-3">
          {module.permissions.map(perm => (
            <label key={perm.code} className="flex items-center gap-3 cursor-pointer hover:bg-gray-50 p-2 rounded-lg">
              <input
                type="checkbox"
                checked={selectedPermissions.includes(perm.code)}
                onChange={() => onToggle(perm.code, !selectedPermissions.includes(perm.code))}
                className="w-4 h-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500"
              />
              <span className="text-gray-700">{perm.name}</span>
              <span className="text-xs text-gray-400">{perm.code}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
};

const RolesPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingRole, setEditingRole] = useState(null);
  const [expandedModules, setExpandedModules] = useState(['dashboard']);
  const [selectedPermissions, setSelectedPermissions] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    color: 'blue',
    icon: 'shield'
  });

  const handleTogglePermission = (code, add) => {
    if (add) {
      setSelectedPermissions([...selectedPermissions, code]);
    } else {
      setSelectedPermissions(selectedPermissions.filter(p => p !== code));
    }
  };

  const handleExpandModule = (moduleId) => {
    setExpandedModules(
      expandedModules.includes(moduleId)
        ? expandedModules.filter(m => m !== moduleId)
        : [...expandedModules, moduleId]
    );
  };

  const filteredRoles = sampleRoles.filter(role =>
    role.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    role.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">الأدوار والصلاحيات</h1>
          <p className="page-subtitle">إدارة أدوار المستخدمين وصلاحياتهم</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus} onClick={() => setShowModal(true)}>
            إضافة دور
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي الأدوار</span>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Shield className="text-purple-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleRoles.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">أدوار نظامية</span>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <Lock className="text-rose-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-rose-600">
            {sampleRoles.filter(r => r.isSystem).length}
          </div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي الصلاحيات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Key className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-teal-600">
            {permissionModules.reduce((sum, m) => sum + m.permissions.length, 0)}
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث في الأدوار..."
            className="form-input-standard pr-12"
          />
        </div>
      </div>

      {/* Roles Grid */}
      <div className="entity-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))' }}>
        {filteredRoles.map(role => (
          <RoleCard
            key={role.id}
            role={role}
            onView={(r) => console.log('View:', r)}
            onEdit={(r) => {
              setEditingRole(r);
              setFormData({
                name: r.name,
                code: r.code,
                description: r.description,
                color: r.color,
                icon: r.icon
              });
              setShowModal(true);
            }}
            onDelete={(r) => console.log('Delete:', r)}
          />
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-xl font-bold text-gray-900">
                {editingRole ? 'تعديل الدور' : 'إضافة دور جديد'}
              </h2>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">اسم الدور</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    placeholder="مثال: مدير المبيعات"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">الرمز</label>
                  <input
                    type="text"
                    value={formData.code}
                    onChange={(e) => setFormData({...formData, code: e.target.value})}
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    placeholder="مثال: sales_manager"
                  />
                </div>
              </div>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">الوصف</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={2}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                  placeholder="وصف مختصر للدور..."
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">الصلاحيات</label>
                <div className="space-y-3">
                  {permissionModules.map(module => (
                    <PermissionModule
                      key={module.id}
                      module={module}
                      selectedPermissions={selectedPermissions}
                      onToggle={handleTogglePermission}
                      expanded={expandedModules.includes(module.id)}
                      onExpand={handleExpandModule}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-gray-100 flex items-center justify-end gap-3">
              <Button variant="secondary" onClick={() => { setShowModal(false); setEditingRole(null); }}>
                إلغاء
              </Button>
              <Button variant="primary" icon={Save}>
                {editingRole ? 'حفظ التغييرات' : 'إنشاء الدور'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RolesPage;

