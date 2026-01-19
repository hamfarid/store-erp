/**
 * Button Components
 * ==================
 * 
 * Reusable button components with variants and states.
 * 
 * Variants:
 * - Primary (emerald)
 * - Secondary (gray)
 * - Danger (red)
 * - Warning (amber)
 * - Success (green)
 * - Outline
 * - Ghost
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * Button Component
 */
const Button = ({
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  fullWidth = false,
  icon: Icon,
  iconPosition = 'left',
  onClick,
  className = '',
  ...props
}) => {
  // Variant styles
  const variants = {
    primary: `
      bg-emerald-500 text-white
      hover:bg-emerald-600 active:bg-emerald-700
      focus:ring-emerald-500/30
      disabled:bg-emerald-300
    `,
    secondary: `
      bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200
      hover:bg-gray-200 dark:hover:bg-gray-600 active:bg-gray-300 dark:active:bg-gray-500
      focus:ring-gray-500/30
      disabled:bg-gray-100 dark:disabled:bg-gray-800
    `,
    danger: `
      bg-red-500 text-white
      hover:bg-red-600 active:bg-red-700
      focus:ring-red-500/30
      disabled:bg-red-300
    `,
    warning: `
      bg-amber-500 text-white
      hover:bg-amber-600 active:bg-amber-700
      focus:ring-amber-500/30
      disabled:bg-amber-300
    `,
    success: `
      bg-green-500 text-white
      hover:bg-green-600 active:bg-green-700
      focus:ring-green-500/30
      disabled:bg-green-300
    `,
    info: `
      bg-blue-500 text-white
      hover:bg-blue-600 active:bg-blue-700
      focus:ring-blue-500/30
      disabled:bg-blue-300
    `,
    outline: `
      border-2 border-emerald-500 text-emerald-500
      hover:bg-emerald-50 dark:hover:bg-emerald-900/20 active:bg-emerald-100
      focus:ring-emerald-500/30
      disabled:border-emerald-300 disabled:text-emerald-300
    `,
    outlineGray: `
      border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200
      hover:bg-gray-50 dark:hover:bg-gray-800 active:bg-gray-100
      focus:ring-gray-500/30
      disabled:border-gray-200 disabled:text-gray-400
    `,
    ghost: `
      text-gray-600 dark:text-gray-300
      hover:bg-gray-100 dark:hover:bg-gray-800 active:bg-gray-200
      focus:ring-gray-500/30
      disabled:text-gray-400
    `,
    link: `
      text-emerald-500
      hover:text-emerald-600 hover:underline
      focus:ring-emerald-500/30
      disabled:text-emerald-300
    `
  };

  // Size styles
  const sizes = {
    xs: 'px-2.5 py-1 text-xs rounded',
    sm: 'px-3 py-1.5 text-sm rounded-md',
    md: 'px-4 py-2 text-sm rounded-lg',
    lg: 'px-5 py-2.5 text-base rounded-lg',
    xl: 'px-6 py-3 text-base rounded-xl'
  };

  // Icon sizes
  const iconSizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
    xl: 'w-5 h-5'
  };

  const isDisabled = disabled || loading;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      className={`
        inline-flex items-center justify-center gap-2
        font-medium
        transition-all duration-200
        focus:outline-none focus:ring-2 focus:ring-offset-2
        disabled:cursor-not-allowed disabled:opacity-60
        ${variants[variant]}
        ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `}
      {...props}
    >
      {/* Loading spinner */}
      {loading && (
        <Loader2 className={`${iconSizes[size]} animate-spin`} />
      )}

      {/* Left icon */}
      {Icon && iconPosition === 'left' && !loading && (
        <Icon className={iconSizes[size]} />
      )}

      {/* Button text */}
      {children}

      {/* Right icon */}
      {Icon && iconPosition === 'right' && !loading && (
        <Icon className={iconSizes[size]} />
      )}
    </button>
  );
};

/**
 * Icon Button (square button with icon only)
 */
export const IconButton = ({
  icon: Icon,
  variant = 'ghost',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  title,
  className = '',
  ...props
}) => {
  const variants = {
    primary: 'bg-emerald-500 text-white hover:bg-emerald-600',
    secondary: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600',
    danger: 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20',
    ghost: 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
  };

  const sizes = {
    xs: 'w-6 h-6',
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12'
  };

  const iconSizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || loading}
      title={title}
      className={`
        inline-flex items-center justify-center
        rounded-lg
        transition-colors duration-200
        focus:outline-none focus:ring-2 focus:ring-emerald-500/30
        disabled:cursor-not-allowed disabled:opacity-50
        ${variants[variant]}
        ${sizes[size]}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <Loader2 className={`${iconSizes[size]} animate-spin`} />
      ) : (
        Icon && <Icon className={iconSizes[size]} />
      )}
    </button>
  );
};

/**
 * Button Group
 */
export const ButtonGroup = ({
  children,
  className = ''
}) => (
  <div className={`inline-flex rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 ${className}`}>
    {React.Children.map(children, (child, index) => {
      if (!React.isValidElement(child)) return child;
      
      return React.cloneElement(child, {
        className: `
          ${child.props.className || ''}
          rounded-none
          ${index > 0 ? 'border-l border-gray-200 dark:border-gray-700' : ''}
        `
      });
    })}
  </div>
);

/**
 * Floating Action Button
 */
export const FAB = ({
  icon: Icon,
  onClick,
  variant = 'primary',
  size = 'lg',
  position = 'bottom-right',
  tooltip,
  className = ''
}) => {
  const variants = {
    primary: 'bg-emerald-500 text-white hover:bg-emerald-600 shadow-emerald-500/30',
    secondary: 'bg-gray-800 text-white hover:bg-gray-700 shadow-gray-800/30'
  };

  const sizes = {
    md: 'w-12 h-12',
    lg: 'w-14 h-14',
    xl: 'w-16 h-16'
  };

  const iconSizes = {
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-7 h-7'
  };

  const positions = {
    'bottom-right': 'bottom-6 right-6 rtl:right-auto rtl:left-6',
    'bottom-left': 'bottom-6 left-6 rtl:left-auto rtl:right-6',
    'bottom-center': 'bottom-6 left-1/2 -translate-x-1/2'
  };

  return (
    <button
      type="button"
      onClick={onClick}
      title={tooltip}
      className={`
        fixed z-40
        ${positions[position]}
        ${sizes[size]}
        ${variants[variant]}
        rounded-full shadow-lg
        flex items-center justify-center
        transition-all duration-200
        hover:scale-105 active:scale-95
        focus:outline-none focus:ring-4 focus:ring-emerald-500/30
        ${className}
      `}
    >
      {Icon && <Icon className={iconSizes[size]} />}
    </button>
  );
};

export default Button;
