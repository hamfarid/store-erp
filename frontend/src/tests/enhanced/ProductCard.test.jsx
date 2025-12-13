// Enhanced Product Card Component Tests
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import ProductCard from '../../components/enhanced/ProductCard';

// Mock data
const mockProduct = {
  id: 1,
  name: 'Test Product',
  name_ar: 'منتج تجريبي',
  description: 'Test product description',
  description_ar: 'وصف المنتج التجريبي',
  price: 99.99,
  original_price: 149.99,
  stock_quantity: 10,
  stock_status: 'in_stock',
  images: [
    { url: 'https://example.com/image1.jpg' }
  ],
  category: {
    id: 1,
    name: 'Electronics',
    name_ar: 'إلكترونيات'
  },
  brand: {
    id: 1,
    name: 'Samsung',
    name_ar: 'سامسونج'
  }
};

const mockOutOfStockProduct = {
  ...mockProduct,
  id: 2,
  stock_status: 'out_of_stock',
  stock_quantity: 0
};

// Wrapper component for router
const RouterWrapper = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('ProductCard Component', () => {
  const mockOnAddToCart = jest.fn();
  const mockOnToggleFavorite = jest.fn();
  const mockOnEdit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    test('renders product information correctly', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText('منتج تجريبي')).toBeInTheDocument();
      expect(screen.getByText('وصف المنتج التجريبي')).toBeInTheDocument();
      expect(screen.getByText('إلكترونيات')).toBeInTheDocument();
      expect(screen.getByText('سامسونج')).toBeInTheDocument();
    });

    test('displays price information correctly', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText(/99.99/)).toBeInTheDocument();
      expect(screen.getByText(/149.99/)).toBeInTheDocument();
    });

    test('shows discount badge when product has discount', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText('-33%')).toBeInTheDocument();
    });

    test('displays stock status correctly', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText('متوفر')).toBeInTheDocument();
    });

    test('shows out of stock status for unavailable products', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockOutOfStockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText('غير متوفر')).toBeInTheDocument();
    });
  });

  describe('Loading State', () => {
    test('renders loading skeleton when isLoading is true', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={{}}
            isLoading={true}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(document.querySelector('.loading')).toBeInTheDocument();
      expect(document.querySelector('.skeleton-text')).toBeInTheDocument();
    });
  });

  describe('Actions', () => {
    test('calls onAddToCart when add to cart button is clicked', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const addToCartButton = screen.getByRole('button', { name: /إضافة للسلة/ });
      fireEvent.click(addToCartButton);

      expect(mockOnAddToCart).toHaveBeenCalledWith(mockProduct);
    });

    test('does not call onAddToCart for out of stock products', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockOutOfStockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const addToCartButton = screen.getByRole('button', { name: /غير متوفر/ });
      fireEvent.click(addToCartButton);

      expect(mockOnAddToCart).not.toHaveBeenCalled();
    });

    test('calls onToggleFavorite when favorite button is clicked', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const favoriteButton = screen.getByRole('button', { name: /إضافة للمفضلة/ });
      fireEvent.click(favoriteButton);

      expect(mockOnToggleFavorite).toHaveBeenCalledWith(mockProduct);
    });

    test('shows edit button when showEditAction is true', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
            onEdit={mockOnEdit}
            showEditAction={true}
          />
        </RouterWrapper>
      );

      const editButton = screen.getByRole('button', { name: /تعديل/ });
      expect(editButton).toBeInTheDocument();

      fireEvent.click(editButton);
      expect(mockOnEdit).toHaveBeenCalledWith(mockProduct);
    });

    test('does not show actions when showActions is false', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
            showActions={false}
          />
        </RouterWrapper>
      );

      expect(screen.queryByRole('button', { name: /إضافة للسلة/ })).not.toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /إضافة للمفضلة/ })).not.toBeInTheDocument();
    });
  });

  describe('Favorite State', () => {
    test('shows filled heart when product is favorite', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
            isFavorite={true}
          />
        </RouterWrapper>
      );

      const favoriteButton = screen.getByRole('button', { name: /إزالة من المفضلة/ });
      expect(favoriteButton).toBeInTheDocument();
      expect(favoriteButton.textContent).toBe('♥');
    });

    test('shows empty heart when product is not favorite', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
            isFavorite={false}
          />
        </RouterWrapper>
      );

      const favoriteButton = screen.getByRole('button', { name: /إضافة للمفضلة/ });
      expect(favoriteButton).toBeInTheDocument();
    });
  });

  describe('Image Handling', () => {
    test('handles image load error gracefully', async () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={{
              ...mockProduct,
              images: [{ url: 'invalid-url' }]
            }}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const image = screen.getByRole('img');
      fireEvent.error(image);

      await waitFor(() => {
        expect(image.src).toContain('placeholder-product.jpg');
      });
    });

    test('uses placeholder image when no image is provided', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={{
              ...mockProduct,
              images: []
            }}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const image = screen.getByRole('img');
      expect(image.src).toContain('placeholder-product.jpg');
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels for buttons', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByRole('button', { name: /إضافة للسلة/ })).toHaveAttribute('aria-label');
      expect(screen.getByRole('button', { name: /إضافة للمفضلة/ })).toHaveAttribute('aria-label');
    });

    test('has proper alt text for product image', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const image = screen.getByRole('img');
      expect(image).toHaveAttribute('alt', 'منتج تجريبي');
    });

    test('supports keyboard navigation', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      const favoriteButton = screen.getByRole('button', { name: /إضافة للمفضلة/ });
      favoriteButton.focus();
      expect(favoriteButton).toHaveFocus();

      fireEvent.keyDown(favoriteButton, { key: 'Enter' });
      expect(mockOnToggleFavorite).toHaveBeenCalledWith(mockProduct);
    });
  });

  describe('Event Propagation', () => {
    test('prevents event propagation when clicking action buttons', () => {
      const mockLinkClick = jest.fn();
      
      render(
        <RouterWrapper>
          <div onClick={mockLinkClick}>
            <ProductCard
              product={mockProduct}
              onAddToCart={mockOnAddToCart}
              onToggleFavorite={mockOnToggleFavorite}
            />
          </div>
        </RouterWrapper>
      );

      const favoriteButton = screen.getByRole('button', { name: /إضافة للمفضلة/ });
      fireEvent.click(favoriteButton);

      expect(mockOnToggleFavorite).toHaveBeenCalled();
      expect(mockLinkClick).not.toHaveBeenCalled();
    });
  });

  describe('Price Formatting', () => {
    test('formats prices in Arabic locale', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      // Check if price is formatted with SAR currency
      expect(screen.getByText(/ر\.س/)).toBeInTheDocument();
    });
  });

  describe('Stock Information', () => {
    test('displays stock quantity when available', () => {
      render(
        <RouterWrapper>
          <ProductCard
            product={mockProduct}
            onAddToCart={mockOnAddToCart}
            onToggleFavorite={mockOnToggleFavorite}
          />
        </RouterWrapper>
      );

      expect(screen.getByText(/الكمية المتوفرة: 10/)).toBeInTheDocument();
    });
  });
});
