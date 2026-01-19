=================================================================================
PROJECT PLANNING - Task Breakdown and Planning
=================================================================================

Version: Latest
Type: Core - Planning

This prompt guides project planning and task breakdown.

=================================================================================
OVERVIEW
=================================================================================

After gathering requirements (01_requirements.txt) or analyzing existing project
(02_analysis.txt), use this prompt to:

1. Break down project into phases
2. Create task lists
3. Estimate timelines
4. Set priorities
5. Define milestones

=================================================================================
PLANNING WORKFLOW
=================================================================================

## Step 1: Define Project Scope

### Questions to Answer:
- What is the main goal?
- Who are the users?
- What are the core features?
- What are nice-to-have features?
- What are the constraints (time, budget, resources)?

### Output: Project Scope Document

```markdown
# Project Scope: {{PROJECT_NAME}}

## Goal
[One-sentence description of the project goal]

## Target Users
- [User type 1]
- [User type 2]

## Core Features (Must-Have)
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

## Additional Features (Nice-to-Have)
1. [Feature A]
2. [Feature B]

## Constraints
- **Timeline:** [X weeks/months]
- **Budget:** [if applicable]
- **Team Size:** [number of developers]
- **Technology:** [any tech constraints]

## Out of Scope
- [What we're NOT building]
```

## Step 2: Break Down into Phases

### Standard Phases for New Projects:

**Phase 1: Setup & Foundation (Week 1)**
- Project initialization
- Development environment setup
- Database schema design
- Basic project structure
- CI/CD pipeline setup

**Phase 2: Core Backend (Weeks 2-3)**
- Database models
- API endpoints
- Authentication
- Business logic
- Unit tests

**Phase 3: Core Frontend (Weeks 3-4)**
- UI components
- Pages/Views
- State management
- API integration
- Responsive design

**Phase 4: Integration (Week 5)**
- Frontend-Backend integration
- End-to-end testing
- Bug fixes
- Performance optimization

**Phase 5: Polish & Deploy (Week 6)**
- UI/UX improvements
- Documentation
- Security audit
- Deployment
- Monitoring setup

### Adjust Based on Project Type:

**API-Only Project:**
- Skip Phase 3 (Frontend)
- Expand Phase 2 (Backend)
- Add API documentation phase

**Data Science Project:**
- Phase 1: Data collection & exploration
- Phase 2: Data cleaning & preprocessing
- Phase 3: Model development
- Phase 4: Model evaluation
- Phase 5: Deployment & monitoring

**Mobile App:**
- Add platform-specific phases (iOS, Android)
- Add app store submission phase

## Step 3: Create Detailed Task Lists

### Phase 1 Example: Setup & Foundation

```markdown
## Phase 1: Setup & Foundation

### 1.1 Project Initialization
- [ ] Create Git repository
- [ ] Initialize backend project (Django/FastAPI/etc.)
- [ ] Initialize frontend project (React/Vue/etc.)
- [ ] Set up project structure
- [ ] Create README.md

### 1.2 Development Environment
- [ ] Create .env.example
- [ ] Set up Docker containers
- [ ] Create docker-compose.yml
- [ ] Configure database
- [ ] Test local development setup

### 1.3 Database Schema
- [ ] Design ER diagram
- [ ] Create models/schemas
- [ ] Create migrations
- [ ] Seed initial data
- [ ] Document schema

### 1.4 CI/CD Setup
- [ ] Create GitHub Actions workflow
- [ ] Set up linting
- [ ] Set up testing
- [ ] Configure deployment pipeline

**Estimated Time:** 5-7 days
**Dependencies:** None
**Deliverables:** Working development environment
```

### Phase 2 Example: Core Backend

