 V. Natural-Language Control Layer (Runtime Commands)
	•	PARAMS: repo_root, min_coverage_pct, build_minutes, test_minutes, p95_ms, brand_palette_source_url, search_web_allowed, language_default, rtl_support_required, multi_tenancy, enable_pwa, enable_rag, ci_provider, infra_as_code, package_manager.
	•	MODES: e.g. “Mode: Security Auditor”, “Mode: Code Surgeon”, “Mode: RAG Auditor”, “Mode: UI Designer”, “Mode: API Governor”, “Mode: DBA”, “Mode: Perf Engineer” (to switch specialized focus).
	•	SCOPE: e.g. “Scope: FE only”, “Scope: BE only”, “Scope: DB only”, “Scope: all”; Profile: e.g. “SaaS”, “API-only”, “Monolith”, “Mobile”, “Microservices” (to set context).
	•	ADD-ONS (toggle features): A=Perf budgets, B=Observability, C=Load, D/X=SBOM/Supply chain, E=Assets, F=Zero-downtime, G=Feature flags,
H/AC=Accessibility/RTL, I=Resilience, J=Privacy, K=Security headers, L=CDN/Edge, M=DX/Monorepo, N=Strict types/mutation,
O=RAG quality, P=Branding/Motion, Q=Multi-tenancy, R=Backups/DR, S=Secrets/KMS, T=IaC/GitOps, U=API governance,
V=DDD/Modular, W=Compliance, Y=FinOps, Z=PWA, AA=Data quality, AB=Test data, AD=Docs-as-code, AE=Visual QA,
AF=PR guardrails, AG=SIEM, AH=SSO/SCIM, AI=Multi-layer caching.
	•	EXECUTION Commands: e.g. “Run OPERATIONAL_FRAMEWORK now and return OUTPUT_PROTOCOL.” or “Proceed with Passes 0→9 …” to trigger full analysis; these run the multi-phase process above.
	•	SAFETY Commands: e.g. “Redact secrets”, “Clear memory for this thread” to handle sensitive data.
	•	OUTPUT FORM Toggles: e.g. “Strict OUTPUT_PROTOCOL” to enforce full format, or “Only ” or “Short ” for specific output sections.

VI. Domain Rails (Always-On)
	•	API Governance: Refresh API contracts; provide typed FE client; add input validators; run drift tests; use a standardized error envelope (e.g. {code, message, details?, traceId}).
	•	RAG Middleware: Define input schema; add prompt-injection guards; allowlisted knowledge sources; implement cache keys & TTL; optional result re-ranker; evaluate retrieval quality (Precision@k, MRR, nDCG); enforce CI checks on these.
	•	UI/Brand & Visual Design: Derive design tokens from Gaara/MagSeeds brand; ensure UI is attractive, interactive, responsive; use tokens for all colors; meet WCAG AA contrast; support light/dark mode and RTL; include a Command Palette; add micro-interactions and robust empty/loading/error states.
	•	Page Protection & Route Obfuscation: Enforce server-side auth; use a strict Content-Security-Policy with nonces; secure cookies (HttpOnly, Secure); JWT rotation; CORS domain allowlist; CSRF tokens; rate limiting; scan uploads; add SSRF defenses; prevent user enumeration (generic 404 on unknown resources); use hashed/obfuscated route identifiers (HMAC-signed, short TTL); use content-hashed build chunk names.
	•	Database (DB): Use idempotent migrations for schema changes; enforce constraints (FKs, unique, check) and add indexes; wrap critical operations in transactions; include database seed data for defaults; use an expand→backfill→switch→contract approach for migrations to avoid downtime.
	•	De-Duplication: Detect duplicate code by semantics (AST/tokens); merge duplicates into a single canonical implementation; move deprecated copies to /unneeded/<original>.removed.<ext> with pointers and commit IDs for reference.
	•	CI Gates: Ensure CI pipelines run build, lint, tests, type-checks; include security scans (dependency audit, secret scanning, CodeQL/Semgrep static analysis); verify security headers and CSP in responses; run Lighthouse for contrast and performance; generate SBOM and enforce performance budgets.

