# 📊 Performance Monitoring System

**Priority:** HIGH  
**Phase:** 4 (Testing) & 6 (Deployment)  
**Status:** Production Ready

---

## 🎯 Purpose

Monitor and optimize application performance continuously using **Lighthouse CI**, **Web Vitals**, and **Performance Budgets** to ensure fast, responsive user experiences.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Performance Metrics](#performance-metrics)
3. [Monitoring Tools](#monitoring-tools)
4. [Implementation](#implementation)
5. [Performance Budgets](#performance-budgets)
6. [Automated Gates](#automated-gates)
7. [Reporting](#reporting)
8. [Best Practices](#best-practices)

---

## 1. Overview

### What is Performance Monitoring?

Performance monitoring tracks key metrics that affect user experience:
- Page load time
- Time to interactive
- First contentful paint
- Largest contentful paint
- Cumulative layout shift
- First input delay

### Why It Matters

**User Impact:**
- 1 second delay = 7% reduction in conversions
- 53% of mobile users abandon sites that take >3 seconds to load
- Fast sites rank higher in search results

**Business Impact:**
- Better user retention
- Higher conversion rates
- Improved SEO rankings
- Reduced bounce rates

---

## 2. Performance Metrics

### Core Web Vitals (Google)

#### 1. Largest Contentful Paint (LCP)
**Measures:** Loading performance  
**Target:** < 2.5 seconds  
**Good:** < 2.5s | **Needs Improvement:** 2.5-4s | **Poor:** > 4s

**What it measures:**
- Time until largest content element is rendered
- Usually the hero image or main heading

**How to improve:**
- Optimize images (WebP, lazy loading)
- Reduce server response time
- Use CDN
- Eliminate render-blocking resources

---

#### 2. First Input Delay (FID)
**Measures:** Interactivity  
**Target:** < 100 milliseconds  
**Good:** < 100ms | **Needs Improvement:** 100-300ms | **Poor:** > 300ms

**What it measures:**
- Time from user interaction to browser response
- Button clicks, link clicks, input focus

**How to improve:**
- Reduce JavaScript execution time
- Break up long tasks
- Use web workers
- Code splitting

---

#### 3. Cumulative Layout Shift (CLS)
**Measures:** Visual stability  
**Target:** < 0.1  
**Good:** < 0.1 | **Needs Improvement:** 0.1-0.25 | **Poor:** > 0.25

**What it measures:**
- Unexpected layout shifts during page load
- Elements moving around

**How to improve:**
- Set size attributes on images/videos
- Avoid inserting content above existing content
- Use transform animations instead of layout properties
- Reserve space for ads

---

### Additional Metrics

#### Time to First Byte (TTFB)
**Target:** < 600ms  
**Measures:** Server response time

#### First Contentful Paint (FCP)
**Target:** < 1.8s  
**Measures:** Time to first content render

#### Time to Interactive (TTI)
**Target:** < 3.8s  
**Measures:** Time until page is fully interactive

#### Total Blocking Time (TBT)
**Target:** < 200ms  
**Measures:** Time page is blocked from user input

#### Speed Index
**Target:** < 3.4s  
**Measures:** How quickly content is visually displayed

---

## 3. Monitoring Tools

### 1. Lighthouse CI

**Installation:**
```bash
npm install -g @lhci/cli
```

**Configuration:**
```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 5,
      settings: {
        preset: 'desktop',
        throttling: {
          rttMs: 40,
          throughputKbps: 10240,
          cpuSlowdownMultiplier: 1
        }
      }
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', {minScore: 0.9}],
        'categories:accessibility': ['error', {minScore: 0.9}],
        'categories:best-practices': ['error', {minScore: 0.9}],
        'categories:seo': ['error', {minScore: 0.9}],
        'first-contentful-paint': ['error', {maxNumericValue: 2000}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'total-blocking-time': ['error', {maxNumericValue: 200}]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
```

**Usage:**
```bash
# Run Lighthouse CI
lhci autorun

# With custom config
lhci autorun --config=./lighthouserc.js
```

---

### 2. Web Vitals Library

**Installation:**
```bash
npm install web-vitals
```

**Implementation:**
```javascript
// monitor-vitals.js
import {onCLS, onFID, onLCP, onFCP, onTTFB} from 'web-vitals';

function sendToAnalytics(metric) {
  // Send to your analytics endpoint
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      name: metric.name,
      value: metric.value,
      id: metric.id,
      delta: metric.delta,
      rating: metric.rating
    }),
    headers: {'Content-Type': 'application/json'}
  });
}

// Monitor all Core Web Vitals
onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

**In HTML:**
```html
<script type="module">
  import {onCLS, onFID, onLCP} from 'https://unpkg.com/web-vitals@3?module';

  onCLS(console.log);
  onFID(console.log);
  onLCP(console.log);
</script>
```

---

### 3. Performance Observer API

**Implementation:**
```javascript
// performance-observer.js
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.initObservers();
  }

  initObservers() {
    // Observe navigation timing
    if ('PerformanceObserver' in window) {
      const navObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.metrics.navigation = {
            dns: entry.domainLookupEnd - entry.domainLookupStart,
            tcp: entry.connectEnd - entry.connectStart,
            ttfb: entry.responseStart - entry.requestStart,
            download: entry.responseEnd - entry.responseStart,
            domInteractive: entry.domInteractive - entry.fetchStart,
            domComplete: entry.domComplete - entry.fetchStart,
            loadComplete: entry.loadEventEnd - entry.fetchStart
          };
        }
      });
      navObserver.observe({type: 'navigation', buffered: true});

      // Observe resource timing
      const resourceObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 1000) {
            console.warn('Slow resource:', entry.name, entry.duration);
          }
        }
      });
      resourceObserver.observe({type: 'resource', buffered: true});

      // Observe long tasks
      const longTaskObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          console.warn('Long task detected:', entry.duration, 'ms');
        }
      });
      longTaskObserver.observe({type: 'longtask', buffered: true});
    }
  }

  getMetrics() {
    return this.metrics;
  }

  sendMetrics() {
    fetch('/api/performance', {
      method: 'POST',
      body: JSON.stringify(this.metrics),
      headers: {'Content-Type': 'application/json'}
    });
  }
}

