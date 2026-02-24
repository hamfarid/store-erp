// K6 Performance Test - Full API Suite
// نص اختبار الأداء - مجموعة API الكاملة

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const authDuration = new Trend('auth_duration');
const productsDuration = new Trend('products_duration');
const inventoryDuration = new Trend('inventory_duration');
const invoicesDuration = new Trend('invoices_duration');
const requestCounter = new Counter('total_requests');

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 20 },   // Ramp up to 20 users
    { duration: '2m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000', 'p(99)<2000'],
    http_req_failed: ['rate<0.05'],
    errors: ['rate<0.05'],
    auth_duration: ['p(95)<500'],
    products_duration: ['p(95)<400'],
    inventory_duration: ['p(95)<600'],
    invoices_duration: ['p(95)<800'],
  },
};

// Helper function to get auth token
function getAuthToken(baseUrl) {
  const loginData = {
    email: 'admin@example.com',
    password: 'admin123'
  };
  
  const response = http.post(`${baseUrl}/api/auth/login`, JSON.stringify(loginData), {
    headers: { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
  });
  
  authDuration.add(response.timings.duration);
  requestCounter.add(1);
  
  if (response.status === 200 || response.status === 201) {
    try {
      const body = JSON.parse(response.body);
      return body.access_token || body.token;
    } catch (e) {
      console.log('Failed to parse login response');
      return null;
    }
  }
  
  return null;
}

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:5001';
  
  // Get authentication token
  const token = getAuthToken(baseUrl);
  
  if (!token) {
    console.log('Failed to get auth token, skipping tests');
    errorRate.add(1);
    return;
  }
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json'
  };
  
  // Group 1: Health & System Endpoints
  group('Health & System', function () {
    let response = http.get(`${baseUrl}/health`, { headers: headers });
    requestCounter.add(1);
    
    check(response, {
      'health check is 200': (r) => r.status === 200,
      'health check < 100ms': (r) => r.timings.duration < 100,
    }) || errorRate.add(1);
    
    sleep(0.3);
  });
  
  // Group 2: Products Endpoints
  group('Products', function () {
    // List products
    let response = http.get(`${baseUrl}/api/products?page=1&per_page=20`, { headers: headers });
    productsDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'products list is 200': (r) => r.status === 200,
      'products list < 400ms': (r) => r.timings.duration < 400,
    }) || errorRate.add(1);
    
    sleep(0.5);
    
    // Get product details
    response = http.get(`${baseUrl}/api/products/1`, { headers: headers });
    productsDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'product detail is 200 or 404': (r) => r.status === 200 || r.status === 404,
      'product detail < 300ms': (r) => r.timings.duration < 300,
    }) || errorRate.add(1);
    
    sleep(0.3);
  });
  
  // Group 3: Inventory Endpoints
  group('Inventory', function () {
    // List inventory
    let response = http.get(`${baseUrl}/api/inventory?page=1&per_page=20`, { headers: headers });
    inventoryDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'inventory list is 200': (r) => r.status === 200,
      'inventory list < 600ms': (r) => r.timings.duration < 600,
    }) || errorRate.add(1);
    
    sleep(0.5);
    
    // Search inventory
    response = http.get(`${baseUrl}/api/inventory/search?q=product`, { headers: headers });
    inventoryDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'inventory search is 200': (r) => r.status === 200,
      'inventory search < 800ms': (r) => r.timings.duration < 800,
    }) || errorRate.add(1);
    
    sleep(0.3);
    
    // Low stock items
    response = http.get(`${baseUrl}/api/inventory/low-stock`, { headers: headers });
    inventoryDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'low stock is 200': (r) => r.status === 200,
      'low stock < 400ms': (r) => r.timings.duration < 400,
    }) || errorRate.add(1);
    
    sleep(0.3);
  });
  
  // Group 4: Invoice Endpoints
  group('Invoices', function () {
    // List invoices
    let response = http.get(`${baseUrl}/api/invoices?page=1&per_page=20`, { headers: headers });
    invoicesDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'invoices list is 200': (r) => r.status === 200,
      'invoices list < 800ms': (r) => r.timings.duration < 800,
    }) || errorRate.add(1);
    
    sleep(0.5);
    
    // Get invoice details
    response = http.get(`${baseUrl}/api/invoices/1`, { headers: headers });
    invoicesDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'invoice detail is 200 or 404': (r) => r.status === 200 || r.status === 404,
      'invoice detail < 500ms': (r) => r.timings.duration < 500,
    }) || errorRate.add(1);
    
    sleep(0.3);
    
    // Invoice statistics
    response = http.get(`${baseUrl}/api/invoices/stats`, { headers: headers });
    invoicesDuration.add(response.timings.duration);
    requestCounter.add(1);
    
    check(response, {
      'invoice stats is 200': (r) => r.status === 200,
      'invoice stats < 600ms': (r) => r.timings.duration < 600,
    }) || errorRate.add(1);
    
    sleep(0.3);
  });
  
  sleep(1);
}

export function handleSummary(data) {
  const successRate = ((1 - data.metrics.http_req_failed.rate) * 100).toFixed(2);
  const avgDuration = data.metrics.iteration_duration.avg.toFixed(2);
  const p95Duration = data.metrics.http_req_duration['p(95)'].toFixed(2);
  const p99Duration = data.metrics.http_req_duration['p(99)'].toFixed(2);
  const totalRequests = data.metrics.http_reqs.count;
  const errorCount = data.metrics.errors ? data.metrics.errors.count : 0;
  
  return {
    'k6-full-suite-summary.json': JSON.stringify(data, null, 2),
    stdout: `
=== K6 Full Suite Performance Test Summary ===
Duration (avg): ${avgDuration}ms
Duration (p95): ${p95Duration}ms
Duration (p99): ${p99Duration}ms
Success Rate: ${successRate}%
Total Requests: ${totalRequests}
Errors: ${errorCount}
VUs (max): ${data.metrics.vus_max.value}

Endpoint Group Performance:
- Auth: ${data.metrics.auth_duration ? data.metrics.auth_duration.avg.toFixed(2) : 'N/A'}ms avg
- Products: ${data.metrics.products_duration ? data.metrics.products_duration.avg.toFixed(2) : 'N/A'}ms avg
- Inventory: ${data.metrics.inventory_duration ? data.metrics.inventory_duration.avg.toFixed(2) : 'N/A'}ms avg
- Invoices: ${data.metrics.invoices_duration ? data.metrics.invoices_duration.avg.toFixed(2) : 'N/A'}ms avg

Performance Thresholds:
- p95 < 1000ms: ${p95Duration < 1000 ? '✅ PASS' : '❌ FAIL'}
- p99 < 2000ms: ${p99Duration < 2000 ? '✅ PASS' : '❌ FAIL'}
- Error rate < 5%: ${(data.metrics.http_req_failed.rate * 100) < 5 ? '✅ PASS' : '❌ FAIL'}
==============================================
    `,
  };
}

