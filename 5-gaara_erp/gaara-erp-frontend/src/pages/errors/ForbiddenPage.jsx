import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { Home, ArrowLeft, ShieldX, Lock } from "lucide-react"
import { Button } from "@/components/ui/button"

const ForbiddenPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-red-50 to-slate-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 p-4" dir="rtl">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-red-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center relative z-10 max-w-lg"
      >
        {/* 403 Illustration */}
        <motion.div
          initial={{ scale: 0.5 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", delay: 0.2 }}
          className="relative mb-8"
        >
          <div className="text-[150px] md:text-[200px] font-black text-slate-200 dark:text-slate-800 leading-none select-none">
            403
          </div>
          <motion.div
            animate={{
              rotate: [0, -5, 5, -5, 0],
            }}
            transition={{ duration: 0.5, repeat: Infinity, repeatDelay: 2 }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
          >
            <div className="w-24 h-24 bg-gradient-to-br from-red-500 to-orange-500 rounded-full flex items-center justify-center shadow-lg shadow-red-500/30">
              <ShieldX className="w-12 h-12 text-white" />
            </div>
          </motion.div>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="space-y-4"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-white">
            الوصول محظور
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-md mx-auto">
            عذراً، ليس لديك صلاحية للوصول إلى هذه الصفحة. تواصل مع مسؤول النظام إذا
            كنت تعتقد أن هذا خطأ.
          </p>
        </motion.div>

        {/* Lock icon */}
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, type: "spring" }}
          className="flex items-center justify-center gap-2 mt-6"
        >
          <Lock className="w-5 h-5 text-red-500" />
          <span className="text-sm font-medium text-red-600 dark:text-red-400">
            يتطلب صلاحيات إضافية
          </span>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8"
        >
          <Button
            asChild
            className="h-12 px-6 bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 shadow-lg shadow-red-500/25"
          >
            <Link to="/dashboard">
              <Home className="w-5 h-5 ml-2" />
              لوحة التحكم
            </Link>
          </Button>

          <Button
            asChild
            variant="outline"
            className="h-12 px-6"
            onClick={() => window.history.back()}
          >
            <button type="button">
              <ArrowLeft className="w-5 h-5 ml-2" />
              العودة للخلف
            </button>
          </Button>
        </motion.div>

        {/* Help link */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 text-sm text-slate-500 dark:text-slate-400"
        >
          تحتاج صلاحيات إضافية؟{" "}
          <Link
            to="/support"
            className="text-red-600 hover:text-red-700 dark:text-red-400 hover:underline"
          >
            تواصل مع مسؤول النظام
          </Link>
        </motion.p>
      </motion.div>
    </div>
  )
}

export default ForbiddenPage
