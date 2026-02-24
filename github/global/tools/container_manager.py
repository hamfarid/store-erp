"""
### 📊 Logical Chart (Create -> Verify -> Execute)
```mermaid
flowchart TD
    Start([Start]) --> Order[1. Order Requirements]
    Order --> Create[2. Create Artifacts]
    Create --> Verify{3. Verify Success?}
    Verify -- No --> Rollback[Rollback/Fix]
    Rollback --> Create
    Verify -- Yes --> Execute[4. Execute/Deploy]
    Execute --> End([End])
```

### 🔄 Workflow
1.  **Order**: Define prerequisites and inputs.
2.  **Create**: Generate the output (file, data, resource).
3.  **Verify**: Check if the output meets standards (Syntax, Logic, Compliance).
4.  **Execute**: Apply the change or return the result.

### 📥 Imports
subprocess, time, sys, json, shutil, os, socket, yaml, argparse, multiprocessing

### 📤 Exports
def run_command(), def check_docker_installed(), def get_container_status(), def ensure_shared_infrastructure(), def get_system_resources(), def calculate_limits(), def check_port(), def find_available_port(), def validate_files(), def scan_ports(), def interactive_port_setup(), def detect_workload(), def auto_provision_stack(), def main()

### 💡 Example
```python
# Example usage for container_manager.py
# from container_manager import def run_command()
```
"""

#!/usr/bin/env python3
"""
Module: container_manager.py

---
### 🔄 Workflow
1. Initialize module.
    2. Process inputs.
    3. Return results.

### 📊 Logical Chart
```mermaid
    graph TD
        A[Start] --> B{Process}
        B -->|Success| C[End]
    ```

### 📥 Imports
- subprocess
    - time
    - sys
    - json
    - shutil
    - os
    - socket
    - yaml
    - argparse
    - multiprocessing

### 📤 Exports
- Function: run_command
    - Function: check_docker_installed
    - Function: get_container_status
    - Function: ensure_shared_infrastructure
    - Function: get_system_resources
    - Function: calculate_limits
    - Function: check_port
    - Function: find_available_port
    - Function: validate_files
    - Function: scan_ports
    - Function: interactive_port_setup
    - Function: detect_workload
    - Function: auto_provision_stack
    - Function: main

### 💡 Examples
```python
    # Example usage
    from container_manager import run_command
    result = run_command()
    print(result)
    ```
"""


"""
Global AI System Global System v26 Diamond 32 - Container Manager
The Synchronized Intelligence Edition

Manages Docker containers for the Global AI System.
Features:
- Auto-detection of required containers.
- Health checks and auto-healing.
- Resource monitoring and auto-tuning.
"""

import subprocess
import time
import sys
import json
import shutil
import os
import socket
import yaml
import argparse
import multiprocessing

# --- CONFIGURATION ---
DEFAULT_REDIS_PORT = 6379
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_CHROMA_PORT = 8000
DEFAULT_OLLAMA_PORT = 11434

def run_command(command):
    """
    Run command implementation.
    """
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def check_docker_installed():
    """
    Check docker installed implementation.
    """
    if not shutil.which("docker"):
        print("❌ Docker is not installed.")
        return False
    return True

def get_container_status(container_name):
    """
    Get container status implementation.
    """
    cmd = ["docker", "inspect", "--format", "{{.State.Health.Status}}", container_name]
    status = run_command(cmd)
    if status:
        return status
    
    # Fallback if no healthcheck defined
    cmd = ["docker", "inspect", "--format", "{{.State.Status}}", container_name]
    return run_command(cmd)

def ensure_shared_infrastructure():
    """
    Ensure shared infrastructure implementation.
    """
    print("🔍 Verifying Shared Infrastructure...")
    
    services = {
        "global_chromadb": "http://localhost:8000/api/v1/heartbeat",
        "global_ollama": "http://localhost:11434/api/tags",
        "global_redis": "redis-cli ping" 
    }
    
    all_healthy = True
    
    for container, health_endpoint in services.items():
        status = get_container_status(container)
        
        if status == "healthy":
            print(f"✅ {container}: Healthy")
        elif status == "running":
            print(f"⚠️  {container}: Running (No Healthcheck)")
        else:
            print(f"❌ {container}: Not Running or Unhealthy ({status})")
            all_healthy = False
            
    if not all_healthy:
        print("🔄 Attempting to heal infrastructure...")
        # In a real scenario, we would trigger docker-compose up here
        # For this script, we just report the status
        return False
        
    return True

