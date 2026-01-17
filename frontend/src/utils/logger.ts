/**
 * Comprehensive Logging System for Store Frontend
 * ================================================
 * 
 * Features:
 * - Multiple log levels with color coding
 * - API error logging
 * - User action tracking
 * - Performance monitoring
 * - Error boundary integration
 * - Console-only output (no file storage)
 */

export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
  CRITICAL = 'CRITICAL'
}

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: Record<string, any>;
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
  user?: {
    id?: number;
    username?: string;
  };
  page?: {
    url: string;
    title: string;
  };
}

class Logger {
  private name: string;
  private minLevel: LogLevel;
  
  // ANSI color codes for console
  private static COLORS = {
    DEBUG: '\x1b[36m',      // Cyan
    INFO: '\x1b[32m',       // Green
    WARN: '\x1b[33m',       // Yellow
    ERROR: '\x1b[31m',      // Red
    CRITICAL: '\x1b[35m',   // Magenta
    RESET: '\x1b[0m'        // Reset
  };
  
  private static LEVEL_PRIORITY = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
    CRITICAL: 4
  };
  
  constructor(name: string = 'store-frontend', minLevel: LogLevel = LogLevel.INFO) {
    this.name = name;
    this.minLevel = minLevel;
  }
  
  /**
   * Build structured log entry
   */
  private buildLogEntry(
    level: LogLevel,
    message: string,
    context?: Record<string, any>,
    error?: Error
  ): LogEntry {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
      page: {
        url: window.location.href,
        title: document.title
      }
    };
    
    // Add user info if available (from localStorage/sessionStorage)
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        entry.user = {
          id: user.id,
          username: user.username
        };
      } catch {}
    }
    
    // Add error info
    if (error) {
      entry.error = {
        name: error.name,
        message: error.message,
        stack: error.stack
      };
    }
    
    return entry;
  }
  
  /**
   * Check if log level should be output
   */
  private shouldLog(level: LogLevel): boolean {
    return Logger.LEVEL_PRIORITY[level] >= Logger.LEVEL_PRIORITY[this.minLevel];
  }
  
  /**
   * Output log to console with formatting
   */
  private output(entry: LogEntry) {
    if (!this.shouldLog(entry.level)) {
      return;
    }
    
    const color = Logger.COLORS[entry.level];
    const reset = Logger.COLORS.RESET;
    
    const prefix = `${color}[${entry.level}]${reset} ${entry.timestamp} | ${this.name} |`;
    
    // Use appropriate console method
    switch (entry.level) {
      case LogLevel.DEBUG:
        console.debug(prefix, entry.message, entry);
        break;
      case LogLevel.INFO:
        console.info(prefix, entry.message, entry);
        break;
      case LogLevel.WARN:
        console.warn(prefix, entry.message, entry);
        break;
      case LogLevel.ERROR:
      case LogLevel.CRITICAL:
        console.error(prefix, entry.message, entry);
        break;
    }
  }
  
  /**
   * Log debug message
   */
  debug(message: string, context?: Record<string, any>) {
    const entry = this.buildLogEntry(LogLevel.DEBUG, message, context);
    this.output(entry);
  }
  
  /**
   * Log info message
   */
  info(message: string, context?: Record<string, any>) {
    const entry = this.buildLogEntry(LogLevel.INFO, message, context);
    this.output(entry);
  }
  
  /**
   * Log warning message
   */
  warn(message: string, context?: Record<string, any>) {
    const entry = this.buildLogEntry(LogLevel.WARN, message, context);
    this.output(entry);
  }
  
  /**
   * Log error message
   */
  error(message: string, error?: Error, context?: Record<string, any>) {
    const entry = this.buildLogEntry(LogLevel.ERROR, message, context, error);
    this.output(entry);
  }
  
  /**
   * Log critical message
   */
  critical(message: string, error?: Error, context?: Record<string, any>) {
    const entry = this.buildLogEntry(LogLevel.CRITICAL, message, context, error);
    this.output(entry);
  }
  
  /**
   * Log API request
   */
  apiRequest(method: string, url: string, data?: any) {
    this.info('API Request', {
      type: 'api_request',
      method,
      url,
      data
    });
  }
  
  /**
   * Log API response
   */
  apiResponse(method: string, url: string, status: number, duration: number) {
    const level = status >= 400 ? LogLevel.ERROR : LogLevel.INFO;
    const entry = this.buildLogEntry(level, 'API Response', {
      type: 'api_response',
      method,
      url,
      status,
      duration_ms: duration
    });
    this.output(entry);
  }
  
  /**
   * Log API error
   */
  apiError(method: string, url: string, error: Error) {
    this.error('API Error', error, {
      type: 'api_error',
      method,
      url
    });
  }
  
  /**
   * Log user action for audit trail
   */
  audit(action: string, resource: string, resourceId?: number, data?: any) {
    this.info('User Action', {
      type: 'audit',
      action,
      resource,
      resourceId,
      data
    });
  }
  
  /**
   * Log performance metric
   */
  performance(metric: string, value: number, unit: string = 'ms') {
    this.info('Performance Metric', {
      type: 'performance',
      metric,
      value,
      unit
    });
  }
  
  /**
   * Set minimum log level
   */
  setLevel(level: LogLevel) {
    this.minLevel = level;
  }
}

