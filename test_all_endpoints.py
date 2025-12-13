"""
Comprehensive endpoint testing for Store Management System
Tests: Products, Inventory, Customers, Suppliers, Invoices, Accounting, Reports
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5002"
TOKEN = None

def print_header(text):
    """Print formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_test(name, passed, details=""):
    """Print test result"""
    symbol = "✓ PASS" if passed else "✗ FAIL"
    print(f"{symbol:10} | {name}")
    if details:
        print(f"           | {details}")

def login():
    """Login and get JWT token"""
    global TOKEN
    print_header("AUTHENTICATION")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'access_token' in data['data']:
                TOKEN = data['data']['access_token']
                print_test("Login", True, f"Token: {TOKEN[:30]}...")
                return True
            else:
                print_test("Login", False, f"No token in response: {data}")
                return False
        else:
            print_test("Login", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Login", False, f"Error: {str(e)}")
        return False

def get_headers():
    """Get authorization headers"""
    return {"Authorization": f"Bearer {TOKEN}"}

# ============================================================================
# TASK 10: PRODUCTS & INVENTORY TESTING
# ============================================================================

def test_products_endpoints():
    """Test products_unified_bp endpoints"""
    print_header("TASK 10: PRODUCTS & INVENTORY")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Get all products
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', [])) if 'data' in data else 0
            print_test("GET /api/products", True, f"Found {count} products")
        else:
            print_test("GET /api/products", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products", False, f"Error: {str(e)}")
    
    # Test 2: Get product stats
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products/stats",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            stats = data.get('data', {})
            print_test("GET /api/products/stats", True, 
                      f"Total: {stats.get('total_products', 0)}, "
                      f"Low stock: {stats.get('low_stock', 0)}")
        else:
            print_test("GET /api/products/stats", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products/stats", False, f"Error: {str(e)}")
    
    # Test 3: Get low stock products
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products/low-stock",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/products/low-stock", True, f"Found {count} items")
        else:
            print_test("GET /api/products/low-stock", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products/low-stock", False, f"Error: {str(e)}")
    
    # Test 4: Get out of stock products
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products/out-of-stock",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/products/out-of-stock", True, f"Found {count} items")
        else:
            print_test("GET /api/products/out-of-stock", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products/out-of-stock", False, f"Error: {str(e)}")
    
    # Test 5: Get categories
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products/categories",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/products/categories", True, f"Found {count} categories")
        else:
            print_test("GET /api/products/categories", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products/categories", False, f"Error: {str(e)}")
    
    # Test 6: Search products
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/products/search?q=test",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/products/search", True, f"Found {count} results")
        else:
            print_test("GET /api/products/search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/products/search", False, f"Error: {str(e)}")
    
    # Test 7: Categories API (separate blueprint)
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/categories",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', [])) if 'data' in data else len(data.get('categories', []))
            print_test("GET /api/categories", True, f"Found {count} categories")
        else:
            print_test("GET /api/categories", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/categories", False, f"Error: {str(e)}")
    
    print(f"\n📊 Task 10 Results: {tests_passed}/{tests_total} tests passed ({int(tests_passed/tests_total*100)}%)")
    return tests_passed, tests_total

# ============================================================================
# TASK 11: CUSTOMERS & SUPPLIERS TESTING
# ============================================================================

def test_partners_endpoints():
    """Test partners_unified_bp endpoints (customers & suppliers)"""
    print_header("TASK 11: CUSTOMERS & SUPPLIERS")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Get all customers
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/customers",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/customers", True, f"Found {count} customers")
        else:
            print_test("GET /api/customers", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/customers", False, f"Error: {str(e)}")
    
    # Test 2: Get all suppliers
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/suppliers",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/suppliers", True, f"Found {count} suppliers")
        else:
            print_test("GET /api/suppliers", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/suppliers", False, f"Error: {str(e)}")
    
    # Test 3: Get customer stats
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/customers/stats",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            stats = data.get('data', {})
            print_test("GET /api/customers/stats", True, 
                      f"Total: {stats.get('total_customers', 0)}")
        else:
            print_test("GET /api/customers/stats", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/customers/stats", False, f"Error: {str(e)}")
    
    # Test 4: Search customers
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/customers/search?q=test",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/customers/search", True, f"Found {count} results")
        else:
            print_test("GET /api/customers/search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/customers/search", False, f"Error: {str(e)}")
    
    print(f"\n📊 Task 11 Results: {tests_passed}/{tests_total} tests passed ({int(tests_passed/tests_total*100)}%)")
    return tests_passed, tests_total

# ============================================================================
# TASK 12: INVOICES & ACCOUNTING TESTING
# ============================================================================

def test_accounting_endpoints():
    """Test accounting_simple_bp endpoints"""
    print_header("TASK 12: INVOICES & ACCOUNTING")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Test route
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/accounting/test",
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            print_test("GET /api/accounting/test", True, "Blueprint active")
        else:
            print_test("GET /api/accounting/test", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/accounting/test", False, f"Error: {str(e)}")
    
    # Test 2: Get currencies
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/accounting/currencies",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/accounting/currencies", True, f"Found {count} currencies")
        else:
            print_test("GET /api/accounting/currencies", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/accounting/currencies", False, f"Error: {str(e)}")
    
    # Test 3: Get cash boxes
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/accounting/cash-boxes",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/accounting/cash-boxes", True, f"Found {count} treasuries")
        else:
            print_test("GET /api/accounting/cash-boxes", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/accounting/cash-boxes", False, f"Error: {str(e)}")
    
    # Test 4: Get vouchers
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/accounting/vouchers",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/accounting/vouchers", True, f"Found {count} vouchers")
        else:
            print_test("GET /api/accounting/vouchers", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/accounting/vouchers", False, f"Error: {str(e)}")
    
    # Test 5: Get profit/loss report
    tests_total += 1
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        response = requests.get(
            f"{BASE_URL}/api/accounting/profit-loss"
            f"?start_date={start_date.strftime('%Y-%m-%d')}"
            f"&end_date={end_date.strftime('%Y-%m-%d')}",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            report = data.get('data', {})
            print_test("GET /api/accounting/profit-loss", True, 
                      f"Revenue: {report.get('revenue', {}).get('total', 0)}, "
                      f"Expenses: {report.get('expenses', {}).get('total', 0)}")
        else:
            print_test("GET /api/accounting/profit-loss", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/accounting/profit-loss", False, f"Error: {str(e)}")
    
    # Test 6: Get purchase invoices
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/invoices?invoice_type=purchase",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/invoices?type=purchase", True, f"Found {count} purchase invoices")
        else:
            print_test("GET /api/invoices?type=purchase", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/invoices?type=purchase", False, f"Error: {str(e)}")
    
    # Test 7: Get sales invoices
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/invoices?invoice_type=sales",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/invoices?type=sales", True, f"Found {count} sales invoices")
        else:
            print_test("GET /api/invoices?type=sales", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/invoices?type=sales", False, f"Error: {str(e)}")
    
    print(f"\n📊 Task 12 Results: {tests_passed}/{tests_total} tests passed ({int(tests_passed/tests_total*100)}%)")
    return tests_passed, tests_total

# ============================================================================
# TASK 13: REPORTS & ADMIN TESTING
# ============================================================================

def test_reports_endpoints():
    """Test reports and admin endpoints"""
    print_header("TASK 13: REPORTS & ADMIN")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Get reports list
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/reports",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', [])) if isinstance(data.get('data'), list) else 0
            print_test("GET /api/reports", True, f"Reports available")
        else:
            print_test("GET /api/reports", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/reports", False, f"Error: {str(e)}")
    
    # Test 2: Get dashboard stats
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/dashboard/stats",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            print_test("GET /api/dashboard/stats", True, "Dashboard data retrieved")
        else:
            print_test("GET /api/dashboard/stats", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/dashboard/stats", False, f"Error: {str(e)}")
    
    # Test 3: Get users (admin)
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/users",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            count = len(data.get('data', []))
            print_test("GET /api/users", True, f"Found {count} users")
        else:
            print_test("GET /api/users", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/users", False, f"Error: {str(e)}")
    
    # Test 4: Get current user profile
    tests_total += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=get_headers(),
            timeout=10
        )
        passed = response.status_code == 200
        if passed:
            tests_passed += 1
            data = response.json()
            user = data.get('data', {})
            print_test("GET /api/users/me", True, f"User: {user.get('username', 'N/A')}")
        else:
            print_test("GET /api/users/me", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /api/users/me", False, f"Error: {str(e)}")
    
    print(f"\n📊 Task 13 Results: {tests_passed}/{tests_total} tests passed ({int(tests_passed/tests_total*100)}%)")
    return tests_passed, tests_total

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("  COMPREHENSIVE ENDPOINT TESTING - TASKS 10-13")
    print("  Store Management System v1.5")
    print("="*80)
    
    # Login first
    if not login():
        print("\n❌ Authentication failed. Cannot proceed with tests.")
        return
    
    # Track overall results
    total_passed = 0
    total_tests = 0
    
    # Task 10: Products & Inventory
    passed, total = test_products_endpoints()
    total_passed += passed
    total_tests += total
    
    # Task 11: Customers & Suppliers
    passed, total = test_partners_endpoints()
    total_passed += passed
    total_tests += total
    
    # Task 12: Invoices & Accounting
    passed, total = test_accounting_endpoints()
    total_passed += passed
    total_tests += total
    
    # Task 13: Reports & Admin
    passed, total = test_reports_endpoints()
    total_passed += passed
    total_tests += total
    
    # Final Summary
    print_header("FINAL SUMMARY")
    percentage = int(total_passed/total_tests*100) if total_tests > 0 else 0
    print(f"✅ Total Tests Passed: {total_passed}/{total_tests} ({percentage}%)")
    print(f"\n{'='*80}\n")
    
    if percentage >= 80:
        print("🎉 EXCELLENT! System is ready for production.")
    elif percentage >= 60:
        print("✓ GOOD! Most endpoints working correctly.")
    else:
        print("⚠ WARNING! Multiple endpoints need attention.")

if __name__ == "__main__":
    main()
