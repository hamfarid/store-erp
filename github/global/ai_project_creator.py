#!/usr/bin/env python3
"""
AI Project Creator Wizard (The Maestro) v5.0 - Diamond 33 Edition

Usage:
    python3 ai_project_creator.py                  # Interactive wizard
    python3 ai_project_creator.py --auto           # Non-interactive
    python3 ai_project_creator.py --audit          # Subsystem audit
    python3 ai_project_creator.py --tasks          # Task menu
    python3 ai_project_creator.py --tasks add "Fix bug" --priority high
    python3 ai_project_creator.py --tasks add "Sub" --parent 2
    python3 ai_project_creator.py --tasks add "After X" --depends-on 3
    python3 ai_project_creator.py --tasks export markdown
    python3 ai_project_creator.py --tasks export csv
    python3 ai_project_creator.py --status         # Project health
    python3 ai_project_creator.py --rollback       # Restore pre-injection snapshot
    python3 ai_project_creator.py --git-init       # Initialize git + first commit
    python3 ai_project_creator.py --watch 5        # Health check every 5 minutes
    python3 ai_project_creator.py --plugins        # List loaded plugins
"""

import os
import sys
import shutil
import subprocess
import json
import re
import argparse
import datetime
import time
import importlib.util
import hashlib
import csv as csv_module
import io
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

GLOBAL_REPO_URL = "https://github.com/hamfarid/Global-System-Ai-Project-Creators.git"
WIZARD_VERSION = "5.0"
SYSTEM_VERSION = "v26.0.2 Diamond 33"
TASKS_FILE = "tasks.json"
CONFIG_FILE = "creator_config.json"
SNAPSHOT_DIR = ".creator_snapshots"
PLUGINS_DIR = "plugins"

DIAMOND33_CRITICAL_FILES = [
    "config/hallucination-memory-config.yaml",
    "knowledge/core/INDEX-trustworthy-ai-subsystem.md",
    "rules/RULES-verification-pipeline.md",
    "rules/RULES-context-integrity.md",
    "rules/99-anti-hallucination.md",
    "roles/ROLE-truth-guardian.md",
    "roles/ROLE-memory-guardian.md",
    "roles/ROLE-context-engineer.md",
    "workflows/18_anti_hallucination_pipeline.md",
    "workflows/19_memory_lifecycle.md",
    "workflows/20_context_engineering.md",
    "docs/RUNBOOK-hallucination-incident.md",
    "memory-bank/activeContext.md",
    "memory-bank/projectBrief.md",
    "CLAUDE.md",
]

MEMORY_BANK_CORE_FILES = [
    "activeContext.md", "projectBrief.md", "progress.md",
    "decisionLog.md", "lessons_learned.md", "systemPatterns.md", "techContext.md",
]

GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# System
.DS_Store
Thumbs.db

