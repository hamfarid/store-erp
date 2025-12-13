/**
 * Modern Invoice Page
 * 
 * A beautiful, professional invoice management page with modern UI/UX.
 */

import React, { useState } from 'react';
import {
  Search,
  Plus,
  Filter,
  Download,
  Eye,
  Edit,
  Trash2,
  FileText,
  Calendar,
  User,
  DollarSign,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  MoreVertical,
  Printer,
  Send,
  ChevronRight,
  ChevronLeft,
  ArrowUpDown,
  RefreshCw
} from 'lucide-react';

// ============================================================================
// Sample Data
// ============================================================================

const sampleInvoices = [
  {
    id: 'INV-2024-001',
    customer: 'شركة الفيصل التجارية',
    date: '2024-12-01',
    dueDate: '2024-12-15',
    amount: 15750,
    paid: 15750,
    status: 'paid',
    items: 8
  },
  {
    id: 'INV-2024-002',
    customer: 'مؤسسة النور للإلكترونيات',
    date: '2024-11-28',
    dueDate: '2024-12-12',
    amount: 8900,
    paid: 5000,
    status: 'partial',
    items: 5
  },
  {
    id: 'INV-2024-003',
    customer: 'أحمد محمد العلي',
    date: '2024-11-25',
    dueDate: '2024-12-09',
    amount: 2340,
    paid: 0,
    status: 'pending',
    items: 3
  },
  {
    id: 'INV-2024-004',
    customer: 'شركة الريادة للتقنية',
    date: '2024-11-20',
    dueDate: '2024-12-04',
    amount: 45000,
    paid: 0,
    status: 'overdue',
    items: 12
  },
  {
    id: 'INV-2024-005',
    customer: 'محمد سعيد الغامدي',
    date: '2024-11-15',
    dueDate: '2024-11-29',
    amount: 6780,
    paid: 6780,
    status: 'paid',
    items: 4
  },
  {
    id: 'INV-2024-006',
    customer: 'مكتبة المعرفة',
    date: '2024-11-10',
    dueDate: '2024-11-24',
    amount: 1200,
    paid: 0,
    status: 'cancelled',
    items: 2
  },
];

// ============================================================================
// Status Badge Component
// ============================================================================

