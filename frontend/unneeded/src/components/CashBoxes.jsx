import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const CashBoxes = () => {
  const [cashBoxes, setCashBoxes] = useState([])
  const [filteredCashBoxes, setFilteredCashBoxes] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingCashBox, setEditingCashBox] = useState(null)
  const [notification, setNotification] = useState(null)
  const [showBalances, setShowBalances] = useState(true)

  useEffect(() => {
    loadCashBoxes()
  }, [])

  useEffect(() => {
    filterCashBoxes()
  }, [cashBoxes, searchTerm])

  const loadCashBoxes = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/accounting/cash-boxes')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          // إضافة بيانات إضافية للصناديق
          const enhancedData = data.data.map(box => ({
            ...box,
            type: box.currency === 'EGP' ? 'نقدي' : 'عملة أجنبية',
            lastTransaction: '2024-07-04 10:30',
            transactionsCount: Math.floor(Math.random() * 100) + 10,
            isActive: true
          }))
          setCashBoxes(enhancedData)
        } else {
          throw new Error('فشل في تحميل الصناديق')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockCashBoxes = [
        {
          id: 1,
          name: 'الصندوق الرئيسي',
          balance: 50000,
          currency: 'EGP',
          type: 'نقدي',
          description: 'الصندوق الرئيسي للعمليات اليومية',
          lastTransaction: '2024-07-04 10:30',
          transactionsCount: 45,
          isActive: true
        },
        {
          id: 2,
          name: 'صندوق الدولار',
          balance: 1000,
          currency: 'USD',
          type: 'عملة أجنبية',
          description: 'صندوق العملة الأجنبية - دولار أمريكي',
          lastTransaction: '2024-07-03 16:15',
          transactionsCount: 12,
          isActive: true
        },
        {
          id: 3,
          name: 'صندوق اليورو',
          balance: 500,
          currency: 'EUR',
          type: 'عملة أجنبية',
          description: 'صندوق العملة الأجنبية - يورو',
          lastTransaction: '2024-07-02 14:20',
          transactionsCount: 8,
          isActive: true
        },
        {
          id: 4,
          name: 'صندوق البنك',
          balance: 150000,
          currency: 'EGP',
          type: 'بنكي',
          description: 'حساب البنك الأهلي المصري',
          lastTransaction: '2024-07-04 09:45',
          transactionsCount: 78,
          isActive: true
        }
      ]
      setCashBoxes(mockCashBoxes)
    } finally {
      setLoading(false)
    }
  }

  const filterCashBoxes = () => {
    if (searchTerm) {
      const filtered = cashBoxes.filter(box =>
        box.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        box.currency.toLowerCase().includes(searchTerm.toLowerCase()) ||
        box.type.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredCashBoxes(filtered)
    } else {
      setFilteredCashBoxes(cashBoxes)
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddCashBox = () => {
    setEditingCashBox(null)
    setShowModal(true)
  }

  const handleEditCashBox = (cashBox) => {
    setEditingCashBox(cashBox)
    setShowModal(true)
  }

  const handleDeleteCashBox = async (cashBoxId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا الصندوق؟')) {
      try {
        setCashBoxes(prev => prev.filter(box => box.id !== cashBoxId))
        showNotification('تم حذف الصندوق بنجاح')
      } catch (error) {
        showNotification('فشل في حذف الصندوق', 'error')
      }
    }
  }

  const getCurrencySymbol = (currency) => {
    const symbols = {
      'EGP': 'ج.م',
      'USD': '$',
      'EUR': '€',
      'SAR': 'ر.س'
    }
    return symbols[currency] || currency
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'نقدي':
        return <Banknote className="h-5 w-5 text-primary" />
      case 'بنكي':
        return <CreditCard className="h-5 w-5 text-primary-600" />
      case 'عملة أجنبية':
        return <DollarSign className="h-5 w-5 text-purple-600" />
      default:
        return <Wallet className="h-5 w-5 text-muted-foreground" />
    }
  }

  const formatBalance = (balance, currency) => {
    if (!showBalances) return '****'
    return `${balance.toLocaleString()} ${getCurrencySymbol(currency)}`
  }

  const getTotalBalance = () => {
    return cashBoxes.reduce((total, box) => {
      if (box.currency === 'EGP') {
        return total + box.balance
      }
      // تحويل تقريبي للعملات الأجنبية
      const rate = box.currency === 'USD' ? 30.5 : box.currency === 'EUR' ? 33.2 : 1
      return total + (box.balance * rate)
    }, 0)
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
          <h1 className="text-2xl font-bold text-foreground">الصناديق والحسابات</h1>
          <p className="text-muted-foreground">إدارة الصناديق النقدية والحسابات البنكية</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowBalances(!showBalances)}
            className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center"
          >
            {showBalances ? <EyeOff className="w-5 h-5 ml-2" /> : <Eye className="w-5 h-5 ml-2" />}
            {showBalances ? 'إخفاء الأرصدة' : 'إظهار الأرصدة'}
          </button>
          <button
            onClick={handleAddCashBox}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
          >
            <Plus className="w-5 h-5 ml-2" />
            إضافة صندوق جديد
          </button>
        </div>
      </div>

      {/* Search and Actions */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="البحث في الصناديق..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
        <button
          onClick={loadCashBoxes}
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
            <Wallet className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الصناديق</p>
              <p className="text-2xl font-bold text-foreground">{cashBoxes.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الرصيد</p>
              <p className="text-2xl font-bold text-foreground">
                {showBalances ? `${getTotalBalance().toLocaleString()} ج.م` : '****'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Banknote className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الصناديق النقدية</p>
              <p className="text-2xl font-bold text-foreground">
                {cashBoxes.filter(box => box.type === 'نقدي').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <CreditCard className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">الحسابات البنكية</p>
              <p className="text-2xl font-bold text-foreground">
                {cashBoxes.filter(box => box.type === 'بنكي').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cash Boxes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCashBoxes.map((cashBox) => (
          <div key={cashBox.id} className="bg-white rounded-lg shadow border hover:shadow-md transition-shadow">
            <div className="p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  {getTypeIcon(cashBox.type)}
                  <div className="mr-3">
                    <h3 className="text-lg font-semibold text-foreground">{cashBox.name}</h3>
                    <p className="text-sm text-gray-500">{cashBox.type}</p>
                  </div>
                </div>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  cashBox.isActive 
                    ? 'bg-primary/20 text-green-800' 
                    : 'bg-destructive/20 text-red-800'
                }`}>
                  {cashBox.isActive ? 'نشط' : 'معطل'}
                </span>
              </div>

              {/* Balance */}
              <div className="mb-4">
                <p className="text-sm text-muted-foreground mb-1">الرصيد الحالي</p>
                <p className="text-2xl font-bold text-foreground">
                  {formatBalance(cashBox.balance, cashBox.currency)}
                </p>
              </div>

              {/* Description */}
              {cashBox.description && (
                <p className="text-sm text-muted-foreground mb-4">{cashBox.description}</p>
              )}

              {/* Stats */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">المعاملات</p>
                  <p className="text-lg font-semibold text-foreground">{cashBox.transactionsCount}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">آخر معاملة</p>
                  <p className="text-sm text-foreground">{cashBox.lastTransaction}</p>
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => handleEditCashBox(cashBox)}
                  className="text-primary-600 hover:text-primary-900 p-1"
                  title="تعديل"
                >
                  <Edit className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleDeleteCashBox(cashBox.id)}
                  className="text-destructive hover:text-red-900 p-1"
                  title="حذف"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium mb-4">
              {editingCashBox ? 'تعديل الصندوق' : 'إضافة صندوق جديد'}
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم الصندوق"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingCashBox?.name || ''}
              />
              <select className="w-full p-2 border border-border rounded-lg">
                <option value="">اختر نوع الصندوق</option>
                <option value="نقدي">نقدي</option>
                <option value="بنكي">بنكي</option>
                <option value="عملة أجنبية">عملة أجنبية</option>
              </select>
              <select className="w-full p-2 border border-border rounded-lg">
                <option value="">اختر العملة</option>
                <option value="EGP">الجنيه المصري (ج.م)</option>
                <option value="USD">الدولار الأمريكي ($)</option>
                <option value="EUR">اليورو (€)</option>
                <option value="SAR">الريال السعودي (ر.س)</option>
              </select>
              <input
                type="number"
                placeholder="الرصيد الابتدائي"
                className="w-full p-2 border border-border rounded-lg"
                defaultValue={editingCashBox?.balance || ''}
              />
              <textarea
                placeholder="وصف الصندوق"
                className="w-full p-2 border border-border rounded-lg"
                rows="3"
                defaultValue={editingCashBox?.description || ''}
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
                onClick={() => {
                  showNotification(editingCashBox ? 'تم تحديث الصندوق بنجاح' : 'تم إضافة الصندوق بنجاح')
                  setShowModal(false)
                }}
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

export default CashBoxes

