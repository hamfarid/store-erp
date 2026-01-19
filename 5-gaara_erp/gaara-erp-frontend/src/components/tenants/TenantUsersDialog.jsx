/**
 * Tenant Users Dialog - حوار إدارة مستخدمي المستأجر
 * Gaara ERP v12
 *
 * Dialog component for managing users within a tenant.
 * Allows adding, editing, and removing tenant users.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 * @created 2026-01-17
 */

import { useState, useEffect, useCallback } from 'react'
import { toast } from 'sonner'
import {
  Users,
  Plus,
  Trash2,
  Edit,
  Search,
  Loader2,
  Shield,
  Mail,
  Calendar,
  MoreVertical,
  UserPlus,
  Crown,
  User,
} from 'lucide-react'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'

import tenantService from '@/services/tenantService'

/**
 * Role configuration
 */
const roleConfig = {
  owner: { name: 'مالك', name_en: 'Owner', icon: Crown, color: 'text-yellow-500' },
  admin: { name: 'مدير', name_en: 'Admin', icon: Shield, color: 'text-blue-500' },
  member: { name: 'عضو', name_en: 'Member', icon: User, color: 'text-gray-500' },
  viewer: { name: 'مشاهد', name_en: 'Viewer', icon: User, color: 'text-gray-400' },
}

/**
 * Get initials from name
 */
const getInitials = (name, email) => {
  if (name) {
    return name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase()
  }
  if (email) {
    return email.substring(0, 2).toUpperCase()
  }
  return 'U'
}

/**
 * Tenant Users Dialog Component
 *
 * @param {Object} props
 * @param {Object} props.tenant - Tenant object
 * @param {boolean} props.open - Dialog open state
 * @param {Function} props.onClose - Close handler
 * @param {Function} props.onUpdate - Update callback (optional)
 */
