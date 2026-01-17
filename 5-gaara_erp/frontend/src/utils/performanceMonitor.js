/**
 * FILE: frontend/src/utils/performanceMonitor.js
 * PURPOSE: Monitor Core Web Vitals (LCP, FID, CLS) and API performance
 * OWNER: Frontend Team
 * RELATED: logger.js, traceId.js
 * LAST-AUDITED: 2025-10-23
 */

import { logEvent } from './logger';
import { getCurrentTraceId } from './traceId';

// Core Web Vitals thresholds (milliseconds)
const VITALS_THRESHOLDS = {
  LCP: 2500,  // Largest Contentful Paint
  FID: 100,   // First Input Delay
  CLS: 0.1    // Cumulative Layout Shift
};

class PerformanceMonitor {
  constructor() {
    this.metrics = {
      lcp: null,
      fid: null,
      cls: null,
      apiRequests: [],
      pageLoadTime: null
    };
    this.initialized = false;
  }

  /**
   * Initialize performance monitoring
   * Call this in App.jsx or main.jsx
   */
  initialize() {
    if (this.initialized) return;
    this.initialized = true;

    // Monitor page load time
    this.monitorPageLoad();

    // Monitor Core Web Vitals
    this.monitorLCP();
    this.monitorFID();
    this.monitorCLS();

    // Report metrics on page unload
    window.addEventListener('beforeunload', () => {
      this.reportMetrics();
    });

    if (import.meta.env?.DEV) {
      console.debug('[PerformanceMonitor] Initialized');
    }
  }

  /**
   * Monitor Largest Contentful Paint (LCP)
   */
  monitorLCP() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.metrics.lcp = lastEntry.renderTime || lastEntry.loadTime;

        const isGood = this.metrics.lcp <= VITALS_THRESHOLDS.LCP;
        if (!isGood) {
          logEvent('web_vital_lcp_poor', {
            value: this.metrics.lcp,
            threshold: VITALS_THRESHOLDS.LCP,
            outcome: 'warning'
          });
        }
      });

      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    } catch (error) {
      console.warn('[PerformanceMonitor] LCP monitoring not supported:', error);
    }
  }

  /**
   * Monitor First Input Delay (FID)
   */
  monitorFID() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          this.metrics.fid = entry.processingDuration;

          const isGood = this.metrics.fid <= VITALS_THRESHOLDS.FID;
          if (!isGood) {
            logEvent('web_vital_fid_poor', {
              value: this.metrics.fid,
              threshold: VITALS_THRESHOLDS.FID,
              outcome: 'warning'
            });
          }
        });
      });

      observer.observe({ entryTypes: ['first-input'] });
    } catch (error) {
      console.warn('[PerformanceMonitor] FID monitoring not supported:', error);
    }
  }

  /**
   * Monitor Cumulative Layout Shift (CLS)
   */
  monitorCLS() {
    try {
      let clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            this.metrics.cls = clsValue;

            const isGood = this.metrics.cls <= VITALS_THRESHOLDS.CLS;
            if (!isGood) {
              logEvent('web_vital_cls_poor', {
                value: this.metrics.cls,
                threshold: VITALS_THRESHOLDS.CLS,
                outcome: 'warning'
              });
            }
          }
        });
      });

      observer.observe({ entryTypes: ['layout-shift'] });
    } catch (error) {
      console.warn('[PerformanceMonitor] CLS monitoring not supported:', error);
    }
  }

  /**
   * Monitor page load time
   */
  monitorPageLoad() {
    window.addEventListener('load', () => {
      const perfData = window.performance.timing;
      const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
      this.metrics.pageLoadTime = pageLoadTime;

      logEvent('page_load_complete', {
        page_load_time_ms: pageLoadTime,
        outcome: 'success'
      });
    });
  }

  /**
   * Track API request performance
   * Call this from API interceptors
   */
  trackApiRequest(method, url, timingMs, statusCode) {
    const request = {
      method,
      url,
      timingMs,
      statusCode,
      timestamp: new Date().toISOString(),
      traceId: getCurrentTraceId()
    };

    this.metrics.apiRequests.push(request);

    // Keep only last 100 requests
    if (this.metrics.apiRequests.length > 100) {
      this.metrics.apiRequests = this.metrics.apiRequests.slice(-100);
    }

    // Log slow requests (> 3 seconds)
    if (timingMs > 3000) {
      logEvent('slow_api_request', {
        method,
        url,
        timing_ms: timingMs,
        status_code: statusCode,
        outcome: 'warning'
      });
    }
  }

  /**
   * Get current metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      apiRequestsCount: this.metrics.apiRequests.length,
      averageApiTime: this.getAverageApiTime(),
      slowApiRequestsCount: this.metrics.apiRequests.filter(r => r.timingMs > 3000).length
    };
  }

  /**
   * Calculate average API request time
   */
  getAverageApiTime() {
    if (this.metrics.apiRequests.length === 0) return 0;
    const total = this.metrics.apiRequests.reduce((sum, r) => sum + r.timingMs, 0);
    return Math.round(total / this.metrics.apiRequests.length);
  }

  /**
   * Report metrics to server
   */
  reportMetrics() {
    const metrics = this.getMetrics();

    try {
      navigator.sendBeacon('/api/metrics/report', JSON.stringify({
        traceId: getCurrentTraceId(),
        timestamp: new Date().toISOString(),
        metrics,
        url: window.location.href
      }));
    } catch (error) {
      console.warn('[PerformanceMonitor] Failed to report metrics:', error);
    }
  }

  /**
   * Get performance summary for debugging
   */
  getSummary() {
    const metrics = this.getMetrics();
    return {
      vitals: {
        lcp: `${metrics.lcp}ms ${metrics.lcp <= VITALS_THRESHOLDS.LCP ? '✓' : '✗'}`,
        fid: `${metrics.fid}ms ${metrics.fid <= VITALS_THRESHOLDS.FID ? '✓' : '✗'}`,
        cls: `${metrics.cls?.toFixed(3)} ${metrics.cls <= VITALS_THRESHOLDS.CLS ? '✓' : '✗'}`
      },
      pageLoadTime: `${metrics.pageLoadTime}ms`,
      apiRequests: {
        total: metrics.apiRequestsCount,
        averageTime: `${metrics.averageApiTime}ms`,
        slowRequests: metrics.slowApiRequestsCount
      }
    };
  }
}

// Global instance
const performanceMonitor = new PerformanceMonitor();

export default performanceMonitor;

