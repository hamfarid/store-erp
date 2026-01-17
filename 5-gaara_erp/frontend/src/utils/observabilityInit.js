/**
 * FILE: frontend/src/utils/observabilityInit.js
 * PURPOSE: Initialize all observability systems on app startup
 * OWNER: Frontend Team
 * RELATED: traceId.js, logger.js, performanceMonitor.js
 * LAST-AUDITED: 2025-10-23
 */

import { initializeTraceIdSystem } from './traceId';
import logger from './logger';
import performanceMonitor from './performanceMonitor';
import { logEvent } from './logger';

/**
 * Initialize all observability systems
 * Call this in App.jsx useEffect or main.jsx
 */
export function initializeObservability() {
  try {
    // 1. Initialize traceId system
    const sessionTraceId = initializeTraceIdSystem();
    console.debug('[Observability] TraceId system initialized:', sessionTraceId);

    // 2. Initialize performance monitoring
    performanceMonitor.initialize();
    console.debug('[Observability] Performance monitoring initialized');

    // 3. Enable logger
    logger.isEnabled = true;
    console.debug('[Observability] Logger enabled');

    // 4. Log app initialization
    logEvent('app_initialized', {
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      outcome: 'success'
    });

    // 5. Setup global error handlers
    setupGlobalErrorHandlers();

    // 6. Setup performance reporting
    setupPerformanceReporting();

    console.debug('[Observability] All systems initialized successfully');

    return {
      sessionTraceId,
      status: 'initialized'
    };
  } catch (error) {
    console.error('[Observability] Initialization failed:', error);
    return {
      status: 'failed',
      error: error.message
    };
  }
}

/**
 * Setup global error handlers
 */
function setupGlobalErrorHandlers() {
  // Handle uncaught errors
  window.addEventListener('error', (event) => {
    console.error('[Global Error Handler]', event.error);
  });

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('[Unhandled Rejection]', event.reason);
  });
}

/**
 * Setup periodic performance reporting
 */
function setupPerformanceReporting() {
  // Report performance metrics every 5 minutes
  setInterval(() => {
    try {
      const metrics = performanceMonitor.getMetrics();
      
      if (import.meta.env?.DEV) {
        console.debug('[Performance Report]', performanceMonitor.getSummary());
      }

      // Send to server if there are metrics to report
      if (metrics.apiRequestsCount > 0 || metrics.pageLoadTime) {
        navigator.sendBeacon('/api/metrics/report', JSON.stringify({
          timestamp: new Date().toISOString(),
          metrics,
          url: window.location.href
        }));
      }
    } catch (error) {
      console.warn('[Performance Reporting] Failed:', error);
    }
  }, 5 * 60 * 1000); // 5 minutes
}

/**
 * Get observability status
 */
export function getObservabilityStatus() {
  return {
    traceId: window.__TRACE_ID__?.getSessionTraceId?.(),
    loggerEnabled: logger.isEnabled,
    performanceMonitorInitialized: performanceMonitor.initialized,
    metrics: performanceMonitor.getMetrics()
  };
}

/**
 * Print observability summary to console
 */
export function printObservabilitySummary() {
  const status = getObservabilityStatus();
  console.group('[Observability Summary]');
  console.log('Status:', status);
  console.log('Performance:', performanceMonitor.getSummary());
  console.groupEnd();
}

export default {
  initializeObservability,
  getObservabilityStatus,
  printObservabilitySummary
};

