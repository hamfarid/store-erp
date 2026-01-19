/**
 * AuthContext.jsx - Authentication Context Provider
 * 
 * This module is kept for backward compatibility.
 * The main AuthContext is now defined in App.jsx
 * 
 * Import from App.jsx:
 * import { useAuth } from '../App';
 * 
 * Or use this context for standalone usage.
 * 
 * Version: 3.0.0
 * Updated: 2025-12-05
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (token) {
        ApiService.setToken(token);
        const userData = localStorage.getItem('user');
        if (userData) {
          setUser(JSON.parse(userData));
        }
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('خطأ في فحص حالة المصادقة:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      // If credentials contains access_token, it's already logged in
      if (credentials.access_token) {
        const token = credentials.access_token;
        const userData = credentials.user || {
          id: 1,
          email: credentials.email,
          username: credentials.username || credentials.email
        };
        
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(userData));
        ApiService.setToken(token);
        setUser(userData);
        setIsAuthenticated(true);
        
        return { success: true, user: userData };
      }
      
      // Mock login for demonstration
      const mockToken = 'mock-token-' + Date.now();
      const mockUser = {
        id: 1,
        username: credentials.username || credentials.email,
        email: credentials.email || `${credentials.username}@gaara-ai.com`,
        full_name: 'مستخدم Gaara AI',
        role: 'user'
      };

      localStorage.setItem('access_token', mockToken);
      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      ApiService.setToken(mockToken);
      setUser(mockUser);
      setIsAuthenticated(true);

      return { success: true, user: mockUser };
    } catch (error) {
      console.error('خطأ في تسجيل الدخول:', error);
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      // TODO: Replace with actual API call
      return { success: true };
    } catch (error) {
      console.error('خطأ في التسجيل:', error);
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    ApiService.removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    register,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext };
export default AuthContext;
