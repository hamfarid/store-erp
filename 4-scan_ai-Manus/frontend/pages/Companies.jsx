/**
 * Companies Page - Company/Organization Management
 * =================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Building, Search, Plus, RefreshCw, Eye, Edit, Trash2, MoreVertical,
  Users, Warehouse, Mail, Phone, Globe, MapPin, Check, X
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Input, TextArea } from '../src/components/Form';
import { StatCard } from '../src/components/Card';

// ============================================
// Company Card
// ============================================
const CompanyCard = ({ company, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);

  return (
    <Card hover onClick={() => onView(company)} className="relative">
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
        <Badge variant={company.is_active ? 'emerald' : 'gray'}>
          {company.is_active ? (isRTL ? 'نشط' : 'Active') : (isRTL ? 'غير نشط' : 'Inactive')}
        </Badge>
      </div>

      <div className="absolute top-4 left-4 rtl:left-auto rtl:right-4">
        <div className="relative">
          <button onClick={(e) => { e.stopPropagation(); setShowMenu(!showMenu); }} className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700">
            <MoreVertical className="w-5 h-5 text-gray-400" />
          </button>
          {showMenu && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setShowMenu(false)} />
              <div className="absolute z-20 top-full mt-1 left-0 rtl:left-auto rtl:right-0 w-36 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button onClick={(e) => { e.stopPropagation(); onView(company); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onEdit(company); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onDelete(company); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="p-6 pt-12">
        <div className="w-16 h-16 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4 overflow-hidden">
          {company.logo_url ? (
            <img src={company.logo_url} alt={company.name} className="w-full h-full object-cover" />
          ) : (
            <Building className="w-8 h-8 text-blue-600" />
          )}
        </div>

        <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
          {isRTL ? company.name_ar || company.name : company.name}
        </h3>
        {company.city && (
          <p className="text-sm text-gray-500 flex items-center gap-1 mb-4">
            <MapPin className="w-3 h-3" /> {company.city}, {company.country}
          </p>
        )}

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">{isRTL ? 'المستخدمين' : 'Users'}</span>
            <p className="font-semibold text-gray-800 dark:text-white">{company.user_count || 0}</p>
          </div>
          <div>
            <span className="text-gray-500">{isRTL ? 'المزارع' : 'Farms'}</span>
            <p className="font-semibold text-gray-800 dark:text-white">{company.farm_count || 0}</p>
          </div>
        </div>

        <div className="flex gap-2 mt-4 pt-4 border-t text-sm">
          {company.email && (
            <a href={`mailto:${company.email}`} onClick={(e) => e.stopPropagation()} className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
              <Mail className="w-4 h-4 text-gray-500" />
            </a>
          )}
          {company.phone && (
            <a href={`tel:${company.phone}`} onClick={(e) => e.stopPropagation()} className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
              <Phone className="w-4 h-4 text-gray-500" />
            </a>
          )}
          {company.website && (
            <a href={company.website} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()} className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
              <Globe className="w-4 h-4 text-gray-500" />
            </a>
          )}
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Company Form
// ============================================
const CompanyForm = ({ company, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: company?.name || '',
    name_ar: company?.name_ar || '',
    email: company?.email || '',
    phone: company?.phone || '',
    address: company?.address || '',
    city: company?.city || '',
    country: company?.country || '',
    website: company?.website || '',
    description: company?.description || '',
    is_active: company?.is_active ?? true
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
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input label={isRTL ? 'الاسم (إنجليزي)' : 'Name (English)'} value={formData.name} onChange={(v) => handleChange('name', v)} error={errors.name} required />
        <Input label={isRTL ? 'الاسم (عربي)' : 'Name (Arabic)'} value={formData.name_ar} onChange={(v) => handleChange('name_ar', v)} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input label={isRTL ? 'البريد' : 'Email'} type="email" value={formData.email} onChange={(v) => handleChange('email', v)} icon={Mail} />
        <Input label={isRTL ? 'الهاتف' : 'Phone'} value={formData.phone} onChange={(v) => handleChange('phone', v)} icon={Phone} />
      </div>

      <Input label={isRTL ? 'العنوان' : 'Address'} value={formData.address} onChange={(v) => handleChange('address', v)} icon={MapPin} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input label={isRTL ? 'المدينة' : 'City'} value={formData.city} onChange={(v) => handleChange('city', v)} />
        <Input label={isRTL ? 'البلد' : 'Country'} value={formData.country} onChange={(v) => handleChange('country', v)} />
      </div>

      <Input label={isRTL ? 'الموقع الإلكتروني' : 'Website'} value={formData.website} onChange={(v) => handleChange('website', v)} icon={Globe} />

      <TextArea label={isRTL ? 'الوصف' : 'Description'} value={formData.description} onChange={(v) => handleChange('description', v)} rows={3} />

      <label className="flex items-center gap-3">
        <input type="checkbox" checked={formData.is_active} onChange={(e) => handleChange('is_active', e.target.checked)} className="w-4 h-4 rounded text-emerald-600" />
        <span>{isRTL ? 'نشط' : 'Active'}</span>
      </label>

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
        <Button type="submit" loading={loading}>{company ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}</Button>
      </div>
    </form>
  );
};

// ============================================
// Main Companies Page
// ============================================
const Companies = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, active: 0, totalUsers: 0, totalFarms: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await ApiService.getCompanies({ search: searchQuery });
      const items = response.items || response || [];
      setCompanies(items);

      setStats({
        total: items.length,
        active: items.filter(c => c.is_active).length,
        totalUsers: items.reduce((sum, c) => sum + (c.user_count || 0), 0),
        totalFarms: items.reduce((sum, c) => sum + (c.farm_count || 0), 0)
      });
    } catch (err) {
      console.error('Error loading companies:', err);
      setCompanies([
        { id: 1, name: 'AgriTech Solutions', city: 'Riyadh', country: 'Saudi Arabia', is_active: true, user_count: 25, farm_count: 12 },
        { id: 2, name: 'Green Farms Inc', city: 'Dubai', country: 'UAE', is_active: true, user_count: 18, farm_count: 8 }
      ]);
    } finally {
      setLoading(false);
    }
  }, [searchQuery]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try { setFormLoading(true); await ApiService.createCompany(data); setShowCreateModal(false); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try { setFormLoading(true); await ApiService.updateCompany(selectedCompany.id, data); setShowEditModal(false); setSelectedCompany(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try { setFormLoading(true); await ApiService.deleteCompany(selectedCompany.id); setShowDeleteModal(false); setSelectedCompany(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleView = (company) => { setSelectedCompany(company); setShowEditModal(true); };
  const handleEdit = (company) => { setSelectedCompany(company); setShowEditModal(true); };
  const handleDeleteClick = (company) => { setSelectedCompany(company); setShowDeleteModal(true); };

  return (
    <div className="space-y-6">
      <PageHeader title={isRTL ? 'الشركات' : 'Companies'} description={isRTL ? 'إدارة الشركات والمؤسسات' : 'Manage companies and organizations'} icon={Building}>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />{isRTL ? 'شركة جديدة' : 'New Company'}
          </Button>
        </div>
      </PageHeader>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي الشركات' : 'Total Companies'} value={stats.total} icon={Building} iconColor="blue" />
        <StatCard title={isRTL ? 'نشطة' : 'Active'} value={stats.active} icon={Check} iconColor="emerald" />
        <StatCard title={isRTL ? 'المستخدمين' : 'Users'} value={stats.totalUsers} icon={Users} iconColor="purple" />
        <StatCard title={isRTL ? 'المزارع' : 'Farms'} value={stats.totalFarms} icon={Warehouse} iconColor="amber" />
      </div>

      <Card>
        <div className="p-4">
          <div className="relative max-w-xs">
            <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder={isRTL ? 'بحث...' : 'Search...'} className="w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm" />
          </div>
        </div>
      </Card>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-64" />)}
        </div>
      ) : companies.length === 0 ? (
        <Card className="p-12 text-center">
          <Building className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا توجد شركات' : 'No Companies'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {companies.map(company => <CompanyCard key={company.id} company={company} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} />)}
        </div>
      )}

      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة شركة' : 'Add Company'} size="lg">
        <CompanyForm onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedCompany(null); }} title={isRTL ? 'تعديل الشركة' : 'Edit Company'} size="lg">
        <CompanyForm company={selectedCompany} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedCompany(null); }} loading={formLoading} />
      </Modal>

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedCompany(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف الشركة' : 'Delete Company'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedCompany?.name}"؟` : `Delete "${selectedCompany?.name}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedCompany(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Companies;
