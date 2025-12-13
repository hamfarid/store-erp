# K6 Load Testing Setup Guide

**Date**: 2025-10-27  
**Purpose**: Step-by-step guide for setting up and running K6 load tests

---

## INSTALLATION

### macOS
```bash
brew install k6
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3232A
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Windows
```bash
choco install k6
```

### Docker
```bash
docker run -i grafana/k6 run - < scripts/perf/k6_login.js
```

### Verify Installation
```bash
k6 version
```

---

## QUICK START

### 1. Start Application
```bash
# Terminal 1: Start backend
cd backend
python -m flask run

# Terminal 2: Start frontend (optional)
cd frontend
npm run dev
```

### 2. Run Basic Load Test
```bash
k6 run scripts/perf/k6_login.js \
  --env BASE_URL=http://localhost:5000 \
  --env USERS=10 \
  --env DURATION=30s
```

### 3. View Results
```
✓ login status is 200
✓ login has access_token
✓ login has refresh_token
✓ login response time < 500ms
✓ refresh status is 200
✓ refresh has new access_token
✓ refresh response time < 300ms
✓ protected endpoint status is 200
✓ logout status is 200

checks.........................: 100% ✓ 900 ✗ 0
data_received..................: 45 kB ✓ 0 B ✗
data_sent.......................: 30 kB ✓ 0 B ✗
http_req_duration..............: avg=250ms p(95)=400ms p(99)=600ms
http_req_failed................: 0.00% ✓ 0 ✗ 300
http_reqs......................: 300 ✓ 0 ✗
iteration_duration.............: avg=5.25s p(95)=5.5s p(99)=5.8s
iterations......................: 10 ✓ 0 ✗
vus............................: 1 ✓ 0 ✗
vus_max........................: 10 ✓ 0 ✗
```

---

## LOAD TEST SCENARIOS

### Scenario 1: Baseline Test
```bash
# 10 users for 30 seconds
k6 run scripts/perf/k6_login.js \
  --env BASE_URL=http://localhost:5000 \
  --env USERS=10 \
  --env DURATION=30s \
  --env RAMP_UP=10s
```

### Scenario 2: Stress Test
```bash
# Gradually increase load
k6 run scripts/perf/k6_login.js \
  --stage 30s:0 \
  --stage 30s:50 \
  --stage 30s:100 \
  --stage 30s:50 \
  --stage 30s:0 \
  --env BASE_URL=http://localhost:5000
```

### Scenario 3: Spike Test
```bash
# Sudden spike in traffic
k6 run scripts/perf/k6_login.js \
  --stage 10s:10 \
  --stage 1s:100 \
  --stage 10s:100 \
  --stage 10s:10 \
  --env BASE_URL=http://localhost:5000
```

### Scenario 4: Soak Test
```bash
# Sustained load for extended period
k6 run scripts/perf/k6_login.js \
  --vus 20 \
  --duration 1h \
  --env BASE_URL=http://localhost:5000
```

### Scenario 5: Ramp Test
```bash
# Gradually increase to peak load
k6 run scripts/perf/k6_login.js \
  --stage 5m:0 \
  --stage 5m:100 \
  --stage 5m:200 \
  --stage 5m:0 \
  --env BASE_URL=http://localhost:5000
```

---

## ADVANCED USAGE

### Custom Thresholds
```bash
k6 run scripts/perf/k6_login.js \
  --threshold 'http_req_duration{staticAsset:yes}<1000' \
  --threshold 'http_req_duration{staticAsset:no}<5000' \
  --threshold 'http_req_failed<0.1'
```

### Output to File
```bash
k6 run scripts/perf/k6_login.js \
  --out json=results.json \
  --out csv=results.csv
```

### Cloud Testing (Grafana Cloud)
```bash
# Login to Grafana Cloud
k6 login cloud

# Run test in cloud
k6 cloud scripts/perf/k6_login.js
```

### Distributed Testing
```bash
# Run test across multiple machines
k6 run scripts/perf/k6_login.js \
  --vus 1000 \
  --duration 10m \
  --execution-segment 0:1/4 \
  --execution-segment-sequence 0,1/4,1/2,3/4,1
```

---

## INTERPRETING RESULTS

### Key Metrics

**Checks**: Pass/fail assertions
- ✓ = Passed
- ✗ = Failed

**HTTP Metrics**:
- `http_reqs`: Total requests
- `http_req_duration`: Response time
- `http_req_failed`: Failed requests percentage

**VU Metrics**:
- `vus`: Current virtual users
- `vus_max`: Maximum virtual users

**Iteration Metrics**:
- `iterations`: Completed iterations
- `iteration_duration`: Time per iteration

### Performance Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|-----------|------|
| P95 Latency | <200ms | <500ms | >1000ms |
| P99 Latency | <500ms | <1000ms | >2000ms |
| Error Rate | <0.1% | <1% | >5% |
| Success Rate | >99.9% | >99% | <95% |

---

## TROUBLESHOOTING

### Connection Refused
```bash
# Check if application is running
curl http://localhost:5000/api/health

# Check firewall
sudo ufw allow 5000
```

### High Error Rate
```bash
# Check application logs
docker logs <container-id>

# Check database connection
psql -U postgres -d gaara -c "SELECT 1"
```

### Out of Memory
```bash
# Reduce VUs
k6 run scripts/perf/k6_login.js --vus 5

# Increase system memory
# Or run on more powerful machine
```

### Slow Response Times
```bash
# Check database performance
EXPLAIN ANALYZE SELECT * FROM products;

# Check application metrics
curl http://localhost:5000/metrics
```

---

## BEST PRACTICES

1. ✅ Start with small load (10 users)
2. ✅ Gradually increase load
3. ✅ Monitor system resources
4. ✅ Run tests during off-peak hours
5. ✅ Document baseline metrics
6. ✅ Compare results over time
7. ✅ Test in staging before production
8. ✅ Use realistic test data

---

## CI/CD INTEGRATION

### GitHub Actions
```yaml
- name: Run K6 Load Test
  run: |
    k6 run scripts/perf/k6_login.js \
      --env BASE_URL=http://localhost:5000 \
      --env USERS=10 \
      --env DURATION=30s \
      --out json=results.json
```

### GitLab CI
```yaml
load_test:
  image: grafana/k6:latest
  script:
    - k6 run scripts/perf/k6_login.js
```

---

**Status**: K6 Setup Complete  
**Next**: Run baseline tests and establish performance baselines

