import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import Layout from './Layout';
import Login from './Login';
import InteractiveDashboard from '../pages/InteractiveDashboard';
import { 
  Error400, Error401, Error402, Error403, Error404, Error405,
  Error500, Error501, Error502, Error503, Error504, Error505, Error506,
  ErrorBoundary, ErrorTestPage 
} from './ErrorPages';
import { PermissionsProvider } from './ui/PermissionsGuard'

// Auth Pages (Lazy loaded)
const ForgotPassword = lazy(() => import('../pages/ForgotPassword'));
const ResetPassword = lazy(() => import('../pages/ResetPassword'));
const TwoFactorVerify = lazy(() => import('../pages/TwoFactorVerify'));
const LogoutPage = lazy(() => import('../pages/Logout'));
const RegisterPage = lazy(() => import('../pages/Register'));
const ProfilePage = lazy(() => import('../pages/Profile'));

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

// New Modern Pages
const ReturnsPage = lazy(() => import('../pages/ReturnsPage'));
const PaymentsPage = lazy(() => import('../pages/PaymentsPage'));
const ReturnsManagement = lazy(() => import('../pages/ReturnsManagement'));
const PaymentDebtManagement = lazy(() => import('../pages/PaymentDebtManagement'));
const WarehouseAdjustments = lazy(() => import('../pages/WarehouseAdjustments'));
const OpeningBalancesTreasury = lazy(() => import('../pages/OpeningBalancesTreasury'));
const CustomerSupplierAccounts = lazy(() => import('../pages/CustomerSupplierAccounts'));
const AccountingVouchers = lazy(() => import('../pages/AccountingVouchers'));
const TreasuryManagement = lazy(() => import('../pages/TreasuryManagement'));
const WarehouseTransfer = lazy(() => import('../pages/WarehouseTransfer'));
const AuditLogs = lazy(() => import('../pages/AuditLogs'));
const AutomationTasks = lazy(() => import('../pages/AutomationTasks'));
const NotificationsCenter = lazy(() => import('../pages/NotificationsCenter'));
const NotificationSettings = lazy(() => import('../pages/NotificationSettings'));
const TaxSettings = lazy(() => import('../pages/TaxSettings'));
const ProfitLossReports = lazy(() => import('../pages/ProfitLossReports'));
const LotBatchManagement = lazy(() => import('../pages/LotBatchManagement'));
const LotExpiryReport = lazy(() => import('../pages/LotExpiryReport'));
const MFASettings = lazy(() => import('../pages/MFASettings'));
const InventoryAlerts = lazy(() => import('../pages/InventoryAlerts'));
const BackupRestore = lazy(() => import('../pages/BackupRestore'));
const SystemStatus = lazy(() => import('../pages/SystemStatus'));
const ExcelOperations = lazy(() => import('../pages/ExcelOperations'));
const CustomerCredit = lazy(() => import('../pages/CustomerCredit'));
const SecurityDashboard = lazy(() => import('../pages/SecurityDashboard'));
const SalesEngineers = lazy(() => import('../pages/SalesEngineers'));
const PurchaseOrders = lazy(() => import('../pages/PurchaseOrders'));
const PotentialCustomers = lazy(() => import('../pages/PotentialCustomers'));
const PriceHistory = lazy(() => import('../pages/PriceHistory'));
const DiscountManagement = lazy(() => import('../pages/DiscountManagement'));
const ModernDashboard = lazy(() => import('../pages/Dashboard'));
const ModernProductsPage = lazy(() => import('../pages/ProductsPage'));
const ModernInvoicePage = lazy(() => import('../pages/InvoicePage'));
const ModernReportsPage = lazy(() => import('../pages/ReportsPage'));
const ModernSettingsPage = lazy(() => import('../pages/SettingsPage'));
const ModernUsersPage = lazy(() => import('../pages/UsersPage'));
const ModernCategoriesPage = lazy(() => import('../pages/CategoriesPage'));
const ModernCustomersPage = lazy(() => import('../pages/CustomersPage'));
const ModernSuppliersPage = lazy(() => import('../pages/SuppliersPage'));
const ModernWarehousesPage = lazy(() => import('../pages/WarehousesPage'));
const ModernStockMovementsPage = lazy(() => import('../pages/StockMovementsPage'));
const ModernPurchasesPage = lazy(() => import('../pages/PurchasesPage'));
const POSSystem = lazy(() => import('../pages/POSSystem'));
const ReportsSystem = lazy(() => import('../pages/ReportsSystem'));
const PurchaseOrdersManagement = lazy(() => import('../pages/PurchaseOrdersManagement'));
const RolesPermissionsManagement = lazy(() => import('../pages/RolesPermissionsManagement'));

// Admin Pages
const AdminDashboard = lazy(() => import('../pages/AdminDashboard'));
const RolesPage = lazy(() => import('../pages/RolesPage'));
const SetupWizardPage = lazy(() => import('../pages/SetupWizardPage'));
const UserRightsPage = lazy(() => import('../pages/UserRightsPage'));
const UserRightsConfigPage = lazy(() => import('../pages/UserRightsConfigPage'));
const ReportsSetupPage = lazy(() => import('../pages/ReportsSetupPage'));