```markdown
## Phase 2: Core Backend

### 2.1 User Management
- [ ] User model
- [ ] Registration endpoint
- [ ] Login endpoint
- [ ] JWT token generation
- [ ] Password reset
- [ ] Email verification
- [ ] Unit tests

### 2.2 Core Models
- [ ] [Model 1] model & serializer
- [ ] [Model 2] model & serializer
- [ ] [Model 3] model & serializer
- [ ] Relationships between models
- [ ] Model validation
- [ ] Unit tests

### 2.3 API Endpoints
- [ ] CRUD for [Model 1]
- [ ] CRUD for [Model 2]
- [ ] CRUD for [Model 3]
- [ ] Filtering & pagination
- [ ] API documentation
- [ ] Integration tests

### 2.4 Business Logic
- [ ] [Business rule 1]
- [ ] [Business rule 2]
- [ ] Error handling
- [ ] Logging
- [ ] Unit tests

**Estimated Time:** 10-14 days
**Dependencies:** Phase 1 complete
**Deliverables:** Functional API
```

## Step 4: Estimate Timelines

### Estimation Techniques:

**1. T-Shirt Sizing:**
- XS: 1-2 hours
- S: 2-4 hours
- M: 4-8 hours (half day to full day)
- L: 1-2 days
- XL: 3-5 days
- XXL: 1+ weeks

**2. Story Points (Fibonacci):**
- 1 point: Very simple task
- 2 points: Simple task
- 3 points: Medium task
- 5 points: Complex task
- 8 points: Very complex task
- 13 points: Extremely complex (should be broken down)

**3. Time-Based:**
- Break tasks into 1-4 hour chunks
- Sum up for total estimate
- Add 20-30% buffer for unknowns

### Example Timeline:

```
Project: E-commerce Platform
Total Estimated Time: 8 weeks

Week 1: Setup & Foundation
  - Days 1-2: Project initialization
  - Days 3-4: Database schema
  - Day 5: CI/CD setup

Week 2-3: Backend Development
  - Week 2: User management & authentication
  - Week 3: Product catalog & cart

Week 4-5: Frontend Development
  - Week 4: User interface & navigation
  - Week 5: Product pages & checkout

Week 6: Integration & Testing
  - Days 1-3: Integration
  - Days 4-5: Testing & bug fixes

Week 7: Polish
  - Days 1-2: UI/UX improvements
  - Days 3-4: Performance optimization
  - Day 5: Security audit

Week 8: Deployment
  - Days 1-2: Staging deployment
  - Days 3-4: Production deployment
  - Day 5: Monitoring & documentation
```

## Step 5: Set Priorities

### Priority Levels:

**P0 (Critical):**
- Blocks entire project
- Must be done first
- Example: Database setup, authentication

**P1 (High):**
- Core features
- Needed for MVP
- Example: User registration, product listing

**P2 (Medium):**
- Important but not critical
- Can be done after MVP
- Example: Email notifications, advanced search

**P3 (Low):**
- Nice to have
- Can be postponed
- Example: Dark mode, social sharing

### Prioritization Matrix:

```
High Impact, Low Effort → Do First (P0-P1)
High Impact, High Effort → Do Second (P1)
Low Impact, Low Effort → Do Third (P2)
Low Impact, High Effort → Do Last or Skip (P3)
```

## Step 6: Define Milestones

### Milestone Types:

**1. Development Milestones:**
- Backend API complete
- Frontend UI complete
- Integration complete

**2. Feature Milestones:**
- User authentication working
- Payment processing working
- Admin dashboard complete

**3. Quality Milestones:**
- 80% test coverage achieved
- All security issues resolved
- Performance targets met

**4. Deployment Milestones:**
- Staging deployment successful
- Production deployment successful
- Monitoring active

### Example Milestones:

```
Milestone 1: Development Environment Ready (End of Week 1)
  - Git repository set up
  - Docker containers running
  - Database schema created
  - CI/CD pipeline active

Milestone 2: Backend MVP Complete (End of Week 3)
  - User authentication working
  - Core API endpoints functional
  - 70% test coverage
  - API documentation published

Milestone 3: Frontend MVP Complete (End of Week 5)
  - All main pages implemented
  - API integration complete
  - Responsive design working
  - Basic tests passing

Milestone 4: Production Ready (End of Week 7)
  - All features complete
  - 80% test coverage
  - Security audit passed
  - Performance optimized

Milestone 5: Deployed (End of Week 8)
  - Production deployment successful
  - Monitoring active
  - Documentation complete
  - Handoff ready
```

