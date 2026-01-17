import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Building, 
  User, 
  Phone, 
  Mail, 
  MapPin,
  Filter,
  Download,
  Upload
} from 'lucide-react';
import toast from 'react-hot-toast';

const SuppliersEnhanced = () => {
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    company_type: 'company',
    email: '',
    phone: '',
    mobile: '',
    website: '',
    address: '',
    tax_number: '',
    payment_terms: '',
    preferred_payment_method: '',
    currency: 'SAR',
    language: 'ar',
    notes: ''
  });

  useEffect(() => {
    fetchSuppliers();
  }, []);

  const fetchSuppliers = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/suppliers');
      if (response.ok) {
        const data = await response.json();
        setSuppliers(data);
      } else {
        toast.error('فشل في تحميل الموردين');
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
      toast.error('اسم المورد مطلوب');
      return;
    }

    try {
      const url = editingSupplier 
        ? `http://localhost:5002/api/suppliers/${editingSupplier.id}`
        : 'http://localhost:5002/api/suppliers';
      
      const method = editingSupplier ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        toast.success(editingSupplier ? 'تم تحديث المورد بنجاح' : 'تم إضافة المورد بنجاح');
        fetchSuppliers();
        resetForm();
        setShowModal(false);
      } else {
        toast.error('فشل في حفظ المورد');
      }
    } catch {
      toast.error('خطأ في الاتصال بالخادم');
    }
  };

  const handleEdit = (supplier) => {
    setEditingSupplier(supplier);
    setFormData({
      name: supplier.name || '',
      company_type: supplier.company_type || 'company',
      email: supplier.email || '',
      phone: supplier.phone || '',
      mobile: supplier.mobile || '',
      website: supplier.website || '',
      address: supplier.address || '',
      tax_number: supplier.tax_number || '',
      payment_terms: supplier.payment_terms || '',
      preferred_payment_method: supplier.preferred_payment_method || '',
      currency: supplier.currency || 'SAR',
      language: supplier.language || 'ar',
      notes: supplier.notes || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('هل أنت متأكد من حذف هذا المورد؟')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5002/api/suppliers/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        toast.success('تم حذف المورد بنجاح');
        fetchSuppliers();
      } else {
        toast.error('فشل في حذف المورد');
      }
    } catch {
      toast.error('خطأ في الاتصال بالخادم');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      company_type: 'company',
      email: '',
      phone: '',
      mobile: '',
      website: '',
      address: '',
      tax_number: '',
      payment_terms: '',
      preferred_payment_method: '',
      currency: 'SAR',
      language: 'ar',
      notes: ''
    });
    setEditingSupplier(null);
  };

  const filteredSuppliers = suppliers.filter(supplier => {
    const matchesSearch = supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (supplier.email && supplier.email.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFilter = filterType === 'all' || supplier.company_type === filterType;
    
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold text-gray-800 flex items-center">
            <Building className="ml-2 text-blue-600" />
            إدارة الموردين
          </h1>
          <button
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors"
          >
            <Plus className="ml-2" size={20} />
            إضافة مورد جديد
          </button>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="البحث في الموردين..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pr-10 pl-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">جميع الأنواع</option>
            <option value="company">شركة</option>
            <option value="individual">فرد</option>
          </select>

          <div className="flex gap-2">
            <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg flex items-center transition-colors">
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

      {/* Suppliers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSuppliers.map((supplier) => (
          <div key={supplier.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center">
                {supplier.company_type === 'company' ? (
                  <Building className="text-blue-600 ml-2" size={24} />
                ) : (
                  <User className="text-green-600 ml-2" size={24} />
                )}
                <div>
                  <h3 className="font-semibold text-gray-800">{supplier.name}</h3>
                  <span className="text-sm text-gray-500">
                    {supplier.company_type === 'company' ? 'شركة' : 'فرد'}
                  </span>
                </div>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(supplier)}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <Edit size={16} />
                </button>
                <button
                  onClick={() => handleDelete(supplier.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>

            <div className="space-y-2 text-sm text-gray-600">
              {supplier.email && (
                <div className="flex items-center">
                  <Mail className="ml-2" size={16} />
                  {supplier.email}
                </div>
              )}
              {supplier.phone && (
                <div className="flex items-center">
                  <Phone className="ml-2" size={16} />
                  {supplier.phone}
                </div>
              )}
              {supplier.address && (
                <div className="flex items-center">
                  <MapPin className="ml-2" size={16} />
                  {supplier.address}
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
              <span className="text-xs text-gray-400">
                تم الإنشاء: {new Date(supplier.created_at).toLocaleDateString('ar-SA')}
              </span>
            </div>
          </div>
        ))}
      </div>

      {filteredSuppliers.length === 0 && (
        <div className="text-center py-12">
          <Building className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-500">لا توجد موردين</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {editingSupplier ? 'تعديل المورد' : 'إضافة مورد جديد'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    اسم المورد *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    نوع المورد
                  </label>
                  <select
                    value={formData.company_type}
                    onChange={(e) => setFormData({...formData, company_type: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="company">شركة</option>
                    <option value="individual">فرد</option>
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    رقم الجوال
                  </label>
                  <input
                    type="tel"
                    value={formData.mobile}
                    onChange={(e) => setFormData({...formData, mobile: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    الموقع الإلكتروني
                  </label>
                  <input
                    type="url"
                    value={formData.website}
                    onChange={(e) => setFormData({...formData, website: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
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
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  {editingSupplier ? 'تحديث' : 'إضافة'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default SuppliersEnhanced;