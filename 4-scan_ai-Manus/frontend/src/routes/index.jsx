/**
 * App Routes Configuration
 * =========================
 * 
 * Centralized routing configuration with protected routes,
 * lazy loading, and role-based access control.
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

// Loading component
const PageLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div className="text-center">
      <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center animate-pulse">
        <svg className="w-8 h-8 text-emerald-500 animate-spin" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>
      <p className="text-gray-500 dark:text-gray-400">جاري التحميل... / Loading...</p>
    </div>
  </div>
);

// Lazy load pages
const Dashboard = lazy(() => import('../../pages/Dashboard'));
const Diagnosis = lazy(() => import('../../pages/Diagnosis'));
const Diseases = lazy(() => import('../../pages/Diseases'));
const Farms = lazy(() => import('../../pages/Farms'));
const Crops = lazy(() => import('../../pages/Crops'));
const Equipment = lazy(() => import('../../pages/Equipment'));
const Inventory = lazy(() => import('../../pages/Inventory'));
const Sensors = lazy(() => import('../../pages/Sensors'));
const Breeding = lazy(() => import('../../pages/Breeding'));
const Analytics = lazy(() => import('../../pages/Analytics'));
const Reports = lazy(() => import('../../pages/Reports'));
const Users = lazy(() => import('../../pages/Users'));
const Companies = lazy(() => import('../../pages/Companies'));
const Settings = lazy(() => import('../../pages/Settings'));
const Profile = lazy(() => import('../../pages/Profile'));
const LearningDashboard = lazy(() => import('../../pages/LearningDashboard'));
const ImageCrawler = lazy(() => import('../../pages/ImageCrawler'));
const Login = lazy(() => import('../../pages/Login'));
const Register = lazy(() => import('../../pages/Register'));
const ForgotPassword = lazy(() => import('../../pages/ForgotPassword'));
const ResetPassword = lazy(() => import('../../pages/ResetPassword'));
const SetupWizard = lazy(() => import('../../pages/SetupWizard'));

// Error pages
const Error404 = lazy(() => import('../../pages/errors/Error404'));
const Error403 = lazy(() => import('../../pages/errors/Error403'));
const Error500 = lazy(() => import('../../pages/errors/Error500'));

/**
 * Protected Route Component
 */
const ProtectedRoute = ({ children, roles = [] }) => {
  const { user, loading, isAuthenticated } = useAuth();
  
  if (loading) {
    return <PageLoader />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  // Check role-based access
  if (roles.length > 0 && !roles.includes(user?.role)) {
    return <Navigate to="/403" replace />;
  }
  
  return children;
};

/**
 * Public Route Component (redirects to dashboard if authenticated)
 */
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <PageLoader />;
  }
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

/**
 * Route Definitions
 */
export const routeConfig = [
  // Dashboard
  {
    path: '/',
    element: Dashboard,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  // Diagnosis
  {
    path: '/diagnosis',
    element: Diagnosis,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  // Diseases
  {
    path: '/diseases',
    element: Diseases,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  // Farm Management
  {
    path: '/farms',
    element: Farms,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    path: '/crops',
    element: Crops,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    path: '/equipment',
    element: Equipment,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  {
    path: '/inventory',
    element: Inventory,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  {
    path: '/sensors',
    element: Sensors,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  {
    path: '/breeding',
    element: Breeding,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  // Analytics & Reports
  {
    path: '/analytics',
    element: Analytics,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  {
    path: '/reports',
    element: Reports,
    protected: true,
    roles: ['ADMIN', 'MANAGER']
  },
  // AI & ML
  {
    path: '/ml-dashboard',
    element: LearningDashboard,
    protected: true,
    roles: ['ADMIN']
  },
  {
    path: '/image-crawler',
    element: ImageCrawler,
    protected: true,
    roles: ['ADMIN']
  },
  // Administration
  {
    path: '/users',
    element: Users,
    protected: true,
    roles: ['ADMIN']
  },
  {
    path: '/companies',
    element: Companies,
    protected: true,
    roles: ['ADMIN']
  },
  // User
  {
    path: '/settings',
    element: Settings,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  {
    path: '/profile',
    element: Profile,
    protected: true,
    roles: ['ADMIN', 'MANAGER', 'USER']
  },
  // Auth
  {
    path: '/login',
    element: Login,
    public: true
  },
  {
    path: '/register',
    element: Register,
    public: true
  },
  {
    path: '/forgot-password',
    element: ForgotPassword,
    public: true
  },
  {
    path: '/reset-password',
    element: ResetPassword,
    public: true
  },
  {
    path: '/setup',
    element: SetupWizard,
    public: true
  },
  // Errors
  {
    path: '/403',
    element: Error403
  },
  {
    path: '/500',
    element: Error500
  },
  {
    path: '*',
    element: Error404
  }
];

// Import Layout
const MainLayout = lazy(() => import('../components/Layout/MainLayout'));

/**
 * App Routes Component
 */
const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        {/* Public routes (no layout) */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />
        <Route
          path="/forgot-password"
          element={
            <PublicRoute>
              <ForgotPassword />
            </PublicRoute>
          }
        />
        <Route
          path="/reset-password"
          element={
            <PublicRoute>
              <ResetPassword />
            </PublicRoute>
          }
        />
        <Route path="/setup" element={<SetupWizard />} />

        {/* Protected routes (with layout) */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="diagnosis" element={<Diagnosis />} />
          <Route path="diseases" element={<Diseases />} />
          <Route path="farms" element={<Farms />} />
          <Route path="crops" element={<Crops />} />
          <Route
            path="equipment"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Equipment />
              </ProtectedRoute>
            }
          />
          <Route
            path="inventory"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Inventory />
              </ProtectedRoute>
            }
          />
          <Route
            path="sensors"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Sensors />
              </ProtectedRoute>
            }
          />
          <Route
            path="breeding"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Breeding />
              </ProtectedRoute>
            }
          />
          <Route
            path="analytics"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Analytics />
              </ProtectedRoute>
            }
          />
          <Route
            path="reports"
            element={
              <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
                <Reports />
              </ProtectedRoute>
            }
          />
          <Route
            path="ml-dashboard"
            element={
              <ProtectedRoute roles={['ADMIN']}>
                <LearningDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="image-crawler"
            element={
              <ProtectedRoute roles={['ADMIN']}>
                <ImageCrawler />
              </ProtectedRoute>
            }
          />
          <Route
            path="users"
            element={
              <ProtectedRoute roles={['ADMIN']}>
                <Users />
              </ProtectedRoute>
            }
          />
          <Route
            path="companies"
            element={
              <ProtectedRoute roles={['ADMIN']}>
                <Companies />
              </ProtectedRoute>
            }
          />
          <Route path="settings" element={<Settings />} />
          <Route path="profile" element={<Profile />} />
        </Route>

        {/* Error pages */}
        <Route path="/403" element={<Error403 />} />
        <Route path="/500" element={<Error500 />} />
        <Route path="*" element={<Error404 />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
