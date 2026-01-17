/**
 * P2.73: Data Table Component
 * 
 * Reusable data table with sorting, filtering, pagination, and selection.
 */

import React, { useState, useMemo, useCallback } from 'react';

// =============================================================================
// Types
// =============================================================================

export type SortDirection = 'asc' | 'desc' | null;

export interface Column<T> {
  key: keyof T | string;
  header: string;
  headerAr?: string;
  sortable?: boolean;
  filterable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: any, row: T, index: number) => React.ReactNode;
  filterType?: 'text' | 'select' | 'date' | 'number';
  filterOptions?: { value: string; label: string }[];
}

export interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  keyField: keyof T;
  
  // Pagination
  pagination?: boolean;
  pageSize?: number;
  pageSizeOptions?: number[];
  
  // Selection
  selectable?: boolean;
  selectedRows?: T[];
  onSelectionChange?: (rows: T[]) => void;
  
  // Actions
  onRowClick?: (row: T) => void;
  actions?: (row: T) => React.ReactNode;
  bulkActions?: React.ReactNode;
  
  // Styling
  striped?: boolean;
  hoverable?: boolean;
  bordered?: boolean;
  compact?: boolean;
  className?: string;
  
  // State
  loading?: boolean;
  emptyMessage?: string;
  
  // Server-side
  serverSide?: boolean;
  totalRows?: number;
  onPageChange?: (page: number, pageSize: number) => void;
  onSort?: (key: string, direction: SortDirection) => void;
  onFilter?: (filters: Record<string, any>) => void;
}

// =============================================================================
// Icons
// =============================================================================

const SortIcon: React.FC<{ direction: SortDirection }> = ({ direction }) => (
  <span className="inline-flex flex-col ml-1">
    <svg
      className={`w-3 h-3 ${direction === 'asc' ? 'text-indigo-600' : 'text-gray-300'}`}
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path d="M5 12l5-5 5 5H5z" />
    </svg>
    <svg
      className={`w-3 h-3 -mt-1 ${direction === 'desc' ? 'text-indigo-600' : 'text-gray-300'}`}
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path d="M15 8l-5 5-5-5h10z" />
    </svg>
  </span>
);

const CheckIcon: React.FC = () => (
  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  </svg>
);

