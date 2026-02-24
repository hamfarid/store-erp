import sys
sys.path.append('backend')
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/api/system/health')
    print('CODE', r.status_code)
    for k in ['Content-Security-Policy','Strict-Transport-Security','X-XSS-Protection','X-Content-Type-Options','X-Frame-Options','Referrer-Policy','Cache-Control']:
        print(k, r.headers.get(k))

