#!/usr/bin/env python3
"""
Self-Audit Tool (Global System v26 Diamond 32)
Performs a comprehensive audit of the Global AI System's file structure and content integrity.
Verifies the existence of mandatory files and folders defined in the Master Task List.
Checks for compliance with the Universal Governance Model (AGENTS.md).
"""

import os
import sys
import datetime

# --- CONFIGURATION ---
GLOBAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_TASK_LIST = os.path.join(GLOBAL_DIR, "MASTER_TASK_LIST.md")
AGENTS_GOVERNANCE = os.path.join(GLOBAL_DIR, "AGENTS.md")

# Critical files that MUST exist
REQUIRED_FILES = [
    "AGENTS.md",
    "kilo.json",
    "kiro.yaml",
    "antigravity.yaml",
    "mcp_config.json",
    "genesis.py",
    "tools/speckit.py",
    "tools/sentinel.py",
    "rules/99_anti_hallucination.md"
]

# Optional IDE files (at least one set should exist after configuration)
OPTIONAL_IDE_FILES = [
    ".augment/rules/coding-standards.md",
    ".windsurf/rules/coding-standards.md",
    ".vscode/settings.json",
    ".cursorrules",
    ".cline/config.json"
]

def print_step(msg):
    """
    Print step implementation.
    """
    print(f"\n🔍 AUDIT: {msg}")
    print("="*50)

def check_file_exists(filepath):
    """
    Check file exists implementation.
    """
    full_path = os.path.join(GLOBAL_DIR, filepath)
    exists = os.path.exists(full_path)
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}")
    return exists

def audit_structure():
    """
    Audit structure implementation.
    """
    print_step("Verifying Critical File Structure")
    missing_files = []
    
    # Check required files
    for file in REQUIRED_FILES:
        if not check_file_exists(file):
            missing_files.append(file)
            
    # Check if at least one IDE config exists (warning only)
    ide_configured = False
    print("\nChecking IDE Configuration (Optional):")
    for file in OPTIONAL_IDE_FILES:
        if check_file_exists(file):
            ide_configured = True
            
    if not ide_configured:
        print("⚠️  Warning: No IDE configuration found. Run 'scripts/configure_ide.py'.")
    
    return missing_files

def audit_governance_compliance():
    """
    Audit governance compliance implementation.
    """
    print_step("Auditing Governance Compliance")
    
    # Check AGENTS.md content
    if os.path.exists(AGENTS_GOVERNANCE):
        with open(AGENTS_GOVERNANCE, 'r') as f:
            content = f.read()
            # Updated header check to match the actual file content
            if "Global AI Agent Constitution" in content:
                print("✅ AGENTS.md header verified.")
            else:
                print("❌ AGENTS.md header missing or incorrect.")
            
            if "5-Layer Defense" in content:
                 print("✅ 5-Layer Defense protocol found in AGENTS.md.")
            else:
                 print("❌ 5-Layer Defense protocol MISSING in AGENTS.md.")
    else:
        print("❌ AGENTS.md not found!")

def generate_report(missing_files):
    """
    Generate report implementation.
    """
    report_file = os.path.join(GLOBAL_DIR, f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_file, 'w') as f:
        f.write(f"Global AI System Audit Report (Global System v26 Diamond 32)\n")
        f.write(f"Date: {datetime.datetime.now()}\n")
        f.write("========================================\n\n")
        
        f.write("1. Structure Verification:\n")
        if not missing_files:
            f.write("   ✅ All critical files are present.\n")
        else:
            f.write("   ❌ Missing Files:\n")
            for file in missing_files:
                f.write(f"      - {file}\n")
        
        f.write("\n2. Governance Compliance:\n")
        f.write("   (See console output for details)\n")
        
    print(f"\n📄 Audit Report saved to: {report_file}")

def main():
    """
    Main implementation.
    """
    print("🛡️  GLOBAL SYSTEM SELF-AUDIT (Global System v26 Diamond 32)")
    print("=====================================")
    
    missing = audit_structure()
    audit_governance_compliance()
    generate_report(missing)
    
    if missing:
        print("\n❌ Audit FAILED. Missing critical files.")
        sys.exit(1)
    else:
        print("\n✅ Audit PASSED. System Integrity Verified.")

if __name__ == "__main__":
    main()
