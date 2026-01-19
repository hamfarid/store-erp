import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

/**
 * ProtectedRoute Component
 * 
 * Wraps routes that require authentication.
 * Redirects to login page if user is not authenticated.
 * Preserves the intended destination for redirect after login.
 * 
 * Features:
 * - Token-based authentication check
 * - Redirect with return URL
 * - Permission checking (optional)
 */
const ProtectedRoute = ({ children, permissions = [], requiredRole = null }) => {
  const location = useLocation();

  // Check authentication
  const isAuthenticated = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return false;

    // Optional: Check token expiration
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.exp && payload.exp * 1000 < Date.now()) {
        // Token expired, clear storage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        return false;
      }
    } catch (e) {
      // Invalid token format
      return false;
    }

    return true;
  };

  // Check permissions
  const hasPermissions = () => {
    if (permissions.length === 0) return true;

    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const userPermissions = user.permissions || [];

    return permissions.every(perm => userPermissions.includes(perm));
  };

  // Check role
  const hasRole = () => {
    if (!requiredRole) return true;

    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return user.role === requiredRole;
  };

  // Not authenticated - redirect to login
  if (!isAuthenticated()) {
    return (
      <Navigate 
        to="/login" 
        state={{ from: location.pathname }} 
        replace 
      />
    );
  }

  // No permissions - redirect to 403
  if (!hasPermissions()) {
    return <Navigate to="/403" replace />;
  }

  // Wrong role - redirect to 403
  if (!hasRole()) {
    return <Navigate to="/403" replace />;
  }

  return children;
};

export default ProtectedRoute;

