import React, { useState, useEffect } from 'react';
import { X, Package, Warehouse, Calendar, Hash } from 'lucide-react';
import apiClient from '../../services/apiClient';

const LotAddModal = ({ isOpen, onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [formData, setFormData] = useState({
    lot_number: '',
    product_id: '',
    warehouse_id: '',
    quantity: '',
    production_date: '',
    expiry_date: '',
    notes: ''
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (isOpen) {
      loadProducts();
      loadWarehouses();
      // Generate automatic lot number
      generateLotNumber();
    }
  }, [isOpen]);

  const loadProducts = async () => {
    try {
      const response = await apiClient.get('/api/products');
      if (response.success && response.data) {
        setProducts(response.data.products || response.data);
      }
    } catch (error) {
      console.error('Error loading products:', error);
    }
  };

  const loadWarehouses = async () => {
    try {
      const response = await apiClient.get('/api/warehouses');
      if (response.success && response.data) {
        setWarehouses(response.data.warehouses || response.data);
      }
    } catch (error) {
      console.error('Error loading warehouses:', error);
    }
  };

  const generateLotNumber = () => {
    const date = new Date();
    const lotNumber = `LOT-${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
    setFormData(prev => ({ ...prev, lot_number: lotNumber }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      return { ...prev, [name]: value };
    });
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.lot_number.trim()) newErrors.lot_number = 'رقم اللوط مطلوب';
    if (!formData.product_id) newErrors.product_id = 'المنتج مطلوب';
    if (!formData.warehouse_id) newErrors.warehouse_id = 'المخزن مطلوب';
    if (!formData.quantity || parseFloat(formData.quantity) <= 0) {
      newErrors.quantity = 'الكمية مطلوبة ويجب أن تكون أكبر من صفر';
    }
    if (!formData.production_date) newErrors.production_date = 'تاريخ الإنتاج مطلوب';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await apiClient.post('/api/lots', {
        ...formData,
        product_id: parseInt(formData.product_id),
        warehouse_id: parseInt(formData.warehouse_id),
        quantity: parseFloat(formData.quantity)
      });

      if (response.success) {
        onSuccess(response.data);
        handleClose();
      } else {
        setErrors({ submit: response.message || 'فشل في إضافة اللوط' });
      }
    } catch (error) {
      console.error('Error adding lot:', error);
      setErrors({ submit: error.message || 'حدث خطأ أثناء إضافة اللوط' });
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      lot_number: '',
      product_id: '',
      warehouse_id: '',
      quantity: '',
      production_date: '',
      expiry_date: '',
      notes: ''
    });
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Package className="w-6 h-6 text-orange-600" />
            </div>
            <h2 className="text-xl font-bold text-gray-800">إضافة لوط جديد</h2>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6">
          <div className="space-y-6">
            {errors.submit && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {errors.submit}
              </div>
            )}

            {/* Lot Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Hash className="w-4 h-4 inline ml-1" />
                رقم اللوط <span className="text-red-500">*</span>
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  name="lot_number"
                  value={formData.lot_number}
                  onChange={handleChange}
                  className={`flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 ${
                    errors.lot_number ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="LOT-XXXXXXXX"
                  readOnly
                />
                <button
                  type="button"
                  onClick={generateLotNumber}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  توليد جديد
                </button>
              </div>
              {errors.lot_number && <p className="mt-1 text-sm text-red-500">{errors.lot_number}</p>}
            </div>

            {/* Product & Warehouse */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Package className="w-4 h-4 inline ml-1" />
                  المنتج <span className="text-red-500">*</span>
                </label>
                <select
                  name="product_id"
                  value={formData.product_id}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 ${
                    errors.product_id ? 'border-red-500' : 'border-gray-300'
                  }`}
                >
                  <option value="">اختر المنتج</option>
                  {products.map(product => (
                    <option key={product.id} value={product.id}>
                      {product.name} ({product.sku})
                    </option>
                  ))}
                </select>
                {errors.product_id && <p className="mt-1 text-sm text-red-500">{errors.product_id}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Warehouse className="w-4 h-4 inline ml-1" />
                  المخزن <span className="text-red-500">*</span>
                </label>
                <select
                  name="warehouse_id"
                  value={formData.warehouse_id}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 ${
                    errors.warehouse_id ? 'border-red-500' : 'border-gray-300'
                  }`}
                >
                  <option value="">اختر المخزن</option>
                  {warehouses.map(warehouse => (
                    <option key={warehouse.id} value={warehouse.id}>
                      {warehouse.name}
                    </option>
                  ))}
                </select>
                {errors.warehouse_id && <p className="mt-1 text-sm text-red-500">{errors.warehouse_id}</p>}
              </div>
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                الكمية <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                step="0.01"
                min="0"
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 ${
                  errors.quantity ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="0.00"
              />
              {errors.quantity && <p className="mt-1 text-sm text-red-500">{errors.quantity}</p>}
            </div>

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="w-4 h-4 inline ml-1" />
                  تاريخ الإنتاج <span className="text-red-500">*</span>
                </label>
                <input
                  type="date"
                  name="production_date"
                  value={formData.production_date}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 ${
                    errors.production_date ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {errors.production_date && <p className="mt-1 text-sm text-red-500">{errors.production_date}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="w-4 h-4 inline ml-1" />
                  تاريخ الانتهاء
                </label>
                <input
                  type="date"
                  name="expiry_date"
                  value={formData.expiry_date}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                />
              </div>
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ملاحظات
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                placeholder="أي ملاحظات إضافية..."
              />
            </div>
          </div>
        </form>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            type="button"
            onClick={handleClose}
            disabled={loading}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50"
          >
            إلغاء
          </button>
          <button
            type="submit"
            onClick={handleSubmit}
            disabled={loading}
            className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                جاري الحفظ...
              </>
            ) : (
              <>
                <Package className="w-4 h-4" />
                حفظ اللوط
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LotAddModal;
