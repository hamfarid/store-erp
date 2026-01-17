/**
 * FILE: frontend/src/api/__tests__/client.test.ts
 * PURPOSE: Unit tests for API client
 * OWNER: Frontend Team
 * RELATED: frontend/src/api/client.ts
 * LAST-AUDITED: 2025-10-27
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ApiClient } from '../client';

describe('ApiClient', () => {
  let client: ApiClient;

  beforeEach(() => {
    client = new ApiClient('http://localhost:5002');
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('Authentication', () => {
    it('should initialize without token', () => {
      expect(client.isAuthenticated()).toBe(false);
      expect(client.getToken()).toBeUndefined();
    });

    it('should save tokens after login', async () => {
      const mockResponse = {
        success: true,
        data: {
          access_token: 'test-access-token',
          refresh_token: 'test-refresh-token',
          user: { id: '1', username: 'test' },
        },
      };

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        } as Response)
      );

      await client.login({ username: 'test', password: 'password' });

      expect(client.isAuthenticated()).toBe(true);
      expect(client.getToken()).toBe('test-access-token');
      expect(localStorage.getItem('access_token')).toBe('test-access-token');
      expect(localStorage.getItem('refresh_token')).toBe('test-refresh-token');
    });

    it('should clear tokens on logout', async () => {
      localStorage.setItem('access_token', 'test-token');
      client['token'] = 'test-token';

      const mockResponse = { success: true, message: 'Logged out' };

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        } as Response)
      );

      await client.logout();

      expect(client.isAuthenticated()).toBe(false);
      expect(localStorage.getItem('access_token')).toBeNull();
    });
  });

  describe('Request handling', () => {
    it('should include authorization header when authenticated', async () => {
      client['token'] = 'test-token';

      const mockResponse = { success: true, data: [] };

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        } as Response)
      );

      await client.getProducts();

      expect(global.fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer test-token',
          }),
        })
      );
    });

    it('should retry on failure', async () => {
      let attempts = 0;

      global.fetch = vi.fn(() => {
        attempts++;
        if (attempts < 3) {
          return Promise.reject(new Error('Network error'));
        }
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ success: true, data: [] }),
        } as Response);
      });

      client.setRetries(2);
      const result = await client.getProducts();

      expect(attempts).toBe(3);
      expect(result).toBeDefined();
    });

    it('should throw error after max retries', async () => {
      global.fetch = vi.fn(() =>
        Promise.reject(new Error('Network error'))
      );

      client.setRetries(1);

      await expect(client.getProducts()).rejects.toThrow();
    });
  });

  describe('Timeout handling', () => {
    it('should respect custom timeout', async () => {
      client.setTimeout(1000);

      global.fetch = vi.fn(() =>
        new Promise(resolve =>
          setTimeout(() => {
            resolve({
              ok: true,
              json: () => Promise.resolve({ success: true, data: [] }),
            } as Response);
          }, 2000)
        )
      );

      await expect(client.getProducts()).rejects.toThrow();
    });
  });

  describe('API methods', () => {
    beforeEach(() => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ success: true, data: {} }),
        } as Response)
      );
    });

    it('should call correct endpoint for getProducts', async () => {
      await client.getProducts({ page: 1, per_page: 10 });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/products'),
        expect.any(Object)
      );
    });

    it('should call correct endpoint for getCustomers', async () => {
      await client.getCustomers({ page: 1, per_page: 10 });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/customers'),
        expect.any(Object)
      );
    });

    it('should call correct endpoint for setupMFA', async () => {
      await client.setupMFA();

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/mfa/setup'),
        expect.any(Object)
      );
    });
  });
});

