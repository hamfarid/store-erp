import { useState, useRef, useEffect } from "react"
import { Link, useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import {
  Menu,
  Search,
  Bell,
  User,
  Settings,
  LogOut,
  Moon,
  Sun,
  Globe,
  ChevronDown,
  MessageSquare,
  HelpCircle,
  X,
  Command,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useAuth } from "@/contexts/AuthContext"
import { useTheme } from "@/contexts/ThemeContext"
import { getInitials } from "@/lib/utils"

const Header = ({ onMenuClick, user }) => {
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [showSearch, setShowSearch] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const { logout } = useAuth()
  const { resolvedTheme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const userMenuRef = useRef(null)
  const notificationRef = useRef(null)
  const searchRef = useRef(null)

  // Mock notifications data
  const notifications = [
    {
      id: 1,
      title: "تنبيه مخزون منخفض",
      message: 'المنتج "بذور الطماطم" يحتاج إعادة طلب',
      time: "5 دقائق",
      type: "warning",
      unread: true,
    },
    {
      id: 2,
      title: "طلب جديد",
      message: "تم استلام طلب شراء جديد من العميل أحمد محمد",
      time: "15 دقيقة",
      type: "info",
      unread: true,
    },
    {
      id: 3,
      title: "تحديث النظام",
      message: "تم تحديث نظام المحاسبة بنجاح",
      time: "ساعة واحدة",
      type: "success",
      unread: false,
    },
    {
      id: 4,
      title: "دفعة مستلمة",
      message: "تم استلام دفعة 15,000 ر.س من شركة ABC",
      time: "ساعتين",
      type: "success",
      unread: false,
    },
  ]

  const unreadCount = notifications.filter((n) => n.unread).length

  // Close menus when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false)
      }
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setShowNotifications(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  // Keyboard shortcut for search (Ctrl/Cmd + K)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault()
        setShowSearch(true)
        setTimeout(() => searchRef.current?.focus(), 100)
      }
      if (e.key === "Escape") {
        setShowSearch(false)
      }
    }

    document.addEventListener("keydown", handleKeyDown)
    return () => document.removeEventListener("keydown", handleKeyDown)
  }, [])

  const handleLogout = async () => {
    setShowUserMenu(false)
    await logout()
    navigate("/login")
  }

  const handleNavigation = (path) => {
    setShowUserMenu(false)
    navigate(path)
  }

  const getNotificationColor = (type) => {
    switch (type) {
      case "warning":
        return "bg-amber-500"
      case "success":
        return "bg-emerald-500"
      case "error":
        return "bg-red-500"
      default:
        return "bg-blue-500"
    }
  }

  return (
    <>
      <header className="sticky top-0 z-30 bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg border-b border-slate-200 dark:border-slate-700 px-4 md:px-6 py-3">
        <div className="flex items-center justify-between">
          {/* Left Section */}
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={onMenuClick}
              className="lg:hidden"
            >
              <Menu className="w-5 h-5" />
            </Button>

            {/* Search Button (Desktop) */}
            <Button
              variant="outline"
              className="hidden md:flex items-center gap-2 text-muted-foreground w-64 justify-start"
              onClick={() => setShowSearch(true)}
            >
              <Search className="w-4 h-4" />
              <span>البحث في النظام...</span>
              <kbd className="mr-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                <Command className="w-3 h-3" />K
              </kbd>
            </Button>

            {/* Search Button (Mobile) */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setShowSearch(true)}
            >
              <Search className="w-5 h-5" />
            </Button>
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-2">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="relative"
            >
              <AnimatePresence mode="wait">
                {resolvedTheme === "dark" ? (
                  <motion.div
                    key="sun"
                    initial={{ rotate: -90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: 90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Sun className="w-5 h-5" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="moon"
                    initial={{ rotate: 90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: -90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Moon className="w-5 h-5" />
                  </motion.div>
                )}
              </AnimatePresence>
            </Button>

            {/* Notifications */}
            <div className="relative" ref={notificationRef}>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative"
              >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-medium"
                  >
                    {unreadCount}
                  </motion.span>
                )}
              </Button>

              <AnimatePresence>
                {showNotifications && (
                  <motion.div
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className="absolute left-0 rtl:left-auto rtl:right-0 mt-2 w-80 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden"
                  >
                    <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between">
                      <h3 className="font-semibold text-slate-800 dark:text-white">
                        الإشعارات
                      </h3>
                      {unreadCount > 0 && (
                        <Badge variant="secondary">{unreadCount} جديد</Badge>
                      )}
                    </div>
                    <div className="max-h-80 overflow-y-auto">
                      {notifications.map((notification) => (
                        <div
                          key={notification.id}
                          className={`p-4 border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/50 cursor-pointer transition-colors ${
                            notification.unread
                              ? "bg-blue-50/50 dark:bg-blue-900/10"
                              : ""
                          }`}
                        >
                          <div className="flex gap-3">
                            <div
                              className={`w-2 h-2 rounded-full mt-2 ${getNotificationColor(
                                notification.type
                              )}`}
                            />
                            <div className="flex-1 min-w-0">
                              <h4 className="text-sm font-medium text-slate-800 dark:text-white mb-1">
                                {notification.title}
                              </h4>
                              <p className="text-sm text-slate-600 dark:text-slate-300 mb-2 line-clamp-2">
                                {notification.message}
                              </p>
                              <span className="text-xs text-slate-400">
                                منذ {notification.time}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="p-3 text-center border-t border-slate-200 dark:border-slate-700">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-primary hover:text-primary"
                        onClick={() => {
                          setShowNotifications(false)
                          navigate("/notifications")
                        }}
                      >
                        عرض جميع الإشعارات
                      </Button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* User Menu */}
            <div className="relative" ref={userMenuRef}>
              <Button
                variant="ghost"
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-2 pr-2"
              >
                <Avatar className="w-8 h-8">
                  <AvatarImage src={user?.avatar} alt={user?.name} />
                  <AvatarFallback className="bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm">
                    {getInitials(user?.name || user?.first_name || "م")}
                  </AvatarFallback>
                </Avatar>
                <div className="hidden sm:block text-right rtl:text-left">
                  <p className="text-sm font-medium text-slate-800 dark:text-white">
                    {user?.first_name || user?.name || "المستخدم"}
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {user?.role === "admin" ? "مدير النظام" : user?.position || "مستخدم"}
                  </p>
                </div>
                <ChevronDown className="w-4 h-4 text-slate-400 hidden sm:block" />
              </Button>

              <AnimatePresence>
                {showUserMenu && (
                  <motion.div
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className="absolute left-0 rtl:left-auto rtl:right-0 mt-2 w-56 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden"
                  >
                    <div className="p-4 border-b border-slate-200 dark:border-slate-700">
                      <div className="flex items-center gap-3">
                        <Avatar className="w-10 h-10">
                          <AvatarImage src={user?.avatar} alt={user?.name} />
                          <AvatarFallback className="bg-gradient-to-r from-emerald-500 to-blue-500 text-white">
                            {getInitials(user?.name || user?.first_name || "م")}
                          </AvatarFallback>
                        </Avatar>
                        <div className="min-w-0">
                          <p className="font-medium text-slate-800 dark:text-white truncate">
                            {user?.first_name} {user?.last_name || ""}
                          </p>
                          <p className="text-sm text-slate-500 dark:text-slate-400 truncate">
                            {user?.email || "admin@gaara-erp.com"}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="py-2">
                      <button
                        onClick={() => handleNavigation("/profile")}
                        className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                      >
                        <User className="w-4 h-4" />
                        <span>الملف الشخصي</span>
                      </button>
                      <button
                        onClick={() => handleNavigation("/settings")}
                        className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                      >
                        <Settings className="w-4 h-4" />
                        <span>الإعدادات</span>
                      </button>
                      <button
                        onClick={() => handleNavigation("/help")}
                        className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                      >
                        <HelpCircle className="w-4 h-4" />
                        <span>المساعدة</span>
                      </button>
                    </div>

                    <div className="border-t border-slate-200 dark:border-slate-700 py-2">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        <span>تسجيل الخروج</span>
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </header>

      {/* Search Modal */}
      <AnimatePresence>
        {showSearch && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-start justify-center pt-20 px-4"
            onClick={() => setShowSearch(false)}
          >
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="w-full max-w-lg bg-white dark:bg-slate-900 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center gap-3 p-4 border-b border-slate-200 dark:border-slate-700">
                <Search className="w-5 h-5 text-slate-400" />
                <Input
                  ref={searchRef}
                  type="text"
                  placeholder="البحث في النظام..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 border-0 bg-transparent focus-visible:ring-0 px-0 text-base"
                />
                <Button
                  variant="ghost"
                  size="icon"
                  className="shrink-0"
                  onClick={() => setShowSearch(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <div className="p-4">
                <p className="text-sm text-muted-foreground text-center py-8">
                  ابدأ بالكتابة للبحث...
                </p>
              </div>

              <div className="p-3 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between text-xs text-muted-foreground">
                <span>استخدم الأسهم للتنقل</span>
                <span>
                  <kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800">
                    Esc
                  </kbd>{" "}
                  للإغلاق
                </span>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default Header
