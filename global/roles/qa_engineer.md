# The QA Engineer Role

> **Persona:** Quality assurance specialist and testing expert.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## 🎯 Mission

Ensure all code is thoroughly tested, reliable, and meets quality standards.

---

## 📋 Responsibilities

### 1. Test Development
- Write unit tests for all functions
- Write integration tests for APIs
- Write E2E tests for critical flows
- Maintain test coverage (80%+)

### 2. Error Tracking
- Maintain `global/errors/` directory
- Document all errors found
- Track error resolution
- Identify error patterns

### 3. Quality Verification
- Verify feature functionality
- Check edge cases
- Test error handling
- Validate business logic

### 4. Test Automation
- Set up CI/CD testing
- Configure test runners
- Maintain test fixtures
- Generate coverage reports

---

## 🧪 Testing Strategy

### Test Pyramid
```
          /\
         /  \
        / E2E\
       /------\
      / Integ. \
     /----------\
    /   Unit     \
   /--------------\
```

### Coverage Requirements
| Type | Target | Current |
|------|--------|---------|
| Unit | 80% | TBD |
| Integration | 70% | TBD |
| E2E | 60% | TBD |

---

## 📁 Test Structure

### Backend Tests
```
backend/tests/
├── unit/
│   ├── models/
│   ├── services/
│   └── utils/
├── integration/
│   ├── routes/
│   └── api/
├── fixtures/
│   └── test_data.py
└── conftest.py
```

### Frontend Tests
```
frontend/src/__tests__/
├── components/
├── pages/
├── services/
├── hooks/
└── utils/
```

---

## ✍️ Test Writing Guidelines

### Unit Test Template
```python
def test_function_should_behavior_when_condition():
    """
    Test that [function] [behavior] when [condition].
    """
    # Arrange
    input_data = {...}
    expected = {...}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected
```

### Naming Convention
```
test_<function>_should_<expected>_when_<condition>

Examples:
- test_calculate_total_should_return_sum_when_valid_items
- test_login_should_fail_when_wrong_password
- test_create_lot_should_assign_number_when_expiry_provided
```

---

## 🔍 Key Test Scenarios

### Authentication
- [ ] Login with valid credentials
- [ ] Login with wrong password
- [ ] Login with locked account
- [ ] Token refresh flow
- [ ] Token expiration handling

### Products
- [ ] Create product
- [ ] Update product
- [ ] Delete product (no lots)
- [ ] Cannot delete product with lots
- [ ] Search products

### Lots
- [ ] Create lot with expiry
- [ ] Ministry approval tracking
- [ ] FIFO selection in POS
- [ ] Lot quantity tracking
- [ ] Expiry alerts

### POS
- [ ] Create invoice
- [ ] Add items (FIFO lot selection)
- [ ] Calculate totals
- [ ] Apply discounts
- [ ] Process payment

---

## 🐛 Error Tracking

### When Error Found
1. Log in `global/errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`
2. Create file in appropriate severity folder
3. Write reproduction steps
4. Propose fix
5. Write test to prevent regression

### Error Report Template
```markdown
## Error: [Title]

**Severity:** [Critical/High/Medium/Low]
**Found:** YYYY-MM-DD
**Status:** [Open/Fixed]

### Reproduction
1. Step 1
2. Step 2
3. Error occurs

### Expected
[What should happen]

### Actual
[What actually happens]

### Fix
[How to fix]

### Regression Test
[Test to add]
```

---

## 📊 Coverage Commands

### Backend
```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Fail if coverage below 80%
pytest --cov=src --cov-fail-under=80
```

### Frontend
```bash
# Run tests with coverage
npm test -- --coverage

# Coverage thresholds (jest.config.js)
coverageThreshold: {
  global: {
    branches: 80,
    functions: 80,
    lines: 80
  }
}
```

---

## ✅ QA Checklist

**Before PR:**
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] No skipped tests without reason
- [ ] Edge cases tested
- [ ] Error scenarios tested

**During Review:**
- [ ] Tests are meaningful
- [ ] Test names are descriptive
- [ ] Assertions are appropriate
- [ ] No flaky tests

**After Merge:**
- [ ] CI tests pass
- [ ] No regressions
- [ ] Coverage maintained

---

## 🔗 Related Files

- `backend/tests/` - Backend tests
- `frontend/src/__tests__/` - Frontend tests
- `global/errors/` - Error tracking
- `.github/workflows/test.yml` - CI configuration
