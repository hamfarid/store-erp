/**
 * Enhanced Navbar Component with shadcn/ui
 * @file components/Layout/Navbar.jsx
 * 
 * Features:
 * - Modern design with Tailwind + Radix
 * - User menu dropdown
 * - Notifications dropdown
 * - Theme toggle
 * - Language toggle
 * - Mobile menu trigger
 * - Arabic RTL support
 * - Dark mode support
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { cn } from '../../lib/utils';
import {
  Menu,
  X,
  Bell,
  Sun,
  Moon,
  User,
  Settings,
  LogOut,
  ChevronDown,
  Search,
  Globe,
  Sparkles,
  HelpCircle,
  Shield,
  MessageSquare,
  CheckCircle,
  AlertTriangle,
  Info
} from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import * as Avatar from '@radix-ui/react-avatar';
import { Button } from '../UI/button';
import { Badge } from '../UI/badge';
import { SearchInput } from '../UI/input';

// ============================================
// User Menu Component
// ============================================
const UserMenu = ({ user, onLogout }) => {
  const navigate = useNavigate();
  
  const getInitials = (name) => {
    if (!name) return 'U';
    const parts = name.split(' ');
    return parts.map(p => p[0]).slice(0, 2).join('').toUpperCase();
  };

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
          <Avatar.Root className="w-9 h-9 rounded-full overflow-hidden bg-emerald-100 dark:bg-emerald-900/30">
            <Avatar.Fallback className="w-full h-full flex items-center justify-center text-sm font-medium text-emerald-600 dark:text-emerald-400">
              {getInitials(user?.full_name || user?.username)}
            </Avatar.Fallback>
          </Avatar.Root>
          <div className="hidden md:block text-right">
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {user?.full_name || user?.username || 'المستخدم'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {user?.role === 'admin' ? 'مدير النظام' : 'مستخدم'}
            </p>
          </div>
          <ChevronDown className="h-4 w-4 text-gray-500 hidden md:block" />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="min-w-[200px] bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-2 z-50"
          sideOffset={5}
          align="end"
        >
          {/* User Info */}
          <div className="px-3 py-2 mb-2 border-b border-gray-100 dark:border-gray-700">
            <p className="font-medium text-gray-900 dark:text-gray-100">
              {user?.full_name || user?.username}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">{user?.email}</p>
          </div>

          <DropdownMenu.Item
            className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer outline-none"
            onClick={() => navigate('/profile')}
          >
            <User className="h-4 w-4" /> الملف الشخصي
          </DropdownMenu.Item>

          <DropdownMenu.Item
            className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer outline-none"
            onClick={() => navigate('/settings')}
          >
            <Settings className="h-4 w-4" /> الإعدادات
          </DropdownMenu.Item>

          <DropdownMenu.Item
            className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer outline-none"
            onClick={() => navigate('/help')}
          >
            <HelpCircle className="h-4 w-4" /> المساعدة
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="h-px bg-gray-100 dark:bg-gray-700 my-2" />

          <DropdownMenu.Item
            className="flex items-center gap-3 px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg cursor-pointer outline-none"
            onClick={onLogout}
          >
            <LogOut className="h-4 w-4" /> تسجيل الخروج
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
};

// ============================================
// Notifications Menu Component
// ============================================
const NotificationsMenu = () => {
  const [notifications] = useState([
    { id: 1, type: 'success', title: 'تم التشخيص بنجاح', message: 'تم تحليل صورة المحصول', time: 'منذ 5 دقائق', read: false },
    { id: 2, type: 'warning', title: 'تنبيه', message: 'تم اكتشاف مرض جديد في المزرعة', time: 'منذ 30 دقيقة', read: false },
    { id: 3, type: 'info', title: 'تحديث النظام', message: 'تم تحديث قاعدة بيانات الأمراض', time: 'منذ ساعة', read: true },
  ]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const getIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'warning': return <AlertTriangle className="h-5 w-5 text-amber-500" />;
      case 'error': return <AlertTriangle className="h-5 w-5 text-red-500" />;
      default: return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="relative p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
          <Bell className="h-5 w-5 text-gray-600 dark:text-gray-400" />
          {unreadCount > 0 && (
            <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
              {unreadCount}
            </span>
          )}
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="w-80 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 z-50 overflow-hidden"
          sideOffset={5}
          align="end"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 dark:border-gray-700">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100">الإشعارات</h3>
            {unreadCount > 0 && (
              <Badge variant="default">{unreadCount} جديد</Badge>
            )}
          </div>

          {/* Notifications List */}
          <div className="max-h-[300px] overflow-y-auto">
            {notifications.map((notification) => (
              <DropdownMenu.Item
                key={notification.id}
                className={cn(
                  "flex items-start gap-3 px-4 py-3 cursor-pointer outline-none",
                  "hover:bg-gray-50 dark:hover:bg-gray-700/50",
                  !notification.read && "bg-emerald-50/50 dark:bg-emerald-900/10"
                )}
              >
                {getIcon(notification.type)}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{notification.title}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 truncate">{notification.message}</p>
                  <p className="text-xs text-gray-400 mt-1">{notification.time}</p>
                </div>
                {!notification.read && (
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mt-2" />
                )}
              </DropdownMenu.Item>
            ))}
          </div>

          {/* Footer */}
          <div className="px-4 py-3 border-t border-gray-100 dark:border-gray-700">
            <Link to="/notifications" className="text-sm text-emerald-600 dark:text-emerald-400 hover:underline">
              عرض جميع الإشعارات
            </Link>
          </div>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
};

// ============================================
// Main Navbar Component
// ============================================
const Navbar = ({
  user,
  theme = 'light',
  language = 'ar',
  sidebarOpen = true,
  onToggleTheme,
  onToggleSidebar,
  onChangeLanguage,
  onLogout,
}) => {
  const [showSearch, setShowSearch] = useState(false);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 h-16",
        "bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg",
        "border-b border-gray-200 dark:border-gray-700"
      )}
    >
      <div className="h-full px-4 flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          {/* Mobile Menu Toggle */}
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onToggleSidebar}
            className="lg:hidden"
          >
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>

          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="font-bold text-gray-900 dark:text-gray-100">Gaara Scan AI</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">نظام الزراعة الذكية</p>
            </div>
          </Link>
        </div>

        {/* Center - Search (Desktop) */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <SearchInput
            placeholder="بحث في النظام..."
            className="w-full"
          />
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* Mobile Search Toggle */}
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={() => setShowSearch(!showSearch)}
            className="md:hidden"
          >
            <Search className="h-5 w-5" />
          </Button>

          {/* Language Toggle */}
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={() => onChangeLanguage?.(language === 'ar' ? 'en' : 'ar')}
            title={language === 'ar' ? 'Switch to English' : 'التحويل للعربية'}
          >
            <Globe className="h-5 w-5" />
          </Button>

          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onToggleTheme}
            title={theme === 'light' ? 'الوضع الداكن' : 'الوضع الفاتح'}
          >
            {theme === 'light' ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>

          {/* Notifications */}
          <NotificationsMenu />

          {/* Divider */}
          <div className="hidden sm:block w-px h-8 bg-gray-200 dark:bg-gray-700 mx-2" />

          {/* User Menu */}
          <UserMenu user={user} onLogout={onLogout} />
        </div>
      </div>

      {/* Mobile Search Bar */}
      {showSearch && (
        <div className="absolute top-16 left-0 right-0 p-4 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 md:hidden">
          <SearchInput
            placeholder="بحث في النظام..."
            className="w-full"
            autoFocus
          />
        </div>
      )}
    </header>
  );
};

export default Navbar;
