/**
 * Data Import Page - صفحة استيراد البيانات
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  Upload,
  FileSpreadsheet,
  FileText,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RefreshCw,
  Download,
  Eye,
  Trash2,
} from 'lucide-react'

const importTemplates = [
  { id: 'customers', name: 'العملاء', fields: ['الاسم', 'البريد', 'الهاتف', 'العنوان'] },
  { id: 'products', name: 'المنتجات', fields: ['الاسم', 'الكود', 'السعر', 'الكمية'] },
  { id: 'suppliers', name: 'الموردين', fields: ['الاسم', 'البريد', 'الهاتف', 'العنوان'] },
  { id: 'inventory', name: 'المخزون', fields: ['المنتج', 'الكمية', 'المستودع', 'الموقع'] },
]

const importHistory = [
  { id: 1, name: 'customers_jan2026.xlsx', module: 'العملاء', records: 150, success: 148, failed: 2, date: '2026-01-17 10:30', status: 'completed' },
  { id: 2, name: 'products_update.csv', module: 'المنتجات', records: 500, success: 500, failed: 0, date: '2026-01-16 15:20', status: 'completed' },
  { id: 3, name: 'inventory.xlsx', module: 'المخزون', records: 0, success: 0, failed: 0, date: '2026-01-15 09:00', status: 'failed' },
]

export default function DataImportPage() {
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [isImporting, setIsImporting] = useState(false)
  const [importProgress, setImportProgress] = useState(0)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setUploadedFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFile(e.target.files[0])
    }
  }

  const handleImport = async () => {
    if (!uploadedFile || !selectedTemplate) {
      toast.error('الرجاء اختيار قالب ورفع ملف')
      return
    }
    setIsImporting(true)
    setImportProgress(0)
    
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200))
      setImportProgress(i)
    }
    
    toast.success('تم استيراد البيانات بنجاح')
    setIsImporting(false)
    setImportProgress(0)
    setUploadedFile(null)
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
              <Upload className="w-8 h-8 text-blue-400" />
              استيراد البيانات
            </h1>
            <p className="text-slate-400 mt-1">استيراد البيانات من ملفات Excel و CSV</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Import Options */}
          <div className="lg:col-span-2 space-y-6">
            {/* Select Template */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">اختر القالب</h2>
                <button className="text-blue-400 text-sm hover:underline flex items-center gap-1">
                  <Download className="w-4 h-4" />
                  تحميل القوالب
                </button>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {importTemplates.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => setSelectedTemplate(template.id)}
                    className={`p-4 rounded-xl border transition-all text-right ${
                      selectedTemplate === template.id
                        ? 'bg-blue-500/20 border-blue-500'
                        : 'bg-slate-700/50 border-slate-600 hover:border-slate-500'
                    }`}
                  >
                    <FileSpreadsheet className={`w-6 h-6 mb-2 ${
                      selectedTemplate === template.id ? 'text-blue-400' : 'text-slate-400'
                    }`} />
                    <p className="text-white font-medium">{template.name}</p>
                    <p className="text-slate-400 text-xs mt-1">
                      الحقول: {template.fields.join('، ')}
                    </p>
                  </button>
                ))}
              </div>
            </div>

            {/* File Upload */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">رفع الملف</h2>
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                  dragActive
                    ? 'border-blue-500 bg-blue-500/10'
                    : 'border-slate-600 hover:border-slate-500'
                }`}
              >
                {uploadedFile ? (
                  <div className="space-y-3">
                    <FileText className="w-12 h-12 mx-auto text-emerald-400" />
                    <p className="text-white font-medium">{uploadedFile.name}</p>
                    <p className="text-slate-400 text-sm">
                      {(uploadedFile.size / 1024).toFixed(2)} KB
                    </p>
                    <button
                      onClick={() => setUploadedFile(null)}
                      className="text-red-400 text-sm hover:underline"
                    >
                      إزالة الملف
                    </button>
                  </div>
                ) : (
                  <>
                    <Upload className="w-12 h-12 mx-auto text-slate-400 mb-4" />
                    <p className="text-white mb-2">اسحب الملف هنا أو</p>
                    <label className="cursor-pointer">
                      <span className="text-blue-400 hover:underline">اختر ملف</span>
                      <input
                        type="file"
                        accept=".xlsx,.xls,.csv"
                        onChange={handleFileChange}
                        className="hidden"
                      />
                    </label>
                    <p className="text-slate-500 text-sm mt-2">
                      الصيغ المدعومة: Excel (.xlsx, .xls), CSV
                    </p>
                  </>
                )}
              </div>
            </div>

            {/* Import Progress */}
            {isImporting && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
                <h2 className="text-xl font-semibold text-white mb-4">جاري الاستيراد...</h2>
                <div className="h-4 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full transition-all"
                    style={{ width: `${importProgress}%` }}
                  />
                </div>
                <p className="text-slate-400 text-center mt-2">{importProgress}%</p>
              </div>
            )}

            {/* Import Button */}
            <button
              onClick={handleImport}
              disabled={isImporting || !uploadedFile || !selectedTemplate}
              className="w-full py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2"
            >
              {isImporting ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  جاري الاستيراد...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  استيراد البيانات
                </>
              )}
            </button>
          </div>

          {/* Import History */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6 h-fit">
            <h2 className="text-xl font-semibold text-white mb-4">سجل الاستيراد</h2>
            <div className="space-y-3">
              {importHistory.map((imp) => (
                <div
                  key={imp.id}
                  className="p-4 bg-slate-700/50 rounded-lg"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-medium text-sm truncate">{imp.name}</span>
                    {imp.status === 'completed' ? (
                      <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
                    )}
                  </div>
                  <p className="text-slate-400 text-sm">{imp.module}</p>
                  <div className="flex items-center justify-between mt-2 text-xs">
                    <span className="text-emerald-400">{imp.success} ناجح</span>
                    {imp.failed > 0 && (
                      <span className="text-red-400">{imp.failed} فاشل</span>
                    )}
                  </div>
                  <p className="text-slate-500 text-xs mt-2">{imp.date}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
