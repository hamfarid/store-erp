import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, User, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu, Moon, Sun, Minimize, Maximize, Bell, Wifi, WifiOff
} from 'lucide-react'
import { Outlet } from 'react-router-dom'
import SidebarEnhanced from './SidebarEnhanced'
import Breadcrumbs from './Breadcrumbs'
import { useConnectionStatus } from '../hooks/useConnectionStatus'
import { useAuth } from '../contexts/AuthContext'
import '../styles/layout-fix.css'
import '../styles/layout-responsive-fix.css'

const Layout = () => {
  const { user, logout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [notificationsOpen, setNotificationsOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [darkMode, setDarkMode] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  
  // Monitor backend connection status
  const { isConnected, lastChecked } = useConnectionStatus(30000) // Check every 30 seconds
  
  const handleLogout = () => {
    logout()
    globalThis.location.href = '/login'
  }

  const notifications = [
    {
      id: 1,
      title: 'مخزون منخفض',
      message: 'بذور الطماطم تحتاج إعادة تموين',
      time: 'منذ 5 دقائق',
      type: 'warning',
      unread: true
    },
    {
      id: 2,
      title: 'فاتورة جديدة',
      message: 'تم إنشاء فاتورة مبيعات جديدة',
      time: 'منذ 15 دقيقة',
      type: 'info',
      unread: true
    },
    {
      id: 3,
      title: 'تحديث النظام',
      message: 'تم تحديث النظام بنجاح',
      time: 'منذ ساعة',
      type: 'success',
      unread: false
    }
  ]

  const unreadCount = notifications.filter(n => n.unread).length

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen()
      setIsFullscreen(true)
    } else {
      document.exitFullscreen()
      setIsFullscreen(false)
    }
  }

  const NotificationItem = ({ notification }) => (
    <div className={`p-3 border-b border-gray-100 hover:bg-muted/50 cursor-pointer ${
      notification.unread ? 'bg-primary-50' : ''
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="text-sm font-medium text-foreground">{notification.title}</h4>
          <p className="text-sm text-muted-foreground mt-1">{notification.message}</p>
          <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
        </div>
        {notification.unread && (
          <div className="w-2 h-2 bg-primary-500 rounded-full mt-1"></div>
        )}
      </div>
    </div>
  )

  return (
    <div className={`app-container min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-muted/50'}`} dir="rtl">
      {/* Header */}
      <header className="fixed-header bg-white shadow-sm border-b border-border">
        <div className="flex items-center justify-between px-6 py-4">
          {/* Left side - Menu toggle and search */}
          <div className="flex items-center space-x-4 space-x-reverse">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
            >
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            
            <div className="search-container relative">
              <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="البحث في النظام..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-4 pr-10 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent w-full"
              />
            </div>
          </div>

          {/* Right side - Actions and user menu */}
          <div className="flex items-center space-x-4 space-x-reverse">
            {/* Connection Status Indicator */}
            <div className={`flex items-center gap-2 px-3 py-1 rounded-lg text-sm ${
              isConnected 
                ? 'bg-primary/10 text-primary-600' 
                : 'bg-destructive/10 text-destructive-600'
            }`}>
              {isConnected ? (
                <>
                  <Wifi className="w-4 h-4" />
                  <span className="font-medium">متصل ✓</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-4 h-4" />
                  <span className="font-medium">غير متصل ✗</span>
                </>
              )}
            </div>
            
            {/* Theme toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {/* Fullscreen toggle */}
            <button
              onClick={toggleFullscreen}
              className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
            >
              {isFullscreen ? <Minimize className="w-5 h-5" /> : <Maximize className="w-5 h-5" />}
            </button>

            {/* Notifications */}
            <div className="relative">
              <button
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors relative"
              >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -left-1 bg-destructive/100 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </button>

              {/* Notifications dropdown */}
              {notificationsOpen && (
                <div className="absolute left-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-border z-50">
                  <div className="p-4 border-b border-border">
                    <h3 className="text-lg font-semibold text-foreground">التنبيهات</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {notifications.map((notification) => (
                      <NotificationItem key={notification.id} notification={notification} />
                    ))}
                  </div>
                  <div className="p-4 border-t border-border">
                    <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      عرض جميع التنبيهات
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* User menu */}
            <div className="relative">
              <button
                data-testid="user-menu"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="flex items-center space-x-3 space-x-reverse hover:bg-muted p-2 rounded-lg transition-colors"
              >
                <div className="text-right">
                  <p className="text-sm font-medium text-foreground">{user?.name || 'مدير النظام'}</p>
                  <p className="text-xs text-muted-foreground">{user?.role || 'مدير عام'}</p>
                </div>
                <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
              </button>

              {/* User dropdown menu */}
              {userMenuOpen && (
                <div className="absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-border z-50">
                  <div className="p-4 border-b border-border">
                    <p className="text-sm font-medium text-foreground">{user?.name}</p>
                    <p className="text-xs text-muted-foreground">{user?.email}</p>
                  </div>
                  <div className="py-1">
                    <button
                      onClick={() => {
                        setUserMenuOpen(false);
                        globalThis.location.href = '/settings';
                      }}
                      className="w-full text-right px-4 py-2 text-sm text-foreground hover:bg-muted flex items-center"
                    >
                      <Settings className="w-4 h-4 ml-2" />
                      <span>الإعدادات</span>
                    </button>
                    <button
                      data-testid="user-menu-logout"
                      onClick={handleLogout}
                      className="w-full text-right px-4 py-2 text-sm text-destructive-600 hover:bg-destructive/10 flex items-center"
                    >
                      <User className="w-4 h-4 ml-2" />
                      <span>تسجيل الخروج</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="flex" dir="rtl">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : 'collapsed'} bg-white shadow-lg overflow-y-auto`}>
          <SidebarEnhanced />
        </aside>

        {/* Main content */}
        <main className={`main-content ${sidebarOpen ? '' : 'full-width'}`}>
          <div className="container">
            <Breadcrumbs />
            <div className="card min-h-96 animate-fade-in">
              <Outlet />
            </div>
          </div>
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="sidebar-overlay lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

export default Layout