VII. Naming, Standards & Style Guardrails
	•	Version Control & Commits: Use Conventional Commits and descriptive branch name prefixes.
	•	File Headers: Every source file must start with a header comment line: FILE: <repo-path> | PURPOSE: … | OWNER: … | RELATED: … | LAST-AUDITED: <date> (enforced in CI).
	•	Logging: Use structured logging format {traceId, userId?, tenantId?, route, action, severity, timed_ms, outcome}; do not expose stack traces to clients.
	•	Accessibility: Ensure full keyboard navigation and visible focus indicators, ARIA attributes where needed; maintain WCAG AA contrast levels.

VIII. Acknowledgment
	•	On first app message after loading these guidelines, output: “Guidelines: LOADED v2.3 — GLOBAL policy active.”

IX. Expanded Search & Web Research (Global Mandate)
	•	Workspace Search: Perform deep searches through the project (regex, AST, symbol analysis, call graphs) to find references, dynamic imports, dead code, etc.
	•	External Research: If search_web_allowed is true, consult official documentation, academic papers, government and international datasets, market/financial reports, and library benchmarks as needed. Record all such external references in /docs/References.md for transparency.

X. Standard Artifacts (“Project Memory”) (Mandatory)
	•	Documentation to Maintain: Create and keep updated the following files to serve as the project memory (append-only where noted):
	•	/docs/Inventory.md, /docs/TechStack.md
	•	/docs/Routes_FE.md, /docs/Routes_BE.md, /docs/Pages_Coverage.md
	•	/docs/API_Contracts.md (and the API spec such as /contracts/openapi.yaml or GraphQL schema files)
	•	/docs/DB_Schema.md (include an ER diagram), /docs/Permissions_Model.md
	•	/docs/Duplicates_And_Drift.md, /docs/Missing_Libraries.md
	•	/docs/Env.md (with env var definitions & a validator), /docs/Security.md, /docs/Threat_Model.md (use OWASP/STRIDE methodology)
	•	/docs/Error_Catalog.md, /docs/Runbook.md
	•	/docs/Remediation_Plan.md, /docs/Status_Report.md
	•	/docs/DONT_DO_THIS_AGAIN.md (post-mortem lessons not to repeat)
	•	/docs/Symbol_Index.md, /docs/Imports_Map.md
	•	/docs/UI_Design_System.md, /docs/Brand_Palette.json, /docs/CSP.md, /docs/Route_Obfuscation.md, /docs/Search.md
	•	/docs/Resilience.md
	•	Shared Types Package: maintain common type definitions in /packages/shared-types/ (and ensure it’s kept up-to-date).

XI. RBAC Permission Model (All Modules)
	•	Roles & Permissions: Define clear permission types (e.g. ADMIN, MODIFY for create/update/delete, READ for full details, VIEW_LIGHT for non-sensitive view, APPROVE for workflow approvals). Document a role-permission matrix in /docs/Permissions_Model.md and cover it with tests.
	•	Enforcement: Use a centralized authorization check (by permission or policy) in backend, and implement frontend route/UI guards based on roles. Ensure sensitive actions require proper permission. Keep the /docs/Permissions_Model.md matrix updated with any changes.

XII. Module Analysis & Merge Protocol (Legacy vs New)
	•	Analyze all existing modules (both legacy and new) thoroughly: compare the intended design/purpose versus actual implementation and behavior (don’t rely just on names or folder structure).
	•	Before creating any new module, search the codebase to avoid duplicating functionality. Update /docs/Inventory.md with a full folder structure/tree of the project.
	•	Refactoring Process: Begin refactoring with modules that have the fewest dependencies (to minimize impact). If modules are provided as archives, inspect and unpack them to integrate their code properly.
	•	After restructuring or refactoring modules, perform a Legacy Parity Check and document it in /docs/Legacy_Parity_Checklist.md to ensure feature parity with the old system.
	•	Re-audit any modules that were previously out-of-scope or deferred to confirm nothing is missing post-merge.

XIII. Documentation & Reference Files (Append-Only)
	•	The following reference files should be treated as append-only logs (never edit or remove old entries). Always include the standard file header line in each:
	•	/function_reference.md
	•	/docs/DONT_DO_THIS_AGAIN.md
	•	/docs/TODO.md
	•	/docs/To_ReActived_again.md (note: likely meant for items to reactivate later)
	•	/docs/fix_this_error.md
	•	/docs/REMOVED_VARIABLES.md

XIV. Python Tooling & Style (If Applicable)
	•	After completing module development or updates, run pipreqs to update Python dependencies.
	•	Enforce Python style: use autopep8 to format code and run flake8 for linting, both locally and as part of CI.

