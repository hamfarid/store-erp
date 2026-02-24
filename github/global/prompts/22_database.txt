=================================================================================
DATABASE DESIGN & MANAGEMENT - PostgreSQL, MySQL, MongoDB
=================================================================================

Version: 5.0.0
Type: Architecture - Database

Comprehensive guidance for database design, optimization, and management.

=================================================================================
DATABASE SELECTION
=================================================================================

**PostgreSQL:**
- ACID compliance
- Advanced features (JSON, arrays, full-text search)
- Strong data integrity
- Complex queries
- Open source

**MySQL:**
- High performance
- Wide adoption
- Good for read-heavy workloads
- Simpler than PostgreSQL
- Open source

**MongoDB:**
- Document-oriented
- Flexible schema
- Horizontal scaling
- Good for unstructured data
- JSON-like documents

=================================================================================
SCHEMA DESIGN PRINCIPLES
=================================================================================

## Normalization

**1NF (First Normal Form):**
- Atomic values
- No repeating groups
- Each column contains only one value

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies
- All non-key attributes depend on entire primary key

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies
- Non-key attributes depend only on primary key

## Example Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock INTEGER DEFAULT 0 CHECK (stock >= 0),
    category_id INTEGER REFERENCES categories(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Unique index
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Partial index
CREATE INDEX idx_active_products ON products(name) 
WHERE is_active = TRUE;

-- Full-text search index (PostgreSQL)
CREATE INDEX idx_products_search ON products 
USING GIN(to_tsvector('english', name || ' ' || description));
```

=================================================================================
QUERY OPTIMIZATION
=================================================================================

## EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT p.*, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.price > 100
ORDER BY p.created_at DESC
LIMIT 20;
```

## Common Optimizations

**1. Use indexes:**
```sql
-- Before
SELECT * FROM products WHERE name LIKE '%laptop%';

-- After (with index)
CREATE INDEX idx_products_name ON products(name);
SELECT * FROM products WHERE name LIKE 'laptop%';
```

**2. Avoid SELECT *:**
```sql
-- Before
SELECT * FROM products;

-- After
SELECT id, name, price FROM products;
```

**3. Use JOINs instead of subqueries:**
```sql
-- Before (slow)
SELECT * FROM orders 
WHERE user_id IN (SELECT id FROM users WHERE is_active = TRUE);

-- After (faster)
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.is_active = TRUE;
```

**4. Limit results:**
```sql
SELECT * FROM products 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 0;
```

=================================================================================
MIGRATIONS
=================================================================================

## Django Migrations

```python
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Custom migration
from django.db import migrations

def add_sample_data(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.create(
        name='Sample Product',
        price=99.99,
        stock=10
    )

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(add_sample_data),
    ]
```

## Alembic Migrations (FastAPI)

```python
# Generate migration
alembic revision --autogenerate -m "Add products table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Migration file
def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('products')
```

=================================================================================
BACKUP & RESTORE
=================================================================================

## PostgreSQL

```bash
# Backup
pg_dump -U postgres -d mydb > backup.sql

# Backup with compression
pg_dump -U postgres -d mydb | gzip > backup.sql.gz

# Restore
psql -U postgres -d mydb < backup.sql

# Restore from compressed
gunzip -c backup.sql.gz | psql -U postgres -d mydb
```

## MySQL

```bash
# Backup
mysqldump -u root -p mydb > backup.sql

# Restore
mysql -u root -p mydb < backup.sql
```

## MongoDB

```bash
# Backup
mongodump --db mydb --out /backup/

# Restore
mongorestore --db mydb /backup/mydb/
```

=================================================================================
SECURITY
=================================================================================

## SQL Injection Prevention

**Bad (vulnerable):**
```python
# DON'T DO THIS
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**Good (safe):**
```python
# Django ORM
User.objects.filter(email=email)

# Raw SQL with parameters
cursor.execute("SELECT * FROM users WHERE email = %s", [email])
```

## Encryption

```sql
-- Encrypt sensitive data
CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users (email, password_hash)
VALUES ('user@example.com', crypt('password123', gen_salt('bf')));

-- Verify password
SELECT * FROM users 
WHERE email = 'user@example.com' 
AND password_hash = crypt('password123', password_hash);
```

=================================================================================
MONITORING
=================================================================================

## PostgreSQL

```sql
-- Active connections
SELECT * FROM pg_stat_activity;

-- Database size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- Table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

=================================================================================
END OF DATABASE PROMPT
=================================================================================


================================================================================
RECOVERED CONTENT FROM v4.2.0 (Phase 2)
================================================================================

Swagger
- Auto-generated from code
- Interactive docs (/docs, /redoc)
- Examples for all endpoints
- Error codes documented

J) Observability Hooks
- log_activity: all requests, CRUD, exports
- system_health: /health endpoint
- system_monitoring: metrics export
- Distributed tracing: OpenTelemetry
- Correlation IDs in logs

