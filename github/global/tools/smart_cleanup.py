#!/usr/bin/env python3
"""
Smart Cleanup Tool - Intelligently identifies safe-to-delete files
Part of PROMPT 84: PROJECT ANALYSIS & CLEANUP
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Set

class SmartCleanup:
    def __init__(self, analysis_file: str):
        self.analysis_file = Path(analysis_file)
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        
        # Safe to delete patterns
        self.safe_patterns = {
            'archive': ['archive', 'backup', 'old', 'deprecated'],
            'test_scripts': ['test_', 'check_', 'verify_', 'debug_'],
            'temp': ['temp', 'tmp', '.pyc', '__pycache__'],
            'duplicates': []  # Will be filled from analysis
        }
        
        # Never delete patterns (critical files)
        self.critical_patterns = {
            'app.py', 'main.py', 'index.js', 'index.tsx', 'index.html',
            'package.json', 'requirements.txt', 'config.py', 'settings.py',
            '__init__.py'  # Keep all __init__.py for now
        }
        
        # Directories that are safe to delete entirely
        self.safe_dirs = {
            'database_archive', 'scripts_archive', '__pycache__',
            'playwright-report', 'test-results', '.pytest_cache'
        }
    
    def categorize_files(self) -> Dict[str, List[str]]:
        """Categorize files into safe/unsafe to delete"""
        categories = {
            'safe_archive': [],
            'safe_test_scripts': [],
            'safe_duplicates': [],
            'safe_temp': [],
            'unsafe_routes': [],
            'unsafe_services': [],
            'unsafe_components': [],
            'review_needed': []
        }
        
        unused = self.analysis.get('unused_files', [])
        
        for file in unused:
            file_lower = file.lower()
            file_name = Path(file).name
            
            # Skip critical files
            if file_name in self.critical_patterns:
                continue
            
            # Archive files
            if any(pattern in file_lower for pattern in self.safe_patterns['archive']):
                categories['safe_archive'].append(file)
            
            # Test/debug scripts
            elif any(file_name.startswith(pattern) for pattern in self.safe_patterns['test_scripts']):
                categories['safe_test_scripts'].append(file)
            
            # Routes (need review - might be registered as blueprints)
            elif 'routes' in file_lower and file.endswith('.py'):
                categories['unsafe_routes'].append(file)
            
            # Services (need review - might be used dynamically)
            elif 'services' in file_lower or 'service' in file_lower:
                categories['unsafe_services'].append(file)
            
            # Components (need review - might be lazy loaded)
            elif any(ext in file for ext in ['.jsx', '.tsx', '.js', '.ts']):
                categories['unsafe_components'].append(file)
            
            # Everything else needs review
            else:
                categories['review_needed'].append(file)
        
        # Add duplicates
        for hash_val, files in self.analysis.get('duplicates', {}).items():
            if len(files) > 1:
                # Keep first, mark rest as safe to delete
                categories['safe_duplicates'].extend(files[1:])
        
        return categories
    
    def generate_cleanup_plan(self) -> Dict:
        """Generate a cleanup plan with safety levels"""
        categories = self.categorize_files()
        
        plan = {
            'high_confidence': {
                'description': 'Safe to delete (archives, backups, test scripts)',
                'files': categories['safe_archive'] + categories['safe_test_scripts'] + categories['safe_temp'],
                'count': len(categories['safe_archive']) + len(categories['safe_test_scripts']) + len(categories['safe_temp'])
            },
            'medium_confidence': {
                'description': 'Duplicates (keep one copy)',
                'files': categories['safe_duplicates'],
                'count': len(categories['safe_duplicates'])
            },
            'needs_review': {
                'description': 'Requires manual review before deletion',
                'routes': categories['unsafe_routes'],
                'services': categories['unsafe_services'],
                'components': categories['unsafe_components'],
                'other': categories['review_needed'],
                'count': len(categories['unsafe_routes']) + len(categories['unsafe_services']) + 
                         len(categories['unsafe_components']) + len(categories['review_needed'])
            },
            'summary': {
                'total_unused': len(self.analysis.get('unused_files', [])),
                'safe_to_delete': len(categories['safe_archive']) + len(categories['safe_test_scripts']) + 
                                  len(categories['safe_temp']) + len(categories['safe_duplicates']),
                'needs_review': len(categories['unsafe_routes']) + len(categories['unsafe_services']) + 
                               len(categories['unsafe_components']) + len(categories['review_needed'])
            }
        }
        
        return plan

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python smart_cleanup.py <analysis.json> <output_plan.json>")
        sys.exit(1)
    
    cleanup = SmartCleanup(sys.argv[1])
    plan = cleanup.generate_cleanup_plan()
    
    # Save plan
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Cleanup plan generated: {sys.argv[2]}")
    print(f"\n📊 Summary:")
    print(f"  Total unused files: {plan['summary']['total_unused']}")
    print(f"  Safe to delete: {plan['summary']['safe_to_delete']}")
    print(f"  Needs review: {plan['summary']['needs_review']}")

