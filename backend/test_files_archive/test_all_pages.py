"""
Test script to verify all frontend pages are accessible and not blank
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5502"

# Test credentials
USERNAME = "admin"
PASSWORD = "admin123"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")


def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text):
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")


# Test login and get token
def test_login():
    print_header("Testing Login")

    try:
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"Login successful: {data.get('message')}")
                print_info(f"User: {data.get('user', {}).get('username')}")
                print_info(f"Role: {data.get('user', {}).get('role')}")
                return data.get("token")
            else:
                print_error(f"Login failed: {data.get('message')}")
                return None
        else:
            print_error(f"Login failed with status {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None


# Test backend API endpoints
def test_backend_endpoints(token):
    print_header("Testing Backend API Endpoints")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" if token else "",
    }

    endpoints = [
        ("GET", "/api/health", "Health Check"),
        ("GET", "/api/dashboard/stats", "Dashboard Statistics"),
        ("GET", "/api/products", "Products List"),
        ("GET", "/api/customers", "Customers List"),
        ("GET", "/api/suppliers", "Suppliers List"),
        ("GET", "/api/inventory", "Inventory List"),
        ("GET", "/api/warehouses", "Warehouses List"),
        ("GET", "/api/categories", "Categories List"),
        ("GET", "/api/invoices", "Invoices List"),
        ("GET", "/api/user/check-session", "Session Check"),
    ]

    results = []

    for method, endpoint, name in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.request(method, url, headers=headers, timeout=10)

            if response.status_code == 200:
                print_success(f"{name}: {endpoint} - Status {response.status_code}")
                results.append((name, True, response.status_code))
            elif response.status_code == 404:
                print_warning(f"{name}: {endpoint} - Not Found (404)")
                results.append((name, False, 404))
            elif response.status_code == 401:
                print_warning(f"{name}: {endpoint} - Unauthorized (401)")
                results.append((name, False, 401))
            else:
                print_error(f"{name}: {endpoint} - Status {response.status_code}")
                results.append((name, False, response.status_code))

        except requests.exceptions.Timeout:
            print_error(f"{name}: {endpoint} - Timeout")
            results.append((name, False, "Timeout"))
        except Exception as e:
            print_error(f"{name}: {endpoint} - Error: {e}")
            results.append((name, False, str(e)))

    return results


# Test frontend routes (check if they return HTML)
def test_frontend_routes():
    print_header("Testing Frontend Routes")

    routes = [
        "/login",
        "/dashboard",
        "/products",
        "/customers",
        "/suppliers",
        "/inventory",
        "/warehouses",
        "/categories",
        "/invoices",
        "/reports",
        "/settings",
        "/users",
        "/company",
        "/notifications",
    ]

    results = []

    for route in routes:
        try:
            url = f"{FRONTEND_URL}{route}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                # Check if response contains HTML
                if "html" in response.text.lower() or "root" in response.text:
                    print_success(f"Route {route} - Accessible (200)")
                    results.append((route, True, 200))
                else:
                    print_warning(f"Route {route} - Returns non-HTML content")
                    results.append((route, False, "Non-HTML"))
            else:
                print_error(f"Route {route} - Status {response.status_code}")
                results.append((route, False, response.status_code))

        except requests.exceptions.ConnectionError:
            print_error(f"Route {route} - Frontend not running")
            results.append((route, False, "Connection Error"))
        except Exception as e:
            print_error(f"Route {route} - Error: {e}")
            results.append((route, False, str(e)))

    return results


# Generate summary report
def generate_report(backend_results, frontend_results):
    print_header("Test Summary Report")

    # Backend summary
    backend_passed = sum(1 for _, success, _ in backend_results if success)
    backend_total = len(backend_results)
    backend_percentage = (
        (backend_passed / backend_total * 100) if backend_total > 0 else 0
    )

    print(f"\n{BLUE}Backend API Endpoints:{RESET}")
    print(f"  Total: {backend_total}")
    print(f"  Passed: {GREEN}{backend_passed}{RESET}")
    print(f"  Failed: {RED}{backend_total - backend_passed}{RESET}")
    print(
        f"  Success Rate: {GREEN if backend_percentage >= 80 else RED}{backend_percentage:.1f}%{RESET}"
    )

    # Frontend summary
    frontend_passed = sum(1 for _, success, _ in frontend_results if success)
    frontend_total = len(frontend_results)
    frontend_percentage = (
        (frontend_passed / frontend_total * 100) if frontend_total > 0 else 0
    )

    print(f"\n{BLUE}Frontend Routes:{RESET}")
    print(f"  Total: {frontend_total}")
    print(f"  Passed: {GREEN}{frontend_passed}{RESET}")
    print(f"  Failed: {RED}{frontend_total - frontend_passed}{RESET}")
    print(
        f"  Success Rate: {GREEN if frontend_percentage >= 80 else RED}{frontend_percentage:.1f}%{RESET}"
    )

    # Overall summary
    total_tests = backend_total + frontend_total
    total_passed = backend_passed + frontend_passed
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"\n{BLUE}Overall:{RESET}")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {GREEN}{total_passed}{RESET}")
    print(f"  Failed: {RED}{total_tests - total_passed}{RESET}")
    print(
        f"  Success Rate: {GREEN if overall_percentage >= 80 else RED}{overall_percentage:.1f}%{RESET}"
    )

    # Failed tests details
    if backend_total - backend_passed > 0 or frontend_total - frontend_passed > 0:
        print(f"\n{RED}Failed Tests:{RESET}")

        for name, success, status in backend_results:
            if not success:
                print(f"  {RED}❌ Backend: {name} - {status}{RESET}")

        for route, success, status in frontend_results:
            if not success:
                print(f"  {RED}❌ Frontend: {route} - {status}{RESET}")

    print(f"\n{BLUE}{'='*80}{RESET}\n")

    return {
        "timestamp": datetime.now().isoformat(),
        "backend": {
            "total": backend_total,
            "passed": backend_passed,
            "failed": backend_total - backend_passed,
            "percentage": backend_percentage,
        },
        "frontend": {
            "total": frontend_total,
            "passed": frontend_passed,
            "failed": frontend_total - frontend_passed,
            "percentage": frontend_percentage,
        },
        "overall": {
            "total": total_tests,
            "passed": total_passed,
            "failed": total_tests - total_passed,
            "percentage": overall_percentage,
        },
    }


def main():
    print_header("Complete Inventory System - Page Validation Test")
    print_info(f"Backend URL: {BASE_URL}")
    print_info(f"Frontend URL: {FRONTEND_URL}")
    print_info(f"Test User: {USERNAME}")

    # Test login
    token = test_login()

    # Test backend endpoints
    backend_results = test_backend_endpoints(token)

    # Test frontend routes
    frontend_results = test_frontend_routes()

    # Generate report
    report = generate_report(backend_results, frontend_results)

    # Save report to file
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_success("Test report saved to: test_results.json")


if __name__ == "__main__":
    main()
