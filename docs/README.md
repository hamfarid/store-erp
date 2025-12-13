# FILE: docs/README.md | PURPOSE: Documentation index and navigation | OWNER: Documentation Team | RELATED: All docs/* files | LAST-AUDITED: 2025-10-25

# Gaara Inventory Management System - Documentation

**Version**: 2.3  
**Last Updated**: 2025-10-25  
**Status**: ✅ Active Development

---

## 📚 Documentation Index

### Quick Links

- [Status Report](Status_Report.md) - Current system status and metrics
- [Test Coverage](Test_Coverage_Report.md) - Detailed test analysis
- [Task List](Task_List.md) - Project tasks and planning
- [Lessons Learned](DONT_DO_THIS_AGAIN.md) - Anti-patterns to avoid
- [Changelog](../CHANGELOG.md) - Version history

---

## 🎯 Getting Started

### For Developers

1. **Setup Environment**
   ```bash
   # Clone repository
   git clone https://github.com/gaaragroup/store.git
   cd store
   
   # Backend setup
   cd backend
   python -m venv .venv311
   .venv311\Scripts\activate  # Windows
   # source .venv311/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   
   # Run tests
   python -m pytest tests/ -v
   ```

2. **Read Key Documentation**
   - [Architecture Overview](TechStack.md)
   - [API Contracts](API_Contracts.md)
   - [Database Schema](DB_Schema.md)
   - [Security Model](Security.md)

