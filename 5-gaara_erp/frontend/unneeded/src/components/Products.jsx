import React, { useState, useEffect } from 'react'
import {
  AlertTriangle, Edit, FileSpreadsheet, Package,
  Plus, Search, Trash2
} from 'lucide-react'

import toast from 'react-hot-toast'
import ApiService from '../services/ApiService'
import { validateProduct } from '../utils/validation'
import {
  FormInput, FormSelect, FormTextarea, Modal, Button
} from './ui/FormComponents'
import ExcelImport from './ExcelImport'
import { isSuccess, getErrorMessage } from '../utils/responseHelper'
import EmptyState from './ui/EmptyState'

const Products = () => {
  const [products, setProducts] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [showImportModal, setShowImportModal] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [deleteConfirm, setDeleteConfirm] = useState(null)

  // تحميل المنتجات عند بدء التشغيل
  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await ApiService.getProducts()
      if (isSuccess(response)) {
        setProducts(response.data)
      } else {
        throw new Error(getErrorMessage(response, 'فشل في تحميل المنتجات'))
      }
    } catch (err) {
      setError(err.message)
      toast.error('فشل في تحميل المنتجات')
      // استخدام البيانات التجريبية في حالة فشل API
      setProducts([
        {
          id: 1,
          name: 'بذور طماطم هجين',
          sku: 'TOM-001',
          category: 'بذور',
          unit: 'كيس',
          cost_price: 50,
          selling_price: 75,
          quantity: 100,
          min_quantity: 10
        },
        {
          id: 2,
          name: 'بذور خيار هجين',
          sku: 'CUC-001',
          category: 'بذور',
          unit: 'كيس',
          cost_price: 40,
          selling_price: 60,
          quantity: 80,
          min_quantity: 15
        },
        {
          id: 3,
          name: 'شتلات طماطم',
          sku: 'TOM-S001',
          category: 'شتلات',
          unit: 'صينية',
          cost_price: 25,
          selling_price: 40,
          quantity: 5,
          min_quantity: 50
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const lowStockProducts = products.filter(product => product.quantity <= product.min_quantity)

  const handleAddProduct = async (productData) => {
    try {
      const response = await ApiService.createProduct(productData)
      if (isSuccess(response)) {
        setProducts([...products, response.data])
        setShowAddModal(false)
        toast.success('تم إضافة المنتج بنجاح')
      } else {
        throw new Error(getErrorMessage(response, 'فشل في إضافة المنتج'))
      }
    } catch (err) {
      toast.error(err.message)
      // محاكاة الإضافة محلياً في حالة فشل API
      const newProduct = {
        id: Date.now(),
        ...productData
      }
      setProducts([...products, newProduct])
      setShowAddModal(false)
      toast.success('تم إضافة المنتج بنجاح (محلياً)')
    }
  }

  const handleEditProduct = async (productData) => {
    try {
      const response = await ApiService.updateProduct(editingProduct.id, productData)
      if (isSuccess(response)) {
        setProducts(products.map(p => p.id === editingProduct.id ? response.data : p))
        setEditingProduct(null)
        toast.success('تم تحديث المنتج بنجاح')
      } else {
        throw new Error(getErrorMessage(response, 'فشل في تحديث المنتج'))
      }
    } catch (err) {
      toast.error(err.message)
      // محاكاة التحديث محلياً في حالة فشل API
      setProducts(products.map(p => p.id === editingProduct.id ? { ...editingProduct, ...productData } : p))
      setEditingProduct(null)
      toast.success('تم تحديث المنتج بنجاح (محلياً)')
    }
  }

  const handleDeleteProduct = async (id) => {
    try {
      const response = await ApiService.deleteProduct(id)
      if (isSuccess(response)) {
        setProducts(products.filter(p => p.id !== id))
        toast.success('تم حذف المنتج بنجاح')
      } else {
        throw new Error(getErrorMessage(response, 'فشل في حذف المنتج'))
      }
    } catch (err) {
      toast.error(err.message)
      // محاكاة الحذف محلياً في حالة فشل API
      setProducts(products.filter(p => p.id !== id))
      toast.success('تم حذف المنتج بنجاح (محلياً)')
    }
    setDeleteConfirm(null)
  }

  // معالجة استيراد Excel
  const handleExcelImport = (importedData) => {
    try {
      const newProducts = importedData.map((row, index) => ({
        id: Date.now() + index,
        name: row['اسم المنتج'] || '',
        code: row['الكود'] || '',
        category: row['الفئة'] || '',
        unit: row['الوحدة'] || '',
        cost_price: parseFloat(row['السعر']) || 0,
        selling_price: parseFloat(row['السعر']) || 0,
        min_quantity: parseInt(row['الكمية الدنيا']) || 0,
        warehouse: row['المخزن'] || '',
        lot_number: row['اللوط'] || '',
        expiry_date: row['تاريخ الانتهاء'] || '',
        current_stock: parseInt(row['الكمية']) || 0,
        status: 'نشط'
      }))

      // إضافة المنتجات الجديدة
      setProducts(prevProducts => [...prevProducts, ...newProducts])
      setShowImportModal(false)
      toast.success(`تم استيراد ${newProducts.length} منتج بنجاح!`)
    } catch (error) {
      toast.error('خطأ في معالجة البيانات المستوردة')
    }
  }

  const ProductModal = ({ product, onSave, onClose }) => {
    const [formData, setFormData] = useState(product || {
      name: '',
      rank_id: '',
      unit: '',
      cost_price: '',
      selling_price: '',
      purchase_price_euro: '',
      purchase_price_egp: '',
      reorder_quantity: '',
      treatment_type: '',
      barcode: '',
      description: ''
    })
    const [errors, setErrors] = useState({})
    const [submitting, setSubmitting] = useState(false)
    const [categories, setCategories] = useState([])
    const [productGroups, setProductGroups] = useState([])
    const [ranks, setRanks] = useState([])
    const [selectedCategory, setSelectedCategory] = useState('')
    const [selectedGroup, setSelectedGroup] = useState('')

    // Load hierarchy data on component mount
    useEffect(() => {
      const loadHierarchyData = async () => {
        try {
          const [categoriesRes, groupsRes, ranksRes] = await Promise.all([
            ApiService.get('/categories'),
            ApiService.get('/product-groups'),
            ApiService.get('/ranks')
          ])

          if (isSuccess(categoriesRes)) setCategories(categoriesRes.data)
          if (isSuccess(groupsRes)) setProductGroups(groupsRes.data)
          if (isSuccess(ranksRes)) setRanks(ranksRes.data)
        } catch (error) {
          }
      }

      loadHierarchyData()
    }, [])

    // Filter groups based on selected category
    const filteredGroups = productGroups.filter(group =>
      group.category_id === parseInt(selectedCategory)
    )

    // Filter ranks based on selected group
    const filteredRanks = ranks.filter(rank =>
      rank.group_id === parseInt(selectedGroup)
    )

    const handleSubmit = async (e) => {
      e.preventDefault()
      
      // التحقق من صحة البيانات
      const validation = validateProduct(formData, products)
      if (!validation.isValid) {
        setErrors(validation.errors)
        return
      }

      setSubmitting(true)
      try {
        await onSave(formData)
      } catch (err) {
        // الأخطاء تتم معالجتها في الدالة الأصلية
      } finally {
        setSubmitting(false)
      }
    }

    const handleChange = (field, value) => {
      setFormData({ ...formData, [field]: value })
      // إزالة الخطأ عند تغيير القيمة
      if (errors[field]) {
        setErrors({ ...errors, [field]: null })
      }
    }

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
          <h3 className="text-lg font-semibold mb-4">
            {product ? 'تعديل المنتج' : 'إضافة منتج جديد'}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <ValidatedInput
              label="اسم المنتج"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              error={errors.name}
              required
            />
            
            <ValidatedInput
              label="الباركود"
              value={formData.barcode}
              onChange={(e) => handleChange('barcode', e.target.value)}
              error={errors.barcode}
            />

            {/* Category Selection */}
            <div className="grid grid-cols-3 gap-4">
              <ValidatedSelect
                label="الفئة"
                value={selectedCategory}
                onChange={(e) => {
                  setSelectedCategory(e.target.value)
                  setSelectedGroup('')
                  setFormData(prev => ({ ...prev, rank_id: '' }))
                }}
                options={categories.map(cat => ({ value: cat.id, label: cat.name }))}
                error={errors.category}
                required
              />

              <ValidatedSelect
                label="المجموعة"
                value={selectedGroup}
                onChange={(e) => {
                  setSelectedGroup(e.target.value)
                  setFormData(prev => ({ ...prev, rank_id: '' }))
                }}
                options={filteredGroups.map(group => ({ value: group.id, label: group.name }))}
                error={errors.group}
                required
                disabled={!selectedCategory}
              />

              <ValidatedSelect
                label="المرتبة"
                value={formData.rank_id}
                onChange={(e) => handleChange('rank_id', e.target.value)}
                options={filteredRanks.map(rank => ({ value: rank.id, label: rank.name }))}
                error={errors.rank_id}
                required
                disabled={!selectedGroup}
              />
            </div>

            <ValidatedInput
              label="الوحدة"
              value={formData.unit}
              onChange={(e) => handleChange('unit', e.target.value)}
              error={errors.unit}
              required
            />
            
            <div className="grid grid-cols-2 gap-4">
              <ValidatedInput
                label="سعر التكلفة"
                type="number"
                step="0.01"
                value={formData.cost_price}
                onChange={(e) => handleChange('cost_price', e.target.value)}
                error={errors.cost_price}
                required
              />
              
              <ValidatedInput
                label="سعر البيع"
                type="number"
                step="0.01"
                value={formData.selling_price}
                onChange={(e) => handleChange('selling_price', e.target.value)}
                error={errors.selling_price}
                required
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <ValidatedInput
                label="الكمية الحالية"
                type="number"
                value={formData.quantity}
                onChange={(e) => handleChange('quantity', e.target.value)}
                error={errors.quantity}
                required
              />
              
              <ValidatedInput
                label="الحد الأدنى"
                type="number"
                value={formData.min_quantity}
                onChange={(e) => handleChange('min_quantity', e.target.value)}
                error={errors.min_quantity}
                required
              />
            </div>
            
            <div className="flex justify-end space-x-2 space-x-reverse pt-4">
              <button
                type="button"
                onClick={onClose}
                disabled={submitting}
                className="px-4 py-2 text-muted-foreground border border-border rounded-md hover:bg-muted/50 disabled:opacity-50"
              >
                إلغاء
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 flex items-center"
              >
                {submitting && <LoadingSpinner size="sm" className="ml-2" />}
                {product ? 'تحديث' : 'إضافة'}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <LoadingSpinner size="lg" />
        <span className="mr-3">جاري تحميل المنتجات...</span>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">إدارة المنتجات</h1>
        <p className="text-muted-foreground mt-2">إدارة وتتبع جميع المنتجات في المخزون</p>
      </div>

      {/* عرض الأخطاء */}
      {error && (
        <Alert
          type="error"
          title="خطأ في تحميل البيانات"
          message={error}
          onClose={() => setError(null)}
          className="mb-6"
        />
      )}

      {/* تنبيه المنتجات منخفضة المخزون */}
      {lowStockProducts.length > 0 && (
        <Alert
          type="warning"
          title="تحذير: منتجات منخفضة المخزون"
          message={`المنتجات التالية تحتاج إلى إعادة تموين: ${lowStockProducts.map(p => p.name).join(', ')}`}
          className="mb-6"
        />
      )}

      {/* شريط البحث والإضافة */}
      <div className="flex justify-between items-center mb-6">
        <div className="relative">
          <Search className="w-5 h-5 absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="البحث في المنتجات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-4 pr-10 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 w-80"
          />
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
          >
            <Plus className="w-4 h-4 ml-2" />
            إضافة منتج جديد
          </button>
          <button
            onClick={() => setShowImportModal(true)}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center"
          >
            <FileSpreadsheet className="w-4 h-4 ml-2" />
            استيراد Excel
          </button>
        </div>
      </div>

      {/* جدول المنتجات أو حالة فارغة */}
      {filteredProducts.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md">
          <EmptyState
            icon="package"
            title={searchTerm ? 'لا توجد نتائج' : 'لا توجد منتجات'}
            description={
              searchTerm
                ? `لم يتم العثور على منتجات تطابق "${searchTerm}". جرب البحث بكلمات مختلفة أو أضف منتجاً جديداً.`
                : 'ابدأ بإضافة منتجك الأول لبناء مخزونك. يمكنك إضافة منتج واحد أو استيراد عدة منتجات من ملف Excel.'
            }
            actionText="إضافة منتج جديد"
            onAction={() => setShowAddModal(true)}
            secondaryActionText="استيراد من Excel"
            onSecondaryAction={() => setShowImportModal(true)}
          />
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المنتج</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الفئة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الكمية</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">سعر التكلفة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">سعر البيع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الحالة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredProducts.map((product) => (
              <tr key={product.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <Package className="w-8 h-8 text-gray-400 ml-3" />
                    <div>
                      <div className="text-sm font-medium text-foreground">{product.name}</div>
                      <div className="text-sm text-gray-500">{product.sku}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-primary-100 text-primary-800">
                    {product.category}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {product.quantity} {product.unit}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {product.cost_price} جنيه
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {product.selling_price} جنيه
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {product.quantity <= product.min_quantity ? (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-destructive/20 text-red-800">
                      مخزون منخفض
                    </span>
                  ) : (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-primary/20 text-green-800">
                      متوفر
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => setEditingProduct(product)}
                    className="text-primary-600 hover:text-primary-900 ml-4"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setDeleteConfirm(product)}
                    className="text-destructive hover:text-red-900"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* نافذة إضافة/تعديل المنتج */}
      {showAddModal && (
        <ProductModal
          onSave={handleAddProduct}
          onClose={() => setShowAddModal(false)}
        />
      )}

      {editingProduct && (
        <ProductModal
          product={editingProduct}
          onSave={handleEditProduct}
          onClose={() => setEditingProduct(null)}
        />
      )}

      {/* نافذة تأكيد الحذف */}
      <ConfirmDialog
        isOpen={!!deleteConfirm}
        title="تأكيد الحذف"
        message={`هل أنت متأكد من حذف المنتج "${deleteConfirm?.name}"؟ لا يمكن التراجع عن هذا الإجراء.`}
        confirmText="حذف"
        cancelText="إلغاء"
        type="danger"
        onConfirm={() => handleDeleteProduct(deleteConfirm.id)}
        onCancel={() => setDeleteConfirm(null)}
      />

      {/* مودال استيراد Excel */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">استيراد المنتجات من Excel</h3>
              <button
                onClick={() => setShowImportModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>

            <ExcelImport
              type="products"
              onImport={handleExcelImport}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default Products


