import ast
import json
import os
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional

# Repository root is assumed to be the current working directory when executing this script
REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPO_ROOT / "gaara_erp"
OUTPUT_DIR = REPO_ROOT / "data"

EXCLUDE_DIR_NAMES = {
    ".venv",
    "venv",
    "__pycache__",
    "migrations",
    ".git",
    "data",
}

# Project package prefixes to consider when building the dependency graph
PROJECT_PREFIXES = (
    "core_modules",
    "business_modules",
    "admin_modules",
    "integration_modules",
    "agricultural_modules",
    "gaara_erp",  # allow absolute within project
    "settings_app",
    "users_app",
    "permissions_app",
    "dashboard",
    "reports",
)

module_graph: Dict[str, List[str]] = defaultdict(list)


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    return any(name in parts for name in EXCLUDE_DIR_NAMES)


def module_name_from_path(py_file: Path) -> str:
    rel = py_file.relative_to(PROJECT_DIR)
    return rel.as_posix().replace("/", ".").removesuffix(".py")


def analyze_file(file_path: Path) -> Optional[Dict[str, Any]]:
    try:
        source = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        return None

    module_name = module_name_from_path(file_path)

    info: Dict[str, Any] = {
        "module": module_name,
        "imports": [],
        "classes": [],
        "functions": [],
        "variables": [],
    }

    # Top-level variable collection (module scope)
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    info["variables"].append(target.id)

    # Walk for imports, classes, functions
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name
                info["imports"].append(mod)
                for prefix in PROJECT_PREFIXES:
                    if mod.startswith(prefix):
                        module_graph[module_name].append(mod)
                        break
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mod = node.module
                info["imports"].append(mod)
                for prefix in PROJECT_PREFIXES:
                    if mod.startswith(prefix):
                        module_graph[module_name].append(mod)
                        break
        elif isinstance(node, ast.ClassDef):
            class_info: Dict[str, Any] = {"name": node.name, "methods": [], "variables": []}
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    class_info["methods"].append(body_item.name)
                elif isinstance(body_item, (ast.Assign, ast.AnnAssign)):
                    targets = []
                    if isinstance(body_item, ast.Assign):
                        targets = body_item.targets
                    elif isinstance(body_item, ast.AnnAssign) and isinstance(body_item.target, ast.Name):
                        targets = [body_item.target]
                    for t in targets:
                        if isinstance(t, ast.Name):
                            class_info["variables"].append(t.id)
            info["classes"].append(class_info)
        elif isinstance(node, ast.FunctionDef):
            params = [arg.arg for arg in node.args.args]
            info["functions"].append({"name": node.name, "parameters": params})

    # Deduplicate lists
    info["imports"] = sorted(set(info["imports"]))
    module_graph[module_name] = sorted(set(module_graph[module_name]))

    return info


def scan_project() -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}
    for root, dirs, files in os.walk(PROJECT_DIR):
        # prune excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIR_NAMES]
        root_path = Path(root)
        if is_excluded(root_path):
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            file_path = root_path / file
            if is_excluded(file_path):
                continue
            info = analyze_file(file_path)
            if info is None:
                continue
            results[info["module"]] = info
    return results


def write_outputs(results: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Per-module JSON files
    for module, data in results.items():
        out_path = OUTPUT_DIR / f"{module}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Unified listing
    all_modules = list(results.values())
    (OUTPUT_DIR / "all_modules.json").write_text(
        json.dumps(all_modules, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Dependency graph
    graph_obj: Dict[str, List[str]] = {mod: deps for mod, deps in sorted(module_graph.items())}
    (OUTPUT_DIR / "module_graph.json").write_text(
        json.dumps(graph_obj, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return graph_obj


def visualize_graph(graph_obj: Dict[str, List[str]]) -> None:
    """Attempt to render a PNG graph. Falls back to DOT and Mermaid if libs unavailable."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Fallback artifacts
    # DOT
    lines = ["digraph ModuleGraph {"]
    for src, targets in graph_obj.items():
        for dst in targets:
            lines.append(f'  "{src}" -> "{dst}";')
    lines.append("}")
    (OUTPUT_DIR / "module_graph.dot").write_text("\n".join(lines), encoding="utf-8")

    # Mermaid
    m_lines = ["flowchart LR"]
    for src, targets in graph_obj.items():
        for dst in targets:
            m_lines.append(f'  {src.replace(".", "_")}-->{dst.replace(".", "_")}')
    (OUTPUT_DIR / "module_graph.mmd").write_text("\n".join(m_lines), encoding="utf-8")

    # Try networkx + matplotlib
    try:
        import networkx as nx  # type: ignore
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return  # PNG not generated, DOT/Mermaid available

    G = nx.DiGraph()
    for src, targets in graph_obj.items():
        for dst in targets:
            G.add_edge(src, dst)

    plt.figure(figsize=(16, 12))
    try:
        pos = nx.spring_layout(G, k=0.5, iterations=100)
    except Exception:
        pos = nx.random_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=800, font_size=7, arrows=True)
    plt.tight_layout()
    out_path = OUTPUT_DIR / "module_graph.png"
    plt.savefig(out_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    results = scan_project()
    graph = write_outputs(results)
    visualize_graph(graph)
    print(f"Analysis complete! Results saved in {OUTPUT_DIR}")
