/**
 * DateRangePicker Component
 * @file frontend/src/components/common/DateRangePicker.jsx
 * 
 * منتقي نطاق التاريخ مع دعم العربية
 */

import React, { useState, useCallback, useMemo } from 'react';
import { format, subDays, startOfMonth, endOfMonth, startOfYear, subMonths, subYears } from 'date-fns';
import { ar } from 'date-fns/locale';
import { Calendar as CalendarIcon, ChevronDown } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from '../ui/button';
import { Calendar } from '../ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '../ui/popover';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';

/**
 * خيارات الفترات المحددة مسبقاً
 */
const PRESET_RANGES = {
  today: {
    label: 'اليوم',
    getValue: () => {
      const today = new Date();
      return { from: today, to: today };
    }
  },
  yesterday: {
    label: 'أمس',
    getValue: () => {
      const yesterday = subDays(new Date(), 1);
      return { from: yesterday, to: yesterday };
    }
  },
  last7days: {
    label: 'آخر 7 أيام',
    getValue: () => ({
      from: subDays(new Date(), 6),
      to: new Date()
    })
  },
  last30days: {
    label: 'آخر 30 يوم',
    getValue: () => ({
      from: subDays(new Date(), 29),
      to: new Date()
    })
  },
  thisMonth: {
    label: 'هذا الشهر',
    getValue: () => ({
      from: startOfMonth(new Date()),
      to: new Date()
    })
  },
  lastMonth: {
    label: 'الشهر الماضي',
    getValue: () => {
      const lastMonth = subMonths(new Date(), 1);
      return {
        from: startOfMonth(lastMonth),
        to: endOfMonth(lastMonth)
      };
    }
  },
  thisYear: {
    label: 'هذا العام',
    getValue: () => ({
      from: startOfYear(new Date()),
      to: new Date()
    })
  },
  lastYear: {
    label: 'العام الماضي',
    getValue: () => {
      const lastYear = subYears(new Date(), 1);
      return {
        from: startOfYear(lastYear),
        to: new Date(lastYear.getFullYear(), 11, 31)
      };
    }
  },
  custom: {
    label: 'فترة مخصصة',
    getValue: () => null
  }
};

/**
 * DateRangePicker Component
 */
export function DateRangePicker({
  value,
  onChange,
  className = '',
  placeholder = 'اختر الفترة',
  showPresets = true,
  minDate,
  maxDate,
  disabled = false,
  numberOfMonths = 2
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState(null);

  const formatDateRange = useCallback((range) => {
    if (!range?.from) return placeholder;
    
    if (!range.to || range.from.toDateString() === range.to.toDateString()) {
      return format(range.from, 'dd MMMM yyyy', { locale: ar });
    }
    
    return `${format(range.from, 'dd MMM', { locale: ar })} - ${format(range.to, 'dd MMM yyyy', { locale: ar })}`;
  }, [placeholder]);

  const handlePresetChange = useCallback((presetKey) => {
    setSelectedPreset(presetKey);
    
    if (presetKey === 'custom') {
      return;
    }
    
    const preset = PRESET_RANGES[presetKey];
    if (preset) {
      const range = preset.getValue();
      onChange?.(range);
      setIsOpen(false);
    }
  }, [onChange]);

  const handleCalendarSelect = useCallback((range) => {
    onChange?.(range);
    setSelectedPreset('custom');
    
    // Close popover if both dates are selected
    if (range?.from && range?.to) {
      setTimeout(() => setIsOpen(false), 200);
    }
  }, [onChange]);

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className={cn(
            'w-full justify-start text-right font-normal',
            !value?.from && 'text-muted-foreground',
            className
          )}
          disabled={disabled}
        >
          <CalendarIcon className="ml-2 h-4 w-4" />
          {formatDateRange(value)}
          <ChevronDown className="mr-auto h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <div className="flex">
          {/* Presets sidebar */}
          {showPresets && (
            <div className="border-l p-2 space-y-1">
              {Object.entries(PRESET_RANGES).map(([key, preset]) => (
                <Button
                  key={key}
                  variant={selectedPreset === key ? 'default' : 'ghost'}
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => handlePresetChange(key)}
                >
                  {preset.label}
                </Button>
              ))}
            </div>
          )}
          
          {/* Calendar */}
          <div className="p-3">
            <Calendar
              mode="range"
              selected={value}
              onSelect={handleCalendarSelect}
              numberOfMonths={numberOfMonths}
              locale={ar}
              dir="rtl"
              disabled={(date) => {
                if (minDate && date < minDate) return true;
                if (maxDate && date > maxDate) return true;
                return false;
              }}
            />
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}

/**
 * SimpleDatePicker - منتقي تاريخ واحد
 */
export function SimpleDatePicker({
  value,
  onChange,
  className = '',
  placeholder = 'اختر التاريخ',
  minDate,
  maxDate,
  disabled = false
}) {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = useCallback((date) => {
    onChange?.(date);
    setIsOpen(false);
  }, [onChange]);

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className={cn(
            'w-full justify-start text-right font-normal',
            !value && 'text-muted-foreground',
            className
          )}
          disabled={disabled}
        >
          <CalendarIcon className="ml-2 h-4 w-4" />
          {value ? format(value, 'dd MMMM yyyy', { locale: ar }) : placeholder}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <Calendar
          mode="single"
          selected={value}
          onSelect={handleSelect}
          locale={ar}
          dir="rtl"
          disabled={(date) => {
            if (minDate && date < minDate) return true;
            if (maxDate && date > maxDate) return true;
            return false;
          }}
        />
      </PopoverContent>
    </Popover>
  );
}

/**
 * MonthYearPicker - منتقي الشهر والسنة
 */
export function MonthYearPicker({
  value,
  onChange,
  className = '',
  minYear = 2020,
  maxYear = new Date().getFullYear() + 5,
  disabled = false
}) {
  const [month, setMonth] = useState(value?.getMonth() ?? new Date().getMonth());
  const [year, setYear] = useState(value?.getFullYear() ?? new Date().getFullYear());

  const months = useMemo(() => [
    'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
    'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
  ], []);

  const years = useMemo(() => {
    const arr = [];
    for (let y = minYear; y <= maxYear; y++) {
      arr.push(y);
    }
    return arr;
  }, [minYear, maxYear]);

  const handleChange = useCallback((newMonth, newYear) => {
    setMonth(newMonth);
    setYear(newYear);
    onChange?.(new Date(newYear, newMonth, 1));
  }, [onChange]);

  return (
    <div className={cn('flex gap-2', className)}>
      <Select
        value={String(month)}
        onValueChange={(v) => handleChange(parseInt(v), year)}
        disabled={disabled}
      >
        <SelectTrigger className="w-32">
          <SelectValue placeholder="الشهر" />
        </SelectTrigger>
        <SelectContent>
          {months.map((m, idx) => (
            <SelectItem key={idx} value={String(idx)}>
              {m}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        value={String(year)}
        onValueChange={(v) => handleChange(month, parseInt(v))}
        disabled={disabled}
      >
        <SelectTrigger className="w-24">
          <SelectValue placeholder="السنة" />
        </SelectTrigger>
        <SelectContent>
          {years.map((y) => (
            <SelectItem key={y} value={String(y)}>
              {y}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

export default DateRangePicker;
