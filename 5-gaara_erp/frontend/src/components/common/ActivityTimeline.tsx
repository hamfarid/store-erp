/**
 * P2.70: Activity Timeline Component
 * 
 * Displays a vertical timeline of activities/events.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export type ActivityType = 
  | 'create'
  | 'update'
  | 'delete'
  | 'login'
  | 'logout'
  | 'payment'
  | 'invoice'
  | 'stock'
  | 'order'
  | 'notification'
  | 'system'
  | 'custom';

export interface ActivityItem {
  id: string;
  type: ActivityType;
  title: string;
  description?: string;
  timestamp: Date | string;
  user?: {
    id: string;
    name: string;
    avatar?: string;
  };
  metadata?: Record<string, any>;
  link?: string;
  icon?: React.ReactNode;
}

interface ActivityTimelineProps {
  activities: ActivityItem[];
  onActivityClick?: (activity: ActivityItem) => void;
  maxItems?: number;
  showLoadMore?: boolean;
  onLoadMore?: () => void;
  loading?: boolean;
  emptyMessage?: string;
  className?: string;
}

// =============================================================================
// Icons
// =============================================================================

const ActivityIcons: Record<ActivityType, React.ReactNode> = {
  create: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
    </svg>
  ),
  update: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
  ),
  delete: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
  ),
  login: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
    </svg>
  ),
  logout: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
    </svg>
  ),
  payment: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
  ),
  invoice: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  stock: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
    </svg>
  ),
  order: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
    </svg>
  ),
  notification: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
  ),
  system: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  ),
  custom: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

const ActivityColors: Record<ActivityType, string> = {
  create: 'bg-green-500',
  update: 'bg-blue-500',
  delete: 'bg-red-500',
  login: 'bg-indigo-500',
  logout: 'bg-gray-500',
  payment: 'bg-emerald-500',
  invoice: 'bg-purple-500',
  stock: 'bg-amber-500',
  order: 'bg-cyan-500',
  notification: 'bg-pink-500',
  system: 'bg-slate-500',
  custom: 'bg-violet-500',
};

// =============================================================================
// Helper Functions
// =============================================================================

function formatRelativeTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (days > 7) {
    return d.toLocaleDateString('ar-SA', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  }
  if (days > 0) return `منذ ${days} يوم`;
  if (hours > 0) return `منذ ${hours} ساعة`;
  if (minutes > 0) return `منذ ${minutes} دقيقة`;
  return 'الآن';
}

// =============================================================================
// Components
// =============================================================================

interface TimelineItemProps {
  activity: ActivityItem;
  isLast: boolean;
  onClick?: (activity: ActivityItem) => void;
}

const TimelineItem: React.FC<TimelineItemProps> = ({ activity, isLast, onClick }) => {
  const icon = activity.icon || ActivityIcons[activity.type];
  const color = ActivityColors[activity.type];
  
  return (
    <div 
      className={`relative flex items-start gap-4 pb-8 ${onClick ? 'cursor-pointer hover:bg-gray-50 rounded-lg p-2 -m-2 transition-colors' : ''}`}
      onClick={() => onClick?.(activity)}
    >
      {/* Timeline Line */}
      {!isLast && (
        <div className="absolute top-10 right-[19px] w-0.5 h-full bg-gray-200" />
      )}
      
      {/* Icon Circle */}
      <div className={`relative z-10 flex items-center justify-center w-10 h-10 rounded-full ${color} text-white shadow-md`}>
        {icon}
      </div>
      
      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2 mb-1">
          <h4 className="text-sm font-semibold text-gray-900 truncate">
            {activity.title}
          </h4>
          <span className="text-xs text-gray-500 whitespace-nowrap">
            {formatRelativeTime(activity.timestamp)}
          </span>
        </div>
        
        {activity.description && (
          <p className="text-sm text-gray-600 mb-2">
            {activity.description}
          </p>
        )}
        
        {activity.user && (
          <div className="flex items-center gap-2">
            {activity.user.avatar ? (
              <img 
                src={activity.user.avatar} 
                alt={activity.user.name}
                className="w-6 h-6 rounded-full"
              />
            ) : (
              <div className="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center text-xs font-medium text-gray-600">
                {activity.user.name.charAt(0)}
              </div>
            )}
            <span className="text-xs text-gray-500">{activity.user.name}</span>
          </div>
        )}
        
        {activity.link && (
          <a 
            href={activity.link}
            className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 mt-2"
            onClick={(e) => e.stopPropagation()}
          >
            عرض التفاصيل
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </a>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Main Component
// =============================================================================

export const ActivityTimeline: React.FC<ActivityTimelineProps> = ({
  activities,
  onActivityClick,
  maxItems = 10,
  showLoadMore = false,
  onLoadMore,
  loading = false,
  emptyMessage = 'لا توجد أنشطة',
  className = '',
}) => {
  const displayedActivities = maxItems ? activities.slice(0, maxItems) : activities;
  
  if (activities.length === 0 && !loading) {
    return (
      <div className={`text-center py-12 text-gray-500 ${className}`}>
        <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p>{emptyMessage}</p>
      </div>
    );
  }
  
  return (
    <div className={`${className}`} dir="rtl">
      {/* Timeline */}
      <div className="relative">
        {displayedActivities.map((activity, index) => (
          <TimelineItem
            key={activity.id}
            activity={activity}
            isLast={index === displayedActivities.length - 1}
            onClick={onActivityClick}
          />
        ))}
      </div>
      
      {/* Loading Indicator */}
      {loading && (
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
        </div>
      )}
      
      {/* Load More Button */}
      {showLoadMore && activities.length > maxItems && !loading && (
        <div className="text-center pt-4">
          <button
            onClick={onLoadMore}
            className="px-4 py-2 text-sm text-indigo-600 hover:text-indigo-800 font-medium"
          >
            عرض المزيد ({activities.length - maxItems} نشاط)
          </button>
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Compact Timeline (for sidebar)
// =============================================================================

interface CompactTimelineProps {
  activities: ActivityItem[];
  maxItems?: number;
  className?: string;
}

export const CompactTimeline: React.FC<CompactTimelineProps> = ({
  activities,
  maxItems = 5,
  className = '',
}) => {
  const displayedActivities = activities.slice(0, maxItems);
  
  return (
    <div className={`space-y-3 ${className}`} dir="rtl">
      {displayedActivities.map((activity) => (
        <div key={activity.id} className="flex items-start gap-3">
          <div className={`flex-shrink-0 w-2 h-2 mt-2 rounded-full ${ActivityColors[activity.type]}`} />
          <div className="flex-1 min-w-0">
            <p className="text-sm text-gray-900 truncate">{activity.title}</p>
            <p className="text-xs text-gray-500">{formatRelativeTime(activity.timestamp)}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ActivityTimeline;

