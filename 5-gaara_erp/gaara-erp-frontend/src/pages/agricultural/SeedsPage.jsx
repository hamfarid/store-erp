/**
 * Seeds Management Page - إدارة البذور
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Wheat,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Package,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Dna,
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

const mockSeeds = [
  { id: 1, name: "قمح سخا 94", category: "حبوب", origin: "محلي", stock: 5000, unit: "كجم", purity: 98.5, germination: 95, expiryDate: "2026-06-01", status: "available" },
  { id: 2, name: "طماطم هجين GS-12", category: "خضروات", origin: "هولندا", stock: 250, unit: "كجم", purity: 99.2, germination: 92, expiryDate: "2025-12-15", status: "low_stock" },
  { id: 3, name: "ذرة هجين 10", category: "حبوب", origin: "محلي", stock: 8000, unit: "كجم", purity: 97.8, germination: 94, expiryDate: "2026-09-01", status: "available" },
  { id: 4, name: "فلفل كاليفورنيا", category: "خضروات", origin: "إسبانيا", stock: 50, unit: "كجم", purity: 98.0, germination: 88, expiryDate: "2025-08-01", status: "expired" },
  { id: 5, name: "برسيم حجازي", category: "علف", origin: "محلي", stock: 12000, unit: "كجم", purity: 96.5, germination: 90, expiryDate: "2026-03-01", status: "available" },
]

const statusConfig = {
  available: { label: "متاح", variant: "default" },
  low_stock: { label: "مخزون منخفض", variant: "secondary" },
  expired: { label: "منتهي الصلاحية", variant: "destructive" },
  reserved: { label: "محجوز", variant: "outline" },
}

const SeedsPage = () => {
  const [seeds, setSeeds] = useState(mockSeeds)
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")

  const filteredSeeds = seeds.filter(s => {
    const matchesSearch = s.name.includes(searchQuery)
    const matchesCategory = categoryFilter === "all" || s.category === categoryFilter
    return matchesSearch && matchesCategory
  })

  const stats = {
    total: seeds.length,
    totalStock: seeds.reduce((sum, s) => sum + s.stock, 0),
    lowStock: seeds.filter(s => s.status === "low_stock").length,
    expired: seeds.filter(s => s.status === "expired").length,
  }

  const columns = [
    {
      accessorKey: "name",
      header: "البذور",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
            <Wheat className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground">{row.original.category}</p>
          </div>
        </div>
      ),
    },
    { accessorKey: "origin", header: "المصدر" },
    {
      accessorKey: "stock",
      header: "المخزون",
      cell: ({ row }) => <span>{row.original.stock.toLocaleString()} {row.original.unit}</span>,
    },
    {
      accessorKey: "quality",
      header: "الجودة",
      cell: ({ row }) => (
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">النقاوة:</span>
            <Progress value={row.original.purity} className="w-16 h-2" />
            <span>{row.original.purity}%</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">الإنبات:</span>
            <Progress value={row.original.germination} className="w-16 h-2" />
            <span>{row.original.germination}%</span>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "expiryDate",
      header: "تاريخ الصلاحية",
      cell: ({ row }) => <span className="text-sm">{row.original.expiryDate}</span>,
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
            <Wheat className="w-7 h-7 text-amber-500" />
            إدارة البذور
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة مخزون البذور والتقاوي</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          إضافة بذور
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <Dna className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">صنف بذور</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalStock / 1000).toFixed(1)}K</p>
              <p className="text-sm text-muted-foreground">كجم مخزون</p>
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
              <Calendar className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.expired}</p>
              <p className="text-sm text-muted-foreground">منتهي الصلاحية</p>
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
                <SelectItem value="خضروات">خضروات</SelectItem>
                <SelectItem value="علف">علف</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>سجل البذور ({filteredSeeds.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredSeeds} searchKey="name" />
        </CardContent>
      </Card>
    </div>
  )
}

export default SeedsPage
