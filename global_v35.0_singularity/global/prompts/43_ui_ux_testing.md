================================================================================
MODULE 43: UI/UX TESTING & FIXES
================================================================================
Version: 1.0.0
Last Updated: 2025-11-07
Purpose: Frontend testing, visual regression, icons, colors, styles
================================================================================

## OVERVIEW

UI/UX testing ensures the frontend renders correctly, looks good, and provides
a great user experience. This module covers common UI issues and how to fix them.

================================================================================
## COMMON UI/UX ISSUES
================================================================================

### 1. Icons Not Displaying ❌

**Symptoms:**
- Empty squares where icons should be
- Missing icon fonts
- Broken icon images

**Causes:**
```
✗ Icon library not imported
✗ CDN link broken or blocked
✗ Wrong icon class names
✗ CSS not loaded
✗ Font files not found
```

**Fixes:**

#### A. Font Awesome
```html
<!-- In <head> -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Usage -->
<i class="fas fa-user"></i>
<i class="far fa-heart"></i>
<i class="fab fa-github"></i>
```

#### B. Material Icons
```html
<!-- In <head> -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- Usage -->
<span class="material-icons">home</span>
<span class="material-icons-outlined">favorite</span>
```

#### C. Bootstrap Icons
```html
<!-- In <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<!-- Usage -->
<i class="bi bi-house"></i>
<i class="bi bi-heart-fill"></i>
```

#### D. SVG Icons (Recommended)
```html
<!-- Inline SVG -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
</svg>

<!-- External SVG -->
<img src="/icons/user.svg" alt="User" width="24" height="24">
```

#### E. Icon Components (React/Vue)
```jsx
// React with react-icons
import { FaUser, FaHeart } from 'react-icons/fa';

function Component() {
  return (
    <div>
      <FaUser size={24} color="#333" />
      <FaHeart size={24} color="red" />
    </div>
  );
}
```

**Testing:**
```typescript
// Playwright test
test('icons display correctly', async ({ page }) => {
  await page.goto('/');
  
  // Check icon is visible
  const icon = page.locator('[data-testid="user-icon"]');
  await expect(icon).toBeVisible();
  
  // Check icon has correct class
  await expect(icon).toHaveClass(/fa-user/);
  
  // Check icon is not empty
  const content = await icon.textContent();
  expect(content).toBeTruthy();
});
```

---

### 2. Colors Not Applying ❌

**Symptoms:**
- Wrong colors displayed
- Colors not changing
- Inconsistent colors

**Causes:**
```
✗ CSS variables not defined
✗ Wrong color values
✗ Specificity issues
✗ !important overrides
✗ Theme not loaded
```

**Fixes:**

#### A. CSS Variables (Recommended)
```css
/* Define colors */
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;
  
  --text-color: #212529;
  --bg-color: #ffffff;
  --border-color: #dee2e6;
}

/* Dark theme */
[data-theme="dark"] {
  --text-color: #ffffff;
  --bg-color: #212529;
  --border-color: #495057;
}

/* Usage */
.button {
  background-color: var(--primary-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}
```

#### B. Tailwind CSS
```html
<!-- Configure colors in tailwind.config.js -->
<script>
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        success: '#28a745',
        danger: '#dc3545',
      }
    }
  }
}
</script>

<!-- Usage -->
<button class="bg-primary text-white hover:bg-primary-dark">
  Click me
</button>
```

#### C. SCSS/SASS
```scss
// _variables.scss
$primary-color: #007bff;
$secondary-color: #6c757d;
$success-color: #28a745;
$danger-color: #dc3545;

// Usage
.button {
  background-color: $primary-color;
  
  &:hover {
    background-color: darken($primary-color, 10%);
  }
}
```

**Testing:**
```typescript
// Playwright test
test('colors apply correctly', async ({ page }) => {
  await page.goto('/');
  
  const button = page.locator('[data-testid="primary-button"]');
  
  // Check background color
  const bgColor = await button.evaluate(el => 
    window.getComputedStyle(el).backgroundColor
  );
  expect(bgColor).toBe('rgb(0, 123, 255)'); // #007bff
  
  // Check text color
  const textColor = await button.evaluate(el => 
    window.getComputedStyle(el).color
  );
  expect(textColor).toBe('rgb(255, 255, 255)'); // white
});
```

---

### 3. CSS Not Loading ❌

**Symptoms:**
- Unstyled content
- Wrong layout
- Missing styles

**Causes:**
```
✗ Wrong file path
✗ File not served
✗ Build not run
✗ Cache issues
✗ CORS errors
```

