import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const StockMovements = () => {
  const [movements, setMovements] = useState([])
  const [filteredMovements, setFilteredMovements] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [typeFilter, setTypeFilter] = useState('all')
  const [dateFilter, setDateFilter] = useState('all')

  useEffect(() => {
    loadMovements()
  }, [])

  useEffect(() => {
    filterMovements()
  }, [movements, searchTerm, typeFilter, dateFilter])

  const loadMovements = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://172.16.16.27:8000/api/stock-movements')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setMovements(data.data)
        } else {
          throw new Error('فشل في تحميل حركات المخزون')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockMovements = [
        {
          id: 1,
          type: 'وارد',
          productName: 'بذور طماطم هجين',
          quantity: 100,
          unit: 'كيس',
          warehouse: 'المخزن الرئيسي',
          reference: 'PO-2024-001',
          date: '2024-07-01',
          time: '10:30',
          user: 'أحمد محمد',
          notes: 'استلام شحنة جديدة من المورد'
        },
        {
          id: 2,
          type: 'صادر',
          productName: 'سماد NPK',
          quantity: 50,
          unit: 'كيس',
          warehouse: 'مخزن الأسمدة',
          reference: 'SO-2024-015',
          date: '2024-07-01',
          time: '14:15',
          user: 'سارة علي',
          notes: 'بيع للعميل مزرعة النيل'
        },
        {
          id: 3,
          type: 'تحويل',
          productName: 'مبيد حشري',
          quantity: 25,
          unit: 'لتر',
          warehouse: 'المخزن الرئيسي → مخزن الفرع',
          reference: 'TR-2024-008',
          date: '2024-06-30',
          time: '16:45',
          user: 'محمد أحمد',
          notes: 'تحويل للفرع الجديد'
        },
        {
          id: 4,
          type: 'تسوية',
          productName: 'بذور خيار',
          quantity: -5,
          unit: 'كيس',
          warehouse: 'مخزن البذور',
          reference: 'ADJ-2024-003',
          date: '2024-06-30',
          time: '09:20',
          user: 'أحمد محمد',
          notes: 'تسوية نقص في الجرد'
        }
      ]
      setMovements(mockMovements)
    } finally {
      setLoading(false)
    }
  }

  const filterMovements = () => {
    let filtered = movements

    if (searchTerm) {
      filtered = filtered.filter(movement =>
        movement.productName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        movement.reference.toLowerCase().includes(searchTerm.toLowerCase()) ||
        movement.warehouse.toLowerCase().includes(searchTerm.toLowerCase()) ||
        movement.user.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (typeFilter !== 'all') {
      filtered = filtered.filter(movement => movement.type === typeFilter)
    }

    if (dateFilter !== 'all') {
      const today = new Date()
      const filterDate = new Date()
      
      switch (dateFilter) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0)
          filtered = filtered.filter(movement => 
            new Date(movement.date) >= filterDate
          )
          break
        case 'week':
          filterDate.setDate(today.getDate() - 7)
          filtered = filtered.filter(movement => 
            new Date(movement.date) >= filterDate
          )
          break
        case 'month':
          filterDate.setMonth(today.getMonth() - 1)
          filtered = filtered.filter(movement => 
            new Date(movement.date) >= filterDate
          )
          break
      }
    }

    setFilteredMovements(filtered)
  }

  const getMovementIcon = (type) => {
    switch (type) {
      case 'وارد':
        return <ArrowDownCircle className="h-5 w-5 text-primary" />
      case 'صادر':
        return <ArrowUpCircle className="h-5 w-5 text-destructive" />
      case 'تحويل':
        return <RotateCcw className="h-5 w-5 text-primary-600" />
      case 'تسوية':
        return <Package className="h-5 w-5 text-accent" />
      default:
        return <Package className="h-5 w-5 text-muted-foreground" />
    }
  }

  const getMovementColor = (type) => {
    switch (type) {
      case 'وارد':
        return 'bg-primary/20 text-green-800'
      case 'صادر':
        return 'bg-destructive/20 text-red-800'
      case 'تحويل':
        return 'bg-primary-100 text-primary-800'
      case 'تسوية':
        return 'bg-accent/20 text-yellow-800'
      default:
        return 'bg-muted text-foreground'
    }
  }

  const getQuantityDisplay = (quantity, type) => {
    const sign = type === 'وارد' ? '+' : type === 'صادر' ? '-' : ''
    return `${sign}${Math.abs(quantity)}`
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
          <h1 className="text-2xl font-bold text-foreground">حركات المخزون</h1>
          <p className="text-muted-foreground">تتبع جميع حركات الدخول والخروج والتحويلات</p>
        </div>
        <div className="flex gap-2">
          <button className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center">
            <Download className="w-5 h-5 ml-2" />
            تصدير
          </button>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center">
            <Plus className="w-5 h-5 ml-2" />
            حركة جديدة
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="البحث في الحركات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>

        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="all">جميع الأنواع</option>
          <option value="وارد">وارد</option>
          <option value="صادر">صادر</option>
          <option value="تحويل">تحويل</option>
          <option value="تسوية">تسوية</option>
        </select>

        <select
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="all">جميع التواريخ</option>
          <option value="today">اليوم</option>
          <option value="week">آخر أسبوع</option>
          <option value="month">آخر شهر</option>
        </select>

        <button
          onClick={loadMovements}
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
            <ArrowDownCircle className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">حركات الوارد</p>
              <p className="text-2xl font-bold text-foreground">
                {movements.filter(m => m.type === 'وارد').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <ArrowUpCircle className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">حركات الصادر</p>
              <p className="text-2xl font-bold text-foreground">
                {movements.filter(m => m.type === 'صادر').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <RotateCcw className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">التحويلات</p>
              <p className="text-2xl font-bold text-foreground">
                {movements.filter(m => m.type === 'تحويل').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">التسويات</p>
              <p className="text-2xl font-bold text-foreground">
                {movements.filter(m => m.type === 'تسوية').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Movements Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                النوع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المنتج
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الكمية
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المخزن
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المرجع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                التاريخ والوقت
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المستخدم
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredMovements.map((movement) => (
              <tr key={movement.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {getMovementIcon(movement.type)}
                    <span className={`mr-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getMovementColor(movement.type)}`}>
                      {movement.type}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-foreground">
                    {movement.productName}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-foreground">
                    <span className={`font-medium ${
                      movement.type === 'وارد' ? 'text-primary' :
                      movement.type === 'صادر' ? 'text-destructive' : 'text-primary-600'
                    }`}>
                      {getQuantityDisplay(movement.quantity, movement.type)}
                    </span>
                    <span className="text-gray-500 mr-1">{movement.unit}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {movement.warehouse}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {movement.reference}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  <div>{new Date(movement.date).toLocaleDateString('ar-EG')}</div>
                  <div className="text-gray-500">{movement.time}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {movement.user}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredMovements.length === 0 && (
        <div className="text-center py-12">
          <Package className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-foreground">لا توجد حركات</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm || typeFilter !== 'all' || dateFilter !== 'all'
              ? 'لا توجد نتائج تطابق الفلاتر المحددة'
              : 'لم يتم تسجيل أي حركات مخزون بعد'}
          </p>
        </div>
      )}
    </div>
  )
}

export default StockMovements

