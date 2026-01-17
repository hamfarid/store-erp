/**
 * P2.57: Dashboard Widgets
 * 
 * Reusable dashboard widget components with charts and statistics.
 */

import React, { useState, useEffect, ReactNode } from 'react';

// =============================================================================
// Types
// =============================================================================

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  icon?: ReactNode;
  loading?: boolean;
  prefix?: string;
  suffix?: string;
}

interface ChartData {
  labels: string[];
  values: number[];
}

interface TopItem {
  id: number;
  name: string;
  value: number;
  secondaryValue?: number;
}

// =============================================================================
// Stat Card Widget
// =============================================================================

export function StatCard({
  title,
  value,
  change,
  trend = 'neutral',
  icon,
  loading = false,
  prefix = '',
  suffix = '',
}: StatCardProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-24 mb-4"></div>
        <div className="h-8 bg-gray-200 rounded w-32"></div>
      </div>
    );
  }

  const trendColors = {
    up: 'text-emerald-500 bg-emerald-50',
    down: 'text-red-500 bg-red-50',
    neutral: 'text-gray-500 bg-gray-50',
  };

  const trendIcons = {
    up: '↑',
    down: '↓',
    neutral: '→',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6" data-testid="metric-card">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm font-medium text-gray-500">{title}</span>
        {icon && (
          <span className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
            {icon}
          </span>
        )}
      </div>
      
      <div className="flex items-end justify-between">
        <div>
          <h3 className="text-2xl font-bold text-gray-900">
            {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
          </h3>
          
          {change !== undefined && (
            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium mt-2 ${trendColors[trend]}`}>
              {trendIcons[trend]} {Math.abs(change).toFixed(1)}%
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Bar Chart Widget
// =============================================================================

interface BarChartProps {
  title: string;
  data: ChartData;
  loading?: boolean;
  height?: number;
  color?: string;
}

export function BarChart({
  title,
  data,
  loading = false,
  height = 200,
  color = '#4F46E5',
}: BarChartProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        <div className="h-48 bg-gray-100 rounded"></div>
      </div>
    );
  }

  const maxValue = Math.max(...data.values, 1);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="flex items-end gap-2" style={{ height }}>
        {data.values.map((value, index) => (
          <div key={index} className="flex-1 flex flex-col items-center">
            <div
              className="w-full rounded-t transition-all duration-300 hover:opacity-80"
              style={{
                height: `${(value / maxValue) * 100}%`,
                backgroundColor: color,
                minHeight: value > 0 ? '4px' : '0',
              }}
              title={`${data.labels[index]}: ${value.toLocaleString()}`}
            ></div>
            <span className="text-xs text-gray-500 mt-2 truncate w-full text-center">
              {data.labels[index]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Line Chart Widget (Simple SVG)
// =============================================================================

interface LineChartProps {
  title: string;
  data: ChartData;
  loading?: boolean;
  height?: number;
  color?: string;
}

export function LineChart({
  title,
  data,
  loading = false,
  height = 200,
  color = '#4F46E5',
}: LineChartProps) {
  if (loading || data.values.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        <div className="h-48 bg-gray-100 rounded"></div>
      </div>
    );
  }

  const padding = 40;
  const width = 400;
  const chartHeight = height - padding;
  const maxValue = Math.max(...data.values, 1);
  const minValue = Math.min(...data.values, 0);
  const range = maxValue - minValue || 1;

  const points = data.values.map((value, index) => ({
    x: padding + (index / (data.values.length - 1 || 1)) * (width - padding * 2),
    y: chartHeight - ((value - minValue) / range) * (chartHeight - padding),
  }));

  const pathD = points
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`)
    .join(' ');

  const areaD = `${pathD} L ${points[points.length - 1].x} ${chartHeight - padding} L ${padding} ${chartHeight - padding} Z`;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full">
        {/* Grid lines */}
        {[0, 25, 50, 75, 100].map((pct) => (
          <line
            key={pct}
            x1={padding}
            y1={chartHeight - (pct / 100) * (chartHeight - padding)}
            x2={width - padding}
            y2={chartHeight - (pct / 100) * (chartHeight - padding)}
            stroke="#E5E7EB"
            strokeWidth="1"
          />
        ))}
        
        {/* Area fill */}
        <path d={areaD} fill={color} fillOpacity="0.1" />
        
        {/* Line */}
        <path d={pathD} fill="none" stroke={color} strokeWidth="2" />
        
        {/* Points */}
        {points.map((p, i) => (
          <circle key={i} cx={p.x} cy={p.y} r="4" fill={color}>
            <title>{`${data.labels[i]}: ${data.values[i].toLocaleString()}`}</title>
          </circle>
        ))}
      </svg>
    </div>
  );
}

// =============================================================================
// Donut Chart Widget
// =============================================================================

interface DonutChartProps {
  title: string;
  data: { label: string; value: number; color: string }[];
  loading?: boolean;
}

export function DonutChart({ title, data, loading = false }: DonutChartProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        <div className="h-48 bg-gray-100 rounded-full mx-auto w-48"></div>
      </div>
    );
  }

  const total = data.reduce((sum, d) => sum + d.value, 0) || 1;
  const size = 160;
  const strokeWidth = 30;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  let offset = 0;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          {data.map((item, index) => {
            const percentage = item.value / total;
            const strokeDasharray = `${percentage * circumference} ${circumference}`;
            const strokeDashoffset = -offset;
            offset += percentage * circumference;
            
            return (
              <circle
                key={index}
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="none"
                stroke={item.color}
                strokeWidth={strokeWidth}
                strokeDasharray={strokeDasharray}
                strokeDashoffset={strokeDashoffset}
                className="transition-all duration-500"
              >
                <title>{`${item.label}: ${item.value.toLocaleString()} (${(percentage * 100).toFixed(1)}%)`}</title>
              </circle>
            );
          })}
        </svg>
      </div>
      
      <div className="mt-4 space-y-2">
        {data.map((item, index) => (
          <div key={index} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <span
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: item.color }}
              ></span>
              <span className="text-gray-600">{item.label}</span>
            </div>
            <span className="font-medium text-gray-900">
              {item.value.toLocaleString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Top Items List Widget
// =============================================================================

interface TopItemsListProps {
  title: string;
  items: TopItem[];
  loading?: boolean;
  valuePrefix?: string;
  valueSuffix?: string;
  secondaryLabel?: string;
}

export function TopItemsList({
  title,
  items,
  loading = false,
  valuePrefix = '',
  valueSuffix = '',
  secondaryLabel,
}: TopItemsListProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="flex items-center gap-3 py-3">
            <div className="h-8 w-8 bg-gray-200 rounded-full"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-24"></div>
            </div>
            <div className="h-4 bg-gray-200 rounded w-16"></div>
          </div>
        ))}
      </div>
    );
  }

  const maxValue = Math.max(...items.map((i) => i.value), 1);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="space-y-4">
        {items.map((item, index) => (
          <div key={item.id} className="flex items-center gap-3">
            <span className="w-6 h-6 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-xs font-bold">
              {index + 1}
            </span>
            
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium text-gray-900 truncate">
                {item.name}
              </div>
              {item.secondaryValue !== undefined && secondaryLabel && (
                <div className="text-xs text-gray-500">
                  {secondaryLabel}: {item.secondaryValue.toLocaleString()}
                </div>
              )}
              
              <div className="mt-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-500 rounded-full transition-all duration-500"
                  style={{ width: `${(item.value / maxValue) * 100}%` }}
                ></div>
              </div>
            </div>
            
            <span className="text-sm font-semibold text-gray-900">
              {valuePrefix}{item.value.toLocaleString()}{valueSuffix}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Activity Feed Widget
// =============================================================================

interface Activity {
  id: string | number;
  type: string;
  action: string;
  description: string;
  timestamp: string;
}

interface ActivityFeedProps {
  title: string;
  activities: Activity[];
  loading?: boolean;
}

export function ActivityFeed({ title, activities, loading = false }: ActivityFeedProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="flex gap-3 py-3">
            <div className="h-10 w-10 bg-gray-200 rounded-full"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-32 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-24"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const typeIcons: Record<string, string> = {
    invoice: '📄',
    stock: '📦',
    user: '👤',
    payment: '💰',
    default: '📌',
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {activities.map((activity) => (
          <div key={activity.id} className="flex gap-3 group">
            <span className="text-2xl">
              {typeIcons[activity.type] || typeIcons.default}
            </span>
            
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">
                {activity.action}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {activity.description}
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {formatTime(activity.timestamp)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Alert Widget
// =============================================================================

interface AlertItem {
  id: string | number;
  type: 'warning' | 'error' | 'info' | 'success';
  title: string;
  message: string;
}

interface AlertsWidgetProps {
  title: string;
  alerts: AlertItem[];
  loading?: boolean;
}

export function AlertsWidget({ title, alerts, loading = false }: AlertsWidgetProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-32 mb-4"></div>
        <div className="h-24 bg-gray-100 rounded"></div>
      </div>
    );
  }

  const typeStyles = {
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    error: 'bg-red-50 border-red-200 text-red-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    success: 'bg-green-50 border-green-200 text-green-800',
  };

  const typeIcons = {
    warning: '⚠️',
    error: '❌',
    info: 'ℹ️',
    success: '✅',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      {alerts.length === 0 ? (
        <p className="text-gray-500 text-sm">No alerts at this time</p>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-3 rounded-lg border ${typeStyles[alert.type]}`}
            >
              <div className="flex gap-2">
                <span>{typeIcons[alert.type]}</span>
                <div>
                  <p className="font-medium text-sm">{alert.title}</p>
                  <p className="text-xs opacity-80">{alert.message}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// =============================================================================
// Exports
// =============================================================================

export default {
  StatCard,
  BarChart,
  LineChart,
  DonutChart,
  TopItemsList,
  ActivityFeed,
  AlertsWidget,
};

