=================================================================================
API DESIGN & DEVELOPMENT - REST, GraphQL, gRPC
=================================================================================

Version: Latest
Type: Architecture - API

Comprehensive guidance for API design, development, and documentation.

=================================================================================
REST API BEST PRACTICES
=================================================================================

## Resource Naming

**Good:**
- GET /api/products
- GET /api/products/{id}
- POST /api/products
- PUT /api/products/{id}
- DELETE /api/products/{id}

**Bad:**
- GET /api/getAllProducts
- POST /api/createProduct
- GET /api/product-detail?id=1

## HTTP Methods

- **GET:** Retrieve resources (idempotent, safe)
- **POST:** Create new resources
- **PUT:** Update entire resource (idempotent)
- **PATCH:** Partial update
- **DELETE:** Remove resource (idempotent)

## Status Codes

**Success:**
- 200 OK - Successful GET, PUT, PATCH
- 201 Created - Successful POST
- 204 No Content - Successful DELETE

**Client Errors:**
- 400 Bad Request - Invalid data
- 401 Unauthorized - Not authenticated
- 403 Forbidden - Not authorized
- 404 Not Found - Resource doesn't exist
- 422 Unprocessable Entity - Validation error

**Server Errors:**
- 500 Internal Server Error
- 503 Service Unavailable

## Request/Response Format

**Request:**
```json
POST /api/products
Content-Type: application/json

{
  "name": "Laptop",
  "price": 999.99,
  "stock": 10,
  "category_id": 1
}
```

**Response:**
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 123,
  "name": "Laptop",
  "price": 999.99,
  "stock": 10,
  "category_id": 1,
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Pagination

```json
GET /api/products?page=2&page_size=20

{
  "count": 150,
  "next": "/api/products?page=3&page_size=20",
  "previous": "/api/products?page=1&page_size=20",
  "results": [...]
}
```

## Filtering & Sorting

```
GET /api/products?category=electronics&min_price=100&max_price=1000&sort=-price
```

## Versioning

**URL Versioning:**
```
/api/v1/products
/api/v2/products
```

**Header Versioning:**
```
Accept: application/vnd.myapi.v1+json
```

## Error Responses

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "price": ["Price must be positive"],
      "stock": ["Stock cannot be negative"]
    }
  }
}
```

=================================================================================
API DOCUMENTATION
=================================================================================

## OpenAPI/Swagger (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for managing products",
    version="1.0.0"
)

class Product(BaseModel):
    """Product model."""
    name: str
    price: float
    stock: int = 0

@app.post("/api/products/", response_model=Product, tags=["products"])
async def create_product(product: Product):
    """
    Create a new product.
    
    - **name**: Product name
    - **price**: Product price (must be positive)
    - **stock**: Available stock (default: 0)
    """
    return product
```

Access docs at: `http://localhost:8000/docs`

## Django REST Framework

```python
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=ProductSerializer,
    responses={
        201: ProductSerializer,
        400: 'Bad Request'
    }
)
@api_view(['POST'])
def create_product(request):
    """Create a new product."""
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
```

=================================================================================
AUTHENTICATION & AUTHORIZATION
=================================================================================

## JWT Authentication

**Login:**
```
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

**Using Token:**
```
GET /api/products
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## API Keys

```
GET /api/products
X-API-Key: your-api-key-here
```

## OAuth 2.0

```
GET /api/products
Authorization: Bearer oauth-access-token
```

=================================================================================
RATE LIMITING
=================================================================================

## Django

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

## FastAPI

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/products/")
@limiter.limit("5/minute")
async def get_products(request: Request):
    return {"products": []}
```

## Response Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

=================================================================================
CACHING
=================================================================================

## HTTP Caching

```
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

## Redis Caching

```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(timeout=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, timeout, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_response(timeout=600)
async def get_products():
    # Expensive database query
    return products
```

=================================================================================
WEBHOOKS
=================================================================================

## Implementing Webhooks

```python
import requests

def send_webhook(event_type, data, webhook_url):
    payload = {
        "event": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Webhook failed: {e}")

# Usage
send_webhook("product.created", product_data, user.webhook_url)
```

