#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test products API to verify it's using the correct table
"""

import requests
import json

# Test without authentication first (to see the error)
url = "http://localhost:5002/api/products"

print("\n🧪 Testing Products API...")
print("=" * 50)

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)

# Also test the stats endpoint
stats_url = "http://localhost:5002/api/products/stats"
print("\n🧪 Testing Products Stats API...")
print("=" * 50)

try:
    response = requests.get(stats_url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
