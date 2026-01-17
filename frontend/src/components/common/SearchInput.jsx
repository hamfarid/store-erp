/**
 * SearchInput Component
 * @file frontend/src/components/common/SearchInput.jsx
 * 
 * حقل البحث مع دعم التأخير والإكمال التلقائي
 */

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Search, X, Loader2 } from 'lucide-react';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { cn } from '../../lib/utils';
import { useDebounce } from '../../hooks/useDebounce';
import { useClickOutside } from '../../hooks/useClickOutside';

/**
 * SearchInput - حقل البحث الأساسي
 */
export function SearchInput({
  value = '',
  onChange,
  onSearch,
  placeholder = 'بحث...',
  debounceMs = 300,
  className = '',
  disabled = false,
  loading = false,
  autoFocus = false,
  clearable = true,
  size = 'default'
}) {
  const [localValue, setLocalValue] = useState(value);
  const debouncedValue = useDebounce(localValue, debounceMs);
  const inputRef = useRef(null);

  // Sync with external value
  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  // Trigger search on debounced value change
  useEffect(() => {
    onSearch?.(debouncedValue);
  }, [debouncedValue, onSearch]);

  const handleChange = useCallback((e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    onChange?.(newValue);
  }, [onChange]);

  const handleClear = useCallback(() => {
    setLocalValue('');
    onChange?.('');
    onSearch?.('');
    inputRef.current?.focus();
  }, [onChange, onSearch]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Escape') {
      handleClear();
    }
  }, [handleClear]);

  const sizeClasses = {
    sm: 'h-8 text-sm',
    default: 'h-10',
    lg: 'h-12 text-lg'
  };

  return (
    <div className={cn('relative', className)}>
      <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        ref={inputRef}
        type="text"
        value={localValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        autoFocus={autoFocus}
        className={cn(
          'pr-10',
          clearable && localValue && 'pl-10',
          sizeClasses[size]
        )}
      />
      {loading && (
        <Loader2 className="absolute left-10 top-1/2 -translate-y-1/2 h-4 w-4 animate-spin text-muted-foreground" />
      )}
      {clearable && localValue && !loading && (
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute left-1 top-1/2 -translate-y-1/2 h-6 w-6"
          onClick={handleClear}
        >
          <X className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
}

/**
 * SearchWithSuggestions - بحث مع اقتراحات
 */
export function SearchWithSuggestions({
  value = '',
  onChange,
  onSearch,
  onSelect,
  suggestions = [],
  placeholder = 'بحث...',
  debounceMs = 300,
  className = '',
  disabled = false,
  loading = false,
  renderSuggestion,
  noResultsText = 'لا توجد نتائج',
  minChars = 2
}) {
  const [localValue, setLocalValue] = useState(value);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const debouncedValue = useDebounce(localValue, debounceMs);
  const containerRef = useClickOutside(() => setShowSuggestions(false));

  // Trigger search on debounced value change
  useEffect(() => {
    if (debouncedValue.length >= minChars) {
      onSearch?.(debouncedValue);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  }, [debouncedValue, minChars, onSearch]);

  const handleChange = useCallback((e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    onChange?.(newValue);
    setHighlightedIndex(-1);
  }, [onChange]);

  const handleSelect = useCallback((item) => {
    onSelect?.(item);
    setLocalValue('');
    setShowSuggestions(false);
  }, [onSelect]);

  const handleKeyDown = useCallback((e) => {
    if (!showSuggestions || suggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex((prev) => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex((prev) => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (highlightedIndex >= 0) {
          handleSelect(suggestions[highlightedIndex]);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        break;
    }
  }, [showSuggestions, suggestions, highlightedIndex, handleSelect]);

  const defaultRenderSuggestion = (item, isHighlighted) => (
    <div
      className={cn(
        'px-3 py-2 cursor-pointer',
        isHighlighted && 'bg-accent'
      )}
    >
      {typeof item === 'string' ? item : item.label || item.name || JSON.stringify(item)}
    </div>
  );

  return (
    <div ref={containerRef} className={cn('relative', className)}>
      <SearchInput
        value={localValue}
        onChange={handleChange}
        placeholder={placeholder}
        disabled={disabled}
        loading={loading}
        onKeyDown={handleKeyDown}
      />
      
      {showSuggestions && (
        <div className="absolute z-50 top-full mt-1 w-full bg-popover border rounded-md shadow-lg max-h-60 overflow-auto">
          {suggestions.length === 0 && !loading ? (
            <div className="px-3 py-2 text-muted-foreground text-sm">
              {noResultsText}
            </div>
          ) : (
            suggestions.map((item, index) => (
              <div
                key={index}
                onClick={() => handleSelect(item)}
                onMouseEnter={() => setHighlightedIndex(index)}
              >
                {(renderSuggestion || defaultRenderSuggestion)(
                  item,
                  index === highlightedIndex
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

/**
 * GlobalSearch - بحث شامل
 */
export function GlobalSearch({
  onSearch,
  categories = [],
  className = ''
}) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const handleSearch = useCallback((value) => {
    onSearch?.({
      query: value,
      category: selectedCategory
    });
  }, [selectedCategory, onSearch]);

  return (
    <div className={cn('flex gap-2', className)}>
      {categories.length > 0 && (
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border rounded-md px-3 py-2 bg-background"
        >
          <option value="all">الكل</option>
          {categories.map((cat) => (
            <option key={cat.value} value={cat.value}>
              {cat.label}
            </option>
          ))}
        </select>
      )}
      <SearchInput
        value={query}
        onChange={setQuery}
        onSearch={handleSearch}
        placeholder="بحث في النظام..."
        className="flex-1"
      />
    </div>
  );
}

export default SearchInput;
