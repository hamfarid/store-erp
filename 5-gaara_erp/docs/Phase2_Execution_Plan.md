# PHASE 2 EXECUTION PLAN - Critical Security Fixes

**Created**: 2025-11-18 09:22
**Phase**: Phase 2 - Code Implementation (P0 Security Fixes)
**Timeline**: Days 3-7 (5 days)
**Status**: READY TO EXECUTE

---

## OVERVIEW

**Objective**: Execute all 23 P0 critical security fixes
**Priority**: CRITICAL - Production deployment blocked until complete
**Estimated Time**: 40-50 hours (5 days @ 8-10 hours/day)
**Success Criteria**: All P0 tasks complete, security scan clean, tests passing

---

## DAY 1: HARDCODED SECRETS & JWT CONFIGURATION (8 hours)

### Morning (4 hours)
**Task**: Remove all hardcoded secrets
- [ ] Fix `api_gateway/main.py` (lines 62, 162)
- [ ] Fix `gaara_erp/gaara_erp/settings/base.py` (line 13)
- [ ] Create `.env.example` with required variables
- [ ] Scan entire codebase for remaining secrets
- [ ] Test application startup with env vars
- [ ] Verify no hardcoded secrets remain

**Deliverable**: Zero hardcoded secrets in codebase

### Afternoon (4 hours)
**Task**: Consolidate JWT configuration
- [ ] Set `ACCESS_TOKEN_LIFETIME = 15 minutes` in `settings/security.py`
- [ ] Set `REFRESH_TOKEN_LIFETIME = 7 days`
- [ ] Enable `ROTATE_REFRESH_TOKENS = True`
- [ ] Delete/deprecate `admin_modules/custom_admin/jwt_config.py`
- [ ] Remove conflicting config from `settings/security_enhanced.py`
- [ ] Test token generation and expiry
- [ ] Test refresh token rotation

**Deliverable**: Single JWT configuration, 15-minute access tokens

---

## DAY 2: ACCOUNT LOCKOUT & HTTPS (8 hours)

### Morning (4 hours)
**Task**: Implement account lockout logic
- [ ] Add lockout logic to `core_modules/users/services.py`
- [ ] Create `AccountLockedException` class
- [ ] Update authentication function
- [ ] Add tests for lockout scenarios
- [ ] Test 5 failed attempts → lock
- [ ] Test auto-unlock after 15 minutes
- [ ] Test successful login resets counter

**Deliverable**: Working account lockout (5 attempts, 15-min lock)

### Afternoon (4 hours)
**Task**: Force HTTPS in production
- [ ] Update `gaara_erp/gaara_erp/settings/prod.py`
- [ ] Set `SECURE_SSL_REDIRECT = True` (no override)
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Configure HSTS headers
- [ ] Test HTTP → HTTPS redirect
- [ ] Verify secure cookie flags

**Deliverable**: HTTPS enforced, secure cookies

---

## DAY 3: MIDDLEWARE & PERMISSIONS (8 hours)

### Morning (4 hours)
**Task**: Verify and configure middleware
- [ ] Verify `SecurityHeadersMiddleware` in MIDDLEWARE list
- [ ] Verify `RateLimitMiddleware` active
- [ ] Verify `CsrfViewMiddleware` enabled
- [ ] Test rate limiting (5 login attempts)
- [ ] Test CSRF protection
- [ ] Test security headers (HSTS, CSP, X-Frame-Options)

**Deliverable**: All security middleware active and tested

### Afternoon (4 hours)
**Task**: Add @require_permission decorators (start)
- [ ] Identify all protected routes (50+ endpoints)
- [ ] Add decorators to auth routes
- [ ] Add decorators to user management routes
- [ ] Add decorators to company routes
- [ ] Test permission checks
- [ ] Document permission matrix

**Deliverable**: 25% of routes protected (12-15 routes)

---

## DAY 4: PERMISSIONS & INPUT VALIDATION (8 hours)

### Morning (4 hours)
**Task**: Continue @require_permission decorators
- [ ] Add decorators to inventory routes
- [ ] Add decorators to sales routes
- [ ] Add decorators to accounting routes
- [ ] Add decorators to reports routes
- [ ] Test all permission checks
- [ ] Update `docs/Permissions_Model.md`

**Deliverable**: 75% of routes protected (35-40 routes)

