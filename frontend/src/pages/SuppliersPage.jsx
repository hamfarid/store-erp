/**
 * Suppliers Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, Edit, Trash2, Eye, Truck, Phone, Mail, MapPin,
  Package, DollarSign, Star, Building2, Globe
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleSuppliers = [
  { id: 1, name: 'شركة التقنية للإلكترونيات', contact: 'محمد أحمد', email: 'tech@supplier.com', phone: '0501234567', city: 'الرياض', country: 'السعودية', totalPurchases: 850000, balance: -25000, productsCount: 156, rating: 5 },
  { id: 2, name: 'مصنع الملابس الحديثة', contact: 'خالد العمري', email: 'clothes@factory.com', phone: '0512345678', city: 'جدة', country: 'السعودية', totalPurchases: 320000, balance: 0, productsCount: 89, rating: 4 },
  { id: 3, name: 'Apple Inc.', contact: 'John Smith', email: 'supplier@apple.com', phone: '+14155551234', city: 'Cupertino', country: 'USA', totalPurchases: 1500000, balance: -150000, productsCount: 45, rating: 5 },
  { id: 4, name: 'Samsung Electronics', contact: 'Kim Lee', email: 'supply@samsung.com', phone: '+82212345678', city: 'Seoul', country: 'South Korea', totalPurchases: 980000, balance: -50000, productsCount: 78, rating: 4 },
];

const SupplierCard = ({ supplier, onView, onEdit, onDelete }) => (
  <div className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-xl transition-all duration-300">
    <div className="flex items-start justify-between mb-4">
      <div className="flex items-center gap-4">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white shadow-lg">
          <Building2 size={24} />
        </div>
        <div>
          <h3 className="font-bold text-gray-900">{supplier.name}</h3>
          <p className="text-sm text-gray-500 flex items-center gap-1">
            <Globe size={12} />
            {supplier.city}، {supplier.country}
          </p>
        </div>
      </div>
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star key={i} size={14} className={i < supplier.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-200'} />
        ))}
      </div>
    </div>

    <div className="space-y-2 mb-4">
      <div className="flex items-center gap-2 text-gray-600 text-sm">
        <Mail size={14} className="text-gray-400" />
        <span>{supplier.email}</span>
      </div>
      <div className="flex items-center gap-2 text-gray-600 text-sm">
        <Phone size={14} className="text-gray-400" />
        <span dir="ltr">{supplier.phone}</span>
      </div>
    </div>

    <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-100">
      <div className="text-center">
        <p className="text-lg font-bold text-gray-900">{supplier.productsCount}</p>
        <p className="text-xs text-gray-500">المنتجات</p>
      </div>
      <div className="text-center">
        <p className="text-lg font-bold text-blue-600">{(supplier.totalPurchases / 1000).toFixed(0)}K</p>
        <p className="text-xs text-gray-500">المشتريات</p>
      </div>
      <div className="text-center">
        <p className={`text-lg font-bold ${supplier.balance < 0 ? 'text-rose-600' : 'text-gray-900'}`}>
          {Math.abs(supplier.balance).toLocaleString()}
        </p>
        <p className="text-xs text-gray-500">{supplier.balance < 0 ? 'مستحق' : 'الرصيد'}</p>
      </div>
    </div>

    <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-100">
      <button onClick={() => onView(supplier)} className="flex-1 py-2 text-center text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg">
        عرض
      </button>
      <button onClick={() => onEdit(supplier)} className="flex-1 py-2 text-center text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg">
        تعديل
      </button>
      <button onClick={() => onDelete(supplier)} className="p-2 text-rose-500 hover:bg-rose-50 rounded-lg">
        <Trash2 size={16} />
      </button>
    </div>
  </div>
);

const SuppliersPage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const totalDebt = sampleSuppliers.filter(s => s.balance < 0).reduce((sum, s) => sum + Math.abs(s.balance), 0);

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">الموردين</h1>
          <p className="text-gray-500 mt-1">إدارة الموردين وطلبات الشراء</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>مورد جديد</Button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي الموردين</span>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <Truck className="text-blue-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleSuppliers.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المنتجات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Package className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-teal-600">
            {sampleSuppliers.reduce((sum, s) => sum + s.productsCount, 0)}
          </div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المشتريات</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <DollarSign className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">
            {(sampleSuppliers.reduce((sum, s) => sum + s.totalPurchases, 0) / 1000000).toFixed(1)}M
          </div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">مستحقات للموردين</span>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <DollarSign className="text-rose-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-rose-600">{totalDebt.toLocaleString()}</div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث في الموردين..."
            className="form-input-standard pr-12"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sampleSuppliers.map(supplier => (
          <SupplierCard
            key={supplier.id}
            supplier={supplier}
            onView={(s) => console.log('View:', s)}
            onEdit={(s) => console.log('Edit:', s)}
            onDelete={(s) => console.log('Delete:', s)}
          />
        ))}
      </div>
    </div>
  );
};

export default SuppliersPage;



