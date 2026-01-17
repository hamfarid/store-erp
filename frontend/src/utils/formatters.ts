/**
 * P3.77: Formatting Utilities
 * 
 * Currency, number, and date formatting utilities.
 */

// =============================================================================
// Currency Formatting
// =============================================================================

export interface CurrencyOptions {
  currency?: string;
  locale?: string;
  decimals?: number;
  showSymbol?: boolean;
}

const defaultCurrency: CurrencyOptions = {
  currency: 'EGP',
  locale: 'ar-SA',
  decimals: 2,
  showSymbol: true,
};

export function formatCurrency(
  amount: number,
  options: CurrencyOptions = {}
): string {
  const opts = { ...defaultCurrency, ...options };
  
  if (opts.showSymbol) {
    return new Intl.NumberFormat(opts.locale, {
      style: 'currency',
      currency: opts.currency,
      minimumFractionDigits: opts.decimals,
      maximumFractionDigits: opts.decimals,
    }).format(amount);
  }
  
  return formatNumber(amount, { decimals: opts.decimals, locale: opts.locale });
}

export function parseCurrency(value: string): number {
  // Remove currency symbols and separators
  const cleaned = value.replace(/[^\d.-]/g, '');
  return parseFloat(cleaned) || 0;
}

// Currency symbols
export const currencySymbols: Record<string, string> = {
  EGP: 'ج.م',
  USD: '$',
  EUR: '€',
  GBP: '£',
  AED: 'د.إ',
  KWD: 'د.ك',
  EGP: 'ج.م',
  QAR: 'ر.ق',
  BHD: 'د.ب',
  OMR: 'ر.ع',
  JOD: 'د.أ',
};

export function getCurrencySymbol(currency: string): string {
  return currencySymbols[currency] || currency;
}

// =============================================================================
// Number Formatting
// =============================================================================

export interface NumberOptions {
  decimals?: number;
  locale?: string;
  compact?: boolean;
  sign?: boolean;
}

export function formatNumber(
  value: number,
  options: NumberOptions = {}
): string {
  const { decimals = 0, locale = 'ar-SA', compact = false, sign = false } = options;
  
  const formatOptions: Intl.NumberFormatOptions = {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  };
  
  if (compact) {
    formatOptions.notation = 'compact';
    formatOptions.compactDisplay = 'short';
  }
  
  if (sign && value > 0) {
    formatOptions.signDisplay = 'always';
  }
  
  return new Intl.NumberFormat(locale, formatOptions).format(value);
}

export function formatPercent(
  value: number,
  options: { decimals?: number; locale?: string } = {}
): string {
  const { decimals = 1, locale = 'ar-SA' } = options;
  
  return new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
}

export function formatCompact(value: number): string {
  if (value >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(1)}B`;
  }
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1)}M`;
  }
  if (value >= 1_000) {
    return `${(value / 1_000).toFixed(1)}K`;
  }
  return value.toString();
}

// Arabic number formatting
export function formatArabicNumber(value: number): string {
  const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return value.toString().replace(/[0-9]/g, (d) => arabicNumerals[parseInt(d)]);
}

// =============================================================================
// Date Formatting
// =============================================================================

export interface DateOptions {
  locale?: string;
  style?: 'full' | 'long' | 'medium' | 'short';
  includeTime?: boolean;
  relative?: boolean;
}

export function formatDate(
  date: Date | string | number,
  options: DateOptions = {}
): string {
  const { locale = 'ar-SA', style = 'medium', includeTime = false, relative = false } = options;
  const d = new Date(date);
  
  if (relative) {
    return formatRelativeTime(d);
  }
  
  const dateOptions: Intl.DateTimeFormatOptions = {
    dateStyle: style,
  };
  
  if (includeTime) {
    dateOptions.timeStyle = 'short';
  }
  
  return new Intl.DateTimeFormat(locale, dateOptions).format(d);
}

export function formatTime(date: Date | string | number, locale = 'ar-SA'): string {
  const d = new Date(date);
  return new Intl.DateTimeFormat(locale, { timeStyle: 'short' }).format(d);
}

export function formatRelativeTime(date: Date | string | number): string {
  const d = new Date(date);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const weeks = Math.floor(days / 7);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);
  
  if (years > 0) return `منذ ${years} سنة`;
  if (months > 0) return `منذ ${months} شهر`;
  if (weeks > 0) return `منذ ${weeks} أسبوع`;
  if (days > 0) return `منذ ${days} يوم`;
  if (hours > 0) return `منذ ${hours} ساعة`;
  if (minutes > 0) return `منذ ${minutes} دقيقة`;
  return 'الآن';
}

export function formatDateRange(start: Date, end: Date, locale = 'ar-SA'): string {
  const formatter = new Intl.DateTimeFormat(locale, { dateStyle: 'medium' });
  return `${formatter.format(start)} - ${formatter.format(end)}`;
}

// =============================================================================
// Text Formatting
// =============================================================================

export function truncate(text: string, maxLength: number, suffix = '...'): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - suffix.length) + suffix;
}

export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

export function titleCase(text: string): string {
  return text.split(' ').map(capitalize).join(' ');
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function pluralize(count: number, singular: string, plural: string): string {
  return count === 1 ? singular : plural;
}

// Arabic pluralization (simplified)
export function pluralizeArabic(count: number, singular: string, dual: string, plural: string): string {
  if (count === 1) return singular;
  if (count === 2) return dual;
  return plural;
}

// =============================================================================
// Phone Formatting
// =============================================================================

export function formatPhone(phone: string, countryCode = '+966'): string {
  // Remove non-digits
  const digits = phone.replace(/\D/g, '');
  
  // Saudi format: +966 5X XXX XXXX
  if (digits.length === 9 && digits.startsWith('5')) {
    return `${countryCode} ${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(5)}`;
  }
  
  // If starts with country code
  if (digits.startsWith('966')) {
    const local = digits.slice(3);
    return `+966 ${local.slice(0, 2)} ${local.slice(2, 5)} ${local.slice(5)}`;
  }
  
  return phone;
}

// =============================================================================
// File Size Formatting
// =============================================================================

export function formatFileSize(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let unitIndex = 0;
  let size = bytes;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

// =============================================================================
// Export
// =============================================================================

export default {
  formatCurrency,
  parseCurrency,
  getCurrencySymbol,
  formatNumber,
  formatPercent,
  formatCompact,
  formatArabicNumber,
  formatDate,
  formatTime,
  formatRelativeTime,
  formatDateRange,
  truncate,
  capitalize,
  titleCase,
  slugify,
  pluralize,
  pluralizeArabic,
  formatPhone,
  formatFileSize,
};

