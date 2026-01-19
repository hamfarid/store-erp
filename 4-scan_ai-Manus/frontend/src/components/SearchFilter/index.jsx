/**
 * SearchFilter Component - Advanced Search & Filter System
 * =========================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useCallback, useEffect, useRef } from 'react';
import { 
  Search, Filter, X, ChevronDown, Check, Calendar, 
  SlidersHorizontal, RotateCcw
} from 'lucide-react';

// ============================================
// Search Input
// ============================================
export const SearchInput = ({
  value,
  onChange,
  placeholder,
  placeholderAr,
  onClear,
  debounceMs = 300,
  size = 'md',
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [localValue, setLocalValue] = useState(value);
  const timeoutRef = useRef(null);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleChange = useCallback((e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);

    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      onChange?.(newValue);
    }, debounceMs);
  }, [onChange, debounceMs]);

  const handleClear = useCallback(() => {
    setLocalValue('');
    onChange?.('');
    onClear?.();
  }, [onChange, onClear]);

  const sizes = {
    sm: 'py-1.5 text-sm',
    md: 'py-2 text-sm',
    lg: 'py-3 text-base'
  };

  return (
    <div className={`relative ${className}`}>
      <Search className={`
        absolute top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400
        ${isRTL ? 'right-3' : 'left-3'}
      `} />
      <input
        type="text"
        value={localValue}
        onChange={handleChange}
        placeholder={isRTL ? placeholderAr : placeholder}
        className={`
          w-full bg-gray-100 dark:bg-gray-800 rounded-lg
          focus:outline-none focus:ring-2 focus:ring-emerald-500
          transition-all duration-200
          ${isRTL ? 'pr-10 pl-10' : 'pl-10 pr-10'}
          ${sizes[size]}
        `}
      />
      {localValue && (
        <button
          onClick={handleClear}
          className={`
            absolute top-1/2 -translate-y-1/2 p-1 rounded-full
            text-gray-400 hover:text-gray-600 hover:bg-gray-200
            dark:hover:bg-gray-700 transition-colors
            ${isRTL ? 'left-2' : 'right-2'}
          `}
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};

// ============================================
// Filter Select
// ============================================
export const FilterSelect = ({
  value,
  onChange,
  options = [],
  placeholder,
  placeholderAr,
  multiple = false,
  size = 'md',
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (optionValue) => {
    if (multiple) {
      const newValue = Array.isArray(value) ? [...value] : [];
      const index = newValue.indexOf(optionValue);
      if (index > -1) {
        newValue.splice(index, 1);
      } else {
        newValue.push(optionValue);
      }
      onChange?.(newValue);
    } else {
      onChange?.(optionValue);
      setIsOpen(false);
    }
  };

  const getDisplayValue = () => {
    if (multiple && Array.isArray(value) && value.length > 0) {
      return `${value.length} ${isRTL ? 'محدد' : 'selected'}`;
    }
    if (!multiple && value) {
      const option = options.find(o => o.value === value);
      return isRTL ? option?.labelAr : option?.label;
    }
    return isRTL ? placeholderAr : placeholder;
  };

  const isSelected = (optionValue) => {
    if (multiple) {
      return Array.isArray(value) && value.includes(optionValue);
    }
    return value === optionValue;
  };

  const sizes = {
    sm: 'py-1.5 px-3 text-sm',
    md: 'py-2 px-3 text-sm',
    lg: 'py-3 px-4 text-base'
  };

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`
          w-full flex items-center justify-between gap-2
          bg-gray-100 dark:bg-gray-800 rounded-lg
          hover:bg-gray-200 dark:hover:bg-gray-700
          focus:outline-none focus:ring-2 focus:ring-emerald-500
          transition-all duration-200
          ${sizes[size]}
        `}
      >
        <span className={`truncate ${!value ? 'text-gray-500' : 'text-gray-800 dark:text-white'}`}>
          {getDisplayValue()}
        </span>
        <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className={`
          absolute z-20 top-full mt-1 w-full min-w-[160px]
          bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700
          rounded-lg shadow-lg py-1 max-h-60 overflow-y-auto
        `}>
          {options.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => handleSelect(option.value)}
              className={`
                w-full px-3 py-2 text-sm flex items-center justify-between
                ${isRTL ? 'text-right' : 'text-left'}
                ${isSelected(option.value)
                  ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }
              `}
            >
              <span>{isRTL ? option.labelAr : option.label}</span>
              {isSelected(option.value) && <Check className="w-4 h-4" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// ============================================
// Date Range Filter
// ============================================
export const DateRangeFilter = ({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  label,
  labelAr,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';

  return (
    <div className={className}>
      {(label || labelAr) && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
          {isRTL ? labelAr : label}
        </label>
      )}
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Calendar className={`absolute top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 ${isRTL ? 'right-3' : 'left-3'}`} />
          <input
            type="date"
            value={startDate || ''}
            onChange={(e) => onStartDateChange?.(e.target.value)}
            className={`
              w-full py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm
              focus:outline-none focus:ring-2 focus:ring-emerald-500
              ${isRTL ? 'pr-10 pl-3' : 'pl-10 pr-3'}
            `}
          />
        </div>
        <span className="text-gray-400">-</span>
        <div className="relative flex-1">
          <Calendar className={`absolute top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 ${isRTL ? 'right-3' : 'left-3'}`} />
          <input
            type="date"
            value={endDate || ''}
            onChange={(e) => onEndDateChange?.(e.target.value)}
            className={`
              w-full py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm
              focus:outline-none focus:ring-2 focus:ring-emerald-500
              ${isRTL ? 'pr-10 pl-3' : 'pl-10 pr-3'}
            `}
          />
        </div>
      </div>
    </div>
  );
};

// ============================================
// Complete Search Filter Bar
// ============================================
export const SearchFilterBar = ({
  searchValue,
  onSearchChange,
  searchPlaceholder = 'Search...',
  searchPlaceholderAr = 'بحث...',
  filters = [],
  onReset,
  showReset = true,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showFilters, setShowFilters] = useState(false);

  const hasActiveFilters = filters.some(f => {
    if (f.multiple) {
      return Array.isArray(f.value) && f.value.length > 0;
    }
    return f.value !== '' && f.value !== undefined;
  });

  return (
    <div className={`space-y-3 ${className}`}>
      {/* Main bar */}
      <div className="flex flex-wrap items-center gap-3">
        <SearchInput
          value={searchValue}
          onChange={onSearchChange}
          placeholder={searchPlaceholder}
          placeholderAr={searchPlaceholderAr}
          className="flex-1 min-w-[200px] max-w-md"
        />

        {/* Quick filters */}
        <div className="flex items-center gap-2">
          {filters.slice(0, 2).map((filter, index) => (
            <FilterSelect
              key={index}
              value={filter.value}
              onChange={filter.onChange}
              options={filter.options}
              placeholder={filter.placeholder}
              placeholderAr={filter.placeholderAr}
              multiple={filter.multiple}
              className="w-40"
            />
          ))}
        </div>

        {/* More filters toggle */}
        {filters.length > 2 && (
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`
              flex items-center gap-2 px-3 py-2 rounded-lg text-sm
              ${showFilters
                ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300'
              }
              hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors
            `}
          >
            <SlidersHorizontal className="w-4 h-4" />
            {isRTL ? 'المزيد' : 'More'}
            {hasActiveFilters && (
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
            )}
          </button>
        )}

        {/* Reset button */}
        {showReset && hasActiveFilters && (
          <button
            onClick={onReset}
            className="flex items-center gap-1 px-3 py-2 text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            {isRTL ? 'إعادة ضبط' : 'Reset'}
          </button>
        )}
      </div>

      {/* Extended filters */}
      {showFilters && filters.length > 2 && (
        <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filters.slice(2).map((filter, index) => {
              if (filter.type === 'dateRange') {
                return (
                  <DateRangeFilter
                    key={index}
                    startDate={filter.startDate}
                    endDate={filter.endDate}
                    onStartDateChange={filter.onStartDateChange}
                    onEndDateChange={filter.onEndDateChange}
                    label={filter.label}
                    labelAr={filter.labelAr}
                  />
                );
              }
              return (
                <div key={index}>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                    {isRTL ? filter.labelAr : filter.label}
                  </label>
                  <FilterSelect
                    value={filter.value}
                    onChange={filter.onChange}
                    options={filter.options}
                    placeholder={filter.placeholder}
                    placeholderAr={filter.placeholderAr}
                    multiple={filter.multiple}
                    className="w-full"
                  />
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================
// Filter Tags (Active Filters Display)
// ============================================
export const FilterTags = ({
  filters = [],
  onRemove,
  onClearAll,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';

  const activeFilters = filters.filter(f => {
    if (f.multiple) {
      return Array.isArray(f.value) && f.value.length > 0;
    }
    return f.value !== '' && f.value !== undefined;
  });

  if (activeFilters.length === 0) return null;

  return (
    <div className={`flex flex-wrap items-center gap-2 ${className}`}>
      <span className="text-sm text-gray-500">
        {isRTL ? 'الفلاتر:' : 'Filters:'}
      </span>
      
      {activeFilters.map((filter, index) => {
        const values = filter.multiple ? filter.value : [filter.value];
        return values.map((val, valIndex) => {
          const option = filter.options?.find(o => o.value === val);
          const label = isRTL ? option?.labelAr : option?.label;
          return (
            <span
              key={`${index}-${valIndex}`}
              className="inline-flex items-center gap-1 px-2 py-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-sm rounded-full"
            >
              <span className="text-xs text-emerald-500">{isRTL ? filter.labelAr : filter.label}:</span>
              {label || val}
              <button
                onClick={() => onRemove?.(filter.key, val)}
                className="p-0.5 hover:bg-emerald-200 dark:hover:bg-emerald-800 rounded-full transition-colors"
              >
                <X className="w-3 h-3" />
              </button>
            </span>
          );
        });
      })}

      <button
        onClick={onClearAll}
        className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
      >
        {isRTL ? 'مسح الكل' : 'Clear all'}
      </button>
    </div>
  );
};

export default { SearchInput, FilterSelect, DateRangeFilter, SearchFilterBar, FilterTags };
