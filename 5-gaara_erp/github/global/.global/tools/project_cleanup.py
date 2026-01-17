#!/usr/bin/env python3
"""
Project Cleanup - Automated codebase cleanup tool.

This tool:
1. Moves unused files to unneeded/
2. Proposes a plan for merging duplicate files
3. Moves all scripts to tools/
"""

import os
import json
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path.cwd()
DOCS_DIR = PROJECT_ROOT / "docs"
UNNEEDED_DIR = PROJECT_ROOT / "unneeded"
TOOLS_DIR = PROJECT_ROOT / "tools"

class ProjectCleanup:
    def __init__(self):
        self.file_usage = {}
        self.duplicate_files = []
        
    def cleanup(self):
        """Run complete cleanup."""
        print("🧹 Starting project cleanup...")
        self._load_reports()
        self._move_unused_files()
        self._propose_merge_plan()
        self._consolidate_tools()
        print("✅ Cleanup complete!")
        
    def _load_reports(self):
        """Load analysis reports."""
        print("📂 Loading analysis reports...")
        
        with open(DOCS_DIR / "file_usage.json") as f:
            self.file_usage = json.load(f)
            
        with open(DOCS_DIR / "duplicate_files.json") as f:
            self.duplicate_files = json.load(f)
            
    def _move_unused_files(self):
        """Move unused files to unneeded/ directory."""
        print("📦 Moving unused files...")
        UNNEEDED_DIR.mkdir(exist_ok=True)
        
        moved_count = 0
        for file_path, info in self.file_usage.items():
            if not info["used"]:
                source = PROJECT_ROOT / file_path
                if source.exists():
                    # Preserve directory structure
                    rel_path = Path(file_path)
                    dest = UNNEEDED_DIR / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.move(str(source), str(dest))
                    print(f"   Moved: {file_path} → unneeded/{file_path}")
                    moved_count += 1
                    
        print(f"   Moved {moved_count} unused files")
        
    def _propose_merge_plan(self):
        """Propose a plan for merging duplicate files."""
        print("🔀 Proposing merge plan...")
        
        merge_plan = []
        
        for dup_group in self.duplicate_files:
            if dup_group["type"] == "exact":
                # For exact duplicates, keep the first and delete the rest
                files = dup_group["files"]
                merge_plan.append({
                    "action": "delete_duplicates",
                    "keep": files[0],
                    "delete": files[1:]
                })
            elif dup_group["type"] == "similar_name":
                # For similar names, propose manual review
                merge_plan.append({
                    "action": "manual_review",
                    "base_name": dup_group["base_name"],
                    "files": dup_group["files"],
                    "suggestion": f"Review and merge these similar files into one: {dup_group['base_name']}"
                })
                
        # Save merge plan
        with open(DOCS_DIR / "merge_plan.json", "w") as f:
            json.dump(merge_plan, f, indent=2)
            
        print(f"   Merge plan saved to docs/merge_plan.json")
        print(f"   {len(merge_plan)} merge actions proposed")
        
    def _consolidate_tools(self):
        """Move all scripts to tools/ directory."""
        print("🛠️  Consolidating tools...")
        TOOLS_DIR.mkdir(exist_ok=True)
        
        # Find all Python scripts
        script_patterns = ["*fix*.py", "*clean*.py", "*test*.py", "*check*.py"]
        moved_count = 0
        
        for pattern in script_patterns:
            for script in PROJECT_ROOT.rglob(pattern):
                if "tools" not in script.parts and "node_modules" not in script.parts:
                    dest = TOOLS_DIR / script.name
                    if not dest.exists():
                        shutil.move(str(script), str(dest))
                        print(f"   Moved: {script.relative_to(PROJECT_ROOT)} → tools/{script.name}")
                        moved_count += 1
                        
        print(f"   Moved {moved_count} scripts to tools/")

if __name__ == "__main__":
    cleanup = ProjectCleanup()
    cleanup.cleanup()

