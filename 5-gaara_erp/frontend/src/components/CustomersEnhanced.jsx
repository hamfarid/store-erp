// FILE: frontend/src/components/CustomersEnhanced.jsx | PURPOSE: Enhanced customer management interface | OWNER: Frontend Team | RELATED: Customers.jsx, CustomersAdvanced.jsx | LAST-AUDITED: 2025-10-29

import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  User, 
  Users, 
  Phone, 
  Mail, 
  MapPin,
  CreditCard,
  Filter,
  Download,
  Upload
} from 'lucide-react';
import toast from 'react-hot-toast';

const CustomersEnhanced = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    customer_type: 'individual',
    email: '',
    phone: '',
    mobile: '',
    address: '',
    tax_number: '',
    payment_terms: '',
    credit_limit: 0,
    currency: 'SAR',
    language: 'ar',
    notes: ''
  });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/customers');
      if (response.ok) {
        const data = await response.json();
        setCustomers(data);
      } else {
        toast.error('فشل في تحميل العملاء');
      }
    } catch {
      toast.error('خطأ في الاتصال بالخادم');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      toast.error('اسم العميل مطلوب');
      return;
    }

    try {
      const url = editingCustomer 
        ? `http://localhost:5002/api/customers/${editingCustomer.id}`
        : 'http://localhost:5002/api/customers';
      
      const method = editingCustomer ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        toast.success(editingCustomer ? 'تم تحديث العميل بنجاح' : 'تم إضافة العميل بنجاح');
        fetchCustomers();
        resetForm();
        setShowModal(false);
      } else {
        toast.error('فشل في حفظ العميل');
      }
    } catch {
      toast.error('خطأ في الاتصال بالخادم');
    }
  };

  const handleEdit = (customer) => {
    setEditingCustomer(customer);
    setFormData({
      name: customer.name || '',
      customer_type: customer.customer_type || 'individual',
      email: customer.email || '',
      phone: customer.phone || '',
      mobile: customer.mobile || '',
      address: customer.address || '',
      tax_number: customer.tax_number || '',
      payment_terms: customer.payment_terms || '',
      credit_limit: customer.credit_limit || 0,
      currency: customer.currency || 'SAR',
      language: customer.language || 'ar',
      notes: customer.notes || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('هل أنت متأكد من حذف هذا العميل؟')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5002/api/customers/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        toast.success('تم حذف العميل بنجاح');
        fetchCustomers();
      } else {
        toast.error('فشل في حذف العميل');
      }
    } catch {
      toast.error('خطأ في الاتصال بالخادم');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      customer_type: 'individual',
      email: '',
      phone: '',
      mobile: '',
      address: '',
      tax_number: '',
      payment_terms: '',
      credit_limit: 0,
      currency: 'SAR',
      language: 'ar',
      notes: ''
    });
    setEditingCustomer(null);
  };

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (customer.email && customer.email.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFilter = filterType === 'all' || customer.customer_type === filterType;
    
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold text-gray-800 flex items-center">
            <Users className="ml-2 text-green-600" />
            إدارة العملاء
          </h1>
          <button
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors"
          >
            <Plus className="ml-2" size={20} />
            إضافة عميل جديد
          </button>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="البحث في العملاء..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pr-10 pl-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="all">جميع الأنواع</option>
            <option value="individual">فرد</option>
            <option value="company">شركة</option>
          </select>

          <div className="flex gap-2">
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center transition-colors">
              <Download className="ml-2" size={16} />
              تصدير
            </button>
            <button className="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg flex items-center transition-colors">
              <Upload className="ml-2" size={16} />
              استيراد
            </button>
          </div>
        </div>
      </div>

      {/* Customers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCustomers.map((customer) => (
          <div key={customer.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center">
                <User className="text-green-600 ml-2" size={24} />
                <div>
                  <h3 className="font-semibold text-gray-800">{customer.name}</h3>
                  <span className="text-sm text-gray-500">
                    {customer.customer_type === 'individual' ? 'فرد' : 'شركة'}
                  </span>
                </div>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(customer)}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <Edit size={16} />
                </button>
                <button
                  onClick={() => handleDelete(customer.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>

            <div className="space-y-2 text-sm text-gray-600">
              {customer.email && (
                <div className="flex items-center">
                  <Mail className="ml-2" size={16} />
                  {customer.email}
                </div>
              )}
              {customer.phone && (
                <div className="flex items-center">
                  <Phone className="ml-2" size={16} />
                  {customer.phone}
                </div>
              )}
              {customer.credit_limit > 0 && (
                <div className="flex items-center">
                  <CreditCard className="ml-2" size={16} />
                  حد الائتمان: {customer.credit_limit} {customer.currency}
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
              <span className="text-xs text-gray-400">
                تم الإنشاء: {new Date(customer.created_at).toLocaleDateString('ar-SA')}
              </span>
            </div>
          </div>
        ))}
      </div>

      {filteredCustomers.length === 0 && (
        <div className="text-center py-12">
          <Users className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-500">لا توجد عملاء</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {editingCustomer ? 'تعديل العميل' : 'إضافة عميل جديد'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    اسم العميل *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    نوع العميل
                  </label>
                  <select
                    value={formData.customer_type}
                    onChange={(e) => setFormData({...formData, customer_type: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="individual">فرد</option>
                    <option value="company">شركة</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    البريد الإلكتروني
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    رقم الهاتف
                  </label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    حد الائتمان
                  </label>
                  <input
                    type="number"
                    value={formData.credit_limit}
                    onChange={(e) => setFormData({...formData, credit_limit: parseFloat(e.target.value) || 0})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    العملة
                  </label>
                  <select
                    value={formData.currency}
                    onChange={(e) => setFormData({...formData, currency: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="SAR">ريال سعودي</option>
                    <option value="USD">دولار أمريكي</option>
                    <option value="EUR">يورو</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  العنوان
                </label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ملاحظات
                </label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div className="flex justify-end gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  إلغاء
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                >
                  {editingCustomer ? 'تحديث' : 'إضافة'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomersEnhanced;