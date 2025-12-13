/**
 * Performance Analysis Test
 * Measures Web Vitals and performance metrics for the Store ERP system
 * 
 * Target Metrics:
 * - FCP (First Contentful Paint): < 1.8s
 * - LCP (Largest Contentful Paint): < 2.5s
 * - TTI (Time to Interactive): < 3.8s
 * - CLS (Cumulative Layout Shift): < 0.1
 */

import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5502';
const API_URL = 'http://localhost:5002';

// Performance thresholds
const THRESHOLDS = {
  FCP: 1800,  // 1.8s in ms
  LCP: 2500,  // 2.5s in ms
  TTI: 3800,  // 3.8s in ms
  CLS: 0.1,   // Cumulative Layout Shift
  TTFB: 600,  // Time to First Byte (600ms)
};

test.describe('Performance Analysis', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/(dashboard)?$/);
  });

  test('measure dashboard performance metrics', async ({ page }) => {
    // const metrics = {}; // Currently unused
    
    // Start performance measurement
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });
    
    // Get Web Vitals using Performance API
    const performanceMetrics = await page.evaluate(() => {
      return new Promise((resolve) => {
        const metrics = {};
        
        // Get Navigation Timing
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
          metrics.TTFB = navigation.responseStart - navigation.requestStart;
          metrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
          metrics.loadComplete = navigation.loadEventEnd - navigation.loadEventStart;
        }
        
        // Get Paint Timing
        const paintEntries = performance.getEntriesByType('paint');
        paintEntries.forEach(entry => {
          if (entry.name === 'first-contentful-paint') {
            metrics.FCP = entry.startTime;
          }
        });
        
        // Get Largest Contentful Paint
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          metrics.LCP = lastEntry.startTime;
        });
        
        try {
          observer.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
          // LCP not supported
        }
        
        // Wait a bit for metrics to be collected
        setTimeout(() => {
          observer.disconnect();
          resolve(metrics);
        }, 3000);
      });
    });
    
    // Get resource timing
    const resourceMetrics = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      const summary = {
        totalResources: resources.length,
        totalSize: 0,
        totalDuration: 0,
        byType: {},
      };
      
      resources.forEach(resource => {
        const type = resource.initiatorType || 'other';
        if (!summary.byType[type]) {
          summary.byType[type] = { count: 0, duration: 0 };
        }
        summary.byType[type].count++;
        summary.byType[type].duration += resource.duration;
        summary.totalDuration += resource.duration;
        
        // Estimate size from transferSize if available
        if (resource.transferSize) {
          summary.totalSize += resource.transferSize;
        }
      });
      
      return summary;
    });
    
    // Log results
    console.log('\n📊 Performance Metrics:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`TTFB: ${performanceMetrics.TTFB?.toFixed(2)}ms (target: < ${THRESHOLDS.TTFB}ms)`);
    console.log(`FCP: ${performanceMetrics.FCP?.toFixed(2)}ms (target: < ${THRESHOLDS.FCP}ms)`);
    console.log(`LCP: ${performanceMetrics.LCP?.toFixed(2)}ms (target: < ${THRESHOLDS.LCP}ms)`);
    console.log(`DOM Content Loaded: ${performanceMetrics.domContentLoaded?.toFixed(2)}ms`);
    console.log(`Load Complete: ${performanceMetrics.loadComplete?.toFixed(2)}ms`);
    console.log('\n📦 Resource Summary:');
    console.log(`Total Resources: ${resourceMetrics.totalResources}`);
    console.log(`Total Size: ${(resourceMetrics.totalSize / 1024).toFixed(2)} KB`);
    console.log(`Total Duration: ${resourceMetrics.totalDuration.toFixed(2)}ms`);
    console.log('\n📋 By Type:');
    Object.entries(resourceMetrics.byType).forEach(([type, data]) => {
      console.log(`  ${type}: ${data.count} resources, ${data.duration.toFixed(2)}ms`);
    });
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    // Assertions
    if (performanceMetrics.TTFB) {
      expect(performanceMetrics.TTFB).toBeLessThan(THRESHOLDS.TTFB);
    }
    if (performanceMetrics.FCP) {
      expect(performanceMetrics.FCP).toBeLessThan(THRESHOLDS.FCP);
    }
    if (performanceMetrics.LCP) {
      expect(performanceMetrics.LCP).toBeLessThan(THRESHOLDS.LCP);
    }
  });

  test('measure products page performance', async ({ page }) => {
    await page.goto(`${BASE_URL}/products`, { waitUntil: 'networkidle' });
    
    const metrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0];
      const paintEntries = performance.getEntriesByType('paint');
      
      const result = {
        TTFB: navigation ? navigation.responseStart - navigation.requestStart : 0,
        FCP: 0,
      };
      
      paintEntries.forEach(entry => {
        if (entry.name === 'first-contentful-paint') {
          result.FCP = entry.startTime;
        }
      });
      
      return result;
    });
    
    console.log('\n📊 Products Page Performance:');
    console.log(`TTFB: ${metrics.TTFB.toFixed(2)}ms`);
    console.log(`FCP: ${metrics.FCP.toFixed(2)}ms\n`);
  });
});