# Project
.vector_db/
.creator_snapshots/
*.sqlite3
node_modules/
"""

# ==================================================================
# Utilities
# ==================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

class StatusTracker:
    def __init__(self):
        self.steps = []

    def ok(self, step, detail=""):
        self.steps.append(("OK", step, detail))

    def warn(self, step, detail=""):
        self.steps.append(("WARN", step, detail))

    def fail(self, step, detail=""):
        self.steps.append(("FAIL", step, detail))

    def skip(self, step, detail=""):
        self.steps.append(("SKIP", step, detail))

    def print_report(self):
        ok_c = sum(1 for s in self.steps if s[0] == "OK")
        warn_c = sum(1 for s in self.steps if s[0] == "WARN")
        fail_c = sum(1 for s in self.steps if s[0] == "FAIL")
        skip_c = sum(1 for s in self.steps if s[0] == "SKIP")
        print(f"\n{Colors.BOLD}{'=' * 60}")
        print(f"  Final Status ({ok_c} OK / {warn_c} WARN / {fail_c} FAIL / {skip_c} SKIP)")
        print(f"{'=' * 60}{Colors.ENDC}")
        icons = {"OK": f"{Colors.GREEN}  OK", "WARN": f"{Colors.WARNING}WARN",
                 "FAIL": f"{Colors.FAIL}FAIL", "SKIP": f"{Colors.DIM}SKIP"}
        for st, step, detail in self.steps:
            icon = icons[st]
            sfx = f" -- {detail}" if detail else ""
            print(f"  [{icon}{Colors.ENDC}] {step}{sfx}")
        print()

def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("+" + "=" * 62 + "+")
    print(f"|     AI Project Creator Wizard (The Maestro) v{WIZARD_VERSION}              |")
    print(f"|   Global System {SYSTEM_VERSION} | Trustworthy AI Ready     |")
    print("|   Plugins - Tasks - Rollback - Git - Watch - Automation     |")
    print("+" + "=" * 62 + "+")
    print(f"{Colors.ENDC}")

def get_input(prompt, default=None, auto_mode=False):
    if auto_mode and default is not None:
        print(f"{Colors.DIM}  [auto] {prompt}: {default}{Colors.ENDC}")
        return default
    if default:
        user_input = input(f"  {Colors.BOLD}{prompt} [{default}]: {Colors.ENDC}")
        return user_input.strip() or default
    return input(f"  {Colors.BOLD}{prompt}: {Colors.ENDC}").strip()

def run_command(command, cwd=None, shell=True, timeout=120):
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell,
                                capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def safe_write(path, content, overwrite=False):
    if os.path.exists(path) and not overwrite:
        if os.path.getsize(path) > 50:
            return False
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def ensure_yaml():
    global HAS_YAML
    if HAS_YAML:
        return True
    print(f"{Colors.WARNING}  PyYAML not found. Installing...{Colors.ENDC}")
    ok, _, _ = run_command(f"{sys.executable} -m pip install pyyaml -q")
    if ok:
        try:
            import yaml as _y
            HAS_YAML = True
            return True
        except ImportError:
            pass
    print(f"{Colors.FAIL}  Install failed. Run: pip install pyyaml{Colors.ENDC}")
    return False

def copy_roles_to_platform(project_path, target_dir):
    roles_src = os.path.join(project_path, "roles")
    if not os.path.exists(roles_src):
        return
    os.makedirs(target_dir, exist_ok=True)
    for item in os.listdir(roles_src):
        if item.endswith(".md"):
            shutil.copy2(os.path.join(roles_src, item), target_dir)

# ==================================================================
# [FEATURE 3] Project Config File
# ==================================================================

class ProjectConfig:
    """Reads creator_config.json for default preferences."""
    DEFAULTS = {
        "repo_url": GLOBAL_REPO_URL,
        "default_platform": "1",
        "default_priority": "medium",
        "auto_git_init": False,
        "auto_generate_tasks": True,
        "enable_rag": True,
        "enable_mcp": True,
        "enable_reviewer": True,
        "watch_interval_minutes": 5,
        "plugins_enabled": True,
    }

    def __init__(self, project_path):
        self.path = os.path.join(project_path, CONFIG_FILE)
        self.data = dict(self.DEFAULTS)
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    user = json.load(f)
                self.data.update(user)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key, fallback=None):
        return self.data.get(key, fallback)

    def save_defaults(self, project_path):
        """Creates a default config file if none exists."""
        cfg_path = os.path.join(project_path, CONFIG_FILE)
        if not os.path.exists(cfg_path):
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULTS, f, indent=2, ensure_ascii=False)
            return True
        return False

# ==================================================================
# [FEATURE 1] Snapshot & Rollback
# ==================================================================

def create_snapshot(project_path):
    """Creates a timestamped snapshot of the project before injection."""
    snap_dir = os.path.join(project_path, SNAPSHOT_DIR)
    os.makedirs(snap_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_name = f"snapshot_{ts}"
    snap_path = os.path.join(snap_dir, snap_name)

    manifest = {}
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in {".git", SNAPSHOT_DIR, "__pycache__", "node_modules"}]
        for fn in files:
            fp = os.path.join(root, fn)
            rp = os.path.relpath(fp, project_path)
            try:
                with open(fp, "rb") as f:
                    h = hashlib.md5(f.read()).hexdigest()
                manifest[rp] = {"hash": h, "size": os.path.getsize(fp)}
            except (IOError, PermissionError):
                pass

    os.makedirs(snap_path, exist_ok=True)
    with open(os.path.join(snap_path, "manifest.json"), "w") as f:
        json.dump({"timestamp": ts, "file_count": len(manifest), "files": manifest}, f, indent=2)

    # Copy actual files for restoration
    for rp in manifest:
        src = os.path.join(project_path, rp)
        dst = os.path.join(snap_path, "files", rp)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.copy2(src, dst)
        except (IOError, PermissionError):
            pass

    print(f"{Colors.GREEN}  Snapshot created: {snap_name} ({len(manifest)} files){Colors.ENDC}")
    return snap_path

def list_snapshots(project_path):
    """Lists available snapshots."""
    snap_dir = os.path.join(project_path, SNAPSHOT_DIR)
    if not os.path.exists(snap_dir):
        print(f"  {Colors.DIM}No snapshots found.{Colors.ENDC}")
        return []
    snaps = sorted([d for d in os.listdir(snap_dir) if d.startswith("snapshot_")])
    if not snaps:
        print(f"  {Colors.DIM}No snapshots found.{Colors.ENDC}")
        return []
    print(f"\n{Colors.BOLD}  Available Snapshots:{Colors.ENDC}")
    for i, s in enumerate(snaps, 1):
        mp = os.path.join(snap_dir, s, "manifest.json")
        info = ""
        if os.path.exists(mp):
            with open(mp) as f:
                m = json.load(f)
            info = f" ({m.get('file_count', '?')} files)"
        ts = s.replace("snapshot_", "").replace("_", " at ")
        print(f"    {i}. {ts}{info}")
    return snaps

def rollback_snapshot(project_path, snap_name=None):
    """Restores project from a snapshot."""
    snaps = list_snapshots(project_path)
    if not snaps:
        return False
    try:
        choice = int(input(f"\n  {Colors.BOLD}Restore which snapshot? (number): {Colors.ENDC}")) - 1
        snap_name = snaps[choice]
    except (ValueError, IndexError):
        print(f"{Colors.FAIL}  Invalid choice.{Colors.ENDC}")
        return False

    snap_path = os.path.join(project_path, SNAPSHOT_DIR, snap_name, "files")
    if not os.path.exists(snap_path):
        print(f"{Colors.FAIL}  Snapshot data not found.{Colors.ENDC}")
        return False

    confirm = input(f"  {Colors.WARNING}This will overwrite current files. Continue? (y/n): {Colors.ENDC}").strip()
    if confirm.lower() != "y":
        print("  Cancelled.")
        return False

    restored = 0
    for root, dirs, files in os.walk(snap_path):
        for fn in files:
            src = os.path.join(root, fn)
            rp = os.path.relpath(src, snap_path)
            dst = os.path.join(project_path, rp)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            restored += 1

    print(f"{Colors.GREEN}  Restored {restored} files from {snap_name}{Colors.ENDC}")
    return True

# ==================================================================
# [FEATURE 2] Plugin System
# ==================================================================

class PluginManager:
    """Discovers and loads plugins from plugins/ directory."""
    def __init__(self, project_path):
        self.project_path = project_path
        self.plugins_dir = os.path.join(project_path, PLUGINS_DIR)
        self.plugins = []
        self._discover()

    def _discover(self):
        if not os.path.exists(self.plugins_dir):
            return
        for fn in sorted(os.listdir(self.plugins_dir)):
            if fn.endswith(".py") and not fn.startswith("_"):
                self._load_plugin(fn)

    def _load_plugin(self, filename):
        fp = os.path.join(self.plugins_dir, filename)
        name = filename[:-3]
        try:
            spec = importlib.util.spec_from_file_location(name, fp)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            info = {
                "name": getattr(module, "PLUGIN_NAME", name),
                "version": getattr(module, "PLUGIN_VERSION", "1.0"),
                "description": getattr(module, "PLUGIN_DESCRIPTION", ""),
                "module": module,
                "file": filename,
            }
            self.plugins.append(info)
        except Exception as e:
            print(f"{Colors.WARNING}  Plugin {filename} failed to load: {e}{Colors.ENDC}")

    def list_plugins(self):
        if not self.plugins:
            print(f"\n  {Colors.DIM}No plugins found. Add .py files to {PLUGINS_DIR}/{Colors.ENDC}")
            return
        print(f"\n{Colors.BOLD}  Loaded Plugins:{Colors.ENDC}")
        for p in self.plugins:
            desc = f" -- {p['description']}" if p['description'] else ""
            print(f"    - {p['name']} v{p['version']}{desc} ({p['file']})")

    def run_hook(self, hook_name, **kwargs):
        """Calls a hook function in all plugins that define it."""
        results = []
        for p in self.plugins:
            fn = getattr(p["module"], hook_name, None)
            if callable(fn):
                try:
                    result = fn(**kwargs)
                    results.append((p["name"], result))
                except Exception as e:
                    print(f"{Colors.WARNING}  Plugin {p['name']}.{hook_name} error: {e}{Colors.ENDC}")
        return results

    def ensure_dir(self):
        """Creates plugins directory with a template if it doesn't exist."""
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir, exist_ok=True)
            template = (
                '"""Example Plugin for AI Project Creator"""\n\n'
                'PLUGIN_NAME = "example"\n'
                'PLUGIN_VERSION = "1.0"\n'
                'PLUGIN_DESCRIPTION = "Template plugin"\n\n\n'
                'def on_project_created(project_path, project_name, **kwargs):\n'
                '    """Called after project creation."""\n'
                '    pass\n\n\n'
                'def on_task_added(task, **kwargs):\n'
                '    """Called when a task is added."""\n'
                '    pass\n\n\n'
                'def on_wizard_complete(project_path, status, **kwargs):\n'
                '    """Called at the end of the wizard."""\n'
                '    pass\n'
            )
            with open(os.path.join(self.plugins_dir, "_example_plugin.py"), "w") as f:
                f.write(template)
            return True
        return False

