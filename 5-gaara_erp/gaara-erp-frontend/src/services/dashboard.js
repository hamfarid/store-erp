/**
 * Dashboard Service
 * Handles dashboard statistics and analytics data
 */

import api from "./api"

export const dashboardService = {
  /**
   * Get main dashboard statistics
   */
  getStats: async () => {
    return api.get("/dashboard/stats/")
  },

  /**
   * Get sales chart data
   */
  getSalesChart: async (period = "month") => {
    return api.get("/dashboard/sales-chart/", { period })
  },

  /**
   * Get revenue chart data
   */
  getRevenueChart: async (period = "year") => {
    return api.get("/dashboard/revenue-chart/", { period })
  },

  /**
   * Get recent activities
   */
  getRecentActivities: async (limit = 10) => {
    return api.get("/dashboard/activities/", { limit })
  },

  /**
   * Get low stock alerts
   */
  getLowStockAlerts: async () => {
    return api.get("/dashboard/low-stock-alerts/")
  },

  /**
   * Get pending orders count
   */
  getPendingOrders: async () => {
    return api.get("/dashboard/pending-orders/")
  },

  /**
   * Get top selling products
   */
  getTopProducts: async (limit = 5) => {
    return api.get("/dashboard/top-products/", { limit })
  },

  /**
   * Get customer growth data
   */
  getCustomerGrowth: async (period = "month") => {
    return api.get("/dashboard/customer-growth/", { period })
  },

  /**
   * Get IoT devices status
   */
  getIoTStatus: async () => {
    return api.get("/dashboard/iot-status/")
  },

  /**
   * Get AI predictions summary
   */
  getAIPredictions: async () => {
    return api.get("/dashboard/ai-predictions/")
  },
}

export default dashboardService
