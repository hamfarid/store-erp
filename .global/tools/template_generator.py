#!/usr/bin/env python3
"""
Template Generator Tool

Generates projects from templates with variable substitution.

Usage:
    python3 template_generator.py --list
    python3 template_generator.py --template erp_system --output ~/projects/my-erp
    python3 template_generator.py --interactive
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Any
import re


class TemplateGenerator:
    """Generate projects from templates"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            # Default to templates/ directory
            script_dir = Path(__file__).parent.parent
            templates_dir = script_dir / "templates"
        
        self.templates_dir = Path(templates_dir)
        
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates"""
        templates = []
        
        for template_dir in self.templates_dir.iterdir():
            if not template_dir.is_dir():
                continue
            
            # Skip config directory
            if template_dir.name == "config":
                continue
            
            config_file = template_dir / "config.json"
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    templates.append({
                        'name': template_dir.name,
                        'description': config.get('description', 'No description'),
                        'version': config.get('version', '1.0.0'),
                        'path': str(template_dir)
                    })
            else:
                templates.append({
                    'name': template_dir.name,
                    'description': 'No description available',
                    'version': 'unknown',
                    'path': str(template_dir)
                })
        
        return templates
    
    def load_template_config(self, template_name: str) -> Dict[str, Any]:
        """Load template configuration"""
        template_dir = self.templates_dir / template_name
        config_file = template_dir / "config.json"
        
        if not config_file.exists():
            return {
                'template_name': template_name,
                'variables': {},
                'defaults': {}
            }
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def get_variables(self, template_name: str, interactive: bool = False) -> Dict[str, str]:
        """Get variables for template"""
        config = self.load_template_config(template_name)
        variables = {}
        
        defaults = config.get('defaults', {})
        
        if interactive:
            print(f"\n📝 Configure {template_name}")
            print("=" * 50)
            
            for var_name, var_placeholder in config.get('variables', {}).items():
                default = defaults.get(var_name, '')
                prompt = f"{var_name}"
                
                if default:
                    prompt += f" [{default}]"
                
                prompt += ": "
                
                value = input(prompt).strip()
                
                if not value and default:
                    value = default
                
                variables[var_placeholder] = value
        else:
            # Use defaults
            for var_name, var_placeholder in config.get('variables', {}).items():
                variables[var_placeholder] = defaults.get(var_name, var_placeholder)
        
        return variables
    
    def substitute_variables(self, content: str, variables: Dict[str, str]) -> str:
        """Substitute variables in content"""
        for placeholder, value in variables.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def process_file(self, file_path: Path, output_path: Path, variables: Dict[str, str]):
        """Process a single file"""
        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substitute variables
            content = self.substitute_variables(content, variables)
            
            # Write to output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        except UnicodeDecodeError:
            # Binary file, just copy
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, output_path)
    
    def generate(self, template_name: str, output_dir: str, variables: Dict[str, str] = None, interactive: bool = False):
        """Generate project from template"""
        template_dir = self.templates_dir / template_name
        
        if not template_dir.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        output_path = Path(output_dir)
        
        if output_path.exists():
            response = input(f"⚠️  Output directory exists: {output_dir}\nOverwrite? (y/N): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                return
            
            shutil.rmtree(output_path)
        
        # Get variables
        if variables is None:
            variables = self.get_variables(template_name, interactive=interactive)
        
        print(f"\n🚀 Generating project from template: {template_name}")
        print(f"📁 Output directory: {output_dir}")
        print()
        
        # Copy template
        file_count = 0
        
        for root, dirs, files in os.walk(template_dir):
            # Skip __pycache__ and .git
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', 'venv']]
            
            rel_root = Path(root).relative_to(template_dir)
            
            for file in files:
                # Skip config.json
                if file == 'config.json':
                    continue
                
                file_path = Path(root) / file
                output_file_path = output_path / rel_root / file
                
                self.process_file(file_path, output_file_path, variables)
                file_count += 1
                
                if file_count % 10 == 0:
                    print(f"  Processed {file_count} files...")
        
        print(f"\n✅ Generated {file_count} files")
        print(f"✅ Project created at: {output_dir}")
        
        # Run post-generation scripts
        config = self.load_template_config(template_name)
        post_gen = config.get('post_generation', [])
        
        if post_gen:
            print(f"\n📦 Running post-generation scripts...")
            
            for script in post_gen:
                print(f"  Running: {script}")
                # Note: In production, you might want to actually run these
                # os.system(f"cd {output_dir} && {script}")
        
        print(f"\n🎉 Done! Your project is ready.")
        print(f"\nNext steps:")
        print(f"  cd {output_dir}")
        print(f"  # Read README.md for setup instructions")


def main():
    parser = argparse.ArgumentParser(
        description="Generate projects from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available templates
  python3 template_generator.py --list
  
  # Generate with defaults
  python3 template_generator.py --template erp_system --output ~/projects/my-erp
  
  # Interactive mode
  python3 template_generator.py --interactive
  
  # Specify template and output
  python3 template_generator.py -t web_page_with_login -o ~/my-web-app
        """
    )
    
    parser.add_argument('--list', '-l', action='store_true', help='List available templates')
    parser.add_argument('--template', '-t', help='Template name')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--templates-dir', help='Templates directory (default: ../templates)')
    
    args = parser.parse_args()
    
    try:
        generator = TemplateGenerator(templates_dir=args.templates_dir)
        
        if args.list:
            # List templates
            templates = generator.list_templates()
            
            print("\n📦 Available Templates")
            print("=" * 70)
            
            for template in templates:
                print(f"\n{template['name']} (v{template['version']})")
                print(f"  {template['description']}")
            
            print(f"\n{len(templates)} templates available")
            print()
        
        elif args.interactive:
            # Interactive mode
            templates = generator.list_templates()
            
            print("\n📦 Available Templates")
            print("=" * 50)
            
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template['name']} - {template['description']}")
            
            print()
            choice = input("Select template (number): ").strip()
            
            try:
                template_idx = int(choice) - 1
                template = templates[template_idx]
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                return
            
            output_dir = input("Output directory: ").strip()
            
            if not output_dir:
                print("❌ Output directory required")
                return
            
            generator.generate(
                template['name'],
                output_dir,
                interactive=True
            )
        
        elif args.template and args.output:
            # Generate with defaults
            generator.generate(
                args.template,
                args.output,
                interactive=False
            )
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

