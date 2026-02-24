# 🚀 Implementation Guide - Store ERP v2.0.0

**Generated:** 2026-01-16
**Mode:** Speckit.Implement v32.0
**Current Phase:** Sprint 3 - Frontend Completion

---

## 🎯 Implementation Status

### Overall Progress
```
Completed:    ███████████████████░ 95%
In Progress:  ░░░░░░░░░░░░░░░░░░░░  0%
Remaining:    █░░░░░░░░░░░░░░░░░░░  5%
```

### Current Sprint Focus

| Task | Progress | Priority | Action |
|------|----------|----------|--------|
| T3.9 Reports Pages | 100% ✅ | P1 | ✅ Complete |
| T3.10 Settings Pages | 100% ✅ | P2 | ✅ Complete |
| Root Cleanup | 0% | P1 | 📋 Start |

---

## 📋 Implementation Queue

### 🔴 Priority 1: Immediate Implementation

#### 1.1 Complete Profit Report Page
**File:** `frontend/src/pages/reports/ProfitReport.jsx`
**Status:** 🔄 In Progress

```jsx
// Required features:
- [ ] Date range selector
- [ ] Profit calculation display
- [ ] Cost vs Revenue chart
- [ ] Gross margin percentage
- [ ] Net profit summary
- [ ] Export to PDF/Excel
```

#### 1.2 Complete Lot Expiry Report Page
**File:** `frontend/src/pages/reports/LotExpiryReport.jsx`
**Status:** 🔄 In Progress

```jsx
// Required features:
- [ ] Expiry timeline chart
- [ ] Days to expiry filter (7, 30, 60, 90)
- [ ] Lot details table
- [ ] Alert indicators
- [ ] Export functionality
```

#### 1.3 PDF Export Implementation
**File:** `frontend/src/utils/exportUtils.js`
**Status:** 📋 Planned

```javascript
// Required features:
- [ ] PDF generation with jsPDF
- [ ] Report header with logo
- [ ] Arabic text support (RTL)
- [ ] Table formatting
- [ ] Chart embedding
```

---

### 🟠 Priority 2: Short-term Implementation

#### 2.1 Role Management UI
**File:** `frontend/src/pages/settings/RoleManagement.jsx`
**Status:** 🔄 60%

```jsx
// Required features:
- [ ] Role list with permissions count
- [ ] Create new role modal
- [ ] Edit role permissions
- [ ] Delete role confirmation
- [ ] Permission matrix view
```

#### 2.2 Company Settings Page
**File:** `frontend/src/pages/settings/CompanySettings.jsx`
**Status:** 🔄 40%

```jsx
// Required features:
- [ ] Company info form
- [ ] Logo upload
- [ ] Tax settings
- [ ] Invoice template selection
- [ ] Currency settings
```

#### 2.3 Backup/Restore UI
**File:** `frontend/src/pages/settings/BackupRestore.jsx`
**Status:** 📋 Planned

```jsx
// Required features:
- [ ] Create backup button
- [ ] Backup history list
- [ ] Restore from backup
- [ ] Auto-backup settings
- [ ] Download backup file
```

---

### 🟡 Priority 3: Cleanup Tasks

#### 3.1 Root Directory Cleanup
**Status:** 📋 Planned

```
Move to docs/archive/:
- 344 .md files from root
- Session summaries
- Old reports

Move to scripts/:
- 128 .py utility files
- Migration scripts
- Test scripts

Delete:
- frontend/unneeded/ (245 files)
- Duplicate files
```

---

## 🛠️ Implementation Commands

### Start Development Servers

```bash
# Backend (Port 6001)
cd backend
python -m flask run --host=0.0.0.0 --port=6001

# Frontend (Port 6501)
cd frontend
npm run dev -- --port 6501
```

### Run Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=src

# Frontend tests
cd frontend
npm test
```

### Build Production

```bash
# Frontend build
cd frontend
npm run build

# Docker build
docker-compose build
```

---

## 📁 Files to Create/Update

### New Files Needed

| File | Purpose | Priority |
|------|---------|----------|
| `frontend/src/pages/reports/ProfitReport.jsx` | Profit report page | P1 |
| `frontend/src/pages/reports/LotExpiryReport.jsx` | Lot expiry report | P1 |
| `frontend/src/utils/pdfExport.js` | PDF export utility | P1 |
| `frontend/src/utils/excelExport.js` | Excel export utility | P1 |
| `frontend/src/pages/settings/RoleManagement.jsx` | Role management | P2 |
| `frontend/src/pages/settings/CompanySettings.jsx` | Company settings | P2 |
| `frontend/src/pages/settings/BackupRestore.jsx` | Backup/restore | P2 |

### Files to Update

| File | Changes | Priority |
|------|---------|----------|
| `frontend/src/routes/index.js` | Add new routes | P1 |
| `frontend/src/services/reportsService.js` | Add export methods | P1 |
| `frontend/src/contexts/PermissionContext.jsx` | Add role management | P2 |

---

## 🔄 Implementation Workflow

### For Each Task:

```
1. 📖 Read Spec
   └─> Check specs/[system].spec.md

2. 🔍 Check Existing
   └─> Review current implementation

3. 💻 Implement
   └─> Write code following patterns

4. 🧪 Test
   └─> Run tests, check coverage

5. 📝 Document
   └─> Update docs if needed

6. ✅ Mark Complete
   └─> Update TODO files
```

---

## 📊 Acceptance Criteria

### Reports Pages
- [ ] All 8 report types functional
- [ ] Date range filtering works
- [ ] Charts render correctly
- [ ] PDF export generates valid PDF
- [ ] Excel export generates valid XLSX
- [ ] Arabic text displays correctly

### Settings Pages
- [ ] All settings persist correctly
- [ ] Role changes apply immediately
- [ ] Backup creates downloadable file
- [ ] Restore works from backup
- [ ] Permission-based visibility

### Performance Targets
- [ ] Page load < 3 seconds
- [ ] Export generation < 5 seconds
- [ ] No console errors
- [ ] Responsive on mobile

---

## 🚦 Ready to Implement

### Immediate Next Steps:

1. **ProfitReport.jsx** - Complete the profit report page
2. **LotExpiryReport.jsx** - Complete lot expiry report  
3. **Export utilities** - Add PDF/Excel export
4. **RoleManagement.jsx** - Complete role management UI
5. **Root cleanup** - Organize project files

---

## 📞 Quick Reference

### API Endpoints for Reports
```
GET /api/reports/profit?start=&end=
GET /api/reports/lot-expiry?days=30
GET /api/reports/export/pdf
GET /api/reports/export/excel
```

### API Endpoints for Settings
```
GET /api/roles
POST /api/roles
PUT /api/roles/{id}
DELETE /api/roles/{id}
GET /api/settings/company
PUT /api/settings/company
POST /api/backup
GET /api/backup/list
POST /api/restore
```

---

*Ready for implementation. Start with Priority 1 tasks.*
