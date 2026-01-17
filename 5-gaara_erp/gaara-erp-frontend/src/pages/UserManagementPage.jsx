import { useState, useEffect, useMemo } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Users,
  UserPlus,
  Search,
  Filter,
  MoreVertical,
  Edit,
  Trash2,
  Shield,
  ShieldCheck,
  UserX,
  UserCheck,
  Key,
  Mail,
  Phone,
  Calendar,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Download,
  Upload,
  Eye,
  EyeOff,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
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
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"

import { DataTable } from "@/components/common"
import { formatDate, getInitials } from "@/lib/utils"
import { mockUsers } from "@/services/users"

// Form schemas
const userSchema = z.object({
  firstName: z.string().min(2, "الاسم الأول يجب أن يكون على الأقل حرفين"),
  lastName: z.string().min(2, "اسم العائلة يجب أن يكون على الأقل حرفين"),
  email: z.string().email("البريد الإلكتروني غير صحيح"),
  phone: z.string().min(10, "رقم الهاتف غير صحيح"),
  role: z.string().min(1, "يجب اختيار الدور"),
  status: z.enum(["active", "inactive"]),
  password: z.string().min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل").optional(),
})

const passwordResetSchema = z.object({
  password: z.string().min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

const UserManagementPage = () => {
  const location = useLocation()
  const [users, setUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [selectedUsers, setSelectedUsers] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [roleFilter, setRoleFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isPasswordDialogOpen, setIsPasswordDialogOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [showPassword, setShowPassword] = useState(false)

  // Form hooks
  const userForm = useForm({
    resolver: zodResolver(userSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      phone: "",
      role: "",
      status: "active",
      password: "",
    },
  })

  const passwordForm = useForm({
    resolver: zodResolver(passwordResetSchema),
    defaultValues: {
      password: "",
      confirmPassword: "",
    },
  })

  // Load users
  useEffect(() => {
    loadUsers()
  }, [])

  // Filter users
  useEffect(() => {
    let filtered = [...users]

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (user) =>
          user.firstName.toLowerCase().includes(query) ||
          user.lastName.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query) ||
          user.phone.includes(query)
      )
    }

    // Role filter
    if (roleFilter !== "all") {
      filtered = filtered.filter((user) => user.role === roleFilter)
    }

    // Status filter
    if (statusFilter !== "all") {
      filtered = filtered.filter((user) => user.status === statusFilter)
    }

    setFilteredUsers(filtered)
  }, [users, searchQuery, roleFilter, statusFilter])

  const loadUsers = async () => {
    setIsLoading(true)
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 500))
      setUsers(mockUsers)
      setFilteredUsers(mockUsers)
    } catch (error) {
      toast.error("فشل تحميل المستخدمين")
    } finally {
      setIsLoading(false)
    }
  }

  // Handle add user
  const handleAddUser = async (data) => {
    try {
      const newUser = {
        id: users.length + 1,
        ...data,
        lastLogin: null,
        createdAt: new Date().toISOString(),
        avatar: null,
        permissions: [],
      }
      setUsers([...users, newUser])
      setIsAddDialogOpen(false)
      userForm.reset()
      toast.success("تم إضافة المستخدم بنجاح")
    } catch (error) {
      toast.error("فشل إضافة المستخدم")
    }
  }

  // Handle edit user
  const handleEditUser = async (data) => {
    try {
      setUsers(
        users.map((user) => (user.id === selectedUser.id ? { ...user, ...data } : user))
      )
      setIsEditDialogOpen(false)
      setSelectedUser(null)
      userForm.reset()
      toast.success("تم تحديث المستخدم بنجاح")
    } catch (error) {
      toast.error("فشل تحديث المستخدم")
    }
  }

  // Handle delete user
  const handleDeleteUser = async () => {
    try {
      setUsers(users.filter((user) => user.id !== selectedUser.id))
      setIsDeleteDialogOpen(false)
      setSelectedUser(null)
      toast.success("تم حذف المستخدم بنجاح")
    } catch (error) {
      toast.error("فشل حذف المستخدم")
    }
  }

  // Handle toggle status
  const handleToggleStatus = async (user) => {
    try {
      setUsers(
        users.map((u) =>
          u.id === user.id ? { ...u, status: u.status === "active" ? "inactive" : "active" } : u
        )
      )
      toast.success(`تم ${user.status === "active" ? "تعطيل" : "تفعيل"} المستخدم`)
    } catch (error) {
      toast.error("فشل تحديث حالة المستخدم")
    }
  }

  // Handle reset password
  const handleResetPassword = async (data) => {
    try {
      setIsPasswordDialogOpen(false)
      passwordForm.reset()
      toast.success("تم إعادة تعيين كلمة المرور بنجاح")
    } catch (error) {
      toast.error("فشل إعادة تعيين كلمة المرور")
    }
  }

  // Open edit dialog
  const openEditDialog = (user) => {
    setSelectedUser(user)
    userForm.reset({
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
      phone: user.phone,
      role: user.role,
      status: user.status,
    })
    setIsEditDialogOpen(true)
  }

  // Open delete dialog
  const openDeleteDialog = (user) => {
    setSelectedUser(user)
    setIsDeleteDialogOpen(true)
  }

  // Open password reset dialog
  const openPasswordDialog = (user) => {
    setSelectedUser(user)
    setIsPasswordDialogOpen(true)
  }

  // Role labels
  const roleLabels = {
    admin: "مدير",
    manager: "مدير فرع",
    accountant: "محاسب",
    user: "مستخدم",
  }

  // Status labels
  const statusLabels = {
    active: "نشط",
    inactive: "معطل",
  }

  // Table columns
  const columns = [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={table.getIsAllPageRowsSelected()}
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
        />
      ),
    },
    {
      accessorKey: "user",
      header: "المستخدم",
      cell: ({ row }) => {
        const user = row.original
        return (
          <div className="flex items-center gap-3">
            <Avatar>
              <AvatarImage src={user.avatar} />
              <AvatarFallback>{getInitials(user.firstName, user.lastName)}</AvatarFallback>
            </Avatar>
            <div>
              <p className="font-medium">
                {user.firstName} {user.lastName}
              </p>
              <p className="text-sm text-muted-foreground">{user.email}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "role",
      header: "الدور",
      cell: ({ row }) => (
        <Badge variant="outline">{roleLabels[row.original.role] || row.original.role}</Badge>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        return (
          <Badge variant={status === "active" ? "default" : "secondary"}>
            {status === "active" ? (
              <CheckCircle2 className="w-3 h-3 ml-1" />
            ) : (
              <XCircle className="w-3 h-3 ml-1" />
            )}
            {statusLabels[status]}
          </Badge>
        )
      },
    },
    {
      accessorKey: "lastLogin",
      header: "آخر تسجيل دخول",
      cell: ({ row }) => {
        const date = row.original.lastLogin
        return date ? formatDate(date) : "لم يسجل دخول"
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const user = row.original
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
              <DropdownMenuItem onClick={() => openEditDialog(user)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openPasswordDialog(user)}>
                <Key className="w-4 h-4 ml-2" />
                إعادة تعيين كلمة المرور
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleToggleStatus(user)}>
                {user.status === "active" ? (
                  <>
                    <UserX className="w-4 h-4 ml-2" />
                    تعطيل
                  </>
                ) : (
                  <>
                    <UserCheck className="w-4 h-4 ml-2" />
                    تفعيل
                  </>
                )}
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => openDeleteDialog(user)} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />
                حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Users className="w-7 h-7 text-blue-500" />
            إدارة المستخدمين
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة المستخدمين والأدوار والصلاحيات
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button variant="outline" size="sm">
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </Button>
          <Button onClick={() => setIsAddDialogOpen(true)}>
            <UserPlus className="w-4 h-4 ml-2" />
            إضافة مستخدم
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="بحث عن مستخدم..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            <Select value={roleFilter} onValueChange={setRoleFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="الدور" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الأدوار</SelectItem>
                <SelectItem value="admin">مدير</SelectItem>
                <SelectItem value="manager">مدير فرع</SelectItem>
                <SelectItem value="accountant">محاسب</SelectItem>
                <SelectItem value="user">مستخدم</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="الحالة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="active">نشط</SelectItem>
                <SelectItem value="inactive">معطل</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={loadUsers}>
              <RefreshCw className="w-4 h-4 ml-2" />
              تحديث
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>المستخدمون ({filteredUsers.length})</CardTitle>
          <CardDescription>قائمة جميع المستخدمين في النظام</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={filteredUsers}
            isLoading={isLoading}
            searchKey="email"
            defaultPageSize={10}
          />
        </CardContent>
      </Card>

      {/* Add User Dialog */}
      <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>إضافة مستخدم جديد</DialogTitle>
            <DialogDescription>أدخل معلومات المستخدم الجديد</DialogDescription>
          </DialogHeader>
          <form onSubmit={userForm.handleSubmit(handleAddUser)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">الاسم الأول</Label>
                <Input
                  id="firstName"
                  aria-invalid={!!userForm.formState.errors.firstName}
                  {...userForm.register("firstName")}
                />
                {userForm.formState.errors.firstName && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.firstName.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="lastName">اسم العائلة</Label>
                <Input
                  id="lastName"
                  aria-invalid={!!userForm.formState.errors.lastName}
                  {...userForm.register("lastName")}
                />
                {userForm.formState.errors.lastName && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.lastName.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="email">البريد الإلكتروني</Label>
                <Input
                  id="email"
                  type="email"
                  aria-invalid={!!userForm.formState.errors.email}
                  {...userForm.register("email")}
                />
                {userForm.formState.errors.email && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.email.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="phone">رقم الهاتف</Label>
                <Input
                  id="phone"
                  aria-invalid={!!userForm.formState.errors.phone}
                  {...userForm.register("phone")}
                />
                {userForm.formState.errors.phone && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.phone.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="role">الدور</Label>
                <Select
                  value={userForm.watch("role")}
                  onValueChange={(value) => userForm.setValue("role", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="اختر الدور" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">مدير</SelectItem>
                    <SelectItem value="manager">مدير فرع</SelectItem>
                    <SelectItem value="accountant">محاسب</SelectItem>
                    <SelectItem value="user">مستخدم</SelectItem>
                  </SelectContent>
                </Select>
                {userForm.formState.errors.role && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.role.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="status">الحالة</Label>
                <Select
                  value={userForm.watch("status")}
                  onValueChange={(value) => userForm.setValue("status", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">معطل</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label htmlFor="password">كلمة المرور</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  aria-invalid={!!userForm.formState.errors.password}
                  {...userForm.register("password")}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute left-2 top-1/2 -translate-y-1/2"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </Button>
              </div>
              {userForm.formState.errors.password && (
                <p className="text-sm text-red-500 mt-1">
                  {userForm.formState.errors.password.message}
                </p>
              )}
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">إضافة</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Edit User Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>تعديل مستخدم</DialogTitle>
            <DialogDescription>تعديل معلومات المستخدم</DialogDescription>
          </DialogHeader>
          <form onSubmit={userForm.handleSubmit(handleEditUser)} className="space-y-4">
            {/* Same form fields as add dialog */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="edit-firstName">الاسم الأول</Label>
                <Input
                  id="edit-firstName"
                  aria-invalid={!!userForm.formState.errors.firstName}
                  {...userForm.register("firstName")}
                />
                {userForm.formState.errors.firstName && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.firstName.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="edit-lastName">اسم العائلة</Label>
                <Input
                  id="edit-lastName"
                  aria-invalid={!!userForm.formState.errors.lastName}
                  {...userForm.register("lastName")}
                />
                {userForm.formState.errors.lastName && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.lastName.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="edit-email">البريد الإلكتروني</Label>
                <Input
                  id="edit-email"
                  type="email"
                  aria-invalid={!!userForm.formState.errors.email}
                  {...userForm.register("email")}
                />
                {userForm.formState.errors.email && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.email.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="edit-phone">رقم الهاتف</Label>
                <Input
                  id="edit-phone"
                  aria-invalid={!!userForm.formState.errors.phone}
                  {...userForm.register("phone")}
                />
                {userForm.formState.errors.phone && (
                  <p className="text-sm text-red-500 mt-1">
                    {userForm.formState.errors.phone.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="edit-role">الدور</Label>
                <Select
                  value={userForm.watch("role")}
                  onValueChange={(value) => userForm.setValue("role", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="اختر الدور" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">مدير</SelectItem>
                    <SelectItem value="manager">مدير فرع</SelectItem>
                    <SelectItem value="accountant">محاسب</SelectItem>
                    <SelectItem value="user">مستخدم</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="edit-status">الحالة</Label>
                <Select
                  value={userForm.watch("status")}
                  onValueChange={(value) => userForm.setValue("status", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">معطل</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">حفظ</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>هل أنت متأكد؟</AlertDialogTitle>
            <AlertDialogDescription>
              سيتم حذف المستخدم {selectedUser?.firstName} {selectedUser?.lastName} بشكل دائم.
              لا يمكن التراجع عن هذا الإجراء.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleDeleteUser} className="bg-red-600 hover:bg-red-700">
              حذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Password Reset Dialog */}
      <Dialog open={isPasswordDialogOpen} onOpenChange={setIsPasswordDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>إعادة تعيين كلمة المرور</DialogTitle>
            <DialogDescription>
              تعيين كلمة مرور جديدة للمستخدم {selectedUser?.firstName} {selectedUser?.lastName}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={passwordForm.handleSubmit(handleResetPassword)} className="space-y-4">
            <div>
              <Label htmlFor="reset-password">كلمة المرور الجديدة</Label>
              <Input
                id="reset-password"
                type="password"
                aria-invalid={!!passwordForm.formState.errors.password}
                {...passwordForm.register("password")}
              />
              {passwordForm.formState.errors.password && (
                <p className="text-sm text-red-500 mt-1">
                  {passwordForm.formState.errors.password.message}
                </p>
              )}
            </div>
            <div>
              <Label htmlFor="reset-confirm">تأكيد كلمة المرور</Label>
              <Input
                id="reset-confirm"
                type="password"
                aria-invalid={!!passwordForm.formState.errors.confirmPassword}
                {...passwordForm.register("confirmPassword")}
              />
              {passwordForm.formState.errors.confirmPassword && (
                <p className="text-sm text-red-500 mt-1">
                  {passwordForm.formState.errors.confirmPassword.message}
                </p>
              )}
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsPasswordDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">تعيين</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default UserManagementPage
