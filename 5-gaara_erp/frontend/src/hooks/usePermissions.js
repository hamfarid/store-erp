/**
 * usePermissions Hook
 * 
 * Custom hook for checking user permissions in the frontend.
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useAuth } from '../contexts/AuthContext';
import adminService from '../services/adminService';

/**
 * Check if a user has a specific permission
 */
export const usePermission = (permissionCode) => {
  const { user, isAuthenticated } = useAuth();
  const [hasPermission, setHasPermission] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated || !user) {
      setHasPermission(false);
      setIsLoading(false);
      return;
    }

    // Check if user is super admin
    if (user.roles?.some(role => role.code === 'super_admin')) {
      setHasPermission(true);
      setIsLoading(false);
      return;
    }

    // Check local permissions first
    const localCheck = user.permissions?.includes(permissionCode) ||
      user.roles?.some(role => 
        role.permissions?.some(p => p.code === permissionCode)
      );

    if (localCheck !== undefined) {
      setHasPermission(localCheck);
      setIsLoading(false);
      return;
    }

    // Fallback to API check
    const checkPermission = async () => {
      try {
        const result = await adminService.checkPermission(permissionCode);
        setHasPermission(result);
      } catch (error) {
        console.error('Permission check failed:', error);
        setHasPermission(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkPermission();
  }, [user, isAuthenticated, permissionCode]);

  return { hasPermission, isLoading };
};

/**
 * Check multiple permissions at once
 */
export const usePermissions = (permissionCodes = []) => {
  const { user, isAuthenticated } = useAuth();
  const [permissions, setPermissions] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated || !user || !permissionCodes.length) {
      setPermissions({});
      setIsLoading(false);
      return;
    }

    const isSuperAdmin = user.roles?.some(role => role.code === 'super_admin');
    
    const result = {};
    permissionCodes.forEach(code => {
      if (isSuperAdmin) {
        result[code] = true;
      } else {
        result[code] = user.permissions?.includes(code) ||
          user.roles?.some(role => 
            role.permissions?.some(p => p.code === code)
          ) || false;
      }
    });

    setPermissions(result);
    setIsLoading(false);
  }, [user, isAuthenticated, permissionCodes.join(',')]);

  const hasPermission = useCallback((code) => permissions[code] || false, [permissions]);
  const hasAnyPermission = useCallback((codes) => codes.some(c => permissions[c]), [permissions]);
  const hasAllPermissions = useCallback((codes) => codes.every(c => permissions[c]), [permissions]);

  return {
    permissions,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    isLoading
  };
};

/**
 * Get all user permissions
 */
export const useAllPermissions = () => {
  const { user, isAuthenticated } = useAuth();
  
  const allPermissions = useMemo(() => {
    if (!isAuthenticated || !user) return [];
    
    // Super admin has all permissions
    if (user.roles?.some(role => role.code === 'super_admin')) {
      return ['*'];
    }

    const perms = new Set(user.permissions || []);
    
    user.roles?.forEach(role => {
      role.permissions?.forEach(p => {
        perms.add(p.code);
      });
    });

    return Array.from(perms);
  }, [user, isAuthenticated]);

  const isSuperAdmin = user?.roles?.some(role => role.code === 'super_admin') || false;

  return { permissions: allPermissions, isSuperAdmin };
};

/**
 * Permission gate component wrapper
 */
export const usePermissionGate = (requiredPermission, fallback = null) => {
  const { hasPermission, isLoading } = usePermission(requiredPermission);
  
  return {
    canAccess: hasPermission,
    isChecking: isLoading,
    Gate: ({ children }) => {
      if (isLoading) return null;
      if (!hasPermission) return fallback;
      return children;
    }
  };
};

/**
 * Get user roles
 */
export const useRoles = () => {
  const { user, isAuthenticated } = useAuth();
  
  const roles = useMemo(() => {
    if (!isAuthenticated || !user) return [];
    return user.roles || [];
  }, [user, isAuthenticated]);

  const hasRole = useCallback((roleCode) => {
    return roles.some(role => role.code === roleCode);
  }, [roles]);

  const hasAnyRole = useCallback((roleCodes) => {
    return roleCodes.some(code => roles.some(role => role.code === code));
  }, [roles]);

  return { roles, hasRole, hasAnyRole };
};

export default {
  usePermission,
  usePermissions,
  useAllPermissions,
  usePermissionGate,
  useRoles
};

