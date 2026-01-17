import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import NotificationSystemAdvanced from './NotificationSystemAdvanced';
import {
  Home, Package, TrendingUp, Warehouse, Users, FileText, BarChart3, Settings,
  Menu, X, Bell, LogOut, User, Search, ChevronRight, ChevronDown
} from 'lucide-react';

const LayoutComplete = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const { user, logout, hasPermission } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // قائمة التنقل الرئيسية
  const navigationItems = [
    {
      name: 'لوحة التحكم',
      href: '/dashboard',
      icon: Home,
      permission: null // متاح للجميع
    },
    {
      name: 'إدارة المنتجات',
      icon: Package,
      permission: 'products.view',
      children: [
        { name: 'المنتجات', href: '/products', permission: 'products.view' },
        { name: 'الفئات', href: '/categories', permission: 'categories.view' },
        { name: 'المخزون', href: '/inventory', permission: 'inventory.view' },
        { name: 'اللوطات', href: '/lots', permission: 'lots.view' }
      ]
    },
    {
      name: 'حركات المخزون',
      href: '/stock-movements',
      icon: TrendingUp,
      permission: 'stock_movements.view'
    },
    {
      name: 'إدارة المخازن',
      href: '/warehouses',
      icon: Warehouse,
      permission: 'warehouses.view'
    },
    {
      name: 'العملاء والموردين',
      icon: Users,
      permission: 'customers.view',
      children: [
        { name: 'العملاء', href: '/customers', permission: 'customers.view' },
        { name: 'الموردين', href: '/suppliers', permission: 'suppliers.view' }
      ]
    },
    {
      name: 'إدارة الفواتير',
      icon: FileText,
      permission: 'invoices.view',
      children: [
        { name: 'جميع الفواتير', href: '/invoices', permission: 'invoices.view' },
        { name: 'فواتير المبيعات', href: '/invoices/sales', permission: 'invoices.view' },
        { name: 'فواتير المشتريات', href: '/invoices/purchase', permission: 'invoices.view' }
      ]
    },
    {
      name: 'التقارير والإحصائيات',
      icon: BarChart3,
      permission: 'reports.view',
      children: [
        { name: 'جميع التقارير', href: '/reports', permission: 'reports.view' },
        { name: 'تقرير المخزون', href: '/reports/inventory', permission: 'reports.view' },
        { name: 'تقرير المبيعات', href: '/reports/sales', permission: 'reports.view' },
        { name: 'التقرير المالي', href: '/reports/financial', permission: 'reports.view' }
      ]
    },
    {
      name: 'الإعدادات والإدارة',
      icon: Settings,
      permission: 'settings.view',
      children: [
        { name: 'المستخدمين', href: '/users', permission: 'users.view' },
        { name: 'بيانات الشركة', href: '/company', permission: 'company.view' },
        { name: 'إعدادات النظام', href: '/settings', permission: 'settings.view' }
      ]
    }
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActiveRoute = (href) => {
    return location.pathname === href || location.pathname.startsWith(href + '/');
  };

  const hasAccessToItem = (item) => {
    if (!item.permission) return true;
    return hasPermission(item.permission);
  };

  // مكون عنصر التنقل
  const NavigationItem = ({ item, level = 0 }) => {
    const [isOpen, setIsOpen] = useState(false);
    
    if (!hasAccessToItem(item)) return null;

    const hasChildren = item.children && item.children.length > 0;
    const isActive = item.href ? isActiveRoute(item.href) : false;

    if (hasChildren) {
      return (
        <div className="space-y-1">
          <button
            onClick={() => setIsOpen(!isOpen)}
            className={`w-full flex items-center justify-between px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              isActive
                ? 'bg-primary-100 text-primary-700'
                : 'text-foreground hover:bg-muted'
            }`}
            style={{ paddingRight: `${16 + level * 16}px` }}
          >
            <div className="flex items-center">
              <item.icon className="h-5 w-5 ml-3" />
              {item.name}
            </div>
            <ChevronRight className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-90' : ''}`} />
          </button>
          
          {isOpen && (
            <div className="space-y-1">
              {item.children.map((child, index) => (
                <NavigationItem key={index} item={child} level={level + 1} />
              ))}
            </div>
          )}
        </div>
      );
    }

    return (
      <button
        onClick={() => {
          navigate(item.href);
          setSidebarOpen(false);
        }}
        className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
          isActive
            ? 'bg-primary-100 text-primary-700'
            : 'text-foreground hover:bg-muted'
        }`}
        style={{ paddingRight: `${16 + level * 16}px` }}
      >
        <item.icon className="h-5 w-5 ml-3" />
        {item.name}
      </button>
    );
  };

  // مكون الشريط الجانبي
  const Sidebar = () => (
    <div className={`fixed inset-y-0 right-0 z-50 w-64 bg-white shadow-lg transform ${
      sidebarOpen ? 'translate-x-0' : 'translate-x-full'
    } transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
      <div className="flex items-center justify-between h-16 px-4 border-b border-border">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <Package className="h-5 w-5 text-white" />
            </div>
          </div>
          <div className="mr-3">
            <h1 className="text-lg font-semibold text-foreground">نظام المخزون</h1>
          </div>
        </div>
        <button
          onClick={() => setSidebarOpen(false)}
          className="lg:hidden text-gray-500 hover:text-foreground"
        >
          <X className="h-6 w-6" />
        </button>
      </div>

      <nav className="mt-5 px-2 space-y-1 max-h-screen overflow-y-auto">
        {navigationItems.map((item, index) => (
          <NavigationItem key={index} item={item} />
        ))}
      </nav>

      {/* معلومات المستخدم في الشريط الجانبي */}
      <div className="absolute bottom-0 w-full p-4 border-t border-border bg-muted/50">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <User className="h-5 w-5 text-muted-foreground" />
            </div>
          </div>
          <div className="mr-3 flex-1 min-w-0">
            <p className="text-sm font-medium text-foreground truncate">{user?.name}</p>
            <p className="text-xs text-gray-500 truncate">{user?.role}</p>
          </div>
        </div>
      </div>
    </div>
  );

  // مكون الرأس العلوي
  const Header = () => (
    <header className="bg-white shadow-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-gray-500 hover:text-foreground"
            >
              <Menu className="h-6 w-6" />
            </button>
            
            {/* شريط البحث */}
            <div className="hidden md:block mr-4">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4 pointer-events-none" />
                <input
                  type="text"
                  placeholder="البحث في النظام..."
                  className="w-64 pr-10 pl-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-foreground placeholder-gray-500 bg-white"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4 space-x-reverse">
            {/* نظام الإشعارات */}
            <NotificationSystemAdvanced />

            {/* قائمة المستخدم */}
            <div className="relative">
              <button
                data-testid="user-menu"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center ml-2">
                  <User className="h-5 w-5 text-muted-foreground" />
                </div>
                <span className="hidden md:block text-foreground font-medium">{user?.name}</span>
                <ChevronDown className="hidden md:block h-4 w-4 text-gray-500 mr-1" />
              </button>

              {userMenuOpen && (
                <div className="origin-top-left absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
                  <div className="py-1">
                    <div className="px-4 py-2 text-sm text-foreground border-b border-gray-100">
                      <p className="font-medium">{user?.name}</p>
                      <p className="text-xs text-gray-500">{user?.email}</p>
                    </div>
                    <button
                      onClick={() => {
                        navigate('/settings');
                        setUserMenuOpen(false);
                      }}
                      className="block w-full text-right px-4 py-2 text-sm text-foreground hover:bg-muted"
                    >
                      <Settings className="inline h-4 w-4 ml-2" />
                      الإعدادات
                    </button>
                    <button
                      data-testid="user-menu-logout"
                      onClick={() => {
                        handleLogout();
                        setUserMenuOpen(false);
                      }}
                      className="block w-full text-right px-4 py-2 text-sm text-foreground hover:bg-muted"
                    >
                      <LogOut className="inline h-4 w-4 ml-2" />
                      تسجيل الخروج
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );

  return (
    <div className="h-screen flex overflow-hidden bg-muted">
      {/* الشريط الجانبي */}
      <Sidebar />
      
      {/* المحتوى الرئيسي */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <Header />
        
        {/* منطقة المحتوى */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>

      {/* خلفية الشريط الجانبي للموبايل */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
        </div>
      )}
    </div>
  );
};

export default LayoutComplete;

