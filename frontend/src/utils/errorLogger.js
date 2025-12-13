/**
 * Frontend Error Logger
 * 
 * Comprehensive error tracking and logging system for the frontend
 * Features:
 * - Console logging with colors
 * - localStorage persistence
 * - Error categorization
 * - Stack trace capture
 * - Performance tracking
 * - User context
 */

// Error levels
export const ERROR_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
  FATAL: 'FATAL',
};

// Error categories
export const ERROR_CATEGORIES = {
  NETWORK: 'NETWORK',
  AUTH: 'AUTH',
  VALIDATION: 'VALIDATION',
  RENDER: 'RENDER',
  STATE: 'STATE',
  API: 'API',
  UNKNOWN: 'UNKNOWN',
};

// Storage key
const STORAGE_KEY = 'store-erp-error-logs';
const MAX_LOGS = 100; // Maximum logs to keep in localStorage

/**
 * Error Logger Class
 */
class ErrorLogger {
  constructor() {
    this.logs = this.loadLogs();
    this.setupGlobalHandlers();
  }

  /**
   * Load logs from localStorage
   */
  loadLogs() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Failed to load error logs:', error);
      return [];
    }
  }

  /**
   * Save logs to localStorage
   */
  saveLogs() {
    try {
      // Keep only the last MAX_LOGS entries
      const logsToSave = this.logs.slice(-MAX_LOGS);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(logsToSave));
    } catch (error) {
      console.error('Failed to save error logs:', error);
    }
  }

  /**
   * Setup global error handlers
   */
  setupGlobalHandlers() {
    // Catch unhandled errors
    window.addEventListener('error', (event) => {
      this.log({
        level: ERROR_LEVELS.ERROR,
        category: ERROR_CATEGORIES.UNKNOWN,
        message: event.message,
        stack: event.error?.stack,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      });
    });

    // Catch unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      this.log({
        level: ERROR_LEVELS.ERROR,
        category: ERROR_CATEGORIES.UNKNOWN,
        message: `Unhandled Promise Rejection: ${event.reason}`,
        stack: event.reason?.stack,
      });
    });

    // Catch console errors
    const originalError = console.error;
    console.error = (...args) => {
      this.log({
        level: ERROR_LEVELS.ERROR,
        category: ERROR_CATEGORIES.UNKNOWN,
        message: args.join(' '),
      });
      originalError.apply(console, args);
    };
  }

  /**
   * Log an error
   */
  log({
    level = ERROR_LEVELS.INFO,
    category = ERROR_CATEGORIES.UNKNOWN,
    message,
    stack,
    data,
    filename,
    lineno,
    colno,
  }) {
    const logEntry = {
      id: Date.now() + Math.random(),
      timestamp: new Date().toISOString(),
      level,
      category,
      message,
      stack,
      data,
      filename,
      lineno,
      colno,
      userAgent: navigator.userAgent,
      url: window.location.href,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
      },
    };

    // Add to logs array
    this.logs.push(logEntry);

    // Save to localStorage
    this.saveLogs();

    // Console output with colors
    this.consoleLog(logEntry);

    // Return log entry for chaining
    return logEntry;
  }

  /**
   * Console log with colors
   */
  consoleLog(logEntry) {
    const colors = {
      [ERROR_LEVELS.DEBUG]: 'color: #708079; font-weight: normal;',
      [ERROR_LEVELS.INFO]: 'color: #80AA45; font-weight: bold;',
      [ERROR_LEVELS.WARN]: 'color: #E65E36; font-weight: bold;',
      [ERROR_LEVELS.ERROR]: 'color: #C7451F; font-weight: bold;',
      [ERROR_LEVELS.FATAL]: 'color: #C7451F; font-weight: bold; font-size: 14px;',
    };

    const style = colors[logEntry.level] || colors[ERROR_LEVELS.INFO];
    const timestamp = new Date(logEntry.timestamp).toLocaleTimeString('ar-SA');

    console.log(
      `%c[${logEntry.level}] [${logEntry.category}] ${timestamp}`,
      style,
      logEntry.message
    );

    if (logEntry.stack) {
      console.log('Stack:', logEntry.stack);
    }

    if (logEntry.data) {
      console.log('Data:', logEntry.data);
    }
  }

  /**
   * Debug log
   */
  debug(message, data) {
    return this.log({
      level: ERROR_LEVELS.DEBUG,
      category: ERROR_CATEGORIES.UNKNOWN,
      message,
      data,
    });
  }

  /**
   * Info log
   */
  info(message, data) {
    return this.log({
      level: ERROR_LEVELS.INFO,
      category: ERROR_CATEGORIES.UNKNOWN,
      message,
      data,
    });
  }

  /**
   * Warning log
   */
  warn(message, data, category = ERROR_CATEGORIES.UNKNOWN) {
    return this.log({
      level: ERROR_LEVELS.WARN,
      category,
      message,
      data,
    });
  }

  /**
   * Error log
   */
  error(message, error, category = ERROR_CATEGORIES.UNKNOWN) {
    return this.log({
      level: ERROR_LEVELS.ERROR,
      category,
      message,
      stack: error?.stack,
      data: error,
    });
  }

  /**
   * Fatal error log
   */
  fatal(message, error, category = ERROR_CATEGORIES.UNKNOWN) {
    return this.log({
      level: ERROR_LEVELS.FATAL,
      category,
      message,
      stack: error?.stack,
      data: error,
    });
  }

  /**
   * Network error log
   */
  networkError(message, error, data) {
    return this.log({
      level: ERROR_LEVELS.ERROR,
      category: ERROR_CATEGORIES.NETWORK,
      message,
      stack: error?.stack,
      data,
    });
  }

  /**
   * API error log
   */
  apiError(endpoint, error, response) {
    return this.log({
      level: ERROR_LEVELS.ERROR,
      category: ERROR_CATEGORIES.API,
      message: `API Error: ${endpoint}`,
      stack: error?.stack,
      data: {
        endpoint,
        error: error?.message,
        response,
      },
    });
  }

  /**
   * Auth error log
   */
  authError(message, error) {
    return this.log({
      level: ERROR_LEVELS.ERROR,
      category: ERROR_CATEGORIES.AUTH,
      message,
      stack: error?.stack,
      data: error,
    });
  }

  /**
   * Validation error log
   */
  validationError(field, message, data) {
    return this.log({
      level: ERROR_LEVELS.WARN,
      category: ERROR_CATEGORIES.VALIDATION,
      message: `Validation Error: ${field} - ${message}`,
      data,
    });
  }

  /**
   * Get all logs
   */
  getLogs(filter = {}) {
    let filtered = [...this.logs];

    if (filter.level) {
      filtered = filtered.filter(log => log.level === filter.level);
    }

    if (filter.category) {
      filtered = filtered.filter(log => log.category === filter.category);
    }

    if (filter.startDate) {
      filtered = filtered.filter(log => new Date(log.timestamp) >= new Date(filter.startDate));
    }

    if (filter.endDate) {
      filtered = filtered.filter(log => new Date(log.timestamp) <= new Date(filter.endDate));
    }

    return filtered;
  }

  /**
   * Clear all logs
   */
  clearLogs() {
    this.logs = [];
    localStorage.removeItem(STORAGE_KEY);
    console.log('%c✅ Error logs cleared', 'color: #80AA45; font-weight: bold;');
  }

  /**
   * Export logs as JSON
   */
  exportLogs() {
    const dataStr = JSON.stringify(this.logs, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `error-logs-${new Date().toISOString()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  /**
   * Get error statistics
   */
  getStats() {
    const stats = {
      total: this.logs.length,
      byLevel: {},
      byCategory: {},
      last24Hours: 0,
    };

    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);

    this.logs.forEach(log => {
      // Count by level
      stats.byLevel[log.level] = (stats.byLevel[log.level] || 0) + 1;

      // Count by category
      stats.byCategory[log.category] = (stats.byCategory[log.category] || 0) + 1;

      // Count last 24 hours
      if (new Date(log.timestamp) >= oneDayAgo) {
        stats.last24Hours++;
      }
    });

    return stats;
  }
}

// Create singleton instance
const errorLogger = new ErrorLogger();

// Export singleton
export default errorLogger;

// Export convenience functions
export const logDebug = (message, data) => errorLogger.debug(message, data);
export const logInfo = (message, data) => errorLogger.info(message, data);
export const logWarn = (message, data, category) => errorLogger.warn(message, data, category);
export const logError = (message, error, category) => errorLogger.error(message, error, category);
export const logFatal = (message, error, category) => errorLogger.fatal(message, error, category);
export const logNetworkError = (message, error, data) => errorLogger.networkError(message, error, data);
export const logApiError = (endpoint, error, response) => errorLogger.apiError(endpoint, error, response);
export const logAuthError = (message, error) => errorLogger.authError(message, error);
export const logValidationError = (field, message, data) => errorLogger.validationError(field, message, data);