XV. Frontend Branding: Colors & Fonts (Gaara & MagSeeds)
	•	Establish design tokens (colors, typography) derived from official Gaara Group and MAGseeds brand guidelines (for both English and Arabic if applicable). Use these in the frontend theme (e.g. /ui/theme/tokens.json) and document in /docs/Brand_Palette.json.
	•	All colors used should be by token name (no hard-coded hex values) and meet WCAG AA contrast standards. Use official brand fonts and ensure they are loaded/available for both languages as needed.

XVI. Post-Deploy GUI Settings (Manual Vars to Screens)
	•	After deployment, any configuration or variables that were manually set (especially those affecting behavior or preferences) should be exposed in the application via administrative GUI settings screens. This ensures non-developers can adjust settings without code changes. Apply this to all modules as applicable.

XVII. Validation & Data Integrity
	•	Implement strict validation on both frontend and backend for all create/update/delete operations to ensure data consistency. Prevent any operations that could lead to database corruption or invalid state. (For example, enforce field formats, required fields, and business rules on both sides.)

XVIII. Duplication & Task Verification
	•	When addressing a task or bug, first search the codebase to ensure a similar fix or implementation doesn’t already exist (avoid duplicating logic that could be reused).
	•	Break down overly large code blocks or functions into smaller, manageable pieces to improve readability and maintainability.
	•	Standardize constants and configuration values (define them in one place and reuse) to avoid divergence or mismatches across the codebase.

XIX. Strategic Goal: Surpass Odoo within Two Years (Top-5 ERP)
	•	Keep a living roadmap in /docs/Gaara_vs_Odoo_Roadmap.md outlining how to progress to be among the top 5 ERP systems within two years. Include quarterly key performance indicators (KPIs) and milestones to track progress against Odoo and other competitors.

XX. Continuous Online Data Refresh & Connectivity
	•	For features relying on live or periodically updated data, ensure the system maintains reliable internet connectivity and schedule automatic refreshes. Update any machine learning models or data assets periodically to keep them current. Document data provenance and update schedules in /docs/References.md or related documentation.

XXI. Backup & Artifact Policy (Clean, Secret-Free)
	•	Backup Triggers: Automatically trigger a backup after completing any module or resolving any 3 TODO items.
	•	Backup Contents: Exclude sensitive or irrelevant files (.env, virtual environments, node_modules, caches, build outputs). Include all documentation (.txt/.md files in repository), source code, scripts, and configuration files (ensuring no secrets are included). The backup should be timestamped and stored securely.

XXII. Dependency Policy (Latest Stable Required)
	•	Keep all dependencies up-to-date with the latest stable releases (after testing for compatibility). Plan and execute migrations to newer versions proactively, documenting changes in the release notes or PR descriptions. Ensure CI tests pass with the updated dependencies before merging.

XXIII. Search API Design (REST)
	•	Design a robust search endpoint (e.g. GET /search) that accepts query parameters like q (query string), limit, offset, and possibly filters. The endpoint should return results in a structured format (JSON or XML) with proper pagination metadata. Enforce authentication and authorization as appropriate, apply rate limiting to prevent abuse, and implement graceful error handling (following the unified error format). Document the search API in the OpenAPI spec. Implement indexing and caching for frequent queries to improve performance.

XXIV. MLOps Lifecycle (Continual Learning)
	•	Establish a machine learning operations pipeline if ML features are present: ensure data quality and proper preprocessing; choose and fine-tune appropriate models; rigorously evaluate model performance; set up model serving and monitoring in production; plan for periodic retraining or fine-tuning as new data arrives. Version both models and datasets (e.g. using Git LFS or an artifact registry) to track changes over time and allow rollbacks if necessary.

XXV. Online Research Mandate (Wide Sources)
	•	Encourage the use of a wide variety of reputable information sources when researching solutions: academic papers, government and international datasets, industry and financial reports, comparative benchmarks, etc. This breadth ensures well-informed decisions. All external sources consulted should be recorded in /docs/References.md for transparency and future reference.

XXVI. Repository Privacy Defaults
	•	Treat all code repositories as private by default. Do not expose source code publicly unless explicitly decided and vetted. Apply strict access controls to repository contents, especially if they contain proprietary or sensitive information.

