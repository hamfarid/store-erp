# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓                                                                             ▓
# ▓                    GAARA ERP v12 - PROJECT CONSTITUTION                     ▓
# ▓                      Speckit Principles & Standards                         ▓
# ▓                                                                             ▓
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

**Version:** 1.0.0
**Effective Date:** 2026-01-15
**Status:** RATIFIED
**Methodology:** Speckit JIT Documentation + Global Core Prompt v23.0

---

## 📜 PREAMBLE

This Constitution establishes the **immutable principles** that govern all development, testing, user experience, and performance decisions for Gaara ERP v12. These principles are **non-negotiable** and form the foundation of our technical excellence.

Every developer, AI agent, and contributor MUST adhere to these principles. Violations require documented exceptions approved by the technical leadership.

---

# 🏛️ ARTICLE I: CODE QUALITY PRINCIPLES

## Section 1.1: The Principle of Clarity Over Cleverness

> **"Code is read 10x more than it is written. Optimize for readability."**

### Requirements:
- ✅ **Self-documenting code**: Variable and function names must clearly express intent
- ✅ **Single Responsibility**: Each function/class does ONE thing well
- ✅ **Maximum function length**: 50 lines (exceptions require comment justification)
- ✅ **Maximum file length**: 500 lines (split into modules if exceeded)
- ❌ **FORBIDDEN**: "Magic numbers" without named constants
- ❌ **FORBIDDEN**: Nested conditionals deeper than 3 levels

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_count`, `total_amount` |
| Functions | snake_case, verb_noun | `get_user_by_id()`, `calculate_tax()` |
| Classes | PascalCase | `InvoiceManager`, `UserSerializer` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_TIMEOUT` |
| Files | snake_case | `invoice_manager.py`, `user_serializer.py` |
| React Components | PascalCase | `UserDashboard.jsx`, `InvoiceTable.jsx` |

```python
# ✅ CORRECT: Clear, self-documenting
def calculate_invoice_total(line_items: list[LineItem], tax_rate: Decimal) -> Decimal:
    """Calculate the total amount for an invoice including tax."""
    subtotal = sum(item.quantity * item.unit_price for item in line_items)
    tax_amount = subtotal * tax_rate
    return subtotal + tax_amount

# ❌ INCORRECT: Unclear, magic numbers
def calc(items, r):
    s = sum(i.q * i.p for i in items)
    return s + s * r
```

---

## Section 1.2: The Principle of Defensive Programming

> **"Assume all external input is hostile. Validate everything."**

### Requirements:
- ✅ **Input validation**: ALL external data must be validated at system boundaries
- ✅ **Type hints**: All Python functions MUST have complete type annotations
- ✅ **Error handling**: Every `try` block MUST have specific exception handling
- ✅ **Fail-safe defaults**: Use secure defaults; opt-in to less secure options
- ❌ **FORBIDDEN**: Bare `except:` clauses
- ❌ **FORBIDDEN**: Trusting client-side validation alone

### Validation Pattern

```python
# ✅ CORRECT: Defensive validation
from marshmallow import Schema, fields, validate, ValidationError

class InvoiceCreateSchema(Schema):
    """Schema for invoice creation with strict validation."""
    customer_id = fields.Integer(required=True, strict=True)
    amount = fields.Decimal(
        required=True,
        validate=validate.Range(min=0.01, max=999999999.99)
    )
    currency = fields.String(
        required=True,
        validate=validate.OneOf(['EGP', 'USD', 'EUR'])
    )
    description = fields.String(
        validate=validate.Length(max=500),
        load_default=""
    )

def create_invoice(data: dict) -> Invoice:
    """Create an invoice with validated data."""
    schema = InvoiceCreateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        raise InvalidInputError(errors=e.messages) from e
    
    return Invoice.objects.create(**validated_data)
```

---

## Section 1.3: The Principle of DRY (Don't Repeat Yourself)

> **"Every piece of knowledge must have a single, unambiguous representation."**

### Requirements:
- ✅ **Single source of truth**: Business logic defined ONCE
- ✅ **Reusable utilities**: Extract common patterns into shared modules
- ✅ **Configuration centralization**: Settings in ONE location per environment
- ✅ **Database constraints**: Enforce at DB level, not just application
- ❌ **FORBIDDEN**: Copy-paste code blocks > 5 lines
- ❌ **FORBIDDEN**: Duplicate model definitions