# ==================================================================
# Task & Sub-Task Management (Enhanced: Dependencies + Export)
# ==================================================================

class TaskManager:
    PRIORITIES = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    STATUSES = ["todo", "in_progress", "done", "blocked"]

    def __init__(self, project_path):
        self.project_path = project_path
        self.tasks_file = os.path.join(project_path, TASKS_FILE)
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"version": WIZARD_VERSION, "tasks": [], "next_id": 1}

    def _save(self):
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def _find_task(self, task_id):
        for t in self.data["tasks"]:
            if t["id"] == task_id:
                return t
        return None

    def _check_dependencies(self, task):
        """Returns list of unmet dependency IDs."""
        deps = task.get("depends_on", [])
        unmet = []
        for dep_id in deps:
            dep = self._find_task(dep_id)
            if not dep or dep["status"] != "done":
                unmet.append(dep_id)
        return unmet

    def _sync_to_memory_bank(self):
        """Syncs tasks to memory-bank/activeContext.md (Placeholder)."""
        pass

    def add_task(self, title, priority="medium", parent_id=None, depends_on=None, description=""):
        task = {
            "id": self.data["next_id"], "title": title, "description": description,
            "priority": priority if priority in self.PRIORITIES else "medium",
            "status": "todo", "parent_id": parent_id, "subtasks": [],
            "depends_on": depends_on or [],
            "created": self._now(), "updated": self._now(), "completed": None,
        }
        if parent_id:
            parent = self._find_task(parent_id)
            if parent:
                parent["subtasks"].append(task["id"])
            else:
                print(f"{Colors.FAIL}  Parent #{parent_id} not found.{Colors.ENDC}")
                return None
        self.data["tasks"].append(task)
        self.data["next_id"] += 1
        self._save()
        self._sync_to_memory_bank()
        return task

    def complete_task(self, task_id):
        task = self._find_task(task_id)
        if not task:
            print(f"{Colors.FAIL}  Task #{task_id} not found.{Colors.ENDC}")
            return False
        
        unmet = self._check_dependencies(task)
        if unmet:
            print(f"{Colors.WARNING}  Cannot complete #{task_id}. Unmet dependencies: {unmet}{Colors.ENDC}")
            return False

        task["status"] = "done"
        task["completed"] = self._now()
        task["updated"] = self._now()
        for sid in task.get("subtasks", []):
            self.complete_task(sid)
        self._save()
        self._sync_to_memory_bank()
        print(f"{Colors.GREEN}  Task #{task_id} completed: {task['title']}{Colors.ENDC}")
        return True

    def update_status(self, task_id, new_status):
        if new_status not in self.STATUSES:
            print(f"{Colors.FAIL}  Invalid. Use: {', '.join(self.STATUSES)}{Colors.ENDC}")
            return False
        task = self._find_task(task_id)
        if not task:
            print(f"{Colors.FAIL}  Task #{task_id} not found.{Colors.ENDC}")
            return False
        task["status"] = new_status
        task["updated"] = self._now()
        if new_status == "done":
            task["completed"] = self._now()
        self._save()
        self._sync_to_memory_bank()
        return True

    def remove_task(self, task_id):
        task = self._find_task(task_id)
        if not task:
            print(f"{Colors.FAIL}  Task #{task_id} not found.{Colors.ENDC}")
            return False
        for sid in task.get("subtasks", []):
            self.remove_task(sid)
        if task.get("parent_id"):
            parent = self._find_task(task["parent_id"])
            if parent and task_id in parent.get("subtasks", []):
                parent["subtasks"].remove(task_id)
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        self._save()
        self._sync_to_memory_bank()
        print(f"{Colors.GREEN}  Task #{task_id} removed: {task['title']}{Colors.ENDC}")
        return True

    def list_tasks(self, show_done=False):
        if not self.data["tasks"]:
            print(f"\n  {Colors.DIM}No tasks. Add: --tasks add \"title\"{Colors.ENDC}")
            return
        top = [t for t in self.data["tasks"]
               if not t.get("parent_id") and (show_done or t["status"] != "done")]
        top.sort(key=lambda t: (self.PRIORITIES.get(t["priority"], 9), t["id"]))
        pi = {"critical": "[!!!!]", "high": "[!!! ]", "medium": "[!!  ]", "low": "[!   ]"}
        si = {"todo": "[ ]", "in_progress": "[~]", "done": "[x]", "blocked": "[#]"}
        print(f"\n{Colors.BOLD}  Task List -- {self._now()}{Colors.ENDC}")
        print(f"  {'-' * 55}")
        for t in top:
            c = Colors.GREEN if t["status"] == "done" else \
                Colors.FAIL if t["status"] == "blocked" else \
                Colors.BLUE if t["status"] == "in_progress" else ""
            deps = f" (deps: {t['depends_on']})" if t.get("depends_on") else ""
            print(f"  {si.get(t['status'],'[ ]')} {pi.get(t['priority'],'[?]')} "
                  f"#{t['id']:<3d} {c}{t['title']}{Colors.ENDC}{deps}")
            for sid in t.get("subtasks", []):
                sub = self._find_task(sid)
                if sub and (show_done or sub["status"] != "done"):
                    sc = Colors.GREEN if sub["status"] == "done" else \
                         Colors.FAIL if sub["status"] == "blocked" else ""
                    print(f"       {si.get(sub['status'],'[ ]')}  #{sub['id']:<3d} "
                          f"{sc}-> {sub['title']}{Colors.ENDC}")
        total = len(self.data["tasks"])
        print(f"  {'-' * 55}")
        print(f"  Total: {total} tasks\n")

    def export_tasks(self, format_type="markdown"):
        if format_type == "markdown":
            print(f"\n# Task Export ({self._now()})\n")
            for t in self.data["tasks"]:
                print(f"- [{'x' if t['status']=='done' else ' '}] {t['title']} (#{t['id']})")
        elif format_type == "csv":
            output = io.StringIO()
            writer = csv_module.writer(output)
            writer.writerow(["ID", "Title", "Status", "Priority", "Parent", "DependsOn"])
            for t in self.data["tasks"]:
                writer.writerow([t["id"], t["title"], t["status"], t["priority"], 
                                 t.get("parent_id",""), ",".join(map(str, t.get("depends_on",[])))])
            print(output.getvalue())

    def generate_initial_tasks(self, project_name):
        """Generates a standard set of initial tasks."""
        t1 = self.add_task("Project Setup", "critical")
        self.add_task("Verify Diamond 33 files", "high", parent_id=t1["id"])
        self.add_task("Configure IDE", "high", parent_id=t1["id"])
        
        t2 = self.add_task("Development", "high")
        self.add_task("Create MVP", "high", parent_id=t2["id"])
        
        t3 = self.add_task("Documentation", "medium")
        self.add_task("Update README", "medium", parent_id=t3["id"])

    def interactive_menu(self):
        while True:
            print(f"\n{Colors.BOLD}Task Menu:{Colors.ENDC}")
            print("1. List Tasks")
            print("2. Add Task")
            print("3. Complete Task")
            print("4. Remove Task")
            print("5. Export (MD/CSV)")
            print("6. Exit")
            choice = input("Select: ").strip()
            if choice == "1":
                self.list_tasks(show_done=True)
            elif choice == "2":
                title = input("Title: ").strip()
                prio = input("Priority (low/medium/high/critical): ").strip()
                dep = input("Depends on (ID, optional): ").strip()
                depends_on = [int(dep)] if dep.isdigit() else []
                self.add_task(title, prio, depends_on=depends_on)
            elif choice == "3":
                tid = input("Task ID: ").strip()
                if tid.isdigit(): self.complete_task(int(tid))
            elif choice == "4":
                tid = input("Task ID: ").strip()
                if tid.isdigit(): self.remove_task(int(tid))
            elif choice == "5":
                fmt = input("Format (markdown/csv): ").strip().lower()
                self.export_tasks(fmt)
            elif choice == "6":
                break

