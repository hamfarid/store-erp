import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, Clock, XCircle, Truck, RefreshCw, ArrowRight, ArrowLeft, RotateCcw
} from 'lucide-react'
import { stockMovementsAPI } from '../services/api'

const StockMovementsAdvanced = () => {
  const [movements, setMovements] = useState([])
  const [filteredMovements, setFilteredMovements] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedMovement, setSelectedMovement] = useState(null)
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [_showCreateModal, setShowCreateModal] = useState(false)
  const [filters, setFilters] = useState({
    movement_type: '',
    state: '',
    date_from: '',
    date_to: '',
    product_id: '',
    warehouse_id: ''
  })

  // بيانات تجريبية لحركات المخزون المتقدمة
  const mockMovements = [
    {
      id: 1,
      movement_number: 'MOV-20241201001',
      movement_type: 'receipt',
      state: 'done',
      product_id: 1,
      product_name: 'بذور طماطم هجين',
      product_sku: 'TOM-HYB-001',
      lot_id: 1,
      lot_number: 'LOT-2024-001',
      quantity_planned: 100.0,
      quantity_done: 100.0,
      quantity_remaining: 0.0,
      unit_of_measure: 'كيلو',
      source_warehouse_name: 'مورد خارجي',
      destination_warehouse_name: 'المخزن الرئيسي',
      scheduled_date: '2024-12-01T10:00:00',
      effective_date: '2024-12-01T14:30:00',
      reference_type: 'purchase_order',
      reference_number: 'PO-2024-001',
      unit_cost: 25.50,
      total_cost: 2550.0,
      quality_check_required: true,
      quality_status: 'approved',
      created_by: 'أحمد محمد',
      created_at: '2024-12-01T09:00:00',
      notes: 'استلام دفعة جديدة من البذور عالية الجودة'
    },
    {
      id: 2,
      movement_number: 'MOV-20241201002',
      movement_type: 'delivery',
      state: 'confirmed',
      product_id: 2,
      product_name: 'سماد NPK متوازن',
      product_sku: 'NPK-BAL-001',
      lot_id: 2,
      lot_number: 'LOT-2024-002',
      quantity_planned: 50.0,
      quantity_done: 0.0,
      quantity_remaining: 50.0,
      unit_of_measure: 'كيس',
      source_warehouse_name: 'المخزن الرئيسي',
      destination_warehouse_name: 'عميل - مزرعة النيل',
      scheduled_date: '2024-12-02T09:00:00',
      effective_date: null,
      reference_type: 'sale_order',
      reference_number: 'SO-2024-001',
      unit_cost: 45.0,
      total_cost: 2250.0,
      quality_check_required: false,
      quality_status: null,
      created_by: 'فاطمة علي',
      created_at: '2024-12-01T15:30:00',
      notes: 'تسليم للعميل أحمد حسن - مزرعة النيل'
    },
    {
      id: 3,
      movement_number: 'MOV-20241201003',
      movement_type: 'internal_transfer',
      state: 'assigned',
      product_id: 1,
      product_name: 'بذور طماطم هجين',
      product_sku: 'TOM-HYB-001',
      lot_id: 1,
      lot_number: 'LOT-2024-001',
      quantity_planned: 25.0,
      quantity_done: 0.0,
      quantity_remaining: 25.0,
      unit_of_measure: 'كيلو',
      source_warehouse_name: 'المخزن الرئيسي',
      destination_warehouse_name: 'مخزن الفرع الأول',
      scheduled_date: '2024-12-02T14:00:00',
      effective_date: null,
      reference_type: 'internal',
      reference_number: 'INT-2024-001',
      unit_cost: 25.50,
      total_cost: 637.5,
      quality_check_required: false,
      quality_status: null,
      created_by: 'محمد أحمد',
      created_at: '2024-12-01T16:00:00',
      notes: 'نقل مخزون للفرع لتلبية الطلب المحلي'
    }
  ]

  useEffect(() => {
    loadMovements()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [movements, filters])

  const loadMovements = async () => {
    try {
      setLoading(true)
      // محاكاة تحميل البيانات
      setTimeout(() => {
        setMovements(mockMovements)
        setLoading(false)
      }, 1000)
    } catch (error) {
      setLoading(false)
    }
  }

  const applyFilters = () => {
    let filtered = [...movements]

    if (filters.movement_type) {
      filtered = filtered.filter(m => m.movement_type === filters.movement_type)
    }

    if (filters.state) {
      filtered = filtered.filter(m => m.state === filters.state)
    }

    if (filters.date_from) {
      filtered = filtered.filter(m => new Date(m.created_at) >= new Date(filters.date_from))
    }

    if (filters.date_to) {
      filtered = filtered.filter(m => new Date(m.created_at) <= new Date(filters.date_to))
    }

    setFilteredMovements(filtered)
  }

  const getMovementTypeIcon = (type) => {
    switch (type) {
      case 'receipt': return <ArrowRight className="w-4 h-4 text-primary" />
      case 'delivery': return <ArrowLeft className="w-4 h-4 text-primary-600" />
      case 'internal_transfer': return <RotateCcw className="w-4 h-4 text-purple-600" />
      case 'adjustment': return <RefreshCw className="w-4 h-4 text-accent" />
      default: return <Package className="w-4 h-4 text-muted-foreground" />
    }
  }

  const getMovementTypeName = (type) => {
    switch (type) {
      case 'receipt': return 'استلام'
      case 'delivery': return 'تسليم'
      case 'internal_transfer': return 'نقل داخلي'
      case 'adjustment': return 'تسوية'
      case 'production_in': return 'إنتاج - دخول'
      case 'production_out': return 'إنتاج - خروج'
      default: return 'غير محدد'
    }
  }

  const getStateIcon = (state) => {
    switch (state) {
      case 'draft': return <Clock className="w-4 h-4 text-gray-500" />
      case 'waiting': return <Clock className="w-4 h-4 text-yellow-500" />
      case 'confirmed': return <AlertCircle className="w-4 h-4 text-primary-500" />
      case 'assigned': return <CheckCircle className="w-4 h-4 text-purple-500" />
      case 'done': return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'cancelled': return <XCircle className="w-4 h-4 text-red-500" />
      default: return <Clock className="w-4 h-4 text-gray-500" />
    }
  }

  const getStateName = (state) => {
    switch (state) {
      case 'draft': return 'مسودة'
      case 'waiting': return 'في الانتظار'
      case 'confirmed': return 'مؤكدة'
      case 'assigned': return 'مخصصة'
      case 'done': return 'منفذة'
      case 'cancelled': return 'ملغاة'
      default: return 'غير محدد'
    }
  }

  const getStateColor = (state) => {
    switch (state) {
      case 'draft': return 'bg-muted text-foreground'
      case 'waiting': return 'bg-accent/20 text-yellow-800'
      case 'confirmed': return 'bg-primary-100 text-primary-800'
      case 'assigned': return 'bg-purple-100 text-purple-800'
      case 'done': return 'bg-primary/20 text-green-800'
      case 'cancelled': return 'bg-destructive/20 text-red-800'
      default: return 'bg-muted text-foreground'
    }
  }

  const handleConfirmMovement = async (movementId) => {
    try {
      await stockMovementsAPI.confirm(movementId)
      loadMovements()
    } catch (error) {
      }
  }

  const handleExecuteMovement = async (movementId, quantity) => {
    try {
      await stockMovementsAPI.execute(movementId, quantity)
      loadMovements()
    } catch (error) {
      }
  }

  const handleCancelMovement = async (movementId, reason) => {
    try {
      await stockMovementsAPI.cancel(movementId, reason)
      loadMovements()
    } catch (error) {
      }
  }

  const handleViewDetails = (movement) => {
    setSelectedMovement(movement)
    setShowDetailsModal(true)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="mr-3 text-muted-foreground">جاري تحميل حركات المخزون...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">حركات المخزون المتقدمة</h1>
          <p className="text-muted-foreground">إدارة شاملة لجميع حركات المخزون مع التتبع المتقدم</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
          >
            <Plus className="w-4 h-4 ml-2" />
            حركة جديدة
          </button>
          <button className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </button>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">إجمالي الحركات</p>
              <p className="text-2xl font-bold text-foreground">{movements.length}</p>
            </div>
            <Package className="w-8 h-8 text-primary-600" />
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">حركات منفذة</p>
              <p className="text-2xl font-bold text-primary">
                {movements.filter(m => m.state === 'done').length}
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-primary" />
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">في الانتظار</p>
              <p className="text-2xl font-bold text-accent">
                {movements.filter(m => ['confirmed', 'assigned'].includes(m.state)).length}
              </p>
            </div>
            <Clock className="w-8 h-8 text-accent" />
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">القيمة الإجمالية</p>
              <p className="text-2xl font-bold text-purple-600">
                {movements.reduce((sum, m) => sum + m.total_cost, 0).toLocaleString()} ج.م
              </p>
            </div>
            <Truck className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* أدوات الفلترة */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
          <select
            value={filters.movement_type}
            onChange={(e) => setFilters({...filters, movement_type: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">جميع الأنواع</option>
            <option value="receipt">استلام</option>
            <option value="delivery">تسليم</option>
            <option value="internal_transfer">نقل داخلي</option>
            <option value="adjustment">تسوية</option>
          </select>

          <select
            value={filters.state}
            onChange={(e) => setFilters({...filters, state: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">جميع الحالات</option>
            <option value="draft">مسودة</option>
            <option value="confirmed">مؤكدة</option>
            <option value="assigned">مخصصة</option>
            <option value="done">منفذة</option>
            <option value="cancelled">ملغاة</option>
          </select>

          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => setFilters({...filters, date_from: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="من تاريخ"
          />

          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => setFilters({...filters, date_to: e.target.value})}
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="إلى تاريخ"
          />

          <button
            onClick={() => setFilters({movement_type: '', state: '', date_from: '', date_to: '', product_id: '', warehouse_id: ''})}
            className="bg-muted text-foreground px-4 py-2 rounded-md hover:bg-muted flex items-center justify-center"
          >
            <RefreshCw className="w-4 h-4 ml-2" />
            إعادة تعيين
          </button>

          <button className="bg-primary-100 text-primary-700 px-4 py-2 rounded-md hover:bg-primary-200 flex items-center justify-center">
            <Filter className="w-4 h-4 ml-2" />
            فلاتر متقدمة
          </button>
        </div>
      </div>

      {/* جدول الحركات */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">رقم الحركة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المنتج</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الكمية</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المسار</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredMovements.map((movement) => (
                <tr key={movement.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-foreground">{movement.movement_number}</div>
                      <div className="text-sm text-gray-500">{movement.reference_number}</div>
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {getMovementTypeIcon(movement.movement_type)}
                      <span className="mr-2 text-sm font-medium text-foreground">
                        {getMovementTypeName(movement.movement_type)}
                      </span>
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-foreground">{movement.product_name}</div>
                      <div className="text-sm text-gray-500">{movement.product_sku}</div>
                      {movement.lot_number && (
                        <div className="text-xs text-primary-600">لوط: {movement.lot_number}</div>
                      )}
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-foreground">
                        {movement.quantity_done}/{movement.quantity_planned} {movement.unit_of_measure}
                      </div>
                      <div className="w-full bg-muted rounded-full h-2 mt-1">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${(movement.quantity_done / movement.quantity_planned) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm">
                      <div className="text-foreground">{movement.source_warehouse_name}</div>
                      <div className="text-gray-400 text-center">↓</div>
                      <div className="text-foreground">{movement.destination_warehouse_name}</div>
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {getStateIcon(movement.state)}
                      <span className={`mr-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStateColor(movement.state)}`}>
                        {getStateName(movement.state)}
                      </span>
                    </div>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">
                      {new Date(movement.scheduled_date).toLocaleDateString('ar-EG')}
                    </div>
                    {movement.effective_date && (
                      <div className="text-xs text-primary">
                        نُفذ: {new Date(movement.effective_date).toLocaleDateString('ar-EG')}
                      </div>
                    )}
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleViewDetails(movement)}
                        className="text-primary-600 hover:text-primary-900"
                        title="عرض التفاصيل"
                      >
                        <Eye className="w-4 h-4" />
                      </button>

                      {movement.state === 'draft' && (
                        <button
                          onClick={() => handleConfirmMovement(movement.id)}
                          className="text-primary hover:text-green-900"
                          title="تأكيد"
                        >
                          <Check className="w-4 h-4" />
                        </button>
                      )}

                      {['confirmed', 'assigned'].includes(movement.state) && (
                        <button
                          onClick={() => handleExecuteMovement(movement.id, movement.quantity_planned)}
                          className="text-purple-600 hover:text-purple-900"
                          title="تنفيذ"
                        >
                          <CheckCircle className="w-4 h-4" />
                        </button>
                      )}

                      {!['done', 'cancelled'].includes(movement.state) && (
                        <button
                          onClick={() => handleCancelMovement(movement.id, 'إلغاء بواسطة المستخدم')}
                          className="text-destructive hover:text-red-900"
                          title="إلغاء"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* مودال تفاصيل الحركة */}
      {showDetailsModal && selectedMovement && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-semibold">تفاصيل الحركة: {selectedMovement.movement_number}</h3>
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
                  <div><span className="font-medium">رقم الحركة:</span> {selectedMovement.movement_number}</div>
                  <div><span className="font-medium">النوع:</span> {getMovementTypeName(selectedMovement.movement_type)}</div>
                  <div><span className="font-medium">الحالة:</span> {getStateName(selectedMovement.state)}</div>
                  <div><span className="font-medium">المرجع:</span> {selectedMovement.reference_number}</div>
                  <div><span className="font-medium">أنشئ بواسطة:</span> {selectedMovement.created_by}</div>
                </div>
              </div>

              {/* معلومات المنتج */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground border-b pb-2">معلومات المنتج</h4>
                <div className="space-y-2">
                  <div><span className="font-medium">المنتج:</span> {selectedMovement.product_name}</div>
                  <div><span className="font-medium">رمز المنتج:</span> {selectedMovement.product_sku}</div>
                  {selectedMovement.lot_number && (
                    <div><span className="font-medium">رقم اللوط:</span> {selectedMovement.lot_number}</div>
                  )}
                  <div><span className="font-medium">الكمية المخططة:</span> {selectedMovement.quantity_planned} {selectedMovement.unit_of_measure}</div>
                  <div><span className="font-medium">الكمية المنفذة:</span> {selectedMovement.quantity_done} {selectedMovement.unit_of_measure}</div>
                </div>
              </div>
            </div>

            {selectedMovement.notes && (
              <div className="mt-6">
                <h4 className="font-medium text-foreground border-b pb-2">ملاحظات</h4>
                <p className="mt-2 text-foreground">{selectedMovement.notes}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default StockMovementsAdvanced
