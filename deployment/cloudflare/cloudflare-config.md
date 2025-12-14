# Cloudflare Configuration for Store ERP

**Version:** 2.0  
**Last Updated:** 2025-12-13

---

## Overview

This document describes the recommended Cloudflare configuration for Store ERP to ensure optimal performance, security, and reliability.

---

## DNS Configuration

### A Records
```
Type: A
Name: @
Content: YOUR_SERVER_IP
Proxy: Enabled (Orange Cloud)
TTL: Auto

Type: A
Name: www
Content: YOUR_SERVER_IP
Proxy: Enabled (Orange Cloud)
TTL: Auto

Type: A
Name: admin
Content: YOUR_SERVER_IP
Proxy: Enabled (Orange Cloud)
TTL: Auto
```

### CNAME Records (if using subdomains)
```
Type: CNAME
Name: api
Content: store-erp.example.com
Proxy: Enabled (Orange Cloud)
TTL: Auto
```

---

## SSL/TLS Configuration

### SSL/TLS Encryption Mode
**Recommended:** Full (Strict)

**Settings:**
- Go to SSL/TLS → Overview
- Select "Full (strict)"
- This ensures end-to-end encryption

### Edge Certificates
**Recommended Settings:**
- Always Use HTTPS: **ON**
- HTTP Strict Transport Security (HSTS): **Enabled**
  - Max Age: 6 months (15768000 seconds)
  - Include subdomains: **ON**
  - Preload: **ON**
  - No-Sniff Header: **ON**
- Minimum TLS Version: **TLS 1.2**
- Opportunistic Encryption: **ON**
- TLS 1.3: **ON**
- Automatic HTTPS Rewrites: **ON**
- Certificate Transparency Monitoring: **ON**

### Origin Server
**Recommended:**
- Use Cloudflare Origin CA Certificate
- Generate certificate in SSL/TLS → Origin Server
- Install on your Nginx server
- Validity: 15 years

---

## Firewall Configuration

### Firewall Rules

#### Rule 1: Block Bad Bots
```
Field: User Agent
Operator: contains
Value: (curl|wget|python|scrapy|bot)
Action: Block
```

#### Rule 2: Rate Limit Login
```
Field: URI Path
Operator: equals
Value: /api/auth/login
Rate: 5 requests per minute
Action: Challenge (CAPTCHA)
```

#### Rule 3: Geo-Blocking (Optional)
```
Field: Country
Operator: not in
Value: [Your Allowed Countries]
Action: Block
```

#### Rule 4: Protect Admin Panel
```
Field: Hostname
Operator: equals
Value: admin.store-erp.example.com
AND
Field: IP Address
Operator: not in
Value: [Your Whitelisted IPs]
Action: Challenge (CAPTCHA)
```

### Security Level
**Recommended:** Medium

**Settings:**
- Go to Security → Settings
- Security Level: Medium
- Challenge Passage: 30 minutes

### Bot Fight Mode
**Recommended:** ON

**Settings:**
- Go to Security → Bots
- Bot Fight Mode: **ON**
- Super Bot Fight Mode: **ON** (if available on your plan)

---

## Speed Configuration

### Auto Minify
**Recommended Settings:**
- JavaScript: **ON**
- CSS: **ON**
- HTML: **ON**

**Location:** Speed → Optimization → Auto Minify

### Brotli Compression
**Recommended:** ON

**Location:** Speed → Optimization → Brotli

### Rocket Loader
**Recommended:** OFF (for React apps)

**Reason:** Can interfere with React hydration

### Early Hints
**Recommended:** ON

**Location:** Speed → Optimization → Early Hints

---

## Caching Configuration

### Caching Level
**Recommended:** Standard

**Settings:**
- Go to Caching → Configuration
- Caching Level: Standard
- Browser Cache TTL: 4 hours

### Page Rules

#### Rule 1: Cache Static Assets
```
URL: *store-erp.example.com/*.{js,css,jpg,jpeg,png,gif,ico,svg,woff,woff2,ttf,eot}
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 1 month
```

#### Rule 2: Bypass Cache for API
```
URL: *store-erp.example.com/api/*
Settings:
  - Cache Level: Bypass
```

#### Rule 3: Cache HTML (with short TTL)
```
URL: *store-erp.example.com/*.html
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 2 hours
  - Browser Cache TTL: 30 minutes
```

---

## Network Configuration

### HTTP/2
**Recommended:** ON (Enabled by default)

### HTTP/3 (QUIC)
**Recommended:** ON

**Location:** Network → HTTP/3

### WebSockets
**Recommended:** ON

**Location:** Network → WebSockets

### IPv6 Compatibility
**Recommended:** ON

**Location:** Network → IPv6 Compatibility

### gRPC
**Recommended:** OFF (not needed for this app)

---

## Scrape Shield

### Email Address Obfuscation
**Recommended:** ON

### Server-side Excludes
**Recommended:** ON

### Hotlink Protection
**Recommended:** ON

**Location:** Scrape Shield

---

## Page Shield (if available)

### Script Monitor
**Recommended:** ON

**Location:** Security → Page Shield

**Purpose:** Detect malicious scripts and third-party code

---

## Workers (Optional - Advanced)

### Use Case 1: API Rate Limiting
```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Rate limiting for API endpoints
  if (url.pathname.startsWith('/api/')) {
    const clientIP = request.headers.get('CF-Connecting-IP')
    // Implement rate limiting logic here
  }
  
  return fetch(request)
}
```

### Use Case 2: A/B Testing
```javascript
// Implement A/B testing for UI changes
```

---

## Analytics & Monitoring

### Web Analytics
**Recommended:** ON

