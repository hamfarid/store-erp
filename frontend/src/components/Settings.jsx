import React, { useState, useEffect } from 'react'
import {
  Edit, Plus, Save, Settings as SettingsIcon,
  Trash2, X
} from 'lucide-react'

import toast from 'react-hot-toast'
import ApiService from '../services/ApiService'
import { isSuccess } from '../utils/responseHelper'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('categories')
  const [categories, setCategories] = useState([])
  const [productGroups, setProductGroups] = useState([])
  const [ranks, setRanks] = useState([])
  const [loading, setLoading] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({ name: '', description: '' })

  useEffect(() => {
    loadData()
  }, [activeTab])

  const loadData = async () => {
    setLoading(true)
    try {
      switch (activeTab) {
        case 'categories': {
          const categoriesResponse = await ApiService.getCategories()
          if (isSuccess(categoriesResponse)) {
            setCategories(categoriesResponse.data)
          }
          break
        }
        case 'groups': {
          const groupsResponse = await ApiService.getProductGroups()
          if (isSuccess(groupsResponse)) {
            setProductGroups(groupsResponse.data)
          }
          break
        }
        case 'ranks': {
          const ranksResponse = await ApiService.getRanks()
          if (isSuccess(ranksResponse)) {
            setRanks(ranksResponse.data)
          }
          break
        }
      }
    } catch (error) {
      toast.error('فشل في تحميل البيانات')
      } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.name.trim()) {
      toast.error('الاسم مطلوب')
      return
    }

    try {
      let response
      if (editingItem) {
        // تحديث
        switch (activeTab) {
          case 'categories':
            response = await ApiService.updateCategory(editingItem.id, formData)
            break
          case 'groups':
            response = await ApiService.updateProductGroup(editingItem.id, formData)
            break
          case 'ranks':
            response = await ApiService.updateRank(editingItem.id, formData)
            break
        }
      } else {
        // إضافة جديد
        switch (activeTab) {
          case 'categories':
            response = await ApiService.createCategory(formData)
            break
          case 'groups':
            response = await ApiService.createProductGroup(formData)
            break
          case 'ranks':
            response = await ApiService.createRank(formData)
            break
        }
      }

      if (isSuccess(response)) {
        toast.success(editingItem ? 'تم التحديث بنجاح' : 'تم الإضافة بنجاح')
        setShowAddModal(false)
        setEditingItem(null)
        setFormData({ name: '', description: '' })
        loadData()
      } else {
        toast.error(response.message || 'حدث خطأ')
      }
    } catch (error) {
      toast.error('حدث خطأ في العملية')
      }
  }

  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({ name: item.name, description: item.description || '' })
    setShowAddModal(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('هل أنت متأكد من الحذف؟')) return

    try {
      let response
      switch (activeTab) {
        case 'categories':
          response = await ApiService.deleteCategory(id)
          break
        case 'groups':
          response = await ApiService.deleteProductGroup(id)
          break
        case 'ranks':
          response = await ApiService.deleteRank(id)
          break
      }

      if (response.success) {
        toast.success('تم الحذف بنجاح')
        loadData()
      } else {
        toast.error(response.message || 'فشل في الحذف')
      }
    } catch (error) {
      toast.error('حدث خطأ في الحذف')
      }
  }

  const getCurrentData = () => {
    switch (activeTab) {
      case 'categories':
        return categories
      case 'groups':
        return productGroups
      case 'ranks':
        return ranks
      default:
        return []
    }
  }

  const getTabTitle = () => {
    switch (activeTab) {
      case 'categories':
        return 'التصنيفات'
      case 'groups':
        return 'مجموعات المنتجات'
      case 'ranks':
        return 'المراتب'
      default:
        return ''
    }
  }

  return (
    <div className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <SettingsIcon className="w-8 h-8 text-primary-600" />
        <h1 className="text-2xl font-bold text-foreground">إعدادات النظام</h1>
      </div>

      {/* التبويبات */}
      <div className="flex space-x-1 mb-6 bg-muted p-1 rounded-lg">
        <button
          onClick={() => setActiveTab('categories')}
          className={`px-4 py-2 rounded-md transition-colors ${
            activeTab === 'categories'
              ? 'bg-white text-primary-600 shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          التصنيفات
        </button>
        <button
          onClick={() => setActiveTab('groups')}
          className={`px-4 py-2 rounded-md transition-colors ${
            activeTab === 'groups'
              ? 'bg-white text-primary-600 shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          مجموعات المنتجات
        </button>
        <button
          onClick={() => setActiveTab('ranks')}
          className={`px-4 py-2 rounded-md transition-colors ${
            activeTab === 'ranks'
              ? 'bg-white text-primary-600 shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          المراتب
        </button>
      </div>

      {/* محتوى التبويب */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-lg font-semibold">{getTabTitle()}</h2>
          <button
            onClick={() => {
              setEditingItem(null)
              setFormData({ name: '', description: '' })
              setShowAddModal(true)
            }}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            إضافة جديد
          </button>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-2 text-muted-foreground">جاري التحميل...</p>
          </div>
        ) : (
          <div className="p-4">
            {getCurrentData().length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                لا توجد بيانات
              </div>
            ) : (
              <div className="grid gap-4">
                {getCurrentData().map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
                  >
                    <div>
                      <h3 className="font-medium text-foreground">{item.name}</h3>
                      {item.description && (
                        <p className="text-sm text-muted-foreground mt-1">{item.description}</p>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleEdit(item)}
                        className="p-2 text-primary-600 hover:bg-primary-50 rounded"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-2 text-destructive hover:bg-destructive/10 rounded"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* نافذة الإضافة/التعديل */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">
                {editingItem ? 'تعديل' : 'إضافة'} {getTabTitle().slice(0, -1)}
              </h3>
              <button
                onClick={() => {
                  setShowAddModal(false)
                  setEditingItem(null)
                  setFormData({ name: '', description: '' })
                }}
                className="text-gray-400 hover:text-muted-foreground"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  الاسم *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  الوصف
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  rows="3"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 flex items-center justify-center gap-2"
                >
                  <Save className="w-4 h-4" />
                  {editingItem ? 'تحديث' : 'حفظ'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddModal(false)
                    setEditingItem(null)
                    setFormData({ name: '', description: '' })
                  }}
                  className="flex-1 bg-gray-300 text-foreground py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  إلغاء
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Settings

