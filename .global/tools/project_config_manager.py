#!/usr/bin/env python3
"""
Project Configuration Manager
Manages project configuration, state, and deployment workflow
"""

import json
import os
import sys
import secrets
import string
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ProjectConfigManager:
    """Manages project configuration and state"""
    
    CONFIG_DIR = ".global"
    CONFIG_FILE = "project_config.json"
    
    DEFAULT_CONFIG = {
        "project": {
            "name": "",
            "phase": "development",
            "deployed": False,
            "created_at": "",
            "updated_at": ""
        },
        "ports": {
            "frontend": 3000,
            "backend": 5000,
            "database": 5432
        },
        "database": {
            "name": "",
            "preserve_data": False,
            "add_sample_data": True,
            "type": "postgresql",
            "host": "localhost",
            "port": 5432
        },
        "environment": {
            "type": "local",
            "host": "localhost",
            "domain": None,
            "ip_address": None
        },
        "admin": {
            "username": "admin",
            "email": "",
            "password_hash": None,
            "created": False
        },
        "features": {
            "auto_backup": True,
            "logging": True,
            "monitoring": True
        }
    }
    
    def __init__(self, project_root: str = "."):
        """Initialize configuration manager"""
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / self.CONFIG_DIR
        self.config_path = self.config_dir / self.CONFIG_FILE
        
    def exists(self) -> bool:
        """Check if configuration file exists"""
        return self.config_path.exists()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.exists():
            return self.DEFAULT_CONFIG.copy()
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Update timestamp
        config['project']['updated_at'] = datetime.now().isoformat()
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def interactive_setup(self) -> Dict[str, Any]:
        """Interactive project setup questionnaire"""
        print("\n" + "="*64)
        print("           PROJECT CONFIGURATION QUESTIONNAIRE")
        print("="*64 + "\n")
        
        print("I need to collect some information about your project to provide")
        print("better assistance. Please answer the following questions:\n")
        
        config = self.DEFAULT_CONFIG.copy()
        
        # 1. Project Phase
        print("1. PROJECT PHASE")
        print("   " + "─"*60)
        print("   Are you in Development or Production phase?")
        print()
        print("   Options:")
        print("   [D] Development - Active development, testing, debugging")
        print("   [P] Production  - Live deployment, production environment")
        print()
        phase = input("   Your choice [D/P]: ").strip().upper()
        config['project']['phase'] = 'production' if phase == 'P' else 'development'
        
        # 2. Project Name
        print("\n2. PROJECT NAME")
        print("   " + "─"*60)
        print("   What is your project/application name?")
        print()
        print("   Example: \"MyAwesomeApp\", \"E-Commerce Platform\", \"Task Manager\"")
        print()
        project_name = input("   Project Name: ").strip()
        config['project']['name'] = project_name or "MyProject"
        
        # 3. Deployment Status
        print("\n3. DEPLOYMENT STATUS")
        print("   " + "─"*60)
        print("   Has this project been deployed before?")
        print()
        print("   Options:")
        print("   [Y] Yes - Already deployed to production")
        print("   [N] No  - First time deployment")
        print()
        deployed = input("   Your choice [Y/N]: ").strip().upper()
        config['project']['deployed'] = deployed == 'Y'
        
        # 4. Port Configuration
        print("\n4. PORT CONFIGURATION")
        print("   " + "─"*60)
        print()
        
        frontend_port = input("   a) Frontend Port [3000]: ").strip()
        config['ports']['frontend'] = int(frontend_port) if frontend_port else 3000
        
        backend_port = input("   b) Backend/API Port [5000]: ").strip()
        config['ports']['backend'] = int(backend_port) if backend_port else 5000
        
        db_port = input("   c) Database Port [5432]: ").strip()
        config['ports']['database'] = int(db_port) if db_port else 5432
        config['database']['port'] = config['ports']['database']
        
        # 5. Database Configuration
        print("\n5. DATABASE CONFIGURATION")
        print("   " + "─"*60)
        print()
        
        db_name = input("   a) Database Name: ").strip()
        config['database']['name'] = db_name or f"{config['project']['name'].lower().replace(' ', '_')}_db"
        
        preserve = input("   b) Preserve existing database data? [Y/N]: ").strip().upper()
        config['database']['preserve_data'] = preserve == 'Y'
        
        if config['project']['phase'] == 'development':
            sample_data = input("   c) Add test/sample data? [Y/N]: ").strip().upper()
            config['database']['add_sample_data'] = sample_data == 'Y'
        
        # 6. Environment
        print("\n6. ENVIRONMENT")
        print("   " + "─"*60)
        print("   Where will this run?")
        print()
        print("   Options:")
        print("   [L] Local    - localhost, 127.0.0.1")
        print("   [E] External - Custom domain, cloud server")
        print()
        env_type = input("   Your choice [L/E]: ").strip().upper()
        config['environment']['type'] = 'external' if env_type == 'E' else 'local'
        
        if config['environment']['type'] == 'external':
            domain = input("   Host/Domain: ").strip()
            config['environment']['domain'] = domain
            config['environment']['host'] = domain
            
            ip = input("   IP Address (optional): ").strip()
            if ip:
                config['environment']['ip_address'] = ip
        
        # 7. Admin User (Production only)
        if config['project']['phase'] == 'production':
            print("\n7. ADMIN USER")
            print("   " + "─"*60)
            print()
            
            admin_username = input("   a) Admin Username [admin]: ").strip()
            config['admin']['username'] = admin_username or "admin"
            
            admin_email = input("   b) Admin Email: ").strip()
            config['admin']['email'] = admin_email
            
            print("   c) Admin Password: (Will be generated securely if not provided)")
            admin_password = input("   Password (optional): ").strip()
            if admin_password:
                # In real implementation, hash the password
                config['admin']['password_hash'] = f"hashed_{admin_password}"
        
        # Set creation timestamp
        config['project']['created_at'] = datetime.now().isoformat()
        config['project']['updated_at'] = config['project']['created_at']
        
        # Display summary
        self.display_summary(config)
        
        # Save configuration
        self.save(config)
        
        print(f"\n✓ Configuration saved to: {self.config_path}")
        
        return config
    
    def display_summary(self, config: Dict[str, Any]) -> None:
        """Display configuration summary"""
        print("\n" + "="*64)
        print("                    CONFIGURATION SUMMARY")
        print("="*64 + "\n")
        
        print(f"Project Name:     {config['project']['name']}")
        print(f"Phase:            {config['project']['phase'].upper()}")
        print(f"Deployed:         {'Yes' if config['project']['deployed'] else 'No'}")
        print()
        print(f"Frontend Port:    {config['ports']['frontend']}")
        print(f"Backend Port:     {config['ports']['backend']}")
        print(f"Database Port:    {config['ports']['database']}")
        print()
        print(f"Database Name:    {config['database']['name']}")
        print(f"Preserve Data:    {'Yes' if config['database']['preserve_data'] else 'No'}")
        if config['project']['phase'] == 'development':
            print(f"Sample Data:      {'Yes' if config['database']['add_sample_data'] else 'No'}")
        print()
        print(f"Environment:      {config['environment']['type'].upper()}")
        print(f"Host:             {config['environment']['host']}")
        if config['environment'].get('domain'):
            print(f"Domain:           {config['environment']['domain']}")
        print()
        if config['project']['phase'] == 'production':
            print(f"Admin Username:   {config['admin']['username']}")
            print(f"Admin Email:      {config['admin']['email']}")
        
        print("\n" + "="*64 + "\n")
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def transition_to_production(self) -> bool:
        """Transition project from development to production"""
        config = self.load()
        
        if config['project']['phase'] == 'production':
            print("⚠️  Project is already in production phase.")
            return False
        
        print("\n" + "="*64)
        print("           TRANSITIONING TO PRODUCTION")
        print("="*64 + "\n")
        
        print("⚠️  WARNING: This will transition your project to PRODUCTION mode.\n")
        print("Current configuration:")
        print(f"  - Project: {config['project']['name']}")
        print(f"  - Database: {config['database']['name']}")
        print(f"  - Frontend: http://{config['environment']['host']}:{config['ports']['frontend']}")
        print(f"  - Backend: http://{config['environment']['host']}:{config['ports']['backend']}")
        print()
        
        confirm = input("Are you sure you want to proceed? [Y/n]: ").strip().upper()
        if confirm != 'Y':
            print("❌ Deployment cancelled.")
            return False
        
        # Update configuration
        config['project']['phase'] = 'production'
        config['project']['deployed'] = True
        config['database']['preserve_data'] = True
        config['database']['add_sample_data'] = False
        
        # Generate admin password if not set
        if not config['admin']['password_hash']:
            password = self.generate_secure_password()
            config['admin']['password_hash'] = f"hashed_{password}"
            print(f"\n✓ Generated admin password: {password}")
            print("⚠️  IMPORTANT: Save this password securely!")
        
        # Save updated configuration
        self.save(config)
        
        print("\n✓ Project phase updated: PRODUCTION")
        
        return True
    
    def get_env_file_content(self, config: Dict[str, Any]) -> str:
        """Generate .env file content from configuration"""
        return f"""# Project Configuration
# Generated by Global Guidelines v4.0.0

# Project
PROJECT_NAME={config['project']['name']}
PROJECT_PHASE={config['project']['phase']}

# Ports
FRONTEND_PORT={config['ports']['frontend']}
BACKEND_PORT={config['ports']['backend']}
DATABASE_PORT={config['ports']['database']}

# Database
DATABASE_NAME={config['database']['name']}
DATABASE_HOST={config['database']['host']}
DATABASE_PORT={config['database']['port']}
DATABASE_TYPE={config['database']['type']}

# Environment
ENVIRONMENT_TYPE={config['environment']['type']}
HOST={config['environment']['host']}
DOMAIN={config['environment'].get('domain', '')}

# URLs
FRONTEND_URL=http://{config['environment']['host']}:{config['ports']['frontend']}
BACKEND_URL=http://{config['environment']['host']}:{config['ports']['backend']}

# Admin
ADMIN_USERNAME={config['admin']['username']}
ADMIN_EMAIL={config['admin']['email']}

# Features
AUTO_BACKUP={'true' if config['features']['auto_backup'] else 'false'}
LOGGING={'true' if config['features']['logging'] else 'false'}
MONITORING={'true' if config['features']['monitoring'] else 'false'}

# Security (set these manually)
SECRET_KEY=your-secret-key-here
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
"""


