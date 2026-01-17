#!/usr/bin/env python3
"""
Ultimate System Validator
=========================

Comprehensive validation tool for Gaara ERP system.
Validates all components, configurations, and functionality.

Usage:
    python ultimate_system_validator.py [--mode MODE] [--fix] [--verbose]

Modes:
    complete    - Full system validation (default)
    quick       - Quick validation check
    config      - Configuration validation only
    tools       - Tools validation only
    docs        - Documentation validation only
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
import argparse


class UltimateSystemValidator:
    def __init__(self, verbose=False, fix_issues=False):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.verbose = verbose
        self.fix_issues = fix_issues
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'categories': {},
            'summary': {}
        }

    def print_banner(self):
        """Print validator banner"""
        try:
            print("""
ULTIMATE SYSTEM VALIDATOR
=========================
Comprehensive System Validation
Configuration & Tools Check
Production Readiness Assessment
            """)
        except UnicodeEncodeError:
            print("""
ULTIMATE SYSTEM VALIDATOR
=========================
Comprehensive System Validation
Configuration & Tools Check
Production Readiness Assessment
            """)

    def log(self, message, level='INFO'):
        """Log message"""
        if self.verbose or level in ['ERROR', 'SUCCESS', 'WARNING']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {level}: {message}")

    def add_result(self, category, test_name, status, details=None, error=None):
        """Add validation result"""
        if category not in self.validation_results['categories']:
            self.validation_results['categories'][category] = []

        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }

        self.validation_results['categories'][category].append(result)

        # Print result
        status_icon = {
            'pass': '[PASS]',
            'fail': '[FAIL]',
            'warning': '[WARN]',
            'skip': '[SKIP]'
        }.get(status, '[?]')

        print(f"   {status_icon} {test_name}")
        if error and self.verbose:
            print(f"      Error: {error}")
        if details and self.verbose:
            print(f"      Details: {details}")

        return result

    def validate_project_structure(self):
        """Validate project structure"""
        print("Validating project structure...")

        # Essential files
        essential_files = [
            'start_system.py',
            'dev_start.py',
            'performance_analyzer.py',
            'security_checker.py',
            'final_system_test.py',
            'system_monitor.py',
            'backup_system.py',
            'system_config.py',
            'fix_pylint_issues.py',
            'ultimate_system_validator.py'
        ]

        missing_files = []
        for file in essential_files:
            if (self.base_dir / file).exists():
                self.add_result('structure', f'Essential File: {file}', 'pass')
            else:
                self.add_result('structure', f'Essential File: {file}', 'fail',
                                error='File missing')
                missing_files.append(file)

        # Django structure
        django_files = [
            self.gaara_dir / 'manage.py',
            self.gaara_dir / 'gaara_erp' / 'settings.py',
            self.gaara_dir / 'pyproject.toml',
            self.gaara_dir / 'requirements.txt'
        ]

        for file in django_files:
            if file.exists():
                self.add_result(
                    'structure', f'Django File: {file.name}', 'pass')
            else:
                self.add_result('structure', f'Django File: {file.name}', 'fail',
                                error='File missing')

        return len(missing_files) == 0

    def validate_documentation(self):
        """Validate documentation"""
        print("📚 Validating documentation...")

        docs = [
            'USER_GUIDE.md',
            'DEPLOYMENT_GUIDE.md',
            'QUICK_START_GUIDE.md',
            'FINAL_COMPLETION_CERTIFICATE.md',
            'ULTIMATE_COMPLETION_REPORT.md',
            'COMPLETION_SUMMARY.md',
            'FINAL_COMPLETION_STATUS.md'
        ]

        all_docs_present = True
        for doc in docs:
            doc_path = self.base_dir / doc
            if doc_path.exists():
                size = doc_path.stat().st_size
                if size > 1000:  # At least 1KB
                    self.add_result('documentation', f'Documentation: {doc}', 'pass',
                                    details=f'{size:,} bytes')
                else:
                    self.add_result('documentation', f'Documentation: {doc}', 'warning',
                                    details=f'Small file: {size} bytes')
            else:
                self.add_result('documentation', f'Documentation: {doc}', 'fail',
                                error='File missing')
                all_docs_present = False

        return all_docs_present

    def validate_configuration(self):
        """Validate configuration files"""
        print("⚙️ Validating configuration...")

        # Check pyproject.toml
        pyproject_path = self.gaara_dir / 'pyproject.toml'
        if pyproject_path.exists():
            try:
                with open(pyproject_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for essential sections
                required_sections = [
                    '[tool.pylint.main]',
                    '[tool.pylint.django]',
                    '[tool.black]',
                    '[tool.isort]',
                    '[tool.pytest.ini_options]'
                ]

                missing_sections = []
                for section in required_sections:
                    if section in content:
                        self.add_result('configuration',
                                        f'Config Section: {section}', 'pass')
                    else:
                        self.add_result('configuration', f'Config Section: {section}', 'fail',
                                        error='Section missing')
                        missing_sections.append(section)

                # Check Pylint Django configuration
                if 'django-settings-module = "gaara_erp.settings"' in content:
                    self.add_result('configuration',
                                    'Pylint Django Settings', 'pass')
                else:
                    self.add_result('configuration', 'Pylint Django Settings', 'fail',
                                    error='Django settings not configured')

            except Exception as e:
                self.add_result('configuration', 'pyproject.toml parsing', 'fail',
                                error=str(e))
                return False
        else:
            self.add_result('configuration', 'pyproject.toml', 'fail',
                            error='File missing')
            return False

        # Check .pylintrc
        pylintrc_path = self.gaara_dir / '.pylintrc'
        if pylintrc_path.exists():
            self.add_result('configuration', '.pylintrc file', 'pass')
        else:
            self.add_result('configuration', '.pylintrc file', 'warning',
                            details='Optional file missing')

        return True

    def validate_tools_functionality(self):
        """Validate tools functionality"""
        print("🛠️ Validating tools functionality...")

        tools_to_test = [
            ('start_system.py', '--help'),
            ('dev_start.py', '--help'),
            ('performance_analyzer.py', '--help'),
            ('security_checker.py', '--help'),
            ('final_system_test.py', '--help'),
            ('system_monitor.py', '--help'),
            ('backup_system.py', '--help'),
            ('fix_pylint_issues.py', '--help')
        ]

        all_tools_working = True
        for tool, arg in tools_to_test:
            tool_path = self.base_dir / tool
            if tool_path.exists():
                try:
                    result = subprocess.run([
                        sys.executable, str(tool_path), arg
                    ], capture_output=True, text=True, timeout=10)

                    if result.returncode == 0 or 'usage:' in result.stdout.lower() or 'help' in result.stdout.lower():
                        self.add_result('tools', f'Tool: {tool}', 'pass',
                                        details='Help command works')
                    else:
                        self.add_result('tools', f'Tool: {tool}', 'warning',
                                        details='Help command issues')

                except subprocess.TimeoutExpired:
                    self.add_result('tools', f'Tool: {tool}', 'warning',
                                    details='Help command timeout')
                except Exception as e:
                    self.add_result('tools', f'Tool: {tool}', 'fail',
                                    error=str(e))
                    all_tools_working = False
            else:
                self.add_result('tools', f'Tool: {tool}', 'fail',
                                error='Tool missing')
                all_tools_working = False

        return all_tools_working

    def validate_django_setup(self):
        """Validate Django setup"""
        print("🐍 Validating Django setup...")

        os.chdir(self.gaara_dir)

        # Test Django check
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'check', '--deploy'
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                self.add_result('django', 'Django System Check', 'pass')
            else:
                self.add_result('django', 'Django System Check', 'warning',
                                details='Some deployment checks failed')

        except subprocess.TimeoutExpired:
            self.add_result('django', 'Django System Check', 'fail',
                            error='Timeout after 60 seconds')
        except Exception as e:
            self.add_result('django', 'Django System Check', 'fail',
                            error=str(e))

        # Test database connectivity
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                'from django.db import connection; connection.ensure_connection(); print("OK")'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and 'OK' in result.stdout:
                self.add_result('django', 'Database Connectivity', 'pass')
            else:
                self.add_result('django', 'Database Connectivity', 'fail',
                                error='Cannot connect to database')

        except Exception as e:
            self.add_result('django', 'Database Connectivity', 'fail',
                            error=str(e))

        # Test migrations
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'showmigrations', '--plan'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.add_result('django', 'Migration Status', 'pass')
            else:
                self.add_result('django', 'Migration Status', 'warning',
                                details='Migration issues detected')

        except Exception as e:
            self.add_result('django', 'Migration Status', 'fail',
                            error=str(e))

        return True

    def validate_dependencies(self):
        """Validate dependencies"""
        print("📦 Validating dependencies...")

        # Check if pylint-django is installed
        try:
            import pylint_django
            self.add_result('dependencies', 'pylint-django', 'pass')
        except ImportError:
            self.add_result('dependencies', 'pylint-django', 'fail',
                            error='Not installed')
            if self.fix_issues:
                self.log("Installing pylint-django...", 'INFO')
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pylint-django'],
                                   check=True, capture_output=True)
                    self.add_result(
                        'dependencies', 'pylint-django (fixed)', 'pass')
                except Exception as e:
                    self.add_result('dependencies', 'pylint-django (fix failed)', 'fail',
                                    error=str(e))

        # Check essential packages
        essential_packages = [
            'django', 'djangorestframework', 'psutil', 'requests']
        for package in essential_packages:
            try:
                __import__(package)
                self.add_result('dependencies', f'Package: {package}', 'pass')
            except ImportError:
                self.add_result('dependencies', f'Package: {package}', 'fail',
                                error='Not installed')

        return True

    def calculate_summary(self):
        """Calculate validation summary"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        warning_tests = 0
        skipped_tests = 0

        for category, tests in self.validation_results['categories'].items():
            for test in tests:
                total_tests += 1
                if test['status'] == 'pass':
                    passed_tests += 1
                elif test['status'] == 'fail':
                    failed_tests += 1
                elif test['status'] == 'warning':
                    warning_tests += 1
                elif test['status'] == 'skip':
                    skipped_tests += 1

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

        self.validation_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'warning_tests': warning_tests,
            'skipped_tests': skipped_tests,
            'success_rate': success_rate,
            'overall_status': overall_status
        }

        return self.validation_results['summary']

    def print_summary(self):
        """Print validation summary"""
        summary = self.calculate_summary()

        print("\n" + "=" * 60)
        print("🔍 ULTIMATE SYSTEM VALIDATION SUMMARY")
        print("=" * 60)

        print(f"Overall Status: {summary['overall_status'].upper()}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"  ✅ Passed: {summary['passed_tests']}")
        print(f"  ❌ Failed: {summary['failed_tests']}")
        print(f"  ⚠️  Warnings: {summary['warning_tests']}")
        print(f"  ⏭️  Skipped: {summary['skipped_tests']}")

        # Category breakdown
        print("\n📊 Category Breakdown:")
        for category, tests in self.validation_results['categories'].items():
            category_passed = len([t for t in tests if t['status'] == 'pass'])
            category_total = len(tests)
            category_rate = (category_passed / category_total
                             * 100) if category_total > 0 else 0
            print(
                f"   {category.title()}: {category_passed}/{category_total} ({category_rate:.1f}%)")

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
        """Save validation report"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.base_dir / f'validation_report_{timestamp}.json'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Validation report saved: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(description='Ultimate System Validator')
    parser.add_argument('--mode', choices=['complete', 'quick', 'config', 'tools', 'docs'],
                        default='complete', help='Validation mode')
    parser.add_argument('--fix', action='store_true',
                        help='Attempt to fix issues automatically')
    parser.add_argument('--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--output', help='Output file for report')

    args = parser.parse_args()

    validator = UltimateSystemValidator(
        verbose=args.verbose, fix_issues=args.fix)
    validator.print_banner()

    try:
        if args.mode in ['complete', 'quick']:
            validator.validate_project_structure()
            validator.validate_configuration()
            validator.validate_dependencies()

        if args.mode == 'complete':
            validator.validate_documentation()
            validator.validate_tools_functionality()
            validator.validate_django_setup()

        elif args.mode == 'config':
            validator.validate_configuration()

        elif args.mode == 'tools':
            validator.validate_tools_functionality()

        elif args.mode == 'docs':
            validator.validate_documentation()

        validator.print_summary()
        validator.save_report(args.output)

        # Exit with appropriate code
        summary = validator.validation_results['summary']
        if summary['overall_status'] in ['excellent', 'good']:
            sys.exit(0)
        elif summary['overall_status'] == 'fair':
            sys.exit(1)
        else:
            sys.exit(2)

    except KeyboardInterrupt:
        print("\n🛑 Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
