import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import Layout from './Layout';
import Login from './Login';
import InteractiveDashboard from '../pages/InteractiveDashboard';
import { Error404, Error403, Error500, ErrorBoundary, ErrorTestPage } from './ErrorPages';
import { PermissionsProvider } from './ui/PermissionsGuard'

// Lazy loading للمكونات الثقيلة
const ProductManagement = lazy(() => import('./ProductManagement'));
const InventoryManagement = lazy(() => import('./InventoryManagement'));
const CustomerManagement = lazy(() => import('./CustomerManagement'));
const SupplierManagement = lazy(() => import('./SupplierManagement'));
const CategoryManagement = lazy(() => import('./CategoryManagement'));
const WarehouseManagement = lazy(() => import('./WarehouseManagement'));
const InvoiceManagementComplete = lazy(() => import('./InvoiceManagementComplete'));
const LotManagementAdvanced = lazy(() => import('./LotManagementAdvanced'));
const StockMovementsAdvanced = lazy(() => import('./StockMovementsAdvanced'));
const NotificationSystemAdvanced = lazy(() => import('./NotificationSystemAdvanced'));
const RagChat = lazy(() => import('./RagChat'));
const AdvancedReportsSystem = lazy(() => import('./AdvancedReportsSystem'));
const UserManagement = lazy(() => import('./UserManagementComplete'));
const AdminRoles = lazy(() => import('./AdminRoles'));
const CompanySettings = lazy(() => import('./CompanySettings'));
const SystemSettings = lazy(() => import('./SystemSettings'));
const SetupWizard = lazy(() => import('./SetupWizard'));
const PurchaseInvoiceManagement = lazy(() => import('./PurchaseInvoiceManagement'));
const CurrencyManagement = lazy(() => import('./CurrencyManagement'));
const CashBoxManagement = lazy(() => import('./CashBoxManagement'));
const ProfitLossReport = lazy(() => import('./ProfitLossReport'));
const SecurityMonitoring = lazy(() => import('./SecurityMonitoring'));
const ImportExport = lazy(() => import('./ImportExport'));

// مكون Loading للـ Suspense
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
    <div className="mr-4 text-lg">جاري التحميل...</div>
  </div>
);

// مكون حماية المسارات
const ProtectedRoute = ({ children, requiredPermission }) => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // فحص الصلاحيات إذا كانت مطلوبة
  if (requiredPermission && user?.role !== 'admin' && !user?.permissions?.includes(requiredPermission)) {
    return <Navigate to="/403" replace />;
  }

  return children;
};