def main():
    """Main entry point"""
    manager = ProjectConfigManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            config = manager.interactive_setup()
            
        elif command == "deploy":
            if manager.transition_to_production():
                config = manager.load()
                print("\n🎉 Deployment successful!")
                print(f"\nAdmin Panel: http://{config['environment']['host']}:{config['ports']['backend']}/admin")
                print(f"Setup Wizard: http://{config['environment']['host']}:{config['ports']['frontend']}/setup")
            
        elif command == "show":
            if manager.exists():
                config = manager.load()
                manager.display_summary(config)
            else:
                print("❌ No configuration found. Run 'setup' first.")
        
        elif command == "env":
            if manager.exists():
                config = manager.load()
                env_content = manager.get_env_file_content(config)
                
                env_path = manager.project_root / ".env"
                with open(env_path, 'w') as f:
                    f.write(env_content)
                
                print(f"✓ .env file created: {env_path}")
            else:
                print("❌ No configuration found. Run 'setup' first.")
        
        else:
            print(f"❌ Unknown command: {command}")
            print("\nUsage:")
            print("  python project_config_manager.py setup   - Interactive setup")
            print("  python project_config_manager.py deploy  - Deploy to production")
            print("  python project_config_manager.py show    - Show current config")
            print("  python project_config_manager.py env     - Generate .env file")
    
    else:
        # No command, check if config exists
        if manager.exists():
            config = manager.load()
            print(f"✓ Configuration loaded: {config['project']['name']}")
            print(f"  Phase: {config['project']['phase']}")
        else:
            print("No configuration found.")
            print("Run: python project_config_manager.py setup")


if __name__ == "__main__":
    main()

