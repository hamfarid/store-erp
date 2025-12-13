/**
 * P1.38: Content Security Policy Meta Tags Component
 * 
 * Provides CSP and other security headers via meta tags for the frontend.
 * Use this component in your app's head/layout.
 */

import { useEffect, useMemo } from 'react';

// =============================================================================
// Types
// =============================================================================

interface CSPDirective {
  name: string;
  values: string[];
}

interface SecurityHeadersConfig {
  /** Enable strict CSP mode */
  strictMode?: boolean;
  /** Additional script sources */
  scriptSrc?: string[];
  /** Additional style sources */
  styleSrc?: string[];
  /** Additional image sources */
  imgSrc?: string[];
  /** Additional font sources */
  fontSrc?: string[];
  /** Additional connect sources (API, websockets) */
  connectSrc?: string[];
  /** Additional frame sources */
  frameSrc?: string[];
  /** CSP nonce for inline scripts */
  nonce?: string;
  /** Report URI for CSP violations */
  reportUri?: string;
  /** Enable report-only mode (doesn't block, just reports) */
  reportOnly?: boolean;
}

// =============================================================================
// Default CSP Configuration
// =============================================================================

const DEFAULT_CONFIG: SecurityHeadersConfig = {
  strictMode: true,
  scriptSrc: [],
  styleSrc: [],
  imgSrc: [],
  fontSrc: [],
  connectSrc: [],
  frameSrc: [],
  nonce: undefined,
  reportUri: undefined,
  reportOnly: false,
};

// =============================================================================
// CSP Builder
// =============================================================================

function buildCSP(config: SecurityHeadersConfig): string {
  const directives: CSPDirective[] = [];
  
  // default-src
  directives.push({
    name: 'default-src',
    values: ["'self'"],
  });
  
  // script-src
  const scriptSrcValues = ["'self'"];
  if (config.nonce) {
    scriptSrcValues.push(`'nonce-${config.nonce}'`);
  }
  if (!config.strictMode) {
    scriptSrcValues.push("'unsafe-inline'");
  }
  scriptSrcValues.push(...(config.scriptSrc || []));
  directives.push({
    name: 'script-src',
    values: scriptSrcValues,
  });
  
  // style-src
  const styleSrcValues = ["'self'"];
  if (config.nonce) {
    styleSrcValues.push(`'nonce-${config.nonce}'`);
  }
  // Allow inline styles for React/CSS-in-JS
  styleSrcValues.push("'unsafe-inline'");
  styleSrcValues.push(...(config.styleSrc || []));
  directives.push({
    name: 'style-src',
    values: styleSrcValues,
  });
  
  // img-src
  directives.push({
    name: 'img-src',
    values: ["'self'", 'data:', 'blob:', ...(config.imgSrc || [])],
  });
  
  // font-src
  directives.push({
    name: 'font-src',
    values: ["'self'", 'data:', ...(config.fontSrc || [])],
  });
  
  // connect-src (API, WebSocket, etc.)
  const connectSrcValues = ["'self'"];
  // Add API URL
  if (typeof window !== 'undefined') {
    connectSrcValues.push(window.location.origin);
  }
  connectSrcValues.push(...(config.connectSrc || []));
  directives.push({
    name: 'connect-src',
    values: connectSrcValues,
  });
  
  // frame-src
  directives.push({
    name: 'frame-src',
    values: ["'none'", ...(config.frameSrc || [])],
  });
  
  // frame-ancestors
  directives.push({
    name: 'frame-ancestors',
    values: ["'none'"],
  });
  
  // base-uri
  directives.push({
    name: 'base-uri',
    values: ["'self'"],
  });
  
  // form-action
  directives.push({
    name: 'form-action',
    values: ["'self'"],
  });
  
  // object-src
  directives.push({
    name: 'object-src',
    values: ["'none'"],
  });
  
  // upgrade-insecure-requests
  if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
    directives.push({
      name: 'upgrade-insecure-requests',
      values: [],
    });
  }
  
  // report-uri
  if (config.reportUri) {
    directives.push({
      name: 'report-uri',
      values: [config.reportUri],
    });
  }
  
  // Build CSP string
  return directives
    .map((d) => {
      if (d.values.length === 0) {
        return d.name;
      }
      return `${d.name} ${d.values.join(' ')}`;
    })
    .join('; ');
}

// =============================================================================
// Security Headers Component
// =============================================================================

interface SecurityHeadersProps extends SecurityHeadersConfig {}

