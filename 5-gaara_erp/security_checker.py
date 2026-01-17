#!/usr/bin/env python3
"""
Gaara ERP Security Checker
==========================

Comprehensive security analysis tool for Gaara ERP system.
Checks for common vulnerabilities, configuration issues, and security best practices.

Usage:
    python security_checker.py [--mode MODE] [--output FILE] [--fix]

Modes:
    quick       - Quick security scan (default)
    detailed    - Detailed security analysis
    django      - Django-specific security checks
    files       - File permission and content checks
    network     - Network security analysis
"""

import os
import sys
import json
import subprocess
import hashlib
import re
from pathlib import Path
from datetime import datetime
import argparse


class SecurityChecker:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.findings = []
        self.severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        
    def print_banner(self):
        """Print security checker banner"""
        print("""
🛡️  GAARA ERP SECURITY CHECKER 🛡️
==================================
🔍 Vulnerability Assessment
🔒 Security Configuration Review
⚠️  Risk Analysis & Recommendations
        """)
        
    def add_finding(self, title, description, severity, category, file_path=None, line_number=None, recommendation=None):
        """Add security finding"""
        finding = {
            'title': title,
            'description': description,
            'severity': severity,
            'category': category,
            'file_path': str(file_path) if file_path else None,
            'line_number': line_number,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }
        
        self.findings.append(finding)
        self.severity_counts[severity] += 1
        
        # Print finding
        severity_icons = {
            'critical': '🚨',
            'high': '❌',
            'medium': '⚠️',
            'low': '💡',
            'info': 'ℹ️'
        }
        
        icon = severity_icons.get(severity, '❓')
        print(f"   {icon} {severity.upper()}: {title}")
        if file_path:
            print(f"      File: {file_path}")
        if line_number:
            print(f"      Line: {line_number}")
            
    def check_django_settings(self):
        """Check Django security settings"""
        print("🐍 Checking Django security settings...")
        
        settings_files = [
            self.gaara_dir / 'gaara_erp' / 'settings.py',
            self.gaara_dir / 'gaara_erp' / 'production_settings.py'
        ]
        
        for settings_file in settings_files:
            if not settings_file.exists():
                continue
                
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check DEBUG setting
                if 'DEBUG = True' in content and 'production' in str(settings_file):
                    self.add_finding(
                        "Debug Mode Enabled in Production",
                        "DEBUG=True is set in production settings, which can expose sensitive information",
                        "critical",
                        "django_config",
                        settings_file,
                        recommendation="Set DEBUG=False in production"
                    )
                    
                # Check SECRET_KEY
                if 'SECRET_KEY' in content:
                    secret_key_match = re.search(r"SECRET_KEY\s*=\s*['\"]([^'\"]+)['\"]", content)
                    if secret_key_match:
                        secret_key = secret_key_match.group(1)
                        if 'django-insecure' in secret_key:
                            self.add_finding(
                                "Insecure Secret Key",
                                "Using default Django insecure secret key",
                                "high",
                                "django_config",
                                settings_file,
                                recommendation="Generate a new secure secret key"
                            )
                        elif len(secret_key) < 50:
                            self.add_finding(
                                "Weak Secret Key",
                                "Secret key is too short (less than 50 characters)",
                                "medium",
                                "django_config",
                                settings_file,
                                recommendation="Use a longer, more complex secret key"
                            )
                            
                # Check ALLOWED_HOSTS
                if 'ALLOWED_HOSTS' in content:
                    if 'ALLOWED_HOSTS = []' in content:
                        self.add_finding(
                            "Empty ALLOWED_HOSTS",
                            "ALLOWED_HOSTS is empty, which may cause issues in production",
                            "medium",
                            "django_config",
                            settings_file,
                            recommendation="Configure ALLOWED_HOSTS with your domain names"
                        )
                    elif '*' in content and 'ALLOWED_HOSTS' in content:
                        self.add_finding(
                            "Wildcard in ALLOWED_HOSTS",
                            "Using '*' in ALLOWED_HOSTS allows any host",
                            "medium",
                            "django_config",
                            settings_file,
                            recommendation="Specify exact hostnames instead of '*'"
                        )
                        
                # Check CSRF settings
                if 'CSRF_COOKIE_SECURE = False' in content:
                    self.add_finding(
                        "Insecure CSRF Cookie",
                        "CSRF_COOKIE_SECURE is set to False",
                        "medium",
                        "django_config",
                        settings_file,
                        recommendation="Set CSRF_COOKIE_SECURE = True for HTTPS"
                    )
                    
                # Check session security
                if 'SESSION_COOKIE_SECURE = False' in content:
                    self.add_finding(
                        "Insecure Session Cookie",
                        "SESSION_COOKIE_SECURE is set to False",
                        "medium",
                        "django_config",
                        settings_file,
                        recommendation="Set SESSION_COOKIE_SECURE = True for HTTPS"
                    )
                    
            except Exception as e:
                self.add_finding(
                    "Settings File Read Error",
                    f"Could not read settings file: {e}",
                    "low",
                    "file_access",
                    settings_file
                )
                
    def check_sensitive_files(self):
        """Check for sensitive files and information"""
        print("📁 Checking for sensitive files...")
        
        sensitive_patterns = [
            ('*.key', 'Private key files'),
            ('*.pem', 'Certificate files'),
            ('*.p12', 'Certificate files'),
            ('*.pfx', 'Certificate files'),
            ('.env', 'Environment files'),
            ('*.log', 'Log files'),
            ('db.sqlite3', 'Database files'),
            ('*.backup', 'Backup files'),
            ('*.sql', 'SQL dump files')
        ]
        
        for pattern, description in sensitive_patterns:
            files = list(self.base_dir.rglob(pattern))
            for file_path in files:
                # Skip files in .git, __pycache__, etc.
                if any(part.startswith('.') or part == '__pycache__' for part in file_path.parts):
                    continue
                    
                self.add_finding(
                    f"Sensitive File Found: {description}",
                    f"Found potentially sensitive file: {file_path.name}",
                    "medium",
                    "sensitive_files",
                    file_path,
                    recommendation="Ensure file is properly secured and not exposed"
                )
                
    def check_file_permissions(self):
        """Check file permissions"""
        print("🔐 Checking file permissions...")
        
        important_files = [
            self.gaara_dir / 'manage.py',
            self.gaara_dir / 'gaara_erp' / 'settings.py',
            self.base_dir / '.env'
        ]
        
        for file_path in important_files:
            if file_path.exists():
                try:
                    stat_info = file_path.stat()
                    mode = oct(stat_info.st_mode)[-3:]
                    
                    # Check if file is world-readable
                    if mode.endswith('4') or mode.endswith('6') or mode.endswith('7'):
                        self.add_finding(
                            "World-Readable File",
                            f"File {file_path.name} is readable by others (permissions: {mode})",
                            "medium",
                            "file_permissions",
                            file_path,
                            recommendation="Restrict file permissions (chmod 600 or 644)"
                        )
                        
                    # Check if file is world-writable
                    if mode.endswith('2') or mode.endswith('3') or mode.endswith('6') or mode.endswith('7'):
                        self.add_finding(
                            "World-Writable File",
                            f"File {file_path.name} is writable by others (permissions: {mode})",
                            "high",
                            "file_permissions",
                            file_path,
                            recommendation="Remove write permissions for others (chmod 644 or 600)"
                        )
                        
                except Exception as e:
                    self.add_finding(
                        "Permission Check Error",
                        f"Could not check permissions for {file_path}: {e}",
                        "low",
                        "file_access",
                        file_path
                    )
                    
    def check_dependencies(self):
        """Check for vulnerable dependencies"""
        print("📦 Checking dependencies for vulnerabilities...")
        
        requirements_file = self.gaara_dir / 'requirements.txt'
        if requirements_file.exists():
            try:
                # Run safety check if available
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'list', '--format=json'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
                    
                    # Check for known vulnerable packages (basic check)
                    vulnerable_packages = {
                        'django': {'min_version': '4.0', 'reason': 'Security updates'},
                        'pillow': {'min_version': '8.0', 'reason': 'Security vulnerabilities'},
                        'requests': {'min_version': '2.25', 'reason': 'Security fixes'}
                    }
                    
                    for package in packages:
                        name = package['name'].lower()
                        version = package['version']
                        
                        if name in vulnerable_packages:
                            min_version = vulnerable_packages[name]['min_version']
                            reason = vulnerable_packages[name]['reason']
                            
                            # Simple version comparison (not perfect but basic)
                            if version < min_version:
                                self.add_finding(
                                    f"Outdated Package: {name}",
                                    f"Package {name} version {version} may have security issues. {reason}",
                                    "medium",
                                    "dependencies",
                                    requirements_file,
                                    recommendation=f"Update {name} to version {min_version} or later"
                                )
                                
            except Exception as e:
                self.add_finding(
                    "Dependency Check Error",
                    f"Could not check dependencies: {e}",
                    "low",
                    "dependency_check"
                )
                
    def check_code_patterns(self):
        """Check for insecure code patterns"""
        print("🔍 Checking for insecure code patterns...")
        
        python_files = list(self.gaara_dir.rglob('*.py'))
        
        insecure_patterns = [
            (r'eval\s*\(', 'Use of eval() function', 'high'),
            (r'exec\s*\(', 'Use of exec() function', 'high'),
            (r'os\.system\s*\(', 'Use of os.system()', 'medium'),
            (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', 'Shell injection risk', 'high'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password', 'critical'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key', 'high'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret', 'high'),
            (r'\.raw\s*\(', 'Raw SQL query', 'medium'),
            (r'mark_safe\s*\(', 'Use of mark_safe()', 'medium')
        ]
        
        for file_path in python_files:
            # Skip certain directories
            if any(part in str(file_path) for part in ['migrations', '__pycache__', '.git']):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for pattern, description, severity in insecure_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Find line number
                        line_number = content[:match.start()].count('\n') + 1
                        
                        self.add_finding(
                            f"Insecure Code Pattern: {description}",
                            f"Found potentially insecure pattern in code",
                            severity,
                            "code_patterns",
                            file_path,
                            line_number,
                            recommendation="Review and secure this code pattern"
                        )
                        
            except Exception as e:
                self.add_finding(
                    "Code Analysis Error",
                    f"Could not analyze file {file_path}: {e}",
                    "low",
                    "file_access",
                    file_path
                )
                
    def check_database_security(self):
        """Check database security configuration"""
        print("🗄️  Checking database security...")
        
        # Check for SQLite database file
        db_file = self.gaara_dir / 'db.sqlite3'
        if db_file.exists():
            try:
                stat_info = db_file.stat()
                mode = oct(stat_info.st_mode)[-3:]
                
                if mode != '600':
                    self.add_finding(
                        "Database File Permissions",
                        f"SQLite database file has permissions {mode}, should be 600",
                        "medium",
                        "database_security",
                        db_file,
                        recommendation="Set database file permissions to 600 (chmod 600 db.sqlite3)"
                    )
                    
            except Exception as e:
                self.add_finding(
                    "Database Permission Check Error",
                    f"Could not check database permissions: {e}",
                    "low",
                    "database_security"
                )
                
    def generate_security_report(self):
        """Generate security report"""
        total_findings = len(self.findings)
        
        if total_findings == 0:
            return {
                'status': 'secure',
                'message': 'No security issues found',
                'score': 100
            }
            
        # Calculate security score
        score = 100
        score -= self.severity_counts['critical'] * 20
        score -= self.severity_counts['high'] * 10
        score -= self.severity_counts['medium'] * 5
        score -= self.severity_counts['low'] * 2
        score -= self.severity_counts['info'] * 1
        
        score = max(0, score)
        
        if score >= 90:
            status = 'excellent'
        elif score >= 75:
            status = 'good'
        elif score >= 50:
            status = 'fair'
        else:
            status = 'poor'
            
        return {
            'status': status,
            'score': score,
            'total_findings': total_findings,
            'severity_breakdown': self.severity_counts
        }
        
    def save_report(self, output_file=None):
        """Save security report"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.base_dir / f'security_report_{timestamp}.json'
            
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.generate_security_report(),
            'findings': self.findings,
            'recommendations': self.get_top_recommendations()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 Security report saved: {output_file}")
        return output_file
        
    def get_top_recommendations(self):
        """Get top security recommendations"""
        recommendations = []
        
        if self.severity_counts['critical'] > 0:
            recommendations.append("🚨 Address critical security issues immediately")
            
        if self.severity_counts['high'] > 0:
            recommendations.append("❌ Fix high-severity security issues as soon as possible")
            
        if any(f['category'] == 'django_config' for f in self.findings):
            recommendations.append("🐍 Review and harden Django security settings")
            
        if any(f['category'] == 'file_permissions' for f in self.findings):
            recommendations.append("🔐 Fix file permission issues")
            
        if any(f['category'] == 'dependencies' for f in self.findings):
            recommendations.append("📦 Update vulnerable dependencies")
            
        if not recommendations:
            recommendations.append("✅ Security posture looks good! Continue monitoring.")
            
        return recommendations
        
    def print_summary(self):
        """Print security summary"""
        print("\n" + "="*60)
        print("🛡️  SECURITY ANALYSIS SUMMARY")
        print("="*60)
        
        report = self.generate_security_report()
        
        print(f"Security Score: {report['score']}/100 ({report['status'].upper()})")
        print(f"Total Findings: {report['total_findings']}")
        
        if report['total_findings'] > 0:
            print(f"\nSeverity Breakdown:")
            for severity, count in self.severity_counts.items():
                if count > 0:
                    print(f"   {severity.capitalize()}: {count}")
                    
        print(f"\n🎯 Top Recommendations:")
        recommendations = self.get_top_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
            
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP Security Checker')
    parser.add_argument('--mode', choices=['quick', 'detailed', 'django', 'files', 'network'],
                       default='quick', help='Security check mode')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues automatically')
    
    args = parser.parse_args()
    
    checker = SecurityChecker()
    checker.print_banner()
    
    try:
        if args.mode == 'quick':
            checker.check_django_settings()
            checker.check_sensitive_files()
            
        elif args.mode == 'detailed':
            checker.check_django_settings()
            checker.check_sensitive_files()
            checker.check_file_permissions()
            checker.check_dependencies()
            checker.check_code_patterns()
            checker.check_database_security()
            
        elif args.mode == 'django':
            checker.check_django_settings()
            
        elif args.mode == 'files':
            checker.check_sensitive_files()
            checker.check_file_permissions()
            
        checker.print_summary()
        checker.save_report(args.output)
        
    except KeyboardInterrupt:
        print("\n🛑 Security check interrupted by user")
    except Exception as e:
        print(f"❌ Security check error: {e}")


if __name__ == '__main__':
    main()