=================================================================================
PLANNING TEMPLATES
=================================================================================

## Template 1: Simple Web Application

```
Phase 1: Setup (3 days)
  - Initialize project
  - Set up database
  - Create basic structure

Phase 2: Backend (1 week)
  - Models & migrations
  - API endpoints
  - Authentication

Phase 3: Frontend (1 week)
  - UI components
  - Pages
  - API integration

Phase 4: Deploy (2 days)
  - Docker setup
  - Deployment
  - Monitoring

Total: 3 weeks
```

## Template 2: API Service

```
Phase 1: Setup (2 days)
  - Initialize project
  - Database schema
  - CI/CD

Phase 2: Core API (1 week)
  - Endpoints
  - Authentication
  - Validation

Phase 3: Advanced Features (1 week)
  - Rate limiting
  - Caching
  - Webhooks

Phase 4: Documentation & Deploy (3 days)
  - OpenAPI docs
  - Deployment
  - Monitoring

Total: 3 weeks
```

## Template 3: Data Science Project

```
Phase 1: Data Collection (1 week)
  - Identify data sources
  - Collect data
  - Store data

Phase 2: Data Preparation (1 week)
  - Clean data
  - Transform data
  - Feature engineering

Phase 3: Model Development (2 weeks)
  - Exploratory analysis
  - Model training
  - Model evaluation

Phase 4: Deployment (1 week)
  - Create API
  - Deploy model
  - Set up monitoring

Total: 5 weeks
```

=================================================================================
RISK MANAGEMENT
=================================================================================

## Identify Risks

**Technical Risks:**
- New technology/framework
- Complex integrations
- Performance requirements
- Scalability needs

**Resource Risks:**
- Limited team size
- Skill gaps
- Time constraints
- Budget limitations

**External Risks:**
- Third-party API dependencies
- Regulatory requirements
- Market changes

## Mitigation Strategies

**For Technical Risks:**
- Proof of concept early
- Allocate buffer time
- Have backup solutions

**For Resource Risks:**
- Training/upskilling
- Hire contractors if needed
- Reduce scope if necessary

**For External Risks:**
- Have fallback providers
- Stay updated on regulations
- Build flexibility into design

=================================================================================
AGILE PLANNING
=================================================================================

## Sprint Planning (2-week sprints)

**Sprint 1:**
- Goal: Development environment ready
- Tasks: [from Phase 1]

**Sprint 2:**
- Goal: User authentication working
- Tasks: [from Phase 2.1]

**Sprint 3:**
- Goal: Core API complete
- Tasks: [from Phase 2.2-2.3]

**Sprint 4:**
- Goal: Frontend foundation
- Tasks: [from Phase 3.1]

And so on...

## Daily Standups

**Questions:**
1. What did I complete yesterday?
2. What will I work on today?
3. Any blockers?

## Sprint Reviews

**End of each sprint:**
- Demo completed features
- Gather feedback
- Adjust plan if needed

=================================================================================
TRACKING PROGRESS
=================================================================================

## Tools

**Project Management:**
- GitHub Projects
- Jira
- Trello
- Asana

**Time Tracking:**
- Toggl
- Harvest
- Clockify

**Documentation:**
- Notion
- Confluence
- Google Docs

## Metrics to Track

**Velocity:**
- Story points completed per sprint
- Tasks completed per week

**Quality:**
- Test coverage %
- Bug count
- Code review time

**Timeline:**
- On track / ahead / behind
- Estimated completion date
- Actual vs estimated time

=================================================================================
COMMUNICATION PLAN
=================================================================================

## Stakeholder Updates

**Daily:** Team standup
**Weekly:** Progress report to stakeholders
**Bi-weekly:** Sprint review & planning
**Monthly:** Milestone review

## Status Report Template

