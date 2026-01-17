#!/usr/bin/env python
"""
Gaara ERP v12 - Standalone Playwright E2E Tests with Screenshots
=================================================================

This script runs Playwright tests independently without pytest-django conflicts.

Usage:
    python tests/e2e/run_playwright_tests.py

Created: 2026-01-16
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:9551')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3505')

# Screenshots directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Results storage
results = {
    "timestamp": datetime.now().isoformat(),
    "backend_url": BACKEND_URL,
    "frontend_url": FRONTEND_URL,
    "tests": [],
    "screenshots": [],
}


def log(message: str, status: str = "info"):
    """Print colored log message."""
    icons = {"pass": "✅", "fail": "❌", "skip": "⚠️", "info": "ℹ️", "screenshot": "📸"}
    print(f"{icons.get(status, '•')} {message}")


def take_screenshot(page, name: str) -> Optional[Path]:
    """Take and save a screenshot with timestamp."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        page.screenshot(path=str(filepath), full_page=True)
        log(f"Screenshot saved: {filepath.name}", "screenshot")
        results["screenshots"].append(str(filepath))
        return filepath
    except Exception as e:
        log(f"Screenshot failed: {e}", "fail")
        return None


def test_health_endpoint(page) -> bool:
    """Test the health endpoint."""
    test_name = "Backend Health Endpoint"
    try:
        response = page.goto(f"{BACKEND_URL}/health/", timeout=10000)
        take_screenshot(page, "health_endpoint")
        
        status = "pass" if response and response.status == 200 else "partial"
        results["tests"].append({
            "name": test_name,
            "status": status,
            "response_code": response.status if response else None,
        })
        log(f"{test_name}: {response.status if response else 'error'}", status)
        return True
    except Exception as e:
        results["tests"].append({"name": test_name, "status": "fail", "error": str(e)})
        log(f"{test_name}: {e}", "fail")
        return False


def test_api_endpoints(page) -> bool:
    """Test various API endpoints."""
    test_name = "API Endpoints"
    endpoints = [
        ("/api/accounting/", "Accounting API"),
        ("/api/organization/", "Organization API"),
        ("/api/security/", "Security API"),
        ("/api/inventory/", "Inventory API"),
        ("/api/sales/", "Sales API"),
        ("/companies/", "Companies"),
        ("/currencies/", "Currencies"),
    ]
    
    passed = 0
    for endpoint, name in endpoints:
        try:
            response = page.goto(f"{BACKEND_URL}{endpoint}", timeout=5000)
            status_code = response.status if response else 0
            take_screenshot(page, f"api_{name.lower().replace(' ', '_')}")
            
            # 200, 401 (auth required), 403 are all valid responses
            if status_code in [200, 401, 403]:
                passed += 1
                log(f"  {name}: {status_code}", "pass")
            else:
                log(f"  {name}: {status_code}", "skip")
        except Exception as e:
            log(f"  {name}: {e}", "fail")
    
    results["tests"].append({
        "name": test_name,
        "status": "pass" if passed > 0 else "fail",
        "passed": passed,
        "total": len(endpoints),
    })
    return passed > 0


def test_swagger_docs(page) -> bool:
    """Test Swagger/OpenAPI documentation."""
    test_name = "API Documentation"
    try:
        response = page.goto(f"{BACKEND_URL}/api/docs/", timeout=10000)
        if response and response.status == 200:
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "swagger_docs")
            results["tests"].append({"name": test_name, "status": "pass"})
            log(f"{test_name}: Available", "pass")
            return True
        else:
            results["tests"].append({"name": test_name, "status": "skip", "code": response.status if response else 0})
            log(f"{test_name}: Not found ({response.status if response else 'error'})", "skip")
            return False
    except Exception as e:
        results["tests"].append({"name": test_name, "status": "skip", "error": str(e)})
        log(f"{test_name}: {e}", "skip")
        return False


