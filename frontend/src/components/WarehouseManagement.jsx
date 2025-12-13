import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Building, MapPin, Thermometer, Shield, Droplets, Camera, Wifi, AlertTriangle
} from 'lucide-react'
// import { toast } from 'react-hot-toast' // Currently unused

const WarehouseManagement = () => {
  const [warehouses, setWarehouses] = useState([])
  const [selectedWarehouse, setSelectedWarehouse] = useState(null)
  // const [showAddModal, setShowAddModal] = useState(false) // Currently unused
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  // بيانات تجريبية للمخازن المتقدمة
  const mockWarehouses = [
    {
      id: 1,
      name: 'المخزن الرئيسي',
      name_en: 'Main Warehouse',
      code: 'WH-001',
      warehouse_type: 'main',
      address: 'شارع الصناعة، المنطقة الصناعية، القاهرة',
      city: 'القاهرة',
      state: 'القاهرة',
      country: 'مصر',
      phone: '+20123456789',
      email: 'warehouse1@company.com',
      manager_name: 'أحمد محمد',
      total_area: 5000.0,
      storage_area: 4000.0,
      max_capacity: 10000.0,
      current_utilization: 75.5,
      operating_hours_start: '08:00',
      operating_hours_end: '18:00',
      temperature_controlled: true,
      min_temperature: 5.0,
      max_temperature: 25.0,
      humidity_controlled: true,
      max_humidity: 60.0,
      security_level: 'high',
      has_cctv: true,
      has_alarm: true,
      has_fire_system: true,
      has_wms: true,
      has_barcode_scanner: true,
      has_rfid: false,
      monthly_rent: 15000.0,
      is_active: true,
      is_default: true,
      locations_count: 25,
      products_count: 150,
      current_stock_value: 125000.0
    },
    {
      id: 2,
      name: 'مخزن الفرع الأول',
      name_en: 'Branch Warehouse 1',
      code: 'WH-002',
      warehouse_type: 'branch',
      address: 'شارع النيل، الجيزة',
      city: 'الجيزة',
      state: 'الجيزة',
      country: 'مصر',
      phone: '+20123456790',
      email: 'warehouse2@company.com',
      manager_name: 'فاطمة علي',
      total_area: 2000.0,
      storage_area: 1600.0,
      max_capacity: 4000.0,
      current_utilization: 60.2,
      operating_hours_start: '09:00',
      operating_hours_end: '17:00',
      temperature_controlled: false,
      humidity_controlled: false,
      security_level: 'medium',
      has_cctv: true,
      has_alarm: false,
      has_fire_system: true,
      has_wms: false,
      has_barcode_scanner: true,
      has_rfid: false,
      monthly_rent: 8000.0,
      is_active: true,
      is_default: false,
      locations_count: 12,
      products_count: 85,
      current_stock_value: 45000.0
    }
  ]

  useEffect(() => {
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setWarehouses(mockWarehouses)
      setLoading(false)
    }, 1000)
  }, [])

  const getWarehouseTypeColor = (type) => {
    switch (type) {
      case 'main': return 'bg-primary-100 text-primary-800'
      case 'branch': return 'bg-primary/20 text-green-800'
      case 'transit': return 'bg-accent/20 text-yellow-800'
      case 'quarantine': return 'bg-destructive/20 text-red-800'
      default: return 'bg-muted text-foreground'
    }
  }

  const getWarehouseTypeName = (type) => {
    switch (type) {
      case 'main': return 'رئيسي'
      case 'branch': return 'فرع'
      case 'transit': return 'عبور'
      case 'quarantine': return 'حجر صحي'
      default: return 'غير محدد'
    }
  }

  const getUtilizationColor = (utilization) => {
    if (utilization >= 90) return 'text-destructive'
    if (utilization >= 75) return 'text-accent'
    if (utilization >= 50) return 'text-accent'
    return 'text-primary'
  }

  const handleViewDetails = (warehouse) => {
    setSelectedWarehouse(warehouse)
    setShowDetailsModal(true)
    setActiveTab('overview')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="mr-3 text-muted-foreground">جاري تحميل المخازن...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة المخازن المتقدمة</h1>
          <p className="text-muted-foreground">إدارة شاملة للمخازن والمواقع مع التحكم البيئي</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center"
          >
            <Plus className="w-4 h-4 ml-2" />
            مخزن جديد
          </button>
          <button className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center">
            <Settings className="w-4 h-4 ml-2" />
            إعدادات المخازن
          </button>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">إجمالي المخازن</p>
              <p className="text-2xl font-bold text-foreground">{warehouses.length}</p>
            </div>
            <Building className="w-8 h-8 text-primary-600" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">المساحة الإجمالية</p>
              <p className="text-2xl font-bold text-primary">
                {warehouses.reduce((sum, w) => sum + w.total_area, 0).toLocaleString()} م²
              </p>
            </div>
            <MapPin className="w-8 h-8 text-primary" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">متوسط الاستخدام</p>
              <p className="text-2xl font-bold text-accent">
                {(warehouses.reduce((sum, w) => sum + w.current_utilization, 0) / warehouses.length).toFixed(1)}%
              </p>
            </div>
            <BarChart3 className="w-8 h-8 text-accent" />
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">قيمة المخزون</p>
              <p className="text-2xl font-bold text-purple-600">
                {warehouses.reduce((sum, w) => sum + w.current_stock_value, 0).toLocaleString()} ج.م
              </p>
            </div>
            <Package className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* جدول المخازن */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المخزن</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">النوع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الموقع</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المساحة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الاستخدام</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المميزات</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراءات</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {warehouses.map((warehouse) => (
                <tr key={warehouse.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-foreground">{warehouse.name}</div>
                      <div className="text-sm text-gray-500">{warehouse.code}</div>
                      <div className="text-xs text-gray-400">{warehouse.manager_name}</div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getWarehouseTypeColor(warehouse.warehouse_type)}`}>
                      {getWarehouseTypeName(warehouse.warehouse_type)}
                    </span>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">{warehouse.city}</div>
                    <div className="text-xs text-gray-500">{warehouse.state}</div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">{warehouse.total_area.toLocaleString()} م²</div>
                    <div className="text-xs text-gray-500">تخزين: {warehouse.storage_area.toLocaleString()} م²</div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-1">
                        <div className={`text-sm font-medium ${getUtilizationColor(warehouse.current_utilization)}`}>
                          {warehouse.current_utilization}%
                        </div>
                        <div className="w-full bg-muted rounded-full h-2 mt-1">
                          <div 
                            className={`h-2 rounded-full ${
                              warehouse.current_utilization >= 90 ? 'bg-destructive/100' :
                              warehouse.current_utilization >= 75 ? 'bg-accent/100' :
                              warehouse.current_utilization >= 50 ? 'bg-accent/100' : 'bg-primary/100'
                            }`}
                            style={{ width: `${warehouse.current_utilization}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-1 space-x-reverse">
                      {warehouse.temperature_controlled && (
                        <Thermometer className="w-4 h-4 text-primary-500" title="تحكم في درجة الحرارة" />
                      )}
                      {warehouse.humidity_controlled && (
                        <Droplets className="w-4 h-4 text-cyan-500" title="تحكم في الرطوبة" />
                      )}
                      {warehouse.has_cctv && (
                        <Camera className="w-4 h-4 text-purple-500" title="كاميرات مراقبة" />
                      )}
                      {warehouse.has_wms && (
                        <Wifi className="w-4 h-4 text-green-500" title="نظام إدارة المخازن" />
                      )}
                      {warehouse.security_level === 'high' && (
                        <Shield className="w-4 h-4 text-red-500" title="أمان عالي" />
                      )}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {warehouse.is_active ? (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-red-500" />
                      )}
                      <span className={`mr-2 text-sm ${warehouse.is_active ? 'text-primary' : 'text-destructive'}`}>
                        {warehouse.is_active ? 'نشط' : 'غير نشط'}
                      </span>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleViewDetails(warehouse)}
                        className="text-primary-600 hover:text-primary-900"
                        title="عرض التفاصيل"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        className="text-primary hover:text-green-900"
                        title="تعديل"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
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

      {/* مودال تفاصيل المخزن */}
      {showDetailsModal && selectedWarehouse && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-6xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold">تفاصيل المخزن: {selectedWarehouse.name}</h3>
              <button
                onClick={() => setShowDetailsModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>
            
            {/* تبويبات */}
            <div className="border-b border-border mb-6">
              <nav className="-mb-px flex space-x-8 space-x-reverse">
                {[
                  { id: 'overview', name: 'نظرة عامة', icon: Building },
                  { id: 'locations', name: 'المواقع', icon: MapPin },
                  { id: 'environment', name: 'البيئة', icon: Thermometer },
                  { id: 'security', name: 'الأمان', icon: Shield },
                  { id: 'performance', name: 'الأداء', icon: TrendingUp }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`${
                      activeTab === tab.id
                        ? 'border-primary-500 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                    } whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center`}
                  >
                    <tab.icon className="w-4 h-4 ml-2" />
                    {tab.name}
                  </button>
                ))}
              </nav>
            </div>

            {/* محتوى التبويبات */}
            <div className="space-y-6">
              {activeTab === 'overview' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground border-b pb-2">المعلومات الأساسية</h4>
                    <div className="space-y-2">
                      <div><span className="font-medium">الاسم:</span> {selectedWarehouse.name}</div>
                      <div><span className="font-medium">الكود:</span> {selectedWarehouse.code}</div>
                      <div><span className="font-medium">النوع:</span> {getWarehouseTypeName(selectedWarehouse.warehouse_type)}</div>
                      <div><span className="font-medium">المدير:</span> {selectedWarehouse.manager_name}</div>
                      <div><span className="font-medium">الهاتف:</span> {selectedWarehouse.phone}</div>
                      <div><span className="font-medium">البريد:</span> {selectedWarehouse.email}</div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground border-b pb-2">المساحة والسعة</h4>
                    <div className="space-y-2">
                      <div><span className="font-medium">المساحة الكلية:</span> {selectedWarehouse.total_area} م²</div>
                      <div><span className="font-medium">مساحة التخزين:</span> {selectedWarehouse.storage_area} م²</div>
                      <div><span className="font-medium">السعة القصوى:</span> {selectedWarehouse.max_capacity}</div>
                      <div><span className="font-medium">نسبة الاستخدام:</span> {selectedWarehouse.current_utilization}%</div>
                      <div><span className="font-medium">عدد المواقع:</span> {selectedWarehouse.locations_count}</div>
                      <div><span className="font-medium">عدد المنتجات:</span> {selectedWarehouse.products_count}</div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'environment' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground border-b pb-2">التحكم في درجة الحرارة</h4>
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <Thermometer className="w-5 h-5 text-primary-500 ml-2" />
                        <span>التحكم في درجة الحرارة: {selectedWarehouse.temperature_controlled ? 'مفعل' : 'غير مفعل'}</span>
                      </div>
                      {selectedWarehouse.temperature_controlled && (
                        <>
                          <div><span className="font-medium">أقل درجة حرارة:</span> {selectedWarehouse.min_temperature}°C</div>
                          <div><span className="font-medium">أعلى درجة حرارة:</span> {selectedWarehouse.max_temperature}°C</div>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground border-b pb-2">التحكم في الرطوبة</h4>
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <Droplets className="w-5 h-5 text-cyan-500 ml-2" />
                        <span>التحكم في الرطوبة: {selectedWarehouse.humidity_controlled ? 'مفعل' : 'غير مفعل'}</span>
                      </div>
                      {selectedWarehouse.humidity_controlled && (
                        <div><span className="font-medium">أقصى رطوبة:</span> {selectedWarehouse.max_humidity}%</div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default WarehouseManagement

