/**
 * P3.78: Loading Skeletons
 * 
 * Skeleton loading placeholders for better UX.
 */

import React from 'react';

// =============================================================================
// Base Skeleton
// =============================================================================

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'full';
  animate?: boolean;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className = '',
  width,
  height,
  rounded = 'md',
  animate = true,
}) => {
  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    full: 'rounded-full',
  };

  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === 'number' ? `${width}px` : width;
  if (height) style.height = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={`
        bg-gray-200 
        ${roundedClasses[rounded]} 
        ${animate ? 'animate-pulse' : ''} 
        ${className}
      `}
      style={style}
    />
  );
};

// =============================================================================
// Text Skeleton
// =============================================================================

interface SkeletonTextProps {
  lines?: number;
  lastLineWidth?: string;
  className?: string;
}

export const SkeletonText: React.FC<SkeletonTextProps> = ({
  lines = 3,
  lastLineWidth = '75%',
  className = '',
}) => {
  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          height={16}
          width={i === lines - 1 ? lastLineWidth : '100%'}
        />
      ))}
    </div>
  );
};

// =============================================================================
// Avatar Skeleton
// =============================================================================

interface SkeletonAvatarProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export const SkeletonAvatar: React.FC<SkeletonAvatarProps> = ({
  size = 'md',
  className = '',
}) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  return (
    <Skeleton
      className={`${sizes[size]} ${className}`}
      rounded="full"
    />
  );
};

// =============================================================================
// Card Skeleton
// =============================================================================

interface SkeletonCardProps {
  hasImage?: boolean;
  imageHeight?: number;
  lines?: number;
  className?: string;
}

export const SkeletonCard: React.FC<SkeletonCardProps> = ({
  hasImage = true,
  imageHeight = 200,
  lines = 3,
  className = '',
}) => {
  return (
    <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
      {hasImage && (
        <Skeleton
          height={imageHeight}
          className="w-full mb-4"
          rounded="lg"
        />
      )}
      <Skeleton height={24} width="70%" className="mb-2" />
      <SkeletonText lines={lines} />
    </div>
  );
};

// =============================================================================
// Table Skeleton
// =============================================================================

interface SkeletonTableProps {
  rows?: number;
  columns?: number;
  hasHeader?: boolean;
  className?: string;
}

export const SkeletonTable: React.FC<SkeletonTableProps> = ({
  rows = 5,
  columns = 4,
  hasHeader = true,
  className = '',
}) => {
  return (
    <div className={`bg-white rounded-lg shadow overflow-hidden ${className}`}>
      <table className="min-w-full">
        {hasHeader && (
          <thead className="bg-gray-50">
            <tr>
              {Array.from({ length: columns }).map((_, i) => (
                <th key={i} className="px-4 py-3">
                  <Skeleton height={16} width="80%" />
                </th>
              ))}
            </tr>
          </thead>
        )}
        <tbody className="divide-y divide-gray-200">
          {Array.from({ length: rows }).map((_, rowIndex) => (
            <tr key={rowIndex}>
              {Array.from({ length: columns }).map((_, colIndex) => (
                <td key={colIndex} className="px-4 py-3">
                  <Skeleton
                    height={16}
                    width={`${60 + Math.random() * 30}%`}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// =============================================================================
// List Skeleton
// =============================================================================

interface SkeletonListProps {
  items?: number;
  hasAvatar?: boolean;
  className?: string;
}

export const SkeletonList: React.FC<SkeletonListProps> = ({
  items = 5,
  hasAvatar = true,
  className = '',
}) => {
  return (
    <div className={`space-y-4 ${className}`}>
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-center gap-3">
          {hasAvatar && <SkeletonAvatar size="md" />}
          <div className="flex-1">
            <Skeleton height={16} width="60%" className="mb-2" />
            <Skeleton height={12} width="40%" />
          </div>
        </div>
      ))}
    </div>
  );
};

// =============================================================================
// Form Skeleton
// =============================================================================

interface SkeletonFormProps {
  fields?: number;
  hasSubmit?: boolean;
  className?: string;
}

export const SkeletonForm: React.FC<SkeletonFormProps> = ({
  fields = 4,
  hasSubmit = true,
  className = '',
}) => {
  return (
    <div className={`space-y-6 ${className}`}>
      {Array.from({ length: fields }).map((_, i) => (
        <div key={i}>
          <Skeleton height={14} width={120} className="mb-2" />
          <Skeleton height={40} className="w-full" />
        </div>
      ))}
      {hasSubmit && (
        <div className="flex justify-end gap-3 pt-4">
          <Skeleton height={40} width={100} />
          <Skeleton height={40} width={100} />
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Dashboard Skeleton
// =============================================================================

export const SkeletonDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between mb-4">
              <Skeleton height={14} width={80} />
              <Skeleton height={32} width={32} rounded="lg" />
            </div>
            <Skeleton height={28} width="60%" className="mb-1" />
            <Skeleton height={12} width="40%" />
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <Skeleton height={20} width={150} className="mb-4" />
          <Skeleton height={250} className="w-full" />
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <Skeleton height={20} width={150} className="mb-4" />
          <Skeleton height={250} className="w-full" />
        </div>
      </div>

      {/* Table */}
      <SkeletonTable rows={5} columns={5} />
    </div>
  );
};

// =============================================================================
// Product Grid Skeleton
// =============================================================================

interface SkeletonProductGridProps {
  items?: number;
  columns?: number;
}

export const SkeletonProductGrid: React.FC<SkeletonProductGridProps> = ({
  items = 8,
  columns = 4,
}) => {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-2',
    3: 'grid-cols-3',
    4: 'grid-cols-4',
  };

  return (
    <div className={`grid ${gridCols[columns as keyof typeof gridCols] || 'grid-cols-4'} gap-4`}>
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="bg-white rounded-lg shadow overflow-hidden">
          <Skeleton height={180} className="w-full" rounded="none" />
          <div className="p-4">
            <Skeleton height={16} width="80%" className="mb-2" />
            <Skeleton height={12} width="50%" className="mb-3" />
            <div className="flex items-center justify-between">
              <Skeleton height={20} width={80} />
              <Skeleton height={32} width={32} rounded="lg" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Skeleton;

