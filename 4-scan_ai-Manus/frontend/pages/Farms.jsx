/**
 * Farms Page - Complete CRUD with all buttons and relationships
 * ==============================================================
 * 
 * Features:
 * - List all farms with pagination
 * - Create new farm
 * - Edit existing farm
 * - Delete farm (with confirmation)
 * - View farm details
 * - Search and filter
 * - Map view
 * - RTL support
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Plus,
  Search,
  Filter,
  MapPin,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Warehouse,
  Sprout,
  BarChart3,
  RefreshCw,
  Download,
  Upload,
  Map,
  List,
  Grid,
  ChevronLeft,
  ChevronRight,
  X,
  Check,
  AlertTriangle
} from 'lucide-react';

// Services
import ApiService from '../services/ApiService';

// Components
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge, StatusBadge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Input, Select, TextArea } from '../src/components/Form';
import DataTable from '../src/components/DataTable';
import { StatCard } from '../src/components/Card';

// ============================================
// Constants
// ============================================
const AREA_UNITS = [
  { value: 'hectare', label: 'Hectare', labelAr: 'هكتار' },
  { value: 'acre', label: 'Acre', labelAr: 'فدان' },
  { value: 'sqm', label: 'Square Meter', labelAr: 'متر مربع' }
];

const SOIL_TYPES = [
  { value: 'clay', label: 'Clay', labelAr: 'طيني' },
  { value: 'sandy', label: 'Sandy', labelAr: 'رملي' },
  { value: 'loamy', label: 'Loamy', labelAr: 'طمي' },
  { value: 'silt', label: 'Silt', labelAr: 'غريني' },
  { value: 'peaty', label: 'Peaty', labelAr: 'خثي' },
  { value: 'chalky', label: 'Chalky', labelAr: 'طباشيري' }
];

const STATUS_OPTIONS = [
  { value: 'active', label: 'Active', labelAr: 'نشط' },
  { value: 'inactive', label: 'Inactive', labelAr: 'غير نشط' },
  { value: 'archived', label: 'Archived', labelAr: 'مؤرشف' }
];

// ============================================
// Farm Form Component
// ============================================
const FarmForm = ({ farm, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: farm?.name || '',
    location: farm?.location || '',
    address: farm?.address || '',
    latitude: farm?.latitude || '',
    longitude: farm?.longitude || '',
    area: farm?.area || '',
    area_unit: farm?.area_unit || 'hectare',
    crop_type: farm?.crop_type || '',
    soil_type: farm?.soil_type || '',
    description: farm?.description || '',
    notes: farm?.notes || '',
    is_active: farm?.is_active || 'active'
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
    if (!formData.location) newErrors.location = isRTL ? 'الموقع مطلوب' : 'Location is required';
    if (!formData.area || formData.area <= 0) newErrors.area = isRTL ? 'المساحة مطلوبة' : 'Valid area is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'اسم المزرعة' : 'Farm Name'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Input
          label={isRTL ? 'الموقع' : 'Location'}
          value={formData.location}
          onChange={(v) => handleChange('location', v)}
          error={errors.location}
          icon={MapPin}
          required
        />
      </div>

      <TextArea
        label={isRTL ? 'العنوان التفصيلي' : 'Address'}
        value={formData.address}
        onChange={(v) => handleChange('address', v)}
        rows={2}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'خط العرض' : 'Latitude'}
          type="number"
          value={formData.latitude}
          onChange={(v) => handleChange('latitude', v)}
          placeholder="-90 to 90"
        />
        <Input
          label={isRTL ? 'خط الطول' : 'Longitude'}
          type="number"
          value={formData.longitude}
          onChange={(v) => handleChange('longitude', v)}
          placeholder="-180 to 180"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label={isRTL ? 'المساحة' : 'Area'}
          type="number"
          value={formData.area}
          onChange={(v) => handleChange('area', v)}
          error={errors.area}
          required
        />
        <Select
          label={isRTL ? 'وحدة القياس' : 'Area Unit'}
          value={formData.area_unit}
          onChange={(v) => handleChange('area_unit', v)}
          options={AREA_UNITS}
        />
        <Select
          label={isRTL ? 'نوع التربة' : 'Soil Type'}
          value={formData.soil_type}
          onChange={(v) => handleChange('soil_type', v)}
          options={SOIL_TYPES}
          placeholder={isRTL ? 'اختر نوع التربة' : 'Select soil type'}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'نوع المحصول' : 'Crop Type'}
          value={formData.crop_type}
          onChange={(v) => handleChange('crop_type', v)}
          icon={Sprout}
        />
        <Select
          label={isRTL ? 'الحالة' : 'Status'}
          value={formData.is_active}
          onChange={(v) => handleChange('is_active', v)}
          options={STATUS_OPTIONS}
        />
      </div>

      <TextArea
        label={isRTL ? 'الوصف' : 'Description'}
        value={formData.description}
        onChange={(v) => handleChange('description', v)}
        rows={3}
      />

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
          {farm ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Farm Card Component
// ============================================
const FarmCard = ({ farm, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);

  const statusColors = {
    active: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
    inactive: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
    archived: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
  };

  return (
    <Card hover onClick={() => onView(farm)} className="relative">
      {/* Status badge */}
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[farm.is_active]}`}>
          {isRTL ? STATUS_OPTIONS.find(s => s.value === farm.is_active)?.labelAr : farm.is_active}
        </span>
      </div>

      {/* Actions menu */}
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
              <div className="absolute z-20 top-full mt-1 left-0 rtl:left-auto rtl:right-0 w-40 py-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
                <button
                  onClick={(e) => { e.stopPropagation(); onView(farm); setShowMenu(false); }}
                  className="w-full px-4 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                >
                  <Eye className="w-4 h-4" />
                  {isRTL ? 'عرض' : 'View'}
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); onEdit(farm); setShowMenu(false); }}
                  className="w-full px-4 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                >
                  <Edit className="w-4 h-4" />
                  {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); onDelete(farm); setShowMenu(false); }}
                  className="w-full px-4 py-2 text-left rtl:text-right text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center gap-2"
                >
                  <Trash2 className="w-4 h-4" />
                  {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="pt-8">
        <div className="w-12 h-12 rounded-xl bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center mb-4">
          <Warehouse className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
        </div>

        <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-1">
          {farm.name}
        </h3>
        
        <div className="flex items-center gap-1 text-sm text-gray-500 mb-4">
          <MapPin className="w-4 h-4" />
          <span className="truncate">{farm.location}</span>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">{isRTL ? 'المساحة' : 'Area'}</span>
            <p className="font-medium text-gray-800 dark:text-white">
              {farm.area} {farm.area_unit}
            </p>
          </div>
          <div>
            <span className="text-gray-500">{isRTL ? 'التشخيصات' : 'Diagnoses'}</span>
            <p className="font-medium text-gray-800 dark:text-white">
              {farm.diagnosis_count || 0}
            </p>
          </div>
          {farm.crop_type && (
            <div className="col-span-2">
              <span className="text-gray-500">{isRTL ? 'المحصول' : 'Crop'}</span>
              <p className="font-medium text-gray-800 dark:text-white">
                {farm.crop_type}
              </p>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Main Farms Page Component
// ============================================
const Farms = () => {
  const navigate = useNavigate();
  const isRTL = document.documentElement.dir === 'rtl';

  // State
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // grid, list
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 12,
    total: 0,
    totalPages: 0
  });

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedFarm, setSelectedFarm] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  // Stats
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    totalArea: 0,
    totalDiagnoses: 0
  });

  // Load farms
  const loadFarms = useCallback(async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...(searchQuery && { search: searchQuery }),
        ...(statusFilter && { status: statusFilter })
      };
      
      const response = await ApiService.getFarms(params);
      setFarms(response.items || response);
      setPagination(prev => ({
        ...prev,
        total: response.total || response.length,
        totalPages: response.total_pages || Math.ceil((response.total || response.length) / prev.limit)
      }));

      // Calculate stats
      const items = response.items || response;
      setStats({
        total: response.total || items.length,
        active: items.filter(f => f.is_active === 'active').length,
        totalArea: items.reduce((sum, f) => sum + (f.area || 0), 0),
        totalDiagnoses: items.reduce((sum, f) => sum + (f.diagnosis_count || 0), 0)
      });
    } catch (err) {
      setError(err.message);
      console.error('Error loading farms:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, statusFilter]);

  useEffect(() => {
    loadFarms();
  }, [loadFarms]);

  // Handlers
  const handleCreate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.createFarm(data);
      setShowCreateModal(false);
      loadFarms();
    } catch (err) {
      console.error('Error creating farm:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleUpdate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.updateFarm(selectedFarm.id, data);
      setShowEditModal(false);
      setSelectedFarm(null);
      loadFarms();
    } catch (err) {
      console.error('Error updating farm:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      setFormLoading(true);
      await ApiService.deleteFarm(selectedFarm.id);
      setShowDeleteModal(false);
      setSelectedFarm(null);
      loadFarms();
    } catch (err) {
      console.error('Error deleting farm:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleView = (farm) => {
    navigate(`/farms/${farm.id}`);
  };

  const handleEdit = (farm) => {
    setSelectedFarm(farm);
    setShowEditModal(true);
  };

  const handleDeleteClick = (farm) => {
    setSelectedFarm(farm);
    setShowDeleteModal(true);
  };

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
  };

  // Table columns for list view
  const columns = [
    { key: 'name', label: 'Name', labelAr: 'الاسم', sortable: true },
    { key: 'location', label: 'Location', labelAr: 'الموقع', sortable: true },
    { key: 'area', label: 'Area', labelAr: 'المساحة', render: (v, row) => `${v} ${row.area_unit}` },
    { key: 'crop_type', label: 'Crop', labelAr: 'المحصول' },
    { key: 'is_active', label: 'Status', labelAr: 'الحالة', render: (v) => (
      <Badge variant={v === 'active' ? 'success' : v === 'inactive' ? 'secondary' : 'warning'}>
        {v}
      </Badge>
    )},
    { key: 'diagnosis_count', label: 'Diagnoses', labelAr: 'التشخيصات' },
    { key: 'created_at', label: 'Created', labelAr: 'تاريخ الإنشاء', render: (v) => new Date(v).toLocaleDateString() }
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <PageHeader
        title={isRTL ? 'المزارع' : 'Farms'}
        description={isRTL ? 'إدارة مزارعك ومراقبة صحة المحاصيل' : 'Manage your farms and monitor crop health'}
        icon={Warehouse}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadFarms}>
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'مزرعة جديدة' : 'New Farm'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          title={isRTL ? 'إجمالي المزارع' : 'Total Farms'}
          value={stats.total}
          icon={Warehouse}
          iconColor="emerald"
        />
        <StatCard
          title={isRTL ? 'المزارع النشطة' : 'Active Farms'}
          value={stats.active}
          icon={Check}
          iconColor="blue"
        />
        <StatCard
          title={isRTL ? 'إجمالي المساحة' : 'Total Area'}
          value={`${stats.totalArea.toLocaleString()} ha`}
          icon={Map}
          iconColor="purple"
        />
        <StatCard
          title={isRTL ? 'التشخيصات' : 'Diagnoses'}
          value={stats.totalDiagnoses}
          icon={BarChart3}
          iconColor="amber"
        />
      </div>

      {/* Filters and View Toggle */}
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
            
            <Select
              value={statusFilter}
              onChange={setStatusFilter}
              options={[
                { value: '', label: isRTL ? 'كل الحالات' : 'All Status' },
                ...STATUS_OPTIONS
              ]}
              className="w-40"
            />
          </div>

          <div className="flex items-center gap-2">
            <div className="flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 ${viewMode === 'grid' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'}`}
              >
                <Grid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 ${viewMode === 'list' ? 'bg-emerald-500 text-white' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded-lg" />
            </Card>
          ))}
        </div>
      ) : error ? (
        <Card className="p-8 text-center">
          <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-red-500" />
          <p className="text-red-500">{error}</p>
          <Button onClick={loadFarms} className="mt-4">
            {isRTL ? 'إعادة المحاولة' : 'Retry'}
          </Button>
        </Card>
      ) : farms.length === 0 ? (
        <Card className="p-12 text-center">
          <Warehouse className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
            {isRTL ? 'لا توجد مزارع' : 'No Farms Yet'}
          </h3>
          <p className="text-gray-500 mb-4">
            {isRTL ? 'ابدأ بإضافة مزرعتك الأولى' : 'Start by adding your first farm'}
          </p>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1" />
            {isRTL ? 'إضافة مزرعة' : 'Add Farm'}
          </Button>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {farms.map(farm => (
            <FarmCard
              key={farm.id}
              farm={farm}
              onView={handleView}
              onEdit={handleEdit}
              onDelete={handleDeleteClick}
            />
          ))}
        </div>
      ) : (
        <DataTable
          columns={columns}
          data={farms}
          onRowClick={handleView}
          pagination={pagination}
          onPageChange={handlePageChange}
        />
      )}

      {/* Pagination for grid view */}
      {viewMode === 'grid' && pagination.totalPages > 1 && (
        <div className="flex justify-center items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page <= 1}
          >
            {isRTL ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </Button>
          <span className="text-sm text-gray-500">
            {pagination.page} / {pagination.totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page >= pagination.totalPages}
          >
            {isRTL ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </Button>
        </div>
      )}

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title={isRTL ? 'إنشاء مزرعة جديدة' : 'Create New Farm'}
        titleAr="إنشاء مزرعة جديدة"
        size="xl"
      >
        <FarmForm
          onSubmit={handleCreate}
          onCancel={() => setShowCreateModal(false)}
          loading={formLoading}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => { setShowEditModal(false); setSelectedFarm(null); }}
        title={isRTL ? 'تعديل المزرعة' : 'Edit Farm'}
        titleAr="تعديل المزرعة"
        size="xl"
      >
        <FarmForm
          farm={selectedFarm}
          onSubmit={handleUpdate}
          onCancel={() => { setShowEditModal(false); setSelectedFarm(null); }}
          loading={formLoading}
        />
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => { setShowDeleteModal(false); setSelectedFarm(null); }}
        size="sm"
        showCloseButton={false}
      >
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
            <Trash2 className="w-8 h-8 text-red-500" />
          </div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
            {isRTL ? 'حذف المزرعة' : 'Delete Farm'}
          </h3>
          <p className="text-gray-500 mb-6">
            {isRTL 
              ? `هل أنت متأكد من حذف "${selectedFarm?.name}"؟ لا يمكن التراجع عن هذا الإجراء.`
              : `Are you sure you want to delete "${selectedFarm?.name}"? This action cannot be undone.`
            }
          </p>
          <div className="flex justify-center gap-3">
            <Button
              variant="secondary"
              onClick={() => { setShowDeleteModal(false); setSelectedFarm(null); }}
            >
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button
              variant="danger"
              onClick={handleDelete}
              loading={formLoading}
            >
              {isRTL ? 'حذف' : 'Delete'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Farms;
