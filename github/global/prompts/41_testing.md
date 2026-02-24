# Prompt 41: Testing — Unit, Integration, E2E

=================================================================================
TESTING - Unit, Integration, E2E
=================================================================================

Version: 5.0.0
Type: Quality Assurance - Testing

Comprehensive testing strategies and implementations.

=================================================================================
UNIT TESTING
=================================================================================

## Python (pytest)

```python
import pytest
from myapp.models import Product

def test_product_creation():
    product = Product(name="Laptop", price=999.99)
    assert product.name == "Laptop"
    assert product.price == 999.99

def test_product_discount():
    product = Product(name="Laptop", price=1000)
    discounted_price = product.apply_discount(10)
    assert discounted_price == 900

def test_invalid_price():
    with pytest.raises(ValueError):
        Product(name="Laptop", price=-100)

@pytest.fixture
def sample_product():
    return Product(name="Test Product", price=100)

def test_with_fixture(sample_product):
    assert sample_product.price == 100
```

## JavaScript (Jest)

```javascript
describe('Product', () => {
  test('creates product correctly', () => {
    const product = new Product('Laptop', 999.99);
    expect(product.name).toBe('Laptop');
    expect(product.price).toBe(999.99);
  });

  test('applies discount correctly', () => {
    const product = new Product('Laptop', 1000);
    const discounted = product.applyDiscount(10);
    expect(discounted).toBe(900);
  });

  test('throws error for invalid price', () => {
    expect(() => {
      new Product('Laptop', -100);
    }).toThrow('Price must be positive');
  });
});
```

=================================================================================
INTEGRATION TESTING
=================================================================================

## API Testing (FastAPI)

```python
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/api/products/",
        json={"name": "Laptop", "price": 999.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert "id" in data

def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_authentication_required():
    response = client.get("/api/admin/")
    assert response.status_code == 401
```

## Database Testing

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    
    retrieved = db_session.query(User).filter_by(email="test@example.com").first()
    assert retrieved is not None
    assert retrieved.email == "test@example.com"
```

=================================================================================
E2E TESTING
=================================================================================

## Playwright (Python)

```python
from playwright.sync_api import Page, expect

def test_login_flow(page: Page):
    page.goto("http://localhost:3000/login")
    
    page.fill('input[name="email"]', "user@example.com")
    page.fill('input[name="password"]', "password123")
    page.click('button[type="submit"]')
    
    expect(page).to_have_url("http://localhost:3000/dashboard")
    expect(page.locator("h1")).to_contain_text("Dashboard")

def test_create_product(page: Page):
    page.goto("http://localhost:3000/products/new")
    
    page.fill('input[name="name"]', "New Product")
    page.fill('input[name="price"]', "99.99")
    page.click('button[type="submit"]')
    
    expect(page.locator(".success-message")).to_be_visible()
