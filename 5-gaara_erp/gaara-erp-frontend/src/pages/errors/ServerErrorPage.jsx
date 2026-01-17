import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import { Home, RefreshCw, ServerCrash, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"

const ServerErrorPage = () => {
  const handleRefresh = () => {
    window.location.reload()
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-orange-50 to-slate-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 p-4" dir="rtl">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center relative z-10 max-w-lg"
      >
        {/* 500 Illustration */}
        <motion.div
          initial={{ scale: 0.5 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", delay: 0.2 }}
          className="relative mb-8"
        >
          <div className="text-[150px] md:text-[200px] font-black text-slate-200 dark:text-slate-800 leading-none select-none">
            500
          </div>
          <motion.div
            animate={{
              y: [0, -5, 0],
              rotate: [0, -2, 2, -2, 0],
            }}
            transition={{ duration: 3, repeat: Infinity }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
          >
            <div className="w-24 h-24 bg-gradient-to-br from-orange-500 to-amber-500 rounded-full flex items-center justify-center shadow-lg shadow-orange-500/30">
              <ServerCrash className="w-12 h-12 text-white" />
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
            خطأ في الخادم
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-md mx-auto">
            عذراً، حدث خطأ غير متوقع في الخادم. فريقنا الفني يعمل على حل المشكلة.
          </p>
        </motion.div>

        {/* Warning notice */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 mt-6 max-w-md mx-auto"
        >
          <div className="flex items-center gap-2 text-amber-800 dark:text-amber-200">
            <AlertTriangle className="w-5 h-5" />
            <span className="text-sm font-medium">
              يرجى المحاولة مرة أخرى بعد قليل
            </span>
          </div>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8"
        >
          <Button
            onClick={handleRefresh}
            className="h-12 px-6 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 shadow-lg shadow-orange-500/25"
          >
            <RefreshCw className="w-5 h-5 ml-2" />
            إعادة المحاولة
          </Button>

          <Button
            asChild
            variant="outline"
            className="h-12 px-6"
          >
            <Link to="/dashboard">
              <Home className="w-5 h-5 ml-2" />
              لوحة التحكم
            </Link>
          </Button>
        </motion.div>

        {/* Status check */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 text-sm text-slate-500 dark:text-slate-400 space-y-2"
        >
          <p>
            للتحقق من حالة الخدمة:{" "}
            <a
              href="https://status.gaara-erp.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-orange-600 hover:text-orange-700 dark:text-orange-400 hover:underline"
            >
              صفحة الحالة
            </a>
          </p>
          <p>
            تحتاج مساعدة؟{" "}
            <Link
              to="/support"
              className="text-orange-600 hover:text-orange-700 dark:text-orange-400 hover:underline"
            >
              تواصل مع الدعم الفني
            </Link>
          </p>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default ServerErrorPage
