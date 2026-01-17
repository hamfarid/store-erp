"""
Helper Manager for Autonomous Multi-Agent System

Manages helper folders (definitions, errors, imports, classes, modules).
"""

from pathlib import Path
from typing import Dict, List, Optional


class HelperManager:
    """Manages helper folders and files"""
    
    def __init__(self):
        """Initialize Helper Manager"""
        self.base_path = Path.home() / ".global" / "helpers"
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Helper folders
        self.folders = {
            "definitions": self.base_path / "definitions",
            "errors": self.base_path / "errors",
            "imports": self.base_path / "imports",
            "classes": self.base_path / "classes",
            "modules": self.base_path / "modules"
        }
        
        # Initialize folders
        self._initialize_folders()
    
    def _initialize_folders(self):
        """Initialize helper folders"""
        for folder in self.folders.values():
            folder.mkdir(exist_ok=True)
            
            # Create __init__.py if it doesn't exist
            init_file = folder / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Helper module"""\n', encoding='utf-8')
    
    def get_definitions(self) -> Dict[str, str]:
        """
        Get all definitions
        
        Returns:
            Dictionary of definitions {name: content}
        """
        definitions = {}
        definitions_dir = self.folders["definitions"]
        
        for file_path in definitions_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                definitions[file_path.stem] = file_path.read_text(encoding='utf-8')
        
        return definitions
    
    def get_error_classes(self) -> Dict[str, str]:
        """
        Get all custom error classes
        
        Returns:
            Dictionary of error classes {name: content}
        """
        errors = {}
        errors_dir = self.folders["errors"]
        
        for file_path in errors_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                errors[file_path.stem] = file_path.read_text(encoding='utf-8')
        
        return errors
    
    def get_imports(self) -> Dict[str, str]:
        """
        Get all common imports
        
        Returns:
            Dictionary of imports {name: content}
        """
        imports = {}
        imports_dir = self.folders["imports"]
        
        for file_path in imports_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                imports[file_path.stem] = file_path.read_text(encoding='utf-8')
        
        return imports
    
    def get_base_classes(self) -> Dict[str, str]:
        """
        Get all base classes
        
        Returns:
            Dictionary of base classes {name: content}
        """
        classes = {}
        classes_dir = self.folders["classes"]
        
        for file_path in classes_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                classes[file_path.stem] = file_path.read_text(encoding='utf-8')
        
        return classes
    
    def get_utility_modules(self) -> Dict[str, str]:
        """
        Get all utility modules
        
        Returns:
            Dictionary of utility modules {name: content}
        """
        modules = {}
        modules_dir = self.folders["modules"]
        
        for file_path in modules_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                modules[file_path.stem] = file_path.read_text(encoding='utf-8')
        
        return modules
    
    def get_all_helpers(self) -> Dict[str, Dict[str, str]]:
        """
        Get all helpers
        
        Returns:
            Dictionary of all helpers organized by type
        """
        return {
            "definitions": self.get_definitions(),
            "errors": self.get_error_classes(),
            "imports": self.get_imports(),
            "classes": self.get_base_classes(),
            "modules": self.get_utility_modules()
        }
    
    def add_definition(self, name: str, content: str):
        """Add a new definition"""
        file_path = self.folders["definitions"] / f"{name}.py"
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Added definition: {name}")
    
    def add_error_class(self, name: str, content: str):
        """Add a new error class"""
        file_path = self.folders["errors"] / f"{name}.py"
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Added error class: {name}")
    
    def add_import(self, name: str, content: str):
        """Add a new import"""
        file_path = self.folders["imports"] / f"{name}.py"
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Added import: {name}")
    
    def add_base_class(self, name: str, content: str):
        """Add a new base class"""
        file_path = self.folders["classes"] / f"{name}.py"
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Added base class: {name}")
    
    def add_utility_module(self, name: str, content: str):
        """Add a new utility module"""
        file_path = self.folders["modules"] / f"{name}.py"
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Added utility module: {name}")
    
    def get_helper_summary(self) -> str:
        """
        Get summary of all helpers
        
        Returns:
            Formatted summary
        """
        helpers = self.get_all_helpers()
        
        summary = "# Helper Files Summary\n\n"
        
        for helper_type, items in helpers.items():
            summary += f"## {helper_type.title()}\n\n"
            if items:
                for name in items.keys():
                    summary += f"- {name}\n"
            else:
                summary += "- (none)\n"
            summary += "\n"
        
        return summary
    
    def __repr__(self):
        helpers = self.get_all_helpers()
        total = sum(len(items) for items in helpers.values())
        return f"HelperManager(total_helpers={total}, path='{self.base_path}')"


if __name__ == "__main__":
    # Test
    helper = HelperManager()
    print(helper.get_helper_summary())
    print(helper)