# ==================================================================
# Platform Automation (relative paths)
# ==================================================================

def setup_claude_code(pp, pn, status):
    cp = os.path.join(pp, "CLAUDE.md")
    if os.path.exists(cp):
        status.ok("Claude Code", f"CLAUDE.md ({os.path.getsize(cp)}B)")
    else:
        generate_claude_md(pp, pn)
        status.ok("Claude Code", "CLAUDE.md generated")
    print("  --> Run 'claude' in project dir.")

def setup_vscode(pp, status):
    vd = os.path.join(pp, ".vscode")
    os.makedirs(vd, exist_ok=True)
    with open(os.path.join(vd, "settings.json"), "w") as f:
        json.dump({"editor.formatOnSave": True, "editor.defaultFormatter": "ms-python.python",
                   "files.exclude": {"**/.git": True, "**/**pycache**": True}}, f, indent=4)
    with open(os.path.join(pp, "vscode_mcp_config.json"), "w") as f:
        json.dump({"mcpServers": {
            "memory": {"command": "python3", "args": ["./tools/memory_mcp_server.py"]},
            "code-reviewer": {"command": "python3", "args": ["./tools/code_reviewer_mcp.py"]}
        }}, f, indent=4)
    copy_roles_to_platform(pp, os.path.join(vd, "prompts"))
    safe_write(os.path.join(pp, "CLAUDE_DEV_INSTRUCTIONS.md"),
               f"# Claude Dev (Diamond 33)\nPowered by {SYSTEM_VERSION}.\n"
               "1. Read memory-bank/activeContext.md before tasks.\n"
               "2. Update memory-bank/ after tasks.\n"
               "3. Follow rules/RULES-verification-pipeline.md.\n"
               "Nav: knowledge/core/INDEX-trustworthy-ai-subsystem.md\n", overwrite=True)
    status.ok("VS Code", "Settings + MCP (relative) + roles")

