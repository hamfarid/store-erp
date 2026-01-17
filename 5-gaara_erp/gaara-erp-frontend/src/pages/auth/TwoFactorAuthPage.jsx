import { useState, useRef, useEffect } from "react"
import { Link, useNavigate, useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Shield,
  Smartphone,
  Mail,
  ArrowLeft,
  Zap,
  RefreshCw,
  Lock,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useAuth } from "@/contexts/AuthContext"

const TwoFactorAuthPage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [code, setCode] = useState(["", "", "", "", "", ""])
  const [method, setMethod] = useState("totp") // totp, email, sms
  const [resendTimer, setResendTimer] = useState(0)
  const inputRefs = useRef([])
  const { verify2FA, resend2FACode } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const from = location.state?.from?.pathname || "/dashboard"
  const email = location.state?.email || ""

  useEffect(() => {
    if (resendTimer > 0) {
      const timer = setTimeout(() => setResendTimer(resendTimer - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [resendTimer])

  useEffect(() => {
    inputRefs.current[0]?.focus()
  }, [])

  const handleChange = (index, value) => {
    if (!/^\d*$/.test(value)) return

    const newCode = [...code]
    newCode[index] = value.slice(-1)
    setCode(newCode)

    // Auto-focus next input
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  const handleKeyDown = (index, e) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6)
    const newCode = [...code]
    pastedData.split("").forEach((char, i) => {
      if (i < 6) newCode[i] = char
    })
    setCode(newCode)
    inputRefs.current[Math.min(pastedData.length, 5)]?.focus()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const verificationCode = code.join("")
    
    if (verificationCode.length !== 6) {
      toast.error("يرجى إدخال الرمز كاملاً")
      return
    }

    setIsLoading(true)
    try {
      await verify2FA(verificationCode, method)
      toast.success("تم التحقق بنجاح!")
      navigate(from, { replace: true })
    } catch (error) {
      toast.error(error.message || "رمز التحقق غير صحيح")
      setCode(["", "", "", "", "", ""])
      inputRefs.current[0]?.focus()
    } finally {
      setIsLoading(false)
    }
  }

  const handleResend = async () => {
    if (resendTimer > 0) return

    setIsLoading(true)
    try {
      await resend2FACode(method)
      toast.success("تم إرسال رمز جديد!")
      setResendTimer(60)
    } catch (error) {
      toast.error(error.message || "حدث خطأ. يرجى المحاولة مرة أخرى.")
    } finally {
      setIsLoading(false)
    }
  }

  const methodIcons = {
    totp: <Smartphone className="w-5 h-5" />,
    email: <Mail className="w-5 h-5" />,
    sms: <Smartphone className="w-5 h-5" />,
  }

  const methodLabels = {
    totp: "تطبيق المصادقة",
    email: "البريد الإلكتروني",
    sms: "رسالة نصية",
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
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", delay: 0.2 }}
              className="mx-auto w-16 h-16 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg"
            >
              <Shield className="w-8 h-8 text-white" />
            </motion.div>

            <div>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-white">
                التحقق بخطوتين
              </CardTitle>
              <CardDescription className="text-slate-600 dark:text-slate-400 mt-2">
                أدخل رمز التحقق المكون من 6 أرقام
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="pt-6">
            {/* Method Selector */}
            <div className="flex gap-2 mb-6">
              {Object.entries(methodLabels).map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setMethod(key)}
                  className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    method === key
                      ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 border-2 border-emerald-500"
                      : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-2 border-transparent hover:border-slate-300"
                  }`}
                >
                  {methodIcons[key]}
                  {label}
                </button>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Code Input */}
              <div className="flex justify-center gap-2 rtl:flex-row-reverse">
                {code.map((digit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Input
                      ref={(el) => (inputRefs.current[index] = el)}
                      type="text"
                      inputMode="numeric"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleChange(index, e.target.value)}
                      onKeyDown={(e) => handleKeyDown(index, e)}
                      onPaste={handlePaste}
                      className="w-12 h-14 text-center text-2xl font-bold bg-slate-50 dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 focus:border-emerald-500 focus:ring-emerald-500"
                    />
                  </motion.div>
                ))}
              </div>

              {/* Helper Text */}
              {method !== "totp" && (
                <p className="text-sm text-center text-slate-500 dark:text-slate-400">
                  تم إرسال الرمز إلى {method === "email" ? email : "رقم هاتفك المسجل"}
                </p>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isLoading || code.join("").length !== 6}
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
                    <Lock className="w-5 h-5 ml-2" />
                    تأكيد
                  </>
                )}
              </Button>
            </form>

            {/* Resend Code */}
            {method !== "totp" && (
              <div className="mt-4 text-center">
                <button
                  onClick={handleResend}
                  disabled={isLoading || resendTimer > 0}
                  className="text-sm text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 disabled:text-slate-400 disabled:cursor-not-allowed flex items-center justify-center gap-1 mx-auto"
                >
                  <RefreshCw className="w-4 h-4" />
                  {resendTimer > 0 ? (
                    `إعادة الإرسال بعد ${resendTimer} ثانية`
                  ) : (
                    "إعادة إرسال الرمز"
                  )}
                </button>
              </div>
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

        <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          © 2025 Gaara ERP. جميع الحقوق محفوظة.
        </p>
      </motion.div>
    </div>
  )
}

export default TwoFactorAuthPage
