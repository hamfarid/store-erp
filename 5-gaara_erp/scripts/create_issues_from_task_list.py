#!/usr/bin/env python3
"""
FILE: scripts/create_issues_from_task_list.py | PURPOSE: Parse docs/Task_List.md and create/update GitHub Issues for each task | OWNER: DX | RELATED: docs/Task_List.md, .github/workflows/create_issues_from_task_list.yml | LAST-AUDITED: 2025-10-24

Usage:
    - Environment variables required:
            GITHUB_TOKEN: GitHub token with repo:issues scope (in GitHub Actions, use secrets.GITHUB_TOKEN)
            GITHUB_REPOSITORY: "owner/repo" (automatically set in GitHub Actions)
    - Optional arguments:
            --dry-run           Do not create issues, just print the plan
            --file PATH         Path to Task_List.md (default: docs/Task_List.md)
            --reopen-closed     If a matching closed issue exists (by TL-ID), reopen and update it instead of creating a new issue

Behavior:
    - Parses numbered tasks in Task_List.md across P0..P3 sections
    - Creates a GitHub issue per task with labels: Priority (P0..P3), Area (area:*), and source:task-list
    - Idempotent: If an open issue already exists containing hidden marker <!-- TL-ID:<n> -->, it is updated instead of duplicated
    - If only a closed issue exists with the TL-ID marker: by default, skip creating a new issue; with --reopen-closed, reopen+update it
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote as url_quote

TASK_LINE_RE = re.compile(r"^(?P<num>\d+)\.\s*\[(?P<status>.|\s)\]\s*\*\*(?P<title>.+?)\*\*\s*—\s*(?P<meta>.+)$")
SECTION_PRIORITY_RE = re.compile(r"^##\s*(?P<priority>P[0-3])\s*—\s*(?P<name>.+)$")
SUBSECTION_AREA_RE = re.compile(r"^###\s*(?P<area>.+?)\s*\((?P<priority>P[0-3])\)")
OWNER_TOKEN_RE = re.compile(r"\[(AA|Sec|BE|FE|DBA|DX)\]")
ESTIMATE_RE = re.compile(r"\[(?P<estimate>[0-9]+\.?[0-9]*)h\]")
DEPS_RE = re.compile(r"Task\s*#(?P<dep>\d+)")

AREA_MAP = {
    "Authentication & Session Management": "area:Security",
    "Authorization & RBAC": "area:Security",
    "HTTPS & Transport Security": "area:Security",
    "Secrets Management": "area:Security",
    "Database Security": "area:DB",
    "Input Validation": "area:API",
    "Deployment Security": "area:DX",
    "API Governance": "area:API",
    "Database": "area:DB",
    "Security Hardening": "area:Security",
    "Frontend Security": "area:FE",
    "RAG Middleware": "area:RAG",
    "Testing": "area:Testing",
    "Documentation": "area:Docs",
    "CI/CD": "area:DX",
    "GitHub Integration": "area:DX",
    "Observability": "area:DX",
    "UI/Brand": "area:UI",
    "Data Quality": "area:DB",
    "Backup & DR": "area:DX",
    "Resilience": "area:DX",
    "Multi-Tenancy": "area:BE",
    "Performance Optimization": "area:Perf",
    "Developer Experience": "area:DX",
    "Feature Enhancements": "area:BE",
    "Analytics & Reporting": "area:BE",
    "Internationalization": "area:FE",
    "Compliance & Privacy": "area:Security",
    "Infrastructure as Code": "area:DX",
    "Monitoring & Alerting": "area:DX",
    "Code Quality": "area:DX",
    "Multi-Region": "area:DX",
    "Advanced Features": "area:BE",
    "Machine Learning": "area:ML",
    "Advanced UI": "area:UI",
    "Infrastructure Enhancements": "area:DX",
    "Documentation & Knowledge Management": "area:Docs",
    "Security Enhancements": "area:Security",
    "Performance & Optimization": "area:Perf",
    "Testing Enhancements": "area:Testing",
    "Accessibility": "area:A11y",
    "Localization": "area:I18n",
    "DevEx & Tooling": "area:DX",
    "Business Intelligence": "area:BI",
    "Legacy Cleanup": "area:DX",
}

OWNER_TO_LABEL = {
    "AA": "owner:AA",
    "Sec": "owner:Security",
    "BE": "owner:Backend",
    "FE": "owner:Frontend",
    "DBA": "owner:DBA",
    "DX": "owner:DX",
}

PRIORITY_LABELS = {"P0", "P1", "P2", "P3"}
BASE_LABELS = {"source:task-list"}


def parse_tasks(md_text: str) -> List[Dict]:
    lines = md_text.splitlines()
    tasks: List[Dict] = []
    current_priority: Optional[str] = None
    current_area: Optional[str] = None
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        sec_m = SECTION_PRIORITY_RE.match(line)
        if sec_m:
            current_priority = sec_m.group("priority")
            i += 1
            continue
        sub_m = SUBSECTION_AREA_RE.match(line)
        if sub_m:
            # Use the visible area title
            current_area = sub_m.group("area").strip()
            i += 1
            continue
        m = TASK_LINE_RE.match(line)
        if m:
            num = int(m.group("num"))
            title = m.group("title").strip()
            meta = m.group("meta")
            owners = OWNER_TOKEN_RE.findall(meta)
            est = None
            est_m = ESTIMATE_RE.search(meta)
            if est_m:
                est = est_m.group("estimate")
            deps = [int(d) for d in DEPS_RE.findall(line)]
            # Collect bullet lines under this task
            body_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if TASK_LINE_RE.match(next_line) or SECTION_PRIORITY_RE.match(next_line) or SUBSECTION_AREA_RE.match(next_line):
                    break
                body_lines.append(next_line)
                j += 1
            body = "\n".join(body_lines).strip()
            area_label = AREA_MAP.get(current_area or "", "area:Uncategorized")
            prio = current_priority or "P?"
            tasks.append({
                "id": num,
                "title": title,
                "priority": prio,
                "owners": owners,
                "estimate_h": est,
                "deps": deps,
                "area": current_area,
                "area_label": area_label,
                "body": body,
            })
            i = j
            continue
        i += 1
    return tasks


def get_repo_env() -> Tuple[str, str]:
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo:
        try:
            owner, name = repo.split("/")
            return owner, name
        except ValueError:
            pass
    # Fallback: try to infer from git remote if needed (not implemented)
    raise RuntimeError("GITHUB_REPOSITORY is not set (expected 'owner/repo')")


def gh_api(token: str, method: str, url: str, **kwargs):
    # Lazy import so --dry-run can work without requests installed locally
    import requests  # type: ignore
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    headers["Accept"] = "application/vnd.github+json"
    headers["X-GitHub-Api-Version"] = "2022-11-28"
    # Add safe timeouts to avoid indefinite hangs
    resp = requests.request(method, url, headers=headers, timeout=(10, 30), **kwargs)
    if resp.status_code >= 400:
        raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text}")
    return resp


def ensure_labels(token: str, owner: str, repo: str, labels: List[str]):
    # Get existing labels (paginate up to a few pages)
    existing = set()
    page = 1
    while True:
        r = gh_api(token, "GET", f"https://api.github.com/repos/{owner}/{repo}/labels?per_page=100&page={page}")
        lst = r.json()
        if not lst:
            break
        for item in lst:
            existing.add(item["name"])
        page += 1
    for label in labels:
        if label not in existing:
            # Create simple labels with deterministic colors
            color = "ededed"
            if label in PRIORITY_LABELS:
                color = {"P0": "d73a4a", "P1": "fbca04", "P2": "0e8a16", "P3": "5319e7"}.get(label, "ededed")
            elif label.startswith("area:"):
                color = "0366d6"
            elif label.startswith("owner:"):
                color = "6f42c1"
            elif label == "source:task-list":
                color = "6a737d"
            gh_api(token, "POST", f"https://api.github.com/repos/{owner}/{repo}/labels", json={"name": label, "color": color})


def find_existing_issue(token: str, owner: str, repo: str, tl_id: int, include_closed: bool = False) -> Optional[Dict]:
    # Search open first
    q_open = f"repo:{owner}/{repo} in:body is:issue is:open TL-ID:{tl_id}"
    r = gh_api(token, "GET", f"https://api.github.com/search/issues?q={url_quote(q_open)}")
    items = r.json().get("items", [])
    if items:
        return items[0]
    if include_closed:
        q_closed = f"repo:{owner}/{repo} in:body is:issue is:closed TL-ID:{tl_id}"
        r2 = gh_api(token, "GET", f"https://api.github.com/search/issues?q={url_quote(q_closed)}")
        items2 = r2.json().get("items", [])
        return items2[0] if items2 else None
    return None


def upsert_issue(token: str, owner: str, repo: str, task: Dict, dry_run: bool = False, reopen_closed: bool = False) -> int:
    tl_id = task["id"]
    title = f"[{task['priority']}] {task['title']}"
    labels = set(BASE_LABELS)
    if task["priority"] in PRIORITY_LABELS:
        labels.add(task["priority"])
    if task["area_label"]:
        labels.add(task["area_label"])
    for o in task["owners"]:
        if o in OWNER_TO_LABEL:
            labels.add(OWNER_TO_LABEL[o])
    labels = sorted(labels)

    body_parts = [
        f"<!-- TL-ID:{tl_id} -->",
        f"Task ID: TL-{tl_id}",
        "",
        "Source: docs/Task_List.md",
        f"Priority: {task['priority']}",
        f"Area: {task.get('area') or 'Uncategorized'}",
        f"Owners: {' '.join(task['owners']) if task['owners'] else 'Unassigned'}",
        f"Estimate: {task['estimate_h']}h" if task['estimate_h'] else "Estimate: n/a",
        "",
        "Details:",
        task["body"] or "(no additional details)",
    ]
    if task["deps"]:
        deps_str = ", ".join([f"TL-{d}" for d in task["deps"]])
        body_parts += ["", f"Dependencies: {deps_str}"]
    body = "\n".join(body_parts)

    if dry_run:
        print(f"DRY RUN: Would upsert issue for TL-{tl_id}: {title} | labels={labels}")
        return -1

    ensure_labels(token, owner, repo, labels)

    existing = find_existing_issue(token, owner, repo, tl_id, include_closed=True)
    if existing:
        # Coerce to explicit types for type-checkers and safety
        issue_number = int(existing.get("number", -1))
        state = str(existing.get("state", ""))
        if state == "closed" and not reopen_closed:
            # Respect closed state; skip creating a duplicate
            print(f"SKIP: TL-{tl_id} has a closed issue #{issue_number}; use --reopen-closed to reopen.")
            return int(issue_number)
        # If closed and reopen requested, reopen first
        if state == "closed" and reopen_closed:
            gh_api(token, "PATCH", f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}", json={
                "state": "open"
            })
        # Update title/body/labels
        gh_api(token, "PATCH", f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}", json={
            "title": title,
            "body": body,
            "labels": labels,
        })
        return int(issue_number)
    r = gh_api(token, "POST", f"https://api.github.com/repos/{owner}/{repo}/issues", json={
        "title": title,
        "body": body,
        "labels": labels,
    })
    try:
        num = r.json().get("number")
    except Exception:
        num = None
    return int(num or -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="docs/Task_List.md")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reopen-closed", action="store_true")
    ap.add_argument("--output", help="Optional path to write a pure-JSON results file")
    ap.add_argument("--priority", help="Comma-separated priorities to include e.g. P0,P1")
    ap.add_argument("--ids", help="Comma-separated list of task IDs to include e.g. 1,2,10")
    ap.add_argument("--id-range", help="ID range to include e.g. 1-40")
    ap.add_argument("--limit", type=int, help="Process only the first N tasks after filtering/sorting")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and not args.dry_run:
        print("Error: GITHUB_TOKEN (or GH_TOKEN) environment variable is required (omit for --dry-run)", file=sys.stderr)
        sys.exit(2)
    if not token and args.dry_run:
        token = "DUMMY"
    # Help type-checkers: by here, token is guaranteed to be a string
    assert token is not None

    # Repository context
    try:
        owner, repo = get_repo_env()
    except RuntimeError:
        if args.dry_run:
            owner, repo = ("owner", "repo")
        else:
            raise

    with open(args.file, "r", encoding="utf-8") as f:
        md = f.read()
    tasks = parse_tasks(md)
    if not tasks:
        print("No tasks parsed from Task_List.md; nothing to do.")
        return

    # Process in order of priority P0..P3 then by id
    prio_map = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    tasks.sort(key=lambda t: (prio_map.get(t["priority"], 9), t["id"]))

    # Optional filters
    if args.priority:
        wanted = {p.strip() for p in args.priority.split(",") if p.strip()}
        tasks = [t for t in tasks if t.get("priority") in wanted]

    id_allow: Optional[set] = None
    if args.ids:
        try:
            id_allow = {int(x.strip()) for x in args.ids.split(",") if x.strip()}
        except ValueError:
            print("Warning: --ids contains non-integer values; ignoring.", file=sys.stderr)
            id_allow = None
    if args.id_range:
        try:
            a, b = args.id_range.split("-", 1)
            lo, hi = int(a), int(b)
            rng = set(range(min(lo, hi), max(lo, hi) + 1))
            id_allow = rng if id_allow is None else (id_allow & rng)
        except Exception:
            print("Warning: --id-range must be like '1-40'; ignoring.", file=sys.stderr)
    if id_allow is not None:
        tasks = [t for t in tasks if t.get("id") in id_allow]

    if args.limit is not None and args.limit >= 0:
        tasks = tasks[: args.limit]

    created = []
    for t in tasks:
        num = upsert_issue(token, owner, repo, t, dry_run=args.dry_run, reopen_closed=args.reopen_closed)
        created.append({"id": t["id"], "issue": num})
        print(f"Upserted TL-{t['id']} -> issue #{num}")
    result = {"count": len(created), "results": created}
    print(json.dumps(result, indent=2))
    # Optionally write a clean JSON file for CI summary/artifacts
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: failed to write output file {args.output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