K) Security Hardening
- HTTPS only (redirect HTTP)
- Security headers: CSP, HSTS, X-Frame-Options
- Secrets: KMS/Vault, never in code
- SSRF prevention: URL validation
- Rate limiting per endpoint
- API key rotation

L) Testing Strategy
- Unit tests: >80% coverage
- Integration tests: DB, external APIs
- Contract tests: API schemas
- Load tests: k6, Locust
- Security tests: OWASP ZAP

⸻

7) DATABASE DESIGN & MIGRATIONS (Expanded in v3.0)

A) Database Selection
- PostgreSQL: ACID, JSON, full-text search
- MySQL: wide adoption, replication
- MongoDB: document store, flexible schema
- Redis: cache, sessions, queues
- Elasticsearch: full-text search, analytics

B) Schem
 resources
- Ansible for configuration
- Version controlled
- Modular, reusable
- Tested in staging

E) Monitoring & Logging
- Prometheus + Grafana for metrics
- ELK / Loki for logs
- OpenTelemetry for tracing
- Alerts: Slack, PagerDuty
- Dashboards: uptime, latency, errors

F) Disaster Recovery
- Multi-region deployment
- Automated backups (daily)
- Tested restore procedure
- RTO: <1 hour, RPO: <15 minutes
- Runbooks for incidents

⸻

10) TESTING & QA FRAMEWORK (Expanded in v3.0)

A) Testing Pyramid
- Unit tests: 70% (fast, isolated)
- Integration tests: 20% (DB, APIs)
- E2E tests: 10% (critical paths)

B) Unit Testing
- Coverage: >80% (target 90%)
- Frameworks: Jest, Pytest, Go test
- Mocking: external dependencies
- Fast: <5 seconds total

C) Integration Testing
- Database: test DB, migrations
- External APIs: mocked or test env
- Message queues: test broker
- Coverage: critical flows

D) E2E Testing
- Playwright, Cypress, Selenium
- Critical user journeys
- Run in CI before deploy

h fixed"
```

### CI Check
```yaml
- name: Check Line Length
  run: |
    flake8 . --max-line-length=120 --exclude=venv,.venv,migrations
```

## Rules
1. ✅ Max 120 characters per line
2. ✅ Break long strings
3. ✅ Use parentheses for line continuation
4. ✅ CI enforced
5. ✅ Auto-fix before commit

## Examples

### ❌ Bad (>120)
```python
result = some_very_long_function_name(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6, parameter7)
```

### ✅ Good (≤120)
```python
result = some_very_long_function_name(
    parameter1, parameter2, parameter3,
    parameter4, parameter5, parameter6,
    parameter7
)
```

================================================================================
42. ENVIRONMENT-BASED ERROR HANDLING
================================================================================

## Problem
- Same error display in Dev & Production
- Stack traces leak in Production (security risk)
- No error tracking

## Solution: Environment-Aware Error Handler
      │
│  ✓ All tests passing                                        │
│  ✓ No uncommitted changes                                   │
│  ✓ Database migrations ready                                │
│  ✓ Environment variables set                                │
│  ✓ SSL certificates valid                                   │
│  ✓ Dependencies up to date                                  │
│                                                             │
│  Step 2: Backup Current State                               │
│  ────────────────────────────                               │
│  ✓ Backup database                                          │
│  ✓ Backup configuration files                               │
│  ✓ Backup uploaded files                                    │
│  ✓ Create restore point                                     │
│                                                             │
│  Step 3: Build Production Assets                            │
│  ─────────────────────────────
──                            │
│  ✓ Build frontend (minified)                                │
│  ✓ Build backend (optimized)                                │
│  ✓ Compile assets                                           │
│  ✓ Generate static files                                    │
│                                                             │
│  Step 4: Database Setup                                     │
│  ─────────────────────                                      │
│  ✓ Run migrations                                           │
│  ✓ Create admin user                                        │
│  ✓ Set up initial data                                      │
│  ✓ Verify database integrity                                │
│                                                             │
│  Step 5: Security Hardening                                 │
│  ──────────────────────                                     │
│  ✓ Enable HTTPS                                             │
│  ✓ Set
e = config['database']['name']
   frontend_port = config['ports']['frontend']
   
   # Never hardcode values
   # ❌ APP_NAME = "Gaara ERP"
   # ✓ APP_NAME = config['project']['name']
   ```

