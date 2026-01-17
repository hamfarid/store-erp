# Global Tools

**Based on:** Global Professional Core Prompt v33.2 (The Adoption Edition)

---

## 🛠️ Available Tools

### 1. Lifecycle Maestro (`lifecycle.py`)

The **ONLY** entry point for project lifecycle management.

```bash
python3 global/tools/lifecycle.py "<Project Name>" "<Description>"
```

**Features:**
- Auto-detects New Project (Genesis) or Existing Project (Adoption)
- Generates Constitution document
- Creates Project Plan
- Initializes file registry

---

### 2. Librarian (`librarian.py`)

File registry manager for the Librarian Protocol.

```bash
# Check if a file exists
python3 global/tools/librarian.py check <file_path>

# Register a file
python3 global/tools/librarian.py register <file_path> "<purpose>" [category]

# Search for files
python3 global/tools/librarian.py search <pattern>

# List all registered files
python3 global/tools/librarian.py list

# View audit log
python3 global/tools/librarian.py audit

# Display Verification Oath
python3 global/tools/librarian.py oath
```

**Features:**
- File existence verification
- File registration with purpose tracking
- Pattern-based file search
- Audit logging

---

### 3. Speckit Bridge (`speckit_bridge.py`)

Spec file manager for "No Code Without Spec" mandate.

```bash
# Create a spec file
python3 global/tools/speckit_bridge.py create <feature_name> [type]

# Validate a spec file
python3 global/tools/speckit_bridge.py validate <spec_path>

# List all spec files
python3 global/tools/speckit_bridge.py list
```

**Spec Types:**
- `feature` - Feature specifications
- `api` - API endpoint specifications
- `component` - Component specifications
- `migration` - Database migration specifications

---

## 📋 Workflow

```
1. Run lifecycle.py to initialize project
   ↓
2. Use librarian.py to verify files before creating
   ↓
3. Use speckit_bridge.py to create spec before coding
   ↓
4. Implement code following the spec
   ↓
5. Validate spec completion
```

---

## 🔒 Core Mandates

1. **No Code Without Spec** - Create .spec.md before implementation
2. **Absolute Paths Only** - Avoid path confusion
3. **Verify Before Create** - Check file_registry.json first
4. **Atomic Updates** - Update docs with code
5. **Respect Legacy** - Don't delete existing without authorization

---

## 📁 Output Locations

| Tool | Output |
|------|--------|
| lifecycle.py | `docs/CONSTITUTION.md`, `docs/PROJECT_PLAN.md` |
| librarian.py | `.memory/file_registry.json` |
| speckit_bridge.py | `specs/[type]/*.spec.md` |

---

## 🎓 Remember

> **"The system that plans before it builds, and adopts what exists."**

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
