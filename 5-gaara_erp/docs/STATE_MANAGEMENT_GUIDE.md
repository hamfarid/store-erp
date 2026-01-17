# 🔄 Gaara Store - State Management Guide

**Version**: 1.0  
**Date**: 2025-10-27  
**Status**: ✅ **ACTIVE**

---

## 🎯 STATE MANAGEMENT OVERVIEW

The application uses React Context API for state management with custom hooks for easy access.

---

## 📦 CONTEXTS

### 1. AuthContext
**Location**: `frontend/src/context/AuthContext.jsx`

**State**:
- `user` - Current user object
- `isLoading` - Loading state
- `isAuthenticated` - Authentication status

**Methods**:
- `login(userData, token)` - Login user
- `logout()` - Logout user
- `checkAuthStatus()` - Verify token on app start

**Usage**:
```jsx
import { useAuth } from '../context/AuthContext'

const { user, isAuthenticated, login, logout } = useAuth()
```

### 2. AppContext
**Location**: `frontend/src/context/AppContext.jsx`

**State**:
- `sidebarOpen` - Sidebar visibility
- `darkMode` - Dark mode toggle
- `notifications` - Notification list
- `loading` - Global loading state
- `error` - Global error state
- `products` - Products data
- `customers` - Customers data
- `invoices` - Invoices data
- `reports` - Reports data
- `pagination` - Pagination state
- `filters` - Filter state

**Methods**:
- `toggleSidebar()` - Toggle sidebar
- `toggleDarkMode()` - Toggle dark mode
- `addNotification(notification)` - Add notification
- `removeNotification(id)` - Remove notification
- `setAppLoading(isLoading)` - Set loading state
- `setAppError(errorMessage)` - Set error state
- `clearError()` - Clear error
- `updatePagination(newPagination)` - Update pagination
- `updateFilters(newFilters)` - Update filters
- `resetFilters()` - Reset filters
- `updateProducts(newProducts)` - Update products
- `updateCustomers(newCustomers)` - Update customers
- `updateInvoices(newInvoices)` - Update invoices
- `updateReports(newReports)` - Update reports

**Usage**:
```jsx
import { useApp } from '../context/AppContext'

const { 
  sidebarOpen, 
  toggleSidebar, 
  darkMode, 
  toggleDarkMode,
  addNotification,
  loading,
  error
} = useApp()
```

---

## 🔐 AUTH CONTEXT USAGE

### Login
```jsx
const { login } = useAuth()

const handleLogin = async (email, password) => {
  try {
    const response = await apiClient.login({ email, password })
    login(response.data.user, response.data.token)
  } catch (error) {
    console.error('Login failed:', error)
  }
}
```

### Logout
```jsx
const { logout } = useAuth()

const handleLogout = async () => {
  await logout()
}
```

### Check Authentication
```jsx
const { isAuthenticated, user } = useAuth()

if (!isAuthenticated) {
  return <Navigate to="/login" />
}

console.log(user.name)
```

---

## 🎨 APP CONTEXT USAGE

### UI State
```jsx
const { sidebarOpen, toggleSidebar, darkMode, toggleDarkMode } = useApp()

return (
  <div className={darkMode ? 'dark' : ''}>
    <button onClick={toggleSidebar}>Toggle Sidebar</button>
    <button onClick={toggleDarkMode}>Toggle Dark Mode</button>
  </div>
)
```

### Notifications
```jsx
const { addNotification, removeNotification } = useApp()

// Add notification
addNotification({
  type: 'success',
  message: 'Operation successful!'
})

// Remove notification
removeNotification(notificationId)
```

### Loading & Error
```jsx
const { loading, error, setAppLoading, setAppError, clearError } = useApp()

const handleFetch = async () => {
  try {
    setAppLoading(true)
    const data = await fetchData()
    // Process data
  } catch (err) {
    setAppError(err.message)
  } finally {
    setAppLoading(false)
  }
}
```

### Data Management
```jsx
const { products, updateProducts, customers, updateCustomers } = useApp()

const handleFetchProducts = async () => {
  const response = await apiClient.getProducts()
  updateProducts(response.data.items)
}
```

### Pagination
```jsx
const { pagination, updatePagination } = useApp()

const handlePageChange = (newPage) => {
  updatePagination({ page: newPage })
}
```

### Filters
```jsx
const { filters, updateFilters, resetFilters } = useApp()

const handleFilterChange = (newFilters) => {
  updateFilters(newFilters)
}

const handleResetFilters = () => {
  resetFilters()
}
```

---

## 🏗️ CONTEXT STRUCTURE

### AuthContext
```
AuthContext
├── user
├── isLoading
├── isAuthenticated
├── login()
├── logout()
└── checkAuthStatus()
```

### AppContext
```
AppContext
├── UI State
│   ├── sidebarOpen
│   ├── darkMode
│   ├── notifications
│   ├── loading
│   └── error
├── Data State
│   ├── products
│   ├── customers
│   ├── invoices
│   └── reports
├── Pagination
│   └── pagination
├── Filters
│   └── filters
└── Methods
    ├── toggleSidebar()
    ├── toggleDarkMode()
    ├── addNotification()
    ├── removeNotification()
    ├── setAppLoading()
    ├── setAppError()
    ├── clearError()
    ├── updatePagination()
    ├── updateFilters()
    ├── resetFilters()
    ├── updateProducts()
    ├── updateCustomers()
    ├── updateInvoices()
    └── updateReports()
```

---

## 🔗 PROVIDER SETUP

### App.jsx
```jsx
import { AuthProvider } from './context/AuthContext'
import { AppProvider } from './context/AppContext'

function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <AppRouter />
      </AppProvider>
    </AuthProvider>
  )
}
```

---

## 📊 STATE FLOW

### Authentication Flow
1. App starts
2. AuthContext checks localStorage for token
3. If token exists, verify with API
4. If valid, set user
5. If invalid, clear token

### Data Flow
1. Component mounts
2. Fetch data from API
3. Update AppContext with data
4. Component re-renders with new data

### Notification Flow
1. Action triggers notification
2. addNotification() called
3. Notification added to state
4. Notification displayed
5. Auto-remove after 5 seconds

---

## ✅ BEST PRACTICES

### Do's ✅
- Use custom hooks for context access
- Keep context focused and single-purpose
- Use useCallback for memoization
- Handle errors gracefully
- Provide loading states
- Clear data on logout
- Use localStorage for persistence

### Don'ts ❌
- Don't put everything in one context
- Don't use context for frequently changing data
- Don't forget error handling
- Don't leave users without feedback
- Don't store sensitive data in localStorage
- Don't create context inside component
- Don't forget to provide context

---

## 📚 RESOURCES

- **AuthContext**: `frontend/src/context/AuthContext.jsx`
- **AppContext**: `frontend/src/context/AppContext.jsx`
- **React Context Docs**: https://react.dev/reference/react/useContext
- **Custom Hooks**: `frontend/src/hooks/`

---

**Status**: ✅ **ACTIVE**  
**Last Updated**: 2025-10-27  
**Maintained By**: Augment Agent

🔄 **Follow this guide for consistent state management!** 🔄

