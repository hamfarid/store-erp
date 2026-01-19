# PROMPT 78: CI/CD & AUTOMATION (v27.0)

## 1. The "Security First" Pipeline
**Rule:** Security checks must run BEFORE build and test steps.
*   **Step 1: Secret Scan:** `trufflehog` or `gitleaks` to find committed secrets.
*   **Step 2: Dependency Audit:** `npm audit` or `pip-audit` to find vulnerable packages.
*   **Step 3: SAST:** `SonarQube` or `CodeQL` to find code vulnerabilities.
*   **Step 4: Build & Test:** Only if steps 1-3 pass.

## 2. GitHub Actions Automation
**Rule:** You must generate `.github/workflows` for every project.
*   **`ci.yml`:** Runs on every PR. Includes Lint, Test, Build, and Security Scan.
*   **`cd.yml`:** Runs on push to `main`. Deploys to Vercel/Supabase/Docker.
*   **`nightly.yml`:** Runs E2E tests (Playwright) every night.

## 3. The "Auto-Fix" Protocol
**Rule:** If a lint or format job fails, the CI should try to fix it automatically.
*   *Action:* Add a step to run `npm run format` or `black .` and commit changes back to the PR.

## 4. "Push on Green"
**Rule:** If all tests pass on `main`, deploy automatically to Staging.
*   *Requirement:* High test coverage (>80%) is mandatory for this rule.

## 5. Infrastructure as Code (IaC)
**Rule:** All infrastructure changes (Supabase, Vercel) must be defined in code (Terraform or Pulumi) and applied via CI/CD.