XXVII. Class & Type Canonical Registry (Mandatory)
	•	Maintain a central registry of all core classes and types in /docs/Class_Registry.md (append-only). Developers must consult this registry before introducing or modifying any model classes or domain types.
	•	For each entry, record details: CanonicalName, Location (file/module), DomainContext, Purpose, Fields, Relations, Invariants, Visibility, Lifecycle, DTO/API mappings, Frontend mapping, Database mapping, Tests, Aliases, and any Migration Notes.
	•	There should be exactly one canonical definition per domain concept. If duplicates exist, they must be merged. The CI pipeline should enforce that any PR adding or changing a core class/type includes an update to the Class_Registry (or it fails build unless an override is documented).

XXVIII. Login-Fix Blitz — Policy & Tests (P1)
	•	Secure Cookies: Set session cookies with Secure, HttpOnly, and appropriate SameSite attributes.
	•	Token Lifetimes & Rotation: Limit access token lifetime to ~15 minutes and refresh token to ~7 days. Implement token rotation on each use and revoke tokens immediately on logout.
	•	Password Storage: Use strong password hashing (Argon2id or scrypt) for storing credentials.
	•	CSRF Protection: Implement CSRF tokens for any state-changing HTTP requests (especially for forms and login/logout actions).
	•	Brute-force Mitigation: Lock out or rate-limit login after a certain number of failed attempts (e.g., 5 attempts within 15 minutes triggers a temporary lock or challenge) to prevent brute force attacks.
	•	MFA: Provide an option for multi-factor authentication (e.g., TOTP or WebAuthn) for user login for added security.
	•	Testing: Write negative test cases (wrong password, etc.) to ensure the system handles them safely, and include end-to-end tests for the entire login and password reset flows. Ensure all new login security features are covered by automated tests.

XXIX. API & RAG Alignment — Specifics
	•	API Contract Refresh: Update and maintain the OpenAPI (or GraphQL) specification to reflect the actual API. Generate a typed client for the frontend (e.g., TypeScript interfaces or client code) from this spec to ensure consistency.
	•	Validation: Implement strict input validation and response schema validation on the backend to ensure adherence to the API contract. Add tests to detect any drift between the docs and implementation.
	•	Error Handling: Standardize error responses using a unified envelope (e.g., JSON containing code, message, optional details and traceId). Update all endpoints to follow this format.
	•	RAG (Retrieval-Augmented Generation) Middleware: Define a clear schema for any prompts or queries sent to language models. Enforce allowlists of data sources to prevent unauthorized data access. Implement guardrails against prompt injection attacks. Utilize caching for repeated queries (with defined keys and TTLs) to improve performance. Optionally, use a reranker to sort retrieved documents by relevance before feeding to the model.
	•	Evaluation: Set up evaluation metrics for the RAG system (e.g., Precision@k, MRR, nDCG for retrieval relevance) and include these in CI to monitor quality regressions. Ensure the entire pipeline is covered by tests and documented in the references.

XXX. File Header Policy (Mandatory)
	•	Every source file must begin with a single-line comment header in the exact format: FILE: <repo-path> | PURPOSE: ... | OWNER: ... | RELATED: ... | LAST-AUDITED: <YYYY-MM-DD>. This is strictly enforced by CI. Do not remove or change this format; update the date when auditing or modifying the file.

XXXI. Device Identity (SUDI) — Frontend & Backend (Mandatory)
	•	Implement Secure Unique Device Identity (SUDI) using hardware-anchored certificates (X.509). Require mutual TLS for device communication, verifying the certificate chain, Extended Key Usage fields, expiration, and revocation status.
	•	Integrate device identity into authorization logic (e.g., certain actions require a known device certificate) and generate audit logs for device-related events. Set up alerts for certificate rotations or unexpected device identity changes. Document the SUDI design and usage in /docs/SUDI.md.

XXXII. Server-Driven UI (SDUI) — Frontend & Backend (Mandatory)
	•	Define a schema for server-driven UI in /contracts/sdui.schema.json (versioned with semantic versioning, append-only extensions). The backend should produce UI configurations according to this schema, and the frontend should validate and render them dynamically.
	•	Secure the SDUI pipeline: sign the UI payloads (JSON Web Signature) and use ETags for caching. Implement node-level RBAC in the UI schema so that sensitive UI components are only rendered if the user has permission.
	•	The frontend renderer must allow only known, safe UI elements as defined in the schema (prevent execution of arbitrary code). Include telemetry events for UI rendering and interactions for monitoring.
	•	Add CI checks to ensure that any changes to UI schema or templates do not break compatibility and adhere to the defined schema contracts.

