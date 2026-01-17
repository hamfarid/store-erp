/**
 * Notifications Page - الإشعارات
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Bell,
  CheckCircle2,
  AlertTriangle,
  Info,
  XCircle,
  Mail,
  Settings,
  Trash2,
  Check,
  CheckCheck,
  RefreshCw,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"

const mockNotifications = [
  { id: 1, type: "success", title: "تم الدفع بنجاح", message: "تم استلام دفعة بقيمة 5,000 ر.س من شركة التقنية", time: "منذ 5 دقائق", read: false },
  { id: 2, type: "warning", title: "مخزون منخفض", message: "منتج 'سماد NPK' وصل للحد الأدنى من المخزون", time: "منذ 15 دقيقة", read: false },
  { id: 3, type: "info", title: "طلب جديد", message: "تم استلام طلب جديد #SO-005 من مصنع الأغذية", time: "منذ ساعة", read: true },
  { id: 4, type: "error", title: "فشل المزامنة", message: "فشلت مزامنة البيانات مع الخادم الخارجي", time: "منذ ساعتين", read: true },
  { id: 5, type: "success", title: "نسخة احتياطية", message: "تم إنشاء نسخة احتياطية يومية بنجاح", time: "منذ 3 ساعات", read: true },
  { id: 6, type: "info", title: "تحديث النظام", message: "تتوفر نسخة جديدة من النظام v12.1.0", time: "منذ يوم", read: false },
]

const typeConfig = {
  success: { icon: CheckCircle2, color: "text-green-500", bg: "bg-green-100 dark:bg-green-900" },
  warning: { icon: AlertTriangle, color: "text-yellow-500", bg: "bg-yellow-100 dark:bg-yellow-900" },
  info: { icon: Info, color: "text-blue-500", bg: "bg-blue-100 dark:bg-blue-900" },
  error: { icon: XCircle, color: "text-red-500", bg: "bg-red-100 dark:bg-red-900" },
}

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState(mockNotifications)
  const [activeTab, setActiveTab] = useState("all")

  const unreadCount = notifications.filter(n => !n.read).length

  const filteredNotifications = notifications.filter(n => {
    if (activeTab === "all") return true
    if (activeTab === "unread") return !n.read
    return n.type === activeTab
  })

  const handleMarkAsRead = (id) => {
    setNotifications(notifications.map(n => n.id === id ? { ...n, read: true } : n))
  }

  const handleMarkAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })))
    toast.success("تم تحديد الكل كمقروء")
  }

  const handleDelete = (id) => {
    setNotifications(notifications.filter(n => n.id !== id))
    toast.success("تم حذف الإشعار")
  }

  const handleClearAll = () => {
    setNotifications([])
    toast.success("تم حذف جميع الإشعارات")
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Bell className="w-7 h-7 text-orange-500" />
            الإشعارات
            {unreadCount > 0 && (
              <Badge variant="destructive" className="mr-2">{unreadCount} جديد</Badge>
            )}
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة الإشعارات والتنبيهات</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleMarkAllAsRead} disabled={unreadCount === 0}>
            <CheckCheck className="w-4 h-4 ml-2" />
            تحديد الكل كمقروء
          </Button>
          <Button variant="outline" onClick={handleClearAll} disabled={notifications.length === 0}>
            <Trash2 className="w-4 h-4 ml-2" />
            مسح الكل
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Bell className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{notifications.length}</p>
              <p className="text-sm text-muted-foreground">إجمالي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <Mail className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{unreadCount}</p>
              <p className="text-sm text-muted-foreground">غير مقروء</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{notifications.filter(n => n.type === "warning").length}</p>
              <p className="text-sm text-muted-foreground">تحذيرات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{notifications.filter(n => n.type === "success").length}</p>
              <p className="text-sm text-muted-foreground">نجاح</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>قائمة الإشعارات</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList>
              <TabsTrigger value="all">الكل</TabsTrigger>
              <TabsTrigger value="unread">غير مقروء ({unreadCount})</TabsTrigger>
              <TabsTrigger value="success">نجاح</TabsTrigger>
              <TabsTrigger value="warning">تحذيرات</TabsTrigger>
              <TabsTrigger value="error">أخطاء</TabsTrigger>
            </TabsList>

            <TabsContent value={activeTab} className="mt-4">
              <ScrollArea className="h-[500px]">
                {filteredNotifications.length === 0 ? (
                  <div className="text-center py-12 text-muted-foreground">
                    <Bell className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>لا توجد إشعارات</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {filteredNotifications.map(notification => {
                      const config = typeConfig[notification.type]
                      const Icon = config.icon
                      return (
                        <div
                          key={notification.id}
                          className={`flex items-start gap-4 p-4 rounded-lg border transition-colors hover:bg-muted/50 ${
                            !notification.read ? "bg-muted/30" : ""
                          }`}
                        >
                          <div className={`w-10 h-10 rounded-lg ${config.bg} flex items-center justify-center flex-shrink-0`}>
                            <Icon className={`w-5 h-5 ${config.color}`} />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <p className="font-medium">{notification.title}</p>
                              {!notification.read && (
                                <Badge variant="default" className="text-xs">جديد</Badge>
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground mt-1">{notification.message}</p>
                            <p className="text-xs text-muted-foreground mt-2">{notification.time}</p>
                          </div>
                          <div className="flex gap-1 flex-shrink-0">
                            {!notification.read && (
                              <Button variant="ghost" size="sm" onClick={() => handleMarkAsRead(notification.id)}>
                                <Check className="w-4 h-4" />
                              </Button>
                            )}
                            <Button variant="ghost" size="sm" onClick={() => handleDelete(notification.id)}>
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                )}
              </ScrollArea>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

export default NotificationsPage
