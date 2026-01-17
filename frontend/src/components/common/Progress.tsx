/**
 * P3.96: Progress Bar Component
 * 
 * Progress indicators with multiple variants and animations.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type ProgressColor = 'blue' | 'green' | 'red' | 'yellow' | 'indigo' | 'purple' | 'pink';
type ProgressSize = 'xs' | 'sm' | 'md' | 'lg';

interface ProgressBarProps {
  value: number;
  max?: number;
  color?: ProgressColor;
  size?: ProgressSize;
  showLabel?: boolean;
  labelPosition?: 'inside' | 'outside' | 'top';
  animated?: boolean;
  striped?: boolean;
  className?: string;
}

// =============================================================================
// Configuration
// =============================================================================

const colorClasses: Record<ProgressColor, string> = {
  blue: 'bg-blue-600',
  green: 'bg-green-600',
  red: 'bg-red-600',
  yellow: 'bg-yellow-500',
  indigo: 'bg-indigo-600',
  purple: 'bg-purple-600',
  pink: 'bg-pink-600',
};

const sizeClasses: Record<ProgressSize, string> = {
  xs: 'h-1',
  sm: 'h-2',
  md: 'h-3',
  lg: 'h-4',
};

// =============================================================================
// Progress Bar Component
// =============================================================================

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  color = 'blue',
  size = 'md',
  showLabel = false,
  labelPosition = 'outside',
  animated = false,
  striped = false,
  className = '',
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  const stripedClass = striped ? `
    bg-[length:1rem_1rem]
    bg-gradient-to-r from-transparent via-white/20 to-transparent
    bg-[linear-gradient(45deg,rgba(255,255,255,.15)_25%,transparent_25%,transparent_50%,rgba(255,255,255,.15)_50%,rgba(255,255,255,.15)_75%,transparent_75%,transparent)]
  ` : '';
  
  const animatedClass = animated ? 'animate-[progress-stripes_1s_linear_infinite]' : '';

  return (
    <div className={className}>
      {showLabel && labelPosition === 'top' && (
        <div className="flex justify-between mb-1">
          <span className="text-sm font-medium text-gray-700">التقدم</span>
          <span className="text-sm font-medium text-gray-700">{percentage.toFixed(0)}%</span>
        </div>
      )}
      
      <div className="flex items-center gap-3">
        <div className={`flex-1 bg-gray-200 rounded-full overflow-hidden ${sizeClasses[size]}`}>
          <div
            className={`
              h-full rounded-full transition-all duration-500 ease-out
              ${colorClasses[color]}
              ${stripedClass}
              ${animatedClass}
            `}
            style={{ width: `${percentage}%` }}
            role="progressbar"
            aria-valuenow={value}
            aria-valuemin={0}
            aria-valuemax={max}
          >
            {showLabel && labelPosition === 'inside' && size !== 'xs' && size !== 'sm' && (
              <span className="flex items-center justify-center h-full text-xs font-medium text-white">
                {percentage.toFixed(0)}%
              </span>
            )}
          </div>
        </div>
        
        {showLabel && labelPosition === 'outside' && (
          <span className="text-sm font-medium text-gray-700 w-12 text-left">
            {percentage.toFixed(0)}%
          </span>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Circular Progress
// =============================================================================

interface CircularProgressProps {
  value: number;
  max?: number;
  size?: number;
  strokeWidth?: number;
  color?: ProgressColor;
  showLabel?: boolean;
  className?: string;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  max = 100,
  size = 80,
  strokeWidth = 8,
  color = 'blue',
  showLabel = true,
  className = '',
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (percentage / 100) * circumference;

  const strokeColors: Record<ProgressColor, string> = {
    blue: '#2563eb',
    green: '#16a34a',
    red: '#dc2626',
    yellow: '#ca8a04',
    indigo: '#4f46e5',
    purple: '#9333ea',
    pink: '#db2777',
  };

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColors[color]}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-500 ease-out"
        />
      </svg>
      
      {showLabel && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-semibold text-gray-700">
            {percentage.toFixed(0)}%
          </span>
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Steps Progress
// =============================================================================

interface Step {
  id: string;
  label: string;
  description?: string;
}

interface StepsProgressProps {
  steps: Step[];
  currentStep: number;
  color?: ProgressColor;
  className?: string;
}

export const StepsProgress: React.FC<StepsProgressProps> = ({
  steps,
  currentStep,
  color = 'indigo',
  className = '',
}) => {
  return (
    <div className={className} dir="rtl">
      <ol className="flex items-center w-full">
        {steps.map((step, index) => {
          const isComplete = index < currentStep;
          const isCurrent = index === currentStep;
          
          return (
            <li
              key={step.id}
              className={`flex items-center ${index !== steps.length - 1 ? 'w-full' : ''}`}
            >
              <div className="flex flex-col items-center">
                <div
                  className={`
                    flex items-center justify-center w-10 h-10 rounded-full
                    transition-colors duration-200
                    ${isComplete ? colorClasses[color] + ' text-white' : 
                      isCurrent ? 'border-2 ' + colorClasses[color].replace('bg-', 'border-') + ' ' + colorClasses[color].replace('bg-', 'text-') : 
                      'border-2 border-gray-300 text-gray-500'}
                  `}
                >
                  {isComplete ? (
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <span className="text-sm font-medium">{index + 1}</span>
                  )}
                </div>
                <span className={`mt-2 text-sm font-medium ${isCurrent ? 'text-gray-900' : 'text-gray-500'}`}>
                  {step.label}
                </span>
                {step.description && (
                  <span className="text-xs text-gray-400">{step.description}</span>
                )}
              </div>
              
              {index !== steps.length - 1 && (
                <div className={`flex-1 h-0.5 mx-4 ${isComplete ? colorClasses[color] : 'bg-gray-300'}`} />
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
};

// =============================================================================
// Loading Progress
// =============================================================================

interface LoadingProgressProps {
  color?: ProgressColor;
  size?: ProgressSize;
  className?: string;
}

export const LoadingProgress: React.FC<LoadingProgressProps> = ({
  color = 'indigo',
  size = 'sm',
  className = '',
}) => {
  return (
    <div className={`w-full bg-gray-200 rounded-full overflow-hidden ${sizeClasses[size]} ${className}`}>
      <div
        className={`h-full ${colorClasses[color]} rounded-full animate-[loading-progress_1.5s_ease-in-out_infinite]`}
        style={{ width: '30%' }}
      />
      <style>{`
        @keyframes loading-progress {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(400%); }
        }
      `}</style>
    </div>
  );
};

// =============================================================================
// Multi-segment Progress
// =============================================================================

interface Segment {
  value: number;
  color: ProgressColor;
  label?: string;
}

interface MultiProgressProps {
  segments: Segment[];
  max?: number;
  size?: ProgressSize;
  showLabels?: boolean;
  className?: string;
}

export const MultiProgress: React.FC<MultiProgressProps> = ({
  segments,
  max = 100,
  size = 'md',
  showLabels = false,
  className = '',
}) => {
  const total = segments.reduce((sum, seg) => sum + seg.value, 0);
  
  return (
    <div className={className}>
      <div className={`flex bg-gray-200 rounded-full overflow-hidden ${sizeClasses[size]}`}>
        {segments.map((segment, index) => {
          const width = (segment.value / (max || total)) * 100;
          return (
            <div
              key={index}
              className={`h-full ${colorClasses[segment.color]} first:rounded-r-full last:rounded-l-full`}
              style={{ width: `${width}%` }}
              title={segment.label}
            />
          );
        })}
      </div>
      
      {showLabels && (
        <div className="flex justify-between mt-2 text-xs">
          {segments.map((segment, index) => (
            <div key={index} className="flex items-center gap-1">
              <span className={`w-2 h-2 rounded-full ${colorClasses[segment.color]}`} />
              <span className="text-gray-600">{segment.label || `${segment.value}`}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default ProgressBar;

