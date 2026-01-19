/**
 * useApi Hook
 * ============
 * 
 * Custom React hook for API calls with loading states, error handling,
 * and automatic retry functionality.
 * 
 * Features:
 * - Loading state management
 * - Error handling with toast notifications
 * - Automatic retry on failure
 * - Request cancellation
 * - Caching support
 * - Pagination helpers
 * 
 * @author Global System v35.0
 * @date 2026-01-17
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import apiService, { ApiError, NetworkError, AuthenticationError } from '../../services/ApiService';

/**
 * Main API hook for data fetching
 * 
 * @param {Function} apiFunction - API function to call
 * @param {Object} options - Hook options
 * @returns {Object} Hook state and methods
 * 
 * @example
 * const { data, loading, error, execute } = useApi(
 *   () => apiService.getFarms(),
 *   { immediate: true }
 * );
 */
export const useApi = (apiFunction, options = {}) => {
  const {
    immediate = false,
    initialData = null,
    onSuccess = null,
    onError = null,
    retryCount = 0,
    retryDelay = 1000,
    cache = false,
    cacheKey = null,
    cacheTTL = 5 * 60 * 1000 // 5 minutes
  } = options;

  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const mountedRef = useRef(true);
  const abortControllerRef = useRef(null);
  const retriesRef = useRef(0);

  // Cache storage
  const cacheRef = useRef(new Map());

  /**
   * Execute the API call
   */
  const execute = useCallback(async (...args) => {
    // Cancel any pending request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    // Check cache
    const effectiveCacheKey = cacheKey || JSON.stringify(args);
    if (cache && cacheRef.current.has(effectiveCacheKey)) {
      const cached = cacheRef.current.get(effectiveCacheKey);
      if (Date.now() - cached.timestamp < cacheTTL) {
        setData(cached.data);
        return cached.data;
      }
      cacheRef.current.delete(effectiveCacheKey);
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiFunction(...args);
      
      if (!mountedRef.current) return;

      // Handle different response formats
      const responseData = result?.data !== undefined ? result.data : result;
      
      setData(responseData);
      retriesRef.current = 0;

      // Cache result
      if (cache) {
        cacheRef.current.set(effectiveCacheKey, {
          data: responseData,
          timestamp: Date.now()
        });
      }

      if (onSuccess) {
        onSuccess(responseData);
      }

      return responseData;

    } catch (err) {
      if (!mountedRef.current) return;

      // Handle retry
      if (retriesRef.current < retryCount && !(err instanceof AuthenticationError)) {
        retriesRef.current += 1;
        console.log(`Retrying request (${retriesRef.current}/${retryCount})...`);
        
        await new Promise(resolve => setTimeout(resolve, retryDelay));
        return execute(...args);
      }

      // Format error
      const formattedError = formatError(err);
      setError(formattedError);

      if (onError) {
        onError(formattedError);
      }

      throw err;

    } finally {
      if (mountedRef.current) {
        setLoading(false);
      }
    }
  }, [apiFunction, cache, cacheKey, cacheTTL, onSuccess, onError, retryCount, retryDelay]);

  /**
   * Reset state
   */
  const reset = useCallback(() => {
    setData(initialData);
    setError(null);
    setLoading(false);
    retriesRef.current = 0;
  }, [initialData]);

  /**
   * Clear cache
   */
  const clearCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  /**
   * Cancel pending request
   */
  const cancel = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  }, []);

  // Execute immediately if requested
  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate]); // eslint-disable-line react-hooks/exhaustive-deps

  // Cleanup
  useEffect(() => {
    return () => {
      mountedRef.current = false;
      cancel();
    };
  }, [cancel]);

  return {
    data,
    loading,
    error,
    execute,
    reset,
    clearCache,
    cancel,
    isError: !!error,
    isSuccess: !loading && !error && data !== null
  };
};

/**
 * Hook for paginated API calls
 * 
 * @param {Function} apiFunction - API function that accepts pagination params
 * @param {Object} options - Hook options
 * @returns {Object} Pagination state and methods
 * 
 * @example
 * const { 
 *   data, loading, page, setPage, hasMore 
 * } = usePaginatedApi(
 *   (params) => apiService.getFarms(params),
 *   { perPage: 20 }
 * );
 */
