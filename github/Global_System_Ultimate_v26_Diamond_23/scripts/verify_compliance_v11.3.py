import os
import sys
from pathlib import Path

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define the requirements to check
REQUIREMENTS = {
    "Context Engineering": {
        "files": ["BOOTSTRAP.md", "AGENTS.md", "docs/2026_STANDARDS_ANALYSIS.md"],
        "terms": ["Context Engineering", "Token Budgeting", "Dynamic Compression", "Prompt Caching"]
    },
    "Governance": {
        "files": ["AGENTS.md", "BOOTSTRAP.md"],
        "terms": ["Layered Verification", "Two-Strike Rule", "AlphaProof", "FORGE '26"]
    },
    "Tech Stack": {
        "files": ["requirements/requirements.txt", "AGENTS.md", "BOOTSTRAP.md"],
        "terms": ["FastAPI>=0.129", "React 19.2.4", "PostgreSQL 18.2", "Bun v1.3.8"]
    },
    "Terminology": {
        "files": ["AGENTS.md", "docs/2026_STANDARDS_ANALYSIS.md"],
        "terms": ["Multi-Agent Systems", "Chain-of-Vibes", "Human-in-the-Loop Workflow"]
    },
    "New Roles (Diamond 12)": {
        "files": ["roles/ROLE-performance-engineer.md", "roles/ROLE-big-data-architect.md"],
        "terms": ["Performance Engineer", "Big Data Architect"]
    },
    "New Rules (Diamond 13)": {
        "files": ["rules/RULES-context-engineering.md", "rules/RULES-big-data-security.md"],
        "terms": ["Context Engineering", "Big Data Security"]
    }
}

def check_file_content(file_path, terms):
    """Check if a file contains the required terms."""
    full_path = ROOT_DIR / file_path
    if not full_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        content = full_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Error reading file {file_path}: {str(e)}"
    
    missing = [term for term in terms if term not in content]
    
    if missing:
        return False, f"Missing terms in {file_path}: {', '.join(missing)}"
    return True, "OK"

def main():
    print("🚀 Starting Final Compliance Matrix Verification (v11.3 - Diamond 14)...")
    all_passed = True
    
    for category, reqs in REQUIREMENTS.items():
        print(f"\nChecking {category}...")
        for file_path in reqs["files"]:
            # Check if file exists first
            full_path = ROOT_DIR / file_path
            if not full_path.exists():
                 print(f"  ❌ {file_path}: File not found")
                 all_passed = False
                 continue

            # Check terms if file exists
            passed, message = check_file_content(file_path, reqs["terms"])
            if passed:
                print(f"  ✅ {file_path}: OK")
            else:
                print(f"  ❌ {file_path}: {message}")
                all_passed = False
                
    if all_passed:
        print("\n✅ ALL CHECKS PASSED. System is 100% Compliant.")
        sys.exit(0)
    else:
        print("\n❌ COMPLIANCE FAILURE. Fix the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
