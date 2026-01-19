/**
 * Enhanced DataTable Component with Search, Filter, Export, Pagination
 * @file components/UI/data-table.jsx
 */

import * as React from "react";
import { cn } from "../../lib/utils";
import { Button } from "./button";
import { SearchInput } from "./input";
import { 
  ChevronLeft, 
  ChevronRight, 
  ChevronsLeft, 
  ChevronsRight,
  Download,
  Filter,
  RefreshCw,
  Plus,
  Eye,
  Pencil,
  Trash2,
  MoreHorizontal,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  FileSpreadsheet,
  Printer
} from "lucide-react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";

// Table Components
const Table = React.forwardRef(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn("w-full caption-bottom text-sm", className)}
      {...props}
    />
  </div>
));
Table.displayName = "Table";

const TableHeader = React.forwardRef(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />
));
TableHeader.displayName = "TableHeader";

const TableBody = React.forwardRef(({ className, ...props }, ref) => (
  <tbody ref={ref} className={cn("[&_tr:last-child]:border-0", className)} {...props} />
));
TableBody.displayName = "TableBody";

const TableFooter = React.forwardRef(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn("border-t bg-gray-50/50 font-medium dark:bg-gray-800/50", className)}
    {...props}
  />
));
TableFooter.displayName = "TableFooter";

const TableRow = React.forwardRef(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b border-gray-100 dark:border-gray-800 transition-colors",
      "hover:bg-gray-50/50 dark:hover:bg-gray-800/50",
      "data-[state=selected]:bg-emerald-50 dark:data-[state=selected]:bg-emerald-900/20",
      className
    )}
    {...props}
  />
));
TableRow.displayName = "TableRow";

const TableHead = React.forwardRef(({ className, sortable, sorted, onSort, children, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-12 px-4 text-right align-middle font-semibold text-gray-600 dark:text-gray-400",
      "[&:has([role=checkbox])]:pr-0",
      sortable && "cursor-pointer select-none hover:bg-gray-50 dark:hover:bg-gray-800",
      className
    )}
    onClick={sortable ? onSort : undefined}
    {...props}
  >
    <div className="flex items-center gap-2">
      {children}
      {sortable && (
        <span className="text-gray-400">
          {sorted === 'asc' ? <ArrowUp className="h-4 w-4" /> : 
           sorted === 'desc' ? <ArrowDown className="h-4 w-4" /> : 
           <ArrowUpDown className="h-4 w-4" />}
        </span>
      )}
    </div>
  </th>
));
TableHead.displayName = "TableHead";

const TableCell = React.forwardRef(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn(
      "p-4 align-middle text-gray-700 dark:text-gray-300",
      "[&:has([role=checkbox])]:pr-0",
      className
    )}
    {...props}
  />
));
TableCell.displayName = "TableCell";

// Action Buttons for each row
const TableActions = ({ onView, onEdit, onDelete, item }) => (
  <DropdownMenu.Root>
    <DropdownMenu.Trigger asChild>
      <Button variant="ghost" size="icon-sm">
        <MoreHorizontal className="h-4 w-4" />
      </Button>
    </DropdownMenu.Trigger>
    <DropdownMenu.Portal>
      <DropdownMenu.Content 
        className="min-w-[160px] bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-1 z-50"
        sideOffset={5}
        align="end"
      >
        {onView && (
          <DropdownMenu.Item 
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md cursor-pointer outline-none"
            onClick={() => onView(item)}
          >
            <Eye className="h-4 w-4" /> عرض التفاصيل
          </DropdownMenu.Item>
        )}
        {onEdit && (
          <DropdownMenu.Item 
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md cursor-pointer outline-none"
            onClick={() => onEdit(item)}
          >
            <Pencil className="h-4 w-4" /> تعديل
          </DropdownMenu.Item>
        )}
        {onDelete && (
          <>
            <DropdownMenu.Separator className="h-px bg-gray-200 dark:bg-gray-700 my-1" />
            <DropdownMenu.Item 
              className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md cursor-pointer outline-none"
              onClick={() => onDelete(item)}
            >
              <Trash2 className="h-4 w-4" /> حذف
            </DropdownMenu.Item>
          </>
        )}
      </DropdownMenu.Content>
    </DropdownMenu.Portal>
  </DropdownMenu.Root>
);

// Pagination Component
const TablePagination = ({ 
  currentPage = 1, 
  totalPages = 1, 
  totalItems = 0,
  pageSize = 10,
  onPageChange,
  onPageSizeChange 
}) => {
  const pageSizes = [10, 25, 50, 100];
  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100 dark:border-gray-800">
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-500 dark:text-gray-400">
          عرض {startItem} - {endItem} من {totalItems}
        </span>
        <select
          value={pageSize}
          onChange={(e) => onPageSizeChange?.(Number(e.target.value))}
          className="h-8 rounded-md border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm px-2"
        >
          {pageSizes.map(size => (
            <option key={size} value={size}>{size} سجل</option>
          ))}
        </select>
      </div>
      <div className="flex items-center gap-1">
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onPageChange?.(1)}
          disabled={currentPage === 1}
        >
          <ChevronsRight className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onPageChange?.(currentPage - 1)}
          disabled={currentPage === 1}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
        <span className="px-4 text-sm text-gray-600 dark:text-gray-400">
          صفحة {currentPage} من {totalPages}
        </span>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onPageChange?.(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onPageChange?.(totalPages)}
          disabled={currentPage === totalPages}
        >
          <ChevronsLeft className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};

