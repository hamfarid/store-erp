import React, { useState, useEffect, useCallback } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, User, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'
import { CustomerAddModal } from './modals'

const CustomersAdvanced = () => {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [filteredCustomers, setFilteredCustomers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [notification, setNotification] = useState(null)

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadCustomers()
  }, [])

  const loadCustomers = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/customers')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setCustomers(data.data)
          setFilteredCustomers(data.data)
          setError(null)
        } else {
          throw new Error(data.message || 'فشل في تحميل العملاء')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      setError(error.message)
      // بيانات تجريبية
      const mockCustomers = [
        {
          id: 1,
          name: 'مزرعة النيل الكبرى',
          email: 'nile@farm.com',
          phone: '+20-1001234567',
          address: 'الجيزة، مصر',
          type: 'مزرعة',
          status: 'نشط',
          totalOrders: 15,
          totalAmount: 125000,
          salesEngineer: 'فاطمة أحمد',
          salesEngineerId: 5
        },
        {
          id: 2,
          name: 'شركة الأراضي الخضراء',
          email: 'green@lands.com',
          phone: '+20-1009876543',
          address: 'الإسكندرية، مصر',
          type: 'شركة',
          status: 'نشط',
          totalOrders: 8,
          totalAmount: 89000,
          salesEngineer: 'أحمد محمد',
          salesEngineerId: 2
        }
      ]
      setCustomers(mockCustomers)
      setFilteredCustomers(mockCustomers)
    } finally {
      setLoading(false)
    }
  }, [])

  // البحث والتصفية
  useEffect(() => {
    if (searchTerm) {
      const filtered = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        customer.phone.includes(searchTerm)
      )
      setFilteredCustomers(filtered)
    } else {
      setFilteredCustomers(customers)
    }
  }, [searchTerm, customers])

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddCustomer = () => {
    setSelectedCustomer(null)
    setShowAddModal(true)
  }

  const handleViewCustomer = (customer) => {
    alert(`عرض تفاصيل العميل: ${customer.name}\n\nالبريد: ${customer.email}\nالهاتف: ${customer.phone}\nالعنوان: ${customer.address}\nالنوع: ${customer.type}\nمهندس المبيعات: ${customer.salesEngineer || 'غير محدد'}\nإجمالي المشتريات: ${customer.totalPurchases || 0} جنيه`)
  }

  const handleEditCustomer = (customer) => {
    setSelectedCustomer(customer)
    setShowEditModal(true)
  }

  const handleDeleteCustomer = async (customerId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا العميل؟')) {
      try {
        const response = await fetch(`/api/customers/${customerId}`, {
          method: 'DELETE'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setCustomers(prev => prev.filter(c => c.id !== customerId))
            showNotification('تم حذف العميل بنجاح')
          } else {
            throw new Error(data.message || 'فشل في حذف العميل')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      } catch (error) {
        showNotification(error.message || 'فشل في حذف العميل', 'error')
      }
    }
  }

  const handleSaveCustomer = async (customerData) => {
    try {
      if (selectedCustomer) {
        // تحديث عميل موجود
        const response = await fetch(`/api/customers/${selectedCustomer.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(customerData)
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setCustomers(prev => prev.map(c =>
              c.id === selectedCustomer.id ? data.data : c
            ))
            showNotification('تم تحديث العميل بنجاح')
            setShowEditModal(false)
          } else {
            throw new Error(data.message || 'فشل في تحديث العميل')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      } else {
        // إضافة عميل جديد
        const response = await fetch('/api/customers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(customerData)
        })

        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            setCustomers(prev => [...prev, data.data])
            showNotification('تم إضافة العميل بنجاح')
            setShowAddModal(false)
          } else {
            throw new Error(data.message || 'فشل في إضافة العميل')
          }
        } else {
          throw new Error('فشل في الاتصال بالخادم')
        }
      }
    } catch (error) {
      showNotification(error.message || 'فشل في حفظ العميل', 'error')
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
          <h1 className="text-2xl font-bold text-foreground">إدارة العملاء</h1>
          <p className="text-muted-foreground">إدارة بيانات العملاء والمزارع</p>
        </div>
        <button
          onClick={handleAddCustomer}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة عميل جديد
        </button>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="البحث في العملاء..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <User className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
      </div>

      {/* Customers Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                العميل
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                معلومات الاتصال
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                النوع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                مهندس المبيعات
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الطلبات
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
            {filteredCustomers.map((customer) => (
              <tr key={customer.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                        <User className="h-5 w-5 text-primary-600" />
                      </div>
                    </div>
                    <div className="mr-4">
                      <div className="text-sm font-medium text-foreground">
                        {customer.name}
                      </div>
                      <div className="text-sm text-gray-500">
                        {customer.address}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-foreground">{customer.email}</div>
                  <div className="text-sm text-gray-500">{customer.phone}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-primary/20 text-green-800">
                    {customer.type}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div className="flex items-center">
                    <User className="h-4 w-4 text-gray-400 ml-2" />
                    <span>{customer.salesEngineer || 'غير محدد'}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2 space-x-reverse">
                    <button
                      onClick={() => handleViewCustomer(customer)}
                      className="text-primary-600 hover:text-primary-900 p-2 rounded-lg hover:bg-blue-50 transition-colors"
                      title="عرض التفاصيل"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleEditCustomer(customer)}
                      className="text-green-600 hover:text-green-900 p-2 rounded-lg hover:bg-green-50 transition-colors"
                      title="تعديل"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteCustomer(customer.id)}
                      className="text-red-600 hover:text-red-900 p-2 rounded-lg hover:bg-red-50 transition-colors"
                      title="حذف"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div>{customer.totalOrders} طلب</div>
                  <div className="text-gray-500">{customer.totalAmount?.toLocaleString()} ج.م</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    customer.status === 'نشط' 
                      ? 'bg-primary/20 text-green-800' 
                      : 'bg-destructive/20 text-red-800'
                  }`}>
                    {customer.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEditCustomer(customer)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteCustomer(customer.id)}
                      className="text-destructive hover:text-red-900"
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

      {/* Customer Add Modal */}
      <CustomerAddModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSuccess={(customer) => {
          setShowAddModal(false)
          showNotification('تم إضافة العميل بنجاح')
          loadCustomers()
        }}
      />
    </div>
  )
}

export default CustomersAdvanced

