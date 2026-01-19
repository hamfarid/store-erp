/**
 * Sidebar Navigation Component
 * =============================
 * 
 * Main navigation sidebar with RTL support, responsive design,
 * and role-based menu visibility.
 * 
 * Features:
 * - Collapsible sidebar
 * - RTL/LTR support
 * - Role-based menu items
 * - Active route highlighting
 * - Mobile responsive drawer
 * - Bilingual labels
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Scan,
  Bug,
  Warehouse,
  Sprout,
  Tractor,
  Package,
  Users,
  BarChart3,
  FileText,
  Settings,
  Brain,
  ImageIcon,
  Building2,
  Dna,
  Radio,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  LogOut,
  User,
  Moon,
  Sun
} from 'lucide-react';

// Navigation items configuration
const navigationItems = [
  {
    id: 'dashboard',
    path: '/',
    icon: LayoutDashboard,
    label: 'Dashboard',
    labelAr: 'لوحة التحكم',
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    id: 'diagnosis',
    path: '/diagnosis',
    icon: Scan,
    label: 'Diagnosis',
    labelAr: 'التشخيص',
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    id: 'diseases',
    path: '/diseases',
    icon: Bug,
    label: 'Diseases',
    labelAr: 'الأمراض',
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    id: 'divider1',
    type: 'divider',
    label: 'Farm Management',
    labelAr: 'إدارة المزرعة'
  },
  {
    id: 'farms',
    path: '/farms',
    icon: Warehouse,
    label: 'Farms',
    labelAr: 'المزارع',
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    id: 'crops',
    path: '/crops',
    icon: Sprout,
    label: 'Crops',
    labelAr: 'المحاصيل',
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    id: 'equipment',
    path: '/equipment',
    icon: Tractor,
    label: 'Equipment',
    labelAr: 'المعدات',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'inventory',
    path: '/inventory',
    icon: Package,
    label: 'Inventory',
    labelAr: 'المخزون',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'sensors',
    path: '/sensors',
    icon: Radio,
    label: 'Sensors',
    labelAr: 'المستشعرات',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'breeding',
    path: '/breeding',
    icon: Dna,
    label: 'Breeding',
    labelAr: 'التهجين',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'divider2',
    type: 'divider',
    label: 'Analytics & Reports',
    labelAr: 'التحليلات والتقارير'
  },
  {
    id: 'analytics',
    path: '/analytics',
    icon: BarChart3,
    label: 'Analytics',
    labelAr: 'التحليلات',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'reports',
    path: '/reports',
    icon: FileText,
    label: 'Reports',
    labelAr: 'التقارير',
    roles: ['ADMIN', 'MANAGER']
  },
  {
    id: 'divider3',
    type: 'divider',
    label: 'AI & Learning',
    labelAr: 'الذكاء الاصطناعي'
  },
  {
    id: 'ml-dashboard',
    path: '/ml-dashboard',
    icon: Brain,
    label: 'ML Dashboard',
    labelAr: 'لوحة التعلم الآلي',
    roles: ['ADMIN']
  },
  {
    id: 'image-crawler',
    path: '/image-crawler',
    icon: ImageIcon,
    label: 'Image Crawler',
    labelAr: 'جامع الصور',
    roles: ['ADMIN']
  },
  {
    id: 'divider4',
    type: 'divider',
    label: 'Administration',
    labelAr: 'الإدارة'
  },
  {
    id: 'users',
    path: '/users',
    icon: Users,
    label: 'Users',
    labelAr: 'المستخدمون',
    roles: ['ADMIN']
  },
  {
    id: 'companies',
    path: '/companies',
    icon: Building2,
    label: 'Companies',
    labelAr: 'الشركات',
    roles: ['ADMIN']
  },
  {
    id: 'settings',
    path: '/settings',
    icon: Settings,
    label: 'Settings',
    labelAr: 'الإعدادات',
    roles: ['ADMIN', 'MANAGER', 'USER']
  }
];

/**
 * Sidebar Component
 */
