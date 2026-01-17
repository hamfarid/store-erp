import React, { useState, useEffect } from 'react';
import { X, Save, Package, DollarSign, Hash, BarChart3 } from 'lucide-react';
import { SaveButton, CancelButton } from './common/EnhancedButton';

const ProductModal = ({ 
  isOpen, 
  onClose, 
  onSave, 
  product = null, 
  title = "إضافة منتج جديد" 
}) => {
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    barcode: '',
    category_id: '',
    warehouse_id: '1',
    current_stock: '',
    min_stock: '',
    cost_price: '',
    selling_price: '',
    description: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  // تحديث البيانات عند تغيير المنتج
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        code: product.code || '',
        barcode: product.barcode || '',
        category_id: product.category_id || '',
        warehouse_id: product.warehouse_id || '1',
        current_stock: product.current_stock || '',
        min_stock: product.min_stock || '',
        cost_price: product.cost_price || '',
        selling_price: product.selling_price || '',
        description: product.description || ''
      });
    } else {
      // إعادة تعيين النموذج للمنتج الجديد
      setFormData({
        name: '',
        code: '',
        barcode: '',
        category_id: '',
        warehouse_id: '1',
        current_stock: '',
        min_stock: '',
        cost_price: '',
        selling_price: '',
        description: ''
      });
    }
    setErrors({});
  }, [product, isOpen]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // إزالة الخطأ عند التعديل
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'اسم المنتج مطلوب';
    }

    if (!formData.code.trim()) {
      newErrors.code = 'كود المنتج مطلوب';
    }

    if (!formData.category_id) {
      newErrors.category_id = 'فئة المنتج مطلوبة';
    }

    if (!formData.current_stock || formData.current_stock < 0) {
      newErrors.current_stock = 'المخزون الحالي مطلوب ويجب أن يكون رقم موجب';
    }

    if (!formData.min_stock || formData.min_stock < 0) {
      newErrors.min_stock = 'الحد الأدنى للمخزون مطلوب ويجب أن يكون رقم موجب';
    }

    if (!formData.cost_price || formData.cost_price <= 0) {
      newErrors.cost_price = 'سعر التكلفة مطلوب ويجب أن يكون أكبر من صفر';
    }

    if (!formData.selling_price || formData.selling_price <= 0) {
      newErrors.selling_price = 'سعر البيع مطلوب ويجب أن يكون أكبر من صفر';
    }

    if (formData.selling_price && formData.cost_price && 
        parseFloat(formData.selling_price) <= parseFloat(formData.cost_price)) {
      newErrors.selling_price = 'سعر البيع يجب أن يكون أكبر من سعر التكلفة';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      await onSave(formData);
      onClose();
    } catch (error) {
      } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold text-foreground" dir="rtl">
            {title}
          </h2>
          <button
            onClick={handleClose}
            disabled={loading}
            className="p-2 hover:bg-muted rounded-lg transition-colors disabled:opacity-50"
            title="إغلاق"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* اسم المنتج */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                <Package className="w-4 h-4 inline ml-1" />
                اسم المنتج *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.name ? 'border-red-500' : 'border-border'
                }`}
                placeholder="أدخل اسم المنتج"
                dir="rtl"
                disabled={loading}
              />
              {errors.name && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.name}</p>
              )}
            </div>

            {/* كود المنتج */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                <Hash className="w-4 h-4 inline ml-1" />
                كود المنتج *
              </label>
              <input
                type="text"
                name="code"
                value={formData.code}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.code ? 'border-red-500' : 'border-border'
                }`}
                placeholder="مثل: SEED-001"
                dir="rtl"
                disabled={loading}
              />
              {errors.code && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.code}</p>
              )}
            </div>

            {/* الباركود */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                الباركود
              </label>
              <input
                type="text"
                name="barcode"
                value={formData.barcode}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="اختياري"
                dir="rtl"
                disabled={loading}
              />
            </div>

            {/* الفئة */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                الفئة *
              </label>
              <select
                name="category_id"
                value={formData.category_id}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.category_id ? 'border-red-500' : 'border-border'
                }`}
                dir="rtl"
                disabled={loading}
              >
                <option value="">اختر الفئة</option>
                <option value="1">بذور</option>
                <option value="2">أسمدة</option>
                <option value="3">مبيدات</option>
                <option value="4">أدوات زراعية</option>
              </select>
              {errors.category_id && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.category_id}</p>
              )}
            </div>

            {/* المخزن */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                المخزن
              </label>
              <select
                name="warehouse_id"
                value={formData.warehouse_id}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                dir="rtl"
                disabled={loading}
              >
                <option value="1">المخزن الرئيسي - القاهرة</option>
              </select>
            </div>

            {/* المخزون الحالي */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                <BarChart3 className="w-4 h-4 inline ml-1" />
                المخزون الحالي *
              </label>
              <input
                type="number"
                name="current_stock"
                value={formData.current_stock}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.current_stock ? 'border-red-500' : 'border-border'
                }`}
                placeholder="0"
                min="0"
                step="0.01"
                disabled={loading}
              />
              {errors.current_stock && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.current_stock}</p>
              )}
            </div>

            {/* الحد الأدنى */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                الحد الأدنى *
              </label>
              <input
                type="number"
                name="min_stock"
                value={formData.min_stock}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.min_stock ? 'border-red-500' : 'border-border'
                }`}
                placeholder="0"
                min="0"
                step="0.01"
                disabled={loading}
              />
              {errors.min_stock && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.min_stock}</p>
              )}
            </div>

            {/* سعر التكلفة */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                <DollarSign className="w-4 h-4 inline ml-1" />
                سعر التكلفة *
              </label>
              <input
                type="number"
                name="cost_price"
                value={formData.cost_price}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.cost_price ? 'border-red-500' : 'border-border'
                }`}
                placeholder="0.00"
                min="0"
                step="0.01"
                disabled={loading}
              />
              {errors.cost_price && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.cost_price}</p>
              )}
            </div>

            {/* سعر البيع */}
            <div>
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                <DollarSign className="w-4 h-4 inline ml-1" />
                سعر البيع *
              </label>
              <input
                type="number"
                name="selling_price"
                value={formData.selling_price}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.selling_price ? 'border-red-500' : 'border-border'
                }`}
                placeholder="0.00"
                min="0"
                step="0.01"
                disabled={loading}
              />
              {errors.selling_price && (
                <p className="text-red-500 text-sm mt-1" dir="rtl">{errors.selling_price}</p>
              )}
            </div>

            {/* الوصف */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-foreground mb-2" dir="rtl">
                الوصف
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows="3"
                className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="وصف اختياري للمنتج"
                dir="rtl"
                disabled={loading}
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-4 rtl:space-x-reverse mt-6 pt-6 border-t">
            <button
              type="button"
              onClick={handleClose}
              disabled={loading}
              className="px-4 py-2 text-foreground bg-muted rounded-lg hover:bg-muted transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              إلغاء
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center min-w-[100px] justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white ml-2"></div>
                  جاري الحفظ...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 ml-2" />
                  {product ? 'تحديث' : 'حفظ'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductModal;

