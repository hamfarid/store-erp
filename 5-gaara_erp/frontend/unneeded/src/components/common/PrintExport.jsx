import React, { useState, useRef } from 'react'
import { useReactToPrint } from 'react-to-print'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import { ExportButton, PrintButton } from './EnhancedButton'
import { useProgress } from './ProgressBar'
import { useToast } from './EnhancedToast'
import './PrintExport.css'

// Print Component Wrapper
export const PrintableComponent = React.forwardRef(({ children, title, className = '' }, ref) => (
  <div ref={ref} className={`printable-component ${className}`}>
    <div className="print-header">
      <h1 className="print-title">{title}</h1>
      <div className="print-date">
        تاريخ الطباعة: {new Date().toLocaleDateString('ar-EG')}
      </div>
    </div>
    <div className="print-content">
      {children}
    </div>
    <div className="print-footer">
      <div className="company-info">
        <p>نظام إدارة المخزون المتكامل</p>
        <p>تم إنشاؤه بواسطة النظام الآلي</p>
      </div>
    </div>
  </div>
))

// Print Hook
export const usePrint = (title = 'تقرير') => {
  const componentRef = useRef()
  const [isPrinting, setIsPrinting] = useState(false)
  const toast = useToast()

  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
    documentTitle: title,
    onBeforeGetContent: () => {
      setIsPrinting(true)
      return Promise.resolve()
    },
    onAfterPrint: () => {
      setIsPrinting(false)
      toast.success('تم إرسال المستند للطباعة بنجاح')
    },
    onPrintError: (error) => {
      setIsPrinting(false)
      toast.error('فشل في طباعة المستند')
      },
    pageStyle: `
      @page {
        size: A4;
        margin: 20mm;
      }
      @media print {
        body { -webkit-print-color-adjust: exact; }
        .no-print { display: none !important; }
        .print-only { display: block !important; }
      }
    `
  })

  return {
    componentRef,
    handlePrint,
    isPrinting,
    PrintableComponent: (props) => <PrintableComponent ref={componentRef} {...props} />
  }
}

// Export Hook
export const useExport = () => {
  const { startOperation, updateOperation, completeOperation, failOperation } = useProgress()
  const toast = useToast()

  const exportToExcel = async (data, filename = 'تقرير', sheetName = 'البيانات') => {
    const operationId = `export-excel-${Date.now()}`
    
    try {
      startOperation(operationId, {
        message: 'جاري تصدير ملف Excel...',
        progress: 0
      })

      updateOperation(operationId, { progress: 25, message: 'جاري معالجة البيانات...' })

      // Create workbook
      const wb = XLSX.utils.book_new()
      
      updateOperation(operationId, { progress: 50, message: 'جاري إنشاء الجدول...' })

      // Convert data to worksheet
      let ws
      if (Array.isArray(data)) {
        ws = XLSX.utils.json_to_sheet(data)
      } else if (typeof data === 'object' && data.headers && data.rows) {
        ws = XLSX.utils.aoa_to_sheet([data.headers, ...data.rows])
      } else {
        throw new Error('تنسيق البيانات غير مدعوم')
      }

      updateOperation(operationId, { progress: 75, message: 'جاري حفظ الملف...' })

      // Add worksheet to workbook
      XLSX.utils.book_append_sheet(wb, ws, sheetName)

      // Generate file
      const timestamp = new Date().toISOString().slice(0, 10)
      const fullFilename = `${filename}_${timestamp}.xlsx`
      
      XLSX.writeFile(wb, fullFilename)

      completeOperation(operationId, 'تم تصدير ملف Excel بنجاح')
      toast.success(`تم تصدير ${fullFilename} بنجاح`)

    } catch (error) {
      failOperation(operationId, 'فشل في تصدير ملف Excel')
      toast.error('فشل في تصدير ملف Excel')
      }
  }

  const exportToPDF = async (data, filename = 'تقرير', options = {}) => {
    const operationId = `export-pdf-${Date.now()}`
    
    try {
      startOperation(operationId, {
        message: 'جاري تصدير ملف PDF...',
        progress: 0
      })

      updateOperation(operationId, { progress: 25, message: 'جاري إنشاء المستند...' })

      // Create PDF
      const doc = new jsPDF({
        orientation: options.orientation || 'portrait',
        unit: 'mm',
        format: 'a4'
      })

      // Add Arabic font support (if available)
      try {
        doc.addFont('/fonts/NotoSansArabic-Regular.ttf', 'NotoSansArabic', 'normal')
        doc.setFont('NotoSansArabic')
      } catch (e) {
        }

      updateOperation(operationId, { progress: 50, message: 'جاري إضافة المحتوى...' })

      // Add title
      doc.setFontSize(16)
      doc.text(filename, 105, 20, { align: 'center' })
      
      // Add date
      doc.setFontSize(10)
      doc.text(`تاريخ الإنشاء: ${new Date().toLocaleDateString('ar-EG')}`, 20, 30)

      updateOperation(operationId, { progress: 75, message: 'جاري تنسيق الجدول...' })

      // Add table
      if (data.headers && data.rows) {
        doc.autoTable({
          head: [data.headers],
          body: data.rows,
          startY: 40,
          styles: {
            font: 'NotoSansArabic',
            fontSize: 8,
            cellPadding: 2
          },
          headStyles: {
            fillColor: [41, 128, 185],
            textColor: 255,
            fontStyle: 'bold'
          },
          alternateRowStyles: {
            fillColor: [245, 245, 245]
          },
          margin: { top: 40, right: 20, bottom: 20, left: 20 }
        })
      }

      // Save file
      const timestamp = new Date().toISOString().slice(0, 10)
      const fullFilename = `${filename}_${timestamp}.pdf`
      
      doc.save(fullFilename)

      completeOperation(operationId, 'تم تصدير ملف PDF بنجاح')
      toast.success(`تم تصدير ${fullFilename} بنجاح`)

    } catch (error) {
      failOperation(operationId, 'فشل في تصدير ملف PDF')
      toast.error('فشل في تصدير ملف PDF')
      }
  }

  const exportToCSV = async (data, filename = 'تقرير') => {
    try {
      let csvContent = ''
      
      if (data.headers && data.rows) {
        csvContent = [data.headers, ...data.rows]
          .map(row => row.map(cell => `"${cell}"`).join(','))
          .join('\n')
      } else if (Array.isArray(data)) {
        const headers = Object.keys(data[0] || {})
        csvContent = [
          headers.join(','),
          ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
        ].join('\n')
      }

      // Add BOM for Arabic support
      const BOM = '\uFEFF'
      const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
      
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      
      const timestamp = new Date().toISOString().slice(0, 10)
      link.setAttribute('download', `${filename}_${timestamp}.csv`)
      
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      toast.success('تم تصدير ملف CSV بنجاح')

    } catch (error) {
      toast.error('فشل في تصدير ملف CSV')
      }
  }

  return {
    exportToExcel,
    exportToPDF,
    exportToCSV
  }
}

