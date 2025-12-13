import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const WarehousesManagement = () => {
  const [warehouses, setWarehouses] = useState([])
  const [filteredWarehouses, setFilteredWarehouses] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingWarehouse, setEditingWarehouse] = useState(null)
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadWarehouses()
  }, [])

  useEffect(() => {
    filterWarehouses()
  }, [warehouses, searchTerm])

  const loadWarehouses = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://172.16.16.27:8000/api/warehouses')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setWarehouses(data.data)
        } else {
          throw new Error('فشل في تحميل المخازن')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockWarehouses = [
        {
          id: 1,
          name: 'المخزن الرئيسي',
          nameEn: 'Main Warehouse',
          location: 'القاهرة، مصر',
          address: 'شارع الهرم، الجيزة',
          manager: 'أحمد محمد',
          phone: '+20-1001234567',
          capacity: 1000,
          currentStock: 750,
          status: 'نشط',
          productsCount: 45
        },
        {
          id: 2,
          name: 'مخزن الأسمدة',
          nameEn: 'Fertilizers Warehouse',
          location: 'الإسكندرية، مصر',
          address: 'طريق الإسكندرية الصحراوي',
          manager: 'محمد أحمد',
          phone: '+20-1009876543',
          capacity: 500,
          currentStock: 300,
          status: 'نشط',
          productsCount: 20
        },
        {
          id: 3,
          name: 'مخزن البذور',
          nameEn: 'Seeds Warehouse',
          location: 'المنيا، مصر',
          address: 'طريق القاهرة أسيوط الزراعي',
          manager: 'سارة علي',
          phone: '+20-1005555555',
          capacity: 300,
          currentStock: 280,
          status: 'نشط',
          productsCount: 30
        }
      ]
      setWarehouses(mockWarehouses)
    } finally {
      setLoading(false)
    }
  }

  const filterWarehouses = () => {
    if (searchTerm) {
      const filtered = warehouses.filter(warehouse =>
        warehouse.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        warehouse.nameEn.toLowerCase().includes(searchTerm.toLowerCase()) ||
        warehouse.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
        warehouse.manager.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredWarehouses(filtered)
    } else {
      setFilteredWarehouses(warehouses)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddWarehouse = () => {
    setEditingWarehouse(null)
    setShowModal(true)
  }

  const handleEditWarehouse = (warehouse) => {
    setEditingWarehouse(warehouse)
    setShowModal(true)
  }

  const handleDeleteWarehouse = async (warehouseId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المخزن؟')) {
      try {
        setWarehouses(prev => prev.filter(w => w.id !== warehouseId))
        showNotification('تم حذف المخزن بنجاح')
      } catch (error) {
        showNotification('فشل في حذف المخزن', 'error')
      }
    }
  }

  const handleSaveWarehouse = async (warehouseData) => {
    try {
      if (editingWarehouse) {
        setWarehouses(prev => prev.map(w => 
          w.id === editingWarehouse.id ? { ...w, ...warehouseData } : w
        ))
        showNotification('تم تحديث المخزن بنجاح')
      } else {
        const newWarehouse = {
          id: Date.now(),
          ...warehouseData,
          currentStock: 0,
          productsCount: 0,
          status: 'نشط'
        }
        setWarehouses(prev => [...prev, newWarehouse])
        showNotification('تم إضافة المخزن بنجاح')
      }
      setShowModal(false)
    } catch (error) {
      showNotification('فشل في حفظ المخزن', 'error')
    }
  }

  const getCapacityPercentage = (current, capacity) => {
    return Math.round((current / capacity) * 100)
  }

  const getCapacityColor = (percentage) => {
    if (percentage >= 90) return 'text-destructive bg-destructive/20'
    if (percentage >= 70) return 'text-accent bg-accent/20'
    return 'text-primary bg-primary/20'
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
          <h1 className="text-2xl font-bold text-foreground">إدارة المخازن</h1>
          <p className="text-muted-foreground">إدارة وتتبع المخازن والمواقع</p>
        </div>
        <button
          onClick={handleAddWarehouse}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة مخزن جديد
        </button>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في المخازن..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadWarehouses}
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
            <Warehouse className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي المخازن</p>
              <p className="text-2xl font-bold text-foreground">{warehouses.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي السعة</p>
              <p className="text-2xl font-bold text-foreground">
                {warehouses.reduce((sum, w) => sum + (w.capacity || 0), 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المخزون الحالي</p>
              <p className="text-2xl font-bold text-foreground">
                {warehouses.reduce((sum, w) => sum + (w.currentStock || 0), 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">المخازن النشطة</p>
              <p className="text-2xl font-bold text-foreground">
                {warehouses.filter(w => w.status === 'نشط').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Warehouses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredWarehouses.map((warehouse) => {
          const capacityPercentage = getCapacityPercentage(warehouse.currentStock, warehouse.capacity)
          return (
            <div key={warehouse.id} className="bg-white rounded-lg shadow border hover:shadow-md transition-shadow">
              <div className="p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <Warehouse className="h-8 w-8 text-primary-600 ml-3" />
                    <div>
                      <h3 className="text-lg font-semibold text-foreground">{warehouse.name}</h3>
                      <p className="text-sm text-gray-500">{warehouse.nameEn}</p>
                    </div>
                  </div>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    warehouse.status === 'نشط' 
                      ? 'bg-primary/20 text-green-800' 
                      : 'bg-destructive/20 text-red-800'
                  }`}>
                    {warehouse.status}
                  </span>
                </div>

                {/* Location */}
                <div className="flex items-center mb-3">
                  <MapPin className="h-4 w-4 text-gray-400 ml-2" />
                  <span className="text-sm text-muted-foreground">{warehouse.location}</span>
                </div>

                {/* Manager */}
                <div className="flex items-center mb-3">
                  <Users className="h-4 w-4 text-gray-400 ml-2" />
                  <span className="text-sm text-muted-foreground">المدير: {warehouse.manager}</span>
                </div>

                {/* Capacity */}
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-foreground">السعة</span>
                    <span className="text-sm text-muted-foreground">
                      {warehouse.currentStock} / {warehouse.capacity}
                    </span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        capacityPercentage >= 90 ? 'bg-destructive/100' :
                        capacityPercentage >= 70 ? 'bg-accent/100' : 'bg-primary/100'
                      }`}
                      style={{ width: `${capacityPercentage}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className={`text-xs px-2 py-1 rounded-full ${getCapacityColor(capacityPercentage)}`}>
                      {capacityPercentage}% ممتلئ
                    </span>
                    <span className="text-xs text-gray-500">
                      {warehouse.productsCount} منتج
                    </span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex justify-end space-x-2">
                  <button
                    onClick={() => handleEditWarehouse(warehouse)}
                    className="text-primary-600 hover:text-primary-900 p-1"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteWarehouse(warehouse.id)}
                    className="text-destructive hover:text-red-900 p-1"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          )
        })}
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
              {editingWarehouse ? 'تعديل المخزن' : 'إضافة مخزن جديد'}
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم المخزن"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.name || ''}
              />
              <input
                type="text"
                placeholder="الاسم بالإنجليزية"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.nameEn || ''}
              />
              <input
                type="text"
                placeholder="الموقع"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.location || ''}
              />
              <input
                type="text"
                placeholder="العنوان التفصيلي"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.address || ''}
              />
              <input
                type="text"
                placeholder="اسم المدير"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.manager || ''}
              />
              <input
                type="tel"
                placeholder="رقم الهاتف"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.phone || ''}
              />
              <input
                type="number"
                placeholder="السعة القصوى"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingWarehouse?.capacity || ''}
              />
            </div>
            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                onClick={() => handleSaveWarehouse({
                  name: 'مخزن جديد',
                  nameEn: 'New Warehouse',
                  location: 'موقع جديد',
                  address: 'عنوان جديد',
                  manager: 'مدير جديد',
                  phone: '+20-1000000000',
                  capacity: 100
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

export default WarehousesManagement