## Receiving Webhooks

```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle event
    if event['type'] == 'payment_intent.succeeded':
        handle_payment_success(event['data']['object'])
    
    return {"status": "success"}
```

=================================================================================
GRAPHQL
=================================================================================

## Schema Definition

```python
import graphene

class Product(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    price = graphene.Float()
    stock = graphene.Int()

class Query(graphene.ObjectType):
    products = graphene.List(Product)
    product = graphene.Field(Product, id=graphene.ID())
    
    def resolve_products(self, info):
        return Product.objects.all()
    
    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        price = graphene.Float()
        stock = graphene.Int()
    
    product = graphene.Field(Product)
    
    def mutate(self, info, name, price, stock):
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
```

## Query Example

```graphql
query {
  products {
    id
    name
    price
  }
}

mutation {
  createProduct(name: "Laptop", price: 999.99, stock: 10) {
    product {
      id
      name
    }
  }
}
```

=================================================================================
API TESTING
=================================================================================

## pytest (FastAPI)

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/api/products/",
        json={"name": "Test", "price": 99.99, "stock": 10}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test"

def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Django REST Framework

```python
from rest_framework.test import APITestCase

class ProductAPITest(APITestCase):
    def test_create_product(self):
        data = {"name": "Test", "price": 99.99}
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)
```

=================================================================================
END OF API PROMPT
=================================================================================


================================================================================
RECOVERED CONTENT FROM  (Phase 2)
================================================================================

management with Redis
- Lockout after N failed attempts
- Password: bcrypt/argon2, min 12 chars

E) Input Validation & Sanitization
- Schema validation: Pydantic, Zod, Joi
- SQL injection prevention: parameterized queries
- XSS prevention: DOMPurify, escape HTML
- CSRF tokens for state-changing ops
- File upload: type/size validation, virus scan
- Rate limiting: 100 req/min default

F) Database Integration
- Connection pooling (min 5, max 20)
- Transactions for multi-step ops
- Read replicas for scaling
- Query optimization: indexes, EXPLAIN
- N+1 query prevention
- Soft deletes preferred

G) Caching Strategy
- Redis for session, rate limits, cache
- Cache invalidation: TTL + manual
- Cache keys: namespaced, versioned
- CDN for static assets
- HTTP caching headers

H) Background Jobs
- Celery (Python), Bull (Node.js)
- Job queues: Redis, RabbitMQ
- Retry logic with exponential backoff
- Dead letter queue for failures
- Monitoring: job success rate

I) API Documentation
- OpenAPI 3.0 / 
ow queries
- Connection pooling
- Read replicas for scaling
- Partitioning for large tables

G) Backup & Recovery
- Daily automated backups
- Point-in-time recovery (PITR)
- Backup retention: 30 days
- Offsite storage (S3, GCS)
- Tested restore procedure
- RTO: <1 hour, RPO: <15 minutes

H) Security
- Least privilege: app user has minimal permissions
- No root/admin access from app
- Encrypted at rest (TDE)
- Encrypted in transit (SSL/TLS)
- Audit logging for DDL/DML
- Row-level security (RLS) where applicable

I) Monitoring
- Query performance metrics
- Connection pool usage
- Replication lag
- Disk usage alerts
- Slow query log

⸻

8) SECURITY & AUTHENTICATION (Expanded in )

A) Authentication Mechanisms
- JWT: access (15min) + refresh (7d) tokens
- OAuth 2.0 / OIDC for SSO
- MFA: TOTP (Google Authenticator), SMS, Email
- Biometric (optional): Face ID, Touch ID
- API keys for service-to-service
- Session management: Redis-backed

B) Password Policy
- Min length: 12 characters
- C
res_str)
        if time.time() > expires:
            return False
        expected = generate_route_token(route, user_id, 0).split('.')[0]
        return hmac.compare_digest(signature, expected)
    except:
        return False
