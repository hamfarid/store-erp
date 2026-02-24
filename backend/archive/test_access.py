import requests
import json

BASE_URL = "http://localhost:5005"


def test_login_and_access():
    # 1. Login
    login_url = f"{BASE_URL}/api/auth/login"
    credentials = {
        "username": "admin",
        "password": "admin123"
    }

    print(f"Attempting login to {login_url}...")
    try:
        response = requests.post(login_url, json=credentials)
        print(f"Login Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return

        data = response.json()
        # Handle nested data structure
        if 'data' in data:
            token = data['data'].get("access_token")
        else:
            token = data.get("access_token")

        if not token:
            print("No access token returned!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return

        print(f"✅ Login successful. Token: {token[:30]}...")

        # 2. Access protected routes
        routes = [
            "/api/products",
            "/api/warehouses",
            "/api/partners/customers"
        ]

        headers = {
            "Authorization": f"Bearer {token}"
        }

        for route in routes:
            url = f"{BASE_URL}{route}"
            print(f"\n🔍 Testing route: {url}")
            resp = requests.get(url, headers=headers)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                print(f"✅ Success!")
            else:
                print(f"❌ Failed: {resp.text[:200]}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_login_and_access()
