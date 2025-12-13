import React, { useState } from 'react'
import { Download, FileSpreadsheet, Upload } from 'lucide-react'
import { toast } from 'react-hot-toast'

const ExcelImport = ({ onImport, type = 'products' }) => {
  const [importing, setImporting] = useState(false)
  const [previewData, setPreviewData] = useState([])
  const [showPreview, setShowPreview] = useState(false)

  // قوالب البيانات المختلفة
  const templates = {
    products: {
      name: 'المنتجات',
      columns: ['اسم المنتج', 'الكود', 'الفئة', 'الوحدة', 'السعر', 'الكمية الدنيا', 'المخزن', 'اللوط', 'تاريخ الانتهاء'],
      sample: [
        ['بذور طماطم', 'P001', 'بذور', 'كيس', '25.50', '10', 'المخزن الرئيسي', 'LOT001', '2025-12-31'],
        ['سماد NPK', 'P002', 'أسمدة', 'كيس', '45.00', '5', 'المخزن الفرعي', 'LOT002', '2026-06-30']
      ]
    },
    customers: {
      name: 'العملاء',
      columns: ['اسم العميل', 'الهاتف', 'العنوان', 'البريد الإلكتروني', 'نوع العميل'],
      sample: [
        ['أحمد محمد', '01234567890', 'القاهرة', 'ahmed@example.com', 'تاجر تجزئة'],
        ['فاطمة علي', '01987654321', 'الإسكندرية', 'fatma@example.com', 'مزارع']
      ]
    },
    suppliers: {
      name: 'الموردين',
      columns: ['اسم المورد', 'الهاتف', 'العنوان', 'البريد الإلكتروني', 'نوع المورد'],
      sample: [
        ['شركة البذور المصرية', '0225551234', 'القاهرة', 'info@seeds.com', 'بذور'],
        ['مصنع الأسمدة الحديث', '0335554567', 'الإسكندرية', 'sales@fertilizer.com', 'أسمدة']
      ]
    }
  }

  // تحميل ملف القالب
  const downloadTemplate = async () => {
    try {
      // استيراد مكتبة xlsx ديناميكياً
      const XLSX = await import('xlsx')
      const template = templates[type]
      const ws = XLSX.utils.aoa_to_sheet([template.columns, ...template.sample])
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, template.name)
      XLSX.writeFile(wb, `قالب_${template.name}.xlsx`)
      toast.success('تم تحميل القالب بنجاح!')
    } catch {
      toast.error('خطأ في تحميل القالب')
    }
  }

  // قراءة ملف Excel
  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (!file.name.match(/\.(xlsx|xls)$/)) {
      toast.error('يرجى اختيار ملف Excel صحيح (.xlsx أو .xls)')
      return
    }

    setImporting(true)
    const reader = new FileReader()

    reader.onload = async (e) => {
      try {
        // استيراد مكتبة xlsx ديناميكياً
        const XLSX = await import('xlsx')
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: 'array' })
        const sheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[sheetName]
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })

        if (jsonData.length < 2) {
          toast.error('الملف فارغ أو لا يحتوي على بيانات صحيحة')
          setImporting(false)
          return
        }

        // تحويل البيانات إلى كائنات
        const headers = jsonData[0]
        const rows = jsonData.slice(1)
        const processedData = rows.map(row => {
          const obj = {}
          headers.forEach((header, index) => {
            obj[header] = row[index] || ''
          })
          return obj
        })

        setPreviewData(processedData)
        setShowPreview(true)
        toast.success(`تم قراءة ${processedData.length} سجل من الملف`)
      } catch (error) {
        toast.error('خطأ في قراءة الملف: ' + error.message)
      } finally {
        setImporting(false)
      }
    }

    reader.readAsArrayBuffer(file)
  }

  // تأكيد الاستيراد
  const confirmImport = () => {
    if (previewData.length === 0) {
      toast.error('لا توجد بيانات للاستيراد')
      return
    }

    onImport(previewData)
    setShowPreview(false)
    setPreviewData([])
    toast.success(`تم استيراد ${previewData.length} سجل بنجاح!`)
  }

  return (
    <div className="space-y-4">
      {/* أزرار التحكم */}
      <div className="flex gap-4 items-center">
        <button
          onClick={downloadTemplate}
          className="flex items-center gap-2 bg-primary hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          <Download className="w-4 h-4" />
          تحميل القالب
        </button>

        <div className="flex items-center gap-2">
          <label className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg cursor-pointer">
            <Upload className="w-4 h-4" />
            {importing ? 'جاري الاستيراد...' : 'استيراد ملف Excel'}
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              className="hidden"
              disabled={importing}
            />
          </label>
        </div>
      </div>

      {/* معاينة البيانات */}
      {showPreview && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">معاينة البيانات المستوردة</h3>
            <div className="flex gap-2">
              <button
                onClick={() => setShowPreview(false)}
                className="bg-gray-300 hover:bg-gray-400 text-foreground px-4 py-2 rounded"
              >
                إلغاء
              </button>
              <button
                onClick={confirmImport}
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded"
              >
                تأكيد الاستيراد ({previewData.length} سجل)
              </button>
            </div>
          </div>

          <div className="overflow-x-auto max-h-96">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-muted/50">
                <tr>
                  {previewData.length > 0 && Object.keys(previewData[0]).map((key, index) => (
                    <th key={index} className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {previewData.slice(0, 10).map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, cellIndex) => (
                      <td key={cellIndex} className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        {value}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {previewData.length > 10 && (
              <p className="text-center text-gray-500 mt-4">
                عرض أول 10 سجلات من أصل {previewData.length} سجل
              </p>
            )}
          </div>
        </div>
      )}

      {/* تعليمات */}
      <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <FileSpreadsheet className="w-5 h-5 text-primary-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-primary-900 mb-2">تعليمات الاستيراد:</h4>
            <ul className="text-sm text-primary-800 space-y-1">
              <li>• قم بتحميل القالب أولاً لمعرفة تنسيق البيانات المطلوب</li>
              <li>• املأ البيانات في القالب واحفظه بصيغة Excel</li>
              <li>• تأكد من صحة البيانات قبل الاستيراد</li>
              <li>• يمكن استيراد ملفات .xlsx و .xls</li>
              <li>• سيتم عرض معاينة للبيانات قبل التأكيد</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExcelImport

