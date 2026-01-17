/**
 * P3.99: Toggle/Switch Component
 * 
 * Toggle switches for boolean settings.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type ToggleSize = 'sm' | 'md' | 'lg';
type ToggleColor = 'blue' | 'green' | 'indigo' | 'purple' | 'red';

interface ToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  size?: ToggleSize;
  color?: ToggleColor;
  label?: string;
  description?: string;
  labelPosition?: 'left' | 'right';
  className?: string;
  id?: string;
}

// =============================================================================
// Configuration
// =============================================================================

const sizeConfig: Record<ToggleSize, { track: string; thumb: string; translate: string }> = {
  sm: {
    track: 'w-8 h-4',
    thumb: 'w-3 h-3',
    translate: 'translate-x-4',
  },
  md: {
    track: 'w-11 h-6',
    thumb: 'w-5 h-5',
    translate: 'translate-x-5',
  },
  lg: {
    track: 'w-14 h-7',
    thumb: 'w-6 h-6',
    translate: 'translate-x-7',
  },
};

const colorConfig: Record<ToggleColor, string> = {
  blue: 'bg-blue-600',
  green: 'bg-green-600',
  indigo: 'bg-indigo-600',
  purple: 'bg-purple-600',
  red: 'bg-red-600',
};

// =============================================================================
// Toggle Component
// =============================================================================

export const Toggle: React.FC<ToggleProps> = ({
  checked,
  onChange,
  disabled = false,
  size = 'md',
  color = 'indigo',
  label,
  description,
  labelPosition = 'right',
  className = '',
  id,
}) => {
  const sizes = sizeConfig[size];
  const activeColor = colorConfig[color];
  const toggleId = id || `toggle-${Math.random().toString(36).substr(2, 9)}`;

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (!disabled) {
        onChange(!checked);
      }
    }
  };

  const toggle = (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-labelledby={label ? `${toggleId}-label` : undefined}
      disabled={disabled}
      onClick={() => !disabled && onChange(!checked)}
      onKeyDown={handleKeyDown}
      className={`
        relative inline-flex flex-shrink-0 cursor-pointer rounded-full
        border-2 border-transparent transition-colors duration-200 ease-in-out
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
        ${sizes.track}
        ${checked ? activeColor : 'bg-gray-200'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <span
        className={`
          pointer-events-none inline-block rounded-full bg-white shadow
          transform ring-0 transition duration-200 ease-in-out
          ${sizes.thumb}
          ${checked ? sizes.translate : 'translate-x-0'}
        `}
      />
    </button>
  );

  if (!label) {
    return toggle;
  }

  return (
    <div className={`flex items-start gap-3 ${labelPosition === 'left' ? 'flex-row-reverse' : ''} ${className}`}>
      {toggle}
      <div className="flex-1">
        <label
          id={`${toggleId}-label`}
          htmlFor={toggleId}
          className={`text-sm font-medium text-gray-900 ${disabled ? 'opacity-50' : 'cursor-pointer'}`}
          onClick={() => !disabled && onChange(!checked)}
        >
          {label}
        </label>
        {description && (
          <p className="text-sm text-gray-500 mt-0.5">{description}</p>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Toggle Group
// =============================================================================

interface ToggleOption {
  id: string;
  label: string;
  description?: string;
  checked: boolean;
}

interface ToggleGroupProps {
  options: ToggleOption[];
  onChange: (id: string, checked: boolean) => void;
  disabled?: boolean;
  size?: ToggleSize;
  color?: ToggleColor;
  className?: string;
}

export const ToggleGroup: React.FC<ToggleGroupProps> = ({
  options,
  onChange,
  disabled = false,
  size = 'md',
  color = 'indigo',
  className = '',
}) => {
  return (
    <div className={`space-y-4 ${className}`}>
      {options.map((option) => (
        <Toggle
          key={option.id}
          id={option.id}
          checked={option.checked}
          onChange={(checked) => onChange(option.id, checked)}
          label={option.label}
          description={option.description}
          disabled={disabled}
          size={size}
          color={color}
        />
      ))}
    </div>
  );
};

// =============================================================================
// Toggle Card
// =============================================================================

interface ToggleCardProps extends ToggleProps {
  icon?: React.ReactNode;
}

export const ToggleCard: React.FC<ToggleCardProps> = ({
  icon,
  label,
  description,
  checked,
  onChange,
  disabled = false,
  size = 'md',
  color = 'indigo',
  className = '',
}) => {
  return (
    <div
      className={`
        flex items-center justify-between p-4 bg-white border rounded-lg
        ${checked ? 'border-indigo-200 bg-indigo-50' : 'border-gray-200'}
        ${disabled ? 'opacity-50' : 'cursor-pointer hover:bg-gray-50'}
        ${className}
      `}
      onClick={() => !disabled && onChange(!checked)}
    >
      <div className="flex items-center gap-3">
        {icon && (
          <div className={`flex-shrink-0 ${checked ? 'text-indigo-600' : 'text-gray-400'}`}>
            {icon}
          </div>
        )}
        <div>
          <p className="text-sm font-medium text-gray-900">{label}</p>
          {description && (
            <p className="text-sm text-gray-500">{description}</p>
          )}
        </div>
      </div>
      <Toggle
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        size={size}
        color={color}
      />
    </div>
  );
};

// =============================================================================
// Checkbox Toggle (Alternative Style)
// =============================================================================

interface CheckboxToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
  description?: string;
  disabled?: boolean;
  className?: string;
}

export const CheckboxToggle: React.FC<CheckboxToggleProps> = ({
  checked,
  onChange,
  label,
  description,
  disabled = false,
  className = '',
}) => {
  return (
    <label className={`flex items-start gap-3 ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} ${className}`}>
      <div className="flex items-center h-5">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          disabled={disabled}
          className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
        />
      </div>
      <div className="flex-1">
        <span className="text-sm font-medium text-gray-900">{label}</span>
        {description && (
          <p className="text-sm text-gray-500">{description}</p>
        )}
      </div>
    </label>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Toggle;