export const usePaginatedApi = (apiFunction, options = {}) => {
  const {
    initialPage = 1,
    perPage = 20,
    onSuccess = null,
    onError = null
  } = options;

  const [items, setItems] = useState([]);
  const [page, setPage] = useState(initialPage);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mountedRef = useRef(true);

  const fetchPage = useCallback(async (pageNum, append = false) => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiFunction({
        page: pageNum,
        per_page: perPage
      });

      if (!mountedRef.current) return;

      // Handle response format
      const responseItems = result?.data || result?.items || result || [];
      const meta = result?.meta?.pagination || result?.pagination || {};

      if (append) {
        setItems(prev => [...prev, ...responseItems]);
      } else {
        setItems(responseItems);
      }

      setTotal(meta.total || responseItems.length);
      setTotalPages(meta.total_pages || Math.ceil((meta.total || responseItems.length) / perPage));
      setPage(pageNum);

      if (onSuccess) {
        onSuccess(result);
      }

      return result;

    } catch (err) {
      if (!mountedRef.current) return;
      
      const formattedError = formatError(err);
      setError(formattedError);

      if (onError) {
        onError(formattedError);
      }

      throw err;

    } finally {
      if (mountedRef.current) {
        setLoading(false);
      }
    }
  }, [apiFunction, perPage, onSuccess, onError]);

  const goToPage = useCallback((pageNum) => {
    if (pageNum >= 1 && pageNum <= totalPages) {
      fetchPage(pageNum);
    }
  }, [fetchPage, totalPages]);

  const nextPage = useCallback(() => {
    if (page < totalPages) {
      fetchPage(page + 1);
    }
  }, [fetchPage, page, totalPages]);

  const prevPage = useCallback(() => {
    if (page > 1) {
      fetchPage(page - 1);
    }
  }, [fetchPage, page]);

  const loadMore = useCallback(() => {
    if (page < totalPages && !loading) {
      fetchPage(page + 1, true);
    }
  }, [fetchPage, page, totalPages, loading]);

  const refresh = useCallback(() => {
    setPage(initialPage);
    fetchPage(initialPage);
  }, [fetchPage, initialPage]);

  // Cleanup
  useEffect(() => {
    return () => {
      mountedRef.current = false;
    };
  }, []);

  return {
    items,
    loading,
    error,
    page,
    perPage,
    total,
    totalPages,
    hasMore: page < totalPages,
    hasPrev: page > 1,
    fetchPage,
    goToPage,
    nextPage,
    prevPage,
    loadMore,
    refresh,
    setPage
  };
};

/**
 * Hook for mutation operations (create, update, delete)
 * 
 * @param {Function} apiFunction - API mutation function
 * @param {Object} options - Hook options
 * @returns {Object} Mutation state and methods
 * 
 * @example
 * const { mutate, loading } = useMutation(
 *   (data) => apiService.createFarm(data),
 *   { onSuccess: () => toast.success('Farm created!') }
 * );
 */
export const useMutation = (apiFunction, options = {}) => {
  const {
    onSuccess = null,
    onError = null,
    invalidateQueries = []
  } = options;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const mutate = useCallback(async (...args) => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiFunction(...args);
      
      setData(result);

      if (onSuccess) {
        onSuccess(result);
      }

      // Invalidate related queries
      if (invalidateQueries.length > 0) {
        // Trigger refetch for related queries
        window.dispatchEvent(new CustomEvent('invalidate-queries', {
          detail: { keys: invalidateQueries }
        }));
      }

      return result;

    } catch (err) {
      const formattedError = formatError(err);
      setError(formattedError);

      if (onError) {
        onError(formattedError);
      }

      throw err;

    } finally {
      setLoading(false);
    }
  }, [apiFunction, onSuccess, onError, invalidateQueries]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    mutate,
    loading,
    error,
    data,
    reset,
    isError: !!error,
    isSuccess: !loading && !error && data !== null
  };
};

/**
 * Hook for form submission with API
 * 
 * @param {Function} submitFunction - API submit function
 * @param {Object} options - Hook options
 * @returns {Object} Form submission state and methods
 */
export const useFormSubmit = (submitFunction, options = {}) => {
  const {
    onSuccess = null,
    onError = null,
    resetOnSuccess = true,
    validateOnSubmit = null
  } = options;

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const submit = useCallback(async (formData) => {
    // Validate if validator provided
    if (validateOnSubmit) {
      const validationErrors = validateOnSubmit(formData);
      if (Object.keys(validationErrors).length > 0) {
        setFieldErrors(validationErrors);
        return false;
      }
    }

    setSubmitting(true);
    setError(null);
    setFieldErrors({});
    setSuccess(false);

    try {
      const result = await submitFunction(formData);

      setSuccess(true);

      if (onSuccess) {
        onSuccess(result);
      }

      return result;

    } catch (err) {
      const formattedError = formatError(err);
      setError(formattedError);

      // Extract field errors if available
      if (err?.errors) {
        setFieldErrors(err.errors);
      }

      if (onError) {
        onError(formattedError);
      }

      return false;

    } finally {
      setSubmitting(false);
    }
  }, [submitFunction, onSuccess, onError, validateOnSubmit]);

  const reset = useCallback(() => {
    setError(null);
    setFieldErrors({});
    setSuccess(false);
  }, []);

  return {
    submit,
    submitting,
    error,
    fieldErrors,
    success,
    reset,
    setFieldErrors
  };
};

/**
 * Format error for display
 */
function formatError(err) {
  if (err instanceof AuthenticationError) {
    return {
      type: 'auth',
      message: err.message || 'Authentication required',
      message_ar: 'يتطلب تسجيل الدخول'
    };
  }

  if (err instanceof NetworkError) {
    return {
      type: 'network',
      message: err.message || 'Network error',
      message_ar: 'خطأ في الاتصال'
    };
  }

  if (err instanceof ApiError) {
    return {
      type: 'api',
      status: err.status,
      message: err.message,
      message_ar: err.data?.message_ar || err.message,
      data: err.data
    };
  }

  return {
    type: 'unknown',
    message: err.message || 'An error occurred',
    message_ar: 'حدث خطأ'
  };
}

export default useApi;
