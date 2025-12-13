import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, FileText, DollarSign, Calendar, Truck, Package, CheckCircle, XCircle, AlertTriangle
} from 'lucide-react';

const PurchaseInvoiceManagement = () => {
  const [invoices, setInvoices] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [formData, setFormData] = useState({
    supplier_id: '',
    warehouse_id: '',
    invoice_number: '',
    invoice_date: new Date().toISOString().split('T')[0],
    due_date: '',
    payment_terms: '',
    notes: '',
    items: []
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      // Fetch purchase invoices
      const invoicesResponse = await fetch('http://localhost:5002/api/purchase-invoices', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (invoicesResponse.ok) {
        const data = await invoicesResponse.json();
        setInvoices(data.data || data.invoices || []);
      }

      // Fetch suppliers
      const suppliersResponse = await fetch('http://localhost:5002/api/suppliers', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (suppliersResponse.ok) {
        const data = await suppliersResponse.json();
        setSuppliers(data.data || data.suppliers || []);
      }

      // Fetch products
      const productsResponse = await fetch('http://localhost:5002/api/products', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (productsResponse.ok) {
        const data = await productsResponse.json();
        setProducts(data.data || data.products || []);
      }

      // Fetch warehouses
      const warehousesResponse = await fetch('http://localhost:5002/api/warehouses', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (warehousesResponse.ok) {
        const data = await warehousesResponse.json();
        setWarehouses(data.data || data.warehouses || []);
      }

      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const filteredInvoices = invoices.filter(invoice => {
    const matchesSearch = (invoice.invoice_number || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (invoice.supplier_name || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !statusFilter || invoice.status === statusFilter;

    let matchesDate = true;
    if (dateFrom || dateTo) {
      const invoiceDate = new Date(invoice.invoice_date);
      if (dateFrom) matchesDate = matchesDate && invoiceDate >= new Date(dateFrom);
      if (dateTo) matchesDate = matchesDate && invoiceDate <= new Date(dateTo);
    }

    return matchesSearch && matchesStatus && matchesDate;
  });

  const handleAddItem = () => {
    setFormData({
      ...formData,
      items: [
        ...formData.items,
        { product_id: '', quantity: 1, unit_price: 0, total: 0, notes: '' }
      ]
    });
  };

  const handleRemoveItem = (index) => {
    const newItems = formData.items.filter((_, i) => i !== index);
    setFormData({ ...formData, items: newItems });
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...formData.items];
    newItems[index][field] = value;
    
    // Calculate total
    if (field === 'quantity' || field === 'unit_price') {
      newItems[index].total = newItems[index].quantity * newItems[index].unit_price;
    }
    
    setFormData({ ...formData, items: newItems });
  };

  const calculateTotals = () => {
    const subtotal = formData.items.reduce((sum, item) => sum + (item.total || 0), 0);
    const tax = subtotal * 0.15; // 15% tax
    const total = subtotal + tax;
    return { subtotal, tax, total };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const { subtotal, tax, total } = calculateTotals();
      
      const invoiceData = {
        ...formData,
        invoice_type: 'purchase',
        subtotal,
        tax_amount: tax,
        total_amount: total,
        status: 'pending'
      };

      const response = await fetch('http://localhost:5002/api/purchase-invoices', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(invoiceData)
      });

      if (response.ok) {
        alert('تم إضافة فاتورة الشراء بنجاح');
        setShowAddModal(false);
        loadData();
        resetForm();
      } else {
        alert('حدث خطأ أثناء إضافة الفاتورة');
      }
    } catch (error) {
      console.error('Error saving invoice:', error);
      alert('حدث خطأ أثناء الحفظ');
    }
  };

  const resetForm = () => {
    setFormData({
      supplier_id: '',
      warehouse_id: '',
      invoice_number: '',
      invoice_date: new Date().toISOString().split('T')[0],
      due_date: '',
      payment_terms: '',
      notes: '',
      items: []
    });
  };

  const handleDelete = async (id) => {
    if (!confirm('هل أنت متأكد من حذف هذه الفاتورة؟')) return;
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5002/api/purchase-invoices/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        alert('تم حذف الفاتورة بنجاح');
        loadData();
      } else {
        alert('حدث خطأ أثناء الحذف');
      }
    } catch (error) {
      console.error('Error deleting invoice:', error);
      alert('حدث خطأ أثناء الحذف');
    }
  };

  const handleViewInvoice = (invoice) => {
    setSelectedInvoice(invoice);
    setShowViewModal(true);
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'معلقة', icon: AlertTriangle, className: 'bg-yellow-100 text-yellow-800' },
      paid: { label: 'مدفوعة', icon: CheckCircle, className: 'bg-green-100 text-green-800' },
      partial: { label: 'دفع جزئي', icon: DollarSign, className: 'bg-blue-100 text-blue-800' },
      cancelled: { label: 'ملغية', icon: XCircle, className: 'bg-red-100 text-red-800' }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`px-3 py-1 rounded-full text-xs font-medium inline-flex items-center ${config.className}`}>
        <Icon className="w-3 h-3 ml-1" />
        {config.label}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">فواتير المشتريات</h1>
          <p className="text-gray-600 mt-1">إدارة فواتير الشراء من الموردين</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
        >
          <Plus className="w-5 h-5" />
          إضافة فاتورة شراء
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Search className="w-4 h-4 inline ml-1" />
              بحث
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="رقم الفاتورة أو المورد..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Filter className="w-4 h-4 inline ml-1" />
              الحالة
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">الكل</option>
              <option value="pending">معلقة</option>
              <option value="paid">مدفوعة</option>
              <option value="partial">دفع جزئي</option>
              <option value="cancelled">ملغية</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="w-4 h-4 inline ml-1" />
              من تاريخ
            </label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="w-4 h-4 inline ml-1" />
              إلى تاريخ
            </label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">إجمالي الفواتير</p>
              <p className="text-2xl font-bold text-gray-800">{filteredInvoices.length}</p>
            </div>
            <FileText className="w-10 h-10 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">معلقة</p>
              <p className="text-2xl font-bold text-yellow-600">
                {filteredInvoices.filter(i => i.status === 'pending').length}
              </p>
            </div>
            <AlertTriangle className="w-10 h-10 text-yellow-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">مدفوعة</p>
              <p className="text-2xl font-bold text-green-600">
                {filteredInvoices.filter(i => i.status === 'paid').length}
              </p>
            </div>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">إجمالي المبلغ</p>
              <p className="text-2xl font-bold text-blue-600">
                {filteredInvoices.reduce((sum, inv) => sum + (inv.total_amount || 0), 0).toFixed(2)} ج.م
              </p>
            </div>
            <DollarSign className="w-10 h-10 text-blue-500" />
          </div>
        </div>
      </div>

      {/* Invoices Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">رقم الفاتورة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المورد</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المبلغ الإجمالي</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المبلغ المدفوع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredInvoices.length === 0 ? (
                <tr>
                  <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                    <FileText className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                    <p>لا توجد فواتير شراء</p>
                  </td>
                </tr>
              ) : (
                filteredInvoices.map((invoice) => (
                  <tr key={invoice.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {invoice.invoice_number}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Truck className="w-4 h-4 ml-2 text-gray-400" />
                        {invoice.supplier_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(invoice.invoice_date).toLocaleDateString('ar-EG')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                      {invoice.total_amount?.toFixed(2)} ج.م
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-semibold">
                      {invoice.paid_amount?.toFixed(2)} ج.م
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {getStatusBadge(invoice.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleViewInvoice(invoice)}
                          className="text-blue-600 hover:text-blue-900"
                          title="عرض"
                        >
                          <Eye className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(invoice.id)}
                          className="text-red-600 hover:text-red-900"
                          title="حذف"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                        <button
                          className="text-green-600 hover:text-green-900"
                          title="تنزيل PDF"
                        >
                          <Download className="w-5 h-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Invoice Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">إضافة فاتورة شراء جديدة</h2>
                <button
                  onClick={() => {
                    setShowAddModal(false);
                    resetForm();
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit}>
                {/* Basic Info */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">المورد *</label>
                    <select
                      value={formData.supplier_id}
                      onChange={(e) => setFormData({ ...formData, supplier_id: e.target.value })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">اختر المورد</option>
                      {suppliers.map(supplier => (
                        <option key={supplier.id} value={supplier.id}>{supplier.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">المخزن *</label>
                    <select
                      value={formData.warehouse_id}
                      onChange={(e) => setFormData({ ...formData, warehouse_id: e.target.value })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">اختر المخزن</option>
                      {warehouses.map(warehouse => (
                        <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">رقم الفاتورة *</label>
                    <input
                      type="text"
                      value={formData.invoice_number}
                      onChange={(e) => setFormData({ ...formData, invoice_number: e.target.value })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">تاريخ الفاتورة *</label>
                    <input
                      type="date"
                      value={formData.invoice_date}
                      onChange={(e) => setFormData({ ...formData, invoice_date: e.target.value })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">تاريخ الاستحقاق</label>
                    <input
                      type="date"
                      value={formData.due_date}
                      onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">شروط الدفع</label>
                    <input
                      type="text"
                      value={formData.payment_terms}
                      onChange={(e) => setFormData({ ...formData, payment_terms: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                {/* Items */}
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold text-gray-800">الأصناف</h3>
                    <button
                      type="button"
                      onClick={handleAddItem}
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      إضافة صنف
                    </button>
                  </div>

                  {formData.items.map((item, index) => (
                    <div key={index} className="grid grid-cols-12 gap-2 mb-2 p-3 bg-gray-50 rounded">
                      <div className="col-span-4">
                        <select
                          value={item.product_id}
                          onChange={(e) => {
                            const product = products.find(p => p.id === parseInt(e.target.value));
                            handleItemChange(index, 'product_id', e.target.value);
                            if (product) {
                              handleItemChange(index, 'unit_price', product.price || 0);
                            }
                          }}
                          className="w-full px-2 py-1 border rounded text-sm"
                          required
                        >
                          <option value="">اختر المنتج</option>
                          {products.map(product => (
                            <option key={product.id} value={product.id}>{product.name}</option>
                          ))}
                        </select>
                      </div>
                      <div className="col-span-2">
                        <input
                          type="number"
                          value={item.quantity}
                          onChange={(e) => handleItemChange(index, 'quantity', parseFloat(e.target.value) || 0)}
                          placeholder="الكمية"
                          className="w-full px-2 py-1 border rounded text-sm"
                          required
                          min="1"
                        />
                      </div>
                      <div className="col-span-2">
                        <input
                          type="number"
                          value={item.unit_price}
                          onChange={(e) => handleItemChange(index, 'unit_price', parseFloat(e.target.value) || 0)}
                          placeholder="السعر"
                          className="w-full px-2 py-1 border rounded text-sm"
                          required
                          step="0.01"
                        />
                      </div>
                      <div className="col-span-2">
                        <input
                          type="number"
                          value={item.total}
                          readOnly
                          placeholder="الإجمالي"
                          className="w-full px-2 py-1 border rounded text-sm bg-gray-100"
                        />
                      </div>
                      <div className="col-span-2">
                        <button
                          type="button"
                          onClick={() => handleRemoveItem(index)}
                          className="w-full bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm"
                        >
                          حذف
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Totals */}
                <div className="bg-gray-50 p-4 rounded-lg mb-6">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-700">المجموع الفرعي:</span>
                      <span className="font-semibold">{calculateTotals().subtotal.toFixed(2)} ج.م</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-700">الضريبة (15%):</span>
                      <span className="font-semibold">{calculateTotals().tax.toFixed(2)} ج.م</span>
                    </div>
                    <div className="flex justify-between text-lg font-bold border-t pt-2">
                      <span>الإجمالي:</span>
                      <span className="text-blue-600">{calculateTotals().total.toFixed(2)} ج.م</span>
                    </div>
                  </div>
                </div>

                {/* Notes */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">ملاحظات</label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows="3"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Actions */}
                <div className="flex justify-end gap-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddModal(false);
                      resetForm();
                    }}
                    className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  >
                    حفظ الفاتورة
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* View Invoice Modal */}
      {showViewModal && selectedInvoice && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">تفاصيل فاتورة الشراء</h2>
                <button
                  onClick={() => setShowViewModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">رقم الفاتورة</p>
                    <p className="font-semibold">{selectedInvoice.invoice_number}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">المورد</p>
                    <p className="font-semibold">{selectedInvoice.supplier_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">التاريخ</p>
                    <p className="font-semibold">
                      {new Date(selectedInvoice.invoice_date).toLocaleDateString('ar-EG')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">الحالة</p>
                    <div>{getStatusBadge(selectedInvoice.status)}</div>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between text-lg">
                    <span>المبلغ الإجمالي:</span>
                    <span className="font-bold text-blue-600">
                      {selectedInvoice.total_amount?.toFixed(2)} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>المبلغ المدفوع:</span>
                    <span className="font-semibold text-green-600">
                      {selectedInvoice.paid_amount?.toFixed(2)} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>المتبقي:</span>
                    <span className="font-semibold text-red-600">
                      {((selectedInvoice.total_amount || 0) - (selectedInvoice.paid_amount || 0)).toFixed(2)} ج.م
                    </span>
                  </div>
                </div>

                {selectedInvoice.notes && (
                  <div className="border-t pt-4">
                    <p className="text-sm text-gray-600 mb-2">ملاحظات</p>
                    <p className="text-gray-800">{selectedInvoice.notes}</p>
                  </div>
                )}
              </div>

              <div className="flex justify-end gap-4 mt-6">
                <button
                  onClick={() => setShowViewModal(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  إغلاق
                </button>
                <button className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg flex items-center gap-2">
                  <Download className="w-4 h-4" />
                  تنزيل PDF
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PurchaseInvoiceManagement;