```
# Weekly Status Report - Week [X]

## Completed This Week
- [Task 1]
- [Task 2]
- [Task 3]

## In Progress
- [Task A] - 60% complete
- [Task B] - 30% complete

## Planned for Next Week
- [Task X]
- [Task Y]

## Blockers
- [Blocker 1] - Waiting for [X]
- [Blocker 2] - Need help with [Y]

## Risks
- [Risk 1] - Mitigation: [action]

## Overall Status
On Track / At Risk / Behind Schedule
```

=================================================================================
NEXT STEPS
=================================================================================

After creating the plan:

1. **Review with team/stakeholders**
2. **Get approval**
3. **Set up project management tool**
4. **Create first sprint/phase tasks**
5. **Start development!**

Load relevant prompts based on tech stack:
- Backend → 10_backend.txt
- Frontend → 11_frontend.txt
- Database → 12_database.txt
- APIs → 13_api.txt

=================================================================================
END OF PLANNING PROMPT
=================================================================================



================================================================================
ADDITIONAL CONTENT FROM 
================================================================================

40. ORGANIZED DEFINITIONS STRUCTURE

--------------------------------------------------------------------------------

## 62. __INIT__.PY PATTERNS & BEST PRACTICES

--------------------------------------------------------------------------------



================================================================================
RECOVERED CONTENT FROM  (Phase 2)
================================================================================

idation, allowlist
- Clickjacking: X-Frame-Options
- Brute force: rate limiting, lockout

G) Compliance
- GDPR: data export, deletion, consent
- HIPAA: encryption, audit logs (if applicable)
- SOC 2: security controls, audits
- PCI DSS: if handling payments

⸻

9) DEVOPS & INFRASTRUCTURE (Expanded in )

A) Containerization (Docker)
- Multi-stage builds
- Non-root user
- Minimal base images (Alpine)
- .dockerignore for efficiency
- Health checks in Dockerfile
- Security scanning (Trivy)

B) Orchestration (Kubernetes)
- Deployments with rolling updates
- Services: ClusterIP, LoadBalancer
- ConfigMaps & Secrets
- Horizontal Pod Autoscaler (HPA)
- Ingress with TLS
- Resource limits & requests

C) CI/CD Pipelines
- GitHub Actions / GitLab CI
- Stages: Lint → Test → Security → Build → Deploy
- Quality gates: coverage >80%, no critical vulns
- Automated deployments: staging (auto), production (manual)
- Rollback strategy: blue-green, canary

D) Infrastructure as Code
- Terraform for cloud
 configurable (high/normal/low)
- Storage: append-only DB table
- Retention: 12 months, then archive
- UI: filterable timeline
- Security: alert on suspicious patterns

B) backup_management Module
- Automated: daily full, hourly incremental
- Storage: S3/GCS, encrypted
- Retention: 30 days online, 1 year archive
- Tested restore: monthly
- Monitoring: backup success rate

C) system_health Module
- Endpoints: /health, /ready
- Checks: DB connection, Redis, external APIs
- Response time: <100ms
- Used by: load balancers, Kubernetes

D) system_monitoring Module
- Metrics: CPU, memory, disk, network
- Application: request rate, latency, errors
- Business: active users, transactions
- Dashboards: Grafana
- Alerts: threshold-based + anomaly detection

⸻

14) RESILIENCE & CIRCUIT BREAKERS (from )

A) Circuit Breaker States
- CLOSED: normal operation
- OPEN: failures exceed threshold, fail fast
- HALF_OPEN: test if service recovered

B) Configuration
- Failure threshold: 50% over 10 reques
tests pass

Documentation:
- [ ] All 30+ docs files present
- [ ] API docs complete
- [ ] Runbooks written
- [ ] Architecture diagrams updated

Infrastructure:
- [ ] Docker images scanned
- [ ] Kubernetes manifests validated
- [ ] HPA configured
- [ ] Backups automated
- [ ] Monitoring configured

CI/CD:
- [ ] All pipelines green
- [ ] Quality gates passed
- [ ] Deployment strategy tested
- [ ] Rollback procedure tested

⸻

END OF GLOBAL_GUIDELINES 

This is the COMPLETE, production-ready edition consolidating all previous versions and expansions.

