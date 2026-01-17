import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// Import Components
import UnifiedDashboard from './UnifiedDashboard';
import UnifiedProductsManager from './UnifiedProductsManager';
import SimpleLogin from './SimpleLogin';

// Layout Component
import UnifiedLayout from './UnifiedLayout';

// Protected Route Component
const ProtectedRoute = ({ children, permission = null }) => {
  const { user, hasPermission } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (permission && !hasPermission(permission)) {
    return (
      <div className="min-h-screen bg-muted/50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-4" dir="rtl">
            غير مصرح لك بالوصول
          </h2>
          <p className="text-muted-foreground" dir="rtl">
            ليس لديك الصلاحية المطلوبة للوصول إلى هذه الصفحة
          </p>
        </div>
      </div>
    );
  }

  return children;
};

// Public Route Component (for login page)
const PublicRoute = ({ children }) => {
  const { user } = useAuth();

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Coming Soon Component
const ComingSoon = ({ title = "قريباً" }) => (
  <div className="min-h-screen bg-muted/50 flex items-center justify-center">
    <div className="text-center">
      <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center">
          <span className="text-white text-xl">🚧</span>
        </div>
      </div>
      <h2 className="text-3xl font-bold text-foreground mb-4" dir="rtl">
        {title}
      </h2>
      <p className="text-muted-foreground mb-6" dir="rtl">
        هذه الصفحة قيد التطوير وستكون متاحة قريباً
      </p>
      <button
        onClick={() => window.history.back()}
        className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700"
      >
        العودة للخلف
      </button>
    </div>
  </div>
);

const UnifiedRouter = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route 
        path="/login" 
        element={
          <PublicRoute>
            <SimpleLogin />
          </PublicRoute>
        } 
      />

      {/* Protected Routes with Layout */}
      <Route 
        path="/*" 
        element={
          <ProtectedRoute>
            <UnifiedLayout>
              <Routes>
                {/* Dashboard */}
                <Route path="/dashboard" element={<UnifiedDashboard />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />

                {/* Products Management */}
                <Route 
                  path="/products" 
                  element={
                    <ProtectedRoute permission="products.view">
                      <UnifiedProductsManager />
                    </ProtectedRoute>
                  } 
                />

                {/* Customers Management */}
                <Route 
                  path="/customers" 
                  element={
                    <ProtectedRoute permission="customers.view">
                      <ComingSoon title="إدارة العملاء" />
                    </ProtectedRoute>
                  } 
                />

                {/* Suppliers Management */}
                <Route 
                  path="/suppliers" 
                  element={
                    <ProtectedRoute permission="suppliers.view">
                      <ComingSoon title="إدارة الموردين" />
                    </ProtectedRoute>
                  } 
                />

                {/* Warehouses Management */}
                <Route 
                  path="/warehouses" 
                  element={
                    <ProtectedRoute permission="warehouses.view">
                      <ComingSoon title="إدارة المخازن" />
                    </ProtectedRoute>
                  } 
                />

                {/* Inventory Management */}
                <Route 
                  path="/inventory" 
                  element={
                    <ProtectedRoute permission="inventory.view">
                      <ComingSoon title="إدارة المخزون" />
                    </ProtectedRoute>
                  } 
                />

                {/* Stock Movements */}
                <Route 
                  path="/stock-movements" 
                  element={
                    <ProtectedRoute permission="stock_movements.view">
                      <ComingSoon title="حركات المخزون" />
                    </ProtectedRoute>
                  } 
                />

                {/* Invoices */}
                <Route 
                  path="/invoices" 
                  element={
                    <ProtectedRoute permission="invoices.view">
                      <ComingSoon title="إدارة الفواتير" />
                    </ProtectedRoute>
                  } 
                />

                {/* Sales Invoices */}
                <Route 
                  path="/invoices/sales" 
                  element={
                    <ProtectedRoute permission="invoices.view">
                      <ComingSoon title="فواتير المبيعات" />
                    </ProtectedRoute>
                  } 
                />

                {/* Purchase Invoices */}
                <Route 
                  path="/invoices/purchases" 
                  element={
                    <ProtectedRoute permission="invoices.view">
                      <ComingSoon title="فواتير المشتريات" />
                    </ProtectedRoute>
                  } 
                />

                {/* Reports */}
                <Route 
                  path="/reports" 
                  element={
                    <ProtectedRoute permission="reports.view">
                      <ComingSoon title="التقارير" />
                    </ProtectedRoute>
                  } 
                />

                {/* Categories */}
                <Route 
                  path="/categories" 
                  element={
                    <ProtectedRoute permission="categories.view">
                      <ComingSoon title="إدارة الفئات" />
                    </ProtectedRoute>
                  } 
                />

                {/* Users Management */}
                <Route 
                  path="/users" 
                  element={
                    <ProtectedRoute permission="users.view">
                      <ComingSoon title="إدارة المستخدمين" />
                    </ProtectedRoute>
                  } 
                />

                {/* Settings */}
                <Route 
                  path="/settings" 
                  element={
                    <ProtectedRoute permission="settings.view">
                      <ComingSoon title="الإعدادات" />
                    </ProtectedRoute>
                  } 
                />

                {/* Company Settings */}
                <Route 
                  path="/settings/company" 
                  element={
                    <ProtectedRoute permission="company.view">
                      <ComingSoon title="إعدادات الشركة" />
                    </ProtectedRoute>
                  } 
                />

                {/* System Settings */}
                <Route 
                  path="/settings/system" 
                  element={
                    <ProtectedRoute permission="settings.edit">
                      <ComingSoon title="إعدادات النظام" />
                    </ProtectedRoute>
                  } 
                />

                {/* Profile */}
                <Route 
                  path="/profile" 
                  element={<ComingSoon title="الملف الشخصي" />} 
                />

                {/* 404 Page */}
                <Route 
                  path="*" 
                  element={
                    <div className="min-h-screen bg-muted/50 flex items-center justify-center">
                      <div className="text-center">
                        <h1 className="text-6xl font-bold text-gray-400 mb-4">404</h1>
                        <h2 className="text-2xl font-bold text-foreground mb-4" dir="rtl">
                          الصفحة غير موجودة
                        </h2>
                        <p className="text-muted-foreground mb-6" dir="rtl">
                          الصفحة التي تبحث عنها غير موجودة أو تم نقلها
                        </p>
                        <button
                          onClick={() => window.location.href = '/dashboard'}
                          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700"
                        >
                          العودة للوحة التحكم
                        </button>
                      </div>
                    </div>
                  } 
                />
              </Routes>
            </UnifiedLayout>
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
};

export default UnifiedRouter;

