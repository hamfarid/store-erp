# 🔍 DATA SOURCE CHECKER - فحص مصدر البيانات
# يتحقق من مصدر البيانات: Database أم Frontend

import requests
import json
from datetime import datetime

print("=" * 60)
print("📊 DATA SOURCE VERIFICATION")
print("   التحقق من مصدر البيانات")
print("=" * 60)

BASE_URL = "http://localhost:5002/api"
headers = {
    'Content-Type': 'application/json'
}

# Login to get token
print("\n🔐 1. Logging in...")
try:
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "admin123", "use_jwt": True},
        headers=headers
    )
    if login_response.status_code == 200:
        data = login_response.json()
        token = data['data']['access_token']
        headers['Authorization'] = f'Bearer {token}'
        print("   ✅ Login successful")
    else:
        print(f"   ❌ Login failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Connection error: {e}")
    exit(1)

# Check endpoints
endpoints = {
    "Users": "/users",
    "Products": "/products",
    "Customers": "/customers",
    "Suppliers": "/suppliers",
    "Categories": "/categories",
    "Warehouses": "/warehouses",
    "Invoices": "/invoices"
}

print("\n📡 2. Checking API Endpoints...")
print("-" * 60)

results = {}
for name, endpoint in endpoints.items():
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Check data structure
            if 'data' in data:
                items = data['data'].get(f'{name.lower()}', [])
                if isinstance(items, list):
                    count = len(items)
                else:
                    count = 0
                results[name] = {
                    "status": "✅ Connected",
                    "count": count,
                    "source": "🗄️ Database" if count > 0 else "⚠️ Empty DB"
                }
            else:
                results[name] = {
                    "status": "⚠️ No data key",
                    "count": 0,
                    "source": "❓ Unknown"
                }
        elif response.status_code == 404:
            results[name] = {
                "status": "❌ Not Found (404)",
                "count": 0,
                "source": "⚠️ Endpoint Missing"
            }
        elif response.status_code == 401:
            results[name] = {
                "status": "🔒 Unauthorized (401)",
                "count": 0,
                "source": "⚠️ Auth Issue"
            }
        else:
            results[name] = {
                "status": f"❌ Error ({response.status_code})",
                "count": 0,
                "source": "⚠️ API Error"
            }
    except Exception as e:
        results[name] = {
            "status": f"❌ Exception",
            "count": 0,
            "source": f"⚠️ {str(e)[:30]}"
        }

# Print results
print(f"\n{'Endpoint':<15} {'Status':<25} {'Count':<10} {'Source':<20}")
print("-" * 70)
for name, result in results.items():
    print(f"{name:<15} {result['status']:<25} {result['count']:<10} {result['source']:<20}")

# Check Frontend hardcoded data
print("\n" + "=" * 60)
print("🔍 3. Frontend Hardcoded Data Check")
print("-" * 60)

frontend_files = {
    "UserManagement": "frontend/src/components/UserManagementComplete.jsx",
    "Products": "frontend/src/components/ProductManagementComplete.jsx",
    "Customers": "frontend/src/components/CustomersAdvanced.jsx",
    "Suppliers": "frontend/src/components/SuppliersAdvanced.jsx"
}

import os
for name, filepath in frontend_files.items():
    full_path = os.path.join("d:\\APPS_AI\\store\\Store", filepath)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'demoUsers' in content or 'demoProducts' in content or 'demoData' in content:
                print(f"⚠️  {name:<15} HAS hardcoded demo data")
            elif 'const users = [' in content or 'const products = [' in content:
                print(f"⚠️  {name:<15} HAS hardcoded array data")
            elif 'fetch(' in content or 'apiClient.get' in content:
                print(f"✅ {name:<15} Uses API calls")
            else:
                print(f"❓ {name:<15} Unknown data source")
    else:
        print(f"❌ {name:<15} File not found")

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY - الملخص")
print("-" * 60)

api_connected = sum(1 for r in results.values() if r['status'].startswith('✅'))
api_empty = sum(1 for r in results.values() if 'Empty' in r['source'])
api_error = len(results) - api_connected - api_empty

print(f"✅ API Endpoints Working:  {api_connected}/{len(results)}")
print(f"⚠️  API Endpoints Empty:    {api_empty}/{len(results)}")
print(f"❌ API Endpoints Error:    {api_error}/{len(results)}")

if api_connected == len(results):
    print("\n🟢 All APIs Connected - البيانات من Database")
elif api_empty > 0:
    print("\n🟡 APIs Connected but Empty - قواعد البيانات فارغة")
    print("   💡 Need to add data via Admin Panel or SQL")
else:
    print("\n🔴 APIs Have Errors - مشاكل في الاتصال")
    print("   💡 Check Backend logs and routes")

print("\n" + "=" * 60)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
