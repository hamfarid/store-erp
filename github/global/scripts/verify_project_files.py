"""
Module: verify_project_files.py
Verify Project Files — part of Global System v26.0.2 Diamond 32.
"""
import os
import sys

# Define the expected file structure and key content requirements
EXPECTED_FILES = {
    "roles/Financial_Analyst_Agent.md": ["Logging & Documentation Requirements", "System Log", "AI Log", "Learning Log", "User Log", "IP Log"],
    "roles/System_Architect_Agent.md": ["Logging & Documentation Requirements", "System Log", "AI Log", "Learning Log", "User Log", "IP Log"],
    "roles/Machine_Learning_Engineer_Agent.md": ["Logging & Documentation Requirements", "System Log", "AI Log", "Learning Log", "User Log", "IP Log"],
    "rules/financial_precision.md": ["Mandatory Logging Requirements", "Calculation Logging", "Transaction Logging", "Audit Trail", "User Access", "Security Monitoring"],
    "rules/data_handling.md": ["Mandatory Logging Requirements", "Data Ingestion Logging", "Processing Logging", "Data Access Logging", "Audit Trail"],
    "rules/security_protocols.md": ["Mandatory Logging Requirements", "Authentication Logging", "Access Control Logging", "Incident Logging"],
    "prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT.md": ["Operational Workflow & Logging", "System Logger", "Deep Integration", "Log Files"],
    "workflows/prediction_lifecycle.md": ["Log Action", "logger.log_system", "logger.log_ai", "logger.log_learning"],
    "templates/solution_tradeoff_log.md": ["Mandatory Logging", "logger.log_learning"],
    "scripts/logger.py": ["class GaaraLogger", "log_system", "log_ai", "log_learning", "log_user", "log_ip"],
    "scripts/setup_project.py": ["logger = GaaraLogger()", "logger.log_system"],
    "scripts/configure_ide.py": ["logger = GaaraLogger()", "logger.log_system"],
}

def verify_files():
    """
    Verify files implementation.
    """
    missing_files = []
    missing_content = []
    
    print("Starting file verification...")
    
    for file_path, required_content in EXPECTED_FILES.items():
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing file: {file_path}")
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            for requirement in required_content:
                if requirement not in content:
                    missing_content.append(f"{file_path}: Missing '{requirement}'")
                    print(f"⚠️  Content missing in {file_path}: '{requirement}'")
                    
            print(f"✅ Verified: {file_path}")
            
        except Exception as e:
            print(f"❌ Error reading {file_path}: {str(e)}")
            
    if missing_files:
        print("\n❌ CRITICAL: Missing files detected!")
        for f in missing_files:
            print(f"  - {f}")
        sys.exit(1)
        
    if missing_content:
        print("\n⚠️  WARNING: Content requirements not met!")
        for c in missing_content:
            print(f"  - {c}")
        sys.exit(1)
        
    print("\n✅ All files verified successfully!")
    sys.exit(0)

if __name__ == "__main__":
    verify_files()
