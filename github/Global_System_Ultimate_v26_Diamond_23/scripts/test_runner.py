#!/usr/bin/env python3
import sys
import subprocess
import json
import os

def run_command(cmd, log_file):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        with open(log_file, "w") as f:
            f.write(f"CMD: {cmd}\n")
            f.write(f"EXIT: {result.returncode}\n")
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\nSTDERR:\n")
            f.write(result.stderr)
        return result.returncode == 0
    except Exception as e:
        with open(log_file, "w") as f:
            f.write(f"ERROR: {str(e)}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: test_runner.py --target <frontend|backend|database>")
        sys.exit(1)
        
    target = sys.argv[2]
    
    if not os.path.exists("reports/audit_result.json"):
        print("Error: Run audit_system.py first")
        sys.exit(1)
        
    with open("reports/audit_result.json") as f:
        audit = json.load(f)
        
    if target == "frontend":
        if not audit["frontend"]:
            print("Skipping Frontend: Not detected")
            return
        
        # Install dependencies if needed (check node_modules)
        if not os.path.exists("node_modules"):
            print("Installing dependencies...")
            run_command("npm install", "reports/frontend_install.log")
            
        print("Running Frontend Lint...")
        run_command("npm run lint", "reports/frontend_lint.log")
        
        print("Running Frontend Build...")
        run_command("npm run build", "reports/frontend_build.log")
        
    elif target == "backend":
        if not audit["backend"]:
            print("Skipping Backend: Not detected")
            return
        print("Running Backend Tests...")
        run_command("pytest", "reports/backend_test.log")
        
    elif target == "database":
        if not audit["database"]:
            print("Skipping Database: Not detected")
            return
        print("Checking Database Connection...")
        # Simple port check using netcat or similar could go here
        run_command("nc -z localhost 5432", "reports/db_check.log")

if __name__ == "__main__":
    main()
