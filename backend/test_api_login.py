#!/usr/bin/env python
"""Test login API"""
import requests
import json

url = "http://localhost:5506/api/auth/login"
data = {"username": "admin", "password": "admin123"}

print(f"Testing login API at {url}")
print(f"Request body: {json.dumps(data)}")

try:
    response = requests.post(url, json=data)
    print(f"\nStatus code: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
