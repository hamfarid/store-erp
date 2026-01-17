/**
 * Lazy Loading Utilities for Frontend Components
 * Provides consistent lazy loading with error boundaries and loading states
 */

import React, { Suspense, lazy } from 'react';

/**
 * Default loading spinner component
 */
export const DefaultLoader = () => (
  <div className="flex items-center justify-center min-h-[200px]">
    <div className="relative">
      <div className="w-12 h-12 rounded-full border-4 border-primary-200 dark:border-primary-800" />
      <div className="absolute top-0 left-0 w-12 h-12 rounded-full border-4 border-t-primary-500 animate-spin" />
    </div>
    <span className="mr-4 text-gray-600 dark:text-gray-400">جاري التحميل...</span>
  </div>
);

/**
 * Full page loader for page-level lazy loading
 */
export const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
    <div className="text-center">
      <div className="relative inline-block">
        <div className="w-16 h-16 rounded-full border-4 border-primary-200 dark:border-primary-800" />
        <div className="absolute top-0 left-0 w-16 h-16 rounded-full border-4 border-t-primary-500 animate-spin" />
      </div>
      <p className="mt-4 text-gray-600 dark:text-gray-400 text-lg">جاري التحميل...</p>
    </div>
  </div>
);

/**
 * Skeleton loader for content areas
 */
export const SkeletonLoader = ({ lines = 3, className = '' }) => (
  <div className={`animate-pulse space-y-3 ${className}`}>
    {Array.from({ length: lines }).map((_, i) => (
      <div
        key={i}
        className="h-4 bg-gray-200 dark:bg-gray-700 rounded"
        style={{ width: `${Math.random() * 40 + 60}%` }}
      />
    ))}
  </div>
);

/**
 * Card skeleton loader
 */
export const CardSkeleton = () => (
  <div className="animate-pulse bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
    <div className="flex items-center gap-4 mb-4">
      <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-xl" />
      <div className="flex-1">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2" />
        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
      </div>
    </div>
    <div className="space-y-2">
      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full" />
      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-5/6" />
      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-4/6" />
    </div>
  </div>
);

/**
 * Table skeleton loader
 */
export const TableSkeleton = ({ rows = 5, cols = 4 }) => (
  <div className="animate-pulse">
    {/* Header */}
    <div className="flex gap-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-t-lg">
      {Array.from({ length: cols }).map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 dark:bg-gray-700 rounded flex-1" />
      ))}
    </div>
    {/* Rows */}
    {Array.from({ length: rows }).map((_, rowIndex) => (
      <div
        key={rowIndex}
        className="flex gap-4 p-4 border-b border-gray-200 dark:border-gray-700"
      >
        {Array.from({ length: cols }).map((_, colIndex) => (
          <div
            key={colIndex}
            className="h-4 bg-gray-200 dark:bg-gray-700 rounded flex-1"
            style={{ opacity: 1 - rowIndex * 0.1 }}
          />
        ))}
      </div>
    ))}
  </div>
);

/**
 * Create a lazy component with custom fallback
 * @param {Function} importFn - Dynamic import function
 * @param {React.Component} Fallback - Loading fallback component
 * @returns {React.Component} Lazy loaded component
 */
export const createLazyComponent = (importFn, _Fallback = DefaultLoader) => {
  const LazyComponent = lazy(importFn);

  return function LazyWrapper(props) {
    return (
      <Suspense fallback={<Fallback />}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };
};

/**
 * Create a lazy page component with full page loader
 * @param {Function} importFn - Dynamic import function
 * @returns {React.Component} Lazy loaded page component
 */
export const createLazyPage = (importFn) => {
  return createLazyComponent(importFn, PageLoader);
};

/**
 * Preload a lazy component (useful for prefetching)
 * @param {Function} importFn - Dynamic import function
 */
export const preloadComponent = (importFn) => {
  importFn();
};

/**
 * Lazy load with retry on failure
 * @param {Function} importFn - Dynamic import function
 * @param {number} retries - Number of retries
 * @param {number} interval - Interval between retries in ms
 * @returns {Promise} Import promise with retry logic
 */
export const lazyWithRetry = (importFn, retries = 3, interval = 1000) => {
  return new Promise((resolve, reject) => {
    const attempt = (retriesLeft) => {
      importFn()
        .then(resolve)
        .catch((error) => {
          if (retriesLeft > 0) {
            setTimeout(() => attempt(retriesLeft - 1), interval);
          } else {
            reject(error);
          }
        });
    };
    attempt(retries);
  });
};

/**
 * Create lazy component with retry logic
 * @param {Function} importFn - Dynamic import function
 * @param {Object} options - Options for retry
 * @returns {React.Component} Lazy loaded component with retry
 */
export const createLazyWithRetry = (importFn, options = {}) => {
  const { retries = 3, interval = 1000, Fallback: _Fallback = DefaultLoader } = options;

  const LazyComponent = lazy(() => lazyWithRetry(importFn, retries, interval));

  return function LazyRetryWrapper(props) {
    return (
      <Suspense fallback={<Fallback />}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };
};

/**
 * Intersection Observer based lazy loading hook
 * Loads component when it enters viewport
 */
export const useLazyLoad = (ref, options = {}) => {
  const [isVisible, setIsVisible] = React.useState(false);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      {
        threshold: 0.1,
        rootMargin: '50px',
        ...options,
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [ref, options]);

  return isVisible;
};

/**
 * Component that renders children only when visible in viewport
 */
export const LazyVisible = ({ children, fallback = <DefaultLoader />, className = '' }) => {
  const ref = React.useRef(null);
  const isVisible = useLazyLoad(ref);

  return (
    <div ref={ref} className={className}>
      {isVisible ? children : fallback}
    </div>
  );
};

// Export commonly used lazy components
export const lazyComponents = {
  // Pages
  Dashboard: createLazyPage(() => import('../pages/Dashboard')),
  ProductsPage: createLazyPage(() => import('../pages/ProductsPage')),
  CustomersPage: createLazyPage(() => import('../pages/CustomersPage')),
  SuppliersPage: createLazyPage(() => import('../pages/SuppliersPage')),
  InvoicesPage: createLazyPage(() => import('../pages/InvoicesPage')),
  WarehousesPage: createLazyPage(() => import('../pages/WarehousesPage')),
  ReportsPage: createLazyPage(() => import('../pages/ReportsPage')),
  SettingsPage: createLazyPage(() => import('../pages/SettingsPage')),
  Settings: createLazyPage(() => import('../pages/Settings')),
  SecurityDashboard: createLazyPage(() => import('../pages/SecurityDashboard')),
  AuditLogs: createLazyPage(() => import('../pages/AuditLogs')),
  BackupRestore: createLazyPage(() => import('../pages/BackupRestore')),
  SystemStatus: createLazyPage(() => import('../pages/SystemStatus')),
};

export default {
  DefaultLoader,
  PageLoader,
  SkeletonLoader,
  CardSkeleton,
  TableSkeleton,
  createLazyComponent,
  createLazyPage,
  preloadComponent,
  lazyWithRetry,
  createLazyWithRetry,
  useLazyLoad,
  LazyVisible,
  lazyComponents,
};

