# Changelog

All notable changes to the Gaara Scan AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.3.0] - 2025-12-05

### Added
- Global Professional Core Prompt integration
- Structured JSON logging system (logs/info.log, error.log, debug.log, warn.log)
- Comprehensive TODO management system (TODO.md, COMPLETE_TASKS.md, INCOMPLETE_TASKS.md)
- COMPLETE_SYSTEM_CHECKLIST.md for verification
- Enhanced MODULE_MAP.md with full project documentation

### Changed
- Updated MODULE_MAP.md to comprehensive format per Global Prompt
- Updated TODO.md with all phases and tasks documented

### Security
- All security modules verified and documented in checklist

---

## [4.2.0] - 2025-11-18

### Added
- Database models (User, Farm, Diagnosis, Report)
- API routes (auth, farms, diagnosis, reports) - 19 endpoints
- Quick API test suite
- Deployment guide
- Quick start guide
- Security documentation

### Changed
- Updated routes.py to include v1 API routers
- Fixed Pydantic v2 migration in config.py
- Fixed bcrypt compatibility

### Fixed
- Test import paths corrected
- Model import errors resolved

---

## [4.1.0] - 2025-11-18

### Added
- CSRF protection middleware
- XSS sanitization utilities
- MFA service (TOTP-based)
- Password policy module
- Security audit module
- Unit tests for security (60+ tests)
- Integration tests (30+ tests)
- E2E tests (15+ tests)
- Performance tests (Locust)
- CI/CD documentation

### Security
- Implemented double-submit cookie CSRF pattern
- Added DOMPurify for frontend XSS protection
- 12+ character password requirement
- Password history (last 5)
- Account lockout after 5 failed attempts
- MFA with backup codes

---

## [4.0.0] - 2025-11-18

### Added
- Canonical project structure (backend/, frontend/)
- Consolidated backend from multiple sources
- Consolidated frontend from gaara_ai_integrated
- Environment configuration files
- Project consolidation documentation

### Changed
- API URL changed from port 5000 to 8000
- Environment variables changed from REACT_APP_* to VITE_*
- Package version updated to 3.0.0

### Deprecated
- Original /src/ directory (kept for reference)
- /gaara_ai_integrated/ directory (kept for reference)
- /clean_project/ directory (kept for reference)

---

## [3.0.0] - 2025-11-15

### Added
- Initial AI-powered plant disease diagnosis
- Farm management system
- 30+ backend modules
- 50+ frontend components
- Docker infrastructure (25+ services)
- Comprehensive documentation

### Features
- AI diagnosis engine with TensorFlow/PyTorch
- Multi-language support (Arabic/English)
- Real-time analytics
- IoT sensor integration
- Role-based access control

---

## [2.0.0] - 2025-11-01

### Added
- React frontend with Vite
- FastAPI backend
- SQLAlchemy ORM
- Tailwind CSS styling
- shadcn/ui components

---

## [1.0.0] - 2025-10-15

### Added
- Initial project setup
- Basic authentication
- Database models
- API structure

---

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

