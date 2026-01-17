import { useState } from "react"
import { motion } from "framer-motion"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { toast } from "sonner"
import {
  User,
  Mail,
  Phone,
  Building2,
  MapPin,
  Camera,
  Save,
  Lock,
  Bell,
  Shield,
  Edit3,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { useAuth } from "@/contexts/AuthContext"
import { getInitials } from "@/lib/utils"

// Validation schema
const profileSchema = z.object({
  firstName: z.string().min(2, "الاسم الأول مطلوب"),
  lastName: z.string().min(2, "اسم العائلة مطلوب"),
  email: z.string().email("بريد إلكتروني غير صحيح"),
  phone: z.string().optional(),
  company: z.string().optional(),
  position: z.string().optional(),
  address: z.string().optional(),
  bio: z.string().max(500).optional(),
})

const passwordSchema = z.object({
  currentPassword: z.string().min(6, "كلمة المرور الحالية مطلوبة"),
  newPassword: z
    .string()
    .min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    .regex(/[A-Z]/, "يجب أن تحتوي على حرف كبير")
    .regex(/[0-9]/, "يجب أن تحتوي على رقم"),
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

const ProfilePage = () => {
  const { user } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register: registerProfile,
    handleSubmit: handleProfileSubmit,
    formState: { errors: profileErrors },
  } = useForm({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      firstName: user?.first_name || "",
      lastName: user?.last_name || "",
      email: user?.email || "",
      phone: user?.phone || "",
      company: user?.company || "",
      position: user?.position || "",
      address: user?.address || "",
      bio: user?.bio || "",
    },
  })

  const {
    register: registerPassword,
    handleSubmit: handlePasswordSubmit,
    reset: resetPassword,
    formState: { errors: passwordErrors },
  } = useForm({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
    },
  })

  const onProfileSubmit = async (data) => {
    setIsLoading(true)
    try {
      // API call would go here
      await new Promise((resolve) => setTimeout(resolve, 1000))
      toast.success("تم تحديث الملف الشخصي بنجاح!")
      setIsEditing(false)
    } catch (error) {
      toast.error("فشل تحديث الملف الشخصي")
    } finally {
      setIsLoading(false)
    }
  }

  const onPasswordSubmit = async (data) => {
    setIsLoading(true)
    try {
      // API call would go here
      await new Promise((resolve) => setTimeout(resolve, 1000))
      toast.success("تم تغيير كلمة المرور بنجاح!")
      resetPassword()
    } catch (error) {
      toast.error("فشل تغيير كلمة المرور")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white">الملف الشخصي</h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة معلوماتك الشخصية وإعدادات الأمان</p>
        </div>
      </div>

      {/* Profile Header Card */}
      <Card className="overflow-hidden">
        <div className="h-32 bg-gradient-to-r from-emerald-500 to-blue-500" />
        <CardContent className="relative pb-6">
          <div className="flex flex-col md:flex-row md:items-end gap-4 -mt-16">
            <div className="relative">
              <Avatar className="w-32 h-32 border-4 border-white dark:border-slate-900 shadow-lg">
                <AvatarImage src={user?.avatar} alt={user?.name} />
                <AvatarFallback className="text-2xl bg-slate-100 dark:bg-slate-800">
                  {getInitials(user?.name || "مستخدم")}
                </AvatarFallback>
              </Avatar>
              <Button
                size="icon"
                variant="secondary"
                className="absolute bottom-0 right-0 rounded-full shadow"
              >
                <Camera className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-bold">
                  {user?.first_name} {user?.last_name}
                </h2>
                <Badge variant="secondary">{user?.role || "مستخدم"}</Badge>
              </div>
              <p className="text-muted-foreground">{user?.email}</p>
            </div>
            <Button
              variant={isEditing ? "secondary" : "default"}
              onClick={() => setIsEditing(!isEditing)}
            >
              <Edit3 className="w-4 h-4 ml-2" />
              {isEditing ? "إلغاء التعديل" : "تعديل الملف"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="profile">
            <User className="w-4 h-4 ml-2" />
            المعلومات الشخصية
          </TabsTrigger>
          <TabsTrigger value="security">
            <Shield className="w-4 h-4 ml-2" />
            الأمان
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <Bell className="w-4 h-4 ml-2" />
            الإشعارات
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>المعلومات الشخصية</CardTitle>
              <CardDescription>قم بتحديث معلوماتك الشخصية</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileSubmit(onProfileSubmit)} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">الاسم الأول</Label>
                    <div className="relative">
                      <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        id="firstName"
                        className="pr-10"
                        disabled={!isEditing}
                        {...registerProfile("firstName")}
                      />
                    </div>
                    {profileErrors.firstName && (
                      <p className="text-sm text-red-500">{profileErrors.firstName.message}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="lastName">اسم العائلة</Label>
                    <div className="relative">
                      <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        id="lastName"
                        className="pr-10"
                        disabled={!isEditing}
                        {...registerProfile("lastName")}
                      />
                    </div>
                    {profileErrors.lastName && (
                      <p className="text-sm text-red-500">{profileErrors.lastName.message}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">البريد الإلكتروني</Label>
                    <div className="relative">
                      <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        id="email"
                        type="email"
                        className="pr-10"
                        disabled={!isEditing}
                        {...registerProfile("email")}
                      />
                    </div>
                    {profileErrors.email && (
                      <p className="text-sm text-red-500">{profileErrors.email.message}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="phone">رقم الجوال</Label>
                    <div className="relative">
                      <Phone className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        id="phone"
                        type="tel"
                        className="pr-10"
                        disabled={!isEditing}
                        {...registerProfile("phone")}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="company">الشركة</Label>
                    <div className="relative">
                      <Building2 className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <Input
                        id="company"
                        className="pr-10"
                        disabled={!isEditing}
                        {...registerProfile("company")}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="position">المنصب</Label>
                    <Input
                      id="position"
                      disabled={!isEditing}
                      {...registerProfile("position")}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="address">العنوان</Label>
                  <div className="relative">
                    <MapPin className="absolute right-3 top-3 w-5 h-5 text-slate-400" />
                    <Input
                      id="address"
                      className="pr-10"
                      disabled={!isEditing}
                      {...registerProfile("address")}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">نبذة عنك</Label>
                  <Textarea
                    id="bio"
                    placeholder="اكتب نبذة مختصرة عنك..."
                    disabled={!isEditing}
                    rows={4}
                    {...registerProfile("bio")}
                  />
                </div>

                {isEditing && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-end"
                  >
                    <Button type="submit" disabled={isLoading}>
                      {isLoading ? (
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                        />
                      ) : (
                        <>
                          <Save className="w-4 h-4 ml-2" />
                          حفظ التغييرات
                        </>
                      )}
                    </Button>
                  </motion.div>
                )}
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>تغيير كلمة المرور</CardTitle>
              <CardDescription>تأكد من استخدام كلمة مرور قوية</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handlePasswordSubmit(onPasswordSubmit)} className="space-y-6 max-w-md">
                <div className="space-y-2">
                  <Label htmlFor="currentPassword">كلمة المرور الحالية</Label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="currentPassword"
                      type="password"
                      className="pr-10"
                      {...registerPassword("currentPassword")}
                    />
                  </div>
                  {passwordErrors.currentPassword && (
                    <p className="text-sm text-red-500">{passwordErrors.currentPassword.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="newPassword">كلمة المرور الجديدة</Label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="newPassword"
                      type="password"
                      className="pr-10"
                      {...registerPassword("newPassword")}
                    />
                  </div>
                  {passwordErrors.newPassword && (
                    <p className="text-sm text-red-500">{passwordErrors.newPassword.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">تأكيد كلمة المرور</Label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="confirmPassword"
                      type="password"
                      className="pr-10"
                      {...registerPassword("confirmPassword")}
                    />
                  </div>
                  {passwordErrors.confirmPassword && (
                    <p className="text-sm text-red-500">{passwordErrors.confirmPassword.message}</p>
                  )}
                </div>

                <Button type="submit" disabled={isLoading}>
                  {isLoading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                    />
                  ) : (
                    <>
                      <Lock className="w-4 h-4 ml-2" />
                      تغيير كلمة المرور
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>إعدادات الإشعارات</CardTitle>
              <CardDescription>تحكم في الإشعارات التي تتلقاها</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">قريباً...</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ProfilePage
