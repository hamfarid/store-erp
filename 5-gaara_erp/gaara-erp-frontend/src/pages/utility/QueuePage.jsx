/**
 * Queue Management Page - صفحة إدارة قوائم الانتظار
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  ListOrdered,
  Play,
  Pause,
  Trash2,
  RefreshCw,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Activity,
  Zap,
  Settings,
} from 'lucide-react'

const queues = [
  { id: 'email', name: 'البريد الإلكتروني', pending: 45, processing: 3, failed: 2, completed: 1250, status: 'active' },
  { id: 'sms', name: 'الرسائل النصية', pending: 12, processing: 1, failed: 0, completed: 890, status: 'active' },
  { id: 'notifications', name: 'الإشعارات', pending: 156, processing: 5, failed: 8, completed: 5600, status: 'active' },
  { id: 'reports', name: 'التقارير', pending: 3, processing: 1, failed: 0, completed: 234, status: 'active' },
  { id: 'imports', name: 'الاستيراد', pending: 0, processing: 0, failed: 1, completed: 56, status: 'paused' },
  { id: 'exports', name: 'التصدير', pending: 2, processing: 0, failed: 0, completed: 89, status: 'active' },
]

const recentJobs = [
  { id: 1, queue: 'البريد', job: 'إرسال فاتورة #INV-001', status: 'completed', time: '10:30' },
  { id: 2, queue: 'الإشعارات', job: 'إشعار طلب جديد', status: 'processing', time: '10:29' },
  { id: 3, queue: 'التقارير', job: 'تقرير المبيعات الشهري', status: 'pending', time: '10:28' },
  { id: 4, queue: 'البريد', job: 'تذكير بالدفع', status: 'failed', time: '10:25' },
]

const statusConfig = {
  completed: { icon: CheckCircle, color: 'emerald', label: 'مكتمل' },
  processing: { icon: RefreshCw, color: 'blue', label: 'قيد التنفيذ' },
  pending: { icon: Clock, color: 'amber', label: 'في الانتظار' },
  failed: { icon: XCircle, color: 'red', label: 'فاشل' },
}

export default function QueuePage() {
  const [queueList, setQueueList] = useState(queues)
  const [selectedQueue, setSelectedQueue] = useState(null)

  const toggleQueue = (id) => {
    setQueueList(queueList.map(q => {
      if (q.id === id) {
        const newStatus = q.status === 'active' ? 'paused' : 'active'
        toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'إيقاف'} قائمة ${q.name}`)
        return { ...q, status: newStatus }
      }
      return q
    }))
  }

  const clearQueue = (id) => {
    setQueueList(queueList.map(q => {
      if (q.id === id) {
        toast.success(`تم مسح المهام المعلقة في ${q.name}`)
        return { ...q, pending: 0 }
      }
      return q
    }))
  }

  const retryFailed = (id) => {
    setQueueList(queueList.map(q => {
      if (q.id === id) {
        toast.success(`تم إعادة المهام الفاشلة في ${q.name}`)
        return { ...q, failed: 0, pending: q.pending + q.failed }
      }
      return q
    }))
  }

  const totalPending = queueList.reduce((sum, q) => sum + q.pending, 0)
  const totalProcessing = queueList.reduce((sum, q) => sum + q.processing, 0)
  const totalFailed = queueList.reduce((sum, q) => sum + q.failed, 0)
  const totalCompleted = queueList.reduce((sum, q) => sum + q.completed, 0)

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
              <ListOrdered className="w-8 h-8 text-purple-400" />
              إدارة قوائم الانتظار
            </h1>
            <p className="text-slate-400 mt-1">مراقبة وإدارة مهام الخلفية</p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
            <Settings className="w-4 h-4" />
            الإعدادات
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'في الانتظار', value: totalPending, icon: Clock, color: 'amber' },
            { label: 'قيد التنفيذ', value: totalProcessing, icon: Activity, color: 'blue' },
            { label: 'فاشل', value: totalFailed, icon: AlertTriangle, color: 'red' },
            { label: 'مكتمل', value: totalCompleted.toLocaleString(), icon: CheckCircle, color: 'emerald' },
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

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Queues */}
          <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700">
              <h2 className="text-xl font-semibold text-white">قوائم الانتظار</h2>
            </div>
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-right text-slate-400 font-medium p-4">القائمة</th>
                  <th className="text-right text-slate-400 font-medium p-4">معلق</th>
                  <th className="text-right text-slate-400 font-medium p-4">جاري</th>
                  <th className="text-right text-slate-400 font-medium p-4">فاشل</th>
                  <th className="text-right text-slate-400 font-medium p-4">الحالة</th>
                  <th className="text-right text-slate-400 font-medium p-4">إجراءات</th>
                </tr>
              </thead>
              <tbody>
                {queueList.map((queue, index) => (
                  <motion.tr
                    key={queue.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                  >
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <Zap className="w-4 h-4 text-purple-400" />
                        <span className="text-white font-medium">{queue.name}</span>
                      </div>
                    </td>
                    <td className="p-4 text-amber-400">{queue.pending}</td>
                    <td className="p-4 text-blue-400">{queue.processing}</td>
                    <td className="p-4 text-red-400">{queue.failed}</td>
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        queue.status === 'active'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-slate-500/20 text-slate-400'
                      }`}>
                        {queue.status === 'active' ? 'نشط' : 'متوقف'}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-1">
                        <button
                          onClick={() => toggleQueue(queue.id)}
                          className={`p-2 rounded-lg transition-colors ${
                            queue.status === 'active'
                              ? 'text-amber-400 hover:bg-amber-500/20'
                              : 'text-emerald-400 hover:bg-emerald-500/20'
                          }`}
                        >
                          {queue.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                        </button>
                        {queue.failed > 0 && (
                          <button
                            onClick={() => retryFailed(queue.id)}
                            className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                          >
                            <RefreshCw className="w-4 h-4" />
                          </button>
                        )}
                        {queue.pending > 0 && (
                          <button
                            onClick={() => clearQueue(queue.id)}
                            className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Recent Jobs */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4">
            <h2 className="text-lg font-semibold text-white mb-4">المهام الأخيرة</h2>
            <div className="space-y-3">
              {recentJobs.map((job) => {
                const { icon: StatusIcon, color, label } = statusConfig[job.status]
                return (
                  <div
                    key={job.id}
                    className="p-3 bg-slate-700/50 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-white text-sm font-medium truncate">{job.job}</span>
                      <StatusIcon className={`w-4 h-4 text-${color}-400 flex-shrink-0`} />
                    </div>
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">{job.queue}</span>
                      <span className="text-slate-500">{job.time}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
