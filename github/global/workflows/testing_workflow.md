# Testing Workflow

**Version:** 2.0.0  
**Last Updated:** 2026-01-16

---

## Testing Pyramid

```
         /\
        /  \
       / E2E \        Few, slow, expensive
      /______\
     /        \
    /Integration\     Some, medium
   /____________\
  /              \
 /   Unit Tests   \   Many, fast, cheap
/________________\
```

---

## Test Types

### Unit Tests

**Purpose:** Test individual functions/components  
**Location:** 
- Backend: `backend/tests/`
- Frontend: `frontend/src/tests/`

**Run:**
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

---

### Integration Tests

**Purpose:** Test component interactions  
**Location:** `backend/tests/integration/`

**Run:**
```bash
pytest tests/integration/ -v
```

---

### E2E Tests

**Purpose:** Test user flows  
**Location:** `e2e/tests/`

**Run:**
```bash
cd e2e
npm test               # All tests
npm run test:auth      # Auth only
npm run test:pos       # POS only
npm run test:security  # Security
```

---

### Performance Tests

**Purpose:** Test response times and load  
**Location:** `e2e/tests/performance.spec.ts`

**Run:**
```bash
npm run test:performance
```

**Thresholds:**
- Page load < 3000ms
- API response < 1000ms
- LCP < 2500ms

---

### Security Tests

**Purpose:** Test security vulnerabilities  
**Location:** `e2e/tests/security.spec.ts`

**Run:**
```bash
npm run test:security
```

**Checks:**
- XSS prevention
- SQL injection
- CSRF protection
- Auth bypass attempts

---

## Test Coverage

### Requirements
- Backend: 80%+ coverage
- Frontend: 80%+ coverage
- Critical paths: 100%

### Check Coverage
```bash
# Backend
pytest --cov=src --cov-report=html

# Frontend
npm run test:coverage
```

---

## Writing Tests

### Unit Test Template
```python
def test_function_name_expected_behavior():
    # Arrange
    input_data = {...}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### E2E Test Template
```typescript
test.describe('Feature', () => {
  test.beforeEach(async ({ page }) => {
    // Setup
  });

  test('should do something', async ({ page }) => {
    // Actions
    await page.goto('/path');
    await page.click('button');
    
    // Assertions
    await expect(page.getByText('Result')).toBeVisible();
  });
});
```

---

## Test Data

### Fixtures
- Use factory functions for test data
- Clean up after tests
- Isolate tests from each other

### Mock Data
- Use realistic data
- Include edge cases
- Test Arabic/RTL content

---

## CI/CD Integration

### On Pull Request
1. Unit tests run
2. Lint checks
3. Build verification

### On Merge to Develop
1. All unit tests
2. Integration tests
3. Deploy to staging
4. E2E tests on staging

### On Release
1. Full test suite
2. Security scan
3. Performance benchmark
4. Manual QA sign-off

---

## Debugging Failed Tests

1. Check test output
2. Review recent changes
3. Run test in isolation
4. Use debug mode: `npm run test:debug`
5. Check test environment
6. Verify test data