def setup_cursor(pp, status):
    cd = os.path.join(pp, ".cursor", "rules")
    os.makedirs(cd, exist_ok=True)
    copy_roles_to_platform(pp, cd)
    safe_write(os.path.join(pp, ".cursorrules"),
               f"# Cursor ({SYSTEM_VERSION})\n"
               "- Read memory-bank/activeContext.md before tasks.\n"
               "- Update memory-bank/ after tasks.\n"
               "- If you did not read it, it does not exist.\n"
               "- After 3 failures, HALT.\n"
               "Nav: knowledge/core/INDEX-trustworthy-ai-subsystem.md\n"
               "Config: config/hallucination-memory-config.yaml\n", overwrite=True)
    status.ok("Cursor", ".cursorrules + roles")

def setup_antigravity(pp, status):
    with open(os.path.join(pp, "antigravity.json"), "w") as f:
        json.dump({"platform": "antigravity", "version": SYSTEM_VERSION,
                   "memory_enabled": True, "hallucination_check": "strict",
                   "diamond33": {"index": "knowledge/core/INDEX-trustworthy-ai-subsystem.md",
                                 "config": "config/hallucination-memory-config.yaml"},
                   "paths": {"roles": "./roles", "tools": "./tools", "memory_bank": "./memory-bank"}
                   }, f, indent=4)
    status.ok("Antigravity", "Config generated")

def generate_claude_md(pp, pn):
    """Generates CLAUDE.md."""
    content = f"""# {pn} - Claude Code Guide
System: {SYSTEM_VERSION}

## Commands
- `python3 ai_project_creator.py --tasks`: Manage tasks
- `python3 ai_project_creator.py --status`: Check health

## Rules
- Follow `rules/RULES-verification-pipeline.md`
- Update `memory-bank/activeContext.md`
"""
    safe_write(os.path.join(pp, "CLAUDE.md"), content, overwrite=True)

# ==================================================================
# Smart Documentation
# ==================================================================

def scan_project(pp):
    comps = {"frontend": [], "backend": [], "database": [], "docker": [], "api": [], "env_vars": set()}
    skip = {".git", "**pycache**", "node_modules", ".vector_db", "memory-bank", "knowledge",
            "rules", "roles", "prompts", "templates", "examples", "errors", "audit_diamond_32",
            "docs", "workflows", "infrastructure", ".vscode", ".cursor", ".creator_snapshots", "plugins"}
    api_re = re.compile(r"@app.(route|get|post|put|delete|patch)|@router.|urlpatterns\s*=|app.(get|post|put|delete)\s*\(")
    for root, dirs, files in os.walk(pp):
        dirs[:] = [d for d in dirs if d not in skip]
        for fn in files:
            fp = os.path.join(root, fn)
            rp = os.path.relpath(fp, pp)
            if fn.endswith((".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss")):
                comps["frontend"].append(rp)
            if fn.endswith((".py", ".js", ".ts", ".go", ".java", ".rs")) and "test" not in fn.lower():
                comps["backend"].append(rp)
            if fn.endswith((".sql", ".db", ".sqlite", ".sqlite3")):
                comps["database"].append(rp)
            if "Dockerfile" in fn or "docker-compose" in fn:
                comps["docker"].append(rp)
            if fn.endswith((".env", ".env.example")):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        for line in f:
                            if "=" in line.strip() and not line.strip().startswith("#"):
                                comps["env_vars"].add(line.split("=")[0].strip())
                except (IOError, UnicodeDecodeError):
                    pass
            if fn.endswith((".py", ".js", ".ts")):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        if api_re.search(f.read(8192)):
                            comps["api"].append(rp)
                except (IOError, UnicodeDecodeError):
                    pass
    return comps