XXXIII. Optimal & Safe over Easy/Fast (OSF) — Global Mandate
	•	Always favor solutions that maximize security, correctness, and maintainability, even if they are not the fastest or simplest initially. In other words, prioritize Optimal & Safe over Easy & Fast.
	•	Use the OSF scoring system to evaluate options (approximate weighting: 40% Security, 25% Correctness, 15% Reliability, 10% Maintainability, 5% Performance, 5% Speed of implementation).
	•	For any significant decision, outline at least three alternative solutions and assess them with an OSF trade-off analysis table. Record this in /docs/Solution_Tradeoff_Log.md (including any temporary risk acceptances, which should automatically expire in 30 days unless renewed with justification).

XXXIV. Environment URL Scheme & Transport Security (Mandatory)
	•	Production Environments: Use HTTPS for all endpoints. Automatically redirect any HTTP requests to HTTPS. Enable strict transport security (HSTS) and support TLS 1.3 (with TLS 1.2 as a minimum). Mark cookies as Secure; use CSP with nonces; and set safe referrer, frame, and permissions policies to harden the app.
	•	Non-Production (Dev/Staging): HTTP may be allowed only for local or VPN-access scenarios if absolutely necessary, but HTTPS is preferred here as well. Do not use real sensitive data in non-prod environments and restrict access to them.
	•	Config Enforcement: Use environment configurations like APP_ENV to toggle security settings. Ensure BASE_URL, API_BASE_URL, SDUI_BASE_URL use https:// in production, and set a flag like FORCE_HTTPS=true in production configs. Implement a CI transport-guard to catch misconfigurations related to transport security.

XXXV. Repository Bootstrap Baseline (Must Exist)
	•	Ensure the repository contains standard baseline files (which can be copied from a global template if needed):
	•	Issue templates: .github/ISSUE_TEMPLATE/bug_report.md and feature_request.md
	•	Repository configs: .gitignore, .markdownlint.json
	•	Documentation: CHANGELOG.md, CONTRIBUTING.md, GLOBAL_GUIDELINES.txt, LICENSE, README.md, Solution_Tradeoff_Log.md
	•	Setup scripts: download_and_setup.sh, setup_project_structure.sh, validate_project.sh
	•	Examples: examples/simple-api/README.md
	•	CI/CD templates: templates/.env.example, templates/Dockerfile, templates/ci.yml, templates/docker-compose.yml
	•	Backup scripts: scripts/backup.sh
	•	The CI should prevent removal of any of these baseline files unless a valid rationale is provided (documented in CHANGELOG.md and /docs/Runbook.md).

XXXVI. Supply Chain & SBOM (Mandatory)
	•	On every pull request and on each main branch update, automatically generate a Software Bill of Materials (SBOM) (e.g., using CycloneDX or Syft). Save the SBOM as a pipeline artifact and compare it to the previous version to detect any unexpected changes in dependencies.
	•	Scan the SBOM with vulnerability scanners like Grype or Trivy; fail the build if new critical vulnerabilities are found (unless they are explicitly allowlisted by policy).
	•	Pin all dependencies to known-good versions. Where possible, verify packages via signatures or checksum to prevent tampering. Document the source and version of each critical dependency in /docs/References.md for traceability.

XXXVII. Secret Scanning & Secrets Management (Mandatory)
	•	Use Managed Secrets: All production credentials, API keys, and encryption keys must be stored in a secure secrets management system (e.g., cloud KMS or HashiCorp Vault). They should never be committed to the repository or stored in plain text in config files.
	•	No Secrets in Code or Images: Do not keep real production secrets in .env files, Docker images, or CI logs. For development, use example env files and secure CI variables.
	•	Key Lifecycle: Create secrets with least privilege and plan for rotation at least every 90 days. Revoke and replace any secret on suspicion of compromise. Document the key IDs or Vault paths (but not the secret values) in /docs/Env.md and update /docs/Security.md with secret management practices.
	•	Runtime Injection: Configure the application to fetch secrets at runtime (for example, via an OIDC token to Vault, Vault Agent sidecar, or cloud secrets API) rather than hardcoding them. The application config should reference secret paths, not literal secrets.
	•	CI Enforcement: Run secret scanners (like Gitleaks or TruffleHog) in CI to prevent committing secrets. If a legitimate test key must be in the repo, it must have an approved risk acceptance in documentation (expiring within 30 days).
	•	Data Protection: Use envelope encryption for sensitive data (like PII or backup files) with master keys from the KMS/Vault. Make sure logs never print sensitive data or secrets. Audit all access to secrets and set up alerts for anomalous access patterns. Exclude secrets and private keys from backups entirely (or store them encrypted outside of code backups).

