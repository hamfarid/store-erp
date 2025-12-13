#!/usr/bin/env python3
"""
Test script to verify all Backend API fixes
Tests Users, Products, Customers, Suppliers, Categories endpoints
"""

import requests
import json

# Backend URL
BASE_URL = "http://localhost:5002"

# First, login to get token
def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') and data.get('data', {}).get('access_token'):
            token = data['data']['access_token']
            print(f"✅ Login successful! Token: {token[:20]}...")
            return token
    
    print(f"❌ Login failed: {response.status_code}")
    print(response.text)
    return None

def test_endpoint(name, url, token):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Response keys: {list(data.keys())}")
            
            if 'data' in data:
                data_obj = data['data']
                if isinstance(data_obj, dict):
                    print(f"Data keys: {list(data_obj.keys())}")
                    # Check for expected arrays
                    for key in ['users', 'products', 'customers', 'suppliers', 'categories']:
                        if key in data_obj:
                            items = data_obj[key]
                            print(f"  - {key}: {len(items)} items")
                            if items:
                                print(f"    First item keys: {list(items[0].keys())[:5]}...")
                elif isinstance(data_obj, list):
                    print(f"Data is array: {len(data_obj)} items")
                else:
                    print(f"Data type: {type(data_obj)}")
            
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("Backend API Fix Verification")
    print("="*60)
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        return
    
    # Test endpoints
    endpoints = [
        ("Users", f"{BASE_URL}/api/users"),
        ("Products", f"{BASE_URL}/api/products"),
        ("Customers", f"{BASE_URL}/api/customers"),
        ("Suppliers", f"{BASE_URL}/api/suppliers"),
        ("Categories", f"{BASE_URL}/api/categories"),
    ]
    
    results = {}
    for name, url in endpoints:
        results[name] = test_endpoint(name, url, token)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("🎉 All APIs working correctly!")
    else:
        print("⚠️ Some APIs need attention")

if __name__ == "__main__":
    main()
