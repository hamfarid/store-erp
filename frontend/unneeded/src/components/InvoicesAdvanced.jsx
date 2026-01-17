import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Clock, XCircle, Printer, Send
} from 'lucide-react'
import DataTable from './ui/DataTable'
import DynamicForm from './ui/DynamicForm'
import { Notification, LoadingSpinner, Modal } from './ui/Notification'
import SearchFilter from './ui/SearchFilter'

const InvoicesAdvanced = () => {
  const [invoices, setInvoices] = useState([])
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedInvoice, setSelectedInvoice] = useState(null)
  const [filteredInvoices, setFilteredInvoices] = useState([])
  const [invoiceType, setInvoiceType] = useState('sales') // sales or purchase

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadData()
  }, [invoiceType])

  const loadData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        loadInvoices(),
        loadCustomers(),
        loadProducts()
      ])
    } catch (error) {
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadInvoices = async () => {
    try {
      const endpoint = invoiceType === 'sales' ? '/api/sales-invoices' : '/api/purchase-invoices'
      const response = await fetch(endpoint)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setInvoices(data.data)
          setFilteredInvoices(data.data)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية المحسنة
      const mockInvoices = [
        {
          id: 1,
          invoice_number: 'INV-2024-001',
          invoice_type: invoiceType,
          customer_name: 'مزرعة النيل الكبرى',
          customer_id: 1,
          invoice_date: '2024-07-01',
          due_date: '2024-07-31',
          subtotal: 15000,
          tax_amount: 2250,
          discount_amount: 500,
          total_amount: 16750,
          paid_amount: 16750,
          remaining_amount: 0,
          status: 'paid',
          payment_status: 'completed',
          payment_method: 'bank_transfer',
          sales_engineer: 'أحمد محمد',
          notes: 'فاتورة مدفوعة بالكامل',
          created_at: '2024-07-01T10:30:00',
          items: [
            { product_name: 'بذور طماطم هجين F1', quantity: 10, unit_price: 1200, total: 12000 },
            { product_name: 'سماد NPK', quantity: 20, unit_price: 150, total: 3000 }
          ]
        },
        {
          id: 2,
          invoice_number: 'INV-2024-002',
          invoice_type: invoiceType,
          customer_name: 'شركة الزراعة الحديثة',
          customer_id: 2,
          invoice_date: '2024-07-02',
          due_date: '2024-08-01',
          subtotal: 25000,
          tax_amount: 3750,
          discount_amount: 1000,
          total_amount: 27750,
          paid_amount: 15000,
          remaining_amount: 12750,
          status: 'partial',
          payment_status: 'partial',
          payment_method: 'cash',
          sales_engineer: 'فاطمة أحمد',
          notes: 'دفعة جزئية، باقي المبلغ خلال أسبوع',
          created_at: '2024-07-02T14:15:00',
          items: [
            { product_name: 'مبيد أكتارا', quantity: 15, unit_price: 1200, total: 18000 },
            { product_name: 'أسمدة مركبة', quantity: 35, unit_price: 200, total: 7000 }
          ]
        },
        {
          id: 3,
          invoice_number: 'INV-2024-003',
          invoice_type: invoiceType,
          customer_name: 'مزارع الصعيد التعاونية',
          customer_id: 3,
          invoice_date: '2024-07-03',
          due_date: '2024-07-18',
          subtotal: 8500,
          tax_amount: 1275,
          discount_amount: 0,
          total_amount: 9775,
          paid_amount: 0,
          remaining_amount: 9775,
          status: 'pending',
          payment_status: 'pending',
          payment_method: 'credit',
          sales_engineer: 'محمد علي',
          notes: 'في انتظار الدفع',
          created_at: '2024-07-03T09:45:00',
          items: [
            { product_name: 'بذور خيار', quantity: 25, unit_price: 340, total: 8500 }
          ]
        }
      ]
      setInvoices(mockInvoices)
      setFilteredInvoices(mockInvoices)
    }
  }

  const loadCustomers = async () => {
    const mockCustomers = [
      { id: 1, name: 'مزرعة النيل الكبرى' },
      { id: 2, name: 'شركة الزراعة الحديثة' },
      { id: 3, name: 'مزارع الصعيد التعاونية' },
      { id: 4, name: 'مزرعة الوادي الجديد' }
    ]
    setCustomers(mockCustomers)
  }

  const loadProducts = async () => {
    const mockProducts = [
      { id: 1, name: 'بذور طماطم هجين F1', price: 1200 },
      { id: 2, name: 'سماد NPK', price: 150 },
      { id: 3, name: 'مبيد أكتارا', price: 1200 },
      { id: 4, name: 'بذور خيار', price: 340 }
    ]
    setProducts(mockProducts)
  }

  const loadMockData = () => {
    loadInvoices()
    loadCustomers()
    loadProducts()
  }

  // تعريف أعمدة الجدول
  const columns = [
    {
      key: 'invoice_number',
      header: 'رقم الفاتورة',
      sortable: true,
      filterable: true,
      render: (value) => (
        <span className="font-mono text-sm bg-primary-100 px-2 py-1 rounded">
          {value}
        </span>
      )
    },
    {
      key: 'customer_name',
      header: 'العميل',
      sortable: true,
      filterable: true,
      render: (value) => (
        <div className="flex items-center">
          <User className="w-4 h-4 text-gray-400 ml-2" />
          <span className="font-medium">{value}</span>
        </div>
      )
    },
    {
      key: 'invoice_date',
      header: 'تاريخ الفاتورة',
      sortable: true,
      render: (value) => (
        <div className="flex items-center">
          <Calendar className="w-4 h-4 text-gray-400 ml-1" />
          <span className="text-sm">{new Date(value).toLocaleDateString('ar-EG')}</span>
        </div>
      )
    },
    {
      key: 'total_amount',
      header: 'إجمالي المبلغ',
      sortable: true,
      render: (value) => (
        <div className="flex items-center">
          <DollarSign className="w-4 h-4 text-green-500 ml-1" />
          <span className="font-medium text-primary">{value?.toLocaleString()} جنيه</span>
        </div>
      )
    },
    {
      key: 'paid_amount',
      header: 'المبلغ المدفوع',
      sortable: true,
      render: (value, item) => (
        <div className="text-center">
          <div className="font-medium text-primary-600">{value?.toLocaleString()} جنيه</div>
          {item.remaining_amount > 0 && (
            <div className="text-xs text-destructive">
              متبقي: {item.remaining_amount?.toLocaleString()} جنيه
            </div>
          )}
        </div>
      )
    },
    {
      key: 'payment_status',
      header: 'حالة الدفع',
      sortable: true,
      render: (value) => {
        const statusConfig = {
          completed: { label: 'مدفوعة', color: 'bg-primary/20 text-green-800', icon: CheckCircle },
          partial: { label: 'دفع جزئي', color: 'bg-accent/20 text-yellow-800', icon: Clock },
          pending: { label: 'في الانتظار', color: 'bg-destructive/20 text-red-800', icon: XCircle },
          overdue: { label: 'متأخرة', color: 'bg-destructive/20 text-red-800', icon: XCircle }
        }
        const config = statusConfig[value] || statusConfig.pending
        const Icon = config.icon
        
        return (
          <div className="flex items-center">
            <Icon className="w-4 h-4 ml-1" />
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          </div>
        )
      }
    },
    {
      key: 'sales_engineer',
      header: 'مهندس المبيعات',
      sortable: true,
      filterable: true,
      render: (value) => (
        <span className="text-sm text-muted-foreground">{value}</span>
      )
    },
    {
      key: 'due_date',
      header: 'تاريخ الاستحقاق',
      sortable: true,
      render: (value, item) => {
        const dueDate = new Date(value)
        const today = new Date()
        const isOverdue = dueDate < today && item.remaining_amount > 0
        
        return (
          <div className={`text-sm ${isOverdue ? 'text-destructive font-medium' : 'text-muted-foreground'}`}>
            {dueDate.toLocaleDateString('ar-EG')}
            {isOverdue && <div className="text-xs">متأخرة</div>}
          </div>
        )
      }
    }
  ]

  // إجراءات الجدول
  const actions = [
    {
      icon: Eye,
      label: 'عرض التفاصيل',
      onClick: (item) => {
        setSelectedInvoice(item)
        setShowDetailsModal(true)
      },
      className: 'text-primary-600 hover:text-primary-800 hover:bg-primary-50'
    },
    {
      icon: Edit,
      label: 'تعديل',
      onClick: (item) => {
        setSelectedInvoice(item)
        setShowEditModal(true)
      },
      className: 'text-primary hover:text-green-800 hover:bg-primary/10'
    },
    {
      icon: Printer,
      label: 'طباعة',
      onClick: (item) => {
        // يمكن إضافة modal للطباعة
      },
      className: 'text-purple-600 hover:text-purple-800 hover:bg-purple-50'
    },
    {
      icon: Send,
      label: 'إرسال',
      onClick: (item) => {
        // يمكن إضافة modal للإرسال
      },
      className: 'text-indigo-600 hover:text-indigo-800 hover:bg-secondary/10'
    },
    {
      icon: Trash2,
      label: 'حذف',
      onClick: (item) => {
        if (window.confirm(`هل أنت متأكد من حذف الفاتورة "${item.invoice_number}"؟`)) {
          handleDeleteInvoice(item.id)
        }
      },
      className: 'text-destructive hover:text-red-800 hover:bg-destructive/10'
    }
  ]

  // معالجة البحث والتصفية
  const handleSearch = (searchTerm) => {
    const filtered = invoices.filter(invoice =>
      invoice.invoice_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      invoice.customer_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      invoice.sales_engineer.toLowerCase().includes(searchTerm.toLowerCase())
    )
    setFilteredInvoices(filtered)
  }

  const handleFilter = (filters) => {
    let filtered = [...invoices]
    
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        filtered = filtered.filter(invoice =>
          invoice[key] && invoice[key].toString().toLowerCase().includes(filters[key].toLowerCase())
        )
      }
    })
    
    setFilteredInvoices(filtered)
  }

  // معالجة العمليات
  const handleDeleteInvoice = async (invoiceId) => {
    try {
      setInvoices(prev => prev.filter(inv => inv.id !== invoiceId))
      setFilteredInvoices(prev => prev.filter(inv => inv.id !== invoiceId))
    } catch (error) {
      }
  }

  // حقول النموذج
  const formFields = [
    {
      name: 'customer_id',
      label: 'العميل',
      type: 'select',
      required: true,
      options: customers.map(customer => ({ value: customer.id, label: customer.name }))
    },
    {
      name: 'invoice_date',
      label: 'تاريخ الفاتورة',
      type: 'date',
      required: true
    },
    {
      name: 'due_date',
      label: 'تاريخ الاستحقاق',
      type: 'date',
      required: true
    },
    {
      name: 'sales_engineer',
      label: 'مهندس المبيعات',
      type: 'text',
      required: true,
      placeholder: 'اسم مهندس المبيعات'
    },
    {
      name: 'payment_method',
      label: 'طريقة الدفع',
      type: 'select',
      required: true,
      options: [
        { value: 'cash', label: 'نقداً' },
        { value: 'bank_transfer', label: 'تحويل بنكي' },
        { value: 'credit', label: 'آجل' },
        { value: 'check', label: 'شيك' }
      ]
    },
    {
      name: 'discount_amount',
      label: 'مبلغ الخصم',
      type: 'number',
      min: 0,
      step: 0.01
    },
    {
      name: 'notes',
      label: 'ملاحظات',
      type: 'textarea',
      rows: 3,
      placeholder: 'ملاحظات إضافية'
    }
  ]

  if (loading) {
    return <LoadingSpinner size="lg" text="جاري تحميل الفواتير..." />
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground flex items-center">
              <FileText className="w-6 h-6 ml-2 text-primary-600" />
              إدارة الفواتير المتقدمة
            </h1>
            <p className="text-muted-foreground mt-1">إدارة شاملة لفواتير المبيعات والمشتريات</p>
          </div>
          
          <div className="flex items-center space-x-3 space-x-reverse">
            {/* Invoice Type Toggle */}
            <div className="flex bg-muted rounded-lg p-1">
              <button
                onClick={() => setInvoiceType('sales')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  invoiceType === 'sales'
                    ? 'bg-primary-600 text-white'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                فواتير المبيعات
              </button>
              <button
                onClick={() => setInvoiceType('purchase')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  invoiceType === 'purchase'
                    ? 'bg-primary-600 text-white'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                فواتير المشتريات
              </button>
            </div>
            
            <button
              onClick={() => }
              className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4 ml-1" />
              تصدير
            </button>
            
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Plus className="w-4 h-4 ml-1" />
              إنشاء فاتورة
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Notification
          type="error"
          title="خطأ في تحميل البيانات"
          message={error}
          className="mb-6"
          onDismiss={() => setError(null)}
        />
      )}

      {/* Search and Filter */}
      <SearchFilter
        onSearch={handleSearch}
        onFilter={handleFilter}
        placeholder="البحث في الفواتير..."
        filters={[
          {
            key: 'payment_status',
            label: 'حالة الدفع',
            type: 'select',
            options: [
              { value: 'completed', label: 'مدفوعة' },
              { value: 'partial', label: 'دفع جزئي' },
              { value: 'pending', label: 'في الانتظار' },
              { value: 'overdue', label: 'متأخرة' }
            ]
          },
          {
            key: 'payment_method',
            label: 'طريقة الدفع',
            type: 'select',
            options: [
              { value: 'cash', label: 'نقداً' },
              { value: 'bank_transfer', label: 'تحويل بنكي' },
              { value: 'credit', label: 'آجل' },
              { value: 'check', label: 'شيك' }
            ]
          },
          {
            key: 'sales_engineer',
            label: 'مهندس المبيعات',
            type: 'text',
            placeholder: 'اسم مهندس المبيعات'
          }
        ]}
        className="mb-6"
      />

      {/* Data Table */}
      <DataTable
        data={filteredInvoices}
        columns={columns}
        actions={actions}
        searchable={false}
        filterable={false}
        exportable={true}
        loading={loading}
        onRowClick={(item) => {
          setSelectedInvoice(item)
          setShowDetailsModal(true)
        }}
      />

      {/* Create Invoice Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title={`إنشاء ${invoiceType === 'sales' ? 'فاتورة مبيعات' : 'فاتورة مشتريات'} جديدة`}
        size="xl"
      >
        <div className="space-y-6">
          <DynamicForm
            fields={formFields}
            onSubmit={(data) => {
              setShowCreateModal(false)
            }}
            onCancel={() => setShowCreateModal(false)}
            submitText="إنشاء الفاتورة"
          />
        </div>
      </Modal>

      {/* Invoice Details Modal */}
      <Modal
        isOpen={showDetailsModal}
        onClose={() => setShowDetailsModal(false)}
        title="تفاصيل الفاتورة"
        size="xl"
      >
        {selectedInvoice && (
          <div className="space-y-6">
            {/* Invoice Header */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <h3 className="font-semibold text-foreground">رقم الفاتورة</h3>
                  <p className="text-lg font-mono">{selectedInvoice.invoice_number}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">العميل</h3>
                  <p>{selectedInvoice.customer_name}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">التاريخ</h3>
                  <p>{new Date(selectedInvoice.invoice_date).toLocaleDateString('ar-EG')}</p>
                </div>
              </div>
            </div>

            {/* Invoice Items */}
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">عناصر الفاتورة</h3>
              <div className="overflow-x-auto">
                <table className="w-full border border-border rounded-lg">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-2 text-right">المنتج</th>
                      <th className="px-4 py-2 text-right">الكمية</th>
                      <th className="px-4 py-2 text-right">السعر</th>
                      <th className="px-4 py-2 text-right">الإجمالي</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedInvoice.items?.map((item, index) => (
                      <tr key={index} className="border-t">
                        <td className="px-4 py-2">{item.product_name}</td>
                        <td className="px-4 py-2">{item.quantity}</td>
                        <td className="px-4 py-2">{item.unit_price?.toLocaleString()} جنيه</td>
                        <td className="px-4 py-2 font-medium">{item.total?.toLocaleString()} جنيه</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Invoice Totals */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>المجموع الفرعي:</span>
                  <span>{selectedInvoice.subtotal?.toLocaleString()} جنيه</span>
                </div>
                {selectedInvoice.discount_amount > 0 && (
                  <div className="flex justify-between text-destructive">
                    <span>الخصم:</span>
                    <span>-{selectedInvoice.discount_amount?.toLocaleString()} جنيه</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>الضريبة:</span>
                  <span>{selectedInvoice.tax_amount?.toLocaleString()} جنيه</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t pt-2">
                  <span>الإجمالي:</span>
                  <span>{selectedInvoice.total_amount?.toLocaleString()} جنيه</span>
                </div>
                <div className="flex justify-between text-primary">
                  <span>المدفوع:</span>
                  <span>{selectedInvoice.paid_amount?.toLocaleString()} جنيه</span>
                </div>
                {selectedInvoice.remaining_amount > 0 && (
                  <div className="flex justify-between text-destructive font-medium">
                    <span>المتبقي:</span>
                    <span>{selectedInvoice.remaining_amount?.toLocaleString()} جنيه</span>
                  </div>
                )}
              </div>
            </div>

            {/* Notes */}
            {selectedInvoice.notes && (
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-2">ملاحظات</h3>
                <p className="text-foreground bg-muted/50 p-3 rounded-lg">{selectedInvoice.notes}</p>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default InvoicesAdvanced

