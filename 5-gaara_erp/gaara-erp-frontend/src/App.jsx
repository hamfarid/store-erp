import { useState, useEffect, Suspense, lazy } from "react"
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Toaster } from "sonner"

// Layout Components
import Sidebar from "./components/Sidebar.jsx"
import Header from "./components/Header.jsx"
import LoadingScreen from "./components/LoadingScreen.jsx"
import { LoadingSpinner } from "./components/common"

// Lazy load pages for better performance
const LoginPage = lazy(() => import("./pages/auth/LoginPage.jsx").then(module => ({ default: module.LoginPage })))
const RegisterPage = lazy(() => import("./pages/auth/RegisterPage.jsx").then(module => ({ default: module.RegisterPage })))
const ForgotPasswordPage = lazy(() => import("./pages/auth/ForgotPasswordPage.jsx").then(module => ({ default: module.ForgotPasswordPage })))
const NotFoundPage = lazy(() => import("./pages/errors/NotFoundPage.jsx").then(module => ({ default: module.NotFoundPage })))
const ForbiddenPage = lazy(() => import("./pages/errors/ForbiddenPage.jsx").then(module => ({ default: module.ForbiddenPage })))
const ServerErrorPage = lazy(() => import("./pages/errors/ServerErrorPage.jsx").then(module => ({ default: module.ServerErrorPage })))
const Dashboard = lazy(() => import("./pages/Dashboard.jsx"))
const ProfilePage = lazy(() => import("./pages/ProfilePage.jsx"))
const SettingsPage = lazy(() => import("./pages/SettingsPage.jsx"))
const UserManagementPage = lazy(() => import("./pages/UserManagementPage.jsx"))

// Legacy Components (to be migrated to pages)
const InventoryManagement = lazy(() => import("./components/InventoryManagement.jsx"))
const IoTMonitoring = lazy(() => import("./components/IoTMonitoring.jsx"))
const AIAnalytics = lazy(() => import("./components/AIAnalytics.jsx"))
const SalesModule = lazy(() => import("./components/SalesModule.jsx"))
const AccountingModule = lazy(() => import("./components/AccountingModule.jsx"))

// Context Providers
import { AuthProvider, useAuth } from "./contexts/AuthContext.jsx"
import { ThemeProvider } from "./contexts/ThemeContext.jsx"
import { NotificationProvider } from "./contexts/NotificationContext.jsx"

// Common Components
import { ErrorBoundary } from "./components/common"

import "./App.css"

// Protected Route Component
const ProtectedRoute = ({ children, requiredRole, requiredPermission }) => {
  const { isAuthenticated, loading, user, hasRole, hasPermission } = useAuth()

  if (loading) {
    return <LoadingScreen />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Check role if required
  if (requiredRole && !hasRole(requiredRole)) {
    return <Navigate to="/403" replace />
  }

  // Check permission if required
  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <Navigate to="/403" replace />
  }

  return children
}

// Public Route Component (redirects to dashboard if already authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return <LoadingScreen />
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

// Main App Layout with Sidebar
const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isMobile, setIsMobile] = useState(false)
  const { user } = useAuth()

  // Handle responsive sidebar
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 1024
      setIsMobile(mobile)
      if (mobile) {
        setSidebarOpen(false)
      } else {
        setSidebarOpen(true)
      }
    }

    handleResize()
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800" dir="rtl">
      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            {/* Mobile overlay */}
            {isMobile && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setSidebarOpen(false)}
                className="fixed inset-0 z-40 bg-black/50 lg:hidden"
              />
            )}

            {/* Sidebar */}
            <motion.div
              initial={{ x: isMobile ? 280 : 0, opacity: isMobile ? 0 : 1 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 280, opacity: 0 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className={`
                fixed inset-y-0 right-0 z-50 w-64
                lg:relative lg:translate-x-0
              `}
            >
              <Sidebar onClose={() => setSidebarOpen(false)} />
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          user={user}
        />

        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-white dark:bg-slate-800 p-4 md:p-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="max-w-7xl mx-auto"
          >
            <Outlet />
          </motion.div>
        </main>
      </div>
    </div>
  )
}

