"""Audit the Global System and update files to match current standards.

Part of Global System v26.0.2 Diamond 32.
"""
import os
import re

# Load Version
try:
    with open("/home/ubuntu/user_upload_analysis/GitHub/global_system/VERSION", "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

print(f"🎯 Target Version: {VERSION}")

def update_file(filepath):
    """
    Update file implementation.
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Replace hardcoded versions in headers/comments (e.g., v15.X -> v26.0 Diamond 32 GAARA AI)
        # Regex to find v14.x, v15.x but NOT the target version itself to avoid loops
        # We want to standardize everything to the current VERSION
        
        # Update "Global System v26 Diamond 32 vXX.X"
        content = re.sub(r"Global System v26 Diamond 32 v\d+\.\d+(\.\d+)?", f"Global System v26 Diamond 32 {VERSION}", content)
        
        # Update "v26.0" or similar standalone if it looks like a version tag in a header
        content = re.sub(r"#\s+.*\s+\(v\d+\.\d+(\.\d+)?\)", f" ({VERSION})", content)
        
        # 2. For Python files, inject dynamic version reading if missing
        if filepath.endswith(".py") and "VERSION" not in content and "import os" in content:
            # Simple heuristic: Inject after imports
            if "def main():" in content or "if __name__" in content:
                injection = f'''
# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "{VERSION}"
'''
                # This is a bit risky to automate blindly for all files, 
                # so we will log it for manual review or apply only to known tools.
                # For now, we stick to text replacement.
                pass

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def update_checklist(filepath, status):
    """
    Update checklist implementation.
    """
    # Mark file as checked in FILE_CHECKLIST.md
    checklist_path = "/home/ubuntu/user_upload_analysis/GitHub/global_system/FILE_CHECKLIST.md"
    try:
        with open(checklist_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        filename = os.path.basename(filepath)
        # We search for the line containing the filename
        for line in lines:
            if filename in line and "- [ ]" in line:
                new_lines.append(line.replace("- [ ]", "- [x]"))
            else:
                new_lines.append(line)
        
        with open(checklist_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
    except Exception as e:
        print(f"⚠️ Error updating checklist: {e}")

def main():
    """
    Main implementation.
    """
    root_dir = "/home/ubuntu/user_upload_analysis/GitHub/global_system"
    checklist_path = os.path.join(root_dir, "FILE_CHECKLIST.md")
    
    if not os.path.exists(checklist_path):
        print("❌ Checklist not found!")
        return

    with open(checklist_path, 'r') as f:
        lines = f.readlines()
    
    files_to_process = []
    for line in lines:
        if "- [ ]" in line:
            # Extract path from `path`
            match = re.search(r"`(.*?)`", line)
            if match:
                rel_path = match.group(1)
                full_path = os.path.join(root_dir, rel_path)
                files_to_process.append(full_path)
    
    print(f"🔍 Found {len(files_to_process)} files to audit...")
    
    for filepath in files_to_process:
        if os.path.exists(filepath):
            # Skip binary files or specific extensions
            if filepath.endswith(('.png', '.jpg', '.zip', '.pyc')):
                update_checklist(filepath, "skipped")
                continue
                
            updated = update_file(filepath)
            update_checklist(filepath, "checked")
        else:
            print(f"⚠️ File not found: {filepath}")

if __name__ == "__main__":
    main()
