// K6 Performance Test - Authentication Flow
// نص اختبار الأداء - تدفق المصادقة

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: __ENV.RAMP_UP || '10s', target: parseInt(__ENV.USERS) || 10 },
    { duration: __ENV.DURATION || '30s', target: parseInt(__ENV.USERS) || 10 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate must be below 10%
    errors: ['rate<0.1'],             // Custom error rate below 10%
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:5001';
  
  // Test 1: Health Check
  let response = http.get(`${baseUrl}/health`);
  let healthCheck = check(response, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 100ms': (r) => r.timings.duration < 100,
  });
  
  if (!healthCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
  
  // Test 2: Login Flow
  const loginData = {
    email: 'admin@example.com',
    password: 'admin123'
  };
  
  response = http.post(`${baseUrl}/api/auth/login`, JSON.stringify(loginData), {
    headers: { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
  });
  
  let loginCheck = check(response, {
    'login status is 200 or 201': (r) => r.status === 200 || r.status === 201,
    'login response time < 500ms': (r) => r.timings.duration < 500,
    'login response has token': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.access_token !== undefined || body.token !== undefined;
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!loginCheck) {
    errorRate.add(1);
  }
  
  // Extract token for authenticated requests
  let token = null;
  try {
    const loginBody = JSON.parse(response.body);
    token = loginBody.access_token || loginBody.token;
  } catch (e) {
    console.log('Failed to parse login response');
  }
  
  sleep(0.5);
  
  // Test 3: Authenticated Request (if token available)
  if (token) {
    response = http.get(`${baseUrl}/api/products`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      },
    });
    
    let productsCheck = check(response, {
      'products status is 200': (r) => r.status === 200,
      'products response time < 300ms': (r) => r.timings.duration < 300,
      'products response is valid JSON': (r) => {
        try {
          JSON.parse(r.body);
          return true;
        } catch (e) {
          return false;
        }
      },
    });
    
    if (!productsCheck) {
      errorRate.add(1);
    }
  }
  
  sleep(1);
  
  // Test 4: Categories Endpoint (cached)
  response = http.get(`${baseUrl}/api/categories`, {
    headers: {
      'Accept': 'application/json'
    },
  });
  
  let categoriesCheck = check(response, {
    'categories status is 200': (r) => r.status === 200,
    'categories response time < 200ms': (r) => r.timings.duration < 200,
    'categories response is array': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body) || Array.isArray(body.categories);
      } catch (e) {
        return false;
      }
    },
  });
  
  if (!categoriesCheck) {
    errorRate.add(1);
  }
  
  sleep(0.5);
}

export function handleSummary(data) {
  return {
    'k6-summary.json': JSON.stringify(data, null, 2),
    stdout: `
=== K6 Performance Test Summary ===
Duration: ${data.metrics.iteration_duration.avg.toFixed(2)}ms avg
Success Rate: ${((1 - data.metrics.http_req_failed.rate) * 100).toFixed(2)}%
Requests: ${data.metrics.http_reqs.count}
Errors: ${data.metrics.errors ? data.metrics.errors.count : 0}
VUs: ${data.metrics.vus_max.value}
=====================================
    `,
  };
}
