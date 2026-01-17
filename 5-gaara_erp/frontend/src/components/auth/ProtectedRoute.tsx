/**
 * P0.11: Frontend Route Protection
 * 
 * Provides route guards and permission-based access control for React Router.
 * Integrates with the backend RBAC system.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';

// =============================================================================
// Types
// =============================================================================

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  role: string;
  role_id: number;
  permissions: string[];
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
  hasRole: (role: string) => boolean;
}

interface ProtectedRouteProps {
  /** Required permission to access the route */
  permission?: string;
  /** Required permissions (any of them) */
  anyPermissions?: string[];
  /** Required permissions (all of them) */
  allPermissions?: string[];
  /** Required role */
  role?: string;
  /** Allowed roles */
  roles?: string[];
  /** Redirect path when unauthorized */
  redirectTo?: string;
  /** Custom fallback component */
  fallback?: ReactNode;
  /** Children components */
  children?: ReactNode;
}

// =============================================================================
// Auth Context
// =============================================================================

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// =============================================================================
// Auth Provider
// =============================================================================

interface AuthProviderProps {
  children: ReactNode;
  apiBaseUrl?: string;
}

export function AuthProvider({ children, apiBaseUrl = '/api' }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user on mount
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await fetch(`${apiBaseUrl}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.success && data.data) {
            setUser(data.data);
          }
        } else {
          // Token invalid, clear it
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      } catch (error) {
        console.error('Failed to load user:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, [apiBaseUrl]);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch(`${apiBaseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (data.success && data.data) {
        localStorage.setItem('access_token', data.data.access_token);
        localStorage.setItem('refresh_token', data.data.refresh_token);
        setUser(data.data.user);
        return true;
      }

      return false;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (token) {
        await fetch(`${apiBaseUrl}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    // Admin has all permissions
    if (user.permissions.includes('admin_full')) return true;
    return user.permissions.includes(permission);
  };

  const hasAnyPermission = (permissions: string[]): boolean => {
    return permissions.some(hasPermission);
  };

  const hasAllPermissions = (permissions: string[]): boolean => {
    return permissions.every(hasPermission);
  };

  const hasRole = (role: string): boolean => {
    if (!user) return false;
    return user.role.toLowerCase() === role.toLowerCase();
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// =============================================================================
// Protected Route Component
// =============================================================================

export function ProtectedRoute({
  permission,
  anyPermissions,
  allPermissions,
  role,
  roles,
  redirectTo = '/login',
  fallback,
  children,
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, hasPermission, hasAnyPermission, hasAllPermissions, hasRole, user } = useAuth();
  const location = useLocation();

  // Show loading state
  if (isLoading) {
    return fallback ? <>{fallback}</> : <LoadingSpinner />;
  }

  // Check authentication
  if (!isAuthenticated) {
    // Save attempted URL for redirect after login
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Check single permission
  if (permission && !hasPermission(permission)) {
    return <AccessDenied permission={permission} />;
  }

  // Check any permissions
  if (anyPermissions && anyPermissions.length > 0 && !hasAnyPermission(anyPermissions)) {
    return <AccessDenied permissions={anyPermissions} type="any" />;
  }

  // Check all permissions
  if (allPermissions && allPermissions.length > 0 && !hasAllPermissions(allPermissions)) {
    return <AccessDenied permissions={allPermissions} type="all" />;
  }

  // Check single role
  if (role && !hasRole(role)) {
    return <AccessDenied role={role} />;
  }

  // Check multiple roles
  if (roles && roles.length > 0 && !roles.some((r) => hasRole(r))) {
    return <AccessDenied roles={roles} />;
  }

  // All checks passed
  return children ? <>{children}</> : <Outlet />;
}

// =============================================================================
// Permission Gate Component
// =============================================================================

interface PermissionGateProps {
  permission?: string;
  anyPermissions?: string[];
  allPermissions?: string[];
  role?: string;
  roles?: string[];
  fallback?: ReactNode;
  children: ReactNode;
}

export function PermissionGate({
  permission,
  anyPermissions,
  allPermissions,
  role,
  roles,
  fallback = null,
  children,
}: PermissionGateProps) {
  const { hasPermission, hasAnyPermission, hasAllPermissions, hasRole } = useAuth();

  // Check single permission
  if (permission && !hasPermission(permission)) {
    return <>{fallback}</>;
  }

  // Check any permissions
  if (anyPermissions && anyPermissions.length > 0 && !hasAnyPermission(anyPermissions)) {
    return <>{fallback}</>;
  }

  // Check all permissions
  if (allPermissions && allPermissions.length > 0 && !hasAllPermissions(allPermissions)) {
    return <>{fallback}</>;
  }

  // Check single role
  if (role && !hasRole(role)) {
    return <>{fallback}</>;
  }

  // Check multiple roles
  if (roles && roles.length > 0 && !roles.some((r) => hasRole(r))) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

// =============================================================================
// Helper Components
// =============================================================================

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  );
}

interface AccessDeniedProps {
  permission?: string;
  permissions?: string[];
  role?: string;
  roles?: string[];
  type?: 'any' | 'all';
}

function AccessDenied({ permission, permissions, role, roles, type }: AccessDeniedProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center p-8 bg-white rounded-lg shadow-lg max-w-md">
        <div className="text-red-500 text-6xl mb-4">🚫</div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Access Denied
        </h1>
        <p className="text-gray-600 mb-4">
          ليس لديك صلاحية للوصول إلى هذه الصفحة
        </p>
        
        {permission && (
          <p className="text-sm text-gray-500">
            Required permission: <code className="bg-gray-100 px-2 py-1 rounded">{permission}</code>
          </p>
        )}
        
        {permissions && (
          <p className="text-sm text-gray-500">
            Required permissions ({type === 'all' ? 'all' : 'any'}): {permissions.map((p, i) => (
              <code key={p} className="bg-gray-100 px-2 py-1 rounded mx-1">{p}</code>
            ))}
          </p>
        )}
        
        {role && (
          <p className="text-sm text-gray-500">
            Required role: <code className="bg-gray-100 px-2 py-1 rounded">{role}</code>
          </p>
        )}
        
        {roles && (
          <p className="text-sm text-gray-500">
            Required roles: {roles.map((r, i) => (
              <code key={r} className="bg-gray-100 px-2 py-1 rounded mx-1">{r}</code>
            ))}
          </p>
        )}
        
        <button
          onClick={() => window.history.back()}
          className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
        >
          Go Back
        </button>
      </div>
    </div>
  );
}

// =============================================================================
// HOC for Class Components
// =============================================================================

export function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P & { auth: AuthContextType }>
) {
  return function WithAuthComponent(props: P) {
    const auth = useAuth();
    return <WrappedComponent {...props} auth={auth} />;
  };
}

export function withPermission<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  permission: string
) {
  return function WithPermissionComponent(props: P) {
    const { hasPermission } = useAuth();
    
    if (!hasPermission(permission)) {
      return <AccessDenied permission={permission} />;
    }
    
    return <WrappedComponent {...props} />;
  };
}

// =============================================================================
// Permissions Constants (matching backend)
// =============================================================================

export const Permissions = {
  // System Management
  ADMIN_FULL: 'admin_full',
  SYSTEM_SETTINGS_VIEW: 'system_settings_view',
  SYSTEM_SETTINGS_EDIT: 'system_settings_edit',

  // User Management
  USER_MANAGEMENT_VIEW: 'user_management_view',
  USER_MANAGEMENT_ADD: 'user_management_add',
  USER_MANAGEMENT_EDIT: 'user_management_edit',
  USER_MANAGEMENT_DELETE: 'user_management_delete',

  // Inventory Management
  INVENTORY_VIEW: 'inventory_view',
  INVENTORY_ADD: 'inventory_add',
  INVENTORY_EDIT: 'inventory_edit',
  INVENTORY_DELETE: 'inventory_delete',
  INVENTORY_STOCK_ADJUST: 'inventory_stock_adjust',

  // Product Management
  PRODUCTS_VIEW: 'products_view',
  PRODUCTS_ADD: 'products_add',
  PRODUCTS_EDIT: 'products_edit',
  PRODUCTS_DELETE: 'products_delete',

  // Sales Management
  SALES_VIEW: 'sales_view',
  SALES_ADD: 'sales_add',
  SALES_EDIT: 'sales_edit',
  SALES_DELETE: 'sales_delete',

  // Purchases Management
  PURCHASES_VIEW: 'purchases_view',
  PURCHASES_ADD: 'purchases_add',
  PURCHASES_EDIT: 'purchases_edit',
  PURCHASES_DELETE: 'purchases_delete',

  // Partners
  PARTNERS_VIEW: 'partners_view',
  PARTNERS_ADD: 'partners_add',
  PARTNERS_EDIT: 'partners_edit',
  PARTNERS_DELETE: 'partners_delete',

  // Reports
  REPORTS_VIEW: 'reports_view',
  REPORTS_EXPORT: 'reports_export',
  REPORTS_ADVANCED: 'reports_advanced',

  // Dashboard
  DASHBOARD_VIEW: 'dashboard_view',
} as const;

// =============================================================================
// Exports
// =============================================================================

export default ProtectedRoute;

