#!/usr/bin/env python3
"""
Diff auto-generated requirements (tools/requirements_autogen.txt)
against curated requirements (requirements_final.txt) and print
which packages appear only on one side. Only compares package names,
ignores version specifiers.

Usage:
  python tools/diff_requirements.py [--auto tools/requirements_autogen.txt] [--cur requirements_final.txt]
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path


def parse_requirements(path: Path) -> dict[str, str]:
    pkgs: dict[str, str] = {}
    if not path.exists():
        return pkgs
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = re.split(r"\s*(==|~=|>=|<=|>|<)\s*", s, maxsplit=1)
        name = parts[0].strip()
        norm = re.sub(r"[^a-z0-9]+", "", name.lower())
        if norm:
            pkgs[norm] = name
    return pkgs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", default="tools/requirements_autogen.txt", type=Path)
    ap.add_argument("--cur", default="requirements_final.txt", type=Path)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero if differences are found",
    )
    args = ap.parse_args()

    auto = parse_requirements(args.auto)
    cur = parse_requirements(args.cur)

    only_auto = sorted((auto[k] for k in auto.keys() - cur.keys()), key=str.lower)
    only_cur = sorted((cur[k] for k in cur.keys() - auto.keys()), key=str.lower)

    print("=== Only in auto-generated ===")
    for p in only_auto:
        print("-", p)
    print("\n=== Only in curated ===")
    for p in only_cur:
        print("-", p)

    if args.strict and (only_auto or only_cur):
        print("\nStrict mode: differences detected. Failing.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
