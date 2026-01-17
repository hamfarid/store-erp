// FILE: frontend/src/components/ui/ExportControls.jsx | PURPOSE: Reusable export format selector and button component | OWNER: Frontend Team | RELATED: export.js, UserManagementAdvanced.jsx, AccountingSystem.jsx | LAST-AUDITED: 2025-10-29

import React, { useState } from 'react'
import { Download } from 'lucide-react'
import { exportToCSV, exportToExcel } from '../../utils/export'

/**
 * Reusable Export Controls Component
 * Provides format selector (CSV/XLSX) and export button with RBAC support
 * 
 * @param {Object} props
 * @param {Array<Object>} props.data - Data to export
 * @param {string} props.filename - Base filename (without extension)
 * @param {boolean} props.canExport - Permission check result
 * @param {string} [props.className] - Additional CSS classes
 * @param {Function} [props.onBeforeExport] - Callback before export
 * @param {Function} [props.onAfterExport] - Callback after export
 * @param {Array<string>} [props.formats] - Available formats (default: ['CSV', 'XLSX'])
 */
const ExportControls = ({
  data,
  filename,
  canExport,
  className = '',
  onBeforeExport,
  onAfterExport,
  formats = ['CSV', 'XLSX']
}) => {
  const [exportFormat, setExportFormat] = useState(formats[0])
  const [isExporting, setIsExporting] = useState(false)

  const handleExport = async () => {
    if (!data || data.length === 0) {
      console.warn('No data to export')
      return
    }

    if (!canExport) {
      console.warn('User does not have export permission')
      return
    }

    setIsExporting(true)

    try {
      if (onBeforeExport) {
        await onBeforeExport(exportFormat)
      }

      if (exportFormat === 'XLSX') {
        exportToExcel(filename, data)
      } else {
        exportToCSV(`${filename}.csv`, data)
      }

      if (onAfterExport) {
        await onAfterExport(exportFormat)
      }
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className={`flex items-center space-x-2 space-x-reverse ${className}`}>
      {/* Format Selector */}
      <select
        value={exportFormat}
        onChange={(e) => setExportFormat(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg bg-white text-gray-700 text-sm hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={!canExport || isExporting}
        title="اختر صيغة التصدير"
      >
        {formats.map((format) => (
          <option key={format} value={format}>
            {format}
          </option>
        ))}
      </select>

      {/* Export Button */}
      <button
        onClick={handleExport}
        disabled={!canExport || isExporting || !data || data.length === 0}
        title={!canExport ? 'لا تملك صلاحية التصدير' : 'تصدير البيانات'}
        className={`flex items-center px-4 py-2 rounded-lg transition-colors text-white font-medium ${
          !canExport || isExporting || !data || data.length === 0
            ? 'bg-gray-400 cursor-not-allowed opacity-50'
            : 'bg-green-600 hover:bg-green-700 active:bg-green-800'
        }`}
      >
        <Download className="w-4 h-4 ml-1" />
        {isExporting ? 'جاري التصدير...' : 'تصدير'}
      </button>
    </div>
  )
}

export default ExportControls

