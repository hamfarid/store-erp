/**
 * App.jsx - Main Application Component
 * 
 * Features:
 * - Error Boundary with PageWrapper for each route
 * - Authentication context
 * - Theme and language support (RTL Arabic)
 * - React Query for data fetching
 * - Toast notifications
 * 
 * Version: 3.0.0
 * Updated: 2025-12-05
 */

import React, { useState, useEffect, createContext, useContext, Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';

// Custom Router wrapper with v7 future flags to suppress warnings
const Router = ({ children }) => (
  <BrowserRouter
    future={{
      v7_startTransition: true,
      v7_relativeSplatPath: true,
    }}
  >
    {children}
  </BrowserRouter>
);
import { Toaster } from 'react-hot-toast';

// Core Components
import PageWrapper from './components/PageWrapper/PageWrapper';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary';
import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import Footer from './components/Layout/Footer';

// Services
import ApiService from './services/ApiService';

// Styles
import './App.css';
import './index.css';

// ============================================
// Lazy Load - Authentication Pages
// ============================================
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'));
const ResetPassword = lazy(() => import('./pages/ResetPassword'));

// ============================================
// Lazy Load - Main Pages
// ============================================
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Farms = lazy(() => import('./pages/Farms'));
const Diagnosis = lazy(() => import('./pages/Diagnosis'));
const Diseases = lazy(() => import('./pages/Diseases'));
const Crops = lazy(() => import('./pages/Crops'));
const Sensors = lazy(() => import('./pages/Sensors'));
const Equipment = lazy(() => import('./pages/Equipment'));
const Inventory = lazy(() => import('./pages/Inventory'));
const Breeding = lazy(() => import('./pages/Breeding'));
const Reports = lazy(() => import('./pages/Reports'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Settings = lazy(() => import('./pages/Settings'));
const Users = lazy(() => import('./pages/Users'));
const Profile = lazy(() => import('./pages/Profile'));
const Companies = lazy(() => import('./pages/Companies'));
const SetupWizard = lazy(() => import('./pages/SetupWizard'));

// ============================================
// Lazy Load - Error Pages
// ============================================
const Error401 = lazy(() => import('./pages/errors/Error401'));
const Error402 = lazy(() => import('./pages/errors/Error402'));
const Error403 = lazy(() => import('./pages/errors/Error403'));
const Error404 = lazy(() => import('./pages/errors/Error404'));
const Error405 = lazy(() => import('./pages/errors/Error405'));
const Error406 = lazy(() => import('./pages/errors/Error406'));
const Error500 = lazy(() => import('./pages/errors/Error500'));
const Error501 = lazy(() => import('./pages/errors/Error501'));
const Error502 = lazy(() => import('./pages/errors/Error502'));
const Error503 = lazy(() => import('./pages/errors/Error503'));
const Error504 = lazy(() => import('./pages/errors/Error504'));
const Error505 = lazy(() => import('./pages/errors/Error505'));
const Error506 = lazy(() => import('./pages/errors/Error506'));

// ============================================
// Loading Spinner
// ============================================
const LoadingSpinner = () => (
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
// Auth Context
// ============================================
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = () => {
    try {
      const token = localStorage.getItem('access_token');
      const userData = localStorage.getItem('user');
      
      if (token && userData) {
        setUser(JSON.parse(userData));
        setIsAuthenticated(true);
        ApiService.setToken(token);
      }
    } catch (error) {
      console.error('Auth check error:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      // TODO: Replace with actual API call
      const mockUser = {
        id: 1,
        username: credentials.username || credentials.email,
        email: credentials.email || `${credentials.username}@gaara-ai.com`,
        full_name: 'مستخدم Gaara AI',
        role: 'admin'
      };
      const mockToken = 'mock-token-' + Date.now();
      
      localStorage.setItem('access_token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      ApiService.setToken(mockToken);
      setUser(mockUser);
      setIsAuthenticated(true);
      
      return { success: true, user: mockUser };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      // TODO: Replace with actual API call
      return { success: true };
    } catch (error) {
      console.error('Register error:', error);
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    ApiService.removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, logout, register, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

// ============================================
// App Context (Theme, Language, Sidebar)
// ============================================
const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('ar');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedLanguage = localStorage.getItem('language') || 'ar';
    
    setTheme(savedTheme);
    setLanguage(savedLanguage);
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('dir', savedLanguage === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', savedLanguage);
    
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const changeLanguage = (lang) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
  };

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <AppContext.Provider value={{ 
      theme, 
      language, 
      sidebarOpen, 
      toggleTheme, 
      changeLanguage, 
      toggleSidebar 
    }}>
      {children}
    </AppContext.Provider>
  );
};

// ============================================
// Protected Route
// ============================================
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  return children;
};

// ============================================
// Public Route
// ============================================
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// ============================================
// Layout with Sidebar
// ============================================
const MainLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const { theme, language, sidebarOpen, toggleTheme, changeLanguage, toggleSidebar } = useApp();
  const location = useLocation();
  
  const noLayoutPaths = ['/login', '/register', '/forgot-password', '/reset-password'];
  const isNoLayout = noLayoutPaths.some(path => location.pathname.startsWith(path));
  const isErrorPage = /^\/(4|5)\d{2}$/.test(location.pathname);

  if (isNoLayout || isErrorPage) {
    return children;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Navbar 
        user={user}
        theme={theme}
        language={language}
        sidebarOpen={sidebarOpen}
        onToggleTheme={toggleTheme}
        onToggleSidebar={toggleSidebar}
        onChangeLanguage={changeLanguage}
        onLogout={logout}
      />
      <div className="flex flex-1">
        <Sidebar isOpen={sidebarOpen} language={language} />
        <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'mr-64' : 'mr-0'}`}>
          <div className="p-6 min-h-[calc(100vh-8rem)]">
            {children}
          </div>
        </main>
      </div>
      <Footer language={language} />
    </div>
  );
};

// ============================================
// Wrap Route with PageWrapper
// ============================================
const WrapRoute = ({ element: Element, title, isProtected = false, isPublic = false }) => {
  let content = (
    <PageWrapper title={title}>
      <Element />
    </PageWrapper>
  );

  if (isProtected) {
    content = <ProtectedRoute>{content}</ProtectedRoute>;
  } else if (isPublic) {
    content = <PublicRoute>{content}</PublicRoute>;
  }

  return content;
};

// ============================================
// Main App Component
// ============================================
const App = () => {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppProvider>
          <Router>
            <Suspense fallback={<LoadingSpinner />}>
              <MainLayout>
                <Routes>
                  {/* Root Redirect */}
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />

                  {/* Public Routes */}
                  <Route path="/login" element={<WrapRoute element={Login} title="تسجيل الدخول" isPublic />} />
                  <Route path="/register" element={<WrapRoute element={Register} title="إنشاء حساب" isPublic />} />
                  <Route path="/forgot-password" element={<WrapRoute element={ForgotPassword} title="نسيت كلمة المرور" isPublic />} />
                  <Route path="/reset-password" element={<WrapRoute element={ResetPassword} title="إعادة تعيين كلمة المرور" isPublic />} />
                  <Route path="/reset-password/:token" element={<WrapRoute element={ResetPassword} title="إعادة تعيين كلمة المرور" isPublic />} />

                  {/* Protected Routes */}
                  <Route path="/dashboard" element={<WrapRoute element={Dashboard} title="لوحة التحكم" isProtected />} />
                  <Route path="/farms/*" element={<WrapRoute element={Farms} title="المزارع" isProtected />} />
                  <Route path="/diagnosis/*" element={<WrapRoute element={Diagnosis} title="التشخيص" isProtected />} />
                  <Route path="/diseases/*" element={<WrapRoute element={Diseases} title="الأمراض" isProtected />} />
                  <Route path="/crops/*" element={<WrapRoute element={Crops} title="المحاصيل" isProtected />} />
                  <Route path="/sensors/*" element={<WrapRoute element={Sensors} title="أجهزة الاستشعار" isProtected />} />
                  <Route path="/equipment/*" element={<WrapRoute element={Equipment} title="المعدات" isProtected />} />
                  <Route path="/inventory/*" element={<WrapRoute element={Inventory} title="المخزون" isProtected />} />
                  <Route path="/breeding/*" element={<WrapRoute element={Breeding} title="التهجين" isProtected />} />
                  <Route path="/reports/*" element={<WrapRoute element={Reports} title="التقارير" isProtected />} />
                  <Route path="/analytics/*" element={<WrapRoute element={Analytics} title="التحليلات" isProtected />} />
                  <Route path="/settings/*" element={<WrapRoute element={Settings} title="الإعدادات" isProtected />} />
                  <Route path="/users/*" element={<WrapRoute element={Users} title="المستخدمين" isProtected />} />
                  <Route path="/profile" element={<WrapRoute element={Profile} title="الملف الشخصي" isProtected />} />
                  <Route path="/companies/*" element={<WrapRoute element={Companies} title="الشركات" isProtected />} />
                  <Route path="/setup" element={<WrapRoute element={SetupWizard} title="معالج الإعداد" isProtected />} />

                  {/* Error Pages - 4xx Client Errors */}
                  <Route path="/401" element={<WrapRoute element={Error401} title="غير مصرح - 401" />} />
                  <Route path="/402" element={<WrapRoute element={Error402} title="الدفع مطلوب - 402" />} />
                  <Route path="/403" element={<WrapRoute element={Error403} title="ممنوع الوصول - 403" />} />
                  <Route path="/404" element={<WrapRoute element={Error404} title="غير موجود - 404" />} />
                  <Route path="/405" element={<WrapRoute element={Error405} title="غير مسموح - 405" />} />
                  <Route path="/406" element={<WrapRoute element={Error406} title="غير مقبول - 406" />} />

                  {/* Error Pages - 5xx Server Errors */}
                  <Route path="/500" element={<WrapRoute element={Error500} title="خطأ الخادم - 500" />} />
                  <Route path="/501" element={<WrapRoute element={Error501} title="غير منفذ - 501" />} />
                  <Route path="/502" element={<WrapRoute element={Error502} title="بوابة خاطئة - 502" />} />
                  <Route path="/503" element={<WrapRoute element={Error503} title="غير متاح - 503" />} />
                  <Route path="/504" element={<WrapRoute element={Error504} title="انتهت المهلة - 504" />} />
                  <Route path="/505" element={<WrapRoute element={Error505} title="HTTP غير مدعوم - 505" />} />
                  <Route path="/506" element={<WrapRoute element={Error506} title="تفاوض - 506" />} />

                  {/* Catch-all 404 */}
                  <Route path="*" element={<WrapRoute element={Error404} title="صفحة غير موجودة" />} />
                </Routes>
              </MainLayout>
            </Suspense>
            
            {/* Toast Notifications */}
            <Toaster
              position="top-left"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#333',
                  color: '#fff',
                  fontFamily: 'Cairo, sans-serif',
                },
                success: {
                  style: {
                    background: '#10b981',
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: '#10b981',
                  },
                },
                error: {
                  style: {
                    background: '#ef4444',
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: '#ef4444',
                  },
                },
              }}
            />
          </Router>
        </AppProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
};

export default App;
export { AuthContext, AppContext };