const Sidebar = ({ 
  user = null,
  collapsed = false,
  onCollapse,
  onLogout
}) => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });
  
  const isRTL = document.documentElement.dir === 'rtl';
  const userRole = user?.role || 'USER';

  // Toggle dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  // Filter navigation items by role
  const filteredItems = navigationItems.filter(item => {
    if (item.type === 'divider') return true;
    return item.roles?.includes(userRole);
  });

  // Check if path is active
  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  // Navigation item component
  const NavItem = ({ item }) => {
    if (item.type === 'divider') {
      if (collapsed) return null;
      return (
        <div className="px-4 py-2 mt-4 first:mt-0">
          <span className="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
            {isRTL ? item.labelAr : item.label}
          </span>
        </div>
      );
    }

    const Icon = item.icon;
    const active = isActive(item.path);
    const label = isRTL ? item.labelAr : item.label;

    return (
      <Link
        to={item.path}
        onClick={() => setMobileOpen(false)}
        className={`
          flex items-center gap-3 px-4 py-2.5 mx-2 rounded-lg
          transition-all duration-200 group
          ${active 
            ? 'bg-emerald-500 text-white shadow-md' 
            : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
          }
        `}
        title={collapsed ? label : undefined}
      >
        <Icon className={`w-5 h-5 flex-shrink-0 ${active ? '' : 'group-hover:text-emerald-500'}`} />
        {!collapsed && (
          <span className="font-medium truncate">{label}</span>
        )}
        {active && !collapsed && (
          <div className="ml-auto rtl:ml-0 rtl:mr-auto w-1.5 h-1.5 rounded-full bg-white" />
        )}
      </Link>
    );
  };

  // Sidebar content
  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className={`
        flex items-center gap-3 p-4 border-b border-gray-200 dark:border-gray-700
        ${collapsed ? 'justify-center' : ''}
      `}>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg">
          <Sprout className="w-6 h-6 text-white" />
        </div>
        {!collapsed && (
          <div>
            <h1 className="font-bold text-gray-800 dark:text-white">Gaara Scan</h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">AI Plant Diagnosis</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 space-y-1">
        {filteredItems.map(item => (
          <NavItem key={item.id} item={item} />
        ))}
      </nav>

      {/* Bottom section */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4 space-y-2">
        {/* Dark mode toggle */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`
            flex items-center gap-3 w-full px-4 py-2.5 rounded-lg
            text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800
            transition-colors duration-200
            ${collapsed ? 'justify-center' : ''}
          `}
        >
          {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          {!collapsed && (
            <span className="font-medium">
              {isRTL ? (darkMode ? 'الوضع الفاتح' : 'الوضع الداكن') : (darkMode ? 'Light Mode' : 'Dark Mode')}
            </span>
          )}
        </button>

        {/* User profile */}
        {user && (
          <Link
            to="/profile"
            className={`
              flex items-center gap-3 w-full px-4 py-2.5 rounded-lg
              text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800
              transition-colors duration-200
              ${collapsed ? 'justify-center' : ''}
            `}
          >
            <div className="w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <User className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">{user.name}</p>
                <p className="text-xs text-gray-500 truncate">{user.email}</p>
              </div>
            )}
          </Link>
        )}

        {/* Logout button */}
        <button
          onClick={onLogout}
          className={`
            flex items-center gap-3 w-full px-4 py-2.5 rounded-lg
            text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20
            transition-colors duration-200
            ${collapsed ? 'justify-center' : ''}
          `}
        >
          <LogOut className="w-5 h-5" />
          {!collapsed && (
            <span className="font-medium">
              {isRTL ? 'تسجيل الخروج' : 'Logout'}
            </span>
          )}
        </button>

        {/* Collapse button */}
        <button
          onClick={() => onCollapse?.(!collapsed)}
          className={`
            hidden lg:flex items-center gap-3 w-full px-4 py-2.5 rounded-lg
            text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800
            transition-colors duration-200
            ${collapsed ? 'justify-center' : ''}
          `}
        >
          {isRTL ? (
            collapsed ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />
          ) : (
            collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />
          )}
          {!collapsed && (
            <span className="font-medium">
              {isRTL ? 'طي القائمة' : 'Collapse'}
            </span>
          )}
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden fixed top-4 left-4 rtl:left-auto rtl:right-4 z-50 p-2 rounded-lg bg-white dark:bg-gray-800 shadow-lg"
      >
        <Menu className="w-6 h-6 text-gray-600 dark:text-gray-300" />
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Mobile sidebar */}
      <aside className={`
        lg:hidden fixed top-0 bottom-0 z-50 w-72 bg-white dark:bg-gray-900
        transform transition-transform duration-300 ease-in-out
        ${isRTL ? 'right-0' : 'left-0'}
        ${mobileOpen 
          ? 'translate-x-0' 
          : isRTL ? 'translate-x-full' : '-translate-x-full'
        }
      `}>
        <button
          onClick={() => setMobileOpen(false)}
          className="absolute top-4 right-4 rtl:right-auto rtl:left-4 p-2"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>
        <SidebarContent />
      </aside>

      {/* Desktop sidebar */}
      <aside className={`
        hidden lg:block fixed top-0 bottom-0 z-30
        ${isRTL ? 'right-0 border-l' : 'left-0 border-r'}
        border-gray-200 dark:border-gray-700
        bg-white dark:bg-gray-900
        transition-all duration-300 ease-in-out
        ${collapsed ? 'w-20' : 'w-64'}
      `}>
        <SidebarContent />
      </aside>

      {/* Main content spacer */}
      <div className={`
        hidden lg:block flex-shrink-0 transition-all duration-300
        ${collapsed ? 'w-20' : 'w-64'}
      `} />
    </>
  );
};

export default Sidebar;
