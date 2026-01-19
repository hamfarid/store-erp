"""
FILE: backend/src/utils/security_audit.py | PURPOSE: Security audit and vulnerability scanning | OWNER: Security Team | LAST-AUDITED: 2025-11-18

Security Audit Module

Provides comprehensive security auditing and vulnerability scanning:
- Dependency vulnerability scanning
- Security header validation
- Configuration security checks
- Code security analysis
- Compliance checks

Version: 1.0.0
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class SecurityAudit:
    """
    Security Audit and Vulnerability Scanner

    Performs comprehensive security checks on the application.
    """

    def __init__(self, project_root: str):
        """
        Initialize security audit

        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.findings = []
        self.score = 100  # Start with perfect score, deduct for issues

    def audit_dependencies(self) -> Dict[str, any]:
        """
        Audit Python dependencies for known vulnerabilities

        Returns:
            Dict: Audit results
        """
        results = {
            "status": "pass",
            "vulnerabilities": [],
            "recommendations": []
        }

        try:
            # Run safety check (requires 'safety' package)
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )

            if result.returncode != 0:
                results["status"] = "fail"
                results["vulnerabilities"] = result.stdout
                self.score -= 20
                self.findings.append({
                    "severity": "high",
                    "category": "dependencies",
                    "message": "Vulnerable dependencies detected",
                    "details": result.stdout
                })
        except FileNotFoundError:
            results["status"] = "skipped"
            results["recommendations"].append(
                "Install 'safety' package for dependency scanning")

        return results

    def audit_security_headers(
            self, headers: Dict[str, str]) -> Dict[str, any]:
        """
        Audit HTTP security headers

        Args:
            headers: HTTP response headers

        Returns:
            Dict: Audit results
        """
        required_headers = {
            "Content-Security-Policy": "default-src 'self'",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Strict-Transport-Security": "max-age=31536000",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        results = {
            "status": "pass",
            "missing_headers": [],
            "weak_headers": []
        }

        for header, recommended_value in required_headers.items():
            if header not in headers:
                results["missing_headers"].append(header)
                results["status"] = "fail"
                self.score -= 5
                self.findings.append({
                    "severity": "medium",
                    "category": "headers",
                    "message": f"Missing security header: {header}",
                    "recommendation": f"Add header: {header}: {recommended_value}"
                })

        return results

    def audit_environment_variables(self) -> Dict[str, any]:
        """
        Audit environment variable security

        Returns:
            Dict: Audit results
        """
        results = {
            "status": "pass",
            "issues": []
        }

        # Check for .env file in repository
        env_file = self.project_root / ".env"
        if env_file.exists():
            results["issues"].append(
                ".env file found in repository (should be in .gitignore)")
            results["status"] = "warning"
            self.score -= 10
            self.findings.append({
                "severity": "high",
                "category": "configuration",
                "message": ".env file should not be committed to repository",
                "recommendation": "Add .env to .gitignore and use .env.example instead"
            })

        # Check for hardcoded secrets in code
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]

        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or "node_modules" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["issues"].append(
                            f"Potential hardcoded secret in {py_file}")
                        results["status"] = "fail"
                        self.score -= 15
                        self.findings.append({
                            "severity": "critical",
                            "category": "secrets",
                            "message": f"Potential hardcoded secret in {py_file.name}",
                            "recommendation": "Use environment variables for secrets"
                        })
                        break
            except Exception:
                pass

        return results

    def audit_sql_injection_protection(self) -> Dict[str, any]:
        """
        Audit SQL injection protection

        Returns:
            Dict: Audit results
        """
        results = {
            "status": "pass",
            "issues": []
        }

        # Check for string concatenation in SQL queries
        dangerous_patterns = [
            r'execute\(["\'].*\+.*["\']',
            r'\.format\(.*SELECT',
            r'f["\']SELECT.*{',
        ]

        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or "node_modules" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                for pattern in dangerous_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["issues"].append(
                            f"Potential SQL injection in {py_file}")
                        results["status"] = "fail"
                        self.score -= 20
                        self.findings.append({
                            "severity": "critical",
                            "category": "sql_injection",
                            "message": f"Potential SQL injection vulnerability in {py_file.name}",
                            "recommendation": "Use parameterized queries or ORM"
                        })
                        break
            except Exception:
                pass

        return results

    def generate_report(self) -> Dict[str, any]:
        """
        Generate comprehensive security audit report

        Returns:
            Dict: Complete audit report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "score": max(0, self.score),  # Ensure score doesn't go below 0
            "grade": self._calculate_grade(self.score),
            "findings": self.findings,
            "summary": {
                "critical": len([f for f in self.findings if f["severity"] == "critical"]),
                "high": len([f for f in self.findings if f["severity"] == "high"]),
                "medium": len([f for f in self.findings if f["severity"] == "medium"]),
                "low": len([f for f in self.findings if f["severity"] == "low"]),
            },
            "recommendations": self._generate_recommendations()
        }

        return report

    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Critical issues first
        critical = [f for f in self.findings if f["severity"] == "critical"]
        if critical:
            recommendations.append(
                "🔴 CRITICAL: Address all critical security issues immediately")

        # High priority
        high = [f for f in self.findings if f["severity"] == "high"]
        if high:
            recommendations.append(
                "🟠 HIGH: Fix high-priority security issues within 24 hours")

        # Medium priority
        medium = [f for f in self.findings if f["severity"] == "medium"]
        if medium:
            recommendations.append(
                "🟡 MEDIUM: Address medium-priority issues within 1 week")

        # General recommendations
        recommendations.extend([
            "✅ Implement automated security scanning in CI/CD pipeline",
            "✅ Conduct regular security audits (monthly)",
            "✅ Keep all dependencies up to date",
            "✅ Enable security monitoring and alerting",
            "✅ Conduct penetration testing (quarterly)"
        ])

        return recommendations


# Convenience function
def run_security_audit(project_root: str) -> Dict[str, any]:
    """
    Run comprehensive security audit

    Args:
        project_root: Path to project root

    Returns:
        Dict: Audit report
    """
    audit = SecurityAudit(project_root)

    # Run all audits
    audit.audit_dependencies()
    audit.audit_environment_variables()
    audit.audit_sql_injection_protection()

    # Generate report
    return audit.generate_report()
