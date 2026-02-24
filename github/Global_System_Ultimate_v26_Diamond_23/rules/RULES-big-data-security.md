# Rule: Big Data Security (v26.0)

> **Status**: MANDATORY
> **Scope**: All Data Infrastructure, Pipelines, and Storage Systems
> **Compliance**: Global System Ultimate v26 Diamond 9

## 1. Data Encryption

### 1.1 At Rest
All storage systems (S3 buckets, HDFS, databases, vector databases) MUST use AES-256 encryption. Key management through AWS KMS, GCP KMS, or HashiCorp Vault — never self-managed keys stored in code or config files.

### 1.2 In Transit
All connections between services MUST use TLS 1.2+ (TLS 1.3 preferred). This includes: Spark cluster communication, Kafka brokers, JDBC connections, vector DB client connections (ChromaDB/Qdrant/Milvus), and all API endpoints. Self-signed certificates are only permitted in development environments.

### 1.3 ML-Specific Encryption
Model weights and training data must be encrypted at rest. Embeddings stored in vector databases must be in encrypted collections. GradCAM heatmaps and diagnostic reports containing patient/farmer data must be encrypted.

## 2. Access Control (RBAC)

### 2.1 Principle of Least Privilege
Every service, pipeline, and user account must have the minimum permissions required for its function. No shared admin accounts. Each pipeline job gets its own service account with scoped permissions.

### 2.2 Service Account Management
Service accounts must be rotated every 90 days. API keys must be rotated every 30 days. All credential rotation must be automated — manual rotation is a compliance violation.

### 2.3 Audit Logging
All data access must be logged with: who (user/service ID), what (operation type), when (timestamp), where (resource path), and outcome (success/failure). Audit logs must be retained for minimum 1 year and stored in a separate, tamper-evident system. Audit logs for ML model access must include model version and prediction metadata.

## 3. Network Security

### 3.1 Network Isolation
Data processing clusters must be isolated in private subnets with no public IP addresses. Access is only through VPN or bastion host with multi-factor authentication. Vector database services must not be exposed to the public internet.

### 3.2 Firewall Rules
Restrict inbound traffic to known CIDR blocks (VPN ranges, bastion hosts). Outbound traffic restricted to required services only (package registries, cloud APIs). All firewall changes require Security Engineer approval and are logged.

### 3.3 Secret Management
Secrets (passwords, API keys, tokens, certificates) must NEVER appear in: source code, CI/CD configuration files, environment variable files committed to git, log output, or error messages. Use HashiCorp Vault, AWS Secrets Manager, or equivalent. Reference secrets by name/path, never by value.

## 4. Data Pipeline Security

### 4.1 Input Validation
All data entering the pipeline must be validated: image files checked for polyglot attacks (malicious payloads hidden in image metadata), CSV/JSON inputs sanitized against injection attacks, file sizes validated against expected ranges.

### 4.2 Pipeline Isolation
Each pipeline stage runs in its own isolated container or process. A failure in one stage must not compromise data in other stages. Staging environment data must never contain production PII.

## 5. Compliance

### 5.1 Data Privacy (GDPR/CCPA)
Implement “Right to be Forgotten” — ability to delete all user data on request within 30 days. This includes: raw images, processed features, embeddings in vector DB, GradCAM outputs, and prediction logs. Data masking must be applied to PII (emails, phone numbers, GPS coordinates) in all non-production environments.

### 5.2 Data Retention
Raw images retained for 2 years (agricultural research compliance). Processed features and embeddings retained for 1 year or until model retirement. Audit logs retained for 1 year minimum. Expired data must be automatically purged via scheduled jobs.

## 6. Cross-References

-   **Embedding Storage**: `rules/ml/RULES-embedding-storage.md` — vector DB security configuration.
-   **Security Engineer**: `roles/ROLE-security-engineer.md` — responsible for security implementation.
-   **Security Auditor**: `roles/ROLE-security-auditor.md` — responsible for compliance auditing.
-   **DevOps**: `roles/ROLE-devops-engineer.md` — responsible for infrastructure security.