### DRY Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    DRY ENFORCEMENT LAYERS                    │
├─────────────────────────────────────────────────────────────┤
│ Level 1: Database    → Constraints, triggers, stored procs  │
│ Level 2: ORM/Models  → Validators, properties, methods      │
│ Level 3: Services    → Business logic, calculations         │
│ Level 4: API         → Serializers, views, permissions      │
│ Level 5: Frontend    → Hooks, utilities, components         │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 1.4: The Principle of Immutable History

> **"Never delete code without explanation. Track all changes."**

### Requirements:
- ✅ **Conventional commits**: All commits follow Conventional Commits spec
- ✅ **Atomic commits**: Each commit represents ONE logical change
- ✅ **No force push**: Never rewrite published history
- ✅ **Deprecation over deletion**: Mark obsolete code, move to `/unneeded/`
- ✅ **Change documentation**: ADRs for architectural decisions

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |
| `security` | Security-related changes |

```bash
# ✅ CORRECT
feat(invoices): add bulk export functionality

Implements CSV and Excel export for invoice lists.
Adds new endpoint POST /api/invoices/export/

Closes #123

# ❌ INCORRECT
fixed stuff
```

---

# 🧪 ARTICLE II: TESTING STANDARDS

## Section 2.1: The Principle of Test Coverage

> **"Untested code is broken code. Every feature ships with tests."**

### Coverage Requirements

| Metric | Minimum | Target | Critical Paths |
|--------|---------|--------|----------------|
| Line Coverage | 70% | 80% | 95% |
| Branch Coverage | 60% | 70% | 90% |
| Function Coverage | 80% | 90% | 100% |

### Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  5%   (Playwright)
                   ┌┴─────────┴┐
                   │Integration│ 15%  (API + DB)
                  ┌┴───────────┴┐
                  │    Unit     │ 80%  (pytest)
                 ┌┴─────────────┴┐
                 │  Static/Lint  │ ∞   (flake8, mypy)
                 └───────────────┘
```

---

## Section 2.2: The RORLOC Testing Methodology

> **"Test at every layer: Route, Object, Relation, Link, Operation, Complete."**

### Testing Layers

| Layer | What to Test | Tools | Coverage |
|-------|--------------|-------|----------|
| **R**oute | API endpoints respond correctly | pytest + DRF | All 255 routes |
| **O**bject | Models validate, serialize, compute | pytest | All 180 models |
| **R**elation | FK integrity, cascades, queries | pytest | All relations |
| **L**ink | Navigation, redirects, guards | Playwright | All UI paths |
| **O**peration | CRUD lifecycle, state machines | pytest + Playwright | All operations |
| **C**omplete | End-to-end user journeys | Playwright | Critical flows |

### Test File Structure

```
tests/
├── unit/
│   ├── models/
│   │   ├── test_invoice.py
│   │   └── test_user.py
│   ├── services/
│   │   └── test_invoice_service.py
│   └── utils/
│       └── test_validators.py
├── integration/
│   ├── api/
│   │   ├── test_auth_api.py
│   │   └── test_invoice_api.py
│   └── db/
│       └── test_migrations.py
└── e2e/
    ├── auth.spec.ts
    ├── dashboard.spec.ts
    └── invoice_workflow.spec.ts
```

---

## Section 2.3: The Principle of Test Independence

> **"Each test must be isolated. No test depends on another's execution."**

### Requirements:
- ✅ **Database isolation**: Each test gets fresh database state
- ✅ **No shared state**: Tests do not share global variables
- ✅ **Explicit setup**: All preconditions in test setup, not implicit
- ✅ **Deterministic**: Same input = same output, always
- ❌ **FORBIDDEN**: Tests that must run in specific order
- ❌ **FORBIDDEN**: Tests that modify shared fixtures

### Test Pattern: Arrange-Act-Assert (AAA)

```python
# ✅ CORRECT: Clear AAA structure
def test_invoice_total_calculation():
    """Test that invoice total includes tax correctly."""
    # ARRANGE
    line_items = [
        LineItem(quantity=2, unit_price=Decimal("100.00")),
        LineItem(quantity=1, unit_price=Decimal("50.00")),
    ]
    tax_rate = Decimal("0.14")  # 14% VAT
    
    # ACT
    total = calculate_invoice_total(line_items, tax_rate)
    
    # ASSERT
    expected = Decimal("285.00")  # 250 + 35 tax
    assert total == expected


def test_user_cannot_access_other_tenant_data(client, user_factory, invoice_factory):
    """Verify tenant isolation prevents cross-tenant data access."""
    # ARRANGE
    tenant_a_user = user_factory(tenant_id=1)
    tenant_b_invoice = invoice_factory(tenant_id=2)
    client.force_authenticate(user=tenant_a_user)
    
    # ACT
    response = client.get(f"/api/invoices/{tenant_b_invoice.id}/")
    
    # ASSERT
    assert response.status_code == 404  # Not 403 - don't reveal existence
