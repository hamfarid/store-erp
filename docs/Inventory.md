# Inventory (PASS 0)

- Backend: Flask app (backend/app.py, backend/wsgi.py), SQLAlchemy models under backend/src/models/**, 55+ blueprints under backend/src/routes/**.
- Frontend: React/Vite (port 5502) [not inventoried here].
- Auth: backend/src/routes/auth_unified.py (canonical), auth_routes.py (delegates).
- Database: SQLAlchemy via src.database.db; canonical models: product_unified.py, invoice_unified.py, user_unified.py, supporting_models.py, etc.
- Duplicates: backend/init_db.py, ./init_db.py, possible legacy invoice.py/invoices.py.
- Env: .env (production settings present).
