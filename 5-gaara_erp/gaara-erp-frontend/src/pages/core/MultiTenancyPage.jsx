/**
 * Multi-Tenancy Management Page - إدارة المستأجرين
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Building,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Users,
  Globe,
  Database,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Key,
  Mail,
  Calendar,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Progress } from "@/components/ui/progress"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"

// Mock data
const mockTenants = [
  {
    id: 1,
    name: "شركة التقنية المتقدمة",
    slug: "advanced-tech",
    domain: "tech.gaara-erp.com",
    admin_email: "admin@advancedtech.com",
    plan: "enterprise",
    status: "active",
    users_count: 45,
    max_users: 100,
    storage_used: 2500000000,
    storage_limit: 10000000000,
    created_at: "2024-01-15T10:00:00Z",
    last_activity: "2026-01-16T10:30:00Z",
  },
  {
    id: 2,
    name: "مؤسسة الزراعة الذكية",
    slug: "smart-agri",
    domain: "agri.gaara-erp.com",
    admin_email: "admin@smartagri.com",
    plan: "professional",
    status: "active",
    users_count: 20,
    max_users: 50,
    storage_used: 1000000000,
    storage_limit: 5000000000,
    created_at: "2024-06-20T14:30:00Z",
    last_activity: "2026-01-15T18:00:00Z",
  },
  {
    id: 3,
    name: "متجر الإلكترونيات",
    slug: "electronics-store",
    domain: null,
    admin_email: "admin@electronics.com",
    plan: "starter",
    status: "suspended",
    users_count: 5,
    max_users: 10,
    storage_used: 500000000,
    storage_limit: 1000000000,
    created_at: "2025-03-10T09:00:00Z",
    last_activity: "2025-12-01T12:00:00Z",
  },
]

const planConfig = {
  free: { name: "مجاني", color: "secondary" },
  starter: { name: "مبتدئ", color: "outline" },
  professional: { name: "احترافي", color: "default" },
  enterprise: { name: "مؤسسي", color: "default" },
}

const statusConfig = {
  active: { label: "نشط", variant: "default" },
  suspended: { label: "موقوف", variant: "destructive" },
  pending: { label: "معلق", variant: "secondary" },
}

const MultiTenancyPage = () => {
  const [tenants, setTenants] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [isTenantDialogOpen, setIsTenantDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [selectedTenant, setSelectedTenant] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")

  const [formData, setFormData] = useState({
    name: "", slug: "", domain: "", admin_email: "",
    plan: "starter", status: "active", max_users: 10,
  })

  useEffect(() => {
    loadTenants()
  }, [])

  const loadTenants = async () => {
    setIsLoading(true)
    await new Promise(resolve => setTimeout(resolve, 500))
    setTenants(mockTenants)
    setIsLoading(false)
  }

  const filteredTenants = tenants.filter(tenant => {
    const matchesSearch = tenant.name.includes(searchQuery) || tenant.slug.includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || tenant.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const handleSave = () => {
    if (dialogMode === "add") {
      const newTenant = { id: Date.now(), ...formData, users_count: 0, storage_used: 0, storage_limit: 5000000000, created_at: new Date().toISOString(), last_activity: new Date().toISOString() }
      setTenants([...tenants, newTenant])
      toast.success("تم إضافة المستأجر بنجاح")
    } else {
      setTenants(tenants.map(t => t.id === selectedTenant.id ? { ...t, ...formData } : t))
      toast.success("تم تحديث المستأجر بنجاح")
    }
    setIsTenantDialogOpen(false)
    setFormData({ name: "", slug: "", domain: "", admin_email: "", plan: "starter", status: "active", max_users: 10 })
  }

  const handleDelete = () => {
    setTenants(tenants.filter(t => t.id !== selectedTenant.id))
    setIsDeleteDialogOpen(false)
    toast.success("تم حذف المستأجر بنجاح")
  }

  const openEditDialog = (tenant) => {
    setSelectedTenant(tenant)
    setDialogMode("edit")
    setFormData({ name: tenant.name, slug: tenant.slug, domain: tenant.domain || "", admin_email: tenant.admin_email, plan: tenant.plan, status: tenant.status, max_users: tenant.max_users })
    setIsTenantDialogOpen(true)
  }

  const formatStorage = (bytes) => {
    const gb = bytes / 1000000000
    return gb >= 1 ? `${gb.toFixed(1)} GB` : `${(bytes / 1000000).toFixed(0)} MB`
  }

  const columns = [
    {
      accessorKey: "name",
      header: "المستأجر",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${row.original.status === "active" ? "bg-green-100 dark:bg-green-900" : "bg-red-100 dark:bg-red-900"}`}>
            <Building className={`w-5 h-5 ${row.original.status === "active" ? "text-green-600" : "text-red-600"}`} />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground">{row.original.slug}</p>
          </div>
        </div>
      ),
    },
    { accessorKey: "plan", header: "الخطة", cell: ({ row }) => <Badge variant={planConfig[row.original.plan].color}>{planConfig[row.original.plan].name}</Badge> },
    {
      accessorKey: "users",
      header: "المستخدمين",
      cell: ({ row }) => (
        <div className="w-24">
          <div className="flex justify-between text-xs mb-1"><span>{row.original.users_count}</span><span className="text-muted-foreground">/ {row.original.max_users}</span></div>
          <Progress value={(row.original.users_count / row.original.max_users) * 100} className="h-1.5" />
        </div>
      ),
    },
    { accessorKey: "status", header: "الحالة", cell: ({ row }) => <Badge variant={statusConfig[row.original.status].variant}>{statusConfig[row.original.status].label}</Badge> },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild><Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button></DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => { setSelectedTenant(row.original); setIsViewDialogOpen(true); }}><Eye className="w-4 h-4 ml-2" />عرض</DropdownMenuItem>
            <DropdownMenuItem onClick={() => openEditDialog(row.original)}><Edit className="w-4 h-4 ml-2" />تعديل</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => { setSelectedTenant(row.original); setIsDeleteDialogOpen(true); }} className="text-red-600"><Trash2 className="w-4 h-4 ml-2" />حذف</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  const stats = { total: tenants.length, active: tenants.filter(t => t.status === "active").length, totalUsers: tenants.reduce((sum, t) => sum + t.users_count, 0), totalStorage: tenants.reduce((sum, t) => sum + t.storage_used, 0) }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2"><Building className="w-7 h-7 text-cyan-500" />إدارة المستأجرين</h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المنظمات والشركات المستأجرة للنظام</p>
        </div>
        <Button onClick={() => { setDialogMode("add"); setIsTenantDialogOpen(true); }}><Plus className="w-4 h-4 ml-2" />إضافة مستأجر</Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-cyan-100 dark:bg-cyan-900 flex items-center justify-center"><Building className="w-5 h-5 text-cyan-500" /></div><div><p className="text-2xl font-bold">{stats.total}</p><p className="text-sm text-muted-foreground">إجمالي المستأجرين</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center"><CheckCircle2 className="w-5 h-5 text-green-500" /></div><div><p className="text-2xl font-bold">{stats.active}</p><p className="text-sm text-muted-foreground">نشط</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center"><Users className="w-5 h-5 text-blue-500" /></div><div><p className="text-2xl font-bold">{stats.totalUsers}</p><p className="text-sm text-muted-foreground">إجمالي المستخدمين</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center"><Database className="w-5 h-5 text-purple-500" /></div><div><p className="text-2xl font-bold">{formatStorage(stats.totalStorage)}</p><p className="text-sm text-muted-foreground">التخزين المستخدم</p></div></CardContent></Card>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative"><Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" /><Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" /></div>
            <Select value={statusFilter} onValueChange={setStatusFilter}><SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger><SelectContent><SelectItem value="all">جميع الحالات</SelectItem><SelectItem value="active">نشط</SelectItem><SelectItem value="suspended">موقوف</SelectItem></SelectContent></Select>
            <Button variant="outline" onClick={loadTenants}><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>المستأجرون ({filteredTenants.length})</CardTitle></CardHeader>
        <CardContent><DataTable columns={columns} data={filteredTenants} isLoading={isLoading} searchKey="name" /></CardContent>
      </Card>

      <Dialog open={isTenantDialogOpen} onOpenChange={setIsTenantDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader><DialogTitle>{dialogMode === "add" ? "إضافة مستأجر جديد" : "تعديل المستأجر"}</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>اسم المستأجر</Label><Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} /></div>
              <div><Label>المعرف (Slug)</Label><Input value={formData.slug} onChange={(e) => setFormData({ ...formData, slug: e.target.value })} dir="ltr" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>البريد الإلكتروني</Label><Input type="email" value={formData.admin_email} onChange={(e) => setFormData({ ...formData, admin_email: e.target.value })} dir="ltr" /></div>
              <div><Label>النطاق</Label><Input value={formData.domain} onChange={(e) => setFormData({ ...formData, domain: e.target.value })} dir="ltr" /></div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div><Label>الخطة</Label><Select value={formData.plan} onValueChange={(v) => setFormData({ ...formData, plan: v })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="free">مجاني</SelectItem><SelectItem value="starter">مبتدئ</SelectItem><SelectItem value="professional">احترافي</SelectItem><SelectItem value="enterprise">مؤسسي</SelectItem></SelectContent></Select></div>
              <div><Label>الحالة</Label><Select value={formData.status} onValueChange={(v) => setFormData({ ...formData, status: v })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="active">نشط</SelectItem><SelectItem value="suspended">موقوف</SelectItem></SelectContent></Select></div>
              <div><Label>الحد الأقصى للمستخدمين</Label><Input type="number" value={formData.max_users} onChange={(e) => setFormData({ ...formData, max_users: parseInt(e.target.value) })} /></div>
            </div>
          </div>
          <DialogFooter><Button variant="outline" onClick={() => setIsTenantDialogOpen(false)}>إلغاء</Button><Button onClick={handleSave}>{dialogMode === "add" ? "إضافة" : "حفظ"}</Button></DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader><DialogTitle>تفاصيل المستأجر</DialogTitle></DialogHeader>
          {selectedTenant && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className={`w-14 h-14 rounded-lg flex items-center justify-center ${selectedTenant.status === "active" ? "bg-green-100" : "bg-gray-100"}`}><Building className={`w-7 h-7 ${selectedTenant.status === "active" ? "text-green-600" : "text-gray-600"}`} /></div>
                <div><h3 className="text-lg font-semibold">{selectedTenant.name}</h3><p className="text-muted-foreground">{selectedTenant.slug}</p></div>
                <div className="mr-auto flex gap-2"><Badge variant={planConfig[selectedTenant.plan].color}>{planConfig[selectedTenant.plan].name}</Badge><Badge variant={statusConfig[selectedTenant.status].variant}>{statusConfig[selectedTenant.status].label}</Badge></div>
              </div>
              <Separator />
              <div className="grid grid-cols-2 gap-4">
                <div><p className="text-sm text-muted-foreground flex items-center gap-1"><Mail className="w-4 h-4" />البريد</p><p className="font-medium">{selectedTenant.admin_email}</p></div>
                <div><p className="text-sm text-muted-foreground flex items-center gap-1"><Globe className="w-4 h-4" />النطاق</p><p className="font-medium">{selectedTenant.domain || "-"}</p></div>
                <div><p className="text-sm text-muted-foreground flex items-center gap-1"><Calendar className="w-4 h-4" />تاريخ الإنشاء</p><p className="font-medium">{formatDate(selectedTenant.created_at, "PPP")}</p></div>
                <div><p className="text-sm text-muted-foreground flex items-center gap-1"><Calendar className="w-4 h-4" />آخر نشاط</p><p className="font-medium">{formatDate(selectedTenant.last_activity, "PPP")}</p></div>
              </div>
              <Separator />
              <div className="space-y-3">
                <div><div className="flex justify-between text-sm mb-1"><span className="flex items-center gap-1"><Users className="w-4 h-4" />المستخدمين</span><span>{selectedTenant.users_count} / {selectedTenant.max_users}</span></div><Progress value={(selectedTenant.users_count / selectedTenant.max_users) * 100} /></div>
                <div><div className="flex justify-between text-sm mb-1"><span className="flex items-center gap-1"><Database className="w-4 h-4" />التخزين</span><span>{formatStorage(selectedTenant.storage_used)} / {formatStorage(selectedTenant.storage_limit)}</span></div><Progress value={(selectedTenant.storage_used / selectedTenant.storage_limit) * 100} /></div>
              </div>
            </div>
          )}
          <DialogFooter><Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>إغلاق</Button></DialogFooter>
        </DialogContent>
      </Dialog>

      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader><AlertDialogTitle>حذف المستأجر</AlertDialogTitle><AlertDialogDescription>هل أنت متأكد من حذف المستأجر "{selectedTenant?.name}"؟</AlertDialogDescription></AlertDialogHeader>
          <AlertDialogFooter><AlertDialogCancel>إلغاء</AlertDialogCancel><AlertDialogAction onClick={handleDelete} className="bg-red-600 hover:bg-red-700">حذف</AlertDialogAction></AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

export default MultiTenancyPage
