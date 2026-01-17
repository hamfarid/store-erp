# ERP System Template

**Complete Enterprise Resource Planning system**

---

## 📋 Overview

Professional ERP system with modules for:
- **Inventory Management** - Stock, warehouses, suppliers
- **Sales & Purchases** - Orders, invoices, customers
- **Accounting** - Ledger, journal entries, reports
- **HR & Payroll** - Employees, attendance, payroll

---

## 🏗️ Architecture

### Frontend
- **Framework:** React 18 + TypeScript
- **State Management:** Redux Toolkit
- **UI Library:** Material-UI (MUI)
- **Routing:** React Router v6
- **Forms:** React Hook Form + Yup
- **Charts:** Recharts
- **Tables:** TanStack Table

### Backend
- **Framework:** Django 4.2 + Django REST Framework
- **Authentication:** JWT (Simple JWT)
- **Database ORM:** Django ORM
- **API Docs:** drf-spectacular (OpenAPI)
- **Task Queue:** Celery + Redis
- **Caching:** Redis

### Database
- **Primary:** PostgreSQL 15
- **Cache:** Redis 7
- **Search:** PostgreSQL Full-Text Search

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Web Server:** Nginx
- **WSGI:** Gunicorn
- **Process Manager:** Supervisor

---

## 📦 Modules

### 1. Inventory Management

**Features:**
- Product catalog
- Stock management
- Warehouse management
- Supplier management
- Purchase orders
- Stock transfers
- Inventory reports

**Models:**
- Product
- Category
- Warehouse
- Stock
- Supplier
- PurchaseOrder
- StockMovement

### 2. Sales & Purchases

**Features:**
- Customer management
- Sales orders
- Invoices
- Payments
- Quotations
- Sales reports

**Models:**
- Customer
- SalesOrder
- Invoice
- Payment
- Quotation

### 3. Accounting

**Features:**
- Chart of accounts
- Journal entries
- General ledger
- Trial balance
- Financial statements
- Tax management

**Models:**
- Account
- JournalEntry
- Transaction
- FiscalYear
- TaxRate

### 4. HR & Payroll

**Features:**
- Employee management
- Attendance tracking
- Leave management
- Payroll processing
- Performance reviews

**Models:**
- Employee
- Department
- Attendance
- Leave
- Payroll
- Performance

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.9+
- PostgreSQL 15+
- Redis 7+

### Installation

```bash
# 1. Clone/Generate from template
python3 ../../tools/template_generator.py \
  --template erp_system \
  --output ~/projects/my-erp

# 2. Navigate
cd ~/projects/my-erp

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Start with Docker
docker-compose up -d

# 5. Run migrations
docker-compose exec backend python manage.py migrate

# 6. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 7. Load sample data (optional)
docker-compose exec backend python manage.py loaddata sample_data

# 8. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000/api/
# Admin: http://localhost:5000/admin/
# API Docs: http://localhost:5000/api/docs/
```

### Manual Setup (without Docker)

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 5000

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## 📁 Project Structure

```
erp_system/
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   │   ├── common/       # Common UI components
│   │   │   ├── inventory/    # Inventory components
│   │   │   ├── sales/        # Sales components
│   │   │   ├── accounting/   # Accounting components
│   │   │   └── hr/           # HR components
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Inventory/
│   │   │   ├── Sales/
│   │   │   ├── Accounting/
│   │   │   └── HR/
│   │   ├── services/         # API services
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── modules/
│   │   ├── store/            # Redux store
│   │   │   ├── slices/
│   │   │   └── store.ts
│   │   ├── utils/            # Utilities
│   │   ├── types/            # TypeScript types
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── backend/
│   ├── apps/
│   │   ├── inventory/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── sales/
│   │   ├── accounting/
│   │   └── hr/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── migrations/
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── nginx.conf
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── setup.md
│   ├── api.md
│   ├── modules.md
│   └── deployment.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── config.json
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=erp_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
REACT_APP_API_URL=http://localhost:5000/api

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### config.json

```json
{
  "template_name": "erp_system",
  "version": "1.0.0",
  "variables": {
    "PROJECT_NAME": "My ERP System",
    "DATABASE_NAME": "erp_db",
    "FRONTEND_PORT": "3000",
    "BACKEND_PORT": "5000",
    "ADMIN_EMAIL": "admin@example.com"
  },
  "modules": [
    "inventory",
    "sales",
    "accounting",
    "hr"
  ],
  "features": {
    "multi_warehouse": true,
    "multi_currency": true,
    "multi_language": false,
    "reporting": true,
    "api": true
  }
}
```

---

## 🎨 Features

### Dashboard
- Real-time metrics
- Sales charts
- Inventory alerts
- Recent activities

### Inventory Management
- Product CRUD
- Stock tracking
- Low stock alerts
- Warehouse management
- Supplier management
- Purchase orders

### Sales & Purchases
- Customer management
- Sales orders
- Invoicing
- Payment tracking
- Sales reports

### Accounting
- Chart of accounts
- Journal entries
- Financial reports
- Tax management

### HR & Payroll
- Employee management
- Attendance tracking
- Leave management
- Payroll processing

---

## 🔐 Security

### Authentication
- JWT-based authentication
- Refresh token rotation
- Password hashing (PBKDF2)
- Session management

### Authorization
- Role-based access control (RBAC)
- Permission-based views
- Object-level permissions

### Security Headers
- CORS configured
- CSRF protection
- XSS protection
- Content Security Policy

---

## 📊 API Documentation

### Endpoints

**Authentication:**
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/register/` - Register

