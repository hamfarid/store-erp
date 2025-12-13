/**
 * Returns Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, RotateCcw, Package, Calendar, User, DollarSign,
  CheckCircle, XCircle, Clock, AlertTriangle, Eye, Edit
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleReturns = [
  { id: 'RET-001', customer: 'أحمد محمد', product: 'آيفون 15 برو', quantity: 1, reason: 'عيب مصنعي', amount: 5499, status: 'approved', date: '2024-12-01' },
  { id: 'RET-002', customer: 'شركة الفيصل', product: 'شاحن MagSafe', quantity: 5, reason: 'منتج خاطئ', amount: 995, status: 'pending', date: '2024-11-30' },
  { id: 'RET-003', customer: 'محمد سعيد', product: 'سماعات إيربودز', quantity: 2, reason: 'لا يعمل', amount: 1998, status: 'processing', date: '2024-11-29' },
  { id: 'RET-004', customer: 'خالد العمري', product: 'كابل USB-C', quantity: 10, reason: 'تغيير رأي', amount: 500, status: 'rejected', date: '2024-11-28' },
];

const StatusBadge = ({ status }) => {
  const config = {
    approved: { label: 'موافق عليه', color: 'emerald', icon: CheckCircle },
    pending: { label: 'قيد المراجعة', color: 'amber', icon: Clock },
    processing: { label: 'قيد المعالجة', color: 'blue', icon: RotateCcw },
    rejected: { label: 'مرفوض', color: 'rose', icon: XCircle },
  };
  const { label, color, icon: Icon } = config[status];

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-${color}-100 text-${color}-700`}>
      <Icon size={12} />
      {label}
    </span>
  );
};

const ReturnsPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const totalReturns = sampleReturns.reduce((sum, r) => sum + r.amount, 0);
  const pendingCount = sampleReturns.filter(r => r.status === 'pending').length;

  const filteredReturns = sampleReturns.filter(r => {
    const matchesSearch = r.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         r.product.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || r.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">المرتجعات</h1>
          <p className="text-gray-500 mt-1">إدارة طلبات الإرجاع والاستبدال</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>طلب إرجاع جديد</Button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المرتجعات</span>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <RotateCcw className="text-purple-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleReturns.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">قيد المراجعة</span>
            <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center">
              <Clock className="text-amber-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-amber-600">{pendingCount}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">قيمة المرتجعات</span>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <DollarSign className="text-rose-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-rose-600">{totalReturns.toLocaleString()}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">الموافق عليها</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">
            {sampleReturns.filter(r => r.status === 'approved').length}
          </div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث..."
            className="form-input-standard pr-12"
          />
        </div>
        <div className="button-group">
          {['all', 'pending', 'processing', 'approved', 'rejected'].map(status => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                statusFilter === status ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {status === 'all' ? 'الكل' : status === 'pending' ? 'قيد المراجعة' : status === 'processing' ? 'قيد المعالجة' : status === 'approved' ? 'موافق عليه' : 'مرفوض'}
            </button>
          ))}
        </div>
      </div>

      <div className="table-wrapper">
        <table className="table-standard">
          <thead>
            <tr>
              <th>رقم الطلب</th>
              <th>العميل</th>
              <th>المنتج</th>
              <th>الكمية</th>
              <th>السبب</th>
              <th>المبلغ</th>
              <th>الحالة</th>
              <th>إجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredReturns.map(ret => (
              <tr key={ret.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-semibold text-teal-600">{ret.id}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <User size={14} className="text-gray-400" />
                    <span className="text-gray-900">{ret.customer}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Package size={14} className="text-gray-400" />
                    <span className="text-gray-900">{ret.product}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-900">{ret.quantity}</td>
                <td className="px-6 py-4 text-gray-600 text-sm">{ret.reason}</td>
                <td className="px-6 py-4 font-semibold text-gray-900">{ret.amount.toLocaleString()} ر.س</td>
                <td className="px-6 py-4"><StatusBadge status={ret.status} /></td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <button className="p-2 hover:bg-gray-100 rounded-lg"><Eye size={16} className="text-gray-500" /></button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg"><Edit size={16} className="text-gray-500" /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ReturnsPage;



