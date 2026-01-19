#!/usr/bin/env bash
set -euo pipefail

echo "== Gaara Scan AI - Security Scan =="

if [ -f "./frontend/package.json" ] && command -v npm >/dev/null 2>&1; then
  echo
  echo "[Frontend] npm audit (omit dev, audit-level=high)"
  (cd frontend && npm audit --omit=dev --audit-level=high)
else
  echo "[Frontend] npm not found or frontend/package.json missing; skipping."
fi

if [ -f "./backend/requirements.txt" ] && command -v python >/dev/null 2>&1; then
  if command -v safety >/dev/null 2>&1; then
    echo
    echo "[Backend] safety check (requirements.txt)"
    (cd backend && safety check -r requirements.txt --full-report)
  else
    echo "[Backend] safety not installed; try: pip install -r backend/requirements-test.txt"
  fi

  if command -v bandit >/dev/null 2>&1; then
    echo
    echo "[Backend] bandit scan (backend/src)"
    bandit -r ./backend/src -ll
  else
    echo "[Backend] bandit not installed; try: pip install -r backend/requirements-test.txt"
  fi

  if command -v semgrep >/dev/null 2>&1; then
    echo
    echo "[Backend] semgrep scan (auto config)"
    semgrep scan --config auto ./backend/src
  else
    echo "[Backend] semgrep not installed (optional); try: pip install -r backend/requirements-test.txt"
  fi
else
  echo "[Backend] python not found or backend/requirements.txt missing; skipping."
fi

echo
echo "Done."

