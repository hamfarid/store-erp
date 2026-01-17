/**
 * Modern Sidebar Component
 * 
 * A beautiful, collapsible sidebar with modern UI/UX.
 */

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  FileText,
  Users,
  Truck,
  BarChart3,
  Settings,
  HelpCircle,
  LogOut,
  ChevronRight,
  ChevronLeft,
  Store,
  Boxes,
  Receipt,
  UserCircle,
  Building2,
  Warehouse,
  ArrowLeftRight,
  RotateCcw,
  CreditCard,
  PieChart,
  Bell,
  Shield,
  Database,
  Globe
} from 'lucide-react';

// ============================================================================
// Navigation Items Configuration
// ============================================================================

const navigationItems = [
  {
    section: 'القائمة الرئيسية',
    items: [
      { name: 'لوحة التحكم', icon: LayoutDashboard, path: '/', badge: null },
    ]
  },
  {
    section: 'المخزون',
    items: [
      { name: 'المنتجات', icon: Package, path: '/products', badge: null },
      { name: 'الفئات', icon: Boxes, path: '/categories', badge: null },
      { name: 'المستودعات', icon: Warehouse, path: '/warehouses', badge: null },
      { name: 'حركة المخزون', icon: ArrowLeftRight, path: '/stock-movements', badge: null },
    ]
  },
  {
    section: 'المبيعات',
    items: [
      { name: 'فواتير البيع', icon: Receipt, path: '/sales', badge: '12', badgeType: 'primary' },
      { name: 'العملاء', icon: Users, path: '/customers', badge: null },
      { name: 'المرتجعات', icon: RotateCcw, path: '/returns', badge: '3', badgeType: 'warning' },
    ]
  },
  {
    section: 'المشتريات',
    items: [
      { name: 'فواتير الشراء', icon: FileText, path: '/purchases', badge: null },
      { name: 'الموردين', icon: Truck, path: '/suppliers', badge: null },
    ]
  },
  {
    section: 'المالية',
    items: [
      { name: 'المدفوعات', icon: CreditCard, path: '/payments', badge: null },
      { name: 'التقارير', icon: BarChart3, path: '/reports', badge: null },
    ]
  },
  {
    section: 'الإعدادات',
    items: [
      { name: 'إعدادات النظام', icon: Settings, path: '/settings', badge: null },
      { name: 'إدارة المستخدمين', icon: Shield, path: '/users', badge: null },
    ]
  },
];

// ============================================================================
// Navigation Item Component
// ============================================================================

const NavItem = ({ item, isCollapsed, isActive }) => {
  const Icon = item.icon;
  
  return (
    <Link
      to={item.path}
      className={`
        flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative
        ${isActive 
          ? 'bg-gradient-to-l from-amber-500 to-amber-600 text-white shadow-lg shadow-amber-500/30' 
          : 'text-gray-300 hover:bg-white/10 hover:text-white'
        }
      `}
    >
      <Icon size={20} className={isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'} />
      
      {!isCollapsed && (
        <>
          <span className="flex-1 font-medium text-sm">{item.name}</span>
          
          {item.badge && (
            <span className={`
              px-2 py-0.5 text-xs font-bold rounded-full
              ${item.badgeType === 'primary' 
                ? 'bg-teal-500 text-white' 
                : item.badgeType === 'warning'
                ? 'bg-rose-500 text-white'
                : 'bg-white/20 text-white'
              }
            `}>
              {item.badge}
            </span>
          )}
        </>
      )}

      {/* Tooltip for collapsed state */}
      {isCollapsed && (
        <div className="
          absolute right-full mr-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg
          opacity-0 invisible group-hover:opacity-100 group-hover:visible
          transition-all duration-200 whitespace-nowrap z-50
          shadow-xl
        ">
          {item.name}
          <div className="absolute left-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-gray-900" />
        </div>
      )}
    </Link>
  );
};

// ============================================================================
// Section Component
// ============================================================================

const NavSection = ({ section, items, isCollapsed, currentPath }) => (
  <div className="mb-6">
    {!isCollapsed && (
      <h3 className="px-4 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
        {section}
      </h3>
    )}
    <div className="space-y-1">
      {items.map((item, index) => (
        <NavItem
          key={index}
          item={item}
          isCollapsed={isCollapsed}
          isActive={currentPath === item.path}
        />
      ))}
    </div>
  </div>
);

// ============================================================================
// Main Sidebar Component
// ============================================================================

const ModernSidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <aside 
      className={`
        fixed right-0 top-0 h-screen z-40
        bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900
        shadow-2xl transition-all duration-300 ease-in-out
        ${isCollapsed ? 'w-20' : 'w-72'}
      `}
    >
      {/* Logo */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/30">
            <Store className="text-white" size={22} />
          </div>
          {!isCollapsed && (
            <div className="overflow-hidden">
              <h1 className="font-bold text-white text-lg leading-tight">Store Pro</h1>
              <p className="text-xs text-gray-400">نظام إدارة المخزون</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar">
        {navigationItems.map((section, index) => (
          <NavSection
            key={index}
            section={section.section}
            items={section.items}
            isCollapsed={isCollapsed}
            currentPath={currentPath}
          />
        ))}
      </nav>

      {/* Bottom Section */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10 bg-slate-900/50 backdrop-blur">
        {/* User Profile */}
        <div className={`flex items-center gap-3 p-3 rounded-xl bg-white/5 mb-3 ${isCollapsed ? 'justify-center' : ''}`}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center text-white font-bold shadow-lg">
            أ
          </div>
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="font-medium text-white text-sm truncate">أحمد محمد</p>
              <p className="text-xs text-gray-400 truncate">مدير النظام</p>
            </div>
          )}
        </div>

        {/* Collapse Button */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full flex items-center justify-center gap-2 p-3 rounded-xl bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-colors"
        >
          {isCollapsed ? (
            <ChevronLeft size={20} />
          ) : (
            <>
              <ChevronRight size={20} />
              <span className="text-sm">طي القائمة</span>
            </>
          )}
        </button>
      </div>

      {/* Custom Scrollbar Styles */}
      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      `}</style>
    </aside>
  );
};

export default ModernSidebar;

