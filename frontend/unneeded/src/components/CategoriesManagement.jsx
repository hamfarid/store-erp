import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Tags, TreePine, Layers, RefreshCw
} from 'lucide-react'

const CategoriesManagement = () => {
  const [categories, setCategories] = useState([])
  const [filteredCategories, setFilteredCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingCategory, setEditingCategory] = useState(null)
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadCategories()
  }, [])

  useEffect(() => {
    filterCategories()
  }, [categories, searchTerm])

  const loadCategories = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/categories')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setCategories(data.data)
        } else {
          throw new Error('فشل في تحميل الفئات')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockCategories = [
        {
          id: 1,
          name: 'بذور',
          nameEn: 'Seeds',
          description: 'جميع أنواع البذور الزراعية',
          parentId: null,
          level: 0,
          productsCount: 25,
          status: 'نشط'
        },
        {
          id: 2,
          name: 'بذور خضروات',
          nameEn: 'Vegetable Seeds',
          description: 'بذور الخضروات المختلفة',
          parentId: 1,
          level: 1,
          productsCount: 15,
          status: 'نشط'
        },
        {
          id: 3,
          name: 'أسمدة',
          nameEn: 'Fertilizers',
          description: 'الأسمدة الزراعية',
          parentId: null,
          level: 0,
          productsCount: 12,
          status: 'نشط'
        },
        {
          id: 4,
          name: 'مبيدات',
          nameEn: 'Pesticides',
          description: 'المبيدات الحشرية والفطرية',
          parentId: null,
          level: 0,
          productsCount: 8,
          status: 'نشط'
        }
      ]
      setCategories(mockCategories)
    } finally {
      setLoading(false)
    }
  }

  const filterCategories = () => {
    if (searchTerm) {
      const filtered = categories.filter(category =>
        category.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        category.nameEn.toLowerCase().includes(searchTerm.toLowerCase()) ||
        category.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredCategories(filtered)
    } else {
      setFilteredCategories(categories)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddCategory = () => {
    setEditingCategory(null)
    setShowModal(true)
  }

  const handleEditCategory = (category) => {
    setEditingCategory(category)
    setShowModal(true)
  }

  const handleDeleteCategory = async (categoryId) => {
    if (window.confirm('هل أنت متأكد من حذف هذه الفئة؟')) {
      try {
        setCategories(prev => prev.filter(c => c.id !== categoryId))
        showNotification('تم حذف الفئة بنجاح')
      } catch (error) {
        showNotification('فشل في حذف الفئة', 'error')
      }
    }
  }

  const handleSaveCategory = async (categoryData) => {
    try {
      if (editingCategory) {
        setCategories(prev => prev.map(c => 
          c.id === editingCategory.id ? { ...c, ...categoryData } : c
        ))
        showNotification('تم تحديث الفئة بنجاح')
      } else {
        const newCategory = {
          id: Date.now(),
          ...categoryData,
          productsCount: 0,
          status: 'نشط'
        }
        setCategories(prev => [...prev, newCategory])
        showNotification('تم إضافة الفئة بنجاح')
      }
      setShowModal(false)
    } catch (error) {
      showNotification('فشل في حفظ الفئة', 'error')
    }
  }

  const getCategoryIcon = (level) => {
    switch (level) {
      case 0: return <TreePine className="h-5 w-5 text-primary" />
      case 1: return <Layers className="h-5 w-5 text-primary-600" />
      default: return <Tags className="h-5 w-5 text-purple-600" />
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
          <h1 className="text-2xl font-bold text-foreground">إدارة الفئات والتصنيفات</h1>
          <p className="text-muted-foreground">تنظيم وإدارة فئات المنتجات</p>
        </div>
        <button
          onClick={handleAddCategory}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة فئة جديدة
        </button>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في الفئات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadCategories}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Tags className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الفئات</p>
              <p className="text-2xl font-bold text-foreground">{categories.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TreePine className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الفئات الرئيسية</p>
              <p className="text-2xl font-bold text-foreground">
                {categories.filter(c => c.level === 0).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Layers className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الفئات الفرعية</p>
              <p className="text-2xl font-bold text-foreground">
                {categories.filter(c => c.level > 0).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المنتجات</p>
              <p className="text-2xl font-bold text-foreground">
                {categories.reduce((sum, c) => sum + (c.productsCount || 0), 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Categories Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الفئة
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الاسم بالإنجليزية
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الوصف
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                عدد المنتجات
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
            {filteredCategories.map((category) => (
              <tr key={category.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {getCategoryIcon(category.level)}
                    <div className="mr-3">
                      <div className="text-sm font-medium text-foreground">
                        {'  '.repeat(category.level)}{category.name}
                      </div>
                      <div className="text-sm text-gray-500">
                        المستوى {category.level + 1}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {category.nameEn}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {category.description}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {category.productsCount} منتج
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    category.status === 'نشط' 
                      ? 'bg-primary/20 text-green-800' 
                      : 'bg-destructive/20 text-red-800'
                  }`}>
                    {category.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEditCategory(category)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteCategory(category.id)}
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

      {/* Add/Edit Modal - Simplified */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium mb-4">
              {editingCategory ? 'تعديل الفئة' : 'إضافة فئة جديدة'}
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم الفئة"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingCategory?.name || ''}
              />
              <input
                type="text"
                placeholder="الاسم بالإنجليزية"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingCategory?.nameEn || ''}
              />
              <textarea
                placeholder="الوصف"
                className="w-full p-2 border border-border rounded-lg"
                rows="3"
                defaultValue={editingCategory?.description || ''}
              />
              <select className="w-full p-2 border border-border rounded-lg">
                <option value="">اختر الفئة الأب</option>
                {categories.filter(c => c.level === 0).map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                onClick={() => handleSaveCategory({
                  name: 'فئة جديدة',
                  nameEn: 'New Category',
                  description: 'وصف الفئة الجديدة',
                  level: 0
                })}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                حفظ
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CategoriesManagement

