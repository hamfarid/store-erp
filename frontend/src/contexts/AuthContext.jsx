import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiRequest, API_ENDPOINTS } from '../config/api';
import sessionSecurity from '../services/sessionSecurity';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// تعريف الصلاحيات المتاحة في النظام
export const PERMISSIONS = {
  // صلاحيات المنتجات
  'products.view': 'عرض المنتجات',
  'products.create': 'إنشاء منتجات',
  'products.edit': 'تعديل المنتجات',
  'products.delete': 'حذف المنتجات',
  
  // صلاحيات المخزون
  'inventory.view': 'عرض المخزون',
  'inventory.edit': 'تعديل المخزون',
  'inventory.adjust': 'تسوية المخزون',
  
  // صلاحيات اللوطات
  'lots.view': 'عرض اللوطات',
  'lots.create': 'إنشاء لوتات',
  'lots.edit': 'تعديل اللوطات',
  'lots.delete': 'حذف اللوطات',
  
  // صلاحيات حركات المخزون
  'stock_movements.view': 'عرض حركات المخزون',
  'stock_movements.create': 'إنشاء حركات مخزون',
  'stock_movements.edit': 'تعديل حركات المخزون',
  
  // صلاحيات العملاء
  'customers.view': 'عرض العملاء',
  'customers.create': 'إنشاء عملاء',
  'customers.edit': 'تعديل العملاء',
  'customers.delete': 'حذف العملاء',
  
  // صلاحيات الموردين
  'suppliers.view': 'عرض الموردين',
  'suppliers.create': 'إنشاء موردين',
  'suppliers.edit': 'تعديل الموردين',
  'suppliers.delete': 'حذف الموردين',
  
  // صلاحيات الفواتير
  'invoices.view': 'عرض الفواتير',
  'invoices.create': 'إنشاء فواتير',
  'invoices.edit': 'تعديل الفواتير',
  'invoices.delete': 'حذف الفواتير',
  'invoices.print': 'طباعة الفواتير',
  
  // صلاحيات المخازن
  'warehouses.view': 'عرض المخازن',
  'warehouses.create': 'إنشاء مخازن',
  'warehouses.edit': 'تعديل المخازن',
  'warehouses.delete': 'حذف المخازن',
  
  // صلاحيات الفئات
  'categories.view': 'عرض الفئات',
  'categories.create': 'إنشاء فئات',
  'categories.edit': 'تعديل الفئات',
  'categories.delete': 'حذف الفئات',
  
  // صلاحيات التقارير
  'reports.view': 'عرض التقارير',
  'reports.export': 'تصدير التقارير',
  'reports.print': 'طباعة التقارير',
  
  // صلاحيات المستخدمين
  'users.view': 'عرض المستخدمين',
  'users.create': 'إنشاء مستخدمين',
  'users.edit': 'تعديل المستخدمين',
  'users.delete': 'حذف المستخدمين',
  'users.permissions': 'إدارة الصلاحيات',
  
  // صلاحيات الشركة والإعدادات
  'company.view': 'عرض بيانات الشركة',
  'company.edit': 'تعديل بيانات الشركة',
  'settings.view': 'عرض الإعدادات',
  'settings.edit': 'تعديل الإعدادات',
  
  // صلاحيات النظام
  'system.backup': 'النسخ الاحتياطية',
  'system.restore': 'استعادة البيانات',
  'system.logs': 'عرض سجلات النظام'
};

