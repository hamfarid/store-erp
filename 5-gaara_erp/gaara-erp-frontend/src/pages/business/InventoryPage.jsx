/**
 * Inventory Management Page - إدارة المخزون
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Package,
  Plus,
  Search,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  AlertTriangle,
  CheckCircle2,
  BarChart3,
  ArrowUpDown,
  Warehouse,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { DataTable } from "@/components/common"

const mockInventory = [
  { id: "PRD-001", name: "قمح فاخر", sku: "WHT-001", category: "حبوب", stock: 5000, minStock: 1000, unit: "كجم", warehouse: "المستودع الرئيسي", price: 15, status: "in_stock" },
  { id: "PRD-002", name: "سماد NPK", sku: "FRT-001", category: "أسمدة", stock: 250, minStock: 500, unit: "كجم", warehouse: "المستودع الفرعي", price: 45, status: "low_stock" },
  { id: "PRD-003", name: "بذور طماطم", sku: "SED-001", category: "بذور", stock: 0, minStock: 100, unit: "عبوة", warehouse: "المستودع الرئيسي", price: 120, status: "out_of_stock" },
  { id: "PRD-004", name: "مبيد حشري", sku: "PST-001", category: "مبيدات", stock: 150, minStock: 50, unit: "لتر", warehouse: "المستودع الفرعي", price: 85, status: "in_stock" },
  { id: "PRD-005", name: "شتلات فلفل", sku: "SED-002", category: "شتلات", stock: 800, minStock: 200, unit: "شتلة", warehouse: "المشتل", price: 5, status: "in_stock" },
]

const statusConfig = {
  in_stock: { label: "متوفر", variant: "default" },
  low_stock: { label: "منخفض", variant: "secondary" },
  out_of_stock: { label: "نفد", variant: "destructive" },
}

const InventoryPage = () => {
  const [inventory, setInventory] = useState(mockInventory)
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")

  const filteredInventory = inventory.filter(item => {
    const matchesSearch = item.name.includes(searchQuery) || item.sku.includes(searchQuery)
    const matchesCategory = categoryFilter === "all" || item.category === categoryFilter
    return matchesSearch && matchesCategory
  })

  const stats = {
    totalProducts: inventory.length,
    totalValue: inventory.reduce((sum, i) => sum + (i.stock * i.price), 0),
    lowStock: inventory.filter(i => i.status === "low_stock").length,
    outOfStock: inventory.filter(i => i.status === "out_of_stock").length,
  }

  const columns = [
    {
      accessorKey: "name",
      header: "المنتج",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <Package className="w-5 h-5 text-blue-500" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground font-mono">{row.original.sku}</p>
          </div>
        </div>
      ),
    },
    { accessorKey: "category", header: "التصنيف" },
    {
      accessorKey: "stock",
      header: "المخزون",
      cell: ({ row }) => (
        <div className="w-28">
          <div className="flex justify-between text-sm mb-1">
            <span>{row.original.stock}</span>
            <span className="text-muted-foreground">/ {row.original.minStock}</span>
          </div>
          <Progress 
            value={Math.min((row.original.stock / row.original.minStock) * 100, 100)} 
            className="h-2" 
          />
        </div>
      ),
    },
    { accessorKey: "warehouse", header: "المستودع" },
    {
      accessorKey: "price",
      header: "السعر",
      cell: ({ row }) => <span className="font-medium">{row.original.price} ر.س</span>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => (
        <Badge variant={statusConfig[row.original.status].variant}>
          {statusConfig[row.original.status].label}
        </Badge>
      ),
    },
    {
      id: "actions",
      header: "",
      cell: () => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem><Eye className="w-4 h-4 ml-2" />عرض</DropdownMenuItem>
            <DropdownMenuItem><Edit className="w-4 h-4 ml-2" />تعديل</DropdownMenuItem>
            <DropdownMenuItem><ArrowUpDown className="w-4 h-4 ml-2" />تحريك</DropdownMenuItem>
            <DropdownMenuItem className="text-red-600"><Trash2 className="w-4 h-4 ml-2" />حذف</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Package className="w-7 h-7 text-indigo-500" />
            إدارة المخزون
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المنتجات والمخازن</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          منتج جديد
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-indigo-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalProducts}</p>
              <p className="text-sm text-muted-foreground">منتج</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalValue / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">قيمة المخزون</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.lowStock}</p>
              <p className="text-sm text-muted-foreground">مخزون منخفض</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <Warehouse className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.outOfStock}</p>
              <p className="text-sm text-muted-foreground">نفد المخزون</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
            </div>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-[150px]"><SelectValue placeholder="التصنيف" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع التصنيفات</SelectItem>
                <SelectItem value="حبوب">حبوب</SelectItem>
                <SelectItem value="أسمدة">أسمدة</SelectItem>
                <SelectItem value="بذور">بذور</SelectItem>
                <SelectItem value="مبيدات">مبيدات</SelectItem>
                <SelectItem value="شتلات">شتلات</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>المنتجات ({filteredInventory.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredInventory} searchKey="name" />
        </CardContent>
      </Card>
    </div>
  )
}

export default InventoryPage
