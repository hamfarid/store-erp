/**
 * Printing Service Page - صفحة خدمة الطباعة
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Printer,
  FileText,
  Search,
  Settings,
  RefreshCw,
  Clock,
  CheckCircle,
  XCircle,
  Pause,
  Play,
  Trash2,
  Download,
  Eye,
} from 'lucide-react'

const printJobs = [
  { id: 1, name: 'فاتورة #INV-2026-0045', printer: 'طابعة المكتب', pages: 2, status: 'completed', date: '10:30' },
  { id: 2, name: 'تقرير المبيعات الشهري', printer: 'طابعة المخزن', pages: 15, status: 'printing', date: '10:28' },
  { id: 3, name: 'قائمة المنتجات', printer: 'طابعة المكتب', pages: 8, status: 'queued', date: '10:25' },
  { id: 4, name: 'باركود المنتجات', printer: 'طابعة الباركود', pages: 50, status: 'paused', date: '10:20' },
  { id: 5, name: 'إيصال #RCP-001', printer: 'طابعة نقطة البيع', pages: 1, status: 'failed', date: '10:15' },
]

const printers = [
  { id: 1, name: 'طابعة المكتب', model: 'HP LaserJet Pro', status: 'online', queue: 2 },
  { id: 2, name: 'طابعة المخزن', model: 'Brother HL-L2350DW', status: 'online', queue: 1 },
  { id: 3, name: 'طابعة الباركود', model: 'Zebra ZD420', status: 'offline', queue: 0 },
  { id: 4, name: 'طابعة نقطة البيع', model: 'Epson TM-T88VI', status: 'error', queue: 0 },
]

const statusConfig = {
  completed: { icon: CheckCircle, color: 'emerald', label: 'مكتمل' },
  printing: { icon: Printer, color: 'blue', label: 'جاري الطباعة' },
  queued: { icon: Clock, color: 'amber', label: 'في الانتظار' },
  paused: { icon: Pause, color: 'slate', label: 'متوقف' },
  failed: { icon: XCircle, color: 'red', label: 'فشل' },
}

const printerStatus = {
  online: { color: 'emerald', label: 'متصل' },
  offline: { color: 'slate', label: 'غير متصل' },
  error: { color: 'red', label: 'خطأ' },
}

export default function PrintingPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPrinter, setSelectedPrinter] = useState('all')

  const filteredJobs = printJobs.filter(job => {
    const matchesSearch = job.name.includes(searchTerm)
    const matchesPrinter = selectedPrinter === 'all' || job.printer === selectedPrinter
    return matchesSearch && matchesPrinter
  })

  const handleCancel = (id) => {
    toast.success('تم إلغاء مهمة الطباعة')
  }

  const handleRetry = (id) => {
    toast.success('تم إعادة إرسال مهمة الطباعة')
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
              <Printer className="w-8 h-8 text-purple-400" />
              خدمة الطباعة
            </h1>
            <p className="text-slate-400 mt-1">إدارة مهام الطباعة والطابعات</p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
            <Settings className="w-4 h-4" />
            إعدادات الطابعات
          </button>
        </div>

        {/* Printers */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {printers.map((printer) => {
            const status = printerStatus[printer.status]
            return (
              <motion.div
                key={printer.id}
                whileHover={{ scale: 1.02 }}
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <Printer className={`w-6 h-6 text-${status.color}-400`} />
                  <span className={`px-2 py-0.5 rounded-full text-xs bg-${status.color}-500/20 text-${status.color}-400`}>
                    {status.label}
                  </span>
                </div>
                <h3 className="text-white font-medium">{printer.name}</h3>
                <p className="text-slate-400 text-sm">{printer.model}</p>
                <p className="text-slate-500 text-xs mt-2">
                  {printer.queue} مهام في الانتظار
                </p>
              </motion.div>
            )
          })}
        </div>

        {/* Search & Filter */}
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="البحث في مهام الطباعة..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <select
            value={selectedPrinter}
            onChange={(e) => setSelectedPrinter(e.target.value)}
            className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">جميع الطابعات</option>
            {printers.map(p => (
              <option key={p.id} value={p.name}>{p.name}</option>
            ))}
          </select>
        </div>

        {/* Print Jobs */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-right text-slate-400 font-medium p-4">المستند</th>
                <th className="text-right text-slate-400 font-medium p-4">الطابعة</th>
                <th className="text-right text-slate-400 font-medium p-4">الصفحات</th>
                <th className="text-right text-slate-400 font-medium p-4">الحالة</th>
                <th className="text-right text-slate-400 font-medium p-4">الوقت</th>
                <th className="text-right text-slate-400 font-medium p-4">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              {filteredJobs.map((job, index) => {
                const { icon: StatusIcon, color, label } = statusConfig[job.status]
                return (
                  <motion.tr
                    key={job.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                  >
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-slate-400" />
                        <span className="text-white">{job.name}</span>
                      </div>
                    </td>
                    <td className="p-4 text-slate-300">{job.printer}</td>
                    <td className="p-4 text-slate-300">{job.pages}</td>
                    <td className="p-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-${color}-500/20 text-${color}-400`}>
                        <StatusIcon className="w-3 h-3" />
                        {label}
                      </span>
                    </td>
                    <td className="p-4 text-slate-400">{job.date}</td>
                    <td className="p-4">
                      <div className="flex gap-1">
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                          <Eye className="w-4 h-4" />
                        </button>
                        {job.status === 'paused' && (
                          <button className="p-2 text-emerald-400 hover:bg-emerald-500/20 rounded-lg transition-colors">
                            <Play className="w-4 h-4" />
                          </button>
                        )}
                        {job.status === 'printing' && (
                          <button className="p-2 text-amber-400 hover:bg-amber-500/20 rounded-lg transition-colors">
                            <Pause className="w-4 h-4" />
                          </button>
                        )}
                        {job.status === 'failed' && (
                          <button
                            onClick={() => handleRetry(job.id)}
                            className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                          >
                            <RefreshCw className="w-4 h-4" />
                          </button>
                        )}
                        {['queued', 'paused'].includes(job.status) && (
                          <button
                            onClick={() => handleCancel(job.id)}
                            className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </motion.tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  )
}
