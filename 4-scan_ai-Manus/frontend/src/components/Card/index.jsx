/**
 * Card Components
 * ================
 * 
 * Reusable card components for consistent UI across the application.
 * 
 * Components:
 * - Card (base)
 * - StatCard
 * - InfoCard
 * - ActionCard
 * - ImageCard
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React from 'react';
import { ArrowUp, ArrowDown, ArrowRight, Minus } from 'lucide-react';

/**
 * Base Card Component
 */
export const Card = ({
  children,
  className = '',
  padding = true,
  hover = false,
  onClick
}) => (
  <div
    onClick={onClick}
    className={`
      bg-white dark:bg-gray-800
      border border-gray-200 dark:border-gray-700
      rounded-xl shadow-sm
      ${padding ? 'p-6' : ''}
      ${hover ? 'hover:shadow-md hover:border-emerald-200 dark:hover:border-emerald-700 cursor-pointer' : ''}
      ${onClick ? 'cursor-pointer' : ''}
      transition-all duration-200
      ${className}
    `}
  >
    {children}
  </div>
);

/**
 * Card Header
 */
export const CardHeader = ({
  title,
  titleAr,
  subtitle,
  subtitleAr,
  action,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displaySubtitle = isRTL ? (subtitleAr || subtitle) : subtitle;

  return (
    <div className={`flex items-start justify-between mb-4 ${className}`}>
      <div>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
          {displayTitle}
        </h3>
        {displaySubtitle && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            {displaySubtitle}
          </p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
};

/**
 * Card Footer
 */
export const CardFooter = ({
  children,
  className = ''
}) => (
  <div className={`mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 ${className}`}>
    {children}
  </div>
);

/**
 * Statistics Card
 */
export const StatCard = ({
  title,
  titleAr,
  value,
  change,
  changeType = 'neutral',
  icon: Icon,
  iconColor = 'emerald',
  suffix,
  prefix,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;

  const changeColors = {
    up: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/30',
    down: 'text-red-500 bg-red-50 dark:bg-red-900/30',
    neutral: 'text-gray-500 bg-gray-50 dark:bg-gray-700'
  };

  const iconColors = {
    emerald: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
    blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
    amber: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
    red: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
  };

  const ChangeIcon = changeType === 'up' ? ArrowUp : changeType === 'down' ? ArrowDown : Minus;

  return (
    <Card className={className}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">
            {displayTitle}
          </p>
          <div className="flex items-baseline gap-1 mt-2">
            {prefix && <span className="text-lg text-gray-500">{prefix}</span>}
            <span className="text-3xl font-bold text-gray-800 dark:text-white">
              {typeof value === 'number' ? value.toLocaleString() : value}
            </span>
            {suffix && <span className="text-lg text-gray-500">{suffix}</span>}
          </div>
          
          {change !== undefined && (
            <div className={`inline-flex items-center gap-1 mt-2 px-2 py-0.5 rounded-full text-xs font-medium ${changeColors[changeType]}`}>
              <ChangeIcon className="w-3 h-3" />
              <span>{change}%</span>
            </div>
          )}
        </div>
        
        {Icon && (
          <div className={`p-3 rounded-xl ${iconColors[iconColor]}`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </Card>
  );
};

/**
 * Info Card with icon
 */
export const InfoCard = ({
  title,
  titleAr,
  description,
  descriptionAr,
  icon: Icon,
  iconColor = 'emerald',
  badge,
  onClick,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displayDescription = isRTL ? (descriptionAr || description) : description;

  const iconColors = {
    emerald: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
    blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
    amber: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
    red: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
  };

  return (
    <Card hover={!!onClick} onClick={onClick} className={className}>
      <div className="flex items-start gap-4">
        {Icon && (
          <div className={`p-3 rounded-xl flex-shrink-0 ${iconColors[iconColor]}`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-800 dark:text-white truncate">
              {displayTitle}
            </h3>
            {badge && (
              <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400">
                {badge}
              </span>
            )}
          </div>
          {displayDescription && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
              {displayDescription}
            </p>
          )}
        </div>
        
        {onClick && (
          <ArrowRight className="w-5 h-5 text-gray-400 flex-shrink-0 rtl:rotate-180" />
        )}
      </div>
    </Card>
  );
};

/**
 * Action Card with button
 */
export const ActionCard = ({
  title,
  titleAr,
  description,
  descriptionAr,
  buttonText,
  buttonTextAr,
  buttonVariant = 'primary',
  onAction,
  icon: Icon,
  disabled = false,
  loading = false,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displayDescription = isRTL ? (descriptionAr || description) : description;
  const displayButton = isRTL ? (buttonTextAr || buttonText) : buttonText;

  const buttonVariants = {
    primary: 'bg-emerald-500 hover:bg-emerald-600 text-white',
    secondary: 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200',
    outline: 'border-2 border-emerald-500 text-emerald-500 hover:bg-emerald-50 dark:hover:bg-emerald-900/20'
  };

  return (
    <Card className={`text-center ${className}`}>
      {Icon && (
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
          <Icon className="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
        </div>
      )}
      
      <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
        {displayTitle}
      </h3>
      
      {displayDescription && (
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 mb-4">
          {displayDescription}
        </p>
      )}
      
      <button
        onClick={onAction}
        disabled={disabled || loading}
        className={`
          w-full py-2.5 px-4 rounded-lg font-medium
          ${buttonVariants[buttonVariant]}
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors duration-200
          flex items-center justify-center gap-2
        `}
      >
        {loading && (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        )}
        {displayButton}
      </button>
    </Card>
  );
};

/**
 * Image Card
 */
export const ImageCard = ({
  title,
  titleAr,
  subtitle,
  subtitleAr,
  image,
  badge,
  badgeColor = 'emerald',
  onClick,
  footer,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displaySubtitle = isRTL ? (subtitleAr || subtitle) : subtitle;

  const badgeColors = {
    emerald: 'bg-emerald-500 text-white',
    blue: 'bg-blue-500 text-white',
    amber: 'bg-amber-500 text-white',
    red: 'bg-red-500 text-white',
    gray: 'bg-gray-500 text-white'
  };

  return (
    <Card padding={false} hover={!!onClick} onClick={onClick} className={className}>
      <div className="relative">
        {image ? (
          <img
            src={image}
            alt={displayTitle}
            className="w-full h-48 object-cover rounded-t-xl"
          />
        ) : (
          <div className="w-full h-48 bg-gray-200 dark:bg-gray-700 rounded-t-xl flex items-center justify-center">
            <span className="text-gray-400 text-4xl">🌱</span>
          </div>
        )}
        
        {badge && (
          <span className={`
            absolute top-3 right-3 rtl:right-auto rtl:left-3
            px-2 py-1 rounded-full text-xs font-medium
            ${badgeColors[badgeColor]}
          `}>
            {badge}
          </span>
        )}
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 dark:text-white truncate">
          {displayTitle}
        </h3>
        {displaySubtitle && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {displaySubtitle}
          </p>
        )}
        {footer && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
            {footer}
          </div>
        )}
      </div>
    </Card>
  );
};

/**
 * Empty State Card
 */
export const EmptyCard = ({
  title,
  titleAr,
  description,
  descriptionAr,
  icon: Icon,
  action,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displayDescription = isRTL ? (descriptionAr || description) : description;

  return (
    <Card className={`text-center py-12 ${className}`}>
      {Icon && (
        <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
          <Icon className="w-10 h-10 text-gray-400" />
        </div>
      )}
      
      <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
        {displayTitle}
      </h3>
      
      {displayDescription && (
        <p className="text-gray-500 dark:text-gray-400 mt-2 max-w-md mx-auto">
          {displayDescription}
        </p>
      )}
      
      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </Card>
  );
};

export default Card;
