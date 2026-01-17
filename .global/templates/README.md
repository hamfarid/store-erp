# Project Templates

**Professional, production-ready templates for common project types**

---

## 📦 Available Templates

### 1. ERP System Template ⭐⭐⭐

**Path:** `templates/erp_system/`

**Description:** Complete ERP system with modules for:
- Inventory management
- Sales & purchases
- Accounting
- HR & payroll
- Reports & analytics

**Tech Stack:**
- Frontend: React + TypeScript
- Backend: Django + DRF
- Database: PostgreSQL
- Cache: Redis

**Use Case:** Business management systems

---

### 2. Web Page Template ⭐⭐

**Path:** `templates/web_page/`

**Description:** Simple static/dynamic website

**Features:**
- Responsive design
- SEO optimized
- Fast loading
- Contact forms

**Tech Stack:**
- HTML5 + CSS3
- JavaScript (vanilla or framework)
- Optional backend

**Use Case:** Landing pages, portfolios, company websites

---

### 3. Web Page with Login Template ⭐⭐⭐

**Path:** `templates/web_page_with_login/`

**Description:** Web application with authentication

**Features:**
- User registration
- Login/logout
- Password reset
- User profiles
- Protected pages

**Tech Stack:**
- Frontend: React/Vue
- Backend: Django/Flask/FastAPI
- Database: PostgreSQL
- Auth: JWT/Session

**Use Case:** Web apps, dashboards, member areas

---

### 4. ML Template ⭐⭐⭐

**Path:** `templates/ml_template/`

**Description:** Machine Learning project structure

**Features:**
- Data preprocessing
- Model training
- Model evaluation
- API deployment
- Monitoring

**Tech Stack:**
- Python 3.9+
- TensorFlow/PyTorch
- FastAPI for serving
- MLflow for tracking

**Use Case:** ML projects, data science

---

### 5. Test Template ⭐⭐

**Path:** `templates/test_template/`

**Description:** Comprehensive testing setup

**Features:**
- Unit tests
- Integration tests
- E2E tests
- Coverage reports
- CI/CD integration

**Tech Stack:**
- pytest (Python)
- Jest (JavaScript)
- Selenium/Playwright
- Coverage.py

**Use Case:** Testing any project

---

### 6. Email Template ⭐⭐

**Path:** `templates/email_template/`

**Description:** Professional email templates

**Features:**
- Responsive design
- Multiple layouts
- Variables support
- Preview tool

**Types:**
- Welcome emails
- Notifications
- Newsletters
- Transactional

**Use Case:** Email campaigns, notifications

---

## 🚀 Quick Start

### Using the Template Generator

```bash
# Generate from template
python3 tools/template_generator.py --template erp_system --output /path/to/project

# Interactive mode
python3 tools/template_generator.py --interactive

# List available templates
python3 tools/template_generator.py --list
```

### Manual Usage

```bash
# Copy template
cp -r templates/web_page_with_login/ /path/to/my-project/

# Customize
cd /path/to/my-project/
# Edit configuration files
# Update project name
# Install dependencies
```

---

## 📋 Template Structure

Each template includes:

```
template_name/
├── README.md              # Template-specific guide
├── frontend/              # Frontend code (if applicable)
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/               # Backend code (if applicable)
│   ├── app/
│   ├── requirements.txt
│   └── manage.py
├── database/              # Database schemas
│   └── schema.sql
├── docker/                # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/                 # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                  # Documentation
│   ├── setup.md
│   ├── api.md
│   └── deployment.md
├── .env.example           # Environment variables
├── .gitignore             # Git ignore
└── config.json            # Template configuration
```

---

## 🎯 Customization

### Variables

Each template supports variables:

```json
{
  "project_name": "My Project",
  "database_name": "myproject_db",
  "frontend_port": 3000,
  "backend_port": 5000,
  "admin_email": "admin@example.com"
}
```

### Placeholders

Templates use placeholders:

