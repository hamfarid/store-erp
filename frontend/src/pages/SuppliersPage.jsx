/**
 * Suppliers Management Page
 * Connected to supplierService API
 */

import React, { useState, useEffect } from 'react';
import {
  Search, Plus, Edit, Trash2, Eye, Truck, Phone, Mail, MapPin,
  Package, DollarSign, Star, Building2, Globe, Download, Upload, RefreshCw
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import Button from '../components/ui/ModernButton';
import supplierService from '../services/supplierService';

const sampleSuppliers = [
  { id: 1, name: 'شركة التقنية للإلكترونيات', contact: 'محمد أحمد', email: 'tech@supplier.com', phone: '0501234567', city: 'الرياض', country: 'السعودية', totalPurchases: 850000, balance: -25000, productsCount: 156, rating: 5 },
  { id: 2, name: 'مصنع الملابس الحديثة', contact: 'خالد العمري', email: 'clothes@factory.com', phone: '0512345678', city: 'جدة', country: 'السعودية', totalPurchases: 320000, balance: 0, productsCount: 89, rating: 4 },
  { id: 3, name: 'Apple Inc.', contact: 'John Smith', email: 'supplier@apple.com', phone: '+14155551234', city: 'Cupertino', country: 'USA', totalPurchases: 1500000, balance: -150000, productsCount: 45, rating: 5 },
  { id: 4, name: 'Samsung Electronics', contact: 'Kim Lee', email: 'supply@samsung.com', phone: '+82212345678', city: 'Seoul', country: 'South Korea', totalPurchases: 980000, balance: -50000, productsCount: 78, rating: 4 },
];

const SupplierCard = ({ supplier, onView, onEdit, onDelete }) => (
  <div className="entity-card">
    <div className="entity-card__header">
      <div className="flex items-center gap-4">
        <div className="entity-card__avatar entity-card__avatar--primary">
          <Building2 size={24} />
        </div>
        <div>
          <h3 className="entity-card__name">{supplier.name}</h3>
          <p className="entity-card__meta">
            <Globe size={12} />
            {supplier.city}، {supplier.country}
          </p>
        </div>
      </div>
      <div className="rating-stars">
        {[...Array(5)].map((_, i) => (
          <Star key={i} size={14} className={i < supplier.rating ? 'rating-star--filled' : 'rating-star--empty'} />
        ))}
      </div>
    </div>

    <div className="entity-card__info">
      <div className="entity-card__info-row">
        <Mail size={14} className="entity-card__info-icon" />
        <span>{supplier.email}</span>
      </div>
      <div className="entity-card__info-row">
        <Phone size={14} className="entity-card__info-icon" />
        <span dir="ltr">{supplier.phone}</span>
      </div>
    </div>

    <div className="entity-card__stats">
      <div className="entity-card__stat">
        <p className="entity-card__stat-value">{supplier.productsCount}</p>
        <p className="entity-card__stat-label">المنتجات</p>
      </div>
      <div className="entity-card__stat">
        <p className="entity-card__stat-value entity-card__stat-value--primary">{(supplier.totalPurchases / 1000).toFixed(0)}K</p>
        <p className="entity-card__stat-label">المشتريات</p>
      </div>
      <div className="entity-card__stat">
        <p className={`entity-card__stat-value ${supplier.balance < 0 ? 'entity-card__stat-value--danger' : ''}`}>
          {Math.abs(supplier.balance).toLocaleString()}
        </p>
        <p className="entity-card__stat-label">{supplier.balance < 0 ? 'مستحق' : 'الرصيد'}</p>
      </div>
    </div>

    <div className="entity-card__actions">
      <button onClick={() => onView(supplier)} className="entity-card__action entity-card__action--primary">
        عرض
      </button>
      <button onClick={() => onEdit(supplier)} className="entity-card__action entity-card__action--secondary">
        تعديل
      </button>
      <button onClick={() => onDelete(supplier)} className="entity-card__action entity-card__action--danger">
        <Trash2 size={16} />
      </button>
    </div>
  </div>
);

const SuppliersPage = () => {
  const [suppliers, setSuppliers] = useState(sampleSuppliers);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSupplier, setSelectedSupplier] = useState(null);

  // Fetch suppliers on mount
  useEffect(() => {
    fetchSuppliers();
  }, []);

  const fetchSuppliers = async () => {
    setIsLoading(true);
    try {
      const response = await supplierService.getAll();
      if (response.suppliers && response.suppliers.length > 0) {
        setSuppliers(response.suppliers);
      }
    } catch (error) {
      console.log('Using sample data:', error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddSupplier = () => {
    setSelectedSupplier(null);
    setShowAddModal(true);
  };

  const handleViewSupplier = async (supplier) => {
    try {
      const details = await supplierService.getById(supplier.id);
      setSelectedSupplier(details);
      toast.success('تم تحميل تفاصيل المورد');
    } catch (error) {
      setSelectedSupplier(supplier);
    }
  };

  const handleEditSupplier = (supplier) => {
    setSelectedSupplier(supplier);
    setShowAddModal(true);
  };

  const handleDeleteSupplier = async (supplier) => {
    if (!window.confirm(`هل أنت متأكد من حذف المورد "${supplier.name}"؟`)) return;
    
    try {
      await supplierService.delete(supplier.id);
      setSuppliers(suppliers.filter(s => s.id !== supplier.id));
      toast.success('تم حذف المورد بنجاح');
    } catch (error) {
      toast.error('فشل في حذف المورد');
    }
  };

  const handleExport = async () => {
    try {
      await supplierService.exportToExcel();
      toast.success('تم تصدير الموردين بنجاح');
    } catch (error) {
      toast.error('فشل في التصدير');
    }
  };

  const filteredSuppliers = suppliers.filter(s => 
    s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.city.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalDebt = filteredSuppliers.filter(s => s.balance < 0).reduce((sum, s) => sum + Math.abs(s.balance), 0);

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">الموردين</h1>
          <p className="text-gray-500 mt-1">إدارة الموردين وطلبات الشراء</p>
        </div>
        <div className="page-actions flex gap-2">
          <Button variant="outline" icon={Download} onClick={handleExport}>تصدير</Button>
          <Button variant="outline" icon={RefreshCw} onClick={fetchSuppliers}>تحديث</Button>
          <Button variant="primary" icon={Plus} onClick={handleAddSupplier}>مورد جديد</Button>
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
          <div className="stats-card-value">{suppliers.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المنتجات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Package className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value text-teal-600">
            {suppliers.reduce((sum, s) => sum + (s.productsCount || 0), 0)}
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
            {(suppliers.reduce((sum, s) => sum + (s.totalPurchases || 0), 0) / 1000000).toFixed(1)}M
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

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
          <span className="mr-2 text-gray-500">جاري التحميل...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSuppliers.map(supplier => (
            <SupplierCard
              key={supplier.id}
              supplier={supplier}
              onView={handleViewSupplier}
              onEdit={handleEditSupplier}
              onDelete={handleDeleteSupplier}
            />
          ))}
        </div>
      )}

      {filteredSuppliers.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <Truck className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900">لا يوجد موردين</h3>
          <p className="text-gray-500">قم بإضافة مورد جديد للبدء</p>
        </div>
      )}

      {/* View Supplier Modal */}
      {selectedSupplier && !showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 max-w-lg w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل المورد</h2>
              <button onClick={() => setSelectedSupplier(null)} className="p-2 hover:bg-gray-100 rounded-full">✕</button>
            </div>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white">
                  <Building2 size={28} />
                </div>
                <div>
                  <h3 className="text-lg font-bold">{selectedSupplier.name}</h3>
                  <p className="text-gray-500">{selectedSupplier.city}، {selectedSupplier.country}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                <div>
                  <label className="text-sm text-gray-500">البريد الإلكتروني</label>
                  <p className="font-medium">{selectedSupplier.email}</p>
                </div>
                <div>
                  <label className="text-sm text-gray-500">الهاتف</label>
                  <p className="font-medium" dir="ltr">{selectedSupplier.phone}</p>
                </div>
                <div>
                  <label className="text-sm text-gray-500">إجمالي المشتريات</label>
                  <p className="font-medium text-blue-600">{selectedSupplier.totalPurchases?.toLocaleString()} ر.س</p>
                </div>
                <div>
                  <label className="text-sm text-gray-500">المستحقات</label>
                  <p className={`font-medium ${selectedSupplier.balance < 0 ? 'text-rose-600' : 'text-green-600'}`}>
                    {Math.abs(selectedSupplier.balance || 0).toLocaleString()} ر.س
                  </p>
                </div>
              </div>
              <div className="flex gap-2 pt-4">
                <Button variant="primary" className="flex-1" onClick={() => { setShowAddModal(true); }}>تعديل</Button>
                <Button variant="outline" className="flex-1" onClick={() => setSelectedSupplier(null)}>إغلاق</Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SuppliersPage;