**Location:** Analytics → Web Analytics

**Features:**
- Page views
- Unique visitors
- Top pages
- Referrers
- Countries

### Security Analytics
**Recommended:** Monitor regularly

**Location:** Security → Analytics

**Metrics:**
- Threats blocked
- Challenge solve rate
- Firewall events

---

## E2E Encryption Setup

### Step 1: Generate Origin Certificate
1. Go to SSL/TLS → Origin Server
2. Click "Create Certificate"
3. Select "Let Cloudflare generate a private key and a CSR"
4. Choose validity: 15 years
5. Click "Create"
6. Save both certificate and private key

### Step 2: Install on Nginx
```bash
# Save certificate
sudo nano /etc/ssl/certs/cloudflare-origin.pem
# Paste certificate content

# Save private key
sudo nano /etc/ssl/private/cloudflare-origin.key
# Paste private key content

# Set permissions
sudo chmod 644 /etc/ssl/certs/cloudflare-origin.pem
sudo chmod 600 /etc/ssl/private/cloudflare-origin.key
```

### Step 3: Update Nginx Configuration
```nginx
ssl_certificate /etc/ssl/certs/cloudflare-origin.pem;
ssl_certificate_key /etc/ssl/private/cloudflare-origin.key;
```

### Step 4: Set SSL Mode to Full (Strict)
1. Go to SSL/TLS → Overview
2. Select "Full (strict)"

---

## Security Recommendations

### 1. Enable DNSSEC
**Location:** DNS → Settings → DNSSEC

**Steps:**
1. Enable DNSSEC in Cloudflare
2. Add DS record to your domain registrar

### 2. Enable Always Use HTTPS
**Location:** SSL/TLS → Edge Certificates

### 3. Enable Authenticated Origin Pulls
**Location:** SSL/TLS → Origin Server → Authenticated Origin Pulls

**Purpose:** Ensures requests to your origin come from Cloudflare

### 4. Configure WAF (Web Application Firewall)
**Location:** Security → WAF

**Recommended Rulesets:**
- Cloudflare Managed Ruleset: **ON**
- OWASP Core Ruleset: **ON**
- Cloudflare Specials: **ON**

### 5. Enable DDoS Protection
**Location:** Security → DDoS

**Settings:**
- HTTP DDoS Attack Protection: **ON**
- Advanced DDoS Protection: **ON** (if available)

---

## Performance Optimization

### 1. Enable Argo Smart Routing (Paid)
**Location:** Traffic → Argo

**Benefits:**
- Faster routing
- Reduced latency
- Better performance

### 2. Enable Tiered Cache (Paid)
**Location:** Caching → Tiered Cache

**Benefits:**
- Better cache hit ratio
- Reduced origin load

### 3. Enable Image Optimization (Paid)
**Location:** Speed → Optimization → Image Optimization

**Features:**
- Polish: Lossless or Lossy
- WebP: ON
- Mirage: ON (lazy loading)

---

## Monitoring & Alerts

### 1. Set Up Notifications
**Location:** Notifications

**Recommended Alerts:**
- SSL/TLS certificate expiration
- DDoS attack detected
- High error rate (5xx)
- Origin unreachable

### 2. Enable Logs (Enterprise)
**Location:** Analytics → Logs

**Use:** Send logs to external service (e.g., Splunk, Datadog)

---

## Testing E2E Encryption

### Test SSL Configuration
```bash
# Test SSL/TLS
curl -I https://store-erp.example.com

# Check SSL certificate
openssl s_client -connect store-erp.example.com:443 -servername store-erp.example.com

# Test HTTP/2
curl -I --http2 https://store-erp.example.com
```

### Verify Cloudflare Headers
```bash
curl -I https://store-erp.example.com | grep -i cf-
```

**Expected Headers:**
- `CF-Ray`: Unique request ID
- `CF-Cache-Status`: HIT/MISS/DYNAMIC
- `CF-Connecting-IP`: Client IP

---

## Troubleshooting

### Issue 1: 525 SSL Handshake Failed
**Solution:** Check origin certificate and ensure SSL mode is "Full (strict)"

### Issue 2: 526 Invalid SSL Certificate
**Solution:** Ensure origin certificate is valid and not expired

### Issue 3: 520 Web Server Returned Unknown Error
**Solution:** Check origin server logs and Nginx configuration

### Issue 4: High Cache Miss Rate
**Solution:** Review cache rules and adjust TTL

---

## Best Practices

1. ✅ Always use "Full (strict)" SSL mode
2. ✅ Enable HSTS with preload
3. ✅ Use Cloudflare Origin CA certificates
4. ✅ Enable Bot Fight Mode
5. ✅ Configure appropriate page rules
6. ✅ Monitor analytics regularly
7. ✅ Set up notifications for critical events
8. ✅ Use firewall rules to block malicious traffic
9. ✅ Enable DDoS protection
10. ✅ Regularly review security settings

---

## Maintenance Checklist

### Weekly
- [ ] Review security analytics
- [ ] Check for blocked threats
- [ ] Monitor error rates

### Monthly
- [ ] Review firewall rules
- [ ] Update page rules if needed
- [ ] Check SSL certificate expiration
- [ ] Review cache hit ratio

### Quarterly
- [ ] Audit security settings
- [ ] Review and update firewall rules
- [ ] Test disaster recovery
- [ ] Update documentation

---

## Resources

- **Cloudflare Dashboard:** https://dash.cloudflare.com/
- **Cloudflare Docs:** https://developers.cloudflare.com/
- **SSL Labs Test:** https://www.ssllabs.com/ssltest/
- **Security Headers Test:** https://securityheaders.com/

---

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Maintained By:** DevOps Team
