=================================================================================
CODE QUALITY & BEST PRACTICES
=================================================================================

Version: 5.0.0
Type: Quality Assurance

Comprehensive guidance for maintaining high code quality.

=================================================================================
CODE STYLE
=================================================================================

## Python (PEP 8)

```python
# Good
def calculate_total_price(items, tax_rate=0.1):
    """Calculate total price including tax.
    
    Args:
        items: List of items with prices
        tax_rate: Tax rate (default: 0.1)
    
    Returns:
        float: Total price with tax
    """
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax

# Bad
def calc(i,t=0.1):
    s=sum(x.price for x in i)
    return s+s*t
```

## JavaScript/TypeScript

```typescript
// Good
interface Product {
  id: number;
  name: string;
  price: number;
}

function calculateTotalPrice(
  items: Product[],
  taxRate: number = 0.1
): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  const tax = subtotal * taxRate;
  return subtotal + tax;
}

// Bad
function calc(i,t=0.1){
  let s=0;
  for(let x of i)s+=x.price;
  return s+s*t;
}
```

=================================================================================
LINTING & FORMATTING
=================================================================================

## Python

**flake8:**
```bash
pip install flake8
flake8 --max-line-length=100 --exclude=venv,migrations
```

**black:**
```bash
pip install black
black --line-length 100 .
```

**pylint:**
```bash
pip install pylint
pylint --disable=C0111 myproject/
```

## JavaScript/TypeScript

**ESLint:**
```json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "semi": ["error", "always"]
  }
}
```

**Prettier:**
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100
}
```

=================================================================================
TYPE CHECKING
=================================================================================

## Python (mypy)

```python
from typing import List, Optional

def get_user(user_id: int) -> Optional[dict]:
    """Get user by ID."""
    return database.get(user_id)

def process_users(users: List[dict]) -> int:
    """Process list of users."""
    return len(users)
```

```bash
pip install mypy
mypy --strict myproject/
```

## TypeScript

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

function getUser(userId: number): User | null {
  return database.get(userId);
}

function processUsers(users: User[]): number {
  return users.length;
}
```

=================================================================================
CODE REVIEW CHECKLIST
=================================================================================

## Before Submitting PR

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No commented-out code
- [ ] No debug prints/logs
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance optimized
- [ ] Code reviewed by yourself first

## Reviewing Others' Code

- [ ] Functionality works as expected
- [ ] Code is readable and maintainable
- [ ] No obvious bugs
- [ ] Edge cases handled
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Documentation is clear

=================================================================================
REFACTORING
=================================================================================

## Extract Function

**Before:**
```python
def process_order(order):
    # Calculate total
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    
    # Apply discount
    if order.customer.is_premium:
        total *= 0.9
    
    # Add tax
    total *= 1.1
    
    return total
```

**After:**
```python
def calculate_subtotal(items):
    return sum(item.price * item.quantity for item in items)

def apply_discount(total, customer):
    if customer.is_premium:
        return total * 0.9
    return total

def add_tax(total, tax_rate=0.1):
    return total * (1 + tax_rate)

def process_order(order):
    subtotal = calculate_subtotal(order.items)
    discounted = apply_discount(subtotal, order.customer)
    return add_tax(discounted)
```

=================================================================================
DOCUMENTATION
=================================================================================

## Docstrings

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Discounted price
    
    Raises:
        ValueError: If discount_percent is not between 0 and 100
    
    Examples:
        >>> calculate_discount(100, 10)
        90.0
        >>> calculate_discount(100, 50)
        50.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

=================================================================================
PERFORMANCE
=================================================================================

## Profiling

```python
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result
```

## Optimization Tips

- Use list comprehensions instead of loops
- Cache expensive computations
- Use generators for large datasets
- Batch database queries
- Use appropriate data structures
- Profile before optimizing

=================================================================================
END OF QUALITY PROMPT
=================================================================================


================================================================================
RECOVERED CONTENT FROM v4.2.0 (Phase 2)
================================================================================

PI keys

C) Inclusions
- All source code (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`)
- All documentation (`.md`, `.txt`)
- Configuration files (`.json`, `.yaml`, `.toml`)
- Database schemas
- Scripts
- Tests

D) Naming Convention
```
backup-YYYY-MM-DD-HHmmss-<trigger>.tar.gz
backup-2025-10-28-150000-module-completion.tar.gz
backup-2025-10-28-030000-daily.tar.gz
```

E) Storage
- Local: `/backups/` (last 7 days)
- S3/GCS: long-term (30 days online, 1 year archive)
- Encrypted at rest
- Versioned

F) Restoration
- Documented procedure in `/docs/Runbook.md`
- Tested monthly
- RTO: <1 hour
- RPO: <24 hours

G) Monitoring
- Alert on backup failure
- Dashboard: backup success rate
- Audit log: all backup/restore operations

⸻

27) MLOPS LIFECYCLE (NEW in v3.1)

A) Data Pipeline
- Data collection & validation
- Data quality checks
- Feature engineering
- Data versioning (DVC, LFS)
- Train/val/test splits

B) Model Development
- Experiment tracking (MLflow, Weights & Biases)
- Hyperparameter tuning

 issues above before starting development.")
        return 1
    else:
        print("\n✅ All pre-development checks passed!")
        print("You're ready to start coding.")
        return 0

if __name__ == '__main__':
    sys.exit(pre_development_check())
```

C) GIT HOOK

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-development checks..."
python scripts/pre_dev_check.py

