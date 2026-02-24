"""Analyze gaps between expected and actual system file structure.

Part of Global System v26.0.2 Diamond 32.
"""
import os

BASE_DIR = "/home/ubuntu/user_upload_analysis/GitHub/global_system"

# 1. Critical Files (Must exist and be deep)
CRITICAL_FILES = {
    "ml-ai-governance/rules/RULES-computer-vision-standards.md": 100,
    "ml-ai-governance/rules/RULES-financial-data-handling.yaml": 100,
    "ml-ai-governance/rules/POLICY-model-backup-retention.yaml": 80,
    "ml-ai-governance/rules/ml_feature_store_governance.md": 100,
    "ml-ai-governance/rules/ml_alerting_escalation.yaml": 80,
    "ml-ai-governance/rules/ml_retraining_triggers.yaml": 80,
    "prompts/69_machine_learning.md": 200,
    "workflows/ml_ai_development.md": 250,
    "ml-ai-governance/errors/ERROR-multi-view-pipeline-catalog.md": 50,
}

# 2. Duplicate Check (Should NOT exist in root if in ml-ai-governance)
DUPLICATE_CANDIDATES = [
    "rules/RULES-computer-vision-standards.md",
    "rules/RULES-financial-data-handling.yaml",
    "rules/POLICY-model-backup-retention.yaml",
    "rules/ml_feature_store_governance.md",
    "rules/ml_alerting_escalation.yaml",
    "rules/ml_retraining_triggers.yaml",
]

def check_files():
    """
    Check files implementation.
    """
    print("🔍 Starting Gap Analysis Check...")
    
    # Check Critical Files
    missing = []
    shallow = []
    for file_path, min_lines in CRITICAL_FILES.items():
        full_path = os.path.join(BASE_DIR, file_path)
        if not os.path.exists(full_path):
            missing.append(file_path)
            continue
            
        with open(full_path, 'r') as f:
            lines = len(f.readlines())
            if lines < min_lines:
                shallow.append(f"{file_path} ({lines}/{min_lines})")

    if missing:
        print(f"❌ MISSING FILES ({len(missing)}):")
        for f in missing: print(f"  - {f}")
    else:
        print("✅ All critical files present.")

    if shallow:
        print(f"⚠️ SHALLOW FILES ({len(shallow)}):")
        for f in shallow: print(f"  - {f}")
    else:
        print("✅ All critical files meet depth requirements.")

    # Check Duplicates
    duplicates = []
    for file_path in DUPLICATE_CANDIDATES:
        full_path = os.path.join(BASE_DIR, file_path)
        if os.path.exists(full_path):
            duplicates.append(file_path)

    if duplicates:
        print(f"⚠️ DUPLICATES FOUND IN ROOT ({len(duplicates)}):")
        for f in duplicates: print(f"  - {f} (Should be deleted or symlinked)")
    else:
        print("✅ No duplicates found in root.")

if __name__ == "__main__":
    check_files()
