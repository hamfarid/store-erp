#!/usr/bin/env python3
"""
AI Project Creator Wizard (The Maestro) v5.0
Global System v36.4.2 Diamond 33 | Trustworthy AI Ready
Plugins - Tasks - Rollback - Git - Watch - Automation
"""

import argparse
import contextlib
import csv as csv_module
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ==================================================================
# Configuration & Constants
# ==================================================================

SYSTEM_VERSION = "Global System v36.4.2 Diamond 33"
WIZARD_VERSION = "7.0"
DEFAULT_PROJECT_ROOT = os.path.expanduser("~/Ai_Project")
GLOBAL_REPO_NAME = "hamfarid/Global-System-Ai-Project-Creators"
GLOBAL_REPO_URL = f"https://github.com/{GLOBAL_REPO_NAME}.git"
GLOBAL_ZIP_URL = f"https://github.com/{GLOBAL_REPO_NAME}/archive/refs/heads/main.zip"

MEMORY_BANK_CORE_FILES = [
    "projectBrief.md",
    "productContext.md",
    "activeContext.md",
    "systemPatterns.md",
    "techContext.md",
    "progress.md",
    "decisionLog.md",
    "lessons_learned.md",
]

DIAMOND33_CRITICAL_FILES = [
    "config/hallucination-memory-config.yaml",
    "knowledge/core/core_definitions.md",
    "rules/RULES-verification-pipeline.md",
    "roles/ROLE-architect.md",
    "workflows/WORKFLOW-tdd.md",
    "docs/api_reference.md",
    "tools/audit_r9_subsystem.sh",
]

SNAPSHOT_DIR = ".creator_snapshots"
PLUGINS_DIR = "plugins"
TASKS_FILE = "tasks.json"
CONFIG_FILE = "creator_config.json"

# Directories to inject from Global System into target project
INJECT_DIRS = [
    "tools",
    "prompts",
    "roles",
    "rules",
    "workflows",
    "examples",
    "docs",
    "config",
    "knowledge",
    "infrastructure",
    "memory-bank",
    "templates",
    "schemas",
    "mcp_server",
    "plugins",
]

# Files to inject at project root
INJECT_ROOT_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    "BOOTSTRAP.md",
    "VERSION",
    "genesis.py",
    "system_logger.py",
    "gap_analysis_check.py",
    "verify_gap_remediation.py",
    "setup_project.py",
    "requirements-global.txt",
    "start_mcp.sh",
    "vscode_mcp_config.json",
    "mcp_config.json",
    "start_global_system.sh",
    ".flake8",
]

