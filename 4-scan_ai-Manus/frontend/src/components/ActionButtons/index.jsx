/**
 * ActionButtons Component - Reusable Action Button Group
 * =======================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState } from 'react';
import { 
  Edit, Trash2, Eye, MoreVertical, MoreHorizontal,
  Download, Share2, Copy, Archive, Star, Pin,
  CheckCircle, XCircle, RefreshCw, Settings
} from 'lucide-react';

// ============================================
// Action Button Icons Map
// ============================================
const ACTION_ICONS = {
  view: Eye,
  edit: Edit,
  delete: Trash2,
  download: Download,
  share: Share2,
  copy: Copy,
  archive: Archive,
  star: Star,
  pin: Pin,
  approve: CheckCircle,
  reject: XCircle,
  refresh: RefreshCw,
  settings: Settings
};

// ============================================
// Single Action Button
// ============================================
export const ActionButton = ({ 
  action, 
  icon: CustomIcon,
  label,
  labelAr,
  onClick, 
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const Icon = CustomIcon || ACTION_ICONS[action] || Settings;

  const variants = {
    default: 'text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700',
    primary: 'text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/20',
    danger: 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20',
    warning: 'text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/20',
    success: 'text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20'
  };

  const sizes = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3'
  };

  const iconSizes = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  };

  return (
    <button
      onClick={(e) => { e.stopPropagation(); onClick?.(); }}
      disabled={disabled || loading}
      title={isRTL ? labelAr : label}
      className={`
        inline-flex items-center justify-center rounded-lg
        transition-all duration-200
        ${variants[variant]}
        ${sizes[size]}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        ${className}
      `}
    >
      {loading ? (
        <RefreshCw className={`${iconSizes[size]} animate-spin`} />
      ) : (
        <Icon className={iconSizes[size]} />
      )}
    </button>
  );
};

// ============================================
// Action Button Group (Inline)
// ============================================
export const ActionButtonGroup = ({
  actions = [],
  size = 'md',
  maxVisible = 3,
  className = ''
}) => {
  const [showMore, setShowMore] = useState(false);
  const isRTL = document.documentElement.dir === 'rtl';

  const visibleActions = actions.slice(0, maxVisible);
  const hiddenActions = actions.slice(maxVisible);

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {visibleActions.map((action, index) => (
        <ActionButton
          key={index}
          action={action.action}
          icon={action.icon}
          label={action.label}
          labelAr={action.labelAr}
          onClick={action.onClick}
          variant={action.variant}
          size={size}
          disabled={action.disabled}
          loading={action.loading}
        />
      ))}

      {hiddenActions.length > 0 && (
        <div className="relative">
          <button
            onClick={(e) => { e.stopPropagation(); setShowMore(!showMore); }}
            className={`
              inline-flex items-center justify-center rounded-lg
              text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700
              transition-colors p-2
            `}
          >
            <MoreHorizontal className="w-4 h-4" />
          </button>

          {showMore && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setShowMore(false)} />
              <div className={`
                absolute z-20 top-full mt-1 py-1
                ${isRTL ? 'left-0' : 'right-0'}
                min-w-[160px] bg-white dark:bg-gray-800
                border border-gray-200 dark:border-gray-700
                rounded-lg shadow-lg
              `}>
                {hiddenActions.map((action, index) => {
                  const Icon = action.icon || ACTION_ICONS[action.action] || Settings;
                  return (
                    <button
                      key={index}
                      onClick={(e) => { e.stopPropagation(); action.onClick?.(); setShowMore(false); }}
                      disabled={action.disabled}
                      className={`
                        w-full px-3 py-2 text-sm flex items-center gap-2
                        ${action.variant === 'danger' 
                          ? 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20' 
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                        }
                        ${isRTL ? 'text-right flex-row-reverse' : 'text-left'}
                        ${action.disabled ? 'opacity-50 cursor-not-allowed' : ''}
                      `}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{isRTL ? action.labelAr : action.label}</span>
                    </button>
                  );
                })}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

// ============================================
// Dropdown Menu Actions
// ============================================
export const ActionDropdown = ({
  actions = [],
  trigger,
  position = 'bottom-right',
  size = 'md',
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const isRTL = document.documentElement.dir === 'rtl';

  const positions = {
    'bottom-right': isRTL ? 'top-full mt-1 left-0' : 'top-full mt-1 right-0',
    'bottom-left': isRTL ? 'top-full mt-1 right-0' : 'top-full mt-1 left-0',
    'top-right': isRTL ? 'bottom-full mb-1 left-0' : 'bottom-full mb-1 right-0',
    'top-left': isRTL ? 'bottom-full mb-1 right-0' : 'bottom-full mb-1 left-0'
  };

  return (
    <div className={`relative inline-block ${className}`}>
      {trigger ? (
        <div onClick={(e) => { e.stopPropagation(); setIsOpen(!isOpen); }}>
          {trigger}
        </div>
      ) : (
        <button
          onClick={(e) => { e.stopPropagation(); setIsOpen(!isOpen); }}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <MoreVertical className="w-5 h-5" />
        </button>
      )}

      {isOpen && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
          <div className={`
            absolute z-20 ${positions[position]}
            min-w-[180px] py-1
            bg-white dark:bg-gray-800
            border border-gray-200 dark:border-gray-700
            rounded-lg shadow-lg
            animate-fadeIn
          `}>
            {actions.map((action, index) => {
              if (action.divider) {
                return <hr key={index} className="my-1 border-gray-200 dark:border-gray-700" />;
              }

              const Icon = action.icon || ACTION_ICONS[action.action] || Settings;
              
              return (
                <button
                  key={index}
                  onClick={(e) => { e.stopPropagation(); action.onClick?.(); setIsOpen(false); }}
                  disabled={action.disabled}
                  className={`
                    w-full px-4 py-2.5 text-sm flex items-center gap-3
                    transition-colors duration-150
                    ${action.variant === 'danger'
                      ? 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }
                    ${isRTL ? 'text-right flex-row-reverse' : 'text-left'}
                    ${action.disabled ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <span className="flex-1">{isRTL ? action.labelAr : action.label}</span>
                  {action.badge && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-emerald-100 text-emerald-600">
                      {action.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};

// ============================================
// CRUD Action Set (Common Pattern)
// ============================================
export const CrudActions = ({
  onView,
  onEdit,
  onDelete,
  viewLabel = { en: 'View', ar: 'عرض' },
  editLabel = { en: 'Edit', ar: 'تعديل' },
  deleteLabel = { en: 'Delete', ar: 'حذف' },
  showView = true,
  showEdit = true,
  showDelete = true,
  size = 'md',
  asDropdown = false
}) => {
  const actions = [];

  if (showView && onView) {
    actions.push({ action: 'view', label: viewLabel.en, labelAr: viewLabel.ar, onClick: onView });
  }
  if (showEdit && onEdit) {
    actions.push({ action: 'edit', label: editLabel.en, labelAr: editLabel.ar, onClick: onEdit });
  }
  if (showDelete && onDelete) {
    actions.push({ action: 'delete', label: deleteLabel.en, labelAr: deleteLabel.ar, onClick: onDelete, variant: 'danger' });
  }

  if (asDropdown) {
    return <ActionDropdown actions={actions} size={size} />;
  }

  return <ActionButtonGroup actions={actions} size={size} />;
};

export default { ActionButton, ActionButtonGroup, ActionDropdown, CrudActions };