// Global logger instance
export const logger = new Logger('store-frontend', LogLevel.INFO);

/**
 * Create a named logger instance
 */
export function getLogger(name: string, minLevel?: LogLevel): Logger {
  return new Logger(name, minLevel);
}

/**
 * Initialize logging with configuration
 */
export function initLogging(config?: { level?: LogLevel }) {
  if (config?.level) {
    logger.setLevel(config.level);
  }
  
  // Log application startup
  logger.info('Application Started', {
    environment: import.meta.env.MODE,
    version: import.meta.env.VITE_APP_VERSION || '1.0.0'
  });
  
  // Add global error handler
  window.addEventListener('error', (event) => {
    logger.critical('Uncaught Error', event.error, {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno
    });
  });
  
  // Add unhandled promise rejection handler
  window.addEventListener('unhandledrejection', (event) => {
    logger.critical('Unhandled Promise Rejection', undefined, {
      reason: event.reason
    });
  });
  
  return logger;
}

/**
 * Axios interceptor for automatic API logging
 */
export function setupAxiosLogging(axiosInstance: any) {
  // Request interceptor
  axiosInstance.interceptors.request.use(
    (config: any) => {
      config.metadata = { startTime: Date.now() };
      logger.apiRequest(config.method.toUpperCase(), config.url, config.data);
      return config;
    },
    (error: Error) => {
      logger.apiError('REQUEST', 'unknown', error);
      return Promise.reject(error);
    }
  );
  
  // Response interceptor
  axiosInstance.interceptors.response.use(
    (response: any) => {
      const duration = Date.now() - response.config.metadata.startTime;
      logger.apiResponse(
        response.config.method.toUpperCase(),
        response.config.url,
        response.status,
        duration
      );
      return response;
    },
    (error: any) => {
      if (error.response) {
        const duration = Date.now() - error.config.metadata.startTime;
        logger.apiResponse(
          error.config.method.toUpperCase(),
          error.config.url,
          error.response.status,
          duration
        );
      } else {
        logger.apiError(
          error.config?.method?.toUpperCase() || 'UNKNOWN',
          error.config?.url || 'unknown',
          error
        );
      }
      return Promise.reject(error);
    }
  );
}

/**
 * React Error Boundary logger
 */
export function logErrorBoundary(error: Error, errorInfo: any) {
  logger.critical('React Error Boundary', error, {
    componentStack: errorInfo.componentStack
  });
}

export default logger;
