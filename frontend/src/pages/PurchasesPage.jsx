/**
 * Purchases Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, FileText, Truck, Calendar, DollarSign,
  CheckCircle, Clock, XCircle, AlertCircle, Eye, Edit, Trash2
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const samplePurchases = [
  { id: 'PO-2024-001', supplier: 'شركة التقنية', items: 25, total: 125000, paid: 125000, status: 'completed', date: '2024-12-01', dueDate: '2024-12-15' },
  { id: 'PO-2024-002', supplier: 'Apple Inc.', items: 50, total: 450000, paid: 200000, status: 'partial', date: '2024-11-28', dueDate: '2024-12-28' },
  { id: 'PO-2024-003', supplier: 'Samsung Electronics', items: 30, total: 180000, paid: 0, status: 'pending', date: '2024-11-25', dueDate: '2024-12-25' },
  { id: 'PO-2024-004', supplier: 'مصنع الملابس', items: 100, total: 85000, paid: 85000, status: 'completed', date: '2024-11-20', dueDate: '2024-12-05' },
  { id: 'PO-2024-005', supplier: 'شركة التقنية', items: 15, total: 45000, paid: 0, status: 'cancelled', date: '2024-11-15', dueDate: '2024-12-01' },
];

const StatusBadge = ({ status }) => {
  const config = {
    completed: { label: 'مكتمل', color: 'emerald', icon: CheckCircle },
    partial: { label: 'مدفوع جزئياً', color: 'amber', icon: Clock },
    pending: { label: 'قيد الانتظار', color: 'blue', icon: Clock },
    cancelled: { label: 'ملغي', color: 'rose', icon: XCircle },
  };
  const { label, color, icon: Icon } = config[status];

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-${color}-100 text-${color}-700`}>
      <Icon size={12} />
      {label}
    </span>
  );
};

const PurchasesPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const totalPurchases = samplePurchases.reduce((sum, p) => sum + p.total, 0);
  const totalPaid = samplePurchases.reduce((sum, p) => sum + p.paid, 0);
  const pendingPayment = totalPurchases - totalPaid;

  const filteredPurchases = samplePurchases.filter(p => {
    const matchesSearch = p.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         p.supplier.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || p.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">فواتير الشراء</h1>
          <p className="text-gray-500 mt-1">إدارة طلبات الشراء من الموردين</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>طلب شراء جديد</Button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">طلبات الشراء</span>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <FileText className="text-blue-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{samplePurchases.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المشتريات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <DollarSign className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-teal-600">{(totalPurchases / 1000).toFixed(0)}K</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">المدفوع</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <CheckCircle className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">{(totalPaid / 1000).toFixed(0)}K</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">المستحق</span>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <AlertCircle className="text-rose-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-rose-600">{(pendingPayment / 1000).toFixed(0)}K</div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث برقم الطلب أو المورد..."
            className="form-input-standard pr-12"
          />
        </div>
        <div className="button-group">
          {['all', 'pending', 'partial', 'completed', 'cancelled'].map(status => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                statusFilter === status ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {status === 'all' ? 'الكل' : status === 'pending' ? 'قيد الانتظار' : status === 'partial' ? 'مدفوع جزئياً' : status === 'completed' ? 'مكتمل' : 'ملغي'}
            </button>
          ))}
        </div>
      </div>

      <div className="table-wrapper">
        <table className="table-standard">
          <thead>
            <tr>
              <th>رقم الطلب</th>
              <th>المورد</th>
              <th>المنتجات</th>
              <th>الإجمالي</th>
              <th>المدفوع</th>
              <th>التاريخ</th>
              <th>الحالة</th>
              <th>إجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredPurchases.map(purchase => (
              <tr key={purchase.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-semibold text-blue-600">{purchase.id}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Truck size={14} className="text-gray-400" />
                    <span className="text-gray-900">{purchase.supplier}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-900">{purchase.items} منتج</td>
                <td className="px-6 py-4 font-semibold text-gray-900">{purchase.total.toLocaleString()} ر.س</td>
                <td className="px-6 py-4">
                  <span className={purchase.paid === purchase.total ? 'text-emerald-600' : 'text-amber-600'}>
                    {purchase.paid.toLocaleString()} ر.س
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Calendar size={14} className="text-gray-400" />
                    <span>{new Date(purchase.date).toLocaleDateString('ar-SA')}</span>
                  </div>
                </td>
                <td className="px-6 py-4"><StatusBadge status={purchase.status} /></td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <button className="p-2 hover:bg-gray-100 rounded-lg"><Eye size={16} className="text-gray-500" /></button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg"><Edit size={16} className="text-gray-500" /></button>
                    <button className="p-2 hover:bg-rose-50 rounded-lg"><Trash2 size={16} className="text-rose-500" /></button>
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

export default PurchasesPage;



