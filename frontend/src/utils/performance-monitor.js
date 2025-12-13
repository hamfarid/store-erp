/**
 * Frontend Performance Monitoring
 * ================================
 * 
 * Monitor and track frontend performance metrics.
 * Part of T26: Frontend Performance Enhancement
 * 
 * Features:
 * - Web Vitals tracking (LCP, FID, CLS, FCP, TTFB)
 * - Component render tracking
 * - API call performance
 * - Bundle size monitoring
 * - Memory usage tracking
 */

// Web Vitals metrics
const webVitals = {
  LCP: null,  // Largest Contentful Paint
  FID: null,  // First Input Delay
  CLS: null,  // Cumulative Layout Shift
  FCP: null,  // First Contentful Paint
  TTFB: null  // Time to First Byte
};

// Performance metrics storage
const performanceMetrics = {
  componentRenders: {},
  apiCalls: {},
  routeChanges: [],
  memoryUsage: []
};

/**
 * Track Web Vitals
 */
export const trackWebVitals = () => {
  if (typeof window === 'undefined' || !window.performance) {
    return;
  }

  // Track FCP (First Contentful Paint)
  const paintEntries = performance.getEntriesByType('paint');
  const fcpEntry = paintEntries.find(entry => entry.name === 'first-contentful-paint');
  if (fcpEntry) {
    webVitals.FCP = fcpEntry.startTime;
    console.log(`[Performance] FCP: ${fcpEntry.startTime.toFixed(2)}ms`);
  }

  // Track TTFB (Time to First Byte)
  const navigationEntries = performance.getEntriesByType('navigation');
  if (navigationEntries.length > 0) {
    const navEntry = navigationEntries[0];
    webVitals.TTFB = navEntry.responseStart - navEntry.requestStart;
    console.log(`[Performance] TTFB: ${webVitals.TTFB.toFixed(2)}ms`);
  }

  // Track LCP (Largest Contentful Paint)
  if ('PerformanceObserver' in window) {
    try {
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        webVitals.LCP = lastEntry.renderTime || lastEntry.loadTime;
        console.log(`[Performance] LCP: ${webVitals.LCP.toFixed(2)}ms`);
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
    } catch (e) {
      console.warn('[Performance] LCP tracking not supported');
    }

    // Track FID (First Input Delay)
    try {
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          webVitals.FID = entry.processingStart - entry.startTime;
          console.log(`[Performance] FID: ${webVitals.FID.toFixed(2)}ms`);
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
    } catch (e) {
      console.warn('[Performance] FID tracking not supported');
    }

    // Track CLS (Cumulative Layout Shift)
    try {
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            webVitals.CLS = clsValue;
            console.log(`[Performance] CLS: ${clsValue.toFixed(4)}`);
          }
        }
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });
    } catch (e) {
      console.warn('[Performance] CLS tracking not supported');
    }
  }
};

/**
 * Track component render performance
 */
export const trackComponentRender = (componentName, renderTime) => {
  if (!performanceMetrics.componentRenders[componentName]) {
    performanceMetrics.componentRenders[componentName] = {
      count: 0,
      totalTime: 0,
      avgTime: 0,
      maxTime: 0,
      minTime: Infinity
    };
  }

  const metrics = performanceMetrics.componentRenders[componentName];
  metrics.count++;
  metrics.totalTime += renderTime;
  metrics.avgTime = metrics.totalTime / metrics.count;
  metrics.maxTime = Math.max(metrics.maxTime, renderTime);
  metrics.minTime = Math.min(metrics.minTime, renderTime);

  // Log slow renders (> 16ms = 60fps threshold)
  if (renderTime > 16) {
    console.warn(`[Performance] Slow render: ${componentName} took ${renderTime.toFixed(2)}ms`);
  }
};

/**
 * Track API call performance
 */
export const trackAPICall = (endpoint, duration, status) => {
  if (!performanceMetrics.apiCalls[endpoint]) {
    performanceMetrics.apiCalls[endpoint] = {
      count: 0,
      totalTime: 0,
      avgTime: 0,
      maxTime: 0,
      minTime: Infinity,
      errors: 0
    };
  }

  const metrics = performanceMetrics.apiCalls[endpoint];
  metrics.count++;
  metrics.totalTime += duration;
  metrics.avgTime = metrics.totalTime / metrics.count;
  metrics.maxTime = Math.max(metrics.maxTime, duration);
  metrics.minTime = Math.min(metrics.minTime, duration);

  if (status >= 400) {
    metrics.errors++;
  }

  // Log slow API calls (> 1000ms)
  if (duration > 1000) {
    console.warn(`[Performance] Slow API call: ${endpoint} took ${duration.toFixed(2)}ms`);
  }
};

