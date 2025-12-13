/**
 * P3.98: Alert/Notification Banner Component
 * 
 * Inline alerts and banners for status messages.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type AlertVariant = 'info' | 'success' | 'warning' | 'error';

interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  children: React.ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

// =============================================================================
// Configuration
// =============================================================================

const variantStyles: Record<AlertVariant, { bg: string; border: string; icon: string; title: string }> = {
  info: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    icon: 'text-blue-500',
    title: 'text-blue-800',
  },
  success: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    icon: 'text-green-500',
    title: 'text-green-800',
  },
  warning: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
    icon: 'text-yellow-500',
    title: 'text-yellow-800',
  },
  error: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    icon: 'text-red-500',
    title: 'text-red-800',
  },
};

const defaultIcons: Record<AlertVariant, React.ReactNode> = {
  info: (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
    </svg>
  ),
  success: (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  ),
  warning: (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  ),
  error: (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
    </svg>
  ),
};

// =============================================================================
// Alert Component
// =============================================================================

export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  dismissible = false,
  onDismiss,
  icon,
  action,
  className = '',
}) => {
  const styles = variantStyles[variant];
  const displayIcon = icon ?? defaultIcons[variant];

  return (
    <div
      className={`
        rounded-lg border p-4
        ${styles.bg} ${styles.border}
        ${className}
      `}
      role="alert"
    >
      <div className="flex">
        {displayIcon && (
          <div className={`flex-shrink-0 ${styles.icon}`}>
            {displayIcon}
          </div>
        )}
        <div className="mr-3 flex-1">
          {title && (
            <h3 className={`text-sm font-medium ${styles.title}`}>
              {title}
            </h3>
          )}
          <div className={`text-sm ${title ? 'mt-1' : ''} text-gray-700`}>
            {children}
          </div>
          {action && (
            <div className="mt-3">
              {action}
            </div>
          )}
        </div>
        {dismissible && (
          <button
            type="button"
            onClick={onDismiss}
            className={`-mx-1.5 -my-1.5 mr-auto rounded-lg p-1.5 inline-flex h-8 w-8 hover:bg-black/5 ${styles.icon}`}
          >
            <span className="sr-only">إغلاق</span>
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Banner Component
// =============================================================================

interface BannerProps {
  variant?: AlertVariant;
  children: React.ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
  sticky?: boolean;
  className?: string;
}

export const Banner: React.FC<BannerProps> = ({
  variant = 'info',
  children,
  dismissible = false,
  onDismiss,
  sticky = false,
  className = '',
}) => {
  const bgColors: Record<AlertVariant, string> = {
    info: 'bg-blue-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-500',
    error: 'bg-red-600',
  };

  return (
    <div
      className={`
        ${bgColors[variant]} text-white py-2 px-4
        ${sticky ? 'sticky top-0 z-50' : ''}
        ${className}
      `}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex-1 text-center text-sm font-medium">
          {children}
        </div>
        {dismissible && (
          <button
            type="button"
            onClick={onDismiss}
            className="p-1 rounded hover:bg-white/20"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Toast Alert (Floating)
// =============================================================================

interface ToastAlertProps extends AlertProps {
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
  autoClose?: number;
}

export const ToastAlert: React.FC<ToastAlertProps> = ({
  position = 'top-left',
  autoClose,
  onDismiss,
  ...props
}) => {
  React.useEffect(() => {
    if (autoClose && onDismiss) {
      const timer = setTimeout(onDismiss, autoClose);
      return () => clearTimeout(timer);
    }
  }, [autoClose, onDismiss]);

  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
  };

  return (
    <div className={`fixed ${positionClasses[position]} z-50 max-w-sm w-full shadow-lg`}>
      <Alert {...props} dismissible onDismiss={onDismiss} />
    </div>
  );
};

// =============================================================================
// Alert List
// =============================================================================

interface AlertItem {
  id: string;
  variant: AlertVariant;
  title?: string;
  message: string;
}

interface AlertListProps {
  alerts: AlertItem[];
  onDismiss?: (id: string) => void;
  className?: string;
}

export const AlertList: React.FC<AlertListProps> = ({
  alerts,
  onDismiss,
  className = '',
}) => {
  if (alerts.length === 0) return null;

  return (
    <div className={`space-y-3 ${className}`}>
      {alerts.map((alert) => (
        <Alert
          key={alert.id}
          variant={alert.variant}
          title={alert.title}
          dismissible={!!onDismiss}
          onDismiss={() => onDismiss?.(alert.id)}
        >
          {alert.message}
        </Alert>
      ))}
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Alert;

