import os
import shutil
import hashlib
import sys
from datetime import datetime

# Configuration
DRY_RUN = True
ROOT_DIR = os.getcwd()

# patterns to ignore
IGNORE_PATTERNS = [
    ".git", ".github", "node_modules", "venv", "__pycache__", ".idea", ".vscode", 
    "dist", "build", "coverage", "htmlcov", ".mypy_cache", ".pytest_cache",
    "project_cleanup.py", ".gemini"
]

# Backend files to KEEP in root
BACKEND_KEEP = [
    "app.py", "wsgi.py", "requirements.txt", "Dockerfile", "docker-entrypoint.sh",
    "docker-compose.yml", "Makefile", "conftest.py", "pytest.ini", ".env", ".env.example",
    "alembic.ini", "gunicorn_config.py"
]

def log(msg):
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    except Exception:
        try:
            safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {safe_msg}")
        except:
            pass
    sys.stdout.flush()

def ensure_dir(path):
    if not os.path.exists(path):
        if DRY_RUN:
            log(f"[DRY-RUN] Create directory: {path}")
        else:
            os.makedirs(path, exist_ok=True)
            log(f"Created directory: {path}")

def move_file(src, dst):
    if src == dst:
        return
    if os.path.exists(dst):
        # Rename if exists
        base, ext = os.path.splitext(dst)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dst = f"{base}_{timestamp}{ext}"
        
    if DRY_RUN:
        log(f"[DRY-RUN] MOVE {src} -> {dst}")
    else:
        try:
            ensure_dir(os.path.dirname(dst))
            shutil.move(src, dst)
            log(f"MOVED {src} -> {dst}")
        except Exception as e:
            log(f"ERROR moving {src}: {e}")

def delete_dir(path):
    if DRY_RUN:
        log(f"[DRY-RUN] DELETE DIR {path}")
    else:
        try:
            shutil.rmtree(path)
            log(f"DELETED DIR {path}")
        except Exception as e:
            log(f"ERROR deleting {path}: {e}")

def process_backend_clutter():
    log("Scanning backend root for clutter...")
    backend_dir = os.path.join(ROOT_DIR, "backend")
    if not os.path.exists(backend_dir):
        return

    archive_dir = os.path.join(backend_dir, "archive")
    logs_dir = os.path.join(backend_dir, "logs")
    scripts_dir = os.path.join(ROOT_DIR, "scripts", "backend_utils")
    docs_archive = os.path.join(ROOT_DIR, "docs", "archive")

    for item in os.listdir(backend_dir):
        path = os.path.join(backend_dir, item)
        
        if os.path.isdir(path):
            if item in ["tmp", "temp", "__pycache__", "htmlcov", "local_db"]:
                delete_dir(path)
            continue
            
        # Files
        if item in BACKEND_KEEP:
            continue
            
        ext = os.path.splitext(item)[1].lower()
        
        # Python files
        if ext == ".py":
            # Heuristic: if it starts with 'test_', it's a test.
            # If it's 'create_admin', 'setup_db', it's a script.
            # If it's 'simple_app', 'minimal_server', it's archive.
            
            if item.startswith("test_"):
                 move_file(path, os.path.join(archive_dir, "tests", item))
            elif any(x in item for x in ["create_", "setup_", "init_", "update_", "fix_", "run_", "check_", "validate_", "migrate_"]):
                 move_file(path, os.path.join(scripts_dir, item))
            else:
                 move_file(path, os.path.join(archive_dir, item))

        # Logs
        elif ext == ".log":
            move_file(path, os.path.join(logs_dir, item))
            
        # JSON Reports
        elif ext == ".json" and ("report" in item or "analysis" in item or "result" in item):
            move_file(path, os.path.join(docs_archive, item))
            
        # Archives/Zips
        elif ext in [".zip", ".tar", ".gz"]:
             move_file(path, os.path.join(archive_dir, "backups", item))
             
        # Text/MD files in backend?
        elif ext in [".md", ".txt"]:
            if item.lower() not in ["requirements.txt", "readme.md"]:
                 move_file(path, os.path.join(docs_archive, item))

def main():
    global DRY_RUN
    if len(sys.argv) > 1 and "--execute" in sys.argv:
        DRY_RUN = False
    else:
        DRY_RUN = True
        
    print(f"Starting Backend Cleanup (Mode: {'DRY RUN' if DRY_RUN else 'EXECUTE'})")
    process_backend_clutter()
    print("Cleanup Completed.")

if __name__ == "__main__":
    main()
