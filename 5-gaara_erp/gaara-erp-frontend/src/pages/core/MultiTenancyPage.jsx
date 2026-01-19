/**
 * Multi-Tenancy Management Page - إدارة المستأجرين
 * Gaara ERP v12
 *
 * Connected to real API via tenantService
 */

import { useState, useEffect, useCallback } from "react"
import { toast } from "sonner"
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
  Loader2,
  AlertTriangle,
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

// Import tenant service
import tenantService from "@/services/tenantService"

// Import tenant components
import { TenantUsersDialog, TenantSettingsDialog } from "@/components/tenants"

// Plan configuration
const planConfig = {
  free: { name: "مجاني", color: "secondary", name_en: "Free" },
  basic: { name: "أساسي", color: "outline", name_en: "Basic" },
  starter: { name: "مبتدئ", color: "outline", name_en: "Starter" },
  pro: { name: "احترافي", color: "default", name_en: "Professional" },
  professional: { name: "احترافي", color: "default", name_en: "Professional" },
  enterprise: { name: "مؤسسي", color: "default", name_en: "Enterprise" },
}

// Status configuration
const statusConfig = {
  active: { label: "نشط", variant: "default" },
  suspended: { label: "موقوف", variant: "destructive" },
  pending: { label: "معلق", variant: "secondary" },
  trial: { label: "تجريبي", variant: "outline" },
  cancelled: { label: "ملغي", variant: "destructive" },
  expired: { label: "منتهي", variant: "secondary" },
}