// مكون التوجيه الرئيسي
const AppRouter = () => {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <PermissionsProvider>
            <Routes>
          {/* صفحة تسجيل الدخول */}
          <Route path="/login" element={<Login />} />

          {/* صفحات الأخطاء العامة (Top-level) */}
          <Route path="/403" element={<Error403 />} />
          <Route path="/500" element={<Error500 />} />
          <Route path="/error-test" element={<ErrorTestPage />} />

          {/* المسارات المحمية */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            {/* الصفحة الرئيسية */}
            <Route index element={<InteractiveDashboard />} />
            <Route path="dashboard" element={<InteractiveDashboard />} />

            {/* إدارة المنتجات والمخزون */}
            <Route path="products" element={
              <ProtectedRoute requiredPermission="products.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ProductManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="inventory" element={
              <ProtectedRoute requiredPermission="inventory.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <InventoryManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="lots" element={
              <ProtectedRoute requiredPermission="lots.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <LotManagementAdvanced />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="stock-movements" element={
              <ProtectedRoute requiredPermission="stock_movements.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <StockMovementsAdvanced />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة العملاء والموردين */}
            <Route path="customers" element={
              <ProtectedRoute requiredPermission="customers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CustomerManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="suppliers" element={
              <ProtectedRoute requiredPermission="suppliers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <SupplierManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة الفواتير */}
            <Route path="invoices" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <InvoiceManagementComplete />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="invoices/sales" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <InvoiceManagementComplete />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="invoices/purchase" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PurchaseInvoiceManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="purchase-invoices" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PurchaseInvoiceManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة المخازن والفئات */}
            <Route path="warehouses" element={
              <ProtectedRoute requiredPermission="warehouses.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <WarehouseManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="categories" element={
              <ProtectedRoute requiredPermission="categories.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CategoryManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* المحاسبة والمالية */}
            <Route path="accounting/currencies" element={
              <ProtectedRoute requiredPermission="accounting.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CurrencyManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="accounting/cash-boxes" element={
              <ProtectedRoute requiredPermission="accounting.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CashBoxManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="accounting/profit-loss" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ProfitLossReport />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* التقارير والإحصائيات */}
            <Route path="reports" element={
              <ProtectedRoute requiredPermission="reports.view">
                <AdvancedReportsSystem />
              </ProtectedRoute>
            } />

            <Route path="reports/inventory" element={
              <ProtectedRoute requiredPermission="reports.view">
                <AdvancedReportsSystem />
              </ProtectedRoute>
            } />

            <Route path="reports/sales" element={
              <ProtectedRoute requiredPermission="reports.view">
                <AdvancedReportsSystem />
              </ProtectedRoute>
            } />

            <Route path="reports/financial" element={
              <ProtectedRoute requiredPermission="reports.view">
                <AdvancedReportsSystem />
              </ProtectedRoute>
            } />

            {/* الإعدارات والإدارة */}
            <Route path="users" element={
              <ProtectedRoute requiredPermission="users.view">
                <UserManagement />
              </ProtectedRoute>
            } />
            
            {/* إدارة المستخدمين المتقدمة */}
            <Route path="system/user-management" element={
              <ProtectedRoute requiredPermission="users.view">
                <UserManagement />
              </ProtectedRoute>
            } />
            
            <Route path="user-management" element={
              <ProtectedRoute requiredPermission="users.view">
                <UserManagement />
              </ProtectedRoute>
            } />

            {/* إدارة الأدوار والصلاحيات */}
            <Route path="admin/roles" element={
              <ProtectedRoute requiredPermission="roles.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <AdminRoles />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="company" element={
              <ProtectedRoute requiredPermission="company.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <CompanySettings />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="settings" element={
              <ProtectedRoute requiredPermission="settings.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <SystemSettings />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* معالج الإعداد */}
            <Route path="system/setup-wizard" element={
              <ProtectedRoute requiredPermission="settings.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <SetupWizard />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* الإشعارات */}
            <Route path="notifications" element={
              <ProtectedRoute>
                <Suspense fallback={<LoadingSpinner />}>
                  <NotificationSystemAdvanced />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* RAG assistant */}
            <Route path="rag" element={
              <ProtectedRoute>
                <Suspense fallback={<LoadingSpinner />}>
                  <RagChat />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* أدوات الإدارة */}
            <Route path="admin/security" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <SecurityMonitoring />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="tools/import-export" element={
              <ProtectedRoute requiredPermission="tools.use">
                <Suspense fallback={<LoadingSpinner />}>
                  <ImportExport />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للمنتجات */}
            <Route path="products/add" element={
              <ProtectedRoute requiredPermission="products.create">
                <ProductManagement />
              </ProtectedRoute>
            } />

            <Route path="products/edit/:id" element={
              <ProtectedRoute requiredPermission="products.edit">
                <ProductManagement />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للعملاء */}
            <Route path="customers/add" element={
              <ProtectedRoute requiredPermission="customers.create">
                <CustomerManagement />
              </ProtectedRoute>
            } />

            <Route path="customers/edit/:id" element={
              <ProtectedRoute requiredPermission="customers.edit">
                <CustomerManagement />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للموردين */}
            <Route path="suppliers/add" element={
              <ProtectedRoute requiredPermission="suppliers.create">
                <SupplierManagement />
              </ProtectedRoute>
            } />

            <Route path="suppliers/edit/:id" element={
              <ProtectedRoute requiredPermission="suppliers.edit">
                <SupplierManagement />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للفواتير */}
            <Route path="invoices/add" element={
              <ProtectedRoute requiredPermission="invoices.create">
                <InvoiceManagementComplete />
              </ProtectedRoute>
            } />

            <Route path="invoices/edit/:id" element={
              <ProtectedRoute requiredPermission="invoices.edit">
                <InvoiceManagementComplete />
              </ProtectedRoute>
            } />

            <Route path="invoices/view/:id" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <InvoiceManagementComplete />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للمخازن */}
            <Route path="warehouses/add" element={
              <ProtectedRoute requiredPermission="warehouses.create">
                <WarehouseManagement />
              </ProtectedRoute>
            } />

            <Route path="warehouses/edit/:id" element={
              <ProtectedRoute requiredPermission="warehouses.edit">
                <WarehouseManagement />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية للوتات */}
            <Route path="lots/add" element={
              <ProtectedRoute requiredPermission="lots.create">
                <LotManagementAdvanced />
              </ProtectedRoute>
            } />

            <Route path="lots/edit/:id" element={
              <ProtectedRoute requiredPermission="lots.edit">
                <LotManagementAdvanced />
              </ProtectedRoute>
            } />

            {/* مسارات فرعية لحركات المخزون */}
            <Route path="stock-movements/add" element={
              <ProtectedRoute requiredPermission="stock_movements.create">
                <StockMovementsAdvanced />

              </ProtectedRoute>
            } />

            {/* Redirects for legacy/old paths */}
            <Route path="system/settings" element={<Navigate to="/settings" replace />} />
            <Route path="settings/company" element={<Navigate to="/company" replace />} />
            <Route path="admin/users" element={<Navigate to="/users" replace />} />
            <Route path="warehouse/adjustments" element={<Navigate to="/warehouses" replace />} />
            <Route path="warehouse/constraints" element={<Navigate to="/warehouses" replace />} />
            <Route path="orders/pickup-delivery" element={<Navigate to="/stock-movements" replace />} />
            <Route path="payments/debt-management" element={<Navigate to="/reports/financial" replace />} />
            <Route path="import-export" element={<Navigate to="/tools/import-export" replace />} />
            <Route path="print-export" element={<Navigate to="/reports" replace />} />
            <Route path="settings/categories" element={<Navigate to="/categories" replace />} />
            <Route path="sales-invoices" element={<Navigate to="/invoices/sales" replace />} />
            <Route path="dashboard/interactive" element={<Navigate to="/dashboard" replace />} />
            <Route path="reports/comprehensive" element={<Navigate to="/reports" replace />} />
            <Route path="accounts/customer-supplier" element={<Navigate to="/customers" replace />} />
            <Route path="treasury/opening-balances" element={<Navigate to="/reports/financial" replace />} />

          </Route>

          {/* صفحة 404 (Top-level) */}
          <Route path="*" element={<Error404 />} />

            </Routes>
          </PermissionsProvider>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
};

export default AppRouter;

