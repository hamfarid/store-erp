# Deployment Instructions (v26.0.2 Diamond 32)

> **Purpose**: Standard Operating Procedure (SOP) for deploying the Global System v26 Diamond 32 framework.
> **Version**: v26.0.2 (Diamond 32)
> **Last Updated**: Feb 16, 2026

## 1. Pre-Deployment Checklist (The "Pre-Flight")

Before initiating any deployment, the **Governance Agent** must verify the following:

1.  **Version Consistency**:
    *   `VERSION` file matches `AGENTS.md` and `BOOTSTRAP.md`.
    *   All `rules/` and `roles/` files are present and accessible.
2.  **Clean State**:
    *   No `node_modules` or `__pycache__` in the source directory.
    *   No duplicate files (run `tools/deduplicate.py` if needed).
3.  **Security Scan**:
    *   Run `gitleaks detect` to ensure no secrets are committed.
    *   Run `semgrep scan` to check for critical vulnerabilities.
4.  **Test Pass**:
    *   All unit tests pass (`pytest tests/unit`).
    *   Critical integration tests pass (`pytest tests/integration`).

## 2. Deployment Steps (The "Launch Sequence")

### Step 1: Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-org/global-system-ultimate.git
cd global-system-ultimate

# Run the bootstrap script
./bootstrap.sh
```

### Step 2: Dependency Installation
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (if applicable)
npm install
```

### Step 3: Configuration
1.  Copy `.env.example` to `.env`.
2.  Fill in the required API keys and configuration values.
3.  **WARNING**: Do not commit the `.env` file!

### Step 4: Database Migration
```bash
# Run migrations
alembic upgrade head
```

### Step 5: Service Start
```bash
# Start the main application
python main.py
```

## 3. Post-Deployment Verification (The "Orbit Check")

After deployment, the **QA Engineer Agent** must verify:

1.  **Health Check**: Access `/health` endpoint to ensure the service is running.
2.  **Log Monitoring**: Check logs for any startup errors or warnings.
3.  **Smoke Test**: Run a basic end-to-end flow to verify core functionality.

## 4. Rollback Procedure (The "Abort Mission")

If any critical error occurs during or immediately after deployment:

1.  **Stop the Service**: `kill $(pgrep -f main.py)`
2.  **Revert Code**: `git revert HEAD`
3.  **Restore Database**: Restore from the latest backup if migrations were run.
4.  **Notify Team**: Alert the **Planner Agent** and **Security Agent** immediately.

## 5. Maintenance & Updates

*   **Regular Updates**: Run `git pull` and `pip install -r requirements.txt` weekly.
*   **Security Patches**: Apply security patches within 24 hours of release.
*   **Audit**: The **Governance Agent** runs a full audit monthly.
