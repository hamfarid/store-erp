# Changelog - Store ERP v2.0.0

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-01-16

### 🎉 Codename: Phoenix Rising

Major release with complete system overhaul.

### Added

#### Core Systems
- **Lot Management System** - Advanced tracking with 50+ fields
- **POS System** - Professional point-of-sale with barcode support
- **Reports System** - 8+ report types with export functionality
- **Settings System** - Comprehensive configuration management
- **Notification System** - Multi-channel alerts and preferences
- **Tax/ZATCA System** - Saudi tax compliance integration

#### Frontend
- React 18.3.1 with Vite 6.0.7
- TailwindCSS 4.1.7 Design System
- 73+ reusable UI components
- Full RTL/Arabic support
- Dark mode with persistence
- Lazy loading and code splitting
- PDF export utility with Arabic support
- Excel/CSV export functionality

#### Backend
- Flask 3.0.3 with SQLAlchemy 2.0.23
- JWT authentication with refresh tokens
- Two-Factor Authentication (2FA/TOTP)
- Role-Based Access Control (68 permissions)
- Structured JSON logging
- Rate limiting middleware
- Comprehensive error handling

#### Security
- JWT + 2FA authentication
- RBAC with 7 default roles
- Security headers (CSP, X-Frame-Options, etc.)
- Rate limiting on auth endpoints
- Audit logging for all operations
- Input validation and sanitization

#### Infrastructure
- Docker Compose configuration
- Nginx reverse proxy setup
- Multi-environment support (dev, staging, production)
- CI/CD ready configuration
- Health check endpoints

#### Testing
- E2E tests with Playwright
- Unit tests (80%+ coverage)
- Performance testing suite
- Security audit tests
- Mobile viewport testing
- Cross-browser testing

#### Documentation
- API Reference documentation
- Testing Guide
- Integration Guide
- Deployment Guide
- Release Notes

### Changed

- Migrated from basic inventory to full ERP system
- Upgraded React from 17.x to 18.3.1
- Upgraded Flask from 2.x to 3.0.3
- Redesigned UI with modern design system
- Improved database schema for better performance
- Enhanced API response standardization

### Fixed

- Token refresh loop causing logout
- RTL layout issues in reports
- POS cart calculation errors
- Lot expiry date validation
- Export filename encoding issues
- Dark mode not persisting
- Mobile responsive layout bugs
- CORS issues in development

### Security

- Added JWT authentication with refresh tokens
- Implemented 2FA with TOTP
- Added rate limiting (5 req/min for login, 100 req/sec for API)
- Added security headers via Nginx
- Implemented RBAC with 68 permissions
- Added audit logging for sensitive operations

### Performance

- Implemented code splitting and lazy loading
- Added API response caching
- Optimized database queries with indexes
- Reduced bundle size with tree shaking
- Added image lazy loading

### Deprecated

- Legacy `/api/login` endpoint (use `/api/auth/login`)
- Basic session authentication (use JWT)

### Removed

- Old authentication middleware
- Unused database tables
- Legacy UI components

---

## [1.6.0] - Previous Release

### Added
- Basic product management
- Simple invoicing
- Customer management

### Fixed
- Various bug fixes

---

## Migration Notes

### v1.x to v2.0.0

1. **Database Migration Required**
   ```bash
   flask db upgrade
   ```

2. **New Environment Variables**
   - `SECRET_KEY` (required)
   - `JWT_SECRET_KEY` (required)
   - `CORS_ORIGINS` (required)

3. **API Changes**
   - Auth endpoints moved to `/api/auth/*`
   - All responses now include `success` field

4. **Frontend Rebuild Required**
   ```bash
   cd frontend && npm ci && npm run build
   ```

---

## Contributors

Thanks to everyone who contributed to this release!

---

## Links

- [GitHub Repository](https://github.com/your-repo/store-erp)
- [Documentation](./docs/)
- [Issue Tracker](https://github.com/your-repo/store-erp/issues)

---

*Store ERP v2.0.0 - Phoenix Rising*
