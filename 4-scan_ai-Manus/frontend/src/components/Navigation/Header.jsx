/**
 * Header Component
 * =================
 * 
 * Top navigation header with search, notifications, and user menu.
 * 
 * Features:
 * - Global search
 * - Notifications dropdown
 * - User menu
 * - Language toggle
 * - Breadcrumbs
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Search,
  Bell,
  User,
  Settings,
  LogOut,
  ChevronDown,
  Globe,
  HelpCircle,
  ChevronRight
} from 'lucide-react';
import LanguageToggle from '../LanguageToggle';

/**
 * Header Component
 */
const Header = ({
  user = null,
  notifications = [],
  onLogout,
  onSearch
}) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  const notificationRef = useRef(null);
  const userMenuRef = useRef(null);
  
  const isRTL = document.documentElement.dir === 'rtl';

  // Close dropdowns on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Generate breadcrumbs from path
  const getBreadcrumbs = () => {
    const paths = location.pathname.split('/').filter(Boolean);
    
    const breadcrumbMap = {
      'dashboard': { en: 'Dashboard', ar: 'لوحة التحكم' },
      'diagnosis': { en: 'Diagnosis', ar: 'التشخيص' },
      'diseases': { en: 'Diseases', ar: 'الأمراض' },
      'farms': { en: 'Farms', ar: 'المزارع' },
      'crops': { en: 'Crops', ar: 'المحاصيل' },
      'equipment': { en: 'Equipment', ar: 'المعدات' },
      'inventory': { en: 'Inventory', ar: 'المخزون' },
      'sensors': { en: 'Sensors', ar: 'المستشعرات' },
      'breeding': { en: 'Breeding', ar: 'التهجين' },
      'analytics': { en: 'Analytics', ar: 'التحليلات' },
      'reports': { en: 'Reports', ar: 'التقارير' },
      'users': { en: 'Users', ar: 'المستخدمون' },
      'companies': { en: 'Companies', ar: 'الشركات' },
      'settings': { en: 'Settings', ar: 'الإعدادات' },
      'profile': { en: 'Profile', ar: 'الملف الشخصي' },
      'ml-dashboard': { en: 'ML Dashboard', ar: 'لوحة التعلم الآلي' },
      'image-crawler': { en: 'Image Crawler', ar: 'جامع الصور' }
    };

    return paths.map((path, index) => {
      const label = breadcrumbMap[path] || { en: path, ar: path };
      const href = '/' + paths.slice(0, index + 1).join('/');
      
      return {
        label: isRTL ? label.ar : label.en,
        href,
        isLast: index === paths.length - 1
      };
    });
  };

  const breadcrumbs = getBreadcrumbs();
  const unreadCount = notifications.filter(n => !n.read).length;

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };

  return (
    <header className="
      sticky top-0 z-20
      bg-white/80 dark:bg-gray-900/80 backdrop-blur-md
      border-b border-gray-200 dark:border-gray-700
      px-4 lg:px-6 py-3
    ">
      <div className="flex items-center justify-between gap-4">
        {/* Left: Breadcrumbs */}
        <div className="flex items-center gap-2 min-w-0">
          <Link 
            to="/"
            className="text-gray-500 dark:text-gray-400 hover:text-emerald-500 transition-colors"
          >
            {isRTL ? 'الرئيسية' : 'Home'}
          </Link>
          
          {breadcrumbs.map((crumb, index) => (
            <React.Fragment key={crumb.href}>
              <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0 rtl:rotate-180" />
              {crumb.isLast ? (
                <span className="font-medium text-gray-800 dark:text-white truncate">
                  {crumb.label}
                </span>
              ) : (
                <Link
                  to={crumb.href}
                  className="text-gray-500 dark:text-gray-400 hover:text-emerald-500 transition-colors truncate"
                >
                  {crumb.label}
                </Link>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2 lg:gap-4">
          {/* Search */}
          <form onSubmit={handleSearch} className="hidden md:block relative">
            <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={isRTL ? 'بحث...' : 'Search...'}
              className="
                w-48 lg:w-64 pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2
                bg-gray-100 dark:bg-gray-800 rounded-lg
                text-sm text-gray-700 dark:text-gray-200
                placeholder:text-gray-400
                focus:outline-none focus:ring-2 focus:ring-emerald-500
                transition-all duration-200
              "
            />
          </form>

          {/* Language Toggle */}
          <LanguageToggle variant="button" size="sm" />

          {/* Help */}
          <button
            className="
              hidden lg:flex items-center justify-center
              w-10 h-10 rounded-lg
              text-gray-500 dark:text-gray-400
              hover:bg-gray-100 dark:hover:bg-gray-800
              transition-colors duration-200
            "
            title={isRTL ? 'المساعدة' : 'Help'}
          >
            <HelpCircle className="w-5 h-5" />
          </button>

          {/* Notifications */}
          <div ref={notificationRef} className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="
                relative flex items-center justify-center
                w-10 h-10 rounded-lg
                text-gray-500 dark:text-gray-400
                hover:bg-gray-100 dark:hover:bg-gray-800
                transition-colors duration-200
              "
            >
              <Bell className="w-5 h-5" />
              {unreadCount > 0 && (
                <span className="
                  absolute -top-1 -right-1 rtl:-left-1 rtl:right-auto
                  w-5 h-5 rounded-full
                  bg-red-500 text-white text-xs
                  flex items-center justify-center font-medium
                ">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="
                absolute top-full right-0 rtl:right-auto rtl:left-0 mt-2
                w-80 max-h-96 overflow-y-auto
                bg-white dark:bg-gray-800
                border border-gray-200 dark:border-gray-700
                rounded-xl shadow-xl
                animate-fadeIn
              ">
                <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                  <h3 className="font-semibold text-gray-800 dark:text-white">
                    {isRTL ? 'الإشعارات' : 'Notifications'}
                  </h3>
                </div>
                
                {notifications.length === 0 ? (
                  <div className="p-8 text-center text-gray-500">
                    <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>{isRTL ? 'لا توجد إشعارات' : 'No notifications'}</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-100 dark:divide-gray-700">
                    {notifications.slice(0, 5).map((notification) => (
                      <div
                        key={notification.id}
                        className={`
                          p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50
                          cursor-pointer transition-colors
                          ${!notification.read ? 'bg-emerald-50/50 dark:bg-emerald-900/10' : ''}
                        `}
                      >
                        <p className="text-sm text-gray-800 dark:text-gray-200">
                          {notification.message}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {notification.time}
                        </p>
                      </div>
                    ))}
                  </div>
                )}

                <div className="p-3 border-t border-gray-200 dark:border-gray-700">
                  <Link
                    to="/notifications"
                    className="
                      block w-full py-2 text-center text-sm
                      text-emerald-600 hover:text-emerald-700
                      font-medium
                    "
                    onClick={() => setShowNotifications(false)}
                  >
                    {isRTL ? 'عرض الكل' : 'View All'}
                  </Link>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div ref={userMenuRef} className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="
                flex items-center gap-2 p-1.5 pr-3 rtl:pr-1.5 rtl:pl-3
                rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800
                transition-colors duration-200
              "
            >
              <div className="
                w-8 h-8 rounded-full
                bg-gradient-to-br from-emerald-400 to-emerald-600
                flex items-center justify-center
              ">
                {user?.avatar ? (
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="w-full h-full rounded-full object-cover"
                  />
                ) : (
                  <User className="w-4 h-4 text-white" />
                )}
              </div>
              <span className="hidden lg:block text-sm font-medium text-gray-700 dark:text-gray-200">
                {user?.name || (isRTL ? 'المستخدم' : 'User')}
              </span>
              <ChevronDown className="hidden lg:block w-4 h-4 text-gray-400" />
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div className="
                absolute top-full right-0 rtl:right-auto rtl:left-0 mt-2
                w-56
                bg-white dark:bg-gray-800
                border border-gray-200 dark:border-gray-700
                rounded-xl shadow-xl
                animate-fadeIn
              ">
                {user && (
                  <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                    <p className="font-medium text-gray-800 dark:text-white">
                      {user.name}
                    </p>
                    <p className="text-sm text-gray-500 truncate">
                      {user.email}
                    </p>
                  </div>
                )}
                
                <div className="p-2">
                  <Link
                    to="/profile"
                    onClick={() => setShowUserMenu(false)}
                    className="
                      flex items-center gap-3 px-3 py-2 rounded-lg
                      text-gray-700 dark:text-gray-200
                      hover:bg-gray-100 dark:hover:bg-gray-700
                      transition-colors
                    "
                  >
                    <User className="w-4 h-4" />
                    <span>{isRTL ? 'الملف الشخصي' : 'Profile'}</span>
                  </Link>
                  
                  <Link
                    to="/settings"
                    onClick={() => setShowUserMenu(false)}
                    className="
                      flex items-center gap-3 px-3 py-2 rounded-lg
                      text-gray-700 dark:text-gray-200
                      hover:bg-gray-100 dark:hover:bg-gray-700
                      transition-colors
                    "
                  >
                    <Settings className="w-4 h-4" />
                    <span>{isRTL ? 'الإعدادات' : 'Settings'}</span>
                  </Link>
                </div>
                
                <div className="p-2 border-t border-gray-200 dark:border-gray-700">
                  <button
                    onClick={() => {
                      setShowUserMenu(false);
                      onLogout?.();
                    }}
                    className="
                      flex items-center gap-3 w-full px-3 py-2 rounded-lg
                      text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20
                      transition-colors
                    "
                  >
                    <LogOut className="w-4 h-4" />
                    <span>{isRTL ? 'تسجيل الخروج' : 'Logout'}</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
