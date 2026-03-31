/**
 * Health Service
 * Provides health check and monitoring functionality.
 */

import apiClient from '../config/apiClient';

const healthService = {
  /**
   * Basic health check
   * @returns {Promise<Object>} Health status
   */
  async check() {
    try {
      const response = await apiClient.get('/api/health');
      return response.data;
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message
      };
    }
  },

  /**
   * Detailed health check with metrics
   * @returns {Promise<Object>} Detailed health status
   */
  async detailed() {
    try {
      const response = await apiClient.get('/api/health/detailed');
      return response.data;
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message
      };
    }
  },

  /**
   * Check if API is reachable
   * @returns {Promise<boolean>} True if API is reachable
   */
  async isOnline() {
    try {
      const response = await this.check();
      return response.status === 'healthy';
    } catch {
      return false;
    }
  },

  /**
   * Get system metrics
   * @returns {Promise<Object>} System metrics
   */
  async getMetrics() {
    try {
      const response = await apiClient.get('/api/health/detailed');
      return response.data.metrics || {};
    } catch {
      return {};
    }
  },

  /**
   * Check database connectivity
   * @returns {Promise<boolean>} True if database is connected
   */
  async checkDatabase() {
    try {
      const response = await this.detailed();
      return response.checks?.database?.status === 'healthy';
    } catch {
      return false;
    }
  },

  /**
   * Monitor health continuously
   * @param {Function} callback - Called with health status
   * @param {number} interval - Check interval in ms (default: 30000)
   * @returns {Function} Stop function
   */
  monitor(callback, interval = 30000) {
    const checkHealth = async () => {
      const health = await this.check();
      callback(health);
    };

    // Initial check
    checkHealth();

    // Periodic checks
    const intervalId = setInterval(checkHealth, interval);

    // Return stop function
    return () => clearInterval(intervalId);
  }
};

export default healthService;