3. **Respect project phase:**
   ```python
   if config['project']['phase'] == 'development':
       # Development behavior
       enable_debug_mode()
       allow_sample_data()
       relaxed_security()
   else:
       # Production behavior
       disable_debug_mode()
       strict_security()
       enable_monitoring()
   ```

---

### 64.10 Commands Reference

**Development Phase:**

```bash
# Database
reset-db              # Drop and recreate database
seed-data             # Add sample data
migrate-db            # Run migrations
backup-db             # Create backup

# Development
dev-server            # Start development server
hot-reload            # Enable hot reload
clear-cache           # Clear all caches
run-tests             # Run test suite

# Deployment
start deploy          # Begin dep

================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```bash
#!/bin/bash
# scripts/fix_line_length.sh

echo "Fixing line length..."

# Install tools
pip install autopep8 black isort

# Fix Python files
autopep8 --in-place --aggressive --aggressive \
  --max-line-length=120 \
  --recursive \
  --exclude=venv,.venv,migrations \
  .

black --line-length=120 .
isort --profile=black --line-length=120 .

echo "✅ Line length fixed"
```

```python
# backend/src/setup/wizard.py
from flask import Blueprint, render_template, request, redirect, session
from .validators import validate_admin_user, validate_db_config, validate_smtp

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

@setup_bp.route('/wizard', methods=['GET', 'POST'])
def wizard():
    step = request.args.get('step', '1')
    
    if request.method == 'POST':
        if step == '1':
            # Requirements check passed
            return redirect('/setup/wizard?step=2')
        
        elif step == '2':
            # Create admin user
            email = request.form['email']
            password = request.form['password']
            
            if validate_admin_user(email, password):
                create_admin_user(email, password)
                return redirect('/setup/wizard?step=3')
            else:
                return render_template('setup/step2.html', error="Invalid input")
        
        elif step == '3':
            # Database config
            db_config = {
                'host': request.form['host'],
                'port': request.form['port'],
                'database': request.form['database'],
                'username': request.form['username'],
                'password': request.form['password'],
            }
            
            if validate_db_config(db_config):
                save_db_config(db_config)
                return redirect('/setup/wizard?step=4')
            else:
                return render_template('setup/step3.html', error="Connection failed")
        
        # ... more steps ...
        
        elif step == '6':
            # Complete setup
            mark_setup_complete()
            session.pop('needs_setup', None)
            return redirect('/login')
    
    return render_template(f'setup/step{step}.html')
