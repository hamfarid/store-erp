/**
 * Admin Dashboard Page
 * 
 * Central hub for system administration with statistics and quick actions.
 */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Shield, Users, Key, Settings, Activity, Database,
  Clock, AlertTriangle, CheckCircle, XCircle, TrendingUp,
  Eye, Edit, Trash2, Plus, RefreshCw, Download, Lock, Unlock
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

// Sample data - In production, fetch from API
const sampleStats = {
  users: { total: 25, active: 22, inactive: 3 },
  roles: { total: 7, system: 3, custom: 4 },
  permissions: { total: 65, modules: 12 },
  auditLogs: { total: 1250, today: 48 }
};

const sampleAuditLogs = [
  { id: 1, user: 'أحمد محمد', action: 'تسجيل دخول', resource: 'النظام', time: '10:30', status: 'success' },
  { id: 2, user: 'سارة العلي', action: 'إضافة منتج', resource: 'المنتجات', time: '10:25', status: 'success' },
  { id: 3, user: 'محمد خالد', action: 'تعديل فاتورة', resource: 'الفواتير', time: '10:20', status: 'success' },
  { id: 4, user: 'فاطمة أحمد', action: 'محاولة حذف', resource: 'المستخدمين', time: '10:15', status: 'failed' },
  { id: 5, user: 'خالد السعيد', action: 'تصدير تقرير', resource: 'التقارير', time: '10:10', status: 'success' },
];

const sampleActiveUsers = [
  { id: 1, name: 'أحمد محمد', role: 'مدير النظام', status: 'online', lastActivity: 'الآن' },
  { id: 2, name: 'سارة العلي', role: 'مدير', status: 'online', lastActivity: 'منذ 2 دقيقة' },
  { id: 3, name: 'محمد خالد', role: 'مبيعات', status: 'away', lastActivity: 'منذ 15 دقيقة' },
  { id: 4, name: 'فاطمة أحمد', role: 'محاسب', status: 'online', lastActivity: 'منذ 5 دقائق' },
];

const StatCard = ({ title, value, subtitle, icon: IconComponent, color, trend }) => (
  <div className="stats-card">
    <div className="stats-card-header">
      <div>
        <p className="stats-card-title">{title}</p>
        <p className="stats-card-value">{value}</p>
        {subtitle && <p className="text-secondary text-sm mt-1">{subtitle}</p>}
      </div>
      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center shadow-lg`}>
        <IconComponent className="text-white" size={24} />
      </div>
    </div>
    {trend && (
      <div className="flex items-center gap-1 mt-4 pt-4 border-t border-light">
        <TrendingUp size={14} className="text-emerald-500" />
        <span className="text-sm text-emerald-600 font-medium">{trend}</span>
      </div>
    )}
  </div>
);

const QuickAction = ({ title, description, icon: IconComponent, color, onClick }) => (
  <button
    onClick={onClick}
    className="entity-card text-right w-full group"
  >
    <div className="flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl ${color} flex items-center justify-center group-hover:scale-110 transition-transform`}>
        <IconComponent className="text-white" size={20} />
      </div>
      <div>
        <h4 className="entity-card__name">{title}</h4>
        <p className="text-secondary text-sm">{description}</p>
      </div>
    </div>
  </button>
);

