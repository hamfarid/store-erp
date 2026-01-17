import React, { useState, useEffect } from 'react'
import { Edit, Eye, FileText, Plus, Trash2 } from 'lucide-react'
import { toast } from 'react-hot-toast'

import { salesInvoicesAPI } from '../services/api'
import LotWarehouseManager from './LotWarehouseManager'
import InvoicePrint from './InvoicePrint'

const SalesInvoices = () => {
  const [invoices, setInvoices] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showPrintModal, setShowPrintModal] = useState(false)
  const [selectedInvoice, setSelectedInvoice] = useState(null)
  const [invoiceItems, setInvoiceItems] = useState([
    { product: '', quantity: 1, price: 0, total: 0, lot: '', warehouse: '' }
  ])
  const [invoiceData, setInvoiceData] = useState({
    customer: '',
    date: new Date().toISOString().split('T')[0],
    notes: '',
    salesEngineer: '',
    paymentMethod: '',
    paymentTerm: '',
    dueDate: ''
  })

  useEffect(() => {
    fetchInvoices()
  }, [])

  const fetchInvoices = async () => {
    try {
      setLoading(true)
      const response = await salesInvoicesAPI.getAll()
      if (response.success) {
        setInvoices(response.invoices || [])
      }
    } catch (error) {
      toast.error('خطأ في تحميل فواتير المبيعات')
      } finally {
      setLoading(false)
    }
  }

  const handleViewInvoice = (invoice) => {
    setSelectedInvoice(invoice)
    setShowModal(true)
  }

  const handleDeleteInvoice = async (id) => {
    if (window.confirm('هل أنت متأكد من حذف هذه الفاتورة؟')) {
      try {
        await salesInvoicesAPI.delete(id)
        toast.success('تم حذف الفاتورة بنجاح')
        fetchInvoices()
      } catch (error) {
        toast.error('خطأ في حذف الفاتورة')
        }
    }
  }

  // حساب الإجمالي لصنف واحد
  const calculateItemTotal = (quantity, price) => {
    return (parseFloat(quantity) || 0) * (parseFloat(price) || 0)
  }

  // تحديث صنف في الفاتورة
  const updateInvoiceItem = (index, field, value) => {
    const updatedItems = [...invoiceItems]
    updatedItems[index][field] = value

    // حساب الإجمالي تلقائياً
    if (field === 'quantity' || field === 'price') {
      updatedItems[index].total = calculateItemTotal(
        updatedItems[index].quantity,
        updatedItems[index].price
      )
    }

    setInvoiceItems(updatedItems)
  }

  // إضافة صنف جديد
  const addInvoiceItem = () => {
    setInvoiceItems([...invoiceItems, {
      product: '',
      quantity: 1,
      price: 0,
      total: 0,
      lot: '',
      warehouse: ''
    }])
  }

  // حذف صنف
  const removeInvoiceItem = (index) => {
    if (invoiceItems.length > 1) {
      const updatedItems = invoiceItems.filter((_, i) => i !== index)
      setInvoiceItems(updatedItems)
    }
  }

  // حساب الإجمالي الكلي
  const calculateGrandTotal = () => {
    return invoiceItems.reduce((sum, item) => sum + (item.total || 0), 0)
  }

  // حفظ الفاتورة
  const saveInvoice = async () => {
    try {
      const newInvoice = {
        invoice_number: `INV-${Date.now()}`,
        date: invoiceData.date,
        customer_name: invoiceData.customer || 'عميل تجريبي',
        sales_engineer: invoiceData.salesEngineer,
        payment_method: invoiceData.paymentMethod,
        payment_term: invoiceData.paymentTerm,
        due_date: invoiceData.dueDate,
        total_amount: calculateGrandTotal(),
        status: 'مسودة',
        notes: invoiceData.notes,
        items: invoiceItems.filter(item => item.product)
      }

      // محاولة حفظ الفاتورة عبر API
      try {
        await salesInvoicesAPI.create(newInvoice)
      } catch (apiError) {
        // إضافة الفاتورة للقائمة محلياً
        const localInvoice = { ...newInvoice, id: Date.now() }
        setInvoices([localInvoice, ...invoices])
        toast.success('تم حفظ الفاتورة محلياً')
      }

      // إعادة تعيين النموذج
      setInvoiceItems([{ product: '', quantity: 1, price: 0, total: 0, lot: '', warehouse: '' }])
      setInvoiceData({
        customer: '',
        date: new Date().toISOString().split('T')[0],
        notes: '',
        salesEngineer: '',
        paymentMethod: '',
        paymentTerm: '',
        dueDate: ''
      })
      setShowCreateModal(false)

      // إعادة تحميل الفواتير
      fetchInvoices()

    } catch (error) {
      toast.error('خطأ في حفظ الفاتورة')
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'مدفوعة':
        return 'bg-primary/20 text-green-800'
      case 'معلقة':
        return 'bg-accent/20 text-yellow-800'
      case 'ملغاة':
        return 'bg-destructive/20 text-red-800'
      default:
        return 'bg-muted text-foreground'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-foreground">فواتير المبيعات</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          فاتورة جديدة
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم الفاتورة
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                العميل
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                التاريخ
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المبلغ الإجمالي
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
            {invoices.map((invoice) => (
              <tr key={invoice.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                  {invoice.invoice_number}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {invoice.customer_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {invoice.date}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {invoice.total_amount.toLocaleString()} جنيه
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(invoice.status)}`}>
                    {invoice.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex gap-1 flex-wrap">
                    <button
                      onClick={() => handleViewInvoice(invoice)}
                      className="text-primary-600 hover:text-primary-900 p-1"
                      title="عرض"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => {
                        toast.info('جاري فتح نافذة التعديل...')
                        // TODO: إضافة وظيفة التعديل
                      }}
                      className="text-primary hover:text-green-900 p-1"
                      title="تعديل"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => {
                        setSelectedInvoice(invoice)
                        setShowPrintModal(true)
                      }}
                      className="text-purple-600 hover:text-purple-900 p-1"
                      title="طباعة"
                    >
                      <FileText className="w-4 h-4" />
                    </button>
                    {invoice.status === 'مسودة' && (
                      <button
                        onClick={() => {
                          const updatedInvoices = invoices.map(inv =>
                            inv.id === invoice.id
                              ? { ...inv, status: 'معتمدة' }
                              : inv
                          )
                          setInvoices(updatedInvoices)
                          toast.success('تم اعتماد الفاتورة! ✅')
                        }}
                        className="text-accent hover:text-orange-900 p-1"
                        title="اعتماد"
                      >
                        ✓
                      </button>
                    )}
                    <button
                      onClick={() => handleDeleteInvoice(invoice.id)}
                      className="text-destructive hover:text-red-900 p-1"
                      title="حذف"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal لعرض تفاصيل الفاتورة */}
      {showModal && selectedInvoice && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-foreground">
                  تفاصيل الفاتورة {selectedInvoice.invoice_number}
                </h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-muted-foreground"
                >
                  ✕
                </button>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-foreground">العميل</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.customer_name}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">التاريخ</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.date}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">مهندس المبيعات</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.sales_engineer || 'غير محدد'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">طريقة الدفع</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.payment_method || 'غير محدد'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">مدة السداد</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.payment_term ? `${selectedInvoice.payment_term} يوم` : 'غير محدد'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">تاريخ الاستحقاق</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.due_date || 'غير محدد'}</p>
                </div>
              </div>

              {selectedInvoice.notes && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-foreground">ملاحظات</label>
                  <p className="mt-1 text-sm text-foreground bg-muted/50 p-3 rounded">{selectedInvoice.notes}</p>
                </div>
              )}

              <div className="mb-4">
                <label className="block text-sm font-medium text-foreground mb-2">الأصناف</label>
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">المنتج</th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">الكمية</th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">السعر</th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">الإجمالي</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {selectedInvoice.items?.map((item, index) => (
                      <tr key={index}>
                        <td className="px-4 py-2 text-sm text-foreground">{item.product_name}</td>
                        <td className="px-4 py-2 text-sm text-gray-500">{item.quantity}</td>
                        <td className="px-4 py-2 text-sm text-gray-500">{item.price}</td>
                        <td className="px-4 py-2 text-sm text-gray-500">{item.total}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="flex justify-between items-center pt-4 border-t">
                <div className="text-lg font-semibold">
                  الإجمالي: {selectedInvoice.total_amount.toLocaleString()} جنيه
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setShowModal(false)}
                    className="bg-gray-300 hover:bg-gray-400 text-foreground px-4 py-2 rounded"
                  >
                    إغلاق
                  </button>
                  <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    طباعة
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal لإنشاء فاتورة جديدة */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-foreground">
                  إنشاء فاتورة مبيعات جديدة
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-400 hover:text-muted-foreground"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      رقم الفاتورة
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="سيتم إنشاؤه تلقائياً"
                      disabled
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      التاريخ
                    </label>
                    <input
                      type="date"
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      defaultValue={new Date().toISOString().split('T')[0]}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      العميل
                    </label>
                    <select
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      value={invoiceData.customer}
                      onChange={(e) => setInvoiceData({...invoiceData, customer: e.target.value})}
                    >
                      <option value="">اختر العميل</option>
                      <option value="أحمد محمد">أحمد محمد</option>
                      <option value="فاطمة علي">فاطمة علي</option>
                      <option value="محمد حسن">محمد حسن</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      مهندس المبيعات
                    </label>
                    <select
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      value={invoiceData.salesEngineer}
                      onChange={(e) => setInvoiceData({...invoiceData, salesEngineer: e.target.value})}
                    >
                      <option value="">اختر مهندس المبيعات</option>
                      <option value="م. أحمد سالم">م. أحمد سالم</option>
                      <option value="م. سارة محمد">م. سارة محمد</option>
                      <option value="م. خالد عبدالله">م. خالد عبدالله</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      طريقة الدفع
                    </label>
                    <select
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      value={invoiceData.paymentMethod}
                      onChange={(e) => setInvoiceData({...invoiceData, paymentMethod: e.target.value})}
                    >
                      <option value="">اختر طريقة الدفع</option>
                      <option value="نقدي">نقدي</option>
                      <option value="شيك">شيك</option>
                      <option value="تحويل بنكي">تحويل بنكي</option>
                      <option value="بطاقة ائتمان">بطاقة ائتمان</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      مدة السداد
                    </label>
                    <select
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      value={invoiceData.paymentTerm}
                      onChange={(e) => {
                        setInvoiceData({...invoiceData, paymentTerm: e.target.value})
                        // حساب تاريخ الاستحقاق تلقائياً
                        if (e.target.value && invoiceData.date) {
                          const dueDate = new Date(invoiceData.date)
                          const days = parseInt(e.target.value)
                          dueDate.setDate(dueDate.getDate() + days)
                          setInvoiceData(prev => ({...prev, dueDate: dueDate.toISOString().split('T')[0]}))
                        }
                      }}
                    >
                      <option value="">اختر مدة السداد</option>
                      <option value="0">فوري</option>
                      <option value="7">7 أيام</option>
                      <option value="15">15 يوم</option>
                      <option value="30">30 يوم</option>
                      <option value="60">60 يوم</option>
                      <option value="90">90 يوم</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      تاريخ الاستحقاق
                    </label>
                    <input
                      type="date"
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      value={invoiceData.dueDate}
                      onChange={(e) => setInvoiceData({...invoiceData, dueDate: e.target.value})}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      ملاحظات
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="ملاحظات إضافية"
                      value={invoiceData.notes}
                      onChange={(e) => setInvoiceData({...invoiceData, notes: e.target.value})}
                    />
                  </div>
                </div>

                <div className="bg-muted/50 p-4 rounded-md">
                  <h4 className="font-medium text-foreground mb-3">أصناف الفاتورة</h4>
                  <div className="space-y-2">
                    <div className="grid grid-cols-7 gap-2 text-sm font-medium text-foreground">
                      <div>الصنف</div>
                      <div>المخزن</div>
                      <div>اللوط</div>
                      <div>الكمية</div>
                      <div>السعر</div>
                      <div>الإجمالي</div>
                      <div>إجراءات</div>
                    </div>
                    {invoiceItems.map((item, index) => (
                      <div key={index} className="border border-border rounded-lg p-4 space-y-4">
                        <div className="flex justify-between items-center">
                          <h5 className="font-medium text-foreground">الصنف #{index + 1}</h5>
                          {invoiceItems.length > 1 && (
                            <button
                              onClick={() => removeInvoiceItem(index)}
                              className="text-destructive hover:text-red-800 text-sm"
                              title="حذف الصنف"
                            >
                              🗑️ حذف
                            </button>
                          )}
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-foreground mb-1">المنتج</label>
                            <select
                              className="w-full px-3 py-2 border border-border rounded text-sm"
                              value={item.product}
                              onChange={(e) => updateInvoiceItem(index, 'product', e.target.value)}
                            >
                              <option value="">اختر المنتج</option>
                              <option value="product1">بذور طماطم</option>
                              <option value="product2">سماد NPK</option>
                              <option value="product3">مبيد حشري</option>
                            </select>
                          </div>

                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label className="block text-sm font-medium text-foreground mb-1">الكمية</label>
                              <input
                                type="number"
                                className="w-full px-3 py-2 border border-border rounded text-sm"
                                placeholder="الكمية"
                                value={item.quantity}
                                onChange={(e) => updateInvoiceItem(index, 'quantity', e.target.value)}
                                min="1"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-foreground mb-1">السعر</label>
                              <input
                                type="number"
                                className="w-full px-3 py-2 border border-border rounded text-sm"
                                placeholder="السعر"
                                value={item.price}
                                onChange={(e) => updateInvoiceItem(index, 'price', e.target.value)}
                                min="0"
                                step="0.01"
                              />
                            </div>
                          </div>
                        </div>

                        {/* مدير اللوط والمخزن */}
                        {item.product && (
                          <LotWarehouseManager
                            productId={item.product}
                            onLotSelect={(lot) => updateInvoiceItem(index, 'lot', lot)}
                            onWarehouseSelect={(warehouse) => updateInvoiceItem(index, 'warehouse', warehouse)}
                          />
                        )}

                        <div className="bg-primary-50 p-3 rounded">
                          <div className="flex justify-between items-center">
                            <span className="text-sm font-medium text-foreground">إجمالي الصنف:</span>
                            <span className="text-lg font-semibold text-primary-600">
                              {item.total.toFixed(2)} جنيه
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={addInvoiceItem}
                    className="mt-2 text-primary-600 hover:text-primary-800 text-sm"
                  >
                    + إضافة صنف آخر
                  </button>
                </div>

                <div className="flex justify-between items-center pt-4 border-t">
                  <div className="text-lg font-semibold">
                    الإجمالي: {calculateGrandTotal().toFixed(2)} جنيه
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowCreateModal(false)}
                      className="bg-gray-300 hover:bg-gray-400 text-foreground px-4 py-2 rounded"
                    >
                      إلغاء
                    </button>
                    <button
                      onClick={saveInvoice}
                      className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded"
                      disabled={invoiceItems.every(item => !item.product)}
                    >
                      حفظ الفاتورة
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* مكون الطباعة */}
      {showPrintModal && (
        <InvoicePrint
          invoice={selectedInvoice}
          onClose={() => {
            setShowPrintModal(false)
            setSelectedInvoice(null)
          }}
        />
      )}
    </div>
  )
}

export default SalesInvoices