export function TenantUsersDialog({ tenant, open, onClose, onUpdate }) {
  // State
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  // Add user dialog state
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [newUserEmail, setNewUserEmail] = useState('')
  const [newUserRole, setNewUserRole] = useState('member')

  // Delete confirmation state
  const [deleteUser, setDeleteUser] = useState(null)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)

  // Edit role state
  const [editingUser, setEditingUser] = useState(null)
  const [editRole, setEditRole] = useState('')

  /**
   * Load tenant users
   */
  const loadUsers = useCallback(async () => {
    if (!tenant?.id) return

    setIsLoading(true)
    try {
      const response = await tenantService.getTenantUsers(tenant.id)
      if (response.success) {
        setUsers(response.data || [])
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (error) {
      console.error('Error loading users:', error)
      toast.error(error.message_ar || 'فشل في تحميل المستخدمين')
    } finally {
      setIsLoading(false)
    }
  }, [tenant?.id])

  // Load users when dialog opens
  useEffect(() => {
    if (open && tenant?.id) {
      loadUsers()
    }
  }, [open, tenant?.id, loadUsers])

  /**
   * Add user to tenant
   */
  const handleAddUser = async () => {
    if (!newUserEmail.trim()) {
      toast.error('الرجاء إدخال البريد الإلكتروني')
      return
    }

    setIsSaving(true)
    try {
      const response = await tenantService.addTenantUser(tenant.id, {
        email: newUserEmail.trim(),
        role: newUserRole,
      })

      if (response.success) {
        toast.success('تم إضافة المستخدم بنجاح')
        setIsAddDialogOpen(false)
        setNewUserEmail('')
        setNewUserRole('member')
        loadUsers()
        onUpdate?.()
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (error) {
      console.error('Error adding user:', error)
      toast.error(error.message_ar || 'فشل في إضافة المستخدم')
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Update user role
   */
  const handleUpdateRole = async () => {
    if (!editingUser || !editRole) return

    setIsSaving(true)
    try {
      const response = await tenantService.updateTenantUser(
        tenant.id,
        editingUser.user_id,
        { role: editRole }
      )

      if (response.success) {
        toast.success('تم تحديث الدور بنجاح')
        setEditingUser(null)
        setEditRole('')
        loadUsers()
        onUpdate?.()
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (error) {
      console.error('Error updating role:', error)
      toast.error(error.message_ar || 'فشل في تحديث الدور')
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Remove user from tenant
   */
  const handleRemoveUser = async () => {
    if (!deleteUser) return

    setIsSaving(true)
    try {
      const response = await tenantService.removeTenantUser(tenant.id, deleteUser.user_id)

      if (response.success) {
        toast.success('تم إزالة المستخدم بنجاح')
        setIsDeleteDialogOpen(false)
        setDeleteUser(null)
        loadUsers()
        onUpdate?.()
      } else {
        throw new Error(response.message_ar || response.message)
      }
    } catch (error) {
      console.error('Error removing user:', error)
      toast.error(error.message_ar || 'فشل في إزالة المستخدم')
    } finally {
      setIsSaving(false)
    }
  }

  /**
   * Filter users by search query
   */
  const filteredUsers = users.filter(user => {
    if (!searchQuery) return true
    const query = searchQuery.toLowerCase()
    return (
      user.email?.toLowerCase().includes(query) ||
      user.name?.toLowerCase().includes(query) ||
      user.role?.toLowerCase().includes(query)
    )
  })

  return (
    <>
      {/* Main Dialog */}
      <Dialog open={open} onOpenChange={onClose}>
        <DialogContent className="max-w-2xl max-h-[80vh]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              مستخدمو المستأجر
            </DialogTitle>
            <DialogDescription>
              إدارة المستخدمين في {tenant?.name_ar || tenant?.name}
            </DialogDescription>
          </DialogHeader>

          {/* Search and Add */}
          <div className="flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="بحث بالاسم أو البريد..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-10"
              />
            </div>
            <Button onClick={() => setIsAddDialogOpen(true)}>
              <UserPlus className="w-4 h-4 ml-2" />
              إضافة مستخدم
            </Button>
          </div>

          <Separator />

          {/* Users List */}
          <ScrollArea className="h-[400px]">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
              </div>
            ) : filteredUsers.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                {searchQuery ? 'لم يتم العثور على نتائج' : 'لا يوجد مستخدمين'}
              </div>
            ) : (
              <div className="space-y-2">
                {filteredUsers.map((user) => {
                  const roleInfo = roleConfig[user.role] || roleConfig.member
                  const RoleIcon = roleInfo.icon

                  return (
                    <div
                      key={user.user_id || user.id}
                      className="flex items-center gap-3 p-3 rounded-lg border hover:bg-muted/50 transition-colors"
                    >
                      {/* Avatar */}
                      <Avatar>
                        <AvatarImage src={user.avatar} />
                        <AvatarFallback>
                          {getInitials(user.name, user.email)}
                        </AvatarFallback>
                      </Avatar>

                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">
                          {user.name || user.email?.split('@')[0]}
                        </p>
                        <p className="text-sm text-muted-foreground truncate">
                          {user.email}
                        </p>
                      </div>

                      {/* Role Badge */}
                      <Badge variant="outline" className="flex items-center gap-1">
                        <RoleIcon className={`w-3 h-3 ${roleInfo.color}`} />
                        {roleInfo.name}
                      </Badge>

                      {/* Actions */}
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreVertical className="w-4 h-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem
                            onClick={() => {
                              setEditingUser(user)
                              setEditRole(user.role)
                            }}
                            disabled={user.role === 'owner'}
                          >
                            <Edit className="w-4 h-4 ml-2" />
                            تغيير الدور
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem
                            onClick={() => {
                              setDeleteUser(user)
                              setIsDeleteDialogOpen(true)
                            }}
                            className="text-red-600"
                            disabled={user.role === 'owner'}
                          >
                            <Trash2 className="w-4 h-4 ml-2" />
                            إزالة
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  )
                })}
              </div>
            )}
          </ScrollArea>

          <DialogFooter>
            <div className="flex items-center justify-between w-full">
              <span className="text-sm text-muted-foreground">
                {users.length} مستخدم / {tenant?.max_users || 10} الحد الأقصى
              </span>
              <Button variant="outline" onClick={onClose}>
                إغلاق
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Add User Dialog */}
      <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>إضافة مستخدم جديد</DialogTitle>
            <DialogDescription>
              أدخل البريد الإلكتروني للمستخدم واختر دوره
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">البريد الإلكتروني</Label>
              <Input
                id="email"
                type="email"
                value={newUserEmail}
                onChange={(e) => setNewUserEmail(e.target.value)}
                placeholder="user@example.com"
                dir="ltr"
              />
            </div>

            <div className="space-y-2">
              <Label>الدور</Label>
              <Select value={newUserRole} onValueChange={setNewUserRole}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">مدير</SelectItem>
                  <SelectItem value="member">عضو</SelectItem>
                  <SelectItem value="viewer">مشاهد</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddDialogOpen(false)} disabled={isSaving}>
              إلغاء
            </Button>
            <Button onClick={handleAddUser} disabled={isSaving || !newUserEmail.trim()}>
              {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
              إضافة
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Role Dialog */}
      <Dialog open={!!editingUser} onOpenChange={() => setEditingUser(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>تغيير دور المستخدم</DialogTitle>
            <DialogDescription>
              تغيير دور {editingUser?.name || editingUser?.email}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label>الدور الجديد</Label>
              <Select value={editRole} onValueChange={setEditRole}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">مدير</SelectItem>
                  <SelectItem value="member">عضو</SelectItem>
                  <SelectItem value="viewer">مشاهد</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setEditingUser(null)} disabled={isSaving}>
              إلغاء
            </Button>
            <Button onClick={handleUpdateRole} disabled={isSaving}>
              {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
              حفظ
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>إزالة المستخدم</AlertDialogTitle>
            <AlertDialogDescription>
              هل أنت متأكد من إزالة {deleteUser?.name || deleteUser?.email} من هذا المستأجر؟
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isSaving}>إلغاء</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleRemoveUser}
              className="bg-red-600 hover:bg-red-700"
              disabled={isSaving}
            >
              {isSaving && <Loader2 className="w-4 h-4 ml-2 animate-spin" />}
              إزالة
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}

export default TenantUsersDialog
