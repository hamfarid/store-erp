/**
 * Users Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, Users, Shield, Mail, Phone, Calendar, MoreVertical,
  Edit, Trash2, Key, CheckCircle, XCircle, Clock, Eye
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleUsers = [
  { id: 1, name: 'أحمد محمد', email: 'ahmed@company.com', phone: '0501234567', role: 'admin', status: 'active', lastLogin: '2024-12-01 10:30', avatar: null },
  { id: 2, name: 'سارة العلي', email: 'sara@company.com', phone: '0512345678', role: 'manager', status: 'active', lastLogin: '2024-12-01 09:15', avatar: null },
  { id: 3, name: 'محمد الخالد', email: 'mohammed@company.com', phone: '0523456789', role: 'sales', status: 'active', lastLogin: '2024-11-30 16:45', avatar: null },
  { id: 4, name: 'فاطمة العمري', email: 'fatima@company.com', phone: '0534567890', role: 'accountant', status: 'inactive', lastLogin: '2024-11-25 11:20', avatar: null },
  { id: 5, name: 'خالد السعيد', email: 'khaled@company.com', phone: '0545678901', role: 'warehouse', status: 'active', lastLogin: '2024-12-01 08:00', avatar: null },
];

const roles = {
  admin: { label: 'مدير النظام', color: 'rose' },
  manager: { label: 'مدير', color: 'purple' },
  sales: { label: 'مبيعات', color: 'blue' },
  accountant: { label: 'محاسب', color: 'emerald' },
  warehouse: { label: 'مستودعات', color: 'amber' },
};

const UserCard = ({ user, onEdit, onDelete, onView }) => (
  <div className="entity-card">
    <div className="entity-card__header">
      <div className="flex items-center gap-4">
        <div className="entity-card__avatar entity-card__avatar--success">
          {user.name.charAt(0)}
        </div>
        <div>
          <h3 className="entity-card__name">{user.name}</h3>
          <span className={`status-badge status-badge--${roles[user.role].color === 'rose' ? 'danger' : roles[user.role].color === 'purple' ? 'info' : roles[user.role].color === 'emerald' ? 'success' : roles[user.role].color === 'amber' ? 'warning' : 'primary'}`}>
            {roles[user.role].label}
          </span>
        </div>
      </div>
      <span className={`status-badge ${user.status === 'active' ? 'status-badge--success' : 'status-badge--neutral'}`}>
        {user.status === 'active' ? <CheckCircle size={12} /> : <XCircle size={12} />}
        {user.status === 'active' ? 'نشط' : 'غير نشط'}
      </span>
    </div>

    <div className="entity-card__info">
      <div className="entity-card__info-row">
        <Mail size={14} className="entity-card__info-icon" />
        <span>{user.email}</span>
      </div>
      <div className="entity-card__info-row">
        <Phone size={14} className="entity-card__info-icon" />
        <span dir="ltr">{user.phone}</span>
      </div>
      <div className="entity-card__info-row text-xs">
        <Clock size={12} className="entity-card__info-icon" />
        <span>آخر دخول: {user.lastLogin}</span>
      </div>
    </div>

    <div className="entity-card__actions">
      <button onClick={() => onView(user)} className="entity-card__action entity-card__action--primary">
        عرض
      </button>
      <button onClick={() => onEdit(user)} className="entity-card__action entity-card__action--secondary">
        تعديل
      </button>
      <button className="entity-card__action entity-card__action--secondary p-2">
        <Key size={16} />
      </button>
      <button onClick={() => onDelete(user)} className="entity-card__action entity-card__action--danger p-2">
        <Trash2 size={16} />
      </button>
    </div>
  </div>
);

const UsersPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');

  const activeUsers = sampleUsers.filter(u => u.status === 'active').length;

  const filteredUsers = sampleUsers.filter(u => {
    const matchesSearch = u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         u.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = roleFilter === 'all' || u.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">المستخدمين</h1>
          <p className="page-subtitle">إدارة المستخدمين والصلاحيات</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>مستخدم جديد</Button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المستخدمين</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Users className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleUsers.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">النشطون</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">{activeUsers}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">غير النشطين</span>
            <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
              <XCircle className="text-gray-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-gray-600">{sampleUsers.length - activeUsers}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">الأدوار</span>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Shield className="text-purple-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-purple-600">{Object.keys(roles).length}</div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث بالاسم أو البريد..."
            className="form-input-standard pr-12"
          />
        </div>
        <div className="button-group">
            <button
              onClick={() => setRoleFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${roleFilter === 'all' ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              الكل
            </button>
            {Object.entries(roles).map(([key, value]) => (
              <button
                key={key}
                onClick={() => setRoleFilter(key)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${roleFilter === key ? `bg-${value.color}-100 text-${value.color}-700` : 'text-gray-600 hover:bg-gray-100'}`}
              >
                {value.label}
              </button>
            ))}
          </div>
        </div>

      <div className="entity-grid">
        {filteredUsers.map(user => (
          <UserCard
            key={user.id}
            user={user}
            onView={(u) => console.log('View:', u)}
            onEdit={(u) => console.log('Edit:', u)}
            onDelete={(u) => console.log('Delete:', u)}
          />
        ))}
      </div>
    </div>
  );
};

export default UsersPage;

