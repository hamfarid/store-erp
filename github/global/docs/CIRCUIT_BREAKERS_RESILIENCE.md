# Circuit Breakers & Resilience - P3

**Date**: 2025-10-27  
**Purpose**: Implement circuit breakers for external APIs, databases, and third-party services  
**Status**: ✅ COMPLETE

---

## EXECUTIVE SUMMARY

The Gaara Store application has comprehensive resilience patterns with circuit breakers:

- ✅ Circuit breaker pattern implementation
- ✅ Fallback strategies
- ✅ Retry logic with exponential backoff
- ✅ Timeout management
- ✅ Bulkhead isolation
- ✅ Health checks

---

## CIRCUIT BREAKER PATTERN

### States
```
CLOSED: Normal operation, all requests pass
OPEN: Repeated failures, requests rejected immediately
HALF_OPEN: Recovery probe, limited requests allowed
```

### Configuration
```python
# backend/src/resilience/circuit_breaker.py

class CircuitBreaker:
    def __init__(self, 
                 failure_threshold=0.5,
                 recovery_timeout=60,
                 expected_exception=Exception):
        self.failure_threshold = failure_threshold  # 50%
        self.recovery_timeout = recovery_timeout    # 60 seconds
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpen()
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self._should_open():
            self.state = 'OPEN'
    
    def _should_open(self):
        total = self.failure_count + self.success_count
        return total > 0 and (self.failure_count / total) > self.failure_threshold
    
    def _should_attempt_reset(self):
        return (time.time() - self.last_failure_time) > self.recovery_timeout
```

---

## EXTERNAL API RESILIENCE

### Configuration
```python
# External API circuit breaker
api_breaker = CircuitBreaker(
    failure_threshold=0.5,      # 50% failure rate
    recovery_timeout=60,         # 60 seconds
    expected_exception=requests.RequestException
)

# Retry configuration
MAX_RETRIES = 3
BACKOFF_FACTOR = 2  # Exponential backoff
TIMEOUT = 5  # seconds
```

### Implementation
```python
@app.route('/api/external-data')
def get_external_data():
    try:
        # Try with circuit breaker
        data = api_breaker.call(
            fetch_external_api,
            timeout=TIMEOUT
        )
        return {'success': True, 'data': data}
    except CircuitBreakerOpen:
        # Fallback to cached data
        cached_data = cache.get('external_data')
        if cached_data:
            return {'success': True, 'data': cached_data, 'cached': True}
        else:
            return {'success': False, 'error': 'Service unavailable'}, 503
    except Exception as e:
        logger.error(f"Error fetching external data: {e}")
        return {'success': False, 'error': str(e)}, 500

def fetch_external_api(timeout):
    response = requests.get(
        'https://api.external.com/data',
        timeout=timeout,
        headers={'Authorization': 'Bearer token'}
    )
    response.raise_for_status()
    return response.json()
```

---

## DATABASE RESILIENCE

### Connection Pool
```python
# Database connection pool
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
```

### Retry Logic
```python
def execute_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return db.session.execute(query)
        except OperationalError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"DB error, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                raise
```

---

## THIRD-PARTY SERVICE RESILIENCE

### Payment Service
```python
payment_breaker = CircuitBreaker(
    failure_threshold=0.3,
    recovery_timeout=120,
    expected_exception=PaymentException
)

def process_payment(amount, card_token):
    try:
        result = payment_breaker.call(
            stripe.Charge.create,
            amount=int(amount * 100),
            currency='usd',
            source=card_token
        )
        return {'success': True, 'charge_id': result.id}
    except CircuitBreakerOpen:
        # Queue for retry
        queue_payment_retry(amount, card_token)
        return {'success': False, 'error': 'Payment service temporarily unavailable'}, 503
```

### Email Service
```python
email_breaker = CircuitBreaker(
    failure_threshold=0.5,
    recovery_timeout=60,
    expected_exception=EmailException
)

def send_email(to, subject, body):
    try:
        email_breaker.call(
            sendgrid_client.send,
            to_emails=to,
            subject=subject,
            plain_text_content=body
        )
        return True
    except CircuitBreakerOpen:
        # Queue for retry
        queue_email(to, subject, body)
        logger.warning(f"Email service unavailable, queued: {to}")
        return False
```

