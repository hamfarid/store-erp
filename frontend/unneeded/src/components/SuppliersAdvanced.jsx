import React, { useState, useEffect, useCallback } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, RefreshCw, Building, Truck
} from 'lucide-react'
import { SupplierAddModal } from './modals'

const SuppliersAdvanced = () => {
  const [suppliers, setSuppliers] = useState([])
  const [filteredSuppliers, setFilteredSuppliers] = useState([])
  const [loading, setLoading] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [editingSupplier, setEditingSupplier] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadSuppliers()
  }, [])

  useEffect(() => {
    filterSuppliers()
  }, [suppliers, searchTerm])

  const loadSuppliers = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/suppliers')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setSuppliers(data.data)
          setFilteredSuppliers(data.data)
        } else {
          throw new Error('فشل في تحميل الموردين')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockSuppliers = [
        {
          id: 1,
          name: 'شركة البذور المتقدمة',
          email: 'info@seeds.com',
          phone: '+20-1009876543',
          address: 'القاهرة، مصر',
          type: 'بذور',
          status: 'نشط',
          totalOrders: 25,
          totalAmount: 250000,
          rating: 4.8
        },
        {
          id: 2,
          name: 'شركة الأسمدة الحديثة',
          email: 'contact@fertilizers.com',
          phone: '+20-1001234567',
          address: 'الإسكندرية، مصر',
          type: 'أسمدة',
          status: 'نشط',
          totalOrders: 18,
          totalAmount: 180000,
          rating: 4.5
        }
      ]
      setSuppliers(mockSuppliers)
      setFilteredSuppliers(mockSuppliers)
    } finally {
      setLoading(false)
    }
  }, [])

  const filterSuppliers = () => {
    if (searchTerm) {
      const filtered = suppliers.filter(supplier =>
        supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        supplier.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        supplier.type.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredSuppliers(filtered)
    } else {
      setFilteredSuppliers(suppliers)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddSupplier = () => {
    setEditingSupplier(null)
    setShowModal(true)
  }

  const handleViewSupplier = (supplier) => {
    setEditingSupplier(supplier)
    alert(`عرض تفاصيل المورد: ${supplier.name}\n\nالبريد: ${supplier.email}\nالهاتف: ${supplier.phone}\nالعنوان: ${supplier.address}\nالنوع: ${supplier.type}\nإجمالي الطلبات: ${supplier.totalOrders || 0}\nإجمالي المبلغ: ${supplier.totalAmount || 0} جنيه`)
  }

  const handleEditSupplier = (supplier) => {
    setEditingSupplier(supplier)
    setShowModal(true)
  }

  const handleDeleteSupplier = async (supplierId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المورد؟')) {
      try {
        const response = await fetch(`/api/suppliers/${supplierId}`, {
          method: 'DELETE'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setSuppliers(prev => prev.filter(s => s.id !== supplierId))
            showNotification('تم حذف المورد بنجاح')
          } else {
            throw new Error(data.message || 'فشل في حذف المورد')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      } catch (error) {
        showNotification(error.message || 'فشل في حذف المورد', 'error')
      }
    }
  }

  const handleSaveSupplier = async (supplierData) => {
    try {
      if (editingSupplier) {
        // تحديث مورد موجود
        const response = await fetch(`/api/suppliers/${editingSupplier.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(supplierData)
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setSuppliers(prev => prev.map(s =>
              s.id === editingSupplier.id ? data.data : s
            ))
            showNotification('تم تحديث المورد بنجاح')
            setShowModal(false)
          } else {
            throw new Error(data.message || 'فشل في تحديث المورد')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      } else {
        // إضافة مورد جديد
        const response = await fetch('/api/suppliers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(supplierData)
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setSuppliers(prev => [...prev, data.data])
            showNotification('تم إضافة المورد بنجاح')
            setShowModal(false)
          } else {
            throw new Error(data.message || 'فشل في إضافة المورد')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      }
    } catch (error) {
      showNotification(error.message || 'فشل في حفظ المورد', 'error')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة الموردين</h1>
          <p className="text-muted-foreground">إدارة بيانات الموردين والشركات</p>
        </div>
        <button
          onClick={handleAddSupplier}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة مورد جديد
        </button>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في الموردين..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadSuppliers}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Building className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الموردين</p>
              <p className="text-2xl font-bold text-foreground">{suppliers.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Truck className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">نشط</p>
              <p className="text-2xl font-bold text-foreground">
                {suppliers.filter(s => s.status === 'نشط').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الطلبات</p>
              <p className="text-2xl font-bold text-foreground">
                {suppliers.reduce((sum, s) => sum + (s.totalOrders || 0), 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المبلغ</p>
              <p className="text-2xl font-bold text-foreground">
                {suppliers.reduce((sum, s) => sum + (s.totalAmount || 0), 0).toLocaleString()} ج.م
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Suppliers Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المورد
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                معلومات الاتصال
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                النوع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الطلبات
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                التقييم
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
            {filteredSuppliers.map((supplier) => (
              <tr key={supplier.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                        <Building className="h-5 w-5 text-primary-600" />
                      </div>
                    </div>
                    <div className="mr-4">
                      <div className="text-sm font-medium text-foreground">
                        {supplier.name}
                      </div>
                      <div className="text-sm text-gray-500">
                        {supplier.address}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-foreground">{supplier.email}</div>
                  <div className="text-sm text-gray-500">{supplier.phone}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                    {supplier.type}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div>{supplier.totalOrders} طلب</div>
                  <div className="text-gray-500">{supplier.totalAmount?.toLocaleString()} ج.م</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <span className="text-yellow-400">★</span>
                    <span className="mr-1 text-sm text-foreground">{supplier.rating}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    supplier.status === 'نشط' 
                      ? 'bg-primary/20 text-green-800' 
                      : 'bg-destructive/20 text-red-800'
                  }`}>
                    {supplier.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleViewSupplier(supplier)}
                      className="text-primary-600 hover:text-primary-900 p-2 rounded-lg hover:bg-blue-50 transition-colors"
                      title="عرض التفاصيل"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleEditSupplier(supplier)}
                      className="text-green-600 hover:text-green-900 p-2 rounded-lg hover:bg-green-50 transition-colors"
                      title="تعديل"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteSupplier(supplier.id)}
                      className="text-red-600 hover:text-red-900 p-2 rounded-lg hover:bg-red-50 transition-colors"
                      title="حذف"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}

      {/* Supplier Add Modal */}
      <SupplierAddModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onSuccess={(supplier) => {
          setShowModal(false)
          showNotification('تم إضافة المورد بنجاح')
          loadSuppliers()
        }}
      />
    </div>
  )
}

export default SuppliersAdvanced

