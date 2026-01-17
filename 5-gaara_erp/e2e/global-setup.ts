/**
 * Playwright Global Setup for Gaara ERP v12
 * 
 * Runs once before all tests.
 */

import { FullConfig } from '@playwright/test';
import fs from 'fs';
import path from 'path';

async function globalSetup(config: FullConfig): Promise<void> {
  console.log('🚀 Starting E2E Global Setup...');
  
  // Create necessary directories
  const authDir = path.join(__dirname, 'playwright/.auth');
  if (!fs.existsSync(authDir)) {
    fs.mkdirSync(authDir, { recursive: true });
  }
  
  // Create test results directory
  const resultsDir = path.join(__dirname, 'test-results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }
  
  // Set environment variables for tests
  process.env.E2E_RUNNING = 'true';
  
  console.log('✅ E2E Global Setup Complete');
}

export default globalSetup;

