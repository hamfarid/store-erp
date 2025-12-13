#!/usr/bin/env python
"""Comprehensive API Endpoint Tester for Store Project"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5506"

# Test results
results = {"passed": [], "failed": [], "skipped": []}


def test_endpoint(method, path, data=None, auth_token=None, expected_status=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None, f"Unknown method: {method}"

        if expected_status and response.status_code != expected_status:
            return (
                response.status_code,
                f"Expected {expected_status}, got {response.status_code}",
            )

        return response.status_code, (
            response.text[:200] if response.text else "No content"
        )
    except Exception as e:
        return None, str(e)


def login():
    """Get auth token"""
    url = f"{BASE_URL}/api/auth/login"
    try:
        response = requests.post(
            url, json={"username": "admin", "password": "admin123"}, timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("access_token")
    except Exception as e:
        print(f"    Login error: {e}")
    return None


def run_tests():
    """Run all endpoint tests"""
    print("=" * 60)
    print("STORE PROJECT - COMPREHENSIVE API ENDPOINT TESTING")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Health Check
    print("\n[1] HEALTH CHECK")
    status, resp = test_endpoint("GET", "/api/health")
    print(f"    /api/health: {status}")

    # 2. Authentication
    print("\n[2] AUTHENTICATION")
    token = login()
    if token:
        print(f"    Login: SUCCESS (token received)")
        results["passed"].append("/api/auth/login")
    else:
        print(f"    Login: FAILED")
        results["failed"].append("/api/auth/login")
        return results  # Can't continue without auth

    # 3. Products
    print("\n[3] PRODUCTS MODULE")
    endpoints = [
        ("GET", "/api/products"),
        ("GET", "/api/products/1"),
        ("GET", "/api/products/search?q=test"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 4. Inventory
    print("\n[4] INVENTORY MODULE")
    endpoints = [
        ("GET", "/api/inventory"),
        ("GET", "/api/inventory/stock"),
        ("GET", "/api/inventory/movements"),
        ("GET", "/api/inventory/alerts"),
        ("GET", "/api/warehouses"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 5. Invoices
    print("\n[5] INVOICES MODULE")
    endpoints = [
        ("GET", "/api/invoices"),
        ("GET", "/api/invoices/1"),
        ("GET", "/api/invoices/sales"),
        ("GET", "/api/invoices/purchases"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 6. Customers
    print("\n[6] CUSTOMERS MODULE")
    endpoints = [
        ("GET", "/api/customers"),
        ("GET", "/api/customers/1"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 7. Suppliers
    print("\n[7] SUPPLIERS MODULE")
    endpoints = [
        ("GET", "/api/suppliers"),
        ("GET", "/api/suppliers/1"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 8. Categories
    print("\n[8] CATEGORIES MODULE")
    endpoints = [
        ("GET", "/api/categories"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 9. Reports
    print("\n[9] REPORTS MODULE")
    endpoints = [
        ("GET", "/api/reports/sales"),
        ("GET", "/api/reports/inventory"),
        ("GET", "/api/reports/profit-loss"),
        ("GET", "/api/dashboard"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 10. Security
    print("\n[10] SECURITY MODULE")
    endpoints = [
        ("GET", "/api/audit/logs"),
        ("GET", "/api/users"),
        ("GET", "/api/users/me"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # 11. System
    print("\n[11] SYSTEM MODULE")
    endpoints = [
        ("GET", "/api/system/status"),
        ("GET", "/api/settings"),
    ]
    for method, path in endpoints:
        status, resp = test_endpoint(method, path, auth_token=token)
        status_str = f"{status}" if status else "ERROR"
        print(f"    {method} {path}: {status_str}")
        if status and status < 500:
            results["passed"].append(path)
        else:
            results["failed"].append(path)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⏭️ Skipped: {len(results['skipped'])}")

    if results["failed"]:
        print("\nFailed endpoints:")
        for ep in results["failed"]:
            print(f"  - {ep}")

    return results


if __name__ == "__main__":
    run_tests()
