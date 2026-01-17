/**
 * FILE: frontend/src/tests/setupTests.js
 * PURPOSE: Test setup for Vitest + Testing Library (jsdom, polyfills, matchers)
 * OWNER: Frontend Team
 * LAST-AUDITED: 2025-10-23
 */

import '@testing-library/jest-dom';
import { TextEncoder as NodeTextEncoder, TextDecoder as NodeTextDecoder } from 'util';
import { vi } from 'vitest';

// Jest compatibility shim
globalThis.jest = {
  fn: vi.fn,
  mock: vi.mock,
  spyOn: vi.spyOn,
  clearAllMocks: vi.clearAllMocks,
  resetAllMocks: vi.resetAllMocks,
  restoreAllMocks: vi.restoreAllMocks,
};

// matchMedia polyfill
if (typeof window !== 'undefined' && !window.matchMedia) {
  window.matchMedia = (query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {}, // deprecated
    removeListener: () => {}, // deprecated
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false
  });
}

// ResizeObserver polyfill
if (typeof window !== 'undefined' && !window.ResizeObserver) {
  class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  window.ResizeObserver = ResizeObserver;
}

// IntersectionObserver polyfill
if (typeof window !== 'undefined' && !window.IntersectionObserver) {
  class IntersectionObserver {
    constructor() {}
    observe() {}
    unobserve() {}
    disconnect() {}
    takeRecords() { return []; }
    root = null;
    rootMargin = '';
    thresholds = [];
  }
  window.IntersectionObserver = IntersectionObserver;
}

// scrollTo stub
if (typeof window !== 'undefined' && !window.scrollTo) {
  window.scrollTo = () => {};
}

// TextEncoder/TextDecoder for some libs
if (typeof globalThis !== 'undefined') {
  if (!globalThis.TextEncoder) {
    globalThis.TextEncoder = NodeTextEncoder;
  }
  if (!globalThis.TextDecoder) {
    globalThis.TextDecoder = NodeTextDecoder;
  }
}
