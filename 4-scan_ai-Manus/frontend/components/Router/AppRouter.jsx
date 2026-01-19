/**
 * AppRouter.jsx - Main Application Router with PageWrapper
 * 
 * Features:
 * - Each route wrapped with ErrorBoundary via PageWrapper
 * - Lazy loading for code splitting
 * - Protected routes for authenticated users
 * - Public routes for guests
 * - Complete error page routing (401-506)
 * - Arabic RTL support
 * 
 * Version: 3.0.0
 * Updated: 2025-12-05
 */

import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PageWrapper from '../PageWrapper/PageWrapper';

// Loading Spinner for initial load
const InitialLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-900 via-green-800 to-emerald-900">
    <div className="text-center">
      <div className="inline-flex items-center justify-center w-20 h-20 bg-green-500 rounded-full mb-4 shadow-lg animate-pulse">
        <span className="text-4xl">🌱</span>
      </div>
      <p className="text-white text-lg">جاري تحميل Gaara Scan AI...</p>
    </div>
  </div>
);

// ============================================
// Lazy Load - Authentication Pages
// ============================================
const Login = lazy(() => import('../../pages/Login'));
const Register = lazy(() => import('../../pages/Register'));
const ForgotPassword = lazy(() => import('../../pages/ForgotPassword'));
const ResetPassword = lazy(() => import('../../pages/ResetPassword'));

// ============================================
// Lazy Load - Main Pages
// ============================================
const Dashboard = lazy(() => import('../../pages/Dashboard'));
const Farms = lazy(() => import('../../pages/Farms'));
const Diagnosis = lazy(() => import('../../pages/Diagnosis'));
const Diseases = lazy(() => import('../../pages/Diseases'));
const Crops = lazy(() => import('../../pages/Crops'));
const Sensors = lazy(() => import('../../pages/Sensors'));
const Equipment = lazy(() => import('../../pages/Equipment'));
const Inventory = lazy(() => import('../../pages/Inventory'));
const Breeding = lazy(() => import('../../pages/Breeding'));
const Reports = lazy(() => import('../../pages/Reports'));
const Analytics = lazy(() => import('../../pages/Analytics'));
const Settings = lazy(() => import('../../pages/Settings'));
const Users = lazy(() => import('../../pages/Users'));
const Profile = lazy(() => import('../../pages/Profile'));
const Companies = lazy(() => import('../../pages/Companies'));
const SetupWizard = lazy(() => import('../../pages/SetupWizard'));

// ============================================
// Lazy Load - Error Pages
// ============================================
const Error401 = lazy(() => import('../../pages/errors/Error401'));
const Error402 = lazy(() => import('../../pages/errors/Error402'));
const Error403 = lazy(() => import('../../pages/errors/Error403'));
const Error404 = lazy(() => import('../../pages/errors/Error404'));
const Error405 = lazy(() => import('../../pages/errors/Error405'));
const Error406 = lazy(() => import('../../pages/errors/Error406'));
const Error500 = lazy(() => import('../../pages/errors/Error500'));
const Error501 = lazy(() => import('../../pages/errors/Error501'));
const Error502 = lazy(() => import('../../pages/errors/Error502'));
const Error503 = lazy(() => import('../../pages/errors/Error503'));
const Error504 = lazy(() => import('../../pages/errors/Error504'));
const Error505 = lazy(() => import('../../pages/errors/Error505'));
const Error506 = lazy(() => import('../../pages/errors/Error506'));

