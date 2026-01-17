import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { toast } from "sonner"
import {
  Eye,
  EyeOff,
  Mail,
  Lock,
  User,
  Phone,
  Building2,
  UserPlus,
  Zap,
  ArrowLeft,
  CheckCircle2,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useAuth } from "@/contexts/AuthContext"

// Validation schema
const registerSchema = z.object({
  firstName: z.string().min(2, "الاسم الأول يجب أن يكون حرفين على الأقل"),
  lastName: z.string().min(2, "اسم العائلة يجب أن يكون حرفين على الأقل"),
  email: z.string().email("يرجى إدخال بريد إلكتروني صحيح"),
  phone: z.string().regex(/^(05|5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$/, "رقم الجوال غير صحيح"),
  companyName: z.string().min(2, "اسم الشركة يجب أن يكون حرفين على الأقل"),
  industry: z.string().min(1, "يرجى اختيار القطاع"),
  password: z
    .string()
    .min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    .regex(/[A-Z]/, "يجب أن تحتوي على حرف كبير")
    .regex(/[a-z]/, "يجب أن تحتوي على حرف صغير")
    .regex(/[0-9]/, "يجب أن تحتوي على رقم"),
  confirmPassword: z.string(),
  terms: z.boolean().refine((val) => val === true, "يجب الموافقة على الشروط والأحكام"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

const industries = [
  { value: "agriculture", label: "الزراعة" },
  { value: "manufacturing", label: "التصنيع" },
  { value: "retail", label: "التجزئة" },
  { value: "wholesale", label: "الجملة" },
  { value: "services", label: "الخدمات" },
  { value: "construction", label: "البناء والتشييد" },
  { value: "technology", label: "التقنية" },
  { value: "healthcare", label: "الرعاية الصحية" },
  { value: "education", label: "التعليم" },
  { value: "other", label: "أخرى" },
]

const passwordRequirements = [
  { regex: /.{8,}/, label: "8 أحرف على الأقل" },
  { regex: /[A-Z]/, label: "حرف كبير واحد" },
  { regex: /[a-z]/, label: "حرف صغير واحد" },
  { regex: /[0-9]/, label: "رقم واحد" },
]

const RegisterPage = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      phone: "",
      companyName: "",
      industry: "",
      password: "",
      confirmPassword: "",
      terms: false,
    },
  })

  const password = watch("password")

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      await registerUser({
        first_name: data.firstName,
        last_name: data.lastName,
        email: data.email,
        phone: data.phone,
        company_name: data.companyName,
        industry: data.industry,
        password: data.password,
      })
      toast.success("تم إنشاء الحساب بنجاح! يرجى التحقق من بريدك الإلكتروني.")
      navigate("/login")
    } catch (error) {
      toast.error(error.message || "فشل إنشاء الحساب. يرجى المحاولة مرة أخرى.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-emerald-50 to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 p-4 py-8" dir="rtl">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-emerald-500/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl relative z-10"
      >
        <Card className="border-0 shadow-2xl bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl">
          <CardHeader className="space-y-4 text-center pb-2">
            {/* Logo */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", delay: 0.2 }}
              className="mx-auto w-16 h-16 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg"
            >
              <Zap className="w-8 h-8 text-white" />
            </motion.div>

            <div>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-white">
                إنشاء حساب جديد
              </CardTitle>
              <CardDescription className="text-slate-600 dark:text-slate-400 mt-2">
                انضم إلى Gaara ERP وابدأ في إدارة أعمالك بذكاء
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="pt-6">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              {/* Name Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">الاسم الأول</Label>
                  <div className="relative">
                    <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="firstName"
                      placeholder="أحمد"
                      className="pr-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("firstName")}
                    />
                  </div>
                  {errors.firstName && (
                    <p className="text-sm text-red-500">{errors.firstName.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="lastName">اسم العائلة</Label>
                  <div className="relative">
                    <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="lastName"
                      placeholder="محمد"
                      className="pr-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("lastName")}
                    />
                  </div>
                  {errors.lastName && (
                    <p className="text-sm text-red-500">{errors.lastName.message}</p>
                  )}
                </div>
              </div>

              {/* Email & Phone */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="email">البريد الإلكتروني</Label>
                  <div className="relative">
                    <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="example@domain.com"
                      className="pr-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("email")}
                    />
                  </div>
                  {errors.email && (
                    <p className="text-sm text-red-500">{errors.email.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">رقم الجوال</Label>
                  <div className="relative">
                    <Phone className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="phone"
                      type="tel"
                      placeholder="05XXXXXXXX"
                      className="pr-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("phone")}
                    />
                  </div>
                  {errors.phone && (
                    <p className="text-sm text-red-500">{errors.phone.message}</p>
                  )}
                </div>
              </div>

              {/* Company & Industry */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="companyName">اسم الشركة</Label>
                  <div className="relative">
                    <Building2 className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="companyName"
                      placeholder="شركة المستقبل"
                      className="pr-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("companyName")}
                    />
                  </div>
                  {errors.companyName && (
                    <p className="text-sm text-red-500">{errors.companyName.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="industry">القطاع</Label>
                  <Select onValueChange={(value) => setValue("industry", value)}>
                    <SelectTrigger className="h-11 bg-slate-50 dark:bg-slate-800">
                      <SelectValue placeholder="اختر القطاع" />
                    </SelectTrigger>
                    <SelectContent>
                      {industries.map((industry) => (
                        <SelectItem key={industry.value} value={industry.value}>
                          {industry.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.industry && (
                    <p className="text-sm text-red-500">{errors.industry.message}</p>
                  )}
                </div>
              </div>

              {/* Password Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="password">كلمة المرور</Label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      className="pr-10 pl-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("password")}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="text-sm text-red-500">{errors.password.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">تأكيد كلمة المرور</Label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="confirmPassword"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="••••••••"
                      className="pr-10 pl-10 h-11 bg-slate-50 dark:bg-slate-800"
                      {...register("confirmPassword")}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                    >
                      {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {errors.confirmPassword && (
                    <p className="text-sm text-red-500">{errors.confirmPassword.message}</p>
                  )}
                </div>
              </div>

              {/* Password Requirements */}
              <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-4">
                <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  متطلبات كلمة المرور:
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {passwordRequirements.map((req, index) => (
                    <div
                      key={index}
                      className={`flex items-center space-x-2 rtl:space-x-reverse text-sm ${
                        req.regex.test(password || "")
                          ? "text-emerald-600 dark:text-emerald-400"
                          : "text-slate-400"
                      }`}
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>{req.label}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Terms */}
              <div className="flex items-start space-x-3 rtl:space-x-reverse">
                <Checkbox
                  id="terms"
                  className="mt-1"
                  onCheckedChange={(checked) => setValue("terms", checked)}
                />
                <Label htmlFor="terms" className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  أوافق على{" "}
                  <Link to="/terms" className="text-emerald-600 hover:underline">
                    الشروط والأحكام
                  </Link>{" "}
                  و{" "}
                  <Link to="/privacy" className="text-emerald-600 hover:underline">
                    سياسة الخصوصية
                  </Link>
                </Label>
              </div>
              {errors.terms && (
                <p className="text-sm text-red-500">{errors.terms.message}</p>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-12 bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white font-medium text-base shadow-lg shadow-emerald-500/25"
              >
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                  />
                ) : (
                  <>
                    <UserPlus className="w-5 h-5 ml-2" />
                    إنشاء الحساب
                  </>
                )}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex flex-col space-y-4 pt-4">
            <p className="text-center text-sm text-slate-600 dark:text-slate-400">
              لديك حساب بالفعل؟{" "}
              <Link
                to="/login"
                className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 font-medium hover:underline"
              >
                تسجيل الدخول
              </Link>
            </p>

            <Link
              to="/"
              className="flex items-center justify-center text-sm text-slate-500 hover:text-slate-700"
            >
              <ArrowLeft className="w-4 h-4 ml-1" />
              العودة للصفحة الرئيسية
            </Link>
          </CardFooter>
        </Card>

        <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          © 2025 Gaara ERP. جميع الحقوق محفوظة.
        </p>
      </motion.div>
    </div>
  )
}

export default RegisterPage
