/**
 * Security Settings Page - صفحة إعدادات الأمان
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Shield,
  Key,
  Lock,
  Smartphone,
  Globe,
  Clock,
  AlertTriangle,
  CheckCircle,
  Settings,
  Save,
  RefreshCw,
  Eye,
  EyeOff,
} from 'lucide-react'

const securityFeatures = [
  { id: 'twoFactor', name: 'المصادقة الثنائية', description: 'طلب رمز إضافي عند تسجيل الدخول', enabled: true },
  { id: 'sessionTimeout', name: 'انتهاء الجلسة التلقائي', description: 'إنهاء الجلسة بعد فترة من عدم النشاط', enabled: true },
  { id: 'ipRestriction', name: 'تقييد عناوين IP', description: 'السماح بالوصول من عناوين محددة فقط', enabled: false },
  { id: 'bruteForce', name: 'حماية من القوة الغاشمة', description: 'قفل الحساب بعد محاولات فاشلة متكررة', enabled: true },
  { id: 'auditLog', name: 'سجل التدقيق', description: 'تسجيل جميع الإجراءات الحساسة', enabled: true },
  { id: 'encryption', name: 'تشفير البيانات', description: 'تشفير البيانات الحساسة في قاعدة البيانات', enabled: true },
]

export default function SecuritySettingsPage() {
  const [features, setFeatures] = useState(securityFeatures)
  const [passwordPolicy, setPasswordPolicy] = useState({
    minLength: 8,
    requireUppercase: true,
    requireLowercase: true,
    requireNumbers: true,
    requireSymbols: true,
    expiryDays: 90,
  })
  const [sessionSettings, setSessionSettings] = useState({
    timeout: 30,
    maxSessions: 3,
    rememberMe: true,
  })
  const [isSaving, setIsSaving] = useState(false)

  const toggleFeature = (id) => {
    setFeatures(features.map(f =>
      f.id === id ? { ...f, enabled: !f.enabled } : f
    ))
  }

  const handleSave = async () => {
    setIsSaving(true)
    await new Promise(resolve => setTimeout(resolve, 1500))
    toast.success('تم حفظ إعدادات الأمان بنجاح')
    setIsSaving(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6" dir="rtl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto space-y-6"
      >
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
              <Shield className="w-8 h-8 text-red-400" />
              إعدادات الأمان
            </h1>
            <p className="text-slate-400 mt-1">إدارة إعدادات الأمان والحماية</p>
          </div>
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="flex items-center gap-2 px-6 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-800 text-white rounded-lg transition-colors"
          >
            {isSaving ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            حفظ التغييرات
          </button>
        </div>

        {/* Security Features */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Settings className="w-5 h-5 text-blue-400" />
            ميزات الأمان
          </h2>
          <div className="space-y-4">
            {features.map((feature) => (
              <div
                key={feature.id}
                className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg"
              >
                <div className="flex items-center gap-4">
                  {feature.enabled ? (
                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                  ) : (
                    <AlertTriangle className="w-5 h-5 text-amber-400" />
                  )}
                  <div>
                    <p className="text-white font-medium">{feature.name}</p>
                    <p className="text-slate-400 text-sm">{feature.description}</p>
                  </div>
                </div>
                <button
                  onClick={() => toggleFeature(feature.id)}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    feature.enabled ? 'bg-emerald-600' : 'bg-slate-600'
                  }`}
                >
                  <span
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      feature.enabled ? 'right-1' : 'left-1'
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Password Policy */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Key className="w-5 h-5 text-amber-400" />
            سياسة كلمات المرور
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-300 text-sm mb-2">الحد الأدنى للطول</label>
              <input
                type="number"
                value={passwordPolicy.minLength}
                onChange={(e) => setPasswordPolicy({ ...passwordPolicy, minLength: Number(e.target.value) })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 text-sm mb-2">انتهاء الصلاحية (أيام)</label>
              <input
                type="number"
                value={passwordPolicy.expiryDays}
                onChange={(e) => setPasswordPolicy({ ...passwordPolicy, expiryDays: Number(e.target.value) })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div className="md:col-span-2 grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { key: 'requireUppercase', label: 'حروف كبيرة' },
                { key: 'requireLowercase', label: 'حروف صغيرة' },
                { key: 'requireNumbers', label: 'أرقام' },
                { key: 'requireSymbols', label: 'رموز' },
              ].map(({ key, label }) => (
                <label key={key} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={passwordPolicy[key]}
                    onChange={(e) => setPasswordPolicy({ ...passwordPolicy, [key]: e.target.checked })}
                    className="w-4 h-4 rounded bg-slate-700 border-slate-600 text-red-600 focus:ring-red-500"
                  />
                  <span className="text-slate-300 text-sm">{label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Session Settings */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5 text-purple-400" />
            إعدادات الجلسة
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-slate-300 text-sm mb-2">مهلة الجلسة (دقائق)</label>
              <input
                type="number"
                value={sessionSettings.timeout}
                onChange={(e) => setSessionSettings({ ...sessionSettings, timeout: Number(e.target.value) })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 text-sm mb-2">الحد الأقصى للجلسات</label>
              <input
                type="number"
                value={sessionSettings.maxSessions}
                onChange={(e) => setSessionSettings({ ...sessionSettings, maxSessions: Number(e.target.value) })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div className="flex items-end">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={sessionSettings.rememberMe}
                  onChange={(e) => setSessionSettings({ ...sessionSettings, rememberMe: e.target.checked })}
                  className="w-4 h-4 rounded bg-slate-700 border-slate-600 text-red-600 focus:ring-red-500"
                />
                <span className="text-slate-300">السماح بـ "تذكرني"</span>
              </label>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
