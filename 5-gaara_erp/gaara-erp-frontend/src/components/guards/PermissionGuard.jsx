/**
 * Permission Guard Components for Gaara ERP v12
 * 
 * SECURITY (2025-11-28):
 * - Route-level permission checking
 * - Component-level permission hiding
 * - Redirect unauthorized users
 */

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth, usePermission, useAnyPermission, useAllPermissions } from '../../contexts/AuthContext';

/**
 * Protected Route Guard
 * Redirects to login if not authenticated
 */
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

/**
 * Permission Route Guard
 * Requires specific permission(s) to access route
 */
export const PermissionRoute = ({ 
  children, 
  permission, 
  permissions = [], 
  requireAll = true,
  fallback = null,
  redirectTo = '/unauthorized'
}) => {
  const { isAuthenticated, loading, hasPermission, hasAnyPermission, hasAllPermissions } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check single permission
  if (permission && !hasPermission(permission)) {
    return fallback || <Navigate to={redirectTo} replace />;
  }

  // Check multiple permissions
  if (permissions.length > 0) {
    const hasAccess = requireAll 
      ? hasAllPermissions(permissions) 
      : hasAnyPermission(permissions);
    
    if (!hasAccess) {
      return fallback || <Navigate to={redirectTo} replace />;
    }
  }

  return children;
};

/**
 * Permission Component Guard
 * Conditionally renders children based on permission
 */
export const RequirePermission = ({ 
  permission, 
  permissions = [], 
  requireAll = true, 
  fallback = null, 
  children 
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions, user } = useAuth();

  // Superuser always has access
  if (user?.is_superuser) {
    return children;
  }

  // Check single permission
  if (permission) {
    return hasPermission(permission) ? children : fallback;
  }

  // Check multiple permissions
  if (permissions.length > 0) {
    const hasAccess = requireAll 
      ? hasAllPermissions(permissions) 
      : hasAnyPermission(permissions);
    
    return hasAccess ? children : fallback;
  }

  return children;
};

/**
 * Role Guard
 * Requires specific role(s) to access
 */
export const RequireRole = ({ 
  role, 
  roles = [], 
  fallback = null, 
  children 
}) => {
  const { user } = useAuth();

  if (!user) return fallback;

  // Check single role
  if (role && user.role !== role) {
    return fallback;
  }

  // Check multiple roles
  if (roles.length > 0 && !roles.includes(user.role)) {
    return fallback;
  }

  return children;
};

/**
 * Admin Only Guard
 * Only superusers/admins can access
 */
export const AdminOnly = ({ fallback = null, children }) => {
  const { user } = useAuth();

  if (!user?.is_superuser && !user?.is_staff) {
    return fallback;
  }

  return children;
};

/**
 * Hook for programmatic permission checking
 */
export const useCanAccess = (permission) => {
  const hasAccess = usePermission(permission);
  return hasAccess;
};

/**
 * HOC for permission-protected components
 */
export const withPermission = (WrappedComponent, permission, FallbackComponent = null) => {
  return function PermissionWrapper(props) {
    const hasAccess = usePermission(permission);
    
    if (!hasAccess) {
      return FallbackComponent ? <FallbackComponent {...props} /> : null;
    }
    
    return <WrappedComponent {...props} />;
  };
};

export default {
  ProtectedRoute,
  PermissionRoute,
  RequirePermission,
  RequireRole,
  AdminOnly,
  useCanAccess,
  withPermission,
};

