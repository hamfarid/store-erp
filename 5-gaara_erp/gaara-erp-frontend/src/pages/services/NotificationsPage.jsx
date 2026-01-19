/**
 * Notifications Management Page - إدارة الإشعارات
 * Gaara ERP v12
 *
 * Notification templates, channels, and delivery management.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Bell,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Send,
  Mail,
  MessageSquare,
  Smartphone,
  Globe,
  CheckCircle2,
  XCircle,
  Clock,
  RefreshCw,
  Settings,
  Filter,
  Users,
  FileText,
  Zap,
  Volume2,
  VolumeX,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"
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
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"
import { Checkbox } from "@/components/ui/checkbox"

// Form schemas
const templateSchema = z.object({
  name: z.string().min(1, "الاسم مطلوب"),
  event: z.string().min(1, "الحدث مطلوب"),
  subject: z.string().optional(),
  body: z.string().min(1, "المحتوى مطلوب"),
  channels: z.array(z.string()).min(1, "يجب اختيار قناة واحدة على الأقل"),
})

const notificationSchema = z.object({
  title: z.string().min(1, "العنوان مطلوب"),
  message: z.string().min(1, "الرسالة مطلوبة"),
  recipients: z.enum(["all", "selected", "roles"]),
  channels: z.array(z.string()).min(1),
  priority: z.enum(["low", "normal", "high"]),
})

// Status configurations
const statusConfig = {
  sent: { label: "تم الإرسال", color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  pending: { label: "معلق", color: "bg-yellow-100 text-yellow-700", icon: Clock },
  failed: { label: "فشل", color: "bg-red-100 text-red-700", icon: XCircle },
}

const channelConfig = {
  email: { label: "البريد الإلكتروني", icon: Mail, color: "bg-blue-100 text-blue-700" },
  sms: { label: "رسائل SMS", icon: MessageSquare, color: "bg-green-100 text-green-700" },
  push: { label: "إشعارات الهاتف", icon: Smartphone, color: "bg-purple-100 text-purple-700" },
  web: { label: "إشعارات الويب", icon: Globe, color: "bg-orange-100 text-orange-700" },
}

// Mock data
const mockTemplates = [
  { id: 1, name: "ترحيب بمستخدم جديد", event: "user.created", subject: "مرحباً بك في نظام Gaara", channels: ["email", "push"], enabled: true },
  { id: 2, name: "تأكيد الطلب", event: "order.created", subject: "تم استلام طلبك", channels: ["email", "sms"], enabled: true },
  { id: 3, name: "تذكير بالدفع", event: "payment.due", subject: "تذكير بموعد الدفع", channels: ["email", "sms", "push"], enabled: true },
  { id: 4, name: "تغيير كلمة المرور", event: "password.changed", subject: "تم تغيير كلمة المرور", channels: ["email"], enabled: true },
  { id: 5, name: "تسجيل دخول جديد", event: "login.new_device", subject: "تسجيل دخول من جهاز جديد", channels: ["email", "push"], enabled: false },
]

const mockNotifications = [
  { id: 1, title: "تحديث النظام", message: "سيتم إجراء تحديث للنظام الليلة", recipients: 150, status: "sent", sent_at: "2026-01-17 10:00", channels: ["email", "web"] },
  { id: 2, title: "عرض خاص", message: "خصم 20% على جميع المنتجات", recipients: 500, status: "sent", sent_at: "2026-01-16 15:30", channels: ["email", "sms", "push"] },
  { id: 3, title: "صيانة مجدولة", message: "صيانة مجدولة يوم الجمعة", recipients: 150, status: "pending", sent_at: null, channels: ["email"] },
]

const mockDeliveryStats = {
  total: 2450,
  delivered: 2380,
  pending: 45,
  failed: 25,
  deliveryRate: "97.1%",
}

const NotificationsPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("notifications")
  const [templates, setTemplates] = useState(mockTemplates)
  const [notifications, setNotifications] = useState(mockNotifications)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")

  // Dialog states
  const [isTemplateDialogOpen, setIsTemplateDialogOpen] = useState(false)
  const [isNotificationDialogOpen, setIsNotificationDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedItem, setSelectedItem] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const templateForm = useForm({
    resolver: zodResolver(templateSchema),
    defaultValues: {
      name: "",
      event: "",
      subject: "",
      body: "",
      channels: ["email"],
    },
  })

  const notificationForm = useForm({
    resolver: zodResolver(notificationSchema),
    defaultValues: {
      title: "",
      message: "",
      recipients: "all",
      channels: ["email"],
      priority: "normal",
    },
  })

  // Stats
  const stats = mockDeliveryStats

  // Handlers
  const handleCreateTemplate = async (data) => {
    setIsSubmitting(true)
    try {
      const newTemplate = {
        id: templates.length + 1,
        ...data,
        enabled: true,
      }
      setTemplates([...templates, newTemplate])
      toast.success("تم إنشاء القالب بنجاح")
      setIsTemplateDialogOpen(false)
      templateForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء القالب")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleSendNotification = async (data) => {
    setIsSubmitting(true)
    try {
      const newNotification = {
        id: notifications.length + 1,
        ...data,
        recipients: data.recipients === "all" ? 150 : 50,
        status: "pending",
        sent_at: null,
      }
      setNotifications([...notifications, newNotification])
      toast.success("تم جدولة الإشعار للإرسال")
      setIsNotificationDialogOpen(false)
      notificationForm.reset()
    } catch (error) {
      toast.error("فشل إرسال الإشعار")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleToggleTemplate = (template) => {
    setTemplates(templates.map(t => 
      t.id === template.id ? { ...t, enabled: !t.enabled } : t
    ))
    toast.success(template.enabled ? "تم تعطيل القالب" : "تم تفعيل القالب")
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      if (activeTab === "templates") {
        setTemplates(templates.filter(t => t.id !== selectedItem.id))
      } else {
        setNotifications(notifications.filter(n => n.id !== selectedItem.id))
      }
      toast.success("تم الحذف بنجاح")
      setIsDeleteDialogOpen(false)
      setSelectedItem(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  // Template columns
  const templateColumns = [
    {
      accessorKey: "name",
      header: "القالب",
      cell: ({ row }) => (
        <div>
          <p className="font-medium">{row.original.name}</p>
          <p className="text-sm text-muted-foreground font-mono">{row.original.event}</p>
        </div>
      ),
    },
    {
      accessorKey: "subject",
      header: "العنوان",
    },
    {
      accessorKey: "channels",
      header: "القنوات",
      cell: ({ row }) => (
        <div className="flex gap-1">
          {row.original.channels.map((ch) => {
            const config = channelConfig[ch]
            const Icon = config?.icon
            return (
              <Badge key={ch} variant="outline" className="flex items-center gap-1">
                {Icon && <Icon className="w-3 h-3" />}
              </Badge>
            )
          })}
        </div>
      ),
    },
    {
      accessorKey: "enabled",
      header: "الحالة",
      cell: ({ row }) => (
        <Switch checked={row.original.enabled} onCheckedChange={() => handleToggleTemplate(row.original)} />
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const template = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedItem(template); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("جاري فتح المحرر...")}>
                <Edit className="w-4 h-4 ml-2" />تعديل
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedItem(template); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Notification columns
  const notificationColumns = [
    {
      accessorKey: "title",
      header: "الإشعار",
      cell: ({ row }) => (
        <div>
          <p className="font-medium">{row.original.title}</p>
          <p className="text-sm text-muted-foreground truncate max-w-xs">{row.original.message}</p>
        </div>
      ),
    },
    {
      accessorKey: "recipients",
      header: "المستلمين",
      cell: ({ row }) => (
        <Badge variant="outline">
          <Users className="w-3 h-3 ml-1" />
          {row.original.recipients}
        </Badge>
      ),
    },
    {
      accessorKey: "channels",
      header: "القنوات",
      cell: ({ row }) => (
        <div className="flex gap-1">
          {row.original.channels.map((ch) => {
            const config = channelConfig[ch]
            const Icon = config?.icon
            return (
              <Badge key={ch} variant="outline" className="flex items-center gap-1">
                {Icon && <Icon className="w-3 h-3" />}
              </Badge>
            )
          })}
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <Badge className={config?.color}>
            <Icon className="w-3 h-3 ml-1" />
            {config?.label}
          </Badge>
        )
      },
    },
    {
      accessorKey: "sent_at",
      header: "تاريخ الإرسال",
      cell: ({ row }) => row.original.sent_at || "—",
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const notification = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedItem(notification); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض
              </DropdownMenuItem>
              {notification.status === "pending" && (
                <DropdownMenuItem onClick={() => toast.info("جاري الإرسال...")}>
                  <Send className="w-4 h-4 ml-2" />إرسال الآن
                </DropdownMenuItem>
              )}
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedItem(notification); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
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
            <Bell className="w-7 h-7 text-amber-500" />
            إدارة الإشعارات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة قوالب وإرسال الإشعارات</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري فتح الإعدادات...")}>
            <Settings className="w-4 h-4 ml-2" />الإعدادات
          </Button>
          <Button onClick={() => setIsNotificationDialogOpen(true)}>
            <Send className="w-4 h-4 ml-2" />إرسال إشعار
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Bell className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.total}</p>
              <p className="text-xs text-muted-foreground">إجمالي الإشعارات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.delivered}</p>
              <p className="text-xs text-muted-foreground">تم التسليم</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.pending}</p>
              <p className="text-xs text-muted-foreground">معلق</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.failed}</p>
              <p className="text-xs text-muted-foreground">فشل</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <Zap className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.deliveryRate}</p>
              <p className="text-xs text-muted-foreground">نسبة التسليم</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="notifications" className="flex items-center gap-2">
            <Send className="w-4 h-4" />الإشعارات المرسلة
          </TabsTrigger>
          <TabsTrigger value="templates" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />قوالب الإشعارات
          </TabsTrigger>
          <TabsTrigger value="channels" className="flex items-center gap-2">
            <Globe className="w-4 h-4" />قنوات الإرسال
          </TabsTrigger>
        </TabsList>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Button variant="outline"><RefreshCw className="w-4 h-4 ml-2" />تحديث</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>الإشعارات ({notifications.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={notificationColumns} data={notifications} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Templates Tab */}
        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>قوالب الإشعارات</CardTitle>
                <CardDescription>إدارة قوالب الإشعارات التلقائية</CardDescription>
              </div>
              <Button onClick={() => setIsTemplateDialogOpen(true)}>
                <Plus className="w-4 h-4 ml-2" />قالب جديد
              </Button>
            </CardHeader>
            <CardContent>
              <DataTable columns={templateColumns} data={templates} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Channels Tab */}
        <TabsContent value="channels" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            {Object.entries(channelConfig).map(([key, config]) => {
              const Icon = config.icon
              return (
                <Card key={key}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${config.color.split(' ')[0]}`}>
                          <Icon className={`w-6 h-6 ${config.color.split(' ')[1]}`} />
                        </div>
                        <div>
                          <h3 className="font-medium">{config.label}</h3>
                          <p className="text-sm text-muted-foreground">نشط</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Switch defaultChecked />
                        <Button variant="ghost" size="sm">
                          <Settings className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>
      </Tabs>

      {/* Template Dialog */}
      <FormDialog
        open={isTemplateDialogOpen}
        onOpenChange={setIsTemplateDialogOpen}
        title="قالب إشعار جديد"
        description="إنشاء قالب إشعار للأحداث التلقائية"
        onSubmit={templateForm.handleSubmit(handleCreateTemplate)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>اسم القالب</Label>
              <Input {...templateForm.register("name")} placeholder="ترحيب بمستخدم جديد" />
            </div>
            <div>
              <Label>الحدث</Label>
              <Select value={templateForm.watch("event")} onValueChange={(v) => templateForm.setValue("event", v)}>
                <SelectTrigger><SelectValue placeholder="اختر الحدث" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="user.created">مستخدم جديد</SelectItem>
                  <SelectItem value="order.created">طلب جديد</SelectItem>
                  <SelectItem value="payment.received">دفعة مستلمة</SelectItem>
                  <SelectItem value="password.changed">تغيير كلمة المرور</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>عنوان البريد (اختياري)</Label>
            <Input {...templateForm.register("subject")} placeholder="مرحباً بك في نظام Gaara" />
          </div>
          <div>
            <Label>محتوى الإشعار</Label>
            <Textarea {...templateForm.register("body")} placeholder="اكتب محتوى الإشعار هنا..." rows={5} />
          </div>
          <div>
            <Label>قنوات الإرسال</Label>
            <div className="flex gap-4 mt-2">
              {Object.entries(channelConfig).map(([key, config]) => (
                <div key={key} className="flex items-center gap-2">
                  <Checkbox 
                    checked={templateForm.watch("channels")?.includes(key)}
                    onCheckedChange={(checked) => {
                      const current = templateForm.watch("channels") || []
                      if (checked) {
                        templateForm.setValue("channels", [...current, key])
                      } else {
                        templateForm.setValue("channels", current.filter(c => c !== key))
                      }
                    }}
                  />
                  <Label className="font-normal">{config.label}</Label>
                </div>
              ))}
            </div>
          </div>
        </div>
      </FormDialog>

      {/* Notification Dialog */}
      <FormDialog
        open={isNotificationDialogOpen}
        onOpenChange={setIsNotificationDialogOpen}
        title="إرسال إشعار"
        description="إرسال إشعار للمستخدمين"
        onSubmit={notificationForm.handleSubmit(handleSendNotification)}
        isSubmitting={isSubmitting}
      >
        <div className="space-y-4">
          <div>
            <Label>العنوان</Label>
            <Input {...notificationForm.register("title")} placeholder="عنوان الإشعار" />
          </div>
          <div>
            <Label>الرسالة</Label>
            <Textarea {...notificationForm.register("message")} placeholder="محتوى الإشعار..." rows={4} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>المستلمين</Label>
              <Select value={notificationForm.watch("recipients")} onValueChange={(v) => notificationForm.setValue("recipients", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع المستخدمين</SelectItem>
                  <SelectItem value="selected">مستخدمين محددين</SelectItem>
                  <SelectItem value="roles">حسب الأدوار</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>الأولوية</Label>
              <Select value={notificationForm.watch("priority")} onValueChange={(v) => notificationForm.setValue("priority", v)}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">منخفضة</SelectItem>
                  <SelectItem value="normal">عادية</SelectItem>
                  <SelectItem value="high">عالية</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label>قنوات الإرسال</Label>
            <div className="flex gap-4 mt-2">
              {Object.entries(channelConfig).map(([key, config]) => (
                <div key={key} className="flex items-center gap-2">
                  <Checkbox 
                    checked={notificationForm.watch("channels")?.includes(key)}
                    onCheckedChange={(checked) => {
                      const current = notificationForm.watch("channels") || []
                      if (checked) {
                        notificationForm.setValue("channels", [...current, key])
                      } else {
                        notificationForm.setValue("channels", current.filter(c => c !== key))
                      }
                    }}
                  />
                  <Label className="font-normal">{config.label}</Label>
                </div>
              ))}
            </div>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedItem(null); }}
        title={selectedItem?.name || selectedItem?.title}
        size="lg"
      >
        {selectedItem && (
          <div className="space-y-4">
            <ViewDialog.Section title="التفاصيل">
              {selectedItem.event && <ViewDialog.Row label="الحدث" value={selectedItem.event} />}
              {selectedItem.subject && <ViewDialog.Row label="العنوان" value={selectedItem.subject} />}
              {selectedItem.message && <ViewDialog.Row label="الرسالة" value={selectedItem.message} />}
              {selectedItem.recipients && <ViewDialog.Row label="المستلمين" value={selectedItem.recipients} />}
            </ViewDialog.Section>
            <ViewDialog.Section title="قنوات الإرسال">
              <div className="flex gap-2">
                {selectedItem.channels?.map(ch => {
                  const config = channelConfig[ch]
                  return <Badge key={ch} className={config?.color}>{config?.label}</Badge>
                })}
              </div>
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف"
        description={`هل أنت متأكد من حذف "${selectedItem?.name || selectedItem?.title}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default NotificationsPage
