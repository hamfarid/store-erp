#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Path & Import Tracing (Phase 1) - Read-only analysis tool.
Outputs:
- .github/docs/PROJECT_STRUCTURE.md
- .github/docs/Path_Analysis.json

Heuristics:
- JS/TS: import ... from 'p', require('p')
- PY: from m import X, import m
- HTML: src= / href=
- CSS: url(...)

Skips: node_modules, .git, dist, build, __pycache__, .venv
"""
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / ".github" / "docs"

SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".venv"}
TARGET_EXTS = {".js", ".jsx", ".ts", ".tsx", ".py", ".css", ".scss", ".html"}

JS_IMPORT_RE = re.compile(r"import\s+[^'\"]*from\s*['\"]([^'\"]+)['\"]")
JS_REQUIRE_RE = re.compile(r"require\(\s*['\"]([^'\"]+)['\"]\s*\)")
PY_FROM_RE = re.compile(r"from\s+([\w\.]+)\s+import\s+([\w\*,\s]+)")
PY_IMPORT_RE = re.compile(r"^\s*import\s+([\w\.]+)")
HTML_SRC_RE = re.compile(r"\b(?:src|href)=['\"]([^'\"]+)['\"]")
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")

VITE_ALIAS = {
    "@": "frontend/src",
    "@components": "frontend/src/components",
    "@pages": "frontend/src/pages",
    "@utils": "frontend/src/utils",
    "@assets": "frontend/src/assets",
}

PY_MODULE_BASES = [
    PROJECT_ROOT,                       # repo root
    PROJECT_ROOT / "backend",          # backend/
    PROJECT_ROOT / "backend" / "src", # backend/src/
]


def list_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            p = Path(dirpath) / f
            if p.suffix.lower() in TARGET_EXTS:
                files.append(p)
    return files


def make_tree(root: Path) -> str:
    def _tree(path: Path, prefix: str = "") -> List[str]:
        entries = [e for e in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())) if e.name not in SKIP_DIRS]
        lines: List[str] = []
        for i, e in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append(f"{prefix}{connector}{e.name}")
            if e.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                lines.extend(_tree(e, prefix + extension))
        return lines
    header = f"Project Structure for {root}\n\n"
    body = "\n".join([root.name, "┐"] + _tree(root))
    return header + body + "\n"


def resolve_js_path(ref: str, file_dir: Path) -> Optional[Path]:
    # alias
    for alias, target in VITE_ALIAS.items():
        if ref.startswith(alias + "/"):
            candidate = PROJECT_ROOT / target / ref[len(alias) + 1 :]
            return candidate if candidate.exists() else None
    # relative
    if ref.startswith("."):
        for ext in ("", ".js", ".jsx", ".ts", ".tsx", "/index.js", "/index.tsx"):
            cand = (file_dir / (ref + ext)).resolve()
            if cand.exists():
                return cand
    return None


def resolve_py_module(mod: str) -> Optional[Path]:
    # convert module to path: a.b.c -> a/b/c.py
    mod_path = Path(*mod.split("."))
    candidates = [mod_path.with_suffix(".py"), mod_path / "__init__.py"]
    for base in PY_MODULE_BASES:
        for c in candidates:
            p = (base / c).resolve()
            if p.exists():
                return p
    return None


def guess_symbol_defined_in(symbol: str) -> List[Path]:
    results: List[Path] = []
    for base in [PROJECT_ROOT / "backend" / "src", PROJECT_ROOT / "backend", PROJECT_ROOT]:
        for p in base.rglob("*.py"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if re.search(rf"\bclass\s+{re.escape(symbol)}\b|def\s+{re.escape(symbol)}\b", text):
                results.append(p)
    return results


def analyze_file(p: Path) -> List[Dict]:
    out: List[Dict] = []
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return out
    lines = content.splitlines()
    for i, line in enumerate(lines, start=1):
        # JS/TS
        for m in JS_IMPORT_RE.finditer(line):
            ref = m.group(1)
            resolved = resolve_js_path(ref, p.parent)
            out.append({"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "path": ref, "type": "js-import", "resolved_path": str(resolved) if resolved else None, "status": "ok" if resolved else "unknown"})
        for m in JS_REQUIRE_RE.finditer(line):
            ref = m.group(1)
            resolved = resolve_js_path(ref, p.parent)
            out.append({"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "path": ref, "type": "js-require", "resolved_path": str(resolved) if resolved else None, "status": "ok" if resolved else "unknown"})
        # PY
        fm = PY_FROM_RE.search(line)
        if fm:
            mod, names = fm.groups()
            resolved = resolve_py_module(mod)
            status = "ok" if resolved else "unknown"
            entry = {"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "module": mod, "names": [n.strip() for n in names.split(",")], "type": "py-from-import", "resolved_path": str(resolved) if resolved else None, "status": status}
            # attempt symbol search if unresolved
            if not resolved:
                suggestions: Dict[str, List[str]] = {}
                for n in entry["names"]:
                    hits = [str(h.relative_to(PROJECT_ROOT)) for h in guess_symbol_defined_in(n)][:3]
                    if hits:
                        suggestions[n] = hits
                if suggestions:
                    entry["suggestions"] = suggestions
            out.append(entry)
        im = PY_IMPORT_RE.search(line)
        if im:
            mod = im.group(1)
            resolved = resolve_py_module(mod)
            out.append({"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "module": mod, "type": "py-import", "resolved_path": str(resolved) if resolved else None, "status": "ok" if resolved else "unknown"})
        # HTML
        for m in HTML_SRC_RE.finditer(line):
            ref = m.group(1)
            out.append({"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "path": ref, "type": "html-attr", "resolved_path": None, "status": "unknown"})
        # CSS
        for m in CSS_URL_RE.finditer(line):
            ref = m.group(1)
            out.append({"file": str(p.relative_to(PROJECT_ROOT)), "line": i, "path": ref, "type": "css-url", "resolved_path": None, "status": "unknown"})
    return out


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Project Structure
    structure_md = make_tree(PROJECT_ROOT)
    (DOCS_DIR / "PROJECT_STRUCTURE.md").write_text(structure_md, encoding="utf-8")

    # 2) Path Analysis
    results: List[Dict] = []
    for f in list_files(PROJECT_ROOT):
        results.extend(analyze_file(f))
    # Mark broken if explicitly unresolved and looks local
    for r in results:
        if r.get("status") == "unknown":
            path_or_mod = r.get("path") or r.get("module")
            if path_or_mod and (str(path_or_mod).startswith((".", "@", "src", "/")) or "." in str(path_or_mod)):
                r["status"] = "broken"
    (DOCS_DIR / "Path_Analysis.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {DOCS_DIR/'PROJECT_STRUCTURE.md'} and {DOCS_DIR/'Path_Analysis.json'} with {len(results)} entries")


if __name__ == "__main__":
    main()

