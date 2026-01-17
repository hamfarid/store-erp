import React, { createContext, useContext, useState, useCallback } from 'react'

// Create App Context
const AppContext = createContext()

// Custom hook to use App Context
export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
}

// App Provider Component
export const AppProvider = ({ children }) => {
  // UI State
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [darkMode, setDarkMode] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Data State
  const [products, setProducts] = useState([])
  const [customers, setCustomers] = useState([])
  const [invoices, setInvoices] = useState([])
  const [reports, setReports] = useState([])

  // Pagination State
  const [pagination, setPagination] = useState({
    page: 1,
    perPage: 10,
    total: 0
  })

  // Filter State
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    status: '',
    dateFrom: '',
    dateTo: ''
  })

  // Toggle Sidebar
  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev)
  }, [])

  // Toggle Dark Mode
  const toggleDarkMode = useCallback(() => {
    setDarkMode(prev => !prev)
    localStorage.setItem('darkMode', JSON.stringify(!darkMode))
  }, [darkMode])

  // Add Notification
  const addNotification = useCallback((notification) => {
    const id = Date.now()
    const newNotification = { ...notification, id }
    setNotifications(prev => [...prev, newNotification])

    // Auto remove after 5 seconds
    setTimeout(() => {
      removeNotification(id)
    }, 5000)

    return id
  }, [])

  // Remove Notification
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }, [])

  // Set Loading
  const setAppLoading = useCallback((isLoading) => {
    setLoading(isLoading)
  }, [])

  // Set Error
  const setAppError = useCallback((errorMessage) => {
    setError(errorMessage)
    if (errorMessage) {
      addNotification({
        type: 'error',
        message: errorMessage
      })
    }
  }, [addNotification])

  // Clear Error
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  // Update Pagination
  const updatePagination = useCallback((newPagination) => {
    setPagination(prev => ({ ...prev, ...newPagination }))
  }, [])

  // Update Filters
  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }))
  }, [])

  // Reset Filters
  const resetFilters = useCallback(() => {
    setFilters({
      search: '',
      category: '',
      status: '',
      dateFrom: '',
      dateTo: ''
    })
  }, [])

  // Update Products
  const updateProducts = useCallback((newProducts) => {
    setProducts(newProducts)
  }, [])

  // Update Customers
  const updateCustomers = useCallback((newCustomers) => {
    setCustomers(newCustomers)
  }, [])

  // Update Invoices
  const updateInvoices = useCallback((newInvoices) => {
    setInvoices(newInvoices)
  }, [])

  // Update Reports
  const updateReports = useCallback((newReports) => {
    setReports(newReports)
  }, [])

  // Context Value
  const value = {
    // UI State
    sidebarOpen,
    toggleSidebar,
    darkMode,
    toggleDarkMode,
    notifications,
    addNotification,
    removeNotification,
    loading,
    setAppLoading,
    error,
    setAppError,
    clearError,

    // Data State
    products,
    updateProducts,
    customers,
    updateCustomers,
    invoices,
    updateInvoices,
    reports,
    updateReports,

    // Pagination
    pagination,
    updatePagination,

    // Filters
    filters,
    updateFilters,
    resetFilters
  }

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  )
}

export default AppContext

