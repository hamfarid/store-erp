# ✅ Testing Rules (Global System Ultimate)

**Status:** MANDATORY
**Enforcement:** Automated by `tools/speckit.py verify`

## Mindset
**You are skeptical. Question everything. Break everything.**

## Core Principles
- **Test First:** Write tests before code (TDD) whenever possible.
- **Automate:** Use `tools/speckit.py verify` to run all checks.
- **Zero Tolerance:** No commit passes if tests fail.

## Test Types & Tools
1.  **Unit Tests:** `pytest` / `jest` (Fast, isolated).
2.  **Integration Tests:** `pytest` (Component interaction).
3.  **E2E Tests:** `playwright` (User flows).
4.  **Security Tests:** `tools/preflight_check.py` (Secrets, TODOs).
5.  **Static Analysis:** `tools/augment.py` (Code quality).

## Test Coverage
- Aim for **80%+ coverage**.
- **Critical Paths:** 100% coverage required.
- **Error Handling:** Must be tested explicitly.

## The Verification Protocol
Before any commit, you MUST run:
```bash
python3 tools/speckit.py verify
```
This runs Sentinel, Augment, and your test suite in sequence.

## Remember
**Untested code is broken code. Unverified code is rejected code.**
