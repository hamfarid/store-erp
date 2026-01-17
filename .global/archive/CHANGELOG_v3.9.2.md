# Changelog v3.9.2 - Generic Edition

## [3.9.2] - 2025-11-02

### 🎯 Major Improvement: Generic Variables

**Removed hardcoded values and replaced with generic placeholders**

This release makes the prompt **truly generic** and **project-agnostic** by replacing all hardcoded values with placeholder variables.

---

## ✨ What Changed

### Problem

The previous versions (v3.9.0, v3.9.1) contained **hardcoded values** that were specific to one project:

❌ **Project name:** "Gaara ERP" (specific project)  
❌ **Database name:** "gaara_erp" (specific database)  
❌ **Port numbers:** 3000, 5000, 5432 (specific ports)  
❌ **Hostnames:** localhost (specific host)  
❌ **Credentials:** user:password (example credentials)

**This made the prompt less generic and potentially confusing for other projects.**

---

### Solution

Replaced all hardcoded values with **generic placeholder variables**:

| Old Value | New Value | Description |
|-----------|-----------|-------------|
| `Gaara ERP` | `{YOUR_PROJECT_NAME}` | Project/application name |
| `gaara_erp` | `{your_database_name}` | Database name |
| `:3000` | `:{FRONTEND_PORT}` | Frontend port |
| `:5000` | `:{BACKEND_PORT}` | Backend port |
| `:5432` | `:{DB_PORT}` | Database port |
| `localhost` | `{HOST}` | Host/domain |
| `user:password` | `{DB_USER}:{DB_PASSWORD}` | Database credentials |

---

## 📊 Replacements Summary

### Statistics

| Replacement | Count | Impact |
|-------------|-------|--------|
| `Gaara ERP` → `{YOUR_PROJECT_NAME}` | 3 | ✅ Generic |
| `gaara_erp` → `{your_database_name}` | 4 | ✅ Generic |
| `:3000` → `:{FRONTEND_PORT}` | 12 | ✅ Generic |
| `:5000` → `:{BACKEND_PORT}` | 2 | ✅ Generic |
| `:5432` → `:{DB_PORT}` | 1 | ✅ Generic |
| `localhost` → `{HOST}` | 22 | ✅ Generic |
| `user:password` → `{DB_USER}:{DB_PASSWORD}` | 1 | ✅ Generic |
| **Total** | **45** | **100% Generic** |

---

## 🎨 New Feature: Variables Section

Added a new **PLACEHOLDER VARIABLES** section at the beginning of the prompt:

```
⸻

PLACEHOLDER VARIABLES:
This prompt uses placeholder variables that should be replaced with your actual values:

Configuration Variables:
• {YOUR_PROJECT_NAME}    - Replace with your project/application name
• {your_database_name}   - Replace with your database name
• {HOST}                 - Replace with your host (e.g., localhost, your-domain.com)
• {FRONTEND_PORT}        - Replace with your frontend port (e.g., 3000, 8080)
• {BACKEND_PORT}         - Replace with your backend port (e.g., 5000, 8000)
• {DB_PORT}              - Replace with your database port (e.g., 5432 for PostgreSQL, 3306 for MySQL)
• {DB_USER}              - Replace with your database username
• {DB_PASSWORD}          - Replace with your database password
• {database_name}        - Replace with your specific database name

Example Replacements:
Before: APP_NAME="{YOUR_PROJECT_NAME}"
After:  APP_NAME="MyAwesomeApp"

Before: DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{your_database_name}
After:  DATABASE_URL=postgresql://admin:secret123@localhost:5432/myapp_db

Note: These are placeholders for examples and should be customized for your specific project.

⸻
```

This section:
- ✅ Explains all placeholder variables
- ✅ Shows example replacements
- ✅ Guides users on customization
- ✅ Makes the prompt self-documenting

---

## 📈 Version Comparison

| Metric | v3.9.1 | v3.9.2 | Change |
|--------|--------|--------|--------|
| **Lines** | 8,752 | 8,780 | **+28** |
| **Size** | 209K | 211K | **+2K** |
| **Hardcoded Values** | 45 | 0 | **-45 ✅** |
| **Generic Variables** | 0 | 7 types | **+7 ✅** |
| **Documentation** | - | Variables section | **+1 section ✅** |

---

## ✅ Benefits

### 1. Truly Generic

- ✅ No project-specific values
- ✅ Works for any project
- ✅ No confusion about "Gaara ERP"
- ✅ Clear placeholders

### 2. Better Documentation

- ✅ Variables section explains everything
- ✅ Example replacements provided
- ✅ Self-documenting
- ✅ Easy to customize

### 3. Professional

- ✅ Industry-standard placeholder format
- ✅ Clear naming conventions
- ✅ Consistent style
- ✅ Production-ready

### 4. User-Friendly