```

---

## Section 2.4: The Principle of Security Testing

> **"Every security control must have a test proving it works."**

### Required Security Tests

| Category | Test Type | Frequency |
|----------|-----------|-----------|
| Authentication | Positive + negative auth flows | Every PR |
| Authorization | Permission matrix validation | Every PR |
| Input Validation | Fuzzing, injection attempts | Weekly |
| Session Management | Hijacking prevention, timeout | Every PR |
| Rate Limiting | Threshold enforcement | Every PR |
| CSRF Protection | Token validation | Every PR |
| SQL Injection | Parameterization verification | Weekly |
| XSS Prevention | Sanitization checks | Every PR |

### Security Test Examples

```python
class TestSecurityControls:
    """Security control verification tests."""
    
    def test_account_lockout_after_failed_attempts(self, client):
        """Verify account locks after 5 failed login attempts."""
        for _ in range(5):
            client.post("/api/auth/login/", {"password": "wrong"})
        
        response = client.post("/api/auth/login/", {"password": "correct"})
        assert response.status_code == 423  # Locked
    
    def test_jwt_expired_token_rejected(self, client, expired_token):
        """Verify expired JWT tokens are rejected."""
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_token}")
        response = client.get("/api/users/me/")
        assert response.status_code == 401
    
    def test_csrf_required_for_mutations(self, client):
        """Verify CSRF token required for state-changing requests."""
        response = client.post("/api/invoices/", {}, format="json")
        assert response.status_code == 403
        assert "CSRF" in response.data["detail"]
```

---

# 🎨 ARTICLE III: USER EXPERIENCE CONSISTENCY

## Section 3.1: The Principle of Design System Adherence

> **"Every UI element must conform to the design system. No exceptions."**

### Design Tokens

```json
{
  "colors": {
    "primary": {
      "50": "#e8f5e9",
      "500": "#4caf50",
      "900": "#1b5e20"
    },
    "neutral": {
      "50": "#fafafa",
      "500": "#9e9e9e",
      "900": "#212121"
    },
    "error": "#f44336",
    "warning": "#ff9800",
    "success": "#4caf50",
    "info": "#2196f3"
  },
  "typography": {
    "fontFamily": {
      "arabic": "'Noto Sans Arabic', 'Cairo', sans-serif",
      "english": "'Inter', 'Roboto', sans-serif",
      "mono": "'JetBrains Mono', monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem"
    }
  },
  "spacing": {
    "unit": "4px",
    "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96]
  },
  "borderRadius": {
    "none": "0",
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "full": "9999px"
  }
}
```

---

## Section 3.2: The Principle of RTL-First Design

> **"Arabic is the primary language. All designs start RTL, then adapt to LTR."**

### RTL Requirements

| Element | RTL Behavior | Implementation |
|---------|--------------|----------------|
| Text alignment | Right-aligned by default | `text-align: start` |
| Icons with direction | Mirrored (arrows, navigation) | CSS `transform: scaleX(-1)` |
| Forms | Labels on right, inputs follow | Flexbox `direction: rtl` |
| Tables | Columns flow right-to-left | `<html dir="rtl">` |
| Numbers | LTR within RTL context | `direction: ltr` on number spans |
| Dates | Localized (Hijri option) | date-fns with locale |

### RTL CSS Pattern

```css
/* ✅ CORRECT: Use logical properties */
.card {
  padding-inline-start: var(--spacing-4);
  padding-inline-end: var(--spacing-4);
  margin-block-start: var(--spacing-2);
  border-start-start-radius: var(--radius-md);
}

