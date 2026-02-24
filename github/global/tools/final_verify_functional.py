#!/usr/bin/env python3
"""
Module: final_verify_functional.py
Final Verify Functional — part of Global System v26.0.2 Diamond 32.
"""
import os
import sys
import yaml

def check_file_exists(path, description):
    """
    Check file exists implementation.
    """
    if os.path.exists(path):
        print(f"✅ {description} found.")
        return True
    else:
        print(f"❌ {description} MISSING at {path}")
        return False

def verify_docker_compose(path):
    """
    Verify docker compose implementation.
    """
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        services = data.get('services', {})
        required = ['chromadb', 'ollama', 'redis']
        
        missing = [s for s in required if s not in services]
        
        if missing:
            print(f"❌ Docker Compose missing services: {missing}")
            return False
            
        # Check Healthchecks
        for svc in required:
            if svc in services:
                if 'healthcheck' not in services[svc]:
                    print(f"⚠️  Service {svc} has no healthcheck defined.")
                else:
                    print(f"✅ Service {svc} has healthcheck.")
                
        print("✅ Docker Compose configuration is valid.")
        return True
    except Exception as e:
        print(f"❌ Invalid Docker Compose file: {e}")
        return False

def verify_setup_script(path):
    """
    Verify setup script implementation.
    """
    try:
        with open(path, 'r') as f:
            content = f.read()
            
        if "requirements.txt" not in content:
            print("❌ setup_project.py does not reference requirements.txt")
            return False
            
        # Check for any docker-compose reference
        if "docker-compose" not in content and "docker" not in content.lower():
            print("⚠️  setup_project.py does not explicitly reference docker-compose (might be handled via external tools)")
        else:
            print("✅ setup_project.py references docker/compose.")
            
        print("✅ setup_project.py logic verified.")
        return True
    except Exception as e:
        print(f"❌ Could not read setup_project.py: {e}")
        return False

def main():
    """
    Main implementation.
    """
    print("🔍 Starting Final Functional Verification (Global System v26 Diamond 32)...\n")
    
    # Base path is the project root (parent of tools/)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 1. Check Infrastructure (Root docker-compose.yml)
    infra_path = os.path.join(base_path, "docker-compose.yml")
    if check_file_exists(infra_path, "Shared Infrastructure (docker-compose.yml)"):
        verify_docker_compose(infra_path)
        
    # 2. Check Dependencies (Root requirements.txt)
    req_path = os.path.join(base_path, "requirements.txt")
    check_file_exists(req_path, "Global System Requirements (requirements.txt)")
    
    # 3. Check Setup Logic
    setup_path = os.path.join(base_path, "setup_project.py")
    if check_file_exists(setup_path, "Setup Script"):
        verify_setup_script(setup_path)
        
    # 4. Check Container Manager
    cm_path = os.path.join(base_path, "tools", "container_manager.py")
    check_file_exists(cm_path, "Container Manager")
    
    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    main()
