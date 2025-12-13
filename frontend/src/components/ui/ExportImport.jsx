import React, { useState } from 'react'
import { Download, FileText, FileSpreadsheet, File } from 'lucide-react'

// مكون تصدير البيانات
const ExportComponent = ({ 
  data, 
  filename = 'export', 
  formats = ['csv', 'xlsx', 'pdf'],
  onExport,
  className = ""
}) => {
  const [exporting, setExporting] = useState(false)
  const [selectedFormat, setSelectedFormat] = useState(formats[0])

  const formatIcons = {
    csv: FileText,
    xlsx: FileSpreadsheet,
    pdf: File,
    json: FileText
  }

  const formatLabels = {
    csv: 'CSV',
    xlsx: 'Excel',
    pdf: 'PDF',
    json: 'JSON'
  }

  const handleExport = async () => {
    setExporting(true)
    try {
      if (onExport) {
        await onExport(data, selectedFormat, filename)
      } else {
        // تصدير افتراضي
        await defaultExport(data, selectedFormat, filename)
      }
    } catch (error) {
      } finally {
      setExporting(false)
    }
  }

  const defaultExport = async (data, format, filename) => {
    let content, mimeType, extension

    switch (format) {
      case 'csv':
        content = convertToCSV(data)
        mimeType = 'text/csv'
        extension = 'csv'
        break
      case 'json':
        content = JSON.stringify(data, null, 2)
        mimeType = 'application/json'
        extension = 'json'
        break
      default:
        throw new Error(`تنسيق غير مدعوم: ${format}`)
    }

    const blob = new Blob([content], { type: mimeType })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}.${extension}`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  const convertToCSV = (data) => {
    if (!data || data.length === 0) return ''
    
    const headers = Object.keys(data[0])
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => {
          const value = row[header]
          return typeof value === 'string' && value.includes(',') 
            ? `"${value}"` 
            : value
        }).join(',')
      )
    ].join('\n')
    
    return csvContent
  }

  return (
    <div className={`bg-white rounded-lg border border-border p-4 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground flex items-center">
          <Download className="w-5 h-5 ml-2 text-primary-600" />
          تصدير البيانات
        </h3>
      </div>

      <div className="space-y-4">
        {/* اختيار التنسيق */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            تنسيق التصدير
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {formats.map(format => {
              const Icon = formatIcons[format]
              return (
                <button
                  key={format}
                  onClick={() => setSelectedFormat(format)}
                  className={`flex items-center justify-center p-3 border rounded-lg transition-colors ${
                    selectedFormat === format
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-border hover:border-gray-400'
                  }`}
                >
                  <Icon className="w-4 h-4 ml-1" />
                  {formatLabels[format]}
                </button>
              )
            })}
          </div>
        </div>

        {/* معلومات البيانات */}
        <div className="bg-muted/50 rounded-lg p-3">
          <div className="text-sm text-muted-foreground">
            <p>عدد السجلات: <span className="font-medium">{data?.length || 0}</span></p>
            <p>اسم الملف: <span className="font-medium">{filename}.{selectedFormat}</span></p>
          </div>
        </div>

        {/* زر التصدير */}
        <button
          onClick={handleExport}
          disabled={exporting || !data || data.length === 0}
          className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {exporting ? (
            <RefreshCw className="w-4 h-4 ml-1 animate-spin" />
          ) : (
            <Download className="w-4 h-4 ml-1" />
          )}
          {exporting ? 'جاري التصدير...' : 'تصدير البيانات'}
        </button>
      </div>
    </div>
  )
}

