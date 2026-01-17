/**
 * SMS Service Page - صفحة خدمة الرسائل النصية
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  MessageSquare,
  Send,
  Users,
  Search,
  Plus,
  Settings,
  RefreshCw,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  BarChart3,
} from 'lucide-react'

const messages = [
  { id: 1, to: '+966501234567', content: 'تم شحن طلبك #1234 بنجاح', status: 'delivered', date: '10:30' },
  { id: 2, to: '+966509876543', content: 'تذكير: موعد الدفع غداً', status: 'sent', date: '09:15' },
  { id: 3, to: '+966502345678', content: 'رمز التحقق: 123456', status: 'failed', date: 'أمس' },
  { id: 4, to: '+966503456789', content: 'مرحباً بك في متجرنا', status: 'delivered', date: 'أمس' },
]

const templates = [
  { id: 1, name: 'تأكيد الطلب', content: 'تم تأكيد طلبك #{order_id} بنجاح' },
  { id: 2, name: 'إشعار الشحن', content: 'تم شحن طلبك #{order_id}. رقم التتبع: {tracking}' },
  { id: 3, name: 'تذكير الدفع', content: 'تذكير: مبلغ {amount} مستحق في {date}' },
  { id: 4, name: 'رمز التحقق', content: 'رمز التحقق الخاص بك: {code}' },
]

const statusConfig = {
  delivered: { icon: CheckCircle, color: 'emerald', label: 'تم التسليم' },
  sent: { icon: Clock, color: 'blue', label: 'أُرسل' },
  failed: { icon: XCircle, color: 'red', label: 'فشل' },
  pending: { icon: AlertTriangle, color: 'amber', label: 'قيد الانتظار' },
}

export default function SMSPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showCompose, setShowCompose] = useState(false)
  const [newSMS, setNewSMS] = useState({ to: '', content: '' })
  const [selectedTemplate, setSelectedTemplate] = useState(null)

  const handleSend = () => {
    if (!newSMS.to || !newSMS.content) {
      toast.error('الرجاء تعبئة الحقول المطلوبة')
      return
    }
    toast.success('تم إرسال الرسالة بنجاح')
    setShowCompose(false)
    setNewSMS({ to: '', content: '' })
  }

  const stats = [
    { label: 'الرسائل اليوم', value: 156, icon: MessageSquare, color: 'blue' },
    { label: 'تم التسليم', value: 142, icon: CheckCircle, color: 'emerald' },
    { label: 'فشل', value: 8, icon: XCircle, color: 'red' },
    { label: 'الرصيد المتبقي', value: '2,450', icon: BarChart3, color: 'purple' },
  ]

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
              <MessageSquare className="w-8 h-8 text-green-400" />
              الرسائل النصية SMS
            </h1>
            <p className="text-slate-400 mt-1">إدارة وإرسال الرسائل النصية</p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              <Settings className="w-4 h-4" />
              الإعدادات
            </button>
            <button
              onClick={() => setShowCompose(true)}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              رسالة جديدة
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
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
          {/* Messages List */}
          <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <div className="p-4 border-b border-slate-700">
              <div className="relative">
                <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="البحث في الرسائل..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pr-12 pl-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>

            <div className="divide-y divide-slate-700">
              {messages.map((msg) => {
                const { icon: StatusIcon, color, label } = statusConfig[msg.status]
                return (
                  <div key={msg.id} className="p-4 hover:bg-slate-700/30 transition-colors">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white font-medium">{msg.to}</span>
                      <div className="flex items-center gap-2">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-${color}-500/20 text-${color}-400`}>
                          <StatusIcon className="w-3 h-3" />
                          {label}
                        </span>
                        <span className="text-slate-500 text-sm">{msg.date}</span>
                      </div>
                    </div>
                    <p className="text-slate-400 text-sm">{msg.content}</p>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Templates */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4">
            <h2 className="text-lg font-semibold text-white mb-4">القوالب الجاهزة</h2>
            <div className="space-y-3">
              {templates.map((template) => (
                <button
                  key={template.id}
                  onClick={() => {
                    setNewSMS({ ...newSMS, content: template.content })
                    setShowCompose(true)
                  }}
                  className="w-full text-right p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors"
                >
                  <p className="text-white font-medium mb-1">{template.name}</p>
                  <p className="text-slate-400 text-sm line-clamp-2">{template.content}</p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Compose Modal */}
        {showCompose && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setShowCompose(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-slate-800 rounded-xl border border-slate-700 w-full max-w-md p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-4">رسالة جديدة</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-slate-300 text-sm mb-2">رقم الهاتف</label>
                  <input
                    type="tel"
                    placeholder="+966..."
                    value={newSMS.to}
                    onChange={(e) => setNewSMS({ ...newSMS, to: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 text-sm mb-2">نص الرسالة</label>
                  <textarea
                    placeholder="اكتب رسالتك هنا..."
                    rows={4}
                    value={newSMS.content}
                    onChange={(e) => setNewSMS({ ...newSMS, content: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-green-500 resize-none"
                  />
                  <p className="text-slate-500 text-xs mt-1">{newSMS.content.length}/160 حرف</p>
                </div>
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setShowCompose(false)}
                    className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                  >
                    إلغاء
                  </button>
                  <button
                    onClick={handleSend}
                    className="flex items-center gap-2 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                  >
                    <Send className="w-4 h-4" />
                    إرسال
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
