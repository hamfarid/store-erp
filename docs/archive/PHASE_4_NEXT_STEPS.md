# Phase 4 Continuation - Action Plan

## Status
**Current:** 170/260 tests passing (65.4%)  
**Target:** >80% pass rate (>200/260 tests)  
**Remaining work:** 30-45 minutes of focused fixes

## Next Work Items (Priority Order)

### 1. Fix Integration Test "Already Defined" Errors (22 errors)
**Time Estimate:** 15-20 minutes  
**Impact:** +20-25 tests

**Issue:**
```
sqlalchemy.exc.InvalidRequestError: index ix_suppliers_name already exists
```

**Root Cause:**
- Models still being loaded multiple times during app initialization
- Database doesn't properly reset between test classes

**Solution:**
1. Add explicit `app.config['SQLALCHEMY_ECHO'] = False` to prevent verbose logging
2. Use `app.app_context()` properly to isolate each test module
3. Call `db.drop_all()` between test modules
4. Consider using `app.teardown_appcontext()` fixture

**File to Modify:**
- `backend/tests/integration/test_api_integration.py` - Add module-level teardown
- `backend/src/database.py` - Verify model registration is idempotent

**Code Changes:**
```python
@pytest.fixture(scope='module', autouse=True)
def cleanup():
    """Cleanup between test modules"""
    yield
    # Cleanup after all tests in module
    db.session.remove()
    db.metadata.clear()
```

### 2. Fix API Test Infrastructure (25 errors - test_api_drift_*.py)
**Time Estimate:** 10-15 minutes  
**Impact:** +15-20 tests

**Issue:**
Tests can't make HTTP requests to Flask app

**Root Cause:**
- Test client created before app properly initialized
- Database in wrong state for test runs

**Solution:**
1. Use `client` fixture from `test_app` properly
2. Ensure `app.app_context()` is active during requests
3. Use `with app.test_client() as client:` pattern

**File to Modify:**
- `backend/tests/test_api_drift_*.py` - Multiple files

### 3. Fix Performance Test Fixtures (20 errors - test_api_performance.py)
**Time Estimate:** 10 minutes  
**Impact:** +10-15 tests

**Issue:**
Similar to API drift tests but with complex data setup

**Root Cause:**
- Fixtures trying to create too much test data at once
- Database transaction issues

**Solution:**
1. Split fixture setup into smaller pieces
2. Use `@pytest.fixture(scope='function')` instead of `@pytest.fixture(scope='class')`
3. Create data only when needed (lazy loading)

**File to Modify:**
- `backend/tests/test_api_performance.py`

### 4. Add Missing Role/User Seeds (16 errors)
**Time Estimate:** 5-10 minutes  
**Impact:** +5-10 tests

**Issue:**
Tests need default roles/users but they don't exist

**Solution:**
Create a `conftest.py` with shared fixtures:
```python
# backend/tests/conftest.py
@pytest.fixture(scope='session', autouse=True)
def setup_default_data():
    """Create default test data"""
    with app.app_context():
        # Create default roles
        admin_role = Role(name='admin', is_active=True)
        user_role = Role(name='user', is_active=True)
        # ... etc
```

## Quick Win Priority List

1. ✅ **Create `backend/tests/conftest.py`** (5 min)
   - Add session-level fixtures for roles/users
   - Add module-level teardown

2. ✅ **Fix test_api_integration.py fixture chain** (10 min)
   - Add db cleanup between modules
   - Verify role creation works

3. ✅ **Test with reduced API drift suite** (5 min)
   - Run just one API drift test to verify fix works
   - Debug remaining issues

4. ✅ **Run full test suite** (2 min)
   - Collect results
   - Document improvements

## Expected Results After Fixes

| Test Suite | Current | Expected | Change |
|-----------|---------|----------|--------|
| Integration | 22 errors | 0-5 errors | +15-20 passing |
| API Drift | 25 errors | 5-10 errors | +15-20 passing |
| Performance | 20 errors | 10-15 errors | +5-10 passing |
| Security | 16 errors | 10-15 errors | +1-5 passing |
| **TOTAL** | **83 errors** | **25-50 errors** | **+33-58 passing** |

**New Expected Pass Rate:** 75-80% (203-228 tests passing)

## Commit Plan

After completing fixes:
```bash
git add -A
git commit -m "Phase 4: Fix integration test teardown and fixtures - 200+ tests passing (76%+)"
```

## Files to Modify

**Primary:**
- [ ] `backend/tests/conftest.py` - NEW FILE (create shared fixtures)
- [ ] `backend/tests/integration/test_api_integration.py` - Add teardown
- [ ] `backend/src/database.py` - Verify idempotency

**Secondary (if needed):**
- [ ] `backend/tests/test_api_drift_invoices.py` - Fix client setup
- [ ] `backend/tests/test_api_performance.py` - Fix fixture scope
- [ ] `backend/tests/test_comprehensive_security.py` - Verify app.testing flag

## Testing Strategy

1. **Run individual test file:** 
   ```bash
   pytest tests/integration/test_api_integration.py -xvs
   ```

2. **Run specific test class:**
   ```bash
   pytest tests/integration/test_api_integration.py::TestAuthIntegration -xvs
   ```

3. **Run full suite:**
   ```bash
   pytest tests/ -q --tb=line
   ```

4. **Check specific error:**
   ```bash
   pytest tests/ -k "test_login_with_valid" -xvs
   ```

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Tests Passing | 170 | 200+ |
| Pass Rate | 65.4% | 76%+ |
| Errors | 83 | <50 |
| Failures | 34 | <30 |
| Collection Time | ~5s | ~5s |
| Execution Time | ~62s | ~60s |

## Notes for Next Session

1. Start by creating `conftest.py` with shared fixtures
2. Test integration suite first (22 errors should drop to 0-5)
3. If successful, apply similar patterns to other test suites
4. Verify each fix works before moving to next one
5. Use `git diff` to see exactly what changed
6. Run full suite regularly to monitor progress

## Related Documentation

- `PHASE_4_COMPREHENSIVE_REPORT.md` - Full test analysis
- `PHASE_4_SESSION_SUMMARY.md` - This session's work
- `PHASE_4_TESTING_PLAN.md` - Original test plan

## Estimated Timeline

- **Setup:** 2 minutes (review plan)
- **Create conftest.py:** 8 minutes
- **Fix integration tests:** 12 minutes
- **Fix API tests:** 15 minutes
- **Verification & testing:** 10 minutes
- **Total:** ~47 minutes to reach 75-80% pass rate
