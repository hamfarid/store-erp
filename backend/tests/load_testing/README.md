# Load Testing with Locust

This directory contains load testing scripts for the Store ERP API using [Locust](https://locust.io/).

## Installation

```bash
pip install locust
```

## Quick Start

### 1. Basic Load Test

Run a basic load test with web UI:

```bash
cd backend/tests/load_testing
locust -f locustfile.py --host=http://localhost:5000
```

Then open http://localhost:8089 in your browser and configure:
- Number of users: 100
- Spawn rate: 10 users/second
- Host: http://localhost:5000

### 2. Headless Load Test

Run without web UI:

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 --run-time 60s --headless
```

### 3. Generate HTML Report

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 --run-time 60s --headless \
       --html=load_test_report.html
```

## User Types

The load test simulates different types of users:

### 1. ReadOnlyUser
- **Purpose:** Simulates viewers, customers
- **Behavior:** Only GET requests
- **Wait time:** 1-3 seconds between requests
- **Task distribution:**
  - Products: 40%
  - Inventory: 30%
  - Invoices: 20%
  - System: 10%

### 2. RegularUser
- **Purpose:** Simulates employees, warehouse staff
- **Behavior:** Mix of read and write operations
- **Wait time:** 0.5-2 seconds between requests
- **Task distribution:**
  - Products: 35%
  - Inventory: 35%
  - Invoices: 25%
  - System: 5%

### 3. AdminUser
- **Purpose:** Simulates admin users
- **Behavior:** All operations including auth
- **Wait time:** 0.5-2 seconds between requests
- **Task distribution:**
  - Auth: 5%
  - Products: 30%
  - Inventory: 30%
  - Invoices: 30%
  - System: 5%

### 4. StressTestUser
- **Purpose:** Stress testing
- **Behavior:** Rapid fire requests
- **Wait time:** 0.1-0.5 seconds between requests
- **Task distribution:**
  - Products: 40%
  - Inventory: 30%
  - Invoices: 20%
  - System: 10%

## Load Shapes

### 1. GradualRampUp

Gradual increase in load:
- 0-1 min: 10 users
- 1-3 min: Ramp to 50 users
- 3-5 min: Ramp to 100 users
- 5-10 min: Hold at 100 users
- 10-12 min: Ramp down to 0

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --headless --shape=GradualRampUp
```

### 2. SpikeTest

Sudden spike in load:
- 0-1 min: 20 users (normal)
- 1-2 min: 200 users (spike!)
- 2-3 min: 20 users (back to normal)
- 3-4 min: 20 users (hold)

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --headless --shape=SpikeTest
```

## Test Scenarios

### Scenario 1: Normal Load

Simulate normal business hours:

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 50 --spawn-rate 5 --run-time 300s --headless \
       --html=normal_load_report.html
```

### Scenario 2: Peak Load

Simulate peak business hours:

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 200 --spawn-rate 20 --run-time 300s --headless \
       --html=peak_load_report.html
```

### Scenario 3: Stress Test

Push the system to its limits:

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 500 --spawn-rate 50 --run-time 300s --headless \
       --html=stress_test_report.html
```

### Scenario 4: Endurance Test

Long-running test to check for memory leaks:

```bash
locust -f locustfile.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 --run-time 3600s --headless \
       --html=endurance_test_report.html
```

## Metrics to Monitor

### Response Time
- **Target:** < 200ms for GET requests
- **Target:** < 500ms for POST/PUT requests
- **Alert:** > 1000ms

### Throughput
- **Target:** > 100 requests/second
- **Alert:** < 50 requests/second

### Error Rate
- **Target:** < 1%
- **Alert:** > 5%

### Resource Usage
- **CPU:** < 70%
- **Memory:** < 80%
- **Database connections:** < 80% of pool

## Interpreting Results

### Good Performance
```
Response Time (ms)
  50th percentile: 50ms
  95th percentile: 200ms
  99th percentile: 500ms

Requests/sec: 150
Failures: 0.5%
```

### Poor Performance
```
Response Time (ms)
  50th percentile: 500ms
  95th percentile: 2000ms
  99th percentile: 5000ms

Requests/sec: 30
Failures: 10%
```

## Troubleshooting

### High Response Times
1. Check database query performance
2. Check for N+1 queries
3. Add database indexes
4. Enable query caching
5. Optimize slow endpoints

### High Error Rate
1. Check application logs
2. Check database connection pool
3. Check for timeout issues
4. Verify API rate limiting

### Low Throughput
1. Check server resources (CPU, memory)
2. Check database performance
3. Check network latency
4. Scale horizontally

## Best Practices

1. **Start Small:** Begin with 10-20 users and gradually increase
2. **Monitor Resources:** Watch CPU, memory, database during tests
3. **Test Realistic Scenarios:** Use realistic data and user behavior
4. **Run Multiple Times:** Run tests multiple times for consistency
5. **Test in Staging:** Never run load tests in production
6. **Document Results:** Keep records of test results over time

## Advanced Usage

### Custom User Behavior

Create custom user class:

```python
from locust import HttpUser, task, between

class CustomUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def my_custom_task(self):
        self.client.get("/api/custom-endpoint")
```

### Custom Load Shape

Create custom load pattern:

```python
from locust import LoadTestShape

class CustomShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        if run_time < 60:
            return (10, 1)
        elif run_time < 120:
            return (50, 5)
        else:
            return None
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Load Test
  run: |
    pip install locust
    locust -f backend/tests/load_testing/locustfile.py \
           --host=http://localhost:5000 \
           --users 50 --spawn-rate 5 --run-time 60s --headless \
           --html=load_test_report.html
    
- name: Upload Report
  uses: actions/upload-artifact@v2
  with:
    name: load-test-report
    path: load_test_report.html
```

## Resources

- [Locust Documentation](https://docs.locust.io/)
- [Load Testing Best Practices](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- [Performance Testing Guide](https://martinfowler.com/articles/practical-test-pyramid.html)