const StatusBadge = ({ status }) => {
  const config = {
    paid: { label: 'مدفوعة', color: 'bg-emerald-100 text-emerald-700', icon: CheckCircle },
    partial: { label: 'مدفوعة جزئياً', color: 'bg-amber-100 text-amber-700', icon: Clock },
    pending: { label: 'قيد الانتظار', color: 'bg-blue-100 text-blue-700', icon: Clock },
    overdue: { label: 'متأخرة', color: 'bg-rose-100 text-rose-700', icon: AlertCircle },
    cancelled: { label: 'ملغاة', color: 'bg-gray-100 text-gray-700', icon: XCircle },
  };

  const { label, color, icon: Icon } = config[status] || config.pending;

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${color}`}>
      <Icon size={12} />
      {label}
    </span>
  );
};

// ============================================================================
// Invoice Row Component
// ============================================================================

const InvoiceRow = ({ invoice, onView, onEdit, onDelete, onPrint, onSend }) => {
  const [showMenu, setShowMenu] = useState(false);
  const remaining = invoice.amount - invoice.paid;
  const paidPercent = (invoice.paid / invoice.amount) * 100;

  return (
    <tr className="hover:bg-gray-50 transition-colors group">
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center">
            <FileText className="text-white" size={18} />
          </div>
          <div>
            <p className="font-semibold text-gray-900">{invoice.id}</p>
            <p className="text-sm text-gray-400">{invoice.items} منتجات</p>
          </div>
        </div>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
            <User className="text-gray-500" size={14} />
          </div>
          <span className="font-medium text-gray-900">{invoice.customer}</span>
        </div>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-2 text-gray-600">
          <Calendar size={14} className="text-gray-400" />
          <span>{new Date(invoice.date).toLocaleDateString('ar-SA')}</span>
        </div>
        <p className="text-xs text-gray-400 mt-0.5">
          استحقاق: {new Date(invoice.dueDate).toLocaleDateString('ar-SA')}
        </p>
      </td>
      <td className="px-6 py-4">
        <p className="font-semibold text-gray-900">{invoice.amount.toLocaleString()} ر.س</p>
        {invoice.status === 'partial' && (
          <div className="mt-1">
            <div className="w-24 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div 
                className="h-full bg-amber-500 rounded-full" 
                style={{ width: `${paidPercent}%` }}
              />
            </div>
            <p className="text-xs text-gray-400 mt-0.5">متبقي: {remaining.toLocaleString()}</p>
          </div>
        )}
      </td>
      <td className="px-6 py-4">
        <StatusBadge status={invoice.status} />
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => onView(invoice)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="عرض"
          >
            <Eye size={16} className="text-gray-500" />
          </button>
          <button
            onClick={() => onEdit(invoice)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="تعديل"
          >
            <Edit size={16} className="text-gray-500" />
          </button>
          <button
            onClick={() => onPrint(invoice)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="طباعة"
          >
            <Printer size={16} className="text-gray-500" />
          </button>
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <MoreVertical size={16} className="text-gray-500" />
            </button>
            {showMenu && (
              <div className="absolute left-0 top-full mt-1 w-48 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-10">
                <button
                  onClick={() => { onSend(invoice); setShowMenu(false); }}
                  className="w-full flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-gray-700"
                >
                  <Send size={16} />
                  <span>إرسال بالبريد</span>
                </button>
                <button
                  onClick={() => { onDelete(invoice); setShowMenu(false); }}
                  className="w-full flex items-center gap-2 px-4 py-2 hover:bg-rose-50 text-rose-600"
                >
                  <Trash2 size={16} />
                  <span>حذف</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </td>
    </tr>
  );
};

// ============================================================================
// Main Invoice Page Component
// ============================================================================

const InvoicePage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [dateRange, setDateRange] = useState('all');

  // Handlers
  const handleView = (invoice) => console.log('View:', invoice);
  const handleEdit = (invoice) => console.log('Edit:', invoice);
  const handleDelete = (invoice) => console.log('Delete:', invoice);
  const handlePrint = (invoice) => console.log('Print:', invoice);
  const handleSend = (invoice) => console.log('Send:', invoice);

  // Calculate stats
  const totalAmount = sampleInvoices.reduce((sum, inv) => sum + inv.amount, 0);
  const totalPaid = sampleInvoices.reduce((sum, inv) => sum + inv.paid, 0);
  const pendingAmount = totalAmount - totalPaid;
  const overdueCount = sampleInvoices.filter(inv => inv.status === 'overdue').length;

  // Filter invoices
  const filteredInvoices = sampleInvoices.filter(invoice => {
    const matchesSearch = 
      invoice.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      invoice.customer.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = selectedStatus === 'all' || invoice.status === selectedStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-8" dir="rtl">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">الفواتير</h1>
            <p className="text-gray-500">إدارة فواتير المبيعات والمشتريات</p>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-l from-teal-500 to-teal-600 text-white font-semibold rounded-xl shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all duration-300">
            <Plus size={20} />
            <span>فاتورة جديدة</span>
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-5 border border-gray-100 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">إجمالي الفواتير</p>
                <p className="text-2xl font-bold text-gray-900">{totalAmount.toLocaleString()} ر.س</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
                <DollarSign className="text-teal-600" size={24} />
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-100 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">المدفوع</p>
                <p className="text-2xl font-bold text-emerald-600">{totalPaid.toLocaleString()} ر.س</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
                <CheckCircle className="text-emerald-600" size={24} />
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-100 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">قيد الانتظار</p>
                <p className="text-2xl font-bold text-amber-600">{pendingAmount.toLocaleString()} ر.س</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center">
                <Clock className="text-amber-600" size={24} />
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-100 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm mb-1">متأخرة</p>
                <p className="text-2xl font-bold text-rose-600">{overdueCount}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
                <AlertCircle className="text-rose-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-4 flex-1 w-full lg:w-auto">
              {/* Search */}
              <div className="relative flex-1 max-w-md">
                <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="بحث برقم الفاتورة أو اسم العميل..."
                  className="w-full pr-12 pl-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-teal-500 transition-all"
                />
              </div>

              {/* Status Filter */}
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-teal-500"
              >
                <option value="all">جميع الحالات</option>
                <option value="paid">مدفوعة</option>
                <option value="partial">مدفوعة جزئياً</option>
                <option value="pending">قيد الانتظار</option>
                <option value="overdue">متأخرة</option>
                <option value="cancelled">ملغاة</option>
              </select>

              {/* Date Range */}
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="px-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-teal-500"
              >
                <option value="all">جميع التواريخ</option>
                <option value="today">اليوم</option>
                <option value="week">هذا الأسبوع</option>
                <option value="month">هذا الشهر</option>
                <option value="quarter">هذا الربع</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <button className="flex items-center gap-2 px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
                <Download size={18} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">تصدير</span>
              </button>
              <button className="flex items-center gap-2 px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
                <RefreshCw size={18} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">تحديث</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm" data-testid="invoices-table">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">
                <button className="flex items-center gap-1 hover:text-teal-600">
                  رقم الفاتورة
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">العميل</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">
                <button className="flex items-center gap-1 hover:text-teal-600">
                  التاريخ
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">
                <button className="flex items-center gap-1 hover:text-teal-600">
                  المبلغ
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الحالة</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">إجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredInvoices.map(invoice => (
              <InvoiceRow
                key={invoice.id}
                invoice={invoice}
                onView={handleView}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onPrint={handlePrint}
                onSend={handleSend}
              />
            ))}
          </tbody>
        </table>

        {/* Empty State */}
        {filteredInvoices.length === 0 && (
          <div className="py-16 text-center">
            <FileText className="mx-auto text-gray-300 mb-4" size={48} />
            <h3 className="text-lg font-semibold text-gray-900 mb-1">لا توجد فواتير</h3>
            <p className="text-gray-500">لم يتم العثور على فواتير تطابق معايير البحث</p>
          </div>
        )}
      </div>

      {/* Pagination */}
      <div className="mt-8 flex items-center justify-between">
        <p className="text-gray-500 text-sm">
          عرض 1-{filteredInvoices.length} من {filteredInvoices.length} فاتورة
        </p>
        <div className="flex items-center gap-2">
          <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50" disabled>
            <ChevronRight size={18} className="text-gray-500" />
          </button>
          <button className="w-10 h-10 bg-teal-600 text-white rounded-lg font-medium">1</button>
          <button className="w-10 h-10 hover:bg-gray-100 rounded-lg font-medium text-gray-700">2</button>
          <button className="w-10 h-10 hover:bg-gray-100 rounded-lg font-medium text-gray-700">3</button>
          <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <ChevronLeft size={18} className="text-gray-500" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default InvoicePage;

