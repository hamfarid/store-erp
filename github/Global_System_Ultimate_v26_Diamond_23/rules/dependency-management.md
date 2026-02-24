 (v15.9.8)

**SEVERITY: HIGH**
**ENFORCEMENT: AUTOMATIC (Renovate & Sentinel)**
**FRAMEWORK: 2026 AI Coding Agent Governance (Area 2)**
**VERSION:** Global System Ultimate v15.9.8 (See VERSION file)

## 1. PACKAGE MANAGERS (The 2026 Standard)
To ensure speed, consistency, and security, the following package managers are MANDATORY:

### 🐍 Python: `uv` (v0.10.2+)
*   **Why:** 10-100x faster than pip, unified toolchain (pip, pip-tools, virtualenv).
*   **Command:** `uv pip install -r requirements.txt` or `uv sync`
*   **Lockfile:** Always commit `uv.lock` or `requirements.lock`.
*   **Constraint:** Do NOT use `pip` directly unless `uv` is unavailable.

### 🟢 Node.js: `pnpm` (v10.x+)
*   **Why:** Efficient disk usage (content-addressable store), strict dependency resolution.
*   **Command:** `pnpm install`
*   **Lockfile:** Always commit `pnpm-lock.yaml`.
*   **Constraint:** Do NOT use `npm` or `yarn`.

## 2. SECURITY SCANNING (Layered Defense)
The 2026 framework mandates a layered approach to supply chain security:

### 🛡️ Behavioral Analysis: `Socket.dev`
*   **Purpose:** Detect malicious packages through static analysis of behavior (install scripts, network requests, obfuscated code).
*   **Why:** CVE databases are reactive; behavioral analysis is proactive.
*   **Action:** Block packages with suspicious install scripts.

### 🔍 Vulnerability Scanning: `Trivy` (v0.68.2+)
*   **Purpose:** Scan container images, filesystems, repositories, SBOMs, secrets, and licenses.
*   **Why:** Single tool for all artifacts.
*   **Action:** Block deployment if HIGH or CRITICAL vulnerabilities are found.

### 🐍 Python-Specific: `pip-audit` (v2.10.0+)
*   **Purpose:** Python-specific scanning using the official Python Packaging Advisory Database.
*   **Feature:** Auto-fix capability for vulnerable dependencies.

### 📊 Aggregation: `DefectDojo`
*   **Purpose:** Aggregate findings from all scanners to reduce alert noise by 90% through deduplication.

## 3. GITHUB ACTIONS SECURITY
*   **Rule:** All GitHub Actions MUST be pinned by **SHA (Digest)**, not tag.
*   **Why:** Tags (e.g., `v2`) are mutable and can be hijacked (e.g., March 2025 tj-actions attack).
*   **Example:**
    *   ❌ `uses: actions/checkout@v3`
    *   ✅ `uses: actions/checkout@f43a0e5ff2bd294095638e18286ca9a3d1956744 # v3.6.0`

## 4. CONTAINER IMAGES
*   **Rule:** All base images in Dockerfiles MUST be pinned by **Digest (SHA256)**.
*   **Why:** Ensures reproducibility and prevents supply chain attacks via tag mutability.
*   **Example:**
    *   ❌ `FROM python:3.11-slim`
    *   ✅ `FROM python:3.11-slim@sha256:a1b2c3...`

## 5. AUTOMATED UPDATES (Renovate)
*   **Configuration:** Managed via `.github/renovate.json`.
*   **Schedule:** Weekly updates (Monday 5am UTC).
*   **Strategy:**
    *   **Patch/Minor:** Auto-merge if tests pass.
    *   **Major:** Requires manual approval.
    *   **Security:** Immediate PR for vulnerabilities.

## 6. BREAKING CHANGES (Codemods)
*   **Strategy:** Use AST-based code transformations for major upgrades.
*   **Tools:**
    *   **jscodeshift:** For JavaScript/TypeScript migrations.
    *   **OpenRewrite:** For Java/JVM migrations.
    *   **Patchwork:** AI-assisted vulnerability fixes and dependency upgrades (Semgrep + LLM).

---
*Signed,*
*The Global Professional Engineer (Global System Ultimate v15.9.8)*