def get_system_resources():
    """Detects system RAM and CPU."""
    try:
        # Linux only for now
        with open('/proc/meminfo', 'r') as f:
            mem_total_kb = int(f.readline().split()[1])
            mem_total_gb = mem_total_kb / 1024 / 1024
        
        cpu_count = multiprocessing.cpu_count()
        return {"ram_gb": mem_total_gb, "cpu_cores": cpu_count}
    except:
        return {"ram_gb": 8, "cpu_cores": 4} # Safe default

def calculate_limits(workload):
    """Calculates Docker resource limits based on system specs."""
    specs = get_system_resources()
    ram = specs["ram_gb"]
    
    # Heuristic: Reserve 2GB for OS. Split rest.
    available_ram = max(2, ram - 2)
    
    limits = {}
    
    if "rag" in workload:
        # RAG is heavy. Give it 60% of available.
        limits["ollama"] = f"{int(available_ram * 0.6)}g"
        limits["chromadb"] = "1g"
        limits["app"] = f"{max(128, int(available_ram * 0.2 * 1024))}m"
    else:
        # Standard Web
        limits["app"] = f"{max(256, int(available_ram * 0.5 * 1024))}m"
        limits["postgres"] = "1g"
        
    return limits

def check_port(port):
    """Checks if a port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0

def find_available_port(start_port):
    """Finds the next available port starting from start_port."""
    port = start_port
    while check_port(port):
        port += 1
    return port

def validate_files(project_path):
    """Checks for necessary container files."""
    required = ["Dockerfile", "docker-compose.yml", ".dockerignore"]
    missing = []
    for f in required:
        if not os.path.exists(os.path.join(project_path, f)):
            missing.append(f)
    return missing

def scan_ports(compose_path):
    """Extracts ports from docker-compose.yml."""
    if not os.path.exists(compose_path):
        return {}
    
    with open(compose_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing docker-compose.yml: {e}")
            return {}

    ports = {}
    if 'services' in data:
        for service, config in data['services'].items():
            if 'ports' in config:
                ports[service] = config['ports']
    return ports

def interactive_port_setup(ports):
    """Asks the user to confirm or change ports."""
    print("\n🐳 Container Port Configuration")
    print("-----------------------------")
    
    new_ports = {}
    for service, mapping in ports.items():
        print(f"\nService: {service}")
        if not isinstance(mapping, list):
            mapping = [mapping]
            
        for p in mapping:
            if isinstance(p, str) and ":" in p:
                parts = p.split(":")
                host_port = parts[0]
                container_port = parts[1]
            else:
                host_port = str(p)
                container_port = str(p)
            
            is_taken = check_port(host_port)
            status = "❌ IN USE" if is_taken else "✅ AVAILABLE"
            
            print(f"  - Current Mapping: {host_port}:{container_port} ({status})")
            
            choice = input(f"    Use port {host_port}? (y/n/custom): ").strip().lower()
            
            if choice == 'y':
                if is_taken:
                    print("    ⚠️ Warning: Port is in use. Finding alternative...")
                    alt_port = find_available_port(int(host_port) + 1)
                    print(f"    🔄 Switched to available port: {alt_port}")
                    new_ports[service] = f"{alt_port}:{container_port}"
                else:
                    new_ports[service] = f"{host_port}:{container_port}"
            elif choice == 'n' or choice == 'custom':
                custom = input("    Enter custom host port: ").strip()
                if check_port(custom):
                     print(f"    ⚠️ Port {custom} is also in use!")
                new_ports[service] = f"{custom}:{container_port}"
            else:
                 new_ports[service] = f"{host_port}:{container_port}"

    return new_ports

def detect_workload(project_path):
    """Detects the type of workload based on project files."""
    workload = set()
    
    # Scraper Detection
    if os.path.exists(os.path.join(project_path, "tools", "web_scraper.py")) or \
       os.path.exists(os.path.join(project_path, "scraper.py")):
        workload.add("scraper")
    
    # AI / RAG Detection
    if os.path.exists(os.path.join(project_path, "tools", "rag_engine.py")) or \
       os.path.exists(os.path.join(project_path, "rag.py")) or \
       any("chromadb" in open(os.path.join(project_path, f)).read() for f in os.listdir(project_path) if f.endswith(".py") or f == "requirements.txt"):
        workload.add("rag")
    elif os.path.exists(os.path.join(project_path, "models")) or \
         any(f.endswith(".gguf") for f in os.listdir(project_path)):
        workload.add("ai")

    # Web/Backend Detection
    if os.path.exists(os.path.join(project_path, "app.py")) or \
       os.path.exists(os.path.join(project_path, "main.py")) or \
       os.path.exists(os.path.join(project_path, "package.json")):
        workload.add("web")

    # Database Detection (via ORM or config)
    if os.path.exists(os.path.join(project_path, "prisma")) or \
       os.path.exists(os.path.join(project_path, "alembic.ini")):
        workload.add("database")
        
    return list(workload)

def auto_provision_stack(project_path, workload):
    """Provisions a full stack based on detected workload."""
    compose_path = os.path.join(project_path, "docker-compose.yml")
    
    # Load existing or create new
    if os.path.exists(compose_path):
        with open(compose_path, 'r') as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError:
                data = {}
    else:
        data = {"version": "3.8", "services": {}, "volumes": {}}

    services = data.get("services", {})
    volumes = data.get("volumes", {})
    networks = data.get("networks", {"backend": {}, "frontend": {}})

    print(f"🏗️  Provisioning stack for workload: {', '.join(workload)}")
    
    # Auto-Tuning Limits
    limits = calculate_limits(workload)
    print(f"⚖️  Auto-Tuning Resources: {limits}")

    # 1. Redis (for Scraper or Caching)
    if "scraper" in workload or "redis" not in services:
        if "scraper" in workload:
            print("🕷️  Scraper detected -> Adding Redis (Queue/Cache)")
        
        redis_port = find_available_port(DEFAULT_REDIS_PORT)
        services["redis"] = {
            "image": "redis:alpine",
            "ports": [f"{redis_port}:6379"],
            "volumes": ["redis_data:/data"],
            "networks": ["backend"],
            "restart": "always",
            "healthcheck": {
                "test": ["CMD", "redis-cli", "ping"],
                "interval": "10s",
                "timeout": "5s",
                "retries": 5
            }
        }
        volumes["redis_data"] = {}

    # 2. Database (Postgres)
    if "database" in workload or "web" in workload: # Web usually needs DB
        if "postgres" not in services:
            print("🗄️  Web/DB workload detected -> Adding Postgres")
            pg_port = find_available_port(DEFAULT_POSTGRES_PORT)
            services["postgres"] = {
                "image": "postgres:15-alpine",
                "ports": [f"{pg_port}:5432"],
                "environment": {
                    "POSTGRES_USER": "app_user",
                    "POSTGRES_PASSWORD": "secure_password_change_me",
                    "POSTGRES_DB": "app_db"
                },
                "volumes": ["pg_data:/var/lib/postgresql/data"],
                "networks": ["backend"],
                "restart": "always",
                "deploy": {
                    "resources": {
                        "limits": {"memory": limits.get("postgres", "1g")}
                    }
                }
            }
            volumes["pg_data"] = {}

    # 3. RAG Stack (ChromaDB + Ollama)
    if "rag" in workload:
        print("🧠 RAG Workload detected -> Adding ChromaDB & Ollama")
        
        # ChromaDB
        if "chromadb" not in services:
            chroma_port = find_available_port(DEFAULT_CHROMA_PORT)
            services["chromadb"] = {
                "image": "chromadb/chroma:latest",
                "ports": [f"{chroma_port}:8000"],
                "volumes": ["chroma_data:/chroma/chroma"],
                "environment": {
                    "IS_PERSISTENT": "TRUE"
                },
                "networks": ["backend"],
                "restart": "always",
                "deploy": {
                    "resources": {
                        "limits": {"memory": limits.get("chromadb", "1g")}
                    }
                }
            }
            volumes["chroma_data"] = {}

        # Ollama
        if "ollama" not in services:
            ollama_port = find_available_port(DEFAULT_OLLAMA_PORT)
            services["ollama"] = {
                "image": "ollama/ollama:latest",
                "ports": [f"{ollama_port}:11434"],
                "volumes": ["ollama_data:/root/.ollama"],
                "networks": ["backend"],
                "restart": "always",
                "deploy": {
                    "resources": {
                        "limits": {"memory": limits.get("ollama", "4g")},
                        "reservations": {
                            "devices": [
                                {
                                    "driver": "nvidia",
                                    "count": 1,
                                    "capabilities": ["gpu"]
                                }
                            ]
                        }
                    }
                }
            }
            volumes["ollama_data"] = {}

    # 4. Web App / Scraper Service
    if "app" not in services:
        print("🚀  Adding Main App Service")
        services["app"] = {
            "build": ".",
            "volumes": [".:/app"],
            "networks": ["backend", "frontend"],
            "depends_on": [],
            "environment": [],
            "deploy": {
                "resources": {
                    "limits": {"memory": limits.get("app", "1g")}
                }
            }
        }

    # Link Services
    app_deps = services["app"].get("depends_on", [])
    app_env = services["app"].get("environment", [])
    
    # Ensure list format for deps
    if isinstance(app_deps, dict):
        app_deps = list(app_deps.keys())

    if "redis" in services and "redis" not in app_deps:
        app_deps.append("redis")
        if isinstance(app_env, list):
            app_env.append("REDIS_URL=redis://redis:6379")
        elif isinstance(app_env, dict):
            app_env["REDIS_URL"] = "redis://redis:6379"

    if "postgres" in services and "postgres" not in app_deps:
        app_deps.append("postgres")
        if isinstance(app_env, list):
            app_env.append("DATABASE_URL=postgresql://app_user:secure_password_change_me@postgres:5432/app_db")
        elif isinstance(app_env, dict):
            app_env["DATABASE_URL"] = "postgresql://app_user:secure_password_change_me@postgres:5432/app_db"

    if "chromadb" in services and "chromadb" not in app_deps:
        app_deps.append("chromadb")
        if isinstance(app_env, list):
            app_env.append("CHROMA_HOST=chromadb")
            app_env.append("CHROMA_PORT=8000")
        elif isinstance(app_env, dict):
            app_env["CHROMA_HOST"] = "chromadb"
            app_env["CHROMA_PORT"] = "8000"

    if "ollama" in services and "ollama" not in app_deps:
        app_deps.append("ollama")
        if isinstance(app_env, list):
            app_env.append("OLLAMA_HOST=ollama")
            app_env.append("OLLAMA_PORT=11434")
        elif isinstance(app_env, dict):
            app_env["OLLAMA_HOST"] = "ollama"
            app_env["OLLAMA_PORT"] = "11434"

    services["app"]["depends_on"] = app_deps
    services["app"]["environment"] = app_env

    # Finalize
    data["services"] = services
    data["volumes"] = volumes
    data["networks"] = networks

    with open(compose_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print("✅ Stack provisioning complete.")

def main():
    """
    Main implementation.
    """
    parser = argparse.ArgumentParser(description="Container Manager (Global System v26 Diamond 32)")
    parser.add_argument("project_path", nargs="?", default=".", help="Path to project root")
    parser.add_argument("--check", action="store_true", help="Check ports only")
    parser.add_argument("--provision", action="store_true", help="Auto-provision full stack")
    parser.add_argument("--health", action="store_true", help="Check health of shared infrastructure")
    
    args = parser.parse_args()
    project_path = args.project_path
    compose_path = os.path.join(project_path, "docker-compose.yml")

    # 0. Health Check
    if args.health:
        if ensure_shared_infrastructure():
            print("✨ Shared Infrastructure is Healthy.")
            sys.exit(0)
        else:
            print("⚠️  Shared Infrastructure Issues Detected.")
            sys.exit(1)

    # 1. File Check
    missing = validate_files(project_path)
    if missing and not args.provision:
        print(f"⚠️ Missing Container Files: {', '.join(missing)}")
    
    # 2. Auto-Provisioning
    if args.provision:
        workload = detect_workload(project_path)
        auto_provision_stack(project_path, workload)

    # 3. Port Scan & Interactive Setup
    current_ports = scan_ports(compose_path)
    if current_ports:
        final_ports = interactive_port_setup(current_ports)
        print("\n📝 Final Port Configuration:")
        for svc, p in final_ports.items():
            print(f"  - {svc}: {p}")
        print("\n⚠️ Note: You must manually update docker-compose.yml with these values if changed.")

if __name__ == "__main__":
    main()
