import React, { useState, useEffect } from 'react'
import { Edit, Eye, FileText, Plus, Trash2 } from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const PurchaseInvoices = () => {
  const [invoices, setInvoices] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedInvoice, setSelectedInvoice] = useState(null)

  useEffect(() => {
    fetchInvoices()
  }, [])

  const fetchInvoices = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/purchase-invoices')
      if (response.success) {
        setInvoices(response.data)
      }
    } catch (error) {
      toast.error('خطأ في تحميل فواتير المشتريات')
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
        await ApiService.delete(`/purchase-invoices/${id}`)
        toast.success('تم حذف الفاتورة بنجاح')
        fetchInvoices()
      } catch (error) {
        toast.error('خطأ في حذف الفاتورة')
      }
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
        <h1 className="text-2xl font-bold text-foreground">فواتير المشتريات</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-primary hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
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
                المورد
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
                  {invoice.supplier_name}
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
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleViewInvoice(invoice)}
                      className="text-primary-600 hover:text-primary-900"
                      title="عرض"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleViewInvoice(invoice)}
                      className="text-primary hover:text-green-900"
                      title="تعديل"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteInvoice(invoice.id)}
                      className="text-destructive hover:text-red-900"
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
                  <label className="block text-sm font-medium text-foreground">المورد</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.supplier_name}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground">التاريخ</label>
                  <p className="mt-1 text-sm text-foreground">{selectedInvoice.date}</p>
                </div>
              </div>

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
                  <button className="bg-primary hover:bg-green-700 text-white px-4 py-2 rounded flex items-center gap-2">
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
                  إنشاء فاتورة مشتريات جديدة
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
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
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
                      className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                      defaultValue={new Date().toISOString().split('T')[0]}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    المورد
                  </label>
                  <select className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
                    <option value="">اختر المورد</option>
                    <option value="1">مورد تجريبي 1</option>
                    <option value="2">مورد تجريبي 2</option>
                  </select>
                </div>

                <div className="bg-muted/50 p-4 rounded-md">
                  <h4 className="font-medium text-foreground mb-3">أصناف الفاتورة</h4>
                  <div className="space-y-2">
                    <div className="grid grid-cols-4 gap-2 text-sm font-medium text-foreground">
                      <div>الصنف</div>
                      <div>الكمية</div>
                      <div>السعر</div>
                      <div>الإجمالي</div>
                    </div>
                    <div className="grid grid-cols-4 gap-2">
                      <select className="px-2 py-1 border border-border rounded text-sm">
                        <option>اختر الصنف</option>
                        <option>منتج تجريبي 1</option>
                        <option>منتج تجريبي 2</option>
                      </select>
                      <input type="number" className="px-2 py-1 border border-border rounded text-sm" placeholder="الكمية" />
                      <input type="number" className="px-2 py-1 border border-border rounded text-sm" placeholder="السعر" />
                      <input type="number" className="px-2 py-1 border border-border rounded text-sm" placeholder="الإجمالي" disabled />
                    </div>
                  </div>
                  <button className="mt-2 text-primary hover:text-green-800 text-sm">
                    + إضافة صنف آخر
                  </button>
                </div>

                <div className="flex justify-between items-center pt-4 border-t">
                  <div className="text-lg font-semibold">
                    الإجمالي: 0 جنيه
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowCreateModal(false)}
                      className="bg-gray-300 hover:bg-gray-400 text-foreground px-4 py-2 rounded"
                    >
                      إلغاء
                    </button>
                    <button
                      onClick={() => {
                        toast.success('تم إنشاء فاتورة المشتريات بنجاح! 🎉')
                        setShowCreateModal(false)
                      }}
                      className="bg-primary hover:bg-green-700 text-white px-4 py-2 rounded"
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
    </div>
  )
}

export default PurchaseInvoices

