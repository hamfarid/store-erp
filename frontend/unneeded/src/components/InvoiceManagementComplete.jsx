import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, Upload, Settings, CheckCircle, XCircle, AlertTriangle, Package, User, Calendar, Clock, FileText, DollarSign, Printer
} from 'lucide-react';

const InvoiceManagementComplete = () => {
  const [invoices, setInvoices] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [invoiceItems, setInvoiceItems] = useState([]);

  // بيانات تجريبية للفواتير
  const demoInvoices = [
    {
      id: 1,
      invoice_number: 'INV-2024-001',
      invoice_type: 'sales',
      customer_id: 1,
      customer_name: 'مزرعة الأمل الزراعية',
      supplier_id: null,
      supplier_name: null,
      warehouse_id: 1,
      warehouse_name: 'المخزن الرئيسي',
      invoice_date: '2024-07-08',
      due_date: '2024-07-23',
      subtotal: 2550.00,
      tax_amount: 382.50,
      discount_amount: 100.00,
      total_amount: 2832.50,
      paid_amount: 1500.00,
      status: 'partial',
      currency: 'EGP',
      exchange_rate: 1,
      payment_terms: 'نقداً خلال 15 يوم',
      notes: 'فاتورة بيع بذور طماطم هجين',
      user_name: 'أحمد محمد',
      created_at: '2024-07-08 10:30:00'
    },
    {
      id: 2,
      invoice_number: 'PO-2024-001',
      invoice_type: 'purchase',
      customer_id: null,
      customer_name: null,
      supplier_id: 1,
      supplier_name: 'شركة البذور المصرية',
      warehouse_id: 1,
      warehouse_name: 'المخزن الرئيسي',
      invoice_date: '2024-07-07',
      due_date: '2024-07-22',
      subtotal: 5100.00,
      tax_amount: 765.00,
      discount_amount: 200.00,
      total_amount: 5665.00,
      paid_amount: 5665.00,
      status: 'paid',
      currency: 'EGP',
      exchange_rate: 1,
      payment_terms: 'نقداً عند الاستلام',
      notes: 'شراء بذور طماطم وخيار',
      user_name: 'فاطمة أحمد',
      created_at: '2024-07-07 14:15:00'
    },
    {
      id: 3,
      invoice_number: 'INV-2024-002',
      invoice_type: 'sales',
      customer_id: 2,
      customer_name: 'شركة الزراعة الحديثة',
      supplier_id: null,
      supplier_name: null,
      warehouse_id: 2,
      warehouse_name: 'مخزن الإسكندرية',
      invoice_date: '2024-07-06',
      due_date: '2024-07-21',
      subtotal: 3400.00,
      tax_amount: 510.00,
      discount_amount: 0.00,
      total_amount: 3910.00,
      paid_amount: 0.00,
      status: 'pending',
      currency: 'EGP',
      exchange_rate: 1,
      payment_terms: 'آجل 15 يوم',
      notes: 'فاتورة بيع أسمدة ومبيدات',
      user_name: 'محمد علي',
      created_at: '2024-07-06 16:45:00'
    }
  ];

  // بيانات تجريبية لتفاصيل الفواتير
  const demoInvoiceItems = {
    1: [
      {
        id: 1,
        product_id: 1,
        product_name: 'بذور طماطم هجين',
        product_sku: 'TOM-HYB-001',
        quantity: 100,
        unit_price: 25.50,
        total_price: 2550.00,
        lot_number: 'LOT-2024-001',
        notes: 'بذور عالية الجودة'
      }
    ],
    2: [
      {
        id: 2,
        product_id: 1,
        product_name: 'بذور طماطم هجين',
        product_sku: 'TOM-HYB-001',
        quantity: 200,
        unit_price: 25.50,
        total_price: 5100.00,
        lot_number: 'LOT-2024-001',
        notes: 'شحنة جديدة'
      }
    ],
    3: [
      {
        id: 3,
        product_id: 2,
        product_name: 'سماد NPK متوازن',
        product_sku: 'NPK-BAL-001',
        quantity: 50,
        unit_price: 45.00,
        total_price: 2250.00,
        lot_number: 'LOT-2024-002',
        notes: 'سماد متوازن'
      },
      {
        id: 4,
        product_id: 3,
        product_name: 'مبيد حشري طبيعي',
        product_sku: 'INS-NAT-001',
        quantity: 15,
        unit_price: 85.00,
        total_price: 1275.00,
        lot_number: 'LOT-2024-003',
        notes: 'مبيد طبيعي آمن'
      }
    ]
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      // محاكاة تحميل البيانات
      setTimeout(() => {
        setInvoices(demoInvoices);
        setCustomers([
          { id: 1, name: 'مزرعة الأمل الزراعية', phone: '01234567890' },
          { id: 2, name: 'شركة الزراعة الحديثة', phone: '01098765432' }
        ]);
        setSuppliers([
          { id: 1, name: 'شركة البذور المصرية', phone: '02123456789' },
          { id: 2, name: 'مصنع الأسمدة الحديث', phone: '02987654321' }
        ]);
        setProducts([
          { id: 1, name: 'بذور طماطم هجين', sku: 'TOM-HYB-001', price: 25.50 },
          { id: 2, name: 'سماد NPK متوازن', sku: 'NPK-BAL-001', price: 45.00 },
          { id: 3, name: 'مبيد حشري طبيعي', sku: 'INS-NAT-001', price: 85.00 }
        ]);
        setWarehouses([
          { id: 1, name: 'المخزن الرئيسي' },
          { id: 2, name: 'مخزن الإسكندرية' }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      setLoading(false);
    }
  };

  const filteredInvoices = invoices.filter(invoice => {
    const matchesSearch = invoice.invoice_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (invoice.customer_name && invoice.customer_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
                         (invoice.supplier_name && invoice.supplier_name.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesType = !typeFilter || invoice.invoice_type === typeFilter;
    const matchesStatus = !statusFilter || invoice.status === statusFilter;

    let matchesDate = true;
    if (dateFrom || dateTo) {
      const invoiceDate = new Date(invoice.invoice_date);
      if (dateFrom) matchesDate = matchesDate && invoiceDate >= new Date(dateFrom);
      if (dateTo) matchesDate = matchesDate && invoiceDate <= new Date(dateTo);
    }

    return matchesSearch && matchesType && matchesStatus && matchesDate;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid': return 'bg-primary/20 text-green-800';
      case 'partial': return 'bg-accent/20 text-yellow-800';
      case 'pending': return 'bg-destructive/20 text-red-800';
      case 'draft': return 'bg-muted text-foreground';
      case 'cancelled': return 'bg-destructive/20 text-red-800';
      default: return 'bg-primary-100 text-primary-800';
    }
  };

  const getStatusText = (status) => {
    const statusMap = {
      'paid': 'مدفوعة',
      'partial': 'مدفوعة جزئياً',
      'pending': 'معلقة',
      'draft': 'مسودة',
      'cancelled': 'ملغية'
    };
    return statusMap[status] || status;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'paid': return <CheckCircle className="h-4 w-4" />;
      case 'partial': return <Clock className="h-4 w-4" />;
      case 'pending': return <AlertTriangle className="h-4 w-4" />;
      case 'cancelled': return <XCircle className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  const viewInvoice = (invoice) => {
    setSelectedInvoice(invoice);
    setInvoiceItems(demoInvoiceItems[invoice.id] || []);
    setShowViewModal(true);
  };

  const printInvoice = (invoice) => {
    // محاكاة طباعة الفاتورة
    alert(`سيتم طباعة الفاتورة ${invoice.invoice_number}`);
  };

  const exportInvoice = (invoice, format) => {
    // محاكاة تصدير الفاتورة
    alert(`سيتم تصدير الفاتورة ${invoice.invoice_number} بصيغة ${format}`);
  };

  // حساب الإحصائيات
  const totalInvoices = invoices.length;
  const salesInvoices = invoices.filter(inv => inv.invoice_type === 'sales').length;
  const purchaseInvoices = invoices.filter(inv => inv.invoice_type === 'purchase').length;
  const totalAmount = invoices.reduce((sum, inv) => sum + inv.total_amount, 0);
  const paidAmount = invoices.reduce((sum, inv) => sum + inv.paid_amount, 0);
  const pendingAmount = totalAmount - paidAmount;

  // مكون عرض تفاصيل الفاتورة
  const InvoiceViewModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold">تفاصيل الفاتورة {selectedInvoice?.invoice_number}</h3>
          <div className="flex space-x-2 space-x-reverse">
            <button
              onClick={() => printInvoice(selectedInvoice)}
              className="bg-gray-600 text-white px-3 py-1 rounded-md hover:bg-gray-700 flex items-center"
            >
              <Printer className="h-4 w-4 ml-1" />
              طباعة
            </button>
            <button
              onClick={() => exportInvoice(selectedInvoice, 'PDF')}
              className="bg-destructive text-white px-3 py-1 rounded-md hover:bg-red-700 flex items-center"
            >
              <Download className="h-4 w-4 ml-1" />
              PDF
            </button>
            <button
              onClick={() => setShowViewModal(false)}
              className="text-gray-500 hover:text-foreground"
            >
              ✕
            </button>
          </div>
        </div>

        {selectedInvoice && (
          <div className="space-y-6">
            {/* معلومات الفاتورة الأساسية */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-muted/50 p-4 rounded-lg">
                <h4 className="font-semibold mb-3">معلومات الفاتورة</h4>
                <div className="space-y-2 text-sm">
                  <div><span className="font-medium">رقم الفاتورة:</span> {selectedInvoice.invoice_number}</div>
                  <div><span className="font-medium">النوع:</span> {selectedInvoice.invoice_type === 'sales' ? 'مبيعات' : 'مشتريات'}</div>
                  <div><span className="font-medium">التاريخ:</span> {selectedInvoice.invoice_date}</div>
                  <div><span className="font-medium">تاريخ الاستحقاق:</span> {selectedInvoice.due_date}</div>
                  <div><span className="font-medium">المخزن:</span> {selectedInvoice.warehouse_name}</div>
                  <div className="flex items-center">
                    <span className="font-medium ml-2">الحالة:</span>
                    <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedInvoice.status)}`}>
                      {getStatusIcon(selectedInvoice.status)}
                      <span className="mr-1">{getStatusText(selectedInvoice.status)}</span>
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-muted/50 p-4 rounded-lg">
                <h4 className="font-semibold mb-3">
                  {selectedInvoice.invoice_type === 'sales' ? 'معلومات العميل' : 'معلومات المورد'}
                </h4>
                <div className="space-y-2 text-sm">
                  <div><span className="font-medium">الاسم:</span> {selectedInvoice.customer_name || selectedInvoice.supplier_name}</div>
                  <div><span className="font-medium">شروط الدفع:</span> {selectedInvoice.payment_terms}</div>
                  <div><span className="font-medium">العملة:</span> {selectedInvoice.currency}</div>
                  <div><span className="font-medium">المستخدم:</span> {selectedInvoice.user_name}</div>
                </div>
              </div>
            </div>

            {/* تفاصيل الأصناف */}
            <div>
              <h4 className="font-semibold mb-3">تفاصيل الأصناف</h4>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 border border-border rounded-lg">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">المنتج</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">الكمية</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">سعر الوحدة</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجمالي</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">رقم اللوت</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {invoiceItems.map((item, index) => (
                      <tr key={index}>
                        <td className="px-4 py-3">
                          <div className="text-sm font-medium text-foreground">{item.product_name}</div>
                          <div className="text-sm text-gray-500">{item.product_sku}</div>
                        </td>
                        <td className="px-4 py-3 text-sm text-foreground">{item.quantity.toLocaleString()}</td>
                        <td className="px-4 py-3 text-sm text-foreground">{item.unit_price.toLocaleString()} ج.م</td>
                        <td className="px-4 py-3 text-sm font-medium text-foreground">{item.total_price.toLocaleString()} ج.م</td>
                        <td className="px-4 py-3 text-sm text-gray-500">{item.lot_number}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* ملخص المبالغ */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <h4 className="font-semibold mb-3">ملخص المبالغ</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>المجموع الفرعي:</span>
                    <span className="font-medium">{selectedInvoice.subtotal.toLocaleString()} ج.م</span>
                  </div>
                  <div className="flex justify-between">
                    <span>الضريبة:</span>
                    <span className="font-medium">{selectedInvoice.tax_amount.toLocaleString()} ج.م</span>
                  </div>
                  <div className="flex justify-between">
                    <span>الخصم:</span>
                    <span className="font-medium">-{selectedInvoice.discount_amount.toLocaleString()} ج.م</span>
                  </div>
                  <div className="flex justify-between border-t pt-2 font-bold">
                    <span>الإجمالي:</span>
                    <span>{selectedInvoice.total_amount.toLocaleString()} ج.م</span>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>المدفوع:</span>
                    <span className="font-medium text-primary">{selectedInvoice.paid_amount.toLocaleString()} ج.م</span>
                  </div>
                  <div className="flex justify-between">
                    <span>المتبقي:</span>
                    <span className="font-medium text-destructive">{(selectedInvoice.total_amount - selectedInvoice.paid_amount).toLocaleString()} ج.م</span>
                  </div>
                </div>
              </div>
            </div>

            {/* الملاحظات */}
            {selectedInvoice.notes && (
              <div className="bg-muted/50 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">الملاحظات</h4>
                <p className="text-sm text-foreground">{selectedInvoice.notes}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="p-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة الفواتير المتكاملة</h1>
          <p className="text-muted-foreground">إدارة شاملة لفواتير المبيعات والمشتريات</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 flex items-center"
        >
          <Plus className="h-4 w-4 ml-2" />
          إنشاء فاتورة جديدة
        </button>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-primary-500">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الفواتير</p>
              <p className="text-2xl font-bold text-foreground">{totalInvoices}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-green-500">
          <div className="flex items-center">
            <DollarSign className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي القيمة</p>
              <p className="text-2xl font-bold text-foreground">{totalAmount.toLocaleString()} ج.م</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-green-500">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المدفوع</p>
              <p className="text-2xl font-bold text-foreground">{paidAmount.toLocaleString()} ج.م</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border-r-4 border-red-500">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المعلق</p>
              <p className="text-2xl font-bold text-foreground">{pendingAmount.toLocaleString()} ج.م</p>
            </div>
          </div>
        </div>
      </div>

      {/* أدوات البحث والفلترة */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="البحث برقم الفاتورة أو العميل..."
              className="w-full pr-10 pl-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
          >
            <option value="">جميع الأنواع</option>
            <option value="sales">مبيعات</option>
            <option value="purchase">مشتريات</option>
          </select>

          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">جميع الحالات</option>
            <option value="paid">مدفوعة</option>
            <option value="partial">مدفوعة جزئياً</option>
            <option value="pending">معلقة</option>
            <option value="draft">مسودة</option>
            <option value="cancelled">ملغية</option>
          </select>

          <input
            type="date"
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            placeholder="من تاريخ"
          />

          <input
            type="date"
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            placeholder="إلى تاريخ"
          />

          <button
            onClick={() => {
              setSearchTerm('');
              setTypeFilter('');
              setStatusFilter('');
              setDateFrom('');
              setDateTo('');
            }}
            className="px-4 py-2 bg-muted text-foreground rounded-md hover:bg-muted flex items-center justify-center"
          >
            <Filter className="h-4 w-4 ml-1" />
            إعادة تعيين
          </button>
        </div>
      </div>

      {/* جدول الفواتير */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200" data-testid="invoices-table">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  رقم الفاتورة
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  النوع
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  العميل/المورد
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  التاريخ
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الإجمالي
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  المدفوع
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الحالة
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الإجراءات
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredInvoices.map((invoice) => (
                <tr key={invoice.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                    {invoice.invoice_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      invoice.invoice_type === 'sales' ? 'bg-primary-100 text-primary-800' : 'bg-purple-100 text-purple-800'
                    }`}>
                      {invoice.invoice_type === 'sales' ? 'مبيعات' : 'مشتريات'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {invoice.customer_name || invoice.supplier_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {invoice.invoice_date}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                    {invoice.total_amount.toLocaleString()} ج.م
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-primary">
                    {invoice.paid_amount.toLocaleString()} ج.م
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(invoice.status)}`}>
                      {getStatusIcon(invoice.status)}
                      <span className="mr-1">{getStatusText(invoice.status)}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2 space-x-reverse">
                      <button
                        onClick={() => viewInvoice(invoice)}
                        className="text-primary-600 hover:text-primary-900 p-2 rounded-lg hover:bg-blue-50 transition-colors"
                        title="عرض التفاصيل"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => printInvoice(invoice)}
                        className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-50 transition-colors"
                        title="طباعة"
                      >
                        <Printer className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => exportInvoice(invoice, 'PDF')}
                        className="text-purple-600 hover:text-purple-900 p-2 rounded-lg hover:bg-purple-50 transition-colors"
                        title="تصدير PDF"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => {
                          alert('سيتم فتح نموذج التعديل قريباً');
                        }}
                        className="text-green-600 hover:text-green-900 p-2 rounded-lg hover:bg-green-50 transition-colors" 
                        title="تعديل"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* نوافذ منبثقة */}
      {showViewModal && <InvoiceViewModal />}
    </div>
  );
};

export default InvoiceManagementComplete;
