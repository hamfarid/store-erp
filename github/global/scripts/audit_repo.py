#!/usr/bin/env python3
"""
FILE: scripts/audit_repo.py | PURPOSE: Full system audit & report generation
OWNER: DevSecOps | RELATED: docs/Task_List.md, docs/Audit_Summary.md
LAST-AUDITED: 2025-11-04

Comprehensive audit script aligned to GLOBAL_GUIDELINES_UNIFIED_v8.0.0.
Generates docs/Status_Report.md and docs/Status_Report.json.
"""

import json
import os
from pathlib import Path
from datetime import datetime


def audit_repo():
    """Run comprehensive audit and generate status report."""
    
    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    findings = {
        "timestamp": datetime.now().isoformat(),
        "repo_root": str(repo_root),
        "checks": {}
    }
    
    # Check 1: Mandatory documentation artifacts
    mandatory_docs = [
        "Inventory.md",
        "TechStack.md",
        "Routes_FE.md",
        "Routes_BE.md",
        "DB_Schema.md",
        "Permissions_Model.md",
        "Env.md",
        "Security.md",
        "Threat_Model.md",
        "Error_Catalog.md",
        "Runbook.md",
        "CSP.md",
        "Resilience.md",
        "Brand_Palette.json",
        "UI_Design_System.md",
        "Class_Registry.md",
        "Imports_Map.md",
        "Symbol_Index.md",
        "Duplicates_And_Drift.md",
        "Missing_Libraries.md",
        "Status_Report.md",
        "Remediation_Plan.md",
        "DONT_DO_THIS_AGAIN.md",
        "Solution_Tradeoff_Log.md"
    ]
    
    present_docs = []
    missing_docs = []
    for doc in mandatory_docs:
        doc_path = docs_dir / doc
        if doc_path.exists():
            present_docs.append(doc)
        else:
            missing_docs.append(doc)
    
    findings["checks"]["documentation"] = {
        "status": "PASS" if len(missing_docs) <= 5 else "WARN",
        "present": len(present_docs),
        "total": len(mandatory_docs),
        "coverage_pct": round(100 * len(present_docs) / len(mandatory_docs), 1),
        "missing": missing_docs
    }
    
    # Check 2: Security middleware
    security_files = [
        "backend/src/security_headers.py",
        "backend/src/middleware/csrf_protection.py",
        "backend/src/middleware/rate_limiter.py"
    ]
    
    present_security = []
    for sec_file in security_files:
        if (repo_root / sec_file).exists():
            present_security.append(sec_file)
    
    findings["checks"]["security_middleware"] = {
        "status": "PASS" if len(present_security) == len(security_files) else "WARN",
        "present": len(present_security),
        "total": len(security_files),
        "files": present_security
    }
    
    # Check 3: API contracts
    api_contract_files = [
        "contracts/openapi.yaml",
        "contracts/sdui.schema.json"
    ]
    
    present_contracts = []
    for contract in api_contract_files:
        if (repo_root / contract).exists():
            present_contracts.append(contract)
    
    findings["checks"]["api_contracts"] = {
        "status": "PASS" if len(present_contracts) >= 1 else "FAIL",
        "present": len(present_contracts),
        "total": len(api_contract_files),
        "files": present_contracts
    }
    
    # Check 4: CI/CD workflows
    workflows_dir = repo_root / ".github" / "workflows"
    workflows = []
    if workflows_dir.exists():
        workflows = [f.name for f in workflows_dir.glob("*.yml")]
    
    findings["checks"]["ci_workflows"] = {
        "status": "PASS" if len(workflows) >= 8 else "WARN",
        "count": len(workflows),
        "workflows": sorted(workflows)
    }
    
    # Check 5: Database models
    models_dir = repo_root / "backend" / "src" / "models"
    models = []
    if models_dir.exists():
        models = [f.name for f in models_dir.glob("*.py") if f.name != "__init__.py"]
    
    findings["checks"]["database_models"] = {
        "status": "PASS" if len(models) >= 10 else "WARN",
        "count": len(models),
        "models": sorted(models)
    }
    
    # Summary
    passed = sum(1 for check in findings["checks"].values() if check.get("status") == "PASS")
    total_checks = len(findings["checks"])
    
    findings["summary"] = {
        "checks_passed": passed,
        "checks_total": total_checks,
        "overall_status": "PASS" if passed == total_checks else "WARN"
    }
    
    # Write JSON report
    json_path = docs_dir / "Status_Report.json"
    with open(json_path, "w") as f:
        json.dump(findings, f, indent=2)
    
    # Write Markdown report
    md_path = docs_dir / "Status_Report.md"
    md_content = f"""# Repository Audit Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status:** {findings['summary']['overall_status']}

## Summary

- **Checks Passed:** {findings['summary']['checks_passed']}/{findings['summary']['checks_total']}
- **Overall Status:** {findings['summary']['overall_status']}

## Detailed Findings

### Documentation Artifacts
- **Status:** {findings['checks']['documentation']['status']}
- **Coverage:** {findings['checks']['documentation']['coverage_pct']}% ({findings['checks']['documentation']['present']}/{findings['checks']['documentation']['total']})
- **Missing:** {len(findings['checks']['documentation']['missing'])} files

### Security Middleware
- **Status:** {findings['checks']['security_middleware']['status']}
- **Present:** {findings['checks']['security_middleware']['present']}/{findings['checks']['security_middleware']['total']}

### API Contracts
- **Status:** {findings['checks']['api_contracts']['status']}
- **Present:** {findings['checks']['api_contracts']['present']}/{findings['checks']['api_contracts']['total']}

### CI/CD Workflows
- **Status:** {findings['checks']['ci_workflows']['status']}
- **Count:** {findings['checks']['ci_workflows']['count']}

### Database Models
- **Status:** {findings['checks']['database_models']['status']}
- **Count:** {findings['checks']['database_models']['count']}

## Next Steps

1. Review missing documentation artifacts
2. Implement missing security middleware (if any)
3. Ensure API contracts are up-to-date
4. Verify CI/CD workflows are running
5. Check database models for consistency

---

*Report generated by audit_repo.py aligned to GLOBAL_GUIDELINES_UNIFIED_v8.0.0*
"""
    
    with open(md_path, "w") as f:
        f.write(md_content)
    
    print(f"✅ Audit complete!")
    print(f"📊 JSON Report: {json_path}")
    print(f"📄 Markdown Report: {md_path}")
    print(f"\n{findings['summary']['overall_status']}: {findings['summary']['checks_passed']}/{findings['summary']['checks_total']} checks passed")
    
    return findings


if __name__ == "__main__":
    audit_repo()

