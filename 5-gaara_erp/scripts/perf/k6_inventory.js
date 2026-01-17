// K6 Performance Test - Inventory Endpoints
// نص اختبار الأداء - نقاط نهاية المخزون

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const inventoryListDuration = new Trend('inventory_list_duration');
const inventoryDetailDuration = new Trend('inventory_detail_duration');
const inventorySearchDuration = new Trend('inventory_search_duration');

export const options = {
  stages: [
    { duration: __ENV.RAMP_UP || '10s', target: parseInt(__ENV.USERS) || 20 },
    { duration: __ENV.DURATION || '60s', target: parseInt(__ENV.USERS) || 20 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],     // 95% of requests must complete below 800ms
    http_req_failed: ['rate<0.05'],       // Error rate must be below 5%
    errors: ['rate<0.05'],                // Custom error rate below 5%
    inventory_list_duration: ['p(95)<500'], // List endpoint < 500ms
    inventory_detail_duration: ['p(95)<300'], // Detail endpoint < 300ms
    inventory_search_duration: ['p(95)<600'], // Search endpoint < 600ms
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
  
  // Test 1: List Inventory Items (with pagination)
  let response = http.get(`${baseUrl}/api/inventory?page=1&per_page=20`, {
    headers: headers,
  });
  
  inventoryListDuration.add(response.timings.duration);
  
  let listCheck = check(response, {
    'inventory list status is 200': (r) => r.status === 200,
    'inventory list response time < 500ms': (r) => r.timings.duration < 500,
    'inventory list has items': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.items) || Array.isArray(body.data) || Array.isArray(body);
      } catch (e) {
        return false;
      }
    },
    'inventory list has pagination': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.total !== undefined || body.pagination !== undefined;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!listCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 2: Get Inventory Item Details
  // Assuming item ID 1 exists (adjust based on your data)
  response = http.get(`${baseUrl}/api/inventory/1`, {
    headers: headers,
  });
  
  inventoryDetailDuration.add(response.timings.duration);
  
  let detailCheck = check(response, {
    'inventory detail status is 200 or 404': (r) => r.status === 200 || r.status === 404,
    'inventory detail response time < 300ms': (r) => r.timings.duration < 300,
    'inventory detail is valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!detailCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 3: Search Inventory
  response = http.get(`${baseUrl}/api/inventory/search?q=product&page=1&per_page=10`, {
    headers: headers,
  });
  
  inventorySearchDuration.add(response.timings.duration);
  
  let searchCheck = check(response, {
    'inventory search status is 200': (r) => r.status === 200,
    'inventory search response time < 600ms': (r) => r.timings.duration < 600,
    'inventory search returns results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.items) || Array.isArray(body.data) || Array.isArray(body);
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!searchCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 4: Get Low Stock Items
  response = http.get(`${baseUrl}/api/inventory/low-stock?threshold=10`, {
    headers: headers,
  });
  
  let lowStockCheck = check(response, {
    'low stock status is 200': (r) => r.status === 200,
    'low stock response time < 400ms': (r) => r.timings.duration < 400,
    'low stock is valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!lowStockCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 5: Get Inventory Statistics
  response = http.get(`${baseUrl}/api/inventory/stats`, {
    headers: headers,
  });
  
  let statsCheck = check(response, {
    'inventory stats status is 200': (r) => r.status === 200,
    'inventory stats response time < 300ms': (r) => r.timings.duration < 300,
    'inventory stats has metrics': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.total_items !== undefined || body.total_value !== undefined;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!statsCheck) {
    errorRate.add(1);
  }
  
  sleep(1);
}

export function handleSummary(data) {
  const successRate = ((1 - data.metrics.http_req_failed.rate) * 100).toFixed(2);
  const avgDuration = data.metrics.iteration_duration.avg.toFixed(2);
  const p95Duration = data.metrics.http_req_duration['p(95)'].toFixed(2);
  const totalRequests = data.metrics.http_reqs.count;
  const errorCount = data.metrics.errors ? data.metrics.errors.count : 0;
  
  return {
    'k6-inventory-summary.json': JSON.stringify(data, null, 2),
    stdout: `
=== K6 Inventory Performance Test Summary ===
Duration (avg): ${avgDuration}ms
Duration (p95): ${p95Duration}ms
Success Rate: ${successRate}%
Total Requests: ${totalRequests}
Errors: ${errorCount}
VUs (max): ${data.metrics.vus_max.value}

Endpoint Performance:
- List Inventory: ${data.metrics.inventory_list_duration ? data.metrics.inventory_list_duration.avg.toFixed(2) : 'N/A'}ms avg
- Item Details: ${data.metrics.inventory_detail_duration ? data.metrics.inventory_detail_duration.avg.toFixed(2) : 'N/A'}ms avg
- Search: ${data.metrics.inventory_search_duration ? data.metrics.inventory_search_duration.avg.toFixed(2) : 'N/A'}ms avg
=============================================
    `,
  };
}

