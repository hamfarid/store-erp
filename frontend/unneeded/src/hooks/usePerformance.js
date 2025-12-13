/**
 * Performance Optimization Hooks
 * ===============================
 * 
 * Custom React hooks for performance optimization.
 * Part of T26: Frontend Performance Enhancement
 * 
 * Features:
 * - Debounce and throttle
 * - Lazy loading
 * - Intersection observer
 * - Virtual scrolling
 * - Memoization helpers
 */

import { useState, useEffect, useRef, useCallback, useMemo } from 'react';

/**
 * useDebounce - Debounce a value
 * 
 * @param {any} value - Value to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {any} Debounced value
 */
export const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

/**
 * useThrottle - Throttle a value
 * 
 * @param {any} value - Value to throttle
 * @param {number} limit - Limit in milliseconds
 * @returns {any} Throttled value
 */
export const useThrottle = (value, limit = 500) => {
  const [throttledValue, setThrottledValue] = useState(value);
  const lastRan = useRef(Date.now());

  useEffect(() => {
    const handler = setTimeout(() => {
      if (Date.now() - lastRan.current >= limit) {
        setThrottledValue(value);
        lastRan.current = Date.now();
      }
    }, limit - (Date.now() - lastRan.current));

    return () => {
      clearTimeout(handler);
    };
  }, [value, limit]);

  return throttledValue;
};

/**
 * useIntersectionObserver - Detect element visibility
 * 
 * @param {Object} options - Intersection observer options
 * @returns {Array} [ref, isIntersecting]
 */
export const useIntersectionObserver = (options = {}) => {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const targetRef = useRef(null);

  useEffect(() => {
    const target = targetRef.current;
    if (!target) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsIntersecting(entry.isIntersecting);
    }, {
      threshold: 0.1,
      ...options
    });

    observer.observe(target);

    return () => {
      observer.disconnect();
    };
  }, [options]);

  return [targetRef, isIntersecting];
};

/**
 * useLazyLoad - Lazy load component when visible
 * 
 * @param {Function} importFunc - Dynamic import function
 * @returns {Object} { Component, isLoading, error }
 */
export const useLazyLoad = (importFunc) => {
  const [Component, setComponent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [ref, isVisible] = useIntersectionObserver();

  useEffect(() => {
    if (isVisible && !Component) {
      importFunc()
        .then(module => {
          setComponent(() => module.default);
          setIsLoading(false);
        })
        .catch(err => {
          setError(err);
          setIsLoading(false);
        });
    }
  }, [isVisible, Component, importFunc]);

  return { ref, Component, isLoading, error };
};

/**
 * useVirtualScroll - Virtual scrolling for large lists
 * 
 * @param {Array} items - Array of items
 * @param {number} itemHeight - Height of each item
 * @param {number} containerHeight - Height of container
 * @returns {Object} Virtual scroll data
 */
export const useVirtualScroll = (items, itemHeight, containerHeight) => {
  const [scrollTop, setScrollTop] = useState(0);

  const visibleCount = Math.ceil(containerHeight / itemHeight);
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + visibleCount + 1, items.length);

  const visibleItems = useMemo(() => {
    return items.slice(startIndex, endIndex).map((item, index) => ({
      item,
      index: startIndex + index,
      top: (startIndex + index) * itemHeight
    }));
  }, [items, startIndex, endIndex, itemHeight]);

  const totalHeight = items.length * itemHeight;

  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop);
  }, []);

  return {
    visibleItems,
    totalHeight,
    handleScroll,
    startIndex,
    endIndex
  };
};

/**
 * useImageLazyLoad - Lazy load images
 * 
 * @param {string} src - Image source
 * @param {string} placeholder - Placeholder image
 * @returns {Object} { imageSrc, isLoading }
 */
export const useImageLazyLoad = (src, placeholder = '') => {
  const [imageSrc, setImageSrc] = useState(placeholder);
  const [isLoading, setIsLoading] = useState(true);
  const [ref, isVisible] = useIntersectionObserver();

  useEffect(() => {
    if (isVisible && src) {
      const img = new Image();
      img.src = src;
      img.onload = () => {
        setImageSrc(src);
        setIsLoading(false);
      };
      img.onerror = () => {
        setIsLoading(false);
      };
    }
  }, [isVisible, src]);

  return { ref, imageSrc, isLoading };
};

/**
 * useMemoCompare - Memoize with custom comparison
 * 
 * @param {any} value - Value to memoize
 * @param {Function} compare - Comparison function
 * @returns {any} Memoized value
 */
export const useMemoCompare = (value, compare) => {
  const previousRef = useRef();
  const previous = previousRef.current;

  const isEqual = compare(previous, value);

  useEffect(() => {
    if (!isEqual) {
      previousRef.current = value;
    }
  });

  return isEqual ? previous : value;
};

/**
 * useWhyDidYouUpdate - Debug why component re-rendered
 * 
 * @param {string} name - Component name
 * @param {Object} props - Component props
 */
export const useWhyDidYouUpdate = (name, props) => {
  const previousProps = useRef();

  useEffect(() => {
    if (previousProps.current) {
      const allKeys = Object.keys({ ...previousProps.current, ...props });
      const changedProps = {};

      allKeys.forEach(key => {
        if (previousProps.current[key] !== props[key]) {
          changedProps[key] = {
            from: previousProps.current[key],
            to: props[key]
          };
        }
      });

      if (Object.keys(changedProps).length > 0) {
        console.log('[Why-Did-You-Update]', name, changedProps);
      }
    }

    previousProps.current = props;
  });
};

/**
 * useRenderCount - Count component renders
 * 
 * @param {string} componentName - Component name
 * @returns {number} Render count
 */
export const useRenderCount = (componentName) => {
  const renderCount = useRef(0);

  useEffect(() => {
    renderCount.current++;
    console.log(`[Render Count] ${componentName}: ${renderCount.current}`);
  });

  return renderCount.current;
};

/**
 * useOptimizedCallback - Optimized callback with dependencies
 * 
 * @param {Function} callback - Callback function
 * @param {Array} deps - Dependencies
 * @returns {Function} Optimized callback
 */
export const useOptimizedCallback = (callback, deps) => {
  return useCallback(callback, deps);
};

/**
 * useOptimizedMemo - Optimized memo with dependencies
 * 
 * @param {Function} factory - Factory function
 * @param {Array} deps - Dependencies
 * @returns {any} Memoized value
 */
export const useOptimizedMemo = (factory, deps) => {
  return useMemo(factory, deps);
};

/**
 * usePrevious - Get previous value
 * 
 * @param {any} value - Current value
 * @returns {any} Previous value
 */
export const usePrevious = (value) => {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
};

/**
 * useMediaQuery - Responsive media query hook
 * 
 * @param {string} query - Media query string
 * @returns {boolean} Match result
 */
export const useMediaQuery = (query) => {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addListener(listener);

    return () => media.removeListener(listener);
  }, [matches, query]);

  return matches;
};

export default {
  useDebounce,
  useThrottle,
  useIntersectionObserver,
  useLazyLoad,
  useVirtualScroll,
  useImageLazyLoad,
  useMemoCompare,
  useWhyDidYouUpdate,
  useRenderCount,
  useOptimizedCallback,
  useOptimizedMemo,
  usePrevious,
  useMediaQuery
};

