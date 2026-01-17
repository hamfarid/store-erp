/**
 * Modules Management Page - صفحة إدارة الوحدات
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Boxes,
  Search,
  Settings,
  Power,
  RefreshCw,
  Info,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Download,
  Upload,
  Trash2,
} from 'lucide-react'

const modules = [
  { id: 'sales', name: 'المبيعات', version: '2.1.0', status: 'active', description: 'إدارة المبيعات والفواتير', dependencies: ['inventory', 'contacts'] },
  { id: 'inventory', name: 'المخزون', version: '2.0.5', status: 'active', description: 'إدارة المخزون والمستودعات', dependencies: [] },
  { id: 'accounting', name: 'المحاسبة', version: '1.8.2', status: 'active', description: 'النظام المحاسبي والمالي', dependencies: ['sales', 'purchasing'] },
  { id: 'purchasing', name: 'المشتريات', version: '1.5.0', status: 'active', description: 'إدارة المشتريات والموردين', dependencies: ['inventory', 'contacts'] },
  { id: 'contacts', name: 'جهات الاتصال', version: '1.3.0', status: 'active', description: 'إدارة العملاء والموردين', dependencies: [] },
  { id: 'hr', name: 'الموارد البشرية', version: '1.0.0', status: 'inactive', description: 'إدارة الموظفين والرواتب', dependencies: [] },
  { id: 'pos', name: 'نقطة البيع', version: '1.2.0', status: 'active', description: 'نظام نقطة البيع', dependencies: ['sales', 'inventory'] },
  { id: 'reports', name: 'التقارير', version: '2.0.0', status: 'active', description: 'نظام التقارير والإحصائيات', dependencies: [] },
  { id: 'ai', name: 'الذكاء الاصطناعي', version: '0.5.0', status: 'beta', description: 'تحليلات وتوقعات ذكية', dependencies: ['reports'] },
]

const statusConfig = {
  active: { icon: CheckCircle, color: 'emerald', label: 'نشط' },
  inactive: { icon: XCircle, color: 'slate', label: 'غير نشط' },
  beta: { icon: AlertTriangle, color: 'amber', label: 'تجريبي' },
  error: { icon: XCircle, color: 'red', label: 'خطأ' },
}

export default function ModulesManagementPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [moduleList, setModuleList] = useState(modules)
  const [selectedModule, setSelectedModule] = useState(null)

  const filteredModules = moduleList.filter(m =>
    m.name.includes(searchTerm) || m.id.includes(searchTerm)
  )

  const toggleModule = (id) => {
    setModuleList(moduleList.map(m => {
      if (m.id === id) {
        const newStatus = m.status === 'active' ? 'inactive' : 'active'
        toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'تعطيل'} وحدة ${m.name}`)
        return { ...m, status: newStatus }
      }
      return m
    }))
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
              <Boxes className="w-8 h-8 text-cyan-400" />
              إدارة الوحدات
            </h1>
            <p className="text-slate-400 mt-1">إدارة وتفعيل وحدات النظام</p>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              <Upload className="w-4 h-4" />
              تثبيت وحدة
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors">
              <RefreshCw className="w-4 h-4" />
              تحديث الكل
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'إجمالي الوحدات', value: moduleList.length, color: 'cyan' },
            { label: 'وحدات نشطة', value: moduleList.filter(m => m.status === 'active').length, color: 'emerald' },
            { label: 'وحدات معطلة', value: moduleList.filter(m => m.status === 'inactive').length, color: 'slate' },
            { label: 'وحدات تجريبية', value: moduleList.filter(m => m.status === 'beta').length, color: 'amber' },
          ].map((stat, i) => (
            <div
              key={i}
              className={`p-4 bg-${stat.color}-500/10 rounded-xl border border-${stat.color}-500/30`}
            >
              <p className="text-slate-400 text-sm">{stat.label}</p>
              <p className={`text-2xl font-bold text-${stat.color}-400`}>{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="البحث في الوحدات..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-cyan-500"
          />
        </div>

        {/* Modules Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredModules.map((module, index) => {
            const { icon: StatusIcon, color, label } = statusConfig[module.status]
            
            return (
              <motion.div
                key={module.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-5 hover:border-slate-600 transition-colors"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{module.name}</h3>
                    <p className="text-slate-400 text-sm">v{module.version}</p>
                  </div>
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-${color}-500/20 text-${color}-400`}>
                    <StatusIcon className="w-3 h-3" />
                    {label}
                  </span>
                </div>

                <p className="text-slate-400 text-sm mb-4">{module.description}</p>

                {module.dependencies.length > 0 && (
                  <div className="mb-4">
                    <p className="text-slate-500 text-xs mb-1">يعتمد على:</p>
                    <div className="flex flex-wrap gap-1">
                      {module.dependencies.map(dep => (
                        <span key={dep} className="px-2 py-0.5 bg-slate-700 rounded text-slate-300 text-xs">
                          {modules.find(m => m.id === dep)?.name || dep}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                  <div className="flex gap-1">
                    <button
                      onClick={() => setSelectedModule(module)}
                      className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <Info className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                      <Settings className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors">
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                  <button
                    onClick={() => toggleModule(module.id)}
                    className={`p-2 rounded-lg transition-colors ${
                      module.status === 'active'
                        ? 'text-emerald-400 hover:bg-emerald-500/20'
                        : 'text-slate-400 hover:bg-slate-700'
                    }`}
                  >
                    <Power className="w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}
