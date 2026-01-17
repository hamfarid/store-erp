import React, { useState, useEffect } from 'react'
import { AlertTriangle, Calendar, MapPin, Package } from 'lucide-react'
// eslint-disable-next-line no-unused-vars
import { toast } from 'react-hot-toast'

const LotWarehouseManager = ({ productId, onLotSelect, onWarehouseSelect }) => {
  const [lots, setLots] = useState([])
  const [warehouses, setWarehouses] = useState([])
  const [selectedLot, setSelectedLot] = useState('')
  const [selectedWarehouse, setSelectedWarehouse] = useState('')
  const [_availableStock, setAvailableStock] = useState(0)

  // بيانات تجريبية للوط والمخازن
  useEffect(() => {
    // محاكاة تحميل اللوط المتاحة للمنتج
    const mockLots = [
      {
        id: 'LOT001',
        number: 'LOT001',
        expiryDate: '2025-12-31',
        quantity: 100,
        warehouse: 'main',
        status: 'متاح'
      },
      {
        id: 'LOT002', 
        number: 'LOT002',
        expiryDate: '2025-06-30',
        quantity: 50,
        warehouse: 'main',
        status: 'قريب الانتهاء'
      },
      {
        id: 'LOT003',
        number: 'LOT003', 
        expiryDate: '2026-03-15',
        quantity: 75,
        warehouse: 'secondary',
        status: 'متاح'
      }
    ]

    // محاكاة تحميل المخازن حسب صلاحية المستخدم
    const mockWarehouses = [
      {
        id: 'main',
        name: 'المخزن الرئيسي',
        location: 'القاهرة',
        hasAccess: true,
        capacity: 1000,
        currentStock: 500
      },
      {
        id: 'secondary',
        name: 'المخزن الفرعي',
        location: 'الإسكندرية', 
        hasAccess: true,
        capacity: 500,
        currentStock: 200
      },
      {
        id: 'restricted',
        name: 'مخزن محدود الصلاحية',
        location: 'الجيزة',
        hasAccess: false,
        capacity: 300,
        currentStock: 100
      }
    ]

    setLots(mockLots)
    setWarehouses(mockWarehouses.filter(w => w.hasAccess)) // فقط المخازن المسموحة
  }, [productId])

  // تحديث الكمية المتاحة عند تغيير اللوط أو المخزن
  useEffect(() => {
    if (selectedLot && selectedWarehouse) {
      const lot = lots.find(l => l.number === selectedLot && l.warehouse === selectedWarehouse)
      setAvailableStock(lot ? lot.quantity : 0)
    } else {
      setAvailableStock(0)
    }
  }, [selectedLot, selectedWarehouse, lots])

  // التحقق من صلاحية اللوط
  const checkLotExpiry = (expiryDate) => {
    const today = new Date()
    const expiry = new Date(expiryDate)
    const daysUntilExpiry = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
    
    if (daysUntilExpiry < 0) return { status: 'منتهي الصلاحية', color: 'text-destructive', days: daysUntilExpiry }
    if (daysUntilExpiry <= 30) return { status: 'قريب الانتهاء', color: 'text-accent', days: daysUntilExpiry }
    return { status: 'صالح', color: 'text-primary', days: daysUntilExpiry }
  }

  // تحديد اللوط
  const handleLotChange = (lotNumber) => {
    setSelectedLot(lotNumber)
    onLotSelect && onLotSelect(lotNumber)
    
    // إذا تم اختيار لوط، اختر المخزن تلقائياً
    const lot = lots.find(l => l.number === lotNumber)
    if (lot) {
      setSelectedWarehouse(lot.warehouse)
      onWarehouseSelect && onWarehouseSelect(lot.warehouse)
    }
  }

  // تحديد المخزن
  const handleWarehouseChange = (warehouseId) => {
    setSelectedWarehouse(warehouseId)
    onWarehouseSelect && onWarehouseSelect(warehouseId)
    
    // إعادة تعيين اللوط إذا لم يكن متاحاً في المخزن الجديد
    if (selectedLot) {
      const lotExists = lots.some(l => l.number === selectedLot && l.warehouse === warehouseId)
      if (!lotExists) {
        setSelectedLot('')
        onLotSelect && onLotSelect('')
      }
    }
  }

  // فلترة اللوط حسب المخزن المختار
  const getAvailableLots = () => {
    if (!selectedWarehouse) return lots
    return lots.filter(lot => lot.warehouse === selectedWarehouse)
  }

  return (
    <div className="space-y-4">
      {/* اختيار المخزن */}
      <div>
        <label className="block text-sm font-medium text-foreground mb-2">
          <MapPin className="w-4 h-4 inline mr-1" />
          المخزن
        </label>
        <select
          value={selectedWarehouse}
          onChange={(e) => handleWarehouseChange(e.target.value)}
          className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">اختر المخزن</option>
          {warehouses.map(warehouse => (
            <option key={warehouse.id} value={warehouse.id}>
              {warehouse.name} - {warehouse.location} 
              (متاح: {warehouse.capacity - warehouse.currentStock})
            </option>
          ))}
        </select>
      </div>

      {/* اختيار اللوط */}
      <div>
        <label className="block text-sm font-medium text-foreground mb-2">
          <Package className="w-4 h-4 inline mr-1" />
          رقم اللوط
        </label>
        <select
          value={selectedLot}
          onChange={(e) => handleLotChange(e.target.value)}
          className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          disabled={!selectedWarehouse}
        >
          <option value="">اختر اللوط</option>
          {getAvailableLots().map(lot => {
            const expiryInfo = checkLotExpiry(lot.expiryDate)
            return (
              <option key={lot.id} value={lot.number}>
                {lot.number} - الكمية: {lot.quantity} - {expiryInfo.status}
              </option>
            )
          })}
        </select>
      </div>

      {/* معلومات اللوط المختار */}
      {selectedLot && (
        <div className="bg-muted/50 p-4 rounded-lg">
          <h4 className="font-medium text-foreground mb-3">معلومات اللوط</h4>
          {(() => {
            const lot = lots.find(l => l.number === selectedLot && l.warehouse === selectedWarehouse)
            if (!lot) return null
            
            const expiryInfo = checkLotExpiry(lot.expiryDate)
            return (
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">رقم اللوط:</span>
                  <span className="ml-2">{lot.number}</span>
                </div>
                <div>
                  <span className="font-medium">الكمية المتاحة:</span>
                  <span className="ml-2 font-semibold text-primary-600">{lot.quantity}</span>
                </div>
                <div>
                  <span className="font-medium">تاريخ الانتهاء:</span>
                  <span className="ml-2">{lot.expiryDate}</span>
                </div>
                <div>
                  <span className="font-medium">حالة الصلاحية:</span>
                  <span className={`ml-2 font-semibold ${expiryInfo.color}`}>
                    {expiryInfo.status}
                    {expiryInfo.days > 0 && ` (${expiryInfo.days} يوم)`}
                  </span>
                </div>
              </div>
            )
          })()}
          
          {/* تحذيرات */}
          {(() => {
            const lot = lots.find(l => l.number === selectedLot && l.warehouse === selectedWarehouse)
            if (!lot) return null
            
            const expiryInfo = checkLotExpiry(lot.expiryDate)
            if (expiryInfo.days <= 30) {
              return (
                <div className="mt-3 p-3 bg-accent/10 border border-orange-200 rounded-md">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-accent" />
                    <span className="text-orange-800 text-sm font-medium">
                      {expiryInfo.days < 0 
                        ? 'تحذير: هذا اللوط منتهي الصلاحية!'
                        : `تحذير: هذا اللوط سينتهي خلال ${expiryInfo.days} يوم`
                      }
                    </span>
                  </div>
                </div>
              )
            }
            return null
          })()}
        </div>
      )}

      {/* معلومات المخزن المختار */}
      {selectedWarehouse && (
        <div className="bg-primary-50 p-4 rounded-lg">
          <h4 className="font-medium text-foreground mb-3">معلومات المخزن</h4>
          {(() => {
            const warehouse = warehouses.find(w => w.id === selectedWarehouse)
            if (!warehouse) return null
            
            return (
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">اسم المخزن:</span>
                  <span className="ml-2">{warehouse.name}</span>
                </div>
                <div>
                  <span className="font-medium">الموقع:</span>
                  <span className="ml-2">{warehouse.location}</span>
                </div>
                <div>
                  <span className="font-medium">السعة الكلية:</span>
                  <span className="ml-2">{warehouse.capacity}</span>
                </div>
                <div>
                  <span className="font-medium">المساحة المتاحة:</span>
                  <span className="ml-2 font-semibold text-primary">
                    {warehouse.capacity - warehouse.currentStock}
                  </span>
                </div>
              </div>
            )
          })()}
        </div>
      )}
    </div>
  )
}

export default LotWarehouseManager

