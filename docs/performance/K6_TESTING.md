# K6 Performance Testing

**Last Updated:** 2025-11-06  
**Status:** ✅ Enhanced (T22 Complete)

---

## Overview

This document describes the K6 performance testing framework for the Store ERP system.

### Test Suites

We have 4 comprehensive K6 test suites:

1. **Auth Flow** (`k6_login.js`) - Authentication and basic endpoints
2. **Inventory** (`k6_inventory.js`) - Inventory management endpoints
3. **Invoices** (`k6_invoices.js`) - Invoice management endpoints
4. **Full Suite** (`k6_full_suite.js`) - Complete API test coverage

---

## Quick Start

### Local Testing

**1. Start the backend server:**
```bash
cd backend
python app.py
```

**2. Run a specific test:**
```bash
# Auth flow test
k6 run scripts/perf/k6_login.js

# Inventory test
k6 run scripts/perf/k6_inventory.js

# Invoices test
k6 run scripts/perf/k6_invoices.js

# Full suite test
k6 run scripts/perf/k6_full_suite.js
```

**3. Run with custom parameters:**
```bash
# Set environment variables
export BASE_URL=http://localhost:5001
export USERS=50
export DURATION=2m
export RAMP_UP=30s

# Run test
k6 run scripts/perf/k6_login.js
```

---

## Test Suites Details

### 1. Auth Flow Test (`k6_login.js`)

**Purpose:** Test authentication and basic API endpoints

**Endpoints Tested:**
- `GET /health` - Health check
- `POST /api/auth/login` - User login
- `GET /api/products` - Products list (authenticated)
- `GET /api/categories` - Categories list (cached)

**Performance Thresholds:**
- p95 response time < 500ms
- Error rate < 10%
- Health check < 100ms
- Login < 500ms
- Products < 300ms
- Categories < 200ms

**Default Configuration:**
- Users: 10
- Duration: 30s
- Ramp-up: 10s

**Usage:**
```bash
k6 run scripts/perf/k6_login.js
```

---

### 2. Inventory Test (`k6_inventory.js`)

**Purpose:** Test inventory management endpoints

**Endpoints Tested:**
- `GET /api/inventory?page=1&per_page=20` - List inventory
- `GET /api/inventory/1` - Get item details
- `GET /api/inventory/search?q=product` - Search inventory
- `GET /api/inventory/low-stock?threshold=10` - Low stock items
- `GET /api/inventory/stats` - Inventory statistics

**Performance Thresholds:**
- p95 response time < 800ms
- Error rate < 5%
- List inventory < 500ms
- Item details < 300ms
- Search < 600ms

**Default Configuration:**
- Users: 20
- Duration: 60s
- Ramp-up: 10s

**Usage:**
```bash
k6 run scripts/perf/k6_inventory.js
```

---

### 3. Invoices Test (`k6_invoices.js`)

**Purpose:** Test invoice management endpoints

**Endpoints Tested:**
- `GET /api/invoices?page=1&per_page=20&status=paid` - List invoices
- `GET /api/invoices/1` - Get invoice details
- `GET /api/invoices/search?q=customer` - Search invoices
- `GET /api/invoices?status=pending` - Pending invoices
- `GET /api/invoices/stats` - Invoice statistics
- `GET /api/invoices/overdue` - Overdue invoices

**Performance Thresholds:**
- p95 response time < 1000ms
- Error rate < 5%
- List invoices < 600ms
- Invoice details < 400ms
- Search < 800ms
- Statistics < 500ms

**Default Configuration:**
- Users: 15
- Duration: 60s
- Ramp-up: 10s

**Usage:**
```bash
k6 run scripts/perf/k6_invoices.js
```

---

### 4. Full Suite Test (`k6_full_suite.js`)

**Purpose:** Comprehensive test of all API endpoints

**Test Groups:**
1. **Health & System** - Health checks
2. **Products** - Product management
3. **Inventory** - Inventory management
4. **Invoices** - Invoice management

**Performance Thresholds:**
- p95 response time < 1000ms
- p99 response time < 2000ms
- Error rate < 5%
- Auth < 500ms
- Products < 400ms
- Inventory < 600ms
- Invoices < 800ms

**Load Profile:**
- Stage 1: Ramp up to 10 users (30s)
- Stage 2: Ramp up to 20 users (1m)
- Stage 3: Stay at 20 users (2m)
- Stage 4: Ramp down to 0 users (30s)

**Usage:**
```bash
k6 run scripts/perf/k6_full_suite.js
```

---

## CI/CD Integration

### GitHub Actions Workflow

The K6 tests run automatically on:
- Push to `main` branch (scripts/perf/** changes)
- Pull requests to `main` (backend/** changes)
- Manual workflow dispatch

**Workflow:** `.github/workflows/perf_k6.yml`

**Matrix Strategy:**
- Runs all 4 test suites in parallel
- Each suite has custom configuration
- Artifacts uploaded for each test

**Artifacts:**
- K6 summary JSON files
- Backend logs (on failure)

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Backend server URL | `http://127.0.0.1:5001` |
| `USERS` | Number of virtual users | Test-specific |
| `DURATION` | Test duration | Test-specific |
| `RAMP_UP` | Ramp-up duration | `10s` |

---

## Performance Baselines

### Expected Performance (Local Development)

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| Health Check | 10ms | 50ms | 100ms |
| Login | 100ms | 300ms | 500ms |
| Products List | 50ms | 200ms | 400ms |
| Inventory List | 100ms | 400ms | 600ms |
| Invoice List | 150ms | 500ms | 800ms |
| Search | 200ms | 600ms | 1000ms |

### Expected Performance (Production)

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| Health Check | 20ms | 100ms | 200ms |
| Login | 150ms | 400ms | 600ms |
| Products List | 100ms | 300ms | 500ms |
| Inventory List | 150ms | 500ms | 800ms |
| Invoice List | 200ms | 600ms | 1000ms |
| Search | 300ms | 800ms | 1200ms |

---

## Interpreting Results

### Success Criteria

✅ **PASS** if:
- All thresholds met
- Error rate < 5%
- No critical failures

⚠️ **WARNING** if:
- Some thresholds exceeded
- Error rate 5-10%
- Performance degradation detected

❌ **FAIL** if:
- Multiple thresholds exceeded
- Error rate > 10%
- Critical failures

### Key Metrics

**Response Time:**
- p50 (median) - Typical user experience
- p95 - 95% of users experience
- p99 - Worst-case scenario

**Error Rate:**
- HTTP failures
- Custom error checks
- Threshold violations

**Throughput:**
- Requests per second
- Data transferred
- Virtual users

---

## Troubleshooting

### Common Issues

**1. High Error Rate**
- Check backend logs
- Verify database connection
- Check authentication

**2. Slow Response Times**
- Check database queries
- Review caching strategy
- Check server resources

**3. Test Failures**
- Verify backend is running
- Check test data exists
- Review threshold values

---

## Next Steps

### Planned Enhancements

1. **Performance Regression Testing**
   - Track performance over time
   - Alert on degradation
   - Historical comparison

2. **Load Testing Scenarios**
   - Peak load simulation
   - Stress testing
   - Endurance testing

3. **Performance Monitoring**
   - Real-time dashboards
   - Grafana integration
   - Alert system

4. **Optimization**
   - Database query optimization
   - Caching improvements
   - API response optimization

---

## Resources

- [K6 Documentation](https://k6.io/docs/)
- [K6 Best Practices](https://k6.io/docs/testing-guides/test-types/)
- [Performance Testing Guide](https://k6.io/docs/testing-guides/)

---

**For questions or issues, contact the development team.**

