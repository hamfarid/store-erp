#!/usr/bin/env python3
"""
Comprehensive Project Analyzer for Gaara ERP v5
Systematically analyzes all aspects of the Django project
"""

import os
import sys
import ast
import importlib
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import subprocess
import traceback
import re

# Add Django setup
sys.path.insert(0, str(Path(__file__).parent / "gaara_erp"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaara_erp.settings")

try:
    import django
    django.setup()
    from django.conf import settings
    from django.apps import apps
    from django.urls import get_resolver
except Exception as e:
    print(f"Django setup failed: {e}")
    print("Attempting to continue without Django...")
    settings = None
    apps = None


class ComprehensiveProjectAnalyzer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.gaara_root = self.project_root / "gaara_erp"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_structure": {},
            "installed_apps": [],
            "python_files": [],
            "import_analysis": {},
            "syntax_errors": [],
            "models_analysis": {},
            "api_endpoints": [],
            "security_analysis": {},
            "performance_issues": [],
            "static_analysis_errors": [],
            "test_files": [],
            "missing_dependencies": [],
            "recommendations": []
        }

    def analyze_project_structure(self):
        """Analyze complete project structure"""
        print("🔍 Analyzing project structure...")

        # Get all installed apps
        if settings:
            self.results["installed_apps"] = list(settings.INSTALLED_APPS)
        else:
            # Try to parse settings file manually
            self.results["installed_apps"] = self._parse_installed_apps()

        # Scan all Python files
        python_files = []
        test_files = []
        for root, dirs, files in os.walk(self.gaara_root):
            # Skip virtual environments and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', '.venv', 'migrations']]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    relative_path = str(file_path.relative_to(self.project_root))
                    python_files.append(relative_path)

                    # Identify test files
                    if 'test' in file or file.startswith('test_'):
                        test_files.append(relative_path)

        self.results["python_files"] = python_files
        self.results["test_files"] = test_files
        print(f"   Found {len(python_files)} Python files")
        print(f"   Found {len(test_files)} test files")

    def _parse_installed_apps(self):
        """Manually parse INSTALLED_APPS from settings file"""
        try:
            settings_path = self.gaara_root / "gaara_erp" / "settings.py"
            if not settings_path.exists():
                settings_path = self.gaara_root / "settings.py"

            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find INSTALLED_APPS
            match = re.search(r'INSTALLED_APPS\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if match:
                apps_str = match.group(1)
                apps = re.findall(r'["\']([^"\']+)["\']', apps_str)
                return apps
        except Exception as e:
            print(f"   Could not parse INSTALLED_APPS: {e}")
        return []

    def analyze_syntax_and_imports(self):
        """Check all Python files for syntax errors and import issues"""
        print("🔍 Analyzing syntax and imports...")

        syntax_errors = []
        import_errors = []
        static_errors = []

        for file_path in self.results["python_files"]:
            self._analyze_single_file(file_path, syntax_errors, import_errors, static_errors)

        self.results["syntax_errors"] = syntax_errors
        self.results["import_analysis"]["errors"] = import_errors
        self.results["static_analysis_errors"] = static_errors

        print(f"   Found {len(syntax_errors)} syntax errors")
        print(f"   Found {len(import_errors)} import issues")
        print(f"   Found {len(static_errors)} static analysis issues")

    def _analyze_single_file(self, file_path, syntax_errors, import_errors, static_errors):
        """Analyze a single Python file for syntax and import issues"""
        full_path = self.project_root / file_path
        tree = None

        try:
            # Check syntax
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                tree = ast.parse(content)
                # Analyze AST for common issues
                self._analyze_ast(tree, file_path, static_errors)
            except SyntaxError as e:
                syntax_errors.append({
                    "file": file_path,
                    "error": str(e),
                    "line": e.lineno,
                    "text": e.text
                })

            # Check imports if parsing succeeded
            if tree:
                self._analyze_imports(tree, file_path, import_errors)

        except UnicodeDecodeError:
            syntax_errors.append({
                "file": file_path,
                "error": "Unicode decode error - file encoding issue",
                "line": 0
            })
        except Exception as e:
            syntax_errors.append({
                "file": file_path,
                "error": f"File read failed: {e}",
                "line": 0
            })

    def _analyze_imports(self, tree, file_path, import_errors):
        """Analyze imports in an AST tree"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Extract import names
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._test_import(alias.name, file_path, import_errors, node.lineno)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self._test_import(node.module, file_path, import_errors, node.lineno)

    def _analyze_ast(self, tree, file_path, static_errors):
        """Analyze AST for common static errors"""
        for node in ast.walk(tree):
            # Check for __str__ methods
            if isinstance(node, ast.FunctionDef) and node.name == '__str__':
                # Check if it has return type annotation
                if not node.returns:
                    static_errors.append({
                        "file": file_path,
                        "error": "__str__ method missing return type annotation",
                        "line": node.lineno,
                        "type": "missing_type_hint"
                    })

            # Check for duplicate class definitions
            if isinstance(node, ast.ClassDef):
                if node.name == 'Meta':
                    # Count Meta classes in the same scope
                    pass  # This requires more complex scope analysis

    def _test_import(self, module_name, file_path, import_errors, line_no):
        """Test if a module can be imported"""
        # Skip relative imports
        if module_name and module_name.startswith('.'):
            return

        try:
            importlib.import_module(module_name)
        except ImportError as e:
            import_errors.append({
                "file": file_path,
                "module": module_name,
                "error": str(e),
                "line": line_no
            })
        except Exception:
            # Other import issues (circular imports, etc.)
            pass

    def analyze_models(self):
        """Analyze all Django models"""
        print("🔍 Analyzing Django models...")

        models_data: dict[str, dict[str, dict]] = {}

        if apps:
            try:
                for model in apps.get_models():
                    app_label = getattr(model._meta, 'app_label', 'unknown')
                    models_data.setdefault(app_label, {})

                    fields, relationships = self._extract_model_fields_and_relationships(model)
                    issues = self._collect_model_issues(model)

                    models_data[app_label][model.__name__] = {
                        "fields": fields,
                        "relationships": relationships,
                        "has_str_method": hasattr(model, '__str__'),
                        "has_custom_manager": len(getattr(model._meta, 'managers', [])) > 1,
                        "issues": issues,
                    }
            except Exception as e:
                print(f"   Error analyzing models: {e}")

        self.results["models_analysis"] = models_data
        print(f"   Analyzed {sum(len(models) for models in models_data.values())} models")

    def _collect_model_issues(self, model):
        """Collect simple structural issues for a model"""
        issues = []
        if not hasattr(model._meta, 'app_label'):
            issues.append("Missing app_label in Meta")
        # __str__ returns string
        if hasattr(model, '__str__'):
            try:
                instance = model()
                str_result = model.__str__(instance)
                if not isinstance(str_result, str):
                    issues.append("__str__ does not return string")
            except Exception:
                # Ignore construction errors
                pass
        else:
            issues.append("Missing __str__ method")
        return issues

    def _extract_model_fields_and_relationships(self, model):
        """Extract fields and relationship metadata from a model"""
        fields = []
        relationships = []
        for field in model._meta.get_fields():
            name = field.name if hasattr(field, 'name') else str(field)
            ftype = field.__class__.__name__
            if hasattr(field, 'related_model') and field.related_model:
                try:
                    target = f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                except Exception:
                    target = str(field.related_model)
                relationships.append({"field": name, "type": ftype, "target": target})
            else:
                fields.append({"name": name, "type": ftype})
        return fields, relationships

    def analyze_api_endpoints(self):
        """Analyze API endpoints"""
        print("🔍 Analyzing API endpoints...")

        endpoints = []

        if settings:
            try:
                # For now, we'll scan for urls.py files
                for file_path in self.results["python_files"]:
                    if file_path.endswith('urls.py'):
                        endpoints.append({
                            "file": file_path,
                            "type": "urls_file"
                        })
            except Exception:
                pass

        self.results["api_endpoints"] = endpoints
        print(f"   Found {len(endpoints)} URL files")

    def analyze_security(self):
        """Analyze security issues"""
        print("🔍 Analyzing security...")

        security_issues = []

        # Check settings for common security issues
        if settings:
            if getattr(settings, 'DEBUG', True):
                security_issues.append({
                    "issue": "DEBUG is True",
                    "severity": "high",
                    "recommendation": "Set DEBUG=False in production"
                })

            if getattr(settings, 'SECRET_KEY', '') == 'django-insecure-key':
                security_issues.append({
                    "issue": "Using default SECRET_KEY",
                    "severity": "critical",
                    "recommendation": "Generate a unique SECRET_KEY"
                })

        self.results["security_analysis"] = security_issues
        print(f"   Found {len(security_issues)} security issues")

    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        print("🔍 Generating recommendations...")

        recommendations = []

        # Based on syntax errors
        if self.results["syntax_errors"]:
            recommendations.append({
                "priority": "critical",
                "category": "syntax",
                "message": f"Fix {len(self.results['syntax_errors'])} syntax errors before proceeding",
                "files": [e["file"] for e in self.results["syntax_errors"][:5]]
            })

        # Based on import errors
        if self.results["import_analysis"].get("errors"):
            missing_modules = set()
            for error in self.results["import_analysis"]["errors"]:
                if "No module named" in error["error"]:
                    module = error["module"].split('.')[0]
                    missing_modules.add(module)

            if missing_modules:
                recommendations.append({
                    "priority": "high",
                    "category": "dependencies",
                    "message": f"Install missing dependencies: {', '.join(list(missing_modules)[:10])}",
                    "modules": list(missing_modules)
                })

        # Based on model issues
        model_issues = 0
        for app_models in self.results["models_analysis"].values():
            for model_data in app_models.values():
                model_issues += len(model_data.get("issues", []))

        if model_issues > 0:
            recommendations.append({
                "priority": "medium",
                "category": "models",
                "message": f"Fix {model_issues} model issues (missing __str__, app_label, etc.)"
            })

        self.results["recommendations"] = recommendations
        print(f"   Generated {len(recommendations)} recommendations")

    def save_results(self):
        """Save analysis results"""
        output_file = self.project_root / ".reports" / "comprehensive_analysis.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)

        print(f"📄 Analysis saved to: {output_file}")
        return output_file

    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE PROJECT ANALYSIS SUMMARY")
        print("=" * 60)

        print("📁 Project Structure:")
        print(f"   - Installed Apps: {len(self.results['installed_apps'])}")
        print(f"   - Python Files: {len(self.results['python_files'])}")
        print(f"   - Test Files: {len(self.results.get('test_files', []))}")

        print("\n🔍 Code Quality:")
        print(f"   - Syntax Errors: {len(self.results['syntax_errors'])}")
        print(f"   - Import Issues: {len(self.results['import_analysis'].get('errors', []))}")
        print(f"   - Static Analysis Issues: {len(self.results.get('static_analysis_errors', []))}")

        print("\n📊 Models Analysis:")
        total_models = sum(len(models) for models in self.results['models_analysis'].values())
        print(f"   - Total Models: {total_models}")
        print(f"   - Apps with Models: {len(self.results['models_analysis'])}")

        print("\n🔒 Security:")
        print(f"   - Security Issues: {len(self.results.get('security_analysis', []))}")

        print("\n📋 Recommendations:")
        for rec in self.results.get('recommendations', []):
            print(f"   [{rec['priority'].upper()}] {rec['message']}")

        if self.results['syntax_errors']:
            print("\n❌ Critical Issues (First 5):")
            for error in self.results['syntax_errors'][:5]:
                print(f"   - {error['file']}:{error.get('line', '?')} - {error['error']}")

        print("\n" + "=" * 60)

    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting Comprehensive Project Analysis...")
        print("=" * 60)

        self.analyze_project_structure()
        self.analyze_syntax_and_imports()
        self.analyze_models()
        self.analyze_api_endpoints()
        self.analyze_security()
        self.generate_recommendations()

        self.print_summary()
        return self.save_results()


if __name__ == "__main__":
    try:
        analyzer = ComprehensiveProjectAnalyzer()
        output_file = analyzer.run_analysis()
        print(f"\n✅ Analysis complete! Check {output_file} for detailed results")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        traceback.print_exc()
        sys.exit(1)
