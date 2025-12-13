import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Package, 
  Users, 
  Building2, 
  TrendingUp, 
  ShoppingCart,
  FileText,
  BarChart3,
  Settings,
  LogOut,
  Menu,
  X,
  Truck,
  Activity,
  User
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const UnifiedLayout = ({ children }) => {
  const { user, logout, hasPermission } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    {
      name: 'لوحة التحكم',
      href: '/dashboard',
      icon: Home,
      permission: null
    },
    {
      name: 'إدارة المنتجات',
      href: '/products',
      icon: Package,
      permission: 'products.view'
    },
    {
      name: 'إدارة العملاء',
      href: '/customers',
      icon: Users,
      permission: 'customers.view'
    },
    {
      name: 'إدارة الموردين',
      href: '/suppliers',
      icon: Truck,
      permission: 'suppliers.view'
    },
    {
      name: 'إدارة المخازن',
      href: '/warehouses',
      icon: Building2,
      permission: 'warehouses.view'
    },
    {
      name: 'إدارة المخزون',
      href: '/inventory',
      icon: TrendingUp,
      permission: 'inventory.view'
    },
    {
      name: 'حركات المخزون',
      href: '/stock-movements',
      icon: Activity,
      permission: 'stock_movements.view'
    },
    {
      name: 'الفواتير',
      href: '/invoices',
      icon: ShoppingCart,
      permission: 'invoices.view',
      children: [
        {
          name: 'فواتير المبيعات',
          href: '/invoices/sales',
          permission: 'invoices.view'
        },
        {
          name: 'فواتير المشتريات',
          href: '/invoices/purchases',
          permission: 'invoices.view'
        }
      ]
    },
    {
      name: 'التقارير',
      href: '/reports',
      icon: BarChart3,
      permission: 'reports.view'
    },
    {
      name: 'الإعدادات',
      href: '/settings',
      icon: Settings,
      permission: 'settings.view',
      children: [
        {
          name: 'إعدادات الشركة',
          href: '/company',
          permission: 'company.view'
        },
        {
          name: 'إعدادات النظام',
          href: '/settings/system',
          permission: 'settings.edit'
        },
        {
          name: 'إدارة المستخدمين',
          href: '/users',
          permission: 'users.view'
        }
      ]
    }
  ];

  const filteredNavigation = navigation.filter(item => 
    !item.permission || hasPermission(item.permission)
  );

  const isActive = (href) => {
    if (href === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(href);
  };

  const NavItem = ({ item, isChild = false }) => {
    const active = isActive(item.href);
    const Icon = item.icon;

    return (
      <Link
        to={item.href}
        className={`
          group flex items-center px-2 py-2 text-sm font-medium rounded-md
          ${active 
            ? 'bg-primary-100 text-primary-900' 
            : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground'
          }
          ${isChild ? 'pl-11' : ''}
        `}
        onClick={() => setSidebarOpen(false)}
      >
        {Icon && (
          <Icon
            className={`
              ml-3 flex-shrink-0 h-5 w-5
              ${active ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'}
            `}
          />
        )}
        <span dir="rtl">{item.name}</span>
      </Link>
    );
  };

  const Sidebar = ({ mobile = false }) => (
    <div className={`flex flex-col flex-grow pt-5 pb-4 overflow-y-auto ${mobile ? 'bg-white' : 'bg-white border-r border-border'}`}>
      <div className="flex items-center flex-shrink-0 px-4">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg flex items-center justify-center shadow-lg">
            <Package className="w-5 h-5 text-white" />
          </div>
          <div className="ml-3 hidden sm:block">
            <h1 className="text-lg font-semibold text-foreground" dir="rtl">
              نظام إدارة المخزون
            </h1>
            <p className="text-sm text-gray-500" dir="rtl">Gaara Seeds</p>
          </div>
          <div className="ml-3 sm:hidden">
            <h1 className="text-base font-semibold text-foreground" dir="rtl">
              المخزون
            </h1>
          </div>
        </div>
      </div>
      
      <div className="mt-5 flex-grow flex flex-col">
        <nav className="flex-1 px-2 space-y-1">
          {filteredNavigation.map((item) => (
            <div key={item.name}>
              <NavItem item={item} />
              {item.children && (
                <div className="mt-1 space-y-1">
                  {item.children
                    .filter(child => !child.permission || hasPermission(child.permission))
                    .map((child) => (
                      <NavItem key={child.name} item={child} isChild={true} />
                    ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </div>

      {/* User Info */}
      <div className="flex-shrink-0 flex border-t border-border p-4">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <User className="w-5 h-5 text-muted-foreground" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-foreground" dir="rtl">
              {user?.full_name || user?.name}
            </p>
            <p className="text-xs text-gray-500" dir="rtl">
              {user?.role === 'admin' ? 'مدير عام' : 
               user?.role === 'manager' ? 'مدير مخزون' : 
               user?.role === 'user' ? 'موظف مبيعات' : 'مستخدم'}
            </p>
          </div>
        </div>
      </div>

      {/* Logout Button */}
      <div className="flex-shrink-0 px-2 pb-2">
        <button
          onClick={logout}
          className="group flex items-center w-full px-2 py-2 text-sm font-medium text-destructive rounded-md hover:bg-destructive/10"
        >
          <LogOut className="ml-3 flex-shrink-0 h-5 w-5 text-red-400 group-hover:text-red-500" />
          <span dir="rtl">تسجيل الخروج</span>
        </button>
      </div>
    </div>
  );

  return (
    <div className="h-screen flex overflow-hidden bg-muted">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-white" />
            </button>
          </div>
          <Sidebar mobile={true} />
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <Sidebar />
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        {/* Mobile header */}
        <div className="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
          <button
            className="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-foreground focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
        </div>

        {/* Main content area */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          {children}
        </main>
      </div>
    </div>
  );
};

export default UnifiedLayout;