// Initialize
const monitor = new PerformanceMonitor();

// Send metrics on page unload
window.addEventListener('beforeunload', () => {
  monitor.sendMetrics();
});
```

---

## 4. Implementation

### Step 1: Setup Lighthouse CI

```bash
# Install
npm install -g @lhci/cli

# Initialize
lhci wizard

# Create config
cat > lighthouserc.js << 'EOF'
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 5
    },
    assert: {
      assertions: {
        'categories:performance': ['error', {minScore: 0.9}],
        'first-contentful-paint': ['error', {maxNumericValue: 2000}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}]
      }
    }
  }
};
EOF
```

---

### Step 2: Add Web Vitals Monitoring

```javascript
// src/utils/performance.js
import {onCLS, onFID, onLCP, onFCP, onTTFB} from 'web-vitals';

export function initPerformanceMonitoring() {
  const sendToAnalytics = (metric) => {
    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(metric.name, metric.value, metric.rating);
    }

    // Send to analytics in production
    if (process.env.NODE_ENV === 'production') {
      fetch('/api/analytics/vitals', {
        method: 'POST',
        body: JSON.stringify(metric),
        headers: {'Content-Type': 'application/json'},
        keepalive: true
      });
    }
  };

  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onLCP(sendToAnalytics);
  onFCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}
```

---

### Step 3: Create Performance Dashboard

```javascript
// backend/routes/performance.js
const express = require('express');
const router = express.Router();

// Store metrics (use database in production)
const metrics = [];

// Receive metrics
router.post('/api/analytics/vitals', (req, res) => {
  const metric = req.body;
  metrics.push({
    ...metric,
    timestamp: Date.now(),
    userAgent: req.headers['user-agent']
  });
  res.status(200).send('OK');
});

// Get metrics summary
router.get('/api/performance/summary', (req, res) => {
  const summary = {
    lcp: calculatePercentile(metrics.filter(m => m.name === 'LCP'), 75),
    fid: calculatePercentile(metrics.filter(m => m.name === 'FID'), 75),
    cls: calculatePercentile(metrics.filter(m => m.name === 'CLS'), 75),
    fcp: calculatePercentile(metrics.filter(m => m.name === 'FCP'), 75),
    ttfb: calculatePercentile(metrics.filter(m => m.name === 'TTFB'), 75)
  };
  res.json(summary);
});

function calculatePercentile(data, percentile) {
  if (data.length === 0) return null;
  const sorted = data.map(d => d.value).sort((a, b) => a - b);
  const index = Math.ceil((percentile / 100) * sorted.length) - 1;
  return sorted[index];
}

