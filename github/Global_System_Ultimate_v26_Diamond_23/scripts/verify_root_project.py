import os
import sys

# Define expected files and their required content snippets
EXPECTED_FILES = {
    "scripts/logger.py": ["class GaaraLogger", "log_ip"],
    "roles/Financial_Analyst_Agent.md": ["Logging & Documentation Requirements", "logger.log_ai"],
    "roles/System_Architect_Agent.md": ["Logging & Documentation Requirements", "logger.log_system"],
    "roles/Machine_Learning_Engineer_Agent.md": ["Logging & Documentation Requirements", "logger.log_learning"],
    "rules/financial_precision.md": ["Mandatory Logging", "logger.log_ai"],
    "rules/data_handling.md": ["Mandatory Logging", "logger.log_system"],
    "rules/security_protocols.md": ["Mandatory Logging", "logger.log_ip"],
    "prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT.md": ["MANDATORY SYSTEM LOGGER", "logs/system_log.md"],
    "workflows/prediction_lifecycle.md": ["Log Action", "logger.log_ai"],
    "templates/solution_tradeoff_log.md": ["Logging Requirement"],
    "scripts/setup_project.py": ["logger.log_system", "shutil.copy"],
}

def verify_project():
    print("Verifying project files in root directory...")
    missing_files = []
    missing_content = []
    
    # Check for logs directory
    if not os.path.exists("logs"):
        print("❌ logs directory missing")
        missing_files.append("logs/")
    else:
        print("✅ logs directory exists")

    for file_path, required_snippets in EXPECTED_FILES.items():
        if not os.path.exists(file_path):
            print(f"❌ File missing: {file_path}")
            missing_files.append(file_path)
            continue
            
        try:
            with open(file_path, "r") as f:
                content = f.read()
                
            all_snippets_found = True
            for snippet in required_snippets:
                if snippet not in content:
                    print(f"❌ Missing content in {file_path}: '{snippet}'")
                    missing_content.append(f"{file_path} -> {snippet}")
                    all_snippets_found = False
            
            if all_snippets_found:
                print(f"✅ Verified: {file_path}")
                
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            missing_files.append(file_path)

    if missing_files or missing_content:
        print("\nVerification FAILED!")
        print(f"Missing Files: {len(missing_files)}")
        print(f"Content Issues: {len(missing_content)}")
        sys.exit(1)
    else:
        print("\n✅ Verification SUCCESS! All files present and correct.")
        sys.exit(0)

if __name__ == "__main__":
    verify_project()
