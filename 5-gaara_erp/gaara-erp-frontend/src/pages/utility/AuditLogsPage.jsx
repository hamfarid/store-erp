/**
 * Audit Logs Page - صفحة سجلات التدقيق
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  FileSearch,
  Search,
  Filter,
  Download,
  Calendar,
  User,
  Activity,
  Eye,
  Clock,
} from 'lucide-react'

const auditLogs = [
  { id: 1, action: 'تسجيل دخول', user: 'admin', module: 'المصادقة', ip: '192.168.1.100', timestamp: '2026-01-17 10:30:45', details: 'تسجيل دخول ناجح' },
  { id: 2, action: 'إنشاء فاتورة', user: 'محمد', module: 'المبيعات', ip: '192.168.1.101', timestamp: '2026-01-17 10:28:12', details: 'فاتورة #INV-2026-0045' },
  { id: 3, action: 'تعديل منتج', user: 'أحمد', module: 'المخزون', ip: '192.168.1.102', timestamp: '2026-01-17 10:25:00', details: 'تحديث سعر المنتج #PRD-001' },
  { id: 4, action: 'حذف عميل', user: 'admin', module: 'جهات الاتصال', ip: '192.168.1.100', timestamp: '2026-01-17 10:20:33', details: 'حذف العميل #CUS-050' },
  { id: 5, action: 'تصدير تقرير', user: 'سارة', module: 'التقارير', ip: '192.168.1.103', timestamp: '2026-01-17 10:15:00', details: 'تقرير المبيعات الشهري' },
  { id: 6, action: 'تغيير صلاحيات', user: 'admin', module: 'إدارة المستخدمين', ip: '192.168.1.100', timestamp: '2026-01-17 10:10:00', details: 'تعديل صلاحيات المستخدم محمد' },
]

const actionColors = {
  'تسجيل دخول': 'blue',
  'إنشاء': 'emerald',
  'تعديل': 'amber',
  'حذف': 'red',
  'تصدير': 'purple',
  'تغيير': 'cyan',
}

export default function AuditLogsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [dateFilter, setDateFilter] = useState('')
  const [selectedLog, setSelectedLog] = useState(null)

  const filteredLogs = auditLogs.filter(log =>
    log.action.includes(searchTerm) ||
    log.user.includes(searchTerm) ||
    log.module.includes(searchTerm)
  )

  const getActionColor = (action) => {
    for (const [key, color] of Object.entries(actionColors)) {
      if (action.includes(key)) return color
    }
    return 'slate'
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
              <FileSearch className="w-8 h-8 text-indigo-400" />
              سجلات التدقيق
            </h1>
            <p className="text-slate-400 mt-1">تتبع جميع الإجراءات والتغييرات في النظام</p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors">
            <Download className="w-4 h-4" />
            تصدير السجلات
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'إجمالي السجلات', value: '12,450', icon: Activity, color: 'indigo' },
            { label: 'سجلات اليوم', value: '156', icon: Calendar, color: 'blue' },
            { label: 'المستخدمين النشطين', value: '24', icon: User, color: 'emerald' },
            { label: 'الوحدات المراقبة', value: '18', icon: Eye, color: 'purple' },
          ].map((stat, i) => (
            <div
              key={i}
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
            </div>
          ))}
        </div>

        {/* Search & Filters */}
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="البحث في السجلات..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <input
            type="date"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
            className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-indigo-500"
          />
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
            <Filter className="w-4 h-4" />
            فلاتر
          </button>
        </div>

        {/* Logs Table */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-right text-slate-400 font-medium p-4">الإجراء</th>
                <th className="text-right text-slate-400 font-medium p-4">المستخدم</th>
                <th className="text-right text-slate-400 font-medium p-4">الوحدة</th>
                <th className="text-right text-slate-400 font-medium p-4">عنوان IP</th>
                <th className="text-right text-slate-400 font-medium p-4">الوقت</th>
                <th className="text-right text-slate-400 font-medium p-4">التفاصيل</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log, index) => {
                const color = getActionColor(log.action)
                return (
                  <motion.tr
                    key={log.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors cursor-pointer"
                    onClick={() => setSelectedLog(log)}
                  >
                    <td className="p-4">
                      <span className={`px-3 py-1 rounded-full text-sm bg-${color}-500/20 text-${color}-400`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2 text-white">
                        <User className="w-4 h-4 text-slate-500" />
                        {log.user}
                      </div>
                    </td>
                    <td className="p-4 text-slate-300">{log.module}</td>
                    <td className="p-4 text-slate-400 font-mono text-sm">{log.ip}</td>
                    <td className="p-4">
                      <div className="flex items-center gap-2 text-slate-400 text-sm">
                        <Clock className="w-4 h-4" />
                        {log.timestamp}
                      </div>
                    </td>
                    <td className="p-4 text-slate-300 text-sm">{log.details}</td>
                  </motion.tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {/* Details Modal */}
        {selectedLog && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setSelectedLog(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-slate-800 rounded-xl border border-slate-700 w-full max-w-lg p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-4">تفاصيل السجل</h2>
              <div className="space-y-4">
                {[
                  { label: 'الإجراء', value: selectedLog.action },
                  { label: 'المستخدم', value: selectedLog.user },
                  { label: 'الوحدة', value: selectedLog.module },
                  { label: 'عنوان IP', value: selectedLog.ip },
                  { label: 'الوقت', value: selectedLog.timestamp },
                  { label: 'التفاصيل', value: selectedLog.details },
                ].map((item, i) => (
                  <div key={i} className="flex justify-between py-2 border-b border-slate-700">
                    <span className="text-slate-400">{item.label}</span>
                    <span className="text-white">{item.value}</span>
                  </div>
                ))}
              </div>
              <button
                onClick={() => setSelectedLog(null)}
                className="w-full mt-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
              >
                إغلاق
              </button>
            </motion.div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
