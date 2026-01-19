/**
 * Loading Skeleton Components
 * ============================
 * 
 * Beautiful animated skeleton loaders for improved UX during data fetching.
 * Matches the agricultural/nature theme of Gaara Scan AI.
 * 
 * Features:
 * - Multiple skeleton variants (text, card, table, etc.)
 * - Shimmer animation
 * - Responsive and RTL-aware
 * - Dark mode support
 * 
 * @author Global System v35.0
 * @date 2026-01-17
 */

import React from 'react';

// ============================================
// Base Skeleton Component
// ============================================

/**
 * Base skeleton with shimmer animation
 * 
 * @param {Object} props - Component props
 * @param {string} props.className - Additional CSS classes
 * @param {string} props.width - Width (default: '100%')
 * @param {string} props.height - Height (default: '1rem')
 * @param {boolean} props.rounded - Full rounded (circle)
 * @param {boolean} props.animate - Enable animation (default: true)
 */
export const Skeleton = ({ 
  className = '', 
  width = '100%', 
  height = '1rem',
  rounded = false,
  animate = true
}) => {
  return (
    <div
      className={`
        bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200
        dark:from-gray-700 dark:via-gray-600 dark:to-gray-700
        ${rounded ? 'rounded-full' : 'rounded-md'}
        ${animate ? 'animate-shimmer' : ''}
        ${className}
      `}
      style={{ 
        width, 
        height,
        backgroundSize: '200% 100%'
      }}
      aria-hidden="true"
    />
  );
};

// ============================================
// Text Skeleton
// ============================================

/**
 * Text line skeleton
 * 
 * @param {Object} props - Component props
 * @param {number} props.lines - Number of lines
 * @param {string} props.width - Last line width
 */
export const TextSkeleton = ({ lines = 3, width = '75%', className = '' }) => {
  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          height="0.875rem"
          width={i === lines - 1 ? width : '100%'}
        />
      ))}
    </div>
  );
};

// ============================================
// Avatar Skeleton
// ============================================

/**
 * Avatar/profile image skeleton
 * 
 * @param {Object} props - Component props
 * @param {string} props.size - Size: 'sm', 'md', 'lg', 'xl'
 */
export const AvatarSkeleton = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24'
  };

  return (
    <Skeleton 
      className={`${sizes[size]} ${className}`} 
      rounded 
      width="auto"
      height="auto"
    />
  );
};

// ============================================
// Card Skeleton
// ============================================

/**
 * Card skeleton with title, text, and optional image
 * 
 * @param {Object} props - Component props
 * @param {boolean} props.hasImage - Include image placeholder
 * @param {boolean} props.hasFooter - Include footer section
 */