**Fixes:**

#### A. Check File Paths
```html
<!-- Correct paths -->
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="{% static 'css/style.css' %}"> <!-- Django -->
<link rel="stylesheet" href="{{ asset('css/style.css') }}"> <!-- Laravel -->
```

#### B. Static File Serving (Django)
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# In development
DEBUG = True

# In production
python manage.py collectstatic
```

#### C. Static File Serving (Flask)
```python
# app.py
from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Usage
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### D. Build Process (React/Vue)
```bash
# Development
npm run dev

# Production
npm run build

# Check build output
ls -la dist/assets/
```

**Testing:**
```typescript
// Playwright test
test('CSS loads correctly', async ({ page }) => {
  await page.goto('/');
  
  // Check stylesheet is loaded
  const stylesheets = await page.evaluate(() => 
    Array.from(document.styleSheets).map(sheet => sheet.href)
  );
  expect(stylesheets.some(href => href?.includes('style.css'))).toBeTruthy();
  
  // Check styles are applied
  const element = page.locator('[data-testid="header"]');
  const fontSize = await element.evaluate(el => 
    window.getComputedStyle(el).fontSize
  );
  expect(fontSize).toBe('24px');
});
```

---

### 4. Images Not Showing ❌

**Symptoms:**
- Broken image icons
- Empty image placeholders
- 404 errors

**Causes:**
```
✗ Wrong image path
✗ Image not uploaded
✗ CORS issues
✗ Lazy loading issues
```

**Fixes:**

#### A. Correct Paths
```html
<!-- Static images -->
<img src="/static/images/logo.png" alt="Logo">
<img src="{% static 'images/logo.png' %}" alt="Logo"> <!-- Django -->

<!-- Dynamic images -->
<img src="{{ user.avatar_url }}" alt="{{ user.name }}">

<!-- With fallback -->
<img src="{{ user.avatar_url }}" 
     alt="{{ user.name }}"
     onerror="this.src='/static/images/default-avatar.png'">
```

#### B. Lazy Loading
```html
<!-- Native lazy loading -->
<img src="/images/large.jpg" loading="lazy" alt="Large image">

<!-- Intersection Observer -->
<script>
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      observer.unobserve(img);
    }
  });
});

images.forEach(img => imageObserver.observe(img));
</script>
```

**Testing:**
```typescript
// Playwright test
test('images load correctly', async ({ page }) => {
  await page.goto('/');
  
  const image = page.locator('[data-testid="logo"]');
  
  // Check image is visible
  await expect(image).toBeVisible();
  
  // Check image loaded successfully
  const naturalWidth = await image.evaluate(img => img.naturalWidth);
  expect(naturalWidth).toBeGreaterThan(0);
  
  // Check image has correct src
  await expect(image).toHaveAttribute('src', /logo\.png/);
});
```

---

### 5. Fonts Not Rendering ❌

**Symptoms:**
- Wrong fonts displayed
- Fallback fonts used
- FOUT (Flash of Unstyled Text)

**Causes:**
```
✗ Font files not loaded
✗ Wrong font-family name
✗ CORS issues
✗ Font format not supported
```

**Fixes:**

#### A. Google Fonts
```html
<!-- In <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Usage -->
<style>
body {
  font-family: 'Inter', sans-serif;
}
</style>
```

#### B. Self-Hosted Fonts
```css
/* fonts.css */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/CustomFont.woff2') format('woff2'),
       url('/fonts/CustomFont.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

body {
  font-family: 'CustomFont', sans-serif;
}
```

**Testing:**
```typescript
// Playwright test
test('fonts load correctly', async ({ page }) => {
  await page.goto('/');
  
  const element = page.locator('body');
  
  // Check font-family
  const fontFamily = await element.evaluate(el => 
    window.getComputedStyle(el).fontFamily
  );
  expect(fontFamily).toContain('Inter');
});
```

---

### 6. Responsive Issues ❌

**Symptoms:**
- Layout breaks on mobile
- Text overflows
- Elements overlap

**Causes:**
```
✗ No viewport meta tag
✗ Fixed widths
✗ No media queries
✗ Not testing on mobile
```

**Fixes:**

