# Global - Professional Development Framework

**Based on:** Global Professional Core Prompt v33.2 (The Adoption Edition)
**Project:** Store Management System

---

## 🎯 Purpose

This directory contains the global development framework that guides all work on this project.
It implements the "System That Plans Before It Builds, and Adopts What Exists".

---

## 📁 Structure

```
global/
├── README.md              # This file
├── tools/                 # Development tools
│   ├── lifecycle.py       # Project lifecycle management
│   ├── librarian.py       # File registry manager
│   ├── speckit_bridge.py  # Spec file manager
│   └── README.md          # Tools documentation
└── rules/                 # Development rules
    ├── 99_context_first.md     # Context-first development
    ├── 100_evolution_engine.md # Self-improvement
    └── README.md          # Rules index
```

---

## 🚀 Quick Start

### 1. Initialize Project Lifecycle

```bash
python3 global/tools/lifecycle.py "Store Management System" "Inventory and ERP solution"
```

### 2. Check File Before Creating

```bash
python3 global/tools/librarian.py check path/to/file.py
```

### 3. Create Spec Before Coding

```bash
python3 global/tools/speckit_bridge.py create feature-name
```

---

## 📜 Core Mandates

1. **No Code Without Spec** - Create .spec.md before implementation
2. **Absolute Paths Only** - Use full paths to avoid confusion
3. **Verify Before Create** - Check file_registry.json first
4. **Atomic Updates** - Documentation with code, not after
5. **Respect Legacy** - Don't delete existing without authorization

---

## 🧠 Thinking Process (v33.2)

1. **Analyze** - What does the user want?
2. **Lifecycle** - Run lifecycle.py to generate plan
3. **Librarian** - Check if files exist
4. **Shadow** - Critique the plan
5. **Oath** - Swear verification
6. **Execute** - Write code
7. **Evolve** - Learn from errors

---

## 📋 Activation Protocol

When starting a new task:

1. ✅ Run lifecycle.py (if first time)
2. ✅ Initialize file_registry.json
3. ✅ Read 99_context_first.md
4. ✅ Critique plan using thinking.md
5. ✅ Swear Verification Oath before imports
6. ✅ Execute with quality

---

## 🔗 Related Locations

| Location | Purpose |
|----------|---------|
| `.memory/` | Memory and context storage |
| `docs/` | Project documentation |
| `specs/` | Specification files |
| `rules/` | Project-specific rules |
| `prompts/` | AI prompts |

---

## ⚠️ Important Notes

### This is NOT a standalone project

This `global/` folder is part of the Store Management System project.
The actual global guidelines source is at `D:\Ai_Project\github\global\`.

### Project vs Global Guidelines

- **Global Guidelines** (`github/global/`) - HOW to work
- **This Project** (`6-store/`) - WHAT to build

Never confuse the two. This project follows the guidelines, but the code lives here.

---

## 🎓 Remember

> **"The system that plans before it builds, and adopts what exists."**

This is the Law.

---

**Version:** 1.0.0
**Last Updated:** 2025-01-16
