/**
 * AuthContext.test.jsx - Tests for Authentication Context
 * Path: /home/ubuntu/gaara_scan_ai/frontend/src/test/AuthContext.test.jsx
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../../context/AuthContext';
import React from 'react';

// Mock ApiService
vi.mock('../../services/ApiService', () => ({
  default: {
    setToken: vi.fn(),
    get: vi.fn(),
    post: vi.fn(),
  }
}));

// Test component that uses AuthContext
const TestComponent = () => {
  const { user, isAuthenticated, loading } = useAuth();
  
  return (
    <div>
      <div data-testid="loading">{loading ? 'loading' : 'loaded'}</div>
      <div data-testid="authenticated">{isAuthenticated ? 'authenticated' : 'not authenticated'}</div>
      <div data-testid="user">{user ? user.email : 'no user'}</div>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should provide authentication context', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('loaded');
    });
  });

  it('should show not authenticated when no token', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('authenticated')).toHaveTextContent('not authenticated');
    });
  });

  it('should show authenticated when token exists', async () => {
    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('user', JSON.stringify({ email: 'test@example.com' }));

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('authenticated')).toHaveTextContent('authenticated');
      expect(screen.getByTestId('user')).toHaveTextContent('test@example.com');
    });
  });

  it('should throw error when useAuth is used outside provider', () => {
    // Suppress console.error for this test
    const originalError = console.error;
    console.error = vi.fn();

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useAuth must be used within an AuthProvider');

    console.error = originalError;
  });
});
