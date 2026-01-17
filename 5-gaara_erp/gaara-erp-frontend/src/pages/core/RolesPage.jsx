/**
 * Roles Management Page - إدارة الأدوار
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Shield,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Users,
  Lock,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Settings,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"

import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"

// Form schema
const roleSchema = z.object({
  name: z.string().min(2, "اسم الدور يجب أن يكون على الأقل حرفين"),
  name_ar: z.string().min(2, "الاسم بالعربية يجب أن يكون على الأقل حرفين"),
  code: z.string().min(2, "الكود يجب أن يكون على الأقل حرفين"),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
  is_system: z.boolean().default(false),
})

// Mock data
const mockRoles = [
  {
    id: 1,
    name: "Super Admin",
    name_ar: "مدير النظام",
    code: "SUPER_ADMIN",
    description: "صلاحيات كاملة على النظام",
    is_active: true,
    is_system: true,
    users_count: 2,
    permissions_count: 150,
    created_at: "2024-01-01T00:00:00Z",
  },
  {
    id: 2,
    name: "Admin",
    name_ar: "مدير",
    code: "ADMIN",
    description: "صلاحيات إدارية متقدمة",
    is_active: true,
    is_system: true,
    users_count: 5,
    permissions_count: 100,
    created_at: "2024-01-01T00:00:00Z",
  },
  {
    id: 3,
    name: "Manager",
    name_ar: "مشرف",
    code: "MANAGER",
    description: "صلاحيات إشرافية",
    is_active: true,
    is_system: false,
    users_count: 10,
    permissions_count: 50,
    created_at: "2024-02-15T10:00:00Z",
  },
  {
    id: 4,
    name: "User",
    name_ar: "مستخدم",
    code: "USER",
    description: "صلاحيات المستخدم العادي",
    is_active: true,
    is_system: true,
    users_count: 50,
    permissions_count: 20,
    created_at: "2024-01-01T00:00:00Z",
  },
  {
    id: 5,
    name: "Accountant",
    name_ar: "محاسب",
    code: "ACCOUNTANT",
    description: "صلاحيات المحاسبة والمالية",
    is_active: true,
    is_system: false,
    users_count: 8,
    permissions_count: 35,
    created_at: "2024-03-01T09:00:00Z",
  },
]

const mockPermissions = [
  { id: 1, name: "عرض المستخدمين", code: "users.view", module: "users" },
  { id: 2, name: "إضافة مستخدم", code: "users.create", module: "users" },
  { id: 3, name: "تعديل مستخدم", code: "users.update", module: "users" },
  { id: 4, name: "حذف مستخدم", code: "users.delete", module: "users" },
  { id: 5, name: "عرض الشركات", code: "companies.view", module: "companies" },
  { id: 6, name: "إضافة شركة", code: "companies.create", module: "companies" },
  { id: 7, name: "تعديل شركة", code: "companies.update", module: "companies" },
  { id: 8, name: "حذف شركة", code: "companies.delete", module: "companies" },
  { id: 9, name: "عرض المخزون", code: "inventory.view", module: "inventory" },
  { id: 10, name: "إدارة المخزون", code: "inventory.manage", module: "inventory" },
  { id: 11, name: "عرض التقارير", code: "reports.view", module: "reports" },
  { id: 12, name: "تصدير التقارير", code: "reports.export", module: "reports" },
]

const RolesPage = () => {
  const [roles, setRoles] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  
  // Dialog states
  const [isRoleDialogOpen, setIsRoleDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isPermissionsDialogOpen, setIsPermissionsDialogOpen] = useState(false)
  const [selectedRole, setSelectedRole] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [selectedPermissions, setSelectedPermissions] = useState([])

  // Form
  const form = useForm({
    resolver: zodResolver(roleSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      code: "",
      description: "",
      is_active: true,
      is_system: false,
    },
  })

  useEffect(() => {
    loadRoles()
  }, [])

  const loadRoles = async () => {
    setIsLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setRoles(mockRoles)
    } catch (error) {
      toast.error("فشل تحميل الأدوار")
    } finally {
      setIsLoading(false)
    }
  }

  // Filter roles
  const filteredRoles = roles.filter((role) => {
    const matchesSearch =
      role.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      role.name_ar.includes(searchQuery) ||
      role.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || 
      (statusFilter === "active" && role.is_active) ||
      (statusFilter === "inactive" && !role.is_active)
    return matchesSearch && matchesStatus
  })

  const handleAddRole = async (data) => {
    try {
      const newRole = {
        id: roles.length + 1,
        ...data,
        users_count: 0,
        permissions_count: 0,
        created_at: new Date().toISOString(),
      }
      setRoles([...roles, newRole])
      setIsRoleDialogOpen(false)
      form.reset()
      toast.success("تم إضافة الدور بنجاح")
    } catch (error) {
      toast.error("فشل إضافة الدور")
    }
  }

  const handleEditRole = async (data) => {
    try {
      setRoles(roles.map((r) => (r.id === selectedRole.id ? { ...r, ...data } : r)))
      setIsRoleDialogOpen(false)
      setSelectedRole(null)
      form.reset()
      toast.success("تم تحديث الدور بنجاح")
    } catch (error) {
      toast.error("فشل تحديث الدور")
    }
  }

  const handleDelete = async () => {
    try {
      if (selectedRole.is_system) {
        toast.error("لا يمكن حذف دور النظام")
        return
      }
      setRoles(roles.filter((r) => r.id !== selectedRole.id))
      setIsDeleteDialogOpen(false)
      setSelectedRole(null)
      toast.success("تم حذف الدور بنجاح")
    } catch (error) {
      toast.error("فشل حذف الدور")
    }
  }

  const handleSavePermissions = () => {
    toast.success("تم حفظ الصلاحيات بنجاح")
    setIsPermissionsDialogOpen(false)
  }

  const openEditDialog = (role) => {
    setSelectedRole(role)
    setDialogMode("edit")
    form.reset({
      name: role.name,
      name_ar: role.name_ar,
      code: role.code,
      description: role.description || "",
      is_active: role.is_active,
      is_system: role.is_system,
    })
    setIsRoleDialogOpen(true)
  }

  const openAddDialog = () => {
    setSelectedRole(null)
    setDialogMode("add")
    form.reset()
    setIsRoleDialogOpen(true)
  }

  const openPermissionsDialog = (role) => {
    setSelectedRole(role)
    setSelectedPermissions(mockPermissions.slice(0, role.permissions_count / 10).map(p => p.id))
    setIsPermissionsDialogOpen(true)
  }

  const togglePermission = (permissionId) => {
    setSelectedPermissions(prev => 
      prev.includes(permissionId) 
        ? prev.filter(id => id !== permissionId)
        : [...prev, permissionId]
    )
  }

  // Group permissions by module
  const groupedPermissions = mockPermissions.reduce((acc, permission) => {
    if (!acc[permission.module]) {
      acc[permission.module] = []
    }
    acc[permission.module].push(permission)
    return acc
  }, {})

  const moduleLabels = {
    users: "المستخدمين",
    companies: "الشركات",
    inventory: "المخزون",
    reports: "التقارير",
  }

  // Table columns
  const columns = [
    {
      accessorKey: "role",
      header: "الدور",
      cell: ({ row }) => {
        const role = row.original
        return (
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              role.is_system ? "bg-purple-100 dark:bg-purple-900" : "bg-blue-100 dark:bg-blue-900"
            }`}>
              <Shield className={`w-5 h-5 ${
                role.is_system ? "text-purple-600 dark:text-purple-400" : "text-blue-600 dark:text-blue-400"
              }`} />
            </div>
            <div>
              <p className="font-medium">{role.name}</p>
              <p className="text-sm text-muted-foreground">{role.name_ar}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "code",
      header: "الكود",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.code}</Badge>
      ),
    },
    {
      accessorKey: "users_count",
      header: "المستخدمين",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Users className="w-4 h-4 text-muted-foreground" />
          {row.original.users_count}
        </div>
      ),
    },
    {
      accessorKey: "permissions_count",
      header: "الصلاحيات",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Lock className="w-4 h-4 text-muted-foreground" />
          {row.original.permissions_count}
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const role = row.original
        return (
          <div className="flex items-center gap-2">
            <Badge variant={role.is_active ? "default" : "secondary"}>
              {role.is_active ? (
                <CheckCircle2 className="w-3 h-3 ml-1" />
              ) : (
                <XCircle className="w-3 h-3 ml-1" />
              )}
              {role.is_active ? "نشط" : "غير نشط"}
            </Badge>
            {role.is_system && (
              <Badge variant="outline" className="text-purple-600">
                نظام
              </Badge>
            )}
          </div>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const role = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => openPermissionsDialog(role)}>
                <Lock className="w-4 h-4 ml-2" />
                إدارة الصلاحيات
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(role)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              {!role.is_system && (
                <>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => { setSelectedRole(role); setIsDeleteDialogOpen(true); }}
                    className="text-red-600"
                  >
                    <Trash2 className="w-4 h-4 ml-2" />
                    حذف
                  </DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Stats
  const stats = {
    total: roles.length,
    active: roles.filter(r => r.is_active).length,
    system: roles.filter(r => r.is_system).length,
    totalUsers: roles.reduce((sum, r) => sum + r.users_count, 0),
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Shield className="w-7 h-7 text-purple-500" />
            إدارة الأدوار
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة أدوار المستخدمين وصلاحياتهم
          </p>
        </div>
        <Button onClick={openAddDialog}>
          <Plus className="w-4 h-4 ml-2" />
          إضافة دور
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Shield className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي الأدوار</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.active}</p>
              <p className="text-sm text-muted-foreground">أدوار نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Settings className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.system}</p>
              <p className="text-sm text-muted-foreground">أدوار النظام</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Users className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalUsers}</p>
              <p className="text-sm text-muted-foreground">إجمالي المستخدمين</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="بحث في الأدوار..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="الحالة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="active">نشط</SelectItem>
                <SelectItem value="inactive">غير نشط</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={loadRoles}>
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Roles Table */}
      <Card>
        <CardHeader>
          <CardTitle>الأدوار ({filteredRoles.length})</CardTitle>
          <CardDescription>قائمة جميع الأدوار المتاحة في النظام</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={filteredRoles}
            isLoading={isLoading}
            searchKey="name"
            defaultPageSize={10}
          />
        </CardContent>
      </Card>

      {/* Role Dialog */}
      <Dialog open={isRoleDialogOpen} onOpenChange={setIsRoleDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {dialogMode === "add" ? "إضافة دور جديد" : "تعديل الدور"}
            </DialogTitle>
            <DialogDescription>
              {dialogMode === "add" ? "أدخل معلومات الدور الجديد" : "تعديل معلومات الدور"}
            </DialogDescription>
          </DialogHeader>
          <form
            onSubmit={form.handleSubmit(dialogMode === "add" ? handleAddRole : handleEditRole)}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">اسم الدور (إنجليزي)</Label>
                <Input id="name" {...form.register("name")} />
                {form.formState.errors.name && (
                  <p className="text-sm text-red-500 mt-1">{form.formState.errors.name.message}</p>
                )}
              </div>
              <div>
                <Label htmlFor="name_ar">اسم الدور (عربي)</Label>
                <Input id="name_ar" {...form.register("name_ar")} />
                {form.formState.errors.name_ar && (
                  <p className="text-sm text-red-500 mt-1">{form.formState.errors.name_ar.message}</p>
                )}
              </div>
            </div>
            <div>
              <Label htmlFor="code">الكود</Label>
              <Input id="code" {...form.register("code")} />
              {form.formState.errors.code && (
                <p className="text-sm text-red-500 mt-1">{form.formState.errors.code.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="description">الوصف</Label>
              <Textarea id="description" {...form.register("description")} />
            </div>
            <div className="flex items-center space-x-2 space-x-reverse">
              <Checkbox
                id="is_active"
                checked={form.watch("is_active")}
                onCheckedChange={(checked) => form.setValue("is_active", checked)}
              />
              <Label htmlFor="is_active">دور نشط</Label>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsRoleDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">{dialogMode === "add" ? "إضافة" : "حفظ"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Permissions Dialog */}
      <Dialog open={isPermissionsDialogOpen} onOpenChange={setIsPermissionsDialogOpen}>
        <DialogContent className="max-w-3xl max-h-[90vh]">
          <DialogHeader>
            <DialogTitle>إدارة صلاحيات: {selectedRole?.name_ar}</DialogTitle>
            <DialogDescription>
              تحديد الصلاحيات المتاحة لهذا الدور
            </DialogDescription>
          </DialogHeader>
          <ScrollArea className="h-[400px] pr-4">
            <div className="space-y-6">
              {Object.entries(groupedPermissions).map(([module, permissions]) => (
                <div key={module} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-lg">{moduleLabels[module] || module}</h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        const modulePermissionIds = permissions.map(p => p.id)
                        const allSelected = modulePermissionIds.every(id => selectedPermissions.includes(id))
                        if (allSelected) {
                          setSelectedPermissions(prev => prev.filter(id => !modulePermissionIds.includes(id)))
                        } else {
                          setSelectedPermissions(prev => [...new Set([...prev, ...modulePermissionIds])])
                        }
                      }}
                    >
                      تحديد الكل
                    </Button>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {permissions.map((permission) => (
                      <div
                        key={permission.id}
                        className={`flex items-center space-x-2 space-x-reverse p-3 rounded-lg border cursor-pointer transition-colors ${
                          selectedPermissions.includes(permission.id)
                            ? "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
                            : "hover:bg-muted"
                        }`}
                        onClick={() => togglePermission(permission.id)}
                      >
                        <Checkbox
                          checked={selectedPermissions.includes(permission.id)}
                          onCheckedChange={() => togglePermission(permission.id)}
                        />
                        <div>
                          <p className="font-medium text-sm">{permission.name}</p>
                          <p className="text-xs text-muted-foreground">{permission.code}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  <Separator />
                </div>
              ))}
            </div>
          </ScrollArea>
          <div className="flex items-center justify-between pt-4 border-t">
            <p className="text-sm text-muted-foreground">
              تم تحديد {selectedPermissions.length} صلاحية
            </p>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setIsPermissionsDialogOpen(false)}>
                إلغاء
              </Button>
              <Button onClick={handleSavePermissions}>
                <Lock className="w-4 h-4 ml-2" />
                حفظ الصلاحيات
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>هل أنت متأكد؟</AlertDialogTitle>
            <AlertDialogDescription>
              سيتم حذف الدور "{selectedRole?.name_ar}" بشكل دائم.
              {selectedRole?.users_count > 0 && (
                <span className="block mt-2 text-red-600">
                  تحذير: يوجد {selectedRole?.users_count} مستخدم مرتبط بهذا الدور.
                </span>
              )}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              حذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

export default RolesPage
