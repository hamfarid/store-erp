#!/usr/bin/env python
"""
Generate Mermaid class diagrams for each module and append to existing docs/analysis/modules/*.md files.
Reads from data/*.json and adds class diagrams showing relationships between classes.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MODULES_DIR = ROOT / "docs" / "analysis" / "modules"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_class_diagram(module_data: Dict[str, Any]) -> str:
    """Generate Mermaid class diagram for a module."""
    classes = module_data.get("classes", [])
    if not classes:
        return ""
    
    lines = ["", "## Class Diagram", "", "```mermaid", "classDiagram"]
    
    # Define classes
    for cls in classes:
        class_name = cls.get("name", "Unknown")
        methods = cls.get("methods", [])
        variables = cls.get("variables", [])
        
        lines.append(f"    class {class_name} {{")
        
        # Add variables (attributes)
        for var in variables[:5]:  # Limit to first 5 to avoid clutter
            lines.append(f"        +{var}")
        if len(variables) > 5:
            lines.append(f"        +... ({len(variables) - 5} more)")
            
        # Add methods
        for method in methods[:5]:  # Limit to first 5
            lines.append(f"        +{method}()")
        if len(methods) > 5:
            lines.append(f"        +... ({len(methods) - 5} more)")
            
        lines.append("    }")
    
    # Add relationships (simple inheritance detection)
    for cls in classes:
        class_name = cls.get("name", "Unknown")
        # Look for common inheritance patterns
        if "Meta" in class_name:
            continue
        # Simple heuristic: if there's a Meta class, it's related to the main class
        for other_cls in classes:
            other_name = other_cls.get("name", "Unknown")
            if other_name == "Meta" and class_name != "Meta":
                lines.append(f"    {class_name} --> {other_name}")
    
    lines.append("```")
    return "\n".join(lines)


def update_module_file(module_name: str, module_data: Dict[str, Any]) -> None:
    """Update a module markdown file with class diagram."""
    module_file = MODULES_DIR / f"{module_name}.md"
    if not module_file.exists():
        return
    
    # Read existing content
    content = module_file.read_text(encoding="utf-8")
    
    # Check if class diagram already exists
    if "## Class Diagram" in content:
        return  # Skip if already has diagram
    
    # Generate diagram
    diagram = generate_class_diagram(module_data)
    if not diagram:
        return  # Skip if no classes
    
    # Append diagram to file
    updated_content = content.rstrip() + "\n" + diagram + "\n"
    module_file.write_text(updated_content, encoding="utf-8")


def main():
    """Process all modules and add class diagrams."""
    if not MODULES_DIR.exists():
        print("Modules directory not found. Run merge_analysis_to_md.py first.")
        return
    
    # Load all module data
    module_data = {}
    for json_file in DATA.glob("**/*.json"):
        if json_file.name in {"all_modules.json", "module_graph.json", "accurate_test_verification.json"}:
            continue
        try:
            data = load_json(json_file)
            module_name = data.get("module") or data.get("name")
            if not module_name:
                # Derive from filename
                rel_path = json_file.relative_to(DATA)
                module_name = str(rel_path).replace("/", ".").replace("\\", ".").rsplit(".", 1)[0]
            module_data[module_name] = data
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            continue
    
    # Update module files
    updated_count = 0
    for module_name, data in module_data.items():
        try:
            update_module_file(module_name, data)
            updated_count += 1
            if updated_count % 100 == 0:
                print(f"Processed {updated_count} modules...")
        except Exception as e:
            print(f"Error updating {module_name}: {e}")
    
    print(f"Updated {updated_count} module files with class diagrams.")


if __name__ == "__main__":
    main()
