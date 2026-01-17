/**
 * useTheme Hook
 * @file frontend/src/hooks/useTheme.js
 * 
 * Hook لإدارة الوضع الداكن/الفاتح
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useLocalStorage } from './useLocalStorage';

const THEME_KEY = 'app-theme';
const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system'
};

/**
 * Hook لإدارة السمة (الوضع الداكن/الفاتح)
 * @returns {Object} - { theme, setTheme, toggleTheme, isDark, isLight }
 */
export function useTheme() {
  const [storedTheme, setStoredTheme] = useLocalStorage(THEME_KEY, THEMES.SYSTEM);
  const [systemTheme, setSystemTheme] = useState(
    typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? THEMES.DARK
      : THEMES.LIGHT
  );

  // Listen for system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      setSystemTheme(e.matches ? THEMES.DARK : THEMES.LIGHT);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  // Compute actual theme
  const actualTheme = useMemo(() => {
    if (storedTheme === THEMES.SYSTEM) {
      return systemTheme;
    }
    return storedTheme;
  }, [storedTheme, systemTheme]);

  // Apply theme to document
  useEffect(() => {
    const root = window.document.documentElement;
    
    root.classList.remove(THEMES.LIGHT, THEMES.DARK);
    root.classList.add(actualTheme);
    
    // Set data attribute for CSS
    root.setAttribute('data-theme', actualTheme);
    
    // Update meta theme-color
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute(
        'content',
        actualTheme === THEMES.DARK ? '#1f2937' : '#ffffff'
      );
    }
  }, [actualTheme]);

  // Set theme
  const setTheme = useCallback((theme) => {
    if (Object.values(THEMES).includes(theme)) {
      setStoredTheme(theme);
    }
  }, [setStoredTheme]);

  // Toggle between light and dark
  const toggleTheme = useCallback(() => {
    if (actualTheme === THEMES.DARK) {
      setStoredTheme(THEMES.LIGHT);
    } else {
      setStoredTheme(THEMES.DARK);
    }
  }, [actualTheme, setStoredTheme]);

  // Set specific themes
  const setLightTheme = useCallback(() => setTheme(THEMES.LIGHT), [setTheme]);
  const setDarkTheme = useCallback(() => setTheme(THEMES.DARK), [setTheme]);
  const setSystemThemePreference = useCallback(() => setTheme(THEMES.SYSTEM), [setTheme]);

  return {
    theme: storedTheme,
    actualTheme,
    systemTheme,
    setTheme,
    toggleTheme,
    setLightTheme,
    setDarkTheme,
    setSystemThemePreference,
    isDark: actualTheme === THEMES.DARK,
    isLight: actualTheme === THEMES.LIGHT,
    isSystem: storedTheme === THEMES.SYSTEM,
    themes: THEMES
  };
}

/**
 * Hook للتحقق من تفضيل الحركة المخفضة
 * @returns {boolean}
 */
export function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(
    typeof window !== 'undefined'
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    const handleChange = (e) => {
      setPrefersReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return prefersReducedMotion;
}

/**
 * Hook للتحقق من حجم الشاشة
 * @returns {Object}
 */
export function useMediaQuery(query) {
  const [matches, setMatches] = useState(
    typeof window !== 'undefined'
      ? window.matchMedia(query).matches
      : false
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    
    const handleChange = (e) => {
      setMatches(e.matches);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [query]);

  return matches;
}

export { THEMES };
export default useTheme;
