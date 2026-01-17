// -*- javascript -*-
// FILE: frontend/src/components/ui/command-palette.jsx
// PURPOSE: Global Command Palette (Ctrl+K / ⌘+K)
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

/**
 * Command Palette Component
 * Global search and navigation using Ctrl+K (Windows) or ⌘+K (Mac)
 * 
 * Features:
 * - Global keyboard shortcut
 * - Page navigation
 * - Quick actions
 * - Recent items
 * - Theme toggle
 * - User actions
 */

import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Calculator,
  Calendar,
  CreditCard,
  FileText,
  Home,
  Moon,
  Package,
  Settings,
  Sun,
  User,
  Users,
  Search,
  LayoutDashboard,
  ShoppingCart,
  Truck,
  BarChart3,
  Warehouse,
  LogOut,
  UserCog,
  FileSpreadsheet,
} from 'lucide-react';

import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from './command';
import { useTheme } from './theme-toggle';

/**
 * Hook to toggle Command Palette
 */
export function useCommandPalette() {
  const [open, setOpen] = React.useState(false);

  React.useEffect(() => {
    const down = (e) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  return { open, setOpen };
}

/**
 * Command Palette Provider
 * Wraps your app to provide global command palette functionality
 * 
 * @example
 * function App() {
 *   return (
 *     <CommandPaletteProvider>
 *       <Routes />
 *     </CommandPaletteProvider>
 *   );
 * }
 */
export function CommandPaletteProvider({ children }) {
  const { open, setOpen } = useCommandPalette();

  return (
    <>
      {children}
      <CommandPalette open={open} onOpenChange={setOpen} />
    </>
  );
}

/**
 * Command Palette Dialog
 */
export function CommandPalette({ open, onOpenChange }) {
  const navigate = useNavigate();
  const { setTheme } = useTheme();

  const runCommand = React.useCallback((command) => {
    onOpenChange(false);
    command();
  }, [onOpenChange]);

  // Navigation items
  const navigationItems = [
    { icon: LayoutDashboard, label: 'لوحة التحكم', href: '/dashboard', shortcut: 'D' },
    { icon: Package, label: 'المنتجات', href: '/products', shortcut: 'P' },
    { icon: ShoppingCart, label: 'الفواتير', href: '/invoices', shortcut: 'I' },
    { icon: Users, label: 'العملاء', href: '/customers', shortcut: 'C' },
    { icon: Truck, label: 'الموردين', href: '/suppliers', shortcut: 'S' },
    { icon: Warehouse, label: 'المخازن', href: '/warehouses', shortcut: 'W' },
    { icon: BarChart3, label: 'التقارير', href: '/reports', shortcut: 'R' },
    { icon: Settings, label: 'الإعدادات', href: '/settings', shortcut: ',' },
  ];

  // Quick actions
  const quickActions = [
    { icon: Package, label: 'إضافة منتج جديد', action: () => navigate('/products/new') },
    { icon: ShoppingCart, label: 'إنشاء فاتورة', action: () => navigate('/invoices/new') },
    { icon: Users, label: 'إضافة عميل', action: () => navigate('/customers/new') },
    { icon: Truck, label: 'إضافة مورد', action: () => navigate('/suppliers/new') },
    { icon: FileSpreadsheet, label: 'تصدير التقرير', action: () => navigate('/reports/export') },
  ];

  // User actions
  const userActions = [
    { icon: User, label: 'الملف الشخصي', action: () => navigate('/profile') },
    { icon: UserCog, label: 'إعدادات الحساب', action: () => navigate('/settings/account') },
    { icon: LogOut, label: 'تسجيل الخروج', action: () => navigate('/logout') },
  ];

  return (
    <CommandDialog 
      open={open} 
      onOpenChange={onOpenChange}
      title="البحث السريع"
      description="ابحث عن صفحة أو إجراء..."
    >
      <CommandInput placeholder="اكتب للبحث..." />
      <CommandList>
        <CommandEmpty>لا توجد نتائج</CommandEmpty>
        
        {/* Navigation */}
        <CommandGroup heading="التنقل">
          {navigationItems.map((item) => (
            <CommandItem
              key={item.href}
              onSelect={() => runCommand(() => navigate(item.href))}
            >
              <item.icon className="ml-2 h-4 w-4" />
              <span>{item.label}</span>
              {item.shortcut && (
                <CommandShortcut>⌘{item.shortcut}</CommandShortcut>
              )}
            </CommandItem>
          ))}
        </CommandGroup>

        <CommandSeparator />

        {/* Quick Actions */}
        <CommandGroup heading="إجراءات سريعة">
          {quickActions.map((item, index) => (
            <CommandItem
              key={index}
              onSelect={() => runCommand(item.action)}
            >
              <item.icon className="ml-2 h-4 w-4" />
              <span>{item.label}</span>
            </CommandItem>
          ))}
        </CommandGroup>

        <CommandSeparator />

        {/* Theme */}
        <CommandGroup heading="المظهر">
          <CommandItem onSelect={() => runCommand(() => setTheme('light'))}>
            <Sun className="ml-2 h-4 w-4" />
            <span>الوضع الفاتح</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => setTheme('dark'))}>
            <Moon className="ml-2 h-4 w-4" />
            <span>الوضع الداكن</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => setTheme('system'))}>
            <Settings className="ml-2 h-4 w-4" />
            <span>حسب النظام</span>
          </CommandItem>
        </CommandGroup>

        <CommandSeparator />

        {/* User Actions */}
        <CommandGroup heading="الحساب">
          {userActions.map((item, index) => (
            <CommandItem
              key={index}
              onSelect={() => runCommand(item.action)}
            >
              <item.icon className="ml-2 h-4 w-4" />
              <span>{item.label}</span>
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}

/**
 * Command Palette Trigger Button
 * Shows the keyboard shortcut hint
 * 
 * @example
 * <CommandPaletteTrigger />
 */
export function CommandPaletteTrigger({ className }) {
  const { setOpen } = useCommandPalette();

  return (
    <button
      onClick={() => setOpen(true)}
      className={cn(
        "inline-flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground",
        "border rounded-md bg-background hover:bg-accent hover:text-accent-foreground",
        "transition-colors cursor-pointer",
        className
      )}
    >
      <Search className="h-4 w-4" />
      <span className="hidden md:inline">بحث...</span>
      <kbd className="pointer-events-none hidden h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-xs font-medium opacity-100 sm:flex">
        <span className="text-xs">⌘</span>K
      </kbd>
    </button>
  );
}

// Helper for cn
function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default CommandPalette;

