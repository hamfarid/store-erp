import { useState, useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Search,
  Filter,
  Download,
  Plus,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  MoreHorizontal,
  Edit,
  Trash2,
  Eye,
  RefreshCw,
  Loader2,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { cn } from "@/lib/utils"

const DataTable = ({
  data = [],
  columns = [],
  title,
  description,
  searchPlaceholder = "البحث...",
  searchKey = "name",
  isLoading = false,
  pageSize: initialPageSize = 10,
  showSearch = true,
  showFilter = true,
  showExport = true,
  showAdd = true,
  showRefresh = true,
  showSelection = true,
  showPagination = true,
  onAdd,
  onEdit,
  onDelete,
  onView,
  onExport,
  onRefresh,
  onRowClick,
  emptyMessage = "لا توجد بيانات",
  addButtonText = "إضافة جديد",
}) => {
  const [searchQuery, setSearchQuery] = useState("")
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" })
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(initialPageSize)
  const [selectedRows, setSelectedRows] = useState([])

  // Filter data based on search
  const filteredData = useMemo(() => {
    if (!searchQuery) return data
    return data.filter((item) => {
      const value = item[searchKey]
      if (typeof value === "string") {
        return value.toLowerCase().includes(searchQuery.toLowerCase())
      }
      return false
    })
  }, [data, searchQuery, searchKey])

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortConfig.key]
      const bVal = b[sortConfig.key]
      if (aVal < bVal) return sortConfig.direction === "asc" ? -1 : 1
      if (aVal > bVal) return sortConfig.direction === "asc" ? 1 : -1
      return 0
    })
  }, [filteredData, sortConfig])

  // Paginate data
  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * pageSize
    return sortedData.slice(start, start + pageSize)
  }, [sortedData, currentPage, pageSize])

  const totalPages = Math.ceil(sortedData.length / pageSize)

  // Handle sort
  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "asc" ? "desc" : "asc",
    }))
  }

  // Handle selection
  const handleSelectAll = (checked) => {
    if (checked) {
      setSelectedRows(paginatedData.map((item) => item.id))
    } else {
      setSelectedRows([])
    }
  }

  const handleSelectRow = (id, checked) => {
    if (checked) {
      setSelectedRows((prev) => [...prev, id])
    } else {
      setSelectedRows((prev) => prev.filter((rowId) => rowId !== id))
    }
  }

  const isAllSelected =
    paginatedData.length > 0 &&
    paginatedData.every((item) => selectedRows.includes(item.id))

  // Render sort icon
  const SortIcon = ({ columnKey }) => {
    if (sortConfig.key !== columnKey) {
      return <ArrowUpDown className="w-4 h-4 text-slate-400" />
    }
    return sortConfig.direction === "asc" ? (
      <ArrowUp className="w-4 h-4 text-primary" />
    ) : (
      <ArrowDown className="w-4 h-4 text-primary" />
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      {(title || description) && (
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            {title && (
              <h2 className="text-xl font-bold text-slate-800 dark:text-white">
                {title}
              </h2>
            )}
            {description && (
              <p className="text-sm text-muted-foreground">{description}</p>
            )}
          </div>
        </div>
      )}

      {/* Toolbar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-50 dark:bg-slate-800/50 p-4 rounded-lg">
        <div className="flex items-center gap-2 flex-1">
          {/* Search */}
          {showSearch && (
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                type="text"
                placeholder={searchPlaceholder}
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  setCurrentPage(1)
                }}
                className="pr-9 bg-white dark:bg-slate-900"
              />
            </div>
          )}

          {/* Filter Button */}
          {showFilter && (
            <Button variant="outline" size="icon">
              <Filter className="w-4 h-4" />
            </Button>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Refresh */}
          {showRefresh && onRefresh && (
            <Button
              variant="outline"
              size="icon"
              onClick={onRefresh}
              disabled={isLoading}
            >
              <RefreshCw className={cn("w-4 h-4", isLoading && "animate-spin")} />
            </Button>
          )}

          {/* Export */}
          {showExport && onExport && (
            <Button variant="outline" onClick={onExport}>
              <Download className="w-4 h-4 ml-2" />
              تصدير
            </Button>
          )}

          {/* Add Button */}
          {showAdd && onAdd && (
            <Button onClick={onAdd} className="bg-primary hover:bg-primary/90">
              <Plus className="w-4 h-4 ml-2" />
              {addButtonText}
            </Button>
          )}
        </div>
      </div>

      {/* Selected count */}
      {selectedRows.length > 0 && (
        <div className="flex items-center gap-4 bg-primary/10 text-primary px-4 py-2 rounded-lg">
          <span className="font-medium">
            تم تحديد {selectedRows.length} عنصر
          </span>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSelectedRows([])}
            className="text-primary hover:text-primary"
          >
            إلغاء التحديد
          </Button>
        </div>
      )}

      {/* Table */}
      <div className="border rounded-lg overflow-hidden bg-white dark:bg-slate-900">
        <Table>
          <TableHeader>
            <TableRow className="bg-slate-50 dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800">
              {showSelection && (
                <TableHead className="w-12">
                  <Checkbox
                    checked={isAllSelected}
                    onCheckedChange={handleSelectAll}
                  />
                </TableHead>
              )}
              {columns.map((column) => (
                <TableHead
                  key={column.key}
                  className={cn(
                    "font-semibold",
                    column.sortable && "cursor-pointer select-none"
                  )}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center gap-2">
                    {column.header}
                    {column.sortable && <SortIcon columnKey={column.key} />}
                  </div>
                </TableHead>
              ))}
              {(onEdit || onDelete || onView) && (
                <TableHead className="w-12 text-center">الإجراءات</TableHead>
              )}
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (showSelection ? 1 : 0) + 1}
                  className="h-40 text-center"
                >
                  <div className="flex flex-col items-center justify-center gap-2">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    <span className="text-muted-foreground">جاري التحميل...</span>
                  </div>
                </TableCell>
              </TableRow>
            ) : paginatedData.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (showSelection ? 1 : 0) + 1}
                  className="h-40 text-center text-muted-foreground"
                >
                  {emptyMessage}
                </TableCell>
              </TableRow>
            ) : (
              <AnimatePresence>
                {paginatedData.map((row, index) => (
                  <motion.tr
                    key={row.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ delay: index * 0.02 }}
                    className={cn(
                      "border-b transition-colors hover:bg-slate-50 dark:hover:bg-slate-800/50",
                      selectedRows.includes(row.id) && "bg-primary/5",
                      onRowClick && "cursor-pointer"
                    )}
                    onClick={() => onRowClick?.(row)}
                  >
                    {showSelection && (
                      <TableCell onClick={(e) => e.stopPropagation()}>
                        <Checkbox
                          checked={selectedRows.includes(row.id)}
                          onCheckedChange={(checked) =>
                            handleSelectRow(row.id, checked)
                          }
                        />
                      </TableCell>
                    )}
                    {columns.map((column) => (
                      <TableCell key={column.key}>
                        {column.render
                          ? column.render(row[column.key], row)
                          : row[column.key]}
                      </TableCell>
                    ))}
                    {(onEdit || onDelete || onView) && (
                      <TableCell onClick={(e) => e.stopPropagation()}>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            {onView && (
                              <DropdownMenuItem onClick={() => onView(row)}>
                                <Eye className="w-4 h-4 ml-2" />
                                عرض
                              </DropdownMenuItem>
                            )}
                            {onEdit && (
                              <DropdownMenuItem onClick={() => onEdit(row)}>
                                <Edit className="w-4 h-4 ml-2" />
                                تعديل
                              </DropdownMenuItem>
                            )}
                            {onDelete && (
                              <>
                                <DropdownMenuSeparator />
                                <DropdownMenuItem
                                  onClick={() => onDelete(row)}
                                  className="text-red-600 dark:text-red-400"
                                >
                                  <Trash2 className="w-4 h-4 ml-2" />
                                  حذف
                                </DropdownMenuItem>
                              </>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    )}
                  </motion.tr>
                ))}
              </AnimatePresence>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 0 && (
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>عرض</span>
            <Select
              value={pageSize.toString()}
              onValueChange={(value) => {
                setPageSize(Number(value))
                setCurrentPage(1)
              }}
            >
              <SelectTrigger className="w-16 h-8">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {[5, 10, 20, 50, 100].map((size) => (
                  <SelectItem key={size} value={size.toString()}>
                    {size}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <span>من أصل {sortedData.length} عنصر</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              صفحة {currentPage} من {totalPages}
            </span>
            <div className="flex items-center gap-1">
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8"
                onClick={() => setCurrentPage(1)}
                disabled={currentPage === 1}
              >
                <ChevronsRight className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8"
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                <ChevronRight className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8"
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
              >
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="h-8 w-8"
                onClick={() => setCurrentPage(totalPages)}
                disabled={currentPage === totalPages}
              >
                <ChevronsLeft className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DataTable
