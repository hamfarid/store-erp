# 🧠 Lessons Learned & Error Journal (Global System Ultimate)

**Purpose:** Institutional memory for errors, fixes, and best practices.
**Directive:** Consult this file before retrying a failed task (Tier 2 Escalation).

## [2024-02-15] - Versioning Strategy
**Error:** Hardcoding version numbers (e.g., Global System Ultimate) in 180+ files made updates painful and error-prone.
**Solution:** Adopted a "Version Agnostic" approach. The system is now referred to as "Global System Ultimate" in all documentation. Version numbers are kept only in `package.json` or a single `VERSION` file if needed.
**Lesson:** decoupling branding from semantic versioning reduces maintenance overhead.

## [2024-02-15] - Memory Bank Location
**Error:** Using a hidden `.memory/` folder caused confusion for some IDEs and agents that ignore dotfiles by default.
**Solution:** Migrated to `memory-bank/` (no dot).
**Lesson:** Explicit is better than implicit. Critical system state should be visible.

## [2024-02-15] - Path Handling in Scripts
**Error:** Python scripts failed when run from different directories because they relied on relative paths like `../`.
**Solution:** Updated all scripts (`activate_global.py`, `preflight_check.py`) to calculate absolute paths based on `__file__`.
**Lesson:** Always use `os.path.abspath(__file__)` to anchor scripts to their own location, making them portable.

---

## ➕ New Lesson Template

### [YYYY-MM-DD] - [Topic]
**Error:** [What went wrong?]
**Solution:** [How was it fixed?]
**Lesson:** [What is the general principle to apply in the future?]
