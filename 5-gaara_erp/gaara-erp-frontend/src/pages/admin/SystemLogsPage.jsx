/**
 * System Logs Page - صفحة سجلات النظام
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  ScrollText,
  Search,
  Filter,
  Download,
  RefreshCw,
  AlertTriangle,
  Info,
  AlertCircle,
  CheckCircle,
  Clock,
  User,
  Monitor,
} from 'lucide-react'

const logLevels = {
  info: { icon: Info, color: 'blue', label: 'معلومات' },
  success: { icon: CheckCircle, color: 'emerald', label: 'نجاح' },
  warning: { icon: AlertTriangle, color: 'amber', label: 'تحذير' },
  error: { icon: AlertCircle, color: 'red', label: 'خطأ' },
}

const logs = [
  { id: 1, level: 'info', message: 'تسجيل دخول مستخدم جديد', user: 'admin', timestamp: '2026-01-17 10:30:45', module: 'auth' },
  { id: 2, level: 'success', message: 'تم إنشاء فاتورة جديدة #INV-2026-0045', user: 'محمد', timestamp: '2026-01-17 10:28:12', module: 'sales' },
  { id: 3, level: 'warning', message: 'محاولة تسجيل دخول فاشلة', user: 'unknown', timestamp: '2026-01-17 10:25:00', module: 'security' },
  { id: 4, level: 'error', message: 'فشل في الاتصال بقاعدة البيانات', user: 'system', timestamp: '2026-01-17 10:20:33', module: 'database' },
  { id: 5, level: 'info', message: 'تم تحديث إعدادات النظام', user: 'admin', timestamp: '2026-01-17 10:15:00', module: 'settings' },
  { id: 6, level: 'success', message: 'النسخ الاحتياطي اليومي مكتمل', user: 'system', timestamp: '2026-01-17 03:00:00', module: 'backup' },
  { id: 7, level: 'warning', message: 'ذاكرة التخزين المؤقت ممتلئة بنسبة 85%', user: 'system', timestamp: '2026-01-17 02:45:00', module: 'cache' },
  { id: 8, level: 'info', message: 'تم إضافة منتج جديد إلى المخزون', user: 'سارة', timestamp: '2026-01-16 18:30:00', module: 'inventory' },
]

export default function SystemLogsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedLevel, setSelectedLevel] = useState('all')
  const [isRefreshing, setIsRefreshing] = useState(false)

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.includes(searchTerm) || log.user.includes(searchTerm)
    const matchesLevel = selectedLevel === 'all' || log.level === selectedLevel
    return matchesSearch && matchesLevel
  })

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsRefreshing(false)
  }

  const levelCounts = logs.reduce((acc, log) => {
    acc[log.level] = (acc[log.level] || 0) + 1
    return acc
  }, {})

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
              <ScrollText className="w-8 h-8 text-purple-400" />
              سجلات النظام
            </h1>
            <p className="text-slate-400 mt-1">مراقبة وتتبع جميع أحداث النظام</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleRefresh}
              className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              تحديث
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors">
              <Download className="w-4 h-4" />
              تصدير
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(logLevels).map(([key, { icon: Icon, color, label }]) => (
            <motion.button
              key={key}
              whileHover={{ scale: 1.02 }}
              onClick={() => setSelectedLevel(selectedLevel === key ? 'all' : key)}
              className={`p-4 rounded-xl border transition-all ${
                selectedLevel === key
                  ? `bg-${color}-500/20 border-${color}-500`
                  : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg bg-${color}-500/20`}>
                    <Icon className={`w-5 h-5 text-${color}-400`} />
                  </div>
                  <span className="text-slate-300">{label}</span>
                </div>
                <span className="text-2xl font-bold text-white">{levelCounts[key] || 0}</span>
              </div>
            </motion.button>
          ))}
        </div>

        {/* Search & Filter */}
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="البحث في السجلات..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
            <Filter className="w-4 h-4" />
            فلاتر متقدمة
          </button>
        </div>

        {/* Logs Table */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-right text-slate-400 font-medium p-4">المستوى</th>
                  <th className="text-right text-slate-400 font-medium p-4">الرسالة</th>
                  <th className="text-right text-slate-400 font-medium p-4">المستخدم</th>
                  <th className="text-right text-slate-400 font-medium p-4">الوحدة</th>
                  <th className="text-right text-slate-400 font-medium p-4">الوقت</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.map((log, index) => {
                  const { icon: Icon, color } = logLevels[log.level]
                  return (
                    <motion.tr
                      key={log.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                    >
                      <td className="p-4">
                        <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full bg-${color}-500/20 text-${color}-400 text-sm`}>
                          <Icon className="w-4 h-4" />
                          {logLevels[log.level].label}
                        </span>
                      </td>
                      <td className="p-4 text-white">{log.message}</td>
                      <td className="p-4">
                        <div className="flex items-center gap-2 text-slate-300">
                          <User className="w-4 h-4 text-slate-500" />
                          {log.user}
                        </div>
                      </td>
                      <td className="p-4">
                        <span className="px-2 py-1 bg-slate-700 rounded text-slate-300 text-sm">
                          {log.module}
                        </span>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2 text-slate-400 text-sm">
                          <Clock className="w-4 h-4" />
                          {log.timestamp}
                        </div>
                      </td>
                    </motion.tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
