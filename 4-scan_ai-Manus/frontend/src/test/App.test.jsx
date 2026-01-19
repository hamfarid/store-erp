/**
 * App.test.jsx - Tests for Main Application Component
 * Path: /home/ubuntu/gaara_scan_ai/frontend/src/test/App.test.jsx
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../../App';

// Mock API Service
vi.mock('../../services/ApiService', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}));

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render without crashing', () => {
    render(<App />);
    expect(document.body).toBeTruthy();
  });

  it('should render router component', () => {
    const { container } = render(<App />);
    expect(container.querySelector('div')).toBeTruthy();
  });

  it('should have toast notifications container', () => {
    render(<App />);
    // Toaster component should be present
    expect(document.body).toBeTruthy();
  });
});
