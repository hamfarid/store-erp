/**
 * Warehouse Management Page - صفحة إدارة المستودعات
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Warehouse,
  Plus,
  Search,
  MapPin,
  Package,
  ArrowUpDown,
  Settings,
  Eye,
  Edit,
  Trash2,
  BarChart3,
} from 'lucide-react'

const warehouses = [
  { id: 1, name: 'المستودع الرئيسي', code: 'WH-001', location: 'الرياض', type: 'main', capacity: 10000, used: 7500, status: 'active' },
  { id: 2, name: 'مستودع الشمال', code: 'WH-002', location: 'الدمام', type: 'branch', capacity: 5000, used: 3200, status: 'active' },
  { id: 3, name: 'مستودع الجنوب', code: 'WH-003', location: 'جدة', type: 'branch', capacity: 8000, used: 6100, status: 'active' },
  { id: 4, name: 'مستودع التبريد', code: 'WH-004', location: 'الرياض', type: 'cold', capacity: 2000, used: 1800, status: 'maintenance' },
]

const warehouseTypes = {
  main: { label: 'رئيسي', color: 'emerald' },
  branch: { label: 'فرعي', color: 'blue' },
  cold: { label: 'تبريد', color: 'cyan' },
  transit: { label: 'عبور', color: 'amber' },
}

export default function WarehousePage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)

  const filteredWarehouses = warehouses.filter(w =>
    w.name.includes(searchTerm) || w.code.includes(searchTerm)
  )

  const getCapacityColor = (used, capacity) => {
    const percent = (used / capacity) * 100
    if (percent >= 90) return 'red'
    if (percent >= 70) return 'amber'
    return 'emerald'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6" dir="rtl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto space-y-6"
      >
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
              <Warehouse className="w-8 h-8 text-blue-400" />
              إدارة المستودعات
            </h1>
            <p className="text-slate-400 mt-1">إدارة ومتابعة جميع المستودعات</p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            إضافة مستودع
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'إجمالي المستودعات', value: warehouses.length, icon: Warehouse, color: 'blue' },
            { label: 'السعة الإجمالية', value: '25,000', icon: Package, color: 'emerald' },
            { label: 'المستخدم', value: '18,600', icon: BarChart3, color: 'amber' },
            { label: 'نسبة الإشغال', value: '74.4%', icon: ArrowUpDown, color: 'purple' },
          ].map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4"
            >
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg bg-${stat.color}-500/20`}>
                  <stat.icon className={`w-5 h-5 text-${stat.color}-400`} />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">{stat.label}</p>
                  <p className="text-white text-xl font-bold">{stat.value}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="البحث في المستودعات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Warehouses Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredWarehouses.map((warehouse, index) => {
            const capacityPercent = (warehouse.used / warehouse.capacity) * 100
            const capacityColor = getCapacityColor(warehouse.used, warehouse.capacity)
            const typeInfo = warehouseTypes[warehouse.type]
            
            return (
              <motion.div
                key={warehouse.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-5 hover:border-slate-600 transition-colors"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{warehouse.name}</h3>
                    <p className="text-slate-400 text-sm">{warehouse.code}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs bg-${typeInfo.color}-500/20 text-${typeInfo.color}-400`}>
                    {typeInfo.label}
                  </span>
                </div>

                <div className="flex items-center gap-2 text-slate-400 text-sm mb-4">
                  <MapPin className="w-4 h-4" />
                  {warehouse.location}
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">السعة</span>
                    <span className="text-white">{warehouse.used.toLocaleString()} / {warehouse.capacity.toLocaleString()}</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-${capacityColor}-500 rounded-full transition-all`}
                      style={{ width: `${capacityPercent}%` }}
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    warehouse.status === 'active'
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {warehouse.status === 'active' ? 'نشط' : 'صيانة'}
                  </span>
                  <div className="flex gap-1">
                    <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                      <Settings className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}
