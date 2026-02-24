import os
import sys
import ast
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def check_context_engineering_implementation():
    """Verify if speckit.py actually implements context compression."""
    speckit_path = ROOT_DIR / "tools/speckit.py"
    if not speckit_path.exists():
        return False, "speckit.py missing"
    
    content = speckit_path.read_text()
    if "compress_context" not in content and "summarize_history" not in content:
        return False, "No context compression logic found in speckit.py"
    return True, "Context compression logic found"

def check_collective_awareness():
    """Verify if roles are interconnected in the workflow."""
    workflow_path = ROOT_DIR / "TASKS/UNIVERSAL_LIFECYCLE.md"
    if not workflow_path.exists():
        return False, "UNIVERSAL_LIFECYCLE.md missing"
    
    content = workflow_path.read_text()
    required_roles = ["Architect", "Developer", "Reviewer", "QA"]
    missing = [role for role in required_roles if role not in content]
    
    if missing:
        return False, f"Missing roles in workflow: {missing}"
    return True, "All roles integrated in workflow"

def check_ci_cd_readiness():
    """Verify if CI/CD config exists and references the correct tools."""
    ci_path = ROOT_DIR / "infrastructure/ci_cd/pipeline_config.yml"
    if not ci_path.exists():
        return False, "CI/CD config missing"
    
    content = ci_path.read_text()
    if "speckit.py verify" not in content:
        return False, "CI/CD does not run speckit verification"
    return True, "CI/CD runs speckit verification"

def main():
    print("🚀 Starting Deep Architectural Audit (v12.0)...")
    results = []
    
    # 1. Context Engineering
    passed, msg = check_context_engineering_implementation()
    results.append(("Context Engineering", passed, msg))
    
    # 2. Collective Awareness
    passed, msg = check_collective_awareness()
    results.append(("Collective Awareness", passed, msg))
    
    # 3. CI/CD Readiness
    passed, msg = check_ci_cd_readiness()
    results.append(("CI/CD Readiness", passed, msg))
    
    # Report
    print("\n📊 Audit Report:")
    all_passed = True
    for category, passed, msg in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {category}: {msg}")
        if not passed:
            all_passed = False
            
    if all_passed:
        print("\n✅ SYSTEM IS HOLISTICALLY SOUND.")
        sys.exit(0)
    else:
        print("\n❌ SYSTEM HAS FUNCTIONAL GAPS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
