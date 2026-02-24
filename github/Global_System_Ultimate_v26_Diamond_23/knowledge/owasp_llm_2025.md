# 🛡️ OWASP Top 10 for LLM Applications (2025 Edition)

> **Standard**: Mandatory Compliance
> **Source**: OWASP Foundation

## 1. LLM01: Prompt Injection
**Risk:** Attackers manipulate LLM input to override instructions.
**Mitigation:**
*   Use **Delimiters** (XML tags) to separate data from instructions.
*   Use **Structured Output** (JSON) to prevent free-text leakage.
*   **Example:**
    ```python
    prompt = f"""
    Analyze the following text.
    <text>{user_input}</text>
    """
    ```

## 2. LLM02: Insecure Output Handling
**Risk:** LLM output is executed blindly (XSS, SQLi).
**Mitigation:**
*   Treat LLM output as **Untrusted User Input**.
*   Sanitize HTML/SQL before execution.
*   **Never** use `eval()` on LLM output.

## 3. LLM03: Training Data Poisoning
**Risk:** Malicious data in training set corrupts model behavior.
**Mitigation:**
*   Verify data provenance (SLSA).
*   Sanitize training datasets.

## 4. LLM04: Model Denial of Service
**Risk:** Resource exhaustion via expensive queries.
**Mitigation:**
*   Implement **Rate Limiting**.
*   Set **Context Window Limits**.
*   Use **Timeouts** for generation.

## 5. LLM05: Supply Chain Vulnerabilities
**Risk:** Compromised models, plugins, or libraries.
**Mitigation:**
*   Scan dependencies (Trivy, Socket.dev).
*   Sign containers (Cosign).
*   Use pinned versions (SHA).

## 6. LLM06: Sensitive Information Disclosure
**Risk:** LLM reveals PII or secrets.
**Mitigation:**
*   **PII Scrubbing** before prompt construction.
*   **Output Filtering** (Regex for SSN, Keys).

## 7. LLM07: Insecure Plugin Design
**Risk:** Plugins accept unvalidated input.
**Mitigation:**
*   Validate all plugin inputs against a schema (Pydantic).
*   Require **Human-in-the-Loop** for sensitive actions.

## 8. LLM08: Excessive Agency
**Risk:** LLM takes autonomous actions without oversight.
**Mitigation:**
*   **Least Privilege**: Grant only necessary permissions.
*   **Approval Gates**: Require confirmation for write/delete operations.

## 9. LLM09: Overreliance
**Risk:** Users trust LLM output blindly.
**Mitigation:**
*   **Citations**: Force model to cite sources.
*   **Disclaimers**: Clearly label AI-generated content.

## 10. LLM10: Model Theft
**Risk:** Unauthorized access or extraction of model weights.
**Mitigation:**
*   **Access Control**: RBAC for model APIs.
*   **Watermarking**: Embed watermarks in output.