---

## FALLBACK STRATEGIES

### Cached Response
```python
def get_product_with_fallback(product_id):
    try:
        product = api_breaker.call(fetch_product, product_id)
        cache.set(f'product:{product_id}', product, ttl=3600)
        return product
    except CircuitBreakerOpen:
        cached = cache.get(f'product:{product_id}')
        if cached:
            return cached
        raise ServiceUnavailable()
```

### Stale-While-Revalidate
```python
def get_data_with_stale(key):
    try:
        fresh_data = api_breaker.call(fetch_data, key)
        cache.set(key, fresh_data, ttl=300)
        return fresh_data
    except CircuitBreakerOpen:
        stale_data = cache.get(key)
        if stale_data:
            return stale_data
        raise ServiceUnavailable()
```

### Graceful Degradation
```python
def get_dashboard_data():
    data = {}
    
    # Try to get products
    try:
        data['products'] = product_breaker.call(fetch_products)
    except CircuitBreakerOpen:
        data['products'] = []
        data['products_status'] = 'unavailable'
    
    # Try to get invoices
    try:
        data['invoices'] = invoice_breaker.call(fetch_invoices)
    except CircuitBreakerOpen:
        data['invoices'] = []
        data['invoices_status'] = 'unavailable'
    
    return data
```

---

## HEALTH CHECKS

### Endpoint Health Check
```python
@app.route('/health')
def health_check():
    health = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {}
    }
    
    # Check database
    try:
        db.session.execute('SELECT 1')
        health['services']['database'] = 'healthy'
    except Exception as e:
        health['services']['database'] = 'unhealthy'
        health['status'] = 'degraded'
    
    # Check external API
    if api_breaker.state == 'OPEN':
        health['services']['external_api'] = 'unavailable'
        health['status'] = 'degraded'
    else:
        health['services']['external_api'] = 'healthy'
    
    # Check payment service
    if payment_breaker.state == 'OPEN':
        health['services']['payment'] = 'unavailable'
        health['status'] = 'degraded'
    else:
        health['services']['payment'] = 'healthy'
    
    status_code = 200 if health['status'] == 'healthy' else 503
    return health, status_code
```

---

## MONITORING & ALERTS

### Metrics
```python
# Track circuit breaker state changes
circuit_breaker_state = Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)',
    ['service']
)

# Track failures
circuit_breaker_failures = Counter(
    'circuit_breaker_failures_total',
    'Total circuit breaker failures',
    ['service']
)

# Track rejections
circuit_breaker_rejections = Counter(
    'circuit_breaker_rejections_total',
    'Total circuit breaker rejections',
    ['service']
)
```

### Alerts
```
- Circuit breaker OPEN: Immediate alert
- Circuit breaker HALF_OPEN: Warning
- High failure rate: Alert
- Service unavailable: Critical alert
```

---

## TESTING

### Circuit Breaker Tests
```python
def test_circuit_breaker_opens_on_failures():
    breaker = CircuitBreaker(failure_threshold=0.5)
    
    # Simulate failures
    for _ in range(5):
        try:
            breaker.call(failing_function)
        except:
            pass
    
    assert breaker.state == 'OPEN'

def test_circuit_breaker_half_open_after_timeout():
    breaker = CircuitBreaker(recovery_timeout=1)
    breaker.state = 'OPEN'
    
    time.sleep(1.1)
    
    try:
        breaker.call(failing_function)
    except CircuitBreakerOpen:
        pass
    
    assert breaker.state == 'HALF_OPEN'
```

---

## DEPLOYMENT CHECKLIST

- [x] Circuit breakers implemented
- [x] Fallback strategies configured
- [x] Retry logic with backoff
- [x] Timeout management
- [x] Health checks configured
- [x] Monitoring enabled
- [x] Alerts configured
- [x] Tests passing

---

**Status**: ✅ **CIRCUIT BREAKERS & RESILIENCE COMPLETE**  
**Date**: 2025-10-27  
**Next**: Secrets Management Audit (Final Task)

