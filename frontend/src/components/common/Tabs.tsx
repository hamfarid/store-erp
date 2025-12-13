/**
 * P3.89: Tabs Component
 * 
 * Accessible tabs component with multiple variants.
 */

import React, { useState, useCallback, createContext, useContext } from 'react';

// =============================================================================
// Types
// =============================================================================

type TabsVariant = 'underline' | 'pills' | 'enclosed' | 'segment';
type TabsSize = 'sm' | 'md' | 'lg';

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  badge?: number | string;
  disabled?: boolean;
  content?: React.ReactNode;
}

interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
  variant: TabsVariant;
  size: TabsSize;
}

// =============================================================================
// Context
// =============================================================================

const TabsContext = createContext<TabsContextType | null>(null);

const useTabsContext = () => {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tab components must be used within a Tabs component');
  }
  return context;
};

// =============================================================================
// Main Tabs Component
// =============================================================================

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  activeTab?: string;
  onChange?: (tabId: string) => void;
  variant?: TabsVariant;
  size?: TabsSize;
  fullWidth?: boolean;
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  defaultTab,
  activeTab: controlledActiveTab,
  onChange,
  variant = 'underline',
  size = 'md',
  fullWidth = false,
  className = '',
}) => {
  const [internalActiveTab, setInternalActiveTab] = useState(
    defaultTab || tabs[0]?.id || ''
  );

  const activeTab = controlledActiveTab ?? internalActiveTab;

  const handleTabChange = useCallback((tabId: string) => {
    if (!controlledActiveTab) {
      setInternalActiveTab(tabId);
    }
    onChange?.(tabId);
  }, [controlledActiveTab, onChange]);

  const activeContent = tabs.find(tab => tab.id === activeTab)?.content;

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleTabChange, variant, size }}>
      <div className={className} dir="rtl">
        <TabList tabs={tabs} fullWidth={fullWidth} />
        {activeContent && (
          <div className="mt-4">
            {activeContent}
          </div>
        )}
      </div>
    </TabsContext.Provider>
  );
};

// =============================================================================
// Tab List
// =============================================================================

interface TabListProps {
  tabs: Tab[];
  fullWidth?: boolean;
  className?: string;
}

export const TabList: React.FC<TabListProps> = ({
  tabs,
  fullWidth = false,
  className = '',
}) => {
  const { variant } = useTabsContext();

  const containerClasses: Record<TabsVariant, string> = {
    underline: 'border-b border-gray-200',
    pills: 'gap-2',
    enclosed: 'border-b border-gray-200',
    segment: 'p-1 bg-gray-100 rounded-lg',
  };

  return (
    <div
      role="tablist"
      className={`
        flex ${fullWidth ? 'w-full' : 'inline-flex'}
        ${containerClasses[variant]}
        ${className}
      `}
    >
      {tabs.map(tab => (
        <TabButton key={tab.id} tab={tab} fullWidth={fullWidth} />
      ))}
    </div>
  );
};

// =============================================================================
// Tab Button
// =============================================================================

interface TabButtonProps {
  tab: Tab;
  fullWidth?: boolean;
}

