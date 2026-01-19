#!/usr/bin/env python
"""Quick security audit runner"""
import sys
sys.path.insert(0, 'src')
from utils.security_audit import SecurityAudit

def main():
    audit = SecurityAudit('.')
    print('Running Security Audit...')
    print('='*60)

    # Check dependencies
    result = audit.audit_dependencies()
    print(f"Dependencies Check: {result['status']}")
    if result.get('recommendations'):
        for rec in result['recommendations']:
            print(f"  Recommendation: {rec}")

    # Check environment variables
    result = audit.audit_environment_variables()
    print(f"Environment Variables Check: {result['status']}")
    if result.get('missing'):
        print(f"  Missing variables: {result['missing']}")

    # Check for SQL injection vulnerabilities
    result = audit.audit_sql_injection_protection()
    print(f"SQL Injection Protection Check: {result['status']}")

    # Generate overall score
    print('='*60)
    print(f"Security Score: {audit.score}/100")
    grade = 'A' if audit.score >= 90 else 'B' if audit.score >= 80 else 'C' if audit.score >= 70 else 'D' if audit.score >= 60 else 'F'
    print(f"Grade: {grade}")
    
    # Print findings
    if audit.findings:
        print('\nFindings:')
        for finding in audit.findings:
            print(f"  [{finding['severity'].upper()}] {finding['message']}")

if __name__ == '__main__':
    main()

