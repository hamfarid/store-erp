// Enhanced Product List Component
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';

const ProductList = ({
  products = [],
  isLoading = false,
  error = null,
  onLoadMore = null,
  hasMore = false,
  onAddToCart,
  onToggleFavorite,
  onEdit,
  favorites = [],
  showEditActions = false,
  searchTerm = '',
  filters = {},
  sortBy = 'name',
  sortOrder = 'asc',
  viewMode = 'grid', // 'grid' or 'list'
  itemsPerPage = 20
}) => {
  const [localLoading, setLocalLoading] = useState(false);
  const [displayedProducts, setDisplayedProducts] = useState([]);

  // Filter and sort products
  const filteredAndSortedProducts = useMemo(() => {
    let filtered = [...products];

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(product => 
        (product.name && product.name.toLowerCase().includes(term)) ||
        (product.name_ar && product.name_ar.toLowerCase().includes(term)) ||
        (product.description && product.description.toLowerCase().includes(term)) ||
        (product.description_ar && product.description_ar.toLowerCase().includes(term)) ||
        (product.sku && product.sku.toLowerCase().includes(term))
      );
    }

    // Apply filters
    if (filters.category) {
      filtered = filtered.filter(product => 
        product.category_id === filters.category
      );
    }

    if (filters.brand) {
      filtered = filtered.filter(product => 
        product.brand_id === filters.brand
      );
    }

    if (filters.priceRange) {
      const [min, max] = filters.priceRange;
      filtered = filtered.filter(product => 
        product.price >= min && product.price <= max
      );
    }

    if (filters.inStock !== undefined) {
      filtered = filtered.filter(product => 
        filters.inStock ? product.stock_quantity > 0 : product.stock_quantity <= 0
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue, bValue;

      switch (sortBy) {
        case 'name':
          aValue = a.name_ar || a.name || '';
          bValue = b.name_ar || b.name || '';
          break;
        case 'price':
          aValue = a.price || 0;
          bValue = b.price || 0;
          break;
        case 'created_at':
          aValue = new Date(a.created_at || 0);
          bValue = new Date(b.created_at || 0);
          break;
        case 'stock_quantity':
          aValue = a.stock_quantity || 0;
          bValue = b.stock_quantity || 0;
          break;
        default:
          aValue = a[sortBy] || '';
          bValue = b[sortBy] || '';
      }

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (sortOrder === 'desc') {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
      } else {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
      }
    });

    return filtered;
  }, [products, searchTerm, filters, sortBy, sortOrder]);

  // Update displayed products when filtered products change
  useEffect(() => {
    setDisplayedProducts(filteredAndSortedProducts.slice(0, itemsPerPage));
  }, [filteredAndSortedProducts, itemsPerPage]);

  // Load more products
  const handleLoadMore = useCallback(async () => {
    if (localLoading || !hasMore) return;

    setLocalLoading(true);
    try {
      if (onLoadMore) {
        await onLoadMore();
      } else {
        // Local pagination
        const currentLength = displayedProducts.length;
        const nextBatch = filteredAndSortedProducts.slice(
          currentLength, 
          currentLength + itemsPerPage
        );
        setDisplayedProducts(prev => [...prev, ...nextBatch]);
      }
    } catch (error) {
      console.error('Error loading more products:', error);
    } finally {
      setLocalLoading(false);
    }
  }, [localLoading, hasMore, onLoadMore, displayedProducts.length, filteredAndSortedProducts, itemsPerPage]);

  // Check if product is favorite
  const isProductFavorite = useCallback((productId) => {
    return favorites.includes(productId);
  }, [favorites]);

  // Render loading skeleton
  const renderLoadingSkeleton = () => {
    return Array.from({ length: 8 }, (_, index) => (
      <ProductCard
        key={`skeleton-${index}`}
        product={{}}
        isLoading={true}
      />
    ));
  };

  // Render empty state
  const renderEmptyState = () => (
    <div className="empty-state">
      <div className="empty-state-icon">📦</div>
      <h3 className="empty-state-title">لا توجد منتجات</h3>
      <p className="empty-state-description">
        {searchTerm || Object.keys(filters).length > 0
          ? 'لم يتم العثور على منتجات تطابق البحث أو الفلاتر المحددة'
          : 'لا توجد منتجات متاحة حالياً'
        }
      </p>
      {(searchTerm || Object.keys(filters).length > 0) && (
        <button 
          className="clear-filters-btn"
          onClick={() => window.location.reload()}
        >
          مسح الفلاتر
        </button>
      )}
    </div>
  );

  // Render error state
  const renderErrorState = () => (
    <div className="error-state">
      <div className="error-state-icon">⚠️</div>
      <h3 className="error-state-title">حدث خطأ</h3>
      <p className="error-state-description">
        {error || 'فشل في تحميل المنتجات. يرجى المحاولة مرة أخرى.'}
      </p>
      <button 
        className="retry-btn"
        onClick={() => window.location.reload()}
      >
        إعادة المحاولة
      </button>
    </div>
  );

  // Render products grid
  const renderProductsGrid = () => (
    <div className={`products-grid ${viewMode}`}>
      {displayedProducts.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={onAddToCart}
          onToggleFavorite={onToggleFavorite}
          onEdit={onEdit}
          isFavorite={isProductFavorite(product.id)}
          showEditAction={showEditActions}
        />
      ))}
    </div>
  );

  // Render load more button
  const renderLoadMoreButton = () => {
    const hasMoreLocal = displayedProducts.length < filteredAndSortedProducts.length;
    const showLoadMore = hasMore || hasMoreLocal;

    if (!showLoadMore) return null;

    return (
      <div className="load-more-container">
        <button
          className={`load-more-btn ${localLoading ? 'loading' : ''}`}
          onClick={handleLoadMore}
          disabled={localLoading}
        >
          {localLoading ? (
            <>
              <span className="spinner"></span>
              جاري التحميل...
            </>
          ) : (
            'تحميل المزيد'
          )}
        </button>
      </div>
    );
  };

  // Render results summary
  const renderResultsSummary = () => {
    const totalResults = filteredAndSortedProducts.length;
    const displayedCount = displayedProducts.length;

    if (totalResults === 0) return null;

    return (
      <div className="results-summary">
        <span className="results-count">
          عرض {displayedCount} من أصل {totalResults} منتج
        </span>
        {(searchTerm || Object.keys(filters).length > 0) && (
          <span className="filters-applied">
            • تم تطبيق فلاتر البحث
          </span>
        )}
      </div>
    );
  };

  return (
    <div className="product-list-container">
      {/* Results Summary */}
      {!isLoading && !error && renderResultsSummary()}

      {/* Main Content */}
      <div className="product-list-content">
        {/* Loading State */}
        {isLoading && renderLoadingSkeleton()}

        {/* Error State */}
        {error && !isLoading && renderErrorState()}

        {/* Empty State */}
        {!isLoading && !error && filteredAndSortedProducts.length === 0 && renderEmptyState()}

        {/* Products Grid */}
        {!isLoading && !error && filteredAndSortedProducts.length > 0 && renderProductsGrid()}
      </div>

      {/* Load More Button */}
      {!isLoading && !error && filteredAndSortedProducts.length > 0 && renderLoadMoreButton()}

      {/* Loading More Indicator */}
      {localLoading && (
        <div className="loading-more">
          <div className="loading-more-spinner"></div>
          <span>جاري تحميل المزيد من المنتجات...</span>
        </div>
      )}
    </div>
  );
};

export default ProductList;