// Export Buttons Component
export const ExportButtons = ({ 
  data, 
  filename = 'تقرير', 
  formats = ['excel', 'pdf', 'csv'],
  onExport 
}) => {
  const { exportToExcel, exportToPDF, exportToCSV } = useExport()
  const [isExporting, setIsExporting] = useState(false)

  const handleExport = async (format) => {
    if (isExporting) return
    
    setIsExporting(true)
    
    try {
      if (onExport) {
        await onExport(format)
      } else {
        switch (format) {
          case 'excel':
            await exportToExcel(data, filename)
            break
          case 'pdf':
            await exportToPDF(data, filename)
            break
          case 'csv':
            await exportToCSV(data, filename)
            break
        }
      }
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className="export-buttons">
      {formats.includes('excel') && (
        <ExportButton
          loading={isExporting}
          onClick={() => handleExport('excel')}
          className="export-button--excel"
        >
          Excel
        </ExportButton>
      )}
      
      {formats.includes('pdf') && (
        <ExportButton
          loading={isExporting}
          onClick={() => handleExport('pdf')}
          className="export-button--pdf"
        >
          PDF
        </ExportButton>
      )}
      
      {formats.includes('csv') && (
        <ExportButton
          loading={isExporting}
          onClick={() => handleExport('csv')}
          className="export-button--csv"
        >
          CSV
        </ExportButton>
      )}
    </div>
  )
}

// Print and Export Toolbar
export const PrintExportToolbar = ({ 
  data, 
  filename, 
  onPrint, 
  onExport,
  printTitle,
  className = ''
}) => {
  const { handlePrint, isPrinting } = usePrint(printTitle)

  return (
    <div className={`print-export-toolbar ${className}`}>
      <div className="toolbar-section">
        <PrintButton
          loading={isPrinting}
          onClick={onPrint || handlePrint}
        />
      </div>
      
      <div className="toolbar-section">
        <ExportButtons
          data={data}
          filename={filename}
          onExport={onExport}
        />
      </div>
    </div>
  )
}

export default { usePrint, useExport, ExportButtons, PrintExportToolbar }