- `{{PROJECT_NAME}}` - Project name
- `{{DATABASE_NAME}}` - Database name
- `{{FRONTEND_PORT}}` - Frontend port
- `{{BACKEND_PORT}}` - Backend port
- `{{ADMIN_EMAIL}}` - Admin email

---

## 💻 Template Generator

### Features

- **Interactive mode** - Asks questions
- **Batch mode** - Uses config file
- **Validation** - Checks requirements
- **Customization** - Replaces placeholders
- **Post-generation** - Runs setup scripts

### Usage

```bash
# Interactive
python3 tools/template_generator.py

# With config
python3 tools/template_generator.py --config myconfig.json

# Specific template
python3 tools/template_generator.py \
  --template erp_system \
  --output ~/projects/my-erp \
  --name "My ERP System"
```

---

## 📚 Documentation

### Per-Template Docs

Each template has its own documentation:

- `templates/erp_system/README.md`
- `templates/web_page/README.md`
- `templates/web_page_with_login/README.md`
- `templates/ml_template/README.md`
- `templates/test_template/README.md`
- `templates/email_template/README.md`

### General Guides

- [Template Development Guide](docs/template_development.md)
- [Customization Guide](docs/customization.md)
- [Best Practices](docs/best_practices.md)

---

## 🔧 Requirements

### All Templates

- Git
- Docker (optional but recommended)

### ERP System

- Node.js 18+
- Python 3.9+
- PostgreSQL 14+
- Redis 7+

### Web Page

- Node.js 18+ (if using framework)
- Or just a web server

### Web Page with Login

- Node.js 18+
- Python 3.9+
- PostgreSQL 14+

### ML Template

- Python 3.9+
- CUDA (for GPU support)
- 8GB+ RAM recommended

### Test Template

- Python 3.9+ or Node.js 18+
- Chrome/Firefox (for E2E)

### Email Template

- Any email service (SendGrid, Mailgun, etc.)

---

## 🎓 Examples

### Example 1: Create ERP System

```bash
# Generate project
python3 tools/template_generator.py \
  --template erp_system \
  --output ~/projects/company-erp \
  --name "Company ERP"

# Navigate
cd ~/projects/company-erp

# Install dependencies
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Admin: http://localhost:5000/admin
```

### Example 2: Create Landing Page

```bash
# Generate
python3 tools/template_generator.py \
  --template web_page \
  --output ~/projects/my-landing

# Customize
cd ~/projects/my-landing
# Edit src/index.html
# Edit src/styles.css

# Deploy
# Upload to hosting
```

### Example 3: Create ML Project

```bash
# Generate
python3 tools/template_generator.py \
  --template ml_template \
  --output ~/projects/image-classifier

# Setup
cd ~/projects/image-classifier
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Train
python3 train.py

# Serve
python3 serve.py
```

---

## 🤝 Contributing

### Adding New Templates

1. Create directory in `templates/`
2. Add template files
3. Create `README.md`
4. Create `config.json`
5. Test generation
6. Submit PR

### Template Guidelines

- Follow existing structure
- Use placeholders
- Include documentation
- Add tests
- Provide examples

---

## 📞 Support

### Issues

Report template issues:
- [GitHub Issues](https://github.com/hamfarid/global/issues)

### Questions

Ask questions:
- [GitHub Discussions](https://github.com/hamfarid/global/discussions)

---

## ✅ Checklist

Before using a template:

- [ ] Read template README
- [ ] Check requirements
- [ ] Prepare configuration
- [ ] Run generator
- [ ] Customize as needed
- [ ] Test locally
- [ ] Deploy

---

## 🎉 Summary

**6 professional templates** ready to use:

1. ✅ **ERP System** - Full business management
2. ✅ **Web Page** - Simple websites
3. ✅ **Web Page with Login** - Web applications
4. ✅ **ML Template** - Machine learning projects
5. ✅ **Test Template** - Comprehensive testing
6. ✅ **Email Template** - Professional emails

**Start building faster with production-ready templates!** 🚀

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

