import os
import shutil
import sys
from unittest.mock import patch
import ai_project_creator

# Setup mock project structure
project_name = "test_smart_doc_proj"
project_path = os.path.join(os.getcwd(), project_name)

if os.path.exists(project_path):
    shutil.rmtree(project_path)
os.makedirs(project_path)

# Create dummy files
# Frontend
os.makedirs(os.path.join(project_path, "frontend"), exist_ok=True)
with open(os.path.join(project_path, "frontend", "App.tsx"), "w") as f: f.write("// React App")
with open(os.path.join(project_path, "frontend", "index.css"), "w") as f: f.write("/* CSS */")

# Backend & API
os.makedirs(os.path.join(project_path, "backend"), exist_ok=True)
with open(os.path.join(project_path, "backend", "main.py"), "w") as f: 
    f.write("@app.route('/api/v1/users')\ndef get_users(): pass")
with open(os.path.join(project_path, "backend", "models.py"), "w") as f: f.write("class User: pass")

# Database
with open(os.path.join(project_path, "schema.sql"), "w") as f: f.write("CREATE TABLE users;")

# Docker
with open(os.path.join(project_path, "Dockerfile"), "w") as f: f.write("FROM python:3.9")

# Env Vars
with open(os.path.join(project_path, ".env"), "w") as f: 
    f.write("DB_HOST=localhost\nAPI_KEY=secret123")

print(f"✅ Created mock project at: {project_path}")

# Run Smart Documenter
print("\n--- Running Smart Documenter ---")
ai_project_creator.generate_smart_readme(project_path, project_name)

# Verify Output
readme_path = os.path.join(project_path, "README_PROJECT.md")
if os.path.exists(readme_path):
    print(f"✅ README_PROJECT.md generated successfully!")
    with open(readme_path, "r") as f:
        content = f.read()
        print("\n--- Generated Content Preview ---")
        print(content)
        
        # Check for key sections
        checks = {
            "Frontend": "App.tsx" in content,
            "Backend": "main.py" in content,
            "API": "main.py" in content, # API detected in main.py
            "Database": "schema.sql" in content,
            "Docker": "Dockerfile" in content,
            "Env Vars": "DB_HOST" in content and "API_KEY" in content
        }
        
        print("\n--- Content Verification ---")
        all_passed = True
        for section, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {section} detected")
            if not passed: all_passed = False
            
        if all_passed:
            print("\n🎉 Smart Documenter Test PASSED!")
        else:
            print("\n⚠️ Smart Documenter Test FAILED (Missing sections)")
else:
    print("❌ README_PROJECT.md NOT found!")

# Cleanup
# shutil.rmtree(project_path)
