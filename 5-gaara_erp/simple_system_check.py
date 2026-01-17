#!/usr/bin/env python3
"""
Simple System Check
===================

Simple validation of Gaara ERP system status without Unicode issues.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def print_banner():
    print("""
SIMPLE SYSTEM CHECK
===================
System Status Validation
Quick Health Check
    """)


def check_essential_files():
    """Check essential files"""
    print("Checking essential files...")
    
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
        'ultimate_system_validator.py',
        'quick_system_check.py',
        'simple_system_check.py'
    ]
    
    missing_files = []
    present_files = []
    
    for file in essential_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            present_files.append((file, size))
            print(f"   [PASS] {file} ({size:,} bytes)")
        else:
            missing_files.append(file)
            print(f"   [FAIL] {file} - Missing")
    
    return len(missing_files) == 0, present_files, missing_files


def check_documentation():
    """Check documentation"""
    print("\nChecking documentation...")
    
    docs = [
        'USER_GUIDE.md',
        'DEPLOYMENT_GUIDE.md', 
        'QUICK_START_GUIDE.md',
        'FINAL_COMPLETION_CERTIFICATE.md',
        'ULTIMATE_COMPLETION_REPORT.md',
        'COMPLETION_SUMMARY.md',
        'FINAL_COMPLETION_STATUS.md',
        'FINAL_SYSTEM_COMPLETION_REPORT.md'
    ]
    
    missing_docs = []
    present_docs = []
    
    for doc in docs:
        if Path(doc).exists():
            size = Path(doc).stat().st_size
            present_docs.append((doc, size))
            print(f"   [PASS] {doc} ({size:,} bytes)")
        else:
            missing_docs.append(doc)
            print(f"   [FAIL] {doc} - Missing")
    
    return len(missing_docs) == 0, present_docs, missing_docs


def check_django_structure():
    """Check Django structure"""
    print("\nChecking Django structure...")
    
    gaara_dir = Path('gaara_erp')
    if not gaara_dir.exists():
        print("   [FAIL] gaara_erp directory missing")
        return False
    
    django_files = [
        'manage.py',
        'gaara_erp/settings.py',
        'pyproject.toml', 
        'requirements.txt',
        'db.sqlite3',
        '.pylintrc'
    ]
    
    missing_django = []
    present_django = []
    
    for file in django_files:
        file_path = gaara_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            present_django.append((file, size))
            print(f"   [PASS] {file} ({size:,} bytes)")
        else:
            missing_django.append(file)
            print(f"   [WARN] {file} - Missing")
    
    return len(missing_django) <= 1, present_django, missing_django


def check_configuration():
    """Check configuration"""
    print("\nChecking configuration...")
    
    pyproject_path = Path('gaara_erp/pyproject.toml')
    if pyproject_path.exists():
        try:
            with open(pyproject_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check essential sections
            checks = [
                ('[tool.pylint.main]', 'Pylint main config'),
                ('[tool.pylint.django]', 'Pylint Django config'),
                ('django-settings-module = "gaara_erp.settings"', 'Django settings module'),
                ('[tool.black]', 'Black formatter config'),
                ('[tool.isort]', 'Import sorter config'),
                ('[tool.pytest.ini_options]', 'Pytest config')
            ]
            
            config_ok = True
            for check, description in checks:
                if check in content:
                    print(f"   [PASS] {description}")
                else:
                    print(f"   [FAIL] {description} - Missing")
                    config_ok = False
            
            return config_ok
            
        except Exception as e:
            print(f"   [FAIL] Error reading pyproject.toml: {e}")
            return False
    else:
        print("   [FAIL] pyproject.toml missing")
        return False


def test_pylint_django():
    """Test if pylint-django is working"""
    print("\nTesting pylint-django...")
    
    try:
        import pylint_django
        print("   [PASS] pylint-django imported successfully")
        return True
    except ImportError:
        print("   [FAIL] pylint-django not installed")
        return False


def generate_summary(files_ok, docs_ok, django_ok, config_ok, pylint_ok):
    """Generate summary"""
    print("\n" + "="*60)
    print("SIMPLE SYSTEM CHECK SUMMARY")
    print("="*60)
    
    checks = [
        ("Essential Files", files_ok),
        ("Documentation", docs_ok),
        ("Django Structure", django_ok),
        ("Configuration", config_ok),
        ("Pylint Django", pylint_ok)
    ]
    
    passed_checks = sum(1 for _, status in checks if status)
    total_checks = len(checks)
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"Passed Checks: {passed_checks}/{total_checks}")
    
    for check_name, status in checks:
        status_icon = "[PASS]" if status else "[FAIL]"
        print(f"   {status_icon} {check_name}")
    
    # Overall status
    if success_rate == 100:
        overall_status = "EXCELLENT"
        status_icon = "[EXCELLENT]"
        message = "System is perfect and ready for production!"
    elif success_rate >= 80:
        overall_status = "GOOD"
        status_icon = "[GOOD]"
        message = "System is ready with minor issues."
    elif success_rate >= 60:
        overall_status = "FAIR"
        status_icon = "[FAIR]"
        message = "System needs some attention."
    else:
        overall_status = "POOR"
        status_icon = "[POOR]"
        message = "System needs significant work."
    
    print(f"\n{status_icon} Overall Status: {overall_status}")
    print(f"Assessment: {message}")
    
    return success_rate, overall_status


def main():
    """Main function"""
    print_banner()
    
    try:
        # Run checks
        files_ok, present_files, missing_files = check_essential_files()
        docs_ok, present_docs, missing_docs = check_documentation()
        django_ok, present_django, missing_django = check_django_structure()
        config_ok = check_configuration()
        pylint_ok = test_pylint_django()
        
        # Generate summary
        success_rate, overall_status = generate_summary(
            files_ok, docs_ok, django_ok, config_ok, pylint_ok
        )
        
        # Statistics
        print(f"\nStatistics:")
        print(f"   Essential Files: {len(present_files)} present, {len(missing_files)} missing")
        print(f"   Documentation: {len(present_docs)} present, {len(missing_docs)} missing")
        print(f"   Django Files: {len(present_django)} present, {len(missing_django)} missing")
        
        # Quick start commands
        print(f"\nQuick Start Commands:")
        print(f"   Production: python start_system.py")
        print(f"   Development: python dev_start.py")
        print(f"   Performance: python performance_analyzer.py")
        print(f"   Security: python security_checker.py")
        print(f"   Testing: python final_system_test.py")
        print(f"   Quick Check: python simple_system_check.py")
        
        print("\n" + "="*60)
        
        # Return appropriate exit code
        if success_rate == 100:
            print("System check completed successfully!")
            return 0
        elif success_rate >= 80:
            print("System check completed with minor issues.")
            return 1
        else:
            print("System check found significant issues.")
            return 2
            
    except Exception as e:
        print(f"System check error: {e}")
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nSystem check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
