# 📋 SPECKIT TASKS - Constitution Implementation

> Generated: 2026-01-22
> Based on: CONSTITUTION.md v1.0.0

---

## 🎯 PHASE 1: CODE QUALITY (Articles 1-4)

### 1.1 Linting & Formatting Setup
- [ ] **P1-test_projects**: Configure ESLint + Prettier for frontend
- [ ] **P2-gold-predictor**: Add Ruff/Black for Python backend
- [ ] **P3-Zakat**: Standardize Flake8 config, fix E302/E731 errors
- [ ] **P4-scan_ai**: Add pre-commit hooks for code quality
- [ ] **P5-gaara_erp**: Fix Pylint/Flake8 warnings in settings
- [ ] **P6-store**: Configure unified linting rules

### 1.2 Code Review Policies
- [ ] Enable branch protection rules on all repos
- [ ] Create PR template with checklist (security, tests, docs)
- [ ] Document code review guidelines in CONTRIBUTING.md

---

## 🧪 PHASE 2: TESTING STANDARDS (Articles 5-8)

### 2.1 Unit Test Coverage (Target: 80%)
| Project | Current | Target | Priority |
|---------|---------|--------|----------|
| test_projects | TBD | 80% | LOW |
| gold-predictor | TBD | 80% | MEDIUM |
| Zakat | ~40% | 80% | HIGH |
| scan_ai | TBD | 80% | MEDIUM |
| gaara_erp | TBD | 80% | HIGH |
| store | TBD | 80% | MEDIUM |

### 2.2 Test Framework Setup
- [ ] **P3-Zakat**: Add pytest with coverage reporting
- [ ] **P5-gaara_erp**: Configure Django test runner + coverage
- [ ] **All**: Add pytest.ini / jest.config.js with coverage thresholds

### 2.3 CI/CD Test Gates
- [ ] Create GitHub Actions workflow for all projects
- [ ] Add pre-commit hooks for linting
- [ ] Configure coverage badge generation

---

## 🎨 PHASE 3: UX CONSISTENCY (Articles 9-12)

### 3.1 Design System
- [ ] Create shared UI component library
- [ ] Document color palette in Storybook/Figma
- [ ] Standardize typography scale (8px grid)

### 3.2 Responsive Design Audit
- [ ] **P3-Zakat Frontend**: Mobile responsiveness check
- [ ] **P5-gaara_erp Frontend**: Tablet breakpoint fixes
- [ ] **P6-store Frontend**: Mobile-first review

### 3.3 Accessibility (WCAG 2.1 AA)
- [ ] Add ARIA labels to interactive elements
- [ ] Verify 4.5:1 color contrast ratios
- [ ] Test keyboard navigation on all forms
- [ ] Add visible focus states

### 3.4 Loading & Error States
- [ ] Implement skeleton loaders for async content
- [ ] Create standardized error message components
- [ ] Add empty state illustrations/messages

---

## ⚡ PHASE 4: PERFORMANCE (Articles 13-15)

### 4.1 API Response Time (Target: <500ms)
- [ ] Add request timing middleware to all backends
- [ ] Identify slow endpoints via Prometheus metrics
- [ ] Optimize N+1 queries with select_related/prefetch_related

### 4.2 Database Optimization
- [ ] Audit indexes on foreign keys
- [ ] Add indexes on common WHERE clauses
- [ ] Configure connection pooling

### 4.3 Caching Strategy
- [ ] Configure Redis caching for hot data
- [ ] Set appropriate TTLs (5-60 min)
- [ ] Add cache invalidation on writes

### 4.4 Monitoring & Alerts
- [ ] ✅ Prometheus scraping enabled (DONE)
- [ ] ✅ Health checks on all containers (DONE)
- [ ] Create Grafana dashboards per project
- [ ] Configure alerting rules for SLA violations

---

## 🔒 PHASE 5: ENFORCEMENT (Articles 16-17)

### 5.1 Automated Checks
- [ ] Add SonarQube/CodeClimate for quality gates
- [ ] Configure security scanning (Snyk/Dependabot)
- [ ] Add commit message linting (Conventional Commits)

### 5.2 Documentation
- [ ] Create CONTRIBUTING.md for each project
- [ ] Add API documentation (OpenAPI/Swagger)
- [ ] Document deployment procedures

---

## 📊 QUICK WINS (Do First)

1. [x] ~~Fix gaara_backend DisallowedHost error~~ ✅ DONE
2. [x] ~~Fix zakat-backend system_logs table~~ ✅ DONE
3. [x] ~~Fix zakat-backend security_middleware~~ ✅ DONE
4. [ ] Add pre-commit config to all projects
5. [ ] Create shared Dockerfile templates

---

## 🚨 CRITICAL ISSUES (Fix ASAP)

| Issue | Project | Priority | Status |
|-------|---------|----------|--------|
| RFC-compliant hostnames | All | HIGH | ✅ Fixed |
| Security middleware signature | Zakat | HIGH | ✅ Fixed |
| ALLOWED_HOSTS config | gaara_erp | HIGH | ✅ Fixed |
| Missing database table | Zakat | HIGH | ✅ Fixed |

---

## 📈 PROGRESS TRACKING

| Phase | Tasks | Completed | Progress |
|-------|-------|-----------|----------|
| Phase 1 | 9 | 0 | 0% |
| Phase 2 | 10 | 0 | 0% |
| Phase 3 | 10 | 0 | 0% |
| Phase 4 | 9 | 4 | 44% |
| Phase 5 | 5 | 0 | 0% |
| **TOTAL** | **43** | **4** | **9%** |

---

*This task list is auto-generated based on CONSTITUTION.md. Update as tasks are completed.*