/* ❌ INCORRECT: Physical properties break RTL */
.card {
  padding-left: 16px;
  padding-right: 16px;
  margin-top: 8px;
  border-top-left-radius: 8px;
}
```

---

## Section 3.3: The Principle of Consistent Interaction Patterns

> **"Users should never be surprised. Same action = same result everywhere."**

### Standard Interaction Patterns

| Action | Visual Feedback | Timing |
|--------|-----------------|--------|
| Button click | Ripple effect + state change | < 100ms |
| Form submit | Loading spinner + disable button | Immediate |
| Success | Green toast notification | 3 seconds |
| Error | Red toast with action | 5 seconds |
| Delete | Confirmation dialog | User-triggered |
| Navigation | Page transition animation | 200ms |

### Loading State Pattern

```jsx
// ✅ CORRECT: Consistent loading pattern
function InvoiceList() {
  const { data, isLoading, error } = useInvoices();
  
  if (isLoading) {
    return <TableSkeleton rows={5} columns={6} />;
  }
  
  if (error) {
    return (
      <ErrorState
        title="فشل تحميل الفواتير"
        message={error.message}
        action={{ label: "إعادة المحاولة", onClick: refetch }}
      />
    );
  }
  
  if (!data?.length) {
    return (
      <EmptyState
        icon={<InvoiceIcon />}
        title="لا توجد فواتير"
        description="ابدأ بإنشاء فاتورة جديدة"
        action={{ label: "إنشاء فاتورة", href: "/invoices/new" }}
      />
    );
  }
  
  return <InvoiceTable data={data} />;
}
```

---

## Section 3.4: The Principle of Accessibility (WCAG AA)

> **"The system must be usable by everyone, regardless of ability."**

### Accessibility Requirements

| Criterion | Requirement | Test Method |
|-----------|-------------|-------------|
| Color contrast | 4.5:1 minimum (text), 3:1 (large text) | Contrast checker |
| Focus indicators | Visible focus ring on all interactive elements | Tab navigation |
| Screen reader | All content accessible via ARIA | NVDA/VoiceOver |
| Keyboard navigation | All functions accessible via keyboard | Manual testing |
| Error identification | Errors identified by more than color | Visual + text |
| Form labels | All inputs have associated labels | Automated scan |

### Accessibility Pattern

```jsx
// ✅ CORRECT: Accessible form field
function FormField({ id, label, error, required, ...props }) {
  const errorId = `${id}-error`;
  const describedBy = error ? errorId : undefined;
  
  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only">(مطلوب)</span>}
      </label>
      <input
        id={id}
        aria-required={required}
        aria-invalid={!!error}
        aria-describedby={describedBy}
        {...props}
      />
      {error && (
        <span id={errorId} role="alert" className="error-message">
          {error}
        </span>
      )}
    </div>
  );
}
```

---

# ⚡ ARTICLE IV: PERFORMANCE REQUIREMENTS

## Section 4.1: The Principle of Speed Budgets

> **"Performance is a feature. Every millisecond matters to the user."**

### Performance Budgets

| Metric | Budget | Critical |
|--------|--------|----------|
| **Time to First Byte (TTFB)** | < 200ms | < 100ms |
| **First Contentful Paint (FCP)** | < 1.5s | < 1.0s |
| **Largest Contentful Paint (LCP)** | < 2.5s | < 1.5s |
| **First Input Delay (FID)** | < 100ms | < 50ms |
| **Cumulative Layout Shift (CLS)** | < 0.1 | < 0.05 |
| **Time to Interactive (TTI)** | < 3.0s | < 2.0s |
| **Total Bundle Size (gzipped)** | < 250KB | < 150KB |
| **API Response (p95)** | < 500ms | < 200ms |
| **Database Query (p95)** | < 100ms | < 50ms |

### Lighthouse Score Requirements

| Category | Minimum | Target |
|----------|---------|--------|
| Performance | 80 | 90+ |
| Accessibility | 90 | 100 |
| Best Practices | 90 | 100 |
| SEO | 90 | 100 |
| PWA | 80 | 90+ |

---

## Section 4.2: The Principle of Database Efficiency

> **"Every query must be intentional. N+1 queries are forbidden."**

### Query Requirements

| Rule | Requirement |
|------|-------------|
| **Select fields** | Only fetch columns needed (`SELECT *` forbidden) |
| **Pagination** | All list endpoints must be paginated (max 100) |
| **Eager loading** | Use `select_related`/`prefetch_related` for relations |
| **Indexing** | All foreign keys and frequently queried fields indexed |
| **Query count** | Maximum 10 queries per request (log warnings at 5) |

### Query Optimization Pattern

```python
# ❌ INCORRECT: N+1 query problem
def get_invoices_slow():
    invoices = Invoice.objects.all()
    for invoice in invoices:
        print(invoice.customer.name)  # Query per invoice!
    return invoices

# ✅ CORRECT: Eager loading
def get_invoices_fast():
    return Invoice.objects.select_related(
        'customer', 
        'created_by'
    ).prefetch_related(
        'line_items',
        'payments'
    ).only(
        'id', 'number', 'total', 'status', 'created_at',
        'customer__id', 'customer__name',
        'created_by__id', 'created_by__username'
    ).order_by('-created_at')[:100]