### Afternoon (4 hours)
**Task**: Add input validation (start)
- [ ] Create validation schemas for auth endpoints
- [ ] Create validation schemas for user endpoints
- [ ] Add validation to POST/PUT/PATCH requests
- [ ] Test with invalid input
- [ ] Verify 400 Bad Request responses

**Deliverable**: 25% of endpoints validated (12-15 endpoints)

---

## DAY 5: FINAL FIXES & TESTING (8 hours)

### Morning (4 hours)
**Task**: Complete remaining P0 fixes
- [ ] Finish @require_permission decorators (remaining 25%)
- [ ] Finish input validation (remaining 75%)
- [ ] Frontend route guards with permission checks
- [ ] Configure CSP with nonces
- [ ] Configure additional security headers
- [ ] Scan repository for leaked secrets (final check)

**Deliverable**: All P0 fixes complete

### Afternoon (4 hours)
**Task**: Comprehensive testing & verification
- [ ] Run full test suite
- [ ] Run security scan (SAST)
- [ ] Run dependency scan
- [ ] Verify all P0 checklist items
- [ ] Update documentation
- [ ] Create Phase 2 completion report

**Deliverable**: Phase 2 complete, ready for Phase 3

---

## P0 CHECKLIST (23 Tasks)

### Authentication & Session Management (8 tasks)
- [ ] 1. Enable CSRF protection globally ✅ (Already enabled)
- [ ] 2. Set JWT access token TTL to 15 minutes
- [ ] 3. Implement JWT refresh token rotation
- [ ] 4. Set refresh token TTL to 7 days
- [ ] 5. Implement account lockout after failed login attempts
- [ ] 6. Add rate limiting to /api/auth/login ✅ (Already implemented)
- [ ] 7. Migrate secrets to KMS/Vault (Phase 1: env vars)
- [ ] 8. Configure secure cookie flags

### Authorization & RBAC (3 tasks)
- [ ] 9. Add @require_permission decorator to all protected routes
- [ ] 10. Document RBAC permission matrix
- [ ] 11. Frontend route guards with permission checks

### HTTPS & Transport Security (4 tasks)
- [ ] 12. Enforce HTTPS in production environment
- [ ] 13. Configure CSP with nonces
- [ ] 14. Configure security headers

### Secrets Management (2 tasks)
- [ ] 15. Scan repository for leaked secrets
- [ ] 16. Remove hardcoded passwords from scripts

### Database Security (2 tasks)
- [ ] 17. Upgrade password hashing to Argon2id/scrypt ✅ (Already using Argon2)
- [ ] 18. Add SQL injection protection audit

### Input Validation (2 tasks)
- [ ] 19. Add input validation to all API endpoints
- [ ] 20. RAG input schema validation

### Deployment Security (2 tasks)
- [ ] 21. Configure production .env with KMS references
- [ ] 22. Docker image security hardening
- [ ] 23. Enable SBOM generation on every PR

---

## RISK MITIGATION

### Risk 1: Breaking Existing Functionality
**Mitigation**:
- Create database backup before starting
- Test each change in isolation
- Run full test suite after each fix
- Maintain rollback plan

### Risk 2: Time Overrun
**Mitigation**:
- Strict prioritization (P0 first)
- Daily progress tracking
- Adjust scope if needed (move P1 tasks to Phase 3)

### Risk 3: Configuration Conflicts
**Mitigation**:
- Document all configuration changes
- Test in staging environment first
- Verify single source of truth for each setting

---

## SUCCESS METRICS

- [ ] All 23 P0 tasks complete
- [ ] Zero hardcoded secrets in codebase
- [ ] JWT tokens expire in 15 minutes
- [ ] Account lockout working (5 attempts, 15-min lock)
- [ ] HTTPS enforced in production
- [ ] All security middleware active
- [ ] 80%+ of routes have permission checks
- [ ] 80%+ of endpoints have input validation
- [ ] All tests passing
- [ ] Security scan clean (no critical/high vulnerabilities)

---

## DELIVERABLES

1. **Code Changes**: All P0 security fixes implemented
2. **Documentation**: Updated security docs, permission matrix
3. **Tests**: New tests for all security features
4. **Configuration**: Production-ready settings
5. **Reports**: Phase 2 completion report, security audit report

---

**Next Phase**: Phase 3 - Architectural Improvements (Database migrations, duplicate consolidation)
**Estimated Start**: Day 8