XXXVIII. DAST & Frontend Quality Budgets (Mandatory)
	•	Automate dynamic security testing: run an OWASP ZAP baseline scan (or equivalent) against a test deployment for each PR. Treat any high-severity findings as failing issues that must be resolved before merge.
	•	Integrate frontend quality gates: run Lighthouse CI (or similar) on key user flows/pages to enforce performance, accessibility, SEO, and PWA score budgets. If any metric regresses beyond the allowed budget, the CI should fail, prompting a fix or explicit approval of the deviation.

XXXIX. Infrastructure as Code & Cluster Security (If Applicable)
	•	Apply static analysis to any infrastructure-as-code definitions (e.g., Terraform, Kubernetes manifests, Helm charts) using tools like tfsec, checkov, or kube-linter. Address any security warnings, such as overly permissive configurations.
	•	Ensure no containers run with unnecessary privileges (avoid running as root when not needed, drop capabilities, etc.). Require NetworkPolicies in Kubernetes to restrict cross-service traffic where appropriate. Limit exposure by only allowing public ingress to intended services.
	•	Manage infrastructure secrets (API keys, credentials) via KMS or Vault integrations within IaC (do not hardcode secrets in terraform files or helm values). Implement drift detection to flag if deployed resources diverge from IaC definitions.

XL. SLOs & Error Budgets (Observability)
	•	Define Service Level Objectives (SLOs) for critical metrics like availability (uptime) and latency. Monitor these and set up alerts when thresholds are breached.
	•	Track error budgets (the allowable downtime or error rate within a period). If the error budget is exhausted (meaning reliability has dipped below targets), halt high-risk changes until stability is restored or an explicit risk acceptance is signed off. Document any such exceptions and ensure rapid mitigation to get back within budget.

XLI. GitHub Actions — Auto Deployment (Mandatory)
	•	Implement an automated deployment workflow (e.g., .github/workflows/deploy.yml) that promotes builds through environments (dev → staging → prod). Require code review approvals and use protected branches for releases.
	•	Use secure storage for environment secrets (fetch from KMS/Vault in the workflow) rather than storing them in the repo or plaintext in the CI config.
	•	Build the application artifacts once (in CI) and reuse the same build for each environment promotion to ensure consistency and traceability (record checksums or provenance info).
	•	Optionally, incorporate deployment strategies like canary releases or blue-green deployments for zero downtime (especially if Add-On F is enabled).
	•	Ensure that all continuous integration gates (tests, linting, type checks, security scans, SBOM generation, DAST, Lighthouse audits) pass successfully before any deployment job is allowed to run.

XLII. Issues, Wiki, GitHub Pages (Mandatory)
	•	Issues: Convert the finalized task list into GitHub Issues automatically. Each issue should be labeled with its priority (P0–P3) and relevant areas (e.g., FE, BE, DB, Security, UI, RAG, Docs). Integrate these with a GitHub Project board for tracking.
	•	Wiki: Use the repository wiki for long-form documentation and guides. Mirror important /docs content in the wiki (excluding any sensitive information) so it’s easily accessible. Keep these pages updated and append new information rather than altering historical records.
	•	Documentation Site: Publish the documentation (from the /docs directory) via GitHub Pages or a documentation generator (like MkDocs or Docusaurus) to provide a user-friendly handbook. Ensure the published site is served over HTTPS and kept in sync with the latest repository docs.

XLIII. Full-System Audit & Report (Mandatory)
	•	Set up an automated audit workflow (e.g., audit.yml) that thoroughly inspects the front-end, back-end, database, API, and security configurations:
	•	Verify that each front-end page and button is properly wired to back-end routes/actions and that there are no orphan routes or UI elements.
	•	Check that all API endpoints adhere to the documented contracts and have proper authorization checks. Ensure database relationships, indexes, and constraints are correctly implemented and that environment config variables conform to a schema (if one exists).
	•	Confirm security measures: e.g., Content-Security-Policy headers are sent, SSO (if applicable) is configured, CSRF tokens are required, rate limiting is active on sensitive endpoints, file uploads are virus-scanned, SSRF protections are in place for any external URL usage.
	•	Have the audit workflow output a detailed report (in JSON and Markdown) saved to /docs/Status_Report.md and as a CI artifact. This report should include coverage metrics (e.g., which UI components and API endpoints were exercised) and highlight any gaps or issues discovered.
	•	As part of the audit, leverage the AI-assisted analysis (security, engineering, etc.) and even compare the system against similar projects. Document external insights or benchmarks in /docs/References.md and compile recommended fixes or improvements in /docs/Remediation_Plan.md.