```

```python
# scripts/validate_env.py
import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Define required variables
REQUIRED_VARS = {
    'APP_ENV': {
        'required': True,
        'allowed_values': ['development', 'staging', 'production'],
        'description': 'Application environment'
    },
    'SECRET_KEY': {
        'required': True,
        'min_length': 32,
        'description': 'Application secret key'
    },
    'JWT_SECRET_KEY': {
        'required': True,
        'min_length': 32,
        'description': 'JWT secret key'
    },
    'DB_HOST': {
        'required': True,
        'description': 'Database host'
    },
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
        return 0
    else:
        print(f"❌ Validation failed with {len(result['errors'])} error(s)")
        print()
        print("Please fix the errors above and run validation again.")
        print("See .env.example for reference.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

```python
from sqlalchemy import Column, Integer, String
from database import db
from services.auth import hash_password
```

```python
import os
import sys

def get_port(env_var: str, default: int) -> int:
    """Get port from environment with validation"""
    try:
        port = int(os.getenv(env_var, default))
    except ValueError:
        print(f"ERROR: Invalid {env_var}. Must be integer.")
        sys.exit(1)
    
    if not (1024 <= port <= 65535):
        print(f"ERROR: {env_var}={port} invalid. Must be 1024-65535.")
        sys.exit(1)
    
    return port

BACKEND_PORT = get_port('BACKEND_PORT', 8000)
FRONTEND_PORT = get_port('FRONTEND_PORT', 3000)
DATABASE_PORT = get_port('DATABASE_PORT', 5432)
REDIS_PORT = get_port('REDIS_PORT', 6379)

# Conflict detection
ports = {
    'BACKEND': BACKEND_PORT,
    'FRONTEND': FRONTEND_PORT,
    'DATABASE': DATABASE_PORT,
    'REDIS': REDIS_PORT,
}

if len(set(ports.values())) != len(ports):
    print("ERROR: Port conflicts detected")
    sys.exit(1)
```

```python
def validate_order_data(order_data: Dict) -> None:
    """Validate order data."""
    if not order_data.get('customer_id'):
        raise ValueError("Missing customer")

def calculate_order_total(items: List[Dict]) -> Decimal:
    """Calculate order total with tax."""
    subtotal = sum(Decimal(str(item['price'])) * item['qty'] for item in items)
    tax = subtotal * Decimal('0.15')
    return subtotal + tax

def create_order(customer_id: int, total: Decimal) -> Order:
    """Create order in database."""
    return Order.objects.create(customer_id=customer_id, total=total)

def send_order_confirmation(order: Order) -> None:
    """Send order confirmation email."""
    send_email(order.customer.email, f"Order {order.id} confirmed")

def process_order(order_data: Dict) -> Order:
    """Process complete order workflow."""
    validate_order_data(order_data)
    total = calculate_order_total(order_data['items'])
    order = create_order(order_data['customer_id'], total)
    send_order_confirmation(order)
    return order
```

```python
# config/__init__.py
"""
File: config/__init__.py
Configuration package with explicit exports
"""

# Explicit imports - clear and maintainable
from .settings import Settings, DatabaseConfig
from .constants import (
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    API_VERSION
)
from .validators import validate_config, ConfigError

# Explicit __all__ definition
__all__ = [
    # Settings
    'Settings',
    'DatabaseConfig',
    # Constants
    'DEFAULT_TIMEOUT',
    'MAX_RETRIES',
    'API_VERSION',
    # Validators
    'validate_config',
    'ConfigError',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Your Team'
```

```python
# ✅ CORRECT ORDER in __init__.py

# 1. Standard library imports
import os
import sys
from typing import Dict, List

# 2. Third-party imports
import requests
from sqlalchemy import create_engine

# 3. Local imports - order matters!
from .exceptions import ConfigError  # No dependencies
from .constants import DEFAULT_CONFIG  # Uses exceptions
from .validators import validate  # Uses constants and exceptions
from .config import Config  # Uses all above

# 4. __all__ definition
__all__ = [
    'Config',
    'ConfigError',
    'DEFAULT_CONFIG',
    'validate',
]
```

```python
   admin_user = {
       "username": config["admin"]["username"],
       "email": config["admin"]["email"],
       "password": generate_secure_password(),
       "is_superuser": True,
       "is_staff": True
   }
   ```

2. **Open Admin Panel:**
   ```python
   admin_url = f"http://{config['environment']['host']}:{config['ports']['backend']}/admin"
   webbrowser.open(admin_url)
   ```

3. **Open Setup Wizard:**
   ```python
   setup_url = f"http://{config['environment']['host']}:{config['ports']['frontend']}/setup"
   webbrowser.open(setup_url)
   ```

4. **Display Credentials:**
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║                  ADMIN CREDENTIALS                         ║
   ╚════════════════════════════════════════════════════════════╝
   
   Admin Panel: http://{HOST}:{BACKEND_PORT}/admin
   
   Username: {ADMIN_USERNAME}
   Password: {GENERATED_PASSWORD}
   
   ⚠️  IMPORTANT: Save these credentials securely!
   ⚠️  Change the password after first login.
   
   Setup Wizard: http://{HOST}:{FRONTEND_PORT}/setup
   
   Follow the setup wizard to:
   - Configure application settings
   - Set up database connections
   - Configure email settings
   - Set up payment gateways (if applicable)
   - Configure integrations
   ```

---

### 64.8 Setup Wizard Flow

**After deployment, setup wizard guides through:**

```

```python
   if not os.path.exists('.global/project_config.json'):
       # Ask all questions
       collect_project_info()
   else:
       # Load existing config
       config = load_config()
       print(f"Loaded config for: {config['project']['name']}")
       print(f"Phase: {config['project']['phase']}")
   ```

2. **Use config throughout:**
   ```python
   # Always use config values
   project_name = config['project']['name']
   db_name = config['database']['name']
   frontend_port = config['ports']['frontend']
   
   # Never hardcode values
   # ❌ APP_NAME = "Gaara ERP"
   # ✓ APP_NAME = config['project']['name']
   ```

3. **Respect project phase:**
   ```python
   if config['project']['phase'] == 'development':
       # Development behavior
       enable_debug_mode()
       allow_sample_data()
       relaxed_security()
   else:
       # Production behavior
       disable_debug_mode()
       strict_security()
       enable_monitoring()
   ```

---

### 64.10 Commands Reference

**Development Phase:**

```

