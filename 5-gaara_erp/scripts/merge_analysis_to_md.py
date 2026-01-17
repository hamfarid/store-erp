#!/usr/bin/env python
"""
Merge analyzer JSON outputs under ./data into Markdown docs with graphs and per-module inventories.
- docs/analysis/MODULES_OVERVIEW.md: summary, top dependencies, counts
- docs/analysis/MODULE_GRAPH_MERMAID.md: Mermaid graph (flowchart LR)
- docs/analysis/modules/<module>.md: inventory of classes/functions/variables

Idempotent; overwrites outputs each run.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = ROOT / "docs" / "analysis"
MODULES_DIR = OUT_DIR / "modules"

OUT_DIR.mkdir(parents=True, exist_ok=True)
MODULES_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def glob_all_module_jsons():
    # Heuristic: per-file analyzer saved files as dotted module paths with .json
    # Skip aggregator files
    for p in DATA.glob("**/*.json"):
        name = p.name.lower()
        if name in {"all_modules.json", "module_graph.json", "accurate_test_verification.json"}:
            continue
        yield p


def build_module_index(all_modules: dict | None) -> dict[str, dict]:
    index: dict[str, dict] = {}
    if all_modules and isinstance(all_modules, dict) and all_modules.get("modules"):
        for m in all_modules["modules"]:
            index[m.get("module") or m.get("name") or "unknown"] = m
        return index
    # Fallback: scan each per-file JSON
    for p in glob_all_module_jsons():
        try:
            d = load_json(p)
        except Exception:
            continue
        module = d.get("module") or d.get("name")
        if not module:
            # derive from path
            rel = p.relative_to(DATA).as_posix().replace("/", ".").rsplit(".", 1)[0]
            module = rel
        index[module] = d
    return index


def summarize_graph(graph: dict[str, list[str]]):
    outdeg = {k: len(v or []) for k, v in graph.items()}
    indeg = defaultdict(int)
    for k, vs in graph.items():
        for v in vs or []:
            indeg[v] += 1
        indeg.setdefault(k, indeg.get(k, 0))
    return outdeg, dict(indeg)


def write_overview(index: dict[str, dict], graph: dict[str, list[str]], outdeg: dict[str, int], indeg: dict[str, int]):
    total_modules = len(index)
    total_edges = sum(len(v or []) for v in graph.values())

    def topn(d: dict[str, int], n=15):
        return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

    lines = []
    lines.append("## Modules Overview")
    lines.append("")
    lines.append(f"- Total modules: {total_modules}")
    lines.append(f"- Total dependency edges: {total_edges}")
    lines.append("")
    lines.append("### Top 15 by Outgoing Dependencies")
    for mod, deg in topn(outdeg):
        lines.append(f"- {mod}: {deg}")
    lines.append("")
    lines.append("### Top 15 by Incoming Dependencies")
    for mod, deg in topn(indeg):
        lines.append(f"- {mod}: {deg}")
    lines.append("")
    lines.append("### Module Index")
    for mod in sorted(index.keys()):
        link = (MODULES_DIR / f"{mod}.md").relative_to(OUT_DIR).as_posix()
        lines.append(f"- [{mod}]({link})")

    (OUT_DIR / "MODULES_OVERVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mermaid(graph: dict[str, list[str]]):
    lines = []
    lines.append("## Module Graph (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    # Safe node id mapping
    def nid(s: str) -> str:
        return s.replace("-", "_").replace("/", "_").replace(".", "_")
    for src, dsts in graph.items():
        if not dsts:
            # singleton node
            lines.append(f"  {nid(src)}[{src}]")
            continue
        for dst in dsts:
            lines.append(f"  {nid(src)}[{src}] --> {nid(dst)}[{dst}]")
    lines.append("```")
    (OUT_DIR / "MODULE_GRAPH_MERMAID.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_module_pages(index: dict[str, dict]):
    for mod, d in index.items():
        classes = d.get("classes") or []
        functions = d.get("functions") or []
        variables = d.get("variables") or []
        imports = d.get("imports") or []
        lines = []
        lines.append(f"# {mod}")
        lines.append("")
        if imports:
            lines.append("## Imports")
            for i in imports:
                lines.append(f"- {i}")
            lines.append("")
        if classes:
            lines.append("## Classes")
            for c in classes:
                cname = c.get("name")
                lines.append(f"- {cname}")
                for v in c.get("variables") or []:
                    lines.append(f"  - attr: `{v}`")
                for m in c.get("methods") or []:
                    lines.append(f"  - method: `{m}`")
            lines.append("")
        if functions:
            lines.append("## Functions")
            for f in functions:
                lines.append(f"- {f.get('name')}")
            lines.append("")
        if variables:
            lines.append("## Module Variables")
            for v in variables:
                lines.append(f"- `{v}`")
            lines.append("")
        (MODULES_DIR / f"{mod}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    graph_path = DATA / "module_graph.json"
    all_modules_path = DATA / "all_modules.json"

    graph = {}
    if graph_path.exists():
        try:
            graph = load_json(graph_path)
        except Exception:
            graph = {}

    all_modules = None
    if all_modules_path.exists():
        try:
            all_modules = load_json(all_modules_path)
        except Exception:
            all_modules = None

    index = build_module_index(all_modules)
    outdeg, indeg = summarize_graph(graph or {})

    write_overview(index, graph or {}, outdeg, indeg)
    write_mermaid(graph or {})
    write_module_pages(index)

    print("Generated:")
    print(" -", OUT_DIR / "MODULES_OVERVIEW.md")
    print(" -", OUT_DIR / "MODULE_GRAPH_MERMAID.md")
    print(" -", MODULES_DIR, "with", len(index), "files")


if __name__ == "__main__":
    main()

