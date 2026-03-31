/**
 * Customers Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, Edit, Trash2, Eye, Users, Phone, Mail, MapPin,
  DollarSign, ShoppingCart, Star, MoreVertical, Download, Filter
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleCustomers = [
  { id: 1, name: 'أحمد محمد العلي', email: 'ahmed@example.com', phone: '0501234567', city: 'الرياض', totalPurchases: 45000, balance: 0, ordersCount: 23, rating: 5 },
  { id: 2, name: 'شركة الفيصل التجارية', email: 'info@faisal.com', phone: '0512345678', city: 'جدة', totalPurchases: 250000, balance: -15000, ordersCount: 89, rating: 4 },
  { id: 3, name: 'محمد سعيد الغامدي', email: 'mohammed@example.com', phone: '0523456789', city: 'الدمام', totalPurchases: 18500, balance: 2500, ordersCount: 12, rating: 5 },
  { id: 4, name: 'مؤسسة النور', email: 'noor@company.com', phone: '0534567890', city: 'مكة', totalPurchases: 120000, balance: 0, ordersCount: 45, rating: 4 },
  { id: 5, name: 'خالد عبدالله', email: 'khaled@example.com', phone: '0545678901', city: 'المدينة', totalPurchases: 8900, balance: -3500, ordersCount: 8, rating: 3 },
];

const CustomerCard = ({ customer, onView, onEdit, onDelete }) => (
  <div className="entity-card group">
    <div className="entity-card__header">
      <div className="flex items-center gap-4">
        <div className="entity-card__avatar entity-card__avatar--secondary">
          {customer.name.charAt(0)}
        </div>
        <div>
          <h3 className="entity-card__name">{customer.name}</h3>
          <p className="entity-card__meta">
            <MapPin size={12} />
            {customer.city}
          </p>
        </div>
      </div>
      <div className="rating-stars">
        {[...Array(5)].map((_, i) => (
          <Star key={i} size={14} className={i < customer.rating ? 'rating-star--filled' : 'rating-star--empty'} />
        ))}
      </div>
    </div>

    <div className="entity-card__info">
      <div className="entity-card__info-row">
        <Mail size={14} className="entity-card__info-icon" />
        <span>{customer.email}</span>
      </div>
      <div className="entity-card__info-row">
        <Phone size={14} className="entity-card__info-icon" />
        <span dir="ltr">{customer.phone}</span>
      </div>
    </div>

    <div className="entity-card__stats">
      <div className="entity-card__stat">
        <p className="entity-card__stat-value">{customer.ordersCount}</p>
        <p className="entity-card__stat-label">الطلبات</p>
      </div>
      <div className="entity-card__stat">
        <p className="entity-card__stat-value entity-card__stat-value--primary">{(customer.totalPurchases / 1000).toFixed(0)}K</p>
        <p className="entity-card__stat-label">المشتريات</p>
      </div>
      <div className="entity-card__stat">
        <p className={`entity-card__stat-value ${customer.balance < 0 ? 'entity-card__stat-value--danger' : customer.balance > 0 ? 'entity-card__stat-value--success' : ''}`}>
          {customer.balance.toLocaleString()}
        </p>
        <p className="entity-card__stat-label">الرصيد</p>
      </div>
    </div>

    <div className="entity-card__actions">
      <button onClick={() => onView(customer)} className="entity-card__action entity-card__action--primary">
        عرض
      </button>
      <button onClick={() => onEdit(customer)} className="entity-card__action entity-card__action--secondary">
        تعديل
      </button>
      <button onClick={() => onDelete(customer)} className="entity-card__action entity-card__action--danger">
        <Trash2 size={16} />
      </button>
    </div>
  </div>
);

const CustomersPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('all');

  const totalDebt = sampleCustomers.filter(c => c.balance < 0).reduce((sum, c) => sum + Math.abs(c.balance), 0);
  const totalCredit = sampleCustomers.filter(c => c.balance > 0).reduce((sum, c) => sum + c.balance, 0);

  const filteredCustomers = sampleCustomers.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         c.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filter === 'all' || 
                         (filter === 'debt' && c.balance < 0) ||
                         (filter === 'credit' && c.balance > 0);
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">العملاء</h1>
          <p className="page-subtitle">إدارة قاعدة بيانات العملاء</p>
        </div>
        <div className="page-actions">
          <Button variant="secondary" icon={Download}>تصدير</Button>
          <Button variant="primary" icon={Plus}>عميل جديد</Button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي العملاء</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Users className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleCustomers.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المبيعات</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <ShoppingCart className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">
            {sampleCustomers.reduce((sum, c) => sum + c.totalPurchases, 0).toLocaleString()}
          </div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">ديون العملاء</span>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <DollarSign className="text-rose-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-rose-600">{totalDebt.toLocaleString()}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">أرصدة دائنة</span>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <DollarSign className="text-blue-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-blue-600">{totalCredit.toLocaleString()}</div>
        </div>
      </div>

      {/* Filters */}
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
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              الكل
            </button>
            <button
              onClick={() => setFilter('debt')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'debt' ? 'bg-rose-100 text-rose-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              عليهم ديون
            </button>
            <button
              onClick={() => setFilter('credit')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'credit' ? 'bg-emerald-100 text-emerald-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              لهم رصيد
            </button>
          </div>
        </div>

      {/* Customers Grid */}
      <div className="entity-grid">
        {filteredCustomers.map(customer => (
          <CustomerCard
            key={customer.id}
            customer={customer}
            onView={(c) => console.log('View:', c)}
            onEdit={(c) => console.log('Edit:', c)}
            onDelete={(c) => console.log('Delete:', c)}
          />
        ))}
      </div>
    </div>
  );
};

export default CustomersPage;



