/**
 * Inventory Page - Stock Management System
 * =========================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Plus, Search, Package, AlertTriangle, TrendingDown, TrendingUp,
  Edit, Trash2, RefreshCw, Grid, List, Calendar, DollarSign,
  MoreVertical, Eye, Archive, ShoppingCart
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
const ITEM_TYPES = [
  { value: 'seed', label: 'Seeds', labelAr: 'بذور', color: 'emerald' },
  { value: 'fertilizer', label: 'Fertilizer', labelAr: 'أسمدة', color: 'amber' },
  { value: 'pesticide', label: 'Pesticide', labelAr: 'مبيدات', color: 'red' },
  { value: 'tool', label: 'Tools', labelAr: 'أدوات', color: 'blue' },
  { value: 'fuel', label: 'Fuel', labelAr: 'وقود', color: 'orange' },
  { value: 'feed', label: 'Feed', labelAr: 'علف', color: 'green' },
  { value: 'medicine', label: 'Medicine', labelAr: 'أدوية', color: 'purple' },
  { value: 'other', label: 'Other', labelAr: 'أخرى', color: 'gray' }
];

const UNITS = [
  { value: 'kg', label: 'Kilogram', labelAr: 'كجم' },
  { value: 'g', label: 'Gram', labelAr: 'جرام' },
  { value: 'l', label: 'Liter', labelAr: 'لتر' },
  { value: 'ml', label: 'Milliliter', labelAr: 'مل' },
  { value: 'pcs', label: 'Pieces', labelAr: 'قطعة' },
  { value: 'bag', label: 'Bags', labelAr: 'كيس' },
  { value: 'box', label: 'Boxes', labelAr: 'صندوق' }
];

// ============================================
// Inventory Form
// ============================================
const InventoryForm = ({ item, farms, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: item?.name || '',
    item_type: item?.item_type || 'seed',
    sku: item?.sku || '',
    quantity: item?.quantity || '',
    unit: item?.unit || 'kg',
    unit_price: item?.unit_price || '',
    min_quantity: item?.min_quantity || '',
    max_quantity: item?.max_quantity || '',
    farm_id: item?.farm_id || '',
    location: item?.location || '',
    supplier: item?.supplier || '',
    expiry_date: item?.expiry_date?.split('T')[0] || '',
    notes: item?.notes || ''
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
    if (!formData.quantity || formData.quantity < 0) newErrors.quantity = isRTL ? 'الكمية مطلوبة' : 'Quantity is required';
    if (!formData.farm_id) newErrors.farm_id = isRTL ? 'المزرعة مطلوبة' : 'Farm is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) onSubmit(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: null }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'اسم الصنف' : 'Item Name'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Select
          label={isRTL ? 'النوع' : 'Type'}
          value={formData.item_type}
          onChange={(v) => handleChange('item_type', v)}
          options={ITEM_TYPES}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label={isRTL ? 'الكمية' : 'Quantity'}
          type="number"
          value={formData.quantity}
          onChange={(v) => handleChange('quantity', v)}
          error={errors.quantity}
          required
        />
        <Select
          label={isRTL ? 'الوحدة' : 'Unit'}
          value={formData.unit}
          onChange={(v) => handleChange('unit', v)}
          options={UNITS}
        />
        <Input
          label={isRTL ? 'سعر الوحدة' : 'Unit Price'}
          type="number"
          value={formData.unit_price}
          onChange={(v) => handleChange('unit_price', v)}
          icon={DollarSign}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الحد الأدنى' : 'Min Quantity'}
          type="number"
          value={formData.min_quantity}
          onChange={(v) => handleChange('min_quantity', v)}
        />
        <Input
          label={isRTL ? 'الحد الأقصى' : 'Max Quantity'}
          type="number"
          value={formData.max_quantity}
          onChange={(v) => handleChange('max_quantity', v)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label={isRTL ? 'المزرعة' : 'Farm'}
          value={formData.farm_id}
          onChange={(v) => handleChange('farm_id', v)}
          options={farms.map(f => ({ value: f.id, label: f.name }))}
          error={errors.farm_id}
          required
        />
        <Input
          label={isRTL ? 'الموقع في المخزن' : 'Storage Location'}
          value={formData.location}
          onChange={(v) => handleChange('location', v)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'المورد' : 'Supplier'}
          value={formData.supplier}
          onChange={(v) => handleChange('supplier', v)}
        />
        <Input
          label={isRTL ? 'تاريخ الانتهاء' : 'Expiry Date'}
          type="date"
          value={formData.expiry_date}
          onChange={(v) => handleChange('expiry_date', v)}
        />
      </div>

      <TextArea
        label={isRTL ? 'ملاحظات' : 'Notes'}
        value={formData.notes}
        onChange={(v) => handleChange('notes', v)}
        rows={2}
      />

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {item ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Inventory Card
// ============================================
const InventoryCard = ({ item, onView, onEdit, onDelete, onAdjust }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  const type = ITEM_TYPES.find(t => t.value === item.item_type);
  const isLowStock = item.min_quantity && item.quantity <= item.min_quantity;
  const isExpiringSoon = item.expiry_date && new Date(item.expiry_date) <= new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);

  return (
    <Card hover onClick={() => onView(item)} className={`relative ${isLowStock ? 'border-amber-500 border-2' : ''}`}>
      {/* Alerts */}
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4 flex gap-1">
        {isLowStock && (
          <span className="p-1 bg-amber-100 rounded-full" title={isRTL ? 'مخزون منخفض' : 'Low Stock'}>
            <TrendingDown className="w-4 h-4 text-amber-600" />
          </span>
        )}
        {isExpiringSoon && (
          <span className="p-1 bg-red-100 rounded-full" title={isRTL ? 'قارب الانتهاء' : 'Expiring Soon'}>
            <Calendar className="w-4 h-4 text-red-600" />
          </span>
        )}
      </div>

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
              <div className="absolute z-20 top-full mt-1 left-0 rtl:left-auto rtl:right-0 w-40 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button onClick={(e) => { e.stopPropagation(); onView(item); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onAdjust(item); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" /> {isRTL ? 'تعديل الكمية' : 'Adjust'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onEdit(item); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onDelete(item); setShowMenu(false); }} className="w-full px-3 py-2 text-left rtl:text-right text-sm text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="pt-10">
        <Badge variant={type?.color} className="mb-3">{isRTL ? type?.labelAr : type?.label}</Badge>
        
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-1">{item.name}</h3>
        <p className="text-sm text-gray-500 mb-4">{item.sku || '-'}</p>

        <div className="flex items-baseline gap-1 mb-4">
          <span className={`text-3xl font-bold ${isLowStock ? 'text-amber-600' : 'text-gray-800 dark:text-white'}`}>
            {item.quantity}
          </span>
          <span className="text-gray-500">{UNITS.find(u => u.value === item.unit)?.[isRTL ? 'labelAr' : 'label']}</span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-500">{isRTL ? 'القيمة' : 'Value'}</span>
          <span className="font-medium text-gray-800 dark:text-white">
            ${((item.quantity || 0) * (item.unit_price || 0)).toFixed(2)}
          </span>
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Adjustment Modal
// ============================================
const AdjustmentModal = ({ item, isOpen, onClose, onSubmit, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [adjustment, setAdjustment] = useState({ quantity_change: '', reason: '', adjustment_type: 'add' });

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isRTL ? 'تعديل الكمية' : 'Adjust Quantity'} size="sm">
      <div className="space-y-4">
        <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <span className="text-sm text-gray-500">{isRTL ? 'الكمية الحالية' : 'Current Quantity'}</span>
          <div className="text-2xl font-bold">{item?.quantity} {item?.unit}</div>
        </div>

        <Select
          label={isRTL ? 'نوع التعديل' : 'Adjustment Type'}
          value={adjustment.adjustment_type}
          onChange={(v) => setAdjustment(prev => ({ ...prev, adjustment_type: v }))}
          options={[
            { value: 'add', label: isRTL ? 'إضافة' : 'Add' },
            { value: 'remove', label: isRTL ? 'سحب' : 'Remove' },
            { value: 'correction', label: isRTL ? 'تصحيح' : 'Correction' },
            { value: 'loss', label: isRTL ? 'فاقد' : 'Loss' }
          ]}
        />

        <Input
          label={isRTL ? 'الكمية' : 'Quantity'}
          type="number"
          value={adjustment.quantity_change}
          onChange={(v) => setAdjustment(prev => ({ ...prev, quantity_change: v }))}
        />

        <TextArea
          label={isRTL ? 'السبب' : 'Reason'}
          value={adjustment.reason}
          onChange={(v) => setAdjustment(prev => ({ ...prev, reason: v }))}
          rows={2}
        />

        <div className="flex justify-end gap-3">
          <Button variant="secondary" onClick={onClose}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
          <Button onClick={() => onSubmit(adjustment)} loading={loading}>{isRTL ? 'تطبيق' : 'Apply'}</Button>
        </div>
      </div>
    </Modal>
  );
};

