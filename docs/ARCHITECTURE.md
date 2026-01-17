# 🏗️ Store ERP - System Architecture

**Version:** 1.0.0  
**Last Updated:** 2025-12-13  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [Technology Stack](#technology-stack)
4. [System Components](#system-components)
5. [Database Schema](#database-schema)
6. [API Architecture](#api-architecture)
7. [Frontend Architecture](#frontend-architecture)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Naming Conventions](#naming-conventions)
11. [Folder Structure](#folder-structure)
12. [Coding Standards](#coding-standards)

---

## 🎯 System Overview

Store ERP is a comprehensive Enterprise Resource Planning system designed specifically for agricultural supply stores, with advanced features for managing seeds, fertilizers, and agricultural products with lot/batch tracking.

### Key Features:
- **Advanced Lot Management** - Track batches with quality control, expiry dates, and ministry approvals
- **Point of Sale (POS)** - Full-featured POS system with FIFO lot selection
- **Purchases Management** - Complete purchase order workflow
- **Reports System** - Comprehensive reporting and analytics
- **Permissions System** - Role-based access control (RBAC)

### System Type:
- **Architecture:** Monolithic with clear separation of concerns
- **Pattern:** MVC (Model-View-Controller)
- **Communication:** RESTful APIs
- **Database:** SQLite (development), PostgreSQL (production ready)

---

## 🧠 Architecture Principles

### 1. Separation of Concerns
- **Backend:** Pure business logic, no UI concerns
- **Frontend:** Pure presentation logic, no business logic
- **Database:** Data persistence only, no business logic

### 2. Single Responsibility
- Each module/component has ONE clear purpose
- Each function does ONE thing well
- Each class represents ONE concept

### 3. DRY (Don't Repeat Yourself)
- Shared logic in utilities
- Reusable components
- Configuration centralization

### 4. Security First (OSF Framework - 35%)
- Input validation on all endpoints
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (React escaping)
- CSRF protection (tokens)
- Authentication on all protected routes

### 5. Scalability
- Stateless backend (horizontal scaling ready)
- Database indexing for performance
- Caching strategy (Redis ready)
- Async operations where needed

---

## 🛠️ Technology Stack

### Backend:
```python
- Python 3.11+
- Flask 3.0.0 (Web Framework)
- SQLAlchemy 2.0+ (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)
- Flask-Migrate (Database Migrations)
- Werkzeug (Security utilities)
```

### Frontend:
```javascript
- React 18.2.0
- React Router 6.x (Routing)
- Axios (HTTP Client)
- TailwindCSS (Styling)
- Lucide React (Icons)
- Chart.js (Charts)
```

### Database:
```
- SQLite (Development)
- PostgreSQL (Production)
- 28 Tables
- 50+ Indexes
- 10+ Triggers
```

---

## 🧩 System Components

### Backend Structure:
```
backend/
├── src/
│   ├── models/          # Database Models (SQLAlchemy)
│   ├── routes/          # API Endpoints (Flask Blueprints)
│   ├── utils/           # Utility Functions
│   └── decorators/      # Custom Decorators
├── migrations/          # Database Migrations
├── instance/            # Instance-specific files
└── app.py              # Application Entry Point
```

### Frontend Structure:
```
frontend/
├── src/
│   ├── pages/           # Page Components
│   ├── components/      # Reusable Components
│   ├── services/        # API Services
│   ├── config/          # Configuration
│   └── App.jsx          # Application Entry Point
```

---

## 🗄️ Database Schema

### Core Tables:
- **users, roles, permissions, role_permissions** - Authentication & Authorization
- **products_advanced, batches_advanced** - Products & Inventory
- **shifts, sales, sale_items** - Sales & POS
- **purchase_orders, purchase_order_items, purchase_receipts** - Purchases

### Total: 28 Tables, 50+ Indexes, 10+ Triggers

---

## 🔌 API Architecture

### RESTful Design with JWT Authentication

**Authentication:** Bearer Token in Authorization header  
**Response Format:** JSON with success/error structure  
**Status Codes:** 200, 201, 400, 401, 403, 404, 500

---

## 🎨 Frontend Architecture

**Component Hierarchy:** App → AppRouter → Protected Routes  
**State Management:** Local State + Context API  
**Routing:** React Router v6 with Protected Routes  
**Styling:** TailwindCSS (Utility-first)

---

## 🔒 Security Architecture

**Authentication:** JWT (24 hours expiry)  
**Authorization:** RBAC with 68 permissions, 7 roles  
**Input Validation:** Backend + Frontend  
**Security Headers:** X-Content-Type-Options, X-Frame-Options, X-XSS-Protection

---

## 📝 Naming Conventions

**Python:** snake_case (files, functions, variables), PascalCase (classes)  
**JavaScript:** PascalCase (components), camelCase (functions, variables)  
**Database:** snake_case (tables, columns)  
**APIs:** kebab-case (endpoints)

---

## 💻 Coding Standards

**Python:** PEP 8, Google docstrings, 100 chars line length  
**JavaScript:** Airbnb style, ES6+, single quotes  
**Git:** Conventional Commits (feat:, fix:, docs:)

---

**Maintained by:** AI Agent + Development Team  
**Repository:** https://github.com/hamfarid/store-erp
