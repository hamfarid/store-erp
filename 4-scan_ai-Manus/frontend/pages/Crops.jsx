/**
 * Crops Page - Crop Management with Disease Relationships
 * ========================================================
 * 
 * Features:
 * - List all crops with categories
 * - CRUD operations
 * - Disease relationships
 * - Growing information
 * - Image gallery
 * - RTL support
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Plus, Search, Filter, Sprout, Leaf, Sun, Droplet, Thermometer,
  Edit, Trash2, Eye, MoreVertical, RefreshCw, Calendar, Bug,
  Grid, List, ChevronRight, ChevronLeft, X
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Input, Select, TextArea, FileUpload } from '../src/components/Form';
import DataTable from '../src/components/DataTable';
import { StatCard } from '../src/components/Card';

// ============================================
// Constants
// ============================================
const CATEGORIES = [
  { value: 'vegetables', label: 'Vegetables', labelAr: 'خضروات', color: 'emerald' },
  { value: 'fruits', label: 'Fruits', labelAr: 'فواكه', color: 'red' },
  { value: 'grains', label: 'Grains', labelAr: 'حبوب', color: 'amber' },
  { value: 'herbs', label: 'Herbs', labelAr: 'أعشاب', color: 'green' },
  { value: 'trees', label: 'Trees', labelAr: 'أشجار', color: 'teal' },
  { value: 'flowers', label: 'Flowers', labelAr: 'زهور', color: 'pink' },
  { value: 'other', label: 'Other', labelAr: 'أخرى', color: 'gray' }
];

const WATER_NEEDS = [
  { value: 'low', label: 'Low', labelAr: 'منخفض' },
  { value: 'medium', label: 'Medium', labelAr: 'متوسط' },
  { value: 'high', label: 'High', labelAr: 'عالي' }
];

const SUNLIGHT_NEEDS = [
  { value: 'full', label: 'Full Sun', labelAr: 'شمس كاملة' },
  { value: 'partial', label: 'Partial Shade', labelAr: 'ظل جزئي' },
  { value: 'shade', label: 'Full Shade', labelAr: 'ظل كامل' }
];

const SEASONS = [
  { value: 'spring', label: 'Spring', labelAr: 'ربيع' },
  { value: 'summer', label: 'Summer', labelAr: 'صيف' },
  { value: 'fall', label: 'Fall', labelAr: 'خريف' },
  { value: 'winter', label: 'Winter', labelAr: 'شتاء' },
  { value: 'year-round', label: 'Year Round', labelAr: 'طوال العام' }
];

// ============================================
// Crop Form Component
// ============================================
const CropForm = ({ crop, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: crop?.name || '',
    name_en: crop?.name_en || '',
    scientific_name: crop?.scientific_name || '',
    category: crop?.category || 'vegetables',
    growing_season: crop?.growing_season || '',
    water_needs: crop?.water_needs || 'medium',
    sunlight_needs: crop?.sunlight_needs || 'full',
    temperature_min: crop?.temperature_min || '',
    temperature_max: crop?.temperature_max || '',
    growth_duration: crop?.growth_duration || '',
    description: crop?.description || '',
    care_tips: crop?.care_tips || '',
    image_url: crop?.image_url || ''
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
    if (!formData.category) newErrors.category = isRTL ? 'الفئة مطلوبة' : 'Category is required';
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
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: null }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الاسم (عربي)' : 'Name (Arabic)'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Input
          label={isRTL ? 'الاسم (إنجليزي)' : 'Name (English)'}
          value={formData.name_en}
          onChange={(v) => handleChange('name_en', v)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الاسم العلمي' : 'Scientific Name'}
          value={formData.scientific_name}
          onChange={(v) => handleChange('scientific_name', v)}
          placeholder="Solanum lycopersicum"
        />
        <Select
          label={isRTL ? 'الفئة' : 'Category'}
          value={formData.category}
          onChange={(v) => handleChange('category', v)}
          options={CATEGORIES}
          error={errors.category}
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Select
          label={isRTL ? 'موسم الزراعة' : 'Growing Season'}
          value={formData.growing_season}
          onChange={(v) => handleChange('growing_season', v)}
          options={SEASONS}
        />
        <Select
          label={isRTL ? 'احتياج المياه' : 'Water Needs'}
          value={formData.water_needs}
          onChange={(v) => handleChange('water_needs', v)}
          options={WATER_NEEDS}
        />
        <Select
          label={isRTL ? 'احتياج الشمس' : 'Sunlight Needs'}
          value={formData.sunlight_needs}
          onChange={(v) => handleChange('sunlight_needs', v)}
          options={SUNLIGHT_NEEDS}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label={isRTL ? 'أدنى حرارة (°C)' : 'Min Temp (°C)'}
          type="number"
          value={formData.temperature_min}
          onChange={(v) => handleChange('temperature_min', v)}
        />
        <Input
          label={isRTL ? 'أقصى حرارة (°C)' : 'Max Temp (°C)'}
          type="number"
          value={formData.temperature_max}
          onChange={(v) => handleChange('temperature_max', v)}
        />
        <Input
          label={isRTL ? 'مدة النمو (أيام)' : 'Growth Duration (days)'}
          type="number"
          value={formData.growth_duration}
          onChange={(v) => handleChange('growth_duration', v)}
        />
      </div>

      <TextArea
        label={isRTL ? 'الوصف' : 'Description'}
        value={formData.description}
        onChange={(v) => handleChange('description', v)}
        rows={3}
      />

      <TextArea
        label={isRTL ? 'نصائح العناية' : 'Care Tips'}
        value={formData.care_tips}
        onChange={(v) => handleChange('care_tips', v)}
        rows={3}
      />

      <Input
        label={isRTL ? 'رابط الصورة' : 'Image URL'}
        value={formData.image_url}
        onChange={(v) => handleChange('image_url', v)}
        placeholder="https://..."
      />

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {crop ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Crop Card Component
// ============================================
const CropCard = ({ crop, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  const category = CATEGORIES.find(c => c.value === crop.category) || CATEGORIES[6];

  return (
    <Card hover onClick={() => onView(crop)} className="relative group">
      {/* Image */}
      <div className="relative h-40 bg-gradient-to-br from-emerald-100 to-teal-100 dark:from-emerald-900/30 dark:to-teal-900/30 rounded-t-lg overflow-hidden">
        {crop.image_url ? (
          <img src={crop.image_url} alt={crop.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Leaf className="w-16 h-16 text-emerald-400 opacity-50" />
          </div>
        )}
        
        {/* Category Badge */}
        <Badge 
          variant={category.color}
          className="absolute top-3 left-3 rtl:left-auto rtl:right-3"
        >
          {isRTL ? category.labelAr : category.label}
        </Badge>

        {/* Actions Menu */}
        <div className="absolute top-3 right-3 rtl:right-auto rtl:left-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="relative">
            <button
              onClick={(e) => { e.stopPropagation(); setShowMenu(!showMenu); }}
              className="p-1.5 rounded-full bg-white/80 dark:bg-gray-800/80 hover:bg-white dark:hover:bg-gray-800"
            >
              <MoreVertical className="w-4 h-4 text-gray-600" />
            </button>
            {showMenu && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowMenu(false)} />
                <div className="absolute z-20 top-full mt-1 right-0 rtl:right-auto rtl:left-0 w-36 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                  <button
                    onClick={(e) => { e.stopPropagation(); onView(crop); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                  >
                    <Eye className="w-4 h-4" />
                    {isRTL ? 'عرض' : 'View'}
                  </button>
                  <button
                    onClick={(e) => { e.stopPropagation(); onEdit(crop); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left rtl:text-right text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
                  >
                    <Edit className="w-4 h-4" />
                    {isRTL ? 'تعديل' : 'Edit'}
                  </button>
                  <button
                    onClick={(e) => { e.stopPropagation(); onDelete(crop); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left rtl:text-right text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center gap-2"
                  >
                    <Trash2 className="w-4 h-4" />
                    {isRTL ? 'حذف' : 'Delete'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
          {crop.name}
        </h3>
        {crop.scientific_name && (
          <p className="text-xs text-gray-500 italic mb-3">{crop.scientific_name}</p>
        )}

        {/* Properties */}
        <div className="flex flex-wrap gap-2 text-xs">
          {crop.water_needs && (
            <span className="flex items-center gap-1 px-2 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 rounded">
              <Droplet className="w-3 h-3" />
              {WATER_NEEDS.find(w => w.value === crop.water_needs)?.[isRTL ? 'labelAr' : 'label']}
            </span>
          )}
          {crop.sunlight_needs && (
            <span className="flex items-center gap-1 px-2 py-1 bg-amber-50 dark:bg-amber-900/20 text-amber-600 rounded">
              <Sun className="w-3 h-3" />
              {SUNLIGHT_NEEDS.find(s => s.value === crop.sunlight_needs)?.[isRTL ? 'labelAr' : 'label']}
            </span>
          )}
          {crop.growth_duration && (
            <span className="flex items-center gap-1 px-2 py-1 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 rounded">
              <Calendar className="w-3 h-3" />
              {crop.growth_duration} {isRTL ? 'يوم' : 'days'}
            </span>
          )}
        </div>

        {/* Stats */}
        <div className="flex justify-between mt-4 pt-3 border-t text-sm">
          <span className="text-gray-500">
            <Bug className="w-4 h-4 inline mr-1" />
            {crop.disease_count || 0} {isRTL ? 'أمراض' : 'diseases'}
          </span>
          <span className="text-gray-500">
            {crop.farm_count || 0} {isRTL ? 'مزارع' : 'farms'}
          </span>
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Main Crops Page
// ============================================
const Crops = () => {
  const navigate = useNavigate();
  const isRTL = document.documentElement.dir === 'rtl';

  // State
  const [crops, setCrops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0, totalPages: 0 });

  // Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  // Stats
  const [stats, setStats] = useState({ total: 0, byCategory: {} });

  // Load crops
  const loadCrops = useCallback(async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...(searchQuery && { search: searchQuery }),
        ...(categoryFilter && { category: categoryFilter })
      };
      
      const response = await ApiService.getCrops(params);
      setCrops(response.items || response);
      setPagination(prev => ({
        ...prev,
        total: response.total || response.length,
        totalPages: response.total_pages || Math.ceil((response.total || response.length) / prev.limit)
      }));

      // Calculate stats
      const items = response.items || response;
      const byCategory = {};
      items.forEach(c => {
        byCategory[c.category] = (byCategory[c.category] || 0) + 1;
      });
      setStats({ total: items.length, byCategory });
    } catch (err) {
      console.error('Error loading crops:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, categoryFilter]);

  useEffect(() => {
    loadCrops();
  }, [loadCrops]);

  // Handlers
  const handleCreate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.createCrop(data);
      setShowCreateModal(false);
      loadCrops();
    } catch (err) {
      console.error('Error creating crop:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleUpdate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.updateCrop(selectedCrop.id, data);
      setShowEditModal(false);
      setSelectedCrop(null);
      loadCrops();
    } catch (err) {
      console.error('Error updating crop:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      setFormLoading(true);
      await ApiService.deleteCrop(selectedCrop.id);
      setShowDeleteModal(false);
      setSelectedCrop(null);
      loadCrops();
    } catch (err) {
      console.error('Error deleting crop:', err);
    } finally {
      setFormLoading(false);
    }
  };

  const handleView = (crop) => navigate(`/crops/${crop.id}`);
  const handleEdit = (crop) => { setSelectedCrop(crop); setShowEditModal(true); };
  const handleDeleteClick = (crop) => { setSelectedCrop(crop); setShowDeleteModal(true); };

  // Table columns
  const columns = [
    { key: 'name', label: 'Name', labelAr: 'الاسم', sortable: true },
    { key: 'scientific_name', label: 'Scientific', labelAr: 'علمي' },
    { key: 'category', label: 'Category', labelAr: 'الفئة', render: (v) => {
      const cat = CATEGORIES.find(c => c.value === v);
      return <Badge variant={cat?.color}>{isRTL ? cat?.labelAr : cat?.label}</Badge>;
    }},
    { key: 'water_needs', label: 'Water', labelAr: 'ماء' },
    { key: 'growth_duration', label: 'Duration', labelAr: 'المدة', render: (v) => v ? `${v} days` : '-' },
    { key: 'disease_count', label: 'Diseases', labelAr: 'أمراض' }
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'المحاصيل' : 'Crops'}
        description={isRTL ? 'إدارة قاعدة بيانات المحاصيل والنباتات' : 'Manage your crops and plants database'}
        icon={Sprout}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadCrops}>
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'محصول جديد' : 'New Crop'}
          </Button>
        </div>
      </PageHeader>

      {/* Category Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
        {CATEGORIES.map(cat => (
          <button
            key={cat.value}
            onClick={() => setCategoryFilter(categoryFilter === cat.value ? '' : cat.value)}
            className={`
              p-3 rounded-lg text-center transition-all
              ${categoryFilter === cat.value 
                ? `bg-${cat.color}-500 text-white` 
                : 'bg-white dark:bg-gray-800 hover:shadow-md'
              }
            `}
          >
            <div className="text-2xl font-bold">{stats.byCategory[cat.value] || 0}</div>
            <div className="text-xs">{isRTL ? cat.labelAr : cat.label}</div>
          </button>
        ))}
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
              <div className="h-40 bg-gray-200 dark:bg-gray-700 rounded-t-lg" />
              <div className="p-4 space-y-2">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
              </div>
            </Card>
          ))}
        </div>
      ) : crops.length === 0 ? (
        <Card className="p-12 text-center">
          <Sprout className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
            {isRTL ? 'لا توجد محاصيل' : 'No Crops Yet'}
          </h3>
          <p className="text-gray-500 mb-4">
            {isRTL ? 'ابدأ بإضافة محصولك الأول' : 'Start by adding your first crop'}
          </p>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1" />
            {isRTL ? 'إضافة محصول' : 'Add Crop'}
          </Button>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {crops.map(crop => (
            <CropCard
              key={crop.id}
              crop={crop}
              onView={handleView}
              onEdit={handleEdit}
              onDelete={handleDeleteClick}
            />
          ))}
        </div>
      ) : (
        <DataTable
          columns={columns}
          data={crops}
          onRowClick={handleView}
          pagination={pagination}
          onPageChange={(p) => setPagination(prev => ({ ...prev, page: p }))}
        />
      )}

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title={isRTL ? 'إضافة محصول جديد' : 'Add New Crop'}
        size="xl"
      >
        <CropForm
          onSubmit={handleCreate}
          onCancel={() => setShowCreateModal(false)}
          loading={formLoading}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => { setShowEditModal(false); setSelectedCrop(null); }}
        title={isRTL ? 'تعديل المحصول' : 'Edit Crop'}
        size="xl"
      >
        <CropForm
          crop={selectedCrop}
          onSubmit={handleUpdate}
          onCancel={() => { setShowEditModal(false); setSelectedCrop(null); }}
          loading={formLoading}
        />
      </Modal>

      {/* Delete Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => { setShowDeleteModal(false); setSelectedCrop(null); }}
        size="sm"
        showCloseButton={false}
      >
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
            <Trash2 className="w-8 h-8 text-red-500" />
          </div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
            {isRTL ? 'حذف المحصول' : 'Delete Crop'}
          </h3>
          <p className="text-gray-500 mb-6">
            {isRTL 
              ? `هل أنت متأكد من حذف "${selectedCrop?.name}"؟`
              : `Are you sure you want to delete "${selectedCrop?.name}"?`
            }
          </p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedCrop(null); }}>
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>
              {isRTL ? 'حذف' : 'Delete'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Crops;
