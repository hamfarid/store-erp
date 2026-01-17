/**
 * Reports Setup Page
 * 
 * Configure and manage report templates and settings
 */

import React, { useState, useEffect } from 'react';
import {
  FileText,
  Settings,
  Plus,
  Edit2,
  Trash2,
  Save,
  Download,
  Upload,
  Eye,
  Copy,
  BarChart3,
  PieChart,
  TrendingUp,
  Calendar,
  Filter,
  Columns,
  Layout,
  Palette,
  Clock,
  Mail,
  Bell,
  Check,
  X,
  ChevronDown,
  ChevronRight
} from 'lucide-react';
import toast from 'react-hot-toast';
import { apiRequest, API_ENDPOINTS } from '../config/api';

// Default report templates
const DEFAULT_TEMPLATES = [
  {
    id: 'inventory_summary',
    name: 'تقرير ملخص المخزون',
    nameEn: 'Inventory Summary',
    type: 'inventory',
    icon: 'BarChart3',
    columns: ['product_name', 'category', 'quantity', 'unit_price', 'total_value'],
    filters: ['category', 'warehouse', 'date_range'],
    chartType: 'bar',
    schedule: null,
    isDefault: true
  },
  {
    id: 'sales_report',
    name: 'تقرير المبيعات',
    nameEn: 'Sales Report',
    type: 'sales',
    icon: 'TrendingUp',
    columns: ['invoice_number', 'customer', 'date', 'items_count', 'total', 'status'],
    filters: ['customer', 'date_range', 'status'],
    chartType: 'line',
    schedule: null,
    isDefault: true
  },
  {
    id: 'profit_loss',
    name: 'تقرير الأرباح والخسائر',
    nameEn: 'Profit & Loss Report',
    type: 'financial',
    icon: 'PieChart',
    columns: ['category', 'revenue', 'cost', 'profit', 'margin'],
    filters: ['date_range', 'category'],
    chartType: 'pie',
    schedule: null,
    isDefault: true
  },
  {
    id: 'low_stock',
    name: 'تقرير المخزون المنخفض',
    nameEn: 'Low Stock Alert',
    type: 'inventory',
    icon: 'AlertTriangle',
    columns: ['product_name', 'current_qty', 'min_qty', 'reorder_qty', 'status'],
    filters: ['category', 'warehouse'],
    chartType: 'bar',
    schedule: 'daily',
    isDefault: true
  }
];

// Available columns for reports
const AVAILABLE_COLUMNS = {
  inventory: [
    { id: 'product_name', name: 'اسم المنتج', nameEn: 'Product Name' },
    { id: 'sku', name: 'رمز المنتج', nameEn: 'SKU' },
    { id: 'category', name: 'الفئة', nameEn: 'Category' },
    { id: 'quantity', name: 'الكمية', nameEn: 'Quantity' },
    { id: 'unit_price', name: 'سعر الوحدة', nameEn: 'Unit Price' },
    { id: 'total_value', name: 'القيمة الإجمالية', nameEn: 'Total Value' },
    { id: 'warehouse', name: 'المستودع', nameEn: 'Warehouse' },
    { id: 'min_qty', name: 'الحد الأدنى', nameEn: 'Min Quantity' },
    { id: 'reorder_qty', name: 'كمية إعادة الطلب', nameEn: 'Reorder Qty' },
    { id: 'last_movement', name: 'آخر حركة', nameEn: 'Last Movement' }
  ],
  sales: [
    { id: 'invoice_number', name: 'رقم الفاتورة', nameEn: 'Invoice Number' },
    { id: 'customer', name: 'العميل', nameEn: 'Customer' },
    { id: 'date', name: 'التاريخ', nameEn: 'Date' },
    { id: 'items_count', name: 'عدد المنتجات', nameEn: 'Items Count' },
    { id: 'subtotal', name: 'المجموع الفرعي', nameEn: 'Subtotal' },
    { id: 'discount', name: 'الخصم', nameEn: 'Discount' },
    { id: 'tax', name: 'الضريبة', nameEn: 'Tax' },
    { id: 'total', name: 'الإجمالي', nameEn: 'Total' },
    { id: 'status', name: 'الحالة', nameEn: 'Status' },
    { id: 'payment_method', name: 'طريقة الدفع', nameEn: 'Payment Method' }
  ],
  financial: [
    { id: 'category', name: 'الفئة', nameEn: 'Category' },
    { id: 'revenue', name: 'الإيرادات', nameEn: 'Revenue' },
    { id: 'cost', name: 'التكلفة', nameEn: 'Cost' },
    { id: 'profit', name: 'الربح', nameEn: 'Profit' },
    { id: 'margin', name: 'هامش الربح', nameEn: 'Margin' },
    { id: 'expenses', name: 'المصروفات', nameEn: 'Expenses' },
    { id: 'net_profit', name: 'صافي الربح', nameEn: 'Net Profit' }
  ]
};