// Error Pages
import NetworkErrorPage from './NetworkErrorPage';

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
          {/* صفحات المصادقة - Authentication Pages */}
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={
            <Suspense fallback={<LoadingSpinner />}>
              <LogoutPage />
            </Suspense>
          } />
          <Route path="/register" element={
            <Suspense fallback={<LoadingSpinner />}>
              <RegisterPage />
            </Suspense>
          } />
          <Route path="/forgot-password" element={
            <Suspense fallback={<LoadingSpinner />}>
              <ForgotPassword />
            </Suspense>
          } />
          <Route path="/reset-password" element={
            <Suspense fallback={<LoadingSpinner />}>
              <ResetPassword />
            </Suspense>
          } />
          <Route path="/2fa-verify" element={
            <Suspense fallback={<LoadingSpinner />}>
              <TwoFactorVerify />
            </Suspense>
          } />
          <Route path="/profile" element={
            <ProtectedRoute>
              <Suspense fallback={<LoadingSpinner />}>
                <ProfilePage />
              </Suspense>
            </ProtectedRoute>
          } />

          {/* Setup Wizard - No auth required */}
          <Route path="/setup" element={
            <Suspense fallback={<LoadingSpinner />}>
              <SetupWizardPage />
            </Suspense>
          } />

          {/* صفحات الأخطاء العامة (Top-level) */}
          {/* 4xx Client Error Pages */}
          <Route path="/400" element={<Error400 />} />
          <Route path="/401" element={<Error401 />} />
          <Route path="/402" element={<Error402 />} />
          <Route path="/403" element={<Error403 />} />
          <Route path="/405" element={<Error405 />} />
          
          {/* 5xx Server Error Pages */}
          <Route path="/500" element={<Error500 />} />
          <Route path="/501" element={<Error501 />} />
          <Route path="/502" element={<Error502 />} />
          <Route path="/503" element={<Error503 />} />
          <Route path="/504" element={<Error504 />} />
          <Route path="/505" element={<Error505 />} />
          <Route path="/506" element={<Error506 />} />
          
          {/* Network and Test Error Pages */}
          <Route path="/network-error" element={<NetworkErrorPage />} />
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

            {/* قسائم الدفع والقبض */}
            <Route path="accounting/vouchers" element={
              <ProtectedRoute requiredPermission="accounting.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <AccountingVouchers />
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

            {/* Modern Admin Dashboard */}
            <Route path="admin/dashboard" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <AdminDashboard />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* Modern Roles Management */}
            <Route path="admin/roles-management" element={
              <ProtectedRoute requiredPermission="roles.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <RolesPage />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* User Rights Configuration */}
            <Route path="admin/user-rights" element={
              <ProtectedRoute requiredPermission="roles.assign">
                <Suspense fallback={<LoadingSpinner />}>
                  <UserRightsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* User Rights Config Page - Advanced */}
            <Route path="admin/user-rights-config" element={
              <ProtectedRoute requiredPermission="users.permissions">
                <Suspense fallback={<LoadingSpinner />}>
                  <UserRightsConfigPage />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* Reports Setup Page */}
            <Route path="reports/setup" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ReportsSetupPage />
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

            {/* المرتجعات */}
            <Route path="returns" element={
              <ProtectedRoute requiredPermission="returns.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ReturnsManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* المدفوعات */}
            <Route path="payments" element={
              <ProtectedRoute requiredPermission="payments.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PaymentsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة المدفوعات والديون */}
            <Route path="debt-management" element={
              <ProtectedRoute requiredPermission="payments.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PaymentDebtManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* تعديلات المخازن */}
            <Route path="warehouse-adjustments" element={
              <ProtectedRoute requiredPermission="warehouses.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <WarehouseAdjustments />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* الأرصدة الافتتاحية للخزنة */}
            <Route path="treasury/opening-balances" element={
              <ProtectedRoute requiredPermission="accounting.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <OpeningBalancesTreasury />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* حسابات العملاء والموردين */}
            <Route path="accounts/customer-supplier" element={
              <ProtectedRoute requiredPermission="customers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CustomerSupplierAccounts />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة الخزينة */}
            <Route path="treasury-management" element={
              <ProtectedRoute requiredPermission="accounting.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <TreasuryManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* تحويلات المخازن */}
            <Route path="warehouse-transfer" element={
              <ProtectedRoute requiredPermission="warehouses.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <WarehouseTransfer />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* سجل التدقيق */}
            <Route path="audit-logs" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <AuditLogs />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* المهام الآلية */}
            <Route path="automation-tasks" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <AutomationTasks />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* مركز الإشعارات */}
            <Route path="notifications-center" element={
              <ProtectedRoute>
                <Suspense fallback={<LoadingSpinner />}>
                  <NotificationsCenter />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إعدادات الإشعارات */}
            <Route path="notification-settings" element={
              <ProtectedRoute requiredPermission="settings.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <NotificationSettings />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إعدادات الضرائب */}
            <Route path="tax-settings" element={
              <ProtectedRoute requiredPermission="settings.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <TaxSettings />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* تقارير الأرباح والخسائر */}
            <Route path="profit-loss-reports" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ProfitLossReports />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة الدفعات */}
            <Route path="lot-batch-management" element={
              <ProtectedRoute requiredPermission="lots.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <LotBatchManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* تقرير انتهاء صلاحية اللوتات */}
            <Route path="lot-expiry-report" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <LotExpiryReport />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إعدادات المصادقة الثنائية */}
            <Route path="mfa-settings" element={
              <ProtectedRoute>
                <Suspense fallback={<LoadingSpinner />}>
                  <MFASettings />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* تنبيهات المخزون */}
            <Route path="inventory-alerts" element={
              <ProtectedRoute requiredPermission="inventory.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <InventoryAlerts />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* النسخ الاحتياطي */}
            <Route path="backup-restore" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <BackupRestore />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* حالة النظام */}
            <Route path="system-status" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <SystemStatus />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* عمليات Excel */}
            <Route path="excel-operations" element={
              <ProtectedRoute requiredPermission="import.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ExcelOperations />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة ائتمان العملاء */}
            <Route path="customer-credit" element={
              <ProtectedRoute requiredPermission="customers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <CustomerCredit />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* لوحة الأمان */}
            <Route path="security-dashboard" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <SecurityDashboard />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* مهندسي المبيعات */}
            <Route path="sales-engineers" element={
              <ProtectedRoute requiredPermission="sales.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <SalesEngineers />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* أوامر الشراء */}
            <Route path="purchase-orders" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PurchaseOrders />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* العملاء المحتملين (CRM) */}
            <Route path="potential-customers" element={
              <ProtectedRoute requiredPermission="customers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PotentialCustomers />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* سجل الأسعار */}
            <Route path="price-history" element={
              <ProtectedRoute requiredPermission="products.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PriceHistory />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة الخصومات */}
            <Route path="discounts" element={
              <ProtectedRoute requiredPermission="products.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <DiscountManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* Modern UI Pages */}
            <Route path="modern/dashboard" element={
              <ProtectedRoute>
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernDashboard />
                </Suspense>
              </ProtectedRoute>
            } />
            
            <Route path="modern/products" element={
              <ProtectedRoute requiredPermission="products.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernProductsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/invoices" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernInvoicePage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/reports" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernReportsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/settings" element={
              <ProtectedRoute requiredPermission="settings.edit">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernSettingsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/users" element={
              <ProtectedRoute requiredPermission="users.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernUsersPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/categories" element={
              <ProtectedRoute requiredPermission="categories.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernCategoriesPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/customers" element={
              <ProtectedRoute requiredPermission="customers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernCustomersPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/suppliers" element={
              <ProtectedRoute requiredPermission="suppliers.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernSuppliersPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/warehouses" element={
              <ProtectedRoute requiredPermission="warehouses.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernWarehousesPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/stock-movements" element={
              <ProtectedRoute requiredPermission="stock_movements.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernStockMovementsPage />
                </Suspense>
              </ProtectedRoute>
            } />

            <Route path="modern/purchases" element={
              <ProtectedRoute requiredPermission="invoices.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ModernPurchasesPage />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* نظام نقطة البيع (POS) */}
            <Route path="pos" element={
              <ProtectedRoute requiredPermission="sales.create">
                <Suspense fallback={<LoadingSpinner />}>
                  <POSSystem />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* نظام التقارير المتقدم */}
            <Route path="reports-system" element={
              <ProtectedRoute requiredPermission="reports.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <ReportsSystem />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة أوامر الشراء */}
            <Route path="purchases-management" element={
              <ProtectedRoute requiredPermission="purchases.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <PurchaseOrdersManagement />
                </Suspense>
              </ProtectedRoute>
            } />

            {/* إدارة الأدوار والأذونات */}
            <Route path="roles-permissions" element={
              <ProtectedRoute requiredPermission="admin.view">
                <Suspense fallback={<LoadingSpinner />}>
                  <RolesPermissionsManagement />
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
            <Route path="warehouse/adjustments" element={<Navigate to="/warehouse-adjustments" replace />} />
            <Route path="warehouse/constraints" element={<Navigate to="/warehouses" replace />} />
            <Route path="orders/pickup-delivery" element={<Navigate to="/stock-movements" replace />} />
            <Route path="payments/debt-management" element={<Navigate to="/debt-management" replace />} />
            <Route path="import-export" element={<Navigate to="/tools/import-export" replace />} />
            <Route path="print-export" element={<Navigate to="/reports" replace />} />
            <Route path="settings/categories" element={<Navigate to="/categories" replace />} />
            <Route path="sales-invoices" element={<Navigate to="/invoices/sales" replace />} />
            <Route path="dashboard/interactive" element={<Navigate to="/dashboard" replace />} />
            <Route path="reports/comprehensive" element={<Navigate to="/reports" replace />} />

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

