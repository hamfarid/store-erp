/**
 * Cache Management Page - صفحة إدارة ذاكرة التخزين المؤقت
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Database,
  Trash2,
  RefreshCw,
  HardDrive,
  Activity,
  Clock,
  AlertTriangle,
  CheckCircle,
  Settings,
} from 'lucide-react'

const cacheCategories = [
  { id: 'api', name: 'ذاكرة API', size: '256 MB', hits: 15420, misses: 320, ratio: 98 },
  { id: 'session', name: 'جلسات المستخدمين', size: '64 MB', hits: 8500, misses: 150, ratio: 98 },
  { id: 'query', name: 'استعلامات قاعدة البيانات', size: '512 MB', hits: 45600, misses: 2400, ratio: 95 },
  { id: 'static', name: 'الملفات الثابتة', size: '1.2 GB', hits: 98000, misses: 500, ratio: 99 },
  { id: 'template', name: 'القوالب', size: '32 MB', hits: 5200, misses: 80, ratio: 98 },
]

const cacheStats = [
  { label: 'الحجم الكلي', value: '2.1 GB', max: '4 GB', color: 'blue' },
  { label: 'نسبة الإصابة', value: '97.2%', color: 'emerald' },
  { label: 'الطلبات/ثانية', value: '1,250', color: 'purple' },
  { label: 'وقت الاستجابة', value: '12ms', color: 'amber' },
]

export default function CachePage() {
  const [isClearing, setIsClearing] = useState({})
  const [autoRefresh, setAutoRefresh] = useState(true)

  const clearCache = async (id) => {
    setIsClearing({ ...isClearing, [id]: true })
    await new Promise(resolve => setTimeout(resolve, 1500))
    toast.success(`تم مسح ${cacheCategories.find(c => c.id === id)?.name}`)
    setIsClearing({ ...isClearing, [id]: false })
  }

  const clearAllCache = async () => {
    setIsClearing({ all: true })
    await new Promise(resolve => setTimeout(resolve, 2000))
    toast.success('تم مسح جميع ذاكرة التخزين المؤقت')
    setIsClearing({ all: false })
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
              <Database className="w-8 h-8 text-cyan-400" />
              إدارة ذاكرة التخزين المؤقت
            </h1>
            <p className="text-slate-400 mt-1">مراقبة وإدارة Cache النظام</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                autoRefresh
                  ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                  : 'bg-slate-700 hover:bg-slate-600 text-white'
              }`}
            >
              <RefreshCw className={`w-4 h-4 ${autoRefresh ? 'animate-spin' : ''}`} />
              تحديث تلقائي
            </button>
            <button
              onClick={clearAllCache}
              disabled={isClearing.all}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-800 text-white rounded-lg transition-colors"
            >
              {isClearing.all ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                <Trash2 className="w-4 h-4" />
              )}
              مسح الكل
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {cacheStats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4"
            >
              <p className="text-slate-400 text-sm">{stat.label}</p>
              <p className={`text-2xl font-bold text-${stat.color}-400 mt-1`}>{stat.value}</p>
              {stat.max && (
                <p className="text-slate-500 text-xs mt-1">من {stat.max}</p>
              )}
            </motion.div>
          ))}
        </div>

        {/* Usage Bar */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-blue-400" />
              استخدام الذاكرة
            </h2>
            <span className="text-slate-400">2.1 GB / 4 GB</span>
          </div>
          <div className="h-4 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
              style={{ width: '52.5%' }}
            />
          </div>
          <div className="flex justify-between mt-2 text-sm">
            <span className="text-slate-400">52.5% مستخدم</span>
            <span className="text-emerald-400">1.9 GB متاح</span>
          </div>
        </div>

        {/* Cache Categories */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <div className="p-4 border-b border-slate-700">
            <h2 className="text-xl font-semibold text-white">فئات الذاكرة المؤقتة</h2>
          </div>
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-right text-slate-400 font-medium p-4">الفئة</th>
                <th className="text-right text-slate-400 font-medium p-4">الحجم</th>
                <th className="text-right text-slate-400 font-medium p-4">الإصابات</th>
                <th className="text-right text-slate-400 font-medium p-4">الأخطاء</th>
                <th className="text-right text-slate-400 font-medium p-4">النسبة</th>
                <th className="text-right text-slate-400 font-medium p-4">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              {cacheCategories.map((cache, index) => (
                <motion.tr
                  key={cache.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                >
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Database className="w-4 h-4 text-cyan-400" />
                      <span className="text-white font-medium">{cache.name}</span>
                    </div>
                  </td>
                  <td className="p-4 text-slate-300">{cache.size}</td>
                  <td className="p-4 text-emerald-400">{cache.hits.toLocaleString()}</td>
                  <td className="p-4 text-red-400">{cache.misses.toLocaleString()}</td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            cache.ratio >= 95 ? 'bg-emerald-500' : cache.ratio >= 80 ? 'bg-amber-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${cache.ratio}%` }}
                        />
                      </div>
                      <span className="text-slate-300 text-sm">{cache.ratio}%</span>
                    </div>
                  </td>
                  <td className="p-4">
                    <div className="flex gap-1">
                      <button
                        onClick={() => clearCache(cache.id)}
                        disabled={isClearing[cache.id]}
                        className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                      >
                        {isClearing[cache.id] ? (
                          <RefreshCw className="w-4 h-4 animate-spin" />
                        ) : (
                          <Trash2 className="w-4 h-4" />
                        )}
                      </button>
                      <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                        <Settings className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  )
}
