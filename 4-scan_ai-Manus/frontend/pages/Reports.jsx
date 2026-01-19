/**
 * Reports Page - Report Generation & Management
 * ==============================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  FileText, Download, Plus, Search, Calendar, RefreshCw, MoreVertical,
  Eye, Trash2, Filter, Clock, Check, AlertTriangle, Loader, File,
  FilePdf, FileSpreadsheet, BarChart3, Warehouse, Leaf
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
const REPORT_TYPES = [
  { value: 'diagnosis', label: 'Diagnosis Report', labelAr: 'تقرير التشخيص', icon: Leaf, color: 'emerald' },
  { value: 'farm', label: 'Farm Report', labelAr: 'تقرير المزرعة', icon: Warehouse, color: 'blue' },
  { value: 'analytics', label: 'Analytics Report', labelAr: 'تقرير التحليلات', icon: BarChart3, color: 'purple' },
  { value: 'custom', label: 'Custom Report', labelAr: 'تقرير مخصص', icon: FileText, color: 'amber' }
];

const STATUS_OPTIONS = [
  { value: 'pending', label: 'Pending', labelAr: 'قيد الانتظار', color: 'amber' },
  { value: 'processing', label: 'Processing', labelAr: 'قيد المعالجة', color: 'blue' },
  { value: 'completed', label: 'Completed', labelAr: 'مكتمل', color: 'emerald' },
  { value: 'failed', label: 'Failed', labelAr: 'فشل', color: 'red' }
];

const FORMAT_OPTIONS = [
  { value: 'pdf', label: 'PDF', icon: FilePdf },
  { value: 'excel', label: 'Excel', icon: FileSpreadsheet },
  { value: 'csv', label: 'CSV', icon: File }
];

// ============================================
// Report Card Component
// ============================================
const ReportCard = ({ report, onView, onDownload, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  
  const type = REPORT_TYPES.find(t => t.value === report.report_type);
  const status = STATUS_OPTIONS.find(s => s.value === report.status);
  const TypeIcon = type?.icon || FileText;

  return (
    <Card hover className="relative">
      {/* Status */}
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
        <Badge variant={status?.color}>
          {report.status === 'processing' && <Loader className="w-3 h-3 mr-1 animate-spin" />}
          {isRTL ? status?.labelAr : status?.label}
        </Badge>
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
                <button onClick={(e) => { e.stopPropagation(); onView(report); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                {report.status === 'completed' && (
                  <button onClick={(e) => { e.stopPropagation(); onDownload(report); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                    <Download className="w-4 h-4" /> {isRTL ? 'تحميل' : 'Download'}
                  </button>
                )}
                <button onClick={(e) => { e.stopPropagation(); onDelete(report); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="p-6 pt-12">
        <div className={`w-12 h-12 rounded-xl bg-${type?.color}-100 dark:bg-${type?.color}-900/30 flex items-center justify-center mb-4`}>
          <TypeIcon className={`w-6 h-6 text-${type?.color}-600`} />
        </div>

        <h3 className="font-semibold text-gray-800 dark:text-white mb-1">{report.title}</h3>
        <p className="text-sm text-gray-500 mb-4">{isRTL ? type?.labelAr : type?.label}</p>

        <div className="flex items-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            {new Date(report.created_at).toLocaleDateString()}
          </div>
          {report.file_size && (
            <div className="flex items-center gap-1">
              <File className="w-4 h-4" />
              {(report.file_size / 1024 / 1024).toFixed(2)} MB
            </div>
          )}
        </div>

        {report.status === 'completed' && (
          <Button variant="outline" size="sm" className="w-full mt-4" onClick={() => onDownload(report)}>
            <Download className="w-4 h-4 mr-2" />
            {isRTL ? 'تحميل' : 'Download'}
          </Button>
        )}
      </div>
    </Card>
  );
};

// ============================================
// Generate Report Modal
// ============================================
const GenerateReportModal = ({ isOpen, onClose, farms, onSubmit, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    title: '',
    report_type: 'diagnosis',
    farm_id: '',
    date_range_start: '',
    date_range_end: '',
    format: 'pdf',
    description: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isRTL ? 'إنشاء تقرير' : 'Generate Report'} size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label={isRTL ? 'عنوان التقرير' : 'Report Title'}
          value={formData.title}
          onChange={(v) => handleChange('title', v)}
          placeholder={isRTL ? 'مثال: تقرير شهر يناير' : 'e.g., January Monthly Report'}
          required
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label={isRTL ? 'نوع التقرير' : 'Report Type'}
            value={formData.report_type}
            onChange={(v) => handleChange('report_type', v)}
            options={REPORT_TYPES}
          />
          <Select
            label={isRTL ? 'المزرعة' : 'Farm'}
            value={formData.farm_id}
            onChange={(v) => handleChange('farm_id', v)}
            options={[
              { value: '', label: isRTL ? 'جميع المزارع' : 'All Farms' },
              ...farms.map(f => ({ value: f.id, label: f.name }))
            ]}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label={isRTL ? 'من تاريخ' : 'Start Date'}
            type="date"
            value={formData.date_range_start}
            onChange={(v) => handleChange('date_range_start', v)}
          />
          <Input
            label={isRTL ? 'إلى تاريخ' : 'End Date'}
            type="date"
            value={formData.date_range_end}
            onChange={(v) => handleChange('date_range_end', v)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {isRTL ? 'صيغة التصدير' : 'Export Format'}
          </label>
          <div className="flex gap-3">
            {FORMAT_OPTIONS.map(format => (
              <button
                key={format.value}
                type="button"
                onClick={() => handleChange('format', format.value)}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-lg border transition-all
                  ${formData.format === format.value
                    ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <format.icon className="w-4 h-4" />
                {format.label}
              </button>
            ))}
          </div>
        </div>

        <TextArea
          label={isRTL ? 'ملاحظات' : 'Notes'}
          value={formData.description}
          onChange={(v) => handleChange('description', v)}
          rows={3}
          placeholder={isRTL ? 'ملاحظات إضافية (اختياري)' : 'Additional notes (optional)'}
        />

        <div className="flex justify-end gap-3 pt-4 border-t">
          <Button type="button" variant="secondary" onClick={onClose}>
            {isRTL ? 'إلغاء' : 'Cancel'}
          </Button>
          <Button type="submit" loading={loading}>
            <FileText className="w-4 h-4 mr-2" />
            {isRTL ? 'إنشاء التقرير' : 'Generate Report'}
          </Button>
        </div>
      </form>
    </Modal>
  );
};

// ============================================
// Main Reports Page
// ============================================
const Reports = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [reports, setReports] = useState([]);
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, thisMonth: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [reportsRes, farmsRes] = await Promise.all([
        ApiService.getReports({ search: searchQuery, type: typeFilter, status: statusFilter }),
        ApiService.getFarms({ limit: 100 })
      ]);

      const items = reportsRes.items || reportsRes || [];
      setReports(items);
      setFarms(farmsRes.items || farmsRes || []);

      const now = new Date();
      const thisMonth = items.filter(r => new Date(r.created_at).getMonth() === now.getMonth()).length;

      setStats({
        total: items.length,
        completed: items.filter(r => r.status === 'completed').length,
        pending: items.filter(r => r.status === 'pending' || r.status === 'processing').length,
        thisMonth
      });
    } catch (err) {
      console.error('Error loading reports:', err);
      // Mock data
      setReports([
        { id: 1, title: 'January Diagnosis Report', report_type: 'diagnosis', status: 'completed', created_at: '2026-01-15', file_size: 1024000 },
        { id: 2, title: 'Farm Performance Q1', report_type: 'farm', status: 'completed', created_at: '2026-01-10', file_size: 2048000 },
        { id: 3, title: 'Weekly Analytics', report_type: 'analytics', status: 'processing', created_at: '2026-01-19' }
      ]);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, typeFilter, statusFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleGenerate = async (data) => {
    try {
      setFormLoading(true);
      await ApiService.generateReport(data);
      setShowGenerateModal(false);
      loadData();
    } finally {
      setFormLoading(false);
    }
  };

  const handleDownload = async (report) => {
    try {
      const blob = await ApiService.downloadReport(report.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${report.title}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading report:', err);
    }
  };

  const handleDelete = async () => {
    try {
      setFormLoading(true);
      await ApiService.deleteReport(selectedReport.id);
      setShowDeleteModal(false);
      setSelectedReport(null);
      loadData();
    } finally {
      setFormLoading(false);
    }
  };

  const handleView = (report) => {
    console.log('View report:', report);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'التقارير' : 'Reports'}
        description={isRTL ? 'إنشاء وإدارة التقارير' : 'Generate and manage reports'}
        icon={FileText}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowGenerateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'تقرير جديد' : 'New Report'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي التقارير' : 'Total Reports'} value={stats.total} icon={FileText} iconColor="blue" />
        <StatCard title={isRTL ? 'مكتملة' : 'Completed'} value={stats.completed} icon={Check} iconColor="emerald" />
        <StatCard title={isRTL ? 'قيد المعالجة' : 'Processing'} value={stats.pending} icon={Clock} iconColor="amber" />
        <StatCard title={isRTL ? 'هذا الشهر' : 'This Month'} value={stats.thisMonth} icon={Calendar} iconColor="purple" />
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4 flex flex-wrap items-center gap-4">
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
            options={[{ value: '', label: isRTL ? 'كل الأنواع' : 'All Types' }, ...REPORT_TYPES]} />
          <Select value={statusFilter} onChange={setStatusFilter} className="w-40"
            options={[{ value: '', label: isRTL ? 'كل الحالات' : 'All Status' }, ...STATUS_OPTIONS]} />
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-56" />)}
        </div>
      ) : reports.length === 0 ? (
        <Card className="p-12 text-center">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا توجد تقارير' : 'No Reports'}</h3>
          <Button onClick={() => setShowGenerateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إنشاء' : 'Create'}</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {reports.map(report => (
            <ReportCard
              key={report.id}
              report={report}
              onView={handleView}
              onDownload={handleDownload}
              onDelete={() => { setSelectedReport(report); setShowDeleteModal(true); }}
            />
          ))}
        </div>
      )}

      {/* Modals */}
      <GenerateReportModal
        isOpen={showGenerateModal}
        onClose={() => setShowGenerateModal(false)}
        farms={farms}
        onSubmit={handleGenerate}
        loading={formLoading}
      />

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedReport(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف التقرير' : 'Delete Report'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedReport?.title}"؟` : `Delete "${selectedReport?.title}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedReport(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Reports;
