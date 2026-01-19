"""
FILE: backend/scripts/run_security_audit.py | PURPOSE: Security audit runner | OWNER: Security Team | LAST-AUDITED: 2025-11-18

Security Audit Runner Script

Runs comprehensive security audit and generates report.

Usage:
    python backend/scripts/run_security_audit.py

Version: 1.0.0
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.src.utils.security_audit import run_security_audit


def main():
    """Run security audit and generate report"""
    
    print("=" * 80)
    print("🔐 GAARA AI - SECURITY AUDIT")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project: {project_root}")
    print("=" * 80)
    print()
    
    # Run audit
    print("Running security audit...")
    print()
    
    report = run_security_audit(str(project_root))
    
    # Display results
    print("=" * 80)
    print("📊 AUDIT RESULTS")
    print("=" * 80)
    print()
    
    print(f"🎯 Security Score: {report['score']}/100")
    print(f"📝 Grade: {report['grade']}")
    print()
    
    print("📋 Findings Summary:")
    print(f"  🔴 Critical: {report['summary']['critical']}")
    print(f"  🟠 High:     {report['summary']['high']}")
    print(f"  🟡 Medium:   {report['summary']['medium']}")
    print(f"  🟢 Low:      {report['summary']['low']}")
    print()
    
    # Display findings
    if report['findings']:
        print("=" * 80)
        print("🔍 DETAILED FINDINGS")
        print("=" * 80)
        print()
        
        for i, finding in enumerate(report['findings'], 1):
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }
            
            print(f"{i}. {severity_emoji.get(finding['severity'], '⚪')} [{finding['severity'].upper()}] {finding['category']}")
            print(f"   Message: {finding['message']}")
            if 'recommendation' in finding:
                print(f"   Fix: {finding['recommendation']}")
            print()
    
    # Display recommendations
    print("=" * 80)
    print("💡 RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print()
    print("=" * 80)
    
    # Save report to file
    report_file = project_root / "docs" / "Security_Audit_Report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Full report saved to: {report_file}")
    print("=" * 80)
    print()
    
    # Exit with appropriate code
    if report['score'] < 70:
        print("❌ AUDIT FAILED: Security score below 70")
        sys.exit(1)
    elif report['summary']['critical'] > 0:
        print("⚠️  WARNING: Critical security issues found")
        sys.exit(1)
    else:
        print("✅ AUDIT PASSED: No critical issues found")
        sys.exit(0)


if __name__ == "__main__":
    main()