XLIV. Multi-Expert Advisory Council (Mandatory)
	•	Establish an AI-driven advisory council with multiple perspectives for critical changes. For example:
	•	Security Consultant AI: Provides insight on threat modeling, vulnerabilities, security headers (CSP, etc.), authorization and data protection.
	•	Software Engineering Consultant AI: Advises on architecture, modular design, testing strategy, performance optimizations, and developer experience.
	•	Political Analyst AI: Evaluates any policy, regulatory, or geopolitical risks that might affect deployment and operations.
	•	Economic Analyst AI: Assesses cost implications (FinOps), ROI, pricing or licensing strategies.
	•	For each pull request that affects core systems or policies, gather a short “scorecard” review from each of these roles, with a score (0.0–1.0) and brief notes. Append these reviews to /docs/Advisory_Reviews.md (append-only).
	•	Feed the Security and Software Engineering scores into the OSF decision metric. If either security or engineering score falls below 0.7, the merge should be blocked unless there is a documented risk acceptance and mitigation plan. Each council recommendation should be neutral, precise, and actionable. Final decisions remain with human maintainers, but this process ensures diverse risk considerations are documented.

XLV. Resilience & Circuit Breakers (Mandatory)
	•	Circuit States: Implement circuit breakers for external dependencies with the standard states: CLOSED (normal operation, requests flow normally), OPEN (circuit tripped after failures, requests are immediately failed fast), and HALF-OPEN (test state where a few requests are allowed to probe if recovery occurred).
	•	Scope of Breakers: Define circuit breakers per critical dependency (not one global breaker). This includes external APIs (e.g., pricing or third-party data feeds), database operations (you may separate read vs write pools), and third-party services (payments, email, etc.), as well as any internal service calls that might be unreliable.
	•	Configuration: Document each breaker’s settings in /docs/Resilience.md. For each dependency, configure a failure rate threshold (e.g., 50% errors) over a rolling time window (e.g., 60 seconds) with a minimum number of requests (e.g., at least 20 calls) before it can trip. Set an open state duration (e.g., 60 seconds) after which the breaker enters HALF-OPEN to test the dependency. Limit the number of trial requests in half-open (e.g., 10 concurrent max), and require a success rate (e.g., 80% of those trials succeed) to close the circuit; otherwise re-open it.
	•	Timeouts & Retries: Apply client-side timeouts to calls (recommended ~1.5x the p95 latency of that service) and allow a limited number of quick retries (e.g., 1-2 retries with backoff and jitter) before counting the call as a failure. Use idempotency keys for any retried operations to avoid duplicate effects. Consider bulkhead isolation (separate threadpool or queue) for each dependency to prevent cascade failures.
	•	Fallbacks: Design fallback strategies for when a circuit is open. For example, serve cached data (possibly stale) or degrade functionality gracefully (return a friendly error or default response) rather than just an error.
	•	Telemetry & Alerts: Instrument metrics for each circuit breaker (e.g., gauge current state per dependency; counters for total failures, successes, rejected requests due to open circuit, and half-open trial outcomes). Set up alerts if a circuit remains open for extended periods or oscillates frequently, including context like which route or user actions are impacted (traceId, userID in logs).
	•	Testing: Include automated chaos testing in CI to simulate dependency failures and ensure the circuit breaker logic works as expected. These tests should verify that circuits open and close appropriately and that fallbacks engage. The CI should block merges if any critical resilience tests fail.
	•	Runbook Integration: In /docs/Runbook.md, provide instructions for operators to manually override or reset circuit breakers if needed during incidents. Also ensure /docs/Status_Report.md includes a snapshot of the current state or recent history of circuit statuses for visibility.
	•	Implementation: Prefer using well-established libraries or frameworks for circuit breaking if available (for correctness and reliability). Use safe default values if custom implementation is needed (e.g., 50% error threshold, 60s window, 60s open, 10 max half-open requests, 80% success to close, etc., as suggested above) as a starting point.