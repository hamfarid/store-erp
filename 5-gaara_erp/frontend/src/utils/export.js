// FILE: frontend/src/utils/export.js | PURPOSE: Simple CSV export utility for table data | OWNER: Frontend Team | RELATED: components/UserManagementAdvanced.jsx, components/AccountingSystem.jsx | LAST-AUDITED: 2025-10-29

import { toast } from 'react-hot-toast'
import * as XLSX from 'xlsx'
import { logActivity } from './activityLogger'

/**
 * Convert an array of objects to CSV and trigger a download.
 * - Automatically derives headers from keys of the first row unless provided.
 * - Safely stringifies nested values.
 * - Includes UTF-8 BOM for Excel compatibility.
 *
 * @param {string} filename e.g. 'users.csv'
 * @param {Array<object>} rows
 * @param {Object} [options]
 * @param {string[]} [options.headers] explicit header keys order
 * @param {Record<string,string>} [options.labels] map key->header label
 */
export function exportToCSV(filename, rows, options = {}) {
  const startedAt = performance.now?.() || Date.now()
  try {
    const data = Array.isArray(rows) ? rows : []
    if (!data.length) {
      toast.error('لا توجد بيانات للتصدير')
      return
    }

    const keys = options.headers && options.headers.length
      ? options.headers
      : Array.from(
          data.reduce((set, row) => {
            Object.keys(row || {}).forEach(k => set.add(k))
            return set
          }, new Set())
        )

    const headerLine = keys
      .map(k => escapeCsv(options.labels?.[k] ?? k))
      .join(',')

    const lines = data.map(row => {
      return keys.map(k => escapeCsv(normalizeValue(row?.[k]))).join(',')
    })

    const csv = [headerLine, ...lines].join('\n')
    // BOM for Excel UTF-8
    const content = '\uFEFF' + csv
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })

    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.href = url
    link.download = filename || 'export.csv'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)

    const ms = (performance.now?.() || Date.now()) - startedAt
    toast.success(`\u062a\u0645 \u062a\u0635\u062f\u064a\u0631 ${data.length} \u0633\u062c\u0644\u0627\u062a`)
    logActivity({ action: 'EXPORT', entityType: filename?.replace(/\.csv$/i, ''), format: 'CSV', recordCount: data.length, outcome: 'success', timed_ms: Math.round(ms) })
  } catch (err) {
    const ms = (performance.now?.() || Date.now()) - startedAt
    toast.error('\u0641\u0634\u0644 \u0627\u0644\u062a\u0635\u062f\u064a\u0631')
    logActivity({ action: 'EXPORT', entityType: filename?.replace(/\.csv$/i, ''), format: 'CSV', recordCount: Array.isArray(rows) ? rows.length : 0, outcome: 'error', timed_ms: Math.round(ms) })
     
    console.error('exportToCSV failed', err)
  }
}

function normalizeValue(v) {
  if (v == null) return ''
  if (typeof v === 'object') {
  try { return JSON.stringify(v) } catch { return String(v) }
  }
  return String(v)
}

function escapeCsv(value) {
  const s = String(value ?? '')
  // Escape double quotes by doubling them and wrap in quotes if contains comma, quote, or newline
  const needsQuotes = /[",\n\r]/.test(s)
  const escaped = s.replace(/"/g, '""')
  return needsQuotes ? `"${escaped}"` : escaped
}

/**
 * Export data to Excel (XLSX) format.
 * @param {string} filename - Output filename (without extension)
 * @param {Array<object>} rows - Data rows
 * @param {Object} [options] - Export options
 * @param {string} [options.sheetName] - Sheet name (default: 'Data')
 * @param {string[]} [options.headers] - Column headers order
 */
export function exportToExcel(filename, rows, options = {}) {
  const startedAt = performance.now?.() || Date.now()
  try {
    const data = Array.isArray(rows) ? rows : []
    if (!data.length) {
      toast.error('لا توجد بيانات للتصدير')
      return
    }

    // Create worksheet from data
    const ws = XLSX.utils.json_to_sheet(data)

    // Auto-size columns based on content
    const colWidths = Object.keys(data[0] || {}).map(key => ({
      wch: Math.max(key.length, 12)
    }))
    ws['!cols'] = colWidths

    // Create workbook and add sheet
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, options.sheetName || 'Data')

    // Write file
    XLSX.writeFile(wb, `${filename}.xlsx`)

    const ms = (performance.now?.() || Date.now()) - startedAt
    toast.success(`تم تصدير ${data.length} سجلات`)
    logActivity({ action: 'EXPORT', entityType: filename?.replace(/\.xlsx$/i, ''), format: 'XLSX', recordCount: data.length, outcome: 'success', timed_ms: Math.round(ms) })
  } catch (err) {
    const ms = (performance.now?.() || Date.now()) - startedAt
    toast.error('فشل التصدير')
    logActivity({ action: 'EXPORT', entityType: filename?.replace(/\.xlsx$/i, ''), format: 'XLSX', recordCount: Array.isArray(rows) ? rows.length : 0, outcome: 'error', timed_ms: Math.round(ms) })
     
    console.error('exportToExcel failed', err)
  }
}