const TabButton: React.FC<TabButtonProps> = ({ tab, fullWidth }) => {
  const { activeTab, setActiveTab, variant, size } = useTabsContext();
  const isActive = activeTab === tab.id;

  const sizeClasses: Record<TabsSize, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  const getVariantClasses = () => {
    switch (variant) {
      case 'underline':
        return isActive
          ? 'border-b-2 border-indigo-600 text-indigo-600'
          : 'border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300';
      
      case 'pills':
        return isActive
          ? 'bg-indigo-600 text-white rounded-lg'
          : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg';
      
      case 'enclosed':
        return isActive
          ? 'bg-white text-indigo-600 border border-gray-200 border-b-white -mb-px rounded-t-lg'
          : 'text-gray-500 hover:text-gray-700';
      
      case 'segment':
        return isActive
          ? 'bg-white text-gray-900 shadow rounded-md'
          : 'text-gray-500 hover:text-gray-700';
      
      default:
        return '';
    }
  };

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`panel-${tab.id}`}
      id={`tab-${tab.id}`}
      tabIndex={isActive ? 0 : -1}
      disabled={tab.disabled}
      onClick={() => setActiveTab(tab.id)}
      className={`
        inline-flex items-center justify-center gap-2
        font-medium whitespace-nowrap
        transition-colors duration-150
        focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500
        ${sizeClasses[size]}
        ${getVariantClasses()}
        ${fullWidth ? 'flex-1' : ''}
        ${tab.disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      {tab.icon && <span className="w-5 h-5">{tab.icon}</span>}
      {tab.label}
      {tab.badge !== undefined && (
        <span className={`
          inline-flex items-center justify-center
          min-w-[20px] h-5 px-1.5
          text-xs font-medium rounded-full
          ${isActive 
            ? variant === 'pills' 
              ? 'bg-indigo-500 text-white' 
              : 'bg-indigo-100 text-indigo-600'
            : 'bg-gray-200 text-gray-600'
          }
        `}>
          {tab.badge}
        </span>
      )}
    </button>
  );
};

// =============================================================================
// Tab Panel
// =============================================================================

interface TabPanelProps {
  id: string;
  children: React.ReactNode;
  className?: string;
}

export const TabPanel: React.FC<TabPanelProps> = ({
  id,
  children,
  className = '',
}) => {
  const { activeTab } = useTabsContext();
  const isActive = activeTab === id;

  if (!isActive) return null;

  return (
    <div
      role="tabpanel"
      id={`panel-${id}`}
      aria-labelledby={`tab-${id}`}
      tabIndex={0}
      className={className}
    >
      {children}
    </div>
  );
};

// =============================================================================
// Vertical Tabs
// =============================================================================

interface VerticalTabsProps extends Omit<TabsProps, 'variant'> {
  sideWidth?: string;
}

export const VerticalTabs: React.FC<VerticalTabsProps> = ({
  tabs,
  defaultTab,
  activeTab: controlledActiveTab,
  onChange,
  size = 'md',
  sideWidth = '200px',
  className = '',
}) => {
  const [internalActiveTab, setInternalActiveTab] = useState(
    defaultTab || tabs[0]?.id || ''
  );

  const activeTab = controlledActiveTab ?? internalActiveTab;

  const handleTabChange = useCallback((tabId: string) => {
    if (!controlledActiveTab) {
      setInternalActiveTab(tabId);
    }
    onChange?.(tabId);
  }, [controlledActiveTab, onChange]);

  const activeContent = tabs.find(tab => tab.id === activeTab)?.content;

  const sizeClasses: Record<TabsSize, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <div className={`flex gap-6 ${className}`} dir="rtl">
      {/* Sidebar */}
      <div
        role="tablist"
        aria-orientation="vertical"
        style={{ width: sideWidth }}
        className="flex-shrink-0 space-y-1"
      >
        {tabs.map(tab => {
          const isActive = activeTab === tab.id;
          
          return (
            <button
              key={tab.id}
              role="tab"
              aria-selected={isActive}
              disabled={tab.disabled}
              onClick={() => handleTabChange(tab.id)}
              className={`
                w-full flex items-center gap-2
                font-medium rounded-lg
                text-right
                transition-colors duration-150
                ${sizeClasses[size]}
                ${isActive
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-gray-600 hover:bg-gray-100'
                }
                ${tab.disabled ? 'opacity-50 cursor-not-allowed' : ''}
              `}
            >
              {tab.icon && <span className="w-5 h-5">{tab.icon}</span>}
              {tab.label}
              {tab.badge !== undefined && (
                <span className={`
                  mr-auto inline-flex items-center justify-center
                  min-w-[20px] h-5 px-1.5
                  text-xs font-medium rounded-full
                  ${isActive ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-200 text-gray-600'}
                `}>
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="flex-1">
        {activeContent}
      </div>
    </div>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Tabs;

