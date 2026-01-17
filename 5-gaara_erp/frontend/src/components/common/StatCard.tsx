/**
 * P3.100: Stat Card Component
 * 
 * Statistics and metric cards for dashboards.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type TrendDirection = 'up' | 'down' | 'neutral';
type StatColor = 'blue' | 'green' | 'red' | 'yellow' | 'indigo' | 'purple' | 'gray';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    direction: TrendDirection;
    label?: string;
  };
  color?: StatColor;
  loading?: boolean;
  className?: string;
  onClick?: () => void;
}

// =============================================================================
// Configuration
// =============================================================================

const colorConfig: Record<StatColor, { bg: string; icon: string; text: string }> = {
  blue: { bg: 'bg-blue-100', icon: 'text-blue-600', text: 'text-blue-600' },
  green: { bg: 'bg-green-100', icon: 'text-green-600', text: 'text-green-600' },
  red: { bg: 'bg-red-100', icon: 'text-red-600', text: 'text-red-600' },
  yellow: { bg: 'bg-yellow-100', icon: 'text-yellow-600', text: 'text-yellow-600' },
  indigo: { bg: 'bg-indigo-100', icon: 'text-indigo-600', text: 'text-indigo-600' },
  purple: { bg: 'bg-purple-100', icon: 'text-purple-600', text: 'text-purple-600' },
  gray: { bg: 'bg-gray-100', icon: 'text-gray-600', text: 'text-gray-600' },
};

// =============================================================================
// Stat Card Component
// =============================================================================

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  color = 'blue',
  loading = false,
  className = '',
  onClick,
}) => {
  const colors = colorConfig[color];

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-1/3"></div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`
        bg-white rounded-lg shadow p-6
        ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}
        ${className}
      `}
      onClick={onClick}
      data-testid="metric-card"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
          
          {(subtitle || trend) && (
            <div className="mt-2 flex items-center gap-2">
              {trend && (
                <span className={`
                  inline-flex items-center text-sm font-medium
                  ${trend.direction === 'up' ? 'text-green-600' : 
                    trend.direction === 'down' ? 'text-red-600' : 'text-gray-500'}
                `}>
                  {trend.direction === 'up' && (
                    <svg className="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                  {trend.direction === 'down' && (
                    <svg className="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                  {Math.abs(trend.value)}%
                </span>
              )}
              {subtitle && (
                <span className="text-sm text-gray-500">{subtitle}</span>
              )}
              {trend?.label && (
                <span className="text-sm text-gray-400">{trend.label}</span>
              )}
            </div>
          )}
        </div>
        
        {icon && (
          <div className={`p-3 rounded-lg ${colors.bg}`}>
            <div className={colors.icon}>{icon}</div>
          </div>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Mini Stat Card
// =============================================================================

interface MiniStatCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  color?: StatColor;
  className?: string;
}

export const MiniStatCard: React.FC<MiniStatCardProps> = ({
  label,
  value,
  icon,
  color = 'gray',
  className = '',
}) => {
  const colors = colorConfig[color];

  return (
    <div className={`flex items-center gap-3 p-3 bg-gray-50 rounded-lg ${className}`}>
      {icon && (
        <div className={`p-2 rounded-lg ${colors.bg}`}>
          <div className={`w-5 h-5 ${colors.icon}`}>{icon}</div>
        </div>
      )}
      <div>
        <p className="text-xs text-gray-500">{label}</p>
        <p className="text-lg font-semibold text-gray-900">{value}</p>
      </div>
    </div>
  );
};

// =============================================================================
// Stat Card Grid
// =============================================================================

interface StatItem {
  id: string;
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  color?: StatColor;
  trend?: {
    value: number;
    direction: TrendDirection;
  };
}

interface StatCardGridProps {
  stats: StatItem[];
  columns?: 2 | 3 | 4;
  loading?: boolean;
  className?: string;
}

export const StatCardGrid: React.FC<StatCardGridProps> = ({
  stats,
  columns = 4,
  loading = false,
  className = '',
}) => {
  const gridCols = {
    2: 'grid-cols-1 sm:grid-cols-2',
    3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
  };

  return (
    <div className={`grid gap-4 ${gridCols[columns]} ${className}`}>
      {stats.map((stat) => (
        <StatCard
          key={stat.id}
          title={stat.title}
          value={stat.value}
          icon={stat.icon}
          color={stat.color}
          trend={stat.trend}
          loading={loading}
        />
      ))}
    </div>
  );
};

// =============================================================================
// Comparison Stat Card
// =============================================================================

interface ComparisonStatCardProps {
  title: string;
  currentValue: number;
  previousValue: number;
  format?: (value: number) => string;
  icon?: React.ReactNode;
  color?: StatColor;
  className?: string;
}

export const ComparisonStatCard: React.FC<ComparisonStatCardProps> = ({
  title,
  currentValue,
  previousValue,
  format = (v) => v.toLocaleString('ar-SA'),
  icon,
  color = 'blue',
  className = '',
}) => {
  const change = previousValue ? ((currentValue - previousValue) / previousValue) * 100 : 0;
  const direction: TrendDirection = change > 0 ? 'up' : change < 0 ? 'down' : 'neutral';

  return (
    <StatCard
      title={title}
      value={format(currentValue)}
      icon={icon}
      color={color}
      trend={{
        value: Math.abs(Math.round(change)),
        direction,
        label: 'مقارنة بالفترة السابقة',
      }}
      className={className}
    />
  );
};

// =============================================================================
// Progress Stat Card
// =============================================================================

interface ProgressStatCardProps {
  title: string;
  value: number;
  max: number;
  unit?: string;
  icon?: React.ReactNode;
  color?: StatColor;
  className?: string;
}

export const ProgressStatCard: React.FC<ProgressStatCardProps> = ({
  title,
  value,
  max,
  unit = '',
  icon,
  color = 'blue',
  className = '',
}) => {
  const percentage = Math.min(100, Math.round((value / max) * 100));
  const colors = colorConfig[color];

  return (
    <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">
            {value.toLocaleString('ar-SA')} {unit}
          </p>
        </div>
        {icon && (
          <div className={`p-3 rounded-lg ${colors.bg}`}>
            <div className={colors.icon}>{icon}</div>
          </div>
        )}
      </div>
      
      <div className="relative">
        <div className="w-full h-2 bg-gray-200 rounded-full">
          <div
            className={`h-2 rounded-full transition-all duration-500 ${colors.bg.replace('100', '500')}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
        <div className="flex justify-between mt-1 text-xs text-gray-500">
          <span>{percentage}%</span>
          <span>من {max.toLocaleString('ar-SA')} {unit}</span>
        </div>
      </div>
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default StatCard;

