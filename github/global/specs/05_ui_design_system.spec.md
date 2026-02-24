# UI Design System Specification

**Version:** 2.0.0  
**Status:** Implemented  
**Last Updated:** 2026-01-16

---

## Overview

نظام تصميم متكامل يوفر 73+ مكون UI مع دعم كامل للعربية (RTL) والوضع الداكن.

---

## Design Tokens

### Colors
```css
/* Primary */
--primary: #3b82f6;
--primary-hover: #2563eb;
--primary-light: #93c5fd;

/* Secondary */
--secondary: #64748b;
--secondary-hover: #475569;

/* Success/Error/Warning */
--success: #22c55e;
--error: #ef4444;
--warning: #f59e0b;
--info: #06b6d4;

/* Background */
--bg-primary: #ffffff;
--bg-secondary: #f8fafc;
--bg-dark: #0f172a;

/* Text */
--text-primary: #1e293b;
--text-secondary: #64748b;
--text-dark: #f8fafc;
```

### Typography
```css
/* Font Family */
--font-primary: 'IBM Plex Sans Arabic', 'Inter', sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
```

### Spacing
```css
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-6: 1.5rem;
--space-8: 2rem;
```

### Border Radius
```css
--radius-sm: 0.25rem;
--radius-md: 0.375rem;
--radius-lg: 0.5rem;
--radius-xl: 0.75rem;
--radius-full: 9999px;
```

---

## Components

### Button
```jsx
<Button variant="primary|secondary|outline|ghost|danger" size="sm|md|lg">
  Label
</Button>
```

### Input
```jsx
<Input 
  type="text|email|password|number"
  label="Label"
  placeholder="Placeholder"
  error="Error message"
/>
```

### Card
```jsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

### Table
```jsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Column</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Data</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Badge
```jsx
<Badge variant="default|success|warning|danger|info">
  Status
</Badge>
```

---

## RTL Support

- All components support `dir="rtl"`
- Automatic text alignment
- Mirrored icons where needed
- Correct date formatting for Arabic

---

## Dark Mode

Toggle via:
```jsx
<ThemeProvider>
  {/* Automatically switches classes */}
</ThemeProvider>
```

CSS classes:
```css
.dark .bg-primary { background: var(--bg-dark); }
.dark .text-primary { color: var(--text-dark); }
```

---

## Responsive Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Small desktop |
| xl | 1280px | Desktop |
| 2xl | 1536px | Large desktop |

---

## Implementation Status

- ✅ 73+ UI Components
- ✅ Design Tokens
- ✅ RTL Support
- ✅ Dark Mode
- ✅ Responsive Design
- ✅ Accessibility (WCAG AA)
