/**
 * API Keys Management Page - إدارة مفاتيح API
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  Key,
  Plus,
  Copy,
  Eye,
  EyeOff,
  Trash2,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Clock,
  Activity,
  AlertTriangle,
  MoreVertical,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
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
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"

import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"

// Mock data
const mockAPIKeys = [
  {
    id: 1,
    name: "تطبيق المبيعات",
    key_prefix: "gaa_live_",
    key_suffix: "****8a4f",
    full_key: "gaa_live_sk_test_4eC39HqLyjWDarjtT1zdp7dc8a4f",
    status: "active",
    scopes: ["read:sales", "write:sales", "read:inventory"],
    last_used: "2026-01-16T10:30:00Z",
    requests_today: 1250,
    requests_limit: 10000,
    created_at: "2025-06-15T10:00:00Z",
    expires_at: "2026-06-15T10:00:00Z",
    created_by: "أحمد محمد",
  },
  {
    id: 2,
    name: "تطبيق المحاسبة",
    key_prefix: "gaa_live_",
    key_suffix: "****2b3c",
    full_key: "gaa_live_sk_test_7fG92IyNxzWEbsluU2zep8df2b3c",
    status: "active",
    scopes: ["read:accounting", "write:accounting", "read:reports"],
    last_used: "2026-01-16T09:15:00Z",
    requests_today: 850,
    requests_limit: 5000,
    created_at: "2025-08-20T14:30:00Z",
    expires_at: "2026-08-20T14:30:00Z",
    created_by: "سارة أحمد",
  },
  {
    id: 3,
    name: "تطبيق الجوال",
    key_prefix: "gaa_test_",
    key_suffix: "****5d6e",
    full_key: "gaa_test_sk_demo_9hJ45KzPqvXFctmuV3afq9gh5d6e",
    status: "inactive",
    scopes: ["read:*"],
    last_used: "2025-12-01T18:00:00Z",
    requests_today: 0,
    requests_limit: 1000,
    created_at: "2025-10-10T09:00:00Z",
    expires_at: "2026-04-10T09:00:00Z",
    created_by: "محمد علي",
  },
]

const availableScopes = [
  { id: "read:sales", name: "قراءة المبيعات", module: "sales" },
  { id: "write:sales", name: "كتابة المبيعات", module: "sales" },
  { id: "read:inventory", name: "قراءة المخزون", module: "inventory" },
  { id: "write:inventory", name: "كتابة المخزون", module: "inventory" },
  { id: "read:accounting", name: "قراءة المحاسبة", module: "accounting" },
  { id: "write:accounting", name: "كتابة المحاسبة", module: "accounting" },
  { id: "read:reports", name: "قراءة التقارير", module: "reports" },
  { id: "read:users", name: "قراءة المستخدمين", module: "users" },
  { id: "read:*", name: "قراءة الكل", module: "all" },
  { id: "write:*", name: "كتابة الكل", module: "all" },
]

const APIKeysPage = () => {
  const [apiKeys, setApiKeys] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  
  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [selectedKey, setSelectedKey] = useState(null)
  const [showFullKey, setShowFullKey] = useState(false)
  const [newKeyCreated, setNewKeyCreated] = useState(null)
  
  // Form states
  const [keyName, setKeyName] = useState("")
  const [keyType, setKeyType] = useState("live")
  const [selectedScopes, setSelectedScopes] = useState([])
  const [expiresIn, setExpiresIn] = useState("1year")

  useEffect(() => {
    loadAPIKeys()
  }, [])

  const loadAPIKeys = async () => {
    setIsLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setApiKeys(mockAPIKeys)
    } catch (error) {
      toast.error("فشل تحميل مفاتيح API")
    } finally {
      setIsLoading(false)
    }
  }

  const generateKey = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    let key = ""
    for (let i = 0; i < 32; i++) {
      key += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return key
  }

  const handleCreateKey = async () => {
    if (!keyName) {
      toast.error("يرجى إدخال اسم المفتاح")
      return
    }
    if (selectedScopes.length === 0) {
      toast.error("يرجى اختيار صلاحية واحدة على الأقل")
      return
    }

    const fullKey = `gaa_${keyType}_sk_${generateKey()}`
    const newKey = {
      id: apiKeys.length + 1,
      name: keyName,
      key_prefix: `gaa_${keyType}_`,
      key_suffix: `****${fullKey.slice(-4)}`,
      full_key: fullKey,
      status: "active",
      scopes: selectedScopes,
      last_used: null,
      requests_today: 0,
      requests_limit: keyType === "live" ? 10000 : 1000,
      created_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + (expiresIn === "1year" ? 365 : expiresIn === "6months" ? 180 : 30) * 24 * 60 * 60 * 1000).toISOString(),
      created_by: "المستخدم الحالي",
    }
    
    setApiKeys([newKey, ...apiKeys])
    setNewKeyCreated(fullKey)
    setKeyName("")
    setSelectedScopes([])
  }

  const handleDelete = async () => {
    setApiKeys(apiKeys.filter((k) => k.id !== selectedKey.id))
    setIsDeleteDialogOpen(false)
    toast.success("تم حذف المفتاح")
  }

  const handleCopyKey = (key) => {
    navigator.clipboard.writeText(key)
    toast.success("تم نسخ المفتاح")
  }

  const handleToggleStatus = (key) => {
    setApiKeys(apiKeys.map(k => 
      k.id === key.id ? { ...k, status: k.status === "active" ? "inactive" : "active" } : k
    ))
    toast.success(key.status === "active" ? "تم إيقاف المفتاح" : "تم تفعيل المفتاح")
  }

  const toggleScope = (scopeId) => {
    setSelectedScopes(prev => 
      prev.includes(scopeId) 
        ? prev.filter(id => id !== scopeId)
        : [...prev, scopeId]
    )
  }

  const columns = [
    {
      accessorKey: "name",
      header: "اسم المفتاح",
      cell: ({ row }) => {
        const key = row.original
        return (
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              key.status === "active" 
                ? "bg-green-100 dark:bg-green-900" 
                : "bg-gray-100 dark:bg-gray-900"
            }`}>
              <Key className={`w-5 h-5 ${
                key.status === "active" 
                  ? "text-green-600 dark:text-green-400" 
                  : "text-gray-600 dark:text-gray-400"
              }`} />
            </div>
            <div>
              <p className="font-medium">{key.name}</p>
              <p className="text-xs text-muted-foreground font-mono">
                {key.key_prefix}{key.key_suffix}
              </p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => (
        <Badge variant={row.original.status === "active" ? "default" : "secondary"}>
          {row.original.status === "active" ? (
            <CheckCircle2 className="w-3 h-3 ml-1" />
          ) : (
            <XCircle className="w-3 h-3 ml-1" />
          )}
          {row.original.status === "active" ? "نشط" : "غير نشط"}
        </Badge>
      ),
    },
    {
      accessorKey: "scopes",
      header: "الصلاحيات",
      cell: ({ row }) => (
        <div className="flex flex-wrap gap-1">
          {row.original.scopes.slice(0, 2).map((scope) => (
            <Badge key={scope} variant="outline" className="text-xs">
              {scope}
            </Badge>
          ))}
          {row.original.scopes.length > 2 && (
            <Badge variant="outline" className="text-xs">
              +{row.original.scopes.length - 2}
            </Badge>
          )}
        </div>
      ),
    },
    {
      accessorKey: "usage",
      header: "الاستخدام",
      cell: ({ row }) => {
        const key = row.original
        const usagePercent = (key.requests_today / key.requests_limit) * 100
        return (
          <div className="w-32">
            <div className="flex justify-between text-xs mb-1">
              <span>{key.requests_today.toLocaleString()}</span>
              <span className="text-muted-foreground">/ {key.requests_limit.toLocaleString()}</span>
            </div>
            <Progress value={usagePercent} className="h-1.5" />
          </div>
        )
      },
    },
    {
      accessorKey: "last_used",
      header: "آخر استخدام",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground text-sm">
          <Clock className="w-3 h-3" />
          {row.original.last_used ? formatDate(row.original.last_used, "PPp") : "لم يستخدم"}
        </div>
      ),
    },
    {
      accessorKey: "expires_at",
      header: "تاريخ الانتهاء",
      cell: ({ row }) => {
        const expiresAt = new Date(row.original.expires_at)
        const isExpiringSoon = expiresAt < new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
        return (
          <div className={`flex items-center gap-1 text-sm ${isExpiringSoon ? "text-yellow-600" : "text-muted-foreground"}`}>
            {isExpiringSoon && <AlertTriangle className="w-3 h-3" />}
            {formatDate(row.original.expires_at, "PP")}
          </div>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const key = row.original
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
              <DropdownMenuItem onClick={() => { setSelectedKey(key); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleCopyKey(key.full_key)}>
                <Copy className="w-4 h-4 ml-2" />
                نسخ المفتاح
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleToggleStatus(key)}>
                {key.status === "active" ? (
                  <>
                    <XCircle className="w-4 h-4 ml-2" />
                    إيقاف
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4 ml-2" />
                    تفعيل
                  </>
                )}
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => { setSelectedKey(key); setIsDeleteDialogOpen(true); }}
                className="text-red-600"
              >
                <Trash2 className="w-4 h-4 ml-2" />
                حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Stats
  const stats = {
    total: apiKeys.length,
    active: apiKeys.filter(k => k.status === "active").length,
    totalRequests: apiKeys.reduce((sum, k) => sum + k.requests_today, 0),
    expiringSoon: apiKeys.filter(k => new Date(k.expires_at) < new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)).length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Key className="w-7 h-7 text-yellow-500" />
            مفاتيح API
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة مفاتيح الوصول للواجهات البرمجية
          </p>
        </div>
        <Button onClick={() => setIsCreateDialogOpen(true)}>
          <Plus className="w-4 h-4 ml-2" />
          إنشاء مفتاح
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Key className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي المفاتيح</p>
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
              <p className="text-sm text-muted-foreground">مفاتيح نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Activity className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalRequests.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">طلبات اليوم</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.expiringSoon}</p>
              <p className="text-sm text-muted-foreground">تنتهي قريباً</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* API Keys Table */}
      <Card>
        <CardHeader>
          <CardTitle>مفاتيح API ({apiKeys.length})</CardTitle>
          <CardDescription>قائمة جميع مفاتيح الوصول للواجهات البرمجية</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={apiKeys}
            isLoading={isLoading}
            searchKey="name"
            defaultPageSize={10}
          />
        </CardContent>
      </Card>

      {/* Create Key Dialog */}
      <Dialog open={isCreateDialogOpen} onOpenChange={(open) => {
        setIsCreateDialogOpen(open)
        if (!open) {
          setNewKeyCreated(null)
          setKeyName("")
          setSelectedScopes([])
        }
      }}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>إنشاء مفتاح API جديد</DialogTitle>
            <DialogDescription>
              {newKeyCreated 
                ? "تم إنشاء المفتاح بنجاح. احفظه في مكان آمن."
                : "أدخل معلومات المفتاح الجديد"
              }
            </DialogDescription>
          </DialogHeader>
          
          {newKeyCreated ? (
            <div className="space-y-4">
              <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-yellow-800 dark:text-yellow-200">
                      هام: احفظ هذا المفتاح الآن
                    </p>
                    <p className="text-sm text-yellow-700 dark:text-yellow-300">
                      لن تتمكن من عرض المفتاح الكامل مرة أخرى بعد إغلاق هذه النافذة.
                    </p>
                  </div>
                </div>
              </div>
              <div className="relative">
                <Input
                  value={newKeyCreated}
                  readOnly
                  className="font-mono pr-20"
                />
                <Button
                  size="sm"
                  variant="ghost"
                  className="absolute left-1 top-1/2 -translate-y-1/2"
                  onClick={() => handleCopyKey(newKeyCreated)}
                >
                  <Copy className="w-4 h-4" />
                </Button>
              </div>
              <DialogFooter>
                <Button onClick={() => {
                  setIsCreateDialogOpen(false)
                  setNewKeyCreated(null)
                }}>
                  تم
                </Button>
              </DialogFooter>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <Label>اسم المفتاح</Label>
                <Input
                  placeholder="مثال: تطبيق المبيعات"
                  value={keyName}
                  onChange={(e) => setKeyName(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>نوع المفتاح</Label>
                  <Select value={keyType} onValueChange={setKeyType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="live">مفتاح إنتاجي (Live)</SelectItem>
                      <SelectItem value="test">مفتاح تجريبي (Test)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>مدة الصلاحية</Label>
                  <Select value={expiresIn} onValueChange={setExpiresIn}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1month">شهر واحد</SelectItem>
                      <SelectItem value="6months">6 أشهر</SelectItem>
                      <SelectItem value="1year">سنة واحدة</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Separator />
              <div>
                <Label className="mb-3 block">الصلاحيات</Label>
                <div className="grid grid-cols-2 gap-2">
                  {availableScopes.map((scope) => (
                    <div
                      key={scope.id}
                      className={`flex items-center space-x-2 space-x-reverse p-3 rounded-lg border cursor-pointer transition-colors ${
                        selectedScopes.includes(scope.id)
                          ? "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
                          : "hover:bg-muted"
                      }`}
                      onClick={() => toggleScope(scope.id)}
                    >
                      <Checkbox
                        checked={selectedScopes.includes(scope.id)}
                        onCheckedChange={() => toggleScope(scope.id)}
                      />
                      <div>
                        <p className="text-sm font-medium">{scope.name}</p>
                        <p className="text-xs text-muted-foreground">{scope.id}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  إلغاء
                </Button>
                <Button onClick={handleCreateKey}>
                  <Key className="w-4 h-4 ml-2" />
                  إنشاء المفتاح
                </Button>
              </DialogFooter>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* View Details Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>تفاصيل المفتاح</DialogTitle>
          </DialogHeader>
          {selectedKey && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                  selectedKey.status === "active" 
                    ? "bg-green-100 dark:bg-green-900" 
                    : "bg-gray-100 dark:bg-gray-900"
                }`}>
                  <Key className={`w-6 h-6 ${
                    selectedKey.status === "active" 
                      ? "text-green-600" 
                      : "text-gray-600"
                  }`} />
                </div>
                <div>
                  <h3 className="font-semibold">{selectedKey.name}</h3>
                  <Badge variant={selectedKey.status === "active" ? "default" : "secondary"}>
                    {selectedKey.status === "active" ? "نشط" : "غير نشط"}
                  </Badge>
                </div>
              </div>
              <Separator />
              <div>
                <Label className="text-muted-foreground">المفتاح</Label>
                <div className="flex items-center gap-2 mt-1">
                  <Input
                    value={showFullKey ? selectedKey.full_key : `${selectedKey.key_prefix}${"•".repeat(20)}${selectedKey.key_suffix.slice(-4)}`}
                    readOnly
                    className="font-mono"
                  />
                  <Button variant="ghost" size="sm" onClick={() => setShowFullKey(!showFullKey)}>
                    {showFullKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => handleCopyKey(selectedKey.full_key)}>
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-muted-foreground">تاريخ الإنشاء</Label>
                  <p>{formatDate(selectedKey.created_at, "PPP")}</p>
                </div>
                <div>
                  <Label className="text-muted-foreground">تاريخ الانتهاء</Label>
                  <p>{formatDate(selectedKey.expires_at, "PPP")}</p>
                </div>
                <div>
                  <Label className="text-muted-foreground">آخر استخدام</Label>
                  <p>{selectedKey.last_used ? formatDate(selectedKey.last_used, "PPp") : "لم يستخدم"}</p>
                </div>
                <div>
                  <Label className="text-muted-foreground">أنشئ بواسطة</Label>
                  <p>{selectedKey.created_by}</p>
                </div>
              </div>
              <div>
                <Label className="text-muted-foreground">الصلاحيات</Label>
                <div className="flex flex-wrap gap-1 mt-1">
                  {selectedKey.scopes.map((scope) => (
                    <Badge key={scope} variant="outline">{scope}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <Label className="text-muted-foreground">الاستخدام اليومي</Label>
                <div className="mt-2">
                  <div className="flex justify-between text-sm mb-1">
                    <span>{selectedKey.requests_today.toLocaleString()} طلب</span>
                    <span className="text-muted-foreground">الحد: {selectedKey.requests_limit.toLocaleString()}</span>
                  </div>
                  <Progress value={(selectedKey.requests_today / selectedKey.requests_limit) * 100} />
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>
              إغلاق
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>حذف مفتاح API</AlertDialogTitle>
            <AlertDialogDescription>
              هل أنت متأكد من حذف المفتاح "{selectedKey?.name}"؟
              سيتم إيقاف جميع التطبيقات التي تستخدم هذا المفتاح.
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

export default APIKeysPage
