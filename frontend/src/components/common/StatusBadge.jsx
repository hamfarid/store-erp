/**
 * StatusBadge Component
 * @file frontend/src/components/common/StatusBadge.jsx
 * 
 * شارة الحالة مع ألوان مختلفة
 */

import React from 'react';
import { Badge } from '../ui/badge';
import { cn } from '../../lib/utils';

/**
 * تعريفات الحالات المعروفة
 */
const STATUS_CONFIG = {
  // حالات عامة
  active: { label: 'نشط', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  inactive: { label: 'غير نشط', variant: 'secondary', color: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400' },
  pending: { label: 'قيد الانتظار', variant: 'warning', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
  completed: { label: 'مكتمل', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  cancelled: { label: 'ملغي', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  
  // حالات الفواتير
  paid: { label: 'مدفوعة', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  unpaid: { label: 'غير مدفوعة', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  partial: { label: 'مدفوعة جزئياً', variant: 'warning', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
  overdue: { label: 'متأخرة', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  
  // حالات المخزون
  in_stock: { label: 'متوفر', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  out_of_stock: { label: 'نفذ', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  low_stock: { label: 'منخفض', variant: 'warning', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
  
  // حالات الطلبات
  draft: { label: 'مسودة', variant: 'secondary', color: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400' },
  processing: { label: 'قيد المعالجة', variant: 'info', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' },
  shipped: { label: 'تم الشحن', variant: 'info', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' },
  delivered: { label: 'تم التسليم', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  returned: { label: 'مرتجع', variant: 'warning', color: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400' },
  
  // حالات المستخدمين
  online: { label: 'متصل', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  offline: { label: 'غير متصل', variant: 'secondary', color: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400' },
  blocked: { label: 'محظور', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  
  // حالات اللوتات
  expired: { label: 'منتهي', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  expiring_soon: { label: 'ينتهي قريباً', variant: 'warning', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
  valid: { label: 'صالح', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  
  // حالات الموافقة
  approved: { label: 'معتمد', variant: 'success', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
  rejected: { label: 'مرفوض', variant: 'destructive', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' },
  review: { label: 'قيد المراجعة', variant: 'warning', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
};

/**
 * StatusBadge Component
 */
export function StatusBadge({
  status,
  label,
  variant,
  size = 'default',
  className = '',
  showDot = false,
  pulse = false
}) {
  // Get config for known status
  const config = STATUS_CONFIG[status?.toLowerCase()] || {
    label: label || status || 'غير محدد',
    variant: variant || 'secondary',
    color: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
  };

  const displayLabel = label || config.label;
  const badgeVariant = variant || config.variant;
  const colorClass = config.color;

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    default: 'text-xs px-2.5 py-0.5',
    lg: 'text-sm px-3 py-1'
  };

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full font-medium',
        sizeClasses[size],
        colorClass,
        className
      )}
    >
      {showDot && (
        <span
          className={cn(
            'w-2 h-2 rounded-full ml-1.5',
            badgeVariant === 'success' && 'bg-green-500',
            badgeVariant === 'destructive' && 'bg-red-500',
            badgeVariant === 'warning' && 'bg-yellow-500',
            badgeVariant === 'info' && 'bg-blue-500',
            badgeVariant === 'secondary' && 'bg-gray-500',
            pulse && 'animate-pulse'
          )}
        />
      )}
      {displayLabel}
    </span>
  );
}

/**
 * StockStatusBadge - شارة حالة المخزون
 */
export function StockStatusBadge({ quantity, minQuantity = 10, className = '' }) {
  let status = 'in_stock';
  
  if (quantity <= 0) {
    status = 'out_of_stock';
  } else if (quantity <= minQuantity) {
    status = 'low_stock';
  }

  return <StatusBadge status={status} showDot className={className} />;
}

/**
 * PaymentStatusBadge - شارة حالة الدفع
 */
export function PaymentStatusBadge({ paid, total, dueDate, className = '' }) {
  let status = 'unpaid';
  
  if (paid >= total) {
    status = 'paid';
  } else if (paid > 0) {
    status = 'partial';
  } else if (dueDate && new Date(dueDate) < new Date()) {
    status = 'overdue';
  }

  return <StatusBadge status={status} showDot className={className} />;
}

/**
 * LotExpiryBadge - شارة انتهاء اللوط
 */
export function LotExpiryBadge({ expiryDate, warningDays = 30, className = '' }) {
  const now = new Date();
  const expiry = new Date(expiryDate);
  const daysUntilExpiry = Math.ceil((expiry - now) / (1000 * 60 * 60 * 24));
  
  let status = 'valid';
  
  if (daysUntilExpiry < 0) {
    status = 'expired';
  } else if (daysUntilExpiry <= warningDays) {
    status = 'expiring_soon';
  }

  return (
    <StatusBadge 
      status={status} 
      label={daysUntilExpiry < 0 ? 'منتهي' : `${daysUntilExpiry} يوم`}
      showDot
      pulse={status === 'expiring_soon'}
      className={className} 
    />
  );
}

/**
 * OnlineStatusBadge - شارة حالة الاتصال
 */
export function OnlineStatusBadge({ isOnline, lastSeen, className = '' }) {
  return (
    <StatusBadge 
      status={isOnline ? 'online' : 'offline'} 
      showDot
      pulse={isOnline}
      className={className} 
    />
  );
}

export default StatusBadge;
