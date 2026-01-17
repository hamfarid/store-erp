import React, { useState, useEffect } from 'react'
import {
  Edit, Mail, Phone, Plus,
  Search, Trash2, User
} from 'lucide-react'

import toast from 'react-hot-toast'

const Customers = () => {
  const [customers, setCustomers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState(null)

  // بيانات تجريبية
  useEffect(() => {
    setCustomers([
      {
        id: 1,
        name: 'مزرعة النيل',
        contact_person: 'خالد حسن',
        phone: '01234567890',
        email: 'khaled@nilfarm.com',
        address: 'المنيا، مصر'
      },
      {
        id: 2,
        name: 'شركة الزراعة الحديثة',
        contact_person: 'فاطمة محمود',
        phone: '01234567891',
        email: 'fatma@modern-agri.com',
        address: 'بني سويف، مصر'
      },
      {
        id: 3,
        name: 'مزارع الصعيد',
        contact_person: 'عبد الرحمن علي',
        phone: '01234567892',
        email: 'abdulrahman@saeed-farms.com',
        address: 'أسوان، مصر'
      },
      {
        id: 4,
        name: 'تعاونية المزارعين',
        contact_person: 'نادية إبراهيم',
        phone: '01234567893',
        email: 'nadia@farmers-coop.com',
        address: 'سوهاج، مصر'
      }
    ])
  }, [])

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.contact_person.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.phone.includes(searchTerm)
  )

  const handleAddCustomer = (customerData) => {
    const newCustomer = {
      id: Date.now(),
      ...customerData
    }
    setCustomers([...customers, newCustomer])
    setShowAddModal(false)
    toast.success('تم إضافة العميل بنجاح')
  }

  const handleEditCustomer = (customerData) => {
    setCustomers(customers.map(c => c.id === editingCustomer.id ? { ...editingCustomer, ...customerData } : c))
    setEditingCustomer(null)
    toast.success('تم تحديث بيانات العميل بنجاح')
  }

  const handleDeleteCustomer = (id) => {
    if (window.confirm('هل أنت متأكد من حذف هذا العميل؟')) {
      setCustomers(customers.filter(c => c.id !== id))
      toast.success('تم حذف العميل بنجاح')
    }
  }

  const CustomerModal = ({ customer, onSave, onClose }) => {
    const [formData, setFormData] = useState(customer || {
      name: '',
      contact_person: '',
      phone: '',
      email: '',
      address: ''
    })

    const handleSubmit = (e) => {
      e.preventDefault()
      onSave(formData)
    }

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 className="text-lg font-semibold mb-4">
            {customer ? 'تعديل بيانات العميل' : 'إضافة عميل جديد'}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">اسم العميل</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">الشخص المسؤول</label>
              <input
                type="text"
                value={formData.contact_person}
                onChange={(e) => setFormData({...formData, contact_person: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">رقم الهاتف</label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({...formData, phone: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">البريد الإلكتروني</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">العنوان</label>
              <textarea
                value={formData.address}
                onChange={(e) => setFormData({...formData, address: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                rows="3"
              />
            </div>
            
            <div className="flex justify-end space-x-2 space-x-reverse pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-muted-foreground border border-border rounded-md hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                {customer ? 'تحديث' : 'إضافة'}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">إدارة العملاء</h1>
        <p className="text-muted-foreground mt-2">إدارة وتتبع جميع العملاء والشركاء التجاريين</p>
      </div>

      {/* شريط البحث والإضافة */}
      <div className="flex justify-between items-center mb-6">
        <div className="relative">
          <Search className="w-5 h-5 absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="البحث في العملاء..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-4 pr-10 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 w-80"
          />
        </div>
        
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
        >
          <Plus className="w-4 h-4 ml-2" />
          إضافة عميل جديد
        </button>
      </div>

      {/* بطاقات العملاء */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCustomers.map((customer) => (
          <div key={customer.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-primary-600" />
                </div>
                <div className="mr-3">
                  <h3 className="text-lg font-semibold text-foreground">{customer.name}</h3>
                  <p className="text-sm text-muted-foreground">{customer.contact_person}</p>
                </div>
              </div>
              
              <div className="flex space-x-2 space-x-reverse">
                <button
                  onClick={() => setEditingCustomer(customer)}
                  className="text-primary-600 hover:text-primary-800"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDeleteCustomer(customer.id)}
                  className="text-destructive hover:text-red-800"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center text-sm text-muted-foreground">
                <Phone className="w-4 h-4 ml-2" />
                {customer.phone}
              </div>
              
              {customer.email && (
                <div className="flex items-center text-sm text-muted-foreground">
                  <Mail className="w-4 h-4 ml-2" />
                  {customer.email}
                </div>
              )}
              
              {customer.address && (
                <div className="text-sm text-muted-foreground mt-2">
                  <strong>العنوان:</strong> {customer.address}
                </div>
              )}
            </div>
            
            <div className="mt-4 pt-4 border-t border-border">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">إجمالي المشتريات:</span>
                <span className="font-medium text-foreground">
                  {Math.floor(Math.random() * 50000 + 10000).toLocaleString()} جنيه
                </span>
              </div>
              <div className="flex justify-between text-sm mt-1">
                <span className="text-muted-foreground">آخر طلب:</span>
                <span className="text-foreground">
                  {new Date(Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000).toLocaleDateString('ar-EG')}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCustomers.length === 0 && (
        <div className="text-center py-12">
          <User className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-2">لا توجد عملاء</h3>
          <p className="text-muted-foreground">لم يتم العثور على عملاء مطابقين لبحثك</p>
        </div>
      )}

      {/* نافذة إضافة/تعديل العميل */}
      {showAddModal && (
        <CustomerModal
          onSave={handleAddCustomer}
          onClose={() => setShowAddModal(false)}
        />
      )}

      {editingCustomer && (
        <CustomerModal
          customer={editingCustomer}
          onSave={handleEditCustomer}
          onClose={() => setEditingCustomer(null)}
        />
      )}
    </div>
  )
}

export default Customers


