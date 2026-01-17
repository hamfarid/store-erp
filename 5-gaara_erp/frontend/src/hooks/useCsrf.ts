/**
 * P1.36: CSRF Token Management Hook
 * 
 * Provides CSRF token fetching, caching, and automatic form integration.
 */

import { useState, useEffect, useCallback, createContext, useContext, ReactNode } from 'react';

// =============================================================================
// Types
// =============================================================================

interface CsrfContextType {
  csrfToken: string | null;
  isLoading: boolean;
  error: Error | null;
  refreshToken: () => Promise<string | null>;
}

interface CsrfProviderProps {
  children: ReactNode;
  apiBaseUrl?: string;
}

// =============================================================================
// Context
// =============================================================================

const CsrfContext = createContext<CsrfContextType | null>(null);

// =============================================================================
// Provider Component
// =============================================================================

export function CsrfProvider({ children, apiBaseUrl = '/api' }: CsrfProviderProps) {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchCsrfToken = useCallback(async (): Promise<string | null> => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetch(`${apiBaseUrl}/csrf-token`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch CSRF token: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success && data.data?.csrf_token) {
        const token = data.data.csrf_token;
        setCsrfToken(token);
        
        // Store in meta tag for easy access
        updateMetaTag(token);
        
        // Store in sessionStorage for persistence
        sessionStorage.setItem('csrf_token', token);
        
        return token;
      }
      
      throw new Error('Invalid CSRF token response');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      console.error('P1.36: CSRF token fetch error:', error);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [apiBaseUrl]);

  const refreshToken = useCallback(async () => {
    return fetchCsrfToken();
  }, [fetchCsrfToken]);

  // Initial fetch
  useEffect(() => {
    // Check sessionStorage first
    const storedToken = sessionStorage.getItem('csrf_token');
    if (storedToken) {
      setCsrfToken(storedToken);
      updateMetaTag(storedToken);
      setIsLoading(false);
    }
    
    // Fetch fresh token
    fetchCsrfToken();
  }, [fetchCsrfToken]);

  // Refresh token periodically (every 30 minutes)
  useEffect(() => {
    const interval = setInterval(() => {
      fetchCsrfToken();
    }, 30 * 60 * 1000);

    return () => clearInterval(interval);
  }, [fetchCsrfToken]);

  return (
    <CsrfContext.Provider value={{ csrfToken, isLoading, error, refreshToken }}>
      {children}
    </CsrfContext.Provider>
  );
}

// =============================================================================
// Hook
// =============================================================================

export function useCsrf(): CsrfContextType {
  const context = useContext(CsrfContext);
  
  if (!context) {
    throw new Error('useCsrf must be used within a CsrfProvider');
  }
  
  return context;
}

// =============================================================================
// Utility Functions
// =============================================================================

function updateMetaTag(token: string): void {
  if (typeof document === 'undefined') return;
  
  let meta = document.querySelector('meta[name="csrf-token"]');
  
  if (!meta) {
    meta = document.createElement('meta');
    meta.setAttribute('name', 'csrf-token');
    document.head.appendChild(meta);
  }
  
  meta.setAttribute('content', token);
}

/**
 * Get CSRF token from various sources.
 */
export function getCsrfToken(): string | null {
  // Try meta tag first
  if (typeof document !== 'undefined') {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) {
      return meta.getAttribute('content');
    }
  }
  
  // Try sessionStorage
  if (typeof sessionStorage !== 'undefined') {
    return sessionStorage.getItem('csrf_token');
  }
  
  return null;
}

/**
 * Add CSRF token to fetch headers.
 */
export function addCsrfHeader(headers: HeadersInit = {}): HeadersInit {
  const token = getCsrfToken();
  
  if (token) {
    return {
      ...headers,
      'X-CSRF-Token': token,
    };
  }
  
  return headers;
}

/**
 * Create a fetch wrapper with automatic CSRF token inclusion.
 */
export function csrfFetch(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<Response> {
  const method = init?.method?.toUpperCase() || 'GET';
  
  // Only add CSRF for state-changing methods
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const headers = addCsrfHeader(init?.headers || {});
    
    return fetch(input, {
      ...init,
      headers,
      credentials: 'include',
    });
  }
  
  return fetch(input, init);
}

// =============================================================================
// Form Components
// =============================================================================

interface CsrfInputProps {
  name?: string;
}

/**
 * Hidden input component for CSRF token in forms.
 */
export function CsrfInput({ name = 'csrf_token' }: CsrfInputProps) {
  const { csrfToken } = useCsrf();
  
  if (!csrfToken) {
    return null;
  }
  
  return (
    <input
      type="hidden"
      name={name}
      value={csrfToken}
      data-testid="csrf-input"
    />
  );
}

// =============================================================================
// HOC for Forms
// =============================================================================

interface WithCsrfFormProps {
  onSubmit?: (event: React.FormEvent<HTMLFormElement>) => void;
}

/**
 * HOC to wrap forms with CSRF protection.
 */
export function withCsrfProtection<P extends WithCsrfFormProps>(
  WrappedComponent: React.ComponentType<P>
) {
  return function CsrfProtectedComponent(props: P) {
    const { csrfToken, refreshToken } = useCsrf();

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
      // Ensure we have a token
      if (!csrfToken) {
        event.preventDefault();
        await refreshToken();
        return;
      }

      // Add token to form if not present
      const form = event.currentTarget;
      let csrfInput = form.querySelector('input[name="csrf_token"]') as HTMLInputElement;
      
      if (!csrfInput) {
        csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrf_token';
        form.appendChild(csrfInput);
      }
      
      csrfInput.value = csrfToken;

      // Call original handler
      if (props.onSubmit) {
        props.onSubmit(event);
      }
    };

    return <WrappedComponent {...props} onSubmit={handleSubmit} />;
  };
}

// =============================================================================
// Axios Interceptor Setup
// =============================================================================

/**
 * Setup CSRF token interceptor for Axios.
 */
export function setupAxiosCsrfInterceptor(axiosInstance: any): void {
  axiosInstance.interceptors.request.use((config: any) => {
    const method = config.method?.toUpperCase();
    
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
      const token = getCsrfToken();
      if (token) {
        config.headers = config.headers || {};
        config.headers['X-CSRF-Token'] = token;
      }
    }
    
    return config;
  });
}

// =============================================================================
// Exports
// =============================================================================

export default useCsrf;

