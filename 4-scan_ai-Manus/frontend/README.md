# 🌾 Gaara AI - Frontend (Canonical)

**Version:** 3.0.0  
**Framework:** React 18 + Vite  
**UI Library:** Tailwind CSS + shadcn/ui  
**Status:** Production Ready

---

## 📁 Project Structure

```
frontend/
├── components/          # Reusable UI components (47+)
│   ├── Advanced/       # Advanced components
│   ├── Analytics/      # Analytics components
│   ├── Charts/         # Chart components
│   ├── Layout/         # Layout components
│   ├── Router/         # Router components
│   └── UI/             # shadcn/ui components
├── pages/              # Page components (30+)
│   ├── Dashboard.jsx
│   ├── Login.jsx
│   ├── Farms.jsx
│   ├── Diagnosis.jsx
│   └── [other pages]/
├── services/           # API services
│   ├── ApiService.js
│   ├── ApiServiceComplete.js
│   └── ApiServiceEnhanced.js
├── context/            # React contexts
│   ├── AuthContext.jsx
│   └── DataContext.jsx
├── hooks/              # Custom hooks
│   └── use-mobile.js
├── assets/             # Static assets
├── App.jsx             # Main app component
├── main.jsx            # Entry point
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
├── tailwind.config.js  # Tailwind configuration
├── package.json        # Dependencies
├── .env                # Environment variables (local)
└── .env.example        # Environment template
```

---

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0 or pnpm >= 8.0.0

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Copy environment file
cp .env.example .env

# Update .env with your backend URL
# VITE_API_URL=http://localhost:8000/api
```

### Development

```bash
# Start development server
npm run dev

# Server will run on http://localhost:3000
```

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🔧 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint errors |
| `npm run format` | Format code with Prettier |
| `npm run test` | Run tests with Vitest |
| `npm run test:ui` | Run tests with UI |
| `npm run test:coverage` | Generate coverage report |
| `npm run type-check` | TypeScript type checking |
| `npm run analyze` | Analyze bundle size |

---

## 🌐 Environment Variables

See `.env.example` for all available environment variables.

**Required:**
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000/api)

**Optional:**
- `VITE_APP_NAME` - Application name
- `VITE_APP_VERSION` - Application version
- `VITE_ENABLE_PWA` - Enable PWA features
- `VITE_ENABLE_DEBUG` - Enable debug mode

---

## 📦 Key Dependencies

### Core
- **React** 18.2.0 - UI library
- **React Router** 6.20.1 - Routing
- **Vite** - Build tool

### UI & Styling
- **Tailwind CSS** 3.3.6 - Utility-first CSS
- **Radix UI** - Accessible components
- **Lucide React** - Icons
- **Framer Motion** - Animations

### State Management
- **TanStack Query** 5.14.2 - Server state
- **Zustand** 4.4.7 - Client state

### Forms & Validation
- **React Hook Form** 7.48.2 - Form handling
- **Zod** 3.22.4 - Schema validation

### Charts & Visualization
- **Recharts** 2.8.0 - Charts
- **Chart.js** 4.4.1 - Advanced charts

### Utilities
- **Axios** 1.6.2 - HTTP client
- **date-fns** 3.0.6 - Date utilities
- **lodash** 4.17.21 - Utility functions

---

## 🎨 UI Components

The frontend uses **shadcn/ui** components built on **Radix UI** primitives:

- Dialog, Dropdown Menu, Select, Tabs
- Tooltip, Progress, Avatar, Checkbox
- Accordion, Alert Dialog, Popover
- And 30+ more components

All components are fully accessible (WCAG AA) and customizable with Tailwind CSS.

---

## 🔐 Authentication

Authentication is handled via JWT tokens:

1. User logs in → receives access token + refresh token
2. Access token stored in localStorage
3. Refresh token used to get new access token
4. AuthContext provides authentication state globally

---

## 📱 Responsive Design

The application is fully responsive with breakpoints:

- **Mobile:** < 640px
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

---

## 🌍 Internationalization (i18n)

Supports Arabic (RTL) and English (LTR):

- Default language: Arabic
- Language switcher in settings
- RTL layout support
- Date/number formatting per locale

---

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

---

## 📄 License

Proprietary - Gaara AI Team

---

## 👥 Team

- **Frontend Team** - UI/UX Development
- **Backend Team** - API Integration
- **Autonomous AI Agent** - Code Consolidation

---

**Last Updated:** 2025-11-18  
**Status:** ✅ Production Ready

