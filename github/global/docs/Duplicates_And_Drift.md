# FILE: docs/Duplicates_And_Drift.md | PURPOSE: Semantic duplication & drift analysis | OWNER: Architecture | RELATED: docs/Class_Registry.md | LAST-AUDITED: 2025-10-21

# Duplicates & Drift — الازدواجية والانجراف

**Version**: 1.0  
**Last Updated**: 2025-10-21

---

## 1. Definitions

- **Semantic Duplicate**: Two or more modules/functions/classes performing similar roles with different names or locations.
- **Drift**: Divergence between canonical design/specification and actual implementation.

---

## 2. Canonical Registry (Source of Truth)

- `/docs/Class_Registry.md` — One canonical per domain model (append-only)

---

## 3. Known Duplicates (Examples)

- `Invoice` vs `LegacyInvoice` — Legacy marked `__abstract__ = True`
- `Product` duplicated in `product_unified.py` and legacy `product.py` — unified kept
- `auth_unified.py` vs `auth_routes.py` — `auth_unified` chosen as canonical

---

## 4. Policy

1. Always search the repository before creating a new module/class/function.
2. If a duplicate is found:
   - Merge into canonical implementation
   - Move duplicate to `/unneeded/<original>.removed.<ext>`
   - Add pointer note with commit ID
3. Update `/docs/Class_Registry.md` with migration notes
4. Add tests to ensure parity and prevent regression

---

## 5. Detection Methods

- Regex & AST search
- Import graph & call graph analysis
- Git history diff
- Code similarity (tokens/AST)

---

## 6. Automation (Scripts)

- Extend `scripts/audit_repo.py` to detect:
  - Same class names in multiple files
  - Similar function names/signatures across modules
  - Orphaned files (no imports)
  - Divergence from Class_Registry

---

## 7. Acceptance Criteria

- [ ] Canonical implementation exists for each domain model
- [ ] All duplicates moved to `/unneeded` with pointers
- [ ] Class_Registry updated
- [ ] Drift documented and remediated
- [ ] CI gate blocks PRs with new duplicates

