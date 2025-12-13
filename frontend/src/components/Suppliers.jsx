import React, { useState, useEffect } from 'react'
import {
  Edit, Mail, Phone, Plus,
  Search, Trash2, Truck
} from 'lucide-react'

import toast from 'react-hot-toast'

const Suppliers = () => {
  const [suppliers, setSuppliers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingSupplier, setEditingSupplier] = useState(null)

  // بيانات تجريبية
  useEffect(() => {
    setSuppliers([
      {
        id: 1,
        name: 'شركة البذور المصرية',
        contact_person: 'أحمد محمد',
        phone: '01234567893',
        email: 'ahmed@seeds.com',
        address: 'القاهرة، مصر',
        category: 'بذور'
      },
      {
        id: 2,
        name: 'مؤسسة الأسمدة الحديثة',
        contact_person: 'محمد علي',
        phone: '01234567894',
        email: 'mohamed@fertilizers.com',
        address: 'الجيزة، مصر',
        category: 'أسمدة'
      },
      {
        id: 3,
        name: 'شركة المبيدات المتقدمة',
        contact_person: 'سارة أحمد',
        phone: '01234567895',
        email: 'sara@pesticides.com',
        address: 'الإسكندرية، مصر',
        category: 'مبيدات'
      },
      {
        id: 4,
        name: 'مشتل الأمل للشتلات',
        contact_person: 'عمر حسن',
        phone: '01234567896',
        email: 'omar@amal-nursery.com',
        address: 'المنوفية، مصر',
        category: 'شتلات'
      }
    ])
  }, [])

  const filteredSuppliers = suppliers.filter(supplier =>
    supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    supplier.contact_person.toLowerCase().includes(searchTerm.toLowerCase()) ||
    supplier.phone.includes(searchTerm) ||
    supplier.category.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddSupplier = (supplierData) => {
    const newSupplier = {
      id: Date.now(),
      ...supplierData
    }
    setSuppliers([...suppliers, newSupplier])
    setShowAddModal(false)
    toast.success('تم إضافة المورد بنجاح')
  }

  const handleEditSupplier = (supplierData) => {
    setSuppliers(suppliers.map(s => s.id === editingSupplier.id ? { ...editingSupplier, ...supplierData } : s))
    setEditingSupplier(null)
    toast.success('تم تحديث بيانات المورد بنجاح')
  }

  const handleDeleteSupplier = (id) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المورد؟')) {
      setSuppliers(suppliers.filter(s => s.id !== id))
      toast.success('تم حذف المورد بنجاح')
    }
  }

  const SupplierModal = ({ supplier, onSave, onClose }) => {
    const [formData, setFormData] = useState(supplier || {
      name: '',
      contact_person: '',
      phone: '',
      email: '',
      address: '',
      category: ''
    })

    const handleSubmit = (e) => {
      e.preventDefault()
      onSave(formData)
    }

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 className="text-lg font-semibold mb-4">
            {supplier ? 'تعديل بيانات المورد' : 'إضافة مورد جديد'}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">اسم المورد</label>
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
              <label className="block text-sm font-medium text-foreground mb-1">التخصص</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value})}
                className="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              >
                <option value="">اختر التخصص</option>
                <option value="بذور">بذور</option>
                <option value="شتلات">شتلات</option>
                <option value="أسمدة">أسمدة</option>
                <option value="مبيدات">مبيدات</option>
                <option value="أدوات زراعية">أدوات زراعية</option>
              </select>
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
                {supplier ? 'تحديث' : 'إضافة'}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  const categoryColors = {
    'بذور': 'bg-primary/20 text-green-800',
    'شتلات': 'bg-primary-100 text-primary-800',
    'أسمدة': 'bg-accent/20 text-yellow-800',
    'مبيدات': 'bg-destructive/20 text-red-800',
    'أدوات زراعية': 'bg-purple-100 text-purple-800'
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">إدارة الموردين</h1>
        <p className="text-muted-foreground mt-2">إدارة وتتبع جميع الموردين والشركاء في التوريد</p>
      </div>

      {/* شريط البحث والإضافة */}
      <div className="flex justify-between items-center mb-6">
        <div className="relative">
          <Search className="w-5 h-5 absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="البحث في الموردين..."
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
          إضافة مورد جديد
        </button>
      </div>

      {/* بطاقات الموردين */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSuppliers.map((supplier) => (
          <div key={supplier.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-accent/20 rounded-full flex items-center justify-center">
                  <Truck className="w-6 h-6 text-accent" />
                </div>
                <div className="mr-3">
                  <h3 className="text-lg font-semibold text-foreground">{supplier.name}</h3>
                  <p className="text-sm text-muted-foreground">{supplier.contact_person}</p>
                </div>
              </div>
              
              <div className="flex space-x-2 space-x-reverse">
                <button
                  onClick={() => setEditingSupplier(supplier)}
                  className="text-primary-600 hover:text-primary-800"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDeleteSupplier(supplier.id)}
                  className="text-destructive hover:text-red-800"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="mb-3">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${categoryColors[supplier.category] || 'bg-muted text-foreground'}`}>
                {supplier.category}
              </span>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center text-sm text-muted-foreground">
                <Phone className="w-4 h-4 ml-2" />
                {supplier.phone}
              </div>
              
              {supplier.email && (
                <div className="flex items-center text-sm text-muted-foreground">
                  <Mail className="w-4 h-4 ml-2" />
                  {supplier.email}
                </div>
              )}
              
              {supplier.address && (
                <div className="text-sm text-muted-foreground mt-2">
                  <strong>العنوان:</strong> {supplier.address}
                </div>
              )}
            </div>
            
            <div className="mt-4 pt-4 border-t border-border">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">إجمالي المشتريات:</span>
                <span className="font-medium text-foreground">
                  {Math.floor(Math.random() * 100000 + 20000).toLocaleString()} جنيه
                </span>
              </div>
              <div className="flex justify-between text-sm mt-1">
                <span className="text-muted-foreground">آخر طلب:</span>
                <span className="text-foreground">
                  {new Date(Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000).toLocaleDateString('ar-EG')}
                </span>
              </div>
              <div className="flex justify-between text-sm mt-1">
                <span className="text-muted-foreground">التقييم:</span>
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={`text-sm ${i < Math.floor(Math.random() * 2 + 3) ? 'text-yellow-400' : 'text-gray-300'}`}>
                      ★
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredSuppliers.length === 0 && (
        <div className="text-center py-12">
          <Truck className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-2">لا توجد موردين</h3>
          <p className="text-muted-foreground">لم يتم العثور على موردين مطابقين لبحثك</p>
        </div>
      )}

      {/* نافذة إضافة/تعديل المورد */}
      {showAddModal && (
        <SupplierModal
          onSave={handleAddSupplier}
          onClose={() => setShowAddModal(false)}
        />
      )}

      {editingSupplier && (
        <SupplierModal
          supplier={editingSupplier}
          onSave={handleEditSupplier}
          onClose={() => setEditingSupplier(null)}
        />
      )}
    </div>
  )
}

export default Suppliers


