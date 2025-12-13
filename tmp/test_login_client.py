import sys
sys.path.insert(0, 'backend')
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.post('/api/auth/login', json={'username':'wrong','password':'nope'})
    print('STATUS', r.status_code)
    print(r.get_data(as_text=True))