#### A. Viewport Meta Tag
```html
<!-- REQUIRED in <head> -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

#### B. Responsive CSS
```css
/* Mobile-first approach */
.container {
  width: 100%;
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}
```

#### C. Flexbox/Grid
```css
/* Flexbox */
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.col {
  flex: 1 1 300px; /* Grow, shrink, base width */
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

**Testing:**
```typescript
// Playwright test
test('responsive on mobile', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  
  // Check mobile menu is visible
  const mobileMenu = page.locator('[data-testid="mobile-menu"]');
  await expect(mobileMenu).toBeVisible();
  
  // Check desktop menu is hidden
  const desktopMenu = page.locator('[data-testid="desktop-menu"]');
  await expect(desktopMenu).not.toBeVisible();
});

test('responsive on desktop', async ({ page }) => {
  // Set desktop viewport
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto('/');
  
  // Check desktop menu is visible
  const desktopMenu = page.locator('[data-testid="desktop-menu"]');
  await expect(desktopMenu).toBeVisible();
  
  // Check mobile menu is hidden
  const mobileMenu = page.locator('[data-testid="mobile-menu"]');
  await expect(mobileMenu).not.toBeVisible();
});
```

================================================================================
## VISUAL REGRESSION TESTING
================================================================================

### Percy (Recommended)
```bash
# Install
npm install --save-dev @percy/cli @percy/playwright

# Run tests with screenshots
npx percy exec -- npx playwright test
```

```typescript
// playwright.config.ts
import { percySnapshot } from '@percy/playwright';

test('visual regression', async ({ page }) => {
  await page.goto('/');
  await percySnapshot(page, 'Homepage');
  
  await page.click('[data-testid="menu"]');
  await percySnapshot(page, 'Homepage with menu open');
});
```

### Playwright Screenshots
```typescript
test('screenshot comparison', async ({ page }) => {
  await page.goto('/');
  
  // Take screenshot
  await expect(page).toHaveScreenshot('homepage.png');
  
  // Take element screenshot
  const header = page.locator('[data-testid="header"]');
  await expect(header).toHaveScreenshot('header.png');
});
```

================================================================================
## ACCESSIBILITY TESTING
================================================================================

### axe-core Integration
```bash
npm install --save-dev @axe-core/playwright
```

```typescript
import { injectAxe, checkA11y } from 'axe-playwright';

test('accessibility', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page);
});
```

### Manual Checks
```typescript
test('keyboard navigation', async ({ page }) => {
  await page.goto('/');
  
  // Tab through elements
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toHaveAttribute('data-testid', 'first-link');
  
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toHaveAttribute('data-testid', 'second-link');
});

test('screen reader text', async ({ page }) => {
  await page.goto('/');
  
  // Check aria-label
  const button = page.locator('[data-testid="close-button"]');
  await expect(button).toHaveAttribute('aria-label', 'Close dialog');
  
  // Check alt text
  const image = page.locator('[data-testid="logo"]');
  await expect(image).toHaveAttribute('alt', 'Company Logo');
});
```

================================================================================
## PERFORMANCE TESTING
================================================================================

### Lighthouse
```bash
npm install --save-dev @playwright/test lighthouse
```

```typescript
import lighthouse from 'lighthouse';

test('performance', async ({ page }) => {
  await page.goto('/');
  
  const result = await lighthouse(page.url(), {
    port: new URL(page.context().browser().wsEndpoint()).port,
  });
  
  const { performance, accessibility, 'best-practices': bestPractices, seo } = result.lhr.categories;
  
  expect(performance.score).toBeGreaterThan(0.9);
  expect(accessibility.score).toBeGreaterThan(0.9);
  expect(bestPractices.score).toBeGreaterThan(0.9);
  expect(seo.score).toBeGreaterThan(0.9);
});
```

================================================================================
## CHECKLIST
================================================================================

UI/UX TESTING CHECKLIST:
────────────────────────────────────────────────────────────────────────────
☐ Icons display correctly
☐ Colors apply correctly
☐ CSS loads properly
☐ Images load successfully
☐ Fonts render correctly
☐ Layout is responsive
☐ Mobile view works
☐ Tablet view works
☐ Desktop view works
☐ Dark mode works (if applicable)
☐ Animations work smoothly
☐ Hover states work
☐ Focus states visible
☐ Loading states show
☐ Error states show
☐ Empty states show
☐ Accessibility passes
☐ Performance is good
☐ Visual regression passes

================================================================================
## REMEMBER
================================================================================

✓ Test on multiple browsers
✓ Test on multiple devices
✓ Test with different screen sizes
✓ Test with slow network
✓ Test with disabled JavaScript
✓ Test accessibility
✓ Test performance
✓ Take screenshots for comparison
✓ Fix issues immediately

Great UI/UX = Happy Users!
================================================================================