// ============================================
// Route Configuration
// ============================================
const routeConfig = {
  // Public Routes (No authentication required)
  public: [
    { path: '/login', element: Login, title: 'تسجيل الدخول' },
    { path: '/register', element: Register, title: 'إنشاء حساب' },
    { path: '/forgot-password', element: ForgotPassword, title: 'نسيت كلمة المرور' },
    { path: '/reset-password', element: ResetPassword, title: 'إعادة تعيين كلمة المرور' },
  ],
  
  // Protected Routes (Authentication required)
  protected: [
    { path: '/dashboard', element: Dashboard, title: 'لوحة التحكم' },
    { path: '/farms', element: Farms, title: 'المزارع' },
    { path: '/diagnosis', element: Diagnosis, title: 'التشخيص' },
    { path: '/diseases', element: Diseases, title: 'الأمراض' },
    { path: '/crops', element: Crops, title: 'المحاصيل' },
    { path: '/sensors', element: Sensors, title: 'أجهزة الاستشعار' },
    { path: '/equipment', element: Equipment, title: 'المعدات' },
    { path: '/inventory', element: Inventory, title: 'المخزون' },
    { path: '/breeding', element: Breeding, title: 'التهجين' },
    { path: '/reports', element: Reports, title: 'التقارير' },
    { path: '/analytics', element: Analytics, title: 'التحليلات' },
    { path: '/settings', element: Settings, title: 'الإعدادات' },
    { path: '/users', element: Users, title: 'المستخدمين' },
    { path: '/profile', element: Profile, title: 'الملف الشخصي' },
    { path: '/companies', element: Companies, title: 'الشركات' },
    { path: '/setup', element: SetupWizard, title: 'معالج الإعداد' },
  ],
  
  // Error Pages
  errors: [
    { path: '/401', element: Error401, title: 'غير مصرح - 401' },
    { path: '/402', element: Error402, title: 'الدفع مطلوب - 402' },
    { path: '/403', element: Error403, title: 'ممنوع الوصول - 403' },
    { path: '/404', element: Error404, title: 'غير موجود - 404' },
    { path: '/405', element: Error405, title: 'غير مسموح - 405' },
    { path: '/406', element: Error406, title: 'غير مقبول - 406' },
    { path: '/500', element: Error500, title: 'خطأ الخادم - 500' },
    { path: '/501', element: Error501, title: 'غير منفذ - 501' },
    { path: '/502', element: Error502, title: 'بوابة خاطئة - 502' },
    { path: '/503', element: Error503, title: 'غير متاح - 503' },
    { path: '/504', element: Error504, title: 'انتهت المهلة - 504' },
    { path: '/505', element: Error505, title: 'HTTP غير مدعوم - 505' },
    { path: '/506', element: Error506, title: 'تفاوض - 506' },
  ],
};

/**
 * Check if user is authenticated
 */
const isAuthenticated = () => {
  const token = localStorage.getItem('access_token');
  return !!token;
};

/**
 * Protected Route Component
 */
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

/**
 * Public Route Component (redirect to dashboard if already logged in)
 */
const PublicRoute = ({ children }) => {
  if (isAuthenticated()) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

/**
 * Render route with PageWrapper
 */
const renderRoute = (route, isProtected = false, isPublic = false) => {
  const RouteComponent = route.element;
  
  let element = (
    <PageWrapper title={route.title}>
      <RouteComponent />
    </PageWrapper>
  );

  if (isProtected) {
    element = <ProtectedRoute>{element}</ProtectedRoute>;
  } else if (isPublic) {
    element = <PublicRoute>{element}</PublicRoute>;
  }

  return (
    <Route
      key={route.path}
      path={route.path}
      element={element}
    />
  );
};

/**
 * Main App Router Component
 */
const AppRouter = () => {
  return (
    <Router>
      <Suspense fallback={<InitialLoader />}>
        <Routes>
          {/* Root redirect */}
          <Route
            path="/"
            element={
              isAuthenticated() 
                ? <Navigate to="/dashboard" replace /> 
                : <Navigate to="/login" replace />
            }
          />

          {/* Public Routes */}
          {routeConfig.public.map(route => renderRoute(route, false, true))}

          {/* Protected Routes */}
          {routeConfig.protected.map(route => renderRoute(route, true, false))}

          {/* Error Pages (accessible to all) */}
          {routeConfig.errors.map(route => renderRoute(route, false, false))}

          {/* Catch-all 404 */}
          <Route
            path="*"
            element={
              <PageWrapper title="صفحة غير موجودة">
                <Error404 />
              </PageWrapper>
            }
          />
        </Routes>
      </Suspense>
    </Router>
  );
};

export default AppRouter;

// Export route configuration for use elsewhere
export { routeConfig, isAuthenticated, ProtectedRoute, PublicRoute };
