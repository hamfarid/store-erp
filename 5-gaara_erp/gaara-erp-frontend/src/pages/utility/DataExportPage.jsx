/**
 * Data Export Page - صفحة تصدير البيانات
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Download,
  FileSpreadsheet,
  FileText,
  Database,
  Calendar,
  CheckCircle,
  Clock,
  RefreshCw,
  Settings,
} from 'lucide-react'

const exportModules = [
  { id: 'customers', name: 'العملاء', records: 1250, icon: '👥' },
  { id: 'products', name: 'المنتجات', records: 3500, icon: '📦' },
  { id: 'invoices', name: 'الفواتير', records: 8900, icon: '🧾' },
  { id: 'orders', name: 'الطلبات', records: 5600, icon: '📋' },
  { id: 'inventory', name: 'المخزون', records: 4200, icon: '🏪' },
  { id: 'transactions', name: 'المعاملات المالية', records: 12000, icon: '💰' },
]

const exportFormats = [
  { id: 'excel', name: 'Excel (.xlsx)', icon: FileSpreadsheet, color: 'emerald' },
  { id: 'csv', name: 'CSV (.csv)', icon: FileText, color: 'blue' },
  { id: 'json', name: 'JSON (.json)', icon: Database, color: 'purple' },
  { id: 'pdf', name: 'PDF (.pdf)', icon: FileText, color: 'red' },
]

const recentExports = [
  { id: 1, name: 'العملاء', format: 'Excel', date: '2026-01-17 10:30', status: 'completed', size: '2.5 MB' },
  { id: 2, name: 'الفواتير', format: 'PDF', date: '2026-01-16 15:20', status: 'completed', size: '15.8 MB' },
  { id: 3, name: 'المنتجات', format: 'CSV', date: '2026-01-15 09:00', status: 'completed', size: '1.2 MB' },
]

export default function DataExportPage() {
  const [selectedModules, setSelectedModules] = useState([])
  const [selectedFormat, setSelectedFormat] = useState('excel')
  const [dateRange, setDateRange] = useState({ from: '', to: '' })
  const [isExporting, setIsExporting] = useState(false)

  const toggleModule = (id) => {
    setSelectedModules(prev =>
      prev.includes(id)
        ? prev.filter(m => m !== id)
        : [...prev, id]
    )
  }

  const handleExport = async () => {
    if (selectedModules.length === 0) {
      toast.error('الرجاء اختيار وحدة واحدة على الأقل')
      return
    }
    setIsExporting(true)
    await new Promise(resolve => setTimeout(resolve, 2000))
    toast.success('تم تصدير البيانات بنجاح')
    setIsExporting(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6" dir="rtl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto space-y-6"
      >
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
              <Download className="w-8 h-8 text-emerald-400" />
              تصدير البيانات
            </h1>
            <p className="text-slate-400 mt-1">تصدير بيانات النظام بصيغ مختلفة</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Export Options */}
          <div className="lg:col-span-2 space-y-6">
            {/* Select Modules */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">اختر الوحدات</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {exportModules.map((module) => (
                  <motion.button
                    key={module.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => toggleModule(module.id)}
                    className={`p-4 rounded-xl border transition-all text-right ${
                      selectedModules.includes(module.id)
                        ? 'bg-emerald-500/20 border-emerald-500'
                        : 'bg-slate-700/50 border-slate-600 hover:border-slate-500'
                    }`}
                  >
                    <span className="text-2xl">{module.icon}</span>
                    <p className="text-white font-medium mt-2">{module.name}</p>
                    <p className="text-slate-400 text-sm">{module.records.toLocaleString()} سجل</p>
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Select Format */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">صيغة التصدير</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {exportFormats.map((format) => (
                  <button
                    key={format.id}
                    onClick={() => setSelectedFormat(format.id)}
                    className={`p-4 rounded-xl border transition-all ${
                      selectedFormat === format.id
                        ? `bg-${format.color}-500/20 border-${format.color}-500`
                        : 'bg-slate-700/50 border-slate-600 hover:border-slate-500'
                    }`}
                  >
                    <format.icon className={`w-8 h-8 mx-auto mb-2 text-${format.color}-400`} />
                    <p className="text-white text-sm">{format.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Date Range */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-blue-400" />
                نطاق التاريخ (اختياري)
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-300 text-sm mb-2">من تاريخ</label>
                  <input
                    type="date"
                    value={dateRange.from}
                    onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 text-sm mb-2">إلى تاريخ</label>
                  <input
                    type="date"
                    value={dateRange.to}
                    onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>
            </div>

            {/* Export Button */}
            <button
              onClick={handleExport}
              disabled={isExporting || selectedModules.length === 0}
              className="w-full py-4 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-700 text-white rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2"
            >
              {isExporting ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  جاري التصدير...
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  تصدير البيانات
                </>
              )}
            </button>
          </div>

          {/* Recent Exports */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6 h-fit">
            <h2 className="text-xl font-semibold text-white mb-4">التصديرات الأخيرة</h2>
            <div className="space-y-3">
              {recentExports.map((exp) => (
                <div
                  key={exp.id}
                  className="p-4 bg-slate-700/50 rounded-lg"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-medium">{exp.name}</span>
                    <span className="text-emerald-400 text-sm">{exp.format}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-400">{exp.date}</span>
                    <span className="text-slate-400">{exp.size}</span>
                  </div>
                  <button className="w-full mt-3 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg text-sm transition-colors flex items-center justify-center gap-2">
                    <Download className="w-4 h-4" />
                    تحميل
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
