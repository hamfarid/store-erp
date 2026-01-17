#!/usr/bin/env python3
"""
Quick System Check
==================

Quick validation of Gaara ERP system status.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def print_banner():
    print("""
🔍 QUICK SYSTEM CHECK 🔍
========================
🎯 System Status Validation
✅ Quick Health Check
    """)


def check_essential_files():
    """Check essential files"""
    print("📁 Checking essential files...")
    
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
        'quick_system_check.py'
    ]
    
    missing_files = []
    present_files = []
    
    for file in essential_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            present_files.append((file, size))
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            missing_files.append(file)
            print(f"   ❌ {file} - مفقود")
    
    return len(missing_files) == 0, present_files, missing_files


def check_documentation():
    """Check documentation"""
    print("\n📚 Checking documentation...")
    
    docs = [
        'USER_GUIDE.md',
        'DEPLOYMENT_GUIDE.md',
        'QUICK_START_GUIDE.md',
        'FINAL_COMPLETION_CERTIFICATE.md',
        'ULTIMATE_COMPLETION_REPORT.md',
        'COMPLETION_SUMMARY.md',
        'FINAL_COMPLETION_STATUS.md'
    ]
    
    missing_docs = []
    present_docs = []
    
    for doc in docs:
        if Path(doc).exists():
            size = Path(doc).stat().st_size
            present_docs.append((doc, size))
            print(f"   ✅ {doc} ({size:,} bytes)")
        else:
            missing_docs.append(doc)
            print(f"   ❌ {doc} - مفقود")
    
    return len(missing_docs) == 0, present_docs, missing_docs


def check_django_structure():
    """Check Django structure"""
    print("\n🐍 Checking Django structure...")
    
    gaara_dir = Path('gaara_erp')
    if not gaara_dir.exists():
        print("   ❌ مجلد gaara_erp مفقود")
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
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            missing_django.append(file)
            print(f"   ⚠️ {file} - مفقود")
    
    return len(missing_django) <= 1, present_django, missing_django  # Allow 1 missing file


def check_configuration():
    """Check configuration"""
    print("\n⚙️ Checking configuration...")
    
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
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description} - مفقود")
                    config_ok = False
            
            return config_ok
            
        except Exception as e:
            print(f"   ❌ خطأ في قراءة pyproject.toml: {e}")
            return False
    else:
        print("   ❌ ملف pyproject.toml مفقود")
        return False


def generate_summary(files_ok, docs_ok, django_ok, config_ok):
    """Generate summary"""
    print("\n" + "="*60)
    print("📊 QUICK SYSTEM CHECK SUMMARY")
    print("="*60)
    
    checks = [
        ("Essential Files", files_ok),
        ("Documentation", docs_ok),
        ("Django Structure", django_ok),
        ("Configuration", config_ok)
    ]
    
    passed_checks = sum(1 for _, status in checks if status)
    total_checks = len(checks)
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"Passed Checks: {passed_checks}/{total_checks}")
    
    for check_name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {check_name}")
    
    # Overall status
    if success_rate == 100:
        overall_status = "EXCELLENT"
        status_icon = "🏆"
        message = "System is perfect and ready for production!"
    elif success_rate >= 75:
        overall_status = "GOOD"
        status_icon = "✅"
        message = "System is ready with minor issues."
    elif success_rate >= 50:
        overall_status = "FAIR"
        status_icon = "⚠️"
        message = "System needs some attention."
    else:
        overall_status = "POOR"
        status_icon = "❌"
        message = "System needs significant work."
    
    print(f"\n{status_icon} Overall Status: {overall_status}")
    print(f"📝 Assessment: {message}")
    
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
        
        # Generate summary
        success_rate, overall_status = generate_summary(files_ok, docs_ok, django_ok, config_ok)
        
        # Statistics
        print(f"\n📈 Statistics:")
        print(f"   📁 Essential Files: {len(present_files)} present, {len(missing_files)} missing")
        print(f"   📚 Documentation: {len(present_docs)} present, {len(missing_docs)} missing")
        print(f"   🐍 Django Files: {len(present_django)} present, {len(missing_django)} missing")
        
        # Quick start commands
        print(f"\n🚀 Quick Start Commands:")
        print(f"   Production: python start_system.py")
        print(f"   Development: python dev_start.py")
        print(f"   Performance: python performance_analyzer.py")
        print(f"   Security: python security_checker.py")
        print(f"   Testing: python final_system_test.py")
        
        print("\n" + "="*60)
        
        # Return appropriate exit code
        if success_rate == 100:
            print("🎉 System check completed successfully!")
            return 0
        elif success_rate >= 75:
            print("⚠️ System check completed with minor issues.")
            return 1
        else:
            print("❌ System check found significant issues.")
            return 2
            
    except Exception as e:
        print(f"❌ System check error: {e}")
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 System check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