def generate_smart_readme(pp, pn, status):
    comps = scan_project(pp)
    s = [f"# {pn}\n\nGlobal System {SYSTEM_VERSION} Smart Documenter\n"]
    for label, key, lim in [("Frontend", "frontend", 8), ("Backend", "backend", 8),
                            ("API", "api", 8), ("Database", "database", 5), ("Docker", "docker", 5)]:
        if comps[key]:
            s.append(f"\n## {label} ({len(comps[key])} files)\n")
            for f in comps[key][:lim]:
                s.append(f"- {f}\n")
    if comps["env_vars"]:
        s.append("\n## Env Vars\n")
        for v in sorted(comps["env_vars"]):
            s.append(f"- {v}\n")
    s.append(f"\n## Diamond 33\n| Resource | Path |\n|---|---|\n"
             "| Nav | knowledge/core/INDEX-trustworthy-ai-subsystem.md |\n"
             "| Config | config/hallucination-memory-config.yaml |\n"
             "| Tasks | python3 ai_project_creator.py --tasks |\n"
             f"\n---\nGenerated by AI Project Creator v{WIZARD_VERSION}\n")
    safe_write(os.path.join(pp, "README_PROJECT.md"), "".join(s), overwrite=True)
    total = sum(len(v) if isinstance(v, list) else len(v) for v in comps.values())
    status.ok("Smart Docs", f"README_PROJECT.md ({total} components)")

def setup_diamond33_subsystem(pp, pn, status):
    """Sets up the Diamond 33 subsystem (Anti-Hallucination & Memory)."""
    dirs = [
        "config", "knowledge/core", "rules", "roles", "workflows", 
        "docs", "memory-bank", "tools", "plugins"
    ]
    for d in dirs:
        os.makedirs(os.path.join(pp, d), exist_ok=True)
        
    config_path = os.path.join(pp, "config/hallucination-memory-config.yaml")
    if not os.path.exists(config_path):
        safe_write(config_path, "# Diamond 33 Config\nversion: 1.0\n", overwrite=False)
        
    status.ok("Diamond 33", "Structure verified")

def verify_diamond33(pp):
    """Verifies the presence of critical Diamond 33 files."""
    missing = []
    for f in DIAMOND33_CRITICAL_FILES:
        if not os.path.exists(os.path.join(pp, f)):
            missing.append(f)
    return missing

# ==================================================================
# Project Health
# ==================================================================

def show_project_status(pp):
    print(f"\n{Colors.BOLD}{'=' * 60}")
    print(f"  Project Health -- {os.path.basename(pp)}")
    print(f"{'=' * 60}{Colors.ENDC}\n")
    vf = os.path.join(pp, "VERSION")
    if os.path.exists(vf):
        with open(vf) as f:
            print(f"  Version: {f.read().strip()}")
    fc = sum(1 for _ in Path(pp).rglob("*") if _.is_file() and ".git" not in str(_))
    print(f"  Files: {fc}")
    print(f"\n  {Colors.BOLD}Memory Bank:{Colors.ENDC}")
    for fn in MEMORY_BANK_CORE_FILES:
        fp = os.path.join(pp, "memory-bank", fn)
        if os.path.exists(fp):
            sz = os.path.getsize(fp)
            print(f"    [{'  OK' if sz > 50 else 'WARN'}] {fn} ({sz}B)")
        else:
            print(f"    [MISS] {fn}")
    missing = verify_diamond33(pp)
    print(f"\n  {Colors.BOLD}Diamond 33:{Colors.ENDC} "
          f"{len(DIAMOND33_CRITICAL_FILES)-len(missing)}/{len(DIAMOND33_CRITICAL_FILES)}")
    tm = TaskManager(pp)
    total = len(tm.data["tasks"])
    done = sum(1 for t in tm.data["tasks"] if t["status"] == "done")
    print(f"\n  {Colors.BOLD}Tasks:{Colors.ENDC} {total} total, {done} done, {total-done} remaining")
    ash = os.path.join(pp, "audit_diamond_32/tools/audit_r9_subsystem.sh")
    if os.path.exists(ash):
        _, stdout, _ = run_command(f"bash {ash}", cwd=pp)
        for line in stdout.split("\n"):
            if "RESULT:" in line:
                print(f"\n  {Colors.BOLD}Audit:{Colors.ENDC} {line.strip()}")
                break
    print()

# ==================================================================
# Main Wizard (10 Steps)
# ==================================================================

