/**
 * useAuth Hook
 * ==============
 * 
 * Authentication hook for managing user state and auth operations.
 * 
 * Features:
 * - Login/Logout
 * - Register
 * - Token management
 * - User state
 * - Role checking
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import { useState, useEffect, useCallback, createContext, useContext } from 'react';
import apiService from '../../services/ApiService';

// Auth Context
const AuthContext = createContext(null);

/**
 * Auth Provider Component
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          setUser(JSON.parse(savedUser));
          
          // Verify token by fetching profile
          const profile = await apiService.getProfile();
          if (profile) {
            setUser(profile);
            localStorage.setItem('user', JSON.stringify(profile));
          }
        } catch (err) {
          console.error('Auth verification failed:', err);
          // Token invalid, clear auth
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          setUser(null);
        }
      }
      
      setLoading(false);
    };

    initAuth();
  }, []);

  // Listen for logout events
  useEffect(() => {
    const handleLogout = () => {
      setUser(null);
      setError(null);
    };

    window.addEventListener('auth:logout', handleLogout);
    return () => window.removeEventListener('auth:logout', handleLogout);
  }, []);

  /**
   * Login
   */
  const login = useCallback(async (credentials) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiService.login(credentials);
      
      if (response.access_token) {
        // Get user profile
        const profile = await apiService.getProfile();
        setUser(profile);
        localStorage.setItem('user', JSON.stringify(profile));
        
        return { success: true, user: profile };
      }
      
      throw new Error('Login failed');
    } catch (err) {
      const errorMessage = err.message || 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Register
   */
  const register = useCallback(async (userData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiService.register(userData);
      
      if (response.access_token) {
        apiService.setToken(response.access_token);
        if (response.refresh_token) {
          apiService.setRefreshToken(response.refresh_token);
        }
        
        const user = response.user || { email: userData.email, name: userData.name };
        setUser(user);
        localStorage.setItem('user', JSON.stringify(user));
        
        return { success: true, user };
      }
      
      return { success: true };
    } catch (err) {
      const errorMessage = err.message || 'Registration failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Logout
   */
  const logout = useCallback(async () => {
    try {
      await apiService.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
      setError(null);
    }
  }, []);

  /**
   * Update user
   */
  const updateUser = useCallback((updatedUser) => {
    setUser(prev => {
      const newUser = { ...prev, ...updatedUser };
      localStorage.setItem('user', JSON.stringify(newUser));
      return newUser;
    });
  }, []);

  /**
   * Check if user has role
   */
  const hasRole = useCallback((roles) => {
    if (!user) return false;
    if (typeof roles === 'string') return user.role === roles;
    return roles.includes(user.role);
  }, [user]);

  /**
   * Check if user has permission
   */
  const hasPermission = useCallback((permission) => {
    if (!user) return false;
    if (user.role === 'ADMIN') return true;
    return user.permissions?.includes(permission);
  }, [user]);

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    updateUser,
    hasRole,
    hasPermission,
    clearError: () => setError(null)
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * useAuth Hook
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default useAuth;
