/**
 * Business Reports Page - صفحة تقارير الأعمال
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import {
  FileText,
  Download,
  Calendar,
  Filter,
  TrendingUp,
  DollarSign,
  Package,
  Users,
  RefreshCw,
  Eye,
  Printer,
  Mail,
} from 'lucide-react'

const reportTypes = [
  { id: 'sales', name: 'تقرير المبيعات', icon: TrendingUp, color: 'emerald' },
  { id: 'purchases', name: 'تقرير المشتريات', icon: Package, color: 'blue' },
  { id: 'inventory', name: 'تقرير المخزون', icon: Package, color: 'amber' },
  { id: 'financial', name: 'التقرير المالي', icon: DollarSign, color: 'purple' },
  { id: 'customers', name: 'تقرير العملاء', icon: Users, color: 'pink' },
  { id: 'suppliers', name: 'تقرير الموردين', icon: Users, color: 'cyan' },
]

const recentReports = [
  { id: 1, name: 'تقرير المبيعات الشهري', type: 'sales', date: '2026-01-15', status: 'ready' },
  { id: 2, name: 'تقرير المخزون', type: 'inventory', date: '2026-01-14', status: 'ready' },
  { id: 3, name: 'التقرير المالي الربعي', type: 'financial', date: '2026-01-10', status: 'processing' },
]

export default function BusinessReportsPage() {
  const [selectedType, setSelectedType] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const { register, handleSubmit } = useForm()

  const onGenerate = async (data) => {
    setIsGenerating(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 2000))
      toast.success('تم إنشاء التقرير بنجاح')
    } catch {
      toast.error('فشل في إنشاء التقرير')
    } finally {
      setIsGenerating(false)
    }
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
              <FileText className="w-8 h-8 text-emerald-400" />
              تقارير الأعمال
            </h1>
            <p className="text-slate-400 mt-1">إنشاء وإدارة تقارير الأعمال</p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors">
            <RefreshCw className="w-4 h-4" />
            تحديث
          </button>
        </div>

        {/* Report Types Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {reportTypes.map((type) => (
            <motion.button
              key={type.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelectedType(type.id)}
              className={`p-4 rounded-xl border transition-all ${
                selectedType === type.id
                  ? `bg-${type.color}-500/20 border-${type.color}-500`
                  : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'
              }`}
            >
              <type.icon className={`w-8 h-8 mx-auto mb-2 text-${type.color}-400`} />
              <p className="text-white text-sm font-medium">{type.name}</p>
            </motion.button>
          ))}
        </div>

        {/* Report Generator */}
        <div className="grid lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6"
          >
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Filter className="w-5 h-5 text-blue-400" />
              إنشاء تقرير جديد
            </h2>
            <form onSubmit={handleSubmit(onGenerate)} className="space-y-4">
              <div>
                <label className="block text-slate-300 text-sm mb-2">نوع التقرير</label>
                <select
                  {...register('type')}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                >
                  {reportTypes.map(t => (
                    <option key={t.id} value={t.id}>{t.name}</option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-300 text-sm mb-2">من تاريخ</label>
                  <input
                    type="date"
                    {...register('fromDate')}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 text-sm mb-2">إلى تاريخ</label>
                  <input
                    type="date"
                    {...register('toDate')}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-slate-300 text-sm mb-2">صيغة التقرير</label>
                <select
                  {...register('format')}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="pdf">PDF</option>
                  <option value="excel">Excel</option>
                  <option value="csv">CSV</option>
                </select>
              </div>
              <button
                type="submit"
                disabled={isGenerating}
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-800 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <RefreshCw className="w-5 h-5 animate-spin" />
                ) : (
                  <FileText className="w-5 h-5" />
                )}
                {isGenerating ? 'جاري الإنشاء...' : 'إنشاء التقرير'}
              </button>
            </form>
          </motion.div>

          {/* Recent Reports */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6"
          >
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-purple-400" />
              التقارير الأخيرة
            </h2>
            <div className="space-y-3">
              {recentReports.map((report) => (
                <div
                  key={report.id}
                  className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg"
                >
                  <div>
                    <p className="text-white font-medium">{report.name}</p>
                    <p className="text-slate-400 text-sm">{report.date}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    {report.status === 'ready' ? (
                      <>
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-600 rounded-lg transition-colors">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-600 rounded-lg transition-colors">
                          <Download className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-600 rounded-lg transition-colors">
                          <Printer className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-600 rounded-lg transition-colors">
                          <Mail className="w-4 h-4" />
                        </button>
                      </>
                    ) : (
                      <span className="px-3 py-1 bg-amber-500/20 text-amber-400 rounded-full text-sm">
                        قيد المعالجة
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  )
}
