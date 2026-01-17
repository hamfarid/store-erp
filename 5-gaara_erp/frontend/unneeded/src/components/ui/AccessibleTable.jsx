// FILE: frontend/src/components/ui/AccessibleTable.jsx | PURPOSE: WCAG AA Compliant Table Component | OWNER: Frontend | RELATED: accessibility.css | LAST-AUDITED: 2025-10-21

import React, { useState, useRef, useEffect } from 'react';
import { cn } from '../../lib/utils';

/**
 * Accessible Table Component - WCAG AA Compliant
 * 
 * P2 Fixes Applied:
 * - P2.1: Proper table structure with headers
 * - P2.2: Keyboard navigation support
 * - P2.3: Screen reader compatibility
 * - P2.4: RTL language support
 */

export const AccessibleTable = ({ 
  data = [], 
  columns = [], 
  caption,
  sortable = false,
  selectable = false,
  onRowSelect,
  onSort,
  className,
  ...props 
}) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [selectedRows, setSelectedRows] = useState(new Set());
  const [focusedCell, setFocusedCell] = useState({ row: -1, col: -1 });
  const tableRef = useRef(null);

  // Handle sorting
  const handleSort = (columnKey) => {
    if (!sortable) return;
    
    let direction = 'asc';
    if (sortConfig.key === columnKey && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    
    setSortConfig({ key: columnKey, direction });
    onSort?.({ key: columnKey, direction });
  };

  // Handle row selection
  const handleRowSelect = (rowIndex, isSelected) => {
    if (!selectable) return;
    
    const newSelectedRows = new Set(selectedRows);
    if (isSelected) {
      newSelectedRows.add(rowIndex);
    } else {
      newSelectedRows.delete(rowIndex);
    }
    
    setSelectedRows(newSelectedRows);
    onRowSelect?.(Array.from(newSelectedRows));
  };

  // Handle select all
  const handleSelectAll = (isSelected) => {
    if (!selectable) return;
    
    const newSelectedRows = isSelected ? new Set(data.map((_, index) => index)) : new Set();
    setSelectedRows(newSelectedRows);
    onRowSelect?.(Array.from(newSelectedRows));
  };

  // Keyboard navigation
  const handleKeyDown = (e, rowIndex, colIndex) => {
    const rowCount = data.length;
    const colCount = columns.length + (selectable ? 1 : 0);
    
    switch (e.key) {
      case 'ArrowUp':
        e.preventDefault();
        setFocusedCell({ 
          row: Math.max(0, rowIndex - 1), 
          col: colIndex 
        });
        break;
      case 'ArrowDown':
        e.preventDefault();
        setFocusedCell({ 
          row: Math.min(rowCount - 1, rowIndex + 1), 
          col: colIndex 
        });
        break;
      case 'ArrowLeft':
        e.preventDefault();
        setFocusedCell({ 
          row: rowIndex, 
          col: Math.max(0, colIndex - 1) 
        });
        break;
      case 'ArrowRight':
        e.preventDefault();
        setFocusedCell({ 
          row: rowIndex, 
          col: Math.min(colCount - 1, colIndex + 1) 
        });
        break;
      case 'Home':
        e.preventDefault();
        setFocusedCell({ row: rowIndex, col: 0 });
        break;
      case 'End':
        e.preventDefault();
        setFocusedCell({ row: rowIndex, col: colCount - 1 });
        break;
      case 'Space':
        if (selectable && colIndex === 0) {
          e.preventDefault();
          handleRowSelect(rowIndex, !selectedRows.has(rowIndex));
        }
        break;
    }
  };

  // Focus management
  useEffect(() => {
    if (focusedCell.row >= 0 && focusedCell.col >= 0) {
      const cell = tableRef.current?.querySelector(
        `[data-row="${focusedCell.row}"][data-col="${focusedCell.col}"]`
      );
      cell?.focus();
    }
  }, [focusedCell]);

  const isAllSelected = selectedRows.size === data.length && data.length > 0;
  const isIndeterminate = selectedRows.size > 0 && selectedRows.size < data.length;

  return (
    <div className="overflow-x-auto">
      <table 
        ref={tableRef}
        className={cn("table-accessible", className)}
        role="table"
        aria-label={caption}
        {...props}
      >
        {caption && (
          <caption className="sr-only">
            {caption}
          </caption>
        )}
        
        <thead>
          <tr role="row">
            {selectable && (
              <th 
                scope="col" 
                className="w-12"
                role="columnheader"
              >
                <input
                  type="checkbox"
                  checked={isAllSelected}
                  ref={(el) => {
                    if (el) el.indeterminate = isIndeterminate;
                  }}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                  aria-label="تحديد جميع الصفوف"
                  className="h-4 w-4 rounded border-2 border-input"
                />
              </th>
            )}
            
            {columns.map((column, colIndex) => (
              <th
                key={column.key}
                scope="col"
                role="columnheader"
                aria-sort={
                  sortConfig.key === column.key 
                    ? sortConfig.direction === 'asc' ? 'ascending' : 'descending'
                    : sortable ? 'none' : undefined
                }
                className={cn(
                  sortable && "cursor-pointer hover:bg-muted/50",
                  column.align === 'center' && "text-center",
                  column.align === 'left' && "text-left"
                )}
                onClick={() => sortable && handleSort(column.key)}
                onKeyDown={(e) => {
                  if (sortable && (e.key === 'Enter' || e.key === ' ')) {
                    e.preventDefault();
                    handleSort(column.key);
                  }
                }}
                tabIndex={sortable ? 0 : -1}
              >
                <div className="flex items-center justify-between">
                  {column.header}
                  {sortable && (
                    <span className="mr-2" aria-hidden="true">
                      {sortConfig.key === column.key ? (
                        sortConfig.direction === 'asc' ? '↑' : '↓'
                      ) : (
                        '↕'
                      )}
                    </span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        
        <tbody>
          {data.map((row, rowIndex) => (
            <tr 
              key={rowIndex}
              role="row"
              className={cn(
                "hover:bg-accent",
                selectedRows.has(rowIndex) && "bg-muted"
              )}
            >
              {selectable && (
                <td 
                  role="gridcell"
                  data-row={rowIndex}
                  data-col={0}
                  tabIndex={focusedCell.row === rowIndex && focusedCell.col === 0 ? 0 : -1}
                  onKeyDown={(e) => handleKeyDown(e, rowIndex, 0)}
                >
                  <input
                    type="checkbox"
                    checked={selectedRows.has(rowIndex)}
                    onChange={(e) => handleRowSelect(rowIndex, e.target.checked)}
                    aria-label={`تحديد الصف ${rowIndex + 1}`}
                    className="h-4 w-4 rounded border-2 border-input"
                  />
                </td>
              )}
              
              {columns.map((column, colIndex) => {
                const actualColIndex = selectable ? colIndex + 1 : colIndex;
                const cellValue = row[column.key];
                
                return (
                  <td
                    key={column.key}
                    role="gridcell"
                    data-row={rowIndex}
                    data-col={actualColIndex}
                    tabIndex={focusedCell.row === rowIndex && focusedCell.col === actualColIndex ? 0 : -1}
                    onKeyDown={(e) => handleKeyDown(e, rowIndex, actualColIndex)}
                    className={cn(
                      "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
                      column.align === 'center' && "text-center",
                      column.align === 'left' && "text-left"
                    )}
                    aria-describedby={column.description ? `${column.key}-desc` : undefined}
                  >
                    {column.render ? column.render(cellValue, row, rowIndex) : cellValue}
                  </td>
                );
              })}
            </tr>
          ))}
          
          {data.length === 0 && (
            <tr>
              <td 
                colSpan={columns.length + (selectable ? 1 : 0)}
                className="text-center py-8 text-muted-foreground"
                role="gridcell"
              >
                لا توجد بيانات للعرض
              </td>
            </tr>
          )}
        </tbody>
      </table>
      
      {/* Hidden descriptions for screen readers */}
      {columns.map((column) => 
        column.description && (
          <div 
            key={`${column.key}-desc`}
            id={`${column.key}-desc`} 
            className="sr-only"
          >
            {column.description}
          </div>
        )
      )}
    </div>
  );
};

// Table pagination component
export const TablePagination = ({
  currentPage = 1,
  totalPages = 1,
  totalItems = 0,
  itemsPerPage = 10,
  onPageChange,
  onItemsPerPageChange,
  className
}) => {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);
  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className={cn("flex items-center justify-between px-2 py-4", className)}>
      <div className="text-sm text-muted-foreground">
        عرض {startItem} إلى {endItem} من {totalItems} عنصر
      </div>
      
      <div className="flex items-center space-x-2 space-x-reverse">
        <button
          onClick={() => onPageChange?.(currentPage - 1)}
          disabled={currentPage <= 1}
          className="btn-accessible h-8 w-8 p-0"
          aria-label="الصفحة السابقة"
        >
          ←
        </button>
        
        {pages.map((page) => (
          <button
            key={page}
            onClick={() => onPageChange?.(page)}
            className={cn(
              "btn-accessible h-8 w-8 p-0",
              page === currentPage && "bg-primary text-primary-foreground"
            )}
            aria-label={`الصفحة ${page}`}
            aria-current={page === currentPage ? "page" : undefined}
          >
            {page}
          </button>
        ))}
        
        <button
          onClick={() => onPageChange?.(currentPage + 1)}
          disabled={currentPage >= totalPages}
          className="btn-accessible h-8 w-8 p-0"
          aria-label="الصفحة التالية"
        >
          →
        </button>
      </div>
    </div>
  );
};

export default AccessibleTable;
