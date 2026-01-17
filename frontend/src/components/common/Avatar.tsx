/**
 * P3.95: Avatar Component
 * 
 * User avatar with image, initials, and status indicator support.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
type AvatarStatus = 'online' | 'offline' | 'busy' | 'away';

interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: AvatarSize;
  status?: AvatarStatus;
  rounded?: boolean;
  border?: boolean;
  className?: string;
  onClick?: () => void;
}

// =============================================================================
// Size Configuration
// =============================================================================

const sizeClasses: Record<AvatarSize, { container: string; text: string; status: string }> = {
  xs: { container: 'w-6 h-6', text: 'text-xs', status: 'w-1.5 h-1.5 border' },
  sm: { container: 'w-8 h-8', text: 'text-xs', status: 'w-2 h-2 border' },
  md: { container: 'w-10 h-10', text: 'text-sm', status: 'w-2.5 h-2.5 border-2' },
  lg: { container: 'w-12 h-12', text: 'text-base', status: 'w-3 h-3 border-2' },
  xl: { container: 'w-16 h-16', text: 'text-lg', status: 'w-4 h-4 border-2' },
  '2xl': { container: 'w-20 h-20', text: 'text-xl', status: 'w-5 h-5 border-2' },
};

const statusColors: Record<AvatarStatus, string> = {
  online: 'bg-green-500',
  offline: 'bg-gray-400',
  busy: 'bg-red-500',
  away: 'bg-yellow-500',
};

// =============================================================================
// Helper Functions
// =============================================================================

function getInitials(name: string): string {
  if (!name) return '؟';
  
  const parts = name.trim().split(' ').filter(Boolean);
  if (parts.length === 1) {
    return parts[0].charAt(0).toUpperCase();
  }
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

function getColorFromName(name: string): string {
  const colors = [
    'bg-red-500',
    'bg-orange-500',
    'bg-yellow-500',
    'bg-green-500',
    'bg-teal-500',
    'bg-blue-500',
    'bg-indigo-500',
    'bg-purple-500',
    'bg-pink-500',
  ];
  
  if (!name) return colors[0];
  
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  return colors[Math.abs(hash) % colors.length];
}

// =============================================================================
// Avatar Component
// =============================================================================

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  name,
  size = 'md',
  status,
  rounded = true,
  border = false,
  className = '',
  onClick,
}) => {
  const [imageError, setImageError] = React.useState(false);
  const sizes = sizeClasses[size];
  
  const handleError = () => {
    setImageError(true);
  };

  const showImage = src && !imageError;
  const initials = getInitials(name || alt || '');
  const bgColor = getColorFromName(name || alt || '');

  return (
    <div
      className={`
        relative inline-flex items-center justify-center
        ${sizes.container}
        ${rounded ? 'rounded-full' : 'rounded-lg'}
        ${border ? 'ring-2 ring-white' : ''}
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
    >
      {showImage ? (
        <img
          src={src}
          alt={alt || name || 'Avatar'}
          onError={handleError}
          className={`
            object-cover w-full h-full
            ${rounded ? 'rounded-full' : 'rounded-lg'}
          `}
        />
      ) : (
        <div
          className={`
            flex items-center justify-center w-full h-full
            text-white font-medium
            ${sizes.text}
            ${bgColor}
            ${rounded ? 'rounded-full' : 'rounded-lg'}
          `}
        >
          {initials}
        </div>
      )}
      
      {status && (
        <span
          className={`
            absolute bottom-0 right-0
            ${sizes.status}
            ${statusColors[status]}
            border-white rounded-full
          `}
        />
      )}
    </div>
  );
};

// =============================================================================
// Avatar Group
// =============================================================================

interface AvatarGroupProps {
  children: React.ReactNode;
  max?: number;
  size?: AvatarSize;
  className?: string;
}

export const AvatarGroup: React.FC<AvatarGroupProps> = ({
  children,
  max,
  size = 'md',
  className = '',
}) => {
  const childArray = React.Children.toArray(children);
  const displayChildren = max ? childArray.slice(0, max) : childArray;
  const remaining = max ? childArray.length - max : 0;
  const sizes = sizeClasses[size];

  return (
    <div className={`flex -space-x-2 rtl:space-x-reverse ${className}`}>
      {displayChildren.map((child, index) => (
        <div key={index} className="ring-2 ring-white rounded-full">
          {React.isValidElement(child)
            ? React.cloneElement(child as React.ReactElement<any>, { size })
            : child}
        </div>
      ))}
      
      {remaining > 0 && (
        <div
          className={`
            flex items-center justify-center
            ${sizes.container}
            bg-gray-200 text-gray-600
            font-medium ${sizes.text}
            rounded-full ring-2 ring-white
          `}
        >
          +{remaining}
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Avatar with Name
// =============================================================================

interface AvatarWithNameProps extends AvatarProps {
  title?: string;
  subtitle?: string;
  reverse?: boolean;
}

export const AvatarWithName: React.FC<AvatarWithNameProps> = ({
  title,
  subtitle,
  reverse = false,
  ...avatarProps
}) => {
  return (
    <div className={`flex items-center gap-3 ${reverse ? 'flex-row-reverse' : ''}`}>
      <Avatar {...avatarProps} />
      <div className={reverse ? 'text-left' : 'text-right'}>
        {title && (
          <p className="text-sm font-medium text-gray-900">{title}</p>
        )}
        {subtitle && (
          <p className="text-xs text-gray-500">{subtitle}</p>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Editable Avatar
// =============================================================================

interface EditableAvatarProps extends AvatarProps {
  onEdit?: () => void;
}

export const EditableAvatar: React.FC<EditableAvatarProps> = ({
  onEdit,
  ...props
}) => {
  return (
    <div className="relative inline-block group">
      <Avatar {...props} />
      {onEdit && (
        <button
          type="button"
          onClick={onEdit}
          className="
            absolute inset-0 flex items-center justify-center
            bg-black/50 rounded-full
            opacity-0 group-hover:opacity-100
            transition-opacity
          "
        >
          <svg
            className="w-5 h-5 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </button>
      )}
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Avatar;

