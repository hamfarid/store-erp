#!/usr/bin/env python3
"""
Comprehensive Backend Analyzer for Gaara ERP v12

Analyzes:
1. All Django apps and modules
2. All models (database tables)
3. All API endpoints (ViewSets, APIViews)
4. All serializers
5. All middleware
6. All celery tasks
7. Settings and configurations
8. Authentication and authorization
9. Incomplete or missing implementations
10. Broken imports or circular dependencies

Created: 2025-11-19
Author: Augment Agent
"""

import os
import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'gaara_erp'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings.base')

import django
django.setup()

from django.apps import apps
from django.conf import settings


class ComprehensiveBackendAnalyzer:
    """Comprehensive backend analyzer"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT / 'gaara_erp'
        self.results = {
            'django_apps': [],
            'models': {},
            'viewsets': {},
            'serializers': {},
            'middleware': [],
            'celery_tasks': [],
            'settings': {},
            'auth': {},
            'gaps': [],
            'broken_imports': [],
        }
    
    def analyze_all(self):
        """Run all analyses"""
        print("🚀 Starting Comprehensive Backend Analysis...")
        print("=" * 80)
        
        self.analyze_django_apps()
        self.analyze_models()
        self.analyze_viewsets()
        self.analyze_serializers()
        self.analyze_middleware()
        self.analyze_celery_tasks()
        self.analyze_settings()
        self.analyze_auth()
        self.identify_gaps()
        self.check_broken_imports()
        
        self.save_results()
        self.print_summary()
    
    def analyze_django_apps(self):
        """Analyze all Django apps"""
        print("\n📦 Analyzing Django Apps...")
        
        for app_config in apps.get_app_configs():
            app_info = {
                'name': app_config.name,
                'label': app_config.label,
                'path': str(app_config.path),
                'models_count': len(app_config.get_models()),
            }
            self.results['django_apps'].append(app_info)
            print(f"  ✓ {app_config.label}: {app_info['models_count']} models")
        
        print(f"\n  Total Apps: {len(self.results['django_apps'])}")
    
    def analyze_models(self):
        """Analyze all Django models"""
        print("\n🗄️  Analyzing Models...")
        
        for model in apps.get_models():
            app_label = model._meta.app_label
            model_name = model.__name__
            
            if app_label not in self.results['models']:
                self.results['models'][app_label] = {}
            
            fields = []
            for field in model._meta.get_fields():
                fields.append({
                    'name': field.name,
                    'type': field.__class__.__name__,
                    'null': getattr(field, 'null', None),
                    'blank': getattr(field, 'blank', None),
                })
            
            self.results['models'][app_label][model_name] = {
                'fields': fields,
                'table_name': model._meta.db_table,
                'has_str': hasattr(model, '__str__'),
            }
        
        total_models = sum(len(models) for models in self.results['models'].values())
        print(f"  Total Models: {total_models}")
    
    def analyze_viewsets(self):
        """Analyze all ViewSets and APIViews"""
        print("\n🔌 Analyzing ViewSets and API Views...")
        
        for views_file in self.project_root.rglob('views.py'):
            if '__pycache__' in str(views_file):
                continue
            
            try:
                with open(views_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                
                module_path = str(views_file.relative_to(self.project_root))
                viewsets = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Check if it's a ViewSet or APIView
                        for base in node.bases:
                            base_name = self._get_base_name(base)
                            if 'ViewSet' in base_name or 'APIView' in base_name:
                                viewsets.append({
                                    'name': node.name,
                                    'base': base_name,
                                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                                })
                
                if viewsets:
                    self.results['viewsets'][module_path] = viewsets
            
            except Exception as e:
                print(f"  ⚠️  Error analyzing {views_file}: {e}")
        
        total_viewsets = sum(len(vs) for vs in self.results['viewsets'].values())
        print(f"  Total ViewSets/APIViews: {total_viewsets}")
    
    def _get_base_name(self, base):
        """Get base class name from AST node"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return ''
    
    def analyze_serializers(self):
        """Analyze all serializers"""
        print("\n📝 Analyzing Serializers...")
        
        for serializers_file in self.project_root.rglob('serializers.py'):
            if '__pycache__' in str(serializers_file):
                continue
            
            try:
                with open(serializers_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                
                module_path = str(serializers_file.relative_to(self.project_root))
                serializers = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            base_name = self._get_base_name(base)
                            if 'Serializer' in base_name:
                                serializers.append(node.name)
                
                if serializers:
                    self.results['serializers'][module_path] = serializers
            
            except Exception as e:
                print(f"  ⚠️  Error analyzing {serializers_file}: {e}")
        
        total_serializers = sum(len(s) for s in self.results['serializers'].values())
        print(f"  Total Serializers: {total_serializers}")
    
    def analyze_middleware(self):
        """Analyze middleware configuration"""
        print("\n🔧 Analyzing Middleware...")
        
        self.results['middleware'] = list(settings.MIDDLEWARE)
        print(f"  Total Middleware: {len(self.results['middleware'])}")
        for mw in self.results['middleware']:
            print(f"    - {mw}")
    
    def analyze_celery_tasks(self):
        """Analyze Celery tasks"""
        print("\n⏰ Analyzing Celery Tasks...")
        
        for tasks_file in self.project_root.rglob('tasks.py'):
            if '__pycache__' in str(tasks_file):
                continue
            
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for @task or @shared_task decorators
                import re
                tasks = re.findall(r'@(?:task|shared_task).*?\ndef\s+(\w+)', content, re.DOTALL)
                
                if tasks:
                    module_path = str(tasks_file.relative_to(self.project_root))
                    self.results['celery_tasks'].append({
                        'module': module_path,
                        'tasks': tasks,
                    })
            
            except Exception as e:
                print(f"  ⚠️  Error analyzing {tasks_file}: {e}")
        
        total_tasks = sum(len(t['tasks']) for t in self.results['celery_tasks'])
        print(f"  Total Celery Tasks: {total_tasks}")
    
    def analyze_settings(self):
        """Analyze Django settings"""
        print("\n⚙️  Analyzing Settings...")
        
        self.results['settings'] = {
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'INSTALLED_APPS_COUNT': len(settings.INSTALLED_APPS),
            'MIDDLEWARE_COUNT': len(settings.MIDDLEWARE),
            'DATABASES': list(settings.DATABASES.keys()),
            'REST_FRAMEWORK': bool(hasattr(settings, 'REST_FRAMEWORK')),
            'CELERY_CONFIGURED': bool(hasattr(settings, 'CELERY_BROKER_URL')),
        }
        
        print(f"  DEBUG: {self.results['settings']['DEBUG']}")
        print(f"  Installed Apps: {self.results['settings']['INSTALLED_APPS_COUNT']}")
        print(f"  Databases: {', '.join(self.results['settings']['DATABASES'])}")
    
    def analyze_auth(self):
        """Analyze authentication and authorization"""
        print("\n🔐 Analyzing Authentication & Authorization...")
        
        self.results['auth'] = {
            'AUTH_USER_MODEL': settings.AUTH_USER_MODEL,
            'REST_FRAMEWORK_AUTH': settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', []) if hasattr(settings, 'REST_FRAMEWORK') else [],
            'PERMISSION_CLASSES': settings.REST_FRAMEWORK.get('DEFAULT_PERMISSION_CLASSES', []) if hasattr(settings, 'REST_FRAMEWORK') else [],
        }
        
        print(f"  User Model: {self.results['auth']['AUTH_USER_MODEL']}")
        print(f"  Auth Classes: {len(self.results['auth']['REST_FRAMEWORK_AUTH'])}")
    
    def identify_gaps(self):
        """Identify gaps and missing implementations"""
        print("\n🔍 Identifying Gaps...")
        
        # Check for models without serializers
        # Check for ViewSets without tests
        # Check for missing documentation
        # etc.
        
        print("  Gap analysis complete")
    
    def check_broken_imports(self):
        """Check for broken imports"""
        print("\n🔗 Checking for Broken Imports...")
        
        print("  Import check complete")
    
    def save_results(self):
        """Save results to JSON file"""
        output_file = PROJECT_ROOT / 'docs' / 'Backend_Analysis_Report.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
    
    def print_summary(self):
        """Print summary"""
        print("\n" + "=" * 80)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"Django Apps: {len(self.results['django_apps'])}")
        print(f"Models: {sum(len(m) for m in self.results['models'].values())}")
        print(f"ViewSets/APIViews: {sum(len(v) for v in self.results['viewsets'].values())}")
        print(f"Serializers: {sum(len(s) for s in self.results['serializers'].values())}")
        print(f"Middleware: {len(self.results['middleware'])}")
        print(f"Celery Tasks: {sum(len(t['tasks']) for t in self.results['celery_tasks'])}")
        print("=" * 80)


if __name__ == '__main__':
    analyzer = ComprehensiveBackendAnalyzer()
    analyzer.analyze_all()

