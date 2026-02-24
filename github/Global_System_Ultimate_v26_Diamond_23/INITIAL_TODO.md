# 🚀 INITIAL_TODO.md (Mandatory Launch Checklist)

**Status:** Required for ALL New Projects
**Version:** v26.0.0 (Diamond Standard)
**Governance:** Global System Ultimate (2026 Standards)

This checklist MUST be completed before any code is written. It enforces the "Touch-First Rule" and ensures compliance with the 2026 AI Coding Agent Governance Framework.

---

## 🚨 THE ONE COMMAND TO RULE THEM ALL
**Execute this FIRST:**
```bash
python3 setup_project.py
```
*This script handles environment checks, dependency installation, and system verification automatically.*

---

## Phase 1: Identity & Governance (The "Who")
- [ ] **Read Identity:** Read `AGENTS.md` and `prompts/00_MASTER.md`.
- [ ] **Verify Version:** Read `VERSION` file to confirm system version (Must be v26+).
- [ ] **Acknowledge Rules:** Read `rules/ml/RULES-*.md` and confirm understanding of ML Governance.
- [ ] **Check Roles:** Verify existence of `roles/ml/` and understand your current role (Planner/Executor/Reviewer).

## Phase 2: Environment & Tooling (The "How")
- [ ] **Run Setup Script:** Confirm `python3 setup_project.py` completed successfully.
- [ ] **Verify Integrity:** Run `python3 tools/verify_system_v40.3.py` to confirm system health.
- [ ] **Self-Correction:** Run `python3 gap_analysis_check.py` to ensure no files are missing.

## Phase 3: Anti-Hallucination & Security (The "Shield")
- [ ] **Active Memory:** Run `python3 tools/verify_context.py --target README.md` to prove tool functionality.
- [ ] **Antigravity Check:** Run `python3 tools/antigravity.py` to verify emergency protocols are inactive (Standard Mode).
- [ ] **Security Scan:** Run `python3 tools/security_scan.py` to check for pre-existing vulnerabilities.

## Phase 4: Project Structure (The "Map")
- [ ] **Create Folders:** Ensure the following exist (handled by setup script):
    - [ ] `roles/ml/`
    - [ ] `rules/ml/`
    - [ ] `workflows/ml/`
    - [ ] `memory-bank/`
    - [ ] `errors/`
- [ ] **Initialize Memory Bank:** Create `activeContext.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`.

## Phase 5: First Commit (The "Start")
- [ ] **Generate Plan:** Create `PLAN.md` using `speckit analyze`.
- [ ] **Commit:** Push initial structure to GitHub with message "feat: Initialize project with Global System Ultimate v26.0.0".

---
**Signed:** The Global Professional Engineer
**Date:** 2026-02-15