// =============================================================================
// Component
// =============================================================================

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  keyField,
  pagination = true,
  pageSize: initialPageSize = 10,
  pageSizeOptions = [10, 25, 50, 100],
  selectable = false,
  selectedRows = [],
  onSelectionChange,
  onRowClick,
  actions,
  bulkActions,
  striped = true,
  hoverable = true,
  bordered = false,
  compact = false,
  className = '',
  loading = false,
  emptyMessage = 'لا توجد بيانات',
  serverSide = false,
  totalRows,
  onPageChange,
  onSort,
  onFilter,
}: DataTableProps<T>) {
  // State
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(initialPageSize);
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [selected, setSelected] = useState<Set<any>>(new Set(selectedRows.map(r => r[keyField])));

  // Filtering
  const filteredData = useMemo(() => {
    if (serverSide) return data;
    
    return data.filter(row => {
      return Object.entries(filters).every(([key, value]) => {
        if (!value) return true;
        const cellValue = String(row[key] || '').toLowerCase();
        return cellValue.includes(String(value).toLowerCase());
      });
    });
  }, [data, filters, serverSide]);

  // Sorting
  const sortedData = useMemo(() => {
    if (serverSide || !sortKey || !sortDirection) return filteredData;
    
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      
      if (aVal === bVal) return 0;
      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;
      
      const comparison = aVal < bVal ? -1 : 1;
      return sortDirection === 'asc' ? comparison : -comparison;
    });
  }, [filteredData, sortKey, sortDirection, serverSide]);

  // Pagination
  const paginatedData = useMemo(() => {
    if (serverSide) return sortedData;
    
    const start = (currentPage - 1) * pageSize;
    return sortedData.slice(start, start + pageSize);
  }, [sortedData, currentPage, pageSize, serverSide]);

  const totalPages = Math.ceil((serverSide ? totalRows || 0 : sortedData.length) / pageSize);
  const totalItems = serverSide ? totalRows || 0 : sortedData.length;

  // Handlers
  const handleSort = useCallback((key: string) => {
    let newDirection: SortDirection = 'asc';
    if (sortKey === key) {
      newDirection = sortDirection === 'asc' ? 'desc' : sortDirection === 'desc' ? null : 'asc';
    }
    
    setSortKey(newDirection ? key : null);
    setSortDirection(newDirection);
    
    if (onSort) {
      onSort(key, newDirection);
    }
  }, [sortKey, sortDirection, onSort]);

  const handleFilter = useCallback((key: string, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    setCurrentPage(1);
    
    if (onFilter) {
      onFilter(newFilters);
    }
  }, [filters, onFilter]);

  const handlePageChange = useCallback((page: number) => {
    setCurrentPage(page);
    if (onPageChange) {
      onPageChange(page, pageSize);
    }
  }, [pageSize, onPageChange]);

  const handlePageSizeChange = useCallback((newSize: number) => {
    setPageSize(newSize);
    setCurrentPage(1);
    if (onPageChange) {
      onPageChange(1, newSize);
    }
  }, [onPageChange]);

  const handleSelectAll = useCallback(() => {
    if (selected.size === paginatedData.length) {
      setSelected(new Set());
      onSelectionChange?.([]);
    } else {
      const newSelected = new Set(paginatedData.map(r => r[keyField]));
      setSelected(newSelected);
      onSelectionChange?.(paginatedData);
    }
  }, [paginatedData, selected, keyField, onSelectionChange]);

  const handleSelectRow = useCallback((row: T) => {
    const key = row[keyField];
    const newSelected = new Set(selected);
    
    if (newSelected.has(key)) {
      newSelected.delete(key);
    } else {
      newSelected.add(key);
    }
    
    setSelected(newSelected);
    onSelectionChange?.(data.filter(r => newSelected.has(r[keyField])));
  }, [selected, keyField, data, onSelectionChange]);

  const getValue = (row: T, key: string): any => {
    const keys = key.split('.');
    let value: any = row;
    for (const k of keys) {
      value = value?.[k];
    }
    return value;
  };

  // Styles
  const cellPadding = compact ? 'px-3 py-2' : 'px-4 py-3';
  const headerPadding = compact ? 'px-3 py-2' : 'px-4 py-3';

  return (
    <div className={`bg-white rounded-lg shadow ${className}`} dir="rtl">
      {/* Bulk Actions */}
      {selectable && selected.size > 0 && bulkActions && (
        <div className="px-4 py-3 bg-indigo-50 border-b flex items-center gap-4">
          <span className="text-sm text-indigo-700">
            تم تحديد {selected.size} عنصر
          </span>
          {bulkActions}
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className={`min-w-full divide-y divide-gray-200 ${bordered ? 'border' : ''}`}>
          <thead className="bg-gray-50">
            <tr>
              {selectable && (
                <th className={`${headerPadding} w-12`}>
                  <input
                    type="checkbox"
                    checked={selected.size === paginatedData.length && paginatedData.length > 0}
                    onChange={handleSelectAll}
                    className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  />
                </th>
              )}
              {columns.map(col => (
                <th
                  key={String(col.key)}
                  className={`
                    ${headerPadding} text-right text-xs font-medium text-gray-500 uppercase tracking-wider
                    ${col.sortable ? 'cursor-pointer hover:bg-gray-100 select-none' : ''}
                    ${col.width ? `w-[${col.width}]` : ''}
                  `}
                  onClick={() => col.sortable && handleSort(String(col.key))}
                >
                  <div className={`flex items-center ${col.align === 'center' ? 'justify-center' : col.align === 'left' ? 'justify-start' : 'justify-end'}`}>
                    {col.headerAr || col.header}
                    {col.sortable && (
                      <SortIcon direction={sortKey === col.key ? sortDirection : null} />
                    )}
                  </div>
                </th>
              ))}
              {actions && (
                <th className={`${headerPadding} w-24 text-center text-xs font-medium text-gray-500 uppercase`}>
                  إجراءات
                </th>
              )}
            </tr>
            
            {/* Filter Row */}
            {columns.some(c => c.filterable) && (
              <tr className="bg-gray-50">
                {selectable && <th />}
                {columns.map(col => (
                  <th key={`filter-${String(col.key)}`} className={headerPadding}>
                    {col.filterable && (
                      col.filterType === 'select' && col.filterOptions ? (
                        <select
                          value={filters[String(col.key)] || ''}
                          onChange={e => handleFilter(String(col.key), e.target.value)}
                          className="w-full text-sm border-gray-300 rounded-md"
                        >
                          <option value="">الكل</option>
                          {col.filterOptions.map(opt => (
                            <option key={opt.value} value={opt.value}>{opt.label}</option>
                          ))}
                        </select>
                      ) : (
                        <input
                          type={col.filterType === 'number' ? 'number' : col.filterType === 'date' ? 'date' : 'text'}
                          placeholder="بحث..."
                          value={filters[String(col.key)] || ''}
                          onChange={e => handleFilter(String(col.key), e.target.value)}
                          className="w-full text-sm border-gray-300 rounded-md"
                        />
                      )
                    )}
                  </th>
                ))}
                {actions && <th />}
              </tr>
            )}
          </thead>
          
          <tbody className={`bg-white divide-y divide-gray-200 ${striped ? '[&>tr:nth-child(odd)]:bg-gray-50' : ''}`}>
            {loading ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0) + (actions ? 1 : 0)} className="px-4 py-12 text-center">
                  <div className="flex justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
                  </div>
                </td>
              </tr>
            ) : paginatedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0) + (actions ? 1 : 0)} className="px-4 py-12 text-center text-gray-500">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              paginatedData.map((row, rowIndex) => (
                <tr
                  key={String(row[keyField])}
                  className={`
                    ${hoverable ? 'hover:bg-indigo-50' : ''}
                    ${onRowClick ? 'cursor-pointer' : ''}
                    ${selected.has(row[keyField]) ? 'bg-indigo-100' : ''}
                  `}
                  onClick={() => onRowClick?.(row)}
                >
                  {selectable && (
                    <td className={cellPadding} onClick={e => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={selected.has(row[keyField])}
                        onChange={() => handleSelectRow(row)}
                        className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </td>
                  )}
                  {columns.map(col => (
                    <td
                      key={String(col.key)}
                      className={`
                        ${cellPadding} text-sm text-gray-900
                        ${col.align === 'center' ? 'text-center' : col.align === 'left' ? 'text-left' : 'text-right'}
                      `}
                    >
                      {col.render
                        ? col.render(getValue(row, String(col.key)), row, rowIndex)
                        : getValue(row, String(col.key))}
                    </td>
                  ))}
                  {actions && (
                    <td className={`${cellPadding} text-center`} onClick={e => e.stopPropagation()}>
                      {actions(row)}
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && totalPages > 0 && (
        <div className="px-4 py-3 border-t flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <span>عرض</span>
            <select
              value={pageSize}
              onChange={e => handlePageSizeChange(Number(e.target.value))}
              className="border-gray-300 rounded text-sm"
            >
              {pageSizeOptions.map(size => (
                <option key={size} value={size}>{size}</option>
              ))}
            </select>
            <span>من {totalItems}</span>
          </div>
          
          <div className="flex items-center gap-1">
            <button
              onClick={() => handlePageChange(1)}
              disabled={currentPage === 1}
              className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
            
            <span className="px-3 text-sm">
              صفحة {currentPage} من {totalPages}
            </span>
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={() => handlePageChange(totalPages)}
              disabled={currentPage === totalPages}
              className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataTable;