const MultiTenancyPage = () => {
  // State management
  const [tenants, setTenants] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [isTenantDialogOpen, setIsTenantDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isUsersDialogOpen, setIsUsersDialogOpen] = useState(false)
  const [isSettingsDialogOpen, setIsSettingsDialogOpen] = useState(false)
  const [selectedTenant, setSelectedTenant] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")

  const [formData, setFormData] = useState({
    name: "",
    name_ar: "",
    slug: "",
    custom_domain: "",
    plan_code: "basic",
    status: "trial",
  })

  // Load tenants on mount
  useEffect(() => {
    loadTenants()
  }, [])

  /**
   * Load tenants from API
   */
  const loadTenants = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await tenantService.getTenants()

      if (response.success) {
        // Transform API data to match component expectations
        const transformedTenants = (response.data || []).map(tenant => ({
          id: tenant.id,
          name: tenant.name,
          name_ar: tenant.name_ar,
          slug: tenant.slug,
          domain: tenant.custom_domain,
          custom_domain: tenant.custom_domain,
          plan: tenant.plan?.code || 'basic',
          plan_name: tenant.plan?.name || 'أساسي',
          status: tenant.status,
          is_active: tenant.is_active,
          users_count: tenant.stats?.users_count || 0,
          max_users: tenant.plan?.max_users || 10,
          storage_used: tenant.stats?.storage_used || 0,
          storage_limit: (tenant.plan?.max_storage_gb || 10) * 1000000000,
          created_at: tenant.created_at,
          last_activity: tenant.updated_at,
          trial_ends_at: tenant.trial_ends_at,
          subscription_ends_at: tenant.subscription_ends_at,
        }))
        setTenants(transformedTenants)
      } else {
        throw new Error(response.message_ar || response.message || 'فشل في جلب المستأجرين')
      }
    } catch (err) {
      console.error('Error loading tenants:', err)
      setError(err.message_ar || err.message || 'فشل في جلب المستأجرين')
      toast.error(err.message_ar || 'فشل في جلب المستأجرين')
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Filter tenants based on search and status
  const filteredTenants = tenants.filter(tenant => {
    const searchLower = searchQuery.toLowerCase()
    const matchesSearch = !searchQuery ||
      tenant.name?.toLowerCase().includes(searchLower) ||
      tenant.name_ar?.includes(searchQuery) ||
      tenant.slug?.toLowerCase().includes(searchLower)
    const matchesStatus = statusFilter === "all" || tenant.status === statusFilter
    return matchesSearch && matchesStatus
  })

  /**
   * Handle save (create or update)
   */
  const handleSave = async () => {
    setIsSaving(true)

    try {
      if (dialogMode === "add") {
        // Create new tenant
        const response = await tenantService.createTenant({
          name: formData.name,
          name_ar: formData.name_ar || formData.name,
          slug: formData.slug,
          custom_domain: formData.custom_domain || null,
          plan_code: formData.plan_code,
        })

        if (response.success) {
          toast.success(response.message_ar || "تم إضافة المستأجر بنجاح")
          loadTenants() // Refresh list
        } else {
          throw new Error(response.message_ar || response.message)
        }
      } else {
        // Update existing tenant
        const response = await tenantService.updateTenant(selectedTenant.id, {
          name: formData.name,
          name_ar: formData.name_ar,
          custom_domain: formData.custom_domain || null,
        })

        if (response.success) {
          toast.success(response.message_ar || "تم تحديث المستأجر بنجاح")
          loadTenants() // Refresh list
        } else {
          throw new Error(response.message_ar || response.message)
        }
      }

      setIsTenantDialogOpen(false)
      resetForm()
    } catch (err) {
      console.error('Error saving tenant:', err)
      toast.error(err.message_ar || err.message || "حدث خطأ أثناء الحفظ")
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Handle delete (deactivate)
   */
  const handleDelete = async () => {
    setIsSaving(true)

    try {
      const response = await tenantService.deleteTenant(
        selectedTenant.id,
        "User requested deletion"
      )

      if (response.success) {
        toast.success(response.message_ar || "تم حذف المستأجر بنجاح")
        loadTenants() // Refresh list
      } else {
        throw new Error(response.message_ar || response.message)
      }

      setIsDeleteDialogOpen(false)
      setSelectedTenant(null)
    } catch (err) {
      console.error('Error deleting tenant:', err)
      toast.error(err.message_ar || err.message || "حدث خطأ أثناء الحذف")
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Reset form to defaults
   */
  const resetForm = () => {
    setFormData({
      name: "",
      name_ar: "",
      slug: "",
      custom_domain: "",
      plan_code: "basic",
      status: "trial",
    })
  }

  /**
   * Open edit dialog with tenant data
   */
  const openEditDialog = (tenant) => {
    setSelectedTenant(tenant)
    setDialogMode("edit")
    setFormData({
      name: tenant.name || "",
      name_ar: tenant.name_ar || "",
      slug: tenant.slug || "",
      custom_domain: tenant.custom_domain || tenant.domain || "",
      plan_code: tenant.plan || "basic",
      status: tenant.status || "active",
    })
    setIsTenantDialogOpen(true)
  }

  /**
   * Open add dialog
   */
  const openAddDialog = () => {
    setSelectedTenant(null)
    setDialogMode("add")
    resetForm()
    setIsTenantDialogOpen(true)
  }

  /**
   * Toggle tenant status (activate/suspend)
   */
  const handleToggleStatus = async (tenant) => {
    const newStatus = tenant.status === 'active' ? 'suspended' : 'active'
    const actionText = newStatus === 'active' ? 'تفعيل' : 'إيقاف'

    try {
      const response = await tenantService.updateTenant(tenant.id, { status: newStatus })

      if (response.success) {
        toast.success(`تم ${actionText} المستأجر بنجاح`)
        loadTenants()
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (err) {
      console.error('Error toggling status:', err)
      toast.error(err.message_ar || err.message || `فشل في ${actionText} المستأجر`)
    }
  }

  /**
   * Generate slug from name
   */
  const generateSlug = (name) => {
    return name
      .toLowerCase()
      .replace(/[أإآا]/g, 'a')
      .replace(/[ي]/g, 'y')
      .replace(/[و]/g, 'w')
      .replace(/[ة]/g, 'h')
      .replace(/[\u0600-\u06FF]/g, '') // Remove remaining Arabic
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 50)
  }

  /**
   * Format storage bytes to human readable
   */
  const formatStorage = (bytes) => {
    if (!bytes) return "0 MB"
    const gb = bytes / 1000000000
    return gb >= 1 ? `${gb.toFixed(1)} GB` : `${(bytes / 1000000).toFixed(0)} MB`
  }

  /**
   * Get plan display info
   */
  const getPlanInfo = (planCode) => {
    return planConfig[planCode] || planConfig.basic
  }

  /**
   * Get status display info
   */
  const getStatusInfo = (status) => {
    return statusConfig[status] || statusConfig.pending
  }

  // Table columns definition
  const columns = [
    {
      accessorKey: "name",
      header: "المستأجر",
      cell: ({ row }) => {
        const isActive = row.original.status === "active" || row.original.status === "trial"
        return (
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${isActive ? "bg-green-100 dark:bg-green-900" : "bg-red-100 dark:bg-red-900"}`}>
              <Building className={`w-5 h-5 ${isActive ? "text-green-600" : "text-red-600"}`} />
            </div>
            <div>
              <p className="font-medium">{row.original.name_ar || row.original.name}</p>
              <p className="text-sm text-muted-foreground">{row.original.slug}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "plan",
      header: "الخطة",
      cell: ({ row }) => {
        const planInfo = getPlanInfo(row.original.plan)
        return <Badge variant={planInfo.color}>{planInfo.name}</Badge>
      }
    },
    {
      accessorKey: "users",
      header: "المستخدمين",
      cell: ({ row }) => {
        const usersCount = row.original.users_count || 0
        const maxUsers = row.original.max_users || 10
        const percentage = maxUsers > 0 ? (usersCount / maxUsers) * 100 : 0
        return (
          <div className="w-24">
            <div className="flex justify-between text-xs mb-1">
              <span>{usersCount}</span>
              <span className="text-muted-foreground">/ {maxUsers}</span>
            </div>
            <Progress value={percentage} className="h-1.5" />
          </div>
        )
      },
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const statusInfo = getStatusInfo(row.original.status)
        return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>
      }
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm">
              <MoreVertical className="w-4 h-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48">
            <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => { setSelectedTenant(row.original); setIsViewDialogOpen(true); }}>
              <Eye className="w-4 h-4 ml-2" />عرض التفاصيل
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => openEditDialog(row.original)}>
              <Edit className="w-4 h-4 ml-2" />تعديل البيانات
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => { setSelectedTenant(row.original); setIsUsersDialogOpen(true); }}>
              <Users className="w-4 h-4 ml-2" />إدارة المستخدمين
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => { setSelectedTenant(row.original); setIsSettingsDialogOpen(true); }}>
              <Database className="w-4 h-4 ml-2" />إعدادات المستأجر
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onClick={() => handleToggleStatus(row.original)}
              className={row.original.status === 'active' ? 'text-orange-600' : 'text-green-600'}
            >
              {row.original.status === 'active' ? (
                <><XCircle className="w-4 h-4 ml-2" />إيقاف مؤقت</>
              ) : (
                <><CheckCircle2 className="w-4 h-4 ml-2" />تفعيل</>
              )}
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={() => { setSelectedTenant(row.original); setIsDeleteDialogOpen(true); }}
              className="text-red-600"
            >
              <Trash2 className="w-4 h-4 ml-2" />تعطيل نهائي
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  // Calculate statistics
  const stats = {
    total: tenants.length,
    active: tenants.filter(t => t.status === "active" || t.status === "trial").length,
    totalUsers: tenants.reduce((sum, t) => sum + (t.users_count || 0), 0),
    totalStorage: tenants.reduce((sum, t) => sum + (t.storage_used || 0), 0)
  }

  // Show error state
  if (error && tenants.length === 0) {
    return (
      <div className="space-y-6">
        <Card className="border-red-200 bg-red-50 dark:bg-red-900/20">
          <CardContent className="p-6 flex flex-col items-center gap-4">
            <AlertTriangle className="w-12 h-12 text-red-500" />
            <h3 className="text-lg font-semibold text-red-700 dark:text-red-300">خطأ في تحميل البيانات</h3>
            <p className="text-red-600 dark:text-red-400">{error}</p>
            <Button onClick={loadTenants} variant="outline">
              <RefreshCw className="w-4 h-4 ml-2" />إعادة المحاولة
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Building className="w-7 h-7 text-cyan-500" />
            إدارة المستأجرين
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المنظمات والشركات المستأجرة للنظام</p>
        </div>
        <Button onClick={openAddDialog} disabled={isLoading}>
          <Plus className="w-4 h-4 ml-2" />إضافة مستأجر
        </Button>
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

      {/* Add/Edit Dialog */}
      <Dialog open={isTenantDialogOpen} onOpenChange={setIsTenantDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{dialogMode === "add" ? "إضافة مستأجر جديد" : "تعديل المستأجر"}</DialogTitle>
            <DialogDescription>
              {dialogMode === "add" ? "أدخل بيانات المستأجر الجديد" : "قم بتعديل بيانات المستأجر"}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            {/* Name fields */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">اسم المستأجر (English)</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => {
                    const name = e.target.value
                    setFormData({
                      ...formData,
                      name,
                      slug: dialogMode === "add" ? generateSlug(name) : formData.slug
                    })
                  }}
                  placeholder="Company Name"
                  dir="ltr"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name_ar">اسم المستأجر (عربي)</Label>
                <Input
                  id="name_ar"
                  value={formData.name_ar}
                  onChange={(e) => setFormData({ ...formData, name_ar: e.target.value })}
                  placeholder="اسم الشركة"
                />
              </div>
            </div>

            {/* Slug and Domain */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="slug">المعرف الفريد (Slug)</Label>
                <Input
                  id="slug"
                  value={formData.slug}
                  onChange={(e) => setFormData({ ...formData, slug: e.target.value.toLowerCase().replace(/[^a-z0-9-]/g, '') })}
                  placeholder="company-name"
                  dir="ltr"
                  disabled={dialogMode === "edit"}
                />
                <p className="text-xs text-muted-foreground">
                  سيكون الرابط: {formData.slug || "company-name"}.gaara-erp.com
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="custom_domain">النطاق المخصص (اختياري)</Label>
                <Input
                  id="custom_domain"
                  value={formData.custom_domain}
                  onChange={(e) => setFormData({ ...formData, custom_domain: e.target.value })}
                  placeholder="erp.yourcompany.com"
                  dir="ltr"
                />
              </div>
            </div>

            {/* Plan selection (only for new tenants) */}
            {dialogMode === "add" && (
              <div className="space-y-2">
                <Label>خطة الاشتراك</Label>
                <Select
                  value={formData.plan_code}
                  onValueChange={(v) => setFormData({ ...formData, plan_code: v })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="اختر الخطة" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="free">مجاني - 5 مستخدمين</SelectItem>
                    <SelectItem value="basic">أساسي - 10 مستخدمين</SelectItem>
                    <SelectItem value="pro">احترافي - 50 مستخدم</SelectItem>
                    <SelectItem value="enterprise">مؤسسي - غير محدود</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>
          <DialogFooter className="gap-2">
            <Button
              variant="outline"
              onClick={() => setIsTenantDialogOpen(false)}
              disabled={isSaving}
            >
              إلغاء
            </Button>
            <Button onClick={handleSave} disabled={isSaving || !formData.name || !formData.slug}>
              {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
              {dialogMode === "add" ? "إضافة" : "حفظ التغييرات"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* View Details Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>تفاصيل المستأجر</DialogTitle>
          </DialogHeader>
          {selectedTenant && (
            <div className="space-y-4">
              {/* Header with name and badges */}
              <div className="flex items-center gap-4">
                <div className={`w-14 h-14 rounded-lg flex items-center justify-center ${
                  selectedTenant.status === "active" || selectedTenant.status === "trial"
                    ? "bg-green-100 dark:bg-green-900"
                    : "bg-gray-100 dark:bg-gray-800"
                }`}>
                  <Building className={`w-7 h-7 ${
                    selectedTenant.status === "active" || selectedTenant.status === "trial"
                      ? "text-green-600"
                      : "text-gray-600"
                  }`} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">{selectedTenant.name_ar || selectedTenant.name}</h3>
                  <p className="text-muted-foreground">{selectedTenant.slug}</p>
                </div>
                <div className="mr-auto flex gap-2">
                  <Badge variant={getPlanInfo(selectedTenant.plan).color}>
                    {getPlanInfo(selectedTenant.plan).name}
                  </Badge>
                  <Badge variant={getStatusInfo(selectedTenant.status).variant}>
                    {getStatusInfo(selectedTenant.status).label}
                  </Badge>
                </div>
              </div>

              <Separator />

              {/* Details grid */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1">
                    <Globe className="w-4 h-4" />النطاق
                  </p>
                  <p className="font-medium">{selectedTenant.custom_domain || selectedTenant.domain || `${selectedTenant.slug}.gaara-erp.com`}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1">
                    <Key className="w-4 h-4" />المعرف
                  </p>
                  <p className="font-medium font-mono text-xs">{selectedTenant.id}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1">
                    <Calendar className="w-4 h-4" />تاريخ الإنشاء
                  </p>
                  <p className="font-medium">{selectedTenant.created_at ? formatDate(selectedTenant.created_at, "PPP") : "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1">
                    <Calendar className="w-4 h-4" />آخر تحديث
                  </p>
                  <p className="font-medium">{selectedTenant.last_activity ? formatDate(selectedTenant.last_activity, "PPP") : "-"}</p>
                </div>
              </div>

              <Separator />

              {/* Usage stats */}
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="flex items-center gap-1">
                      <Users className="w-4 h-4" />المستخدمين
                    </span>
                    <span>{selectedTenant.users_count || 0} / {selectedTenant.max_users || 10}</span>
                  </div>
                  <Progress
                    value={selectedTenant.max_users > 0
                      ? ((selectedTenant.users_count || 0) / selectedTenant.max_users) * 100
                      : 0}
                  />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="flex items-center gap-1">
                      <Database className="w-4 h-4" />التخزين
                    </span>
                    <span>{formatStorage(selectedTenant.storage_used)} / {formatStorage(selectedTenant.storage_limit)}</span>
                  </div>
                  <Progress
                    value={selectedTenant.storage_limit > 0
                      ? ((selectedTenant.storage_used || 0) / selectedTenant.storage_limit) * 100
                      : 0}
                  />
                </div>
              </div>

              {/* Trial/Subscription info */}
              {selectedTenant.trial_ends_at && selectedTenant.status === "trial" && (
                <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                  <p className="text-sm text-yellow-800 dark:text-yellow-200">
                    <Calendar className="w-4 h-4 inline ml-1" />
                    الفترة التجريبية تنتهي في: {formatDate(selectedTenant.trial_ends_at, "PPP")}
                  </p>
                </div>
              )}
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>إغلاق</Button>
            <Button onClick={() => { setIsViewDialogOpen(false); openEditDialog(selectedTenant); }}>
              <Edit className="w-4 h-4 ml-2" />تعديل
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>تعطيل المستأجر</AlertDialogTitle>
            <AlertDialogDescription>
              هل أنت متأكد من تعطيل المستأجر "{selectedTenant?.name_ar || selectedTenant?.name}"؟
              <br /><br />
              <span className="text-yellow-600">ملاحظة: لن يتم حذف البيانات، سيتم تعطيل الحساب فقط.</span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isSaving}>إلغاء</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              className="bg-red-600 hover:bg-red-700"
              disabled={isSaving}
            >
              {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
              تعطيل
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Users Management Dialog */}
      <TenantUsersDialog
        tenant={selectedTenant}
        open={isUsersDialogOpen}
        onClose={() => {
          setIsUsersDialogOpen(false)
          setSelectedTenant(null)
        }}
        onUpdate={loadTenants}
      />

      {/* Settings Dialog */}
      <TenantSettingsDialog
        tenant={selectedTenant}
        open={isSettingsDialogOpen}
        onClose={() => {
          setIsSettingsDialogOpen(false)
          setSelectedTenant(null)
        }}
        onUpdate={loadTenants}
      />
    </div>
  )
}

export default MultiTenancyPage
