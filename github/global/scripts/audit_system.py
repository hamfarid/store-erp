"""
Module: audit_system.py
Audit System — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import json

def audit_system():
    """
    Audit system implementation.
    """
    report = {
        "frontend": False,
        "backend": False,
        "database": False,
        "details": {}
    }
    
    # Check Frontend
    if os.path.exists("package.json"):
        report["frontend"] = True
        with open("package.json") as f:
            pkg = json.load(f)
            report["details"]["frontend_deps"] = list(pkg.get("dependencies", {}).keys())
            
    # Check Backend
    if os.path.exists("requirements.txt"):
        report["backend"] = True
        with open("requirements.txt") as f:
            report["details"]["backend_deps"] = f.read().splitlines()
    elif os.path.exists("pyproject.toml"):
        report["backend"] = True
        report["details"]["backend_type"] = "poetry/uv"
        
    # Check Database
    if os.path.exists("docker-compose.yml"):
        with open("docker-compose.yml") as f:
            content = f.read()
            if "postgres" in content or "mysql" in content:
                report["database"] = True
                report["details"]["db_type"] = "docker"
    
    print(json.dumps(report, indent=2))
    
    # Save to file for other scripts
    with open("reports/audit_result.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    audit_system()
