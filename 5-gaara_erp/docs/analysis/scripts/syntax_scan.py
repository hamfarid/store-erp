import os
import sys
import py_compile
from pathlib import Path

EXCLUDE_DIRS = {"venv", "venv_new", ".venv",
                "node_modules", "__pycache__", "site-packages"}
# Repo root is three levels up: docs/analysis/scripts -> repo
REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "docs" / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FAIL_LOG = OUTPUT_DIR / "SyntaxFailures.txt"

failures = []

for root, dirs, files in os.walk(REPO_ROOT):
    # prune excluded dirs in-place for efficiency
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for name in files:
        if not name.endswith('.py'):
            continue
        path = Path(root) / name
        # Skip files inside any excluded path segment
        parts = set(Path(root).parts)
        if parts & EXCLUDE_DIRS:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as e:
            failures.append((str(path.relative_to(REPO_ROOT)),
                            f"{type(e).__name__}: {e}"))

with FAIL_LOG.open('w', encoding='utf-8') as f:
    if not failures:
        f.write("No syntax errors detected.\n")
    else:
        for p, err in failures:
            f.write(f"{p} :: {err}\n")
        f.write(f"\nTotal failures: {len(failures)}\n")

print(f"Scanned repository: {REPO_ROOT}")
print(f"Syntax failures: {len(failures)}")
print(f"Details written to: {FAIL_LOG}")
