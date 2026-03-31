/**
 * Warehouses Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, Edit, Trash2, Warehouse, Package, MapPin,
  TrendingUp, TrendingDown, AlertTriangle, CheckCircle
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleWarehouses = [
  { id: 1, name: 'المستودع الرئيسي', location: 'الرياض - حي الصناعية', capacity: 10000, used: 7500, products: 456, value: 2500000, status: 'active' },
  { id: 2, name: 'مستودع جدة', location: 'جدة - حي الميناء', capacity: 5000, used: 4200, products: 234, value: 980000, status: 'active' },
  { id: 3, name: 'مستودع الدمام', location: 'الدمام - المنطقة الصناعية', capacity: 3000, used: 2800, products: 178, value: 650000, status: 'warning' },
  { id: 4, name: 'مستودع المدينة', location: 'المدينة المنورة', capacity: 2000, used: 500, products: 89, value: 120000, status: 'active' },
];

const WarehouseCard = ({ warehouse, onEdit, onDelete, onView }) => {
  const usagePercent = (warehouse.used / warehouse.capacity) * 100;
  const statusConfig = {
    active: { className: 'status-badge--success', label: 'نشط' },
    warning: { className: 'status-badge--warning', label: 'شبه ممتلئ' },
    full: { className: 'status-badge--danger', label: 'ممتلئ' },
  };
  const status = statusConfig[warehouse.status];

  return (
    <div className="entity-card">
      <div className="entity-card__header">
        <div className="flex items-center gap-4">
          <div className="entity-card__avatar entity-card__avatar--info">
            <Warehouse size={24} />
          </div>
          <div>
            <h3 className="entity-card__name">{warehouse.name}</h3>
            <p className="entity-card__meta">
              <MapPin size={12} />
              {warehouse.location}
            </p>
          </div>
        </div>
        <span className={`status-badge ${status.className}`}>
          {status.label}
        </span>
      </div>

      {/* Capacity Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-secondary">السعة المستخدمة</span>
          <span className="font-semibold text-primary">{usagePercent.toFixed(0)}%</span>
        </div>
        <div className="progress-bar">
          <div
            className={`progress-bar__fill ${
              usagePercent > 90 ? 'progress-bar__fill--danger' : usagePercent > 70 ? 'progress-bar__fill--warning' : 'progress-bar__fill--success'
            }`}
            style={{ width: `${usagePercent}%` }}
          />
        </div>
        <div className="flex items-center justify-between text-xs text-tertiary mt-1">
          <span>{warehouse.used.toLocaleString()} وحدة</span>
          <span>{warehouse.capacity.toLocaleString()} وحدة</span>
        </div>
      </div>

      <div className="entity-card__stats" style={{ gridTemplateColumns: 'repeat(2, 1fr)' }}>
        <div className="entity-card__stat">
          <p className="entity-card__stat-value">{warehouse.products}</p>
          <p className="entity-card__stat-label">منتج</p>
        </div>
        <div className="entity-card__stat">
          <p className="entity-card__stat-value entity-card__stat-value--success">{(warehouse.value / 1000).toFixed(0)}K</p>
          <p className="entity-card__stat-label">ج.م قيمة</p>
        </div>
      </div>

      <div className="entity-card__actions">
        <button onClick={() => onView(warehouse)} className="entity-card__action entity-card__action--primary">
          عرض
        </button>
        <button onClick={() => onEdit(warehouse)} className="entity-card__action entity-card__action--secondary">
          تعديل
        </button>
        <button onClick={() => onDelete(warehouse)} className="entity-card__action entity-card__action--danger">
          <Trash2 size={16} />
        </button>
      </div>
    </div>
  );
};

const WarehousesPage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const totalCapacity = sampleWarehouses.reduce((sum, w) => sum + w.capacity, 0);
  const totalUsed = sampleWarehouses.reduce((sum, w) => sum + w.used, 0);
  const totalProducts = sampleWarehouses.reduce((sum, w) => sum + w.products, 0);
  const totalValue = sampleWarehouses.reduce((sum, w) => sum + w.value, 0);

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">المستودعات</h1>
          <p className="page-subtitle">إدارة المستودعات والمخزون</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>مستودع جديد</Button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">المستودعات</span>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Warehouse className="text-purple-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleWarehouses.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المنتجات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Package className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-teal-600">{totalProducts.toLocaleString()}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">السعة الكلية</span>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <TrendingUp className="text-blue-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-blue-600">{((totalUsed / totalCapacity) * 100).toFixed(0)}%</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">قيمة المخزون</span>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <DollarSign className="text-emerald-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-emerald-600">{(totalValue / 1000000).toFixed(1)}M</div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث في المستودعات..."
            className="form-input-standard pr-12"
          />
        </div>
      </div>

      <div className="entity-grid">
        {sampleWarehouses.map(warehouse => (
          <WarehouseCard
            key={warehouse.id}
            warehouse={warehouse}
            onView={(w) => console.log('View:', w)}
            onEdit={(w) => console.log('Edit:', w)}
            onDelete={(w) => console.log('Delete:', w)}
          />
        ))}
      </div>
    </div>
  );
};

export default WarehousesPage;