For implementation details, see:
- guides/DOCKER_INTEGRATION.md
- guides/KUBERNETES_INTEGRATION.md
- guides/CICD_INTEGRATION.md
- guides/MATURITY_MODEL.md
- examples/code-samples/log_activity_example.py

OSF Score: Aim for 0.85+ (Level 4: Optimizing)
Maturity Level: Target Level 3-4 for production systems

⸻

Version: Latest
Date: 2025-10-28
Status: Production Ready
License: Proprietary

⸻

21) SUDI DEVICE IDENTITY (NEW in )

A) Devic
**Module:** module_name
**File:** path/to/file.py

### Description
Detailed description of the error that occurred.

### Root Cause
What caused this error to happen.

### Impact
- What broke
- Who was affected
- Duration of issue

### Solution Applied
```python
# Code that fixed the issue
def fixed_function():
    # Corrected implementation
    pass
```

### Prevention Measures
1. Added validation for X
2. Implemented error handling for Y
3. Added unit test to catch this scenario

### Related Errors
- Error #YYY (similar issue)

### Lessons Learned
- Always validate input X
- Never assume Y
- Use Z pattern for this scenario

---
```

### 48.2 Error Categories

**1. Logic Errors**
- Incorrect algorithm
- Wrong assumptions
- Edge cases not handled

**2. Integration Errors**
- API mismatch
- Database schema mismatch
- Frontend/Backend disconnect

**3. Configuration Errors**
- Wrong environment variables
- Missing dependencies
- Incorrect permissions

**4. Performance Errors**
- N+1 querie
حساب الإجمالي من العناصر المرتبطة.
        
        Returns:
            Decimal: الإجمالي المحسوب
        """
        total = sum(
            item.subtotal for item in self.items.all()
        )
        self.total = Decimal(str(total))
        self.save()
        return self.total
```

### 54.4 Quality Checklist

**Every module MUST have:**
- [ ] Professional folder structure
- [ ] Comprehensive models with relationships
- [ ] State management (if applicable)
- [ ] Arabic docstrings
- [ ] Custom methods (confirm/cancel/compute)
- [ ] Validation logic
- [ ] Unit tests (≥80% coverage)
- [ ] Integration tests
- [ ] API endpoints
- [ ] Frontend components
- [ ] Permissions/RBAC
- [ ] README.md
- [ ] Custom reports (if applicable)
- [ ] Smart filters

---

## 55. Constants & Definitions Registry

### 55.1 Centralized Constants

**Location:** `config/constants.py`

