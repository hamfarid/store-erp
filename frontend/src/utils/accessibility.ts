/**
 * P1.50: WCAG AA Accessibility Utilities
 * 
 * Provides utilities for checking WCAG 2.1 AA compliance:
 * - Color contrast ratio calculations
 * - Accessible color suggestions
 * - Focus management
 * - Screen reader announcements
 */

// =============================================================================
// Color Types
// =============================================================================

interface RGB {
  r: number;
  g: number;
  b: number;
}

interface HSL {
  h: number;
  s: number;
  l: number;
}

interface ContrastResult {
  ratio: number;
  passesAA: boolean;
  passesAALarge: boolean;
  passesAAA: boolean;
  passesAAALarge: boolean;
  level: 'AAA' | 'AA' | 'AA Large' | 'Fail';
}

// =============================================================================
// WCAG Contrast Requirements
// =============================================================================

// WCAG 2.1 minimum contrast ratios
const WCAG_AA_NORMAL = 4.5;    // Normal text (< 18pt or < 14pt bold)
const WCAG_AA_LARGE = 3.0;     // Large text (>= 18pt or >= 14pt bold)
const WCAG_AAA_NORMAL = 7.0;   // Enhanced: Normal text
const WCAG_AAA_LARGE = 4.5;    // Enhanced: Large text

// =============================================================================
// Color Parsing
// =============================================================================

/**
 * Parse a color string to RGB values.
 */
export function parseColor(color: string): RGB | null {
  if (!color) return null;
  
  // Remove whitespace
  color = color.trim();
  
  // Hex color
  if (color.startsWith('#')) {
    return hexToRgb(color);
  }
  
  // RGB/RGBA
  const rgbMatch = color.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
  if (rgbMatch) {
    return {
      r: parseInt(rgbMatch[1], 10),
      g: parseInt(rgbMatch[2], 10),
      b: parseInt(rgbMatch[3], 10),
    };
  }
  
  // HSL/HSLA
  const hslMatch = color.match(/hsla?\s*\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%/i);
  if (hslMatch) {
    return hslToRgb({
      h: parseInt(hslMatch[1], 10),
      s: parseInt(hslMatch[2], 10),
      l: parseInt(hslMatch[3], 10),
    });
  }
  
  // Named colors
  return namedColorToRgb(color);
}

/**
 * Convert hex color to RGB.
 */
export function hexToRgb(hex: string): RGB | null {
  // Remove #
  hex = hex.replace('#', '');
  
  // Expand shorthand (#abc -> #aabbcc)
  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  
  if (hex.length !== 6) {
    return null;
  }
  
  const num = parseInt(hex, 16);
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255,
  };
}

/**
 * Convert RGB to hex color.
 */
