#!/usr/bin/env python3
"""
Project Analyzer
Reads existing projects and generates project-specific configuration and prompts
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class ProjectAnalyzer:
    """Analyzes existing projects and generates configuration"""
    
    def __init__(self, project_root: str):
        """Initialize analyzer"""
        self.project_root = Path(project_root)
        self.analysis = {
            "project": {},
            "structure": {},
            "technologies": {},
            "dependencies": {},
            "database": {},
            "api": {},
            "frontend": {},
            "backend": {},
            "recommendations": []
        }
        
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis"""
        print("🔍 Analyzing project...")
        
        self.detect_project_info()
        self.analyze_structure()
        self.detect_technologies()
        self.analyze_dependencies()
        self.detect_database()
        self.detect_api_endpoints()
        self.analyze_frontend()
        self.analyze_backend()
        self.generate_recommendations()
        
        return self.analysis
    
    def detect_project_info(self):
        """Detect basic project information"""
        print("  📋 Detecting project info...")
        
        # Try to get project name from various sources
        project_name = self.project_root.name
        
        # Check package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                project_name = data.get("name", project_name)
                self.analysis["project"]["description"] = data.get("description", "")
                self.analysis["project"]["version"] = data.get("version", "")
        
        # Check setup.py or pyproject.toml
        setup_py = self.project_root / "setup.py"
        pyproject_toml = self.project_root / "pyproject.toml"
        
        if setup_py.exists():
            # Parse setup.py (simplified)
            with open(setup_py) as f:
                content = f.read()
                if 'name=' in content:
                    # Extract name
                    pass
        
        self.analysis["project"]["name"] = project_name
        self.analysis["project"]["root"] = str(self.project_root)
        
    def analyze_structure(self):
        """Analyze project structure"""
        print("  📁 Analyzing structure...")
        
        structure = {
            "directories": [],
            "files": [],
            "has_frontend": False,
            "has_backend": False,
            "has_database": False,
            "has_tests": False,
            "has_docs": False
        }
        
        # Common directory patterns
        frontend_dirs = ["frontend", "client", "web", "ui", "src/components", "src/pages"]
        backend_dirs = ["backend", "server", "api", "src/routes", "src/controllers"]
        test_dirs = ["tests", "test", "__tests__", "spec"]
        docs_dirs = ["docs", "documentation", "doc"]
        
        for item in self.project_root.rglob("*"):
            if item.is_dir() and not any(p in str(item) for p in [".git", "node_modules", "__pycache__", "venv"]):
                rel_path = str(item.relative_to(self.project_root))
                structure["directories"].append(rel_path)
                
                # Check for frontend
                if any(d in rel_path.lower() for d in frontend_dirs):
                    structure["has_frontend"] = True
                
                # Check for backend
                if any(d in rel_path.lower() for d in backend_dirs):
                    structure["has_backend"] = True
                
                # Check for tests
                if any(d in rel_path.lower() for d in test_dirs):
                    structure["has_tests"] = True
                
                # Check for docs
                if any(d in rel_path.lower() for d in docs_dirs):
                    structure["has_docs"] = True
        
        self.analysis["structure"] = structure
        
    def detect_technologies(self):
        """Detect technologies used"""
        print("  🔧 Detecting technologies...")
        
        tech = {
            "frontend": [],
            "backend": [],
            "database": [],
            "tools": []
        }
        
        # Check package.json for frontend
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                
                if "react" in deps:
                    tech["frontend"].append("React")
                if "vue" in deps:
                    tech["frontend"].append("Vue")
                if "angular" in deps or "@angular/core" in deps:
                    tech["frontend"].append("Angular")
                if "next" in deps:
                    tech["frontend"].append("Next.js")
                if "express" in deps:
                    tech["backend"].append("Express.js")
        
        # Check requirements.txt or Pipfile for backend
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            with open(requirements) as f:
                content = f.read().lower()
                if "django" in content:
                    tech["backend"].append("Django")
                if "flask" in content:
                    tech["backend"].append("Flask")
                if "fastapi" in content:
                    tech["backend"].append("FastAPI")
                if "sqlalchemy" in content:
                    tech["database"].append("SQLAlchemy")
                if "psycopg2" in content or "psycopg" in content:
                    tech["database"].append("PostgreSQL")
                if "pymongo" in content:
                    tech["database"].append("MongoDB")
                if "mysql" in content:
                    tech["database"].append("MySQL")
        
        # Check for Docker
        if (self.project_root / "Dockerfile").exists():
            tech["tools"].append("Docker")
        if (self.project_root / "docker-compose.yml").exists():
            tech["tools"].append("Docker Compose")
        
        # Check for Git
        if (self.project_root / ".git").exists():
            tech["tools"].append("Git")
        
        self.analysis["technologies"] = tech
        
    def analyze_dependencies(self):
        """Analyze project dependencies"""
        print("  📦 Analyzing dependencies...")
        
        deps = {
            "frontend": {},
            "backend": {},
            "total": 0
        }
        
        # Frontend dependencies
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                deps["frontend"] = {
                    **data.get("dependencies", {}),
                    **data.get("devDependencies", {})
                }
                deps["total"] += len(deps["frontend"])
        
        # Backend dependencies
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            with open(requirements) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "==" in line:
                            name, version = line.split("==", 1)
                            deps["backend"][name.strip()] = version.strip()
                        else:
                            deps["backend"][line] = "latest"
                deps["total"] += len(deps["backend"])
        
        self.analysis["dependencies"] = deps
        
    def detect_database(self):
        """Detect database configuration"""
        print("  🗄️  Detecting database...")
        
        db = {
            "type": None,
            "detected": False,
            "config_files": []
        }
        
        # Check for database config files
        config_files = [
            "config/database.py",
            "config/db.py",
            "database.py",
            "db.py",
            "models.py",
            "settings.py"
        ]
        
        for config_file in config_files:
            path = self.project_root / config_file
            if path.exists():
                db["config_files"].append(config_file)
                db["detected"] = True
                
                # Try to detect database type
                with open(path) as f:
                    content = f.read().lower()
                    if "postgresql" in content or "psycopg" in content:
                        db["type"] = "PostgreSQL"
                    elif "mysql" in content:
                        db["type"] = "MySQL"
                    elif "mongodb" in content or "pymongo" in content:
                        db["type"] = "MongoDB"
                    elif "sqlite" in content:
                        db["type"] = "SQLite"
        
        # Check docker-compose.yml
        docker_compose = self.project_root / "docker-compose.yml"
        if docker_compose.exists():
            with open(docker_compose) as f:
                content = f.read().lower()
                if "postgres" in content:
                    db["type"] = "PostgreSQL"
                elif "mysql" in content:
                    db["type"] = "MySQL"
                elif "mongodb" in content or "mongo:" in content:
                    db["type"] = "MongoDB"
        
        self.analysis["database"] = db
        
    def detect_api_endpoints(self):
        """Detect API endpoints"""
        print("  🌐 Detecting API endpoints...")
        
        api = {
            "detected": False,
            "endpoints": [],
            "route_files": []
        }
        
        # Look for route files
        route_patterns = [
            "**/routes.py",
            "**/urls.py",
            "**/api.py",
            "**/routes/*.py",
            "**/api/*.py"
        ]
        
        for pattern in route_patterns:
            for file in self.project_root.glob(pattern):
                if "__pycache__" not in str(file):
                    api["route_files"].append(str(file.relative_to(self.project_root)))
                    api["detected"] = True
        
        self.analysis["api"] = api
        
    def analyze_frontend(self):
        """Analyze frontend"""
        print("  🎨 Analyzing frontend...")
        
        frontend = {
            "detected": False,
            "framework": None,
            "components": [],
            "pages": []
        }
        
        # Check for frontend framework
        package_json = self.project_root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                
                if "react" in deps:
                    frontend["framework"] = "React"
                    frontend["detected"] = True
                elif "vue" in deps:
                    frontend["framework"] = "Vue"
                    frontend["detected"] = True
                elif "angular" in deps or "@angular/core" in deps:
                    frontend["framework"] = "Angular"
                    frontend["detected"] = True
        
        # Look for components
        component_dirs = [
            "src/components",
            "components",
            "frontend/components",
            "client/components"
        ]
        
        for comp_dir in component_dirs:
            path = self.project_root / comp_dir
            if path.exists():
                for file in path.rglob("*"):
                    if file.is_file() and file.suffix in [".js", ".jsx", ".ts", ".tsx", ".vue"]:
                        frontend["components"].append(str(file.relative_to(self.project_root)))
        
        # Look for pages
        page_dirs = [
            "src/pages",
            "pages",
            "frontend/pages",
            "client/pages"
        ]
        
        for page_dir in page_dirs:
            path = self.project_root / page_dir
            if path.exists():
                for file in path.rglob("*"):
                    if file.is_file() and file.suffix in [".js", ".jsx", ".ts", ".tsx", ".vue"]:
                        frontend["pages"].append(str(file.relative_to(self.project_root)))
        
        self.analysis["frontend"] = frontend
        
    def analyze_backend(self):
        """Analyze backend"""
        print("  ⚙️  Analyzing backend...")
        
        backend = {
            "detected": False,
            "framework": None,
            "models": [],
            "views": [],
            "controllers": []
        }
        
        # Detect framework
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            with open(requirements) as f:
                content = f.read().lower()
                if "django" in content:
                    backend["framework"] = "Django"
                    backend["detected"] = True
                elif "flask" in content:
                    backend["framework"] = "Flask"
                    backend["detected"] = True
                elif "fastapi" in content:
                    backend["framework"] = "FastAPI"
                    backend["detected"] = True
        
        # Look for models
        for file in self.project_root.rglob("models.py"):
            if "__pycache__" not in str(file):
                backend["models"].append(str(file.relative_to(self.project_root)))
        
        # Look for views
        for file in self.project_root.rglob("views.py"):
            if "__pycache__" not in str(file):
                backend["views"].append(str(file.relative_to(self.project_root)))
        
        # Look for controllers
        for file in self.project_root.rglob("controllers.py"):
            if "__pycache__" not in str(file):
                backend["controllers"].append(str(file.relative_to(self.project_root)))
        
        self.analysis["backend"] = backend
        
    def generate_recommendations(self):
        """Generate recommendations"""
        print("  💡 Generating recommendations...")
        
        recs = []
        
        # Check for missing documentation
        if not self.analysis["structure"]["has_docs"]:
            recs.append({
                "type": "documentation",
                "priority": "high",
                "message": "No documentation directory found. Consider adding docs/"
            })
        
        # Check for missing tests
        if not self.analysis["structure"]["has_tests"]:
            recs.append({
                "type": "testing",
                "priority": "high",
                "message": "No tests directory found. Consider adding tests/"
            })
        
        # Check for Docker
        if "Docker" not in self.analysis["technologies"]["tools"]:
            recs.append({
                "type": "deployment",
                "priority": "medium",
                "message": "No Docker configuration found. Consider adding Dockerfile and docker-compose.yml"
            })
        
        # Check for .gitignore
        if not (self.project_root / ".gitignore").exists():
            recs.append({
                "type": "version_control",
                "priority": "high",
                "message": "No .gitignore found. Consider adding one"
            })
        
        # Check for README
        if not (self.project_root / "README.md").exists():
            recs.append({
                "type": "documentation",
                "priority": "high",
                "message": "No README.md found. Consider adding project documentation"
            })
        
        self.analysis["recommendations"] = recs
        
    def generate_config(self) -> Dict[str, Any]:
        """Generate project configuration"""
        print("\n📝 Generating configuration...")
        
        config = {
            "project": {
                "name": self.analysis["project"]["name"],
                "phase": "development",  # Default to development
                "deployed": False,
                "created_at": "",
                "updated_at": ""
            },
            "ports": {
                "frontend": 3000,
                "backend": 5000,
                "database": 5432 if self.analysis["database"]["type"] == "PostgreSQL" else 3306
            },
            "database": {
                "name": f"{self.analysis['project']['name'].lower().replace(' ', '_')}_db",
                "preserve_data": False,
                "add_sample_data": True,
                "type": self.analysis["database"]["type"].lower() if self.analysis["database"]["type"] else "postgresql",
                "host": "localhost",
                "port": 5432 if self.analysis["database"]["type"] == "PostgreSQL" else 3306
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
            },
            "detected": {
                "frontend_framework": self.analysis["frontend"]["framework"],
                "backend_framework": self.analysis["backend"]["framework"],
                "database_type": self.analysis["database"]["type"],
                "has_tests": self.analysis["structure"]["has_tests"],
                "has_docs": self.analysis["structure"]["has_docs"]
            }
        }
        
        return config
        
    def generate_prompt_additions(self) -> str:
        """Generate project-specific prompt additions"""
        print("\n📄 Generating project-specific prompt...")
        
        prompt = f"""
## Project-Specific Configuration

### Project: {self.analysis['project']['name']}

**Auto-detected information:**

#### Technologies
- **Frontend:** {', '.join(self.analysis['technologies']['frontend']) or 'Not detected'}
- **Backend:** {', '.join(self.analysis['technologies']['backend']) or 'Not detected'}
- **Database:** {', '.join(self.analysis['technologies']['database']) or 'Not detected'}
- **Tools:** {', '.join(self.analysis['technologies']['tools']) or 'Not detected'}

#### Structure
- Frontend detected: {'Yes' if self.analysis['structure']['has_frontend'] else 'No'}
- Backend detected: {'Yes' if self.analysis['structure']['has_backend'] else 'No'}
- Tests found: {'Yes' if self.analysis['structure']['has_tests'] else 'No'}
- Documentation found: {'Yes' if self.analysis['structure']['has_docs'] else 'No'}

#### Frontend
- Framework: {self.analysis['frontend']['framework'] or 'Not detected'}
- Components: {len(self.analysis['frontend']['components'])} found
- Pages: {len(self.analysis['frontend']['pages'])} found

#### Backend
- Framework: {self.analysis['backend']['framework'] or 'Not detected'}
- Models: {len(self.analysis['backend']['models'])} found
- Views: {len(self.analysis['backend']['views'])} found

#### Database
- Type: {self.analysis['database']['type'] or 'Not detected'}
- Config files: {', '.join(self.analysis['database']['config_files']) or 'None'}

#### Dependencies
- Total: {self.analysis['dependencies']['total']}
- Frontend: {len(self.analysis['dependencies']['frontend'])}
- Backend: {len(self.analysis['dependencies']['backend'])}

#### Recommendations
"""
        
        for rec in self.analysis["recommendations"]:
            prompt += f"\n- [{rec['priority'].upper()}] {rec['message']}"
        
        prompt += "\n\n**Use this information to provide context-aware assistance.**\n"
        
        return prompt
        
    def save_analysis(self, output_dir: str = ".global"):
        """Save analysis results"""
        output_path = self.project_root / output_dir
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save full analysis
        analysis_file = output_path / "project_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        print(f"\n✅ Analysis saved to: {analysis_file}")
        
        # Save configuration
        config = self.generate_config()
        config_file = output_path / "project_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to: {config_file}")
        
        # Save prompt additions
        prompt_additions = self.generate_prompt_additions()
        prompt_file = output_path / "project_prompt_additions.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt_additions)
        print(f"✅ Prompt additions saved to: {prompt_file}")
        
        return {
            "analysis": str(analysis_file),
            "config": str(config_file),
            "prompt": str(prompt_file)
        }


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python project_analyzer.py <project_path>")
        print("\nExample:")
        print("  python project_analyzer.py /path/to/project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)
    
    print("="*60)
    print("PROJECT ANALYZER")
    print("="*60)
    print(f"\nProject: {project_path}\n")
    
    analyzer = ProjectAnalyzer(project_path)
    analysis = analyzer.analyze()
    files = analyzer.save_analysis()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"\nProject: {analysis['project']['name']}")
    print(f"Frontend: {analysis['frontend']['framework'] or 'Not detected'}")
    print(f"Backend: {analysis['backend']['framework'] or 'Not detected'}")
    print(f"Database: {analysis['database']['type'] or 'Not detected'}")
    print(f"\nRecommendations: {len(analysis['recommendations'])}")
    for rec in analysis['recommendations']:
        print(f"  - [{rec['priority'].upper()}] {rec['message']}")
    
    print("\n" + "="*60)
    print("FILES GENERATED")
    print("="*60)
    for name, path in files.items():
        print(f"  {name}: {path}")
    
    print("\n✅ Done! Use the generated files with Augment.")


if __name__ == "__main__":
    main()

