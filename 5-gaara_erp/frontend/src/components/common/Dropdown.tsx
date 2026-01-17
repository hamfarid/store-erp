/**
 * P3.88: Dropdown Menu Component
 * 
 * Accessible dropdown menu with keyboard navigation.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';

// =============================================================================
// Types
// =============================================================================

type DropdownPosition = 'bottom-start' | 'bottom-end' | 'top-start' | 'top-end';

interface DropdownItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  danger?: boolean;
  divider?: boolean;
  onClick?: () => void;
}

interface DropdownProps {
  trigger: React.ReactElement;
  items: DropdownItem[];
  position?: DropdownPosition;
  className?: string;
  menuClassName?: string;
  disabled?: boolean;
  closeOnClick?: boolean;
}

// =============================================================================
// Dropdown Component
// =============================================================================

export const Dropdown: React.FC<DropdownProps> = ({
  trigger,
  items,
  position = 'bottom-end',
  className = '',
  menuClassName = '',
  disabled = false,
  closeOnClick = true,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [coords, setCoords] = useState({ top: 0, left: 0 });
  const [focusedIndex, setFocusedIndex] = useState(-1);
  
  const triggerRef = useRef<HTMLDivElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  // Calculate position
  const updatePosition = useCallback(() => {
    if (!triggerRef.current) return;
    
    const rect = triggerRef.current.getBoundingClientRect();
    const menuHeight = menuRef.current?.offsetHeight || 200;
    const menuWidth = menuRef.current?.offsetWidth || 200;
    
    let top = 0;
    let left = 0;
    
    switch (position) {
      case 'bottom-start':
        top = rect.bottom + window.scrollY + 4;
        left = rect.left + window.scrollX;
        break;
      case 'bottom-end':
        top = rect.bottom + window.scrollY + 4;
        left = rect.right + window.scrollX - menuWidth;
        break;
      case 'top-start':
        top = rect.top + window.scrollY - menuHeight - 4;
        left = rect.left + window.scrollX;
        break;
      case 'top-end':
        top = rect.top + window.scrollY - menuHeight - 4;
        left = rect.right + window.scrollX - menuWidth;
        break;
    }
    
    setCoords({ top, left });
  }, [position]);

  // Toggle dropdown
  const toggle = useCallback(() => {
    if (disabled) return;
    setIsOpen(prev => !prev);
    setFocusedIndex(-1);
  }, [disabled]);

  // Handle click outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        menuRef.current && !menuRef.current.contains(e.target as Node) &&
        triggerRef.current && !triggerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      updatePosition();
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, updatePosition]);

  // Handle keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    const enabledItems = items.filter(item => !item.disabled && !item.divider);
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex(prev => 
          prev < enabledItems.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex(prev => 
          prev > 0 ? prev - 1 : enabledItems.length - 1
        );
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (focusedIndex >= 0 && enabledItems[focusedIndex]) {
          enabledItems[focusedIndex].onClick?.();
          if (closeOnClick) setIsOpen(false);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        break;
      case 'Tab':
        setIsOpen(false);
        break;
    }
  }, [items, focusedIndex, closeOnClick]);

  // Handle item click
  const handleItemClick = useCallback((item: DropdownItem) => {
    if (item.disabled) return;
    item.onClick?.();
    if (closeOnClick) setIsOpen(false);
  }, [closeOnClick]);

  // Clone trigger with ref and onClick
  const triggerElement = React.cloneElement(trigger, {
    onClick: (e: React.MouseEvent) => {
      trigger.props.onClick?.(e);
      toggle();
    },
    'aria-haspopup': 'true',
    'aria-expanded': isOpen,
  });

  return (
    <div className={`relative inline-block ${className}`}>
      <div ref={triggerRef}>
        {triggerElement}
      </div>

      {isOpen && createPortal(
        <div
          ref={menuRef}
          role="menu"
          aria-orientation="vertical"
          className={`
            fixed z-50
            min-w-[180px]
            bg-white rounded-lg shadow-lg
            border border-gray-200
            py-1
            ${menuClassName}
          `}
          style={{ top: coords.top, left: coords.left }}
          onKeyDown={handleKeyDown}
          dir="rtl"
        >
          {items.map((item, index) => {
            if (item.divider) {
              return (
                <div
                  key={item.id}
                  className="my-1 border-t border-gray-200"
                  role="separator"
                />
              );
            }

            const enabledIndex = items
              .slice(0, index)
              .filter(i => !i.disabled && !i.divider).length;

            return (
              <button
                key={item.id}
                role="menuitem"
                disabled={item.disabled}
                onClick={() => handleItemClick(item)}
                className={`
                  w-full px-4 py-2 text-sm text-right
                  flex items-center gap-2
                  transition-colors
                  ${focusedIndex === enabledIndex ? 'bg-gray-100' : ''}
                  ${item.disabled 
                    ? 'text-gray-400 cursor-not-allowed' 
                    : item.danger
                      ? 'text-red-600 hover:bg-red-50'
                      : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                {item.icon && (
                  <span className="w-5 h-5">{item.icon}</span>
                )}
                {item.label}
              </button>
            );
          })}
        </div>,
        document.body
      )}
    </div>
  );
};

// =============================================================================
// Dropdown Button
// =============================================================================

interface DropdownButtonProps {
  label: string;
  items: DropdownItem[];
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  position?: DropdownPosition;
  disabled?: boolean;
}

export const DropdownButton: React.FC<DropdownButtonProps> = ({
  label,
  items,
  variant = 'secondary',
  size = 'md',
  icon,
  position = 'bottom-end',
  disabled = false,
}) => {
  const variantClasses = {
    primary: 'bg-indigo-600 text-white hover:bg-indigo-700',
    secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
    ghost: 'text-gray-700 hover:bg-gray-100',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  const ChevronIcon = () => (
    <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
    </svg>
  );

  return (
    <Dropdown
      items={items}
      position={position}
      disabled={disabled}
      trigger={
        <button
          type="button"
          disabled={disabled}
          className={`
            inline-flex items-center justify-center
            font-medium rounded-lg
            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
            ${variantClasses[variant]}
            ${sizeClasses[size]}
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          {icon && <span className="ml-2">{icon}</span>}
          {label}
          <ChevronIcon />
        </button>
      }
    />
  );
};

// =============================================================================
// Context Menu
// =============================================================================

interface ContextMenuProps {
  items: DropdownItem[];
  children: React.ReactNode;
  className?: string;
}

export const ContextMenu: React.FC<ContextMenuProps> = ({
  items,
  children,
  className = '',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [coords, setCoords] = useState({ top: 0, left: 0 });
  const menuRef = useRef<HTMLDivElement>(null);

  const handleContextMenu = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setCoords({ top: e.clientY, left: e.clientX });
    setIsOpen(true);
  }, []);

  useEffect(() => {
    const handleClick = () => setIsOpen(false);
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false);
    };

    if (isOpen) {
      document.addEventListener('click', handleClick);
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('click', handleClick);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen]);

  return (
    <>
      <div className={className} onContextMenu={handleContextMenu}>
        {children}
      </div>
      
      {isOpen && createPortal(
        <div
          ref={menuRef}
          role="menu"
          className="fixed z-50 min-w-[180px] bg-white rounded-lg shadow-lg border border-gray-200 py-1"
          style={{ top: coords.top, left: coords.left }}
          dir="rtl"
        >
          {items.map(item => {
            if (item.divider) {
              return <div key={item.id} className="my-1 border-t border-gray-200" />;
            }

            return (
              <button
                key={item.id}
                disabled={item.disabled}
                onClick={() => {
                  item.onClick?.();
                  setIsOpen(false);
                }}
                className={`
                  w-full px-4 py-2 text-sm text-right
                  flex items-center gap-2
                  ${item.disabled 
                    ? 'text-gray-400 cursor-not-allowed' 
                    : item.danger
                      ? 'text-red-600 hover:bg-red-50'
                      : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                {item.icon && <span className="w-5 h-5">{item.icon}</span>}
                {item.label}
              </button>
            );
          })}
        </div>,
        document.body
      )}
    </>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Dropdown;

