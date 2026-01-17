import React, { useState, useEffect } from 'react';
import {
  Package,
  Plus,
  Search,
  Edit,
  Trash2,
  AlertTriangle,
  Filter,
  Download,
  Upload
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import ProductModal from './ProductModal';
import { DeleteConfirmDialog } from './common/ConfirmDialog';
import { useToast } from './common/Toast';
import apiClient from '../services/apiClient';
import EmptyState from './ui/EmptyState';

const UnifiedProductsManager = () => {
  const { hasPermission } = useAuth();
  const { showSuccess, showError } = useToast();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [productToDelete, setProductToDelete] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get('/api/products');
      
      if (data.success || data.status === 'success') {
        const productsList = data.products || data.data?.products || [];
        setProducts(productsList);
      } else {
        throw new Error(data.message || 'فشل في تحميل المنتجات');
      }
    } catch (error) {
      setError(error.message);
      
      // بيانات احتياطية للعرض
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProduct = (productId) => {
    if (!hasPermission('products.delete')) {
      alert('ليس لديك صلاحية لحذف المنتجات');
      return;
    }

    const product = products.find(p => p.id === productId);
    setProductToDelete(product);
    setShowDeleteConfirm(true);
  };

  const confirmDeleteProduct = async () => {
    if (!productToDelete) return;

    setDeleteLoading(true);
    try {
      const data = await apiClient.delete(`/api/products/${productToDelete.id}`);
      
      if (data.success || data.status === 'success') {
        setProducts(products.filter(p => p.id !== productToDelete.id));
        setShowDeleteConfirm(false);
        setProductToDelete(null);
        showSuccess('تم حذف المنتج بنجاح');
      } else {
        throw new Error(data.message || 'فشل في حذف المنتج');
      }
    } catch (error) {
      showError('خطأ في حذف المنتج: ' + error.message);
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleEditProduct = (product) => {
    setSelectedProduct(product);
    setShowEditModal(true);
  };

  const handleFilterProducts = () => {
    // TODO: Implement filtering logic
    };

  const handleExportProducts = async () => {
    setExportLoading(true);
    try {
      // تحضير البيانات للتصدير
      const exportData = filteredProducts.map(product => ({
        'اسم المنتج': product.name,
        'الكود': product.code,
        'الباركود': product.barcode || '',
        'الفئة': getCategoryName(product.category_id),
        'المخزون الحالي': product.current_stock,
        'الحد الأدنى': product.min_stock,
        'سعر التكلفة': product.cost_price,
        'سعر البيع': product.selling_price,
        'الوصف': product.description || ''
      }));

      // تحويل إلى CSV
      const headers = Object.keys(exportData[0] || {});
      const csvContent = [
        headers.join(','),
        ...exportData.map(row =>
          headers.map(header => `"${row[header] || ''}"`).join(',')
        )
      ].join('\n');

      // إنشاء ملف وتحميله
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `products_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      showSuccess(`تم تصدير ${exportData.length} منتج بنجاح`);
    } catch (error) {
      showError('حدث خطأ أثناء التصدير');
    } finally {
      setExportLoading(false);
    }
  };

  const getCategoryName = (categoryId) => {
    const categories = {
      1: 'بذور',
      2: 'أسمدة',
      3: 'مبيدات',
      4: 'أدوات زراعية'
    };
    return categories[categoryId] || 'غير محدد';
  };

  const handleSaveProduct = async (productData) => {
    try {
      const url = selectedProduct
        ? `http://localhost:5000/api/products/${selectedProduct.id}`
        : 'http://localhost:5000/api/products';

      const method = selectedProduct ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(productData)
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          if (selectedProduct) {
            // تحديث المنتج في القائمة
            setProducts(products.map(p =>
              p.id === selectedProduct.id ? { ...p, ...productData } : p
            ));
            alert('تم تحديث المنتج بنجاح');
          } else {
            // إضافة المنتج الجديد
            setProducts([...products, data.product]);
            alert('تم إضافة المنتج بنجاح');
          }
          setShowAddModal(false);
          setShowEditModal(false);
          setSelectedProduct(null);
        } else {
          throw new Error(data.message || 'فشل في حفظ المنتج');
        }
      } else {
        throw new Error('خطأ في الاتصال بالخادم');
      }
    } catch (error) {
      alert('خطأ في حفظ المنتج: ' + error.message);
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.code?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || product.category_id === parseInt(selectedCategory);
    return matchesSearch && matchesCategory;
  });

  const ProductCard = ({ product }) => (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-foreground" dir="rtl">{product.name}</h3>
          <p className="text-sm text-muted-foreground" dir="rtl">كود: {product.code}</p>
          {product.barcode && (
            <p className="text-sm text-muted-foreground" dir="rtl">باركود: {product.barcode}</p>
          )}
        </div>
        <div className="flex space-x-2 rtl:space-x-reverse">
          {hasPermission('products.edit') && (
            <button
              onClick={() => handleEditProduct(product)}
              className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200 hover:scale-110 active:scale-95"
              title="تعديل المنتج"
            >
              <Edit className="w-4 h-4" />
            </button>
          )}
          {hasPermission('products.delete') && (
            <button
              onClick={() => handleDeleteProduct(product.id)}
              className="p-2 text-destructive hover:bg-destructive/10 rounded-lg transition-all duration-200 hover:scale-110 active:scale-95"
              title="حذف المنتج"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-muted-foreground" dir="rtl">المخزون الحالي:</span>
          <span className={`font-medium ${product.current_stock <= product.min_stock ? 'text-destructive' : 'text-primary'}`}>
            {product.current_stock} {product.unit}
          </span>
        </div>
        <div>
          <span className="text-muted-foreground" dir="rtl">سعر البيع:</span>
          <span className="font-medium text-foreground">{product.selling_price} ج.م</span>
        </div>
        <div>
          <span className="text-muted-foreground" dir="rtl">الحد الأدنى:</span>
          <span className="font-medium text-muted-foreground">{product.min_stock} {product.unit}</span>
        </div>
        <div>
          <span className="text-muted-foreground" dir="rtl">سعر التكلفة:</span>
          <span className="font-medium text-muted-foreground">{product.cost_price} ج.م</span>
        </div>
      </div>

      {product.current_stock <= product.min_stock && (
        <div className="mt-4 flex items-center text-destructive bg-destructive/10 p-2 rounded">
          <AlertTriangle className="w-4 h-4 ml-2" />
          <span className="text-sm" dir="rtl">مخزون منخفض</span>
        </div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-muted/50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-muted-foreground" dir="rtl">جاري تحميل المنتجات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-muted/50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Package className="w-6 h-6 text-primary-600 ml-3" />
              <h1 className="text-xl font-semibold text-foreground" dir="rtl">
                إدارة المنتجات
              </h1>
            </div>
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              <button
                onClick={() => setShowAddModal(true)}
                className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
              >
                <Plus className="w-4 h-4 ml-2" />
                <span dir="rtl">إضافة منتج</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          
          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-destructive/10 border border-destructive/30 rounded-lg p-4">
              <div className="flex">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <div className="ml-3 rtl:mr-3 rtl:ml-0">
                  <p className="text-sm text-destructive" dir="rtl">
                    خطأ: {error}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Search and Filters */}
          <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="relative">
                <Search className="absolute right-3 top-3 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="البحث في المنتجات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pr-10 pl-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  dir="rtl"
                />
              </div>
              
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                dir="rtl"
              >
                <option value="">جميع الفئات</option>
                <option value="1">بذور</option>
                <option value="2">أسمدة</option>
                <option value="3">مبيدات</option>
                <option value="4">أدوات زراعية</option>
              </select>

              <div className="flex space-x-2 rtl:space-x-reverse">
                <button
                  onClick={handleFilterProducts}
                  className="flex-1 bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted flex items-center justify-center transition-colors"
                  title="تطبيق الفلاتر"
                >
                  <Filter className="w-4 h-4 ml-2" />
                  <span dir="rtl">فلترة</span>
                </button>
                <button
                  onClick={handleExportProducts}
                  disabled={exportLoading}
                  className="flex-1 bg-primary/20 text-primary px-4 py-2 rounded-lg hover:bg-green-200 flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  title="تصدير قائمة المنتجات"
                >
                  {exportLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-700 ml-2"></div>
                      <span dir="rtl">جاري التصدير...</span>
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4 ml-2" />
                      <span dir="rtl">تصدير</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Products Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          {/* Empty State */}
          {filteredProducts.length === 0 && !loading && (
            <EmptyState
              icon="package"
              title={searchTerm || selectedCategory ? 'لا توجد نتائج' : 'لا توجد منتجات'}
              description={
                searchTerm || selectedCategory
                  ? `لم يتم العثور على منتجات تطابق ${searchTerm ? `"${searchTerm}"` : 'الفئة المحددة'}. جرب البحث بكلمات مختلفة أو أضف منتجاً جديداً.`
                  : 'ابدأ بإضافة منتجك الأول لبناء مخزونك. يمكنك إضافة منتج واحد أو استيراد عدة منتجات من ملف Excel.'
              }
              actionText="إضافة منتج جديد"
              onAction={() => setShowAddModal(true)}
              secondaryActionText="استيراد من Excel"
              onSecondaryAction={() => setShowImportModal(true)}
            />
          )}
        </div>
      </main>

      {/* Product Modals */}
      <ProductModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSave={handleSaveProduct}
        title="إضافة منتج جديد"
      />

      <ProductModal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          setSelectedProduct(null);
        }}
        onSave={handleSaveProduct}
        product={selectedProduct}
        title="تعديل المنتج"
      />

      {/* Delete Confirmation Dialog */}
      <DeleteConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => {
          setShowDeleteConfirm(false);
          setProductToDelete(null);
        }}
        onConfirm={confirmDeleteProduct}
        itemName={productToDelete?.name}
        loading={deleteLoading}
      />
    </div>
  );
};

export default UnifiedProductsManager;

