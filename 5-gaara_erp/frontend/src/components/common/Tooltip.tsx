/**
 * P3.79: Tooltip Component
 * 
 * Accessible tooltip component with multiple positions.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';

// =============================================================================
// Types
// =============================================================================

type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  position?: TooltipPosition;
  delay?: number;
  disabled?: boolean;
  maxWidth?: number;
  className?: string;
  arrow?: boolean;
}

// =============================================================================
// Position Calculator
// =============================================================================

function calculatePosition(
  triggerRect: DOMRect,
  tooltipRect: DOMRect,
  position: TooltipPosition,
  offset: number = 8
): { top: number; left: number; actualPosition: TooltipPosition } {
  const { innerWidth, innerHeight } = window;
  const scrollY = window.scrollY;
  const scrollX = window.scrollX;

  let top = 0;
  let left = 0;
  let actualPosition = position;

  // Calculate initial position
  switch (position) {
    case 'top':
      top = triggerRect.top + scrollY - tooltipRect.height - offset;
      left = triggerRect.left + scrollX + (triggerRect.width - tooltipRect.width) / 2;
      break;
    case 'bottom':
      top = triggerRect.bottom + scrollY + offset;
      left = triggerRect.left + scrollX + (triggerRect.width - tooltipRect.width) / 2;
      break;
    case 'left':
      top = triggerRect.top + scrollY + (triggerRect.height - tooltipRect.height) / 2;
      left = triggerRect.left + scrollX - tooltipRect.width - offset;
      break;
    case 'right':
      top = triggerRect.top + scrollY + (triggerRect.height - tooltipRect.height) / 2;
      left = triggerRect.right + scrollX + offset;
      break;
  }

  // Boundary checks and flipping
  if (position === 'top' && top < scrollY) {
    // Flip to bottom
    top = triggerRect.bottom + scrollY + offset;
    actualPosition = 'bottom';
  } else if (position === 'bottom' && top + tooltipRect.height > scrollY + innerHeight) {
    // Flip to top
    top = triggerRect.top + scrollY - tooltipRect.height - offset;
    actualPosition = 'top';
  } else if (position === 'left' && left < scrollX) {
    // Flip to right
    left = triggerRect.right + scrollX + offset;
    actualPosition = 'right';
  } else if (position === 'right' && left + tooltipRect.width > scrollX + innerWidth) {
    // Flip to left
    left = triggerRect.left + scrollX - tooltipRect.width - offset;
    actualPosition = 'left';
  }

  // Keep within viewport bounds
  left = Math.max(scrollX + 8, Math.min(left, scrollX + innerWidth - tooltipRect.width - 8));
  top = Math.max(scrollY + 8, Math.min(top, scrollY + innerHeight - tooltipRect.height - 8));

  return { top, left, actualPosition };
}

// =============================================================================
// Arrow Component
// =============================================================================

const TooltipArrow: React.FC<{ position: TooltipPosition }> = ({ position }) => {
  const arrowClasses: Record<TooltipPosition, string> = {
    top: 'bottom-0 left-1/2 -translate-x-1/2 translate-y-full border-t-gray-900 border-x-transparent border-b-transparent',
    bottom: 'top-0 left-1/2 -translate-x-1/2 -translate-y-full border-b-gray-900 border-x-transparent border-t-transparent',
    left: 'right-0 top-1/2 -translate-y-1/2 translate-x-full border-l-gray-900 border-y-transparent border-r-transparent',
    right: 'left-0 top-1/2 -translate-y-1/2 -translate-x-full border-r-gray-900 border-y-transparent border-l-transparent',
  };

  return (
    <div
      className={`absolute w-0 h-0 border-4 ${arrowClasses[position]}`}
    />
  );
};

// =============================================================================
// Tooltip Component
// =============================================================================

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  position = 'top',
  delay = 200,
  disabled = false,
  maxWidth = 250,
  className = '',
  arrow = true,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [coords, setCoords] = useState({ top: 0, left: 0 });
  const [actualPosition, setActualPosition] = useState(position);
  
  const triggerRef = useRef<HTMLElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout>();

  const updatePosition = useCallback(() => {
    if (triggerRef.current && tooltipRef.current) {
      const triggerRect = triggerRef.current.getBoundingClientRect();
      const tooltipRect = tooltipRef.current.getBoundingClientRect();
      const { top, left, actualPosition: newPosition } = calculatePosition(
        triggerRect,
        tooltipRect,
        position
      );
      setCoords({ top, left });
      setActualPosition(newPosition);
    }
  }, [position]);

  const showTooltip = useCallback(() => {
    if (disabled) return;
    
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  }, [disabled, delay]);

  const hideTooltip = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  }, []);

  // Update position when visible
  useEffect(() => {
    if (isVisible) {
      updatePosition();
      
      // Add listeners for repositioning
      window.addEventListener('scroll', updatePosition, true);
      window.addEventListener('resize', updatePosition);
      
      return () => {
        window.removeEventListener('scroll', updatePosition, true);
        window.removeEventListener('resize', updatePosition);
      };
    }
  }, [isVisible, updatePosition]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  // Clone children with ref and event handlers
  const trigger = React.cloneElement(children, {
    ref: triggerRef,
    onMouseEnter: (e: React.MouseEvent) => {
      showTooltip();
      children.props.onMouseEnter?.(e);
    },
    onMouseLeave: (e: React.MouseEvent) => {
      hideTooltip();
      children.props.onMouseLeave?.(e);
    },
    onFocus: (e: React.FocusEvent) => {
      showTooltip();
      children.props.onFocus?.(e);
    },
    onBlur: (e: React.FocusEvent) => {
      hideTooltip();
      children.props.onBlur?.(e);
    },
    'aria-describedby': isVisible ? 'tooltip' : undefined,
  });

  if (disabled || !content) {
    return children;
  }

  return (
    <>
      {trigger}
      {isVisible && createPortal(
        <div
          ref={tooltipRef}
          id="tooltip"
          role="tooltip"
          className={`
            fixed z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg
            transition-opacity duration-150
            ${className}
          `}
          style={{
            top: coords.top,
            left: coords.left,
            maxWidth,
          }}
        >
          {content}
          {arrow && <TooltipArrow position={actualPosition} />}
        </div>,
        document.body
      )}
    </>
  );
};

// =============================================================================
// Info Tooltip
// =============================================================================

interface InfoTooltipProps {
  content: React.ReactNode;
  position?: TooltipPosition;
  iconSize?: 'sm' | 'md' | 'lg';
}

export const InfoTooltip: React.FC<InfoTooltipProps> = ({
  content,
  position = 'top',
  iconSize = 'md',
}) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <Tooltip content={content} position={position}>
      <button
        type="button"
        className={`
          inline-flex items-center justify-center
          text-gray-400 hover:text-gray-600
          focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
          rounded-full
        `}
      >
        <svg
          className={sizes[iconSize]}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span className="sr-only">معلومات إضافية</span>
      </button>
    </Tooltip>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Tooltip;