const AdminDashboard = () => {
  const [stats] = useState(sampleStats);
  const [auditLogs] = useState(sampleAuditLogs);
  const [activeUsers] = useState(sampleActiveUsers);

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">لوحة تحكم المدير</h1>
          <p className="page-subtitle">إدارة النظام والمستخدمين والصلاحيات</p>
        </div>
        <div className="page-actions">
          <Button variant="secondary" icon={RefreshCw}>تحديث</Button>
          <Button variant="primary" icon={Settings}>الإعدادات</Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid mb-8">
        <StatCard
          title="المستخدمين"
          value={stats.users.total}
          subtitle={`${stats.users.active} نشط`}
          icon={Users}
          color="from-teal-500 to-teal-600"
          trend="+3 هذا الأسبوع"
        />
        <StatCard
          title="الأدوار"
          value={stats.roles.total}
          subtitle={`${stats.roles.system} نظامي`}
          icon={Shield}
          color="from-purple-500 to-purple-600"
        />
        <StatCard
          title="الصلاحيات"
          value={stats.permissions.total}
          subtitle={`${stats.permissions.modules} وحدة`}
          icon={Key}
          color="from-blue-500 to-blue-600"
        />
        <StatCard
          title="سجلات اليوم"
          value={stats.auditLogs.today}
          subtitle={`من ${stats.auditLogs.total} إجمالي`}
          icon={Activity}
          color="from-amber-500 to-amber-600"
        />
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-primary mb-4">إجراءات سريعة</h2>
        <div className="stats-grid">
          <Link to="/admin/users/new">
            <QuickAction
              title="إضافة مستخدم"
              description="إنشاء حساب جديد"
              icon={Plus}
              color="bg-teal-500"
            />
          </Link>
          <Link to="/admin/roles">
            <QuickAction
              title="إدارة الأدوار"
              description="تعديل الصلاحيات"
              icon={Shield}
              color="bg-purple-500"
            />
          </Link>
          <Link to="/admin/backup">
            <QuickAction
              title="نسخ احتياطي"
              description="حفظ البيانات"
              icon={Database}
              color="bg-blue-500"
            />
          </Link>
          <Link to="/admin/audit">
            <QuickAction
              title="سجل النشاط"
              description="مراجعة العمليات"
              icon={Activity}
              color="bg-amber-500"
            />
          </Link>
        </div>
      </div>

      <div className="grid-container grid-2">
        {/* Recent Audit Logs */}
        <div className="entity-card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="entity-card__name text-lg">آخر النشاطات</h2>
            <Link to="/admin/audit" className="text-teal-600 text-sm font-medium hover:underline">
              عرض الكل
            </Link>
          </div>
          <div className="space-y-4">
            {auditLogs.map(log => (
              <div key={log.id} className="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  log.status === 'success' ? 'bg-emerald-100' : 'bg-rose-100'
                }`}>
                  {log.status === 'success' ? (
                    <CheckCircle size={18} className="text-emerald-600" />
                  ) : (
                    <XCircle size={18} className="text-rose-600" />
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-primary font-medium">{log.user}</p>
                  <p className="text-secondary text-sm">{log.action} - {log.resource}</p>
                </div>
                <div className="text-left">
                  <p className="text-tertiary text-sm">{log.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Active Users */}
        <div className="entity-card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="entity-card__name text-lg">المستخدمين النشطين</h2>
            <span className="status-badge--success">
              {activeUsers.filter(u => u.status === 'online').length} متصل
            </span>
          </div>
          <div className="space-y-4">
            {activeUsers.map(user => (
              <div key={user.id} className="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors">
                <div className="relative">
                  <div className="entity-card__avatar entity-card__avatar--primary">
                    {user.name.charAt(0)}
                  </div>
                  <span className={`absolute -bottom-1 -left-1 w-4 h-4 rounded-full border-2 border-white ${
                    user.status === 'online' ? 'bg-emerald-500' : 'bg-amber-500'
                  }`} />
                </div>
                <div className="flex-1">
                  <p className="text-primary font-medium">{user.name}</p>
                  <p className="text-secondary text-sm">{user.role}</p>
                </div>
                <div className="text-left">
                  <p className="text-tertiary text-xs">{user.lastActivity}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="mt-8 entity-card">
        <h2 className="entity-card__name text-lg mb-6">حالة النظام</h2>
        <div className="stats-grid">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle size={24} className="text-emerald-600" />
            </div>
            <div>
              <p className="text-primary font-medium">قاعدة البيانات</p>
              <p className="text-sm text-emerald-600">متصل</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle size={24} className="text-emerald-600" />
            </div>
            <div>
              <p className="text-primary font-medium">Redis Cache</p>
              <p className="text-sm text-emerald-600">متصل</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle size={24} className="text-emerald-600" />
            </div>
            <div>
              <p className="text-primary font-medium">خادم البريد</p>
              <p className="text-sm text-emerald-600">متصل</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center">
              <AlertTriangle size={24} className="text-amber-600" />
            </div>
            <div>
              <p className="text-primary font-medium">التخزين</p>
              <p className="text-sm text-amber-600">78% مستخدم</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

