# FILE: docs/Imports_Map.md | PURPOSE: Import dependency map | OWNER: Architecture | RELATED: docs/Symbol_Index.md | LAST-AUDITED: 2025-10-21

# Imports Map — خريطة الاستيراد

Version: 1.0  
Last Updated: 2025-10-21

—

## 1. High-Level Graph

- backend/app.py
  -> src/routes/* (blueprints)
  -> src/database/db.py (db)
  -> src/models/* (ORM)
  -> src/utils/* (helpers)

- src/routes/auth_unified.py
  -> src/models/user_unified.py
  -> src/utils/security.py
  -> src/utils/errors.py

- src/routes/products.py
  -> src/models/product_unified.py
  -> src/utils/errors.py

- src/routes/invoices.py
  -> src/models/invoice_unified.py
  -> src/models/supporting_models.py
  -> src/utils/errors.py

- src/models/*
  -> src/database/db.py (single SQLAlchemy instance)

## 2. Notes

- Ensure all imports use `src.routes.*` and `src.models.*` (no bare `routes.*`)
- Avoid circular imports by using application factory and deferred imports in blueprints
- Use fully qualified relationship targets in SQLAlchemy to avoid mapper conflicts

## 3. Known Circular Risks

- routes → models → routes (avoid importing routes inside models)
- utils/errors.py importing Flask app (avoid; use lightweight helpers only)

## 4. Actions

- [ ] Run static analysis to generate DOT graph (e.g., `pydeps`)
- [ ] Add CI job to detect new cycles
- [ ] Enforce single `db` import from `src.database.db`