export function rgbToHex(rgb: RGB): string {
  const toHex = (n: number) => {
    const hex = Math.round(Math.max(0, Math.min(255, n))).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(rgb.r)}${toHex(rgb.g)}${toHex(rgb.b)}`;
}

/**
 * Convert HSL to RGB.
 */
export function hslToRgb(hsl: HSL): RGB {
  const h = hsl.h / 360;
  const s = hsl.s / 100;
  const l = hsl.l / 100;
  
  let r, g, b;
  
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }
  
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  };
}

/**
 * Convert common named colors to RGB.
 */
function namedColorToRgb(name: string): RGB | null {
  const colors: Record<string, RGB> = {
    white: { r: 255, g: 255, b: 255 },
    black: { r: 0, g: 0, b: 0 },
    red: { r: 255, g: 0, b: 0 },
    green: { r: 0, g: 128, b: 0 },
    blue: { r: 0, g: 0, b: 255 },
    yellow: { r: 255, g: 255, b: 0 },
    orange: { r: 255, g: 165, b: 0 },
    purple: { r: 128, g: 0, b: 128 },
    gray: { r: 128, g: 128, b: 128 },
    grey: { r: 128, g: 128, b: 128 },
  };
  
  return colors[name.toLowerCase()] || null;
}

// =============================================================================
// Luminance & Contrast
// =============================================================================

/**
 * Calculate relative luminance of a color.
 * Based on WCAG 2.1 formula.
 */
export function getLuminance(rgb: RGB): number {
  const [rs, gs, bs] = [rgb.r, rgb.g, rgb.b].map((c) => {
    const sRGB = c / 255;
    return sRGB <= 0.03928
      ? sRGB / 12.92
      : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  });
  
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

/**
 * Calculate contrast ratio between two colors.
 * Returns a value between 1 (no contrast) and 21 (max contrast).
 */
export function getContrastRatio(color1: string | RGB, color2: string | RGB): number {
  const rgb1 = typeof color1 === 'string' ? parseColor(color1) : color1;
  const rgb2 = typeof color2 === 'string' ? parseColor(color2) : color2;
  
  if (!rgb1 || !rgb2) {
    return 1;
  }
  
  const l1 = getLuminance(rgb1);
  const l2 = getLuminance(rgb2);
  
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if contrast meets WCAG requirements.
 */
export function checkContrast(
  foreground: string,
  background: string,
  isLargeText: boolean = false
): ContrastResult {
  const ratio = getContrastRatio(foreground, background);
  
  const passesAALarge = ratio >= WCAG_AA_LARGE;
  const passesAA = ratio >= WCAG_AA_NORMAL;
  const passesAAALarge = ratio >= WCAG_AAA_LARGE;
  const passesAAA = ratio >= WCAG_AAA_NORMAL;
  
  let level: ContrastResult['level'];
  if (isLargeText) {
    if (passesAAALarge) level = 'AAA';
    else if (passesAALarge) level = 'AA';
    else level = 'Fail';
  } else {
    if (passesAAA) level = 'AAA';
    else if (passesAA) level = 'AA';
    else if (passesAALarge) level = 'AA Large';
    else level = 'Fail';
  }
  
  return {
    ratio: Math.round(ratio * 100) / 100,
    passesAA,
    passesAALarge,
    passesAAA,
    passesAAALarge,
    level,
  };
}

// =============================================================================
// Color Suggestions
// =============================================================================

/**
 * Suggest an accessible foreground color for a given background.
 */
export function suggestAccessibleColor(
  background: string,
  preferDark: boolean = true,
  targetRatio: number = WCAG_AA_NORMAL
): string {
  const bgRgb = parseColor(background);
  if (!bgRgb) return preferDark ? '#000000' : '#FFFFFF';
  
  const bgLuminance = getLuminance(bgRgb);
  
  // Try black or white first
  const blackContrast = getContrastRatio(bgRgb, { r: 0, g: 0, b: 0 });
  const whiteContrast = getContrastRatio(bgRgb, { r: 255, g: 255, b: 255 });
  
  if (blackContrast >= targetRatio && (preferDark || whiteContrast < targetRatio)) {
    return '#000000';
  }
  if (whiteContrast >= targetRatio) {
    return '#FFFFFF';
  }
  
  // Find a color that meets the target ratio
  // Adjust brightness of the background color
  const targetLuminance = bgLuminance > 0.5
    ? (bgLuminance + 0.05) / targetRatio - 0.05  // Need darker
    : (bgLuminance + 0.05) * targetRatio - 0.05; // Need lighter
  
  // Create a grayscale color with target luminance
  const gray = Math.round(
    targetLuminance <= 0.03928
      ? targetLuminance * 12.92 * 255
      : (Math.pow(targetLuminance, 1/2.4) * 1.055 - 0.055) * 255
  );
  
  const clampedGray = Math.max(0, Math.min(255, gray));
  return rgbToHex({ r: clampedGray, g: clampedGray, b: clampedGray });
}

/**
 * Adjust a color to meet contrast requirements.
 */
export function adjustColorForContrast(
  foreground: string,
  background: string,
  targetRatio: number = WCAG_AA_NORMAL
): string {
  const fgRgb = parseColor(foreground);
  const bgRgb = parseColor(background);
  
  if (!fgRgb || !bgRgb) return foreground;
  
  let currentRatio = getContrastRatio(fgRgb, bgRgb);
  
  if (currentRatio >= targetRatio) {
    return foreground; // Already meets requirement
  }
  
  const bgLuminance = getLuminance(bgRgb);
  const shouldDarken = bgLuminance > 0.5;
  
  // Incrementally adjust the color
  let adjusted = { ...fgRgb };
  const step = shouldDarken ? -5 : 5;
  
  for (let i = 0; i < 51; i++) { // Max 51 iterations
    adjusted = {
      r: Math.max(0, Math.min(255, adjusted.r + step)),
      g: Math.max(0, Math.min(255, adjusted.g + step)),
      b: Math.max(0, Math.min(255, adjusted.b + step)),
    };
    
    currentRatio = getContrastRatio(adjusted, bgRgb);
    if (currentRatio >= targetRatio) {
      return rgbToHex(adjusted);
    }
  }
  
  // Fallback to black or white
  return shouldDarken ? '#000000' : '#FFFFFF';
}

// =============================================================================
// Focus Management
// =============================================================================

/**
 * Trap focus within an element (for modals, dialogs).
 */
export function trapFocus(container: HTMLElement): () => void {
  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(', ');
  
  const focusableElements = container.querySelectorAll<HTMLElement>(focusableSelector);
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return;
    
    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement?.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement?.focus();
      }
    }
  };
  
  container.addEventListener('keydown', handleKeyDown);
  firstElement?.focus();
  
  return () => {
    container.removeEventListener('keydown', handleKeyDown);
  };
}

/**
 * Restore focus to a previously focused element.
 */
export function restoreFocus(element: HTMLElement | null): void {
  if (element && typeof element.focus === 'function') {
    element.focus();
  }
}

// =============================================================================
// Screen Reader Announcements
// =============================================================================

let liveRegion: HTMLElement | null = null;

/**
 * Announce a message to screen readers.
 */
export function announce(
  message: string,
  priority: 'polite' | 'assertive' = 'polite'
): void {
  if (typeof document === 'undefined') return;
  
  // Create live region if needed
  if (!liveRegion) {
    liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', priority);
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.style.cssText = `
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    `;
    document.body.appendChild(liveRegion);
  }
  
  // Update aria-live if needed
  liveRegion.setAttribute('aria-live', priority);
  
  // Clear and set message
  liveRegion.textContent = '';
  
  // Use timeout to ensure the change is detected
  setTimeout(() => {
    if (liveRegion) {
      liveRegion.textContent = message;
    }
  }, 100);
}

// =============================================================================
// Accessibility Checker
// =============================================================================

interface A11yIssue {
  type: 'error' | 'warning';
  element: HTMLElement;
  message: string;
  wcag: string;
}

/**
 * Check an element for common accessibility issues.
 */
export function checkAccessibility(container: HTMLElement): A11yIssue[] {
  const issues: A11yIssue[] = [];
  
  // Check images for alt text
  const images = container.querySelectorAll('img');
  images.forEach((img) => {
    if (!img.hasAttribute('alt')) {
      issues.push({
        type: 'error',
        element: img,
        message: 'Image missing alt attribute',
        wcag: '1.1.1',
      });
    }
  });
  
  // Check buttons and links for accessible names
  const interactives = container.querySelectorAll('button, a');
  interactives.forEach((el) => {
    const hasText = el.textContent?.trim();
    const hasAriaLabel = el.hasAttribute('aria-label');
    const hasAriaLabelledby = el.hasAttribute('aria-labelledby');
    
    if (!hasText && !hasAriaLabel && !hasAriaLabelledby) {
      issues.push({
        type: 'error',
        element: el as HTMLElement,
        message: 'Interactive element missing accessible name',
        wcag: '4.1.2',
      });
    }
  });
  
  // Check form inputs for labels
  const inputs = container.querySelectorAll('input, select, textarea');
  inputs.forEach((input) => {
    const id = input.getAttribute('id');
    const hasLabel = id && container.querySelector(`label[for="${id}"]`);
    const hasAriaLabel = input.hasAttribute('aria-label');
    const hasAriaLabelledby = input.hasAttribute('aria-labelledby');
    
    if (!hasLabel && !hasAriaLabel && !hasAriaLabelledby) {
      issues.push({
        type: 'error',
        element: input as HTMLElement,
        message: 'Form input missing label',
        wcag: '1.3.1',
      });
    }
  });
  
  // Check heading order
  const headings = container.querySelectorAll('h1, h2, h3, h4, h5, h6');
  let lastLevel = 0;
  headings.forEach((h) => {
    const level = parseInt(h.tagName[1], 10);
    if (level > lastLevel + 1) {
      issues.push({
        type: 'warning',
        element: h as HTMLElement,
        message: `Skipped heading level (h${lastLevel} to h${level})`,
        wcag: '1.3.1',
      });
    }
    lastLevel = level;
  });
  
  return issues;
}

// =============================================================================
// Exports
// =============================================================================

export default {
  // Color utilities
  parseColor,
  hexToRgb,
  rgbToHex,
  hslToRgb,
  getLuminance,
  getContrastRatio,
  checkContrast,
  suggestAccessibleColor,
  adjustColorForContrast,
  // Focus management
  trapFocus,
  restoreFocus,
  // Screen reader
  announce,
  // Checking
  checkAccessibility,
  // Constants
  WCAG_AA_NORMAL,
  WCAG_AA_LARGE,
  WCAG_AAA_NORMAL,
  WCAG_AAA_LARGE,
};