```

D) Frontend
```typescript
// Use obfuscated routes
const obfuscatedRoute = await api.getRouteToken('/admin/users');
navigate(obfuscatedRoute);
```

E) Benefits
- Security through obscurity (additional layer)
- Harder to enumerate endpoints
- Time-limited access

F) Considerations
- Not a replacement for proper auth
- Adds complexity
- Cache implications

⸻

26) BACKUP POLICY (Enhanced in )

A) Trigger Conditions
- After any module completion
- After any 3 TODO items completed
- Daily automated (3 AM)
- Before major deployments
- On-demand via admin panel

B) Exclusions
- `.env`, `.env.*`
- `.venv`, `venv`, `node_modules`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `caches/`, `temp/`, `build/`, `dist/`
- `.git/` (separate Git backup)
- Secrets, A

================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```python
# Backend
def generate_route_token(route: str, user_id: str, ttl: int = 300) -> str:
    """Generate HMAC-signed route token"""
    expires = int(time.time()) + ttl
    payload = f"{route}:{user_id}:{expires}"
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()[:16]
    return f"{signature}.{expires}"

def verify_route_token(token: str, route: str, user_id: str) -> bool:
    """Verify route token"""
    try:
        signature, expires_str = token.split('.')
        expires = int(expires_str)
        if time.time() > expires:
            return False
        expected = generate_route_token(route, user_id, 0).split('.')[0]
        return hmac.compare_digest(signature, expected)
    except:
        return False
```

```python
# backend/src/error_handlers.py
from flask import jsonify
import logging
import traceback
import uuid

logger = logging.getLogger(__name__)

def generate_trace_id():
    """Generate unique trace ID for error tracking"""
    return str(uuid.uuid4())

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions"""
    trace_id = generate_trace_id()
    
    # Log detailed error internally
    logger.error(
        f"Unhandled exception [TraceID: {trace_id}]",
        exc_info=True,
        extra={
            'trace_id': trace_id,
            'error_type': type(e).__name__,
            'error_message': str(e),
            'stack_trace': traceback.format_exc(),
        }
    )
    
    # Return generic error to client
    if app.config['ENV'] == 'production':
        return jsonify({
            'error': 'An unexpected error occurred',
            'code': 'INTERNAL_ERROR',
            'traceId': trace_id,
            'message': 'Please contact support if the problem persists'
        }), 500
    else:
        # In development, return detailed error
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc().split('\n'),
            'traceId': trace_id
        }), 500

@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 errors"""
    # Don't reveal route structure
    return jsonify({
        'error': 'Resource not found',
        'code': 'NOT_FOUND'
    }), 404

@app.errorhandler(403)
def handle_forbidden(e):
    """Handle 403 errors"""
    # Don't reveal permission structure
    return jsonify({
        'error': 'Access denied',
        'code': 'FORBIDDEN'
    }), 403
```

```python
"""Environment-based error handling middleware"""

import os
import uuid
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime

APP_ENV = os.getenv('APP_ENV', 'development')

async def error_handler_middleware(request: Request, call_next):
    """Handle errors based on environment"""
    try:
        return await call_next(request)
    
    except Exception as e:
        error_id = str(uuid.uuid4())
        
        # Log error (always)
        log_error(error_id, e, request)
        
        if APP_ENV == 'production':
            # Production: Generic error
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "An error occurred. Please contact support.",
                    "error_id": error_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        else:
            # Development: Detailed error
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": str(e),
                    "error_type": type(e).__name__,
                    "error_id": error_id,
                    "traceback": traceback.format_exc(),
                    "request": {
                        "method": request.method,
                        "url": str(request.url),
                        "headers": dict(request.headers)
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

def log_error(error_id: str, error: Exception, request: Request):
    """Log error to file/service"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.error(
        f"Error ID: {error_id}\n"
        f"Type: {type(error).__name__}\n"
        f"Message: {str(error)}\n"
        f"URL: {request.url}\n"
        f"Method: {request.method}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )
```

```python
from config.definitions import (
    Status,           # ACTIVE, INACTIVE, PENDING, DELETED
    UserRole,         # ADMIN, USER, GUEST, MODERATOR
    Environment,      # DEV, STAGING, PROD
    APIResponse,      # استجابة API موحدة
    ErrorResponse     # استجابة خطأ موحدة
)
```

