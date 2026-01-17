/**
 * Permissions Management Page - إدارة الصلاحيات
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Lock,
  Shield,
  Users,
  Search,
  Filter,
  RefreshCw,
  CheckCircle2,
  XCircle,
  ChevronRight,
  Eye,
  Building2,
  FileText,
  Package,
  DollarSign,
  Settings,
  BarChart3,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

// Mock data
const modules = [
  { id: "companies", name: "الشركات", name_en: "Companies", icon: Building2 },
  { id: "users", name: "المستخدمين", name_en: "Users", icon: Users },
  { id: "inventory", name: "المخزون", name_en: "Inventory", icon: Package },
  { id: "sales", name: "المبيعات", name_en: "Sales", icon: DollarSign },
  { id: "reports", name: "التقارير", name_en: "Reports", icon: BarChart3 },
  { id: "settings", name: "الإعدادات", name_en: "Settings", icon: Settings },
]

const actions = [
  { id: "view", name: "عرض", name_en: "View" },
  { id: "create", name: "إنشاء", name_en: "Create" },
  { id: "update", name: "تعديل", name_en: "Update" },
  { id: "delete", name: "حذف", name_en: "Delete" },
  { id: "export", name: "تصدير", name_en: "Export" },
]

const roles = [
  { id: "super_admin", name: "مدير النظام", is_system: true },
  { id: "admin", name: "مدير", is_system: true },
  { id: "manager", name: "مشرف", is_system: false },
  { id: "user", name: "مستخدم", is_system: true },
  { id: "accountant", name: "محاسب", is_system: false },
]

// Generate mock permissions matrix
const generatePermissionMatrix = () => {
  const matrix = {}
  roles.forEach(role => {
    matrix[role.id] = {}
    modules.forEach(module => {
      matrix[role.id][module.id] = {}
      actions.forEach(action => {
        // Super admin has all permissions
        if (role.id === "super_admin") {
          matrix[role.id][module.id][action.id] = true
        } else if (role.id === "admin") {
          matrix[role.id][module.id][action.id] = action.id !== "delete" || module.id !== "users"
        } else if (role.id === "manager") {
          matrix[role.id][module.id][action.id] = ["view", "create", "update"].includes(action.id)
        } else if (role.id === "user") {
          matrix[role.id][module.id][action.id] = action.id === "view"
        } else {
          matrix[role.id][module.id][action.id] = module.id === "reports" || (module.id === "sales" && action.id === "view")
        }
      })
    })
  })
  return matrix
}

const PermissionsPage = () => {
  const [activeTab, setActiveTab] = useState("matrix")
  const [selectedRole, setSelectedRole] = useState("admin")
  const [permissionMatrix, setPermissionMatrix] = useState({})
  const [searchQuery, setSearchQuery] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadPermissions()
  }, [])

  const loadPermissions = async () => {
    setIsLoading(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setPermissionMatrix(generatePermissionMatrix())
    } catch (error) {
      toast.error("فشل تحميل الصلاحيات")
    } finally {
      setIsLoading(false)
    }
  }

  const togglePermission = (roleId, moduleId, actionId) => {
    if (roleId === "super_admin") {
      toast.error("لا يمكن تعديل صلاحيات مدير النظام")
      return
    }
    
    setPermissionMatrix(prev => ({
      ...prev,
      [roleId]: {
        ...prev[roleId],
        [moduleId]: {
          ...prev[roleId][moduleId],
          [actionId]: !prev[roleId][moduleId][actionId]
        }
      }
    }))
    toast.success("تم تحديث الصلاحية")
  }

  const toggleModuleForRole = (roleId, moduleId) => {
    if (roleId === "super_admin") return
    
    const allEnabled = actions.every(action => permissionMatrix[roleId]?.[moduleId]?.[action.id])
    const newValue = !allEnabled
    
    setPermissionMatrix(prev => ({
      ...prev,
      [roleId]: {
        ...prev[roleId],
        [moduleId]: actions.reduce((acc, action) => {
          acc[action.id] = newValue
          return acc
        }, {})
      }
    }))
    toast.success(newValue ? "تم تفعيل جميع الصلاحيات" : "تم إلغاء جميع الصلاحيات")
  }

  const handleSavePermissions = () => {
    toast.success("تم حفظ الصلاحيات بنجاح")
  }

  // Stats
  const stats = {
    totalPermissions: modules.length * actions.length * roles.length,
    enabledPermissions: Object.values(permissionMatrix).reduce((total, rolePerms) => {
      return total + Object.values(rolePerms).reduce((moduleTotal, modulePerms) => {
        return moduleTotal + Object.values(modulePerms).filter(Boolean).length
      }, 0)
    }, 0),
    totalRoles: roles.length,
    totalModules: modules.length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Lock className="w-7 h-7 text-indigo-500" />
            إدارة الصلاحيات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            تعيين وإدارة صلاحيات الوصول للأدوار والمستخدمين
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadPermissions}>
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث
          </Button>
          <Button onClick={handleSavePermissions}>
            <CheckCircle2 className="w-4 h-4 ml-2" />
            حفظ التغييرات
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
              <Lock className="w-5 h-5 text-indigo-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.enabledPermissions}</p>
              <p className="text-sm text-muted-foreground">صلاحية مفعلة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Shield className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalRoles}</p>
              <p className="text-sm text-muted-foreground">دور</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalModules}</p>
              <p className="text-sm text-muted-foreground">وحدة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Settings className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{actions.length}</p>
              <p className="text-sm text-muted-foreground">إجراء</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="matrix" className="gap-2">
            <BarChart3 className="w-4 h-4" />
            مصفوفة الصلاحيات
          </TabsTrigger>
          <TabsTrigger value="by-role" className="gap-2">
            <Shield className="w-4 h-4" />
            حسب الدور
          </TabsTrigger>
          <TabsTrigger value="by-module" className="gap-2">
            <Package className="w-4 h-4" />
            حسب الوحدة
          </TabsTrigger>
        </TabsList>

        {/* Matrix View */}
        <TabsContent value="matrix">
          <Card>
            <CardHeader>
              <CardTitle>مصفوفة الصلاحيات</CardTitle>
              <CardDescription>عرض شامل لجميع الصلاحيات حسب الأدوار والوحدات</CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="w-full">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[200px]">الوحدة / الإجراء</TableHead>
                      {roles.map(role => (
                        <TableHead key={role.id} className="text-center min-w-[100px]">
                          <div className="flex flex-col items-center gap-1">
                            <span>{role.name}</span>
                            {role.is_system && (
                              <Badge variant="outline" className="text-xs">نظام</Badge>
                            )}
                          </div>
                        </TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {modules.map(module => (
                      <>
                        <TableRow key={module.id} className="bg-muted/50">
                          <TableCell className="font-medium">
                            <div className="flex items-center gap-2">
                              <module.icon className="w-4 h-4" />
                              {module.name}
                            </div>
                          </TableCell>
                          {roles.map(role => (
                            <TableCell key={role.id} className="text-center">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => toggleModuleForRole(role.id, module.id)}
                                disabled={role.id === "super_admin"}
                              >
                                {actions.every(a => permissionMatrix[role.id]?.[module.id]?.[a.id]) ? (
                                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                                ) : actions.some(a => permissionMatrix[role.id]?.[module.id]?.[a.id]) ? (
                                  <div className="w-4 h-4 rounded border-2 border-yellow-500 bg-yellow-100" />
                                ) : (
                                  <XCircle className="w-4 h-4 text-gray-300" />
                                )}
                              </Button>
                            </TableCell>
                          ))}
                        </TableRow>
                        {actions.map(action => (
                          <TableRow key={`${module.id}-${action.id}`}>
                            <TableCell className="pr-8 text-muted-foreground">
                              <ChevronRight className="w-3 h-3 inline ml-1" />
                              {action.name}
                            </TableCell>
                            {roles.map(role => (
                              <TableCell key={role.id} className="text-center">
                                <TooltipProvider>
                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <div className="flex justify-center">
                                        <Checkbox
                                          checked={permissionMatrix[role.id]?.[module.id]?.[action.id] || false}
                                          onCheckedChange={() => togglePermission(role.id, module.id, action.id)}
                                          disabled={role.id === "super_admin"}
                                        />
                                      </div>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                      <p>{role.name}: {action.name} {module.name}</p>
                                    </TooltipContent>
                                  </Tooltip>
                                </TooltipProvider>
                              </TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </>
                    ))}
                  </TableBody>
                </Table>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        {/* By Role View */}
        <TabsContent value="by-role">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <Card className="lg:col-span-1">
              <CardHeader>
                <CardTitle>الأدوار</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <div className="space-y-1">
                  {roles.map(role => (
                    <button
                      key={role.id}
                      onClick={() => setSelectedRole(role.id)}
                      className={`w-full flex items-center justify-between p-3 hover:bg-muted transition-colors ${
                        selectedRole === role.id ? "bg-muted border-r-2 border-primary" : ""
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <Shield className="w-4 h-4" />
                        <span>{role.name}</span>
                      </div>
                      {role.is_system && (
                        <Badge variant="outline" className="text-xs">نظام</Badge>
                      )}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>
                  صلاحيات: {roles.find(r => r.id === selectedRole)?.name}
                </CardTitle>
                <CardDescription>
                  تعديل صلاحيات الدور المحدد
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {modules.map(module => (
                    <Card key={module.id}>
                      <CardHeader className="pb-3">
                        <CardTitle className="text-base flex items-center gap-2">
                          <module.icon className="w-4 h-4" />
                          {module.name}
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {actions.map(action => (
                            <div
                              key={action.id}
                              className="flex items-center justify-between p-2 rounded hover:bg-muted"
                            >
                              <span className="text-sm">{action.name}</span>
                              <Checkbox
                                checked={permissionMatrix[selectedRole]?.[module.id]?.[action.id] || false}
                                onCheckedChange={() => togglePermission(selectedRole, module.id, action.id)}
                                disabled={selectedRole === "super_admin"}
                              />
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* By Module View */}
        <TabsContent value="by-module">
          <div className="space-y-4">
            {modules.map(module => (
              <Card key={module.id}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <module.icon className="w-5 h-5" />
                    {module.name}
                    <Badge variant="outline" className="mr-2">{module.name_en}</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>الدور</TableHead>
                        {actions.map(action => (
                          <TableHead key={action.id} className="text-center">{action.name}</TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {roles.map(role => (
                        <TableRow key={role.id}>
                          <TableCell className="font-medium">
                            <div className="flex items-center gap-2">
                              {role.name}
                              {role.is_system && (
                                <Badge variant="outline" className="text-xs">نظام</Badge>
                              )}
                            </div>
                          </TableCell>
                          {actions.map(action => (
                            <TableCell key={action.id} className="text-center">
                              <Checkbox
                                checked={permissionMatrix[role.id]?.[module.id]?.[action.id] || false}
                                onCheckedChange={() => togglePermission(role.id, module.id, action.id)}
                                disabled={role.id === "super_admin"}
                              />
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default PermissionsPage
