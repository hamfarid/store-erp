// K6 Performance Test - Invoice Endpoints
// نص اختبار الأداء - نقاط نهاية الفواتير

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const invoiceListDuration = new Trend('invoice_list_duration');
const invoiceDetailDuration = new Trend('invoice_detail_duration');
const invoiceSearchDuration = new Trend('invoice_search_duration');
const invoiceStatsDuration = new Trend('invoice_stats_duration');

export const options = {
  stages: [
    { duration: __ENV.RAMP_UP || '10s', target: parseInt(__ENV.USERS) || 15 },
    { duration: __ENV.DURATION || '60s', target: parseInt(__ENV.USERS) || 15 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],    // 95% of requests must complete below 1000ms
    http_req_failed: ['rate<0.05'],       // Error rate must be below 5%
    errors: ['rate<0.05'],                // Custom error rate below 5%
    invoice_list_duration: ['p(95)<600'], // List endpoint < 600ms
    invoice_detail_duration: ['p(95)<400'], // Detail endpoint < 400ms
    invoice_search_duration: ['p(95)<800'], // Search endpoint < 800ms
    invoice_stats_duration: ['p(95)<500'], // Stats endpoint < 500ms
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
  
  // Test 1: List Invoices (with pagination and filters)
  let response = http.get(`${baseUrl}/api/invoices?page=1&per_page=20&status=paid`, {
    headers: headers,
  });
  
  invoiceListDuration.add(response.timings.duration);
  
  let listCheck = check(response, {
    'invoice list status is 200': (r) => r.status === 200,
    'invoice list response time < 600ms': (r) => r.timings.duration < 600,
    'invoice list has items': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.items) || Array.isArray(body.data) || Array.isArray(body);
      } catch (e) {
        return false;
      }
    },
    'invoice list has pagination': (r) => {
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
  
  // Test 2: Get Invoice Details
  // Assuming invoice ID 1 exists (adjust based on your data)
  response = http.get(`${baseUrl}/api/invoices/1`, {
    headers: headers,
  });
  
  invoiceDetailDuration.add(response.timings.duration);
  
  let detailCheck = check(response, {
    'invoice detail status is 200 or 404': (r) => r.status === 200 || r.status === 404,
    'invoice detail response time < 400ms': (r) => r.timings.duration < 400,
    'invoice detail is valid JSON': (r) => {
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
  
  // Test 3: Search Invoices
  response = http.get(`${baseUrl}/api/invoices/search?q=customer&page=1&per_page=10`, {
    headers: headers,
  });
  
  invoiceSearchDuration.add(response.timings.duration);
  
  let searchCheck = check(response, {
    'invoice search status is 200': (r) => r.status === 200,
    'invoice search response time < 800ms': (r) => r.timings.duration < 800,
    'invoice search returns results': (r) => {
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
  
  // Test 4: Get Pending Invoices
  response = http.get(`${baseUrl}/api/invoices?status=pending&page=1&per_page=10`, {
    headers: headers,
  });
  
  let pendingCheck = check(response, {
    'pending invoices status is 200': (r) => r.status === 200,
    'pending invoices response time < 500ms': (r) => r.timings.duration < 500,
    'pending invoices is valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!pendingCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 5: Get Invoice Statistics
  response = http.get(`${baseUrl}/api/invoices/stats`, {
    headers: headers,
  });
  
  invoiceStatsDuration.add(response.timings.duration);
  
  let statsCheck = check(response, {
    'invoice stats status is 200': (r) => r.status === 200,
    'invoice stats response time < 500ms': (r) => r.timings.duration < 500,
    'invoice stats has metrics': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.total_invoices !== undefined || body.total_amount !== undefined;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!statsCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 6: Get Overdue Invoices
  response = http.get(`${baseUrl}/api/invoices/overdue?page=1&per_page=10`, {
    headers: headers,
  });
  
  let overdueCheck = check(response, {
    'overdue invoices status is 200': (r) => r.status === 200,
    'overdue invoices response time < 600ms': (r) => r.timings.duration < 600,
    'overdue invoices is valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!overdueCheck) {
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
    'k6-invoices-summary.json': JSON.stringify(data, null, 2),
    stdout: `
=== K6 Invoice Performance Test Summary ===
Duration (avg): ${avgDuration}ms
Duration (p95): ${p95Duration}ms
Success Rate: ${successRate}%
Total Requests: ${totalRequests}
Errors: ${errorCount}
VUs (max): ${data.metrics.vus_max.value}

Endpoint Performance:
- List Invoices: ${data.metrics.invoice_list_duration ? data.metrics.invoice_list_duration.avg.toFixed(2) : 'N/A'}ms avg
- Invoice Details: ${data.metrics.invoice_detail_duration ? data.metrics.invoice_detail_duration.avg.toFixed(2) : 'N/A'}ms avg
- Search: ${data.metrics.invoice_search_duration ? data.metrics.invoice_search_duration.avg.toFixed(2) : 'N/A'}ms avg
- Statistics: ${data.metrics.invoice_stats_duration ? data.metrics.invoice_stats_duration.avg.toFixed(2) : 'N/A'}ms avg
============================================
    `,
  };
}

