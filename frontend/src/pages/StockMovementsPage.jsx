/**
 * Stock Movements Page
 */

import React, { useState } from 'react';
import {
  Search, Download, ArrowUpRight, ArrowDownRight, ArrowLeftRight,
  Package, Calendar, Filter, RefreshCw, Warehouse, User
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleMovements = [
  { id: 1, type: 'in', product: 'آيفون 15 برو', quantity: 50, warehouse: 'المستودع الرئيسي', date: '2024-12-01', user: 'أحمد محمد', reference: 'PO-2024-001', note: 'استلام من المورد' },
  { id: 2, type: 'out', product: 'سماعات إيربودز', quantity: 25, warehouse: 'مستودع جدة', date: '2024-12-01', user: 'خالد العمري', reference: 'INV-2024-089', note: 'فاتورة بيع' },
  { id: 3, type: 'transfer', product: 'شاحن MagSafe', quantity: 100, warehouse: 'الرئيسي → جدة', date: '2024-11-30', user: 'محمد سعيد', reference: 'TR-2024-015', note: 'تحويل بين المستودعات' },
  { id: 4, type: 'in', product: 'ماك بوك برو', quantity: 20, warehouse: 'المستودع الرئيسي', date: '2024-11-30', user: 'أحمد محمد', reference: 'PO-2024-002', note: 'استلام شحنة جديدة' },
  { id: 5, type: 'out', product: 'آيباد برو', quantity: 15, warehouse: 'مستودع الدمام', date: '2024-11-29', user: 'سعد الدوسري', reference: 'INV-2024-088', note: 'فاتورة بيع' },
  { id: 6, type: 'adjustment', product: 'كابل USB-C', quantity: -5, warehouse: 'المستودع الرئيسي', date: '2024-11-28', user: 'خالد العمري', reference: 'ADJ-2024-003', note: 'تالف - جرد' },
];

const MovementRow = ({ movement }) => {
  const typeConfig = {
    in: { icon: ArrowDownRight, color: 'emerald', label: 'وارد', bg: 'bg-emerald-100' },
    out: { icon: ArrowUpRight, color: 'rose', label: 'صادر', bg: 'bg-rose-100' },
    transfer: { icon: ArrowLeftRight, color: 'blue', label: 'تحويل', bg: 'bg-blue-100' },
    adjustment: { icon: RefreshCw, color: 'amber', label: 'تسوية', bg: 'bg-amber-100' },
  };
  const config = typeConfig[movement.type];
  const Icon = config.icon;

  return (
    <tr className="hover:bg-gray-50 transition-colors">
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-xl ${config.bg} flex items-center justify-center`}>
            <Icon size={18} className={`text-${config.color}-600`} />
          </div>
          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold bg-${config.color}-100 text-${config.color}-700`}>
            {config.label}
          </span>
        </div>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center">
            <Package size={18} className="text-gray-500" />
          </div>
          <span className="font-medium text-gray-900">{movement.product}</span>
        </div>
      </td>
      <td className="px-6 py-4">
        <span className={`font-semibold ${movement.quantity > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
          {movement.quantity > 0 ? '+' : ''}{movement.quantity}
        </span>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-2 text-gray-600">
          <Warehouse size={14} className="text-gray-400" />
          <span>{movement.warehouse}</span>
        </div>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-2 text-gray-600">
          <Calendar size={14} className="text-gray-400" />
          <span>{new Date(movement.date).toLocaleDateString('ar-SA')}</span>
        </div>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-2 text-gray-600">
          <User size={14} className="text-gray-400" />
          <span>{movement.user}</span>
        </div>
      </td>
      <td className="px-6 py-4">
        <span className="text-sm text-teal-600 font-medium">{movement.reference}</span>
      </td>
    </tr>
  );
};

const StockMovementsPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');

  const totalIn = sampleMovements.filter(m => m.type === 'in').reduce((sum, m) => sum + m.quantity, 0);
  const totalOut = sampleMovements.filter(m => m.type === 'out').reduce((sum, m) => sum + m.quantity, 0);

  const filteredMovements = sampleMovements.filter(m => {
    const matchesSearch = m.product.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = typeFilter === 'all' || m.type === typeFilter;
    return matchesSearch && matchesType;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-8" dir="rtl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">حركة المخزون</h1>
          <p className="text-gray-500">تتبع جميع حركات المخزون</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" icon={Download}>تصدير</Button>
          <Button variant="primary" icon={RefreshCw}>تسوية جديدة</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">إجمالي الحركات</p>
              <p className="text-2xl font-bold text-gray-900">{sampleMovements.length}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <ArrowLeftRight className="text-purple-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">إجمالي الوارد</p>
              <p className="text-2xl font-bold text-emerald-600">+{totalIn}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <ArrowDownRight className="text-emerald-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">إجمالي الصادر</p>
              <p className="text-2xl font-bold text-rose-600">-{totalOut}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <ArrowUpRight className="text-rose-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">صافي الحركة</p>
              <p className={`text-2xl font-bold ${totalIn - totalOut > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                {totalIn - totalOut > 0 ? '+' : ''}{totalIn - totalOut}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <Package className="text-blue-600" size={24} />
            </div>
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
            placeholder="بحث بالمنتج..."
            className="form-input-standard pr-12"
          />
        </div>
        <div className="button-group">
          {['all', 'in', 'out', 'transfer', 'adjustment'].map(type => (
            <button
              key={type}
              onClick={() => setTypeFilter(type)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                typeFilter === type ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {type === 'all' ? 'الكل' : type === 'in' ? 'وارد' : type === 'out' ? 'صادر' : type === 'transfer' ? 'تحويل' : 'تسوية'}
            </button>
          ))}
        </div>
      </div>

      <div className="table-wrapper">
        <table className="table-standard">
          <thead>
            <tr>
              <th>النوع</th>
              <th>المنتج</th>
              <th>الكمية</th>
              <th>المستودع</th>
              <th>التاريخ</th>
              <th>المستخدم</th>
              <th>المرجع</th>
            </tr>
          </thead>
          <tbody>
            {filteredMovements.map(movement => (
              <MovementRow key={movement.id} movement={movement} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StockMovementsPage;



