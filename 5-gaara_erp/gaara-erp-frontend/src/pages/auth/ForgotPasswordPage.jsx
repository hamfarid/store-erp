import { useState } from "react"
import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { toast } from "sonner"
import { Mail, ArrowLeft, Zap, CheckCircle, Send } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { authService } from "@/services"

// Validation schema
const forgotPasswordSchema = z.object({
  email: z.string().email("يرجى إدخال بريد إلكتروني صحيح"),
})

const ForgotPasswordPage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  })

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      await authService.forgotPassword(data.email)
      setIsSubmitted(true)
      toast.success("تم إرسال رابط إعادة تعيين كلمة المرور!")
    } catch (error) {
      toast.error(error.message || "حدث خطأ. يرجى المحاولة مرة أخرى.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleResend = async () => {
    setIsLoading(true)
    try {
      await authService.forgotPassword(getValues("email"))
      toast.success("تم إعادة إرسال الرابط!")
    } catch (error) {
      toast.error(error.message || "حدث خطأ. يرجى المحاولة مرة أخرى.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-emerald-50 to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 p-4" dir="rtl">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-emerald-500/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md relative z-10"
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
              {isSubmitted ? (
                <CheckCircle className="w-8 h-8 text-white" />
              ) : (
                <Zap className="w-8 h-8 text-white" />
              )}
            </motion.div>

            <div>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-white">
                {isSubmitted ? "تم الإرسال!" : "نسيت كلمة المرور؟"}
              </CardTitle>
              <CardDescription className="text-slate-600 dark:text-slate-400 mt-2">
                {isSubmitted
                  ? "تحقق من بريدك الإلكتروني للحصول على رابط إعادة تعيين كلمة المرور"
                  : "أدخل بريدك الإلكتروني وسنرسل لك رابط إعادة تعيين كلمة المرور"}
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="pt-6">
            {isSubmitted ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6"
              >
                {/* Success illustration */}
                <div className="flex justify-center">
                  <div className="w-24 h-24 bg-emerald-100 dark:bg-emerald-900/30 rounded-full flex items-center justify-center">
                    <Mail className="w-12 h-12 text-emerald-600 dark:text-emerald-400" />
                  </div>
                </div>

                <div className="text-center space-y-2">
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    أرسلنا رابط إعادة التعيين إلى:
                  </p>
                  <p className="font-medium text-slate-800 dark:text-white">
                    {getValues("email")}
                  </p>
                </div>

                <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
                  <p className="text-sm text-amber-800 dark:text-amber-200">
                    <strong>ملاحظة:</strong> إذا لم تجد الرسالة في صندوق الوارد، تحقق من
                    مجلد البريد غير المرغوب فيه (Spam).
                  </p>
                </div>

                <Button
                  onClick={handleResend}
                  disabled={isLoading}
                  variant="outline"
                  className="w-full h-12"
                >
                  {isLoading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-5 h-5 border-2 border-emerald-500 border-t-transparent rounded-full"
                    />
                  ) : (
                    <>
                      <Send className="w-5 h-5 ml-2" />
                      إعادة إرسال الرابط
                    </>
                  )}
                </Button>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                {/* Email Field */}
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-slate-700 dark:text-slate-300">
                    البريد الإلكتروني
                  </Label>
                  <div className="relative">
                    <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="example@domain.com"
                      className="pr-10 h-12 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                      {...register("email")}
                    />
                  </div>
                  {errors.email && (
                    <p className="text-sm text-red-500">{errors.email.message}</p>
                  )}
                </div>

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
                      <Send className="w-5 h-5 ml-2" />
                      إرسال رابط إعادة التعيين
                    </>
                  )}
                </Button>
              </form>
            )}
          </CardContent>

          <CardFooter className="flex flex-col space-y-4 pt-4">
            <Link
              to="/login"
              className="flex items-center justify-center text-sm text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
            >
              <ArrowLeft className="w-4 h-4 ml-1" />
              العودة لتسجيل الدخول
            </Link>
          </CardFooter>
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          © 2025 Gaara ERP. جميع الحقوق محفوظة.
        </p>
      </motion.div>
    </div>
  )
}

export default ForgotPasswordPage
