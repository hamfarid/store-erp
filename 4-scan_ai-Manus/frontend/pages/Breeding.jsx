/**
 * Breeding Programs Page
 * ======================
 * Manage plant breeding programs and genetic research
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Plus, Search, Filter, Edit, Trash2, Eye, Download, Upload,
  Dna, Target, Calendar, Award, TrendingUp, Users, AlertCircle,
  ChevronDown, MoreVertical, Leaf, FlaskConical, Microscope
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Input, Select, TextArea } from '../src/components/Form';
import { Button } from '../components/UI/button';
import { Modal } from '../src/components/Modal';

const Breeding = () => {
  const isRTL = document.documentElement.dir === 'rtl';

  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [pagination, setPagination] = useState({ page: 1, limit: 10, total: 0 });

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    crop_type: '',
    objective: '',
    start_date: '',
    target_completion: '',
    status: 'planning',
    generation: 'F1',
    parent_varieties: '',
    target_traits: '',
    methodology: '',
    lead_researcher: '',
    budget: '',
    notes: ''
  });

  const fetchPrograms = useCallback(async () => {
    setLoading(true);
    try {
      const response = await ApiService.getBreedingPrograms({
        page: pagination.page,
        limit: pagination.limit,
        search: searchTerm,
        status: filterStatus !== 'all' ? filterStatus : undefined
      });
      setPrograms(response.data || []);
      setPagination(prev => ({ ...prev, total: response.total || 0 }));
    } catch (err) {
      console.error('Failed to fetch programs:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchTerm, filterStatus]);

  useEffect(() => {
    fetchPrograms();
  }, [fetchPrograms]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedProgram) {
        await ApiService.updateBreedingProgram(selectedProgram.id, formData);
      } else {
        await ApiService.createBreedingProgram(formData);
      }
      setShowCreateModal(false);
      resetForm();
      fetchPrograms();
    } catch (err) {
      console.error('Failed to save program:', err);
    }
  };

  const handleDelete = async () => {
    try {
      await ApiService.deleteBreedingProgram(selectedProgram.id);
      setShowDeleteModal(false);
      setSelectedProgram(null);
      fetchPrograms();
    } catch (err) {
      console.error('Failed to delete program:', err);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      crop_type: '',
      objective: '',
      start_date: '',
      target_completion: '',
      status: 'planning',
      generation: 'F1',
      parent_varieties: '',
      target_traits: '',
      methodology: '',
      lead_researcher: '',
      budget: '',
      notes: ''
    });
    setSelectedProgram(null);
  };

  const openEditModal = (program) => {
    setSelectedProgram(program);
    setFormData({
      name: program.name || '',
      crop_type: program.crop_type || '',
      objective: program.objective || '',
      start_date: program.start_date || '',
      target_completion: program.target_completion || '',
      status: program.status || 'planning',
      generation: program.generation || 'F1',
      parent_varieties: program.parent_varieties || '',
      target_traits: program.target_traits || '',
      methodology: program.methodology || '',
      lead_researcher: program.lead_researcher || '',
      budget: program.budget || '',
      notes: program.notes || ''
    });
    setShowCreateModal(true);
  };

  const statusColors = {
    planning: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    active: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400',
    on_hold: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
    completed: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
  };

  const statusOptions = [
    { value: 'planning', label: isRTL ? 'قيد التخطيط' : 'Planning' },
    { value: 'active', label: isRTL ? 'نشط' : 'Active' },
    { value: 'on_hold', label: isRTL ? 'معلق' : 'On Hold' },
    { value: 'completed', label: isRTL ? 'مكتمل' : 'Completed' },
    { value: 'cancelled', label: isRTL ? 'ملغي' : 'Cancelled' }
  ];

  const generationOptions = [
    { value: 'F1', label: 'F1' },
    { value: 'F2', label: 'F2' },
    { value: 'F3', label: 'F3' },
    { value: 'F4', label: 'F4' },
    { value: 'F5', label: 'F5' },
    { value: 'BC1', label: 'BC1' },
    { value: 'BC2', label: 'BC2' }
  ];

  const stats = {
    total: programs.length,
    active: programs.filter(p => p.status === 'active').length,
    completed: programs.filter(p => p.status === 'completed').length,
    onHold: programs.filter(p => p.status === 'on_hold').length
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
            <Dna className="w-7 h-7 text-emerald-500" />
            {isRTL ? 'برامج التربية' : 'Breeding Programs'}
          </h1>
          <p className="text-gray-500 mt-1">
            {isRTL ? 'إدارة برامج التربية والبحث الوراثي' : 'Manage breeding programs and genetic research'}
          </p>
        </div>
        <Button onClick={() => { resetForm(); setShowCreateModal(true); }}>
          <Plus className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
          {isRTL ? 'برنامج جديد' : 'New Program'}
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
              <Dna className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{stats.total}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'إجمالي البرامج' : 'Total Programs'}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
              <FlaskConical className="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{stats.active}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'نشطة' : 'Active'}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <Award className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{stats.completed}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'مكتملة' : 'Completed'}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{stats.onHold}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'معلقة' : 'On Hold'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder={isRTL ? 'بحث...' : 'Search programs...'}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
          >
            <option value="all">{isRTL ? 'جميع الحالات' : 'All Status'}</option>
            {statusOptions.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Programs Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 animate-pulse">
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full" />
            </div>
          ))}
        </div>
      ) : programs.length === 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-700">
          <Microscope className="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
          <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">
            {isRTL ? 'لا توجد برامج' : 'No Programs Found'}
          </h3>
          <p className="text-gray-500 mb-4">
            {isRTL ? 'ابدأ بإنشاء برنامج تربية جديد' : 'Start by creating a new breeding program'}
          </p>
          <Button onClick={() => { resetForm(); setShowCreateModal(true); }}>
            <Plus className="w-4 h-4 mr-2" />
            {isRTL ? 'إنشاء برنامج' : 'Create Program'}
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {programs.map((program) => (
            <div key={program.id} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white">
                      <Dna className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-white">{program.name}</h3>
                      <p className="text-sm text-gray-500">{program.crop_type}</p>
                    </div>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[program.status]}`}>
                    {statusOptions.find(s => s.value === program.status)?.label}
                  </span>
                </div>

                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                  {program.objective}
                </p>

                <div className="grid grid-cols-2 gap-3 text-sm mb-4">
                  <div className="flex items-center gap-2 text-gray-500">
                    <Target className="w-4 h-4" />
                    <span>{program.generation}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500">
                    <Calendar className="w-4 h-4" />
                    <span>{program.start_date}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500">
                    <Users className="w-4 h-4" />
                    <span>{program.lead_researcher || '-'}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500">
                    <TrendingUp className="w-4 h-4" />
                    <span>{program.progress || 0}%</span>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden mb-4">
                  <div 
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all"
                    style={{ width: `${program.progress || 0}%` }}
                  />
                </div>

                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="flex-1"
                    onClick={() => { setSelectedProgram(program); setShowViewModal(true); }}
                  >
                    <Eye className="w-4 h-4 mr-1" />
                    {isRTL ? 'عرض' : 'View'}
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => openEditModal(program)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className="text-red-500 hover:bg-red-50"
                    onClick={() => { setSelectedProgram(program); setShowDeleteModal(true); }}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => { setShowCreateModal(false); resetForm(); }}
        title={selectedProgram 
          ? (isRTL ? 'تعديل البرنامج' : 'Edit Program')
          : (isRTL ? 'برنامج جديد' : 'New Breeding Program')
        }
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label={isRTL ? 'اسم البرنامج' : 'Program Name'}
              value={formData.name}
              onChange={(v) => setFormData(prev => ({ ...prev, name: v }))}
              required
            />
            <Input
              label={isRTL ? 'نوع المحصول' : 'Crop Type'}
              value={formData.crop_type}
              onChange={(v) => setFormData(prev => ({ ...prev, crop_type: v }))}
              required
            />
          </div>

          <TextArea
            label={isRTL ? 'الهدف' : 'Objective'}
            value={formData.objective}
            onChange={(v) => setFormData(prev => ({ ...prev, objective: v }))}
            rows={2}
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label={isRTL ? 'تاريخ البدء' : 'Start Date'}
              type="date"
              value={formData.start_date}
              onChange={(v) => setFormData(prev => ({ ...prev, start_date: v }))}
            />
            <Input
              label={isRTL ? 'تاريخ الانتهاء المتوقع' : 'Target Completion'}
              type="date"
              value={formData.target_completion}
              onChange={(v) => setFormData(prev => ({ ...prev, target_completion: v }))}
            />
            <Select
              label={isRTL ? 'الحالة' : 'Status'}
              value={formData.status}
              onChange={(v) => setFormData(prev => ({ ...prev, status: v }))}
              options={statusOptions}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label={isRTL ? 'الجيل' : 'Generation'}
              value={formData.generation}
              onChange={(v) => setFormData(prev => ({ ...prev, generation: v }))}
              options={generationOptions}
            />
            <Input
              label={isRTL ? 'الباحث الرئيسي' : 'Lead Researcher'}
              value={formData.lead_researcher}
              onChange={(v) => setFormData(prev => ({ ...prev, lead_researcher: v }))}
            />
          </div>

          <TextArea
            label={isRTL ? 'الأصناف الأبوية' : 'Parent Varieties'}
            value={formData.parent_varieties}
            onChange={(v) => setFormData(prev => ({ ...prev, parent_varieties: v }))}
            rows={2}
          />

          <TextArea
            label={isRTL ? 'الصفات المستهدفة' : 'Target Traits'}
            value={formData.target_traits}
            onChange={(v) => setFormData(prev => ({ ...prev, target_traits: v }))}
            rows={2}
          />

          <TextArea
            label={isRTL ? 'المنهجية' : 'Methodology'}
            value={formData.methodology}
            onChange={(v) => setFormData(prev => ({ ...prev, methodology: v }))}
            rows={2}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label={isRTL ? 'الميزانية' : 'Budget'}
              type="number"
              value={formData.budget}
              onChange={(v) => setFormData(prev => ({ ...prev, budget: v }))}
            />
          </div>

          <TextArea
            label={isRTL ? 'ملاحظات' : 'Notes'}
            value={formData.notes}
            onChange={(v) => setFormData(prev => ({ ...prev, notes: v }))}
            rows={2}
          />

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={() => { setShowCreateModal(false); resetForm(); }}>
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button type="submit">
              {selectedProgram ? (isRTL ? 'حفظ التغييرات' : 'Save Changes') : (isRTL ? 'إنشاء' : 'Create')}
            </Button>
          </div>
        </form>
      </Modal>

      {/* View Modal */}
      <Modal
        isOpen={showViewModal}
        onClose={() => { setShowViewModal(false); setSelectedProgram(null); }}
        title={selectedProgram?.name || ''}
        size="lg"
      >
        {selectedProgram && (
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white">
                <Dna className="w-8 h-8" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white">{selectedProgram.name}</h3>
                <p className="text-gray-500">{selectedProgram.crop_type}</p>
                <span className={`inline-block mt-1 px-2 py-1 text-xs font-medium rounded-full ${statusColors[selectedProgram.status]}`}>
                  {statusOptions.find(s => s.value === selectedProgram.status)?.label}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">{isRTL ? 'الجيل' : 'Generation'}</p>
                <p className="font-medium text-gray-800 dark:text-white">{selectedProgram.generation}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{isRTL ? 'الباحث الرئيسي' : 'Lead Researcher'}</p>
                <p className="font-medium text-gray-800 dark:text-white">{selectedProgram.lead_researcher || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{isRTL ? 'تاريخ البدء' : 'Start Date'}</p>
                <p className="font-medium text-gray-800 dark:text-white">{selectedProgram.start_date}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{isRTL ? 'تاريخ الانتهاء المتوقع' : 'Target Completion'}</p>
                <p className="font-medium text-gray-800 dark:text-white">{selectedProgram.target_completion || '-'}</p>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-500 mb-2">{isRTL ? 'الهدف' : 'Objective'}</p>
              <p className="text-gray-800 dark:text-white bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                {selectedProgram.objective || '-'}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500 mb-2">{isRTL ? 'الصفات المستهدفة' : 'Target Traits'}</p>
              <p className="text-gray-800 dark:text-white bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                {selectedProgram.target_traits || '-'}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500 mb-2">{isRTL ? 'التقدم' : 'Progress'}</p>
              <div className="flex items-center gap-3">
                <div className="flex-1 h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                    style={{ width: `${selectedProgram.progress || 0}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {selectedProgram.progress || 0}%
                </span>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t dark:border-gray-700">
              <Button variant="outline" onClick={() => { setShowViewModal(false); openEditModal(selectedProgram); }}>
                <Edit className="w-4 h-4 mr-2" />
                {isRTL ? 'تعديل' : 'Edit'}
              </Button>
              <Button onClick={() => setShowViewModal(false)}>
                {isRTL ? 'إغلاق' : 'Close'}
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* Delete Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => { setShowDeleteModal(false); setSelectedProgram(null); }}
        title={isRTL ? 'حذف البرنامج' : 'Delete Program'}
        size="sm"
      >
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
            <Trash2 className="w-8 h-8 text-red-500" />
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {isRTL 
              ? `هل أنت متأكد من حذف "${selectedProgram?.name}"؟`
              : `Are you sure you want to delete "${selectedProgram?.name}"?`
            }
          </p>
          <div className="flex gap-3">
            <Button variant="outline" className="flex-1" onClick={() => setShowDeleteModal(false)}>
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button variant="danger" className="flex-1 bg-red-500 hover:bg-red-600" onClick={handleDelete}>
              {isRTL ? 'حذف' : 'Delete'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Breeding;