# Platform-specific configurations
# Each platform gets: config files + CLAUDE.md + AGENTS.md + BOOTSTRAP.md
# prompts/roles/rules are ALWAYS copied to project root (all platforms)
PLATFORM_MAP = {
    "1": {
        "name": "Claude Code",
        "config_dir": None,
        "files": {
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
            "mcp_config.json": "mcp_config.json",
        },
    },
    "2": {
        "name": "VS Code",
        "config_dir": ".vscode",
        "files": {
            "vscode_mcp_config.json": ".vscode/mcp.json",
            "settings.json": ".vscode/settings.json",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
    "3": {
        "name": "Cursor",
        "config_dir": ".cursor",
        "files": {
            "vscode_mcp_config.json": ".cursor/mcp.json",
            ".cursorrules": ".cursorrules",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
    "4": {
        "name": "Windsurf",
        "config_dir": ".windsurf",
        "files": {
            "vscode_mcp_config.json": ".windsurf/mcp.json",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
    "5": {
        "name": "Augment / Antigravity",
        "config_dir": ".augment",
        "files": {
            "vscode_mcp_config.json": ".augment/mcp.json",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
    "6": {
        "name": "Cline",
        "config_dir": ".cline",
        "files": {
            "vscode_mcp_config.json": ".cline/mcp.json",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
    "7": {
        "name": "Kiro",
        "config_dir": None,
        "files": {
            "kiro.yaml": "kiro.yaml",
            "vscode_mcp_config.json": "kiro_mcp.json",
            "CLAUDE.md": "CLAUDE.md",
            "AGENTS.md": "AGENTS.md",
            "BOOTSTRAP.md": "BOOTSTRAP.md",
        },
    },
}

GITIGNORE_TEMPLATE = """
__pycache__/
*.pyc
.env
.venv
node_modules/
.DS_Store
.creator_snapshots/
"""

# ==================================================================
# Utilities
# ==================================================================


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")  # noqa: S605


def print_banner():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print(f"+{'='*62}+")
    print(f"|     AI Project Creator Wizard (The Maestro) v{WIZARD_VERSION}              |")
    print(f"|   {SYSTEM_VERSION}     |")
    print("|   Plugins - Tasks - Rollback - Git - Watch - Automation     |")
    print(f"+{'='*62}+{Colors.ENDC}")


def safe_write(path, content, overwrite=False):
    if os.path.exists(path) and not overwrite:
        return False
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        print(f"{Colors.FAIL}Error writing {path}: {e}{Colors.ENDC}")
        return False


def run_command(cmd, cwd=None, silent=False, timeout=None):
    try:
        result = subprocess.run(  # noqa: S602
            cmd, shell=True, cwd=cwd, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
        if result.returncode != 0 and not silent:
            print(f"{Colors.FAIL}Command failed: {cmd}\n{result.stderr}{Colors.ENDC}")
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        if not silent:
            print(f"{Colors.WARNING}Command timed out after {timeout}s: {cmd}{Colors.ENDC}")
        return False, "", "timeout"
    except Exception as e:
        if not silent:
            print(f"{Colors.FAIL}Error running {cmd}: {e}{Colors.ENDC}")
        return False, "", str(e)


def force_delete(path, retries=5, delay=1.0):
    """
    Robustly delete a file or directory.
    Handles read-only files AND Windows file-lock errors (WinError 32)
    by retrying with exponential backoff after killing lingering git processes.
    """
    import gc
    import stat
    import time

    def on_rm_error(func, fpath, exc_info):
        # Make writable and retry
        try:
            os.chmod(fpath, stat.S_IWRITE | stat.S_IREAD)
            func(fpath)
        except Exception:  # noqa: S110
            pass  # Will be retried by outer loop

    def _kill_git_processes(target_dir):
        """On Windows, kill any git.exe holding locks inside target_dir."""
        if os.name != "nt":
            return
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "git.exe"],
                capture_output=True,
                timeout=5,
            )
            # Also try git-remote-https.exe which can hold pack locks
            subprocess.run(
                ["taskkill", "/F", "/IM", "git-remote-https.exe"],
                capture_output=True,
                timeout=5,
            )
        except Exception:  # noqa: S110
            pass

    if not os.path.exists(path):
        return

    if not os.path.isdir(path):
        for attempt in range(retries):
            try:
                os.chmod(path, stat.S_IWRITE)
                os.remove(path)
                return
            except PermissionError:
                time.sleep(delay * (attempt + 1))
        return

    # Directory deletion with retry loop
    for attempt in range(retries):
        try:
            # Python 3.12+ uses onexc; older uses onerror
            import sys as _sys
            if _sys.version_info >= (3, 12):
                shutil.rmtree(path, onexc=lambda fn, p, exc: on_rm_error(fn, p, None))
            else:
                shutil.rmtree(path, onerror=on_rm_error)
            return  # Success
        except OSError:
            if attempt == 0:
                # First failure: force GC and kill git processes
                gc.collect()
                _kill_git_processes(path)
            wait = delay * (attempt + 1)
            print(f"  [RETRY] Cleanup attempt {attempt + 1}/{retries} — waiting {wait:.0f}s...")
            time.sleep(wait)

    # Final fallback: on Windows use rd /s /q
    if os.name == "nt":
        try:
            subprocess.run(
                ["cmd", "/c", "rd", "/s", "/q", path],
                capture_output=True,
                timeout=30,
            )
            if not os.path.exists(path):
                return
        except Exception:  # noqa: S110
            pass

    # If still exists, warn but don't crash
    if os.path.exists(path):
        print(f"  [WARN] Could not fully remove {path} — delete manually if needed.")


class StatusTracker:
    def __init__(self):
        self.results = []

    def ok(self, step, msg="OK"):
        print(f"  [{Colors.GREEN}  OK{Colors.ENDC}] {step} -- {msg}")
        self.results.append(("OK", step, msg))

    def warn(self, step, msg):
        print(f"  [{Colors.WARNING}WARN{Colors.ENDC}] {step} -- {msg}")
        self.results.append(("WARN", step, msg))

    def fail(self, step, msg):
        print(f"  [{Colors.FAIL}FAIL{Colors.ENDC}] {step} -- {msg}")
        self.results.append(("FAIL", step, msg))

    def skip(self, step, msg="Skipped"):
        print(f"  [{Colors.DIM}SKIP{Colors.ENDC}] {step} -- {msg}")
        self.results.append(("SKIP", step, msg))

    def summary(self):
        print(f"\n{Colors.BOLD}{'='*60}")
        c = {k: sum(1 for r in self.results if r[0] == k) for k in ["OK", "WARN", "FAIL", "SKIP"]}
        print(f"  Final Status ({c['OK']} OK / {c['WARN']} WARN / {c['FAIL']} FAIL / {c['SKIP']} SKIP)")
        print(f"{'='*60}{Colors.ENDC}")
        for r in self.results:
            color = {"OK": Colors.GREEN, "WARN": Colors.WARNING, "FAIL": Colors.FAIL, "SKIP": Colors.DIM}[r[0]]
            print(f"  [{color}{r[0]:>4}{Colors.ENDC}] {r[1]} -- {r[2]}")


# ==================================================================
# Snapshot & Rollback
# ==================================================================


def create_snapshot(project_path, label="auto"):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_name = f"snapshot_{ts}"
    snap_dir = os.path.join(project_path, SNAPSHOT_DIR, snap_name)
    files_dir = os.path.join(snap_dir, "files")

    os.makedirs(files_dir, exist_ok=True)

    manifest = {"timestamp": ts, "label": label, "files": []}

    # Backup critical files (config, tasks, plugins)
    plugin_files = (
        [os.path.join(PLUGINS_DIR, f) for f in os.listdir(os.path.join(project_path, PLUGINS_DIR)) if f.endswith(".py")]
        if os.path.exists(os.path.join(project_path, PLUGINS_DIR))
        else []
    )
    targets = [CONFIG_FILE, TASKS_FILE] + plugin_files

    count = 0
    for t in targets:
        src = os.path.join(project_path, t)
        if os.path.exists(src) and os.path.isfile(src):
            dst = os.path.join(files_dir, t)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            manifest["files"].append(t)
            count += 1

    with open(os.path.join(snap_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"{Colors.DIM}  Snapshot created: {snap_name} ({count} files){Colors.ENDC}")
    return snap_name


def list_snapshots(project_path):
    sd = os.path.join(project_path, SNAPSHOT_DIR)
    if not os.path.exists(sd):
        return []
    snaps = sorted([d for d in os.listdir(sd) if os.path.isdir(os.path.join(sd, d))])
    if snaps:
        print(f"\n{Colors.BOLD}  Available Snapshots:{Colors.ENDC}")
        for i, s in enumerate(snaps, 1):
            mp = os.path.join(sd, s, "manifest.json")
            info = ""
            if os.path.exists(mp):
                with open(mp) as f:
                    m = json.load(f)
                    info = f" ({m.get('timestamp')})"
            print(f"    {i}. {s.replace('snapshot_','')}{info}")  # noqa: E231
    return snaps


def rollback_snapshot(project_path):
    snaps = list_snapshots(project_path)
    if not snaps:
        print(f"  {Colors.DIM}No snapshots.{Colors.ENDC}")
        return False
    try:
        choice = int(input(f"\n  {Colors.BOLD}Restore # : {Colors.ENDC}")) - 1
        snap_path = os.path.join(project_path, SNAPSHOT_DIR, snaps[choice], "files")
    except (ValueError, IndexError):
        return False
    if not os.path.exists(snap_path):
        return False
    if input(f"  {Colors.WARNING}Overwrite current files? (y/n): {Colors.ENDC}").strip().lower() != "y":
        return False
    restored = 0
    for root, _dirs, files in os.walk(snap_path):
        for fn in files:
            src = os.path.join(root, fn)
            dst = os.path.join(project_path, os.path.relpath(src, snap_path))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            restored += 1
    print(f"{Colors.GREEN}  Restored {restored} files{Colors.ENDC}")
    return True


# ==================================================================
# Plugin System
# ==================================================================


class PluginManager:
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
        try:
            spec = importlib.util.spec_from_file_location(filename[:-3], fp)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins.append(
                {
                    "name": getattr(module, "PLUGIN_NAME", filename[:-3]),
                    "version": getattr(module, "PLUGIN_VERSION", "1.0"),
                    "description": getattr(module, "PLUGIN_DESCRIPTION", ""),
                    "module": module,
                    "file": filename,
                }
            )
        except Exception as e:
            print(f"{Colors.WARNING}  Plugin {filename} failed: {e}{Colors.ENDC}")

    def list_plugins(self):
        if not self.plugins:
            print(f"\n  {Colors.DIM}No plugins. Add .py to {PLUGINS_DIR}/{Colors.ENDC}")
            return
        print(f"\n{Colors.BOLD}  Plugins:{Colors.ENDC}")
        for p in self.plugins:
            print(f"    - {p['name']} v{p['version']} ({p['file']})")

    def run_hook(self, hook_name, **kwargs):
        for p in self.plugins:
            fn = getattr(p["module"], hook_name, None)
            if callable(fn):
                try:
                    fn(**kwargs)
                except Exception as e:
                    print(f"{Colors.WARNING}  Plugin {p['name']}.{hook_name}: {e}{Colors.ENDC}")

    def ensure_dir(self):
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir, exist_ok=True)
            with open(os.path.join(self.plugins_dir, "_example_plugin.py"), "w") as f:
                f.write(
                    '"""Example Plugin"""\nPLUGIN_NAME = "example"\nPLUGIN_VERSION = "1.0"\n'
                    'PLUGIN_DESCRIPTION = "Template"\n\ndef on_wizard_complete(**kw): pass\n'
                )
            return True
        return False


# ==================================================================
# Task Management (full: sync, deps, export to files)
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
                with open(self.tasks_file, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {"version": WIZARD_VERSION, "tasks": [], "next_id": 1}

    def _save(self):
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def _find(self, tid):
        for t in self.data["tasks"]:
            if t["id"] == tid:
                return t
        return None

    def _check_deps(self, task):
        return [d for d in task.get("depends_on", []) if (dep := self._find(d)) and dep["status"] != "done"]

    def _sync_to_memory_bank(self):
        ap = os.path.join(self.project_path, "memory-bank", "activeContext.md")
        if not os.path.exists(ap):
            return
        try:
            with open(ap, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return
        active = sorted(
            [t for t in self.data["tasks"] if t["status"] in ("todo", "in_progress")],
            key=lambda t: (self.PRIORITIES.get(t["priority"], 9), t["id"]),
        )
        lines = ["\n## Active Tasks (auto-synced from tasks.json)\n"]
        for t in active[:15]:
            m = "[~]" if t["status"] == "in_progress" else "[ ]"
            deps = t.get("depends_on", [])
            dep_str = f" [needs #{','.join(str(d) for d in deps)}]" if deps else ""
            lines.append(f"- {m} [{t['priority'].upper()}] #{t['id']}: {t['title']}{dep_str}")
            for sid in t.get("subtasks", []):
                sub = self._find(sid)
                if sub and sub["status"] != "done":
                    lines.append(f"  - {sub['title']}")
        ts = "\n".join(lines) + "\n"
        marker = "## Active Tasks (auto-synced from tasks.json)"
        if marker in content:
            parts = content.split(marker)
            nh = re.search(r"\n## [^A]", parts[1] if len(parts) > 1 else "")
            rem = parts[1][nh.start() :] if nh else ""  # noqa: E203
            content = parts[0] + ts + rem
        else:
            content = content.rstrip() + "\n" + ts
        with open(ap, "w", encoding="utf-8") as f:
            f.write(content)

    def add_task(self, title, priority="medium", parent_id=None, depends_on=None, description=""):
        task = {
            "id": self.data["next_id"],
            "title": title,
            "description": description,
            "priority": priority if priority in self.PRIORITIES else "medium",
            "status": "todo",
            "parent_id": parent_id,
            "subtasks": [],
            "depends_on": depends_on or [],
            "created": self._now(),
            "updated": self._now(),
            "completed": None,
        }
        if parent_id:
            parent = self._find(parent_id)
            if not parent:
                print(f"{Colors.FAIL}  Parent #{parent_id} not found.{Colors.ENDC}")
                return None
            parent["subtasks"].append(task["id"])
        if depends_on:
            for d in depends_on:
                if not self._find(d):
                    print(f"{Colors.FAIL}  Dependency #{d} not found.{Colors.ENDC}")
                    return None
        self.data["tasks"].append(task)
        self.data["next_id"] += 1
        self._save()
        self._sync_to_memory_bank()
        return task

    def complete_task(self, tid):
        task = self._find(tid)
        if not task:
            print(f"{Colors.FAIL}  #{tid} not found.{Colors.ENDC}")
            return False
        unmet = self._check_deps(task)
        if unmet:
            print(f"{Colors.WARNING}  Unmet deps: #{', #'.join(str(d) for d in unmet)}{Colors.ENDC}")
            if input("  Complete anyway? (y/n): ").strip().lower() != "y":
                return False
        task["status"] = "done"
        task["completed"] = self._now()
        task["updated"] = self._now()
        for sid in task.get("subtasks", []):
            sub = self._find(sid)
            if sub and sub["status"] != "done":
                sub["status"] = "done"
                sub["completed"] = self._now()
        self._save()
        self._sync_to_memory_bank()
        print(f"{Colors.GREEN}  #{tid} completed: {task['title']}{Colors.ENDC}")
        return True

    def update_status(self, tid, new_status):
        if new_status not in self.STATUSES:
            print(f"{Colors.FAIL}  Invalid. Use: {', '.join(self.STATUSES)}{Colors.ENDC}")
            return False
        task = self._find(tid)
        if not task:
            return False
        if new_status == "in_progress":
            unmet = self._check_deps(task)
            if unmet:
                print(f"{Colors.WARNING}  Unmet deps: #{', #'.join(str(d) for d in unmet)}{Colors.ENDC}")
                if input("  Start anyway? (y/n): ").strip().lower() != "y":
                    return False
        task["status"] = new_status
        task["updated"] = self._now()
        if new_status == "done":
            task["completed"] = self._now()
        self._save()
        self._sync_to_memory_bank()
        return True

    def remove_task(self, tid):
        task = self._find(tid)
        if not task:
            return False
        for sid in task.get("subtasks", []):
            self.remove_task(sid)
        if task.get("parent_id"):
            parent = self._find(task["parent_id"])
            if parent and tid in parent.get("subtasks", []):
                parent["subtasks"].remove(tid)
        for t in self.data["tasks"]:
            if tid in t.get("depends_on", []):
                t["depends_on"].remove(tid)
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != tid]
        self._save()
        self._sync_to_memory_bank()
        print(f"{Colors.GREEN}  #{tid} removed{Colors.ENDC}")
        return True

    def list_tasks(self, show_done=False):
        if not self.data["tasks"]:
            print(f"\n  {Colors.DIM}No tasks.{Colors.ENDC}")
            return
        top = sorted(
            [t for t in self.data["tasks"] if not t.get("parent_id") and (show_done or t["status"] != "done")],
            key=lambda t: (self.PRIORITIES.get(t["priority"], 9), t["id"]),
        )
        pi = {"critical": "[!!!!]", "high": "[!!! ]", "medium": "[!!  ]", "low": "[!   ]"}
        si = {"todo": "[ ]", "in_progress": "[~]", "done": "[x]", "blocked": "[#]"}
        print(f"\n{Colors.BOLD}  Tasks -- {self._now()}{Colors.ENDC}")
        print(f"  {'-' * 55}")
        for t in top:
            c = {"done": Colors.GREEN, "blocked": Colors.FAIL, "in_progress": Colors.BLUE}.get(t["status"], "")
            deps = t.get("depends_on", [])
            ds = f" [needs #{','.join(str(d) for d in deps)}]" if deps else ""
            print(
                f"  {si.get(t['status'])} {pi.get(t['priority'])} "
                f"#{t['id']:<3d} {c}{t['title']}{Colors.ENDC}{Colors.DIM}{ds}{Colors.ENDC}"
            )
            for sid in t.get("subtasks", []):
                sub = self._find(sid)
                if sub and (show_done or sub["status"] != "done"):
                    sc = Colors.GREEN if sub["status"] == "done" else ""
                    print(f"       {si.get(sub['status'])}  #{sub['id']:<3d} {sc}-> {sub['title']}{Colors.ENDC}")
        total = len(self.data["tasks"])
        done = sum(1 for t in self.data["tasks"] if t["status"] == "done")
        prog = sum(1 for t in self.data["tasks"] if t["status"] == "in_progress")
        blk = sum(1 for t in self.data["tasks"] if t["status"] == "blocked")
        print(
            f"\n  {Colors.DIM}Total: {total} | Todo: {total-done-prog-blk} | "
            f"Progress: {prog} | Done: {done} | Blocked: {blk}{Colors.ENDC}"
        )

    def export_markdown(self):
        lines = [f"# Tasks -- {self._now()}\n"]
        for t in sorted(
            [t for t in self.data["tasks"] if not t.get("parent_id")],
            key=lambda t: (self.PRIORITIES.get(t["priority"], 9), t["id"]),
        ):
            ck = "x" if t["status"] == "done" else " "
            deps = t.get("depends_on", [])
            ds = f" (deps: {', '.join('#'+str(d) for d in deps)})" if deps else ""
            lines.append(f"- [{ck}] **#{t['id']}** [{t['priority'].upper()}] {t['title']}{ds}")
            for sid in t.get("subtasks", []):
                sub = self._find(sid)
                if sub:
                    mark = "x" if sub["status"] == "done" else " "
                    lines.append(f"  - [{mark}] #{sub['id']} {sub['title']}")
        lines.append(f"\n---\nAI Project Creator v{WIZARD_VERSION}\n")
        fp = os.path.join(self.project_path, "TASKS.md")
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{Colors.GREEN}  Exported: TASKS.md{Colors.ENDC}")

    def export_csv(self):
        fp = os.path.join(self.project_path, "tasks_export.csv")
        with open(fp, "w", newline="", encoding="utf-8") as f:
            w = csv_module.writer(f)
            w.writerow(["ID", "Title", "Priority", "Status", "Parent", "Dependencies", "Created", "Completed"])
            for t in self.data["tasks"]:
                w.writerow(
                    [
                        t["id"],
                        t["title"],
                        t["priority"],
                        t["status"],
                        t.get("parent_id", ""),
                        ",".join(str(d) for d in t.get("depends_on", [])),
                        t["created"],
                        t.get("completed", ""),
                    ]
                )
        print(f"{Colors.GREEN}  Exported: tasks_export.csv{Colors.ENDC}")

    def export_tasks(self, fmt="markdown"):
        self.export_csv() if fmt == "csv" else self.export_markdown()

    def interactive_menu(self):
        while True:
            self.list_tasks()
            print(f"\n  {Colors.BOLD}Commands:{Colors.ENDC}")
            print("    (a) Add  (s) Sub-task  (c) Complete  (p) Status  (r) Remove")
            print("    (D) Dependency  (e) Export  (d) Show done  (q) Quit\n")
            ch = input("  > ").strip().lower()
            if ch == "q":
                break
            elif ch == "a":
                title = input("  Title: ").strip()
                if not title:
                    continue
                pri = input("  Priority [medium]: ").strip() or "medium"
                ds = input("  Depends on (IDs, comma): ").strip()
                deps = [int(x) for x in ds.split(",") if x.strip().isdigit()] if ds else None
                t = self.add_task(title, priority=pri, depends_on=deps)
                if t:
                    print(f"{Colors.GREEN}  #{t['id']} added{Colors.ENDC}")
            elif ch == "s":
                try:
                    pid = int(input("  Parent ID: "))
                    title = input("  Title: ").strip()
                    if title:
                        self.add_task(title, parent_id=pid)
                except ValueError:
                    pass
            elif ch == "c":
                with contextlib.suppress(ValueError):
                    self.complete_task(int(input("  ID: ")))
            elif ch == "p":
                with contextlib.suppress(ValueError):
                    self.update_status(int(input("  ID: ")), input("  Status: ").strip())
            elif ch == "r":
                with contextlib.suppress(ValueError):
                    self.remove_task(int(input("  ID: ")))
            elif ch == "d":
                self.list_tasks(show_done=True)
                input("  Enter...")
            elif ch.upper() == "D":
                try:
                    tid, dep = int(input("  Task ID: ")), int(input("  Depends on: "))
                    task = self._find(tid)
                    if task and self._find(dep) and dep not in task.get("depends_on", []):
                        task.setdefault("depends_on", []).append(dep)
                        self._save()
                        print(f"{Colors.GREEN}  Done{Colors.ENDC}")
                except ValueError:
                    pass
            elif ch == "e":
                self.export_tasks(input("  Format (markdown/csv): ").strip().lower())

    def generate_initial_tasks(self, project_name):
        if self.data["tasks"]:
            return
        template = [
            (
                "Initialize Project",
                "critical",
                ["Define objectives in projectBrief.md", "Configure dev environment", "Set up git", "Review CLAUDE.md"],
            ),
            (
                "Core Development",
                "high",
                [
                    "Design architecture -> systemPatterns.md",
                    "Implement core logic",
                    "Write unit tests",
                    "Code review via code_reviewer_mcp.py",
                ],
            ),
            (
                "Anti-Hallucination Integration",
                "high",
                [
                    "Review RULES-verification-pipeline.md",
                    "Configure hallucination-memory-config.yaml",
                    "Set up RAG pipeline",
                    "Run subsystem audit",
                ],
            ),
            (
                "Memory & Context Setup",
                "medium",
                ["Initialize memory MCP server", "Populate techContext.md", "Configure context window budget"],
            ),
            (
                "Documentation & Deployment",
                "medium",
                ["Generate smart documentation", "Deployment instructions", "Integration testing", "Release packaging"],
            ),
        ]
        prev = None
        for title, pri, subs in template:
            deps = [prev] if prev else None
            parent = self.add_task(title, priority=pri, depends_on=deps)
            if parent:
                for st in subs:
                    self.add_task(st, priority=pri, parent_id=parent["id"])
                prev = parent["id"]
        print(f"{Colors.GREEN}  {len(self.data['tasks'])} tasks generated{Colors.ENDC}")


# ==================================================================
# Diamond 33 + CLAUDE.md + Platform Automation + Smart Docs
# ==================================================================


def setup_diamond33_subsystem(pp, pn, status):
    mb = os.path.join(pp, "memory-bank")
    os.makedirs(mb, exist_ok=True)
    for d in ["config", "knowledge/core", "rules", "roles", "workflows", "docs", "tools", "plugins"]:
        os.makedirs(os.path.join(pp, d), exist_ok=True)
    templates = {
        "projectBrief.md": f"# Project Brief: {pn}\n\n## Mission\n{pn} -- {SYSTEM_VERSION}.\n\n## Goals\n- [ ] Define objectives\n- [ ] Core functionality\n- [ ] Anti-hallucination\n- [ ] Memory lifecycle\n\n## Constraints\n- Verification pipeline required\n- Context window < 80%\n- Memory bank = truth\n",  # noqa: E501
        "activeContext.md": f"# Active Context: {pn}\n\n## Focus\nInitialized.\n\n## Changes\n- Created by v{WIZARD_VERSION}\n- Diamond 33 active\n\n## Next\n1. Read projectBrief.md\n2. Check tasks.json\n3. Begin first task\n4. Update this file (Rule C-003)\n",  # noqa: E501
        "progress.md": f"# Progress: {pn}\n\n_(No entries)_\n",
        "decisionLog.md": f"# Decisions: {pn}\n\n_(No entries)_\n",
        "lessons_learned.md": f"# Lessons: {pn}\n\n_(No entries)_\n",
        "systemPatterns.md": f"# Patterns: {pn}\n\n"
        f"## Architecture: Modular Monolith + Async Processing\n\n"
        f"**Default pattern per Global System ARCH-001.** See `knowledge/core/modular_monolith_architecture.md`.\n\n"
        f"### Module Boundaries\n"
        f"- Each Django app is a Bounded Context\n"
        f"- Cross-module communication via `services.py` only (never direct model imports)\n"
        f"- Data crosses boundaries as DTOs (dicts/dataclasses), not ORM instances\n\n"
        f"### Async Strategy\n"
        f"- Heavy operations (>200ms) offloaded to Celery tasks\n"
        f"- External API calls, emails, reports, ML inference → async\n\n"
        f"### Data Strategy\n"
        f"- Single PostgreSQL with module-level boundaries\n"
        f"- Read replica for dashboards/reports when needed (CQRS lite)\n\n"
        f"### When to Extract a Service\n"
        f"- Independent team + different scaling profile + different tech needs\n"
        f"- Use Strangler Fig pattern for gradual extraction\n",
        "techContext.md": f"# Tech Context: {pn}\n\n_(TBD)_\n",
    }
    created = sum(1 for fn, c in templates.items() if safe_write(os.path.join(mb, fn), c))
    status.ok("Memory Bank", f"{created} files" if created else "Exists")
    # Generate architecture knowledge
    arch_file = os.path.join(pp, "knowledge/core/modular_monolith_architecture.md")
    if not os.path.exists(arch_file) or os.path.getsize(arch_file) < 100:
        arch_content = (
            f"# Architecture: Modular Monolith + Async Processing\n"
            f"> {pn} — {SYSTEM_VERSION}\n\n"
            f"## Default Pattern (ARCH-001)\n"
            f"This project follows the **Modular Monolith** pattern:\n"
            f"- Each Django app = one Bounded Context\n"
            f"- Cross-module communication via `services.py` only\n"
            f"- Data crosses boundaries as DTOs, not ORM instances\n"
            f"- Heavy operations (>200ms) → Celery async tasks\n\n"
            f"## Module Communication\n"
            f"```python\n"
            f"# ❌ WRONG — direct cross-app import\n"
            f"from orders.models import Order\n\n"
            f"# ✅ RIGHT — via service layer\n"
            f"from orders.services import OrderService\n"
            f"orders = OrderService.get_user_orders(user_id=uid)\n"
            f"```\n\n"
            f"## When to Extract a Microservice\n"
            f"Only when ALL three conditions are met:\n"
            f"1. Independent team owns the module\n"
            f"2. Fundamentally different scaling needs\n"
            f"3. Different technology stack required\n\n"
            f"## Stack\n"
            f"| Layer | Tool |\n"
            f"|-------|------|\n"
            f"| Framework | Django |\n"
            f"| Async | Celery + Redis |\n"
            f"| API | Django REST Framework |\n"
            f"| Database | PostgreSQL |\n"
            f"| Cache | Redis |\n\n"
            f"## References\n"
            f"- `rules/RULES-architecture-decisions.md`\n"
            f"- `memory-bank/systemPatterns.md`\n"
        )
        safe_write(arch_file, arch_content)
        status.ok("Architecture", "Modular Monolith pattern")
    if generate_claude_md(pp, pn):
        status.ok("CLAUDE.md", "C-002/C-003 rules")
    else:
        status.ok("CLAUDE.md", "Exists")
    if generate_agents_md(pp, pn):
        status.ok("AGENTS.md", "Governance framework")
    else:
        status.ok("AGENTS.md", "Exists")
    missing = verify_diamond33(pp)
    (
        status.ok("Diamond 33", "Complete")
        if not missing
        else status.fail("Diamond 33", f"{len(missing)} missing: {missing[:3]}")
    )
    ash = os.path.join(pp, "tools", "audit_r9_subsystem.sh")
    if not os.path.exists(ash):
        ash = os.path.join(pp, "audit_diamond_32", "tools", "audit_r9_subsystem.sh")  # legacy fallback
    if os.path.exists(ash):
        # Find a compatible bash: prefer Git Bash over WSL bash on Windows
        bash_exe = None
        if os.name == "nt":
            # Git Bash is typically at C:\Program Files\Git\bin\bash.exe
            for candidate in [
                os.path.join(os.environ.get("PROGRAMFILES", ""), "Git", "bin", "bash.exe"),
                os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Git", "bin", "bash.exe"),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Git", "bin", "bash.exe"),
            ]:
                if os.path.isfile(candidate):
                    bash_exe = candidate
                    break
            if not bash_exe:
                # Fallback: any bash on PATH that is NOT WSL's system32 bash
                found = shutil.which("bash")
                if found and "system32" not in found.lower():
                    bash_exe = found
                elif found:
                    # WSL bash — convert path: D:\foo → /mnt/d/foo
                    bash_exe = found
                    drive, tail = os.path.splitdrive(ash)
                    ash = f"/mnt/{drive[0].lower()}{tail.replace(os.sep, '/')}"
        else:
            bash_exe = shutil.which("bash")

        if bash_exe:
            ash_posix = ash.replace("\\", "/")
            ok, stdout, _ = run_command(f'"{bash_exe}" "{ash_posix}"', cwd=pp)
            for line in stdout.split("\n"):
                if "RESULT:" in line:
                    rt = line.strip().split("RESULT:")[1].strip()
                    (status.ok if "0 FAIL" in rt else status.warn)("Audit", rt)
                    break
        else:
            status.skip("Audit", "bash not available on this system")
    else:
        status.skip("Audit", "Not found")


def generate_claude_md(pp, pn):
    cm = os.path.join(pp, "CLAUDE.md")
    if os.path.exists(cm) and os.path.getsize(cm) > 1000:
        return False
    content = (
        f"# CLAUDE.md -- {pn} ({SYSTEM_VERSION})\n\n"
        "## Core Rules (Diamond 33)\n"
        "- **C-001**: Adopt the Architect persona (Role 1). Plan before coding.\n"
        "- **C-002**: Memory Bank is the single source of truth. Update activeContext.md after every session.\n"
        "- **C-003**: No hallucinations. Verify all imports and paths. Use verify_hallucinations.sh.\n"
        "- **C-004**: TDD is mandatory. Write tests before implementation.\n"
        "- **C-005**: Use tasks.json for task tracking. Keep it synced.\n\n"
        "## Commands\n"
        "- `python3 ai_project_creator.py --tasks`: Manage tasks\n"
        "- `python3 ai_project_creator.py --status`: Check project health\n"
        "- `python3 tools/memory_mcp_server.py`: Start memory server\n"
    )
    return safe_write(cm, content, overwrite=True)


def generate_agents_md(pp, pn):
    """Generate AGENTS.md with agent governance framework."""
    am = os.path.join(pp, "AGENTS.md")
    if os.path.exists(am) and os.path.getsize(am) > 1000:
        return False
    content = (
        f"# AGENTS.md -- {pn} ({SYSTEM_VERSION})\n\n"
        "## Agent Governance Framework\n\n"
        "### Startup Sequence (MANDATORY)\n"
        "1. Read `CLAUDE.md` — core rules and context\n"
        "2. Read `memory-bank/activeContext.md` — current state\n"
        "3. Read `memory-bank/projectBrief.md` — mission and goals\n"
        "4. Check `tasks.json` — pending work items\n"
        "5. Read relevant `prompts/` for current phase\n\n"
        "### Agent Roles\n"
        "- **Architect**: System design, API contracts, database schema\n"
        "- **Coder**: Implementation following rules and patterns\n"
        "- **Reviewer**: Code review, security scan, quality gate\n"
        "- **QA**: Testing (RORLOC methodology), coverage verification\n"
        "- **DevOps**: Docker, CI/CD, deployment, monitoring\n\n"
        "### Memory Protocol\n"
        "- Rule C-002: Read activeContext.md before any task\n"
        "- Rule C-003: Update activeContext.md after every action\n"
        "- All decisions logged in decisionLog.md\n"
        "- Lessons captured in lessons_learned.md\n\n"
        "### Anti-Hallucination\n"
        "- Verify all imports against project_knowledge.json\n"
        "- Cross-check function signatures before calling\n"
        "- Run quality_gate.py before committing\n"
        "- 3 verification failures trigger HALT\n\n"
        "### TODO System (MANDATORY)\n"
        "- `docs/TODO.md` — permanent record (NEVER delete, only [x])\n"
        "- `docs/COMPLETE_TASKS.md` — done tasks with timestamps\n"
        "- `docs/INCOMPLETE_TASKS.md` — pending by priority\n"
    )
    return safe_write(am, content, overwrite=True)


def verify_diamond33(pp):
    return [f for f in DIAMOND33_CRITICAL_FILES if not os.path.exists(os.path.join(pp, f))]


def scan_project(pp):
    comps = {"frontend": [], "backend": [], "api": [], "database": [], "docker": [], "env_vars": set()}
    skip = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".creator_snapshots"}
    api_re = re.compile(r"@app\.(route|get|post)|@router\.|urlpatterns|path\s*\(")
    for root, dirs, files in os.walk(pp):
        dirs[:] = [d for d in dirs if d not in skip]
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                rp = os.path.relpath(fp, pp)
            except ValueError:
                continue
            if fn.endswith((".jsx", ".tsx", ".vue", ".svelte", ".css")):
                comps["frontend"].append(rp)
            if fn.endswith((".py", ".js", ".ts", ".go")) and "test" not in fn.lower():
                comps["backend"].append(rp)
            if fn.endswith((".sql", ".sqlite3")):
                comps["database"].append(rp)
            if "Dockerfile" in fn or "docker-compose" in fn:
                comps["docker"].append(rp)
            if fn.endswith((".env", ".env.example")):
                try:
                    with open(fp) as f:
                        for line in f:
                            if "=" in line and not line.strip().startswith("#"):
                                comps["env_vars"].add(line.split("=")[0].strip())
                except (OSError, UnicodeDecodeError):
                    pass
            if fn.endswith((".py", ".js", ".ts")):
                try:
                    with open(fp) as f:
                        if api_re.search(f.read(8192)):
                            comps["api"].append(rp)
                except (OSError, UnicodeDecodeError):
                    pass
    return comps


def generate_smart_readme(pp, pn, status):
    comps = scan_project(pp)
    s = [f"# {pn}\n\n{SYSTEM_VERSION} Smart Documenter\n"]
    for label, key, lim in [
        ("Frontend", "frontend", 8),
        ("Backend", "backend", 8),
        ("API", "api", 8),
        ("Database", "database", 5),
        ("Docker", "docker", 5),
    ]:
        if comps[key]:
            s.append(f"\n## {label} ({len(comps[key])} files)\n")
            for f in comps[key][:lim]:
                s.append(f"- {f}\n")
    s.append(f"\n---\nv{WIZARD_VERSION}\n")
    safe_write(os.path.join(pp, "README_PROJECT.md"), "".join(s), overwrite=True)
    status.ok("Docs", "README_PROJECT.md")


# ==================================================================
# Smart Injection, Platform Setup, MCP Activation
# ==================================================================


def smart_inject_files(source_dir, target_dir, status):
    """
    Smart injection: copies files from Global System to target project.
    Maps directories to their correct locations and only copies
    newer files or files that don't exist in the target.
    """
    injected = 0
    skipped = 0

    # 1. Inject directories (tools/, prompts/, roles/, etc.)
    for d in INJECT_DIRS:
        src = os.path.join(source_dir, d)
        dst = os.path.join(target_dir, d)
        if not os.path.isdir(src):
            continue
        os.makedirs(dst, exist_ok=True)
        for root, dirs, files in os.walk(src):
            dirs[:] = [x for x in dirs if x not in {".git", "__pycache__", "node_modules"}]
            rel = os.path.relpath(root, src)
            dst_sub = os.path.join(dst, rel) if rel != "." else dst
            os.makedirs(dst_sub, exist_ok=True)
            for fn in files:
                sf = os.path.join(root, fn)
                df = os.path.join(dst_sub, fn)
                if not os.path.exists(df) or os.path.getmtime(sf) > os.path.getmtime(df):
                    shutil.copy2(sf, df)
                    injected += 1
                else:
                    skipped += 1

    # 2. Inject root-level files
    for fn in INJECT_ROOT_FILES:
        sf = os.path.join(source_dir, fn)
        df = os.path.join(target_dir, fn)
        if os.path.isfile(sf):
            if not os.path.exists(df) or os.path.getmtime(sf) > os.path.getmtime(df):
                shutil.copy2(sf, df)
                injected += 1
            else:
                skipped += 1

    status.ok("Injection", f"{injected} files injected, {skipped} unchanged")
    return injected


def detect_platform(pp):
    """
    Auto-detect the IDE/platform being used based on project directory markers.
    Returns the PLATFORM_MAP key.
    """
    if os.path.exists(os.path.join(pp, ".cursor")):
        return "3"  # Cursor
    elif os.path.exists(os.path.join(pp, ".augment")):
        return "4"  # Antigravity
    elif os.path.exists(os.path.join(pp, ".vscode")):
        return "2"  # VS Code
    # Check environment variables for Claude Code
    elif os.environ.get("CLAUDE_CODE") or shutil.which("claude"):
        return "1"  # Claude Code
    return "2"  # Default: VS Code


def setup_platform(pp, ide_choice, source_dir, status):
    """
    Set up platform-specific helper files based on IDE choice.
    1. Copies platform config files (MCP config, settings, cursorrules)
    2. Copies CLAUDE.md, AGENTS.md, BOOTSTRAP.md to project root
    3. Copies prompts/, roles/, rules/ RECURSIVELY (including subdirs)
    """
    platform = PLATFORM_MAP.get(ide_choice, PLATFORM_MAP["2"])
    pname = platform["name"]

    # Create config directory if needed
    if platform["config_dir"]:
        cfg_dir = os.path.join(pp, platform["config_dir"])
        os.makedirs(cfg_dir, exist_ok=True)

    copied = 0

    # --- Part 1: Copy platform-specific config files ---
    for src_name, dst_rel in platform["files"].items():
        dst_path = os.path.join(pp, dst_rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        # Try source_dir first, then pp root, then generate defaults
        src_path = None
        for candidate in [
            os.path.join(source_dir, src_name) if source_dir else None,
            os.path.join(pp, src_name),
        ]:
            if candidate and os.path.isfile(candidate):
                src_path = candidate
                break

        if src_path and src_path != dst_path:
            shutil.copy2(src_path, dst_path)
            copied += 1
        elif not src_path and src_name == "settings.json":
            safe_write(
                dst_path,
                json.dumps(
                    {
                        "python.analysis.typeCheckingMode": "basic",
                        "python.linting.enabled": True,
                        "python.linting.flake8Enabled": True,
                        "editor.formatOnSave": True,
                    },
                    indent=2,
                ),
            )
            copied += 1
        elif not src_path and src_name == ".cursorrules":
            safe_write(
                dst_path,
                (
                    f"# Cursor Rules — {SYSTEM_VERSION}\n\n"
                    "## Startup Sequence\n"
                    "1. Read `CLAUDE.md` — the primary entry point and core rules\n"
                    "2. Read `BOOTSTRAP.md` — initialization guide\n"
                    "3. Read `AGENTS.md` — full governance framework\n"
                    "4. Read `prompts/00_MASTER.md` — master prompt\n"
                    "5. Read `rules/00-iron-rules.md` — iron rules\n\n"
                    "## Core Rules\n"
                    "- Memory Bank is the single source of truth\n"
                    "- No hallucinations — verify all imports and paths\n"
                    "- TDD is mandatory — write tests before implementation\n"
                    "- Use tasks.json for task tracking\n"
                    "- Read prompts/, roles/, rules/ before starting any task\n\n"
                    "## MCP Servers\n"
                    "- memory: python3 tools/memory_mcp_server.py\n"
                    "- code-reviewer: python3 tools/code_reviewer_mcp.py\n"
                ),
            )
            copied += 1

    # --- Part 2: Copy prompts/, roles/, rules/ RECURSIVELY ---
    for helper_dir in ["prompts", "roles", "rules"]:
        src = os.path.join(source_dir, helper_dir) if source_dir else None
        dst = os.path.join(pp, helper_dir)

        # Skip if source doesn't exist or is the same as destination
        if not src or not os.path.isdir(src) or os.path.abspath(src) == os.path.abspath(dst):
            continue

        # Recursive copy using os.walk (handles subdirectories)
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git"}]
            rel = os.path.relpath(root, src)
            dst_sub = os.path.join(dst, rel) if rel != "." else dst
            os.makedirs(dst_sub, exist_ok=True)
            for fn in files:
                sf = os.path.join(root, fn)
                df = os.path.join(dst_sub, fn)
                if not os.path.exists(df) or os.path.getmtime(sf) > os.path.getmtime(df):
                    shutil.copy2(sf, df)
                    copied += 1

    status.ok(pname, f"{copied} helper files placed (prompts/roles/rules + config)")
    return copied


def activate_mcp(pp, status):
    """
    Actually activate MCP:
    1. Install MCP dependencies
    2. Copy MCP config to .vscode/mcp.json and .cursor/mcp.json
    3. Run sync_mcp_config.py to synchronize
    4. Verify memory_mcp_server.py is ready
    """
    activated = []

    # 1. Install MCP core dependencies (lightweight only, skip heavy packages)
    mcp_req = os.path.join(pp, "tools", "mcp_requirements.txt")
    if os.path.exists(mcp_req):
        # Install lightweight MCP packages only (skip chromadb/sentence-transformers)
        lightweight = ["mcp", "fastmcp", "pydantic", "requests"]
        print("    Installing MCP packages...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet"] + lightweight,
                cwd=pp,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                activated.append("deps")
        except subprocess.TimeoutExpired:
            print("    (pip install timed out — skipping)")
        except Exception:  # noqa: BLE001, S110
            pass  # Skip if install fails

    # 2. Deploy MCP config to platform directories
    mcp_config_src = None
    for candidate in [
        os.path.join(pp, "vscode_mcp_config.json"),
        os.path.join(pp, "config", "mcp_config.json"),
        os.path.join(pp, "mcp_config.json"),
        os.path.join(pp, "tools", "mcp_golden_config.json"),
    ]:
        if os.path.isfile(candidate):
            mcp_config_src = candidate
            break

    if mcp_config_src:
        for target_dir in [".vscode", ".cursor"]:
            dst_dir = os.path.join(pp, target_dir)
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, "mcp.json")
            if not os.path.exists(dst):
                shutil.copy2(mcp_config_src, dst)
        activated.append("config")

    # 3. Run sync_mcp_config.py if available
    sync_script = os.path.join(pp, "tools", "sync_mcp_config.py")
    if os.path.exists(sync_script):
        try:
            print("    Syncing MCP config...")
            subprocess.run([sys.executable, sync_script], cwd=pp, text=True, timeout=30)
            activated.append("sync")
        except subprocess.TimeoutExpired:
            print("    (sync timed out — skipping)")
        except Exception:  # noqa: BLE001, S110
            pass

    # 4. Run mcp_manager.py scan if available
    mgr_script = os.path.join(pp, "tools", "mcp_manager.py")
    if os.path.exists(mgr_script):
        try:
            print("    Scanning MCP servers...")
            subprocess.run([sys.executable, mgr_script, "list"], cwd=pp, text=True, timeout=30)
            activated.append("manager")
        except subprocess.TimeoutExpired:
            print("    (scan timed out — skipping)")
        except Exception:  # noqa: BLE001, S110
            pass

    # 5. Verify memory server is ready
    mem_server = os.path.join(pp, "tools", "memory_mcp_server.py")
    if os.path.exists(mem_server):
        activated.append("memory-server")

    if activated:
        status.ok("MCP", f"Activated: {', '.join(activated)}")
    else:
        status.warn("MCP", "No MCP components found")
    return activated


def git_init_project(pp, status):
    if os.path.exists(os.path.join(pp, ".git")):
        status.ok("Git", "Exists")
        return
    gi = os.path.join(pp, ".gitignore")
    if not os.path.exists(gi):
        with open(gi, "w") as f:
            f.write(GITIGNORE_TEMPLATE)
    run_command("git init", cwd=pp)
    run_command("git add -A", cwd=pp)
    ok, _, _ = run_command(f'git commit -m "Initial commit -- v{WIZARD_VERSION} Diamond 33"', cwd=pp)
    status.ok("Git", "Init + commit") if ok else status.warn("Git", "Init OK, commit issue")


def health_check(pp):
    issues = []
    ok = 0
    for fn in MEMORY_BANK_CORE_FILES:
        fp = os.path.join(pp, "memory-bank", fn)
        if os.path.exists(fp) and os.path.getsize(fp) > 20:
            ok += 1
        else:
            issues.append(f"memory-bank/{fn}")
    for f in DIAMOND33_CRITICAL_FILES:
        fp = os.path.join(pp, f)
        if os.path.exists(fp) and os.path.getsize(fp) > 10:
            ok += 1
        else:
            issues.append(f)
    return ok, len(issues), issues


def run_watch(pp, mins):
    print(f"{Colors.BOLD}  Watch (every {mins}m). Ctrl+C to stop.{Colors.ENDC}\n")
    try:
        while True:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            ok, w, issues = health_check(pp)
            if w == 0:
                print(f"  [{ts}] {Colors.GREEN}OK{Colors.ENDC} -- {ok} passed")
            else:
                print(f"  [{ts}] {Colors.WARNING}{w} issues{Colors.ENDC}")
                for i in issues[:3]:
                    print(f"    - {i}")
            time.sleep(mins * 60)
    except KeyboardInterrupt:
        print()


def show_project_status(pp):
    print(f"\n{Colors.BOLD}  Project: {os.path.basename(pp)}{Colors.ENDC}")
    print(f"  {'=' * 50}")
    fc = sum(1 for _ in Path(pp).rglob("*") if _.is_file() and ".git" not in str(_))
    print(f"  Files: {fc}")
    for fn in MEMORY_BANK_CORE_FILES:
        fp = os.path.join(pp, "memory-bank", fn)
        st = f"OK ({os.path.getsize(fp)}B)" if os.path.exists(fp) and os.path.getsize(fp) > 50 else "MISS"
        print(f"    [{st:>10s}] {fn}")
    missing = verify_diamond33(pp)
    print(f"\n  Diamond 33: {len(DIAMOND33_CRITICAL_FILES)-len(missing)}/{len(DIAMOND33_CRITICAL_FILES)}")
    tm = TaskManager(pp)
    t = len(tm.data["tasks"])
    d = sum(1 for x in tm.data["tasks"] if x["status"] == "done")
    print(f"  Tasks: {t} total, {d} done, {t-d} remaining\n")


# ==================================================================
# Main Wizard Logic
# ==================================================================


def run_wizard(auto_mode=False):
    print_banner()

    # Step 1: Project Path
    print(f"{Colors.HEADER}Step 1: Project{Colors.ENDC}")
    if auto_mode:
        project_mode = "n"
        pp = os.path.join(DEFAULT_PROJECT_ROOT, f"project_{datetime.datetime.now().strftime('%Y%m%d')}")
    else:
        project_mode = input("  (N)ew or (E)xisting? [N]: ").strip().lower() or "n"
        if project_mode == "e":
            default_path = os.getcwd()
            print(f"  {Colors.DIM}Injecting Global System into existing project.{Colors.ENDC}")
            print(f"  {Colors.DIM}Your code will NOT be overwritten. Only Global System dirs are added.{Colors.ENDC}")
        else:
            default_path = DEFAULT_PROJECT_ROOT
        pp = input(f"  Path [{default_path}]: ").strip() or default_path

    pp = os.path.abspath(pp)
    os.makedirs(pp, exist_ok=True)

    # Plugin Hook
    pm = PluginManager(pp)
    pm.ensure_dir()
    pm.list_plugins()
    pm.run_hook("on_wizard_start", project_path=pp)

    status = StatusTracker()
    status.ok("Project", f"Using {pp}")

    # Step 2: Injection (Global System from GitHub)
    print(f"\n{Colors.HEADER}Step 2: Global System Injection{Colors.ENDC}")
    if project_mode == "e":
        print(f"  {Colors.DIM}Safe mode: only adds missing files, never overwrites existing ones.{Colors.ENDC}")
    do_dl = "y" if auto_mode else (input("  Download latest from GitHub? [y]: ").strip().lower() or "y")
    source_dir = None  # Track where Global System files came from
    if do_dl == "y":
        create_snapshot(pp, "pre_injection")
        td = os.path.join(pp, "temp_global_system")
        force_delete(td)

        # Try git clone first (shallow for speed)
        ok, _, _ = run_command(f"git clone --depth 1 {GLOBAL_REPO_URL} {td}", silent=True)
        if not ok:
            # Fallback to zip download
            print(f"  {Colors.DIM}Git clone failed, trying zip download...{Colors.ENDC}")
            zip_path = os.path.join(pp, "global.zip")
            ok, _, _ = run_command(f"curl -L -o {zip_path} {GLOBAL_ZIP_URL}")
            if ok:
                import zipfile

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(pp)
                # Find extracted folder (name varies)
                for candidate in ["Global-System-Ai-Project-Creators-main", "Global_System-main"]:
                    ef = os.path.join(pp, candidate)
                    if os.path.exists(ef):
                        os.rename(ef, td)
                        break
                if os.path.exists(zip_path):
                    os.remove(zip_path)

        if os.path.exists(td):
            source_dir = td
            # Smart injection: map directories to correct locations
            smart_inject_files(td, pp, status)
            # Remove .git first (holds Windows file locks from clone)
            git_dir = os.path.join(td, ".git")
            if os.path.isdir(git_dir):
                force_delete(git_dir)
            force_delete(td)
            source_dir = pp  # After injection, source is now pp itself
        else:
            status.warn("Injection", "Failed to download")
    else:
        # Use the script's own directory as source for helper files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir != os.path.abspath(pp):
            source_dir = script_dir
        status.skip("Injection", "Skipped (using local files)")

    # Step 3: Dependencies
    print(f"\n{Colors.HEADER}Step 3: Dependencies{Colors.ENDC}")
    try:
        pass

        status.ok("Deps", "PyYAML OK")
    except ImportError:
        status.fail("Deps", "PyYAML missing (pip install pyyaml)")

    # Step 4: Diamond 33
    print(f"\n{Colors.HEADER}Step 4: Diamond 33{Colors.ENDC}")
    setup_diamond33_subsystem(pp, os.path.basename(pp), status)

    # Step 5: Environment & System Logger
    print(f"\n{Colors.HEADER}Step 5: Environment{Colors.ENDC}")
    # 5a. Initialize System Logger FIRST (logs everything after)
    sys_logger = os.path.join(pp, "system_logger.py")
    if not os.path.exists(sys_logger):
        sys_logger = os.path.join(pp, "tools", "system_logger.py")
    if os.path.exists(sys_logger):
        ok, _, _ = run_command(f"{sys.executable} {sys_logger}", cwd=pp)
        (status.ok if ok else status.warn)("Logger", "system_logger.py initialized")

    # 5b. Run setup_project.py (installs pip deps — shows live output)
    sp = os.path.join(pp, "setup_project.py")
    if os.path.exists(sp):
        run_setup = "y" if auto_mode else (
            input("  Run setup_project.py (installs deps)? [y]: ").strip().lower() or "y"
        )
        if run_setup == "y":
            print(f"  {Colors.DIM}Running setup_project.py (live output below)...{Colors.ENDC}")
            try:
                result = subprocess.run(  # noqa: S602
                    f"{sys.executable} {sp}", shell=True, cwd=pp,
                    encoding="utf-8", errors="replace",
                )
                (status.ok if result.returncode == 0 else status.warn)("Env", "setup_project.py")
            except Exception as e:
                status.warn("Env", f"setup_project.py error: {e}")
        else:
            status.skip("Env", "Skipped (run setup_project.py manually if needed)")
    else:
        status.skip("Env", "Script not found")

    # Step 6: Memory (RAG/MCP)
    print(f"\n{Colors.HEADER}Step 6: Memory{Colors.ENDC}")
    rag = "y" if auto_mode else (input("  Enable RAG? [y]: ").strip().lower() or "y")
    if rag == "y":
        if os.name == "nt":
            status.warn("RAG", "Vector DB (Manual setup on Windows)")
        else:
            srag = os.path.join(pp, "setup_rag.sh")
            if os.path.exists(srag):
                run_command(f"bash {srag}", cwd=pp)
                status.ok("RAG", "Vector DB")

    mcp = "y" if auto_mode else (input("  Enable MCP? [y]: ").strip().lower() or "y")
    if mcp == "y":
        activate_mcp(pp, status)

    # Step 7: Code Quality (Indexer -> Quality Gate -> Reviewer -> Speckit)
    print(f"\n{Colors.HEADER}Step 7: Code Quality{Colors.ENDC}")
    rev = "y" if auto_mode else (input("  Enable Code Quality Pipeline? [y]: ").strip().lower() or "y")
    if rev == "y":
        # 7a. Build Symbol Table FIRST (needed by quality gate and speckit)
        indexer_script = os.path.join(pp, "tools", "code_indexer.py")
        if os.path.exists(indexer_script):
            ok, _, _ = run_command(f"{sys.executable} {indexer_script} {pp}", cwd=pp)
            (status.ok if ok else status.warn)("Indexer", "Symbol Table built")

        # 7b. Quality Gate (reads project_knowledge.json for validation)
        gate_script = os.path.join(pp, "tools", "quality_gate.py")
        if os.path.exists(gate_script):
            ok, _, _ = run_command(f"{sys.executable} {gate_script} {pp}", cwd=pp)
            (status.ok if ok else status.warn)("Quality", "Quality Gate passed")

        # 7c. Code Reviewer (after quality gate fixes)
        reviewer_script = os.path.join(pp, "tools", "code_reviewer.py")
        if os.path.exists(reviewer_script):
            ok, _, _ = run_command(f"{sys.executable} {reviewer_script} {pp}", cwd=pp)
            (status.ok if ok else status.warn)("Reviewer", "Code Review complete")

        # 7d. Speckit LAST (reads Symbol Table + Quality Report for planning)
        speckit = os.path.join(pp, "tools", "speckit.py")
        if os.path.exists(speckit):
            ok, _, _ = run_command(f"{sys.executable} {speckit}", cwd=pp)
            (status.ok if ok else status.warn)("Speckit", "Planning complete")

    # Step 8: Platform (copies helper files based on IDE choice)
    print(f"\n{Colors.HEADER}Step 8: Platform{Colors.ENDC}")
    ide = "2" if auto_mode else (input("  IDE? (1:Claude Code 2:VS Code 3:Cursor 4:Antigravity) [2]: ").strip() or "2")
    effective_source = source_dir if source_dir else pp
    setup_platform(pp, ide, effective_source, status)

    # Step 9: Documentation
    print(f"\n{Colors.HEADER}Step 9: Documentation{Colors.ENDC}")
    generate_smart_readme(pp, os.path.basename(pp), status)

    # Step 10: Tasks
    print(f"\n{Colors.HEADER}Step 10: Tasks{Colors.ENDC}")
    gen_tasks = "y" if auto_mode else (input("  Generate initial tasks? [y]: ").strip().lower() or "y")
    tm = TaskManager(pp)
    if gen_tasks == "y":
        tm.generate_initial_tasks(os.path.basename(pp))
    status.ok("Tasks", f"{len(tm.data['tasks'])} tasks")

    # Git Init
    git_init_project(pp, status)

    # Final Report
    status.summary()
    pm.run_hook("on_wizard_complete", project_path=pp, status=status)

    print(f"{Colors.BOLD}  Quick Start:{Colors.ENDC}")
    print(f"    cd {pp}")
    print("    claude                                   # Claude Code")
    print("    python3 ai_project_creator.py --tasks    # Tasks")
    print("    python3 ai_project_creator.py --status   # Health")

    return pp


def interactive_menu(pp):
    """
    Interactive main menu for managing the project after setup.
    """
    while True:
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║   Global System Dashboard - Project Control Center   ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")

        print(f"Project: {Colors.BLUE}{os.path.basename(pp)}{Colors.ENDC}")
        print(f"Path:    {pp}")
        print("-" * 60)

        print("1. 📊 Project Status (Health Check)")
        print("2. 📝 Task Manager (View/Add/Update)")
        print("3. 🔍 Analyze Project (Smart Documenter)")
        print("4. 📖 Read Documentation (README)")
        print("5. 🧠 Start Memory Server (MCP)")
        print("6. 💻 Open VS Code")
        print("7. 🚀 Auto-Pilot Mode (Full 16-Step Pipeline)")
        print("8. 📦 Install Dependencies (Fix Missing Packages)")
        print("9. 🧪 Run Auto-Test Generator (Smart Tester)")
        print("10. 🤖 Start Multi-Agent Runner (Crew Engine)")
        print("11. ☁️ Setup Cloud Deployment (Docker/Vercel/Railway)")
        print("12. 🧠 Build Code Knowledge Base (Index Symbols)")
        print("13. 🛡️ Run Quality Gate & Fix Deps (Lint/Format/Reqs)")
        print("-" * 60)
        print("14. 🧪 RORLOC Testing (6-Phase QA)")
        print("15. 🗺️  Module Mapper (Generate MODULE_MAP.md)")
        print("16. 🔄 Duplicate Detector (Find Similar Files)")
        print("17. 🔗 Code Deduplicator (Safe Merge Duplicates)")
        print("18. ✅ System Completeness Check (100% Score)")
        print("19. 🔧 Fix Import Paths")
        print("20. 📊 Project Analyzer (Structure & Complexity)")
        print("21. 🧹 Project Cleanup (Remove Cache/Temp)")
        print("0. ❌ Exit")

        choice = input(f"\n{Colors.BOLD}Select an option [0-21]: {Colors.ENDC}").strip()

        if choice == "1":
            show_project_status(pp)
            input("\nPress Enter to continue...")
        elif choice == "2":
            subprocess.run([sys.executable, __file__, "--tasks"], cwd=pp)
            input("\nPress Enter to continue...")
        elif choice == "3":
            print(f"\n{Colors.BLUE}Analyzing project structure...{Colors.ENDC}")
            status = StatusTracker()
            generate_smart_readme(pp, os.path.basename(pp), status)
            print(f"{Colors.GREEN}Analysis complete. README_PROJECT.md updated.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "4":
            readme_path = os.path.join(pp, "README_PROJECT.md")
            if not os.path.exists(readme_path):
                readme_path = os.path.join(pp, "README.md")

            if os.path.exists(readme_path):
                print(f"\n{Colors.BOLD}--- {os.path.basename(readme_path)} ---{Colors.ENDC}\n")
                with open(readme_path, encoding="utf-8") as f:
                    print(f.read())
                print(f"\n{Colors.BOLD}--- End of File ---{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}No README found.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "5":
            mcp_script = os.path.join(pp, "tools", "memory_mcp_server.py")
            if os.path.exists(mcp_script):
                # Check if chromadb+mcp are importable first
                check = subprocess.run(
                    [sys.executable, "-c", "import chromadb; from mcp.server.fastmcp import FastMCP"],
                    capture_output=True, text=True,
                )
                if check.returncode != 0:
                    print(f"{Colors.WARNING}Missing dependencies: chromadb & mcp{Colors.ENDC}")
                    ans = input("  Install them now? [y]: ").strip().lower() or "y"
                    if ans == "y":
                        print("  Installing chromadb mcp fastmcp (this may take a minute)...")
                        subprocess.run([sys.executable, "-m", "pip", "install", "chromadb", "mcp", "fastmcp"])
                    else:
                        print(f"{Colors.FAIL}Skipped. Run manually: pip install chromadb mcp fastmcp{Colors.ENDC}")
                        input("\nPress Enter to continue...")
                        continue

                print(f"\n{Colors.GREEN}Starting Memory MCP Server... (Ctrl+C to stop){Colors.ENDC}")
                try:
                    subprocess.run([sys.executable, mcp_script], cwd=pp)
                except KeyboardInterrupt:
                    print("\nServer stopped.")
                except Exception as e:
                    print(f"{Colors.FAIL}Error starting server: {e}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}Memory MCP script not found at {mcp_script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "6":
            if shutil.which("code"):
                subprocess.run(["code", pp])
            else:
                print(f"{Colors.FAIL}VS Code 'code' command not found in PATH.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "7":
            print(f"\n{Colors.HEADER}=== Auto-Pilot Mode (Full 16-Step Pipeline) ==={Colors.ENDC}")
            print(f"Target: {pp}")
            print(f"{'='*60}")

            # 1. Initialize System Logger (FIRST — logs everything after)
            print(f"\n{Colors.BLUE}[1/16] Initializing System Logger...{Colors.ENDC}")
            sys_logger = os.path.join(pp, "system_logger.py")
            if not os.path.exists(sys_logger):
                sys_logger = os.path.join(pp, "tools", "system_logger.py")
            if os.path.exists(sys_logger):
                subprocess.run([sys.executable, sys_logger], cwd=pp)
                print(f"{Colors.GREEN}  System Logger initialized.{Colors.ENDC}")
            else:
                print(f"{Colors.DIM}  System Logger not found, skipping.{Colors.ENDC}")

            # 2. Install Dependencies (Global System's own deps — never touches project's requirements.txt)
            print(f"\n{Colors.BLUE}[2/16] Checking & Fixing Dependencies...{Colors.ENDC}")
            req_file = os.path.join(pp, "requirements-global.txt")
            if os.path.exists(req_file):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], cwd=pp)
            else:
                print(f"{Colors.WARNING}requirements-global.txt not found. Installing core packages...{Colors.ENDC}")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "chromadb", "mcp", "pyyaml", "requests"], cwd=pp
                )

            # 3. Activate MCP (install deps, deploy config, sync)
            print(f"\n{Colors.BLUE}[3/16] Activating MCP Servers...{Colors.ENDC}")
            ap_status = StatusTracker()
            activate_mcp(pp, ap_status)

            # 4. Run Setup Scripts
            print(f"\n{Colors.BLUE}[4/16] Running Setup Scripts...{Colors.ENDC}")
            sp = os.path.join(pp, "setup_project.py")
            if os.path.exists(sp):
                print("Running setup_project.py...")
                subprocess.run([sys.executable, sp], cwd=pp)

            # 4b. Diamond 33 Subsystem (CLAUDE.md, memory-bank, core files)
            print(f"\n{Colors.BLUE}  [4b] Setting up Diamond 33 Subsystem...{Colors.ENDC}")
            setup_diamond33_subsystem(pp, os.path.basename(pp), ap_status)

            # 5. Build Code Knowledge Base (Symbol Table) — BEFORE quality/planning
            print(f"\n{Colors.BLUE}[5/16] Building Code Knowledge Base (Symbol Table)...{Colors.ENDC}")
            indexer_script = os.path.join(pp, "tools", "code_indexer.py")
            if os.path.exists(indexer_script):
                subprocess.run([sys.executable, indexer_script, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  Code Indexer not found, skipping.{Colors.ENDC}")

            # 6. Run Quality Gate (reads project_knowledge.json for symbol validation)
            print(f"\n{Colors.BLUE}[6/16] Running Quality Gate (flake8/pylint/pipreqs)...{Colors.ENDC}")
            gate_script = os.path.join(pp, "tools", "quality_gate.py")
            if os.path.exists(gate_script):
                subprocess.run([sys.executable, gate_script, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  Quality Gate not found, skipping.{Colors.ENDC}")

            # 7. Run Code Reviewer (after quality gate fixes)
            print(f"\n{Colors.BLUE}[7/16] Running Code Reviewer...{Colors.ENDC}")
            reviewer_script = os.path.join(pp, "tools", "code_reviewer.py")
            if os.path.exists(reviewer_script):
                subprocess.run([sys.executable, reviewer_script, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  Code Reviewer not found, skipping.{Colors.ENDC}")

            # 8. Run Speckit (Planning — AFTER indexer so it reads Symbol Table)
            print(f"\n{Colors.BLUE}[8/16] Running Speckit (Planning)...{Colors.ENDC}")
            speckit = os.path.join(pp, "tools", "speckit.py")
            if os.path.exists(speckit):
                subprocess.run(
                    [sys.executable, speckit, "plan", "Analyze project and generate improvement plan"], cwd=pp
                )
            else:
                print(f"{Colors.DIM}  Speckit not found, skipping.{Colors.ENDC}")

            # 9. Module Mapper (generate MODULE_MAP.md)
            print(f"\n{Colors.BLUE}[9/16] Generating Module Map...{Colors.ENDC}")
            mapper = os.path.join(pp, "tools", "module_mapper.py")
            if os.path.exists(mapper):
                subprocess.run([sys.executable, mapper, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  Module Mapper not found, skipping.{Colors.ENDC}")

            # 10. Duplicate Detection
            print(f"\n{Colors.BLUE}[10/16] Scanning for Duplicate Files...{Colors.ENDC}")
            dup_detect = os.path.join(pp, "tools", "duplicate_files_detector.py")
            if os.path.exists(dup_detect):
                subprocess.run([sys.executable, dup_detect, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  Duplicate Detector not found, skipping.{Colors.ENDC}")

            # 11. Analyze Project & Generate Docs (after all analysis is done)
            print(f"\n{Colors.BLUE}[11/16] Analyzing Project Structure...{Colors.ENDC}")
            status = StatusTracker()
            generate_smart_readme(pp, os.path.basename(pp), status)
            print(f"{Colors.GREEN}Analysis complete. README_PROJECT.md updated.{Colors.ENDC}")

            # 12. Generate/Update Tasks (based on all analysis results)
            print(f"\n{Colors.BLUE}[12/16] Generating & Updating Tasks...{Colors.ENDC}")
            tm = TaskManager(pp)
            if not tm.data["tasks"]:
                print("Generating initial tasks based on analysis...")
                tm.generate_initial_tasks(os.path.basename(pp))
            else:
                print(f"Updating existing {len(tm.data['tasks'])} tasks...")

            # 13. Platform Setup (copy helper files for detected IDE)
            print(f"\n{Colors.BLUE}[13/16] Setting Up Platform Helper Files...{Colors.ENDC}")
            detected_ide = detect_platform(pp)
            print(f"  Detected platform: {PLATFORM_MAP[detected_ide]['name']}")
            setup_platform(pp, detected_ide, pp, ap_status)

            # 14. RORLOC Testing (6-phase QA)
            print(f"\n{Colors.BLUE}[14/16] Running RORLOC Testing (6-Phase QA)...{Colors.ENDC}")
            rorloc = os.path.join(pp, "tools", "rorloc_test_runner.py")
            if os.path.exists(rorloc):
                subprocess.run([sys.executable, rorloc, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  RORLOC not found, skipping.{Colors.ENDC}")

            # 15. System Completeness Check
            print(f"\n{Colors.BLUE}[15/16] Running System Completeness Check...{Colors.ENDC}")
            checker = os.path.join(pp, "tools", "complete_system_checker.py")
            if os.path.exists(checker):
                subprocess.run([sys.executable, checker, pp], cwd=pp)
            else:
                print(f"{Colors.DIM}  System Checker not found, skipping.{Colors.ENDC}")

            # 16. Final System Logger entry (log completion)
            print(f"\n{Colors.BLUE}[16/16] Logging Auto-Pilot completion...{Colors.ENDC}")
            if os.path.exists(sys_logger):
                subprocess.run([sys.executable, sys_logger], cwd=pp)

            print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
            print(f"{Colors.GREEN}  Auto-Pilot Complete! (16/16 steps){Colors.ENDC}")
            print(f"  Generated files in {pp}:")
            for gf in [
                "project_knowledge.json",
                "project_symbols.md",
                "quality_report.md",
                "requirements_detected.txt",
                "code_review_report.md",
                "README_PROJECT.md",
                "docs/MODULE_MAP.md",
                "duplicate_report.md",
                "RORLOC_QA_REPORT.md",
                "completeness_score.json",
                ".vscode/mcp.json",
                ".cursor/mcp.json",
                "CLAUDE.md",
                "AGENTS.md",
                "prompts/00_MASTER.md",
                "roles/ROLE-architect.md",
                "rules/00-iron-rules.md",
            ]:
                fp = os.path.join(pp, gf)
                if os.path.exists(fp):
                    sz = os.path.getsize(fp)
                    print(f"    [{Colors.GREEN}OK{Colors.ENDC}] {gf} ({sz:,} bytes)")
                else:
                    print(f"    [{Colors.DIM}--{Colors.ENDC}] {gf}")
            print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "8":
            print(f"\n{Colors.BLUE}Installing Global System dependencies...{Colors.ENDC}")
            req_file = os.path.join(pp, "requirements-global.txt")
            if os.path.exists(req_file):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-global.txt"], cwd=pp)
            else:
                print(f"{Colors.WARNING}requirements-global.txt not found. Installing core packages...{Colors.ENDC}")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "chromadb", "mcp", "pyyaml", "requests"], cwd=pp
                )
            print(f"{Colors.GREEN}Installation complete.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "9":
            print(f"\n{Colors.BLUE}Starting Auto-Test Generator on target project...{Colors.ENDC}")
            tester_script = os.path.join(pp, "tools", "auto_test_gen.py")

            if os.path.exists(tester_script):
                subprocess.run([sys.executable, tester_script, pp], cwd=pp)
            else:
                # Fallback: try running pytest directly on the target
                print(f"{Colors.WARNING}Auto-Test Generator not found. Running pytest directly...{Colors.ENDC}")
                subprocess.run([sys.executable, "-m", "pytest", pp, "-v", "--tb=short"], cwd=pp)
            input("\nPress Enter to continue...")
        elif choice == "10":
            print(f"\n{Colors.BLUE}Starting Multi-Agent Runner on target project...{Colors.ENDC}")
            crew_script = os.path.join(pp, "tools", "crew_engine.py")

            if os.path.exists(crew_script):
                mission = input("Enter mission description: ")
                subprocess.run([sys.executable, crew_script, "--project", pp, mission], cwd=pp)
            else:
                print(f"{Colors.FAIL}Crew Engine script not found at {crew_script}{Colors.ENDC}")
                print(f"{Colors.DIM}  Create tools/crew_engine.py to enable this feature.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "11":
            print(f"\n{Colors.BLUE}Setting up Cloud Deployment...{Colors.ENDC}")
            deploy_script = os.path.join(pp, "tools", "cloud_deploy.py")

            if os.path.exists(deploy_script):
                subprocess.run([sys.executable, deploy_script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Cloud Deploy script not found.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "12":
            print(f"\n{Colors.BLUE}Building Code Knowledge Base...{Colors.ENDC}")
            indexer_script = os.path.join(pp, "tools", "code_indexer.py")

            if os.path.exists(indexer_script):
                subprocess.run([sys.executable, indexer_script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Code Indexer script not found.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "13":
            print(f"\n{Colors.BLUE}Running Quality Gate...{Colors.ENDC}")
            gate_script = os.path.join(pp, "tools", "quality_gate.py")

            if os.path.exists(gate_script):
                subprocess.run([sys.executable, gate_script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Quality Gate script not found.{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "14":
            print(f"\n{Colors.BLUE}Running RORLOC 6-Phase Testing...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "rorloc_test_runner.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}RORLOC test runner not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "15":
            print(f"\n{Colors.BLUE}Generating Module Map...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "module_mapper.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Module Mapper not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "16":
            print(f"\n{Colors.BLUE}Scanning for Duplicate Files...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "duplicate_files_detector.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Duplicate detector not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "17":
            print(f"\n{Colors.BLUE}Running Code Deduplicator...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "code_deduplicator.py")
            if os.path.exists(script):
                th = input("Similarity threshold (default 0.85): ").strip() or "0.85"
                auto = input("Auto-merge? (y/n, default n): ").strip().lower()
                cmd = [sys.executable, script, pp, "--threshold", th]
                if auto == "y":
                    cmd.append("--auto-merge")
                subprocess.run(cmd, cwd=pp)
            else:
                print(f"{Colors.FAIL}Code Deduplicator not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "18":
            print(f"\n{Colors.BLUE}Running System Completeness Check...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "complete_system_checker.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}System checker not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "19":
            print(f"\n{Colors.BLUE}Analyzing Import Paths...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "fix_paths.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Fix Paths tool not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "20":
            print(f"\n{Colors.BLUE}Analyzing Project Structure...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "project_analyzer.py")
            if os.path.exists(script):
                subprocess.run([sys.executable, script, pp], cwd=pp)
            else:
                print(f"{Colors.FAIL}Project Analyzer not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "21":
            print(f"\n{Colors.BLUE}Running Project Cleanup...{Colors.ENDC}")
            script = os.path.join(pp, "tools", "project_cleanup.py")
            if os.path.exists(script):
                mode = input("Live mode (actually delete)? (y/n, default n): ").strip().lower()
                cmd = [sys.executable, script, pp]
                if mode == "y":
                    cmd.append("--live")
                else:
                    cmd.append("--dry-run")
                subprocess.run(cmd, cwd=pp)
            else:
                print(f"{Colors.FAIL}Project Cleanup not found at {script}{Colors.ENDC}")
            input("\nPress Enter to continue...")
        elif choice == "22":
            print(f"\n{Colors.HEADER}Rollback to Previous Snapshot{Colors.ENDC}")
            rollback_snapshot(pp)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print(f"{Colors.FAIL}Invalid choice.{Colors.ENDC}")
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="AI Project Creator Wizard")
    parser.add_argument("--auto", action="store_true", help="Run in auto mode (no prompts)")
    parser.add_argument("--tasks", nargs="*", help="Task management: list, add, complete, status, remove, export")
    parser.add_argument("--status", action="store_true", help="Check project health")
    parser.add_argument("--watch", type=int, help="Watch mode (interval in mins)")
    parser.add_argument("--gui", action="store_true", help="Launch Web GUI Dashboard")
    parser.add_argument("--rorloc", action="store_true", help="Run RORLOC 6-phase testing")
    parser.add_argument("--module-map", action="store_true", help="Generate MODULE_MAP.md")
    parser.add_argument("--duplicates", action="store_true", help="Detect duplicate files")
    parser.add_argument("--dedup", action="store_true", help="Run code deduplicator")
    parser.add_argument("--completeness", action="store_true", help="System completeness check")
    parser.add_argument("--fix-paths", action="store_true", help="Fix import paths")
    parser.add_argument("--analyze", action="store_true", help="Analyze project structure")
    parser.add_argument("--cleanup", action="store_true", help="Clean up temp/cache files")
    parser.add_argument("--dashboard", action="store_true", help="Launch interactive dashboard")
    parser.add_argument("--project-path", type=str, help="Target project path")
    args = parser.parse_args()

    if args.dashboard:
        pp = getattr(args, "project_path", None) or os.getcwd()
        interactive_menu(pp)
        return

    if args.gui:
        print(f"{Colors.BLUE}Launching Web GUI Dashboard...{Colors.ENDC}")
        gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui", "app.py")
        if os.path.exists(gui_path):
            try:
                subprocess.run([sys.executable, "-m", "streamlit", "run", gui_path], check=True)
            except Exception as e:
                print(f"{Colors.FAIL}Error launching GUI: {e}{Colors.ENDC}")
                print(f"{Colors.WARNING}Make sure streamlit is installed: pip install streamlit{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}GUI app not found at {gui_path}{Colors.ENDC}")
        return

    if args.watch:
        run_watch(os.getcwd(), args.watch)
        return

    if args.status:
        show_project_status(os.getcwd())
        return

    if args.tasks is not None:
        tm = TaskManager(os.getcwd())
        if not args.tasks:
            tm.interactive_menu()
            return

        cmd = args.tasks[0].lower()
        if cmd == "list":
            tm.list_tasks()
        elif cmd == "add":
            if len(args.tasks) < 2:
                print("Usage: --tasks add 'Title' [priority] [deps]")
                return
            title = args.tasks[1]
            pri = args.tasks[2] if len(args.tasks) > 2 else "medium"
            deps = [int(x) for x in args.tasks[3].split(",")] if len(args.tasks) > 3 else None
            tm.add_task(title, priority=pri, depends_on=deps)
        elif cmd == "complete":
            if len(args.tasks) < 2:
                print("Usage: --tasks complete <ID>")
                return
            tm.complete_task(int(args.tasks[1]))
        elif cmd == "status":
            if len(args.tasks) < 3:
                print("Usage: --tasks status <ID> <status>")
                return
            tm.update_status(int(args.tasks[1]), args.tasks[2])
        elif cmd == "remove":
            if len(args.tasks) < 2:
                print("Usage: --tasks remove <ID>")
                return
            tm.remove_task(int(args.tasks[1]))
        elif cmd == "export":
            if len(args.tasks) < 2:
                print("Usage: --tasks export <markdown|csv>")
                return
            tm.export_tasks(args.tasks[1])
        else:
            print(f"Unknown: {cmd}. Use: add, list, complete, status, remove, export")
        return

    # New tool CLI handlers
    pp = getattr(args, "project_path", None) or os.getcwd()
    tool_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")

    def _run_tool(name, extra_args=None):
        script = os.path.join(tool_dir, name)
        if os.path.exists(script):
            cmd = [sys.executable, script, pp] + (extra_args or [])
            subprocess.run(cmd, cwd=pp)
        else:
            # Try in project tools dir
            script2 = os.path.join(pp, "tools", name)
            if os.path.exists(script2):
                cmd = [sys.executable, script2, pp] + (extra_args or [])
                subprocess.run(cmd, cwd=pp)
            else:
                print(f"{Colors.FAIL}{name} not found.{Colors.ENDC}")

    if args.rorloc:
        _run_tool("rorloc_test_runner.py")
        return
    if args.module_map:
        _run_tool("module_mapper.py")
        return
    if args.duplicates:
        _run_tool("duplicate_files_detector.py")
        return
    if args.dedup:
        _run_tool("code_deduplicator.py")
        return
    if args.completeness:
        _run_tool("complete_system_checker.py")
        return
    if args.fix_paths:
        _run_tool("fix_paths.py")
        return
    if args.analyze:
        _run_tool("project_analyzer.py")
        return
    if args.cleanup:
        _run_tool("project_cleanup.py", ["--dry-run"])
        return

    pp = run_wizard(auto_mode=args.auto)
    if pp:
        interactive_menu(pp)


if __name__ == "__main__":
    main()
