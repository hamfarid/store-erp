// -*- javascript -*-
// FILE: frontend/src/theme/index.js | PURPOSE: Unified Design System Theme | OWNER: Frontend | RELATED: App.jsx | LAST-AUDITED: 2025-10-21

/**
 * نظام التصميم الموحد لنظام إدارة المخزون العربي
 * Unified Design System for Arabic Inventory Management System
 * 
 * يحتوي على:
 * - ألوان النظام الموحدة
 * - الخطوط العربية والإنجليزية
 * - المسافات والأحجام
 * - الظلال والحدود
 * - متغيرات RTL/LTR
 */

export const theme = {
  // الألوان الأساسية
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
      950: '#082f49'
    },
    secondary: {
      50: '#fefce8',
      100: '#fef3c7',
      200: '#fde68a',
      300: '#fcd34d',
      400: '#fbbf24',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f'
    },
    success: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d'
    },
    error: {
      50: '#fef2f2',
      100: '#fee2e2',
      200: '#fecaca',
      300: '#fca5a5',
      400: '#f87171',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
      800: '#991b1b',
      900: '#7f1d1d'
    },
    warning: {
      50: '#fffbeb',
      100: '#fef3c7',
      200: '#fde68a',
      300: '#fcd34d',
      400: '#fbbf24',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f'
    },
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827'
    },
    // ألوان خاصة بالنظام
    background: {
      primary: '#ffffff',
      secondary: '#f8fafc',
      tertiary: '#f1f5f9'
    },
    text: {
      primary: '#1e293b',
      secondary: '#475569',
      tertiary: '#64748b',
      inverse: '#ffffff'
    },
    border: {
      light: '#e2e8f0',
      medium: '#cbd5e1',
      dark: '#94a3b8'
    }
  },

  // الخطوط
  fonts: {
    arabic: {
      primary: "'Cairo', 'Noto Sans Arabic', 'Amiri', sans-serif",
      secondary: "'Amiri', 'Noto Sans Arabic', 'Cairo', serif",
      mono: "'Fira Code', 'Courier New', monospace"
    },
    english: {
      primary: "'Inter', 'Segoe UI', 'Roboto', sans-serif",
      secondary: "'Merriweather', 'Georgia', serif",
      mono: "'Fira Code', 'Consolas', 'Monaco', monospace"
    },
    weights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800
    },
    sizes: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
      '5xl': '3rem',    // 48px
      '6xl': '3.75rem'  // 60px
    }
  },

  // المسافات والأحجام
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    7: '1.75rem',   // 28px
    8: '2rem',      // 32px
    9: '2.25rem',   // 36px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
    32: '8rem',     // 128px
    40: '10rem',    // 160px
    48: '12rem',    // 192px
    56: '14rem',    // 224px
    64: '16rem'     // 256px
  },

  // نصف الأقطار (Border Radius)
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    base: '0.25rem',  // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px'
  },

  // الظلال
  shadows: {
    xs: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    base: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    md: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    lg: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    xl: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    none: 'none'
  },

  // نقاط الكسر للتصميم المتجاوب
  breakpoints: {
    xs: '475px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  },

  // الانتقالات والحركات
  transitions: {
    duration: {
      75: '75ms',
      100: '100ms',
      150: '150ms',
      200: '200ms',
      300: '300ms',
      500: '500ms',
      700: '700ms',
      1000: '1000ms'
    },
    timing: {
      linear: 'linear',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
  },

  // الطبقات (Z-Index)
  zIndex: {
    0: 0,
    10: 10,
    20: 20,
    30: 30,
    40: 40,
    50: 50,
    auto: 'auto',
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070
  },

  // إعدادات RTL/LTR
  direction: {
    rtl: {
      textAlign: 'right',
      direction: 'rtl',
      fontFamily: "'Cairo', 'Noto Sans Arabic', 'Amiri', sans-serif"
    },
    ltr: {
      textAlign: 'left',
      direction: 'ltr',
      fontFamily: "'Inter', 'Segoe UI', 'Roboto', sans-serif"
    }
  },

  // مكونات النظام
  components: {
    button: {
      sizes: {
        xs: {
          padding: '0.25rem 0.5rem',
          fontSize: '0.75rem',
          lineHeight: '1rem'
        },
        sm: {
          padding: '0.375rem 0.75rem',
          fontSize: '0.875rem',
          lineHeight: '1.25rem'
        },
        md: {
          padding: '0.5rem 1rem',
          fontSize: '1rem',
          lineHeight: '1.5rem'
        },
        lg: {
          padding: '0.75rem 1.5rem',
          fontSize: '1.125rem',
          lineHeight: '1.75rem'
        },
        xl: {
          padding: '1rem 2rem',
          fontSize: '1.25rem',
          lineHeight: '1.75rem'
        }
      }
    },
    input: {
      sizes: {
        sm: {
          padding: '0.375rem 0.75rem',
          fontSize: '0.875rem',
          lineHeight: '1.25rem'
        },
        md: {
          padding: '0.5rem 0.75rem',
          fontSize: '1rem',
          lineHeight: '1.5rem'
        },
        lg: {
          padding: '0.75rem 1rem',
          fontSize: '1.125rem',
          lineHeight: '1.75rem'
        }
      }
    },
    card: {
      padding: {
        sm: '1rem',
        md: '1.5rem',
        lg: '2rem'
      }
    }
  }
};

// دوال مساعدة للثيم
export const getColor = (colorPath) => {
  const keys = colorPath.split('.');
  let value = theme.colors;
  
  for (const key of keys) {
    value = value[key];
    if (!value) return null;
  }
  
  return value;
};

export const getSpacing = (size) => {
  return theme.spacing[size] || size;
};

export const getFontFamily = (language = 'arabic', type = 'primary') => {
  return theme.fonts[language]?.[type] || theme.fonts.arabic.primary;
};

export const getBreakpoint = (size) => {
  return theme.breakpoints[size];
};

// CSS متغيرات للاستخدام في CSS
export const cssVariables = {
  '--color-primary-50': theme.colors.primary[50],
  '--color-primary-500': theme.colors.primary[500],
  '--color-primary-600': theme.colors.primary[600],
  '--color-primary-700': theme.colors.primary[700],
  '--color-secondary-500': theme.colors.secondary[500],
  '--color-success-500': theme.colors.success[500],
  '--color-error-500': theme.colors.error[500],
  '--color-warning-500': theme.colors.warning[500],
  '--color-gray-100': theme.colors.gray[100],
  '--color-gray-200': theme.colors.gray[200],
  '--color-gray-300': theme.colors.gray[300],
  '--color-gray-500': theme.colors.gray[500],
  '--color-gray-700': theme.colors.gray[700],
  '--color-gray-900': theme.colors.gray[900],
  '--font-arabic': theme.fonts.arabic.primary,
  '--font-english': theme.fonts.english.primary,
  '--spacing-1': theme.spacing[1],
  '--spacing-2': theme.spacing[2],
  '--spacing-4': theme.spacing[4],
  '--spacing-8': theme.spacing[8],
  '--border-radius-md': theme.borderRadius.md,
  '--shadow-md': theme.shadows.md,
  '--transition-duration': theme.transitions.duration[200]
};

export default theme;
