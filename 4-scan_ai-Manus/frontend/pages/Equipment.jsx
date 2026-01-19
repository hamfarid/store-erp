/**
 * Equipment Page - Farm Equipment Management
 * ===========================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Plus, Search, Tractor, Wrench, Settings, MoreVertical,
  Edit, Trash2, Eye, RefreshCw, Grid, List, AlertTriangle,
  CheckCircle, Clock, Calendar, DollarSign, MapPin
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
const EQUIPMENT_TYPES = [
  { value: 'tractor', label: 'Tractor', labelAr: 'جرار', icon: Tractor },
  { value: 'harvester', label: 'Harvester', labelAr: 'حصادة', icon: Settings },
  { value: 'irrigation', label: 'Irrigation', labelAr: 'ري', icon: Settings },
  { value: 'sprayer', label: 'Sprayer', labelAr: 'رشاشة', icon: Settings },
  { value: 'seeder', label: 'Seeder', labelAr: 'بذارة', icon: Settings },
  { value: 'plow', label: 'Plow', labelAr: 'محراث', icon: Settings },
  { value: 'other', label: 'Other', labelAr: 'أخرى', icon: Wrench }
];

const STATUS_OPTIONS = [
  { value: 'operational', label: 'Operational', labelAr: 'يعمل', color: 'emerald' },
  { value: 'maintenance', label: 'Maintenance', labelAr: 'صيانة', color: 'amber' },
  { value: 'repair', label: 'Repair', labelAr: 'إصلاح', color: 'red' },
  { value: 'retired', label: 'Retired', labelAr: 'متقاعد', color: 'gray' }
];

const CONDITION_OPTIONS = [
  { value: 'excellent', label: 'Excellent', labelAr: 'ممتاز' },
  { value: 'good', label: 'Good', labelAr: 'جيد' },
  { value: 'fair', label: 'Fair', labelAr: 'متوسط' },
  { value: 'poor', label: 'Poor', labelAr: 'سيء' }
];

// ============================================
// Equipment Form
// ============================================
const EquipmentForm = ({ equipment, farms, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: equipment?.name || '',
    equipment_type: equipment?.equipment_type || 'tractor',
    brand: equipment?.brand || '',
    model: equipment?.model || '',
    serial_number: equipment?.serial_number || '',
    farm_id: equipment?.farm_id || '',
    purchase_date: equipment?.purchase_date?.split('T')[0] || '',
    purchase_price: equipment?.purchase_price || '',
    status: equipment?.status || 'operational',
    condition: equipment?.condition || 'good',
    location: equipment?.location || '',
    notes: equipment?.notes || ''
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
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
          label={isRTL ? 'اسم المعدة' : 'Equipment Name'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Select
          label={isRTL ? 'النوع' : 'Type'}
          value={formData.equipment_type}
          onChange={(v) => handleChange('equipment_type', v)}
          options={EQUIPMENT_TYPES}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label={isRTL ? 'الماركة' : 'Brand'}
          value={formData.brand}
          onChange={(v) => handleChange('brand', v)}
        />
        <Input
          label={isRTL ? 'الموديل' : 'Model'}
          value={formData.model}
          onChange={(v) => handleChange('model', v)}
        />
        <Input
          label={isRTL ? 'الرقم التسلسلي' : 'Serial Number'}
          value={formData.serial_number}
          onChange={(v) => handleChange('serial_number', v)}
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
          label={isRTL ? 'الموقع داخل المزرعة' : 'Location in Farm'}
          value={formData.location}
          onChange={(v) => handleChange('location', v)}
          icon={MapPin}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'تاريخ الشراء' : 'Purchase Date'}
          type="date"
          value={formData.purchase_date}
          onChange={(v) => handleChange('purchase_date', v)}
        />
        <Input
          label={isRTL ? 'سعر الشراء' : 'Purchase Price'}
          type="number"
          value={formData.purchase_price}
          onChange={(v) => handleChange('purchase_price', v)}
          icon={DollarSign}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label={isRTL ? 'الحالة' : 'Status'}
          value={formData.status}
          onChange={(v) => handleChange('status', v)}
          options={STATUS_OPTIONS}
        />
        <Select
          label={isRTL ? 'الظرف' : 'Condition'}
          value={formData.condition}
          onChange={(v) => handleChange('condition', v)}
          options={CONDITION_OPTIONS}
        />
      </div>

      <TextArea
        label={isRTL ? 'ملاحظات' : 'Notes'}
        value={formData.notes}
        onChange={(v) => handleChange('notes', v)}
        rows={3}
      />

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {equipment ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Equipment Card
// ============================================
const EquipmentCard = ({ item, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  const status = STATUS_OPTIONS.find(s => s.value === item.status);
  const type = EQUIPMENT_TYPES.find(t => t.value === item.equipment_type);
  const TypeIcon = type?.icon || Wrench;

  return (
    <Card hover onClick={() => onView(item)} className="relative">
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
        <Badge variant={status?.color}>{isRTL ? status?.labelAr : status?.label}</Badge>
      </div>

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
              <div className="absolute z-20 top-full mt-1 left-0 rtl:left-auto rtl:right-0 w-36 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button
                  onClick={(e) => { e.stopPropagation(); onView(item); setShowMenu(false); }}
                  className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                >
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); onEdit(item); setShowMenu(false); }}
                  className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                >
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); onDelete(item); setShowMenu(false); }}
                  className="w-full px-3 py-2 text-left rtl:text-right text-sm text-red-500 hover:bg-red-50 flex items-center gap-2"
                >
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="pt-8">
        <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
          <TypeIcon className="w-6 h-6 text-blue-600" />
        </div>

        <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-1">{item.name}</h3>
        <p className="text-sm text-gray-500 mb-3">{item.brand} {item.model}</p>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <span className="text-gray-500">{isRTL ? 'المزرعة' : 'Farm'}</span>
            <p className="font-medium text-gray-800 dark:text-white">{item.farm_name || '-'}</p>
          </div>
          <div>
            <span className="text-gray-500">{isRTL ? 'الظرف' : 'Condition'}</span>
            <p className="font-medium text-gray-800 dark:text-white capitalize">{item.condition}</p>
          </div>
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Main Equipment Page
// ============================================
const Equipment = () => {
  const navigate = useNavigate();
  const isRTL = document.documentElement.dir === 'rtl';

  const [equipment, setEquipment] = useState([]);
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0, totalPages: 0 });

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, operational: 0, maintenance: 0, value: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [equipmentRes, farmsRes] = await Promise.all([
        ApiService.getEquipment({ page: pagination.page, limit: pagination.limit, search: searchQuery, status: statusFilter }),
        ApiService.getFarms({ limit: 100 })
      ]);

      const items = equipmentRes.items || equipmentRes;
      setEquipment(items);
      setFarms(farmsRes.items || farmsRes);
      setPagination(prev => ({
        ...prev,
        total: equipmentRes.total || items.length,
        totalPages: equipmentRes.total_pages || Math.ceil((equipmentRes.total || items.length) / prev.limit)
      }));

      setStats({
        total: items.length,
        operational: items.filter(e => e.status === 'operational').length,
        maintenance: items.filter(e => e.status === 'maintenance' || e.status === 'repair').length,
        value: items.reduce((sum, e) => sum + (e.purchase_price || 0), 0)
      });
    } catch (err) {
      console.error('Error loading equipment:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, statusFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.createEquipment(data);
      setShowCreateModal(false);
      loadData();
    } finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.updateEquipment(selectedItem.id, data);
      setShowEditModal(false);
      setSelectedItem(null);
      loadData();
    } finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try {
      setFormLoading(true);
      await ApiService.deleteEquipment(selectedItem.id);
      setShowDeleteModal(false);
      setSelectedItem(null);
      loadData();
    } finally { setFormLoading(false); }
  };

  const handleView = (item) => navigate(`/equipment/${item.id}`);
  const handleEdit = (item) => { setSelectedItem(item); setShowEditModal(true); };
  const handleDeleteClick = (item) => { setSelectedItem(item); setShowDeleteModal(true); };

  const columns = [
    { key: 'name', label: 'Name', labelAr: 'الاسم', sortable: true },
    { key: 'equipment_type', label: 'Type', labelAr: 'النوع', render: (v) => EQUIPMENT_TYPES.find(t => t.value === v)?.[isRTL ? 'labelAr' : 'label'] },
    { key: 'brand', label: 'Brand', labelAr: 'الماركة' },
    { key: 'farm_name', label: 'Farm', labelAr: 'المزرعة' },
    { key: 'status', label: 'Status', labelAr: 'الحالة', render: (v) => {
      const s = STATUS_OPTIONS.find(s => s.value === v);
      return <Badge variant={s?.color}>{isRTL ? s?.labelAr : s?.label}</Badge>;
    }},
    { key: 'condition', label: 'Condition', labelAr: 'الظرف' }
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'المعدات' : 'Equipment'}
        description={isRTL ? 'إدارة معدات ومكائن المزرعة' : 'Manage your farm machinery and equipment'}
        icon={Tractor}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'معدة جديدة' : 'New Equipment'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي المعدات' : 'Total Equipment'} value={stats.total} icon={Tractor} iconColor="blue" />
        <StatCard title={isRTL ? 'تعمل' : 'Operational'} value={stats.operational} icon={CheckCircle} iconColor="emerald" />
        <StatCard title={isRTL ? 'تحتاج صيانة' : 'Needs Attention'} value={stats.maintenance} icon={AlertTriangle} iconColor="amber" />
        <StatCard title={isRTL ? 'القيمة الإجمالية' : 'Total Value'} value={`$${stats.value.toLocaleString()}`} icon={DollarSign} iconColor="purple" />
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
                className="w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <Select value={statusFilter} onChange={setStatusFilter} className="w-40"
              options={[{ value: '', label: isRTL ? 'كل الحالات' : 'All Status' }, ...STATUS_OPTIONS]}
            />
          </div>
          <div className="flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <button onClick={() => setViewMode('grid')} className={`p-2 ${viewMode === 'grid' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100'}`}><Grid className="w-4 h-4" /></button>
            <button onClick={() => setViewMode('list')} className={`p-2 ${viewMode === 'list' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100'}`}><List className="w-4 h-4" /></button>
          </div>
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-48" />)}
        </div>
      ) : equipment.length === 0 ? (
        <Card className="p-12 text-center">
          <Tractor className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا توجد معدات' : 'No Equipment'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {equipment.map(item => <EquipmentCard key={item.id} item={item} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} />)}
        </div>
      ) : (
        <DataTable columns={columns} data={equipment} onRowClick={handleView} pagination={pagination} onPageChange={(p) => setPagination(prev => ({ ...prev, page: p }))} />
      )}

      {/* Modals */}
      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة معدة' : 'Add Equipment'} size="xl">
        <EquipmentForm farms={farms} onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedItem(null); }} title={isRTL ? 'تعديل المعدة' : 'Edit Equipment'} size="xl">
        <EquipmentForm equipment={selectedItem} farms={farms} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedItem(null); }} loading={formLoading} />
      </Modal>

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedItem(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف المعدة' : 'Delete Equipment'}</h3>
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

export default Equipment;