**Inventory:**
- `GET /api/inventory/products/` - List products
- `POST /api/inventory/products/` - Create product
- `GET /api/inventory/products/{id}/` - Get product
- `PUT /api/inventory/products/{id}/` - Update product
- `DELETE /api/inventory/products/{id}/` - Delete product

**Sales:**
- `GET /api/sales/orders/` - List orders
- `POST /api/sales/orders/` - Create order
- `GET /api/sales/invoices/` - List invoices
- `POST /api/sales/invoices/` - Create invoice

**Accounting:**
- `GET /api/accounting/accounts/` - List accounts
- `POST /api/accounting/entries/` - Create entry
- `GET /api/accounting/reports/balance-sheet/` - Balance sheet

**HR:**
- `GET /api/hr/employees/` - List employees
- `POST /api/hr/attendance/` - Record attendance
- `GET /api/hr/payroll/` - List payroll

### API Docs

Access interactive API documentation:
- **Swagger UI:** http://localhost:5000/api/docs/
- **ReDoc:** http://localhost:5000/api/redoc/

---

## 🧪 Testing

### Run Tests

```bash
# All tests
docker-compose exec backend python manage.py test

# Specific module
docker-compose exec backend python manage.py test apps.inventory

# With coverage
docker-compose exec backend coverage run manage.py test
docker-compose exec backend coverage report
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

---

## 📈 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure database backups
- [ ] Set up SSL/TLS
- [ ] Configure email service
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Run security checks
- [ ] Test all modules

### Deploy with Docker

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

---

## 🤝 Customization

### Adding New Module

1. Create app:
```bash
cd backend
python manage.py startapp mymodule
```

2. Add to `INSTALLED_APPS` in `settings.py`

3. Create models, views, serializers

4. Add URLs

5. Create frontend components

### Modifying Existing Module

1. Edit models in `backend/apps/{module}/models.py`
2. Create migration: `python manage.py makemigrations`
3. Run migration: `python manage.py migrate`
4. Update serializers and views
5. Update frontend components

---

## 📚 Documentation

- [Setup Guide](docs/setup.md)
- [API Reference](docs/api.md)
- [Modules Guide](docs/modules.md)
- [Deployment Guide](docs/deployment.md)
- [Customization Guide](docs/customization.md)

---

## 🐛 Troubleshooting

### Common Issues

**Database connection error:**
```bash
# Check database is running
docker-compose ps db

# Check connection
docker-compose exec backend python manage.py dbshell
```

**Frontend not loading:**
```bash
# Check frontend is running
docker-compose ps frontend

# Check logs
docker-compose logs frontend
```

**API errors:**
```bash
# Check backend logs
docker-compose logs backend

# Check Django errors
docker-compose exec backend python manage.py check
```

---

## ✅ Summary

**Complete ERP System** with:

✅ **4 core modules** - Inventory, Sales, Accounting, HR  
✅ **Modern tech stack** - React + Django + PostgreSQL  
✅ **Docker ready** - Easy deployment  
✅ **API documented** - OpenAPI/Swagger  
✅ **Secure** - JWT auth, RBAC  
✅ **Tested** - Unit + Integration tests  
✅ **Production ready** - All best practices

**Start building your ERP system now!** 🚀

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