/**
 * Track route change performance
 */
export const trackRouteChange = (from, to, duration) => {
  performanceMetrics.routeChanges.push({
    from,
    to,
    duration,
    timestamp: Date.now()
  });

  // Keep only last 50 route changes
  if (performanceMetrics.routeChanges.length > 50) {
    performanceMetrics.routeChanges.shift();
  }

  console.log(`[Performance] Route change: ${from} → ${to} (${duration.toFixed(2)}ms)`);
};

/**
 * Track memory usage
 */
export const trackMemoryUsage = () => {
  if (performance.memory) {
    const usage = {
      usedJSHeapSize: performance.memory.usedJSHeapSize,
      totalJSHeapSize: performance.memory.totalJSHeapSize,
      jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
      timestamp: Date.now()
    };

    performanceMetrics.memoryUsage.push(usage);

    // Keep only last 100 measurements
    if (performanceMetrics.memoryUsage.length > 100) {
      performanceMetrics.memoryUsage.shift();
    }

    // Log if memory usage is high (> 80%)
    const usagePercent = (usage.usedJSHeapSize / usage.jsHeapSizeLimit) * 100;
    if (usagePercent > 80) {
      console.warn(`[Performance] High memory usage: ${usagePercent.toFixed(2)}%`);
    }
  }
};

/**
 * Get performance report
 */
export const getPerformanceReport = () => {
  return {
    webVitals: { ...webVitals },
    componentRenders: { ...performanceMetrics.componentRenders },
    apiCalls: { ...performanceMetrics.apiCalls },
    routeChanges: [...performanceMetrics.routeChanges],
    memoryUsage: [...performanceMetrics.memoryUsage]
  };
};

/**
 * Print performance report to console
 */
export const printPerformanceReport = () => {
  console.group('📊 Performance Report');

  // Web Vitals
  console.group('🌐 Web Vitals');
  console.table(webVitals);
  console.groupEnd();

  // Component Renders
  console.group('⚛️ Component Renders');
  const topComponents = Object.entries(performanceMetrics.componentRenders)
    .sort((a, b) => b[1].totalTime - a[1].totalTime)
    .slice(0, 10);
  console.table(Object.fromEntries(topComponents));
  console.groupEnd();

  // API Calls
  console.group('🌍 API Calls');
  const topAPIs = Object.entries(performanceMetrics.apiCalls)
    .sort((a, b) => b[1].totalTime - a[1].totalTime)
    .slice(0, 10);
  console.table(Object.fromEntries(topAPIs));
  console.groupEnd();

  // Memory Usage
  if (performanceMetrics.memoryUsage.length > 0) {
    console.group('💾 Memory Usage');
    const latestMemory = performanceMetrics.memoryUsage[performanceMetrics.memoryUsage.length - 1];
    console.log(`Used: ${(latestMemory.usedJSHeapSize / 1024 / 1024).toFixed(2)} MB`);
    console.log(`Total: ${(latestMemory.totalJSHeapSize / 1024 / 1024).toFixed(2)} MB`);
    console.log(`Limit: ${(latestMemory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)} MB`);
    console.groupEnd();
  }

  console.groupEnd();
};

/**
 * Initialize performance monitoring
 */
export const initPerformanceMonitoring = () => {
  // Track Web Vitals
  trackWebVitals();

  // Track memory usage every 30 seconds
  setInterval(trackMemoryUsage, 30000);

  // Print report every 5 minutes in development
  if (import.meta.env.DEV) {
    setInterval(printPerformanceReport, 300000);
  }

  console.log('[Performance] Monitoring initialized');
};

/**
 * React Hook for component performance tracking
 */
export const usePerformanceTracking = (componentName) => {
  const startTime = performance.now();

  return () => {
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    trackComponentRender(componentName, renderTime);
  };
};

// Auto-initialize in browser
if (typeof window !== 'undefined') {
  window.addEventListener('load', initPerformanceMonitoring);
}

export default {
  trackWebVitals,
  trackComponentRender,
  trackAPICall,
  trackRouteChange,
  trackMemoryUsage,
  getPerformanceReport,
  printPerformanceReport,
  initPerformanceMonitoring,
  usePerformanceTracking
};

