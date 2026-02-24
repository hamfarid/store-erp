# 🎨 Store Project - UI Design System

**Version:** 1.0.0  
**Last Updated:** December 8, 2025  
**Framework:** React + TailwindCSS + shadcn/ui + Radix UI

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Color System](#color-system)
4. [Typography](#typography)
5. [Spacing & Layout](#spacing--layout)
6. [Components](#components)
7. [Icons](#icons)
8. [Accessibility](#accessibility)
9. [RTL Support](#rtl-support)
10. [Dark Mode](#dark-mode)

---

## Overview

This design system provides a comprehensive set of reusable UI components and design tokens for the Store inventory management application. Built on TailwindCSS and shadcn/ui, it ensures consistency, accessibility, and a modern user experience.

### Tech Stack

- **React 18** - UI Framework
- **TailwindCSS 4** - Utility-first CSS
- **Radix UI** - Headless accessible components
- **shadcn/ui** - Pre-styled component library
- **Lucide React** - Icon library
- **class-variance-authority (CVA)** - Variant management
- **clsx + tailwind-merge** - Class utilities

---

## Design Principles

### 1. **Consistency**
All components follow the same design patterns, spacing, and color schemes.

### 2. **Accessibility**
WCAG 2.1 AA compliant with proper ARIA labels, keyboard navigation, and focus indicators.

### 3. **RTL Support**
Full right-to-left support for Arabic language users with proper text alignment and directional icons.

### 4. **Performance**
Lazy loading, code splitting, and optimized bundle sizes.

### 5. **Responsiveness**
Mobile-first design with breakpoints at sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px).

---

## Color System

### Primary Colors (Teal)

```css
--primary-50: #f0fdfa
--primary-100: #ccfbf1
--primary-200: #99f6e4
--primary-300: #5eead4
--primary-400: #2dd4bf
--primary-500: #14b8a6  /* Primary */
--primary-600: #0d9488
--primary-700: #0f766e
--primary-800: #115e59
--primary-900: #134e4a
```

### Semantic Colors

| Color | Usage | CSS Variable |
|-------|-------|--------------|
| **Success** | Positive actions, confirmations | `--color-success: #10b981` |
| **Warning** | Caution states | `--color-warning: #f59e0b` |
| **Error** | Destructive actions, errors | `--color-destructive: #ef4444` |
| **Info** | Informational messages | `--color-info: #3b82f6` |

### Background Colors

```css
/* Light Mode */
--background: 0 0% 100%
--foreground: 222.2 84% 4.9%
--muted: 210 40% 96.1%
--muted-foreground: 215.4 16.3% 46.9%

/* Dark Mode */
--background: 222.2 84% 4.9%
--foreground: 210 40% 98%
--muted: 217.2 32.6% 17.5%
--muted-foreground: 215 20.2% 65.1%
```

---

## Typography

### Font Families

```css
--font-sans: 'Cairo', 'Tajawal', 'Segoe UI', sans-serif
--font-arabic: 'Cairo', 'Tajawal', 'Noto Sans Arabic', sans-serif
```

### Font Sizes

| Class | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `text-xs` | 12px | 16px | Captions, labels |
| `text-sm` | 14px | 20px | Secondary text |
| `text-base` | 16px | 24px | Body text |
| `text-lg` | 18px | 28px | Emphasis |
| `text-xl` | 20px | 28px | Subheadings |
| `text-2xl` | 24px | 32px | Section titles |
| `text-3xl` | 30px | 36px | Page titles |
| `text-4xl` | 36px | 40px | Hero text |

### Font Weights

- `font-normal`: 400
- `font-medium`: 500
- `font-semibold`: 600
- `font-bold`: 700

---

## Spacing & Layout

### Spacing Scale

```css
/* 4px base unit */
0: 0px
1: 4px
2: 8px
3: 12px
4: 16px
5: 20px
6: 24px
8: 32px
10: 40px
12: 48px
16: 64px
20: 80px
24: 96px
```

### Border Radius

```css
--radius: 0.75rem  /* 12px - Default */

rounded-none: 0
rounded-sm: 4px
rounded: 6px
rounded-md: 8px
rounded-lg: 12px
rounded-xl: 16px
rounded-2xl: 24px
rounded-full: 9999px
```

### Shadows

```css
shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)
shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1)
shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)
shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1)
shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.25)
```

---

## Components

### Button

Location: `src/components/ui/button.jsx`

**Variants:**
- `default` - Primary teal background
- `secondary` - Muted background
- `destructive` - Red for dangerous actions
- `outline` - Border only
- `ghost` - No background
- `link` - Text link style
- `success` - Green for confirmations

**Sizes:**
- `sm` - 32px height
- `default` - 40px height
- `lg` - 48px height
- `icon` - Square icon button

```jsx
import { Button } from '@/components/ui/button'

<Button variant="default" size="lg">
  Save Changes
</Button>

<Button variant="destructive" isLoading>
  Delete
</Button>
```

### Card

Location: `src/components/ui/card.jsx`

```jsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description text</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Dialog/Modal

Location: `src/components/ui/dialog.jsx`

Built on Radix UI Dialog with proper accessibility and RTL support.

```jsx
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog'

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
      <DialogDescription>Dialog description</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Alert

Location: `src/components/ui/alert.jsx`

**Variants:**
- `default` - Neutral
- `destructive` - Error/danger
- `success` - Success message
- `warning` - Warning message
- `info` - Informational

```jsx
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'

<Alert variant="success">
  <AlertTitle>Success</AlertTitle>
  <AlertDescription>Your changes have been saved.</AlertDescription>
</Alert>
```

### Badge

Location: `src/components/ui/badge.jsx`

**Variants:**
- `default`, `secondary`, `destructive`, `outline`
- `success`, `warning`, `info`

```jsx
import { Badge } from '@/components/ui/badge'

<Badge variant="success">Active</Badge>
<Badge variant="warning">Pending</Badge>
```

### DataTable

Location: `src/components/ui/DataTable.jsx`

Full-featured data table with sorting, filtering, pagination, and export.

```jsx
import DataTable from '@/components/ui/DataTable'

const columns = [
  { key: 'id', label: 'ID', sortable: true },
  { key: 'name', label: 'Name', searchable: true },
  { key: 'status', label: 'Status', render: (row) => <Badge>{row.status}</Badge> }
]

<DataTable
  data={data}
  columns={columns}
  searchable
  pagination
  pageSize={10}
  exportable
/>
```

### Form

Location: `src/components/ui/form.jsx`

Integrated with react-hook-form and Zod validation.

```jsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'

const form = useForm({
  resolver: zodResolver(schema),
  defaultValues: {}
})

<Form {...form}>
  <FormField
    control={form.control}
    name="email"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input {...field} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>
```

### Command Palette

Location: `src/components/ui/command-palette.jsx`

Global search and navigation (Ctrl+K).

```jsx
import { CommandPalette } from '@/components/ui/command-palette'

<CommandPalette /> // Add to App.jsx
```

### Toast/Sonner

Location: `src/components/ui/sonner.jsx`

Modern toast notifications.

```jsx
import { toast } from 'sonner'

// Success
toast.success('Saved successfully')

// Error
toast.error('Something went wrong')

// Loading
toast.loading('Processing...')

// Promise
toast.promise(saveData(), {
  loading: 'Saving...',
  success: 'Saved!',
  error: 'Failed to save'
})
```

### Sidebar

Location: `src/components/ui/sidebar.jsx`

Responsive sidebar with mobile support.

```jsx
import { SidebarProvider, Sidebar, SidebarContent, SidebarMenu, SidebarMenuItem, SidebarMenuButton } from '@/components/ui/sidebar'

<SidebarProvider>
  <Sidebar>
    <SidebarContent>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton>Dashboard</SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarContent>
  </Sidebar>
</SidebarProvider>
```

### Input

Location: `src/components/ui/input.jsx`

```jsx
import { Input } from '@/components/ui/input'

<Input type="email" placeholder="Enter email" />
```

### Textarea

Location: `src/components/ui/textarea.jsx`

```jsx
import { Textarea } from '@/components/ui/textarea'

<Textarea placeholder="Enter description" rows={4} />
```

### Select

Location: `src/components/ui/select.jsx`

```jsx
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'

<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="1">Option 1</SelectItem>
    <SelectItem value="2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

### Switch

Location: `src/components/ui/switch.jsx`

```jsx
import { Switch } from '@/components/ui/switch'

<Switch checked={enabled} onCheckedChange={setEnabled} />
```

### Tabs

Location: `src/components/ui/tabs.jsx`

```jsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Content 1</TabsContent>
  <TabsContent value="tab2">Content 2</TabsContent>
</Tabs>
```

---

## Icons

Using Lucide React for consistent iconography.

```jsx
import { Home, Settings, User, ChevronRight } from 'lucide-react'

<Home size={24} className="text-primary" />
```

### Common Icons

| Icon | Usage |
|------|-------|
| `Home` | Dashboard |
| `Package` | Products |
| `Users` | Customers |
| `Truck` | Suppliers |
| `Warehouse` | Warehouses |
| `Receipt` | Invoices |
| `BarChart3` | Reports |
| `Settings` | Settings |
| `Shield` | Security |
| `Bell` | Notifications |

---

## Accessibility

### Keyboard Navigation

- All interactive elements are focusable
- Tab order follows visual order
- Focus indicators are visible
- Escape closes modals/dialogs

### ARIA Labels

```jsx
<Button aria-label="Save changes">
  <Save className="h-4 w-4" />
</Button>

<Dialog aria-labelledby="dialog-title" aria-describedby="dialog-description">
  <DialogTitle id="dialog-title">Title</DialogTitle>
  <DialogDescription id="dialog-description">Description</DialogDescription>
</Dialog>
```

### Color Contrast

All text meets WCAG AA contrast requirements:
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum

---

## RTL Support

The application supports full RTL layout for Arabic users.

### Configuration

```jsx
// App.jsx
<div className="App" dir="rtl">
```

### RTL Utilities

```css
/* Automatic RTL in Tailwind */
.rtl\:mr-4:dir(rtl) { margin-right: 1rem; }
.ltr\:ml-4:dir(ltr) { margin-left: 1rem; }

/* Start/End instead of Left/Right */
.ms-4 { margin-inline-start: 1rem; }
.me-4 { margin-inline-end: 1rem; }
.ps-4 { padding-inline-start: 1rem; }
.pe-4 { padding-inline-end: 1rem; }
```

### Icon Mirroring

```jsx
// Icons that need RTL mirroring
<ChevronRight className="rtl:rotate-180" />
<ArrowLeft className="rtl:rotate-180" />
```

---

## Dark Mode

### Theme Toggle

Location: `src/components/ui/theme-toggle.jsx`

```jsx
import { ThemeToggle } from '@/components/ui/theme-toggle'

<ThemeToggle /> // Adds to header
```

### Theme Classes

```css
/* Apply to html element */
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... other dark mode variables */
}
```

### Component Dark Mode

```jsx
// Components automatically adapt
<Card className="bg-card text-card-foreground">
  Content adapts to theme
</Card>
```

---

## File Structure

```
src/
├── components/
│   ├── ui/
│   │   ├── button.jsx
│   │   ├── card.jsx
│   │   ├── dialog.jsx
│   │   ├── alert.jsx
│   │   ├── badge.jsx
│   │   ├── input.jsx
│   │   ├── form.jsx
│   │   ├── select.jsx
│   │   ├── switch.jsx
│   │   ├── tabs.jsx
│   │   ├── table.jsx
│   │   ├── DataTable.jsx
│   │   ├── sidebar.jsx
│   │   ├── command.jsx
│   │   ├── command-palette.jsx
│   │   ├── sonner.jsx
│   │   ├── theme-toggle.jsx
│   │   └── ... more components
│   ├── auth/
│   │   └── ProtectedRoute.jsx
│   └── ... feature components
├── contexts/
│   ├── ThemeContext.jsx
│   ├── AuthContext.jsx
│   └── PermissionContext.jsx
├── hooks/
│   └── use-mobile.js
├── lib/
│   └── utils.js
├── styles/
│   └── theme.css
└── App.css
```

---

## Usage Guidelines

### Do's ✅

- Use semantic HTML elements
- Provide descriptive labels and alt text
- Use the design tokens (colors, spacing)
- Test on mobile devices
- Test keyboard navigation
- Use loading states for async operations

### Don'ts ❌

- Don't use inline styles
- Don't hardcode colors (use CSS variables)
- Don't skip accessibility attributes
- Don't create new components without checking existing ones
- Don't ignore RTL considerations

---

## Contributing

When adding new components:

1. Follow the existing component structure
2. Use CVA for variant management
3. Add proper TypeScript/JSDoc types
4. Include accessibility features
5. Support dark mode
6. Support RTL layout
7. Add to this documentation

---

**Maintained by:** Store Development Team  
**Questions?** Open an issue in the repository