```python
"""
File: config/constants.py
Module: config.constants
Created: 2025-01-15
Author: Team
Description: System-wide con
plementation Gap Analysis

### 57.1 Gap Analysis Checklist

**Before marking module as complete:**

**Frontend/Backend Integration:**
- [ ] All backend endpoints have frontend consumers
- [ ] All frontend features have backend support
- [ ] API contracts match on both sides
- [ ] Error handling is consistent

**Sub-screens and Buttons:**
- [ ] All designed screens are implemented
- [ ] All buttons have click handlers
- [ ] All forms submit to correct endpoints
- [ ] All modals/dialogs work correctly

**Routing:**
- [ ] All routes are defined
- [ ] Navigation works between all pages
- [ ] Deep linking works
- [ ] 404 pages handled
- [ ] Protected routes require auth

**Database Integration:**
- [ ] All models are created
- [ ] Migrations are applied
- [ ] Relationships are correct (ForeignKey, ManyToMany)
- [ ] Indexes are in place
- [ ] Constraints are enforced (unique, check)

**Testing:**
- [ ] Unit tests exist and pass
- [ ] Integration tests exist and pass
- [ ] E2E tests for criti
 pattern
│       └── definitions/
│           ├── __init__.py
│           ├── common.py                # تعريفات عامة
│           ├── core.py                  # تعريفات أساسية
│           └── custom.py                # تعريفات مخصصة
│
├── examples/                            # الأمثلة 💡
│   ├── simple-api/                      # مثال API بسيط
│   ├── code-samples/                    # عينات كود
│   └── init_py_patterns/                # أنماط __init__.py
│       ├── 01_central_registry/
│       ├── 02_lazy_loading/
│       └── 03_plugin_system/
│
├── scripts/                             # سكريبتات التكامل 🔧
│   ├── integrate.sh                     # تثبيت رئيسي
│   ├── configure.sh                     # تكوين
│   ├── apply.sh                         # تطبيق
│   ├── update.sh                        # تحديث
│   ├── uninstall.sh                     # إزالة
│   └── README.md                        # دليل السكريبتات
│
├── flows/                               # سير العمل 📚
│   ├── DEVELOPMEN
tion
- **Inherited projects** you're unfamiliar with
- **Large projects** with complex structure
- **Multi-technology projects** (full-stack)
- **Before major changes** to understand current state

---

**Auto-analysis makes Augment truly intelligent about your project!** 🎯



================================================================================

# SECTION 66: PROJECT TEMPLATES SYSTEM

**Professional, production-ready templates for rapid project initialization**

---

## Overview

The Global Guidelines includes a comprehensive template system with **9 professional templates** covering common project types. Each template is production-ready with best practices, complete documentation, and automated setup.

---

## Available Templates

### 1. ERP System Template ⭐⭐⭐

**Path:** `templates/erp_system/`

**Description:** Complete Enterprise Resource Planning system

**Modules:**
- Inventory Management
- Sales & Purchases
- Accounting & Finance
- HR & Payroll

**Tech Stack:**
- Fr
ontend: React + TypeScript
- Backend: Django + DRF
- Database: PostgreSQL
- Cache: Redis

**Use Cases:**
- Business management systems
- Manufacturing ERP
- Distribution management
- Multi-company systems

---

### 2. Web Page Template ⭐⭐

**Path:** `templates/web_page/`

**Description:** Simple static/dynamic website

**Features:**
- Responsive design
- SEO optimized
- Contact forms
- Fast loading

**Tech Stack:**
- HTML5 + CSS3
- JavaScript
- Optional backend

**Use Cases:**
- Landing pages
- Portfolios
- Company websites
- Product pages

---

### 3. Web Page with Login Template ⭐⭐⭐

**Path:** `templates/web_page_with_login/`

**Description:** Web application with authentication

**Features:**
- User registration/login
- Password reset
- User profiles
- Protected pages
- Session management

**Tech Stack:**
- Frontend: React/Vue
- Backend: Django/Flask/FastAPI
- Database: PostgreSQL
- Auth: JWT/Session

**Use Cases:**
- Web applications
- Dashboards
- Member areas
- SaaS products

---


### 4. ML Template ⭐⭐⭐

**Path:** `templates/ml_template/`

**Description:** Machine Learning project structure

**Features:**
- Data preprocessing
- Model training
- Model evaluation
- API deployment
- Experiment tracking

**Tech Stack:**
- Python 3.9+
- TensorFlow/PyTorch
- FastAPI
- MLflow

**Use Cases:**
- ML projects
- Data science
- Model deployment
- Research projects

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

**Use Cases:**
- Testing any project
- QA automation
- CI/CD pipelines

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
- Notific
template for you..."
   ```

2. **User mentions specific project type**
   ```
   User: "Build a charity donation platform"
   Augment: "We have a Charity Management template..."
   ```

3. **User asks for project structure**
   ```
   User: "How should I structure an AI assistant?"
   Augment: "Use our AI Assistant template..."
   ```

### Template Selection

Match user intent to template:

| User Intent | Template |
|-------------|----------|
| "ERP", "business management" | ERP System |
| "landing page", "website" | Web Page |
| "web app", "login system" | Web Page with Login |
| "machine learning", "ML project" | ML Template |
| "testing", "test automation" | Test Template |
| "email campaign", "newsletter" | Email Template |
| "chatbot", "AI assistant" | AI Assistant |
| "charity", "donations", "NGO" | Charity Management |
| "prediction", "forecasting" | AI Prediction |

### Generation Workflow

1. **Identify need**
   - Detect project type from user request

2. **Suggest template