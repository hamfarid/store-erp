# 🗺️ Gaara Store - Routing Guide

**Version**: 1.0  
**Date**: 2025-10-27  
**Status**: ✅ **ACTIVE**

---

## 🎯 ROUTING OVERVIEW

The application uses React Router v6 with protected routes, permission-based access control, and comprehensive error handling.

---

## 📋 ROUTE STRUCTURE

### Public Routes
```
/login                    - Login page
/403                      - Forbidden page
/500                      - Server error page
/error-test               - Error test page
*                         - 404 Not Found page
```

### Protected Routes (Require Authentication)
```
/                         - Dashboard (home)
/dashboard                - Dashboard
/products                 - Products management
/inventory                - Inventory management
/lots                     - Lots management
/customers                - Customers management
/suppliers                - Suppliers management
/categories               - Categories management
/warehouses               - Warehouses management
/invoices                 - Invoices management
/invoices/sales           - Sales invoices
/invoices/purchases       - Purchase invoices
/stock-movements          - Stock movements
/notifications            - Notifications
/rag-chat                 - RAG Chat
/reports                  - Reports
/reports/inventory        - Inventory reports
/reports/financial        - Financial reports
/users                    - User management
/settings                 - System settings
/company-settings         - Company settings
```

---

## 🔐 PROTECTED ROUTES

### ProtectedRoute Component
```jsx
const ProtectedRoute = ({ children, requiredPermission }) => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredPermission && user?.role !== 'admin' && !user?.permissions?.includes(requiredPermission)) {
    return <Navigate to="/403" replace />;
  }

  return children;
};
```

### Usage
```jsx
<Route path="products" element={
  <ProtectedRoute requiredPermission="products.view">
    <ProductManagement />
  </ProtectedRoute>
} />
```

---

## 🔑 PERMISSIONS

### Permission Types
- `products.view` - View products
- `products.create` - Create products
- `products.edit` - Edit products
- `products.delete` - Delete products
- `inventory.view` - View inventory
- `customers.view` - View customers
- `invoices.view` - View invoices
- `reports.view` - View reports
- `users.manage` - Manage users
- `settings.manage` - Manage settings

### Permission Checking
```jsx
const { hasPermission } = usePermissions();

if (hasPermission('products.edit')) {
  // Show edit button
}
```

---

## 🧭 NAVIGATION

### Navigation Menu Items
```javascript
const menuItems = [
  { path: '/', label: 'لوحة التحكم', icon: 'BarChart3' },
  { path: '/products', label: 'المنتجات', icon: 'Package' },
  { path: '/inventory', label: 'المخزون', icon: 'Boxes' },
  { path: '/customers', label: 'العملاء', icon: 'Users' },
  { path: '/suppliers', label: 'الموردين', icon: 'Truck' },
  { path: '/invoices', label: 'الفواتير', icon: 'FileText' },
  { path: '/reports', label: 'التقارير', icon: 'BarChart3' },
  { path: '/settings', label: 'الإعدادات', icon: 'Settings' },
];
```

### Breadcrumbs
```jsx
<Breadcrumbs />
```

---

## 🔄 ROUTE TRANSITIONS

### Lazy Loading
```jsx
const ProductManagement = lazy(() => import('./ProductManagement'));

<Suspense fallback={<LoadingSpinner />}>
  <ProductManagement />
</Suspense>
```

### Loading Spinner
```jsx
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
    <div className="mr-4 text-lg">جاري التحميل...</div>
  </div>
);
```

---

## ❌ ERROR HANDLING

### Error Pages
- **404**: Page not found
- **403**: Forbidden (permission denied)
- **500**: Server error
- **Error Boundary**: Catches React errors

### Error Boundary
```jsx
<ErrorBoundary>
  <Routes>
    {/* Routes */}
  </Routes>
</ErrorBoundary>
```

---

## 🔗 NAVIGATION LINKS

### Using Link Component
```jsx
import { Link } from 'react-router-dom';

<Link to="/products" className="text-blue-600 hover:underline">
  Products
</Link>
```

### Using useNavigate Hook
```jsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/products');
```

---

## 📍 CURRENT LOCATION

### Using useLocation Hook
```jsx
import { useLocation } from 'react-router-dom';

const location = useLocation();
console.log(location.pathname); // Current path
```

---

## 🔐 AUTHENTICATION FLOW

### Login Flow
1. User navigates to `/login`
2. User enters credentials
3. API validates credentials
4. Token stored in localStorage
5. User redirected to `/`

### Logout Flow
1. User clicks logout
2. Token removed from localStorage
3. User redirected to `/login`

### Protected Route Flow
1. User navigates to protected route
2. Check if authenticated
3. If not authenticated → redirect to `/login`
4. If authenticated → check permissions
5. If no permission → redirect to `/403`
6. If permission → render component

---

## 🎯 ROUTE PARAMETERS

### Dynamic Routes
```jsx
<Route path="/products/:id" element={<ProductDetails />} />
```

### Using useParams Hook
```jsx
import { useParams } from 'react-router-dom';

const { id } = useParams();
```

---

## 🔍 QUERY PARAMETERS

### Using useSearchParams Hook
```jsx
import { useSearchParams } from 'react-router-dom';

const [searchParams, setSearchParams] = useSearchParams();
const page = searchParams.get('page');
```

---

## 📊 ROUTE CONFIGURATION

### Routes File
- **Location**: `frontend/src/routes/index.js`
- **Purpose**: Centralized route configuration
- **Usage**: Import and use in AppRouter

### AppRouter Component
- **Location**: `frontend/src/components/AppRouter.jsx`
- **Purpose**: Main routing component
- **Usage**: Wrap entire app with AppRouter

---

## ✅ BEST PRACTICES

### Do's ✅
- Use protected routes for sensitive pages
- Check permissions before rendering
- Use lazy loading for heavy components
- Provide loading states
- Handle errors gracefully
- Use meaningful route names
- Implement breadcrumbs
- Use semantic URLs

### Don'ts ❌
- Don't expose sensitive routes
- Don't skip permission checks
- Don't load all components at once
- Don't leave users without feedback
- Don't ignore errors
- Don't use cryptic route names
- Don't forget error pages
- Don't use non-semantic URLs

---

## 📚 RESOURCES

- **React Router Docs**: https://reactrouter.com/
- **AppRouter**: `frontend/src/components/AppRouter.jsx`
- **Routes Config**: `frontend/src/routes/index.js`
- **Auth Context**: `frontend/src/context/AuthContext.jsx`
- **Permissions Guard**: `frontend/src/components/ui/PermissionsGuard.jsx`

---

**Status**: ✅ **ACTIVE**  
**Last Updated**: 2025-10-27  
**Maintained By**: Augment Agent

🗺️ **Follow this guide for consistent routing!** 🗺️