// Main App Component
function App() {
  const [isInitializing, setIsInitializing] = useState(true)

  useEffect(() => {
    // Simulate app initialization (loading configs, etc.)
    const timer = setTimeout(() => {
      setIsInitializing(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  if (isInitializing) {
    return <LoadingScreen />
  }

  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <NotificationProvider>
            <Router>
              <div className="min-h-screen">
                <Routes>
                {/* Public Routes */}
                <Route
                  path="/login"
                  element={
                    <PublicRoute>
                      <LoginPage />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/register"
                  element={
                    <PublicRoute>
                      <RegisterPage />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/forgot-password"
                  element={
                    <PublicRoute>
                      <ForgotPasswordPage />
                    </PublicRoute>
                  }
                />

                {/* Error Pages */}
                <Route path="/404" element={<NotFoundPage />} />
                <Route path="/403" element={<ForbiddenPage />} />
                <Route path="/500" element={<ServerErrorPage />} />

                {/* Protected Routes with Layout */}
                <Route
                  element={
                    <ProtectedRoute>
                      <AppLayout />
                    </ProtectedRoute>
                  }
                >
                  {/* Dashboard */}
                  <Route index element={<Navigate to="/dashboard" replace />} />
                  <Route path="dashboard" element={<Dashboard />} />

                  {/* Profile & Settings */}
                  <Route path="profile" element={<ProfilePage />} />
                  <Route path="settings" element={<SettingsPage />} />

                  {/* Inventory Module */}
                  <Route path="inventory" element={<InventoryManagement />} />
                  <Route path="inventory/products" element={<InventoryManagement />} />
                  <Route path="inventory/warehouses" element={<InventoryManagement />} />
                  <Route path="inventory/movements" element={<InventoryManagement />} />
                  <Route path="inventory/reports" element={<InventoryManagement />} />

                  {/* IoT Module */}
                  <Route path="iot" element={<IoTMonitoring />} />
                  <Route path="iot/devices" element={<IoTMonitoring />} />
                  <Route path="iot/sensors" element={<IoTMonitoring />} />
                  <Route path="iot/alerts" element={<IoTMonitoring />} />
                  <Route path="iot/analytics" element={<IoTMonitoring />} />

                  {/* AI Analytics Module */}
                  <Route path="ai-analytics" element={<AIAnalytics />} />
                  <Route path="ai-analytics/predictions" element={<AIAnalytics />} />
                  <Route path="ai-analytics/data-analysis" element={<AIAnalytics />} />
                  <Route path="ai-analytics/smart-reports" element={<AIAnalytics />} />

                  {/* Sales Module */}
                  <Route path="sales" element={<SalesModule />} />
                  <Route path="sales/customers" element={<SalesModule />} />
                  <Route path="sales/orders" element={<SalesModule />} />
                  <Route path="sales/invoices" element={<SalesModule />} />
                  <Route path="sales/reports" element={<SalesModule />} />

                  {/* Accounting Module */}
                  <Route path="accounting" element={<AccountingModule />} />
                  <Route path="accounting/chart-of-accounts" element={<AccountingModule />} />
                  <Route path="accounting/journal-entries" element={<AccountingModule />} />
                  <Route path="accounting/financial-reports" element={<AccountingModule />} />

                  {/* User Management (Admin only) */}
                  <Route
                    path="users"
                    element={
                      <ProtectedRoute requiredRole="admin">
                        <UserManagementPage />
                      </ProtectedRoute>
                    }
                  />
                </Route>

                {/* Catch all - 404 */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>

              {/* Toast Notifications */}
              <Toaster
                position="top-center"
                richColors
                toastOptions={{
                  style: {
                    direction: "rtl",
                  },
                }}
              />
              </div>
            </Router>
          </NotificationProvider>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
