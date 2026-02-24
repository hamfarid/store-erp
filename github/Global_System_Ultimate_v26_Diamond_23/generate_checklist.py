import os

def generate_checklist(root_dir):
    checklist = []
    exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache', 'dist', 'build'}
    
    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        rel_root = os.path.relpath(root, root_dir)
        if rel_root == ".":
            rel_root = ""
            
        if rel_root:
            checklist.append(f"\n### 📂 {rel_root}/")
        else:
            checklist.append("\n### 📂 (Root)")
            
        for file in sorted(files):
            file_path = os.path.join(rel_root, file)
            checklist.append(f"- [ ] `{file_path}`")

    return "\n".join(checklist)

if __name__ == "__main__":
    target_dir = "/home/ubuntu/user_upload_analysis/GitHub/global_system"
    content = "# 📋 Global System File Checklist (v15.9.8)\n\n"
    content += "This checklist tracks the migration of all files to Dynamic Versioning.\n"
    content += generate_checklist(target_dir)
    
    with open("/home/ubuntu/user_upload_analysis/GitHub/global_system/FILE_CHECKLIST.md", "w") as f:
        f.write(content)
    
    print("✅ Checklist generated at FILE_CHECKLIST.md")
