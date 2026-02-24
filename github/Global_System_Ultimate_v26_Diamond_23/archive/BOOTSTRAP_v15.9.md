 (v15.9.8)

**SYSTEM STATUS: LEVEL 15.9.8 INTELLIGENCE ACTIVE**
**MODE: AUTONOMOUS SWARM INTELLIGENCE**
**DATE: 2026-02-15**
**FRAMEWORK: 2026 AI Coding Agent Governance (Areas 1-7)**

## 1. 🏁 QUICK START (The "Zero-to-Hero" Protocol)

### Step 1: Install Package Managers (The Foundation)
We use `uv` for Python (100x faster than pip) and `pnpm` for Node.js (disk-efficient).

```bash
# Install uv (Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install pnpm (Node.js)
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

### Step 2: Clone & Setup (The Structure)
```bash
# Clone the repository (if not already done)
git clone <your-repo-url> .

# Install dependencies (Python)
uv sync --frozen

# Install dependencies (Node.js)
pnpm install --frozen-lockfile
```

### Step 3: Verify Environment (The Check)
Run the preflight check to ensure all systems are go.
```bash
python3 global_system/scripts/preflight_check.py
```

## 2. 📜 CORE DOCUMENTS (MANDATORY READING)

Before writing a single line of code, you MUST read and internalize:

1.  **`prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT_v15.9.8.md`**: The Constitution. Your operating system.
2.  **`AGENTS.md`**: The Single Source of Truth for platform configuration.
3.  **`knowledge/core/project_lifecycle.md`**: The Roadmap. How we build things.
4.  **`knowledge/protocols/future_proof_architecture.md`**: The Blueprint. How we design things.
5.  **`VERSION`**: The Single Source of Truth for the system version.

## 3. 🛠️ OPERATIONAL WORKFLOW (The Swarm Loop)

For every task, follow this loop:

1.  **ANALYZE:** `python3 global_system/tools/speckit.py analyze`
2.  **PLAN:** Create a detailed `PLAN.md`.
3.  **IMPLEMENT:** Write code & tests (EDD).
4.  **VERIFY:** `python3 global_system/tools/speckit.py verify`
5.  **AUDIT:** `python3 global_system/tools/sentinel.py`

## 4. 🛡️ SECURITY & COMPLIANCE

*   **Secrets:** NEVER commit `.env` files. Use `gitleaks` to check.
*   **Updates:** Use `renovate` for dependency updates.
*   **Scanning:** Use `trivy` for container/IaC scanning.

---
*Signed,*
*The Global Professional Engineer (Global System Ultimate v15.9.8)*
