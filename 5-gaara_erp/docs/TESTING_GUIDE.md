# 🧪 Gaara Store - Testing Guide

**Version**: 1.0  
**Date**: 2025-10-27  
**Status**: ✅ **ACTIVE**

---

## 🎯 TESTING OVERVIEW

The application uses Vitest for unit testing and Playwright for E2E testing.

---

## 🧪 UNIT TESTS

### Test Setup
```jsx
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../Button'

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalled()
  })
})
```

### Component Tests
- Button component
- Modal component
- Form component
- Table component
- Input component
- Select component
- Card component
- Badge component

### Hook Tests
- useAuth hook
- useApp hook
- useApi hook
- useForm hook

### Context Tests
- AuthContext
- AppContext

---

## 🔗 INTEGRATION TESTS

### API Integration
```jsx
describe('API Integration', () => {
  it('fetches products from API', async () => {
    const response = await apiClient.getProducts()
    expect(response.data).toBeDefined()
    expect(response.data.items).toBeInstanceOf(Array)
  })

  it('creates product via API', async () => {
    const productData = {
      name: 'Test Product',
      sku: 'TEST-001',
      price: 100
    }
    const response = await apiClient.createProduct(productData)
    expect(response.data.id).toBeDefined()
  })
})
```

### Form Integration
```jsx
describe('ProductForm Integration', () => {
  it('submits form with valid data', async () => {
    render(<ProductForm onSuccess={vi.fn()} />)
    
    fireEvent.change(screen.getByLabelText('Name'), {
      target: { value: 'Test Product' }
    })
    fireEvent.change(screen.getByLabelText('SKU'), {
      target: { value: 'TEST-001' }
    })
    fireEvent.click(screen.getByText('Submit'))
    
    await waitFor(() => {
      expect(screen.getByText('Success')).toBeInTheDocument()
    })
  })
})
```

### State Management
```jsx
describe('AppContext Integration', () => {
  it('adds notification', () => {
    const { result } = renderHook(() => useApp(), {
      wrapper: AppProvider
    })
    
    act(() => {
      result.current.addNotification({
        type: 'success',
        message: 'Test'
      })
    })
    
    expect(result.current.notifications).toHaveLength(1)
  })
})
```

---

## 🌐 E2E TESTS

### Playwright Setup
```javascript
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:5173/login')
  
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  await expect(page).toHaveURL('http://localhost:5173/')
})
```

### User Flows
- Login flow
- Product creation flow
- Customer creation flow
- Invoice creation flow
- Report generation flow

### Navigation Tests
- Sidebar navigation
- Breadcrumbs
- Menu items
- Route transitions

---

## ♿ ACCESSIBILITY TESTS

### WCAG AA Compliance
```jsx
describe('Accessibility', () => {
  it('has proper heading hierarchy', () => {
    render(<Dashboard />)
    const headings = screen.getAllByRole('heading')
    expect(headings[0]).toHaveAttribute('aria-level', '1')
  })

  it('has proper color contrast', () => {
    // Use axe-core for contrast checking
    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('has proper ARIA labels', () => {
    render(<Button aria-label="Close">×</Button>)
    expect(screen.getByLabelText('Close')).toBeInTheDocument()
  })
})
```

### Keyboard Navigation
- Tab order
- Focus management
- Keyboard shortcuts
- Screen reader support

---

## 📊 PERFORMANCE TESTS

### Lighthouse Metrics
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

### Load Time Tests
```javascript
test('page loads in < 3 seconds', async ({ page }) => {
  const startTime = Date.now()
  await page.goto('http://localhost:5173/')
  const loadTime = Date.now() - startTime
  expect(loadTime).toBeLessThan(3000)
})
```

### Bundle Size
- Main bundle: < 500KB
- Vendor bundle: < 300KB
- Total: < 800KB

---

## 🔍 TEST COVERAGE

### Target Coverage
- Statements: > 80%
- Branches: > 75%
- Functions: > 80%
- Lines: > 80%

### Coverage Report
```bash
npm run test:coverage
```

---

## 🚀 RUNNING TESTS

### Unit Tests
```bash
npm run test
npm run test:watch
npm run test:coverage
```

### E2E Tests
```bash
npm run test:e2e
npm run test:e2e:ui
```

### All Tests
```bash
npm run test:all
```

---

## 📝 TEST EXAMPLES

### Button Component Test
```jsx
describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('applies correct variant class', () => {
    render(<Button variant="primary">Click</Button>)
    expect(screen.getByText('Click')).toHaveClass('bg-primary-600')
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByText('Click')).toBeDisabled()
  })
})
```

### Form Component Test
```jsx
describe('ProductForm', () => {
  it('validates required fields', async () => {
    render(<ProductForm />)
    fireEvent.click(screen.getByText('Submit'))
    
    await waitFor(() => {
      expect(screen.getByText('Name is required')).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const onSuccess = vi.fn()
    render(<ProductForm onSuccess={onSuccess} />)
    
    fireEvent.change(screen.getByLabelText('Name'), {
      target: { value: 'Test' }
    })
    fireEvent.click(screen.getByText('Submit'))
    
    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalled()
    })
  })
})
```

---

## ✅ BEST PRACTICES

### Do's ✅
- Write tests for critical paths
- Test user interactions
- Test error states
- Test loading states
- Use meaningful test names
- Keep tests focused
- Mock external APIs
- Test accessibility

### Don'ts ❌
- Don't test implementation details
- Don't skip error cases
- Don't ignore accessibility
- Don't write flaky tests
- Don't test third-party libraries
- Don't skip edge cases
- Don't forget cleanup
- Don't ignore performance

---

## 📚 RESOURCES

- **Vitest**: https://vitest.dev/
- **Testing Library**: https://testing-library.com/
- **Playwright**: https://playwright.dev/
- **Test Files**: `frontend/src/**/*.test.jsx`

---

**Status**: ✅ **ACTIVE**  
**Last Updated**: 2025-10-27  
**Maintained By**: Augment Agent

🧪 **Follow this guide for comprehensive testing!** 🧪