export function SecurityHeaders(props: SecurityHeadersProps) {
  const config = { ...DEFAULT_CONFIG, ...props };
  
  const csp = useMemo(() => buildCSP(config), [config]);
  
  useEffect(() => {
    // Update or create CSP meta tag
    const metaName = config.reportOnly
      ? 'Content-Security-Policy-Report-Only'
      : 'Content-Security-Policy';
    
    let meta = document.querySelector(`meta[http-equiv="${metaName}"]`);
    
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute('http-equiv', metaName);
      document.head.appendChild(meta);
    }
    
    meta.setAttribute('content', csp);
    
    // Add other security meta tags
    addSecurityMeta('X-Content-Type-Options', 'nosniff');
    addSecurityMeta('X-Frame-Options', 'DENY');
    addSecurityMeta('X-XSS-Protection', '1; mode=block');
    addSecurityMeta('Referrer-Policy', 'strict-origin-when-cross-origin');
    
    // Permissions Policy
    const permissionsPolicy = [
      'camera=()',
      'microphone=()',
      'geolocation=()',
      'payment=()',
      'usb=()',
      'magnetometer=()',
      'gyroscope=()',
      'accelerometer=()',
    ].join(', ');
    addSecurityMeta('Permissions-Policy', permissionsPolicy);
    
    return () => {
      // Cleanup is optional since these should persist
    };
  }, [csp, config.reportOnly]);
  
  // Return null as this component only manages meta tags
  return null;
}

// =============================================================================
// Helper Functions
// =============================================================================

function addSecurityMeta(name: string, content: string): void {
  // Check for http-equiv first
  let meta = document.querySelector(`meta[http-equiv="${name}"]`);
  
  if (!meta) {
    // Check for name
    meta = document.querySelector(`meta[name="${name}"]`);
  }
  
  if (!meta) {
    meta = document.createElement('meta');
    // Some headers work better as http-equiv
    if (['X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection'].includes(name)) {
      meta.setAttribute('http-equiv', name);
    } else {
      meta.setAttribute('name', name);
    }
    document.head.appendChild(meta);
  }
  
  meta.setAttribute('content', content);
}

// =============================================================================
// Nonce Provider
// =============================================================================

/**
 * Generate a cryptographic nonce for inline scripts/styles.
 */
export function generateNonce(): string {
  const array = new Uint8Array(16);
  crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array));
}

/**
 * Get the current nonce from the page (if set by server).
 */
export function getServerNonce(): string | null {
  if (typeof document === 'undefined') return null;
  
  const script = document.querySelector('script[nonce]');
  return script?.getAttribute('nonce') || null;
}

// =============================================================================
// CSP Violation Reporter
// =============================================================================

interface CSPViolation {
  documentUri: string;
  violatedDirective: string;
  blockedUri: string;
  sourceFile: string;
  lineNumber: number;
  columnNumber: number;
}

/**
 * Set up CSP violation reporting to the console and optional endpoint.
 */
export function setupCSPReporting(reportEndpoint?: string): void {
  if (typeof document === 'undefined') return;
  
  document.addEventListener('securitypolicyviolation', (e) => {
    const violation: CSPViolation = {
      documentUri: e.documentURI,
      violatedDirective: e.violatedDirective,
      blockedUri: e.blockedURI,
      sourceFile: e.sourceFile,
      lineNumber: e.lineNumber,
      columnNumber: e.columnNumber,
    };
    
    console.warn('P1.38: CSP Violation detected:', violation);
    
    // Report to endpoint if configured
    if (reportEndpoint) {
      fetch(reportEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'csp-report': violation }),
      }).catch(() => {
        // Silently fail - don't want reporting errors to break the app
      });
    }
  });
}

// =============================================================================
// Presets
// =============================================================================

/**
 * Strict CSP preset for maximum security.
 */
export const STRICT_CSP: SecurityHeadersConfig = {
  strictMode: true,
  scriptSrc: [],
  styleSrc: [],
  imgSrc: [],
  fontSrc: [],
  connectSrc: [],
  frameSrc: [],
};

/**
 * Development CSP preset (more permissive).
 */
export const DEV_CSP: SecurityHeadersConfig = {
  strictMode: false,
  scriptSrc: ["'unsafe-eval'"], // For hot reload
  styleSrc: [],
  imgSrc: ['*'],
  fontSrc: ['*'],
  connectSrc: ['*', 'ws:', 'wss:'], // For dev server
  frameSrc: [],
};

/**
 * Production CSP preset with common CDNs.
 */
export const PRODUCTION_CSP: SecurityHeadersConfig = {
  strictMode: true,
  scriptSrc: [
    'https://cdn.jsdelivr.net',
    'https://unpkg.com',
  ],
  styleSrc: [
    'https://fonts.googleapis.com',
    'https://cdn.jsdelivr.net',
  ],
  imgSrc: [
    'https:',
    'data:',
  ],
  fontSrc: [
    'https://fonts.gstatic.com',
    'https://cdn.jsdelivr.net',
  ],
  connectSrc: [],
  frameSrc: [],
};

// =============================================================================
// Exports
// =============================================================================

export default SecurityHeaders;

