# FILE: docs/Search.md | PURPOSE: Search API design and implementation | OWNER: Backend | RELATED: docs/API_Contracts.md | LAST-AUDITED: 2025-10-21

# Search API — تصميم وبناء البحث

**Version**: 1.0  
**Last Updated**: 2025-10-21

---

## 1. Overview

Unified Search API endpoint supporting products, invoices, customers, suppliers, and users with filtering, pagination, and sorting.

---

## 2. Endpoint Specification

- Method: `GET`
- Path: `/api/search`
- Auth: JWT (role-based authorization)

### 2.1 Query Parameters

- `q` (string, optional): free-text query
- `type` (string, required): one of `product|invoice|customer|supplier|user`
- `limit` (int, optional, default=20, max=100)
- `offset` (int, optional, default=0)
- `sort` (string, optional): e.g., `name:asc`, `created_at:desc`
- `filters` (JSON string, optional): key-value filters

### 2.2 Response

```json
{
  "success": true,
  "data": [ { /* results */ } ],
  "pagination": { "limit": 20, "offset": 0, "total": 123 },
  "traceId": "abc123"
}
```

### 2.3 Error Envelope

```json
{
  "success": false,
  "error": { "code": "INVALID_REQUEST", "message": "...", "details": {"field": "type"}, "traceId": "..." }
}
```

---

## 3. Authorization

- Enforce RBAC via `Permissions_Model.md`.
- Examples:
  - `product`: READ for Products
  - `invoice`: READ for Invoices
  - `user`: ADMIN or READ:User

---

## 4. Indexing Strategy

- Use database indexes on searchable fields:
  - Products: `name`, `sku`, `category_id`
  - Invoices: `invoice_number`, `customer_id`, `date`
  - Customers: `name`, `email`, `phone`
  - Suppliers: `name`, `email`, `phone`
  - Users: `username`, `email`, `role`
- Add trigram or full-text indexes where supported (PostgreSQL).

---

## 5. Caching

- Cache frequent queries (keyed by `type|q|filters|sort|limit|offset`).
- TTL: 300s (5 minutes).
- Invalidate cache on CRUD changes for relevant entities.

---

## 6. Rate Limits

- Default: `100 per hour` per IP.
- Burst: `10 per minute` per IP.
- Stricter limits for `user` type.

---

## 7. SQL (Parameterised)

Example (Products):

```sql
SELECT id, name, sku, price FROM products
WHERE (:q IS NULL OR (name ILIKE '%' || :q || '%' OR sku ILIKE '%' || :q || '%'))
AND (:category_id IS NULL OR category_id = :category_id)
ORDER BY name ASC
LIMIT :limit OFFSET :offset;
```

---

## 8. Flask Implementation (Skeleton)

```python
from flask import Blueprint, request, jsonify
from src.auth import require_permission
from src.db import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
@require_permission('READ')
def search():
    q = request.args.get('q')
    type_ = request.args.get('type')
    limit = min(int(request.args.get('limit', 20)), 100)
    offset = int(request.args.get('offset', 0))
    sort = request.args.get('sort')
    filters = request.args.get('filters')
    
    # Validate type
    if type_ not in {'product', 'invoice', 'customer', 'supplier', 'user'}:
        return jsonify({ 'success': False, 'error': { 'code': 'INVALID_REQUEST', 'message': 'Invalid type', 'details': {'type': type_} } }), 400
    
    # Dispatch per type (use SQLAlchemy with parameterized filters)
    # ...
    
    return jsonify({ 'success': True, 'data': [], 'pagination': { 'limit': limit, 'offset': offset, 'total': 0 } })
```

---

## 9. OpenAPI Snippet

```yaml
paths:
  /api/search:
    get:
      summary: Unified search endpoint
      security:
        - bearerAuth: []
      parameters:
        - in: query
          name: q
          schema: { type: string }
        - in: query
          name: type
          schema: { type: string, enum: [product, invoice, customer, supplier, user] }
          required: true
        - in: query
          name: limit
          schema: { type: integer, default: 20, maximum: 100 }
        - in: query
          name: offset
          schema: { type: integer, default: 0 }
        - in: query
          name: sort
          schema: { type: string }
        - in: query
          name: filters
          schema: { type: string, description: "JSON string of filters" }
      responses:
        '200':
          description: Search results
        '400':
          description: Invalid request
        '401':
          description: Unauthorized
```

---

## 10. Acceptance Criteria

- [ ] Endpoint `/api/search` implemented with pagination and sorting
- [ ] RBAC enforced per entity type
- [ ] Input validation and standard error envelope
- [ ] Rate limits enforced
- [ ] Caching implemented (TTL 300s)
- [ ] SQL injection prevented (parameterized queries)
- [ ] OpenAPI updated

