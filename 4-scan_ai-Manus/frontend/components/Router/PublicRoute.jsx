import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

/**
 * PublicRoute Component
 * 
 * Wraps routes that should only be accessible to guests.
 * Redirects authenticated users to dashboard or their intended destination.
 * 
 * Features:
 * - Redirect authenticated users
 * - Preserve return URL from login redirect
 */
const PublicRoute = ({ children, redirectTo = '/dashboard' }) => {
  const location = useLocation();

  // Check if user is authenticated
  const isAuthenticated = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return false;

    // Optional: Check token expiration
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.exp && payload.exp * 1000 < Date.now()) {
        // Token expired
        return false;
      }
    } catch (e) {
      return false;
    }

    return true;
  };

  if (isAuthenticated()) {
    // If there's a return URL from login redirect, use it
    const from = location.state?.from || redirectTo;
    return <Navigate to={from} replace />;
  }

  return children;
};

export default PublicRoute;

