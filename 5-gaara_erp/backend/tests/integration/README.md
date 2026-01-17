# Integration Tests

Integration tests for the Store ERP API that test the full stack with a real database.

## Overview

Integration tests verify that different components of the system work together correctly:
- Database operations
- API endpoints
- Business logic
- Data validation
- Transactions

## Setup

### 1. Install Dependencies

```bash
pip install pytest pytest-cov
```

### 2. Database Setup

Integration tests use an in-memory SQLite database by default. For testing with PostgreSQL:

```bash
# Set test database URL
export TEST_DATABASE_URL="postgresql://user:password@localhost/test_db"
```

## Running Tests

### Run All Integration Tests

```bash
cd backend
python -m pytest tests/integration/ -v
```

### Run Specific Test File

```bash
python -m pytest tests/integration/test_api_integration.py -v
```

### Run Specific Test Class

```bash
python -m pytest tests/integration/test_api_integration.py::TestAuthIntegration -v
```

### Run Specific Test

```bash
python -m pytest tests/integration/test_api_integration.py::TestAuthIntegration::test_login_with_valid_credentials -v
```

### Run with Coverage

```bash
python -m pytest tests/integration/ --cov=src --cov-report=html -v
```

## Test Structure

### Fixtures

#### `test_app`
- **Scope:** Module
- **Purpose:** Creates test application with test database
- **Usage:** Automatically available in all tests

#### `client`
- **Scope:** Module
- **Purpose:** Creates test client for making HTTP requests
- **Usage:** Pass as parameter to test functions

#### `db_session`
- **Scope:** Function
- **Purpose:** Creates a new database session for each test
- **Usage:** Automatically rolls back after each test

#### `sample_user`
- **Purpose:** Creates a test user
- **Usage:** Use when testing authentication

#### `sample_category`
- **Purpose:** Creates a test category
- **Usage:** Use when testing products/inventory

#### `sample_warehouse`
- **Purpose:** Creates a test warehouse
- **Usage:** Use when testing inventory

#### `sample_product`
- **Purpose:** Creates a test product
- **Usage:** Use when testing products/invoices

## Test Classes

### TestAuthIntegration

Tests authentication functionality:
- Login with valid credentials
- Login with invalid credentials
- Login with nonexistent user

### TestProductsIntegration

Tests product management:
- List products
- List products with pagination
- Search products
- Filter products by category

### TestInventoryIntegration

Tests inventory management:
- List categories
- Create category
- List warehouses
- Create warehouse

### TestInvoicesIntegration

Tests invoice management:
- List invoices
- Filter invoices by type
- Filter invoices by status

## Writing Integration Tests

### Basic Test

```python
def test_my_feature(client, db_session):
    """Test my feature"""
    # Arrange: Create test data
    user = User(username='test', email='test@example.com')
    db_session.add(user)
    db_session.commit()
    
    # Act: Make API request
    response = client.get('/api/users')
    
    # Assert: Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) > 0
```

### Test with Authentication

```python
def test_protected_endpoint(client, sample_user):
    """Test protected endpoint"""
    # Login first
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.get_json()['access_token']
    
    # Make authenticated request
    response = client.get('/api/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
```

### Test with Multiple Records

```python
def test_pagination(client, db_session, sample_category):
    """Test pagination"""
    # Create multiple products
    for i in range(25):
        product = Product(
            name=f'Product {i}',
            sku=f'PROD-{i:03d}',
            category_id=sample_category.id,
            unit_price=100.00
        )
        db_session.add(product)
    db_session.commit()
    
    # Test first page
    response = client.get('/api/products?page=1&per_page=10')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 10
    assert data['pagination']['total'] >= 25
```

### Test Error Handling

```python
def test_invalid_input(client):
    """Test error handling for invalid input"""
    response = client.post('/api/products', json={
        'name': '',  # Invalid: empty name
        'price': -100  # Invalid: negative price
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data or 'errors' in data
```

## Best Practices

### 1. Use Fixtures

```python
@pytest.fixture
def sample_data(db_session):
    """Create sample data for tests"""
    # Create data
    yield data
    # Cleanup happens automatically with db_session rollback
```

### 2. Test Isolation

Each test should be independent:
- Don't rely on test execution order
- Use fixtures to create test data
- Use `db_session` fixture for automatic rollback

### 3. Descriptive Test Names

```python
# Good
def test_login_with_valid_credentials_returns_token(client):
    pass

# Bad
def test_login(client):
    pass
```

### 4. Arrange-Act-Assert Pattern

```python
def test_create_product(client, db_session):
    # Arrange: Set up test data
    product_data = {'name': 'Test', 'price': 100}
    
    # Act: Perform action
    response = client.post('/api/products', json=product_data)
    
    # Assert: Verify results
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Test'
```

### 5. Test Both Success and Failure

```python
def test_create_product_success(client):
    """Test successful product creation"""
    # Test happy path
    pass

def test_create_product_invalid_data(client):
    """Test product creation with invalid data"""
    # Test error handling
    pass
```

## Common Patterns

### Testing Pagination

```python
def test_pagination(client, db_session):
    # Create test data
    for i in range(25):
        db_session.add(Product(name=f'Product {i}'))
    db_session.commit()
    
    # Test first page
    response = client.get('/api/products?page=1&per_page=10')
    assert len(response.get_json()['items']) == 10
    
    # Test second page
    response = client.get('/api/products?page=2&per_page=10')
    assert len(response.get_json()['items']) == 10
```

### Testing Filtering

```python
def test_filtering(client, db_session):
    # Create test data with different attributes
    db_session.add(Product(name='A', category='electronics'))
    db_session.add(Product(name='B', category='furniture'))
    db_session.commit()
    
    # Test filter
    response = client.get('/api/products?category=electronics')
    items = response.get_json()['items']
    assert all(item['category'] == 'electronics' for item in items)
```

### Testing Search

```python
def test_search(client, db_session):
    # Create test data
    db_session.add(Product(name='Laptop'))
    db_session.add(Product(name='Phone'))
    db_session.commit()
    
    # Test search
    response = client.get('/api/products?search=Laptop')
    items = response.get_json()['items']
    assert any('Laptop' in item['name'] for item in items)
```

## Troubleshooting

### Database Connection Issues

```python
# Check database URL
print(app.config['SQLALCHEMY_DATABASE_URI'])

# Verify tables are created
with app.app_context():
    print(db.engine.table_names())
```

### Fixture Not Found

```python
# Make sure fixture is defined in conftest.py or same file
# Check fixture scope (function, class, module, session)
```

### Test Isolation Issues

```python
# Use db_session fixture for automatic rollback
def test_my_test(db_session):
    # Changes will be rolled back after test
    pass
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Integration Tests
  run: |
    cd backend
    python -m pytest tests/integration/ -v --cov=src --cov-report=xml
  env:
    DATABASE_URL: postgresql://postgres:postgres@localhost/test_db

- name: Upload Coverage
  uses: codecov/codecov-action@v2
  with:
    files: ./backend/coverage.xml
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html)

