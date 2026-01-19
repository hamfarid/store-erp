import activityLogService from '../services/activityLogService';
import store from '../store';
import router from './index';

/**
 * Initialize global error handler for the application
 * Handles errors and redirects users to appropriate error pages
 */
export function setupErrorHandler() {
  // Handle routing errors (404)
  router.onError((error) => {
    console.error('Router error:', error);

    // Log error in activity log
    logRouterError(error);

    // Redirect user to 500 error page if it's a routing error
    router.push({
      name: 'error',
      params: {
        errorCode: 500,
        errorMessage: 'An error occurred while loading the page',
        errorDetails: error.message
      }
    });
  });

  // Add global error handler for window
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);

    // Log error in activity log
    logGlobalError(event.error);

    // Prevent default browser behavior
    event.preventDefault();

    // Redirect user to 500 error page
    router.push({
      name: 'error',
      params: {
        errorCode: 500,
        errorMessage: 'An unexpected error occurred in the application',
        errorDetails: event.error ? event.error.stack : 'Error details not available'
      }
    });

    return true;
  });

  // Add unhandled promise rejection handler
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);

    // Log error in activity log
    logPromiseError(event.reason);

    // Prevent default browser behavior
    event.preventDefault();

    // Redirect user to 500 error page
    router.push({
      name: 'error',
      params: {
        errorCode: 500,
        errorMessage: 'An unexpected error occurred while processing the request',
        errorDetails: event.reason ? (event.reason.stack || event.reason.message) : 'Error details not available'
      }
    });

    return true;
  });

  // Add network error handler
  window.addEventListener('offline', () => {
    console.warn('Network connection lost');

    // Log connection loss event in activity log
    logNetworkError('offline');

    // Show notification to user
    store.dispatch('notifications/showNotification', {
      type: 'warning',
      message: 'Internet connection lost. Some features may not work correctly.'
    });
  });

  // Add connection restoration handler
  window.addEventListener('online', () => {
    console.info('Network connection restored');

    // Log connection restoration event in activity log
    logNetworkError('online');

    // Show notification to user
    store.dispatch('notifications/showNotification', {
      type: 'success',
      message: 'Internet connection restored.'
    });
  });

  // Add server error handler (504)
  // Called manually from API services when 504 error is detected
  window.handleGatewayTimeout = () => {
    console.error('Gateway timeout (504) detected');

    // Log 504 error in activity log
    logHttpError(504, window.location.pathname);

    // Redirect user to 504 error page
    router.push({
      name: 'error',
      params: {
        errorCode: 504,
        errorMessage: 'Gateway Timeout',
        errorDetails: 'The server did not respond in time. Please try again later.'
      }
    });
  };
}

/**
 * Log routing error in activity log
 * @param {Error} error - Error object
 */
function logRouterError(error) {
  try {
    const currentUser = store.getters['auth/currentUser'];
    const userId = currentUser ? currentUser.id : null;

    activityLogService.logSystemEvent({
      event_type: 'router_error',
      details: {
        error_message: error.message,
        error_stack: error.stack,
        url: window.location.href,
        route: router.currentRoute.value,
        user_agent: navigator.userAgent,
        timestamp: new Date().toISOString()
      },
      user_id: userId
    }).catch(err => {
      console.error('Failed to log router error:', err);
    });
  } catch (err) {
    console.error('Error in logRouterError:', err);
  }
}

/**
 * Log global error in activity log
 * @param {Error} error - Error object
 */
function logGlobalError(error) {
  try {
    const currentUser = store.getters['auth/currentUser'];
    const userId = currentUser ? currentUser.id : null;

    activityLogService.logSystemEvent({
      event_type: 'global_error',
      details: {
        error_message: error.message,
        error_stack: error.stack,
        url: window.location.href,
        route: router.currentRoute.value,
        user_agent: navigator.userAgent,
        timestamp: new Date().toISOString()
      },
      user_id: userId
    }).catch(err => {
      console.error('Failed to log global error:', err);
    });
  } catch (err) {
    console.error('Error in logGlobalError:', err);
  }
}

/**
 * Log unhandled promise rejection in activity log
 * @param {Error|any} reason - Promise rejection reason
 */
function logPromiseError(reason) {
  try {
    const currentUser = store.getters['auth/currentUser'];
    const userId = currentUser ? currentUser.id : null;

    activityLogService.logSystemEvent({
      event_type: 'unhandled_promise_rejection',
      details: {
        error_message: reason.message || String(reason),
        error_stack: reason.stack || 'No stack trace available',
        url: window.location.href,
        route: router.currentRoute.value,
        user_agent: navigator.userAgent,
        timestamp: new Date().toISOString()
      },
      user_id: userId
    }).catch(err => {
      console.error('Failed to log promise error:', err);
    });
  } catch (err) {
    console.error('Error in logPromiseError:', err);
  }
}

/**
 * Log network error in activity log
 * @param {string} eventType - Type of network event ('online' or 'offline')
 */
function logNetworkError(eventType) {
  try {
    const currentUser = store.getters['auth/currentUser'];
    const userId = currentUser ? currentUser.id : null;

    activityLogService.logSystemEvent({
      event_type: 'network_error',
      details: {
        event_type: eventType,
        url: window.location.href,
        route: router.currentRoute.value,
        user_agent: navigator.userAgent,
        timestamp: new Date().toISOString()
      },
      user_id: userId
    }).catch(err => {
      console.error('Failed to log network error:', err);
    });
  } catch (err) {
    console.error('Error in logNetworkError:', err);
  }
}

/**
 * Log HTTP error in activity log
 * @param {number} statusCode - HTTP status code
 * @param {string} url - Request URL
 * @param {Object|null} requestData - Request data (optional)
 */
function logHttpError(statusCode, url, requestData = null) {
  try {
    const currentUser = store.getters['auth/currentUser'];
    const userId = currentUser ? currentUser.id : null;

    activityLogService.logSystemEvent({
      event_type: 'http_error',
      details: {
        status_code: statusCode,
        url: url,
        request_data: requestData,
        user_agent: navigator.userAgent,
        timestamp: new Date().toISOString()
      },
      user_id: userId
    }).catch(err => {
      console.error('Failed to log HTTP error:', err);
    });
  } catch (err) {
    console.error('Error in logHttpError:', err);
  }
}

/**
 * Export HTTP error logging function for external use
 * @param {number} statusCode - HTTP status code
 * @param {string} url - Request URL
 * @param {Object|null} requestData - Request data (optional)
 */
export function logHttpErrorEvent(statusCode, url, requestData = null) {
  logHttpError(statusCode, url, requestData);
}