```

## Cypress (JavaScript)

```javascript
describe('Login Flow', () => {
  it('logs in successfully', () => {
    cy.visit('/login');
    
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    
    cy.url().should('include', '/dashboard');
    cy.get('h1').should('contain', 'Dashboard');
  });
});
```

=================================================================================
TEST COVERAGE
=================================================================================

## Python (pytest-cov)

```bash
pip install pytest-cov
pytest --cov=myapp --cov-report=html
```

## JavaScript (Jest)

```json
{
  "scripts": {
    "test": "jest --coverage"
  },
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.{js,jsx,ts,tsx}",
      "!src/**/*.test.{js,jsx,ts,tsx}"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

=================================================================================
MOCKING
=================================================================================

## Python

```python
from unittest.mock import Mock, patch

def test_api_call():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"data": "test"}
        mock_get.return_value.status_code = 200
        
        result = fetch_data_from_api()
        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

## JavaScript

```javascript
jest.mock('./api');

test('fetches data from API', async () => {
  const mockData = { data: 'test' };
  api.fetchData.mockResolvedValue(mockData);
  
  const result = await getData();
  expect(result).toEqual(mockData);
  expect(api.fetchData).toHaveBeenCalledTimes(1);
});
```

=================================================================================
TEST ORGANIZATION
=================================================================================

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_services.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
├── e2e/
│   ├── test_login.py
│   └── test_checkout.py
└── conftest.py  # Shared fixtures
```

=================================================================================
END OF TESTING PROMPT
=================================================================================


================================================================================
RECOVERED CONTENT FROM Global System v26 Diamond 32 (Phase 2)
================================================================================

shared', 'core']
    functions = []
    
    for dir_name in shared_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob('*.py'):
            if py_file.name.startswith('test_'):
                continue
            
            with open(py_file) as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Public functions only
                        functions.append((str(py_file), node.name))
    
    return functions

def check_documented(functions):
    """Check if functions are documented in function_reference.md"""
    ref_file = Path('docs/function_reference.md')
    if not ref_file.exists():
        print("❌ docs/function_reference.md not found!")
        return False
    
    with open(ref_file) as f:
        content = f.read()
    
    un
                    PROJECT STATES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DEVELOPMENT                                             │
│     ├─ Active development                                   │
│     ├─ Testing enabled                                      │
│     ├─ Debug mode ON                                        │
│     ├─ Sample data available                                │
│     ├─ Hot reload enabled                                   │
│     └─ Detailed logging                                     │
│                                                             │
│  2. STAGING (Optional)                                      │
│     ├─ Pre-production testing                               │
│     ├─ Production-like environment                          │
│     ├─ Performance testing                                  │
│     └─ Final QA                          
elligent chatbots
8. ✅ **Charity Management** - Donation platforms
9. ✅ **AI Prediction** - Forecasting systems

**Benefits:**

✅ **Rapid development** - Start projects in minutes  
✅ **Best practices** - Production-ready code  
✅ **Fully documented** - Complete guides  
✅ **Customizable** - Easy to modify  
✅ **Tested** - All templates tested

**Augment can now generate complete projects instantly!** 🚀

---

**Section Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Templates Count:** 9



================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```bash
#!/bin/bash
# Comprehensive verification script

set -e

echo "🔍 Running comprehensive verification..."

# 1. Code style
echo "📝 Checking code style..."
black --check --line-length=120 . || exit 1
isort --check-only --profile=black . || exit 1

# 2. Linting
echo "🔎 Linting..."
flake8 . --max-line-length=120 --extend-ignore=E203 || exit 1
pylint --max-line-length=120 --disable=C0111 . || exit 1

# 3. Type checking
echo "🔢 Type checking..."
mypy --strict --ignore-missing-imports . || exit 1

# 4. Security
echo "🔒 Security checks..."
bandit -r . -f json -o bandit-report.json || exit 1
safety check || exit 1

# 5. Complexity
echo "📊 Complexity analysis..."
radon cc . -a -s -n C || exit 1
radon mi . -s -n B || exit 1

# 6. Dead code
echo "💀 Dead code detection..."
vulture . --min-confidence 80 || exit 1

# 7. Tests
echo "🧪 Running tests..."
pytest --cov=. --cov-report=term --cov-report=html --cov-fail-under=80 || exit 1

# 8. Line length check
echo "📏 Checking line length..."
bash scripts/fix_line_length.sh --check || exit 1

# 9. Unused imports
echo "🗑️  Checking unused imports..."
bash scripts/remove_unused.sh --check || exit 1

echo "✅ All verification checks passed!"
```

```python
#!/usr/bin/env python3
"""Check that all shared functions are documented in function_reference.md"""

import ast
import sys
from pathlib import Path

def find_shared_functions():
    """Find all functions in shared/common modules."""
    shared_dirs = ['utils', 'common', 'shared', 'core']
    functions = []
    
    for dir_name in shared_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob('*.py'):
            if py_file.name.startswith('test_'):
                continue
            
            with open(py_file) as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Public functions only
                        functions.append((str(py_file), node.name))
    
    return functions

def check_documented(functions):
    """Check if functions are documented in function_reference.md"""
    ref_file = Path('docs/function_reference.md')
    if not ref_file.exists():
        print("❌ docs/function_reference.md not found!")
        return False
    
    with open(ref_file) as f:
        content = f.read()
    
    undocumented = []
    for file_path, func_name in functions:
        if f"`{func_name}`" not in content:
            undocumented.append(f"{file_path}::{func_name}")
    
    if undocumented:
        print("❌ Undocumented functions found:")
        for func in undocumented:
            print(f"  - {func}")
        print("\nPlease add them to docs/function_reference.md")
        return False
    
    print("✅ All shared functions are documented")
    return True

if __name__ == '__main__':
    functions = find_shared_functions()
    if not check_documented(functions):
        sys.exit(1)
```

```python
#!/usr/bin/env python3
"""Check code for known error patterns from error log."""

import re
import sys
from pathlib import Path

def load_error_patterns():
    """Load error patterns from error log."""
    error_file = Path('docs/errors/DONT_MAKE_THESE_ERRORS_AGAIN.md')
    if not error_file.exists():
        return []
    
    patterns = []
    with open(error_file) as f:
        content = f.read()
    
    # Extract code patterns that caused errors
    # This is a simplified example
    pattern_blocks = re.findall(r'```python\n# WRONG:(.*?)```', content, re.DOTALL)
    for block in pattern_blocks:
        patterns.append(block.strip())
    
    return patterns

def check_files_for_patterns(patterns):
    """Check Python files for error patterns."""
    issues_found = False
    
    for py_file in Path('.').rglob('*.py'):
        if 'test_' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        with open(py_file) as f:
            content = f.read()
        
        for pattern in patterns:
            if pattern in content:
                print(f"⚠️  Known error pattern found in {py_file}")
                print(f"   Pattern: {pattern[:50]}...")
                issues_found = True
    
    return issues_found

if __name__ == '__main__':
    patterns = load_error_patterns()
    if check_files_for_patterns(patterns):
        print("\n❌ Known error patterns detected!")
        print("   Check docs/errors/DONT_MAKE_THESE_ERRORS_AGAIN.md")
        sys.exit(1)
    
    print("✅ No known error patterns found")
```

```python
"""
File: tests/unit/test_order_service.py
Module: tests.unit.test_order_service
Created: 2025-01-15
Author: Team
Description: Unit tests for order service
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from services.order_service import OrderService

class TestOrderService:
    """Test OrderService class."""
    
    @pytest.fixture
    def order_service(self):
        """Create OrderService instance."""
        return OrderService()
    
    @pytest.fixture
    def sample_order_data(self):
        """Sample order data."""
        return {
            'customer_id': 1,
            'items': [
                {'price': '10.00', 'qty': 2},
                {'price': '5.00', 'qty': 3}
            ]
        }
    
    def test_calculate_total_success(self, order_service, sample_order_data):
        """Test successful total calculation."""
        total = order_service.calculate_total(sample_order_data['items'])
        expected = Decimal('35.00') * Decimal('1.15')  # With 15% tax
        assert total == expected
    
    def test_calculate_total_empty_items(self, order_service):
        """Test calculation with empty items."""
        with pytest.raises(ValueError, match="Items list cannot be empty"):
            order_service.calculate_total([])
    
    @patch('services.order_service.Order.objects.create')
    def test_create_order(self, mock_create, order_service, sample_order_data):
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

```python
"""
File: tests/frontend/test_login.py
Module: tests.frontend.test_login
Created: 2025-01-15
Author: Team
Description: Frontend tests for login functionality
"""

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page(browser):
    """Create new page for each test."""
    page = browser.new_page()
    yield page
    page.close()

def test_login_success(page: Page):
    """Test successful login."""
    # Navigate
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    # Fill form
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'testpass123')
    
    # Submit
    page.click('button[type="submit"]')
    
    # Verify redirect
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # Verify welcome message
    expect(page.locator('text=Welcome, testuser')).to_be_visible()

def test_login_invalid_credentials(page: Page):
    """Test login with invalid credentials."""
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    page.fill('input[name="username"]', 'invalid')
    page.fill('input[name="password"]', 'wrong')
    page.click('button[type="submit"]')
    
    # Should show error
    expect(page.locator('text=Invalid credentials')).to_be_visible()
    
    # Should stay on login page
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/login")

def test_login_validation(page: Page):
    """Test form validation."""
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    # Try to submit empty form
    page.click('button[type="submit"]')
    
    # Should show validation errors
    expect(page.locator('text=Username is required')).to_be_visible()
    expect(page.locator('text=Password is required')).to_be_visible()
```

```python
"""
File: tests/frontend/test_dashboard_selenium.py
Module: tests.frontend.test_dashboard_selenium
Created: 2025-01-15
Author: Team
Description: Selenium tests for dashboard
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Create WebDriver instance."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_dashboard_loads(driver):
    """Test dashboard page loads correctly."""
    driver.get("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # Wait for page load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )
    
    # Check title
    assert "Dashboard" in driver.title
    
    # Check key elements
    assert driver.find_element(By.ID, "user-menu")
    assert driver.find_element(By.CLASS_NAME, "stats-widget")

def test_dashboard_navigation(driver):
    """Test navigation from dashboard."""
    driver.get("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # Click on Orders link
    orders_link = driver.find_element(By.LINK_TEXT, "Orders")
    orders_link.click()
    
    # Should navigate to orders page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/orders")
    )
    
    assert "/orders" in driver.current_url
```

```python
"""
File: tests/integration/test_order_api.py
Module: tests.integration.test_order_api
Created: 2025-01-15
Author: Team
Description: Integration tests for order API
"""

import pytest
from django.test import Client
from decimal import Decimal
from models import Order, Customer

@pytest.fixture
def client():
    """Create test client."""
    return Client()

@pytest.fixture
def customer(db):
    """Create test customer."""
    return Customer.objects.create(
        name="Test Customer",
        email="test@example.com"
    )

@pytest.mark.django_db
def test_create_order_api(client, customer):
    """Test order creation via API."""
    data = {
        'customer_id': customer.id,
        'items': [
            {'product_id': 1, 'quantity': 2, 'price': '10.00'},
            {'product_id': 2, 'quantity': 1, 'price': '15.00'}
        ]
    }
    
    response = client.post('/api/orders/', data, content_type='application/json')
    
    assert response.status_code == 201
    assert 'id' in response.json()
    
    # Verify in database
    order = Order.objects.get(id=response.json()['id'])
    assert order.customer == customer
    assert order.total == Decimal('40.25')  # (20 + 15) * 1.15 tax
```

```python
"""
File: tests/e2e/test_order_workflow.py
Module: tests.e2e.test_order_workflow
Created: 2025-01-15
Author: Team
Description: End-to-end test for complete order workflow
"""

import pytest
from playwright.sync_api import Page, expect

def test_complete_order_workflow(page: Page):
    """Test complete order creation workflow."""
    # 1. Login
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # 2. Navigate to orders
    page.click('text=Orders')
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/orders")
    
    # 3. Create new order
    page.click('button:has-text("New Order")')
    expect(page.locator('h1:has-text("Create Order")')).to_be_visible()
    
    # 4. Fill order form
    page.select_option('select[name="customer"]', label='Test Customer')
    page.click('button:has-text("Add Item")')
    page.select_option('select[name="items[0].product"]', label='Product A')
    page.fill('input[name="items[0].quantity"]', '2')
    
    # 5. Submit order
    page.click('button[type="submit"]:has-text("Create Order")')
    
    # 6. Verify success
    expect(page.locator('text=Order created successfully')).to_be_visible()
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/orders")
    
    # 7. Verify order appears in list
    expect(page.locator('table tbody tr').first).to_contain_text('Test Customer')
```

```python
"""
File: tests/integration/test_order_integration.py
Module: tests.integration.test_order_integration
Created: 2025-01-15
Author: Team
Description: Integration tests for complete order workflow
"""

import pytest
from django.test import Client
from models import Order, Customer

@pytest.mark.django_db
class TestOrderIntegration:
    """Test complete order integration."""
    
    def test_order_workflow(self, client: Client):
        """Test complete order workflow from design spec."""
        # 1. Create customer
        customer = Customer.objects.create(name="Test", email="test@example.com")
        
        # 2. Create order via API
        response = client.post('/api/orders/', {
            'customer_id': customer.id,
            'items': [{'product_id': 1, 'quantity': 2}]
        }, content_type='application/json')
        assert response.status_code == 201
        order_id = response.json()['id']
        
        # 3. Retrieve order
        response = client.get(f'/api/orders/{order_id}/')
        assert response.status_code == 200
        assert response.json()['state'] == 'draft'
        
        # 4. Confirm order
        response = client.post(f'/api/orders/{order_id}/confirm/')
        assert response.status_code == 200
        
        # 5. Verify state changed
        order = Order.objects.get(id=order_id)
        assert order.state == 'confirmed'
        
        # 6. Cancel order
        response = client.post(f'/api/orders/{order_id}/cancel/')
        assert response.status_code == 200
        
        # 7. Verify cancelled
        order.refresh_from_db()
        assert order.state == 'cancelled'
```

```python
# tests/test_package_init.py
"""Test package __init__.py structure"""

import mypackage


def test_public_api_available():
    """Test that public API is accessible"""
    assert hasattr(mypackage, 'PublicClass')
    assert hasattr(mypackage, 'public_function')


def test_private_not_exposed():
    """Test that private items are not in public API"""
    assert not hasattr(mypackage, '_private_helper')


def test_all_defined():
    """Test that __all__ is properly defined"""
    assert hasattr(mypackage, '__all__')
    assert isinstance(mypackage.__all__, list)
    assert len(mypackage.__all__) > 0


def test_all_items_exist():
    """Test that all items in __all__ actually exist"""
    for item in mypackage.__all__:
        assert hasattr(mypackage, item), f"{item} in __all__ but not found"


def test_version_available():
    """Test that version info is available"""
    assert hasattr(mypackage, '__version__')
    assert isinstance(mypackage.__version__, str)


def test_no_import_side_effects():
    """Test that importing doesn't have side effects"""
    import sys
    import importlib
    
    # Remove module if already imported
    if 'mypackage' in sys.modules:
        del sys.modules['mypackage']
    
    # Import should not raise or print anything
    import mypackage  # noqa: F401
```

