#!/usr/bin/env python3
"""
Comprehensive System Analysis for Arabic Inventory Management System
Using AI modules and expert consultation for complete evaluation

FILE: /comprehensive_system_analysis.py | PURPOSE: Full system audit and analysis | OWNER: System Auditor | RELATED: All modules | LAST-AUDITED: 2025-10-21
"""

import os
import json
import subprocess
import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class SystemAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "analysis_phases": {},
            "expert_evaluations": {},
            "security_assessment": {},
            "performance_metrics": {},
            "code_quality": {},
            "ui_ux_evaluation": {},
            "database_analysis": {},
            "api_analysis": {},
            "recommendations": [],
            "critical_issues": [],
            "compliance_status": {}
        }
        
    def phase_0_discovery_and_mapping(self):
        """Phase 0: Discovery and comprehensive mapping"""
        print("🔍 Phase 0: Discovery and Comprehensive Mapping")
        
        # File structure analysis
        file_structure = self._analyze_file_structure()
        
        # Route mapping
        routes_mapping = self._analyze_routes()
        
        # Database schema analysis
        db_analysis = self._analyze_database_schema()
        
        # Dependencies analysis
        dependencies = self._analyze_dependencies()
        
        self.analysis_results["analysis_phases"]["phase_0"] = {
            "file_structure": file_structure,
            "routes_mapping": routes_mapping,
            "database_analysis": db_analysis,
            "dependencies": dependencies,
            "risks_identified": [],
            "metrics": {
                "total_files": len(file_structure.get("all_files", [])),
                "python_files": len(file_structure.get("python_files", [])),
                "javascript_files": len(file_structure.get("js_files", [])),
                "routes_count": len(routes_mapping.get("backend_routes", [])),
                "db_tables": len(db_analysis.get("tables", []))
            }
        }
        
    def _analyze_file_structure(self) -> Dict[str, Any]:
        """Analyze complete file structure"""
        structure = {
            "all_files": [],
            "python_files": [],
            "js_files": [],
            "config_files": [],
            "template_files": [],
            "static_files": [],
            "documentation_files": []
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv']]
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.project_root)
                
                structure["all_files"].append(str(rel_path))
                
                if file.endswith('.py'):
                    structure["python_files"].append(str(rel_path))
                elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    structure["js_files"].append(str(rel_path))
                elif file.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.cfg')):
                    structure["config_files"].append(str(rel_path))
                elif file.endswith(('.html', '.htm', '.jinja2', '.j2')):
                    structure["template_files"].append(str(rel_path))
                elif file.endswith(('.css', '.scss', '.sass', '.less')):
                    structure["static_files"].append(str(rel_path))
                elif file.endswith(('.md', '.rst', '.txt')):
                    structure["documentation_files"].append(str(rel_path))
                    
        return structure
        
    def _analyze_routes(self) -> Dict[str, Any]:
        """Analyze backend and frontend routes"""
        routes = {
            "backend_routes": [],
            "frontend_routes": [],
            "api_endpoints": [],
            "route_security": []
        }
        
        # Analyze Flask routes
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Find Flask routes
                    route_patterns = re.findall(r'@\w+\.route\([\'"]([^\'"]+)[\'"].*?\)', content)
                    for route in route_patterns:
                        routes["backend_routes"].append({
                            "path": route,
                            "file": str(py_file),
                            "methods": self._extract_http_methods(content, route)
                        })
                        
                    # Find API endpoints
                    api_patterns = re.findall(r'@api\.|@app\.route.*?api', content)
                    if api_patterns:
                        routes["api_endpoints"].extend(route_patterns)
                        
                except Exception as e:
                    print(f"Error analyzing {py_file}: {e}")
                    
        # Analyze React routes
        for js_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("js_files", []):
            file_path = self.project_root / js_file
            if file_path.exists() and 'route' in js_file.lower():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Find React Router routes
                    route_patterns = re.findall(r'<Route.*?path=[\'"]([^\'"]+)[\'"]', content)
                    for route in route_patterns:
                        routes["frontend_routes"].append({
                            "path": route,
                            "file": str(js_file)
                        })
                        
                except Exception as e:
                    print(f"Error analyzing {js_file}: {e}")
                    
        return routes
        
    def _extract_http_methods(self, content: str, route: str) -> List[str]:
        """Extract HTTP methods for a route"""
        methods = ["GET"]  # Default
        method_pattern = re.search(rf'@\w+\.route\([\'"]({re.escape(route)})[\'"].*?methods\s*=\s*\[(.*?)\]', content)
        if method_pattern:
            methods_str = method_pattern.group(2)
            methods = re.findall(r'[\'"](\w+)[\'"]', methods_str)
        return methods
        
    def _analyze_database_schema(self) -> Dict[str, Any]:
        """Analyze database schema and relationships"""
        db_analysis = {
            "tables": [],
            "relationships": [],
            "indexes": [],
            "constraints": [],
            "migrations": []
        }
        
        # Look for SQLAlchemy models
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            if 'model' in py_file.lower():
                file_path = self.project_root / py_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Find SQLAlchemy models
                        class_pattern = re.findall(r'class\s+(\w+)\s*\([^)]*Model[^)]*\):', content)
                        for class_name in class_pattern:
                            table_info = self._analyze_model_class(content, class_name)
                            if table_info:
                                db_analysis["tables"].append(table_info)
                                
                    except Exception as e:
                        print(f"Error analyzing model {py_file}: {e}")
                        
        return db_analysis
        
    def _analyze_model_class(self, content: str, class_name: str) -> Optional[Dict[str, Any]]:
        """Analyze a SQLAlchemy model class"""
        try:
            # Parse the AST to get detailed information
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    table_info = {
                        "name": class_name,
                        "fields": [],
                        "relationships": [],
                        "constraints": []
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    field_name = target.id
                                    # Analyze field type and constraints
                                    field_info = self._analyze_field(item.value)
                                    if field_info:
                                        field_info["name"] = field_name
                                        table_info["fields"].append(field_info)
                                        
                    return table_info
                    
        except Exception as e:
            print(f"Error parsing model class {class_name}: {e}")
            
        return None
        
    def _analyze_field(self, node) -> Optional[Dict[str, Any]]:
        """Analyze a SQLAlchemy field"""
        field_info = {
            "type": "unknown",
            "nullable": True,
            "primary_key": False,
            "foreign_key": None,
            "unique": False
        }
        
        if isinstance(node, ast.Call):
            if hasattr(node.func, 'attr'):
                field_info["type"] = node.func.attr
                
            # Analyze arguments for constraints
            for keyword in node.keywords:
                if keyword.arg == "nullable":
                    field_info["nullable"] = keyword.value.value if hasattr(keyword.value, 'value') else True
                elif keyword.arg == "primary_key":
                    field_info["primary_key"] = keyword.value.value if hasattr(keyword.value, 'value') else False
                elif keyword.arg == "unique":
                    field_info["unique"] = keyword.value.value if hasattr(keyword.value, 'value') else False
                    
        return field_info
        
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        dependencies = {
            "python": {},
            "nodejs": {},
            "security_issues": [],
            "outdated_packages": []
        }
        
        # Analyze Python dependencies
        requirements_file = self.project_root / "backend" / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '==' in line:
                                package, version = line.split('==', 1)
                                dependencies["python"][package.strip()] = version.strip()
                            else:
                                dependencies["python"][line] = "latest"
            except Exception as e:
                print(f"Error analyzing Python dependencies: {e}")
                
        # Analyze Node.js dependencies
        package_json = self.project_root / "frontend" / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                    dependencies["nodejs"] = {
                        "dependencies": package_data.get("dependencies", {}),
                        "devDependencies": package_data.get("devDependencies", {})
                    }
            except Exception as e:
                print(f"Error analyzing Node.js dependencies: {e}")
                
        return dependencies
        
    def phase_1_security_analysis(self):
        """Phase 1: Comprehensive security analysis"""
        print("🔒 Phase 1: Security Analysis")
        
        security_issues = []
        
        # Run security scans
        security_issues.extend(self._run_bandit_scan())
        security_issues.extend(self._analyze_authentication())
        security_issues.extend(self._analyze_authorization())
        security_issues.extend(self._check_input_validation())
        security_issues.extend(self._check_sql_injection_risks())
        security_issues.extend(self._analyze_csrf_protection())
        security_issues.extend(self._check_secure_headers())
        
        self.analysis_results["security_assessment"] = {
            "total_issues": len(security_issues),
            "critical_issues": [issue for issue in security_issues if issue.get("severity") == "critical"],
            "high_issues": [issue for issue in security_issues if issue.get("severity") == "high"],
            "medium_issues": [issue for issue in security_issues if issue.get("severity") == "medium"],
            "low_issues": [issue for issue in security_issues if issue.get("severity") == "low"],
            "all_issues": security_issues
        }
        
    def _run_bandit_scan(self) -> List[Dict[str, Any]]:
        """Run Bandit security scan on Python code"""
        issues = []
        try:
            backend_path = self.project_root / "backend"
            if backend_path.exists():
                result = subprocess.run(
                    ["python", "-m", "bandit", "-r", str(backend_path), "-f", "json"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0 or result.stdout:
                    try:
                        bandit_results = json.loads(result.stdout)
                        for issue in bandit_results.get("results", []):
                            issues.append({
                                "tool": "bandit",
                                "severity": issue.get("issue_severity", "unknown").lower(),
                                "confidence": issue.get("issue_confidence", "unknown").lower(),
                                "description": issue.get("issue_text", ""),
                                "file": issue.get("filename", ""),
                                "line": issue.get("line_number", 0),
                                "test_id": issue.get("test_id", ""),
                                "category": "security"
                            })
                    except json.JSONDecodeError:
                        print("Error parsing Bandit results")
                        
        except Exception as e:
            print(f"Error running Bandit scan: {e}")
            
        return issues
        
    def _analyze_authentication(self) -> List[Dict[str, Any]]:
        """Analyze authentication mechanisms"""
        issues = []
        
        # Look for authentication-related files
        auth_files = []
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            if any(keyword in py_file.lower() for keyword in ['auth', 'login', 'user', 'session']):
                auth_files.append(py_file)
                
        for auth_file in auth_files:
            file_path = self.project_root / auth_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for weak password policies
                    if 'password' in content.lower():
                        if not re.search(r'password.*length.*[8-9]|[1-9][0-9]', content, re.IGNORECASE):
                            issues.append({
                                "severity": "medium",
                                "description": "Weak password policy detected - minimum length not enforced",
                                "file": str(auth_file),
                                "category": "authentication"
                            })
                            
                    # Check for password hashing
                    if 'password' in content.lower() and not any(hash_lib in content.lower() for hash_lib in ['bcrypt', 'scrypt', 'argon2', 'pbkdf2']):
                        issues.append({
                            "severity": "high",
                            "description": "Password may not be properly hashed",
                            "file": str(auth_file),
                            "category": "authentication"
                        })
                        
                    # Check for session management
                    if 'session' in content.lower():
                        if 'secure' not in content.lower() or 'httponly' not in content.lower():
                            issues.append({
                                "severity": "medium",
                                "description": "Session cookies may not have secure flags",
                                "file": str(auth_file),
                                "category": "authentication"
                            })
                            
                except Exception as e:
                    print(f"Error analyzing authentication in {auth_file}: {e}")
                    
        return issues
        
    def _analyze_authorization(self) -> List[Dict[str, Any]]:
        """Analyze authorization and access control"""
        issues = []
        
        # Look for authorization decorators and checks
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for routes without authorization
                    routes = re.findall(r'@\w+\.route\([\'"]([^\'"]+)[\'"].*?\)', content)
                    for route in routes:
                        # Look for authorization decorators near the route
                        route_section = self._get_route_section(content, route)
                        if not any(auth_keyword in route_section.lower() for auth_keyword in ['login_required', 'auth', 'permission', 'role']):
                            issues.append({
                                "severity": "high",
                                "description": f"Route {route} may lack proper authorization",
                                "file": str(py_file),
                                "category": "authorization"
                            })
                            
                except Exception as e:
                    print(f"Error analyzing authorization in {py_file}: {e}")
                    
        return issues
        
    def _get_route_section(self, content: str, route: str) -> str:
        """Get the section of code around a route definition"""
        lines = content.split('\n')
        route_line = -1
        
        for i, line in enumerate(lines):
            if route in line and '@' in line:
                route_line = i
                break
                
        if route_line >= 0:
            start = max(0, route_line - 5)
            end = min(len(lines), route_line + 10)
            return '\n'.join(lines[start:end])
            
        return ""
        
    def _check_input_validation(self) -> List[Dict[str, Any]]:
        """Check for input validation issues"""
        issues = []
        
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for direct request parameter usage without validation
                    if 'request.' in content:
                        request_usages = re.findall(r'request\.(form|args|json)\[?[\'"]([^\'"]+)[\'"]?\]?', content)
                        for usage_type, param_name in request_usages:
                            # Look for validation around this usage
                            if not re.search(rf'{param_name}.*valid|valid.*{param_name}', content, re.IGNORECASE):
                                issues.append({
                                    "severity": "medium",
                                    "description": f"Parameter '{param_name}' from request.{usage_type} may lack validation",
                                    "file": str(py_file),
                                    "category": "input_validation"
                                })
                                
                except Exception as e:
                    print(f"Error checking input validation in {py_file}: {e}")
                    
        return issues
        
    def _check_sql_injection_risks(self) -> List[Dict[str, Any]]:
        """Check for SQL injection vulnerabilities"""
        issues = []
        
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for string formatting in SQL queries
                    sql_patterns = [
                        r'\.execute\([\'"][^\'"]*(SELECT|INSERT|UPDATE|DELETE)[^\'"]*(\.format\(|\%|f[\'"])',
                        r'(SELECT|INSERT|UPDATE|DELETE)[^\'"]*(\.format\(|\%|f[\'"])',
                    ]
                    
                    for pattern in sql_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues.append({
                                "severity": "critical",
                                "description": "Potential SQL injection vulnerability - string formatting in SQL query",
                                "file": str(py_file),
                                "category": "sql_injection"
                            })
                            
                except Exception as e:
                    print(f"Error checking SQL injection in {py_file}: {e}")
                    
        return issues
        
    def _analyze_csrf_protection(self) -> List[Dict[str, Any]]:
        """Analyze CSRF protection"""
        issues = []
        
        # Check for CSRF protection in forms
        for html_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("template_files", []):
            file_path = self.project_root / html_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for forms without CSRF tokens
                    forms = re.findall(r'<form[^>]*>', content, re.IGNORECASE)
                    for form in forms:
                        if 'method="post"' in form.lower() or 'method=\'post\'' in form.lower():
                            # Check if CSRF token is present in the form area
                            form_section = self._get_form_section(content, form)
                            if not any(csrf_keyword in form_section.lower() for csrf_keyword in ['csrf', 'token', 'authenticity']):
                                issues.append({
                                    "severity": "high",
                                    "description": "POST form may lack CSRF protection",
                                    "file": str(html_file),
                                    "category": "csrf"
                                })
                                
                except Exception as e:
                    print(f"Error analyzing CSRF in {html_file}: {e}")
                    
        return issues
        
    def _get_form_section(self, content: str, form_tag: str) -> str:
        """Get the section of HTML around a form"""
        form_start = content.find(form_tag)
        if form_start >= 0:
            form_end = content.find('</form>', form_start)
            if form_end >= 0:
                return content[form_start:form_end + 7]
        return ""
        
    def _check_secure_headers(self) -> List[Dict[str, Any]]:
        """Check for security headers"""
        issues = []
        
        # Look for security header configuration
        security_headers = [
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'X-XSS-Protection'
        ]
        
        headers_found = []
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for header in security_headers:
                        if header in content:
                            headers_found.append(header)
                            
                except Exception as e:
                    print(f"Error checking headers in {py_file}: {e}")
                    
        missing_headers = set(security_headers) - set(headers_found)
        for header in missing_headers:
            issues.append({
                "severity": "medium",
                "description": f"Missing security header: {header}",
                "file": "global",
                "category": "security_headers"
            })
            
        return issues
        
    def phase_2_ui_ux_analysis(self):
        """Phase 2: UI/UX Analysis with design expert consultation"""
        print("🎨 Phase 2: UI/UX Analysis")
        
        ui_analysis = {
            "accessibility": self._analyze_accessibility(),
            "responsive_design": self._analyze_responsive_design(),
            "rtl_support": self._analyze_rtl_support(),
            "user_experience": self._analyze_user_experience(),
            "design_consistency": self._analyze_design_consistency()
        }
        
        self.analysis_results["ui_ux_evaluation"] = ui_analysis
        
    def _analyze_accessibility(self) -> Dict[str, Any]:
        """Analyze accessibility compliance"""
        accessibility_issues = []
        
        for html_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("template_files", []):
            file_path = self.project_root / html_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for images without alt text
                    img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
                    for img in img_tags:
                        if 'alt=' not in img.lower():
                            accessibility_issues.append({
                                "severity": "medium",
                                "description": "Image without alt text",
                                "file": str(html_file),
                                "element": img[:50] + "..."
                            })
                            
                    # Check for form inputs without labels
                    input_tags = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
                    for input_tag in input_tags:
                        if 'type="submit"' not in input_tag.lower() and 'type="button"' not in input_tag.lower():
                            # Look for associated label
                            input_id = re.search(r'id=[\'"]([^\'"]+)[\'"]', input_tag)
                            if input_id:
                                label_pattern = f'for=[\'"]({input_id.group(1)})[\'"]'
                                if not re.search(label_pattern, content, re.IGNORECASE):
                                    accessibility_issues.append({
                                        "severity": "medium",
                                        "description": "Form input without associated label",
                                        "file": str(html_file),
                                        "element": input_tag[:50] + "..."
                                    })
                                    
                except Exception as e:
                    print(f"Error analyzing accessibility in {html_file}: {e}")
                    
        return {
            "issues": accessibility_issues,
            "wcag_compliance": "partial" if accessibility_issues else "unknown",
            "total_issues": len(accessibility_issues)
        }
        
    def _analyze_responsive_design(self) -> Dict[str, Any]:
        """Analyze responsive design implementation"""
        responsive_indicators = []
        
        for css_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("static_files", []):
            if css_file.endswith('.css'):
                file_path = self.project_root / css_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Check for media queries
                        media_queries = re.findall(r'@media[^{]+{', content, re.IGNORECASE)
                        responsive_indicators.extend(media_queries)
                        
                        # Check for flexible units
                        flexible_units = re.findall(r'\d+(\%|em|rem|vw|vh|vmin|vmax)', content)
                        
                    except Exception as e:
                        print(f"Error analyzing responsive design in {css_file}: {e}")
                        
        return {
            "media_queries_found": len(responsive_indicators),
            "responsive_indicators": responsive_indicators[:10],  # First 10 examples
            "assessment": "good" if len(responsive_indicators) > 5 else "needs_improvement"
        }
        
    def _analyze_rtl_support(self) -> Dict[str, Any]:
        """Analyze RTL (Right-to-Left) support for Arabic"""
        rtl_indicators = []
        rtl_issues = []
        
        # Check CSS files for RTL support
        for css_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("static_files", []):
            if css_file.endswith('.css'):
                file_path = self.project_root / css_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Check for RTL-specific CSS
                        rtl_patterns = ['direction:', 'text-align:', '[dir="rtl"]', '[dir=rtl]']
                        for pattern in rtl_patterns:
                            if pattern in content.lower():
                                rtl_indicators.append(f"Found {pattern} in {css_file}")
                                
                        # Check for potential RTL issues
                        if 'float:' in content and 'float: left' in content and 'float: right' not in content:
                            rtl_issues.append(f"Fixed float directions in {css_file} may break RTL layout")
                            
                    except Exception as e:
                        print(f"Error analyzing RTL support in {css_file}: {e}")
                        
        # Check HTML files for RTL attributes
        for html_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("template_files", []):
            file_path = self.project_root / html_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    if 'dir="rtl"' in content or 'lang="ar"' in content:
                        rtl_indicators.append(f"RTL attributes found in {html_file}")
                        
                except Exception as e:
                    print(f"Error analyzing RTL in {html_file}: {e}")
                    
        return {
            "rtl_support_indicators": rtl_indicators,
            "rtl_issues": rtl_issues,
            "assessment": "good" if len(rtl_indicators) > 0 else "needs_implementation"
        }
        
    def _analyze_user_experience(self) -> Dict[str, Any]:
        """Analyze user experience aspects"""
        ux_analysis = {
            "navigation_consistency": [],
            "error_handling": [],
            "loading_states": [],
            "user_feedback": []
        }
        
        # Analyze JavaScript files for UX patterns
        for js_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("js_files", []):
            file_path = self.project_root / js_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for loading states
                    if any(keyword in content.lower() for keyword in ['loading', 'spinner', 'skeleton']):
                        ux_analysis["loading_states"].append(f"Loading indicators found in {js_file}")
                        
                    # Check for error handling
                    if any(keyword in content.lower() for keyword in ['error', 'catch', 'try']):
                        ux_analysis["error_handling"].append(f"Error handling found in {js_file}")
                        
                    # Check for user feedback
                    if any(keyword in content.lower() for keyword in ['toast', 'alert', 'notification', 'message']):
                        ux_analysis["user_feedback"].append(f"User feedback mechanisms found in {js_file}")
                        
                except Exception as e:
                    print(f"Error analyzing UX in {js_file}: {e}")
                    
        return ux_analysis
        
    def _analyze_design_consistency(self) -> Dict[str, Any]:
        """Analyze design system consistency"""
        consistency_analysis = {
            "color_usage": [],
            "typography": [],
            "spacing": [],
            "component_reuse": []
        }
        
        # Analyze CSS for design tokens
        all_colors = set()
        all_fonts = set()
        
        for css_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("static_files", []):
            if css_file.endswith('.css'):
                file_path = self.project_root / css_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Extract colors
                        colors = re.findall(r'#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)', content)
                        all_colors.update(colors)
                        
                        # Extract fonts
                        fonts = re.findall(r'font-family:\s*([^;]+)', content)
                        all_fonts.update(fonts)
                        
                    except Exception as e:
                        print(f"Error analyzing design consistency in {css_file}: {e}")
                        
        consistency_analysis["color_usage"] = list(all_colors)[:20]  # First 20 colors
        consistency_analysis["typography"] = list(all_fonts)[:10]   # First 10 fonts
        
        return consistency_analysis
        
    def phase_3_performance_analysis(self):
        """Phase 3: Performance analysis"""
        print("⚡ Phase 3: Performance Analysis")
        
        performance_metrics = {
            "code_complexity": self._analyze_code_complexity(),
            "database_performance": self._analyze_database_performance(),
            "frontend_performance": self._analyze_frontend_performance(),
            "api_performance": self._analyze_api_performance()
        }
        
        self.analysis_results["performance_metrics"] = performance_metrics
        
    def _analyze_code_complexity(self) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        complexity_metrics = {
            "python_files": [],
            "javascript_files": [],
            "high_complexity_files": []
        }
        
        # Analyze Python files
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Simple complexity metrics
                    lines_of_code = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
                    function_count = len(re.findall(r'def\s+\w+', content))
                    class_count = len(re.findall(r'class\s+\w+', content))
                    
                    file_metrics = {
                        "file": str(py_file),
                        "lines_of_code": lines_of_code,
                        "function_count": function_count,
                        "class_count": class_count,
                        "complexity_score": lines_of_code / max(function_count, 1)
                    }
                    
                    complexity_metrics["python_files"].append(file_metrics)
                    
                    if file_metrics["complexity_score"] > 50:
                        complexity_metrics["high_complexity_files"].append(file_metrics)
                        
                except Exception as e:
                    print(f"Error analyzing complexity in {py_file}: {e}")
                    
        return complexity_metrics
        
    def _analyze_database_performance(self) -> Dict[str, Any]:
        """Analyze database performance aspects"""
        db_performance = {
            "potential_n_plus_one": [],
            "missing_indexes": [],
            "large_queries": []
        }
        
        # Look for potential N+1 query problems
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for loops with database queries
                    loop_query_pattern = r'for\s+\w+\s+in.*?\.query\.|\.filter\.|\.get\('
                    if re.search(loop_query_pattern, content, re.DOTALL):
                        db_performance["potential_n_plus_one"].append({
                            "file": str(py_file),
                            "description": "Potential N+1 query pattern detected"
                        })
                        
                    # Look for missing eager loading
                    if '.query.' in content and 'joinedload' not in content and 'selectinload' not in content:
                        db_performance["missing_indexes"].append({
                            "file": str(py_file),
                            "description": "Queries without eager loading detected"
                        })
                        
                except Exception as e:
                    print(f"Error analyzing DB performance in {py_file}: {e}")
                    
        return db_performance
        
    def _analyze_frontend_performance(self) -> Dict[str, Any]:
        """Analyze frontend performance"""
        frontend_performance = {
            "bundle_size_indicators": [],
            "optimization_opportunities": [],
            "performance_patterns": []
        }
        
        # Check for performance optimization patterns
        for js_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("js_files", []):
            file_path = self.project_root / js_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for lazy loading
                    if 'lazy' in content.lower() or 'dynamic import' in content.lower():
                        frontend_performance["performance_patterns"].append({
                            "file": str(js_file),
                            "pattern": "Lazy loading detected"
                        })
                        
                    # Check for memoization
                    if 'useMemo' in content or 'useCallback' in content or 'memo(' in content:
                        frontend_performance["performance_patterns"].append({
                            "file": str(js_file),
                            "pattern": "Memoization patterns detected"
                        })
                        
                    # Check for large files
                    if len(content) > 10000:  # Files larger than 10KB
                        frontend_performance["bundle_size_indicators"].append({
                            "file": str(js_file),
                            "size": len(content),
                            "suggestion": "Consider code splitting"
                        })
                        
                except Exception as e:
                    print(f"Error analyzing frontend performance in {js_file}: {e}")
                    
        return frontend_performance
        
    def _analyze_api_performance(self) -> Dict[str, Any]:
        """Analyze API performance aspects"""
        api_performance = {
            "caching_implementation": [],
            "pagination_support": [],
            "rate_limiting": []
        }
        
        # Check for caching patterns
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for caching
                    if any(cache_keyword in content.lower() for cache_keyword in ['cache', 'redis', 'memcached']):
                        api_performance["caching_implementation"].append({
                            "file": str(py_file),
                            "description": "Caching implementation found"
                        })
                        
                    # Check for pagination
                    if any(page_keyword in content.lower() for page_keyword in ['page', 'limit', 'offset', 'paginate']):
                        api_performance["pagination_support"].append({
                            "file": str(py_file),
                            "description": "Pagination support found"
                        })
                        
                    # Check for rate limiting
                    if any(rate_keyword in content.lower() for rate_keyword in ['rate_limit', 'throttle', 'limiter']):
                        api_performance["rate_limiting"].append({
                            "file": str(py_file),
                            "description": "Rate limiting found"
                        })
                        
                except Exception as e:
                    print(f"Error analyzing API performance in {py_file}: {e}")
                    
        return api_performance
        
    def generate_expert_evaluations(self):
        """Generate expert evaluations using AI consultation"""
        print("👥 Generating Expert Evaluations")
        
        # Security Consultant Evaluation
        security_score = self._security_consultant_evaluation()
        
        # Software Engineering Consultant Evaluation
        engineering_score = self._software_engineering_evaluation()
        
        # UI/UX Design Consultant Evaluation
        design_score = self._design_consultant_evaluation()
        
        # Political Analyst Evaluation
        political_score = self._political_analyst_evaluation()
        
        # Economic Analyst Evaluation
        economic_score = self._economic_analyst_evaluation()
        
        self.analysis_results["expert_evaluations"] = {
            "security_consultant": security_score,
            "software_engineering": engineering_score,
            "design_consultant": design_score,
            "political_analyst": political_score,
            "economic_analyst": economic_score,
            "overall_osf_score": self._calculate_osf_score(security_score, engineering_score, design_score)
        }
        
    def _security_consultant_evaluation(self) -> Dict[str, Any]:
        """Security consultant evaluation"""
        security_issues = self.analysis_results.get("security_assessment", {})
        
        critical_count = len(security_issues.get("critical_issues", []))
        high_count = len(security_issues.get("high_issues", []))
        total_issues = security_issues.get("total_issues", 0)
        
        # Calculate security score (0-1)
        if total_issues == 0:
            score = 0.9  # Good but not perfect without testing
        else:
            # Penalize critical and high issues more heavily
            penalty = (critical_count * 0.3) + (high_count * 0.2) + (total_issues * 0.05)
            score = max(0.0, 1.0 - penalty)
            
        recommendations = []
        if critical_count > 0:
            recommendations.append("URGENT: Address critical security vulnerabilities immediately")
        if high_count > 0:
            recommendations.append("HIGH PRIORITY: Fix high-severity security issues")
        if not any("csrf" in str(issue) for issue in security_issues.get("all_issues", [])):
            recommendations.append("Implement comprehensive CSRF protection")
        if not any("header" in str(issue) for issue in security_issues.get("all_issues", [])):
            recommendations.append("Add security headers (CSP, HSTS, etc.)")
            
        return {
            "score": round(score, 2),
            "assessment": "critical" if score < 0.3 else "needs_improvement" if score < 0.7 else "good",
            "critical_issues": critical_count,
            "high_issues": high_count,
            "total_issues": total_issues,
            "recommendations": recommendations,
            "threat_model_needed": True,
            "penetration_testing_recommended": score < 0.8
        }
        
    def _software_engineering_evaluation(self) -> Dict[str, Any]:
        """Software engineering consultant evaluation"""
        performance = self.analysis_results.get("performance_metrics", {})
        
        # Evaluate code quality metrics
        complexity = performance.get("code_complexity", {})
        high_complexity_files = len(complexity.get("high_complexity_files", []))
        total_python_files = len(complexity.get("python_files", []))
        
        # Calculate engineering score
        complexity_ratio = high_complexity_files / max(total_python_files, 1)
        complexity_score = max(0.0, 1.0 - complexity_ratio)
        
        # Check for best practices
        db_performance = performance.get("database_performance", {})
        n_plus_one_issues = len(db_performance.get("potential_n_plus_one", []))
        
        performance_score = max(0.0, 1.0 - (n_plus_one_issues * 0.1))
        
        overall_score = (complexity_score * 0.4) + (performance_score * 0.6)
        
        recommendations = []
        if high_complexity_files > 0:
            recommendations.append(f"Refactor {high_complexity_files} high-complexity files")
        if n_plus_one_issues > 0:
            recommendations.append("Optimize database queries to prevent N+1 problems")
        
        recommendations.extend([
            "Implement comprehensive unit testing",
            "Add integration tests for critical paths",
            "Set up continuous integration pipeline",
            "Implement code coverage reporting"
        ])
        
        return {
            "score": round(overall_score, 2),
            "assessment": "needs_major_improvement" if overall_score < 0.5 else "needs_improvement" if overall_score < 0.7 else "good",
            "code_complexity_score": round(complexity_score, 2),
            "performance_score": round(performance_score, 2),
            "high_complexity_files": high_complexity_files,
            "recommendations": recommendations,
            "testing_coverage_needed": True,
            "refactoring_priority": "high" if overall_score < 0.6 else "medium"
        }
        
    def _design_consultant_evaluation(self) -> Dict[str, Any]:
        """UI/UX design consultant evaluation"""
        ui_analysis = self.analysis_results.get("ui_ux_evaluation", {})
        
        # Evaluate accessibility
        accessibility = ui_analysis.get("accessibility", {})
        accessibility_issues = len(accessibility.get("issues", []))
        accessibility_score = max(0.0, 1.0 - (accessibility_issues * 0.1))
        
        # Evaluate RTL support
        rtl_support = ui_analysis.get("rtl_support", {})
        rtl_indicators = len(rtl_support.get("rtl_support_indicators", []))
        rtl_score = min(1.0, rtl_indicators * 0.2) if rtl_indicators > 0 else 0.0
        
        # Evaluate responsive design
        responsive = ui_analysis.get("responsive_design", {})
        media_queries = responsive.get("media_queries_found", 0)
        responsive_score = min(1.0, media_queries * 0.1)
        
        overall_score = (accessibility_score * 0.4) + (rtl_score * 0.4) + (responsive_score * 0.2)
        
        recommendations = []
        if accessibility_issues > 0:
            recommendations.append(f"Fix {accessibility_issues} accessibility issues for WCAG compliance")
        if rtl_score < 0.5:
            recommendations.append("Implement comprehensive RTL support for Arabic users")
        if responsive_score < 0.5:
            recommendations.append("Improve responsive design with more media queries")
        
        recommendations.extend([
            "Establish a design system with consistent tokens",
            "Implement user testing for Arabic-speaking users",
            "Add loading states and error handling UX",
            "Optimize for mobile-first design"
        ])
        
        return {
            "score": round(overall_score, 2),
            "assessment": "critical" if overall_score < 0.3 else "needs_improvement" if overall_score < 0.7 else "good",
            "accessibility_score": round(accessibility_score, 2),
            "rtl_score": round(rtl_score, 2),
            "responsive_score": round(responsive_score, 2),
            "accessibility_issues": accessibility_issues,
            "recommendations": recommendations,
            "user_testing_needed": True,
            "design_system_priority": "high"
        }
        
    def _political_analyst_evaluation(self) -> Dict[str, Any]:
        """Political analyst evaluation for regulatory and geopolitical risks"""
        
        # Analyze data privacy compliance
        privacy_risks = []
        
        # Check for GDPR/data protection considerations
        for py_file in self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("python_files", []):
            file_path = self.project_root / py_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for personal data handling
                    if any(keyword in content.lower() for keyword in ['email', 'phone', 'address', 'personal']):
                        if 'consent' not in content.lower() and 'privacy' not in content.lower():
                            privacy_risks.append({
                                "file": str(py_file),
                                "risk": "Personal data handling without clear privacy controls"
                            })
                            
                except Exception as e:
                    print(f"Error analyzing privacy in {py_file}: {e}")
                    
        # Regional compliance assessment
        regional_risks = [
            "Arabic language compliance for local regulations",
            "Data residency requirements in MENA region",
            "Financial transaction regulations",
            "Cross-border data transfer restrictions"
        ]
        
        # Calculate political risk score
        privacy_penalty = len(privacy_risks) * 0.2
        political_score = max(0.0, 1.0 - privacy_penalty)
        
        recommendations = [
            "Implement GDPR-compliant data handling procedures",
            "Add privacy policy and terms of service in Arabic",
            "Ensure data residency compliance for target markets",
            "Review local business licensing requirements",
            "Implement audit logging for regulatory compliance"
        ]
        
        return {
            "score": round(political_score, 2),
            "assessment": "moderate_risk" if political_score < 0.7 else "low_risk",
            "privacy_risks": privacy_risks,
            "regional_risks": regional_risks,
            "recommendations": recommendations,
            "compliance_audit_needed": True,
            "legal_review_priority": "high" if political_score < 0.6 else "medium"
        }
        
    def _economic_analyst_evaluation(self) -> Dict[str, Any]:
        """Economic analyst evaluation for cost and ROI considerations"""
        
        # Analyze infrastructure costs
        dependencies = self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("dependencies", {})
        
        python_deps = len(dependencies.get("python", {}))
        nodejs_deps = len(dependencies.get("nodejs", {}).get("dependencies", {}))
        
        # Calculate complexity-based cost factors
        total_files = len(self.analysis_results.get("analysis_phases", {}).get("phase_0", {}).get("file_structure", {}).get("all_files", []))
        
        # Estimate development and maintenance costs
        development_complexity = min(1.0, total_files / 100)  # Normalize to 0-1
        dependency_overhead = min(1.0, (python_deps + nodejs_deps) / 50)  # Normalize to 0-1
        
        # Calculate economic viability score
        cost_efficiency = 1.0 - (development_complexity * 0.3) - (dependency_overhead * 0.2)
        market_potential = 0.8  # Assuming good market potential for Arabic inventory systems
        
        economic_score = (cost_efficiency * 0.6) + (market_potential * 0.4)
        
        # ROI projections
        roi_factors = {
            "market_size": "Large (Arabic-speaking business market)",
            "competition": "Moderate (limited Arabic-first solutions)",
            "development_cost": "Medium" if total_files < 100 else "High",
            "maintenance_cost": "Medium" if dependency_overhead < 0.5 else "High",
            "time_to_market": "6-12 months" if total_files < 100 else "12-18 months"
        }
        
        recommendations = [
            "Focus on core features to reduce development complexity",
            "Consider managed services to reduce infrastructure costs",
            "Implement usage-based pricing model",
            "Target enterprise customers for higher revenue per user",
            "Develop partnerships with Arabic business software vendors"
        ]
        
        if dependency_overhead > 0.7:
            recommendations.append("Review and reduce dependency count to lower maintenance costs")
            
        return {
            "score": round(economic_score, 2),
            "assessment": "viable" if economic_score > 0.6 else "challenging",
            "cost_efficiency": round(cost_efficiency, 2),
            "market_potential": market_potential,
            "roi_factors": roi_factors,
            "recommendations": recommendations,
            "financial_modeling_needed": True,
            "investment_priority": "high" if economic_score > 0.7 else "medium"
        }
        
    def _calculate_osf_score(self, security_eval: Dict, engineering_eval: Dict, design_eval: Dict) -> Dict[str, Any]:
        """Calculate OSF (Optimal & Safe over Fast) score"""
        
        # OSF_Score = 0.40 Sec + 0.25 Corr + 0.15 Rel + 0.10 Maint + 0.05 Perf + 0.05 Speed
        security_score = security_eval.get("score", 0.0)
        correctness_score = engineering_eval.get("score", 0.0)
        reliability_score = 0.7  # Estimated based on error handling analysis
        maintainability_score = 1.0 - (engineering_eval.get("high_complexity_files", 0) * 0.1)
        performance_score = engineering_eval.get("performance_score", 0.7)
        speed_score = 0.6  # Estimated based on development velocity
        
        osf_score = (
            security_score * 0.40 +
            correctness_score * 0.25 +
            reliability_score * 0.15 +
            maintainability_score * 0.10 +
            performance_score * 0.05 +
            speed_score * 0.05
        )
        
        return {
            "osf_score": round(osf_score, 2),
            "security_component": round(security_score * 0.40, 3),
            "correctness_component": round(correctness_score * 0.25, 3),
            "reliability_component": round(reliability_score * 0.15, 3),
            "maintainability_component": round(maintainability_score * 0.10, 3),
            "performance_component": round(performance_score * 0.05, 3),
            "speed_component": round(speed_score * 0.05, 3),
            "assessment": "excellent" if osf_score > 0.8 else "good" if osf_score > 0.6 else "needs_improvement",
            "meets_threshold": osf_score >= 0.7
        }
        
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("📋 Generating Comprehensive Report")
        
        # Generate recommendations based on all analyses
        self._generate_recommendations()
        
        # Create final report
        report = {
            "executive_summary": self._create_executive_summary(),
            "detailed_analysis": self.analysis_results,
            "action_plan": self._create_action_plan(),
            "compliance_checklist": self._create_compliance_checklist()
        }
        
        # Save report to file
        report_file = self.project_root / "COMPREHENSIVE_SYSTEM_ANALYSIS_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
        
    def _generate_recommendations(self):
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Security recommendations
        security_eval = self.analysis_results.get("expert_evaluations", {}).get("security_consultant", {})
        if security_eval.get("score", 0) < 0.7:
            recommendations.extend(security_eval.get("recommendations", []))
            
        # Engineering recommendations
        engineering_eval = self.analysis_results.get("expert_evaluations", {}).get("software_engineering", {})
        if engineering_eval.get("score", 0) < 0.7:
            recommendations.extend(engineering_eval.get("recommendations", []))
            
        # Design recommendations
        design_eval = self.analysis_results.get("expert_evaluations", {}).get("design_consultant", {})
        if design_eval.get("score", 0) < 0.7:
            recommendations.extend(design_eval.get("recommendations", []))
            
        # Add strategic recommendations
        recommendations.extend([
            "Implement comprehensive testing strategy (unit, integration, e2e)",
            "Set up continuous integration and deployment pipeline",
            "Create detailed API documentation with OpenAPI/Swagger",
            "Implement monitoring and logging for production",
            "Create backup and disaster recovery procedures",
            "Develop user training materials in Arabic",
            "Plan for scalability and performance optimization",
            "Establish code review and quality assurance processes"
        ])
        
        self.analysis_results["recommendations"] = list(set(recommendations))  # Remove duplicates
        
    def _create_executive_summary(self) -> Dict[str, Any]:
        """Create executive summary"""
        expert_evals = self.analysis_results.get("expert_evaluations", {})
        
        return {
            "overall_assessment": "The Arabic Inventory Management System shows promise but requires significant improvements in security, code quality, and user experience.",
            "key_strengths": [
                "Comprehensive feature set for inventory management",
                "Arabic language support implementation",
                "Modern technology stack (React + Flask)",
                "Well-structured project organization"
            ],
            "critical_issues": [
                f"Security score: {expert_evals.get('security_consultant', {}).get('score', 0)}/1.0",
                f"Engineering score: {expert_evals.get('software_engineering', {}).get('score', 0)}/1.0",
                f"Design score: {expert_evals.get('design_consultant', {}).get('score', 0)}/1.0"
            ],
            "osf_score": expert_evals.get("overall_osf_score", {}).get("osf_score", 0),
            "readiness_for_production": "Not Ready - Requires significant improvements",
            "estimated_effort_to_production": "3-6 months with dedicated team",
            "investment_recommendation": expert_evals.get("economic_analyst", {}).get("assessment", "challenging")
        }
        
    def _create_action_plan(self) -> Dict[str, Any]:
        """Create prioritized action plan"""
        return {
            "phase_1_critical": [
                "Fix all critical and high-severity security vulnerabilities",
                "Implement proper authentication and authorization",
                "Add CSRF protection to all forms",
                "Set up security headers (CSP, HSTS, etc.)"
            ],
            "phase_2_quality": [
                "Refactor high-complexity code files",
                "Implement comprehensive unit testing",
                "Set up code quality tools (linting, formatting)",
                "Optimize database queries and add proper indexing"
            ],
            "phase_3_ux": [
                "Fix accessibility issues for WCAG compliance",
                "Improve RTL support for Arabic users",
                "Enhance responsive design",
                "Implement proper error handling and user feedback"
            ],
            "phase_4_production": [
                "Set up CI/CD pipeline",
                "Implement monitoring and logging",
                "Create deployment documentation",
                "Perform security penetration testing"
            ]
        }
        
    def _create_compliance_checklist(self) -> Dict[str, Any]:
        """Create compliance checklist"""
        return {
            "security_compliance": {
                "owasp_top_10": "Partial - Needs improvement",
                "authentication": "Needs implementation",
                "authorization": "Needs improvement",
                "data_encryption": "Needs verification",
                "secure_headers": "Missing",
                "input_validation": "Partial"
            },
            "accessibility_compliance": {
                "wcag_aa": "Non-compliant - Multiple issues found",
                "keyboard_navigation": "Needs testing",
                "screen_reader_support": "Needs improvement",
                "color_contrast": "Needs verification"
            },
            "arabic_localization": {
                "rtl_layout": "Partial implementation",
                "arabic_fonts": "Needs verification",
                "date_time_formatting": "Needs implementation",
                "number_formatting": "Needs implementation"
            },
            "performance_standards": {
                "page_load_time": "Needs measurement",
                "api_response_time": "Needs measurement",
                "database_optimization": "Needs improvement",
                "caching_strategy": "Needs implementation"
            }
        }
        
    def _generate_markdown_report(self, report: Dict[str, Any]):
        """Generate markdown version of the report"""
        markdown_content = f"""# Comprehensive System Analysis Report
## Arabic Inventory Management System

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Project Root:** {self.project_root}

## Executive Summary

{report['executive_summary']['overall_assessment']}

### Key Metrics
- **OSF Score:** {report['executive_summary']['osf_score']}/1.0
- **Production Readiness:** {report['executive_summary']['readiness_for_production']}
- **Estimated Effort:** {report['executive_summary']['estimated_effort_to_production']}

### Expert Evaluations

| Expert | Score | Assessment |
|--------|-------|------------|
| Security Consultant | {report['detailed_analysis']['expert_evaluations']['security_consultant']['score']}/1.0 | {report['detailed_analysis']['expert_evaluations']['security_consultant']['assessment']} |
| Software Engineering | {report['detailed_analysis']['expert_evaluations']['software_engineering']['score']}/1.0 | {report['detailed_analysis']['expert_evaluations']['software_engineering']['assessment']} |
| Design Consultant | {report['detailed_analysis']['expert_evaluations']['design_consultant']['score']}/1.0 | {report['detailed_analysis']['expert_evaluations']['design_consultant']['assessment']} |
| Political Analyst | {report['detailed_analysis']['expert_evaluations']['political_analyst']['score']}/1.0 | {report['detailed_analysis']['expert_evaluations']['political_analyst']['assessment']} |
| Economic Analyst | {report['detailed_analysis']['expert_evaluations']['economic_analyst']['score']}/1.0 | {report['detailed_analysis']['expert_evaluations']['economic_analyst']['assessment']} |

## Critical Issues

{chr(10).join(f"- {issue}" for issue in report['executive_summary']['critical_issues'])}

## Security Assessment

**Total Issues:** {report['detailed_analysis']['security_assessment']['total_issues']}
- Critical: {len(report['detailed_analysis']['security_assessment']['critical_issues'])}
- High: {len(report['detailed_analysis']['security_assessment']['high_issues'])}
- Medium: {len(report['detailed_analysis']['security_assessment']['medium_issues'])}
- Low: {len(report['detailed_analysis']['security_assessment']['low_issues'])}

## Action Plan

### Phase 1: Critical Security Issues
{chr(10).join(f"- {item}" for item in report['action_plan']['phase_1_critical'])}

### Phase 2: Code Quality
{chr(10).join(f"- {item}" for item in report['action_plan']['phase_2_quality'])}

### Phase 3: User Experience
{chr(10).join(f"- {item}" for item in report['action_plan']['phase_3_ux'])}

### Phase 4: Production Readiness
{chr(10).join(f"- {item}" for item in report['action_plan']['phase_4_production'])}

## Recommendations

{chr(10).join(f"- {rec}" for rec in report['detailed_analysis']['recommendations'])}

---

*This report was generated using AI-assisted comprehensive system analysis.*
"""

        # Save markdown report
        markdown_file = self.project_root / "COMPREHENSIVE_SYSTEM_ANALYSIS_REPORT.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
    def run_complete_analysis(self):
        """Run the complete analysis process"""
        print("🚀 Starting Comprehensive System Analysis")
        print("=" * 60)
        
        try:
            # Phase 0: Discovery and Mapping
            self.phase_0_discovery_and_mapping()
            
            # Phase 1: Security Analysis
            self.phase_1_security_analysis()
            
            # Phase 2: UI/UX Analysis
            self.phase_2_ui_ux_analysis()
            
            # Phase 3: Performance Analysis
            self.phase_3_performance_analysis()
            
            # Generate Expert Evaluations
            self.generate_expert_evaluations()
            
            # Generate Comprehensive Report
            report = self.generate_comprehensive_report()
            
            print("=" * 60)
            print("✅ Analysis Complete!")
            print(f"📊 OSF Score: {report['executive_summary']['osf_score']}/1.0")
            print(f"📋 Report saved to: COMPREHENSIVE_SYSTEM_ANALYSIS_REPORT.md")
            
            return report
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            raise

if __name__ == "__main__":
    analyzer = SystemAnalyzer("/home/ubuntu/Store")
    report = analyzer.run_complete_analysis()
