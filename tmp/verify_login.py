import sys, json, traceback
sys.path.insert(0, 'backend')

try:
    from app import create_app
except Exception as e:
    print('IMPORT_APP_ERROR', type(e).__name__, str(e))
    traceback.print_exc()
    raise

app = create_app()

try:
    with app.app_context():
        from src.models.invoice_unified import Invoice, InvoiceItem
        from src.models.supporting_models import Payment
        print('MAPPED', Invoice.__table__.name, InvoiceItem.__table__.name, Payment.__table__.name)
except Exception as e:
    print('MAPPER_ERROR', type(e).__name__, str(e))
    traceback.print_exc()
    raise

try:
    with app.test_client() as c:
        h = c.get('/api/health')
        print('HEALTH_STATUS', h.status_code)
        r = c.post('/api/auth/login', json={'username':'wrong','password':'nope'})
        print('LOGIN_STATUS', r.status_code)
        try:
            print('LOGIN_JSON', json.dumps(r.get_json(), ensure_ascii=False))
        except Exception:
            print('LOGIN_TEXT', r.get_data(as_text=True))
except Exception as e:
    print('TEST_ERROR', type(e).__name__, str(e))
    traceback.print_exc()
    raise

