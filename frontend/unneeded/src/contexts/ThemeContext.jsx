/**
 * Theme Context - Light/Dark Mode Support
 * 
 * Provides theme management with:
 * - Light/Dark mode toggle
 * - localStorage persistence
 * - System preference detection
 * - CSS variable updates
 */

import React, { createContext, useContext, useState, useEffect } from 'react';

// Create Theme Context
const ThemeContext = createContext();

// Theme modes
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
};

// Local storage key
const THEME_STORAGE_KEY = 'store-erp-theme';

/**
 * Theme Provider Component
 */
export const ThemeProvider = ({ children }) => {
  // Get initial theme from localStorage or default to system
  const getInitialTheme = () => {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    if (savedTheme && Object.values(THEMES).includes(savedTheme)) {
      return savedTheme;
    }
    return THEMES.SYSTEM;
  };

  const [theme, setTheme] = useState(getInitialTheme);
  const [resolvedTheme, setResolvedTheme] = useState(THEMES.LIGHT);

  /**
   * Get system theme preference
   */
  const getSystemTheme = () => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return THEMES.DARK;
    }
    return THEMES.LIGHT;
  };

  /**
   * Resolve theme (handle 'system' option)
   */
  const resolveTheme = (currentTheme) => {
    if (currentTheme === THEMES.SYSTEM) {
      return getSystemTheme();
    }
    return currentTheme;
  };

  /**
   * Apply theme to document
   */
  const applyTheme = (themeToApply) => {
    const root = document.documentElement;
    
    // Remove existing theme classes
    root.classList.remove('light', 'dark');
    
    // Add new theme class
    root.classList.add(themeToApply);
    
    // Update data attribute
    root.setAttribute('data-theme', themeToApply);
    
    // Update CSS variables based on theme
    if (themeToApply === THEMES.DARK) {
      applyDarkTheme(root);
    } else {
      applyLightTheme(root);
    }
  };

  /**
   * Apply light theme CSS variables - Gaara Seeds Brand
   */
  const applyLightTheme = (root) => {
    // Background colors - Light theme with Gaara tones
    root.style.setProperty('--bg-primary', '#FFFFFF');
    root.style.setProperty('--bg-secondary', '#E7F0E9');
    root.style.setProperty('--bg-tertiary', '#BFCBC2');

    // Text colors - Dark text on light background
    root.style.setProperty('--text-primary', '#10271D');
    root.style.setProperty('--text-secondary', '#708079');
    root.style.setProperty('--text-tertiary', '#7A7A7A');

    // Border colors - Subtle Gaara greens
    root.style.setProperty('--border-light', '#E7F0E9');
    root.style.setProperty('--border-base', '#BFCBC2');
    root.style.setProperty('--border-dark', '#708079');

    // Brand colors
    root.style.setProperty('--primary-color', '#80AA45');
    root.style.setProperty('--secondary-color', '#3B715A');
    root.style.setProperty('--accent-color', '#E65E36');
  };

  /**
   * Apply dark theme CSS variables - Gaara Seeds Brand
   */
  const applyDarkTheme = (root) => {
    // Background colors - Dark theme with Gaara tones
    root.style.setProperty('--bg-primary', '#10271D');
    root.style.setProperty('--bg-secondary', '#22523D');
    root.style.setProperty('--bg-tertiary', '#3B715A');

    // Text colors - Light text on dark background
    root.style.setProperty('--text-primary', '#E7F0E9');
    root.style.setProperty('--text-secondary', '#BFCBC2');
    root.style.setProperty('--text-tertiary', '#708079');

    // Border colors - Darker Gaara greens
    root.style.setProperty('--border-light', '#3B715A');
    root.style.setProperty('--border-base', '#708079');
    root.style.setProperty('--border-dark', '#BFCBC2');

    // Brand colors (same in both themes)
    root.style.setProperty('--primary-color', '#80AA45');
    root.style.setProperty('--secondary-color', '#3B715A');
    root.style.setProperty('--accent-color', '#E65E36');
  };

  /**
   * Change theme
   */
  const changeTheme = (newTheme) => {
    if (!Object.values(THEMES).includes(newTheme)) {
      console.error(`Invalid theme: ${newTheme}`);
      return;
    }
    
    setTheme(newTheme);
    localStorage.setItem(THEME_STORAGE_KEY, newTheme);
    
    const resolved = resolveTheme(newTheme);
    setResolvedTheme(resolved);
    applyTheme(resolved);
  };

  /**
   * Toggle between light and dark
   */
  const toggleTheme = () => {
    const newTheme = resolvedTheme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT;
    changeTheme(newTheme);
  };

  /**
   * Initialize theme on mount
   */
  useEffect(() => {
    const resolved = resolveTheme(theme);
    setResolvedTheme(resolved);
    applyTheme(resolved);
  }, []);

  /**
   * Listen for system theme changes
   */
  useEffect(() => {
    if (theme !== THEMES.SYSTEM) return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      const newResolvedTheme = e.matches ? THEMES.DARK : THEMES.LIGHT;
      setResolvedTheme(newResolvedTheme);
      applyTheme(newResolvedTheme);
    };

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } 
    // Legacy browsers
    else if (mediaQuery.addListener) {
      mediaQuery.addListener(handleChange);
      return () => mediaQuery.removeListener(handleChange);
    }
  }, [theme]);

  /**
   * Context value
   */
  const value = {
    theme,              // Current theme setting (light/dark/system)
    resolvedTheme,      // Actual theme being used (light/dark)
    changeTheme,        // Function to change theme
    toggleTheme,        // Function to toggle between light/dark
    isLight: resolvedTheme === THEMES.LIGHT,
    isDark: resolvedTheme === THEMES.DARK,
    isSystem: theme === THEMES.SYSTEM,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

/**
 * useTheme Hook
 * 
 * Usage:
 * const { theme, resolvedTheme, changeTheme, toggleTheme, isLight, isDark } = useTheme();
 */
export const useTheme = () => {
  const context = useContext(ThemeContext);
  
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  
  return context;
};

/**
 * Theme Toggle Button Component
 */
export const ThemeToggle = ({ className = '' }) => {
  const { resolvedTheme, toggleTheme } = useTheme();
  
  return (
    <button
      onClick={toggleTheme}
      className={`
        p-2 rounded-lg
        bg-background-secondary hover:bg-background-tertiary
        border border-border-base
        transition-all duration-base
        focus:outline-none focus:ring-2 focus:ring-primary-500
        ${className}
      `}
      aria-label={resolvedTheme === THEMES.LIGHT ? 'تفعيل الوضع الداكن' : 'تفعيل الوضع الفاتح'}
      title={resolvedTheme === THEMES.LIGHT ? 'تفعيل الوضع الداكن' : 'تفعيل الوضع الفاتح'}
    >
      {resolvedTheme === THEMES.LIGHT ? (
        // Moon icon for dark mode
        <svg
          className="w-5 h-5 text-text-primary"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
          />
        </svg>
      ) : (
        // Sun icon for light mode
        <svg
          className="w-5 h-5 text-text-primary"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
      )}
    </button>
  );
};

/**
 * Theme Selector Component (Light/Dark/System)
 */
export const ThemeSelector = ({ className = '' }) => {
  const { theme, changeTheme } = useTheme();
  
  return (
    <div className={`flex gap-2 ${className}`}>
      <button
        onClick={() => changeTheme(THEMES.LIGHT)}
        className={`
          px-4 py-2 rounded-lg font-medium
          transition-all duration-base
          ${theme === THEMES.LIGHT
            ? 'bg-primary-500 text-white'
            : 'bg-background-secondary text-text-primary hover:bg-background-tertiary'
          }
        `}
      >
        فاتح
      </button>
      
      <button
        onClick={() => changeTheme(THEMES.DARK)}
        className={`
          px-4 py-2 rounded-lg font-medium
          transition-all duration-base
          ${theme === THEMES.DARK
            ? 'bg-primary-500 text-white'
            : 'bg-background-secondary text-text-primary hover:bg-background-tertiary'
          }
        `}
      >
        داكن
      </button>
      
      <button
        onClick={() => changeTheme(THEMES.SYSTEM)}
        className={`
          px-4 py-2 rounded-lg font-medium
          transition-all duration-base
          ${theme === THEMES.SYSTEM
            ? 'bg-primary-500 text-white'
            : 'bg-background-secondary text-text-primary hover:bg-background-tertiary'
          }
        `}
      >
        النظام
      </button>
    </div>
  );
};

export default ThemeContext;

