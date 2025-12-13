#!/usr/bin/env python3
"""Quick endpoint testing script"""
import requests
import json

BASE_URL = "http://127.0.0.1:5002"

def test_endpoints():
    print("=" * 50)
    print("Testing Store API Endpoints")
    print("=" * 50)
    
    # Test 1: Login
    print("\n[1] Testing Login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        response.raise_for_status()
        data = response.json()
        token = data['data']['access_token']
        print(f"✓ Login successful! Token: {token[:50]}...")
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return
    
    # Test 2: Test Route
    print("\n[2] Testing accounting test route...")
    try:
        response = requests.get(f"{BASE_URL}/api/accounting/test")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Test route: {data['message']}")
    except Exception as e:
        print(f"✗ Test route failed: {e}")
    
    # Test 3: Currencies
    print("\n[3] Testing currencies...")
    try:
        response = requests.get(f"{BASE_URL}/api/accounting/currencies", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Currencies: {len(data['data'])} found")
    except Exception as e:
        print(f"✗ Currencies failed: {e}")
    
    # Test 4: Cash Boxes
    print("\n[4] Testing cash boxes...")
    try:
        response = requests.get(f"{BASE_URL}/api/accounting/cash-boxes", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Cash boxes: {len(data['data'])} found")
    except Exception as e:
        print(f"✗ Cash boxes failed: {e}")
    
    # Test 5: Vouchers
    print("\n[5] Testing vouchers...")
    try:
        response = requests.get(f"{BASE_URL}/api/accounting/vouchers", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Vouchers: {len(data['data'])} found")
    except Exception as e:
        print(f"✗ Vouchers failed: {e}")
    
    # Test 6: Profit/Loss
    print("\n[6] Testing profit/loss...")
    try:
        response = requests.get(f"{BASE_URL}/api/accounting/profit-loss", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Profit/Loss: Period {data['data']['period']}, Net Profit: ${data['data']['net_profit']}")
    except Exception as e:
        print(f"✗ Profit/Loss failed: {e}")
    
    # Test 7: Dashboard
    print("\n[7] Testing dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers)
        response.raise_for_status()
        print(f"✓ Dashboard accessible")
    except Exception as e:
        print(f"✗ Dashboard failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_endpoints()
