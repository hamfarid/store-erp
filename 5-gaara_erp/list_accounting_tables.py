import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.gaara_erp.accounting_migration_settings')
django.setup()
from django.db import connection
cur = connection.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'accounting_%';")
print('ACCOUNTING TABLES:', [r[0] for r in cur.fetchall()])
cur.execute("SELECT app,name FROM django_migrations WHERE app='accounting' ORDER BY id;")
print('Applied accounting migrations:', cur.fetchall())