3. **Start Development**
   - Check [Task List](Task_List.md) for available tasks
   - Follow [Contributing Guidelines](../CONTRIBUTING.md)
   - Review [Code Standards](../CONTRIBUTING.md#code-standards)

### For QA/Testers

1. **Run Tests**
   ```bash
   cd backend
   python -m pytest tests/ -v --cov=src --cov-report=html
   ```

2. **Review Coverage**
   - Open `backend/htmlcov/index.html` in browser
   - Check [Test Coverage Report](Test_Coverage_Report.md)

3. **Report Issues**
   - Use GitHub Issues
   - Follow issue templates in `.github/ISSUE_TEMPLATE/`

### For DevOps

1. **CI/CD Setup**
   - Review [.github/workflows/ci.yml](../.github/workflows/ci.yml)
   - Review [.github/workflows/deploy.yml](../.github/workflows/deploy.yml)

2. **Deployment**
   - Check [Runbook](Runbook.md) for procedures
   - Review [Environment Config](Env.md)

3. **Monitoring**
   - See [Observability Guide](Resilience.md)

---

## 📖 Core Documentation

### System Architecture

| Document | Description | Status |
|----------|-------------|--------|
| [TechStack.md](TechStack.md) | Technology stack and versions | ✅ Current |
| [Inventory.md](Inventory.md) | System inventory and file structure | ✅ Current |
| [Routes_FE.md](Routes_FE.md) | Frontend routes mapping | ⚠️ Needs update |
| [Routes_BE.md](Routes_BE.md) | Backend API routes | ✅ Current |
| [DB_Schema.md](DB_Schema.md) | Database schema and ERD | ✅ Current |

### API & Contracts

| Document | Description | Status |
|----------|-------------|--------|
| [API_Contracts.md](API_Contracts.md) | API specifications | ✅ Current |
| [/contracts/openapi.yaml](../contracts/openapi.yaml) | OpenAPI 3.0 spec | ⚠️ Needs update |
| [Error_Catalog.md](Error_Catalog.md) | Error codes reference | ✅ Current |

### Security & Compliance

| Document | Description | Status |
|----------|-------------|--------|
| [Security.md](Security.md) | Security policies and controls | ✅ Current |
| [Threat_Model.md](Threat_Model.md) | OWASP/STRIDE threat analysis | ⚠️ Needs update |
| [Permissions_Model.md](Permissions_Model.md) | RBAC permission matrix | ✅ Current |
| [CSP.md](CSP.md) | Content Security Policy | ✅ Current |

### Development & Testing

| Document | Description | Status |
|----------|-------------|--------|
| [Test_Coverage_Report.md](Test_Coverage_Report.md) | Test analysis | ✅ Current |
| [DONT_DO_THIS_AGAIN.md](DONT_DO_THIS_AGAIN.md) | Lessons learned | ✅ Current |
| [Class_Registry.md](Class_Registry.md) | Canonical model registry | ⚠️ Needs creation |

### Operations

| Document | Description | Status |
|----------|-------------|--------|
| [Runbook.md](Runbook.md) | Operational procedures | ⚠️ Needs update |
| [Resilience.md](Resilience.md) | Circuit breakers & fallbacks | ⚠️ Needs creation |
| [Env.md](Env.md) | Environment configuration | ✅ Current |

---

## 🔍 Quick Reference

### Test Results (Latest)

```
Total Tests: 64
✅ Passed: 64 (100%)
❌ Failed: 0 (0%)
⚠️ Errors: 0 (0%)
⏱️ Duration: ~18.7s
```

See [Test Coverage Report](Test_Coverage_Report.md) for details.

### Recent Fixes

- ✅ SQLAlchemy model duplication (13 errors → 0)
- ✅ Test isolation issues (24 failed → 0)
- ✅ 100% test success rate achieved
- ✅ CI/CD pipeline configured

See [Status Report](Status_Report.md) for full details.

### Current Sprint

**Focus**: Secrets Management + Load Testing + Coverage  
**Dates**: 2025-10-28 to 2025-11-01  
**Tasks**: See [Task List](Task_List.md)

---

## 🛠️ Development Workflow

### 1. Pick a Task

```bash
# Check task list
cat docs/Task_List.md

# Or view in GitHub Projects
# https://github.com/gaaragroup/store/projects
```

### 2. Create Branch

```bash
git checkout -b feature/P1.1-kms-integration
# or
git checkout -b fix/issue-123-login-error
```

### 3. Develop & Test

```bash
# Make changes
# ...

# Run tests
python -m pytest tests/ -v

# Run linting
flake8 src/
autopep8 --diff --recursive src/
```

### 4. Commit & Push

```bash
# Conventional commits
git commit -m "feat(auth): add KMS integration for secrets"
git push origin feature/P1.1-kms-integration
```

### 5. Create PR

- Use PR template
- Link to issue/task
- Request reviews
- Wait for CI to pass

### 6. Merge

- Squash and merge
- Delete branch
- Update task list

---

## 📊 Metrics & KPIs

### Code Quality

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Coverage | ~75% | ≥70% | ✅ Met |
| Test Success Rate | 100% | 100% | ✅ Met |
| Linting Errors | 0 | 0 | ✅ Met |
| Security Vulnerabilities | 0 | 0 | ✅ Met |

### Performance

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Suite Duration | ~18.7s | <30s | ✅ Met |
| API Response Time (p95) | TBD | <500ms | ⏳ Pending |
| Page Load Time (p95) | TBD | <2s | ⏳ Pending |

### Deployment

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Deployment Frequency | Manual | Daily | ⏳ Pending |
| Lead Time | TBD | <1 day | ⏳ Pending |
| MTTR | TBD | <1 hour | ⏳ Pending |

---

## 🔗 External Resources

### Official Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [React Documentation](https://react.dev/)

### Tools & Services

- [GitHub Repository](https://github.com/gaaragroup/store)
- [CI/CD Pipeline](https://github.com/gaaragroup/store/actions)
- [Issue Tracker](https://github.com/gaaragroup/store/issues)

### Company Resources

- [Gaara Group Website](https://www.gaaragroup.com)
- [MagSeeds Website](https://www.magseeds.com)

---

## 📝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code standards
- Commit message format
- PR process
- Code review guidelines

---

## 📞 Support

### For Issues

- **Bugs**: Create GitHub Issue with `bug` label
- **Features**: Create GitHub Issue with `enhancement` label
- **Security**: Email security@gaaragroup.com

### For Questions

- **Technical**: Ask in team chat or create Discussion
- **Process**: Check [Runbook](Runbook.md) or ask team lead
- **Documentation**: Check this README or create Issue

---

## 📅 Maintenance

### Documentation Updates

- **Frequency**: Weekly or after major changes
- **Owner**: Documentation Team
- **Process**: Update docs → Create PR → Review → Merge

### Review Schedule

| Document | Frequency | Next Review |
|----------|-----------|-------------|
| Status Report | Weekly | 2025-11-01 |
| Test Coverage | Weekly | 2025-11-01 |
| Task List | Bi-weekly | 2025-10-28 |
| Security Docs | Monthly | 2025-11-15 |
| All Others | Quarterly | 2026-01-15 |

---

**Last Updated**: 2025-10-25  
**Maintained By**: Documentation Team  
**Questions?**: Create an issue or ask in team chat

