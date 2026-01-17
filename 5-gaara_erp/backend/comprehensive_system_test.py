#!/usr/bin/env python3
"""
Comprehensive System Testing Script
Tests all major components of the Arabic Inventory Management System
"""

import sys
import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


class SystemTester:
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "errors": []},
        }
        self.auth_token = None

    def log_test(self, test_name, status, message="", details=None):
        """Log test result"""
        test_result = {
            "name": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        if details:
            test_result["details"] = details

        self.test_results["tests"].append(test_result)
        self.test_results["summary"]["total"] += 1

        if status == "PASS":
            self.test_results["summary"]["passed"] += 1
            print(f"✅ {test_name}: {message}")
        else:
            self.test_results["summary"]["failed"] += 1
            self.test_results["summary"]["errors"].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: {message}")

    def test_flask_app_creation(self):
        """Test Flask application creation"""
        try:
            from app import create_app

            app = create_app()
            self.log_test(
                "Flask App Creation", "PASS", "Flask app created successfully"
            )
            return app
        except Exception as e:
            self.log_test(
                "Flask App Creation", "FAIL", f"Failed to create Flask app: {e}"
            )
            return None

    def test_database_initialization(self, app):
        """Test database initialization"""
        try:
            with app.app_context():
                from database import db

                # Test database connection
                from sqlalchemy import text

                db.session.execute(text("SELECT 1"))
                self.log_test(
                    "Database Connection", "PASS", "Database connection successful"
                )

                # Test table creation
                db.create_all()
                tables = list(db.metadata.tables.keys())
                self.log_test(
                    "Database Tables",
                    "PASS",
                    f"Created {len(tables)} tables",
                    {"tables": tables},
                )

                return True
        except Exception as e:
            self.log_test(
                "Database Initialization",
                "FAIL",
                f"Database initialization failed: {e}",
            )
            return False

    def test_model_imports(self):
        """Test model imports"""
        try:
            from models import User, Role, Customer, Product, Category, Warehouse

            self.log_test(
                "Basic Model Imports", "PASS", "Basic models imported successfully"
            )

            from models import UnifiedInvoice, UnifiedInvoiceItem, InvoicePayment

            self.log_test(
                "Advanced Model Imports",
                "PASS",
                "Advanced models imported successfully",
            )

            from models import SalesInvoice, SalesInvoiceItem, CustomerPayment

            self.log_test(
                "Sales Model Imports", "PASS", "Sales models imported successfully"
            )

            return True
        except Exception as e:
            self.log_test("Model Imports", "FAIL", f"Model import failed: {e}")
            return False

    def test_model_instantiation(self, app):
        """Test model instantiation"""
        try:
            with app.app_context():
                from models import User, Customer, Product, Category, Warehouse

                # Test User model
                user = User(
                    username="test_user",
                    email="test@example.com",
                    full_name="Test User",
                    role_id=1,
                )
                self.log_test(
                    "User Model Instantiation",
                    "PASS",
                    "User model created successfully",
                )

                # Test Customer model
                customer = Customer(name="Test Customer", email="customer@example.com")
                self.log_test(
                    "Customer Model Instantiation",
                    "PASS",
                    "Customer model created successfully",
                )

                # Test Product model
                product = Product(name="Test Product", selling_price=100.0)
                self.log_test(
                    "Product Model Instantiation",
                    "PASS",
                    "Product model created successfully",
                )

                # Test Category model
                category = Category(name="Test Category")
                self.log_test(
                    "Category Model Instantiation",
                    "PASS",
                    "Category model created successfully",
                )

                # Test Warehouse model
                warehouse = Warehouse(name="Test Warehouse")
                self.log_test(
                    "Warehouse Model Instantiation",
                    "PASS",
                    "Warehouse model created successfully",
                )

                return True
        except Exception as e:
            self.log_test(
                "Model Instantiation", "FAIL", f"Model instantiation failed: {e}"
            )
            return False

    def start_flask_server(self, app):
        """Start Flask server for API testing"""
        try:
            import threading
            import time

            def run_server():
                app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)

            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()

            # Wait for server to start
            time.sleep(3)

            # Test server is running
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.log_test(
                    "Flask Server Start", "PASS", "Flask server started successfully"
                )
                return True
            else:
                self.log_test(
                    "Flask Server Start",
                    "FAIL",
                    f"Server responded with status {response.status_code}",
                )
                return False

        except Exception as e:
            self.log_test(
                "Flask Server Start", "FAIL", f"Failed to start Flask server: {e}"
            )
            return False

    def test_api_endpoints(self):
        """Test API endpoints"""
        endpoints_to_test = [
            ("/api/health", "Health Check"),
            ("/api/info", "System Info"),
            ("/api/dashboard/stats", "Dashboard Stats"),
            ("/api/products", "Products API"),
            ("/api/customers", "Customers API"),
            ("/api/suppliers", "Suppliers API"),
        ]

        for endpoint, name in endpoints_to_test:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code in [
                    200,
                    401,
                ]:  # 401 is expected for protected endpoints
                    self.log_test(
                        f"API Endpoint {name}",
                        "PASS",
                        f"Endpoint {endpoint} responded with status {response.status_code}",
                    )
                else:
                    self.log_test(
                        f"API Endpoint {name}",
                        "FAIL",
                        f"Endpoint {endpoint} responded with status {response.status_code}",
                    )
            except Exception as e:
                self.log_test(
                    f"API Endpoint {name}",
                    "FAIL",
                    f"Failed to test endpoint {endpoint}: {e}",
                )

    def test_frontend_files(self):
        """Test frontend files existence"""
        frontend_dir = current_dir.parent / "frontend"

        critical_files = [
            "package.json",
            "src/App.jsx",
            "src/main.jsx",
            "index.html",
            "vite.config.js",
        ]

        for file_path in critical_files:
            full_path = frontend_dir / file_path
            if full_path.exists():
                self.log_test(
                    f"Frontend File {file_path}", "PASS", f"File exists: {file_path}"
                )
            else:
                self.log_test(
                    f"Frontend File {file_path}", "FAIL", f"File missing: {file_path}"
                )

    def test_authentication_system(self, app):
        """Test authentication system"""
        try:
            with app.app_context():
                from models import User, Role
                from database import db

                # Create a test role
                test_role = Role(name="test_role", description="Test Role")
                db.session.add(test_role)
                db.session.commit()

                # Create a test user
                test_user = User(
                    username="test_auth_user",
                    email="auth@example.com",
                    full_name="Auth Test User",
                    role_id=test_role.id,
                )
                test_user.set_password("test123")
                db.session.add(test_user)
                db.session.commit()

                # Test password verification
                if test_user.check_password("test123"):
                    self.log_test(
                        "Authentication System",
                        "PASS",
                        "Password verification works correctly",
                    )
                else:
                    self.log_test(
                        "Authentication System", "FAIL", "Password verification failed"
                    )

                # Clean up
                db.session.delete(test_user)
                db.session.delete(test_role)
                db.session.commit()

                return True
        except Exception as e:
            self.log_test(
                "Authentication System", "FAIL", f"Authentication test failed: {e}"
            )
            return False

    def test_database_operations(self, app):
        """Test basic database operations"""
        try:
            with app.app_context():
                from models import Customer
                from database import db

                # Test CREATE
                test_customer = Customer(
                    name="Test DB Customer",
                    email="dbtest@example.com",
                    phone="123456789",
                )
                db.session.add(test_customer)
                db.session.commit()

                # Test READ
                found_customer = Customer.query.filter_by(
                    email="dbtest@example.com"
                ).first()
                if found_customer:
                    self.log_test(
                        "Database CREATE/READ",
                        "PASS",
                        "Customer created and retrieved successfully",
                    )
                else:
                    self.log_test(
                        "Database CREATE/READ",
                        "FAIL",
                        "Failed to retrieve created customer",
                    )
                    return False

                # Test UPDATE
                found_customer.name = "Updated Test Customer"
                db.session.commit()

                updated_customer = Customer.query.filter_by(
                    email="dbtest@example.com"
                ).first()
                if updated_customer.name == "Updated Test Customer":
                    self.log_test(
                        "Database UPDATE", "PASS", "Customer updated successfully"
                    )
                else:
                    self.log_test(
                        "Database UPDATE", "FAIL", "Failed to update customer"
                    )

                # Test DELETE
                db.session.delete(updated_customer)
                db.session.commit()

                deleted_customer = Customer.query.filter_by(
                    email="dbtest@example.com"
                ).first()
                if deleted_customer is None:
                    self.log_test(
                        "Database DELETE", "PASS", "Customer deleted successfully"
                    )
                else:
                    self.log_test(
                        "Database DELETE", "FAIL", "Failed to delete customer"
                    )

                return True
        except Exception as e:
            self.log_test(
                "Database Operations", "FAIL", f"Database operations test failed: {e}"
            )
            return False

    def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting Comprehensive System Testing...")
        print("=" * 60)

        # Test 1: Flask App Creation
        app = self.test_flask_app_creation()
        if not app:
            return self.generate_report()

        # Test 2: Database Initialization
        if not self.test_database_initialization(app):
            return self.generate_report()

        # Test 3: Model Imports
        if not self.test_model_imports():
            return self.generate_report()

        # Test 4: Model Instantiation
        self.test_model_instantiation(app)

        # Test 5: Authentication System
        self.test_authentication_system(app)

        # Test 6: Database Operations
        self.test_database_operations(app)

        # Test 7: Frontend Files
        self.test_frontend_files()

        # Test 8: Start Flask Server and Test APIs
        if self.start_flask_server(app):
            self.test_api_endpoints()

        return self.generate_report()

    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        summary = self.test_results["summary"]
        print(f"Total Tests: {summary['total']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")

        if summary["failed"] > 0:
            print("\n❌ FAILED TESTS:")
            for error in summary["errors"]:
                print(f"  - {error}")

        # Save detailed report
        report_file = (
            current_dir
            / f"system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Detailed report saved to: {report_file}")

        success_rate = (
            (summary["passed"] / summary["total"]) * 100 if summary["total"] > 0 else 0
        )
        print(f"🎯 Success Rate: {success_rate:.1f}%")

        if success_rate >= 90:
            print("🎉 System is in excellent condition!")
            return True
        elif success_rate >= 75:
            print("⚠️ System is in good condition with minor issues")
            return True
        else:
            print("🚨 System has significant issues that need attention")
            return False


def main():
    """Main function"""
    tester = SystemTester()
    success = tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
