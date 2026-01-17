import requests
import json
import traceback

try:
    response = requests.post(
        'http://localhost:5005/api/auth/login',
        json={'username': 'admin', 'password': 'admin123'},
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
