/**
 * Enhanced Sidebar Component with shadcn/ui
 * @file components/Layout/Sidebar.jsx
 * 
 * Features:
 * - Modern design with Tailwind + Radix
 * - Collapsible groups
 * - Active state indicators
 * - Responsive design
 * - Arabic RTL support
 * - Dark mode support
 */

import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { cn } from '../../lib/utils';
import {
  LayoutDashboard,
  Home,
  Bug,
  Leaf,
  Activity,
  Thermometer,
  Wrench,
  Package,
  GitBranch,
  FileText,
  BarChart3,
  Settings,
  Users,
  Building,
  HelpCircle,
  ChevronDown,
  ChevronLeft,
  Bell,
  User,
  LogOut,
  Sparkles,
  Shield,
  Database,
  Zap,
  FlaskConical,
  Map,
  Layers
} from 'lucide-react';
import * as Collapsible from '@radix-ui/react-collapsible';
import { Button } from '../UI/button';
import { Badge } from '../UI/badge';

// ============================================
// Navigation Configuration
// ============================================
const navigationGroups = [
  {
    id: 'main',
    label: 'الرئيسية',
    items: [
      { path: '/dashboard', label: 'لوحة التحكم', icon: LayoutDashboard },
      { path: '/farms', label: 'المزارع', icon: Home, badge: '24' },
      { path: '/diagnosis', label: 'التشخيص', icon: Bug },
    ]
  },
  {
    id: 'agriculture',
    label: 'الزراعة',
    items: [
      { path: '/diseases', label: 'الأمراض', icon: FlaskConical },
      { path: '/crops', label: 'المحاصيل', icon: Leaf },
      { path: '/breeding', label: 'التهجين', icon: GitBranch },
    ]
  },
  {
    id: 'monitoring',
    label: 'المراقبة',
    items: [
      { path: '/sensors', label: 'المستشعرات', icon: Thermometer },
      { path: '/equipment', label: 'المعدات', icon: Wrench },
      { path: '/inventory', label: 'المخزون', icon: Package },
    ]
  },
  {
    id: 'reports',
    label: 'التقارير',
    items: [
      { path: '/reports', label: 'التقارير', icon: FileText },
      { path: '/analytics', label: 'التحليلات', icon: BarChart3 },
    ]
  },
  {
    id: 'admin',
    label: 'الإدارة',
    items: [
      { path: '/users', label: 'المستخدمين', icon: Users },
      { path: '/companies', label: 'الشركات', icon: Building },
      { path: '/settings', label: 'الإعدادات', icon: Settings },
    ]
  },
];

// ============================================
// NavItem Component
// ============================================
const NavItem = ({ item, collapsed = false }) => {
  const Icon = item.icon;
  
  return (
    <NavLink
      to={item.path}
      className={({ isActive }) => cn(
        "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200",
        "text-gray-600 dark:text-gray-400",
        "hover:bg-gray-100 dark:hover:bg-gray-800",
        isActive && "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 font-medium",
        collapsed && "justify-center px-2"
      )}
    >
      <Icon className="h-5 w-5 flex-shrink-0" />
      {!collapsed && (
        <>
          <span className="flex-1">{item.label}</span>
          {item.badge && (
            <Badge variant="secondary" size="sm">{item.badge}</Badge>
          )}
        </>
      )}
    </NavLink>
  );
};

// ============================================
// NavGroup Component
// ============================================
const NavGroup = ({ group, collapsed = false, defaultOpen = true }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const location = useLocation();
  
  // Check if any item in group is active
  const hasActiveItem = group.items.some(item => location.pathname.startsWith(item.path));

  if (collapsed) {
    return (
      <div className="space-y-1">
        {group.items.map((item) => (
          <NavItem key={item.path} item={item} collapsed />
        ))}
      </div>
    );
  }

  return (
    <Collapsible.Root open={isOpen} onOpenChange={setIsOpen}>
      <Collapsible.Trigger asChild>
        <button
          className={cn(
            "flex items-center justify-between w-full px-3 py-2 text-xs font-semibold uppercase tracking-wider",
            "text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-400",
            "transition-colors"
          )}
        >
          {group.label}
          <ChevronDown className={cn(
            "h-4 w-4 transition-transform",
            isOpen && "rotate-180"
          )} />
        </button>
      </Collapsible.Trigger>
      <Collapsible.Content className="space-y-1 mt-1">
        {group.items.map((item) => (
          <NavItem key={item.path} item={item} />
        ))}
      </Collapsible.Content>
    </Collapsible.Root>
  );
};

// ============================================
// Main Sidebar Component
// ============================================
const Sidebar = ({ isOpen = true, onClose, language = 'ar' }) => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed top-16 h-[calc(100vh-4rem)] z-40 flex flex-col",
          "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700",
          "transition-all duration-300 ease-in-out",
          // RTL Support
          language === 'ar' ? "right-0 border-l" : "left-0 border-r",
          // Width
          collapsed ? "w-20" : "w-64",
          // Mobile visibility
          isOpen ? "translate-x-0" : (language === 'ar' ? "translate-x-full" : "-translate-x-full"),
          "lg:translate-x-0"
        )}
      >
        {/* Logo Section */}
        <div className="p-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            {!collapsed && (
              <div>
                <h2 className="font-bold text-gray-900 dark:text-gray-100">Gaara Scan</h2>
                <p className="text-xs text-gray-500 dark:text-gray-400">نظام الذكاء الاصطناعي</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-6">
          {navigationGroups.map((group) => (
            <NavGroup 
              key={group.id} 
              group={group} 
              collapsed={collapsed}
              defaultOpen={group.id === 'main' || group.id === 'agriculture'}
            />
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-100 dark:border-gray-800">
          {!collapsed ? (
            <div className="space-y-2">
              <NavLink
                to="/help"
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <HelpCircle className="h-5 w-5" />
                <span>المساعدة والدعم</span>
              </NavLink>
              
              {/* Collapse Button */}
              <button
                onClick={() => setCollapsed(true)}
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors w-full"
              >
                <ChevronLeft className="h-5 w-5" />
                <span>تصغير القائمة</span>
              </button>
            </div>
          ) : (
            <button
              onClick={() => setCollapsed(false)}
              className="flex items-center justify-center p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors w-full"
            >
              <ChevronLeft className="h-5 w-5 rotate-180" />
            </button>
          )}
        </div>

        {/* Version Badge */}
        {!collapsed && (
          <div className="px-4 pb-4">
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-800/50">
              <Shield className="h-4 w-4 text-emerald-500" />
              <span className="text-xs text-gray-500 dark:text-gray-400">الإصدار 4.3</span>
            </div>
          </div>
        )}
      </aside>
    </>
  );
};

export default Sidebar;
