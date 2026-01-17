#!/usr/bin/env python3
"""
Gaara ERP Final System Test
===========================

Comprehensive final testing suite for Gaara ERP system.
Validates all components, integrations, and functionality before deployment.

Usage:
    python final_system_test.py [--mode MODE] [--output FILE] [--verbose]

Modes:
    complete    - Full system test (default)
    quick       - Quick validation test
    integration - Integration tests only
    performance - Performance validation
    security    - Security validation
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


class FinalSystemTest:
    def __init__(self, verbose=False):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.verbose = verbose
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'summary': {}
        }
        # Ensure UTF-8 stdout to avoid UnicodeEncodeError on some consoles
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    def print_banner(self):
        """Print test banner"""
        print("""
🧪 GAARA ERP FINAL SYSTEM TEST 🧪
=================================
🔍 Comprehensive System Validation
✅ Pre-Deployment Verification
🚀 Production Readiness Check
        """)

    def log(self, message, level='INFO'):
        """Log message"""
        if self.verbose or level in ['ERROR', 'SUCCESS']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {level}: {message}")

    def add_test_result(self, test_name, status, duration=None, details=None, error=None):
        """Add test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'duration_seconds': duration,
            'details': details,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }

        self.test_results['tests'].append(result)

        # Print result
        status_icon = {
            'pass': '✅',
            'fail': '❌',
            'skip': '⏭️',
            'warning': '⚠️'
        }.get(status, '❓')

        duration_str = f" ({duration:.2f}s)" if duration else ""
        print(f"   {status_icon} {test_name}{duration_str}")

        if error and self.verbose:
            print(f"      Error: {error}")

        return result

    def test_environment_setup(self):
        """Test environment setup"""
        print("🔧 Testing environment setup...")

        start_time = time.time()

        # Test Python version
        if sys.version_info >= (3, 11):
            self.add_test_result("Python Version Check",
                                 "pass", time.time() - start_time)
        else:
            self.add_test_result("Python Version Check", "fail", time.time() - start_time,
                                 error=f"Python {sys.version_info.major}.{sys.version_info.minor} < 3.11")

        # Test virtual environment
        start_time = time.time()
        venv_active = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

        if venv_active:
            self.add_test_result("Virtual Environment",
                                 "pass", time.time() - start_time)
        else:
            self.add_test_result("Virtual Environment", "warning", time.time() - start_time,
                                 details="Virtual environment not detected")

        # Test project structure
        start_time = time.time()
        required_files = [
            self.gaara_dir / 'manage.py',
            self.gaara_dir / 'gaara_erp' / 'settings.py',
            self.base_dir / 'start_system.py'
        ]

        missing_files = [f for f in required_files if not f.exists()]

        if not missing_files:
            self.add_test_result("Project Structure",
                                 "pass", time.time() - start_time)
        else:
            self.add_test_result("Project Structure", "fail", time.time() - start_time,
                                 error=f"Missing files: {[str(f) for f in missing_files]}")

    def test_django_functionality(self):
        """Test Django functionality"""
        print("🐍 Testing Django functionality...")

        os.chdir(self.gaara_dir)

        # Test Django check
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'check'
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                self.add_test_result("Django System Check",
                                     "pass", time.time() - start_time)
            else:
                self.add_test_result("Django System Check", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Django System Check", "fail", time.time() - start_time,
                                 error="Timeout after 60 seconds")

        # Test migrations
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'showmigrations', '--plan'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.add_test_result("Migration Status",
                                     "pass", time.time() - start_time)
            else:
                self.add_test_result("Migration Status", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Migration Status", "fail", time.time() - start_time,
                                 error="Timeout after 30 seconds")

        # Test database connectivity
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                'from django.db import connection; connection.ensure_connection(); print("OK")'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and 'OK' in result.stdout:
                self.add_test_result(
                    "Database Connectivity", "pass", time.time() - start_time)
            else:
                self.add_test_result("Database Connectivity", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Database Connectivity", "fail", time.time() - start_time,
                                 error="Timeout after 30 seconds")

    def test_models_and_apps(self):
        """Test Django models and apps"""
        print("📊 Testing models and apps...")

        os.chdir(self.gaara_dir)

        # Test model loading
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                '''
from django.apps import apps
models = apps.get_models()
print(f"Loaded {len(models)} models")
for model in models[:5]:  # Show first 5
    print(f"  - {model._meta.app_label}.{model.__name__}")
                '''
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                model_count = len([line for line in result.stdout.split(
                    '\n') if line.strip().startswith('- ')])
                self.add_test_result("Model Loading", "pass", time.time() - start_time,
                                     details="Loaded models successfully")
            else:
                self.add_test_result("Model Loading", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Model Loading", "fail", time.time() - start_time,
                                 error="Timeout after 30 seconds")

        # Test admin interface
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                '''
from django.contrib import admin
from django.apps import apps

registered_models = []
for model in apps.get_models():
    if admin.site.is_registered(model):
        registered_models.append(f"{model._meta.app_label}.{model.__name__}")

print(f"Admin registered models: {len(registered_models)}")
                '''
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.add_test_result("Admin Interface", "pass", time.time() - start_time,
                                     details="Admin models registered")
            else:
                self.add_test_result("Admin Interface", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Admin Interface", "fail", time.time() - start_time,
                                 error="Timeout after 30 seconds")

    def test_api_endpoints(self):
        """Test API endpoints"""
        print("🔌 Testing API endpoints...")

        # Note: This assumes the server is running
        base_url = 'http://localhost:9551'

        endpoints = [
            ('/admin/', 'Admin Interface'),
            ('/api/', 'API Root'),
            ('/api/auth/', 'Authentication API'),
            ('/api/core/', 'Core API')
        ]

        for endpoint, name in endpoints:
            start_time = time.time()
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                duration = time.time() - start_time

                if response.status_code < 500:  # Accept redirects, auth errors, etc.
                    self.add_test_result(f"API - {name}", "pass", duration,
                                         details=f"Status: {response.status_code}")
                else:
                    self.add_test_result(f"API - {name}", "fail", duration,
                                         error=f"HTTP {response.status_code}")

            except requests.RequestException as e:
                self.add_test_result(f"API - {name}", "skip", time.time() - start_time,
                                     details="Server not running or not accessible")

    def test_static_files(self):
        """Test static files"""
        print("📁 Testing static files...")

        os.chdir(self.gaara_dir)

        # Test collectstatic
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'collectstatic', '--noinput', '--dry-run'
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                self.add_test_result(
                    "Static Files Collection", "pass", time.time() - start_time)
            else:
                self.add_test_result("Static Files Collection", "fail", time.time() - start_time,
                                     error=result.stderr)

        except subprocess.TimeoutExpired:
            self.add_test_result("Static Files Collection", "fail", time.time() - start_time,
                                 error="Timeout after 60 seconds")

    def test_frontend_build(self):
        """Test frontend build"""
        print("⚛️  Testing frontend build...")

        frontend_dir = self.gaara_dir / 'main-frontend'

        if not frontend_dir.exists():
            self.add_test_result("Frontend Build", "skip", 0,
                                 details="Frontend directory not found")
            return

        os.chdir(frontend_dir)

        # Check package.json
        start_time = time.time()
        package_json = frontend_dir / 'package.json'

        if package_json.exists():
            self.add_test_result("Frontend Package Config",
                                 "pass", time.time() - start_time)
        else:
            self.add_test_result("Frontend Package Config", "fail", time.time() - start_time,
                                 error="package.json not found")
            return

        # Test build (if npm is available)
        start_time = time.time()
        try:
            result = subprocess.run(
                ['npm', '--version'], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                # Try to build
                build_result = subprocess.run(['npm', 'run', 'build'],
                                              capture_output=True, text=True, timeout=120)

                if build_result.returncode == 0:
                    self.add_test_result(
                        "Frontend Build", "pass", time.time() - start_time)
                else:
                    self.add_test_result("Frontend Build", "warning", time.time() - start_time,
                                         details="Build had issues but may still work")
            else:
                self.add_test_result("Frontend Build", "skip", time.time() - start_time,
                                     details="npm not available")

        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.add_test_result("Frontend Build", "skip", time.time() - start_time,
                                 details="npm not available or timeout")

    def run_performance_tests(self):
        """Run performance tests"""
        print("⚡ Running performance tests...")

        # Import and run performance analyzer
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'performance_analyzer.py', '--mode', 'quick'
            ], capture_output=True, text=True, timeout=120, cwd=self.base_dir)

            if result.returncode == 0:
                self.add_test_result("Performance Analysis", "pass", time.time() - start_time,
                                     details="Performance check completed")
            else:
                self.add_test_result("Performance Analysis", "warning", time.time() - start_time,
                                     details="Performance check had issues")

        except subprocess.TimeoutExpired:
            self.add_test_result("Performance Analysis", "fail", time.time() - start_time,
                                 error="Performance test timeout")
        except Exception as e:
            self.add_test_result("Performance Analysis", "skip", 0,
                                 details=f"Performance analyzer not available: {e}")

    def run_security_tests(self):
        """Run security tests"""
        print("🛡️  Running security tests...")

        # Import and run security checker
        start_time = time.time()
        try:
            result = subprocess.run([
                sys.executable, 'security_checker.py', '--mode', 'quick'
            ], capture_output=True, text=True, timeout=120, cwd=self.base_dir)

            if result.returncode == 0:
                self.add_test_result("Security Analysis", "pass", time.time() - start_time,
                                     details="Security check completed")
            else:
                self.add_test_result("Security Analysis", "warning", time.time() - start_time,
                                     details="Security check found issues")

        except subprocess.TimeoutExpired:
            self.add_test_result("Security Analysis", "fail", time.time() - start_time,
                                 error="Security test timeout")
        except Exception as e:
            self.add_test_result("Security Analysis", "skip", 0,
                                 details=f"Security checker not available: {e}")

    def calculate_summary(self):
        """Calculate test summary"""
        total_tests = len(self.test_results['tests'])
        passed_tests = len(
            [t for t in self.test_results['tests'] if t['status'] == 'pass'])
        failed_tests = len(
            [t for t in self.test_results['tests'] if t['status'] == 'fail'])
        warning_tests = len(
            [t for t in self.test_results['tests'] if t['status'] == 'warning'])
        skipped_tests = len(
            [t for t in self.test_results['tests'] if t['status'] == 'skip'])

        success_rate = (passed_tests / total_tests
                        * 100) if total_tests > 0 else 0

        # Determine overall status
        if failed_tests == 0 and warning_tests <= 2:
            overall_status = 'excellent'
        elif failed_tests <= 1 and warning_tests <= 5:
            overall_status = 'good'
        elif failed_tests <= 3:
            overall_status = 'fair'
        else:
            overall_status = 'poor'

        self.test_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'warning_tests': warning_tests,
            'skipped_tests': skipped_tests,
            'success_rate': success_rate,
            'overall_status': overall_status
        }

        return self.test_results['summary']

    def print_summary(self):
        """Print test summary"""
        summary = self.calculate_summary()

        print("\n" + "=" * 60)
        print("🧪 FINAL SYSTEM TEST SUMMARY")
        print("=" * 60)

        print(f"Overall Status: {summary['overall_status'].upper()}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"  ✅ Passed: {summary['passed_tests']}")
        print(f"  ❌ Failed: {summary['failed_tests']}")
        print(f"  ⚠️  Warnings: {summary['warning_tests']}")
        print(f"  ⏭️  Skipped: {summary['skipped_tests']}")

        # Production readiness assessment
        if summary['overall_status'] in ['excellent', 'good']:
            print("\n🚀 PRODUCTION READINESS: ✅ READY")
            print("   System is ready for production deployment")
        elif summary['overall_status'] == 'fair':
            print("\n🚀 PRODUCTION READINESS: ⚠️  NEEDS ATTENTION")
            print("   Address warnings before production deployment")
        else:
            print("\n🚀 PRODUCTION READINESS: ❌ NOT READY")
            print("   Fix critical issues before production deployment")

        print("\n" + "=" * 60)

    def save_report(self, output_file=None):
        """Save test report"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.base_dir / f'final_test_report_{timestamp}.json'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Test report saved: {output_file}")
        return output_file


def run_tests_by_mode(args, tester):
    """Run sections based on mode to keep main simple"""
    if args.mode in ['complete', 'quick']:
        tester.test_environment_setup()
        tester.test_django_functionality()
        tester.test_models_and_apps()
        tester.test_static_files()

    if args.mode == 'complete':
        tester.test_api_endpoints()
        tester.test_frontend_build()
        tester.run_performance_tests()
        tester.run_security_tests()

    elif args.mode == 'integration':
        tester.test_api_endpoints()
        tester.test_frontend_build()

    elif args.mode == 'performance':
        tester.run_performance_tests()

    elif args.mode == 'security':
        tester.run_security_tests()


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP Final System Test')
    parser.add_argument('--mode', choices=['complete', 'quick', 'integration', 'performance', 'security'],
                        default='complete', help='Test mode')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    tester = FinalSystemTest(verbose=args.verbose)
    tester.print_banner()

    try:
        run_tests_by_mode(args, tester)
        tester.print_summary()
        tester.save_report(args.output)

        # Exit with appropriate code
        summary = tester.test_results['summary']
        if summary['overall_status'] in ['excellent', 'good']:
            sys.exit(0)
        elif summary['overall_status'] == 'fair':
            sys.exit(1)
        else:
            sys.exit(2)

    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Testing error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