module.exports = router;
```

---

## 5. Performance Budgets

### What are Performance Budgets?

Limits on metrics that affect site performance:
- Maximum page weight
- Maximum number of requests
- Maximum JavaScript size
- Maximum image size
- Maximum time to interactive

### Setting Budgets

```javascript
// performance-budget.json
{
  "budgets": [
    {
      "resourceSizes": [
        {
          "resourceType": "script",
          "budget": 300
        },
        {
          "resourceType": "image",
          "budget": 500
        },
        {
          "resourceType": "total",
          "budget": 1000
        }
      ],
      "resourceCounts": [
        {
          "resourceType": "third-party",
          "budget": 10
        },
        {
          "resourceType": "total",
          "budget": 50
        }
      ],
      "timings": [
        {
          "metric": "interactive",
          "budget": 3000
        },
        {
          "metric": "first-contentful-paint",
          "budget": 2000
        }
      ]
    }
  ]
}
```

---

### Webpack Bundle Analyzer

```bash
npm install --save-dev webpack-bundle-analyzer
```

```javascript
// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
      reportFilename: 'bundle-report.html'
    })
  ]
};
```

---

## 6. Automated Gates

### CI/CD Integration

```yaml
# .github/workflows/performance.yml
name: Performance Check

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Start server
        run: npm start &
        
      - name: Wait for server
        run: npx wait-on http://localhost:3000
      
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
      
      - name: Check performance budgets
        run: npm run check-budgets
```

---

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Check bundle size
npm run check-bundle-size

# Run Lighthouse (quick check)
npm run lighthouse:quick
```

---

## 7. Reporting

### Daily Performance Report

```javascript
// scripts/generate-performance-report.js
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function generateReport() {
  const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
  const options = {
    logLevel: 'info',
    output: 'html',
    port: chrome.port
  };
  
  const runnerResult = await lighthouse('http://localhost:3000', options);
  
  // Generate report
  const report = {
    date: new Date().toISOString(),
    performance: runnerResult.lhr.categories.performance.score * 100,
    accessibility: runnerResult.lhr.categories.accessibility.score * 100,
    bestPractices: runnerResult.lhr.categories['best-practices'].score * 100,
    seo: runnerResult.lhr.categories.seo.score * 100,
    metrics: {
      fcp: runnerResult.lhr.audits['first-contentful-paint'].numericValue,
      lcp: runnerResult.lhr.audits['largest-contentful-paint'].numericValue,
      cls: runnerResult.lhr.audits['cumulative-layout-shift'].numericValue,
      tbt: runnerResult.lhr.audits['total-blocking-time'].numericValue,
      tti: runnerResult.lhr.audits['interactive'].numericValue
    }
  };
  
  // Save report
  fs.writeFileSync(
    `reports/performance-${Date.now()}.json`,
    JSON.stringify(report, null, 2)
  );
  
  await chrome.kill();
  return report;
}

generateReport().then(report => {
  console.log('Performance Report:', report);
});
```

---

## 8. Best Practices

### DO ✅

1. **Monitor continuously** - Not just once
2. **Set realistic budgets** - Based on your users
3. **Test on real devices** - Not just desktop
4. **Track trends** - Not just snapshots
5. **Optimize images** - Use WebP, lazy loading
6. **Code splitting** - Load only what's needed
7. **Use CDN** - For static assets
8. **Compress assets** - Gzip/Brotli
9. **Minimize JavaScript** - Remove unused code
10. **Cache aggressively** - With proper invalidation

### DON'T ❌

1. **Don't ignore mobile** - Most traffic is mobile
2. **Don't test only on fast networks** - Simulate 3G
3. **Don't skip accessibility** - It affects performance
4. **Don't load everything upfront** - Lazy load
5. **Don't use large libraries** - For small features
6. **Don't block rendering** - Defer non-critical JS
7. **Don't forget caching** - Use service workers
8. **Don't ignore third-party scripts** - They slow you down
9. **Don't skip compression** - Always compress
10. **Don't set unrealistic budgets** - Be practical

---

## 🎯 Integration with Our System

### Phase 4: Testing
- Run Lighthouse CI
- Check Web Vitals
- Verify performance budgets
- Generate performance report

### Phase 6: Deployment
- Setup continuous monitoring
- Configure alerts
- Enable real-user monitoring (RUM)
- Track performance trends

### Checkpoints
- ✅ Lighthouse score > 90
- ✅ LCP < 2.5s
- ✅ FID < 100ms
- ✅ CLS < 0.1
- ✅ Bundle size within budget
- ✅ No performance regressions

---

## 📚 Resources

- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Performance Budgets](https://web.dev/performance-budgets-101/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-17  
**Version:** 1.0