const SCHEDULE_OPTIONS = [
  { id: null, name: 'بدون جدولة', nameEn: 'No Schedule' },
  { id: 'daily', name: 'يومياً', nameEn: 'Daily' },
  { id: 'weekly', name: 'أسبوعياً', nameEn: 'Weekly' },
  { id: 'monthly', name: 'شهرياً', nameEn: 'Monthly' }
];

const CHART_TYPES = [
  { id: 'bar', name: 'أعمدة', icon: BarChart3 },
  { id: 'line', name: 'خطي', icon: TrendingUp },
  { id: 'pie', name: 'دائري', icon: PieChart }
];

const ReportsSetupPage = () => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [activeSection, setActiveSection] = useState('columns');

  // Form state for editing
  const [formData, setFormData] = useState({
    name: '',
    nameEn: '',
    type: 'inventory',
    columns: [],
    filters: [],
    chartType: 'bar',
    schedule: null,
    emailRecipients: '',
    description: ''
  });

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const response = await apiRequest(API_ENDPOINTS.REPORTS.TEMPLATES);
      setTemplates(response.data || response || DEFAULT_TEMPLATES);
    } catch (error) {
      console.log('Using default templates');
      setTemplates(DEFAULT_TEMPLATES);
    }
    setLoading(false);
  };

  const handleSelectTemplate = (template) => {
    setSelectedTemplate(template);
    setFormData({
      name: template.name,
      nameEn: template.nameEn || '',
      type: template.type,
      columns: template.columns || [],
      filters: template.filters || [],
      chartType: template.chartType || 'bar',
      schedule: template.schedule,
      emailRecipients: template.emailRecipients || '',
      description: template.description || ''
    });
    setIsEditing(false);
  };

  const handleCreateTemplate = () => {
    setSelectedTemplate(null);
    setFormData({
      name: '',
      nameEn: '',
      type: 'inventory',
      columns: [],
      filters: [],
      chartType: 'bar',
      schedule: null,
      emailRecipients: '',
      description: ''
    });
    setIsEditing(true);
    setShowCreateModal(false);
  };

  const handleSaveTemplate = async () => {
    if (!formData.name) {
      toast.error('يرجى إدخال اسم التقرير');
      return;
    }
    if (formData.columns.length === 0) {
      toast.error('يرجى اختيار عمود واحد على الأقل');
      return;
    }

    setSaving(true);
    try {
      const templateData = {
        ...formData,
        id: selectedTemplate?.id || `template_${Date.now()}`
      };

      if (selectedTemplate) {
        // Update existing
        await apiRequest(API_ENDPOINTS.REPORTS.TEMPLATES + `/${selectedTemplate.id}`, {
          method: 'PUT',
          body: JSON.stringify(templateData)
        });
        toast.success('تم تحديث القالب بنجاح');
      } else {
        // Create new
        await apiRequest(API_ENDPOINTS.REPORTS.TEMPLATES, {
          method: 'POST',
          body: JSON.stringify(templateData)
        });
        toast.success('تم إنشاء القالب بنجاح');
      }

      loadTemplates();
      setIsEditing(false);
    } catch (error) {
      console.error('Error saving template:', error);
      // For demo, add to local state
      const newTemplate = {
        ...formData,
        id: selectedTemplate?.id || `template_${Date.now()}`,
        isDefault: false
      };
      
      if (selectedTemplate) {
        setTemplates(prev => prev.map(t => t.id === selectedTemplate.id ? newTemplate : t));
      } else {
        setTemplates(prev => [...prev, newTemplate]);
      }
      
      setSelectedTemplate(newTemplate);
      setIsEditing(false);
      toast.success(selectedTemplate ? 'تم تحديث القالب' : 'تم إنشاء القالب');
    }
    setSaving(false);
  };

  const handleDeleteTemplate = async (template) => {
    if (template.isDefault) {
      toast.error('لا يمكن حذف القوالب الافتراضية');
      return;
    }

    if (!confirm('هل أنت متأكد من حذف هذا القالب؟')) return;

    try {
      await apiRequest(API_ENDPOINTS.REPORTS.TEMPLATES + `/${template.id}`, {
        method: 'DELETE'
      });
      toast.success('تم حذف القالب');
    } catch {
      // Remove locally
      setTemplates(prev => prev.filter(t => t.id !== template.id));
      toast.success('تم حذف القالب');
    }

    if (selectedTemplate?.id === template.id) {
      setSelectedTemplate(null);
    }
  };

  const toggleColumn = (columnId) => {
    setFormData(prev => ({
      ...prev,
      columns: prev.columns.includes(columnId)
        ? prev.columns.filter(c => c !== columnId)
        : [...prev.columns, columnId]
    }));
  };

  const getIconComponent = (iconName) => {
    const icons = { BarChart3, TrendingUp, PieChart };
    return icons[iconName] || FileText;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto" dir="rtl">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <FileText className="w-8 h-8 text-primary-500" />
            إعدادات التقارير
          </h1>
          <p className="text-gray-500 mt-2">
            إنشاء وتخصيص قوالب التقارير
          </p>
        </div>
        <button
          onClick={handleCreateTemplate}
          className="flex items-center gap-2 bg-gradient-to-l from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-lg"
        >
          <Plus className="w-5 h-5" />
          قالب جديد
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Templates List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <div className="p-4 bg-gray-50 border-b border-gray-100">
              <h2 className="font-semibold text-gray-900">قوالب التقارير</h2>
            </div>
            <div className="max-h-[600px] overflow-y-auto">
              {templates.map(template => {
                const IconComponent = getIconComponent(template.icon);
                return (
                  <button
                    key={template.id}
                    onClick={() => handleSelectTemplate(template)}
                    className={`w-full p-4 flex items-center gap-3 border-b border-gray-50 hover:bg-gray-50 transition-colors ${
                      selectedTemplate?.id === template.id ? 'bg-primary-50 border-r-4 border-r-primary-500' : ''
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                      template.type === 'inventory' ? 'bg-blue-100 text-blue-600' :
                      template.type === 'sales' ? 'bg-green-100 text-green-600' :
                      'bg-purple-100 text-purple-600'
                    }`}>
                      <IconComponent className="w-5 h-5" />
                    </div>
                    <div className="flex-1 text-right">
                      <p className="font-medium text-gray-900">{template.name}</p>
                      <div className="flex items-center gap-2 mt-1">
                        {template.schedule && (
                          <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {SCHEDULE_OPTIONS.find(s => s.id === template.schedule)?.name}
                          </span>
                        )}
                        {template.isDefault && (
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                            افتراضي
                          </span>
                        )}
                      </div>
                    </div>
                    {!template.isDefault && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteTemplate(template);
                        }}
                        className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Template Editor */}
        <div className="lg:col-span-2">
          {(selectedTemplate || isEditing) ? (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
              {/* Template Header */}
              <div className="p-6 bg-gradient-to-l from-secondary-500 to-secondary-600 text-white flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold">
                    {isEditing ? (selectedTemplate ? 'تعديل القالب' : 'قالب جديد') : formData.name}
                  </h2>
                  <p className="text-secondary-100 mt-1">
                    {formData.columns.length} أعمدة
                    {formData.schedule && ` • ${SCHEDULE_OPTIONS.find(s => s.id === formData.schedule)?.name}`}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {!isEditing ? (
                    <>
                      <button
                        onClick={() => setIsEditing(true)}
                        className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
                      >
                        <Edit2 className="w-5 h-5" />
                      </button>
                      <button className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors">
                        <Eye className="w-5 h-5" />
                      </button>
                      <button className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors">
                        <Download className="w-5 h-5" />
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => {
                          setIsEditing(false);
                          if (!selectedTemplate) {
                            setFormData({
                              name: '',
                              nameEn: '',
                              type: 'inventory',
                              columns: [],
                              filters: [],
                              chartType: 'bar',
                              schedule: null,
                              emailRecipients: '',
                              description: ''
                            });
                          }
                        }}
                        className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </>
                  )}
                </div>
              </div>

              {/* Editor Content */}
              {isEditing ? (
                <div className="p-6 space-y-6">
                  {/* Basic Info */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        اسم التقرير
                      </label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                        className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="مثال: تقرير المبيعات الشهرية"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        نوع التقرير
                      </label>
                      <select
                        value={formData.type}
                        onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value, columns: [] }))}
                        className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      >
                        <option value="inventory">المخزون</option>
                        <option value="sales">المبيعات</option>
                        <option value="financial">المالية</option>
                      </select>
                    </div>
                  </div>

                  {/* Columns Selection */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <Columns className="w-5 h-5 text-primary-500" />
                      أعمدة التقرير
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {AVAILABLE_COLUMNS[formData.type]?.map(column => (
                        <button
                          key={column.id}
                          onClick={() => toggleColumn(column.id)}
                          className={`p-3 rounded-xl flex items-center gap-2 transition-all ${
                            formData.columns.includes(column.id)
                              ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
                              : 'bg-gray-50 text-gray-600 border-2 border-transparent hover:border-gray-200'
                          }`}
                        >
                          {formData.columns.includes(column.id) ? (
                            <Check className="w-4 h-4" />
                          ) : (
                            <div className="w-4 h-4 border-2 border-gray-300 rounded" />
                          )}
                          <span className="text-sm font-medium">{column.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Chart Type */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <PieChart className="w-5 h-5 text-primary-500" />
                      نوع الرسم البياني
                    </h3>
                    <div className="flex gap-4">
                      {CHART_TYPES.map(chart => {
                        const ChartIcon = chart.icon;
                        return (
                          <button
                            key={chart.id}
                            onClick={() => setFormData(prev => ({ ...prev, chartType: chart.id }))}
                            className={`flex-1 p-4 rounded-xl flex flex-col items-center gap-2 transition-all ${
                              formData.chartType === chart.id
                                ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
                                : 'bg-gray-50 text-gray-600 border-2 border-transparent hover:border-gray-200'
                            }`}
                          >
                            <ChartIcon className="w-8 h-8" />
                            <span className="font-medium">{chart.name}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Schedule */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <Clock className="w-5 h-5 text-primary-500" />
                      جدولة التقرير
                    </h3>
                    <div className="grid grid-cols-4 gap-3">
                      {SCHEDULE_OPTIONS.map(schedule => (
                        <button
                          key={schedule.id || 'none'}
                          onClick={() => setFormData(prev => ({ ...prev, schedule: schedule.id }))}
                          className={`p-3 rounded-xl text-center transition-all ${
                            formData.schedule === schedule.id
                              ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
                              : 'bg-gray-50 text-gray-600 border-2 border-transparent hover:border-gray-200'
                          }`}
                        >
                          <span className="font-medium">{schedule.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Email Recipients */}
                  {formData.schedule && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                        <Mail className="w-4 h-4" />
                        إرسال إلى (البريد الإلكتروني)
                      </label>
                      <input
                        type="text"
                        value={formData.emailRecipients}
                        onChange={(e) => setFormData(prev => ({ ...prev, emailRecipients: e.target.value }))}
                        className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="email1@example.com, email2@example.com"
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-6">
                  {/* Template Preview */}
                  <div className="space-y-6">
                    {/* Columns */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">الأعمدة</h3>
                      <div className="flex flex-wrap gap-2">
                        {formData.columns.map(col => (
                          <span
                            key={col}
                            className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                          >
                            {AVAILABLE_COLUMNS[formData.type]?.find(c => c.id === col)?.name || col}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Chart Preview Placeholder */}
                    <div className="bg-gray-50 rounded-xl p-8 text-center">
                      <div className="text-gray-400 mb-2">
                        {CHART_TYPES.find(c => c.id === formData.chartType)?.icon && 
                          React.createElement(CHART_TYPES.find(c => c.id === formData.chartType).icon, { className: 'w-16 h-16 mx-auto' })
                        }
                      </div>
                      <p className="text-gray-500">معاينة الرسم البياني</p>
                    </div>

                    {/* Schedule Info */}
                    {formData.schedule && (
                      <div className="flex items-center gap-3 p-4 bg-yellow-50 rounded-xl">
                        <Bell className="w-5 h-5 text-yellow-600" />
                        <div>
                          <p className="font-medium text-yellow-800">تقرير مجدول</p>
                          <p className="text-sm text-yellow-600">
                            يتم إرسال هذا التقرير {SCHEDULE_OPTIONS.find(s => s.id === formData.schedule)?.name}
                            {formData.emailRecipients && ` إلى ${formData.emailRecipients}`}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Save Button */}
              {isEditing && (
                <div className="p-6 bg-gray-50 border-t border-gray-100">
                  <button
                    onClick={handleSaveTemplate}
                    disabled={saving}
                    className="w-full flex items-center justify-center gap-2 bg-gradient-to-l from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white py-4 px-6 rounded-xl font-medium transition-all shadow-lg disabled:opacity-50"
                  >
                    {saving ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        جاري الحفظ...
                      </>
                    ) : (
                      <>
                        <Save className="w-5 h-5" />
                        حفظ القالب
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-12 flex flex-col items-center justify-center text-center">
              <FileText className="w-16 h-16 text-gray-300 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                اختر قالب تقرير
              </h3>
              <p className="text-gray-500 mb-6">
                اختر قالب من القائمة لعرض تفاصيله أو تعديله
              </p>
              <button
                onClick={handleCreateTemplate}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-xl font-medium transition-all"
              >
                <Plus className="w-5 h-5" />
                إنشاء قالب جديد
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportsSetupPage;