// ============================================
// Main Inventory Page
// ============================================
const Inventory = () => {
  const isRTL = document.documentElement.dir === 'rtl';

  const [inventory, setInventory] = useState([]);
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0, totalPages: 0 });

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showAdjustModal, setShowAdjustModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, value: 0, lowStock: 0, expiring: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [inventoryRes, farmsRes] = await Promise.all([
        ApiService.getInventory({ page: pagination.page, limit: pagination.limit, search: searchQuery, type: typeFilter }),
        ApiService.getFarms({ limit: 100 })
      ]);

      const items = inventoryRes.items || inventoryRes;
      setInventory(items);
      setFarms(farmsRes.items || farmsRes);
      setPagination(prev => ({
        ...prev,
        total: inventoryRes.total || items.length,
        totalPages: inventoryRes.total_pages || Math.ceil((inventoryRes.total || items.length) / prev.limit)
      }));

      const now = Date.now();
      const thirtyDays = 30 * 24 * 60 * 60 * 1000;
      setStats({
        total: items.length,
        value: items.reduce((sum, i) => sum + (i.quantity || 0) * (i.unit_price || 0), 0),
        lowStock: items.filter(i => i.min_quantity && i.quantity <= i.min_quantity).length,
        expiring: items.filter(i => i.expiry_date && new Date(i.expiry_date) <= new Date(now + thirtyDays)).length
      });
    } catch (err) {
      console.error('Error loading inventory:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, typeFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try { setFormLoading(true); await ApiService.createInventory(data); setShowCreateModal(false); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try { setFormLoading(true); await ApiService.updateInventory(selectedItem.id, data); setShowEditModal(false); setSelectedItem(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try { setFormLoading(true); await ApiService.deleteInventory(selectedItem.id); setShowDeleteModal(false); setSelectedItem(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleAdjust = async (adjustment) => {
    try { setFormLoading(true); await ApiService.adjustInventory(selectedItem.id, adjustment); setShowAdjustModal(false); setSelectedItem(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleView = (item) => { setSelectedItem(item); setShowEditModal(true); };
  const handleEdit = (item) => { setSelectedItem(item); setShowEditModal(true); };
  const handleDeleteClick = (item) => { setSelectedItem(item); setShowDeleteModal(true); };
  const handleAdjustClick = (item) => { setSelectedItem(item); setShowAdjustModal(true); };

  const columns = [
    { key: 'name', label: 'Name', labelAr: 'الاسم', sortable: true },
    { key: 'item_type', label: 'Type', labelAr: 'النوع', render: (v) => {
      const t = ITEM_TYPES.find(t => t.value === v);
      return <Badge variant={t?.color}>{isRTL ? t?.labelAr : t?.label}</Badge>;
    }},
    { key: 'quantity', label: 'Quantity', labelAr: 'الكمية', render: (v, row) => `${v} ${row.unit}` },
    { key: 'unit_price', label: 'Price', labelAr: 'السعر', render: (v) => v ? `$${v}` : '-' },
    { key: 'farm_name', label: 'Farm', labelAr: 'المزرعة' },
    { key: 'expiry_date', label: 'Expiry', labelAr: 'الانتهاء', render: (v) => v ? new Date(v).toLocaleDateString() : '-' }
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'المخزون' : 'Inventory'}
        description={isRTL ? 'إدارة مخزون المزرعة والمستلزمات' : 'Manage farm stock and supplies'}
        icon={Package}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'صنف جديد' : 'New Item'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي الأصناف' : 'Total Items'} value={stats.total} icon={Package} iconColor="blue" />
        <StatCard title={isRTL ? 'القيمة الإجمالية' : 'Total Value'} value={`$${stats.value.toFixed(2)}`} icon={DollarSign} iconColor="emerald" />
        <StatCard title={isRTL ? 'مخزون منخفض' : 'Low Stock'} value={stats.lowStock} icon={AlertTriangle} iconColor="amber" />
        <StatCard title={isRTL ? 'قارب الانتهاء' : 'Expiring Soon'} value={stats.expiring} icon={Calendar} iconColor="red" />
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
            <Select value={typeFilter} onChange={setTypeFilter} className="w-40"
              options={[{ value: '', label: isRTL ? 'كل الأنواع' : 'All Types' }, ...ITEM_TYPES]}
            />
          </div>
          <div className="flex rounded-lg border overflow-hidden">
            <button onClick={() => setViewMode('grid')} className={`p-2 ${viewMode === 'grid' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100'}`}><Grid className="w-4 h-4" /></button>
            <button onClick={() => setViewMode('list')} className={`p-2 ${viewMode === 'list' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100'}`}><List className="w-4 h-4" /></button>
          </div>
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-52" />)}
        </div>
      ) : inventory.length === 0 ? (
        <Card className="p-12 text-center">
          <Package className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا يوجد مخزون' : 'No Inventory'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {inventory.map(item => <InventoryCard key={item.id} item={item} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} onAdjust={handleAdjustClick} />)}
        </div>
      ) : (
        <DataTable columns={columns} data={inventory} onRowClick={handleView} pagination={pagination} onPageChange={(p) => setPagination(prev => ({ ...prev, page: p }))} />
      )}

      {/* Modals */}
      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة صنف' : 'Add Item'} size="xl">
        <InventoryForm farms={farms} onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedItem(null); }} title={isRTL ? 'تعديل الصنف' : 'Edit Item'} size="xl">
        <InventoryForm item={selectedItem} farms={farms} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedItem(null); }} loading={formLoading} />
      </Modal>

      <AdjustmentModal item={selectedItem} isOpen={showAdjustModal} onClose={() => { setShowAdjustModal(false); setSelectedItem(null); }} onSubmit={handleAdjust} loading={formLoading} />

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedItem(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف الصنف' : 'Delete Item'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedItem?.name}"؟` : `Delete "${selectedItem?.name}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedItem(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Inventory;
