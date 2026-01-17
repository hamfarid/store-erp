/**
 * Sales Management Page - إدارة المبيعات
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  ShoppingCart,
  Plus,
  Search,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  DollarSign,
  TrendingUp,
  Package,
  Users,
  FileText,
  Calendar,
  CheckCircle2,
  Clock,
  XCircle,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
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

const mockSales = [
  { id: "SO-001", customer: "شركة التقنية", date: "2026-01-17", items: 5, total: 15000, status: "completed", payment: "paid" },
  { id: "SO-002", customer: "مؤسسة الزراعة", date: "2026-01-16", items: 3, total: 8500, status: "pending", payment: "pending" },
  { id: "SO-003", customer: "متجر الإلكترونيات", date: "2026-01-15", items: 8, total: 22000, status: "processing", payment: "partial" },
  { id: "SO-004", customer: "شركة البناء", date: "2026-01-14", items: 2, total: 5000, status: "cancelled", payment: "refunded" },
  { id: "SO-005", customer: "مصنع الأغذية", date: "2026-01-13", items: 12, total: 45000, status: "completed", payment: "paid" },
]

const statusConfig = {
  pending: { label: "معلق", variant: "secondary", icon: Clock },
  processing: { label: "قيد التجهيز", variant: "default", icon: Package },
  completed: { label: "مكتمل", variant: "default", icon: CheckCircle2 },
  cancelled: { label: "ملغي", variant: "destructive", icon: XCircle },
}

const paymentConfig = {
  paid: { label: "مدفوع", variant: "default" },
  pending: { label: "معلق", variant: "secondary" },
  partial: { label: "جزئي", variant: "outline" },
  refunded: { label: "مسترد", variant: "destructive" },
}

const SalesPage = () => {
  const [sales, setSales] = useState(mockSales)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredSales = sales.filter(s => {
    const matchesSearch = s.id.includes(searchQuery) || s.customer.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || s.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    totalSales: sales.reduce((sum, s) => sum + (s.status !== "cancelled" ? s.total : 0), 0),
    ordersCount: sales.filter(s => s.status !== "cancelled").length,
    pendingOrders: sales.filter(s => s.status === "pending").length,
    avgOrderValue: Math.round(sales.reduce((sum, s) => sum + s.total, 0) / sales.length),
  }

  const columns = [
    {
      accessorKey: "id",
      header: "رقم الطلب",
      cell: ({ row }) => <span className="font-mono font-medium">{row.original.id}</span>,
    },
    { accessorKey: "customer", header: "العميل" },
    { accessorKey: "date", header: "التاريخ" },
    { accessorKey: "items", header: "العناصر" },
    {
      accessorKey: "total",
      header: "الإجمالي",
      cell: ({ row }) => <span className="font-medium">{row.original.total.toLocaleString()} ر.س</span>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <Badge variant={config.variant}>
            <Icon className="w-3 h-3 ml-1" />
            {config.label}
          </Badge>
        )
      },
    },
    {
      accessorKey: "payment",
      header: "الدفع",
      cell: ({ row }) => (
        <Badge variant={paymentConfig[row.original.payment].variant}>
          {paymentConfig[row.original.payment].label}
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
            <DropdownMenuItem><FileText className="w-4 h-4 ml-2" />فاتورة</DropdownMenuItem>
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
            <ShoppingCart className="w-7 h-7 text-blue-500" />
            إدارة المبيعات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة أوامر البيع والفواتير</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          طلب بيع جديد
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalSales / 1000).toFixed(0)}K</p>
              <p className="text-sm text-muted-foreground">إجمالي المبيعات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.ordersCount}</p>
              <p className="text-sm text-muted-foreground">طلب</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.pendingOrders}</p>
              <p className="text-sm text-muted-foreground">معلق</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.avgOrderValue.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">متوسط الطلب</p>
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
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="pending">معلق</SelectItem>
                <SelectItem value="processing">قيد التجهيز</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
                <SelectItem value="cancelled">ملغي</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>أوامر البيع ({filteredSales.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredSales} searchKey="id" />
        </CardContent>
      </Card>
    </div>
  )
}

export default SalesPage
