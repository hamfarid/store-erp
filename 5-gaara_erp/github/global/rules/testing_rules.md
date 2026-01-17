# TESTING RULES (P1 - Must Follow)

**FILE**: github/global/rules/testing_rules.md | **PURPOSE**: Testing rules | **OWNER**: QA | **LAST-AUDITED**: 2025-11-18

## Overview

These are **mandatory** testing rules for production-ready code.

## 1. Minimum Coverage

### Rule
Achieve minimum 80% test coverage overall.

### Coverage Targets
- **Overall**: ≥80%
- **Critical Paths**: 100%
- **Services/Business Logic**: ≥90%
- **Models**: ≥90%
- **Routes/Controllers**: ≥80%
- **Utils**: ≥80%
- **UI Components**: ≥70%

### Enforcement
```bash
# Backend (Python)
pytest --cov=backend --cov-report=term --cov-fail-under=80

# Frontend (TypeScript)
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

## 2. Test Pyramid

### Rule
Follow the test pyramid distribution.

### Distribution
- **Unit Tests**: 70% (fast, isolated)
- **Integration Tests**: 20% (DB, APIs)
- **E2E Tests**: 10% (critical paths)

### Rationale
- Unit tests are fast and catch most bugs
- Integration tests verify components work together
- E2E tests verify critical user journeys

## 3. All Tests Must Pass

### Rule
All tests must pass before merging.

### ❌ Bad
```bash
# 5 tests passed, 2 failed
# Merging anyway... NO!
```

### ✅ Good
```bash
# All tests passed
# Safe to merge
```

### Enforcement
- CI pipeline blocks merge if tests fail
- No skipped tests without justification
- Fix failing tests immediately

## 4. Test Naming

### Rule
Use descriptive test names that explain what is being tested.

### ❌ Bad
```python
def test_user():
    pass

def test_1():
    pass
```

### ✅ Good
```python
def test_create_user_with_valid_data():
    """Test that a user can be created with valid data"""
    pass

def test_login_fails_with_invalid_password():
    """Test that login fails when password is incorrect"""
    pass
```

```typescript
describe('Button', () => {
  it('calls onClick when clicked', () => {
    // Test implementation
  });

  it('does not call onClick when disabled', () => {
    // Test implementation
  });
});
```

## 5. Test Independence

### Rule
Tests must be independent and not rely on execution order.

### ❌ Bad
```python
# Test 2 depends on Test 1
def test_create_user():
    global user_id
    user_id = create_user()

def test_get_user():
    # Depends on test_create_user running first
    user = get_user(user_id)
```

### ✅ Good
```python
@pytest.fixture
def created_user():
    user = create_user()
    yield user
    # Cleanup
    delete_user(user.id)

def test_create_user():
    user = create_user()
    assert user.id is not None

def test_get_user(created_user):
    user = get_user(created_user.id)
    assert user.id == created_user.id
```

## 6. Test Data

### Rule
Use fixtures or factories for test data. Don't hardcode.

### ❌ Bad
```python
def test_user():
    user = User(email="test@example.com", password="password123")
    # Hardcoded data
```

### ✅ Good
```python
@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }

def test_user(user_data):
    user = User(**user_data)
    assert user.email == user_data["email"]
```

```typescript
// Factory pattern
const createTestUser = (overrides = {}) => ({
  email: 'test@example.com',
  password: 'SecurePassword123!',
  role: 'user',
  ...overrides,
});

it('creates a user', () => {
  const user = createTestUser({ email: 'custom@example.com' });
  expect(user.email).toBe('custom@example.com');
});
```

## 7. Test Edge Cases

### Rule
Test edge cases, not just happy paths.

### Test Cases to Include
- ✅ Happy path (valid input)
- ✅ Invalid input
- ✅ Empty input
- ✅ Null/undefined
- ✅ Boundary values (min, max)
- ✅ Duplicate data
- ✅ Concurrent operations
- ✅ Error conditions

### Example
```python
class TestUserCreation:
    def test_create_user_with_valid_data(self):
        """Happy path"""
        pass

    def test_create_user_with_invalid_email(self):
        """Invalid input"""
        pass

    def test_create_user_with_empty_email(self):
        """Empty input"""
        pass

    def test_create_user_with_duplicate_email(self):
        """Duplicate data"""
        pass

    def test_create_user_with_weak_password(self):
        """Validation error"""
        pass
```

## 8. Mock External Dependencies

### Rule
Mock external dependencies (APIs, databases, file systems) in unit tests.

### ❌ Bad
```python
def test_get_weather():
    # Calls real API
    weather = get_weather_from_api("London")
    assert weather is not None
```

### ✅ Good
```python
from unittest.mock import Mock, patch

@patch('services.weather.requests.get')
def test_get_weather(mock_get):
    # Mock the API response
    mock_get.return_value.json.return_value = {"temp": 20}
    
    weather = get_weather_from_api("London")
    assert weather["temp"] == 20
```

```typescript
import { vi } from 'vitest';

it('fetches weather data', async () => {
  const mockFetch = vi.fn().mockResolvedValue({
    json: async () => ({ temp: 20 }),
  });
  global.fetch = mockFetch;

  const weather = await getWeather('London');
  expect(weather.temp).toBe(20);
});
```

## 9. Test Performance

### Rule
Include performance tests for critical operations.

### Example
```python
import time

def test_query_performance():
    """Test that query completes in under 100ms"""
    start = time.time()
    result = db.query(User).all()
    duration = (time.time() - start) * 1000
    
    assert duration < 100, f"Query took {duration}ms, expected <100ms"
```

## 10. Integration Tests

### Rule
Write integration tests for critical flows.

### Example
```python
def test_user_registration_flow(test_client):
    """Test complete user registration flow"""
    # 1. Register user
    response = test_client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePassword123!"
    })
    assert response.status_code == 201
    
    # 2. Verify email sent (mock)
    # ...
    
    # 3. Confirm email
    response = test_client.get(f"/api/auth/confirm/{token}")
    assert response.status_code == 200
    
    # 4. Login
    response = test_client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePassword123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 11. E2E Tests

### Rule
Write E2E tests for critical user journeys.

### Example (Playwright)
```typescript
import { test, expect } from '@playwright/test';

test('user can login and view dashboard', async ({ page }) => {
  // Navigate to login page
  await page.goto('http://localhost:3000/login');

  // Fill in credentials
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'SecurePassword123!');

  // Click login button
  await page.click('button[type="submit"]');

  // Verify redirect to dashboard
  await expect(page).toHaveURL('http://localhost:3000/dashboard');

  // Verify dashboard content
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

## 12. Test Documentation

### Rule
Document complex test logic.

### ✅ Good
```python
def test_payment_processing_with_retry():
    """
    Test payment processing with automatic retry on failure.
    
    Scenario:
    1. First payment attempt fails with network error
    2. System automatically retries after 1 second
    3. Second attempt succeeds
    4. User is charged only once
    """
    # Test implementation
```

## Automated Enforcement

### CI Pipeline
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run backend tests
        run: |
          cd backend
          pytest --cov=backend --cov-report=term --cov-fail-under=80
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

---

**Remember**: Tests are your safety net. Write them first, run them often, and never skip them.

