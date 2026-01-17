/**
 * FILE: frontend/src/hooks/useObservability.js
 * PURPOSE: React hooks for observability, performance tracking, and error handling
 * OWNER: Frontend Team
 * RELATED: logger.js, performanceMonitor.js, traceId.js
 * LAST-AUDITED: 2025-10-23
 */

import { useEffect, useRef, useCallback } from 'react';
import { logEvent, logError, logApiRequest } from '../utils/logger';
import performanceMonitor from '../utils/performanceMonitor';
import { getCurrentTraceId, createOperationTraceId, setCurrentTraceId, clearCurrentTraceId } from '../utils/traceId';

/**
 * Hook for tracking component lifecycle and performance
 * @param {string} componentName - Name of the component
 * @param {Object} props - Component props to track
 */
export function useObservability(componentName, props = {}) {
  const mountTimeRef = useRef(Date.now());
  const renderCountRef = useRef(0);

  useEffect(() => {
    renderCountRef.current += 1;
    const renderTime = Date.now() - mountTimeRef.current;

    logEvent('component_render', {
      component: componentName,
      render_count: renderCountRef.current,
      render_time_ms: renderTime,
      props: Object.keys(props)
    });

    return () => {
      logEvent('component_unmount', {
        component: componentName,
        total_renders: renderCountRef.current,
        mounted_duration_ms: Date.now() - mountTimeRef.current
      });
    };
  }, [componentName, props]);

  return {
    traceId: getCurrentTraceId(),
    renderCount: renderCountRef.current
  };
}

/**
 * Hook for tracking async operations with timing
 * @param {Function} asyncFn - Async function to track
 * @param {string} operationName - Name of the operation
 * @returns {Function} Wrapped async function with tracking
 */
export function useAsyncObservability(asyncFn, operationName) {
  const operationTraceIdRef = useRef(null);

  const wrappedFn = useCallback(
    async (...args) => {
      operationTraceIdRef.current = createOperationTraceId(operationName);
      setCurrentTraceId(operationTraceIdRef.current);

      const startTime = performance.now();

      try {
        logEvent(`${operationName}_started`, {
          operation: operationName,
          args_count: args.length
        });

        const result = await asyncFn(...args);

        const timingMs = Math.round(performance.now() - startTime);
        logEvent(`${operationName}_completed`, {
          operation: operationName,
          timing_ms: timingMs,
          outcome: 'success'
        });

        return result;
      } catch (error) {
        const timingMs = Math.round(performance.now() - startTime);
        logError(error, {
          operation: operationName,
          timing_ms: timingMs,
          args_count: args.length
        });
        throw error;
      } finally {
        clearCurrentTraceId();
      }
    },
    [asyncFn, operationName]
  );

  return wrappedFn;
}

/**
 * Hook for tracking API calls with performance metrics
 * @param {string} method - HTTP method
 * @param {string} url - API endpoint
 * @returns {Object} Object with trackRequest function
 */
export function useApiObservability(method, url) {
  const trackRequest = useCallback(
    (statusCode, additionalData = {}) => {
      // Timing is tracked by the API client, we just log it
      logApiRequest(method, url, 0, statusCode, additionalData);
      performanceMonitor.trackApiRequest(method, url, 0, statusCode);
    },
    [method, url]
  );

  return { trackRequest, traceId: getCurrentTraceId() };
}

/**
 * Hook for tracking user interactions
 * @param {string} actionName - Name of the action
 * @returns {Function} Function to call when action occurs
 */
export function useActionTracking(actionName) {
  return useCallback(
    (additionalData = {}) => {
      logEvent('user_action', {
        action: actionName,
        ...additionalData,
        outcome: 'success'
      });
    },
    [actionName]
  );
}

/**
 * Hook for tracking form submissions
 * @param {string} formName - Name of the form
 * @returns {Object} Object with trackSubmit and trackError functions
 */
export function useFormObservability(formName) {
  const trackSubmit = useCallback(
    (formData = {}) => {
      const startTime = performance.now();

      logEvent('form_submitted', {
        form: formName,
        fields_count: Object.keys(formData).length,
        outcome: 'pending'
      });

      return {
        success: (_result) => {
          const timingMs = Math.round(performance.now() - startTime);
          logEvent('form_submission_success', {
            form: formName,
            timing_ms: timingMs,
            outcome: 'success'
          });
        },
        error: (error) => {
          const timingMs = Math.round(performance.now() - startTime);
          logError(error, {
            form: formName,
            timing_ms: timingMs,
            context: 'form_submission'
          });
        }
      };
    },
    [formName]
  );

  return { trackSubmit, traceId: getCurrentTraceId() };
}

/**
 * Hook for tracking page navigation
 * @param {string} pageName - Name of the page
 * @returns {Object} Object with tracking data
 */
export function usePageObservability(pageName) {
  useEffect(() => {
    logEvent('page_view', {
      page: pageName,
      url: window.location.href,
      referrer: document.referrer,
      outcome: 'success'
    });

    return () => {
      logEvent('page_leave', {
        page: pageName,
        duration_ms: Date.now() - performance.now()
      });
    };
  }, [pageName]);

  return {
    traceId: getCurrentTraceId(),
    pageName
  };
}

/**
 * Hook for error tracking in functional components
 * @param {string} componentName - Name of the component
 * @returns {Function} Function to call when error occurs
 */
export function useErrorTracking(componentName) {
  return useCallback(
    (error, context = {}) => {
      logError(error, {
        component: componentName,
        ...context
      });
    },
    [componentName]
  );
}

export default {
  useObservability,
  useAsyncObservability,
  useApiObservability,
  useActionTracking,
  useFormObservability,
  usePageObservability,
  useErrorTracking
};

