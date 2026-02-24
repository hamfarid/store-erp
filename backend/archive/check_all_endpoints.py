#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل لجميع Endpoints في النظام
Complete Endpoints Checker
"""

import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

def check_frontend_api_calls():
    """فحص جميع استدعاءات API في Frontend"""
    print("\n" + "="*80)
    print("📱 Frontend API Calls")
    print("="*80)
    
    frontend_apis = {
        "Authentication": [
            "/api/auth/login",
            "/api/auth/logout",
            "/api/auth/refresh",
            "/api/auth/status",
            "/api/auth/register"
        ],
        "Users": [
            "/api/users",
            "/api/users/{id}"
        ],
        "Products": [
            "/api/products",
            "/api/products/{id}",
            "/api/products/search",
            "/api/products-advanced"
        ],
        "Inventory": [
            "/api/inventory",
            "/api/inventory/{id}",
            "/api/inventory/movements",
            "/api/inventory/adjust"
        ],
        "Customers": [
            "/api/customers",
            "/api/customers/{id}"
        ],
        "Suppliers": [
            "/api/suppliers",
            "/api/suppliers/{id}"
        ],
        "Invoices": [
            "/api/invoices",
            "/api/invoices/{id}",
            "/api/invoices/sales",
            "/api/invoices/purchases"
        ],
        "Warehouses": [
            "/api/warehouses",
            "/api/warehouses/{id}"
        ],
        "Categories": [
            "/api/categories",
            "/api/categories/{id}"
        ],
        "Dashboard": [
            "/api/dashboard/data",
            "/api/dashboard/stats",
            "/api/dashboard/statistics",
            "/api/dashboard/alerts"
        ],
        "Reports": [
            "/api/reports/inventory",
            "/api/reports/sales",
            "/api/reports/purchases",
            "/api/reports/profit-loss",
            "/api/reports/custom"
        ],
        "Accounting": [
            "/api/accounting/accounts",
            "/api/accounting/entries",
            "/api/accounting/balance",
            "/api/accounting/trial-balance"
        ],
        "Settings": [
            "/api/settings/company",
            "/api/settings/system",
            "/api/settings/permissions"
        ],
        "Integration": [
            "/api/integration/inventory-accounting/journal-entry",
            "/api/integration/inventory-accounting/reconciliation"
        ],
        "RAG": [
            "/api/rag/query"
        ]
    }
    
    total = 0
    for category, endpoints in frontend_apis.items():
        print(f"\n{category}:")
        for endpoint in endpoints:
            print(f"  ✅ {endpoint}")
            total += 1
    
    print(f"\n📊 Total Frontend API Calls: {total}")
    return frontend_apis


def check_backend_routes():
    """فحص جميع Routes في Backend"""
    print("\n" + "="*80)
    print("🔧 Backend Routes")
    print("="*80)
    
    routes_dir = Path(__file__).parent / 'backend' / 'src' / 'routes'
    
    if not routes_dir.exists():
        print("❌ Routes directory not found!")
        return {}
    
    route_files = list(routes_dir.glob('*.py'))
    route_files = [f for f in route_files if f.name != '__init__.py']
    
    print(f"\n📁 Found {len(route_files)} route files:")
    
    backend_routes = {}
    for route_file in sorted(route_files):
        route_name = route_file.stem
        print(f"  ✅ {route_name}.py")
        backend_routes[route_name] = str(route_file)
    
    return backend_routes


def check_registered_blueprints():
    """فحص Blueprints المسجلة في app.py"""
    print("\n" + "="*80)
    print("📦 Registered Blueprints in app.py")
    print("="*80)
    
    app_file = Path(__file__).parent / 'backend' / 'app.py'
    
    if not app_file.exists():
        print("❌ app.py not found!")
        return []
    
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن blueprints_to_register
    import re
    pattern = r"\('routes\.(\w+)',\s*'(\w+)'\)"
    matches = re.findall(pattern, content)
    
    print(f"\n📋 Found {len(matches)} registered blueprints:")
    
    registered = []
    for module, blueprint in matches:
        print(f"  ✅ routes.{module} → {blueprint}")
        registered.append((module, blueprint))
    
    return registered


def compare_frontend_backend():
    """مقارنة Frontend APIs مع Backend Routes"""
    print("\n" + "="*80)
    print("🔍 Comparison: Frontend vs Backend")
    print("="*80)
    
    # Frontend APIs
    frontend_apis = check_frontend_api_calls()
    
    # Backend Routes
    backend_routes = check_backend_routes()
    
    # Registered Blueprints
    registered = check_registered_blueprints()
    
    # تحليل
    print("\n" + "="*80)
    print("📊 Analysis")
    print("="*80)
    
    # حساب المجاميع
    total_frontend = sum(len(endpoints) for endpoints in frontend_apis.values())
    total_backend = len(backend_routes)
    total_registered = len(registered)
    
    print(f"\n📱 Frontend API Calls: {total_frontend}")
    print(f"🔧 Backend Route Files: {total_backend}")
    print(f"📦 Registered Blueprints: {total_registered}")
    
    # فحص الملفات المفقودة
    print("\n⚠️ Missing Route Files:")
    required_routes = {
        'auth_unified', 'users_unified', 'products_unified', 'partners_unified',
        'invoices_unified', 'customers', 'suppliers', 'inventory', 'warehouses',
        'categories', 'dashboard', 'reports', 'accounting', 'settings',
        'integration_apis', 'rag'
    }
    
    existing_routes = set(backend_routes.keys())
    missing_routes = required_routes - existing_routes
    
    if missing_routes:
        for route in sorted(missing_routes):
            print(f"  ❌ {route}.py")
    else:
        print("  ✅ All required route files exist!")
    
    # فحص Blueprints غير المسجلة
    print("\n⚠️ Unregistered Blueprints:")
    registered_modules = {module for module, _ in registered}
    unregistered = existing_routes - registered_modules
    
    if unregistered:
        for route in sorted(unregistered):
            print(f"  ⚠️ {route}.py (exists but not registered)")
    else:
        print("  ✅ All route files are registered!")
    
    return {
        'frontend_apis': frontend_apis,
        'backend_routes': backend_routes,
        'registered': registered,
        'missing_routes': list(missing_routes),
        'unregistered': list(unregistered)
    }


def generate_report(results):
    """إنشاء تقرير JSON"""
    report_file = Path(__file__).parent / 'endpoints_check_report.json'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Report saved to: {report_file}")


if __name__ == '__main__':
    print("🚀 Starting Complete Endpoints Check...")
    print("="*80)
    
    results = compare_frontend_backend()
    generate_report(results)
    
    print("\n" + "="*80)
    print("✅ Check Complete!")
    print("="*80)

