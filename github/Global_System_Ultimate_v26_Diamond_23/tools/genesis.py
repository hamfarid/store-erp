#!/usr/bin/env python3
"""
Genesis (Global System Ultimate)
Bootstraps the project structure, calculates smart ports, and configures infrastructure.
"""

import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_ports():
    """Calculates smart ports based on user input."""
    print(f"\n🔢 Smart Port Calculator ({VERSION})")
    try:
        backend_port = int(input("Enter Backend Port (Default 8000): ") or 8000)
        frontend_port = int(input("Enter Frontend Port (Default 3000): ") or 3000)
    except ValueError:
        logging.error("Invalid input. Using defaults.")
        backend_port = 8000
        frontend_port = 3000

    ports = {
        "BACKEND_PORT": backend_port,
        "FRONTEND_PORT": frontend_port,
        "REDIS_PORT": backend_port + frontend_port,
        "DB_PORT": backend_port + 100,
        "AI_PORT": backend_port + 200,
        "ML_PORT": frontend_port + 100,
        "PROXY_PORT": 8080  # Default Nginx proxy port
    }
    
    logging.info(f"✅ Calculated Ports: {ports}")
    return ports

def generate_env_file(ports):
    """Generates .env file with calculated ports."""
    env_content = f"""# Global System Ultimate {VERSION} Environment
BACKEND_PORT={ports['BACKEND_PORT']}
FRONTEND_PORT={ports['FRONTEND_PORT']}
REDIS_PORT={ports['REDIS_PORT']}
DB_PORT={ports['DB_PORT']}
AI_PORT={ports['AI_PORT']}
ML_PORT={ports['ML_PORT']}
PROXY_PORT={ports['PROXY_PORT']}

# Database Config
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=global_system

# AI Config
OLLAMA_HOST=http://localhost:{ports['AI_PORT']}
CHROMA_HOST=http://localhost:{ports['DB_PORT']}
"""
    with open(".env", "w") as f:
        f.write(env_content)
    logging.info("✅ Generated .env file.")

def generate_nginx_config(ports):
    """Generates nginx.conf from template."""
    template_path = Path("infrastructure/nginx/nginx.conf.template")
    output_path = Path("infrastructure/nginx/nginx.conf")
    
    if not template_path.exists():
        logging.warning("⚠️ Nginx template not found. Skipping.")
        return

    with open(template_path, "r") as f:
        template = f.read()
    
    config = template.replace("${BACKEND_PORT}", str(ports['BACKEND_PORT'])) \
                     .replace("${FRONTEND_PORT}", str(ports['FRONTEND_PORT'])) \
                     .replace("${PROXY_PORT}", str(ports['PROXY_PORT'])) \
                     .replace("${BACKEND_HOST}", "global_backend") \
                     .replace("${FRONTEND_HOST}", "global_frontend")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(config)
    logging.info("✅ Generated nginx.conf.")

def setup_host_infrastructure():
    """Installs dependencies for Host-Only mode."""
    logging.info("🖥️ Setting up Host-Only Infrastructure...")
    
    # Check for Ollama
    if shutil.which("ollama"):
        logging.info("✅ Ollama detected.")
    else:
        logging.warning("⚠️ Ollama not found. Please install manually: curl -fsSL https://ollama.com/install.sh | sh")

    # Check for Redis
    if shutil.which("redis-server"):
        logging.info("✅ Redis detected.")
    else:
        logging.warning("⚠️ Redis not found. Please install manually: sudo apt install redis-server")

def main():
    logging.info(f"🚀 Genesis {VERSION} Initiated...")
    
    # 1. Calculate Ports
    ports = calculate_ports()
    
    # 2. Generate Configs
    generate_env_file(ports)
    generate_nginx_config(ports)
    
    # 3. Setup Infrastructure
    if shutil.which("docker"):
        logging.info("🐳 Docker detected. Ready for 'docker-compose up'.")
    else:
        setup_host_infrastructure()
        
    logging.info("✅ Genesis Complete. System Ready.")

if __name__ == "__main__":
    main()
