import React, { useState, useMemo, useEffect, useCallback } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, Columns, ChevronUp, ChevronDown, ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight
} from 'lucide-react'
import EmptyState from './EmptyState'

const AdvancedTable = ({
  data = [], 
  columns = [], 
  searchable = true,
  filterable = true,
  sortable = true,
  exportable = true,
  selectable = false,
  actions = [],
  pageSize = 10,
  loading = false,
  onRowClick = null,
  onSelectionChange = null,
  className = "",
  title = "",
  subtitle = ""
}) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' })
  const [currentPage, setCurrentPage] = useState(1)
  const [filters, setFilters] = useState({})
  const [showFilters, setShowFilters] = useState(false)
  const [selectedRows, setSelectedRows] = useState(new Set())
  const [showColumnSettings, setShowColumnSettings] = useState(false)
  const [visibleColumns, setVisibleColumns] = useState(
    columns.reduce((acc, col) => ({ ...acc, [col.key]: true }), {})
  )

  // تصفية وبحث البيانات
  const filteredData = useMemo(() => {
    let filtered = [...data]

    // البحث
    if (searchTerm) {
      filtered = filtered.filter(item =>
        columns.some(column => {
          if (!visibleColumns[column.key]) return false
          const value = item[column.key]
          return value && value.toString().toLowerCase().includes(searchTerm.toLowerCase())
        })
      )
    }

    // التصفية
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        filtered = filtered.filter(item => {
          const value = item[key]
          if (typeof filters[key] === 'string') {
            return value && value.toString().toLowerCase().includes(filters[key].toLowerCase())
          }
          return value === filters[key]
        })
      }
    })

    return filtered
  }, [data, searchTerm, filters, columns, visibleColumns])

  // ترتيب البيانات
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData

    return [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key]
      const bValue = b[sortConfig.key]

      if (aValue === null || aValue === undefined) return 1
      if (bValue === null || bValue === undefined) return -1

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue
      }

      const aString = aValue.toString().toLowerCase()
      const bString = bValue.toString().toLowerCase()

      if (aString < bString) return sortConfig.direction === 'asc' ? -1 : 1
      if (aString > bString) return sortConfig.direction === 'asc' ? 1 : -1
      return 0
    })
  }, [filteredData, sortConfig])

  // ترقيم البيانات
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize
    return sortedData.slice(startIndex, startIndex + pageSize)
  }, [sortedData, currentPage, pageSize])

  const totalPages = Math.ceil(sortedData.length / pageSize)

  // معالجة الترتيب
  const handleSort = useCallback((key) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }))
  }, [])

  // معالجة اختيار الصفوف
  const handleRowSelect = useCallback((rowId, checked) => {
    setSelectedRows(prev => {
      const newSelection = new Set(prev)
      if (checked) {
        newSelection.add(rowId)
      } else {
        newSelection.delete(rowId)
      }
      
      if (onSelectionChange) {
        onSelectionChange(Array.from(newSelection))
      }
      
      return newSelection
    })
  }, [onSelectionChange])

  // اختيار جميع الصفوف
  const handleSelectAll = useCallback((checked) => {
    if (checked) {
      const allIds = paginatedData.map(item => item.id)
      setSelectedRows(new Set(allIds))
      if (onSelectionChange) {
        onSelectionChange(allIds)
      }
    } else {
      setSelectedRows(new Set())
      if (onSelectionChange) {
        onSelectionChange([])
      }
    }
  }, [paginatedData, onSelectionChange])

  // تصدير البيانات
  const handleExport = useCallback(() => {
    const csvContent = [
      columns.filter(col => visibleColumns[col.key]).map(col => col.header).join(','),
      ...sortedData.map(row => 
        columns.filter(col => visibleColumns[col.key]).map(col => {
          const value = row[col.key]
          return typeof value === 'string' && value.includes(',') 
            ? `"${value}"` 
            : value
        }).join(',')
      )
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${title || 'data'}.csv`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }, [sortedData, columns, visibleColumns, title])

  // تبديل رؤية العمود
  const toggleColumnVisibility = useCallback((columnKey) => {
    setVisibleColumns(prev => ({
      ...prev,
      [columnKey]: !prev[columnKey]
    }))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="w-6 h-6 animate-spin text-primary-600" />
        <span className="mr-2 text-muted-foreground">جاري التحميل...</span>
      </div>
    )
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-border ${className}`} dir="rtl">
      {/* Header */}
      {(title || subtitle || searchable || filterable || exportable) && (
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between">
            <div>
              {title && <h3 className="text-lg font-semibold text-foreground">{title}</h3>}
              {subtitle && <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>}
            </div>
            
            <div className="flex items-center space-x-2 space-x-reverse">
              {/* البحث */}
              {searchable && (
                <div className="relative">
                  <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="البحث..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-3 pr-10 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              )}

              {/* التصفية */}
              {filterable && (
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className={`p-2 border border-border rounded-lg hover:bg-muted/50 transition-colors ${
                    showFilters ? 'bg-primary-50 border-primary-300 text-primary-600' : ''
                  }`}
                >
                  <Filter className="w-4 h-4" />
                </button>
              )}

              {/* إعدادات الأعمدة */}
              <button
                onClick={() => setShowColumnSettings(!showColumnSettings)}
                className="p-2 border border-border rounded-lg hover:bg-muted/50 transition-colors"
              >
                <Columns className="w-4 h-4" />
              </button>

              {/* التصدير */}
              {exportable && (
                <button
                  onClick={handleExport}
                  className="p-2 border border-border rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <Download className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>

          {/* فلاتر متقدمة */}
          {showFilters && (
            <div className="mt-4 p-4 bg-muted/50 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {columns.filter(col => col.filterable).map(column => (
                  <div key={column.key}>
                    <label className="block text-sm font-medium text-foreground mb-1">
                      {column.header}
                    </label>
                    <input
                      type="text"
                      placeholder={`فلترة ${column.header}...`}
                      value={filters[column.key] || ''}
                      onChange={(e) => setFilters(prev => ({
                        ...prev,
                        [column.key]: e.target.value
                      }))}
                      className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* إعدادات الأعمدة */}
          {showColumnSettings && (
            <div className="mt-4 p-4 bg-muted/50 rounded-lg">
              <h4 className="text-sm font-medium text-foreground mb-3">إعدادات الأعمدة</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {columns.map(column => (
                  <label key={column.key} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={visibleColumns[column.key]}
                      onChange={() => toggleColumnVisibility(column.key)}
                      className="rounded border-border text-primary-600 focus:ring-primary-500"
                    />
                    <span className="mr-2 text-sm text-foreground">{column.header}</span>
                  </label>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* الجدول */}
      <div className="overflow-x-auto">
        <table className="w-full" data-testid="products-table">
          <thead className="bg-muted/50">
            <tr>
              {selectable && (
                <th className="px-4 py-3 text-right">
                  <input
                    type="checkbox"
                    checked={selectedRows.size === paginatedData.length && paginatedData.length > 0}
                    onChange={(e) => handleSelectAll(e.target.checked)}
                    className="rounded border-border text-primary-600 focus:ring-primary-500"
                  />
                </th>
              )}
              
              {columns.filter(col => visibleColumns[col.key]).map(column => (
                <th
                  key={column.key}
                  className={`px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider ${
                    sortable && column.sortable ? 'cursor-pointer hover:bg-muted' : ''
                  }`}
                  onClick={() => sortable && column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center justify-between">
                    <span>{column.header}</span>
                    {sortable && column.sortable && (
                      <div className="flex flex-col">
                        <ChevronUp 
                          className={`w-3 h-3 ${
                            sortConfig.key === column.key && sortConfig.direction === 'asc'
                              ? 'text-primary-600' 
                              : 'text-gray-400'
                          }`} 
                        />
                        <ChevronDown 
                          className={`w-3 h-3 -mt-1 ${
                            sortConfig.key === column.key && sortConfig.direction === 'desc'
                              ? 'text-primary-600' 
                              : 'text-gray-400'
                          }`} 
                        />
                      </div>
                    )}
                  </div>
                </th>
              ))}
              
              {actions.length > 0 && (
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الإجراءات
                </th>
              )}
            </tr>
          </thead>
          
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((item, index) => (
              <tr 
                key={item.id || index}
                className={`hover:bg-muted/50 transition-colors ${
                  onRowClick ? 'cursor-pointer' : ''
                } ${selectedRows.has(item.id) ? 'bg-primary-50' : ''}`}
                onClick={() => onRowClick && onRowClick(item)}
              >
                {selectable && (
                  <td className="px-4 py-3">
                    <input
                      type="checkbox"
                      checked={selectedRows.has(item.id)}
                      onChange={(e) => {
                        e.stopPropagation()
                        handleRowSelect(item.id, e.target.checked)
                      }}
                      className="rounded border-border text-primary-600 focus:ring-primary-500"
                    />
                  </td>
                )}
                
                {columns.filter(col => visibleColumns[col.key]).map(column => (
                  <td key={column.key} className="px-4 py-3 text-sm text-foreground">
                    {column.render ? column.render(item[column.key], item) : item[column.key]}
                  </td>
                ))}
                
                {actions.length > 0 && (
                  <td className="px-4 py-3 text-sm">
                    <div className="flex items-center space-x-2 space-x-reverse">
                      {actions.map((action, actionIndex) => {
                        const Icon = action.icon
                        return (
                          <button
                            key={actionIndex}
                            onClick={(e) => {
                              e.stopPropagation()
                              action.onClick(item)
                            }}
                            className={`p-1 rounded hover:bg-muted transition-colors ${action.className || ''}`}
                            title={action.label}
                          >
                            <Icon className="w-4 h-4" />
                          </button>
                        )
                      })}
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* التنقل بين الصفحات */}
      {totalPages > 1 && (
        <div className="px-4 py-3 border-t border-border flex items-center justify-between">
          <div className="text-sm text-foreground">
            عرض {((currentPage - 1) * pageSize) + 1} إلى {Math.min(currentPage * pageSize, sortedData.length)} من {sortedData.length} نتيجة
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={() => setCurrentPage(1)}
              disabled={currentPage === 1}
              className="p-2 border border-border rounded-lg hover:bg-muted/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronsRight className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="p-2 border border-border rounded-lg hover:bg-muted/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
            
            <span className="px-3 py-2 text-sm text-foreground">
              صفحة {currentPage} من {totalPages}
            </span>
            
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="p-2 border border-border rounded-lg hover:bg-muted/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setCurrentPage(totalPages)}
              disabled={currentPage === totalPages}
              className="p-2 border border-border rounded-lg hover:bg-muted/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronsLeft className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* رسالة عدم وجود بيانات */}
      {paginatedData.length === 0 && !loading && (
        <EmptyState
          icon="package"
          title={searchTerm ? 'لا توجد نتائج' : 'لا توجد بيانات'}
          description={
            searchTerm
              ? `لم يتم العثور على نتائج تطابق "${searchTerm}". جرب البحث بكلمات مختلفة.`
              : 'لم يتم إضافة أي بيانات بعد. ابدأ بإضافة البيانات باستخدام الأزرار أعلاه.'
          }
          showAction={false}
        />
      )}
    </div>
  )
}

export default AdvancedTable

