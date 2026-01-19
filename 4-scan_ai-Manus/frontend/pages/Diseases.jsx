/**
 * Diseases Page - Disease Database Management
 * ============================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Bug, Search, Plus, RefreshCw, Eye, Edit, Trash2, MoreVertical,
  AlertTriangle, Shield, Leaf, FlaskConical, Microscope, BookOpen, Grid, List
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
const CATEGORIES = [
  { value: 'fungal', label: 'Fungal', labelAr: 'فطري', color: 'amber' },
  { value: 'bacterial', label: 'Bacterial', labelAr: 'بكتيري', color: 'red' },
  { value: 'viral', label: 'Viral', labelAr: 'فيروسي', color: 'purple' },
  { value: 'pest', label: 'Pest', labelAr: 'آفات', color: 'orange' },
  { value: 'nutrient', label: 'Nutrient', labelAr: 'تغذية', color: 'emerald' },
  { value: 'environmental', label: 'Environmental', labelAr: 'بيئي', color: 'blue' },
  { value: 'other', label: 'Other', labelAr: 'أخرى', color: 'gray' }
];

const SEVERITY_LEVELS = [
  { value: 'low', label: 'Low', labelAr: 'منخفض', color: 'emerald' },
  { value: 'medium', label: 'Medium', labelAr: 'متوسط', color: 'amber' },
  { value: 'high', label: 'High', labelAr: 'مرتفع', color: 'orange' },
  { value: 'critical', label: 'Critical', labelAr: 'حرج', color: 'red' }
];

// ============================================
// Disease Card Component
// ============================================
const DiseaseCard = ({ disease, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  
  const category = CATEGORIES.find(c => c.value === disease.category);
  const severity = SEVERITY_LEVELS.find(s => s.value === disease.severity_level);

  return (
    <Card hover onClick={() => onView(disease)} className="relative">
      {/* Severity Indicator */}
      <div className={`absolute top-0 left-0 right-0 h-1 bg-${severity?.color}-500`} />

      {/* Menu */}
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
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
              <div className="absolute z-20 top-full mt-1 right-0 rtl:right-auto rtl:left-0 w-36 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button onClick={(e) => { e.stopPropagation(); onView(disease); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onEdit(disease); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onDelete(disease); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="p-6 pt-8">
        {/* Image */}
        <div className="w-full h-32 rounded-xl bg-gradient-to-br from-red-100 to-orange-100 dark:from-red-900/30 dark:to-orange-900/30 mb-4 overflow-hidden">
          {disease.image_url ? (
            <img src={disease.image_url} alt={disease.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Bug className="w-12 h-12 text-red-400 opacity-50" />
            </div>
          )}
        </div>

        {/* Info */}
        <div className="flex items-start gap-2 mb-2">
          <Badge variant={category?.color}>{isRTL ? category?.labelAr : category?.label}</Badge>
          <Badge variant={severity?.color}>{isRTL ? severity?.labelAr : severity?.label}</Badge>
        </div>

        <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
          {isRTL ? disease.name_ar || disease.name : disease.name}
        </h3>
        {disease.scientific_name && (
          <p className="text-xs text-gray-500 italic mb-3">{disease.scientific_name}</p>
        )}

        {disease.symptoms && (
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            {isRTL ? disease.symptoms_ar || disease.symptoms : disease.symptoms}
          </p>
        )}

        {/* Stats */}
        <div className="flex justify-between mt-4 pt-3 border-t text-sm">
          <span className="text-gray-500">
            {disease.diagnosis_count || 0} {isRTL ? 'تشخيص' : 'diagnoses'}
          </span>
          <span className="text-gray-500">
            {disease.affected_crops?.length || 0} {isRTL ? 'محاصيل' : 'crops'}
          </span>
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Disease Form Component
// ============================================
const DiseaseForm = ({ disease, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: disease?.name || '',
    name_ar: disease?.name_ar || '',
    scientific_name: disease?.scientific_name || '',
    category: disease?.category || 'fungal',
    severity_level: disease?.severity_level || 'medium',
    symptoms: disease?.symptoms || '',
    symptoms_ar: disease?.symptoms_ar || '',
    causes: disease?.causes || '',
    causes_ar: disease?.causes_ar || '',
    treatment: disease?.treatment || '',
    treatment_ar: disease?.treatment_ar || '',
    prevention: disease?.prevention || '',
    prevention_ar: disease?.prevention_ar || '',
    image_url: disease?.image_url || ''
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
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
    <form onSubmit={handleSubmit} className="space-y-4 max-h-[70vh] overflow-y-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الاسم (إنجليزي)' : 'Name (English)'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Input
          label={isRTL ? 'الاسم (عربي)' : 'Name (Arabic)'}
          value={formData.name_ar}
          onChange={(v) => handleChange('name_ar', v)}
        />
      </div>

      <Input
        label={isRTL ? 'الاسم العلمي' : 'Scientific Name'}
        value={formData.scientific_name}
        onChange={(v) => handleChange('scientific_name', v)}
        placeholder="e.g., Phytophthora infestans"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label={isRTL ? 'الفئة' : 'Category'}
          value={formData.category}
          onChange={(v) => handleChange('category', v)}
          options={CATEGORIES}
        />
        <Select
          label={isRTL ? 'مستوى الخطورة' : 'Severity Level'}
          value={formData.severity_level}
          onChange={(v) => handleChange('severity_level', v)}
          options={SEVERITY_LEVELS}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <TextArea
          label={isRTL ? 'الأعراض (إنجليزي)' : 'Symptoms (English)'}
          value={formData.symptoms}
          onChange={(v) => handleChange('symptoms', v)}
          rows={3}
        />
        <TextArea
          label={isRTL ? 'الأعراض (عربي)' : 'Symptoms (Arabic)'}
          value={formData.symptoms_ar}
          onChange={(v) => handleChange('symptoms_ar', v)}
          rows={3}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <TextArea
          label={isRTL ? 'العلاج (إنجليزي)' : 'Treatment (English)'}
          value={formData.treatment}
          onChange={(v) => handleChange('treatment', v)}
          rows={3}
        />
        <TextArea
          label={isRTL ? 'العلاج (عربي)' : 'Treatment (Arabic)'}
          value={formData.treatment_ar}
          onChange={(v) => handleChange('treatment_ar', v)}
          rows={3}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <TextArea
          label={isRTL ? 'الوقاية (إنجليزي)' : 'Prevention (English)'}
          value={formData.prevention}
          onChange={(v) => handleChange('prevention', v)}
          rows={3}
        />
        <TextArea
          label={isRTL ? 'الوقاية (عربي)' : 'Prevention (Arabic)'}
          value={formData.prevention_ar}
          onChange={(v) => handleChange('prevention_ar', v)}
          rows={3}
        />
      </div>

      <Input
        label={isRTL ? 'رابط الصورة' : 'Image URL'}
        value={formData.image_url}
        onChange={(v) => handleChange('image_url', v)}
      />

      <div className="flex justify-end gap-3 pt-4 border-t sticky bottom-0 bg-white dark:bg-gray-900">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {disease ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Disease Detail Modal
// ============================================
const DiseaseDetailModal = ({ disease, isOpen, onClose }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  if (!disease) return null;

  const category = CATEGORIES.find(c => c.value === disease.category);
  const severity = SEVERITY_LEVELS.find(s => s.value === disease.severity_level);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isRTL ? disease.name_ar || disease.name : disease.name} size="xl">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-start gap-4">
          <div className="w-24 h-24 rounded-xl bg-red-100 dark:bg-red-900/30 overflow-hidden flex-shrink-0">
            {disease.image_url ? (
              <img src={disease.image_url} alt={disease.name} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <Bug className="w-10 h-10 text-red-400" />
              </div>
            )}
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap gap-2 mb-2">
              <Badge variant={category?.color}>{isRTL ? category?.labelAr : category?.label}</Badge>
              <Badge variant={severity?.color}>{isRTL ? severity?.labelAr : severity?.label}</Badge>
            </div>
            {disease.scientific_name && (
              <p className="text-sm text-gray-500 italic">{disease.scientific_name}</p>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Symptoms */}
          <div>
            <h4 className="font-semibold flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              {isRTL ? 'الأعراض' : 'Symptoms'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {isRTL ? disease.symptoms_ar || disease.symptoms : disease.symptoms}
            </p>
          </div>

          {/* Causes */}
          <div>
            <h4 className="font-semibold flex items-center gap-2 mb-2">
              <Microscope className="w-4 h-4 text-purple-500" />
              {isRTL ? 'الأسباب' : 'Causes'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {isRTL ? disease.causes_ar || disease.causes : disease.causes}
            </p>
          </div>

          {/* Treatment */}
          <div>
            <h4 className="font-semibold flex items-center gap-2 mb-2">
              <FlaskConical className="w-4 h-4 text-emerald-500" />
              {isRTL ? 'العلاج' : 'Treatment'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {isRTL ? disease.treatment_ar || disease.treatment : disease.treatment}
            </p>
          </div>

          {/* Prevention */}
          <div>
            <h4 className="font-semibold flex items-center gap-2 mb-2">
              <Shield className="w-4 h-4 text-blue-500" />
              {isRTL ? 'الوقاية' : 'Prevention'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {isRTL ? disease.prevention_ar || disease.prevention : disease.prevention}
            </p>
          </div>
        </div>
      </div>
    </Modal>
  );
};

// ============================================
// Main Diseases Page
// ============================================
const Diseases = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedDisease, setSelectedDisease] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, fungal: 0, bacterial: 0, viral: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await ApiService.getDiseases({ search: searchQuery, category: categoryFilter });
      const items = response.items || response || [];
      setDiseases(items);

      setStats({
        total: items.length,
        fungal: items.filter(d => d.category === 'fungal').length,
        bacterial: items.filter(d => d.category === 'bacterial').length,
        viral: items.filter(d => d.category === 'viral').length
      });
    } catch (err) {
      console.error('Error loading diseases:', err);
      // Mock data
      setDiseases([
        { id: 1, name: 'Early Blight', name_ar: 'اللفحة المبكرة', category: 'fungal', severity_level: 'medium', symptoms: 'Dark spots on leaves' },
        { id: 2, name: 'Late Blight', name_ar: 'اللفحة المتأخرة', category: 'fungal', severity_level: 'high', symptoms: 'Water-soaked lesions' },
        { id: 3, name: 'Bacterial Spot', name_ar: 'البقعة البكتيرية', category: 'bacterial', severity_level: 'medium', symptoms: 'Small dark spots' }
      ]);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, categoryFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try { setFormLoading(true); await ApiService.createDisease(data); setShowCreateModal(false); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try { setFormLoading(true); await ApiService.updateDisease(selectedDisease.id, data); setShowEditModal(false); setSelectedDisease(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try { setFormLoading(true); await ApiService.deleteDisease(selectedDisease.id); setShowDeleteModal(false); setSelectedDisease(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleView = (disease) => { setSelectedDisease(disease); setShowDetailModal(true); };
  const handleEdit = (disease) => { setSelectedDisease(disease); setShowEditModal(true); };
  const handleDeleteClick = (disease) => { setSelectedDisease(disease); setShowDeleteModal(true); };

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'الأمراض' : 'Diseases'}
        description={isRTL ? 'قاعدة بيانات أمراض النباتات' : 'Plant diseases database'}
        icon={Bug}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'مرض جديد' : 'New Disease'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي الأمراض' : 'Total Diseases'} value={stats.total} icon={Bug} iconColor="red" />
        <StatCard title={isRTL ? 'فطرية' : 'Fungal'} value={stats.fungal} icon={Leaf} iconColor="amber" />
        <StatCard title={isRTL ? 'بكتيرية' : 'Bacterial'} value={stats.bacterial} icon={Microscope} iconColor="red" />
        <StatCard title={isRTL ? 'فيروسية' : 'Viral'} value={stats.viral} icon={AlertTriangle} iconColor="purple" />
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
            <Select value={categoryFilter} onChange={setCategoryFilter} className="w-40"
              options={[{ value: '', label: isRTL ? 'كل الفئات' : 'All Categories' }, ...CATEGORIES]} />
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
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-64" />)}
        </div>
      ) : diseases.length === 0 ? (
        <Card className="p-12 text-center">
          <Bug className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا توجد أمراض' : 'No Diseases'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {diseases.map(disease => (
            <DiseaseCard key={disease.id} disease={disease} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} />
          ))}
        </div>
      )}

      {/* Modals */}
      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة مرض' : 'Add Disease'} size="xl">
        <DiseaseForm onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedDisease(null); }} title={isRTL ? 'تعديل المرض' : 'Edit Disease'} size="xl">
        <DiseaseForm disease={selectedDisease} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedDisease(null); }} loading={formLoading} />
      </Modal>

      <DiseaseDetailModal disease={selectedDisease} isOpen={showDetailModal} onClose={() => { setShowDetailModal(false); setSelectedDisease(null); }} />

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedDisease(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف المرض' : 'Delete Disease'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedDisease?.name_ar || selectedDisease?.name}"؟` : `Delete "${selectedDisease?.name}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedDisease(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Diseases;
