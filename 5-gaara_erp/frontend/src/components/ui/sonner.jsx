// -*- javascript -*-
// FILE: frontend/src/components/ui/sonner.jsx
// PURPOSE: Toast Notification System using Sonner
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

/**
 * Toast/Notification System
 * Uses Sonner for beautiful, accessible toast notifications
 * 
 * Features:
 * - RTL support
 * - Dark mode support
 * - Rich toast types (success, error, warning, info)
 * - Custom styling matching the design system
 */

import { Toaster as Sonner, toast } from "sonner";

/**
 * Toaster Provider Component
 * Place this at the root of your app
 * 
 * @example
 * // In App.jsx or main.jsx
 * import { Toaster } from '@/components/ui/sonner';
 * 
 * function App() {
 *   return (
 *     <>
 *       <Toaster />
 *       <Routes />
 *     </>
 *   );
 * }
 */
const Toaster = ({ ...props }) => {
  // Check if dark mode is enabled
  const isDark = typeof document !== 'undefined' && 
    document.documentElement.classList.contains('dark');

  return (
    <Sonner
      theme={isDark ? 'dark' : 'light'}
      className="toaster group"
      position="bottom-left"
      dir="rtl"
      closeButton
      richColors
      toastOptions={{
        classNames: {
          toast: [
            'group toast',
            'group-[.toaster]:bg-background',
            'group-[.toaster]:text-foreground',
            'group-[.toaster]:border-border',
            'group-[.toaster]:shadow-lg',
            'group-[.toaster]:rounded-lg',
          ].join(' '),
          description: 'group-[.toast]:text-muted-foreground',
          actionButton: [
            'group-[.toast]:bg-primary',
            'group-[.toast]:text-primary-foreground',
          ].join(' '),
          cancelButton: [
            'group-[.toast]:bg-muted',
            'group-[.toast]:text-muted-foreground',
          ].join(' '),
          success: [
            'group-[.toaster]:bg-emerald-50',
            'group-[.toaster]:text-emerald-900',
            'group-[.toaster]:border-emerald-200',
            'dark:group-[.toaster]:bg-emerald-950',
            'dark:group-[.toaster]:text-emerald-100',
            'dark:group-[.toaster]:border-emerald-800',
          ].join(' '),
          error: [
            'group-[.toaster]:bg-rose-50',
            'group-[.toaster]:text-rose-900',
            'group-[.toaster]:border-rose-200',
            'dark:group-[.toaster]:bg-rose-950',
            'dark:group-[.toaster]:text-rose-100',
            'dark:group-[.toaster]:border-rose-800',
          ].join(' '),
          warning: [
            'group-[.toaster]:bg-amber-50',
            'group-[.toaster]:text-amber-900',
            'group-[.toaster]:border-amber-200',
            'dark:group-[.toaster]:bg-amber-950',
            'dark:group-[.toaster]:text-amber-100',
            'dark:group-[.toaster]:border-amber-800',
          ].join(' '),
          info: [
            'group-[.toaster]:bg-blue-50',
            'group-[.toaster]:text-blue-900',
            'group-[.toaster]:border-blue-200',
            'dark:group-[.toaster]:bg-blue-950',
            'dark:group-[.toaster]:text-blue-100',
            'dark:group-[.toaster]:border-blue-800',
          ].join(' '),
        },
      }}
      style={{
        '--normal-bg': 'hsl(var(--popover))',
        '--normal-text': 'hsl(var(--popover-foreground))',
        '--normal-border': 'hsl(var(--border))',
        '--success-bg': 'hsl(142 76% 36%)',
        '--success-text': 'hsl(0 0% 100%)',
        '--error-bg': 'hsl(0 72% 51%)',
        '--error-text': 'hsl(0 0% 100%)',
      }}
      {...props}
    />
  );
};

/**
 * Toast utility functions
 * 
 * @example
 * import { toast } from '@/components/ui/sonner';
 * 
 * // Success toast
 * toast.success('تم الحفظ بنجاح');
 * 
 * // Error toast
 * toast.error('حدث خطأ أثناء الحفظ');
 * 
 * // Warning toast
 * toast.warning('تحذير: البيانات غير مكتملة');
 * 
 * // Info toast
 * toast.info('معلومة: يتم معالجة طلبك');
 * 
 * // With action
 * toast.success('تم الحذف', {
 *   action: {
 *     label: 'تراجع',
 *     onClick: () => handleUndo(),
 *   },
 * });
 * 
 * // Promise toast
 * toast.promise(saveData(), {
 *   loading: 'جاري الحفظ...',
 *   success: 'تم الحفظ بنجاح',
 *   error: 'فشل الحفظ',
 * });
 */

export { Toaster, toast };
