// Enhanced Product Card Component
import React, { useState, useCallback, memo } from 'react';
import { Link } from 'react-router-dom';
import './ProductCard.css';

const ProductCard = memo(({ 
  product, 
  onAddToCart, 
  onToggleFavorite, 
  onEdit,
  isFavorite = false,
  isLoading = false,
  showActions = true,
  showEditAction = false,
  className = '',
  ...props 
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageLoad = useCallback(() => {
    setImageLoaded(true);
  }, []);

  const handleImageError = useCallback(() => {
    setImageError(true);
    setImageLoaded(true);
  }, []);

  const handleAddToCart = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onAddToCart && product.stock_status !== 'out_of_stock') {
      onAddToCart(product);
    }
  }, [onAddToCart, product]);

  const handleToggleFavorite = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onToggleFavorite) {
      onToggleFavorite(product);
    }
  }, [onToggleFavorite, product]);

  const handleEdit = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onEdit) {
      onEdit(product);
    }
  }, [onEdit, product]);

  const hasDiscount = product.original_price && product.original_price > product.price;
  const discountPercentage = hasDiscount 
    ? Math.round(((product.original_price - product.price) / product.original_price) * 100)
    : 0;

  const getStockStatusText = (status) => {
    switch (status) {
      case 'in_stock': return 'متوفر';
      case 'low_stock': return 'مخزون منخفض';
      case 'out_of_stock': return 'غير متوفر';
      default: return 'غير محدد';
    }
  };

  if (isLoading) {
    return (
      <div className={`product-card loading ${className}`} {...props}>
        <div className="product-image skeleton"></div>
        <div className="product-content">
          <div className="skeleton-text"></div>
          <div className="skeleton-text short"></div>
          <div className="skeleton-text shorter"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`product-card ${product.stock_status} ${className}`} {...props}>
      <Link to={`/products/${product.id}`} className="product-link">
        {/* Product Image */}
        <div className="product-image-container">
          {!imageLoaded && !imageError && <div className="image-skeleton"></div>}
          
          <img
            src={imageError ? '/images/placeholder-product.jpg' : product.images?.[0]?.url || '/images/placeholder-product.jpg'}
            alt={product.name_ar || product.name}
            className="product-image"
            onLoad={handleImageLoad}
            onError={handleImageError}
            style={{ display: imageLoaded ? 'block' : 'none' }}
          />

          {/* Discount Badge */}
          {hasDiscount && (
            <div className="discount-badge">
              -{discountPercentage}%
            </div>
          )}

          {/* Stock Status */}
          <div className={`stock-status ${product.stock_status}`}>
            {getStockStatusText(product.stock_status)}
          </div>

          {/* Action Buttons */}
          {showActions && (
            <div className="product-actions">
              <button
                className={`action-btn favorite ${isFavorite ? 'active' : ''}`}
                onClick={handleToggleFavorite}
                title={isFavorite ? 'إزالة من المفضلة' : 'إضافة للمفضلة'}
                aria-label={isFavorite ? 'إزالة من المفضلة' : 'إضافة للمفضلة'}
              >
                ♥
              </button>

              <button
                className="action-btn view"
                title="عرض سريع"
                aria-label="عرض سريع"
              >
                👁
              </button>

              {showEditAction && (
                <button
                  className="action-btn edit"
                  onClick={handleEdit}
                  title="تعديل"
                  aria-label="تعديل"
                >
                  ✏
                </button>
              )}
            </div>
          )}
        </div>

        {/* Product Content */}
        <div className="product-content">
          <h3 className="product-name" title={product.name_ar || product.name}>
            {product.name_ar || product.name}
          </h3>

          {product.description && (
            <p className="product-description">
              {product.description_ar || product.description}
            </p>
          )}

          <div className="product-tags">
            {product.category && (
              <span className="tag category">
                {product.category.name_ar || product.category.name}
              </span>
            )}
            {product.brand && (
              <span className="tag brand">
                {product.brand.name_ar || product.brand.name}
              </span>
            )}
          </div>

          <div className="price-container">
            <span className="current-price">
              {new Intl.NumberFormat('ar-SA', {
                style: 'currency',
                currency: 'SAR'
              }).format(product.price)}
            </span>
            
            {hasDiscount && (
              <span className="original-price">
                {new Intl.NumberFormat('ar-SA', {
                  style: 'currency',
                  currency: 'SAR'
                }).format(product.original_price)}
              </span>
            )}
          </div>

          {product.stock_quantity !== undefined && (
            <div className="stock-info">
              الكمية المتوفرة: {product.stock_quantity}
            </div>
          )}

          {showActions && onAddToCart && (
            <button
              className={`add-to-cart-btn ${product.stock_status === 'out_of_stock' ? 'disabled' : ''}`}
              onClick={handleAddToCart}
              disabled={product.stock_status === 'out_of_stock'}
              aria-label="إضافة للسلة"
            >
              🛒 {product.stock_status === 'out_of_stock' ? 'غير متوفر' : 'إضافة للسلة'}
            </button>
          )}
        </div>
      </Link>
    </div>
  );
});

ProductCard.displayName = 'ProductCard';

export default ProductCard;