- ✅ Clear what to replace
- ✅ Examples provided
- ✅ No guessing needed
- ✅ Copy-paste friendly

---

## 🎯 Use Cases

### Before v3.9.2 (Confusing)

```python
# User sees this and thinks: "What is Gaara ERP? Is this for that project only?"
APP_NAME="Gaara ERP"
DB_NAME=gaara_erp
APP_URL=http://localhost:5000
```

### After v3.9.2 (Clear)

```python
# User sees this and knows: "I need to replace these with my values"
APP_NAME="{YOUR_PROJECT_NAME}"
DB_NAME={your_database_name}
APP_URL=http://{HOST}:{BACKEND_PORT}
```

---

## 📋 Migration Guide

### From v3.9.1 to v3.9.2

**No action required for most users**

If you were using v3.9.1 and:
- Ignored "Gaara ERP" references → v3.9.2 is clearer
- Replaced values manually → v3.9.2 makes it official
- Were confused → v3.9.2 solves the confusion

### To Update

```bash
# Simply replace the file
cp GLOBAL_GUIDELINES_v3.9.2.txt ~/augment/prompts/

# Read the new PLACEHOLDER VARIABLES section
head -n 50 GLOBAL_GUIDELINES_v3.9.2.txt

# Replace placeholders with your values (optional)
# Or leave them as-is for examples
```

---

## 🔍 Examples

### Example 1: Django Project

```python
# Before (v3.9.1)
APP_NAME="Gaara ERP"  # Confusing!

# After (v3.9.2)
APP_NAME="{YOUR_PROJECT_NAME}"

# Your replacement
APP_NAME="MyDjangoShop"
```

### Example 2: FastAPI Project

```python
# Before (v3.9.1)
DATABASE_URL=postgresql://user:password@localhost:5432/gaara_erp

# After (v3.9.2)
DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{your_database_name}

# Your replacement
DATABASE_URL=postgresql://admin:secret@db.example.com:5432/fastapi_db
```

### Example 3: React Frontend

```javascript
// Before (v3.9.1)
const API_URL = "http://localhost:5000";  // Hardcoded!

// After (v3.9.2)
const API_URL = "http://{HOST}:{BACKEND_PORT}";

// Your replacement
const API_URL = "http://api.myapp.com:8000";
```

---

## 📁 Files

### Main Files

- **GLOBAL_GUIDELINES_v3.9.2.txt** - Generic version (8,780 lines) ⭐
- **GLOBAL_GUIDELINES_FINAL.txt** - Same as v3.9.2 (latest)
- **GLOBAL_GUIDELINES_v3.9.1.txt** - Previous version (8,752 lines)

### Changes

```diff
+ Added PLACEHOLDER VARIABLES section (28 lines)
+ Replaced "Gaara ERP" with {YOUR_PROJECT_NAME} (3 times)
+ Replaced "gaara_erp" with {your_database_name} (4 times)
+ Replaced ":3000" with :{FRONTEND_PORT} (12 times)
+ Replaced ":5000" with :{BACKEND_PORT} (2 times)
+ Replaced ":5432" with :{DB_PORT} (1 time)
+ Replaced "localhost" with {HOST} (22 times)
+ Replaced "user:password" with {DB_USER}:{DB_PASSWORD} (1 time)
```

---

## ✨ Summary

Version 3.9.2 makes the prompt **truly generic**:

✅ **45 hardcoded values removed**  
✅ **7 generic variable types added**  
✅ **1 documentation section added**  
✅ **100% project-agnostic**  
✅ **Clear and professional**  
✅ **User-friendly**

**Perfect for:**
- Any project (not just "Gaara ERP")
- Any technology stack
- Any configuration
- Professional use

**No more confusion about project-specific values!**

---

## 🔮 What's Next

### Planned for v4.0.0

- [ ] Interactive variable replacement
- [ ] Project-specific profiles
- [ ] Auto-detection of values
- [ ] Configuration wizard
- [ ] Multi-project support

---

## 📞 Support

### Questions?

- **GitHub Issues:** https://github.com/hamfarid/global/issues
- **Discussions:** https://github.com/hamfarid/global/discussions
- **Documentation:** PLACEHOLDER VARIABLES section in prompt

### Need Help Replacing Variables?

See the **PLACEHOLDER VARIABLES** section at the beginning of the prompt for:
- Complete list of variables
- Example replacements
- Usage guidelines

---

**Full Changelog:** https://github.com/hamfarid/global/compare/v3.9.1...v3.9.2

---

**Release Date:** 2025-11-02  
**Version:** 3.9.2  
**Type:** Generic Variables Release  
**Status:** ✅ Stable  
**Recommended:** Yes ⭐⭐⭐

---

## Note

This release focuses on making the prompt **truly generic** and **project-agnostic**. All hardcoded, project-specific values have been replaced with clear placeholder variables that can be easily customized for any project.

