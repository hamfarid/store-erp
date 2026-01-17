/**
 * Task Scheduler Page - صفحة جدولة المهام
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Calendar,
  Clock,
  Plus,
  Search,
  Settings,
  Play,
  Pause,
  Trash2,
  Edit,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RefreshCw,
  Timer,
} from 'lucide-react'

const scheduledTasks = [
  { id: 1, name: 'النسخ الاحتياطي اليومي', schedule: '03:00 يومياً', lastRun: '2026-01-17 03:00', nextRun: '2026-01-18 03:00', status: 'active' },
  { id: 2, name: 'تقرير المبيعات الأسبوعي', schedule: 'الأحد 08:00', lastRun: '2026-01-12 08:00', nextRun: '2026-01-19 08:00', status: 'active' },
  { id: 3, name: 'تنظيف السجلات القديمة', schedule: '01:00 يومياً', lastRun: '2026-01-17 01:00', nextRun: '2026-01-18 01:00', status: 'active' },
  { id: 4, name: 'إرسال تذكيرات الدفع', schedule: '09:00 يومياً', lastRun: '2026-01-17 09:00', nextRun: '2026-01-18 09:00', status: 'paused' },
  { id: 5, name: 'تحديث أسعار الصرف', schedule: 'كل 6 ساعات', lastRun: '2026-01-17 06:00', nextRun: '2026-01-17 12:00', status: 'error' },
]

const statusConfig = {
  active: { icon: CheckCircle, color: 'emerald', label: 'نشط' },
  paused: { icon: Pause, color: 'amber', label: 'متوقف' },
  error: { icon: XCircle, color: 'red', label: 'خطأ' },
  running: { icon: RefreshCw, color: 'blue', label: 'قيد التنفيذ' },
}

const scheduleOptions = [
  { id: 'minutely', label: 'كل دقيقة' },
  { id: 'hourly', label: 'كل ساعة' },
  { id: 'daily', label: 'يومياً' },
  { id: 'weekly', label: 'أسبوعياً' },
  { id: 'monthly', label: 'شهرياً' },
  { id: 'custom', label: 'مخصص' },
]

export default function SchedulerPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [tasks, setTasks] = useState(scheduledTasks)
  const [newTask, setNewTask] = useState({ name: '', schedule: 'daily', time: '00:00' })

  const filteredTasks = tasks.filter(task =>
    task.name.includes(searchTerm)
  )

  const toggleTask = (id) => {
    setTasks(tasks.map(t => {
      if (t.id === id) {
        const newStatus = t.status === 'active' ? 'paused' : 'active'
        toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'إيقاف'} المهمة`)
        return { ...t, status: newStatus }
      }
      return t
    }))
  }

  const runNow = (id) => {
    toast.success('تم بدء تنفيذ المهمة')
  }

  const deleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id))
    toast.success('تم حذف المهمة')
  }

  const handleAddTask = () => {
    if (!newTask.name) {
      toast.error('الرجاء إدخال اسم المهمة')
      return
    }
    const task = {
      id: Date.now(),
      name: newTask.name,
      schedule: `${newTask.time} ${scheduleOptions.find(s => s.id === newTask.schedule)?.label}`,
      lastRun: '-',
      nextRun: 'قريباً',
      status: 'active',
    }
    setTasks([...tasks, task])
    setShowAddModal(false)
    setNewTask({ name: '', schedule: 'daily', time: '00:00' })
    toast.success('تم إضافة المهمة بنجاح')
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
              <Calendar className="w-8 h-8 text-amber-400" />
              جدولة المهام
            </h1>
            <p className="text-slate-400 mt-1">إدارة المهام المجدولة تلقائياً</p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            مهمة جديدة
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'إجمالي المهام', value: tasks.length, icon: Calendar, color: 'amber' },
            { label: 'مهام نشطة', value: tasks.filter(t => t.status === 'active').length, icon: CheckCircle, color: 'emerald' },
            { label: 'مهام متوقفة', value: tasks.filter(t => t.status === 'paused').length, icon: Pause, color: 'slate' },
            { label: 'مهام بها أخطاء', value: tasks.filter(t => t.status === 'error').length, icon: AlertTriangle, color: 'red' },
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

        {/* Search */}
        <div className="relative">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="البحث في المهام..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-amber-500"
          />
        </div>

        {/* Tasks List */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-right text-slate-400 font-medium p-4">المهمة</th>
                <th className="text-right text-slate-400 font-medium p-4">الجدول</th>
                <th className="text-right text-slate-400 font-medium p-4">آخر تنفيذ</th>
                <th className="text-right text-slate-400 font-medium p-4">التنفيذ القادم</th>
                <th className="text-right text-slate-400 font-medium p-4">الحالة</th>
                <th className="text-right text-slate-400 font-medium p-4">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              {filteredTasks.map((task, index) => {
                const { icon: StatusIcon, color, label } = statusConfig[task.status]
                return (
                  <motion.tr
                    key={task.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                  >
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <Timer className="w-4 h-4 text-slate-400" />
                        <span className="text-white font-medium">{task.name}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2 text-slate-300">
                        <Clock className="w-4 h-4 text-slate-500" />
                        {task.schedule}
                      </div>
                    </td>
                    <td className="p-4 text-slate-400">{task.lastRun}</td>
                    <td className="p-4 text-slate-300">{task.nextRun}</td>
                    <td className="p-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-${color}-500/20 text-${color}-400`}>
                        <StatusIcon className="w-3 h-3" />
                        {label}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-1">
                        <button
                          onClick={() => runNow(task.id)}
                          className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                          title="تنفيذ الآن"
                        >
                          <Play className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => toggleTask(task.id)}
                          className={`p-2 rounded-lg transition-colors ${
                            task.status === 'active'
                              ? 'text-amber-400 hover:bg-amber-500/20'
                              : 'text-emerald-400 hover:bg-emerald-500/20'
                          }`}
                          title={task.status === 'active' ? 'إيقاف' : 'تفعيل'}
                        >
                          {task.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                        </button>
                        <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => deleteTask(task.id)}
                          className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </motion.tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {/* Add Task Modal */}
        {showAddModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setShowAddModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-slate-800 rounded-xl border border-slate-700 w-full max-w-md p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-4">إضافة مهمة مجدولة</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-slate-300 text-sm mb-2">اسم المهمة</label>
                  <input
                    type="text"
                    value={newTask.name}
                    onChange={(e) => setNewTask({ ...newTask, name: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-amber-500"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-300 text-sm mb-2">التكرار</label>
                    <select
                      value={newTask.schedule}
                      onChange={(e) => setNewTask({ ...newTask, schedule: e.target.value })}
                      className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-amber-500"
                    >
                      {scheduleOptions.map(opt => (
                        <option key={opt.id} value={opt.id}>{opt.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-300 text-sm mb-2">الوقت</label>
                    <input
                      type="time"
                      value={newTask.time}
                      onChange={(e) => setNewTask({ ...newTask, time: e.target.value })}
                      className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-amber-500"
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-2 pt-4">
                  <button
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                  >
                    إلغاء
                  </button>
                  <button
                    onClick={handleAddTask}
                    className="px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg transition-colors"
                  >
                    إضافة
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
