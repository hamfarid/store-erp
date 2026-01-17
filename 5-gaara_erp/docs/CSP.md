# Content Security Policy (CSP)

**Last Updated:** 2025-11-04  
**Owner:** Security Team  
**Status:** ✅ Current

---

## Overview

Content Security Policy (CSP) implementation to prevent XSS, clickjacking, and injection attacks.

## CSP Headers

### Development

```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-{random}' https://cdn.jsdelivr.net;
  style-src 'self' 'nonce-{random}' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' http://localhost:5001 http://localhost:5173;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
  upgrade-insecure-requests;
```

### Production

```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-{random}' https://cdn.example.com;
  style-src 'self' 'nonce-{random}' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
  upgrade-insecure-requests;
  block-all-mixed-content;
```

## Directives

| Directive | Value | Purpose |
|-----------|-------|---------|
| `default-src` | `'self'` | Default for all content |
| `script-src` | `'self' 'nonce-{random}'` | JavaScript sources |
| `style-src` | `'self' 'nonce-{random}'` | CSS sources |
| `font-src` | `'self' https://fonts.gstatic.com` | Font sources |
| `img-src` | `'self' data: https:` | Image sources |
| `connect-src` | `'self' https://api.example.com` | XHR, WebSocket, fetch |
| `frame-ancestors` | `'none'` | Prevent clickjacking |
| `base-uri` | `'self'` | Base URL for relative URLs |
| `form-action` | `'self'` | Form submission targets |
| `upgrade-insecure-requests` | - | Upgrade HTTP to HTTPS |
| `block-all-mixed-content` | - | Block HTTP content in HTTPS |

## Nonce Implementation

### Backend (Flask)

```python
import secrets
import base64

def generate_nonce():
    """Generate random nonce for CSP"""
    return base64.b64encode(secrets.token_bytes(16)).decode('utf-8')

@app.before_request
def set_csp_nonce():
    """Set CSP nonce for each request"""
    g.csp_nonce = generate_nonce()

@app.after_request
def set_csp_header(response):
    """Add CSP header with nonce"""
    nonce = g.get('csp_nonce', '')
    csp = f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; ..."
    response.headers['Content-Security-Policy'] = csp
    return response
```

### Frontend (React)

```javascript
// Get nonce from meta tag or window object
const nonce = document.querySelector('meta[property="csp-nonce"]')?.content
  || window.__CSP_NONCE__;

// Use in inline scripts
<script nonce={nonce}>
  console.log('This script is allowed by CSP');
</script>

// Use in inline styles
<style nonce={nonce}>
  body { color: blue; }
</style>
```

## CSP Violations

### Monitoring

```javascript
// Listen for CSP violations
document.addEventListener('securitypolicyviolation', (e) => {
  console.error('CSP Violation:', {
    blockedURI: e.blockedURI,
    violatedDirective: e.violatedDirective,
    originalPolicy: e.originalPolicy,
    sourceFile: e.sourceFile,
    lineNumber: e.lineNumber,
  });
  
  // Send to monitoring service
  fetch('/api/security/csp-violation', {
    method: 'POST',
    body: JSON.stringify({
      blockedURI: e.blockedURI,
      violatedDirective: e.violatedDirective,
      timestamp: new Date().toISOString(),
    }),
  });
});
```

### Report-Only Mode

```
Content-Security-Policy-Report-Only: 
  default-src 'self';
  report-uri https://example.com/csp-report;
```

## Common Issues & Solutions

### Issue: Inline Styles Not Working

**Problem:** CSP blocks inline styles

**Solution:** Use nonce or move to external stylesheet

```javascript
// ❌ Blocked
<div style={{ color: 'red' }}>Text</div>

// ✅ Allowed with nonce
<div style={{ color: 'red' }} nonce={nonce}>Text</div>

// ✅ Allowed with class
<div className="text-red">Text</div>
```

### Issue: External Scripts Blocked

**Problem:** CSP blocks external scripts

**Solution:** Add to `script-src` directive

```
script-src 'self' https://cdn.example.com;
```

### Issue: Fonts Not Loading

**Problem:** CSP blocks font sources

**Solution:** Add to `font-src` directive

```
font-src 'self' https://fonts.gstatic.com;
```

### Issue: Images Not Loading

**Problem:** CSP blocks image sources

**Solution:** Add to `img-src` directive

```
img-src 'self' data: https:;
```

## Testing

### Manual Testing

```bash
# Check CSP headers
curl -I https://api.example.com

# Look for Content-Security-Policy header
```

### Automated Testing

```javascript
// Test CSP in CI/CD
describe('CSP Headers', () => {
  it('should have CSP header', async () => {
    const response = await fetch('https://api.example.com');
    expect(response.headers.get('Content-Security-Policy')).toBeDefined();
  });
  
  it('should have nonce in CSP', async () => {
    const response = await fetch('https://api.example.com');
    const csp = response.headers.get('Content-Security-Policy');
    expect(csp).toMatch(/nonce-/);
  });
});
```

## Best Practices

1. **Use nonces** for inline scripts/styles
2. **Avoid `unsafe-inline`** and `unsafe-eval`
3. **Use `report-uri`** to monitor violations
4. **Start with report-only** mode
5. **Gradually tighten** CSP over time
6. **Test thoroughly** before enforcing
7. **Monitor violations** in production
8. **Update regularly** as dependencies change

## CSP Levels

### Level 1 (Permissive)

```
default-src 'self' 'unsafe-inline' 'unsafe-eval';
```

### Level 2 (Moderate)

```
default-src 'self';
script-src 'self' 'unsafe-inline';
style-src 'self' 'unsafe-inline';
```

### Level 3 (Strict)

```
default-src 'self';
script-src 'self' 'nonce-{random}';
style-src 'self' 'nonce-{random}';
```

## Compliance

- **OWASP:** CSP recommended for XSS prevention
- **GDPR:** Helps protect user data
- **PCI DSS:** Required for payment processing
- **SOC 2:** Security control

---

**Next Steps:**

- [ ] Implement CSP nonce generation
- [ ] Add CSP violation monitoring
- [ ] Test CSP in all browsers
- [ ] Document CSP exceptions
