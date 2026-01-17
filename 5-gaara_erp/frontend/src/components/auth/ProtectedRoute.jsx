// -*- javascript -*-
// FILE: frontend/src/components/auth/ProtectedRoute.jsx
// PURPOSE: Route protection with permission checks
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

/**
 * Protected Route Components
 * Implement frontend route guards with RBAC permission checks
 * 
 * Features:
 * - Role-based access control
 * - Permission-based access control
 * - Loading states
 * - Unauthorized fallback
 * - Redirect on unauthorized
 */

import * as React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Shield, Lock, Loader2, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
// import { cn } from '@/lib/utils'; // Currently unused

// ============================================================================
// Auth Context Hook (you can replace with your actual auth context)
// ============================================================================

/**
 * Mock useAuth hook - replace with your actual implementation
 */
const useAuth = () => {
  const [user, setUser] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    // Check for stored auth token
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          // Verify token with backend
          const response = await fetch('/api/auth/me', {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.ok) {
            const userData = await response.json();
            setUser(userData.data || userData);
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const isAuthenticated = !!user;
  const isAdmin = user?.role === 'admin';
  const hasRole = (role) => user?.role === role;
  const hasPermission = (permission) => {
    if (!user?.permissions) return false;
    return user.permissions.includes(permission) || user.permissions.includes('*');
  };

  return {
    user,
    loading,
    isAuthenticated,
    isAdmin,
    hasRole,
    hasPermission,
  };
};

// ============================================================================
// Loading Component
// ============================================================================

const LoadingScreen = () => (
  <div className="min-h-screen flex items-center justify-center bg-background">
    <div className="text-center">
      <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
      <p className="mt-4 text-muted-foreground">جاري التحقق من الصلاحيات...</p>
    </div>
  </div>
);

// ============================================================================
// Unauthorized Component
// ============================================================================

const UnauthorizedPage = ({ 
  title = "غير مصرح بالوصول",
  description = "ليس لديك الصلاحيات الكافية للوصول إلى هذه الصفحة",
  showBackButton = true,
  showLoginButton = false,
}) => {
  const navigate = React.useCallback(() => window.history.back(), []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <div className="mx-auto h-16 w-16 rounded-full bg-destructive/10 flex items-center justify-center mb-4">
            <Lock className="h-8 w-8 text-destructive" />
          </div>
          <CardTitle className="text-2xl">{title}</CardTitle>
          <CardDescription className="text-base">
            {description}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          {showBackButton && (
            <Button variant="outline" onClick={navigate}>
              العودة للصفحة السابقة
            </Button>
          )}
          {showLoginButton && (
            <Button asChild>
              <a href="/login">تسجيل الدخول</a>
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

// ============================================================================
// Protected Route Component
// ============================================================================

/**
 * ProtectedRoute - Wrap routes that require authentication
 * 
 * @example
 * // Basic authentication check
 * <ProtectedRoute>
 *   <Dashboard />
 * </ProtectedRoute>
 * 
 * @example
 * // With role requirement
 * <ProtectedRoute requiredRole="admin">
 *   <AdminPanel />
 * </ProtectedRoute>
 * 
 * @example
 * // With permission requirement
 * <ProtectedRoute requiredPermission="products:write">
 *   <ProductsPage />
 * </ProtectedRoute>
 */
export function ProtectedRoute({
  children,
  requiredRole,
  requiredPermission,
  requiredPermissions,
  requireAdmin = false,
  requireAll = false,
  redirectTo = '/login',
  fallback,
  showUnauthorized = true,
}) {
  const location = useLocation();
  const { loading, isAuthenticated, isAdmin, hasRole, hasPermission } = useAuth();

  // Show loading state
  if (loading) {
    return <LoadingScreen />;
  }

  // Check authentication
  if (!isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Check admin requirement
  if (requireAdmin && !isAdmin) {
    if (fallback) return fallback;
    if (showUnauthorized) {
      return (
        <UnauthorizedPage
          title="صفحة المشرفين فقط"
          description="هذه الصفحة متاحة للمشرفين فقط"
        />
      );
    }
    return <Navigate to="/" replace />;
  }

  // Check role requirement
  if (requiredRole && !hasRole(requiredRole)) {
    if (fallback) return fallback;
    if (showUnauthorized) {
      return (
        <UnauthorizedPage
          title="صلاحية غير كافية"
          description={`تحتاج صلاحية "${requiredRole}" للوصول إلى هذه الصفحة`}
        />
      );
    }
    return <Navigate to="/" replace />;
  }

  // Check single permission requirement
  if (requiredPermission && !hasPermission(requiredPermission)) {
    if (fallback) return fallback;
    if (showUnauthorized) {
      return (
        <UnauthorizedPage
          title="صلاحية غير كافية"
          description="ليس لديك الصلاحية المطلوبة للوصول إلى هذه الصفحة"
        />
      );
    }
    return <Navigate to="/" replace />;
  }

  // Check multiple permissions
  if (requiredPermissions && requiredPermissions.length > 0) {
    const hasAccess = requireAll
      ? requiredPermissions.every(hasPermission)
      : requiredPermissions.some(hasPermission);

    if (!hasAccess) {
      if (fallback) return fallback;
      if (showUnauthorized) {
        return (
          <UnauthorizedPage
            title="صلاحيات غير كافية"
            description="ليس لديك الصلاحيات المطلوبة للوصول إلى هذه الصفحة"
          />
        );
      }
      return <Navigate to="/" replace />;
    }
  }

  // All checks passed
  return children;
}

// ============================================================================
// Permission Guard Component
// ============================================================================

/**
 * PermissionGuard - Conditionally render content based on permissions
 * 
 * @example
 * <PermissionGuard permission="products:write">
 *   <Button>إضافة منتج</Button>
 * </PermissionGuard>
 * 
 * @example
 * <PermissionGuard permission="products:delete" fallback={<span>غير مسموح</span>}>
 *   <Button variant="destructive">حذف</Button>
 * </PermissionGuard>
 */
export function PermissionGuard({
  children,
  permission,
  permissions,
  role,
  requireAdmin = false,
  requireAll = false,
  fallback = null,
  hide = false,
}) {
  const { isAuthenticated, isAdmin, hasRole, hasPermission } = useAuth();

  // Not authenticated
  if (!isAuthenticated) {
    return hide ? null : fallback;
  }

  // Admin check
  if (requireAdmin && !isAdmin) {
    return hide ? null : fallback;
  }

  // Role check
  if (role && !hasRole(role)) {
    return hide ? null : fallback;
  }

  // Single permission check
  if (permission && !hasPermission(permission)) {
    return hide ? null : fallback;
  }

  // Multiple permissions check
  if (permissions && permissions.length > 0) {
    const hasAccess = requireAll
      ? permissions.every(hasPermission)
      : permissions.some(hasPermission);

    if (!hasAccess) {
      return hide ? null : fallback;
    }
  }

  return children;
}

// ============================================================================
// Admin Only Component
// ============================================================================

/**
 * AdminOnly - Render content only for admin users
 * 
 * @example
 * <AdminOnly>
 *   <Button>إعدادات المشرف</Button>
 * </AdminOnly>
 */
export function AdminOnly({ children, fallback = null }) {
  return (
    <PermissionGuard requireAdmin fallback={fallback}>
      {children}
    </PermissionGuard>
  );
}

// ============================================================================
// usePermissionCheck Hook
// ============================================================================

/**
 * usePermissionCheck - Hook to check permissions programmatically
 * 
 * @example
 * const { canEdit, canDelete } = usePermissionCheck({
 *   permissions: ['products:write', 'products:delete']
 * });
 * 
 * if (canEdit) {
 *   // Show edit button
 * }
 */
export function usePermissionCheck({
  permission,
  permissions,
  role,
  requireAdmin = false,
}) {
  const { isAuthenticated, isAdmin, hasRole, hasPermission, loading } = useAuth();

  const checks = React.useMemo(() => {
    if (loading || !isAuthenticated) {
      return {
        hasAccess: false,
        loading,
        isAuthenticated,
      };
    }

    let hasAccess = true;

    if (requireAdmin) {
      hasAccess = isAdmin;
    }

    if (hasAccess && role) {
      hasAccess = hasRole(role);
    }

    if (hasAccess && permission) {
      hasAccess = hasPermission(permission);
    }

    // Create individual permission checks
    const permissionChecks = {};
    if (permissions) {
      permissions.forEach((p) => {
        const key = p.replace(':', '_').replace('-', '_');
        permissionChecks[`can_${key}`] = hasPermission(p);
      });
    }

    return {
      hasAccess,
      loading,
      isAuthenticated,
      isAdmin,
      ...permissionChecks,
    };
  }, [loading, isAuthenticated, isAdmin, role, permission, permissions, hasRole, hasPermission, requireAdmin]);

  return checks;
}

// ============================================================================
// Exports
// ============================================================================

export {
  useAuth,
  LoadingScreen,
  UnauthorizedPage,
};

export default ProtectedRoute;

