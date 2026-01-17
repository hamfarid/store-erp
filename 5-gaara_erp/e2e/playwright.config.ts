/**
 * Playwright E2E Test Configuration for Gaara ERP v12
 * 
 * Usage:
 *   npm run test:e2e       # Run all E2E tests
 *   npm run test:e2e:ui    # Run with Playwright UI
 *   npm run test:e2e:headed # Run in headed mode
 */

import { defineConfig, devices } from '@playwright/test';

// Environment variables with defaults
const BASE_URL = process.env.E2E_BASE_URL || 'http://localhost:5173';
const API_URL = process.env.E2E_API_URL || 'http://localhost:8000';
const CI = process.env.CI === 'true';

export default defineConfig({
  // Test directory
  testDir: './tests',
  
  // Test file patterns
  testMatch: ['**/*.spec.ts', '**/*.e2e.ts'],
  
  // Timeout settings
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  
  // Parallel execution
  fullyParallel: true,
  
  // Fail fast in CI
  forbidOnly: CI,
  
  // Retry settings
  retries: CI ? 2 : 0,
  
  // Workers
  workers: CI ? 1 : undefined,
  
  // Reporter configuration
  reporter: CI
    ? [
        ['html', { outputFolder: 'playwright-report' }],
        ['junit', { outputFile: 'test-results/e2e-results.xml' }],
        ['github'],
      ]
    : [['html', { open: 'never' }]],
  
  // Shared settings for all projects
  use: {
    baseURL: BASE_URL,
    
    // Tracing
    trace: CI ? 'on-first-retry' : 'retain-on-failure',
    
    // Screenshots
    screenshot: 'only-on-failure',
    
    // Videos
    video: CI ? 'on-first-retry' : 'off',
    
    // Viewport
    viewport: { width: 1280, height: 720 },
    
    // Locale for Arabic support
    locale: 'ar-SA',
    
    // Timezone
    timezoneId: 'Asia/Riyadh',
    
    // Action timeout
    actionTimeout: 15000,
    
    // Navigation timeout
    navigationTimeout: 30000,
    
    // Extra HTTP headers
    extraHTTPHeaders: {
      'Accept-Language': 'ar,en',
    },
  },
  
  // Browser projects
  projects: [
    // Setup project - runs before all tests
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    
    // Chrome Desktop
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    
    // Firefox Desktop
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    
    // Safari Desktop
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    
    // Mobile Chrome
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    
    // Mobile Safari
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 12'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
  
  // Output directory
  outputDir: 'test-results',
  
  // Global setup/teardown
  globalSetup: './global-setup.ts',
  globalTeardown: './global-teardown.ts',
  
  // Web server configuration - start the app before tests
  webServer: [
    // Frontend
    {
      command: 'npm run dev',
      url: BASE_URL,
      reuseExistingServer: !CI,
      timeout: 120000,
      cwd: '../gaara-erp-frontend',
    },
    // Backend API (optional, comment if running separately)
    // {
    //   command: 'python manage.py runserver',
    //   url: API_URL,
    //   reuseExistingServer: !CI,
    //   timeout: 120000,
    //   cwd: '../gaara_erp',
    // },
  ],
});

