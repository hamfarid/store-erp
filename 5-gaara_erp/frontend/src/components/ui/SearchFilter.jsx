import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu
} from 'lucide-react'

const SearchFilter = ({
  onSearch, 
  onFilter, 
  filters = [],
  placeholder = "البحث...",
  className = ""
}) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [activeFilters, setActiveFilters] = useState({})
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      onSearch(searchTerm)
    }, 300)

    return () => clearTimeout(debounceTimer)
  }, [searchTerm, onSearch])

  useEffect(() => {
    if (onFilter && typeof onFilter === 'function') {
      onFilter(activeFilters)
    }
  }, [activeFilters]) // إزالة onFilter من dependencies

  const handleFilterChange = (filterKey, value) => {
    setActiveFilters(prev => ({
      ...prev,
      [filterKey]: value
    }))
  }

  const clearFilter = (filterKey) => {
    setActiveFilters(prev => {
      const newFilters = { ...prev }
      delete newFilters[filterKey]
      return newFilters
    })
  }

  const clearAllFilters = () => {
    setActiveFilters({})
    setSearchTerm('')
  }

  const renderFilterInput = (filter) => {
    const value = activeFilters[filter.key] || ''

    switch (filter.type) {
      case 'text':
        return (
          <input
            type="text"
            placeholder={filter.placeholder}
            value={value}
            onChange={(e) => handleFilterChange(filter.key, e.target.value)}
            className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        )

      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handleFilterChange(filter.key, e.target.value)}
            className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">جميع {filter.label}</option>
            {filter.options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )

      case 'date':
        return (
          <div className="relative">
            <input
              type="date"
              value={value}
              onChange={(e) => handleFilterChange(filter.key, e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          </div>
        )

      case 'number':
        return (
          <input
            type="number"
            placeholder={filter.placeholder}
            value={value}
            onChange={(e) => handleFilterChange(filter.key, e.target.value)}
            min={filter.min}
            max={filter.max}
            step={filter.step}
            className="w-full px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        )

      case 'range':
        return (
          <div className="grid grid-cols-2 gap-2">
            <input
              type="number"
              placeholder="من"
              value={value.min || ''}
              onChange={(e) => handleFilterChange(filter.key, { ...value, min: e.target.value })}
              className="px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <input
              type="number"
              placeholder="إلى"
              value={value.max || ''}
              onChange={(e) => handleFilterChange(filter.key, { ...value, max: e.target.value })}
              className="px-3 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        )

      default:
        return null
    }
  }

  const activeFilterCount = Object.keys(activeFilters).filter(key => 
    activeFilters[key] && 
    (typeof activeFilters[key] === 'string' ? activeFilters[key].trim() !== '' : true)
  ).length

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-border p-4 ${className}`} dir="rtl">
      {/* Search and Filter Toggle */}
      <div className="flex items-center space-x-4 space-x-reverse mb-4">
        {/* Search Input */}
        <div className="flex-1 relative">
          <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder={placeholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-4 pr-10 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-muted-foreground"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Filter Toggle */}
        {filters.length > 0 && (
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center px-4 py-2 border rounded-lg transition-colors ${
              showFilters || activeFilterCount > 0
                ? 'bg-primary-50 border-primary-300 text-primary-700'
                : 'border-border text-foreground hover:bg-muted/50'
            }`}
          >
            <Filter className="w-4 h-4 ml-1" />
            تصفية
            {activeFilterCount > 0 && (
              <span className="mr-1 px-2 py-0.5 bg-primary-600 text-white text-xs rounded-full">
                {activeFilterCount}
              </span>
            )}
            <ChevronDown className={`w-4 h-4 mr-1 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </button>
        )}

        {/* Clear All */}
        {(searchTerm || activeFilterCount > 0) && (
          <button
            onClick={clearAllFilters}
            className="px-4 py-2 text-destructive hover:text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
          >
            مسح الكل
          </button>
        )}
      </div>

      {/* Active Filters Display */}
      {activeFilterCount > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {Object.keys(activeFilters).map(key => {
            const filter = filters.find(f => f.key === key)
            const value = activeFilters[key]
            
            if (!value || (typeof value === 'string' && value.trim() === '')) return null

            let displayValue = value
            if (filter?.type === 'select') {
              const option = filter.options?.find(opt => opt.value === value)
              displayValue = option?.label || value
            } else if (filter?.type === 'range' && typeof value === 'object') {
              displayValue = `${value.min || '0'} - ${value.max || '∞'}`
            }

            return (
              <div
                key={key}
                className="flex items-center bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm"
              >
                <span className="font-medium ml-1">{filter?.label}:</span>
                <span>{displayValue}</span>
                <button
                  onClick={() => clearFilter(key)}
                  className="mr-2 text-primary-600 hover:text-primary-800"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            )
          })}
        </div>
      )}

      {/* Filter Inputs */}
      {showFilters && filters.length > 0 && (
        <div className="border-t border-border pt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filters.map((filter) => (
              <div key={filter.key} className="space-y-2">
                <label className="block text-sm font-medium text-foreground">
                  {filter.label}
                </label>
                {renderFilterInput(filter)}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// مكونات تصفية سريعة جاهزة
const QuickFilters = ({ onFilterChange, activeFilter = 'all' }) => {
  const quickFilters = [
    { key: 'all', label: 'الكل', icon: Package },
    { key: 'low_stock', label: 'مخزون منخفض', icon: Package },
    { key: 'out_of_stock', label: 'نفد المخزون', icon: X },
    { key: 'recent', label: 'حديث', icon: Calendar },
    { key: 'popular', label: 'الأكثر مبيعاً', icon: Users }
  ]

  return (
    <div className="flex flex-wrap gap-2 mb-4" dir="rtl">
      {quickFilters.map((filter) => {
        const Icon = filter.icon
        return (
          <button
            key={filter.key}
            onClick={() => onFilterChange(filter.key)}
            className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeFilter === filter.key
                ? 'bg-primary-600 text-white'
                : 'bg-muted text-foreground hover:bg-muted'
            }`}
          >
            <Icon className="w-4 h-4 ml-1" />
            {filter.label}
          </button>
        )
      })}
    </div>
  )
}

export { SearchFilter, QuickFilters }
export default SearchFilter

