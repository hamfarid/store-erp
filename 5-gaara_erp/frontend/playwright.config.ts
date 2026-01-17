/**
 * Playwright Configuration
 * 
 * Configuration for E2E testing of Store Pro application.
 */

import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory - supports both ./tests/e2e and ./e2e
  testDir: './e2e',
  
  // Fallback test directories
  testMatch: ['**/*.spec.{js,ts}', '**/tests/e2e/**/*.spec.{js,ts}'],
  
  // Output directory for test artifacts
  outputDir: './test-results',
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list'],
  ],
  
  // Shared settings for all the projects below
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: process.env.TEST_URL || 'http://localhost:5505',
    
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video recording
    video: 'on-first-retry',
    
    // Viewport size
    viewport: { width: 1280, height: 720 },
    
    // Ignore HTTPS errors
    ignoreHTTPSErrors: true,
    
    // Maximum time each action such as `click()` can take
    actionTimeout: 10000,
    
    // Navigation timeout
    navigationTimeout: 30000,
    
    // Locale for the browser
    locale: 'ar-SA',
    
    // Timezone
    timezoneId: 'Asia/Riyadh',
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // Test against mobile viewports
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
    // Test against branded browsers
    {
      name: 'Microsoft Edge',
      use: { ...devices['Desktop Edge'], channel: 'msedge' },
    },
    {
      name: 'Google Chrome',
      use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    },
  ],

  // Run local dev server before starting the tests
  // Disabled - run dev server manually: npm run dev
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:5505',
  //   reuseExistingServer: true,
  //   timeout: 120 * 1000,
  // },

  // Global timeout for each test
  timeout: 60 * 1000,
  
  // Expect timeout
  expect: {
    timeout: 10 * 1000,
  },
});

