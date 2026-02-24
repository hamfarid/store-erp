# Security Policy (Global System Ultimate)

## 1. Universal Governance (Layer 1)
*   **Mandate:** Security practices must align with `AGENTS.md`.
*   **Agent Verification:** Kilo and Kiro configurations must be secure by default.

## 2. Authentication & Authorization
*   **JWT:** Short-lived (15m), signed with HS256/RS256.
*   **Cookies:** HttpOnly, Secure, SameSite=Strict.
*   **Passwords:** Hashed with Argon2 or bcrypt (work factor 12+).

## 3. Data Protection
*   **Encryption:** AES-256-GCM for sensitive data at rest.
*   **Transport:** TLS 1.3 for all communications.
*   **Secrets:** Never committed to Git. Use `.env` or Vault.
*   **Sentinel Check:** `tools/preflight_check.py` must verify no secrets are exposed.

## 4. Input Validation
*   **Sanitization:** All user input is untrusted.
*   **Validation:** Pydantic (Python) / Zod (TypeScript) for strict schemas.
*   **SQL Injection:** Use ORM or parameterized queries only.

## 5. Vulnerability Management
*   **Dependencies:** Scan weekly with `pip-audit` / `npm audit`.
*   **Code:** Static analysis with Bandit (Python) / ESLint Security (JS).
*   **Reporting:** Critical vulnerabilities must be patched within 24 hours.

## 6. 5-Layer Defense Integration
*   **Layer 2 (Source Grounding):** Verify security libraries exist before use.
*   **Layer 5 (Tool Verification):** Use `tools/preflight_check.py` to audit security configs.

---

# 🛡️ Secure AI Framework (SAIF 2.0) Principles

> **Standard**: Secure AI Framework (SAIF) 2.0 (Google/Industry Standard)
> **Goal**: Ensure AI systems are secure by design, default, and deployment.

## 1. Secure the AI Supply Chain
*   **Principle**: Know your ingredients.
*   **Action**: Maintain a Software Bill of Materials (SBOM) for all models, datasets, and libraries.
*   **Tool**: Use `syft` or `trivy` to scan dependencies.

## 2. Extend Security Controls to AI
*   **Principle**: Treat AI like any other software component.
*   **Action**: Apply existing security controls (IAM, encryption, logging) to AI infrastructure.
*   **Tool**: Integrate with existing SIEM/SOAR platforms.

## 3. Detect & Respond to AI Threats
*   **Principle**: Assume breach.
*   **Action**: Monitor for adversarial attacks (prompt injection, model theft).
*   **Tool**: Use specialized AI threat detection (e.g., HiddenLayer, Protect AI).

## 4. Automate Defenses
*   **Principle**: Speed beats perfection.
*   **Action**: Use AI to defend AI. Automate vulnerability scanning and patching.
*   **Tool**: Automated red-teaming (e.g., Garak, PyRIT).

## 5. Harmonize Controls
*   **Principle**: Consistency is key.
*   **Action**: Align AI security controls with organizational policies and compliance standards (NIST AI RMF, ISO 42001).
*   **Tool**: Compliance automation platforms (e.g., Drata, Vanta).

## 6. Context-Aware Security
*   **Principle**: Context matters.
*   **Action**: Adjust security controls based on the sensitivity of the data and the impact of the AI system.
*   **Tool**: Data classification and DLP tools.

## 7. Human-Centric Security
*   **Principle**: People are the perimeter.
*   **Action**: Train developers and users on AI security risks and best practices.
*   **Tool**: Security awareness training and phishing simulations.

## 8. Resilience & Recovery
*   **Principle**: Bounce back stronger.
*   **Action**: Design AI systems to be resilient to attacks and failures.
*   **Tool**: Chaos engineering and disaster recovery planning.

## 9. Transparency & Accountability
*   **Principle**: Trust but verify.
*   **Action**: Document model behavior, limitations, and security controls.
*   **Tool**: Model cards and system cards.

## 10. Continuous Improvement
*   **Principle**: Security is a journey, not a destination.
*   **Action**: Regularly review and update security policies and controls.
*   **Tool**: Post-incident reviews and lessons learned.

---

## 🤖 Agent-Specific SAIF Principles (Research 2026)
1.  **Accountability**: Agents must have well-defined human controllers. (See `knowledge/protocols/approval_gates.md`)
2.  **Least Privilege**: Agent powers must be carefully limited. (See `rules/mcp_security.md`)
3.  **Observability**: Agent actions must be observable. (See `system_log.md` and Audit Trails)
