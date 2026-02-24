# 🎨 Gaara Store - Branding Guide

**Version**: 1.0  
**Date**: 2025-10-27  
**Status**: ✅ **ACTIVE**

---

## 🎯 BRAND IDENTITY

### Brand Name
**Gaara Store** - Inventory Management System for Agricultural Seeds & Supplies

### Brand Values
- 🌱 **Growth**: Helping businesses grow
- 🔒 **Trust**: Secure and reliable
- 🚀 **Innovation**: Modern technology
- 🌍 **Sustainability**: Eco-friendly approach

---

## 🎨 COLOR PALETTE

### Primary Colors

#### Gaara Dark (Primary)
- **Color**: #1F2937 (Dark Gray)
- **Usage**: Main brand color, headers, buttons
- **Hex**: `#1F2937`
- **RGB**: `31, 41, 55`
- **Tailwind**: `gaara-800`

#### Gaara Light (Secondary)
- **Color**: #F3F4F6 (Light Gray)
- **Usage**: Backgrounds, cards
- **Hex**: `#F3F4F6`
- **RGB**: `243, 244, 246`
- **Tailwind**: `gaara-100`

### Accent Colors

#### Indigo (Primary Accent)
- **Color**: #6366F1
- **Usage**: Links, highlights, CTAs
- **Hex**: `#6366F1`
- **RGB**: `99, 102, 241`
- **Tailwind**: `primary-500`

#### Green (Success)
- **Color**: #10B981
- **Usage**: Success messages, positive actions
- **Hex**: `#10B981`
- **RGB**: `16, 185, 129`
- **Tailwind**: `success-500`

#### Amber (Warning)
- **Color**: #F59E0B
- **Usage**: Warnings, alerts
- **Hex**: `#F59E0B`
- **RGB**: `245, 158, 11`
- **Tailwind**: `warning-500`

#### Red (Error)
- **Color**: #EF4444
- **Usage**: Errors, destructive actions
- **Hex**: `#EF4444`
- **RGB**: `239, 68, 68`
- **Tailwind**: `danger-500`

### MagSeeds Brand Colors
- **Primary**: #F04438 (Red)
- **Secondary**: #D92D20 (Dark Red)
- **Accent**: #F97066 (Light Red)

---

## 🔤 TYPOGRAPHY

### Font Family
- **Primary**: Cairo (Arabic)
- **Secondary**: Tajawal (Arabic)
- **Fallback**: System UI, Sans-serif

### Font Sizes

| Size | Pixels | Usage |
|------|--------|-------|
| H1 | 32px | Page titles |
| H2 | 24px | Section titles |
| H3 | 20px | Subsection titles |
| Body | 16px | Regular text |
| Small | 14px | Secondary text |
| Tiny | 12px | Labels, hints |

### Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Light | 300 | Subtle text |
| Regular | 400 | Body text |
| Medium | 500 | Emphasis |
| Bold | 700 | Headings |
| Black | 900 | Strong emphasis |

---

## 📏 SPACING SYSTEM

| Size | Pixels | Tailwind | Usage |
|------|--------|----------|-------|
| xs | 4px | `p-1` | Tight spacing |
| sm | 8px | `p-2` | Small spacing |
| md | 16px | `p-4` | Default spacing |
| lg | 24px | `p-6` | Large spacing |
| xl | 32px | `p-8` | Extra large |
| 2xl | 48px | `p-12` | Huge spacing |

---

## 🔘 COMPONENT STYLING

### Buttons

#### Primary Button
```jsx
<button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
  Primary Action
</button>
```

#### Secondary Button
```jsx
<button className="px-4 py-2 bg-gaara-200 text-gaara-900 rounded-lg hover:bg-gaara-300 transition">
  Secondary Action
</button>
```

#### Danger Button
```jsx
<button className="px-4 py-2 bg-danger-600 text-white rounded-lg hover:bg-danger-700 transition">
  Delete
</button>
```

### Cards

```jsx
<div className="bg-white rounded-lg shadow-md p-6 border border-gaara-200">
  <h3 className="text-lg font-bold text-gaara-900 mb-4">Card Title</h3>
  <p className="text-gaara-600">Card content</p>
</div>
```

### Forms

```jsx
<input
  type="text"
  className="w-full px-4 py-2 border border-gaara-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
  placeholder="Enter text"
/>
```

---

## 🌙 DARK MODE

### Dark Mode Colors
- **Background**: #111827 (Dark)
- **Surface**: #1F2937 (Darker)
- **Text**: #F3F4F6 (Light)
- **Border**: #374151 (Gray)

### Dark Mode Usage
```jsx
<div className="dark:bg-gaara-900 dark:text-gaara-100">
  Content
</div>
```

---

## 🌐 RTL SUPPORT

### RTL Implementation
```jsx
<div dir="rtl" className="text-right">
  محتوى عربي
</div>
```

### RTL Spacing
- Use `mr-` instead of `ml-` for margins
- Use `pr-` instead of `pl-` for padding
- Use `right-` instead of `left-` for positioning

---

## ✨ ANIMATIONS

### Fade In
```jsx
<div className="animate-fade-in">Content</div>
```

### Slide Up
```jsx
<div className="animate-slide-up">Content</div>
```

### Bounce In
```jsx
<div className="animate-bounce-in">Content</div>
```

---

## 📱 RESPONSIVE DESIGN

### Breakpoints
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

### Responsive Classes
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Responsive grid */}
</div>
```

---

## 🎯 USAGE GUIDELINES

### Do's ✅
- Use brand colors consistently
- Maintain proper spacing
- Use Arabic fonts for Arabic text
- Implement dark mode
- Support RTL layout
- Use semantic HTML
- Follow accessibility guidelines

### Don'ts ❌
- Don't mix brand colors randomly
- Don't use non-brand fonts
- Don't ignore dark mode
- Don't forget RTL support
- Don't use low contrast colors
- Don't create custom colors

---

## 📚 RESOURCES

- **Tailwind Config**: `frontend/tailwind.config.js`
- **Global Styles**: `frontend/src/App.css`
- **Component Styles**: `frontend/src/styles/`
- **Design System**: `frontend/src/components/ui/`

---

**Status**: ✅ **ACTIVE**  
**Last Updated**: 2025-10-27  
**Maintained By**: Augment Agent

🎨 **Follow this guide for consistent branding!** 🎨

