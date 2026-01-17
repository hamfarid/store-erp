/**
 * FILE: frontend/src/hooks/useApi.ts
 * PURPOSE: React hook for API client with loading and error states
 * OWNER: Frontend Team
 * RELATED: frontend/src/api/client.ts
 * LAST-AUDITED: 2025-10-27
 */

import { useState, useCallback } from 'react';
import { apiClient } from '../api';
import type { ApiError } from '../api';

/**
 * API hook state
 */
export interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
}

/**
 * useApi hook for making API calls with loading and error states
 */
export function useApi<T>() {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async (fn: () => Promise<T>) => {
    setState({ data: null, loading: true, error: null });
    try {
      const result = await fn();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error) {
      const apiError: ApiError = {
        code: 'UNKNOWN_ERROR',
        message: error instanceof Error ? error.message : 'Unknown error',
      };
      setState({ data: null, loading: false, error: apiError });
      throw error;
    }
  }, []);

  return { ...state, execute };
}

/**
 * useLogin hook
 */
export function useLogin() {
  const api = useApi<any>();

  const login = useCallback(async (username: string, password: string) => {
    return api.execute(() =>
      apiClient.login({ username, password })
    );
  }, [api]);

  return { ...api, login };
}

/**
 * useLogout hook
 */
export function useLogout() {
  const api = useApi<any>();

  const logout = useCallback(async () => {
    return api.execute(() => apiClient.logout());
  }, [api]);

  return { ...api, logout };
}

/**
 * useProducts hook
 */
export function useProducts() {
  const api = useApi<any>();

  const getProducts = useCallback(async (page?: number, perPage?: number) => {
    return api.execute(() =>
      apiClient.getProducts({ page, per_page: perPage })
    );
  }, [api]);

  const getProduct = useCallback(async (id: string) => {
    return api.execute(() => apiClient.getProduct(id));
  }, [api]);

  const createProduct = useCallback(async (data: any) => {
    return api.execute(() => apiClient.createProduct(data));
  }, [api]);

  const updateProduct = useCallback(async (id: string, data: any) => {
    return api.execute(() => apiClient.updateProduct(id, data));
  }, [api]);

  const deleteProduct = useCallback(async (id: string) => {
    return api.execute(() => apiClient.deleteProduct(id));
  }, [api]);

  return {
    ...api,
    getProducts,
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct,
  };
}

/**
 * useCustomers hook
 */
export function useCustomers() {
  const api = useApi<any>();

  const getCustomers = useCallback(async (page?: number, perPage?: number) => {
    return api.execute(() =>
      apiClient.getCustomers({ page, per_page: perPage })
    );
  }, [api]);

  const getCustomer = useCallback(async (id: string) => {
    return api.execute(() => apiClient.getCustomer(id));
  }, [api]);

  const createCustomer = useCallback(async (data: any) => {
    return api.execute(() => apiClient.createCustomer(data));
  }, [api]);

  const updateCustomer = useCallback(async (id: string, data: any) => {
    return api.execute(() => apiClient.updateCustomer(id, data));
  }, [api]);

  const deleteCustomer = useCallback(async (id: string) => {
    return api.execute(() => apiClient.deleteCustomer(id));
  }, [api]);

  return {
    ...api,
    getCustomers,
    getCustomer,
    createCustomer,
    updateCustomer,
    deleteCustomer,
  };
}

/**
 * useMFA hook
 */
export function useMFA() {
  const api = useApi<any>();

  const setupMFA = useCallback(async () => {
    return api.execute(() => apiClient.setupMFA());
  }, [api]);

  const verifyMFA = useCallback(async (code: string) => {
    return api.execute(() => apiClient.verifyMFA(code));
  }, [api]);

  const disableMFA = useCallback(async () => {
    return api.execute(() => apiClient.disableMFA());
  }, [api]);

  return { ...api, setupMFA, verifyMFA, disableMFA };
}

