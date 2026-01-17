import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const ProductsAdvanced = () => {
  const [products, setProducts] = useState([])
  const [filteredProducts, setFilteredProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showImportModal, setShowImportModal] = useState(false)
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedType, setSelectedType] = useState('')

  // بيانات تجريبية متقدمة
  const mockProducts = [
    {
      id: 1,
      name: 'بذور طماطم هجين',
      name_en: 'Hybrid Tomato Seeds',
      sku: 'TOM-HYB-001',
      barcode: '1234567890123',
      category: 'بذور',
      product_type: 'storable',
      tracking_type: 'lot',
      cost_price: 25.50,
      sale_price: 35.00,
      wholesale_price: 30.00,
      min_quantity: 10,
      max_quantity: 1000,
      reorder_point: 20,
      quality_grade: 'premium',
      shelf_life_days: 730,
      plant_family: 'Solanaceae',
      variety: 'Cherry',
      origin_country: 'Netherlands',
      germination_rate: 95.5,
      purity_rate: 98.0,
      moisture_content: 8.5,
      storage_temperature_min: 5,
      storage_temperature_max: 25,
      storage_humidity_max: 60,
      is_active: true,
      current_stock: 150.0,
      profit_margin: 37.3
    },
    {
      id: 2,
      name: 'سماد NPK متوازن',
      name_en: 'Balanced NPK Fertilizer',
      sku: 'NPK-BAL-001',
      barcode: '1234567890124',
      category: 'أسمدة',
      product_type: 'storable',
      tracking_type: 'batch',
      cost_price: 45.00,
      sale_price: 60.00,
      wholesale_price: 55.00,
      min_quantity: 5,
      max_quantity: 500,
      reorder_point: 15,
      quality_grade: 'standard',
      shelf_life_days: 1095,
      active_ingredient: 'NPK',
      concentration: '20-20-20',
      npk_ratio: '20:20:20',
      ph_level: 6.5,
      storage_temperature_min: 10,
      storage_temperature_max: 35,
      storage_humidity_max: 70,
      is_active: true,
      current_stock: 75.0,
      profit_margin: 33.3
    }
  ]

  useEffect(() => {
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setProducts(mockProducts)
      setFilteredProducts(mockProducts)
      setLoading(false)
    }, 1000)
  }, [])

  // فلترة المنتجات
  useEffect(() => {
    let filtered = products

    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.barcode.includes(searchTerm)
      )
    }

    if (selectedCategory) {
      filtered = filtered.filter(product => product.category === selectedCategory)
    }

    if (selectedType) {
      filtered = filtered.filter(product => product.product_type === selectedType)
    }

    setFilteredProducts(filtered)
  }, [searchTerm, selectedCategory, selectedType, products])

  const getQualityBadgeColor = (grade) => {
    switch (grade) {
      case 'premium': return 'bg-purple-100 text-purple-800'
      case 'standard': return 'bg-primary-100 text-primary-800'
      case 'economy': return 'bg-primary/20 text-green-800'
      default: return 'bg-muted text-foreground'
    }
  }

  const getStockStatusColor = (current, min, reorder) => {
    if (current <= min) return 'text-destructive'
    if (current <= reorder) return 'text-accent'
    return 'text-primary'
  }

  const handleViewDetails = (product) => {
    setSelectedProduct(product)
    setShowDetailsModal(true)
  }

  const handleExportProducts = () => {
    // تصدير المنتجات إلى Excel
    const csvContent = "data:text/csv;charset=utf-8,"
      + "الاسم,SKU,الفئة,السعر,المخزون\n"
      + filteredProducts.map(product =>
          `${product.name},${product.sku},${product.category},${product.sale_price},${product.current_stock || 0}`
        ).join("\n")

    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", `products_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // إشعار نجاح
    alert('تم تصدير المنتجات بنجاح!')
  }

  const handleEditProduct = (product) => {
    setSelectedProduct(product)
    setShowEditModal(true)
  }

  const handleDeleteProduct = (productId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المنتج؟')) {
      setProducts(prev => prev.filter(p => p.id !== productId))
      alert('تم حذف المنتج بنجاح!')
    }
  }

  const handleAdvancedFilters = () => {
    alert('فلاتر متقدمة - قيد التطوير')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="mr-3 text-muted-foreground">جاري تحميل المنتجات...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة المنتجات المتقدمة</h1>
          <p className="text-muted-foreground">إدارة شاملة للمنتجات مع تتبع اللوط والجودة</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
          >
            <Plus className="w-4 h-4 ml-2" />
            منتج جديد
          </button>
          <button
            onClick={() => setShowImportModal(true)}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center"
          >
            <FileSpreadsheet className="w-4 h-4 ml-2" />
            استيراد Excel
          </button>
          <button
            onClick={handleExportProducts}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center"
          >
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </button>
        </div>
      </div>

      {/* أدوات البحث والفلترة */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute right-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="البحث في المنتجات..."
              className="w-full pr-10 pl-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="">جميع الفئات</option>
            <option value="بذور">بذور</option>
            <option value="أسمدة">أسمدة</option>
            <option value="مبيدات">مبيدات</option>
          </select>

          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            <option value="">جميع الأنواع</option>
            <option value="storable">قابل للتخزين</option>
            <option value="consumable">استهلاكي</option>
            <option value="service">خدمة</option>
          </select>

          <button
            onClick={handleAdvancedFilters}
            className="bg-muted text-foreground px-4 py-2 rounded-md hover:bg-muted flex items-center justify-center"
          >
            <Filter className="w-4 h-4 ml-2" />
            فلاتر متقدمة
          </button>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">إجمالي المنتجات</p>
              <p className="text-2xl font-bold text-foreground">{products.length}</p>
            </div>
            <Package className="w-8 h-8 text-primary-600" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">منتجات نشطة</p>
              <p className="text-2xl font-bold text-primary">
                {products.filter(p => p.is_active).length}
              </p>
            </div>
            <Star className="w-8 h-8 text-primary" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">منخفضة المخزون</p>
              <p className="text-2xl font-bold text-accent">
                {products.filter(p => p.current_stock <= p.reorder_point).length}
              </p>
            </div>
            <AlertTriangle className="w-8 h-8 text-accent" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">قيمة المخزون</p>
              <p className="text-2xl font-bold text-purple-600">
                {products.reduce((sum, p) => sum + (p.current_stock * p.cost_price), 0).toLocaleString()} ج.م
              </p>
            </div>
            <Download className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* جدول المنتجات */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المنتج</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الفئة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الجودة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المخزون</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الأسعار</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التخزين</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredProducts.map((product) => (
                <tr key={product.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-foreground">{product.name}</div>
                      <div className="text-sm text-gray-500">{product.sku}</div>
                      <div className="text-xs text-gray-400">{product.barcode}</div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {product.category}
                    </span>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="space-y-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getQualityBadgeColor(product.quality_grade)}`}>
                        {product.quality_grade}
                      </span>
                      {product.germination_rate && (
                        <div className="text-xs text-gray-500">إنبات: {product.germination_rate}%</div>
                      )}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="space-y-1">
                      <div className={`text-sm font-medium ${getStockStatusColor(product.current_stock, product.min_quantity, product.reorder_point)}`}>
                        {product.current_stock}
                      </div>
                      <div className="text-xs text-gray-500">
                        حد أدنى: {product.min_quantity}
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="space-y-1">
                      <div className="text-sm text-foreground">بيع: {product.sale_price} ج.م</div>
                      <div className="text-xs text-gray-500">تكلفة: {product.cost_price} ج.م</div>
                      <div className="text-xs text-primary">ربح: {product.profit_margin?.toFixed(1)}%</div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2 space-x-reverse">
                      {product.storage_temperature_min && (
                        <div className="flex items-center text-xs text-gray-500">
                          <Thermometer className="w-3 h-3 ml-1" />
                          {product.storage_temperature_min}-{product.storage_temperature_max}°C
                        </div>
                      )}
                      {product.storage_humidity_max && (
                        <div className="flex items-center text-xs text-gray-500">
                          <Droplets className="w-3 h-3 ml-1" />
                          {product.storage_humidity_max}%
                        </div>
                      )}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleViewDetails(product)}
                        className="text-primary-600 hover:text-primary-900"
                        title="عرض التفاصيل"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleEditProduct(product)}
                        className="text-primary hover:text-green-900"
                        title="تعديل"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(product.id)}
                        className="text-destructive hover:text-red-900"
                        title="حذف"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* مودال تفاصيل المنتج */}
      {showDetailsModal && selectedProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-semibold">تفاصيل المنتج: {selectedProduct.name}</h3>
              <button
                onClick={() => setShowDetailsModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* المعلومات الأساسية */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground border-b pb-2">المعلومات الأساسية</h4>
                <div className="space-y-2">
                  <div><span className="font-medium">الاسم:</span> {selectedProduct.name}</div>
                  <div><span className="font-medium">الاسم الإنجليزي:</span> {selectedProduct.name_en}</div>
                  <div><span className="font-medium">رمز المنتج:</span> {selectedProduct.sku}</div>
                  <div><span className="font-medium">الباركود:</span> {selectedProduct.barcode}</div>
                  <div><span className="font-medium">الفئة:</span> {selectedProduct.category}</div>
                </div>
              </div>

              {/* معلومات الجودة */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground border-b pb-2">معلومات الجودة</h4>
                <div className="space-y-2">
                  <div><span className="font-medium">درجة الجودة:</span> {selectedProduct.quality_grade}</div>
                  {selectedProduct.germination_rate && (
                    <div><span className="font-medium">معدل الإنبات:</span> {selectedProduct.germination_rate}%</div>
                  )}
                  {selectedProduct.purity_rate && (
                    <div><span className="font-medium">معدل النقاء:</span> {selectedProduct.purity_rate}%</div>
                  )}
                  {selectedProduct.moisture_content && (
                    <div><span className="font-medium">محتوى الرطوبة:</span> {selectedProduct.moisture_content}%</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* نافذة استيراد Excel */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">استيراد المنتجات من Excel</h3>
              <button
                onClick={() => setShowImportModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  اختر ملف Excel
                </label>
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  className="w-full p-2 border border-border rounded-lg"
                />
              </div>

              <div className="bg-primary-50 p-3 rounded-lg">
                <p className="text-sm text-primary-800">
                  💡 تأكد من أن الملف يحتوي على الأعمدة التالية:
                  <br />
                  الاسم، SKU، الفئة، السعر، المخزون
                </p>
              </div>

              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setShowImportModal(false)}
                  className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
                >
                  إلغاء
                </button>
                <button
                  onClick={() => {
                    alert('تم استيراد المنتجات بنجاح!')
                    setShowImportModal(false)
                  }}
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700"
                >
                  استيراد
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductsAdvanced

