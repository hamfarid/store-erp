// Simple end-to-end CSRF verification script (Node/ESM)
// - Primes /api/csrf-token to receive cookies
// - Posts to /api/temp/auth/login with X-CSRFToken header
// - Prints PASS/FAIL summary

import http from 'http';

const BASE_URL = process.env.BACKEND_BASE_URL || 'http://127.0.0.1:5002';
const url = new URL(BASE_URL);

function request(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, headers: res.headers, data: json });
        } catch {
          resolve({ status: res.statusCode, headers: res.headers, data });
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function main() {
  const result = {
    baseUrl: BASE_URL,
    prime: { ok: false, status: null, csrfTokenPresent: false },
    post: { ok: false, status: null, success: false, message: null },
  };

  try {
    // 1) Prime CSRF
    const prime = await request({
      hostname: url.hostname,
      port: url.port || 80,
      path: '/api/csrf-token',
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    result.prime.status = prime.status;

    const setCookie = prime.headers['set-cookie'] || [];
    const xsrfMatch = setCookie.find(c => c.startsWith('XSRF-TOKEN='));
    const sessionMatch = setCookie.find(c => c.startsWith('session='));

    let csrfToken = prime.data?.csrfToken;
    if (!csrfToken && xsrfMatch) {
      csrfToken = xsrfMatch.split(';')[0].split('=')[1];
    }

    result.prime.csrfTokenPresent = Boolean(csrfToken);
    result.prime.ok = prime.status === 200 && Boolean(csrfToken);

    if (!result.prime.ok) {
      throw new Error(`Failed to prime CSRF (status=${prime.status})`);
    }

    // Build Cookie header from set-cookie responses
    const cookieHeader = setCookie.map(c => c.split(';')[0]).join('; ');

    // 2) POST with CSRF token
    const payload = JSON.stringify({ username: 'admin', password: 'admin' });
    const post = await request({
      hostname: url.hostname,
      port: url.port || 80,
      path: '/api/temp/auth/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'X-CSRFToken': csrfToken,
        'Cookie': cookieHeader,
        'Accept': 'application/json',
      },
    }, payload);

    result.post.status = post.status;
    result.post.success = Boolean(post.data?.success);
    result.post.message = post.data?.message || null;
    result.post.errorData = post.status >= 400 ? post.data : null;
    result.post.ok = post.status === 200 && result.post.success === true;

    const pass = result.prime.ok && result.post.ok;

    const summary = {
      baseUrl: result.baseUrl,
      csrfPrimed: result.prime.ok,
      csrfTokenPresent: result.prime.csrfTokenPresent,
      loginPost: {
        ok: result.post.ok,
        status: result.post.status,
        success: result.post.success,
        message: result.post.message,
        errorData: result.post.errorData,
      },
      verdict: pass ? 'PASS' : 'FAIL',
    };

    console.log(JSON.stringify(summary, null, 2));
    process.exit(pass ? 0 : 2);
  } catch (err) {
    const msg = err?.response?.data || err?.message || String(err);
    console.error(JSON.stringify({ error: msg, ...result }, null, 2));
    process.exit(2);
  }
}

main();
