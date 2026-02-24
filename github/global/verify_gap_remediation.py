"""Verify that previously identified gaps have been remediated.

Part of Global System v26.0.2 Diamond 32.
"""
import os

BASE_DIR = "/home/ubuntu/user_upload_analysis/GitHub/global_system"
REQUIRED_FILES = [
    "ml-ai-governance/rules/RULES-computer-vision-standards.md",
    "ml-ai-governance/rules/RULES-financial-data-handling.yaml",
    "ml-ai-governance/rules/POLICY-model-backup-retention.yaml",
    "ml-ai-governance/rules/ml_feature_store_governance.md",
    "ml-ai-governance/rules/ml_alerting_escalation.yaml",
    "ml-ai-governance/rules/ml_retraining_triggers.yaml",
    "ml-ai-governance/rules/RULES-image-binarization.md",
    "ml-ai-governance/rules/RULES-embedding-storage.md",
    "ml-ai-governance/rules/RULES-multi-crop-augmentation.md",
    "ml-ai-governance/rules/RULES-gradcam-heatmap.md",
    "ml-ai-governance/errors/ERROR-multi-view-pipeline-catalog.md",
    "ml-ai-governance/examples/EXAMPLE-docker-compose-ml-pipeline.yaml",
    "ml-ai-governance/examples/EXAMPLE-multi-view-plant-disease.md",
    "ml-ai-governance/templates/TEMPLATE-data-pipeline-docs.md",
    "ml-ai-governance/knowledge/GUIDE-scraping-tool-selection.md",
    "ml-ai-governance/knowledge/GUIDE-vector-database-selection.md",
    "ml-ai-governance/knowledge/workflows/ML_MULTI_VIEW_WORKFLOW.md",
    "prompts/69_machine_learning.md",
    "workflows/ml_ai_development.md"
]

def verify():
    """
    Verify implementation.
    """
    missing = []
    shallow = []
    
    for file_path in REQUIRED_FILES:
        full_path = os.path.join(BASE_DIR, file_path)
        if not os.path.exists(full_path):
            missing.append(file_path)
            continue
            
        with open(full_path, 'r') as f:
            lines = f.readlines()
            if len(lines) < 50: # Threshold for "Deep" content
                shallow.append(f"{file_path} ({len(lines)} lines)")
                
    if missing:
        print("❌ MISSING FILES:")
        for f in missing: print(f"  - {f}")
    else:
        print("✅ All required files present.")
        
    if shallow:
        print("⚠️ SHALLOW FILES (< 50 lines):")
        for f in shallow: print(f"  - {f}")
    else:
        print("✅ All files have deep content (> 50 lines).")

if __name__ == "__main__":
    verify()