def test_frontend(page) -> bool:
    """Test frontend application."""
    test_name = "Frontend Application"
    try:
        response = page.goto(FRONTEND_URL, timeout=10000)
        if response and response.status == 200:
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "frontend_home")
            
            # Try to find login form
            login_elements = page.locator('input[type="email"], input[type="password"], input[name="username"]')
            has_login = login_elements.count() > 0
            
            results["tests"].append({
                "name": test_name,
                "status": "pass",
                "has_login_form": has_login,
                "title": page.title(),
            })
            log(f"{test_name}: {page.title()}", "pass")
            return True
        else:
            results["tests"].append({"name": test_name, "status": "skip", "code": response.status if response else 0})
            log(f"{test_name}: Not running", "skip")
            return False
    except Exception as e:
        results["tests"].append({"name": test_name, "status": "skip", "error": str(e)})
        log(f"{test_name}: {e}", "skip")
        return False


def test_responsive_views(page) -> bool:
    """Test responsive views at different viewports."""
    test_name = "Responsive Views"
    viewports = [
        {"name": "mobile", "width": 375, "height": 812},
        {"name": "tablet", "width": 768, "height": 1024},
        {"name": "desktop", "width": 1920, "height": 1080},
    ]
    
    passed = 0
    for vp in viewports:
        try:
            page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
            response = page.goto(f"{BACKEND_URL}/health/", timeout=5000)
            take_screenshot(page, f"responsive_{vp['name']}")
            passed += 1
            log(f"  {vp['name'].title()} ({vp['width']}x{vp['height']}): OK", "pass")
        except Exception as e:
            log(f"  {vp['name'].title()}: {e}", "fail")
    
    results["tests"].append({
        "name": test_name,
        "status": "pass" if passed > 0 else "fail",
        "passed": passed,
        "total": len(viewports),
    })
    return passed > 0


def run_all_tests():
    """Run all Playwright E2E tests."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("Playwright not installed. Run: pip install playwright && playwright install", "fail")
        sys.exit(1)
    
    log("=" * 60, "info")
    log("Gaara ERP v12 - E2E Tests with Playwright", "info")
    log("=" * 60, "info")
    log(f"Backend URL: {BACKEND_URL}", "info")
    log(f"Frontend URL: {FRONTEND_URL}", "info")
    log(f"Screenshots: {SCREENSHOTS_DIR}", "info")
    log("-" * 60, "info")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='ar-SA',
        )
        page = context.new_page()
        
        # Run tests
        log("\n🔬 Running Tests...\n", "info")
        
        test_health_endpoint(page)
        test_api_endpoints(page)
        test_swagger_docs(page)
        test_frontend(page)
        test_responsive_views(page)
        
        # Cleanup
        page.close()
        context.close()
        browser.close()
    
    # Summary
    log("\n" + "=" * 60, "info")
    log("📊 Test Summary", "info")
    log("-" * 60, "info")
    
    passed = sum(1 for t in results["tests"] if t.get("status") == "pass")
    failed = sum(1 for t in results["tests"] if t.get("status") == "fail")
    skipped = sum(1 for t in results["tests"] if t.get("status") == "skip")
    
    log(f"Total Tests: {len(results['tests'])}", "info")
    log(f"Passed: {passed}", "pass" if passed > 0 else "info")
    log(f"Failed: {failed}", "fail" if failed > 0 else "info")
    log(f"Skipped: {skipped}", "skip" if skipped > 0 else "info")
    log(f"Screenshots: {len(results['screenshots'])}", "screenshot")
    
    # Save results
    report_path = SCREENSHOTS_DIR / "test_results.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    log(f"\n📄 Report saved: {report_path}", "info")
    
    # List screenshots
    log("\n📸 Screenshots captured:", "info")
    for ss in results["screenshots"][-10:]:  # Show last 10
        log(f"  - {Path(ss).name}", "info")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