if [ $? -ne 0 ]; then
    echo "❌ Pre-development checks failed!"
    echo "Fix the issues or use 'git commit --no-verify' to skip (not recommended)"
    exit 1
fi
```

D) BENEFITS

✅ Prevents duplicate work  
✅ Ensures awareness of codebase  
✅ Catches issues early  
✅ Enforces best practices  
✅ Improves code quality

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻

END OF GLOBAL_GUIDELINES v3.2

## Summary of v3.2 Additions

**NEW SECTIONS (10):**
29. File Discovery & Mapping Protocol
30. Environment Detection & Configuration
31. Production Setup Wizard
32. Cross-Browser Testing
33. UI Asset Management
description
3. Add estimate and dependencies if known
4. Set status to "Not Started"

**Working on Tasks:**
1. Update status to "In Progress"
2. Add notes/blockers if needed
3. Update estimate if changed

**Completing Tasks:**
1. Mark with 'x'
2. Add completion date
3. Move to "Completed Tasks" section at bottom
4. **Never delete**

**Archiving:**
```bash
# Monthly archive
grep "^\- \[x\]" docs/TODO.md >> docs/completed_tasks.md
# Then manually remove from TODO.md (but keep in completed_tasks.md)
```

### 50.4 CI Integration

**Pre-commit Hook:**
```yaml
- repo: local
  hooks:
    - id: check-todo-format
      name: Check TODO file format
      entry: python scripts/check_todo_format.py
      language: python
      files: docs/TODO.md
```

---

## 51. Code Modularization

### 51.1 Modularization Rules

**Maximum Sizes:**
- **Function:** ≤50 lines (excluding docstring)
- **Class:** ≤300 lines
- **File:** ≤500 lines
- **Module:** ≤10 files

**If Exceeded:**
- Split function into smaller 
_create, order_service, sample_order_data):
        """Test order creation."""
        mock_order = Mock(id=123)
        mock_create.return_value = mock_order
        
        order = order_service.create_order(
            customer_id=sample_order_data['customer_id'],
            total=Decimal('40.25')
        )
        
        assert order.id == 123
        mock_create.assert_called_once()
```

**Running Tests:**
```bash
# All tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific file
pytest tests/unit/test_order_service.py

# Specific test
pytest tests/unit/test_order_service.py::TestOrderService::test_calculate_total_success

# Parallel execution
pytest -n auto
```

**Code Quality Checks:**
```bash
# Before running tests
flake8 . --max-line-length=120
autopep8 --in-place --aggressive --aggressive -r .
pylint --max-line-length=120 .
mypy --strict .
```

### 53.2 Frontend Testing (Selenium/Playwright)

**Tools:**
```bash
# Selenium
pip install selenium webdriver
overage)
```

**base.txt:**
```
# Core framework
django==4.2.0
djangorestframework==3.14.0

# Database
psycopg2-binary==2.9.5

# Utilities
python-dotenv==1.0.0
requests==2.31.0
```

**development.txt:**
```
-r base.txt

# Development tools
django-debug-toolbar==4.0.0
ipython==8.12.0

# Linting & formatting
flake8==6.0.0
black==23.3.0
isort==5.12.0
pylint==2.17.0
mypy==1.2.0

# Testing
pytest==7.3.1
pytest-django==4.5.2
pytest-cov==4.0.0
```

**production.txt:**
```
-r base.txt

# Production server
gunicorn==20.1.0

# Monitoring
sentry-sdk==1.25.0
```

**testing.txt:**
```
-r base.txt

# Testing framework
pytest==7.3.1
pytest-django==4.5.2
pytest-cov==4.0.0
pytest-mock==3.10.0
pytest-xdist==3.2.1

# Browser testing
selenium==4.9.0
playwright==1.33.0
```

### 56.3 Version Pinning

**Pin exact versions in production:**
```
# ✅ GOOD - Exact version
django==4.2.0
requests==2.31.0

# ❌ BAD - Unpinned
django
requests>=2.0
```

**Use compatible release for development:**
```
# Development can 
              │
│  - Set up 2FA (optional)                                    │
│  - Configure admin email                                    │
│                                                             │
│  Step 4: Application Settings                               │
│  ────────────────────────────                               │
│  - Site name and description                                │
│  - Timezone and locale                                      │
│  - Currency settings                                        │
│  - Date/time formats                                        │
│                                                             │
│  Step 5: Email Configuration                                │
│  ───────────────────────────                                │
│  - SMTP settings                                            │
│  - Test email sending                                       │
│  - Email templates                                          │
│                       

================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```bash
   python scripts/map_files.py --output docs/File_Map.md
   ```

2. **Read Mandatory Documentation**
   - `/docs/File_Map.md` - Complete file inventory
   - `/docs/Class_Registry.md` - All classes/types
   - `/docs/Imports_Map.md` - Import dependencies
   - `/docs/Exports_Map.md` - Export mappings

3. **Search for Existing Files**
   ```bash
   # Search by name
   find . -name "*user*" -type f
   
   # Search by content (AST-based)
   python scripts/detect_duplicates.py --semantic --target "User"
   ```

B) FILE MAP STRUCTURE

`/docs/File_Map.md` format:
```

