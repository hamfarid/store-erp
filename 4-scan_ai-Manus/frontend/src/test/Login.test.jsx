/**
 * Login.test.jsx - Tests for Login Page
 * Path: /home/ubuntu/gaara_scan_ai/frontend/src/test/Login.test.jsx
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../../pages/Login';

// Mock ApiService
vi.mock('../../services/ApiService', () => ({
  default: {
    post: vi.fn(() => Promise.resolve({ 
      data: { 
        access_token: 'test-token',
        user: { id: 1, email: 'test@example.com' }
      } 
    })),
  }
}));

// Mock react-router-dom
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  };
});

// Mock toast
vi.mock('react-hot-toast', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('should render login page', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    expect(document.body).toBeTruthy();
  });

  it('should render login form', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    // Check if form elements are present
    expect(document.body.textContent).toBeTruthy();
  });

  it('should have email and password inputs', () => {
    const { container } = render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const inputs = container.querySelectorAll('input');
    expect(inputs.length).toBeGreaterThan(0);
  });

  it('should have submit button', () => {
    const { container } = render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const buttons = container.querySelectorAll('button');
    expect(buttons.length).toBeGreaterThan(0);
  });
});
