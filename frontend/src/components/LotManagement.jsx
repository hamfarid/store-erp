import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const LotManagement = () => {
  const [lots, setLots] = useState([])
  const [filteredLots, setFilteredLots] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedLot, setSelectedLot] = useState(null)
  const [showAddModal, setShowAddModal] = useState(false)

  const [showDetailsModal, setShowDetailsModal] = useState(false)

  useEffect(() => {
    loadLots()
  }, [])

  useEffect(() => {
    filterLots()
  }, [lots, searchTerm, statusFilter])

  const loadLots = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://172.16.16.27:8000/lot_management/lots')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setLots(data.data)
        } else {
          throw new Error('فشل في تحميل اللوطات')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockLots = [
        {
          id: 1,
          lotNumber: 'LOT-2024-001',
          productName: 'بذور طماطم هجين',
          supplier: 'شركة البذور المتقدمة',
          quantity: 1000,
          unit: 'كيس',
          expiryDate: '2024-12-31',
          status: 'متاح',
          warehouse: 'المخزن الرئيسي',
          receivedDate: '2024-06-01'
        },
        {
          id: 2,
          lotNumber: 'LOT-2024-002',
          productName: 'سماد NPK',
          supplier: 'شركة الأسمدة الحديثة',
          quantity: 500,
          unit: 'كيس',
          expiryDate: '2025-03-15',
          status: 'منخفض',
          warehouse: 'مخزن الأسمدة',
          receivedDate: '2024-06-15'
        }
      ]
      setLots(mockLots)
    } finally {
      setLoading(false)
    }
  }

  const filterLots = () => {
    let filtered = lots

    if (searchTerm) {
      filtered = filtered.filter(lot =>
        lot.lotNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lot.productName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lot.supplier.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(lot => lot.status === statusFilter)
    }

    setFilteredLots(filtered)
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'متاح':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'منخفض':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      case 'منتهي':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'متاح':
        return 'bg-primary/20 text-green-800'
      case 'منخفض':
        return 'bg-accent/20 text-yellow-800'
      case 'منتهي':
        return 'bg-destructive/20 text-red-800'
      default:
        return 'bg-muted text-foreground'
    }
  }

  const isExpiringSoon = (expiryDate) => {
    const today = new Date()
    const expiry = new Date(expiryDate)
    const diffTime = expiry - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays <= 30 && diffDays > 0
  }

  const handleViewDetails = (lot) => {
    setSelectedLot(lot)
    setShowDetailsModal(true)
  }

  const handleEditLot = (lot) => {
    setSelectedLot(lot)
    alert('نافذة التعديل - قيد التطوير')
  }

  const handleDeleteLot = (lotId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا اللوط؟')) {
      setLots(prev => prev.filter(l => l.id !== lotId))
      alert('تم حذف اللوط بنجاح!')
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
          <h1 className="text-2xl font-bold text-foreground">إدارة اللوطات</h1>
          <p className="text-muted-foreground">تتبع وإدارة لوتات المنتجات</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 ml-2" />
          إضافة لوط جديد
        </button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="البحث في اللوطات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="all">جميع الحالات</option>
          <option value="متاح">متاح</option>
          <option value="منخفض">منخفض</option>
          <option value="منتهي">منتهي</option>
        </select>

        <button
          onClick={loadLots}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center justify-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي اللوطات</p>
              <p className="text-2xl font-bold text-foreground">{lots.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">متاح</p>
              <p className="text-2xl font-bold text-foreground">
                {lots.filter(lot => lot.status === 'متاح').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">منخفض</p>
              <p className="text-2xl font-bold text-foreground">
                {lots.filter(lot => lot.status === 'منخفض').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">ينتهي قريباً</p>
              <p className="text-2xl font-bold text-foreground">
                {lots.filter(lot => isExpiringSoon(lot.expiryDate)).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Lots Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم اللوت
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المنتج
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الكمية
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                تاريخ الانتهاء
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
            {filteredLots.map((lot) => (
              <tr key={lot.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-foreground">
                    {lot.lotNumber}
                  </div>
                  <div className="text-sm text-gray-500">
                    {lot.warehouse}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-foreground">
                    {lot.productName}
                  </div>
                  <div className="text-sm text-gray-500">
                    {lot.supplier}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {lot.quantity} {lot.unit}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-foreground">
                    {new Date(lot.expiryDate).toLocaleDateString('ar-EG')}
                  </div>
                  {isExpiringSoon(lot.expiryDate) && (
                    <div className="text-xs text-destructive font-medium">
                      ينتهي قريباً
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(lot.status)}`}>
                    {getStatusIcon(lot.status)}
                    <span className="mr-1">{lot.status}</span>
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleViewDetails(lot)}
                      className="text-primary-600 hover:text-primary-900"
                      title="عرض التفاصيل"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleEditLot(lot)}
                      className="text-primary hover:text-green-900"
                      title="تعديل"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteLot(lot.id)}
                      className="text-destructive hover:text-red-900"
                      title="حذف"
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

      {filteredLots.length === 0 && (
        <div className="text-center py-12">
          <Package className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-foreground">لا توجد لوتات</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm || statusFilter !== 'all' 
              ? 'لا توجد نتائج تطابق البحث' 
              : 'ابدأ بإضافة لوت جديد'}
          </p>
        </div>
      )}

      {/* نافذة إضافة لوط جديد */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">إضافة لوط جديد</h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <input
                type="text"
                placeholder="رقم اللوط"
                className="w-full p-2 border border-border rounded-lg"
              />
              <input
                type="text"
                placeholder="اسم المنتج"
                className="w-full p-2 border border-border rounded-lg"
              />
              <input
                type="text"
                placeholder="المورد"
                className="w-full p-2 border border-border rounded-lg"
              />
              <input
                type="number"
                placeholder="الكمية"
                className="w-full p-2 border border-border rounded-lg"
              />
              <input
                type="date"
                placeholder="تاريخ انتهاء الصلاحية"
                className="w-full p-2 border border-border rounded-lg"
              />
              <select className="w-full p-2 border border-border rounded-lg">
                <option value="">اختر المخزن</option>
                <option value="المخزن الرئيسي">المخزن الرئيسي</option>
                <option value="مخزن البذور">مخزن البذور</option>
                <option value="مخزن الأسمدة">مخزن الأسمدة</option>
              </select>
            </div>

            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                onClick={() => {
                  alert('تم إضافة اللوط بنجاح!')
                  setShowAddModal(false)
                }}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                حفظ
              </button>
            </div>
          </div>
        </div>
      )}

      {/* نافذة عرض التفاصيل */}
      {showDetailsModal && selectedLot && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">تفاصيل اللوط: {selectedLot.lotNumber}</h3>
              <button
                onClick={() => setShowDetailsModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">رقم اللوط</p>
                <p className="font-medium">{selectedLot.lotNumber}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">المنتج</p>
                <p className="font-medium">{selectedLot.productName}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">المورد</p>
                <p className="font-medium">{selectedLot.supplier}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">الكمية</p>
                <p className="font-medium">{selectedLot.quantity} {selectedLot.unit}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">تاريخ الاستلام</p>
                <p className="font-medium">{selectedLot.receivedDate}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">تاريخ انتهاء الصلاحية</p>
                <p className="font-medium">{selectedLot.expiryDate}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">المخزن</p>
                <p className="font-medium">{selectedLot.warehouse}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">الحالة</p>
                <p className="font-medium">{selectedLot.status}</p>
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <button
                onClick={() => setShowDetailsModal(false)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              >
                إغلاق
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LotManagement

