/**
 * Data Table Component
 * =====================
 * 
 * Reusable data table with sorting, pagination, search, and actions.
 * 
 * Features:
 * - Column sorting
 * - Pagination
 * - Row selection
 * - Search/filter
 * - Row actions
 * - Loading skeleton
 * - Empty state
 * - RTL support
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useMemo } from 'react';
import {
  ChevronUp,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Search,
  MoreVertical,
  Check,
  Minus,
  RefreshCw
} from 'lucide-react';

/**
 * DataTable Component
 * 
 * @param {Object} props
 * @param {Array} props.columns - Column definitions
 * @param {Array} props.data - Table data
 * @param {boolean} props.loading - Loading state
 * @param {Object} props.pagination - Pagination config
 * @param {Function} props.onPageChange - Page change handler
 * @param {Function} props.onSort - Sort handler
 * @param {Function} props.onRowClick - Row click handler
 * @param {boolean} props.selectable - Enable row selection
 * @param {Function} props.onSelectionChange - Selection change handler
 */
const DataTable = ({
  columns = [],
  data = [],
  loading = false,
  pagination = null,
  onPageChange,
  onSort,
  onRowClick,
  selectable = false,
  onSelectionChange,
  emptyIcon: EmptyIcon,
  emptyMessage,
  emptyMessageAr,
  actions = [],
  onRefresh,
  className = ''
}) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [selectedRows, setSelectedRows] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [activeDropdown, setActiveDropdown] = useState(null);
  
  const isRTL = document.documentElement.dir === 'rtl';

  // Handle sorting
  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
    onSort?.({ key, direction });
  };

  // Handle row selection
  const handleSelectAll = () => {
    if (selectedRows.size === data.length) {
      setSelectedRows(new Set());
      onSelectionChange?.([]);
    } else {
      const allIds = new Set(data.map(row => row.id));
      setSelectedRows(allIds);
      onSelectionChange?.(data);
    }
  };

  const handleSelectRow = (row) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(row.id)) {
      newSelected.delete(row.id);
    } else {
      newSelected.add(row.id);
    }
    setSelectedRows(newSelected);
    onSelectionChange?.(data.filter(r => newSelected.has(r.id)));
  };

  // Filter data by search
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;
    
    return data.filter(row => {
      return columns.some(col => {
        const value = row[col.key];
        if (value == null) return false;
        return String(value).toLowerCase().includes(searchTerm.toLowerCase());
      });
    });
  }, [data, columns, searchTerm]);

  // Render cell value
  const renderCell = (row, column) => {
    if (column.render) {
      return column.render(row[column.key], row);
    }
    
    const value = row[column.key];
    
    // Handle different types
    if (value === null || value === undefined) {
      return <span className="text-gray-400">-</span>;
    }
    
    if (typeof value === 'boolean') {
      return value ? (
        <Check className="w-5 h-5 text-emerald-500" />
      ) : (
        <Minus className="w-5 h-5 text-gray-400" />
      );
    }
    
    return value;
  };

  // Loading skeleton
  if (loading) {
    return (
      <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden ${className}`}>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse w-64" />
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="p-4 flex gap-4">
              {columns.map((col, j) => (
                <div
                  key={j}
                  className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"
                  style={{ width: col.width || '100%' }}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    );
  }

  const displayMessage = isRTL ? (emptyMessageAr || emptyMessage) : emptyMessage;

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex flex-wrap items-center justify-between gap-4">
        {/* Search */}
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={isRTL ? 'بحث...' : 'Search...'}
            className="
              w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2
              bg-gray-100 dark:bg-gray-700 rounded-lg
              text-sm text-gray-700 dark:text-gray-200
              placeholder:text-gray-400
              focus:outline-none focus:ring-2 focus:ring-emerald-500
            "
          />
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title={isRTL ? 'تحديث' : 'Refresh'}
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          )}
          
          {selectedRows.size > 0 && actions.length > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500">
                {selectedRows.size} {isRTL ? 'محدد' : 'selected'}
              </span>
              {actions.map((action, i) => (
                <button
                  key={i}
                  onClick={() => action.onClick(Array.from(selectedRows))}
                  className={`
                    px-3 py-1.5 rounded-lg text-sm font-medium
                    ${action.variant === 'danger' 
                      ? 'text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20' 
                      : 'text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/20'
                    }
                    transition-colors
                  `}
                >
                  {isRTL ? (action.labelAr || action.label) : action.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 dark:bg-gray-900/50">
              {/* Selection column */}
              {selectable && (
                <th className="w-12 px-4 py-3">
                  <input
                    type="checkbox"
                    checked={selectedRows.size === data.length && data.length > 0}
                    onChange={handleSelectAll}
                    className="w-4 h-4 rounded border-gray-300 text-emerald-500 focus:ring-emerald-500"
                  />
                </th>
              )}
              
              {/* Data columns */}
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={`
                    px-4 py-3 text-left rtl:text-right
                    text-xs font-semibold text-gray-600 dark:text-gray-400
                    uppercase tracking-wider
                    ${column.sortable ? 'cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800' : ''}
                  `}
                  style={{ width: column.width }}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center gap-1">
                    <span>{isRTL ? (column.labelAr || column.label) : column.label}</span>
                    {column.sortable && sortConfig.key === column.key && (
                      sortConfig.direction === 'asc' 
                        ? <ChevronUp className="w-4 h-4" />
                        : <ChevronDown className="w-4 h-4" />
                    )}
                  </div>
                </th>
              ))}
              
              {/* Actions column */}
              <th className="w-12 px-4 py-3" />
            </tr>
          </thead>
          
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {filteredData.length === 0 ? (
              <tr>
                <td 
                  colSpan={columns.length + (selectable ? 2 : 1)}
                  className="px-4 py-12 text-center"
                >
                  <div className="flex flex-col items-center text-gray-500">
                    {EmptyIcon && <EmptyIcon className="w-12 h-12 mb-3 opacity-50" />}
                    <p>{displayMessage || (isRTL ? 'لا توجد بيانات' : 'No data available')}</p>
                  </div>
                </td>
              </tr>
            ) : (
              filteredData.map((row, rowIndex) => (
                <tr
                  key={row.id || rowIndex}
                  onClick={() => onRowClick?.(row)}
                  className={`
                    hover:bg-gray-50 dark:hover:bg-gray-700/50
                    ${onRowClick ? 'cursor-pointer' : ''}
                    ${selectedRows.has(row.id) ? 'bg-emerald-50/50 dark:bg-emerald-900/10' : ''}
                    transition-colors
                  `}
                >
                  {/* Selection cell */}
                  {selectable && (
                    <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={selectedRows.has(row.id)}
                        onChange={() => handleSelectRow(row)}
                        className="w-4 h-4 rounded border-gray-300 text-emerald-500 focus:ring-emerald-500"
                      />
                    </td>
                  )}
                  
                  {/* Data cells */}
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={`
                        px-4 py-3 text-sm
                        ${column.className || 'text-gray-700 dark:text-gray-200'}
                      `}
                    >
                      {renderCell(row, column)}
                    </td>
                  ))}
                  
                  {/* Row actions */}
                  <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
                    <div className="relative">
                      <button
                        onClick={() => setActiveDropdown(activeDropdown === row.id ? null : row.id)}
                        className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        <MoreVertical className="w-5 h-5 text-gray-400" />
                      </button>
                      
                      {activeDropdown === row.id && (
                        <>
                          <div
                            className="fixed inset-0 z-10"
                            onClick={() => setActiveDropdown(null)}
                          />
                          <div className={`
                            absolute z-20 top-full mt-1
                            ${isRTL ? 'left-0' : 'right-0'}
                            w-40 py-1
                            bg-white dark:bg-gray-800
                            border border-gray-200 dark:border-gray-700
                            rounded-lg shadow-lg
                          `}>
                            <button
                              onClick={() => {
                                setActiveDropdown(null);
                                onRowClick?.(row);
                              }}
                              className="w-full px-4 py-2 text-left rtl:text-right text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                            >
                              {isRTL ? 'عرض' : 'View'}
                            </button>
                            <button
                              onClick={() => {
                                setActiveDropdown(null);
                                row.onEdit?.(row);
                              }}
                              className="w-full px-4 py-2 text-left rtl:text-right text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                            >
                              {isRTL ? 'تعديل' : 'Edit'}
                            </button>
                            <button
                              onClick={() => {
                                setActiveDropdown(null);
                                row.onDelete?.(row);
                              }}
                              className="w-full px-4 py-2 text-left rtl:text-right text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
                            >
                              {isRTL ? 'حذف' : 'Delete'}
                            </button>
                          </div>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm text-gray-500">
            {isRTL 
              ? `عرض ${pagination.from || 1} - ${pagination.to || filteredData.length} من ${pagination.total || filteredData.length}`
              : `Showing ${pagination.from || 1} - ${pagination.to || filteredData.length} of ${pagination.total || filteredData.length}`
            }
          </p>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => onPageChange?.(pagination.page - 1)}
              disabled={pagination.page <= 1}
              className="
                p-2 rounded-lg
                text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-colors
              "
            >
              {isRTL ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
            </button>
            
            <span className="px-3 py-1 text-sm font-medium text-gray-700 dark:text-gray-200">
              {pagination.page} / {pagination.totalPages || 1}
            </span>
            
            <button
              onClick={() => onPageChange?.(pagination.page + 1)}
              disabled={pagination.page >= (pagination.totalPages || 1)}
              className="
                p-2 rounded-lg
                text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-colors
              "
            >
              {isRTL ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataTable;