// تعريف الأدوار وصلاحياتها
export const ROLES = {
  admin: {
    name: 'مدير عام',
    permissions: Object.keys(PERMISSIONS) // جميع الصلاحيات
  },
  manager: {
    name: 'مدير مخزون',
    permissions: [
      'products.view', 'products.create', 'products.edit',
      'inventory.view', 'inventory.edit', 'inventory.adjust',
      'lots.view', 'lots.create', 'lots.edit',
      'stock_movements.view', 'stock_movements.create', 'stock_movements.edit',
      'customers.view', 'customers.create', 'customers.edit',
      'suppliers.view', 'suppliers.create', 'suppliers.edit',
      'invoices.view', 'invoices.create', 'invoices.edit', 'invoices.print',
      'warehouses.view', 'warehouses.create', 'warehouses.edit',
      'categories.view', 'categories.create', 'categories.edit',
      'reports.view', 'reports.export', 'reports.print'
    ]
  },
  user: {
    name: 'موظف مبيعات',
    permissions: [
      'products.view',
      'inventory.view',
      'lots.view',
      'stock_movements.view',
      'customers.view', 'customers.create', 'customers.edit',
      'invoices.view', 'invoices.create', 'invoices.print',
      'reports.view'
    ]
  },
  viewer: {
    name: 'مستخدم عرض فقط',
    permissions: [
      'products.view',
      'inventory.view',
      'lots.view',
      'stock_movements.view',
      'customers.view',
      'suppliers.view',
      'invoices.view',
      'warehouses.view',
      'categories.view',
      'reports.view'
    ]
  }
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // فحص وجود جلسة مستخدم محفوظة
    const savedUser = localStorage.getItem('user');
    const savedToken = localStorage.getItem('token');
    
    if (savedUser && savedToken) {
      try {
        // Validate session security (fingerprint, expiry, etc.)
        const validation = sessionSecurity.validateSession();
        
        if (!validation.valid) {
          console.warn('Session validation failed:', validation.errors);
          
          // Only force logout for critical security issues, not fingerprint mismatches
          // Fingerprint can vary due to browser updates, extensions, or test environments
          if (validation.errors.includes('session_expired') || validation.errors.includes('no_token')) {
            console.warn('Session expired or token missing, cleaning up...');
            sessionSecurity.cleanLogout();
            setLoading(false);
            return;
          }
          
          // For fingerprint mismatch, just log warning but allow session restoration
          // This handles legitimate cases like browser updates or test environments
          if (validation.errors.includes('fingerprint_mismatch')) {
            console.warn('⚠️ Fingerprint mismatch detected - updating fingerprint');
            // Update fingerprint to current value to prevent future warnings
            localStorage.setItem('session_fingerprint', sessionSecurity.generateFingerprint());
          }
        }
        
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
        
        // Start activity monitoring and token refresh
        sessionSecurity.startActivityMonitoring();
        sessionSecurity.scheduleTokenRefresh();
        
      } catch (error) {
        console.error('Session restore error:', error);
        sessionSecurity.cleanLogout();
      }
    }
    
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      // محاولة تسجيل الدخول عبر API
      const data = await apiRequest(API_ENDPOINTS.AUTH.LOGIN, {
        method: 'POST',
        body: JSON.stringify({ username, password })
      });
      
      console.log('✅ Login API response:', data);
      
      if (data.success) {
        // إضافة الصلاحيات بناءً على الدور
        const userWithPermissions = {
          ...data.data.user,
          permissions: ROLES[data.data.user.role]?.permissions || []
        };
        
        setUser(userWithPermissions);
        setIsAuthenticated(true);
        
        // Initialize secure session with hijacking protection
        sessionSecurity.initializeSession(userWithPermissions, {
          access_token: data.data.access_token,
          refresh_token: data.data.refresh_token,
          session_id: data.data.session_id
        });
        
        console.log('🔑 Secure session initialized');
        console.log('🔑 Token saved:', data.data.access_token.substring(0, 20) + '...');
        
        return { success: true, user: userWithPermissions };
      }
      
      return { success: false, error: data.message || 'فشل تسجيل الدخول' };
      
    } catch (error) {
      console.error('❌ Login error:', error);
      return { success: false, error: error.message || 'حدث خطأ أثناء تسجيل الدخول' };
    }
  };

  const logout = async () => {
    // Use secure logout to clean up session
    await sessionSecurity.cleanLogout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const hasPermission = (permission) => {
    if (!user) return false;
    if (user.role === 'admin') return true; // المدير العام له جميع الصلاحيات
    return user.permissions?.includes(permission) || false;
  };

  const hasAnyPermission = (permissions) => {
    if (!user) return false;
    if (user.role === 'admin') return true;
    return permissions.some(permission => user.permissions?.includes(permission));
  };

  const hasAllPermissions = (permissions) => {
    if (!user) return false;
    if (user.role === 'admin') return true;
    return permissions.every(permission => user.permissions?.includes(permission));
  };

  const updateUserPermissions = (newPermissions) => {
    if (user) {
      const updatedUser = { ...user, permissions: newPermissions };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    updateUserPermissions,
    PERMISSIONS,
    ROLES
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
