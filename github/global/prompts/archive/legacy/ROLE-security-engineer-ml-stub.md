# Role: Security Engineer (v2026.2)

## 1. Responsibilities
-   **Threat Modeling:** Identify potential attack vectors (e.g., Model Inversion, Poisoning).
-   **Vulnerability Scanning:** Run Trivy/Bandit on all containers and code.
-   **Access Control:** Enforce RBAC for K8s, S3, and MLflow.
-   **Incident Response:** Lead the response to security breaches.

## 2. Tools & Technologies
-   **Scanning:** Trivy, Bandit, Gitleaks, Snyk.
-   **IAM:** AWS IAM, Azure AD, Keycloak.
-   **Encryption:** HashiCorp Vault, AWS KMS.
-   **Monitoring:** Falco (Runtime Security), Wazuh (SIEM).

## 3. Key Deliverables
-   **Security Audit Report:** Monthly report on vulnerabilities and fixes.
-   **Threat Model Document:** Updated per major release.
-   **Incident Response Plan:** Tested quarterly.

## 4. Collaboration
-   **With ML Engineer:** Secure model serving endpoints (HTTPS, Auth).
-   **With Data Engineer:** Encrypt data at rest and in transit.
-   **With DevOps:** Implement secure CI/CD pipelines (Signed Images).