// DataTable Toolbar
const DataTableToolbar = ({
  searchValue,
  onSearchChange,
  onAdd,
  onRefresh,
  onExport,
  onPrint,
  onFilter,
  addLabel = "إضافة جديد",
  loading = false,
  showSearch = true,
  showFilter = true,
  showExport = true,
  showPrint = true,
  customActions,
}) => (
  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
    <div className="flex items-center gap-3 w-full sm:w-auto">
      {showSearch && (
        <SearchInput
          value={searchValue}
          onChange={(e) => onSearchChange?.(e.target.value)}
          placeholder="بحث..."
          className="w-full sm:w-64"
        />
      )}
      {showFilter && (
        <Button variant="outline" size="sm" onClick={onFilter}>
          <Filter className="h-4 w-4" />
          <span className="hidden sm:inline">تصفية</span>
        </Button>
      )}
    </div>
    <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
      {onRefresh && (
        <Button variant="ghost" size="icon-sm" onClick={onRefresh} disabled={loading}>
          <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
        </Button>
      )}
      {showExport && onExport && (
        <Button variant="outline" size="sm" onClick={onExport}>
          <Download className="h-4 w-4" />
          <span className="hidden sm:inline">تصدير</span>
        </Button>
      )}
      {showPrint && onPrint && (
        <Button variant="outline" size="sm" onClick={onPrint}>
          <Printer className="h-4 w-4" />
          <span className="hidden sm:inline">طباعة</span>
        </Button>
      )}
      {customActions}
      {onAdd && (
        <Button onClick={onAdd}>
          <Plus className="h-4 w-4" />
          {addLabel}
        </Button>
      )}
    </div>
  </div>
);

// Empty State
const TableEmptyState = ({ 
  title = "لا توجد بيانات", 
  description = "لم يتم العثور على أي سجلات",
  icon: Icon = FileSpreadsheet,
  action,
  actionLabel = "إضافة جديد"
}) => (
  <div className="flex flex-col items-center justify-center py-16 text-center">
    <div className="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
      <Icon className="h-8 w-8 text-gray-400" />
    </div>
    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{title}</h3>
    <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-sm">{description}</p>
    {action && (
      <Button onClick={action}>
        <Plus className="h-4 w-4" />
        {actionLabel}
      </Button>
    )}
  </div>
);

// Loading State
const TableLoadingState = ({ rows = 5, columns = 5 }) => (
  <div className="animate-pulse">
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="flex gap-4 p-4 border-b border-gray-100 dark:border-gray-800">
        {Array.from({ length: columns }).map((_, j) => (
          <div key={j} className="h-4 bg-gray-200 dark:bg-gray-700 rounded flex-1" />
        ))}
      </div>
    ))}
  </div>
);

// Complete DataTable Component
const DataTable = ({
  columns = [],
  data = [],
  loading = false,
  searchValue = "",
  onSearchChange,
  onAdd,
  onRefresh,
  onExport,
  onPrint,
  onFilter,
  onView,
  onEdit,
  onDelete,
  pagination,
  emptyState,
  addLabel,
  showToolbar = true,
  className,
}) => {
  return (
    <div className={cn("rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden", className)}>
      {showToolbar && (
        <div className="p-4 border-b border-gray-100 dark:border-gray-800">
          <DataTableToolbar
            searchValue={searchValue}
            onSearchChange={onSearchChange}
            onAdd={onAdd}
            onRefresh={onRefresh}
            onExport={onExport}
            onPrint={onPrint}
            onFilter={onFilter}
            addLabel={addLabel}
            loading={loading}
          />
        </div>
      )}
      
      {loading ? (
        <TableLoadingState columns={columns.length} />
      ) : data.length === 0 ? (
        <TableEmptyState {...emptyState} action={onAdd} />
      ) : (
        <>
          <Table>
            <TableHeader>
              <TableRow>
                {columns.map((column, index) => (
                  <TableHead
                    key={column.key || index}
                    sortable={column.sortable}
                    sorted={column.sorted}
                    onSort={column.onSort}
                    className={column.headerClassName}
                  >
                    {column.title}
                  </TableHead>
                ))}
                {(onView || onEdit || onDelete) && (
                  <TableHead className="w-[80px]">الإجراءات</TableHead>
                )}
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((row, rowIndex) => (
                <TableRow key={row.id || rowIndex}>
                  {columns.map((column, colIndex) => (
                    <TableCell key={column.key || colIndex} className={column.cellClassName}>
                      {column.render ? column.render(row[column.key], row, rowIndex) : row[column.key]}
                    </TableCell>
                  ))}
                  {(onView || onEdit || onDelete) && (
                    <TableCell>
                      <TableActions
                        item={row}
                        onView={onView}
                        onEdit={onEdit}
                        onDelete={onDelete}
                      />
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          
          {pagination && (
            <TablePagination {...pagination} />
          )}
        </>
      )}
    </div>
  );
};

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableActions,
  TablePagination,
  DataTableToolbar,
  TableEmptyState,
  TableLoadingState,
  DataTable,
};

