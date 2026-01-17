import api from "./api"

/**
 * Sales Service
 * Handles all sales management API calls
 */

// Customers
export const getCustomers = async (params = {}) => {
  const { page = 1, limit = 10, search = "", status = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(search && { search }),
    ...(status && { status }),
  })

  return api.get(`/sales/customers?${queryParams}`)
}

export const getCustomerById = async (customerId) => {
  return api.get(`/sales/customers/${customerId}`)
}

export const createCustomer = async (customerData) => {
  return api.post("/sales/customers", customerData)
}

export const updateCustomer = async (customerId, customerData) => {
  return api.put(`/sales/customers/${customerId}`, customerData)
}

export const deleteCustomer = async (customerId) => {
  return api.delete(`/sales/customers/${customerId}`)
}

// Orders
export const getOrders = async (params = {}) => {
  const { page = 1, limit = 20, status = "", customer = "", dateFrom = "", dateTo = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(status && { status }),
    ...(customer && { customer }),
    ...(dateFrom && { dateFrom }),
    ...(dateTo && { dateTo }),
  })

  return api.get(`/sales/orders?${queryParams}`)
}

export const getOrderById = async (orderId) => {
  return api.get(`/sales/orders/${orderId}`)
}

export const createOrder = async (orderData) => {
  return api.post("/sales/orders", orderData)
}

export const updateOrder = async (orderId, orderData) => {
  return api.put(`/sales/orders/${orderId}`, orderData)
}

export const cancelOrder = async (orderId, reason) => {
  return api.post(`/sales/orders/${orderId}/cancel`, { reason })
}

export const fulfillOrder = async (orderId) => {
  return api.post(`/sales/orders/${orderId}/fulfill`)
}

// Invoices
export const getInvoices = async (params = {}) => {
  const { page = 1, limit = 20, status = "", customer = "", dateFrom = "", dateTo = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(status && { status }),
    ...(customer && { customer }),
    ...(dateFrom && { dateFrom }),
    ...(dateTo && { dateTo }),
  })

  return api.get(`/sales/invoices?${queryParams}`)
}

export const getInvoiceById = async (invoiceId) => {
  return api.get(`/sales/invoices/${invoiceId}`)
}

export const createInvoice = async (invoiceData) => {
  return api.post("/sales/invoices", invoiceData)
}

export const updateInvoice = async (invoiceId, invoiceData) => {
  return api.put(`/sales/invoices/${invoiceId}`, invoiceData)
}

export const sendInvoice = async (invoiceId) => {
  return api.post(`/sales/invoices/${invoiceId}/send`)
}

export const markInvoicePaid = async (invoiceId, paymentData) => {
  return api.post(`/sales/invoices/${invoiceId}/pay`, paymentData)
}

// Reports
export const getSalesReport = async (params = {}) => {
  return api.get("/sales/reports/summary", { params })
}

export const getCustomerReport = async (customerId, params = {}) => {
  return api.get(`/sales/customers/${customerId}/report`, { params })
}

export const getTopProducts = async (params = {}) => {
  return api.get("/sales/reports/top-products", { params })
}

export const getSalesTrend = async (params = {}) => {
  return api.get("/sales/reports/trend", { params })
}

// Mock data for development
export const mockCustomers = [
  {
    id: 1,
    name: "مزرعة النخيل",
    email: "nakhil@example.com",
    phone: "+966501234567",
    address: "الرياض، حي النخيل",
    type: "company",
    status: "active",
    totalOrders: 45,
    totalSpent: 125000,
    createdAt: "2023-01-15T08:00:00Z",
  },
  {
    id: 2,
    name: "أحمد محمد",
    email: "ahmed@example.com",
    phone: "+966502345678",
    address: "جدة، حي الزهراء",
    type: "individual",
    status: "active",
    totalOrders: 12,
    totalSpent: 35000,
    createdAt: "2023-03-20T10:30:00Z",
  },
]

export default {
  getCustomers,
  getCustomerById,
  createCustomer,
  updateCustomer,
  deleteCustomer,
  getOrders,
  getOrderById,
  createOrder,
  updateOrder,
  cancelOrder,
  fulfillOrder,
  getInvoices,
  getInvoiceById,
  createInvoice,
  updateInvoice,
  sendInvoice,
  markInvoicePaid,
  getSalesReport,
  getCustomerReport,
  getTopProducts,
  getSalesTrend,
  mockCustomers,
}