export const CardSkeleton = ({ hasImage = true, hasFooter = false, className = '' }) => {
  return (
    <div 
      className={`
        bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden
        border border-gray-100 dark:border-gray-700
        ${className}
      `}
    >
      {/* Image placeholder */}
      {hasImage && (
        <Skeleton height="12rem" className="rounded-none" />
      )}
      
      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Title */}
        <Skeleton height="1.25rem" width="60%" />
        
        {/* Text lines */}
        <div className="space-y-2">
          <Skeleton height="0.875rem" />
          <Skeleton height="0.875rem" width="85%" />
        </div>
        
        {/* Meta info */}
        <div className="flex items-center gap-2 pt-2">
          <AvatarSkeleton size="sm" />
          <Skeleton height="0.75rem" width="40%" />
        </div>
      </div>
      
      {/* Footer */}
      {hasFooter && (
        <div className="px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-100 dark:border-gray-700">
          <div className="flex justify-between items-center">
            <Skeleton height="2rem" width="5rem" />
            <Skeleton height="2rem" width="5rem" />
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================
// Table Skeleton
// ============================================

/**
 * Table rows skeleton
 * 
 * @param {Object} props - Component props
 * @param {number} props.rows - Number of rows
 * @param {number} props.columns - Number of columns
 */
export const TableSkeleton = ({ rows = 5, columns = 4, className = '' }) => {
  return (
    <div className={`overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 ${className}`}>
      {/* Header */}
      <div className="bg-gray-50 dark:bg-gray-800 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <div className="flex gap-4">
          {Array.from({ length: columns }).map((_, i) => (
            <Skeleton 
              key={i} 
              height="0.875rem" 
              width={`${100 / columns}%`}
            />
          ))}
        </div>
      </div>
      
      {/* Rows */}
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="px-4 py-3 flex gap-4 items-center">
            {Array.from({ length: columns }).map((_, colIndex) => (
              <Skeleton 
                key={colIndex} 
                height="0.875rem" 
                width={colIndex === 0 ? '30%' : `${70 / (columns - 1)}%`}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================
// Stat Card Skeleton
// ============================================

/**
 * Statistics card skeleton for dashboard
 */
export const StatCardSkeleton = ({ className = '' }) => {
  return (
    <div 
      className={`
        bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm
        border border-gray-100 dark:border-gray-700
        ${className}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2 flex-1">
          <Skeleton height="0.75rem" width="40%" />
          <Skeleton height="2rem" width="60%" />
          <Skeleton height="0.625rem" width="30%" />
        </div>
        <Skeleton 
          width="3rem" 
          height="3rem" 
          className="rounded-lg"
        />
      </div>
    </div>
  );
};

// ============================================
// Chart Skeleton
// ============================================

/**
 * Chart/graph placeholder skeleton
 * 
 * @param {Object} props - Component props
 * @param {string} props.type - Chart type: 'bar', 'line', 'pie'
 */
export const ChartSkeleton = ({ type = 'bar', className = '' }) => {
  if (type === 'pie') {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <div className="relative">
          <Skeleton 
            width="12rem" 
            height="12rem" 
            rounded 
          />
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <Skeleton 
              width="6rem" 
              height="6rem" 
              rounded 
              className="bg-white dark:bg-gray-800"
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 ${className}`}>
      {/* Chart title */}
      <Skeleton height="1rem" width="40%" className="mb-4" />
      
      {/* Chart area */}
      <div className="flex items-end gap-2 h-48">
        {type === 'bar' ? (
          // Bar chart
          Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="flex-1 flex flex-col justify-end">
              <Skeleton 
                height={`${Math.random() * 60 + 40}%`}
                className="rounded-t-md"
              />
            </div>
          ))
        ) : (
          // Line chart placeholder
          <div className="w-full h-full relative">
            <Skeleton height="100%" className="opacity-30" />
            <div className="absolute bottom-0 left-0 right-0 h-px bg-gray-300 dark:bg-gray-600" />
            <div className="absolute top-0 bottom-0 left-0 w-px bg-gray-300 dark:bg-gray-600" />
          </div>
        )}
      </div>
      
      {/* X-axis labels */}
      <div className="flex gap-2 mt-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} height="0.625rem" className="flex-1" />
        ))}
      </div>
    </div>
  );
};

// ============================================
// Diagnosis Result Skeleton
// ============================================

/**
 * Diagnosis result card skeleton (specific to Gaara Scan)
 */
export const DiagnosisResultSkeleton = ({ className = '' }) => {
  return (
    <div 
      className={`
        bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden
        border border-emerald-100 dark:border-emerald-900
        ${className}
      `}
    >
      {/* Image section */}
      <div className="relative">
        <Skeleton height="16rem" className="rounded-none" />
        <div className="absolute bottom-4 right-4">
          <Skeleton 
            width="4rem" 
            height="1.5rem" 
            className="rounded-full"
          />
        </div>
      </div>
      
      {/* Results section */}
      <div className="p-6 space-y-4">
        {/* Disease name */}
        <div className="space-y-1">
          <Skeleton height="0.75rem" width="30%" />
          <Skeleton height="1.5rem" width="70%" />
        </div>
        
        {/* Confidence bar */}
        <div className="space-y-2">
          <div className="flex justify-between">
            <Skeleton height="0.75rem" width="20%" />
            <Skeleton height="0.75rem" width="10%" />
          </div>
          <Skeleton height="0.5rem" className="rounded-full" />
        </div>
        
        {/* Severity indicator */}
        <div className="flex gap-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton 
              key={i} 
              width="3rem" 
              height="0.5rem" 
              className="rounded-full"
            />
          ))}
        </div>
        
        {/* Recommendations */}
        <div className="pt-4 space-y-2">
          <Skeleton height="0.875rem" width="40%" />
          <div className="space-y-1">
            <Skeleton height="0.75rem" />
            <Skeleton height="0.75rem" />
            <Skeleton height="0.75rem" width="60%" />
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================
// Farm Card Skeleton
// ============================================

/**
 * Farm management card skeleton
 */
export const FarmCardSkeleton = ({ className = '' }) => {
  return (
    <div 
      className={`
        bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden
        border border-gray-100 dark:border-gray-700
        ${className}
      `}
    >
      {/* Map/Image placeholder */}
      <Skeleton height="10rem" className="rounded-none" />
      
      {/* Content */}
      <div className="p-4 space-y-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1 flex-1">
            <Skeleton height="1.25rem" width="70%" />
            <Skeleton height="0.75rem" width="50%" />
          </div>
          <Skeleton width="3rem" height="1.5rem" className="rounded-full" />
        </div>
        
        {/* Stats */}
        <div className="grid grid-cols-3 gap-2 pt-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="text-center space-y-1">
              <Skeleton height="1rem" width="60%" className="mx-auto" />
              <Skeleton height="0.625rem" width="80%" className="mx-auto" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ============================================
// List Item Skeleton
// ============================================

/**
 * List item skeleton
 */
export const ListItemSkeleton = ({ hasAvatar = true, className = '' }) => {
  return (
    <div className={`flex items-center gap-3 p-3 ${className}`}>
      {hasAvatar && <AvatarSkeleton size="md" />}
      <div className="flex-1 space-y-1">
        <Skeleton height="0.875rem" width="60%" />
        <Skeleton height="0.75rem" width="40%" />
      </div>
      <Skeleton width="4rem" height="1.5rem" className="rounded-md" />
    </div>
  );
};

// ============================================
// Page Header Skeleton
// ============================================

/**
 * Page header with title and actions
 */
export const PageHeaderSkeleton = ({ className = '' }) => {
  return (
    <div className={`flex items-center justify-between py-4 ${className}`}>
      <div className="space-y-1">
        <Skeleton height="1.5rem" width="12rem" />
        <Skeleton height="0.875rem" width="20rem" />
      </div>
      <div className="flex gap-2">
        <Skeleton width="6rem" height="2.5rem" className="rounded-lg" />
        <Skeleton width="6rem" height="2.5rem" className="rounded-lg" />
      </div>
    </div>
  );
};

// ============================================
// Shimmer Animation Styles
// ============================================

// Add this to your global CSS or Tailwind config:
/*
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-shimmer {
  animation: shimmer 1.5s infinite linear;
}
*/

// Inline style for shimmer (if not using global CSS)
export const shimmerStyle = `
  @keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }
  .animate-shimmer {
    animation: shimmer 1.5s infinite linear;
  }
`;

// ============================================
// Dashboard Skeleton (Composite)
// ============================================

/**
 * Full dashboard loading skeleton
 */
export const DashboardSkeleton = () => {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <PageHeaderSkeleton />
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <StatCardSkeleton key={i} />
        ))}
      </div>
      
      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <ChartSkeleton type="bar" />
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <ChartSkeleton type="line" />
        </div>
      </div>
      
      {/* Recent Activity */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4">
        <Skeleton height="1.25rem" width="30%" className="mb-4" />
        <div className="divide-y divide-gray-100 dark:divide-gray-700">
          {Array.from({ length: 5 }).map((_, i) => (
            <ListItemSkeleton key={i} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Skeleton;