def run_wizard(auto_mode=False):
    print_header()
    status = StatusTracker()

    print(f"\n{Colors.BLUE}Step 1: Project{Colors.ENDC}")
    pt = get_input("(N)ew or (E)xisting?", "N", auto_mode).upper()
    pp = os.getcwd()
    pn = os.path.basename(pp)
    if pt == "N":
        pn = get_input("Project name", "my_project", auto_mode)
        pp = os.path.join(os.getcwd(), pn)
        if os.path.exists(pp):
            if get_input("Exists. Overwrite?", "n", auto_mode).lower() != "y":
                return
        else:
            os.makedirs(pp)
        status.ok("Project", f"Created {pp}")
    else:
        pi = get_input("Path", os.getcwd(), auto_mode)
        if os.path.exists(pi):
            pp = os.path.abspath(pi)
            pn = os.path.basename(pp)
            status.ok("Project", f"Using {pp}")
        else:
            print(f"{Colors.FAIL}  Not found.{Colors.ENDC}")
            return

    # Load Config
    cfg = ProjectConfig(pp)
    cfg.save_defaults(pp)
    
    # Load Plugins
    pm = PluginManager(pp)
    pm.ensure_dir()
    pm.list_plugins()
    pm.run_hook("on_project_created", project_path=pp, project_name=pn)

    print(f"\n{Colors.BLUE}Step 2: Global System{Colors.ENDC}")
    if get_input("Download from GitHub?", "y", auto_mode).lower() == "y":
        # Create Snapshot before injection
        create_snapshot(pp)
        
        td = os.path.join(pp, "temp_global_system")
        if os.path.exists(td):
            shutil.rmtree(td)
        ok, _, err = run_command(f"git clone --depth 1 {GLOBAL_REPO_URL} {td}")
        if ok:
            for item in os.listdir(td):
                if item == ".git":
                    continue
                src = os.path.join(td, item)
                dst = os.path.join(pp, item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        for r, d, fs in os.walk(src):
                            rel = os.path.relpath(r, src)
                            dr = os.path.join(dst, rel) if rel != "." else dst
                            os.makedirs(dr, exist_ok=True)
                            for fn in fs:
                                df = os.path.join(dr, fn)
                                sf = os.path.join(r, fn)
                                if os.path.exists(df) and os.path.getsize(sf) < os.path.getsize(df):
                                    continue
                                shutil.copy2(sf, df)
                    else:
                        shutil.copytree(src, dst)
                elif not os.path.exists(dst):
                    shutil.copy2(src, dst)
            shutil.rmtree(td)
            status.ok("Injection", "Merged (protected)")
        else:
            status.warn("Injection", f"Failed: {err[:80]}")
    else:
        status.skip("Injection", "Skipped")

    print(f"\n{Colors.BLUE}Step 3: Dependencies{Colors.ENDC}")
    status.ok("Deps", "PyYAML OK") if ensure_yaml() else status.warn("Deps", "No PyYAML")

    print(f"\n{Colors.BLUE}Step 4: Diamond 33{Colors.ENDC}")
    setup_diamond33_subsystem(pp, pn, status)

    print(f"\n{Colors.BLUE}Step 5: Environment{Colors.ENDC}")
    os.chdir(pp)
    sp = os.path.join(pp, "setup_project.py")
    if os.path.exists(sp):
        ok, _, _ = run_command(f"{sys.executable} {sp}")
        (status.ok if ok else status.warn)("Env", "setup_project.py")
    else:
        status.skip("Env", "No setup_project.py")

    print(f"\n{Colors.BLUE}Step 6: Memory{Colors.ENDC}")
    if cfg.get("enable_rag") and get_input("Enable RAG?", "y", auto_mode).lower() == "y":
        rsh = os.path.join(pp, "setup_rag.sh")
        rpy = os.path.join(pp, "tools/setup_local_rag.py")
        if os.path.exists(rsh):
            ok, _, _ = run_command(f"bash {rsh}", cwd=pp)
            (status.ok if ok else status.warn)("RAG", "Vector DB")
        elif os.path.exists(rpy):
            status.ok("RAG", "Ready: tools/setup_local_rag.py")
        else:
            status.skip("RAG", "No script")
    else:
        status.skip("RAG", "Skipped")
    
    if cfg.get("enable_mcp") and get_input("Enable MCP?", "y", auto_mode).lower() == "y":
        mp = os.path.join(pp, "tools/memory_mcp_server.py")
        (status.ok if os.path.exists(mp) else status.warn)("MCP", "Ready" if os.path.exists(mp) else "Missing")
    else:
        status.skip("MCP", "Skipped")

    print(f"\n{Colors.BLUE}Step 7: Code Quality{Colors.ENDC}")
    if cfg.get("enable_reviewer") and get_input("Enable Reviewer?", "y", auto_mode).lower() == "y":
        rv = os.path.join(pp, "tools/code_reviewer_mcp.py")
        (status.ok if os.path.exists(rv) else status.warn)("Reviewer", "Ready" if os.path.exists(rv) else "Missing")
    else:
        status.skip("Reviewer", "Skipped")

    print(f"\n{Colors.BLUE}Step 8: Platform{Colors.ENDC}")
    pl = get_input("IDE? (1:Claude Code 2:VS Code 3:Cursor 4:Antigravity)", cfg.get("default_platform", "1"), auto_mode)
    if pl == "1": setup_claude_code(pp, pn, status)
    elif pl == "2": setup_vscode(pp, status)
    elif pl == "3": setup_cursor(pp, status)
    elif pl == "4": setup_antigravity(pp, status)

    print(f"\n{Colors.BLUE}Step 9: Documentation{Colors.ENDC}")
    generate_smart_readme(pp, pn, status)

    print(f"\n{Colors.BLUE}Step 10: Tasks{Colors.ENDC}")
    if cfg.get("auto_generate_tasks") and get_input("Generate initial tasks?", "y", auto_mode).lower() == "y":
        tm = TaskManager(pp)
        tm.generate_initial_tasks(pn)
        status.ok("Tasks", f"{len(tm.data['tasks'])} tasks")
    else:
        status.skip("Tasks", "Skipped")

    pm.run_hook("on_wizard_complete", project_path=pp, status=status)
    status.print_report()
    print(f"  {Colors.BOLD}Quick Start:{Colors.ENDC}")
    print(f"    cd {pp}")
    print(f"    claude                                   # Claude Code")
    print(f"    python3 ai_project_creator.py --tasks    # Tasks")
    print(f"    python3 ai_project_creator.py --status   # Health")
    print()

# ==================================================================
# CLI
# ==================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"AI Project Creator v{WIZARD_VERSION} - Diamond 33",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 ai_project_creator.py               # Wizard\n"
               "  python3 ai_project_creator.py --auto        # Auto\n"
               "  python3 ai_project_creator.py --tasks       # Task menu\n"
               "  python3 ai_project_creator.py --tasks add 'Bug fix' --priority high\n"
               "  python3 ai_project_creator.py --tasks add 'Test' --parent 2\n"
               "  python3 ai_project_creator.py --tasks list --all\n"
               "  python3 ai_project_creator.py --tasks complete 3\n"
               "  python3 ai_project_creator.py --tasks status 3 in_progress\n"
               "  python3 ai_project_creator.py --tasks remove 5\n"
               "  python3 ai_project_creator.py --audit\n"
               "  python3 ai_project_creator.py --status\n"
               "  python3 ai_project_creator.py --rollback\n"
               "  python3 ai_project_creator.py --watch 5\n"
               "  python3 ai_project_creator.py --plugins\n"
    )
    parser.add_argument("--auto", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--plugins", action="store_true")
    parser.add_argument("--watch", type=int, help="Watch interval in minutes")
    parser.add_argument("--tasks", nargs="*", default=None)
    parser.add_argument("--priority", default="medium", choices=["critical", "high", "medium", "low"])
    parser.add_argument("--parent", type=int, default=None)
    parser.add_argument("--depends-on", type=int, default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--project-path", default=os.getcwd())
    args = parser.parse_args()
    pp = os.path.abspath(args.project_path)

    if args.audit:
        a = os.path.join(pp, "audit_diamond_32/tools/audit_r9_subsystem.sh")
        if os.path.exists(a):
            os.execvp("bash", ["bash", a])
        else:
            print(f"{Colors.FAIL}Audit not found: {a}{Colors.ENDC}")
            sys.exit(1)

    if args.status:
        show_project_status(pp)
        return

    if args.rollback:
        rollback_snapshot(pp)
        return

    if args.plugins:
        pm = PluginManager(pp)
        pm.list_plugins()
        return

    if args.watch:
        print(f"{Colors.BLUE}Starting watch mode (every {args.watch} mins)... Ctrl+C to stop.{Colors.ENDC}")
        try:
            while True:
                show_project_status(pp)
                time.sleep(args.watch * 60)
        except KeyboardInterrupt:
            print("\nStopped.")
        return

    if args.tasks is not None:
        tm = TaskManager(pp)
        if not args.tasks:
            tm.interactive_menu()
            return
        cmd = args.tasks[0].lower()
        if cmd == "list":
            tm.list_tasks(show_done=args.all)
        elif cmd == "add":
            if len(args.tasks) < 2:
                print("Usage: --tasks add \"title\"")
                return
            title = " ".join(args.tasks[1:])
            depends_on = [args.depends_on] if args.depends_on else []
            t = tm.add_task(title, priority=args.priority, parent_id=args.parent, depends_on=depends_on)
            if t:
                n = f" (sub of #{args.parent})" if args.parent else ""
                d = f" (depends on #{args.depends_on})" if args.depends_on else ""
                print(f"{Colors.GREEN}Task #{t['id']}: {title} [{args.priority}]{n}{d}{Colors.ENDC}")
        elif cmd == "complete":
            if len(args.tasks) < 2:
                print("Usage: --tasks complete <id>")
                return
            try:
                tm.complete_task(int(args.tasks[1]))
            except ValueError:
                print("Invalid ID")
        elif cmd == "status":
            if len(args.tasks) < 3:
                print("Usage: --tasks status <id> <status>")
                return
            try:
                tm.update_status(int(args.tasks[1]), args.tasks[2])
            except ValueError:
                print("Invalid ID")
        elif cmd == "remove":
            if len(args.tasks) < 2:
                print("Usage: --tasks remove <id>")
                return
            try:
                tm.remove_task(int(args.tasks[1]))
            except ValueError:
                print("Invalid ID")
        elif cmd == "export":
            if len(args.tasks) < 2:
                print("Usage: --tasks export <markdown|csv>")
                return
            tm.export_tasks(args.tasks[1])
        else:
            print(f"Unknown: {cmd}. Use: add, list, complete, status, remove, export")
        return

    run_wizard(auto_mode=args.auto)

if __name__ == "__main__":
    main()