```

---

## Section 4.3: The Principle of Caching Strategy

> **"The fastest request is the one you don't make."**

### Caching Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      CACHING ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│ Layer 1: Browser Cache    │ Static assets (1 year), API (5 min) │
│ Layer 2: CDN Cache        │ Static assets, public API responses │
│ Layer 3: Application      │ LRU cache for computations          │
│ Layer 4: Redis            │ Session, rate limits, query cache   │
│ Layer 5: Database         │ Query cache, materialized views     │
└─────────────────────────────────────────────────────────────────┘
```

### Cache TTL Guidelines

| Data Type | TTL | Invalidation |
|-----------|-----|--------------|
| Static assets | 1 year | Version in filename |
| User session | 15 min | On logout/password change |
| API list responses | 5 min | On any write to resource |
| Computed aggregates | 1 hour | On underlying data change |
| Configuration | 24 hours | On admin update |

---

## Section 4.4: The Principle of Graceful Degradation

> **"The system must remain functional under adverse conditions."**

### Degradation Strategy

| Condition | Response |
|-----------|----------|
| Database slow | Return cached data with "stale" indicator |
| External API down | Use fallback/cached values |
| High load | Shed non-critical features (analytics, AI) |
| Memory pressure | Clear caches, reject new sessions |
| Network partition | Queue writes for later sync |

### Circuit Breaker Pattern

```python
from circuitbreaker import circuit

@circuit(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=ExternalServiceError
)
def fetch_exchange_rate(currency: str) -> Decimal:
    """Fetch current exchange rate with circuit breaker protection."""
    try:
        response = external_api.get_rate(currency)
        cache.set(f"rate:{currency}", response.rate, ttl=3600)
        return response.rate
    except ExternalServiceError:
        # Circuit will open after 5 failures
        cached_rate = cache.get(f"rate:{currency}")
        if cached_rate:
            return cached_rate
        raise
```

---

# 📋 ARTICLE V: ENFORCEMENT & COMPLIANCE

## Section 5.1: Automated Enforcement

### CI/CD Gates (Must Pass Before Merge)

| Gate | Tool | Threshold |
|------|------|-----------|
| Lint | flake8, ESLint | 0 errors |
| Type Check | mypy, TypeScript | 0 errors |
| Unit Tests | pytest, vitest | 100% pass |
| Coverage | pytest-cov | ≥ 70% |
| Security Scan | gitleaks, Snyk | 0 critical |
| Bundle Size | size-limit | ≤ budget |
| Lighthouse | lighthouse-ci | ≥ 80 all |

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint-python
        name: Lint Python
        entry: flake8
        language: system
        types: [python]
      
      - id: type-check
        name: Type Check
        entry: mypy --strict
        language: system
        types: [python]
      
      - id: format-python
        name: Format Python
        entry: black
        language: system
        types: [python]
      
      - id: lint-frontend
        name: Lint Frontend
        entry: npm run lint
        language: system
        files: \.(js|jsx|ts|tsx)$
      
      - id: secrets-check
        name: Check Secrets
        entry: gitleaks detect --source .
        language: system
```

---

## Section 5.2: Exception Process

### When to Request an Exception

1. **Legacy code** that cannot be immediately refactored
2. **Third-party constraints** that conflict with principles
3. **Performance trade-offs** documented with benchmarks
4. **Security trade-offs** with compensating controls

### Exception Request Format

```markdown
## Exception Request

**Principle:** [Article.Section]
**Requested by:** [Name]
**Date:** [YYYY-MM-DD]

### Justification
[Why this exception is necessary]

### Scope
[What code/feature is affected]

### Duration
[Temporary until X / Permanent]

### Compensating Controls
[What mitigations are in place]

### Approval
- [ ] Tech Lead
- [ ] Security (if security-related)
- [ ] Product (if UX-related)
```

---

## Section 5.3: Constitution Amendment Process

1. **Proposal**: Submit RFC in `docs/rfcs/` directory
2. **Review Period**: 7 days for team feedback
3. **Discussion**: Team meeting to resolve concerns
4. **Approval**: Requires unanimous consent of tech leads
5. **Implementation**: Update CONSTITUTION.md, CI/CD gates
6. **Announcement**: Team notification and training

---

# ✅ CONSTITUTION ACCEPTANCE

By contributing to Gaara ERP v12, all developers agree to:

- [ ] Read and understand this Constitution
- [ ] Follow all principles without exception (unless approved)
- [ ] Report violations when observed
- [ ] Propose improvements through the amendment process
- [ ] Help teammates understand and follow these standards

---

**RATIFIED:** 2026-01-15
**VERSION:** 1.0.0
**NEXT REVIEW:** 2026-04-15

---

*"Excellence is not a skill. It's an attitude." — Ralph Marston*

**END OF CONSTITUTION**
