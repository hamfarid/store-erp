# FRONTEND DEVELOPMENT PROMPT

**FILE**: github/global/prompts/21_frontend.md | **PURPOSE**: Frontend development guidelines | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 4: Code Implementation - Frontend

This prompt guides you through building production-ready frontend code.

## Pre-Execution Checklist

- [ ] Planning phase complete
- [ ] Task list exists in `docs/Task_List.md`
- [ ] Design tokens defined
- [ ] Tech stack selected (React/Vue/Angular)

## Core Principles

1. **OSF Framework**: Security (35%) > Correctness (20%) > Reliability (15%)
2. **Component-Based**: Reusable, testable components
3. **Type Safety**: TypeScript for all code
4. **Accessibility**: WCAG AA compliance
5. **Performance**: Lighthouse score ≥90

## Step 1: Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom hooks
│   ├── store/           # State management
│   ├── services/        # API services
│   ├── utils/           # Helper functions
│   ├── types/           # TypeScript types
│   ├── theme/           # Design tokens
│   └── App.tsx          # Root component
├── public/
├── tests/
└── package.json
```

## Step 2: Design Tokens

### theme/tokens.ts

```typescript
// FILE: frontend/src/theme/tokens.ts | PURPOSE: Design tokens | OWNER: Frontend | LAST-AUDITED: 2025-11-18

export const tokens = {
  color: {
    brand: {
      primary: '#0F6CBD',
      secondary: '#0A3D62',
      accent: '#1ABC9C',
    },
    neutral: {
      50: '#F8FAFC',
      100: '#F1F5F9',
      200: '#E2E8F0',
      300: '#CBD5E1',
      400: '#94A3B8',
      500: '#64748B',
      600: '#475569',
      700: '#334155',
      800: '#1E293B',
      900: '#0F172A',
    },
    text: {
      default: '#0F172A',
      muted: '#64748B',
      inverse: '#FFFFFF',
    },
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
  },
  typography: {
    fontFamily: {
      en: 'Inter, system-ui, sans-serif',
      ar: 'Tajawal, system-ui, sans-serif',
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      md: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '24px',
    '2xl': '32px',
    '3xl': '48px',
  },
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    full: '9999px',
  },
  shadow: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  },
};
```

## Step 3: Core Components

### components/Button.tsx

```typescript
// FILE: frontend/src/components/Button.tsx | PURPOSE: Button component | OWNER: Frontend | LAST-AUDITED: 2025-11-18

import React from 'react';
import { tokens } from '../theme/tokens';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'tertiary' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
}) => {
  const styles = {
    base: {
      fontFamily: tokens.typography.fontFamily.en,
      fontWeight: tokens.typography.fontWeight.medium,
      borderRadius: tokens.radius.md,
      cursor: disabled || loading ? 'not-allowed' : 'pointer',
      opacity: disabled || loading ? 0.6 : 1,
      transition: 'all 0.2s ease',
    },
    variant: {
      primary: {
        backgroundColor: tokens.color.brand.primary,
        color: tokens.color.text.inverse,
        border: 'none',
      },
      secondary: {
        backgroundColor: tokens.color.neutral[100],
        color: tokens.color.text.default,
        border: `1px solid ${tokens.color.neutral[300]}`,
      },
      tertiary: {
        backgroundColor: 'transparent',
        color: tokens.color.brand.primary,
        border: 'none',
      },
      destructive: {
        backgroundColor: tokens.color.danger,
        color: tokens.color.text.inverse,
        border: 'none',
      },
    },
    size: {
      sm: {
        fontSize: tokens.typography.fontSize.sm,
        padding: `${tokens.spacing.sm} ${tokens.spacing.md}`,
      },
      md: {
        fontSize: tokens.typography.fontSize.md,
        padding: `${tokens.spacing.md} ${tokens.spacing.lg}`,
      },
      lg: {
        fontSize: tokens.typography.fontSize.lg,
        padding: `${tokens.spacing.lg} ${tokens.spacing.xl}`,
      },
    },
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        ...styles.base,
        ...styles.variant[variant],
        ...styles.size[size],
      }}
      aria-busy={loading}
      aria-disabled={disabled}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
};
```

## Step 4: API Service

### services/api.ts

```typescript
// FILE: frontend/src/services/api.ts | PURPOSE: API client | OWNER: Frontend | LAST-AUDITED: 2025-11-18

import axios, { AxiosInstance, AxiosError } from 'axios';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor (add auth token)
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor (handle errors)
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired, try to refresh
          try {
            await this.refreshToken();
            // Retry the original request
            return this.client.request(error.config!);
          } catch {
            // Refresh failed, logout
            this.logout();
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async login(email: string, password: string) {
    const response = await this.client.post('/api/auth/login', { email, password });
    const { access_token, refresh_token, user } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    return user;
  }

  async refreshToken() {
    const refresh_token = localStorage.getItem('refresh_token');
    const response = await this.client.post('/api/auth/refresh', { refresh_token });
    const { access_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }

  async get<T>(url: string): Promise<T> {
    const response = await this.client.get<T>(url);
    return response.data;
  }

  async post<T>(url: string, data: any): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data: any): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const api = new ApiService();
```

## Step 5: State Management

### store/authStore.ts (using Zustand)

```typescript
// FILE: frontend/src/store/authStore.ts | PURPOSE: Auth state | OWNER: Frontend | LAST-AUDITED: 2025-11-18

import { create } from 'zustand';
import { api } from '../services/api';

interface User {
  id: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  login: async (email: string, password: string) => {
    set({ loading: true, error: null });
    try {
      const user = await api.login(email, password);
      set({ user, isAuthenticated: true, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  logout: () => {
    api.logout();
    set({ user: null, isAuthenticated: false });
  },
}));
```

## Step 6: Pages

### pages/LoginPage.tsx

```typescript
// FILE: frontend/src/pages/LoginPage.tsx | PURPOSE: Login page | OWNER: Frontend | LAST-AUDITED: 2025-11-18

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/Button';
import { useAuthStore } from '../store/authStore';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (error) {
      // Error is handled by the store
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px' }}>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '16px' }}>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <div style={{ marginBottom: '16px' }}>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        {error && <div style={{ color: 'red', marginBottom: '16px' }}>{error}</div>}
        <Button type="submit" loading={loading} disabled={loading}>
          Login
        </Button>
      </form>
    </div>
  );
};
```

## Step 7: Write Tests

See `43_ui_ux_testing.md` for detailed testing guidelines.

## Step 8: Log Actions

Log all implementation to `logs/info.log`

---

**Completion Criteria**:
- [ ] All components created
- [ ] All pages implemented
- [ ] State management configured
- [ ] API service implemented
- [ ] All tests written (≥80% coverage)
- [ ] Accessibility verified (WCAG AA)
- [ ] Performance verified (Lighthouse ≥90)
- [ ] Actions logged

