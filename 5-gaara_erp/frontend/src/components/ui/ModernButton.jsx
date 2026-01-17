/**
 * Modern Button Components
 * 
 * Beautiful, reusable button components with various styles and states.
 */

import React from 'react';
import { Loader2 } from 'lucide-react';

// ============================================================================
// Base Button Component
// ============================================================================

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'right',
  isLoading = false,
  disabled = false,
  fullWidth = false,
  className = '',
  onClick,
  type = 'button',
  ...props
}) => {
  // Variant styles
  const variants = {
    primary: 'bg-gradient-to-l from-teal-500 to-teal-600 text-white shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40',
    secondary: 'bg-white text-gray-700 border-2 border-gray-200 hover:bg-gray-50 hover:border-gray-300',
    accent: 'bg-gradient-to-l from-amber-500 to-amber-600 text-white shadow-lg shadow-amber-500/30 hover:shadow-xl hover:shadow-amber-500/40',
    danger: 'bg-gradient-to-l from-rose-500 to-rose-600 text-white shadow-lg shadow-rose-500/30 hover:shadow-xl hover:shadow-rose-500/40',
    success: 'bg-gradient-to-l from-emerald-500 to-emerald-600 text-white shadow-lg shadow-emerald-500/30 hover:shadow-xl hover:shadow-emerald-500/40',
    ghost: 'bg-transparent text-gray-600 hover:bg-gray-100',
    outline: 'bg-transparent border-2 border-teal-500 text-teal-600 hover:bg-teal-50',
    link: 'bg-transparent text-teal-600 hover:text-teal-700 hover:underline p-0',
  };

  // Size styles
  const sizes = {
    xs: 'px-3 py-1.5 text-xs',
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-2.5 text-sm',
    lg: 'px-8 py-3 text-base',
    xl: 'px-10 py-4 text-lg',
  };

  // Icon sizes
  const iconSizes = {
    xs: 14,
    sm: 16,
    md: 18,
    lg: 20,
    xl: 24,
  };

  const baseStyles = `
    inline-flex items-center justify-center gap-2 font-semibold rounded-xl
    transition-all duration-300 ease-out
    disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500
  `;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`
        ${baseStyles}
        ${variants[variant]}
        ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `}
      {...props}
    >
      {isLoading ? (
        <>
          <Loader2 size={iconSizes[size]} className="animate-spin" />
          <span>جاري التحميل...</span>
        </>
      ) : (
        <>
          {Icon && iconPosition === 'right' && <Icon size={iconSizes[size]} />}
          {children}
          {Icon && iconPosition === 'left' && <Icon size={iconSizes[size]} />}
        </>
      )}
    </button>
  );
};

// ============================================================================
// Icon Button Component
// ============================================================================

export const IconButton = ({
  icon: Icon,
  variant = 'ghost',
  size = 'md',
  tooltip,
  isLoading = false,
  disabled = false,
  className = '',
  onClick,
  ...props
}) => {
  const variants = {
    primary: 'bg-teal-500 text-white hover:bg-teal-600',
    secondary: 'bg-gray-100 text-gray-600 hover:bg-gray-200',
    ghost: 'bg-transparent text-gray-500 hover:bg-gray-100',
    danger: 'bg-transparent text-gray-500 hover:bg-rose-50 hover:text-rose-600',
    success: 'bg-transparent text-gray-500 hover:bg-emerald-50 hover:text-emerald-600',
  };

  const sizes = {
    xs: 'w-7 h-7',
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  const iconSizes = {
    xs: 14,
    sm: 16,
    md: 18,
    lg: 22,
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      title={tooltip}
      className={`
        ${sizes[size]}
        ${variants[variant]}
        inline-flex items-center justify-center rounded-xl
        transition-all duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500
        ${className}
      `}
      {...props}
    >
      {isLoading ? (
        <Loader2 size={iconSizes[size]} className="animate-spin" />
      ) : (
        <Icon size={iconSizes[size]} />
      )}
    </button>
  );
};

// ============================================================================
// Button Group Component
// ============================================================================

export const ButtonGroup = ({ children, className = '' }) => (
  <div className={`inline-flex rounded-xl overflow-hidden border border-gray-200 ${className}`}>
    {React.Children.map(children, (child, index) => (
      <div className={index > 0 ? 'border-r border-gray-200' : ''}>
        {React.cloneElement(child, {
          className: `${child.props.className || ''} rounded-none border-0`,
        })}
      </div>
    ))}
  </div>
);

// ============================================================================
// Floating Action Button
// ============================================================================

export const FAB = ({
  icon: Icon,
  onClick,
  variant = 'primary',
  size = 'md',
  position = 'bottom-left',
  tooltip,
  className = '',
  ...props
}) => {
  const variants = {
    primary: 'bg-gradient-to-br from-teal-500 to-teal-600 text-white shadow-xl shadow-teal-500/40',
    accent: 'bg-gradient-to-br from-amber-500 to-amber-600 text-white shadow-xl shadow-amber-500/40',
  };

  const sizes = {
    sm: 'w-12 h-12',
    md: 'w-14 h-14',
    lg: 'w-16 h-16',
  };

  const iconSizes = {
    sm: 20,
    md: 24,
    lg: 28,
  };

  const positions = {
    'bottom-left': 'fixed bottom-6 left-6',
    'bottom-right': 'fixed bottom-6 right-6',
    'top-left': 'fixed top-6 left-6',
    'top-right': 'fixed top-6 right-6',
  };

  return (
    <button
      onClick={onClick}
      title={tooltip}
      className={`
        ${sizes[size]}
        ${variants[variant]}
        ${positions[position]}
        rounded-full flex items-center justify-center
        hover:scale-110 hover:shadow-2xl
        transition-all duration-300 ease-out
        z-50
        ${className}
      `}
      {...props}
    >
      <Icon size={iconSizes[size]} />
    </button>
  );
};

// ============================================================================
// Split Button Component
// ============================================================================

export const SplitButton = ({
  children,
  icon: Icon,
  options = [],
  variant = 'primary',
  size = 'md',
  className = '',
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className={`relative inline-flex ${className}`}>
      <Button variant={variant} size={size} icon={Icon} className="rounded-l-none">
        {children}
      </Button>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          px-2 border-r border-white/20 rounded-r-xl
          ${variant === 'primary' ? 'bg-teal-600 hover:bg-teal-700 text-white' : ''}
          ${variant === 'secondary' ? 'bg-gray-100 hover:bg-gray-200 text-gray-700 border-l border-gray-200' : ''}
        `}
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      {isOpen && (
        <div className="absolute top-full left-0 mt-1 w-48 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-10">
          {options.map((option, index) => (
            <button
              key={index}
              onClick={() => { option.onClick(); setIsOpen(false); }}
              className="w-full flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-gray-700 text-sm"
            >
              {option.icon && <option.icon size={16} />}
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default Button;



