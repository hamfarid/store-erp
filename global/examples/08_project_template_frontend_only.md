# Project Template: Frontend-Only Application

## Overview
Modern frontend application template with React, TypeScript, and best practices.

## Project Structure
```
frontend-project/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   └── Modal/
│   │   ├── layout/
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   └── Sidebar/
│   │   └── features/
│   │       ├── auth/
│   │       └── dashboard/
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   └── NotFound.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── auth.service.ts
│   ├── store/
│   │   ├── slices/
│   │   └── store.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── useApi.ts
│   ├── utils/
│   │   ├── validators.ts
│   │   └── formatters.ts
│   ├── types/
│   │   └── index.ts
│   ├── styles/
│   │   └── global.css
│   ├── App.tsx
│   └── main.tsx
├── public/
│   ├── favicon.ico
│   └── manifest.json
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

## Tech Stack
- **Framework:** React 18+
- **Language:** TypeScript
- **Build Tool:** Vite
- **State Management:** Redux Toolkit or Zustand
- **Routing:** React Router v6
- **UI Library:** Material-UI, Ant Design, or Tailwind CSS
- **HTTP Client:** Axios or React Query
- **Form Handling:** React Hook Form
- **Validation:** Zod
- **Testing:** Vitest + React Testing Library
- **E2E Testing:** Playwright

## Key Features
1. **TypeScript** for type safety
2. **Component Library** with reusable components
3. **State Management** with Redux Toolkit
4. **API Integration** with Axios and React Query
5. **Form Validation** with React Hook Form + Zod
6. **Routing** with protected routes
7. **Responsive Design** mobile-first
8. **Dark Mode** support
9. **Internationalization (i18n)**
10. **Progressive Web App (PWA)**

## Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env:
# VITE_API_URL=http://localhost:3000/api
```

### 3. Run Development Server
```bash
npm run dev
```

Application will be available at: `http://localhost:5173`

## Component Example

### Button Component
```typescript
// src/components/common/Button/Button.tsx
import React from 'react';
import './Button.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  children,
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## API Service Example

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

## Testing

### Unit Tests
```bash
npm run test
```

### E2E Tests
```bash
npm run test:e2e
```

### Coverage
```bash
npm run test:coverage
```

## Build for Production
```bash
npm run build
```

Output will be in `dist/` directory.

## Deployment

### Static Hosting (Netlify, Vercel)
```bash
npm run build
# Upload dist/ folder
```

### Docker
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Performance Optimization
- ✅ Code splitting with React.lazy()
- ✅ Image optimization
- ✅ Bundle size analysis
- ✅ Lazy loading routes
- ✅ Memoization with useMemo/useCallback
- ✅ Virtual scrolling for large lists

## Accessibility
- ✅ Semantic HTML
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast compliance

## Next Steps
1. Customize theme and branding
2. Add business logic
3. Integrate with backend API
4. Set up CI/CD
5. Deploy to production