// مكون استيراد البيانات
const ImportComponent = ({ 
  onImport,
  acceptedFormats = ['.csv', '.xlsx', '.json'],
  maxFileSize = 5 * 1024 * 1024, // 5MB
  className = ""
}) => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file) => {
    // التحقق من نوع الملف
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    if (!acceptedFormats.includes(fileExtension)) {
      setUploadResult({
        success: false,
        message: `نوع الملف غير مدعوم. الأنواع المدعومة: ${acceptedFormats.join(', ')}`
      })
      return
    }

    // التحقق من حجم الملف
    if (file.size > maxFileSize) {
      setUploadResult({
        success: false,
        message: `حجم الملف كبير جداً. الحد الأقصى: ${(maxFileSize / 1024 / 1024).toFixed(1)} MB`
      })
      return
    }

    setUploading(true)
    setUploadResult(null)

    try {
      const data = await parseFile(file)
      
      if (onImport) {
        const result = await onImport(data, file)
        setUploadResult(result)
      } else {
        setUploadResult({
          success: true,
          message: `تم تحليل ${data.length} سجل بنجاح`,
          data: data
        })
      }
    } catch (error) {
      setUploadResult({
        success: false,
        message: `خطأ في تحليل الملف: ${error.message}`
      })
    } finally {
      setUploading(false)
    }
  }

  const parseFile = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (e) => {
        try {
          const content = e.target.result
          const extension = file.name.split('.').pop().toLowerCase()
          
          switch (extension) {
            case 'json':
              resolve(JSON.parse(content))
              break
            case 'csv':
              resolve(parseCSV(content))
              break
            default:
              reject(new Error('نوع ملف غير مدعوم'))
          }
        } catch (error) {
          reject(error)
        }
      }
      
      reader.onerror = () => reject(new Error('خطأ في قراءة الملف'))
      reader.readAsText(file)
    })
  }

  const parseCSV = (content) => {
    const lines = content.split('\n').filter(line => line.trim())
    if (lines.length === 0) return []
    
    const headers = lines[0].split(',').map(h => h.trim())
    const data = []
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim())
      const row = {}
      headers.forEach((header, index) => {
        row[header] = values[index] || ''
      })
      data.push(row)
    }
    
    return data
  }

  return (
    <div className={`bg-white rounded-lg border border-border p-4 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground flex items-center">
          <Upload className="w-5 h-5 ml-2 text-primary" />
          استيراد البيانات
        </h3>
      </div>

      <div className="space-y-4">
        {/* منطقة السحب والإفلات */}
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive 
              ? 'border-primary-500 bg-primary-50' 
              : 'border-border hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-lg font-medium text-foreground mb-2">
            اسحب الملف هنا أو انقر للاختيار
          </p>
          <p className="text-sm text-muted-foreground mb-4">
            الأنواع المدعومة: {acceptedFormats.join(', ')}
          </p>
          <input
            type="file"
            accept={acceptedFormats.join(',')}
            onChange={handleFileInput}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 cursor-pointer transition-colors"
          >
            <Upload className="w-4 h-4 ml-1" />
            اختيار ملف
          </label>
        </div>

        {/* حالة التحميل */}
        {uploading && (
          <div className="flex items-center justify-center p-4 bg-primary-50 rounded-lg">
            <RefreshCw className="w-5 h-5 text-primary-600 animate-spin ml-2" />
            <span className="text-primary-700">جاري تحليل الملف...</span>
          </div>
        )}

        {/* نتيجة التحميل */}
        {uploadResult && (
          <div className={`p-4 rounded-lg flex items-start ${
            uploadResult.success 
              ? 'bg-primary/10 border border-primary/30' 
              : 'bg-destructive/10 border border-destructive/30'
          }`}>
            {uploadResult.success ? (
              <CheckCircle className="w-5 h-5 text-primary ml-2 mt-0.5" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-destructive ml-2 mt-0.5" />
            )}
            <div className="flex-1">
              <p className={`font-medium ${
                uploadResult.success ? 'text-green-800' : 'text-red-800'
              }`}>
                {uploadResult.success ? 'نجح الاستيراد' : 'فشل الاستيراد'}
              </p>
              <p className={`text-sm mt-1 ${
                uploadResult.success ? 'text-primary' : 'text-destructive'
              }`}>
                {uploadResult.message}
              </p>
            </div>
            <button
              onClick={() => setUploadResult(null)}
              className="text-gray-400 hover:text-muted-foreground"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

// مكون مجمع للتصدير والاستيراد
const ExportImportComponent = ({ 
  data, 
  onImport, 
  onExport,
  filename = 'data',
  className = ""
}) => {
  return (
    <div className={`grid grid-cols-1 lg:grid-cols-2 gap-6 ${className}`}>
      <ExportComponent 
        data={data}
        filename={filename}
        onExport={onExport}
      />
      <ImportComponent 
        onImport={onImport}
      />
    </div>
  )
}

export {
  ExportComponent,
  ImportComponent,
  ExportImportComponent
}

