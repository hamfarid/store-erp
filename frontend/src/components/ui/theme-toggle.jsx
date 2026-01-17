// -*- javascript -*-
// FILE: frontend/src/components/ui/theme-toggle.jsx
// PURPOSE: Dark/Light Theme Toggle Component
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

/**
 * Theme Toggle Component
 * Switches between light and dark modes with smooth animation
 * 
 * Features:
 * - Persists preference to localStorage
 * - System preference detection
 * - Smooth icon transition animation
 * - Keyboard accessible
 */

import * as React from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';
import { Button } from './button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './dropdown-menu';
import { cn } from '@/lib/utils';

const THEME_KEY = 'store-theme';

/**
 * Hook to manage theme state
 */
export function useTheme() {
  const [theme, setThemeState] = React.useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(THEME_KEY) || 'system';
    }
    return 'system';
  });

  React.useEffect(() => {
    const root = window.document.documentElement;
    
    // Remove old theme class
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }

    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  // Listen for system theme changes
  React.useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = () => {
      if (theme === 'system') {
        const root = window.document.documentElement;
        root.classList.remove('light', 'dark');
        root.classList.add(mediaQuery.matches ? 'dark' : 'light');
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  return { theme, setTheme: setThemeState };
}

/**
 * Simple Theme Toggle Button
 * Toggles between light and dark mode
 * 
 * @example
 * <ThemeToggle />
 */
export function ThemeToggle({ className, variant = 'ghost' }) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant={variant} size="icon" className={cn('h-9 w-9', className)} disabled>
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const isDark = theme === 'dark' || 
    (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

  return (
    <Button
      variant={variant}
      size="icon"
      onClick={toggleTheme}
      className={cn('h-9 w-9 relative', className)}
      aria-label={isDark ? 'تبديل إلى الوضع الفاتح' : 'تبديل إلى الوضع الداكن'}
    >
      <Sun 
        className={cn(
          'h-4 w-4 transition-all duration-300',
          isDark ? 'rotate-90 scale-0' : 'rotate-0 scale-100'
        )} 
      />
      <Moon 
        className={cn(
          'absolute h-4 w-4 transition-all duration-300',
          isDark ? 'rotate-0 scale-100' : '-rotate-90 scale-0'
        )} 
      />
    </Button>
  );
}

/**
 * Theme Toggle Dropdown
 * Allows selection between light, dark, and system themes
 * 
 * @example
 * <ThemeToggleDropdown />
 */
export function ThemeToggleDropdown({ className }) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon" className={cn('h-9 w-9', className)} disabled>
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  const isDark = theme === 'dark' || 
    (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button 
          variant="ghost" 
          size="icon"
          className={cn('h-9 w-9 relative', className)}
          aria-label="تبديل المظهر"
        >
          <Sun 
            className={cn(
              'h-4 w-4 transition-all duration-300',
              isDark ? 'rotate-90 scale-0' : 'rotate-0 scale-100'
            )} 
          />
          <Moon 
            className={cn(
              'absolute h-4 w-4 transition-all duration-300',
              isDark ? 'rotate-0 scale-100' : '-rotate-90 scale-0'
            )} 
          />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-[120px]">
        <DropdownMenuItem 
          onClick={() => setTheme('light')}
          className={cn(theme === 'light' && 'bg-accent')}
        >
          <Sun className="ml-2 h-4 w-4" />
          <span>فاتح</span>
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={() => setTheme('dark')}
          className={cn(theme === 'dark' && 'bg-accent')}
        >
          <Moon className="ml-2 h-4 w-4" />
          <span>داكن</span>
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={() => setTheme('system')}
          className={cn(theme === 'system' && 'bg-accent')}
        >
          <Monitor className="ml-2 h-4 w-4" />
          <span>النظام</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default ThemeToggle;

