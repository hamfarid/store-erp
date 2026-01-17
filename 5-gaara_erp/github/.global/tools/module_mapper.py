#!/usr/bin/env python3
"""
Module Mapper
Automatically generates a complete module map for a project

Usage:
    python module_mapper.py /path/to/project
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
from datetime import datetime

class ModuleMapper:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        
        # Detect project structure
        self.has_frontend = (self.project_path / 'frontend').exists() or \
                           (self.project_path / 'src' / 'pages').exists() or \
                           (self.project_path / 'src' / 'components').exists()
        
        self.has_backend = (self.project_path / 'backend').exists() or \
                          (self.project_path / 'server').exists() or \
                          (self.project_path / 'api').exists()
        
        # Paths
        self.frontend_path = self._detect_frontend_path()
        self.backend_path = self._detect_backend_path()
        
        # Data storage
        self.modules = {
            'frontend': {
                'pages': [],
                'components': [],
                'services': [],
                'utils': [],
                'hooks': [],
                'contexts': []
            },
            'backend': {
                'routes': [],
                'controllers': [],
                'services': [],
                'models': [],
                'middleware': [],
                'validators': []
            },
            'database': {
                'migrations': [],
                'seeds': []
            }
        }
        
        self.dependencies = defaultdict(list)
        self.framework = self._detect_framework()
    
    def _detect_frontend_path(self) -> Path:
        """Detect frontend directory"""
        candidates = [
            self.project_path / 'frontend' / 'src',
            self.project_path / 'frontend',
            self.project_path / 'src',
            self.project_path / 'client' / 'src',
            self.project_path / 'client',
        ]
        
        for path in candidates:
            if path.exists():
                return path
        
        return None
    
    def _detect_backend_path(self) -> Path:
        """Detect backend directory"""
        candidates = [
            self.project_path / 'backend',
            self.project_path / 'server',
            self.project_path / 'api',
            self.project_path / 'src',
        ]
        
        for path in candidates:
            if path.exists() and (
                (path / 'controllers').exists() or
                (path / 'routes').exists() or
                (path / 'models').exists()
            ):
                return path
        
        return None
    
    def _detect_framework(self) -> Dict[str, str]:
        """Detect frameworks used"""
        frameworks = {
            'frontend': 'Unknown',
            'backend': 'Unknown'
        }
        
        # Check package.json for frontend
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    
                    if 'react' in deps:
                        frameworks['frontend'] = 'React'
                    elif 'vue' in deps:
                        frameworks['frontend'] = 'Vue'
                    elif '@angular/core' in deps:
                        frameworks['frontend'] = 'Angular'
                    elif 'svelte' in deps:
                        frameworks['frontend'] = 'Svelte'
                    
                    if 'express' in deps:
                        frameworks['backend'] = 'Express.js'
                    elif 'fastify' in deps:
                        frameworks['backend'] = 'Fastify'
                    elif 'koa' in deps:
                        frameworks['backend'] = 'Koa'
            except:
                pass
        
        # Check requirements.txt for backend
        requirements = self.project_path / 'requirements.txt'
        if requirements.exists():
            try:
                with open(requirements) as f:
                    content = f.read().lower()
                    if 'fastapi' in content:
                        frameworks['backend'] = 'FastAPI'
                    elif 'flask' in content:
                        frameworks['backend'] = 'Flask'
                    elif 'django' in content:
                        frameworks['backend'] = 'Django'
            except:
                pass
        
        return frameworks
    
    def scan_frontend(self):
        """Scan frontend modules"""
        if not self.frontend_path:
            return
        
        print("🔍 Scanning frontend modules...")
        
        # Scan pages
        pages_dirs = [
            self.frontend_path / 'pages',
            self.frontend_path / 'views',
            self.frontend_path / 'screens'
        ]
        
        for pages_dir in pages_dirs:
            if pages_dir.exists():
                for file_path in pages_dir.rglob('*.{jsx,js,tsx,ts,vue}'):
                    if file_path.is_file():
                        self.modules['frontend']['pages'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path)),
                            'imports': self._extract_imports(file_path)
                        })
        
        # Scan components
        components_dirs = [
            self.frontend_path / 'components',
            self.frontend_path / 'Components'
        ]
        
        for components_dir in components_dirs:
            if components_dir.exists():
                for file_path in components_dir.rglob('*.{jsx,js,tsx,ts,vue}'):
                    if file_path.is_file():
                        self.modules['frontend']['components'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path)),
                            'imports': self._extract_imports(file_path)
                        })
        
        # Scan services
        services_dirs = [
            self.frontend_path / 'services',
            self.frontend_path / 'api'
        ]
        
        for services_dir in services_dirs:
            if services_dir.exists():
                for file_path in services_dir.rglob('*.{js,ts}'):
                    if file_path.is_file():
                        self.modules['frontend']['services'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path)),
                            'functions': self._extract_functions(file_path)
                        })
        
        # Scan utils
        utils_dirs = [
            self.frontend_path / 'utils',
            self.frontend_path / 'helpers'
        ]
        
        for utils_dir in utils_dirs:
            if utils_dir.exists():
                for file_path in utils_dir.rglob('*.{js,ts}'):
                    if file_path.is_file():
                        self.modules['frontend']['utils'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path)),
                            'functions': self._extract_functions(file_path)
                        })
    
    def scan_backend(self):
        """Scan backend modules"""
        if not self.backend_path:
            return
        
        print("🔍 Scanning backend modules...")
        
        # Scan routes
        routes_dir = self.backend_path / 'routes'
        if routes_dir.exists():
            for file_path in routes_dir.rglob('*.{js,ts,py}'):
                if file_path.is_file():
                    self.modules['backend']['routes'].append({
                        'name': file_path.stem,
                        'path': str(file_path.relative_to(self.project_path)),
                        'endpoints': self._extract_endpoints(file_path)
                    })
        
        # Scan controllers
        controllers_dir = self.backend_path / 'controllers'
        if controllers_dir.exists():
            for file_path in controllers_dir.rglob('*.{js,ts,py}'):
                if file_path.is_file():
                    self.modules['backend']['controllers'].append({
                        'name': file_path.stem,
                        'path': str(file_path.relative_to(self.project_path)),
                        'methods': self._extract_functions(file_path)
                    })
        
        # Scan services
        services_dir = self.backend_path / 'services'
        if services_dir.exists():
            for file_path in services_dir.rglob('*.{js,ts,py}'):
                if file_path.is_file():
                    self.modules['backend']['services'].append({
                        'name': file_path.stem,
                        'path': str(file_path.relative_to(self.project_path)),
                        'methods': self._extract_functions(file_path)
                    })
        
        # Scan models
        models_dir = self.backend_path / 'models'
        if models_dir.exists():
            for file_path in models_dir.rglob('*.{js,ts,py}'):
                if file_path.is_file() and file_path.stem not in ['index', '__init__']:
                    self.modules['backend']['models'].append({
                        'name': file_path.stem,
                        'path': str(file_path.relative_to(self.project_path)),
                        'fields': []  # Could be extracted with more complex parsing
                    })
        
        # Scan middleware
        middleware_dirs = [
            self.backend_path / 'middleware',
            self.backend_path / 'middlewares'
        ]
        
        for middleware_dir in middleware_dirs:
            if middleware_dir.exists():
                for file_path in middleware_dir.rglob('*.{js,ts,py}'):
                    if file_path.is_file():
                        self.modules['backend']['middleware'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path))
                        })
    
    def scan_database(self):
        """Scan database modules"""
        print("🔍 Scanning database modules...")
        
        # Scan migrations
        migrations_dirs = [
            self.backend_path / 'migrations' if self.backend_path else None,
            self.project_path / 'migrations',
            self.project_path / 'database' / 'migrations'
        ]
        
        for migrations_dir in migrations_dirs:
            if migrations_dir and migrations_dir.exists():
                for file_path in migrations_dir.rglob('*.{js,ts,py,sql}'):
                    if file_path.is_file():
                        self.modules['database']['migrations'].append({
                            'name': file_path.stem,
                            'path': str(file_path.relative_to(self.project_path))
                        })
    
    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract import statements from file"""
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # JavaScript/TypeScript imports
                js_imports = re.findall(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]', content)
                imports.extend(js_imports)
                
                # Python imports
                py_imports = re.findall(r'from\s+(\S+)\s+import', content)
                imports.extend(py_imports)
                
        except:
            pass
        
        return imports
    
    def _extract_functions(self, file_path: Path) -> List[str]:
        """Extract function names from file"""
        functions = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # JavaScript/TypeScript functions
                js_functions = re.findall(r'(?:function|const|let|var)\s+(\w+)\s*[=\(]', content)
                functions.extend(js_functions)
                
                # Python functions
                py_functions = re.findall(r'def\s+(\w+)\s*\(', content)
                functions.extend(py_functions)
                
        except:
            pass
        
        return functions[:10]  # Limit to first 10
    
    def _extract_endpoints(self, file_path: Path) -> List[Dict]:
        """Extract API endpoints from routes file"""
        endpoints = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Express.js routes
                express_routes = re.findall(r'router\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]', content)
                for method, path in express_routes:
                    endpoints.append({'method': method.upper(), 'path': path})
                
                # FastAPI routes
                fastapi_routes = re.findall(r'@router\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]', content)
                for method, path in fastapi_routes:
                    endpoints.append({'method': method.upper(), 'path': path})
                
        except:
            pass
        
        return endpoints
    
    def generate_module_map(self) -> str:
        """Generate module map markdown"""
        lines = []
        
        # Header
        lines.append("# Module Map")
        lines.append("")
        lines.append(f"## Project: {self.project_name}")
        
        if self.has_frontend and self.has_backend:
            lines.append("**Type:** Full-Stack")
        elif self.has_frontend:
            lines.append("**Type:** Frontend")
        elif self.has_backend:
            lines.append("**Type:** Backend")
        
        lines.append(f"**Frontend Framework:** {self.framework['frontend']}")
        lines.append(f"**Backend Framework:** {self.framework['backend']}")
        lines.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("")
        
        # Frontend modules
        if self.has_frontend:
            lines.append("## Frontend Modules")
            lines.append("")
            
            if self.modules['frontend']['pages']:
                lines.append("### Pages")
                lines.append("")
                lines.append("| Page | Path | Imports |")
                lines.append("|------|------|---------|")
                for page in self.modules['frontend']['pages']:
                    imports = ', '.join(page['imports'][:3]) if page['imports'] else '-'
                    lines.append(f"| {page['name']} | `{page['path']}` | {imports} |")
                lines.append("")
            
            if self.modules['frontend']['components']:
                lines.append("### Components")
                lines.append("")
                lines.append("| Component | Path |")
                lines.append("|-----------|------|")
                for component in self.modules['frontend']['components']:
                    lines.append(f"| {component['name']} | `{component['path']}` |")
                lines.append("")
            
            if self.modules['frontend']['services']:
                lines.append("### Services")
                lines.append("")
                lines.append("| Service | Path | Functions |")
                lines.append("|---------|------|-----------|")
                for service in self.modules['frontend']['services']:
                    functions = ', '.join(service['functions'][:5]) if service['functions'] else '-'
                    lines.append(f"| {service['name']} | `{service['path']}` | {functions} |")
                lines.append("")
        
        # Backend modules
        if self.has_backend:
            lines.append("## Backend Modules")
            lines.append("")
            
            if self.modules['backend']['routes']:
                lines.append("### Routes")
                lines.append("")
                lines.append("| Route File | Path | Endpoints |")
                lines.append("|------------|------|-----------|")
                for route in self.modules['backend']['routes']:
                    endpoints = ', '.join([f"{ep['method']} {ep['path']}" for ep in route['endpoints'][:3]]) if route['endpoints'] else '-'
                    lines.append(f"| {route['name']} | `{route['path']}` | {endpoints} |")
                lines.append("")
            
            if self.modules['backend']['controllers']:
                lines.append("### Controllers")
                lines.append("")
                lines.append("| Controller | Path | Methods |")
                lines.append("|------------|------|---------|")
                for controller in self.modules['backend']['controllers']:
                    methods = ', '.join(controller['methods'][:5]) if controller['methods'] else '-'
                    lines.append(f"| {controller['name']} | `{controller['path']}` | {methods} |")
                lines.append("")
            
            if self.modules['backend']['models']:
                lines.append("### Models")
                lines.append("")
                lines.append("| Model | Path |")
                lines.append("|-------|------|")
                for model in self.modules['backend']['models']:
                    lines.append(f"| {model['name']} | `{model['path']}` |")
                lines.append("")
        
        # Database
        if self.modules['database']['migrations']:
            lines.append("## Database")
            lines.append("")
            lines.append("### Migrations")
            lines.append("")
            lines.append("| Migration | Path |")
            lines.append("|-----------|------|")
            for migration in self.modules['database']['migrations']:
                lines.append(f"| {migration['name']} | `{migration['path']}` |")
            lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Pages:** {len(self.modules['frontend']['pages'])}")
        lines.append(f"- **Total Components:** {len(self.modules['frontend']['components'])}")
        lines.append(f"- **Total Services (Frontend):** {len(self.modules['frontend']['services'])}")
        lines.append(f"- **Total Routes:** {len(self.modules['backend']['routes'])}")
        lines.append(f"- **Total Controllers:** {len(self.modules['backend']['controllers'])}")
        lines.append(f"- **Total Models:** {len(self.modules['backend']['models'])}")
        lines.append(f"- **Total Migrations:** {len(self.modules['database']['migrations'])}")
        lines.append("")
        
        return '\n'.join(lines)
    
    def save_module_map(self, output_file: str = None):
        """Save module map to file"""
        if output_file is None:
            output_file = self.project_path / 'docs' / 'MODULE_MAP.md'
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = self.generate_module_map()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n📄 Module map saved to: {output_path}")
        
        return output_path
    
    def run(self):
        """Run the complete module mapping process"""
        print("\n" + "="*80)
        print("MODULE MAPPER")
        print("="*80)
        print(f"Project: {self.project_path}")
        print(f"Frontend: {'Yes' if self.has_frontend else 'No'}")
        print(f"Backend: {'Yes' if self.has_backend else 'No'}")
        print("")
        
        self.scan_frontend()
        self.scan_backend()
        self.scan_database()
        
        self.save_module_map()
        
        print("\n✅ Module mapping complete!")
        print("="*80 + "\n")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python module_mapper.py /path/to/project")
        print("\nExample:")
        print("  python module_mapper.py /home/user/my-project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)
    
    mapper = ModuleMapper(project_path)
    mapper.run()

if __name__ == '__main__':
    main()

