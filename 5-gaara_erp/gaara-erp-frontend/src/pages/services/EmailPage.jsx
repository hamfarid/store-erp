/**
 * Email Service Page - صفحة خدمة البريد الإلكتروني
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Mail,
  Send,
  Inbox,
  Search,
  Plus,
  Settings,
  RefreshCw,
  Paperclip,
  Star,
  Trash2,
  Archive,
  Reply,
  Forward,
  Clock,
} from 'lucide-react'

const emails = [
  { id: 1, from: 'client@example.com', subject: 'استفسار عن المنتجات', preview: 'مرحباً، أود الاستفسار عن...', date: '10:30', read: false, starred: true },
  { id: 2, from: 'supplier@company.com', subject: 'تأكيد الطلب #1234', preview: 'تم تأكيد طلبكم بنجاح...', date: '09:15', read: true, starred: false },
  { id: 3, from: 'support@erp.com', subject: 'تحديث النظام', preview: 'يسعدنا إعلامكم بتوفر تحديث...', date: 'أمس', read: true, starred: false },
  { id: 4, from: 'hr@company.com', subject: 'إشعار الرواتب', preview: 'تم إيداع راتب شهر...', date: 'أمس', read: true, starred: true },
]

const templates = [
  { id: 1, name: 'ترحيب عميل جديد', category: 'عملاء' },
  { id: 2, name: 'تأكيد الطلب', category: 'مبيعات' },
  { id: 3, name: 'تذكير بالدفع', category: 'محاسبة' },
  { id: 4, name: 'عرض سعر', category: 'مبيعات' },
]

export default function EmailPage() {
  const [selectedEmail, setSelectedEmail] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCompose, setShowCompose] = useState(false)
  const [newEmail, setNewEmail] = useState({ to: '', subject: '', body: '' })

  const handleSend = () => {
    if (!newEmail.to || !newEmail.subject) {
      toast.error('الرجاء تعبئة الحقول المطلوبة')
      return
    }
    toast.success('تم إرسال البريد بنجاح')
    setShowCompose(false)
    setNewEmail({ to: '', subject: '', body: '' })
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
              <Mail className="w-8 h-8 text-blue-400" />
              البريد الإلكتروني
            </h1>
            <p className="text-slate-400 mt-1">إدارة الرسائل والمراسلات</p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              <Settings className="w-4 h-4" />
              الإعدادات
            </button>
            <button
              onClick={() => setShowCompose(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              رسالة جديدة
            </button>
          </div>
        </div>

        <div className="flex gap-6">
          {/* Sidebar */}
          <div className="w-64 space-y-4">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4">
              <nav className="space-y-1">
                {[
                  { icon: Inbox, label: 'الوارد', count: 4, active: true },
                  { icon: Send, label: 'المرسل', count: 0 },
                  { icon: Star, label: 'المميز', count: 2 },
                  { icon: Archive, label: 'الأرشيف', count: 0 },
                  { icon: Trash2, label: 'المحذوف', count: 0 },
                ].map((item, i) => (
                  <button
                    key={i}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg transition-colors ${
                      item.active
                        ? 'bg-blue-600/20 text-blue-400'
                        : 'text-slate-400 hover:bg-slate-700 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <item.icon className="w-4 h-4" />
                      {item.label}
                    </div>
                    {item.count > 0 && (
                      <span className="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-full">
                        {item.count}
                      </span>
                    )}
                  </button>
                ))}
              </nav>
            </div>

            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4">
              <h3 className="text-white font-medium mb-3">القوالب</h3>
              <div className="space-y-2">
                {templates.map((template) => (
                  <button
                    key={template.id}
                    className="w-full text-right px-3 py-2 text-slate-400 hover:bg-slate-700 hover:text-white rounded-lg transition-colors text-sm"
                  >
                    {template.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            {/* Search */}
            <div className="p-4 border-b border-slate-700">
              <div className="relative">
                <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="البحث في البريد..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pr-12 pl-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Email List */}
            <div className="divide-y divide-slate-700">
              {emails.map((email) => (
                <button
                  key={email.id}
                  onClick={() => setSelectedEmail(email)}
                  className={`w-full text-right p-4 hover:bg-slate-700/50 transition-colors ${
                    !email.read ? 'bg-blue-500/5' : ''
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <button className={`${email.starred ? 'text-amber-400' : 'text-slate-500'}`}>
                      <Star className="w-4 h-4" />
                    </button>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className={`font-medium ${!email.read ? 'text-white' : 'text-slate-300'}`}>
                          {email.from}
                        </span>
                        <span className="text-slate-500 text-sm">{email.date}</span>
                      </div>
                      <p className={`font-medium mb-1 ${!email.read ? 'text-white' : 'text-slate-400'}`}>
                        {email.subject}
                      </p>
                      <p className="text-slate-500 text-sm truncate">{email.preview}</p>
                    </div>
                  </div>
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
              className="bg-slate-800 rounded-xl border border-slate-700 w-full max-w-2xl p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-4">رسالة جديدة</h2>
              <div className="space-y-4">
                <input
                  type="email"
                  placeholder="إلى..."
                  value={newEmail.to}
                  onChange={(e) => setNewEmail({ ...newEmail, to: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500"
                />
                <input
                  type="text"
                  placeholder="الموضوع..."
                  value={newEmail.subject}
                  onChange={(e) => setNewEmail({ ...newEmail, subject: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500"
                />
                <textarea
                  placeholder="نص الرسالة..."
                  rows={8}
                  value={newEmail.body}
                  onChange={(e) => setNewEmail({ ...newEmail, body: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 resize-none"
                />
                <div className="flex justify-between">
                  <button className="flex items-center gap-2 px-4 py-2 text-slate-400 hover:text-white transition-colors">
                    <Paperclip className="w-4 h-4" />
                    إرفاق ملف
                  </button>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowCompose(false)}
                      className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                    >
                      إلغاء
                    </button>
                    <button
                      onClick={handleSend}
                      className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                    >
                      <Send className="w-4 h-4" />
                      إرسال
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
