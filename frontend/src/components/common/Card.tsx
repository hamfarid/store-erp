/**
 * P3.97: Card Component
 * 
 * Versatile card component with multiple variants.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  shadow?: 'none' | 'sm' | 'md' | 'lg';
  border?: boolean;
  hoverable?: boolean;
  clickable?: boolean;
  onClick?: () => void;
}

interface CardHeaderProps {
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
  children?: React.ReactNode;
  className?: string;
}

interface CardBodyProps {
  children: React.ReactNode;
  className?: string;
}

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
  align?: 'left' | 'center' | 'right' | 'between';
}

// =============================================================================
// Configuration
// =============================================================================

const paddingClasses = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
};

const shadowClasses = {
  none: '',
  sm: 'shadow-sm',
  md: 'shadow',
  lg: 'shadow-lg',
};

// =============================================================================
// Card Component
// =============================================================================

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  padding = 'md',
  shadow = 'md',
  border = false,
  hoverable = false,
  clickable = false,
  onClick,
}) => {
  return (
    <div
      className={`
        bg-white rounded-lg
        ${paddingClasses[padding]}
        ${shadowClasses[shadow]}
        ${border ? 'border border-gray-200' : ''}
        ${hoverable ? 'transition-shadow hover:shadow-lg' : ''}
        ${clickable ? 'cursor-pointer' : ''}
        ${className}
      `}
      onClick={clickable ? onClick : undefined}
      role={clickable ? 'button' : undefined}
      tabIndex={clickable ? 0 : undefined}
    >
      {children}
    </div>
  );
};

// =============================================================================
// Card Header
// =============================================================================

export const CardHeader: React.FC<CardHeaderProps> = ({
  title,
  subtitle,
  action,
  icon,
  children,
  className = '',
}) => {
  if (children) {
    return (
      <div className={`border-b border-gray-200 px-4 py-3 ${className}`}>
        {children}
      </div>
    );
  }

  return (
    <div className={`border-b border-gray-200 px-4 py-3 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {icon && (
            <div className="flex-shrink-0 text-gray-400">
              {icon}
            </div>
          )}
          <div>
            {title && (
              <h3 className="text-base font-semibold text-gray-900">{title}</h3>
            )}
            {subtitle && (
              <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>
            )}
          </div>
        </div>
        {action && (
          <div className="flex-shrink-0">
            {action}
          </div>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Card Body
// =============================================================================

export const CardBody: React.FC<CardBodyProps> = ({
  children,
  className = '',
}) => {
  return (
    <div className={`px-4 py-4 ${className}`}>
      {children}
    </div>
  );
};

// =============================================================================
// Card Footer
// =============================================================================

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  className = '',
  align = 'right',
}) => {
  const alignClasses = {
    left: 'justify-start',
    center: 'justify-center',
    right: 'justify-end',
    between: 'justify-between',
  };

  return (
    <div className={`
      border-t border-gray-200 px-4 py-3
      flex items-center gap-3 ${alignClasses[align]}
      ${className}
    `}>
      {children}
    </div>
  );
};

// =============================================================================
// Image Card
// =============================================================================

interface ImageCardProps extends CardProps {
  image: string;
  imageAlt?: string;
  imageHeight?: string;
  overlay?: React.ReactNode;
}

export const ImageCard: React.FC<ImageCardProps> = ({
  image,
  imageAlt = '',
  imageHeight = 'h-48',
  overlay,
  children,
  ...props
}) => {
  return (
    <Card {...props} padding="none">
      <div className={`relative ${imageHeight} overflow-hidden rounded-t-lg`}>
        <img
          src={image}
          alt={imageAlt}
          className="w-full h-full object-cover"
        />
        {overlay && (
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
            {overlay}
          </div>
        )}
      </div>
      <div className="p-4">
        {children}
      </div>
    </Card>
  );
};

// =============================================================================
// Horizontal Card
// =============================================================================

interface HorizontalCardProps extends CardProps {
  image?: string;
  imageAlt?: string;
  imageWidth?: string;
}

export const HorizontalCard: React.FC<HorizontalCardProps> = ({
  image,
  imageAlt = '',
  imageWidth = 'w-32',
  children,
  ...props
}) => {
  return (
    <Card {...props} padding="none">
      <div className="flex">
        {image && (
          <div className={`flex-shrink-0 ${imageWidth}`}>
            <img
              src={image}
              alt={imageAlt}
              className="h-full w-full object-cover rounded-r-lg"
            />
          </div>
        )}
        <div className="flex-1 p-4">
          {children}
        </div>
      </div>
    </Card>
  );
};

// =============================================================================
// Feature Card
// =============================================================================

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  action?: React.ReactNode;
  className?: string;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({
  icon,
  title,
  description,
  action,
  className = '',
}) => {
  return (
    <Card className={`text-center ${className}`} hoverable>
      <div className="mx-auto w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center text-indigo-600 mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-500 mb-4">{description}</p>
      {action}
    </Card>
  );
};

// =============================================================================
// Pricing Card
// =============================================================================

interface PricingCardProps {
  title: string;
  price: string;
  period?: string;
  features: string[];
  highlighted?: boolean;
  action?: React.ReactNode;
  className?: string;
}

export const PricingCard: React.FC<PricingCardProps> = ({
  title,
  price,
  period = '/شهر',
  features,
  highlighted = false,
  action,
  className = '',
}) => {
  return (
    <Card
      className={`
        ${highlighted ? 'ring-2 ring-indigo-600 scale-105' : ''}
        ${className}
      `}
      shadow={highlighted ? 'lg' : 'md'}
    >
      {highlighted && (
        <div className="bg-indigo-600 text-white text-xs font-medium py-1 px-3 rounded-full w-fit mx-auto -mt-6 mb-4">
          الأكثر شعبية
        </div>
      )}
      <div className="text-center mb-6">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="mt-4">
          <span className="text-4xl font-bold text-gray-900">{price}</span>
          <span className="text-gray-500">{period}</span>
        </div>
      </div>
      <ul className="space-y-3 mb-6">
        {features.map((feature, index) => (
          <li key={index} className="flex items-center gap-2 text-sm text-gray-600">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            {feature}
          </li>
        ))}
      </ul>
      {action}
    </Card>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Card;

